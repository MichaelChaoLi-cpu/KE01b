#!/usr/bin/env python3
"""Profile geospatial raw layers omitted by the tabular briefing helper."""

from __future__ import annotations

import csv
from pathlib import Path

from pyogrio import read_info


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "emergency_access" / "extracted"
OUTPUT = ROOT / "data" / "exp" / "data-briefing" / "tables"

LAYERS = (
    (
        "administrative_areas",
        RAW / "mlit_ksj_n03_2025_kumamoto" / "N03-20250101_43.geojson",
        "core",
    ),
    ("medical_facilities", RAW / "mlit_ksj_p04_2020_kumamoto" / "P04-20_43.geojson", "core"),
    ("fire_stations", RAW / "mlit_ksj_p17_2012_kumamoto" / "P17-12_43_FireStation.shp", "core"),
    (
        "fire_station_jurisdictions",
        RAW / "mlit_ksj_p17_2012_kumamoto" / "P17-12_43_FireStationJurisdiction.shp",
        "validation",
    ),
    ("emergency_transport_roads", RAW / "mlit_ksj_n10_2024_kumamoto" / "N10-24_43.geojson", "core"),
    ("road_centerlines_4829", RAW / "mlit_ksj_n13_2024_mesh_4829" / "N13-24_4829.geojson", "core"),
    ("road_centerlines_4830", RAW / "mlit_ksj_n13_2024_mesh_4830" / "N13-24_4830.geojson", "core"),
    ("road_centerlines_4831", RAW / "mlit_ksj_n13_2024_mesh_4831" / "N13-24_4831.geojson", "core"),
    ("road_centerlines_4930", RAW / "mlit_ksj_n13_2024_mesh_4930" / "N13-24_4930.geojson", "core"),
    ("road_centerlines_4931", RAW / "mlit_ksj_n13_2024_mesh_4931" / "N13-24_4931.geojson", "core"),
    ("landslide_warning_zones", RAW / "mlit_ksj_a33_2025_kumamoto" / "A33-25_43Polygon.geojson", "scenario"),
    ("evacuation_facilities", RAW / "mlit_ksj_p20_2012_kumamoto" / "P20-12_43.shp", "context"),
)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    inventory: list[dict[str, object]] = []
    variables: list[dict[str, object]] = []

    for logical_name, path, analytical_role in LAYERS:
        if not path.exists():
            raise FileNotFoundError(path)
        info = read_info(path)
        bounds = info["total_bounds"]
        inventory.append(
            {
                "logical_name": logical_name,
                "source_dataset": relative(path),
                "analytical_role": analytical_role,
                "feature_count": int(info["features"]),
                "geometry_type": info["geometry_type"],
                "crs": info["crs"],
                "field_count": len(info["fields"]),
                "min_x": bounds[0],
                "min_y": bounds[1],
                "max_x": bounds[2],
                "max_y": bounds[3],
                "encoding": info.get("encoding", ""),
            }
        )
        for field, dtype in zip(info["fields"], info["dtypes"], strict=True):
            variables.append(
                {
                    "logical_name": logical_name,
                    "source_dataset": relative(path),
                    "original_name": field,
                    "dtype": dtype,
                    "geometry_type": info["geometry_type"],
                    "analytical_role": analytical_role,
                    "readable_name": "",
                    "full_name": "",
                    "is_final_variable": "",
                }
            )

    inventory_path = OUTPUT / "geospatial_layer_inventory.csv"
    with inventory_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(inventory[0]))
        writer.writeheader()
        writer.writerows(inventory)

    variables_path = ROOT / "data" / "exp" / "data-preprocessing" / "geospatial_variable_list.csv"
    variables_path.parent.mkdir(parents=True, exist_ok=True)
    with variables_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(variables[0]))
        writer.writeheader()
        writer.writerows(variables)

    print(f"Layers: {len(inventory)}")
    print(f"Features: {sum(int(row['feature_count']) for row in inventory):,}")
    print(f"Variables: {len(variables)}")
    print(f"Inventory: {relative(inventory_path)}")
    print(f"Variables: {relative(variables_path)}")


if __name__ == "__main__":
    main()
