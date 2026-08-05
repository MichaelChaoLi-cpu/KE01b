#!/usr/bin/env python3
"""Exact fixed-baseline-chain path-dependency Shapley attribution utilities."""

from __future__ import annotations

import heapq
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from emergency_routing import (
    _accepted_connectors,
    _load_demand,
    compute_emergency_access,
    scenario_availability_mask,
)


@dataclass(frozen=True)
class BaselinePathContext:
    """Baseline graph, deterministic shortest-path trees, and source metadata."""

    graph: nx.Graph
    edges: pd.DataFrame
    corridor_ids: np.ndarray
    corridor_code_by_edge: np.ndarray
    demand: pd.DataFrame
    dispatch_distance: dict[str, float]
    dispatch_label: dict[str, str]
    dispatch_parent: dict[str, str]
    hospital_distance: dict[str, float]
    hospital_label: dict[str, str]
    hospital_parent: dict[str, str]
    connector_access_edge: dict[str, int]


@dataclass(frozen=True)
class PathShapleyResult:
    """Scenario corridor values, hospital decomposition, and diagnostics."""

    scenario: str
    values: pd.DataFrame
    hospital_values: pd.DataFrame
    diagnostics: dict[str, float | int]


def _add_fastest_edge(
    graph: nx.Graph,
    start: str,
    end: str,
    minutes: float,
    edge_index: int,
) -> None:
    """Add the fastest undirected connection with deterministic edge tie handling."""
    if graph.has_edge(start, end):
        current = graph[start][end]
        current_minutes = float(current["minutes"])
        current_index = int(current["edge_index"])
        if minutes > current_minutes + 1e-12:
            return
        if abs(minutes - current_minutes) <= 1e-12 and edge_index >= current_index:
            return
    graph.add_edge(start, end, minutes=float(minutes), edge_index=int(edge_index))


def _build_attributed_graph(
    edges: pd.DataFrame,
    connectors: pd.DataFrame,
) -> tuple[nx.Graph, dict[str, int]]:
    """Split baseline edges at connector positions and retain source-edge indices."""
    edge_index_by_id = dict(
        zip(edges["Road Edge ID"].astype(str), edges["_Edge Index"].astype(int), strict=True)
    )
    edge_speed_by_id = dict(
        zip(
            edges["Road Edge ID"].astype(str),
            edges["Assumed Speed (km/h)"].astype(float),
            strict=True,
        )
    )
    connectors = connectors.loc[
        connectors["Access Road Edge ID"].astype(str).isin(edge_index_by_id)
    ].copy()
    connectors["Access Road Edge ID"] = connectors["Access Road Edge ID"].astype(str)
    connectors["_Access Edge Index"] = connectors["Access Road Edge ID"].map(
        edge_index_by_id
    )
    connectors["_Access Speed"] = connectors["Access Road Edge ID"].map(edge_speed_by_id)
    connectors["Access Edge Fraction"] = connectors["Access Edge Fraction"].astype(float).clip(
        0.0, 1.0
    )
    connectors["_Connector Minutes"] = (
        60.0
        * connectors["Network Snap Distance (m)"].astype(float)
        / (1_000.0 * connectors["_Access Speed"].astype(float))
    )
    access_by_edge = {
        str(edge_id): group.sort_values(
            ["Access Edge Fraction", "Connector ID"], kind="stable"
        )
        for edge_id, group in connectors.groupby("Access Road Edge ID", sort=False)
    }

    graph = nx.Graph()
    edge_columns = [
        "Road Edge ID",
        "From Node ID",
        "To Node ID",
        "Baseline Edge Travel Time (min)",
        "_Edge Index",
    ]
    for edge_id, from_node, to_node, edge_minutes, edge_index in edges[
        edge_columns
    ].itertuples(index=False, name=None):
        edge_id = str(edge_id)
        from_node = str(from_node)
        to_node = str(to_node)
        edge_minutes = float(edge_minutes)
        edge_index = int(edge_index)
        access = access_by_edge.get(edge_id)
        if access is None:
            _add_fastest_edge(graph, from_node, to_node, edge_minutes, edge_index)
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
            _add_fastest_edge(
                graph,
                start,
                end,
                edge_minutes * (end_fraction - start_fraction),
                edge_index,
            )

        snap_for_fraction = dict(zip(positions, chain_nodes[1:-1], strict=True))
        for row in access.itertuples(index=False):
            connector_id = str(row[0])
            fraction = float(row[3])
            connector_minutes = float(row[-1])
            _add_fastest_edge(
                graph,
                connector_id,
                snap_for_fraction[fraction],
                connector_minutes,
                -1,
            )

    connector_access_edge = dict(
        zip(
            connectors["Connector ID"].astype(str),
            connectors["_Access Edge Index"].astype(int),
            strict=True,
        )
    )
    return graph, connector_access_edge


