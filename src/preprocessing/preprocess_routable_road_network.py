#!/usr/bin/env python3
"""Build a grade-aware, one-metre-snapped ambulance road network for Kumamoto."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from shapely import MultiLineString, STRtree


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
CALC_CRS = "EPSG:6670"
OUTPUT_CRS = "EPSG:6668"
SNAP_GRID_M = 1.0
EMERGENCY_ROUTE_TOLERANCE_M = 30.0

ROAD_COLUMNS = [
    "Road Category",
    "Road State",
    "Vertical Level",
    "Width Category",
    "Toll Category",
    "Secondary Mesh Code",
]

BASE_SPEED = {
    "National Expressway or Equivalent": 80.0,
    "National Highway": 50.0,
    "Prefectural Road": 40.0,
    "Municipal Road or Equivalent": 30.0,
    "Other": 20.0,
    "Unknown": 20.0,
}
WIDTH_CAP = {
    "Under 3 m": 20.0,
    "3 to Under 5.5 m": 30.0,
    "5.5 to Under 13 m": 50.0,
    "13 to Under 19.5 m": 60.0,
    "19.5 m or More": 80.0,
    "Unknown": 20.0,
}
ROUTE_TYPE_TO_ROAD_CATEGORY = {
    "National Expressway": "National Expressway or Equivalent",
    "National Highway": "National Highway",
    "Major Prefectural": "Prefectural Road",
    "General Prefectural": "Prefectural Road",
    "Municipal Road": "Municipal Road or Equivalent",
    "Major Designated-City": "Municipal Road or Equivalent",
}


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = np.arange(size, dtype=np.int64)
        self.rank = np.zeros(size, dtype=np.int8)

    def find(self, value: int) -> int:
        parent = self.parent
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = int(parent[value])
        return value

    def union(self, left: int, right: int) -> None:
        a, b = self.find(left), self.find(right)
        if a == b:
            return
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1


def _flatten_source(group: gpd.GeoDataFrame) -> tuple[np.ndarray, list[int]]:
    geometries: list[object] = []
    parents: list[int] = []
    for position, geometry in enumerate(group.geometry.array):
        for part in shapely.get_parts(geometry):
            if part.geom_type == "LineString" and not part.is_empty and part.length > 0:
                snapped = shapely.set_precision(part, SNAP_GRID_M)
                if not snapped.is_empty and snapped.length > 0:
                    geometries.append(snapped)
                    parents.append(position)
    return np.asarray(geometries, dtype=object), parents


def _node_group(group: gpd.GeoDataFrame) -> list[dict[str, object]]:
    source_geometries, parent_positions = _flatten_source(group)
    if not len(source_geometries):
        return []
    noded = shapely.node(MultiLineString(source_geometries.tolist()))
    parts = np.asarray(
        [part for part in shapely.get_parts(noded) if part.geom_type == "LineString" and part.length > 0],
        dtype=object,
    )
    midpoints = shapely.line_interpolate_point(parts, 0.5, normalized=True)
    tree = STRtree(source_geometries)
    pairs = tree.query(midpoints, predicate="intersects")
    chosen: dict[int, int] = {}
    for part_position, source_position in zip(pairs[0], pairs[1], strict=True):
        chosen.setdefault(int(part_position), int(source_position))
    missing = [position for position in range(len(parts)) if position not in chosen]
    if missing:
        nearest = tree.query_nearest(midpoints[missing], all_matches=False)
        for local_position, source_position in zip(nearest[0], nearest[1], strict=True):
            chosen[missing[int(local_position)]] = int(source_position)

    records: list[dict[str, object]] = []
    for part_position, geometry in enumerate(parts):
        source_row = group.iloc[parent_positions[chosen[part_position]]]
        record = {column: source_row[column] for column in ROAD_COLUMNS}
        record["Geometry"] = geometry
        records.append(record)
    return records


def _assign_emergency_routes(edges: gpd.GeoDataFrame) -> pd.DataFrame:
    """Match compatible emergency routes without assigning crossing road classes."""
    routes = gpd.read_parquet(
        PROCESSED / "kumamoto_emergency_transport_roads_2024_preprocessed.parquet"
    ).to_crs(CALC_CRS)
    route_geometries = np.asarray(routes.geometry.array, dtype=object)
    tree = STRtree(route_geometries)
    midpoints = shapely.line_interpolate_point(np.asarray(edges.geometry.array, dtype=object), 0.5, normalized=True)
    pairs = tree.query(
        midpoints,
        predicate="dwithin",
        distance=EMERGENCY_ROUTE_TOLERANCE_M,
    )
    route_category = routes["Road Type"].map(ROUTE_TYPE_TO_ROAD_CATEGORY)
    compatible = (
        edges["Road Category"].fillna("Unknown").astype(str).to_numpy()[pairs[0]]
        == route_category.fillna("Unmatchable").astype(str).to_numpy()[pairs[1]]
    )
    edge_positions = pairs[0][compatible]
    route_positions = pairs[1][compatible]
    if len(edge_positions):
        distances = shapely.distance(
            midpoints[edge_positions], route_geometries[route_positions]
        )
        candidates = pd.DataFrame(
            {
                "_Edge Position": edge_positions,
                "_Route Position": route_positions,
                "_Distance": distances,
                "_Route ID": routes["Route ID"].astype("string").to_numpy()[route_positions],
            }
        ).sort_values(
            ["_Edge Position", "_Distance", "_Route ID", "_Route Position"],
            kind="stable",
        )
        chosen = candidates.drop_duplicates("_Edge Position", keep="first")
    else:
        chosen = pd.DataFrame(columns=["_Edge Position", "_Route Position"])

    membership = np.full(len(edges), "None", dtype=object)
    route_ids = np.full(len(edges), pd.NA, dtype=object)
    route_names = np.full(len(edges), pd.NA, dtype=object)
    if len(chosen):
        edge_position = chosen["_Edge Position"].to_numpy(dtype=int)
        route_position = chosen["_Route Position"].to_numpy(dtype=int)
        membership[edge_position] = (
            routes["Emergency Road Class"]
            .fillna("Other or Unspecified")
            .astype(str)
            .to_numpy()[route_position]
        )
        route_ids[edge_position] = routes["Route ID"].astype("string").to_numpy()[
            route_position
        ]
        route_names[edge_position] = routes["Route Name"].astype("string").to_numpy()[
            route_position
        ]
    return pd.DataFrame(
        {
            "Emergency Route Membership": pd.Series(membership, dtype="string"),
            "Route ID": pd.Series(route_ids, dtype="string"),
            "Route Name": pd.Series(route_names, dtype="string"),
        },
        index=edges.index,
    )


def _assign_hazard_exposure(edges: gpd.GeoDataFrame) -> pd.Series:
    zones = gpd.read_parquet(
        PROCESSED / "kumamoto_landslide_warning_zones_2025_preprocessed.parquet"
    ).to_crs(CALC_CRS)
    zone_geometries = np.asarray(zones.geometry.array, dtype=object)
    tree = STRtree(zone_geometries)
    edge_geometries = np.asarray(edges.geometry.array, dtype=object)
    pairs = tree.query(edge_geometries, predicate="intersects")
    score = np.zeros(len(edges), dtype=np.int8)
    classes = zones["Warning Zone Class"].fillna("None").astype(str).to_numpy()
    zone_score = np.where(classes == "Special Warning Zone", 2, np.where(classes == "Warning Zone", 1, 0))
    np.maximum.at(score, pairs[0], zone_score[pairs[1]])
    labels = np.asarray(["None", "Warning Zone", "Special Warning Zone"], dtype=object)
    return pd.Series(labels[score], index=edges.index, dtype="string")


def _node_keys(edges: gpd.GeoDataFrame) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    geometries = np.asarray(edges.geometry.array, dtype=object)
    starts = shapely.get_coordinates(shapely.get_point(geometries, 0))
    ends = shapely.get_coordinates(shapely.get_point(geometries, -1))
    levels = edges["Vertical Level"].fillna(0).astype(int).to_numpy()
    start_keys = [(int(level), int(round(x)), int(round(y))) for level, (x, y) in zip(levels, starts, strict=True)]
    end_keys = [(int(level), int(round(x)), int(round(y))) for level, (x, y) in zip(levels, ends, strict=True)]
    return start_keys, end_keys


def _assign_components(edges: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    start_keys, end_keys = _node_keys(edges)
    keys = sorted(set(start_keys) | set(end_keys))
    key_to_position = {key: position for position, key in enumerate(keys)}
    start_positions = np.fromiter((key_to_position[key] for key in start_keys), dtype=np.int64)
    end_positions = np.fromiter((key_to_position[key] for key in end_keys), dtype=np.int64)
    union_find = UnionFind(len(keys))
    for start, end in zip(start_positions, end_positions, strict=True):
        union_find.union(int(start), int(end))
    roots = np.fromiter((union_find.find(position) for position in range(len(keys))), dtype=np.int64)
    root_counts = pd.Series(roots).value_counts()
    ordered_roots = sorted(root_counts.index, key=lambda root: (-int(root_counts[root]), keys[int(root)]))
    root_to_component = {int(root): f"COMP-{rank:04d}" for rank, root in enumerate(ordered_roots, 1)}
    node_ids = [f"NODE-{position + 1:07d}" for position in range(len(keys))]
    node_components = [root_to_component[int(root)] for root in roots]

    edges = edges.copy()
    edges["From Node ID"] = [node_ids[position] for position in start_positions]
    edges["To Node ID"] = [node_ids[position] for position in end_positions]
    edges["Network Component ID"] = [node_components[position] for position in start_positions]
    # Every valid Standard Road component remains eligible. Component IDs allow
    # the routing stage to return disconnected access explicitly instead of
    # silently dropping island and remote-area demand during preprocessing.
    edges["Network Analysis Eligible"] = True

    nodes = gpd.GeoDataFrame(
        {
            "Network Node ID": node_ids,
            "Network Component ID": node_components,
            "Network Analysis Eligible": True,
            "Vertical Level": [key[0] for key in keys],
        },
        geometry=gpd.points_from_xy([key[1] for key in keys], [key[2] for key in keys], crs=CALC_CRS),
    ).rename_geometry("Geometry")
    return edges, nodes


def _assign_road_sections(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Assign maximal junction-to-junction sections without distance splitting."""
    from_nodes = edges["From Node ID"].astype(str).to_numpy()
    to_nodes = edges["To Node ID"].astype(str).to_numpy()
    node_edges: dict[str, list[int]] = {}
    for edge_position, (start, end) in enumerate(
        zip(from_nodes, to_nodes, strict=True)
    ):
        node_edges.setdefault(start, []).append(edge_position)
        node_edges.setdefault(end, []).append(edge_position)
    for incident in node_edges.values():
        incident.sort()
    degree = {node: len(incident) for node, incident in node_edges.items()}

    assigned = np.full(len(edges), -1, dtype=np.int64)
    section_records: list[tuple[str, str, list[int]]] = []

    def other_node(edge_position: int, node: str) -> str:
        start = from_nodes[edge_position]
        end = to_nodes[edge_position]
        if start == node:
            return end
        if end == node:
            return start
        raise RuntimeError("Road-section traversal encountered a nonincident edge")

    junctions = sorted(node for node, value in degree.items() if value != 2)
    for start_node in junctions:
        for first_edge in node_edges[start_node]:
            if assigned[first_edge] >= 0:
                continue
            section_edges: list[int] = []
            current_node = start_node
            current_edge = first_edge
            while True:
                if assigned[current_edge] >= 0:
                    break
                assigned[current_edge] = len(section_records)
                section_edges.append(current_edge)
                next_node = other_node(current_edge, current_node)
                if degree[next_node] != 2:
                    current_node = next_node
                    break
                candidates = [
                    edge_position
                    for edge_position in node_edges[next_node]
                    if edge_position != current_edge
                ]
                if len(candidates) != 1 or assigned[candidates[0]] >= 0:
                    current_node = next_node
                    break
                current_node = next_node
                current_edge = candidates[0]
            section_records.append((start_node, current_node, section_edges))

    # Components containing no degree-not-two node are closed cycles. They have
    # no true junction at which to split, so the full cycle is one road section.
    for first_edge in np.flatnonzero(assigned < 0):
        if assigned[first_edge] >= 0:
            continue
        section_number = len(section_records)
        stack = [int(first_edge)]
        cycle_edges: list[int] = []
        cycle_nodes: set[str] = set()
        while stack:
            edge_position = stack.pop()
            if assigned[edge_position] >= 0:
                continue
            assigned[edge_position] = section_number
            cycle_edges.append(edge_position)
            for node in (from_nodes[edge_position], to_nodes[edge_position]):
                cycle_nodes.add(node)
                stack.extend(
                    candidate
                    for candidate in node_edges[node]
                    if assigned[candidate] < 0
                )
        anchor = min(cycle_nodes)
        section_records.append((anchor, anchor, sorted(cycle_edges)))

    if np.any(assigned < 0):
        raise RuntimeError("Not every routing edge received a road section")

    section_order = sorted(
        range(len(section_records)),
        key=lambda position: (
            edges.iloc[section_records[position][2][0]]["Network Component ID"],
            section_records[position][0],
            section_records[position][1],
            min(section_records[position][2]),
        ),
    )
    old_to_new = {
        old: new for new, old in enumerate(section_order, start=1)
    }
    edges = edges.copy()
    edges["Road Section ID"] = [
        f"SECTION-{old_to_new[int(value)]:07d}" for value in assigned
    ]
    section_from = {
        f"SECTION-{old_to_new[position]:07d}": section_records[position][0]
        for position in range(len(section_records))
    }
    section_to = {
        f"SECTION-{old_to_new[position]:07d}": section_records[position][1]
        for position in range(len(section_records))
    }
    edges["Section From Node ID"] = edges["Road Section ID"].map(section_from)
    edges["Section To Node ID"] = edges["Road Section ID"].map(section_to)
    return edges


