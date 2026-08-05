#!/usr/bin/env python3
"""Write the confirmed preprocessing decisions and generator subset."""

from __future__ import annotations

import json
from pathlib import Path

from emergency_access_common import PREFECTURE_HOSPITAL_COLUMNS, ROOT, hospital_facility_mapping, speciality_hours_mapping


def variables(mapping: dict[str, str], final: bool = True) -> list[dict[str, object]]:
    return [
        {
            "original_name": original,
            "readable_name": readable,
            "full_name": readable.replace(" ID", " Identifier") if readable.endswith(" ID") else readable,
            "is_final_variable": "yes" if final else "no",
            "preprocessing": [],
        }
        for original, readable in mapping.items()
    ]


def item(source: str, output: str, script: str, mapping: dict[str, str], final: bool = True) -> dict[str, object]:
    return {"source": source, "output": output, "script": script, "variables": variables(mapping, final)}


def main() -> None:
    tabular = {
        "data/raw/emergency_access/extracted/mhlw_hospital_facility_20260601/01-1_hospital_facility_info_20260601.csv": item("MHLW hospital facility open data", "data/processed/kumamoto_hospitals_2026_preprocessed.parquet", "src/preprocessing/preprocess_mhlw_hospitals.py", hospital_facility_mapping() | {"derived:geometry": "Geometry"}),
        "data/raw/emergency_access/extracted/mhlw_hospital_speciality_hours_20260601/01-2_hospital_speciality_hours_20260601.csv": item("MHLW specialty and consultation-hours open data", "data/processed/kumamoto_hospital_speciality_hours_2026_preprocessed.parquet", "src/preprocessing/preprocess_mhlw_speciality_hours.py", speciality_hours_mapping(), False),
    }
    datasets = dict(tabular)
    datasets.update({
        "logical:administrative_areas": item("MLIT N03 2025", "data/processed/kumamoto_administrative_areas_preprocessed.parquet", "src/preprocessing/preprocess_administrative_areas.py", {"N03_001": "Prefecture Name", "N03_002": "Subprefecture Name", "N03_003": "District Name", "N03_004": "Municipality Name", "N03_005": "Ward Name", "N03_007": "Municipality Code", "derived:municipality label": "Municipality Label", "geometry": "Geometry"}),
        "logical:medical_facilities": item("MLIT P04 2020", "data/processed/kumamoto_medical_facilities_2020_preprocessed.parquet", "src/preprocessing/preprocess_medical_facilities.py", {f"P04_{i:03d}": n for i, n in enumerate(["Medical Facility Class Code", "Facility Name", "Address", "Medical Departments 1", "Medical Departments 2", "Medical Departments 3", "Operator Class Code", "Bed Count", "Emergency Designation Code", "Disaster Base Designation Code"], 1)} | {"derived:facility class label": "Medical Facility Class", "derived:emergency designation label": "Emergency Designation", "derived:disaster base label": "Disaster Base Designation", "derived:eligibility flag": "Eligible Emergency Hospital", "geometry": "Geometry"}),
        "logical:fire_stations": item("MLIT P17 fire stations 2012", "data/processed/kumamoto_fire_stations_2012_preprocessed.parquet", "src/preprocessing/preprocess_fire_stations.py", {"P17_001": "Fire Facility Name", "P17_002": "Municipality Code", "P17_003": "Fire Facility Type Code", "P17_004": "Address", "derived:facility type label": "Fire Facility Type", "derived:dispatch-base flag": "Candidate Dispatch Base", "geometry": "Geometry"}),
        "logical:fire_jurisdictions": item("MLIT P17 fire jurisdictions 2012", "data/processed/kumamoto_fire_jurisdictions_2012_preprocessed.parquet", "src/preprocessing/preprocess_fire_jurisdictions.py", {"P17_005": "Fire Station Name"} | {f"P17_{i:03d}": f"Jurisdiction Area {i - 5}" for i in range(6, 27)} | {"geometry": "Geometry"}, False),
        "logical:emergency_transport_roads": item("MLIT N10 2024; archive fields use N01 prefix", "data/processed/kumamoto_emergency_transport_roads_2024_preprocessed.parquet", "src/preprocessing/preprocess_emergency_transport_roads.py", {f"N01_{i:03d}": n for i, n in enumerate(["Prefecture Code", "Emergency Road Class Code", "Road Type Code", "Route Name", "Route ID", "Branch ID", "Source Name", "Source Date", "Service Status", "Notes"], 1)} | {"derived:emergency-road label": "Emergency Road Class", "derived:road-type label": "Road Type", "geometry": "Geometry"}),
        "logical:road_centerlines": item("MLIT N13 2024 five meshes", "data/processed/kumamoto_road_centerlines_2024_preprocessed.parquet", "src/preprocessing/preprocess_road_centerlines.py", {f"N13_{i:03d}": n for i, n in enumerate(["Registration Date", "Road Centerline Type Code", "Road Category Code", "Road State Code", "Vertical Level", "Width Category Code", "Toll Category Code", "Secondary Mesh Code"], 1)} | {"derived:centerline-type label": "Road Centerline Type", "derived:road-category label": "Road Category", "derived:road-state label": "Road State", "derived:width label": "Width Category", "derived:toll label": "Toll Category", "geometry": "Geometry"}),
        "logical:landslide_zones": item("MLIT A33 2025", "data/processed/kumamoto_landslide_warning_zones_2025_preprocessed.parquet", "src/preprocessing/preprocess_landslide_zones.py", {f"A33_{i:03d}": n for i, n in enumerate(["Hazard Type Code", "Warning Zone Class Code", "Prefecture Code", "Zone ID", "Zone Name", "Address", "Designation Date", "Special Warning Zone Pending Code"], 1)} | {"derived:hazard label": "Hazard Type", "derived:zone-class label": "Warning Zone Class", "derived:pending label": "Special Warning Zone Pending", "geometry": "Geometry"}),
        "logical:evacuation_facilities": item("MLIT P20 2012", "data/processed/kumamoto_evacuation_facilities_2012_preprocessed.parquet", "src/preprocessing/preprocess_evacuation_facilities.py", {f"P20_{i:03d}": n for i, n in enumerate(["Municipality Code", "Facility Name", "Address", "Facility Type", "Capacity", "Facility Area m2", "Earthquake Hazard", "Tsunami Hazard", "Flood Hazard", "Volcanic Hazard", "Other Hazard", "No Hazard Specified"], 1)} | {"レベル": "Location Accuracy Level", "備考": "Notes", "緯度": "Latitude", "経度": "Longitude", "NO": "Source Record ID", "geometry": "Geometry"}, False),
        "logical:population_mesh": item("KE01 125 m population mesh", "data/processed/kumamoto_population_mesh_125m_preprocessed.parquet", "src/preprocessing/preprocess_population_mesh.py", {name if name != "geometry" else "geometry": name if name != "geometry" else "Geometry" for name in ["Mesh Code", "geometry", "Disclosure Group Code", "Disclosure Group Size", "Disclosure Status", "Aggregation Destination Mesh Code", "Aggregated Source Mesh Codes", "Total Population", "Total Households", "General Households"]}),
        "logical:population_groups": item("KE01 disclosure groups", "data/processed/kumamoto_population_disclosure_groups_preprocessed.parquet", "src/preprocessing/preprocess_population_groups.py", {name if name != "geometry" else "geometry": name if name != "geometry" else "Geometry" for name in ["Disclosure Group Code", "geometry", "Disclosure Group Size", "Suppressed Source Mesh Count", "Total Population", "Total Households", "General Households", "Population Age 65+", "Population Age 75+", "Population Age 85+", "One-Person Households", "Households with Member Age 65+", "Older Single-Person Households", "Older Couple Households", "Population Age 65+ Share", "Population Age 75+ Share", "Population Age 85+ Share", "Older Single-Person Household Share", "Older Couple Household Share"]}),
        "logical:fdma_validation": item("FDMA 2024 multi-row CSV", "data/processed/kumamoto_fire_organization_validation_2024_preprocessed.parquet", "src/preprocessing/preprocess_fdma_validation.py", {f"column_{i}": n for i, n in enumerate(["Prefecture Name", "Fire Headquarters Total", "Municipal Headquarters", "Town Headquarters", "Village Headquarters", "Joint Headquarters", "Fire Stations", "Fire Outposts", "Fire Service Personnel", "Volunteer Fire Corps", "Volunteer Fire Divisions", "Volunteer Firefighters"])}, False),
        "logical:prefecture_hospital_registry": item("Kumamoto Prefecture 2025 multi-row workbook", "data/processed/kumamoto_prefecture_hospital_registry_2025_preprocessed.parquet", "src/preprocessing/preprocess_prefecture_hospital_registry.py", {f"column_{i}": name for i, name in enumerate(PREFECTURE_HOSPITAL_COLUMNS[1:], 1)}, False),
        "logical:emergency_hospital_roles": item("Eighth Kumamoto Healthcare Plan, September 2023 table", "data/processed/kumamoto_emergency_hospital_roles_2023_preprocessed.parquet", "src/preprocessing/preprocess_emergency_hospital_roles.py", {f"derived:{name}": name for name in ["Plan Hospital Name", "Hospital ID", "Matched Hospital Name", "Name Match Score", "Match Status", "Emergency Designated", "Rotation Hospital", "Tertiary Emergency Hospital", "External Reference", "Reference Date"]}),
    })
    output_dir = ROOT / "data/exp/data-preprocessing"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "decisions.json").write_text(json.dumps({"schema_version": 1, "datasets": datasets}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "generator_input_tabular.json").write_text(json.dumps({"datasets": tabular}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote decisions for {len(datasets)} logical datasets")


if __name__ == "__main__":
    main()
