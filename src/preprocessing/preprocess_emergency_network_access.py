#!/usr/bin/env python3
"""Snap ambulance bases, emergency hospitals, and demand units to the road network."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from shapely import STRtree


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
CALC_CRS = "EPSG:6670"
OUTPUT_CRS = "EPSG:6668"


def _network() -> tuple[gpd.GeoDataFrame, STRtree, np.ndarray]:
    edges = gpd.read_parquet(PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet")
    edges = edges.loc[edges["Network Analysis Eligible"]].to_crs(CALC_CRS).reset_index(drop=True)
    geometries = np.asarray(edges.geometry.array, dtype=object)
    return edges, STRtree(geometries), geometries


def _access_points(
    source: gpd.GeoDataFrame,
    id_column: str,
    id_prefix: str,
    maximum_distance: float,
    tree: STRtree,
    edge_geometries: np.ndarray,
    edges: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    source = source.to_crs(CALC_CRS).reset_index(drop=True).copy()
    points = np.asarray(source.geometry.array, dtype=object)
    pairs, distances = tree.query_nearest(points, all_matches=False, return_distance=True)
    if not np.array_equal(pairs[0], np.arange(len(source))):
        raise RuntimeError("Nearest-edge query did not return one result per access point")
    edge_positions = pairs[1]
    nearest_edges = edge_geometries[edge_positions]
    fractions = shapely.line_locate_point(nearest_edges, points, normalized=True)
    snapped = shapely.line_interpolate_point(nearest_edges, fractions, normalized=True)
    accepted = distances <= maximum_distance
    virtual_ids = pd.Series(
        [f"{id_prefix}-{position + 1:07d}" for position in range(len(source))],
        dtype="string",
    ).where(accepted)
    source[id_column] = virtual_ids
    source["Network Snap Distance (m)"] = distances
    source["Network Snap Accepted"] = accepted
    source["Access Road Edge ID"] = pd.Series(edges.iloc[edge_positions]["Road Edge ID"].to_numpy(), dtype="string").where(accepted)
    source["Access Edge Fraction"] = pd.Series(fractions, dtype="Float64").where(accepted)
    source["Geometry"] = gpd.GeoSeries(np.where(accepted, snapped, points), crs=CALC_CRS)
    source = source.set_geometry("Geometry")
    return source.to_crs(OUTPUT_CRS)


def _save(frame: gpd.GeoDataFrame, filename: str) -> None:
    path = PROCESSED / filename
    frame.to_parquet(path, index=False)
    accepted = int(frame["Network Snap Accepted"].sum())
    print(
        f"Saved {len(frame):,} rows x {len(frame.columns)} columns -> {path.relative_to(ROOT)}; "
        f"accepted snaps: {accepted:,}/{len(frame):,}"
    )


def main() -> None:
    edges, tree, edge_geometries = _network()

    fire = gpd.read_parquet(PROCESSED / "kumamoto_fire_stations_2012_preprocessed.parquet")
    fire = fire.loc[fire["Candidate Dispatch Base"]].sort_values(
        ["Municipality Code", "Fire Facility Name"], kind="stable"
    ).reset_index(drop=True)
    fire = _access_points(
        fire, "Dispatch Base Node ID", "DISPATCH", 150.0, tree, edge_geometries, edges
    )
    _save(fire, "kumamoto_dispatch_base_network_access_preprocessed.parquet")

    hospitals = gpd.read_parquet(PROCESSED / "kumamoto_medical_facilities_2020_preprocessed.parquet")
    hospitals = hospitals.loc[hospitals["Eligible Emergency Hospital"]].sort_values(
        ["Facility Name", "Address"], kind="stable"
    ).reset_index(drop=True)
    hospitals["Operational Hospital Set"] = "P04 Emergency or Disaster-Base Baseline"
    hospitals["Hospital Role Weight"] = 1.0
    # Reported bed count is retained as the capacity weight. Missing bed counts
    # remain missing; normalization, if required, belongs to estimation.
    hospitals["Hospital Capacity Weight"] = hospitals["Bed Count"].astype("Float64")
    hospitals = _access_points(
        hospitals, "Hospital Node ID", "HOSPITAL", 150.0, tree, edge_geometries, edges
    )
    _save(hospitals, "kumamoto_hospital_network_access_preprocessed.parquet")

    meshes = gpd.read_parquet(PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet")
    meshes = meshes.sort_values("Mesh Code", kind="stable").reset_index(drop=True)
    meshes["Analysis Unit ID"] = meshes["Mesh Code"].astype("string")
    meshes = meshes.to_crs(CALC_CRS)
    meshes = meshes.set_geometry(meshes.geometry.centroid)
    meshes = _access_points(
        meshes, "Demand Node ID", "DEMAND-MESH", 250.0, tree, edge_geometries, edges
    )
    _save(meshes, "kumamoto_population_mesh_network_access_preprocessed.parquet")

    groups = gpd.read_parquet(PROCESSED / "kumamoto_population_disclosure_groups_preprocessed.parquet")
    groups = groups.sort_values("Disclosure Group Code", kind="stable").reset_index(drop=True)
    groups["Analysis Unit ID"] = groups["Disclosure Group Code"].astype("string")
    destination_meshes = gpd.read_parquet(PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet")
    destination_meshes = destination_meshes.loc[
        destination_meshes["Mesh Code"].astype("string").eq(destination_meshes["Disclosure Group Code"].astype("string")),
        ["Mesh Code", "Geometry"],
    ].rename(columns={"Mesh Code": "Representative Mesh Code"})
    if len(destination_meshes) != len(groups) or not destination_meshes["Representative Mesh Code"].is_unique:
        raise RuntimeError("Each disclosure group must have exactly one aggregation-destination mesh")
    groups = groups.drop(columns="Geometry").merge(
        destination_meshes,
        left_on="Disclosure Group Code",
        right_on="Representative Mesh Code",
        how="left",
        validate="one_to_one",
    )
    groups = gpd.GeoDataFrame(groups, geometry="Geometry", crs=OUTPUT_CRS).to_crs(CALC_CRS)
    groups = groups.set_geometry(groups.geometry.centroid)
    groups = _access_points(
        groups, "Demand Node ID", "DEMAND-GROUP", 250.0, tree, edge_geometries, edges
    )
    _save(groups, "kumamoto_population_group_network_access_preprocessed.parquet")


if __name__ == "__main__":
    main()