def _deterministic_multi_source_tree(
    graph: nx.Graph,
    sources: list[str],
) -> tuple[dict[str, float], dict[str, str], dict[str, str]]:
    """Return distances, nearest-source labels, and one deterministic predecessor tree."""
    distances: dict[str, float] = {}
    labels: dict[str, str] = {}
    parents: dict[str, str] = {}
    queue: list[tuple[float, str, str]] = []
    for source in sorted(set(sources)):
        distances[source] = 0.0
        labels[source] = source
        heapq.heappush(queue, (0.0, source, source))

    tolerance = 1e-12
    while queue:
        distance, source, node = heapq.heappop(queue)
        known_distance = distances.get(node, np.inf)
        known_source = labels.get(node)
        if distance > known_distance + tolerance:
            continue
        if abs(distance - known_distance) <= tolerance and source != known_source:
            continue
        for neighbour, attributes in graph[node].items():
            candidate = distance + float(attributes["minutes"])
            current = distances.get(neighbour, np.inf)
            current_source = labels.get(neighbour)
            shorter = candidate < current - tolerance
            better_source_tie = (
                abs(candidate - current) <= tolerance
                and (current_source is None or source < current_source)
            )
            if shorter or better_source_tie:
                distances[neighbour] = candidate
                labels[neighbour] = source
                parents[neighbour] = node
                heapq.heappush(queue, (candidate, source, neighbour))
    return distances, labels, parents


def build_baseline_path_context(processed: Path) -> BaselinePathContext:
    """Build the deterministic baseline path context once for all scenarios."""
    edge_columns = [
        "Road Edge ID",
        "From Node ID",
        "To Node ID",
        "Medical Corridor ID",
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
    edges = edges.loc[scenario_availability_mask(edges, "Baseline")].reset_index(drop=True)
    edges["_Edge Index"] = np.arange(len(edges), dtype=np.int32)
    corridor_codes, corridor_ids = pd.factorize(
        edges["Medical Corridor ID"].astype("string"), sort=True
    )
    edges["_Corridor Code"] = corridor_codes.astype(np.int32)

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
        [demand_connectors, dispatch_connectors, hospital_connectors], ignore_index=True
    )
    graph, connector_access_edge = _build_attributed_graph(edges, connectors)

    dispatch_sources = sorted(
        source
        for source in dispatch_connectors["Connector ID"].astype(str)
        if source in graph
    )
    hospital_sources = sorted(
        source
        for source in hospital_connectors["Connector ID"].astype(str)
        if source in graph
    )
    print("Tracing deterministic baseline dispatch tree...", flush=True)
    dispatch_distance, dispatch_label, dispatch_parent = _deterministic_multi_source_tree(
        graph, dispatch_sources
    )
    print("Tracing deterministic baseline hospital tree...", flush=True)
    hospital_distance, hospital_label, hospital_parent = _deterministic_multi_source_tree(
        graph, hospital_sources
    )
    return BaselinePathContext(
        graph=graph,
        edges=edges,
        corridor_ids=np.asarray(corridor_ids.astype(str)),
        corridor_code_by_edge=edges["_Corridor Code"].to_numpy(dtype=np.int32),
        demand=demand,
        dispatch_distance=dispatch_distance,
        dispatch_label=dispatch_label,
        dispatch_parent=dispatch_parent,
        hospital_distance=hospital_distance,
        hospital_label=hospital_label,
        hospital_parent=hospital_parent,
        connector_access_edge=connector_access_edge,
    )