def _build_section_layer(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Dissolve routing fragments into one record per junction-defined section."""
    grouped = edges.groupby("Road Section ID", sort=True, observed=True)
    sections = grouped.agg(
        **{
            "Section From Node ID": ("Section From Node ID", "first"),
            "Section To Node ID": ("Section To Node ID", "first"),
            "Network Component ID": ("Network Component ID", "first"),
            "Road Section Length (m)": ("Road Length (m)", "sum"),
            "Road Edge Count": ("Road Edge ID", "size"),
            "Baseline Section Travel Time (min)": (
                "Baseline Edge Travel Time (min)",
                "sum",
            ),
            "Vertical Level": ("Vertical Level", "first"),
        }
    ).reset_index()

    # Use the longest constituent edge as the deterministic representative for
    # descriptors that may change inside a junction-defined section.
    descriptor_columns = [
        "Emergency Route Membership",
        "Route ID",
        "Route Name",
        "Road Category",
        "Road State",
        "Width Category",
        "Toll Category",
    ]
    representative = (
        edges.sort_values(
            ["Road Section ID", "Road Length (m)", "From Node ID", "To Node ID"],
            ascending=[True, False, True, True],
            kind="stable",
        )
        .drop_duplicates("Road Section ID", keep="first")
        [["Road Section ID", *descriptor_columns]]
    )
    sections = sections.merge(
        representative,
        on="Road Section ID",
        how="left",
        validate="one_to_one",
    )

    hazard_score = edges["Hazard Exposure Class"].map(
        {"None": 0, "Warning Zone": 1, "Special Warning Zone": 2}
    ).fillna(0)
    maximum_hazard = hazard_score.groupby(
        edges["Road Section ID"], sort=True
    ).max()
    hazard_labels = np.asarray(
        ["None", "Warning Zone", "Special Warning Zone"], dtype=object
    )
    sections["Hazard Exposure Class"] = pd.Series(
        hazard_labels[
            sections["Road Section ID"].map(maximum_hazard).to_numpy(dtype=int)
        ],
        dtype="string",
    )
    sections["Assumed Speed (km/h)"] = sections["Road Section Length (m)"] / (
        sections["Baseline Section Travel Time (min)"] * 1000.0 / 60.0
    )
    sections["Road Available"] = True
    sections["Network Analysis Eligible"] = True

    geometry = (
        edges[["Road Section ID", "Geometry"]]
        .dissolve(by="Road Section ID", as_index=False)
        [["Road Section ID", "Geometry"]]
    )
    sections = sections.merge(
        geometry,
        on="Road Section ID",
        how="left",
        validate="one_to_one",
    )
    return gpd.GeoDataFrame(sections, geometry="Geometry", crs=edges.crs)


def main() -> None:
    roads = gpd.read_parquet(PROCESSED / "kumamoto_road_centerlines_2024_preprocessed.parquet")
    roads = roads.loc[roads["Road Centerline Type"].eq("Standard Road"), ROAD_COLUMNS + ["Geometry"]].to_crs(CALC_CRS)
    records: list[dict[str, object]] = []
    grouped = roads.groupby(["Secondary Mesh Code", "Vertical Level"], dropna=False, sort=True)
    for group_number, (_, group) in enumerate(grouped, 1):
        records.extend(_node_group(group.reset_index(drop=True)))
        if group_number % 25 == 0:
            print(f"Noded {group_number} same-level mesh groups")
    edges = gpd.GeoDataFrame(records, geometry="Geometry", crs=CALC_CRS)
    edges = edges.loc[~edges.geometry.is_empty & edges.geometry.is_valid & (edges.geometry.length > 0)].reset_index(drop=True)
    edges = edges.drop_duplicates(subset=["Vertical Level", "Geometry"]).reset_index(drop=True)
    geometries = np.asarray(edges.geometry.array, dtype=object)
    start_coordinates = shapely.get_coordinates(shapely.get_point(geometries, 0))
    end_coordinates = shapely.get_coordinates(shapely.get_point(geometries, -1))
    self_loops = np.all(np.rint(start_coordinates) == np.rint(end_coordinates), axis=1)
    if self_loops.any():
        print(f"Excluded {int(self_loops.sum()):,} closed self-loop lines that do not connect distinct network nodes")
        edges = edges.loc[~self_loops].reset_index(drop=True)

    edges["Road Length (m)"] = edges.geometry.length
    category_speed = edges["Road Category"].map(BASE_SPEED).fillna(20.0).astype(float)
    width_speed = edges["Width Category"].map(WIDTH_CAP).fillna(20.0).astype(float)
    edges["Assumed Speed (km/h)"] = np.minimum(category_speed, width_speed)
    edges["Baseline Edge Travel Time (min)"] = edges["Road Length (m)"] / (edges["Assumed Speed (km/h)"] * 1000.0 / 60.0)
    route_attributes = _assign_emergency_routes(edges)
    for column in route_attributes.columns:
        edges[column] = route_attributes[column]
    edges["Hazard Exposure Class"] = _assign_hazard_exposure(edges)
    edges["Road Available"] = True
    edges, nodes = _assign_components(edges)
    edges = _assign_road_sections(edges)

    order_columns = ["Network Component ID", "From Node ID", "To Node ID", "Road Category", "Road Length (m)"]
    edges = edges.sort_values(order_columns, kind="stable").reset_index(drop=True)
    edges["Road Edge ID"] = [f"EDGE-{position + 1:07d}" for position in range(len(edges))]
    sections = _build_section_layer(edges)

    edge_columns = [
        "Road Edge ID", "Road Section ID", "From Node ID", "To Node ID", "Network Component ID",
        "Road Length (m)", "Assumed Speed (km/h)", "Baseline Edge Travel Time (min)",
        "Hazard Exposure Class", "Emergency Route Membership", "Road Available", "Network Analysis Eligible",
        "Route ID", "Route Name",
        "Road Category", "Road State", "Vertical Level", "Width Category", "Toll Category", "Secondary Mesh Code", "Geometry",
    ]
    edge_output = edges[edge_columns].to_crs(OUTPUT_CRS)
    node_output = nodes.to_crs(OUTPUT_CRS)
    edge_path = PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet"
    node_path = PROCESSED / "kumamoto_routable_road_nodes_preprocessed.parquet"
    section_path = PROCESSED / "kumamoto_road_sections_preprocessed.parquet"
    edge_output.to_parquet(edge_path, index=False)
    node_output.to_parquet(node_path, index=False)
    sections.to_crs(OUTPUT_CRS).to_parquet(section_path, index=False)
    print(f"Saved {len(edge_output):,} road edges x {len(edge_output.columns)} columns -> {edge_path.relative_to(ROOT)}")
    print(f"Saved {len(node_output):,} road nodes x {len(node_output.columns)} columns -> {node_path.relative_to(ROOT)}")
    print(f"Saved {len(sections):,} road sections x {len(sections.columns)} columns -> {section_path.relative_to(ROOT)}")
    largest_component_edges = int(edge_output["Network Component ID"].value_counts().iloc[0])
    print(
        f"Analysis-eligible edges: {int(edge_output['Network Analysis Eligible'].sum()):,}; "
        f"largest component edges: {largest_component_edges:,}; "
        f"junction-to-junction road sections: {edge_output['Road Section ID'].nunique():,}"
    )


if __name__ == "__main__":
    main()
