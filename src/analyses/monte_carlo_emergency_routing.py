#!/usr/bin/env python3
"""Compact repeated-routing engine for Monte Carlo road-failure experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


ROAD_COLUMNS = [
    "Road Edge ID",
    "Road Section ID",
    "From Node ID",
    "To Node ID",
    "Baseline Edge Travel Time (min)",
    "Assumed Speed (km/h)",
    "Road Available",
    "Network Analysis Eligible",
]


@dataclass(frozen=True)
class EmergencyStateResult:
    """Demand-level travel times and compact system diagnostics for one state."""

    dispatch_time: np.ndarray
    hospital_time: np.ndarray
    total_time: np.ndarray
    assigned_hospital_index: np.ndarray | None
    routing_seconds: float


@dataclass
class CompactEmergencyNetwork:
    """Fixed sparse topology whose edge weights can be masked by road section."""

    road_section_ids: np.ndarray
    demand_ids: np.ndarray
    demand_population: np.ndarray
    demand_older_population: np.ndarray
    demand_type: np.ndarray
    demand_node_index: np.ndarray
    graph: csr_matrix
    arc_base_weight: np.ndarray
    arc_road_section: np.ndarray
    arc_group_starts: np.ndarray
    dispatch_super_index: int
    hospital_super_index: int
    dispatch_source_indices: np.ndarray
    hospital_source_indices: np.ndarray
    hospital_ids: np.ndarray
    hospital_index_by_node: np.ndarray
    build_seconds: float

    @property
    def road_section_count(self) -> int:
        return int(len(self.road_section_ids))

    @property
    def node_count(self) -> int:
        return int(self.graph.shape[0])

    @property
    def directed_pair_count(self) -> int:
        return int(self.graph.nnz)

    def route(
        self,
        failed: np.ndarray | None = None,
        assign_hospitals: bool = False,
    ) -> EmergencyStateResult:
        """Compute the complete dispatch-to-demand-to-hospital chain for one state."""
        if failed is None:
            failed = np.zeros(self.road_section_count, dtype=bool)
        failed = np.asarray(failed, dtype=bool)
        if failed.shape != (self.road_section_count,):
            raise ValueError(
                f"Expected failure mask shape {(self.road_section_count,)}, got {failed.shape}"
            )

        started = perf_counter()
        available_arc = self.arc_road_section < 0
        road_arc = ~available_arc
        available_arc[road_arc] = ~failed[self.arc_road_section[road_arc]]
        candidate_weight = np.where(available_arc, self.arc_base_weight, np.inf)
        self.graph.data[:] = np.minimum.reduceat(
            candidate_weight,
            self.arc_group_starts,
        )

        dispatch_distance = dijkstra(
            self.graph,
            directed=True,
            indices=self.dispatch_source_indices,
            return_predecessors=False,
            min_only=True,
        )
        hospital_sources = None
        if assign_hospitals:
            hospital_distance, _, hospital_sources = dijkstra(
                self.graph,
                directed=True,
                indices=self.hospital_source_indices,
                return_predecessors=True,
                min_only=True,
            )
        else:
            hospital_distance = dijkstra(
                self.graph,
                directed=True,
                indices=self.hospital_source_indices,
                return_predecessors=False,
                min_only=True,
            )

        valid = self.demand_node_index >= 0
        dispatch_time = np.full(len(self.demand_node_index), np.inf, dtype=np.float64)
        hospital_time = np.full(len(self.demand_node_index), np.inf, dtype=np.float64)
        dispatch_time[valid] = dispatch_distance[self.demand_node_index[valid]]
        hospital_time[valid] = hospital_distance[self.demand_node_index[valid]]
        total_time = dispatch_time + hospital_time
        assigned_hospital_index = None
        if hospital_sources is not None:
            assigned_hospital_index = np.full(
                len(self.demand_node_index), -1, dtype=np.int16
            )
            demand_sources = hospital_sources[self.demand_node_index[valid]]
            source_valid = demand_sources >= 0
            valid_positions = np.flatnonzero(valid)
            assigned_hospital_index[valid_positions[source_valid]] = (
                self.hospital_index_by_node[demand_sources[source_valid]]
            )
        return EmergencyStateResult(
            dispatch_time=dispatch_time,
            hospital_time=hospital_time,
            total_time=total_time,
            assigned_hospital_index=assigned_hospital_index,
            routing_seconds=perf_counter() - started,
        )


def _accepted_connectors(
    frame: pd.DataFrame,
    identifier: str,
    eligibility: str | None,
    connector_type: str,
) -> pd.DataFrame:
    """Return valid connectors using a shared compact schema."""
    selected = frame.loc[frame["Network Snap Accepted"].fillna(False)].copy()
    if eligibility is not None:
        selected = selected.loc[selected[eligibility].fillna(False)].copy()
    selected = selected.loc[selected[identifier].notna()].copy()
    return selected.rename(columns={identifier: "Connector ID"}).assign(
        **{"Connector Type": connector_type}
    )[
        [
            "Connector ID",
            "Connector Type",
            "Access Road Edge ID",
            "Access Edge Fraction",
            "Network Snap Distance (m)",
        ]
    ]


def _append_undirected(
    arc_from: list[int],
    arc_to: list[int],
    arc_weight: list[float],
    arc_failure: list[int],
    start: int,
    end: int,
    weight: float,
    road_section: int,
) -> None:
    """Append both directions of one nonnegative graph connection."""
    if weight < 0 or not np.isfinite(weight):
        raise ValueError(f"Invalid edge weight: {weight}")
    arc_from.extend((start, end))
    arc_to.extend((end, start))
    arc_weight.extend((weight, weight))
    arc_failure.extend((road_section, road_section))


def build_compact_emergency_network(
    processed: Path,
    include_population_groups: bool = False,
) -> CompactEmergencyNetwork:
    """Build a reusable sparse graph with road-section-labelled directed arcs."""
    started = perf_counter()
    edges = pd.read_parquet(
        processed / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=ROAD_COLUMNS,
    )
    eligible = edges["Road Available"].fillna(False) & edges[
        "Network Analysis Eligible"
    ].fillna(False)
    edges = edges.loc[eligible].reset_index(drop=True)
    if not edges["Road Edge ID"].is_unique:
        raise ValueError("Road Edge ID must be unique")
    road_section_ids = np.sort(edges["Road Section ID"].astype(str).unique())
    section_index_by_id = pd.Series(
        np.arange(len(road_section_ids), dtype=np.int32),
        index=road_section_ids,
    )
    edge_section_index = (
        edges["Road Section ID"].astype(str).map(section_index_by_id).to_numpy(np.int32)
    )
    edge_index_by_id = pd.Series(
        np.arange(len(edges), dtype=np.int32),
        index=edges["Road Edge ID"].astype(str),
    )
    speed_by_edge = pd.Series(
        edges["Assumed Speed (km/h)"].to_numpy(dtype=np.float64),
        index=edges["Road Edge ID"].astype(str),
    )

    demand = pd.read_parquet(
        processed / "kumamoto_population_mesh_network_access_preprocessed.parquet",
        columns=[
            "Demand Node ID",
            "Total Population",
            "Network Snap Distance (m)",
            "Network Snap Accepted",
            "Access Road Edge ID",
            "Access Edge Fraction",
        ],
    )
    demand["Older Population Weight"] = 0.0
    demand["Demand Type"] = "population_mesh"
    if include_population_groups:
        older_demand = pd.read_parquet(
            processed / "kumamoto_population_group_network_access_preprocessed.parquet",
            columns=[
                "Demand Node ID",
                "Population Age 65+",
                "Network Snap Distance (m)",
                "Network Snap Accepted",
                "Access Road Edge ID",
                "Access Edge Fraction",
            ],
        ).rename(columns={"Population Age 65+": "Older Population Weight"})
        older_demand["Total Population"] = 0.0
        older_demand["Demand Type"] = "older_population_group"
        demand = pd.concat([demand, older_demand], ignore_index=True)
    dispatch = pd.read_parquet(
        processed / "kumamoto_dispatch_base_network_access_preprocessed.parquet",
        columns=[
            "Dispatch Base Node ID",
            "Candidate Dispatch Base",
            "Network Snap Distance (m)",
            "Network Snap Accepted",
            "Access Road Edge ID",
            "Access Edge Fraction",
        ],
    )
    hospitals = pd.read_parquet(
        processed / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=[
            "Hospital Node ID",
            "Eligible Emergency Hospital",
            "Network Snap Distance (m)",
            "Network Snap Accepted",
            "Access Road Edge ID",
            "Access Edge Fraction",
        ],
    )
    connectors = pd.concat(
        [
            _accepted_connectors(demand, "Demand Node ID", None, "demand"),
            _accepted_connectors(
                dispatch,
                "Dispatch Base Node ID",
                "Candidate Dispatch Base",
                "dispatch",
            ),
            _accepted_connectors(
                hospitals,
                "Hospital Node ID",
                "Eligible Emergency Hospital",
                "hospital",
            ),
        ],
        ignore_index=True,
    )
    connectors["Connector ID"] = connectors["Connector ID"].astype(str)
    connectors["Access Road Edge ID"] = connectors["Access Road Edge ID"].astype(str)
    if not connectors["Connector ID"].is_unique:
        duplicates = connectors.loc[
            connectors["Connector ID"].duplicated(False), "Connector ID"
        ].head().tolist()
        raise ValueError(f"Connector IDs must be globally unique: {duplicates}")
    missing_edge = ~connectors["Access Road Edge ID"].isin(edge_index_by_id.index)
    if missing_edge.any():
        raise ValueError(
            f"{int(missing_edge.sum())} accepted connectors reference ineligible road edges"
        )
    connectors["Edge Index"] = connectors["Access Road Edge ID"].map(
        edge_index_by_id
    ).astype(np.int32)
    connectors["Road Section Index"] = edge_section_index[
        connectors["Edge Index"].to_numpy(np.int32)
    ]
    connectors["Assumed Speed (km/h)"] = connectors["Access Road Edge ID"].map(
        speed_by_edge
    ).astype(float)
    connectors["Access Edge Fraction"] = (
        connectors["Access Edge Fraction"].astype(float).clip(0.0, 1.0)
    )
    connectors["Connector Time (min)"] = (
        60.0
        * connectors["Network Snap Distance (m)"].astype(float)
        / (1_000.0 * connectors["Assumed Speed (km/h)"])
    )

    road_node_ids = pd.Index(
        pd.concat(
            [edges["From Node ID"], edges["To Node ID"]],
            ignore_index=True,
        ).astype(str).unique()
    )
    road_node_index = pd.Series(
        np.arange(len(road_node_ids), dtype=np.int32),
        index=road_node_ids,
    )
    from_index = edges["From Node ID"].astype(str).map(road_node_index).to_numpy(np.int32)
    to_index = edges["To Node ID"].astype(str).map(road_node_index).to_numpy(np.int32)
    edge_minutes = edges["Baseline Edge Travel Time (min)"].to_numpy(np.float64)

    connector_start = len(road_node_ids)
    connectors["Connector Node Index"] = np.arange(
        connector_start,
        connector_start + len(connectors),
        dtype=np.int32,
    )
    connector_node_by_id = pd.Series(
        connectors["Connector Node Index"].to_numpy(np.int32),
        index=connectors["Connector ID"],
    )

    arc_from: list[int] = []
    arc_to: list[int] = []
    arc_weight: list[float] = []
    arc_failure: list[int] = []
    next_node = connector_start + len(connectors)

    connectors_by_edge = {
        int(edge_position): group.sort_values(
            ["Access Edge Fraction", "Connector ID"], kind="stable"
        )
        for edge_position, group in connectors.groupby("Edge Index", sort=False)
    }
    connector_edges = np.fromiter(
        connectors_by_edge.keys(),
        dtype=np.int32,
        count=len(connectors_by_edge),
    )
    no_connector = np.ones(len(edges), dtype=bool)
    no_connector[connector_edges] = False
    for edge_position in np.flatnonzero(no_connector):
        _append_undirected(
            arc_from,
            arc_to,
            arc_weight,
            arc_failure,
            int(from_index[edge_position]),
            int(to_index[edge_position]),
            float(edge_minutes[edge_position]),
            int(edge_section_index[edge_position]),
        )

    for edge_position, group in connectors_by_edge.items():
        section_index = int(edge_section_index[edge_position])
        fractions = np.sort(group["Access Edge Fraction"].unique().astype(float))
        position_node: dict[float, int] = {
            0.0: int(from_index[edge_position]),
            1.0: int(to_index[edge_position]),
        }
        for fraction in fractions:
            if 0.0 < fraction < 1.0:
                position_node[float(fraction)] = next_node
                next_node += 1
        chain_fractions = np.concatenate(([0.0], fractions[(fractions > 0) & (fractions < 1)], [1.0]))
        for start_fraction, end_fraction in zip(
            chain_fractions[:-1], chain_fractions[1:], strict=True
        ):
            _append_undirected(
                arc_from,
                arc_to,
                arc_weight,
                arc_failure,
                position_node[float(start_fraction)],
                position_node[float(end_fraction)],
                float(edge_minutes[edge_position] * (end_fraction - start_fraction)),
                section_index,
            )
        for connector_node, fraction, connector_minutes in group[
            [
                "Connector Node Index",
                "Access Edge Fraction",
                "Connector Time (min)",
            ]
        ].itertuples(index=False, name=None):
            _append_undirected(
                arc_from,
                arc_to,
                arc_weight,
                arc_failure,
                int(connector_node),
                position_node[fraction],
                float(connector_minutes),
                section_index,
            )

    dispatch_sources = connectors.loc[
        connectors["Connector Type"].eq("dispatch"), "Connector Node Index"
    ].to_numpy(np.int32)
    hospital_connector_rows = connectors.loc[
        connectors["Connector Type"].eq("hospital"),
        ["Connector ID", "Connector Node Index"],
    ].reset_index(drop=True)
    hospital_sources = hospital_connector_rows["Connector Node Index"].to_numpy(np.int32)
    if not len(dispatch_sources):
        raise ValueError("No accepted dispatch connectors")
    if not len(hospital_sources):
        raise ValueError("No accepted hospital connectors")

    dispatch_super_index = next_node
    hospital_super_index = next_node + 1
    node_count = next_node + 2
    for sources, super_index in (
        (dispatch_sources, dispatch_super_index),
        (hospital_sources, hospital_super_index),
    ):
        arc_from.extend([super_index] * len(sources))
        arc_to.extend(sources.tolist())
        arc_weight.extend([0.0] * len(sources))
        arc_failure.extend([-1] * len(sources))

    arc_from_array = np.asarray(arc_from, dtype=np.int32)
    arc_to_array = np.asarray(arc_to, dtype=np.int32)
    arc_weight_array = np.asarray(arc_weight, dtype=np.float64)
    arc_failure_array = np.asarray(arc_failure, dtype=np.int32)
    pair_key = arc_from_array.astype(np.int64) * np.int64(node_count) + arc_to_array
    order = np.argsort(pair_key, kind="stable")
    pair_key = pair_key[order]
    arc_from_array = arc_from_array[order]
    arc_to_array = arc_to_array[order]
    arc_weight_array = arc_weight_array[order]
    arc_failure_array = arc_failure_array[order]
    group_starts = np.flatnonzero(
        np.r_[True, pair_key[1:] != pair_key[:-1]]
    ).astype(np.int64)
    unique_from = arc_from_array[group_starts]
    unique_to = arc_to_array[group_starts]
    base_pair_weight = np.minimum.reduceat(arc_weight_array, group_starts)
    row_counts = np.bincount(unique_from, minlength=node_count)
    indptr = np.empty(node_count + 1, dtype=np.int64)
    indptr[0] = 0
    np.cumsum(row_counts, out=indptr[1:])
    graph = csr_matrix(
        (base_pair_weight.copy(), unique_to, indptr),
        shape=(node_count, node_count),
    )
    hospital_index_by_node = np.full(node_count, -1, dtype=np.int16)
    hospital_index_by_node[hospital_sources] = np.arange(
        len(hospital_sources), dtype=np.int16
    )

    demand_ids = demand["Demand Node ID"].astype("string").fillna("").astype(str).to_numpy()
    demand_node_index = np.full(len(demand), -1, dtype=np.int32)
    demand_valid = demand["Demand Node ID"].notna() & demand[
        "Network Snap Accepted"
    ].fillna(False)
    demand_node_index[demand_valid.to_numpy()] = (
        demand.loc[demand_valid, "Demand Node ID"]
        .astype(str)
        .map(connector_node_by_id)
        .to_numpy(np.int32)
    )

    return CompactEmergencyNetwork(
        road_section_ids=road_section_ids,
        demand_ids=demand_ids,
        demand_population=demand["Total Population"].fillna(0).to_numpy(np.float64),
        demand_older_population=demand["Older Population Weight"].fillna(0).to_numpy(np.float64),
        demand_type=demand["Demand Type"].astype(str).to_numpy(),
        demand_node_index=demand_node_index,
        graph=graph,
        arc_base_weight=arc_weight_array,
        arc_road_section=arc_failure_array,
        arc_group_starts=group_starts,
        dispatch_super_index=dispatch_super_index,
        hospital_super_index=hospital_super_index,
        dispatch_source_indices=dispatch_sources,
        hospital_source_indices=hospital_sources,
        hospital_ids=hospital_connector_rows["Connector ID"].astype(str).to_numpy(),
        hospital_index_by_node=hospital_index_by_node,
        build_seconds=perf_counter() - started,
    )


def summarize_state(
    network: CompactEmergencyNetwork,
    result: EmergencyStateResult,
    failure_rate: float,
    failed_units: int,
) -> dict[str, float | int]:
    """Summarize population coverage and computation time for one network state."""
    finite = np.isfinite(result.total_time)
    population = network.demand_population
    summary: dict[str, float | int] = {
        "failure_rate": float(failure_rate),
        "failed_units": int(failed_units),
        "finite_demand_units": int(finite.sum()),
        "finite_population": int(population[finite].sum()),
        "routing_seconds": round(float(result.routing_seconds), 6),
    }
    for threshold in (15, 30, 45):
        timely = result.total_time <= threshold
        summary[f"population_within_{threshold}_minutes"] = int(population[timely].sum())
    return summary