def _tree_dependency_set(
    node: str,
    parents: dict[str, str],
    graph: nx.Graph,
    unavailable_edge: np.ndarray,
    corridor_code_by_edge: np.ndarray,
    cache: dict[str, frozenset[int]],
) -> frozenset[int]:
    """Return disrupted corridor codes on a tree path, memoizing shared branches."""
    if node in cache:
        return cache[node]
    trail: list[str] = []
    current = node
    while current in parents and current not in cache:
        trail.append(current)
        current = parents[current]
    dependencies = cache.get(current, frozenset())
    for child in reversed(trail):
        parent = parents[child]
        edge_index = int(graph[child][parent]["edge_index"])
        if edge_index >= 0 and unavailable_edge[edge_index]:
            dependencies = dependencies.union(
                [int(corridor_code_by_edge[edge_index])]
            )
        cache[child] = dependencies
    return cache.get(node, dependencies)


def compute_path_shapley(
    processed: Path,
    context: BaselinePathContext,
    scenario: str,
    threshold: float = 30.0,
) -> PathShapleyResult:
    """Allocate lost timely-access population across baseline-chain blockers."""
    scenario_access = compute_emergency_access(
        processed, scenario=scenario, demand_support="mesh"
    ).demand
    baseline = context.demand[
        ["Mesh Code", "Demand Node ID", "Total Population"]
    ].copy()
    demand_ids = baseline["Demand Node ID"].astype("string")
    baseline["Baseline Time"] = demand_ids.map(context.dispatch_distance).astype(float) + demand_ids.map(
        context.hospital_distance
    ).astype(float)
    baseline = baseline.merge(
        scenario_access[["Mesh Code", "Total Emergency Access Time"]].rename(
            columns={"Total Emergency Access Time": "Scenario Time"}
        ),
        on="Mesh Code",
        validate="one_to_one",
    )
    baseline_timely = baseline["Baseline Time"].le(float(threshold))
    scenario_timely = baseline["Scenario Time"].le(float(threshold))
    lost = baseline.loc[baseline_timely & ~scenario_timely].copy()

    available = scenario_availability_mask(context.edges, scenario).to_numpy(dtype=bool)
    unavailable_edge = ~available
    dispatch_cache: dict[str, frozenset[int]] = {}
    hospital_cache: dict[str, frozenset[int]] = {}
    attributed: defaultdict[int, float] = defaultdict(float)
    hospital_attributed: defaultdict[tuple[int, str], float] = defaultdict(float)
    traced_population = 0.0
    untraced_population = 0.0
    untraced_units = 0

    for number, row in enumerate(lost.itertuples(index=False), start=1):
        demand_node = str(row[1])
        population = float(row[2])
        dependencies = set(
            _tree_dependency_set(
                demand_node,
                context.dispatch_parent,
                context.graph,
                unavailable_edge,
                context.corridor_code_by_edge,
                dispatch_cache,
            )
        )
        dependencies.update(
            _tree_dependency_set(
                demand_node,
                context.hospital_parent,
                context.graph,
                unavailable_edge,
                context.corridor_code_by_edge,
                hospital_cache,
            )
        )
        connector_ids = [
            demand_node,
            context.dispatch_label.get(demand_node),
            context.hospital_label.get(demand_node),
        ]
        for connector_id in connector_ids:
            if connector_id is None:
                continue
            edge_index = context.connector_access_edge.get(str(connector_id))
            if edge_index is not None and unavailable_edge[edge_index]:
                dependencies.add(int(context.corridor_code_by_edge[edge_index]))

        dependencies.discard(-1)
        if dependencies:
            baseline_hospital = context.hospital_label.get(demand_node)
            if baseline_hospital is None:
                raise RuntimeError(
                    f"{scenario} lost-demand unit {demand_node} has no baseline hospital label"
                )
            share = population / len(dependencies)
            for corridor_code in dependencies:
                attributed[corridor_code] += share
                hospital_attributed[(corridor_code, str(baseline_hospital))] += share
            traced_population += population
        else:
            untraced_units += 1
            untraced_population += population
        if number % 10_000 == 0:
            print(
                f"{scenario}: traced {number:,}/{len(lost):,} lost-demand units",
                flush=True,
            )

    values = pd.DataFrame(
        {
            "_Corridor Code": list(attributed),
            "Path-Dependency Road Shapley Value": list(attributed.values()),
        }
    )
    if len(values):
        values["Medical Corridor ID"] = values["_Corridor Code"].map(
            dict(enumerate(context.corridor_ids))
        )
        values["Disruption Scenario"] = scenario
        values = values.sort_values(
            ["Path-Dependency Road Shapley Value", "Medical Corridor ID"],
            ascending=[False, True],
            kind="stable",
        ).reset_index(drop=True)
        values["Scenario Priority Rank"] = np.arange(1, len(values) + 1)
    else:
        values = pd.DataFrame(
            columns=[
                "_Corridor Code",
                "Path-Dependency Road Shapley Value",
                "Medical Corridor ID",
                "Disruption Scenario",
                "Scenario Priority Rank",
            ]
        )

    hospital_values = pd.DataFrame(
        [
            {
                "_Corridor Code": corridor_code,
                "Hospital Node ID": hospital_node_id,
                "Path-Dependency Road-Hospital Shapley Value": value,
            }
            for (corridor_code, hospital_node_id), value in hospital_attributed.items()
        ]
    )
    if len(hospital_values):
        hospital_values["Medical Corridor ID"] = hospital_values[
            "_Corridor Code"
        ].map(dict(enumerate(context.corridor_ids)))
        hospital_values["Disruption Scenario"] = scenario
        hospital_values = hospital_values.sort_values(
            [
                "Path-Dependency Road-Hospital Shapley Value",
                "Medical Corridor ID",
                "Hospital Node ID",
            ],
            ascending=[False, True, True],
            kind="stable",
        ).reset_index(drop=True)
    else:
        hospital_values = pd.DataFrame(
            columns=[
                "_Corridor Code",
                "Hospital Node ID",
                "Path-Dependency Road-Hospital Shapley Value",
                "Medical Corridor ID",
                "Disruption Scenario",
            ]
        )

    hospital_corridor_totals = (
        hospital_values.groupby("Medical Corridor ID", sort=False)[
            "Path-Dependency Road-Hospital Shapley Value"
        ]
        .sum()
        .reindex(values["Medical Corridor ID"], fill_value=0.0)
        .to_numpy(dtype=float)
    )
    road_corridor_totals = values[
        "Path-Dependency Road Shapley Value"
    ].to_numpy(dtype=float)
    if not np.allclose(hospital_corridor_totals, road_corridor_totals, rtol=0, atol=1e-5):
        maximum_difference = float(
            np.max(np.abs(hospital_corridor_totals - road_corridor_totals))
        )
        raise RuntimeError(
            f"{scenario} road-hospital decomposition failed: "
            f"maximum corridor difference {maximum_difference}"
        )

    shapley_total = float(values["Path-Dependency Road Shapley Value"].sum())
    if not np.isclose(shapley_total, traced_population, rtol=0, atol=1e-5):
        raise RuntimeError(
            f"{scenario} path-Shapley efficiency failed: {shapley_total} != {traced_population}"
        )
    diagnostics: dict[str, float | int] = {
        "lost_units": int(len(lost)),
        "lost_population": float(lost["Total Population"].sum()),
        "traced_units": int(len(lost) - untraced_units),
        "traced_population": traced_population,
        "untraced_units": int(untraced_units),
        "untraced_population": untraced_population,
        "positive_corridors": int(len(values)),
        "positive_road_hospital_pairs": int(len(hospital_values)),
        "shapley_total": shapley_total,
    }
    return PathShapleyResult(
        scenario=scenario,
        values=values,
        hospital_values=hospital_values,
        diagnostics=diagnostics,
    )
