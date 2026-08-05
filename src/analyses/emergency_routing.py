#!/usr/bin/env python3
"""Shared routing utilities for the Kumamoto two-stage emergency-access analysis."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class EmergencyAccessResult:
    """Scenario-specific travel times and validation diagnostics."""

    demand: pd.DataFrame
    diagnostics: dict[str, float | int]


@dataclass(frozen=True)
class HospitalCatchmentResult:
    """Scenario-specific hospital assignment, redundancy, and diagnostics."""

    demand: pd.DataFrame
    hospitals: pd.DataFrame
    diagnostics: dict[str, float | int]


def _add_minimum_edge(graph: nx.Graph, start: str, end: str, minutes: float) -> None:
    """Add an undirected edge, retaining the fastest parallel connection."""
    if graph.has_edge(start, end):
        if minutes < float(graph[start][end]["minutes"]):
            graph[start][end]["minutes"] = minutes
    else:
        graph.add_edge(start, end, minutes=minutes)


def _accepted_connectors(
    frame: pd.DataFrame,
    identifier: str,
    eligibility: str | None,
    connector_type: str,
) -> pd.DataFrame:
    """Return accepted external connectors with a common schema."""
    selected = frame.loc[frame["Network Snap Accepted"]].copy()
    if eligibility is not None:
        selected = selected.loc[selected[eligibility]].copy()
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


def _build_augmented_graph(
    edges: pd.DataFrame,
    connectors: pd.DataFrame,
) -> nx.Graph:
    """Split road edges at access positions and attach external connector nodes."""
    edge_lookup = edges.set_index("Road Edge ID")
    connectors = connectors.loc[
        connectors["Access Road Edge ID"].isin(edge_lookup.index)
    ].copy()
    connectors = connectors.join(
        edge_lookup[["Assumed Speed (km/h)"]],
        on="Access Road Edge ID",
        validate="many_to_one",
    )
    if connectors["Assumed Speed (km/h)"].isna().any():
        raise ValueError("A connector references a road edge absent from the baseline graph")

    connectors = connectors.copy()
    connectors["Access Edge Fraction"] = connectors["Access Edge Fraction"].astype(float).clip(0.0, 1.0)
    connectors["Connector Time (min)"] = (
        60.0
        * connectors["Network Snap Distance (m)"].astype(float)
        / (1_000.0 * connectors["Assumed Speed (km/h)"].astype(float))
    )

    access_by_edge: dict[str, pd.DataFrame] = {
        str(edge_id): group.sort_values(["Access Edge Fraction", "Connector ID"], kind="stable")
        for edge_id, group in connectors.groupby("Access Road Edge ID", sort=False)
    }
    graph = nx.Graph()

    for row in edges.itertuples(index=False):
        edge_id = str(getattr(row, "_0"))
        from_node = str(getattr(row, "_1"))
        to_node = str(getattr(row, "_2"))
        edge_minutes = float(getattr(row, "_3"))
        access = access_by_edge.get(edge_id)
        if access is None:
            _add_minimum_edge(graph, from_node, to_node, edge_minutes)
            continue

        positions = access["Access Edge Fraction"].drop_duplicates().sort_values().tolist()
        chain_nodes = [from_node]
        chain_fractions = [0.0]
        for position_number, fraction in enumerate(positions, start=1):
            chain_nodes.append(f"SNAP::{edge_id}::{position_number:05d}")
            chain_fractions.append(float(fraction))
        chain_nodes.append(to_node)
        chain_fractions.append(1.0)
        for start, end, start_fraction, end_fraction in zip(
            chain_nodes[:-1],
            chain_nodes[1:],
            chain_fractions[:-1],
            chain_fractions[1:],
            strict=True,
        ):
            _add_minimum_edge(graph, start, end, edge_minutes * (end_fraction - start_fraction))

        snap_for_fraction = dict(zip(positions, chain_nodes[1:-1], strict=True))
        for connector in access.itertuples(index=False):
            connector_id = str(getattr(connector, "_0"))
            fraction = float(getattr(connector, "_3"))
            connector_minutes = float(getattr(connector, "_6"))
            _add_minimum_edge(
                graph,
                connector_id,
                snap_for_fraction[fraction],
                connector_minutes,
            )

    return graph


def _labelled_multi_source_distances(
    graph: nx.Graph,
    sources: list[str],
) -> tuple[dict[str, float], dict[str, str]]:
    """Return nearest-source distances and deterministic source labels."""
    distances: dict[str, float] = {}
    labels: dict[str, str] = {}
    queue: list[tuple[float, str, str]] = []
    for source in sorted(set(sources)):
        distances[source] = 0.0
        labels[source] = source
        heapq.heappush(queue, (0.0, source, source))

    tolerance = 1e-12
    while queue:
        distance, source, node = heapq.heappop(queue)
        current_distance = distances.get(node, np.inf)
        current_source = labels.get(node)
        if distance > current_distance + tolerance:
            continue
        if abs(distance - current_distance) <= tolerance and current_source != source:
            continue
        for neighbour, attributes in graph[node].items():
            candidate = distance + float(attributes["minutes"])
            known = distances.get(neighbour, np.inf)
            known_source = labels.get(neighbour)
            shorter = candidate < known - tolerance
            tied_better_source = (
                abs(candidate - known) <= tolerance
                and (known_source is None or source < known_source)
            )
            if shorter or tied_better_source:
                distances[neighbour] = candidate
                labels[neighbour] = source
                heapq.heappush(queue, (candidate, source, neighbour))
    return distances, labels


def scenario_availability_mask(edges: pd.DataFrame, scenario: str) -> pd.Series:
    """Return the AnaSOP Section 5 nested road-availability rule."""
    scenario_key = scenario.casefold()
    available = edges["Road Available"].fillna(False) & edges["Network Analysis Eligible"].fillna(False)
    hazard = edges["Hazard Exposure Class"].astype("string")
    road_state = edges["Road State"].astype("string")
    if scenario_key == "baseline":
        return available
    if scenario_key == "low":
        return available & ~hazard.eq("Special Warning Zone")
    if scenario_key == "central":
        return available & ~hazard.isin(["Warning Zone", "Special Warning Zone"])
    if scenario_key == "high":
        disrupted = hazard.isin(["Warning Zone", "Special Warning Zone"]) | road_state.isin(
            ["Bridge or Elevated", "Tunnel"]
        )
        return available & ~disrupted
    raise ValueError(f"Unknown disruption scenario: {scenario}")


def _load_demand(processed: Path, demand_support: str) -> pd.DataFrame:
    """Load mesh, disclosure-group, or combined demand connectors."""
    connector_columns = [
        "Analysis Unit ID",
        "Demand Node ID",
        "Total Population",
        "Network Snap Distance (m)",
        "Network Snap Accepted",
        "Access Road Edge ID",
        "Access Edge Fraction",
    ]
    support_key = demand_support.casefold()
    frames: list[pd.DataFrame] = []
    if support_key in {"mesh", "combined"}:
        mesh = pd.read_parquet(
            processed / "kumamoto_population_mesh_network_access_preprocessed.parquet",
            columns=["Mesh Code", *connector_columns],
        )
        mesh["Demand Support"] = "mesh"
        frames.append(mesh)
    if support_key in {"group", "combined"}:
        group = pd.read_parquet(
            processed / "kumamoto_population_group_network_access_preprocessed.parquet",
            columns=[
                "Disclosure Group Code",
                "Population Age 65+",
                "Population Age 75+",
                "Population Age 85+",
                *connector_columns,
            ],
        )
        group["Demand Support"] = "group"
        frames.append(group)
    if not frames:
        raise ValueError(f"Unknown demand support: {demand_support}")
    return pd.concat(frames, ignore_index=True, sort=False)


def compute_emergency_access(
    processed: Path,
    scenario: str = "Baseline",
    demand_support: str = "mesh",
) -> EmergencyAccessResult:
    """Compute dispatch, hospital, and total two-stage travel times for one scenario."""
    edge_columns = [
        "Road Edge ID",
        "From Node ID",
        "To Node ID",
        "Baseline Edge Travel Time (min)",
        "Assumed Speed (km/h)",
        "Road Available",
        "Network Analysis Eligible",
        "Hazard Exposure Class",
        "Road State",
    ]
    edges = pd.read_parquet(
        processed / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=edge_columns,
    )
    all_eligible_edges = int(edges["Network Analysis Eligible"].fillna(False).sum())
    edges = edges.loc[scenario_availability_mask(edges, scenario)].copy()

    demand = _load_demand(processed, demand_support)
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

    demand_connectors = _accepted_connectors(demand, "Demand Node ID", None, "demand")
    dispatch_connectors = _accepted_connectors(
        dispatch, "Dispatch Base Node ID", "Candidate Dispatch Base", "dispatch"
    )
    hospital_connectors = _accepted_connectors(
        hospitals, "Hospital Node ID", "Eligible Emergency Hospital", "hospital"
    )
    connectors = pd.concat(
        [demand_connectors, dispatch_connectors, hospital_connectors],
        ignore_index=True,
    )

    graph_edges = edges[
        [
            "Road Edge ID",
            "From Node ID",
            "To Node ID",
            "Baseline Edge Travel Time (min)",
            "Assumed Speed (km/h)",
        ]
    ].copy()
    graph = _build_augmented_graph(graph_edges, connectors)

    dispatch_sources = [
        identifier
        for identifier in dispatch_connectors["Connector ID"].astype(str)
        if identifier in graph
    ]
    hospital_sources = [
        identifier
        for identifier in hospital_connectors["Connector ID"].astype(str)
        if identifier in graph
    ]
    if not dispatch_sources:
        raise ValueError(f"No dispatch bases remain connected in the {scenario} scenario")
    if not hospital_sources:
        raise ValueError(f"No hospitals remain connected in the {scenario} scenario")
    dispatch_distance = nx.multi_source_dijkstra_path_length(
        graph, dispatch_sources, weight="minutes"
    )
    hospital_distance = nx.multi_source_dijkstra_path_length(
        graph, hospital_sources, weight="minutes"
    )

    result = demand.copy()
    demand_ids = result["Demand Node ID"].astype("string")
    result["Dispatch Travel Time"] = demand_ids.map(dispatch_distance).astype(float)
    result["Hospital Transport Time"] = demand_ids.map(hospital_distance).astype(float)
    result["Total Emergency Access Time"] = (
        result["Dispatch Travel Time"] + result["Hospital Transport Time"]
    )

    population = result["Total Population"].astype(float)
    snapped = result["Network Snap Accepted"].fillna(False)
    finite_dispatch = np.isfinite(result["Dispatch Travel Time"])
    finite_hospital = np.isfinite(result["Hospital Transport Time"])
    finite_total = np.isfinite(result["Total Emergency Access Time"])
    diagnostics: dict[str, float | int] = {
        "eligible_road_edges": all_eligible_edges,
        "available_road_edges": int(len(edges)),
        "unavailable_road_edges": int(all_eligible_edges - len(edges)),
        "graph_nodes": int(graph.number_of_nodes()),
        "graph_edges": int(graph.number_of_edges()),
        "dispatch_bases": int(len(dispatch_sources)),
        "hospitals": int(len(hospital_sources)),
        "demand_units": int(len(result)),
        "total_population": int(population.sum()),
        "failed_snap_units": int((~snapped).sum()),
        "failed_snap_population": int(population.loc[~snapped].sum()),
        "finite_dispatch_population": int(population.loc[finite_dispatch].sum()),
        "finite_hospital_population": int(population.loc[finite_hospital].sum()),
        "finite_total_population": int(population.loc[finite_total].sum()),
    }
    return EmergencyAccessResult(demand=result, diagnostics=diagnostics)


def compute_hospital_catchment_access(
    processed: Path,
    scenario: str = "Baseline",
    threshold: float = 30.0,
    compute_alternatives: bool = False,
) -> HospitalCatchmentResult:
    """Compute mesh-level hospital assignment and optional timely alternatives."""
    edge_columns = [
        "Road Edge ID",
        "From Node ID",
        "To Node ID",
        "Baseline Edge Travel Time (min)",
        "Assumed Speed (km/h)",
        "Road Available",
        "Network Analysis Eligible",
        "Hazard Exposure Class",
        "Road State",
    ]
    all_edges = pd.read_parquet(
        processed / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=edge_columns,
    )
    all_eligible_edges = int(all_edges["Network Analysis Eligible"].fillna(False).sum())
    edges = all_edges.loc[scenario_availability_mask(all_edges, scenario)].copy()

    demand = _load_demand(processed, "mesh")
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
            "Facility Name",
            "Bed Count",
            "Eligible Emergency Hospital",
            "Network Snap Distance (m)",
            "Network Snap Accepted",
            "Access Road Edge ID",
            "Access Edge Fraction",
        ],
    )

    demand_connectors = _accepted_connectors(demand, "Demand Node ID", None, "demand")
    dispatch_connectors = _accepted_connectors(
        dispatch, "Dispatch Base Node ID", "Candidate Dispatch Base", "dispatch"
    )
    hospital_connectors = _accepted_connectors(
        hospitals, "Hospital Node ID", "Eligible Emergency Hospital", "hospital"
    )
    connectors = pd.concat(
        [demand_connectors, dispatch_connectors, hospital_connectors],
        ignore_index=True,
    )
    graph = _build_augmented_graph(
        edges[
            [
                "Road Edge ID",
                "From Node ID",
                "To Node ID",
                "Baseline Edge Travel Time (min)",
                "Assumed Speed (km/h)",
            ]
        ].copy(),
        connectors,
    )
    dispatch_sources = sorted(
        identifier
        for identifier in dispatch_connectors["Connector ID"].astype(str)
        if identifier in graph
    )
    hospital_sources = sorted(
        identifier
        for identifier in hospital_connectors["Connector ID"].astype(str)
        if identifier in graph
    )
    if not dispatch_sources:
        raise ValueError(f"No dispatch bases remain connected in the {scenario} scenario")
    if not hospital_sources:
        raise ValueError(f"No hospitals remain connected in the {scenario} scenario")

    dispatch_distance = nx.multi_source_dijkstra_path_length(
        graph, dispatch_sources, weight="minutes"
    )
    hospital_distance, hospital_label = _labelled_multi_source_distances(
        graph, hospital_sources
    )
    result = demand.copy()
    demand_ids = result["Demand Node ID"].astype("string")
    result["Dispatch Travel Time"] = demand_ids.map(dispatch_distance).astype(float)
    result["Hospital Transport Time"] = demand_ids.map(hospital_distance).astype(float)
    result["Total Emergency Access Time"] = (
        result["Dispatch Travel Time"] + result["Hospital Transport Time"]
    )
    complete_chain = np.isfinite(result["Total Emergency Access Time"])
    result["Assigned Hospital Node ID"] = demand_ids.map(hospital_label).where(complete_chain)
    timely = complete_chain & result["Total Emergency Access Time"].le(float(threshold))
    result["Timely Access Status"] = timely.astype(int)

    if compute_alternatives:
        demand_node_to_index = {
            str(node_id): index
            for index, node_id in result["Demand Node ID"].items()
            if pd.notna(node_id)
        }
        remaining = float(threshold) - result["Dispatch Travel Time"].to_numpy(dtype=float)
        feasible_hospitals = np.zeros(len(result), dtype=np.int16)
        for number, hospital_id in enumerate(hospital_sources, start=1):
            distances = nx.single_source_dijkstra_path_length(
                graph,
                hospital_id,
                cutoff=float(threshold),
                weight="minutes",
            )
            for node_id, transport_time in distances.items():
                index = demand_node_to_index.get(str(node_id))
                if index is not None and transport_time <= remaining[index] + 1e-12:
                    feasible_hospitals[index] += 1
            if number % 10 == 0 or number == len(hospital_sources):
                print(
                    f"Counted timely hospital options: {number}/{len(hospital_sources)}",
                    flush=True,
                )
        result["Alternative Hospital Count"] = np.maximum(
            feasible_hospitals - result["Timely Access Status"].to_numpy(dtype=np.int16),
            0,
        )
    else:
        result["Alternative Hospital Count"] = pd.Series(
            pd.NA, index=result.index, dtype="Int16"
        )

    population = result["Total Population"].astype(float)
    finite_total = np.isfinite(result["Total Emergency Access Time"])
    hospital_summary = hospitals.loc[
        hospitals["Eligible Emergency Hospital"].fillna(False)
        & hospitals["Hospital Node ID"].astype(str).isin(hospital_sources)
    ].copy()
    diagnostics: dict[str, float | int] = {
        "eligible_road_edges": all_eligible_edges,
        "available_road_edges": int(len(edges)),
        "unavailable_road_edges": int(all_eligible_edges - len(edges)),
        "graph_nodes": int(graph.number_of_nodes()),
        "graph_edges": int(graph.number_of_edges()),
        "dispatch_bases": int(len(dispatch_sources)),
        "hospitals": int(len(hospital_sources)),
        "demand_units": int(len(result)),
        "total_population": int(population.sum()),
        "finite_total_population": int(population.loc[finite_total].sum()),
        "timely_population": int(population.loc[timely].sum()),
    }
    return HospitalCatchmentResult(
        demand=result,
        hospitals=hospital_summary,
        diagnostics=diagnostics,
    )


def compute_baseline_access(processed: Path) -> EmergencyAccessResult:
    """Compatibility wrapper for the baseline figure."""
    return compute_emergency_access(processed, scenario="Baseline")
