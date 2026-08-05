#!/usr/bin/env python3
"""Build a grade-aware, one-metre-snapped ambulance road network for Kumamoto."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from shapely import MultiLineString, STRtree
from shapely.ops import substring


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
CALC_CRS = "EPSG:6670"
OUTPUT_CRS = "EPSG:6668"
SNAP_GRID_M = 1.0
EMERGENCY_ROUTE_TOLERANCE_M = 30.0
MAX_FAILURE_UNIT_LENGTH_M = 100.0
FAILURE_UNIT_SPLIT_TARGET_M = 98.0

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


def _split_long_edges(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Split every topological edge into road-failure units no longer than 100 m."""
    records: list[dict[str, object]] = []
    columns = list(edges.columns)
    geometry_column = edges.geometry.name
    for values in edges.itertuples(index=False, name=None):
        record = dict(zip(columns, values, strict=True))
        geometry = record.pop(geometry_column)
        piece_count = max(1, int(np.ceil(geometry.length / FAILURE_UNIT_SPLIT_TARGET_M)))
        if piece_count == 1:
            record[geometry_column] = geometry
            records.append(record)
            continue
        boundaries = np.linspace(0.0, float(geometry.length), piece_count + 1)
        for start, end in zip(boundaries[:-1], boundaries[1:], strict=True):
            piece = shapely.set_precision(
                substring(geometry, float(start), float(end)), SNAP_GRID_M
            )
            if not piece.is_empty and piece.length > 0:
                piece_record = record.copy()
                piece_record[geometry_column] = piece
                records.append(piece_record)
    return gpd.GeoDataFrame(records, geometry=geometry_column, crs=edges.crs)


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

    edges = _split_long_edges(edges)
    edges = edges.loc[~edges.geometry.is_empty & (edges.geometry.length > 0)].reset_index(drop=True)
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

    order_columns = ["Network Component ID", "From Node ID", "To Node ID", "Road Category", "Road Length (m)"]
    edges = edges.sort_values(order_columns, kind="stable").reset_index(drop=True)
    edges["Road Edge ID"] = [f"EDGE-{position + 1:07d}" for position in range(len(edges))]
    edges["Road Failure Unit ID"] = [
        f"RFU-{position + 1:07d}" for position in range(len(edges))
    ]

    edge_columns = [
        "Road Edge ID", "Road Failure Unit ID", "From Node ID", "To Node ID", "Network Component ID",
        "Road Length (m)", "Assumed Speed (km/h)", "Baseline Edge Travel Time (min)",
        "Hazard Exposure Class", "Emergency Route Membership", "Road Available", "Network Analysis Eligible",
        "Route ID", "Route Name",
        "Road Category", "Road State", "Vertical Level", "Width Category", "Toll Category", "Secondary Mesh Code", "Geometry",
    ]
    edge_output = edges[edge_columns].to_crs(OUTPUT_CRS)
    node_output = nodes.to_crs(OUTPUT_CRS)
    edge_path = PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet"
    node_path = PROCESSED / "kumamoto_routable_road_nodes_preprocessed.parquet"
    edge_output.to_parquet(edge_path, index=False)
    node_output.to_parquet(node_path, index=False)
    print(f"Saved {len(edge_output):,} road edges x {len(edge_output.columns)} columns -> {edge_path.relative_to(ROOT)}")
    print(f"Saved {len(node_output):,} road nodes x {len(node_output.columns)} columns -> {node_path.relative_to(ROOT)}")
    largest_component_edges = int(edge_output["Network Component ID"].value_counts().iloc[0])
    print(
        f"Analysis-eligible edges: {int(edge_output['Network Analysis Eligible'].sum()):,}; "
        f"largest component edges: {largest_component_edges:,}; "
        f"100 m road-failure units: {edge_output['Road Failure Unit ID'].nunique():,}"
    )


if __name__ == "__main__":
    main()
