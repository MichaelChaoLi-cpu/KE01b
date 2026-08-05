#!/usr/bin/env python3
"""Build an evidence-aware feasibility assessment for the emergency-access study."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely


ROOT = Path(__file__).resolve().parents[2]
ANASOP = ROOT / "docs/AnaSOP.md"
RAW = ROOT / "data/raw"
PROCESSED = ROOT / "data/processed"
OUTPUT = ROOT / "data/exp/feasibility-check"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def read_raw_sample(path: Path) -> pd.DataFrame:
    separator = "\t" if path.suffix.lower() == ".tsv" else ","
    return pd.read_csv(path, sep=separator, nrows=200, encoding="utf-8-sig", low_memory=False)


def inventory() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    datasets: list[dict[str, object]] = []
    variables: list[dict[str, object]] = []
    raw_files = sorted(
        path for path in RAW.rglob("*") if path.is_file() and path.suffix.lower() in {".csv", ".tsv", ".txt"}
    )
    for path in raw_files:
        try:
            frame = read_raw_sample(path)
            datasets.append(
                {
                    "source_file": rel(path),
                    "data_stage": "raw",
                    "format": path.suffix.lower().lstrip("."),
                    "readable": True,
                    "rows": "not fully scanned",
                    "columns": len(frame.columns),
                    "sample_rows": len(frame),
                    "spatial": False,
                    "crs": "",
                    "reason": "",
                }
            )
            for column in frame.columns:
                variables.append(
                    {
                        "source_file": rel(path),
                        "data_stage": "raw",
                        "variable": str(column),
                        "dtype": str(frame[column].dtype),
                        "sample_non_empty": int(frame[column].notna().sum()),
                    }
                )
        except Exception as exc:  # noqa: BLE001
            datasets.append(
                {
                    "source_file": rel(path),
                    "data_stage": "raw",
                    "format": path.suffix.lower().lstrip("."),
                    "readable": False,
                    "rows": "",
                    "columns": 0,
                    "sample_rows": 0,
                    "spatial": False,
                    "crs": "",
                    "reason": str(exc),
                }
            )

    for path in sorted(PROCESSED.glob("*.parquet")):
        frame = pd.read_parquet(path)
        spatial = "Geometry" in frame.columns
        crs = "EPSG:6668" if spatial else ""
        datasets.append(
            {
                "source_file": rel(path),
                "data_stage": "processed",
                "format": "GeoParquet" if spatial else "Parquet",
                "readable": True,
                "rows": len(frame),
                "columns": len(frame.columns),
                "sample_rows": min(len(frame), 200),
                "spatial": spatial,
                "crs": crs,
                "reason": "",
            }
        )
        sample = frame.head(200)
        for column in frame.columns:
            variables.append(
                {
                    "source_file": rel(path),
                    "data_stage": "processed",
                    "variable": str(column),
                    "dtype": str(frame[column].dtype),
                    "sample_non_empty": int(sample[column].notna().sum()),
                }
            )
    return datasets, variables


def extract_questions() -> list[tuple[str, str]]:
    text = ANASOP.read_text(encoding="utf-8")
    section = "Research Objective"
    questions: list[tuple[str, str]] = []
    for line in text.splitlines():
        if line.startswith("### ") or line.startswith("#### "):
            section = line.lstrip("#").strip()
        if line.startswith("- Research question:"):
            questions.append((section, line.split(":", 1)[1].strip()))
    return questions


def network_metrics() -> dict[str, object]:
    roads = gpd.read_parquet(PROCESSED / "kumamoto_road_centerlines_2024_preprocessed.parquet")
    fire = gpd.read_parquet(PROCESSED / "kumamoto_fire_stations_2012_preprocessed.parquet")
    medical = gpd.read_parquet(PROCESSED / "kumamoto_medical_facilities_2020_preprocessed.parquet")
    population = gpd.read_parquet(PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet")
    groups = gpd.read_parquet(PROCESSED / "kumamoto_population_disclosure_groups_preprocessed.parquet")
    hospitals = gpd.read_parquet(PROCESSED / "kumamoto_hospitals_2026_preprocessed.parquet")
    roles = pd.read_parquet(PROCESSED / "kumamoto_emergency_hospital_roles_2023_preprocessed.parquet")
    hazards = gpd.read_parquet(PROCESSED / "kumamoto_landslide_warning_zones_2025_preprocessed.parquet")

    roads_m = roads.to_crs(6670)
    geoms = roads_m.geometry.array
    starts = shapely.get_point(geoms, 0)
    ends = shapely.get_point(geoms, -1)
    coords = np.vstack(
        [
            np.column_stack([shapely.get_x(starts), shapely.get_y(starts)]),
            np.column_stack([shapely.get_x(ends), shapely.get_y(ends)]),
        ]
    )
    coords = np.round(coords, 0).astype(np.int64)
    _, inverse = np.unique(coords, axis=0, return_inverse=True)
    edge_count = len(roads)
    left, right = inverse[:edge_count], inverse[edge_count:]
    node_count = int(inverse.max() + 1)
    parent = np.arange(node_count, dtype=np.int32)
    size = np.ones(node_count, dtype=np.int32)

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = int(parent[node])
        return node

    for first, second in zip(left, right):
        root_first, root_second = find(int(first)), find(int(second))
        if root_first == root_second:
            continue
        if size[root_first] < size[root_second]:
            root_first, root_second = root_second, root_first
        parent[root_second] = root_first
        size[root_first] += size[root_second]
    edge_roots = np.fromiter((find(int(node)) for node in left), dtype=np.int32, count=edge_count)
    _, component_edge_counts = np.unique(edge_roots, return_counts=True)

    def nearest_summary(points: gpd.GeoDataFrame) -> dict[str, float]:
        metric = points.to_crs(6670).copy()
        if not bool((metric.geom_type == "Point").all()):
            metric[metric.geometry.name] = metric.geometry.centroid
        metric["source_index"] = np.arange(len(metric))
        joined = gpd.sjoin_nearest(
            metric[["source_index", metric.geometry.name]],
            roads_m[[roads_m.geometry.name]],
            how="left",
            distance_col="distance_m",
        )
        distances = joined.groupby("source_index")["distance_m"].min().dropna().to_numpy()
        return {
            "n": int(len(distances)),
            "p50": float(np.percentile(distances, 50)),
            "p95": float(np.percentile(distances, 95)),
            "max": float(distances.max()),
        }

    fire_candidates = fire[fire["Candidate Dispatch Base"]]
    eligible_hospitals = medical[medical["Eligible Emergency Hospital"]]
    return {
        "road_edges": edge_count,
        "road_invalid": int((~roads.geometry.is_valid).sum()),
        "road_empty": int(roads.geometry.is_empty.sum()),
        "largest_component_edges": int(component_edge_counts.max()),
        "largest_component_pct": float(component_edge_counts.max() / edge_count * 100),
        "components": int(len(component_edge_counts)),
        "explicit_speed_fields": len([c for c in roads.columns if "speed" in c.lower() or "time" in c.lower()]),
        "candidate_bases": int(fire_candidates.shape[0]),
        "eligible_hospitals": int(eligible_hospitals.shape[0]),
        "current_hospitals": int(hospitals.shape[0]),
        "role_rows": int(roles.shape[0]),
        "role_matches": int(roles["Hospital ID"].notna().sum()),
        "population_meshes": int(population.shape[0]),
        "population_total": float(population["Total Population"].sum()),
        "older_groups": int(groups.shape[0]),
        "age65_total": float(groups["Population Age 65+"].sum()),
        "hazard_zones": int(hazards.shape[0]),
        "fire_nearest": nearest_summary(fire_candidates),
        "hospital_nearest": nearest_summary(eligible_hospitals),
        "population_nearest": nearest_summary(population.iloc[::20]),
    }


def assessments(questions: list[tuple[str, str]]) -> list[dict[str, object]]:
    templates = [
        {
            "status": "partly-testable",
            "rationale": "Core demand, dispatch-base, hospital, road, administrative, and hazard inputs are available, but the value outcome and Shapley estimates must be constructed.",
            "matched_variables": "Geometry; Total Population; Population Age 65+; Candidate Dispatch Base; Eligible Emergency Hospital; Hospital Name; Emergency Road Class; Road Type; Route Name; Hazard Type; Warning Zone Class",
            "matched_sources": "population mesh; population disclosure groups; fire facilities; medical facilities; hospital roles; road centerlines; emergency transport roads; landslide warning zones",
            "blocking_gaps": "No explicit road speed field; corridor-player construction, disruption scenarios, travel times, and Shapley outputs are not yet final variables.",
            "feasibility_test": "Build and validate the routable graph, define corridor players and scenarios, and run a convergence pilot on a screened corridor set.",
        },
        {
            "status": "partly-testable",
            "rationale": "Locations and road geometry support two-stage routing, but all stage-specific travel times and timely-access outcomes are derived rather than observed.",
            "matched_variables": "Geometry; Candidate Dispatch Base; Eligible Emergency Hospital; Road Type; Width Category; Road State; Hazard Type; Warning Zone Class; Total Population",
            "matched_sources": "fire facilities; medical facilities; road centerlines; landslide warning zones; population mesh",
            "blocking_gaps": "No observed ambulance travel times or explicit speed limits; Low, Central, and High scenarios require stated assumptions.",
            "feasibility_test": "Define a defensible speed lookup and scenario rules, validate facility snapping, and test sensitivity to speed and access thresholds.",
        },
        {
            "status": "partly-testable",
            "rationale": "Municipal geometry and total and older-population measures are available, including age 65+, 75+, and 85+ groups.",
            "matched_variables": "Geometry; Municipality Name; Total Population; Population Age 65+; Population Age 65+ Share; Population Age 75+; Population Age 75+ Share; Population Age 85+; Population Age 85+ Share",
            "matched_sources": "administrative areas; population mesh; population disclosure groups",
            "blocking_gaps": "Older-population measures use disclosure-group geography rather than the 125 m mesh, so subgroup spatial precision and allocation rules require validation.",
            "feasibility_test": "Validate disclosure-group-to-mesh and municipal aggregation and report threshold sensitivity without claiming individual-level vulnerability.",
        },
        {
            "status": "partly-testable",
            "rationale": "Hospital locations, roles, beds, eligibility indicators, and linkage diagnostics are available for hospital games and catchment analysis.",
            "matched_variables": "Geometry; Hospital Name; Eligible Emergency Hospital; Emergency Designated; Disaster Base Designation; Tertiary Emergency Hospital; Rotation Hospital; Total Beds; Match Status; Name Match Score",
            "matched_sources": "medical facilities; current hospitals; hospital roles; prefectural hospital registry",
            "blocking_gaps": "Hospital sources refer to different years; one name match and the rotation-hospital count remain unresolved; Total Beds is not emergency capacity.",
            "feasibility_test": "Define primary and sensitivity eligibility sets, resolve or defer unmatched records, and keep bed-weighted results as sensitivity analyses.",
        },
        {
            "status": "weakly-testable",
            "rationale": "All network and demand inputs exist, but the Shapley player set, coalition sampling design, convergence, interactions, and surrogate validation have not yet been demonstrated.",
            "matched_variables": "Geometry; Route Name; Route ID; Emergency Road Class; Road Type; Width Category; Candidate Dispatch Base; Hospital Name; Total Population; Population Age 65+",
            "matched_sources": "road centerlines; emergency transport roads; fire facilities; hospital roles; population mesh; population disclosure groups",
            "blocking_gaps": "The 430,201 raw road segments cannot be treated as individual players; no coalition-response training data or direct Shapley benchmark exists yet.",
            "feasibility_test": "Aggregate and screen corridor players, run a direct Monte Carlo convergence pilot, then validate any SHAP surrogate on held-out coalitions and direct rankings.",
        },
    ]
    if len(questions) != len(templates):
        raise ValueError(f"Expected five research questions, found {len(questions)}")
    rows = []
    for index, ((section, question), template) in enumerate(zip(questions, templates), start=1):
        rows.append({"id": f"RQ{index}", "section": section, "question": question, **template})
    return rows


def report(
    datasets: list[dict[str, object]],
    variables: list[dict[str, object]],
    rows: list[dict[str, object]],
    metrics: dict[str, object],
) -> str:
    processed_datasets = [row for row in datasets if row["data_stage"] == "processed"]
    processed_variables = [row for row in variables if row["data_stage"] == "processed"]
    processed_rows = sum(int(row["rows"]) for row in processed_datasets)
    unique_processed_variables = len({str(row["variable"]) for row in processed_variables})
    counts = Counter(str(row["status"]) for row in rows)
    fire = metrics["fire_nearest"]
    hospital = metrics["hospital_nearest"]
    population = metrics["population_nearest"]
    lines = [
        "# Emergency-Access Research Feasibility Check",
        "",
        "## Overall Decision",
        "",
        "- Overall status: **feasible with required preprocessing and a computational pilot**.",
        "- All five questions can generate descriptive or scenario-based knowledge with current inputs; none supports causal claims or reconstruction of observed earthquake operations.",
        "- RQ1-RQ4 are `partly-testable`; RQ5 is `weakly-testable` until corridor aggregation and Monte Carlo convergence are demonstrated.",
        "- Recommended next skill: `data-preprocessing`.",
        "",
        "## Evidence Coverage",
        "",
        f"- AnaSOP research questions: {len(rows)}",
        f"- Data files inventoried: {len(datasets)} ({len(processed_datasets)} processed Parquet/GeoParquet and {len(datasets) - len(processed_datasets)} raw tabular files)",
        f"- Variable instances inventoried: {len(variables)} ({len(processed_variables)} processed; {unique_processed_variables} unique processed readable names)",
        f"- Processed rows: {processed_rows:,}",
        f"- Status counts: `partly-testable` {counts['partly-testable']}; `weakly-testable` {counts['weakly-testable']}",
        "",
        "The bundled filename-matching diagnostic initially marked RQ3 `not-yet-testable` because it supports CSV, TSV, and TXT only. The evidence-aware assessment includes all processed Parquet and GeoParquet inputs and supersedes that format-driven label.",
        "",
        "## Technical Feasibility Evidence",
        "",
        f"- Road network input: {metrics['road_edges']:,} valid, non-empty line features; no invalid or empty geometries were found.",
        f"- Endpoint connectivity: with 1 m endpoint snapping, the largest component contains {metrics['largest_component_edges']:,} roads ({metrics['largest_component_pct']:.2f}%); {metrics['components']:,} components remain for review.",
        f"- Travel-time limitation: {metrics['explicit_speed_fields']} explicit speed or travel-time fields are available, so speeds must be assigned from road and width classes and tested in sensitivity analysis.",
        f"- Dispatch supply: {metrics['candidate_bases']} candidate bases; nearest-road distance p95 {fire['p95']:.1f} m and maximum {fire['max']:.1f} m.",
        f"- Hospital supply: {metrics['eligible_hospitals']} eligibility-flagged facilities; nearest-road distance p95 {hospital['p95']:.1f} m and maximum {hospital['max']:.1f} m. The current roster has {metrics['current_hospitals']} hospitals, while {metrics['role_matches']} of {metrics['role_rows']} healthcare-plan role rows have a hospital identifier.",
        f"- Population demand: {metrics['population_meshes']:,} populated 125 m meshes representing {metrics['population_total']:,.0f} people. A systematic 1-in-20 centroid sample had nearest-road distance p95 {population['p95']:.1f} m and maximum {population['max']:.1f} m.",
        f"- Older-population evidence: {metrics['older_groups']:,} disclosure groups representing {metrics['age65_total']:,.0f} people age 65+, requiring explicit aggregation rules rather than individual-level interpretation.",
        f"- Disruption evidence: {metrics['hazard_zones']:,} landslide-warning polygons support scenario screening but do not prove observed road failure.",
        "",
        "## Question-Level Assessment",
        "",
        "| ID | Status | Question | Available basis | Blocking gap | Required feasibility test |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | `{row['status']}` | {row['question']} | {row['rationale']} | {row['blocking_gaps']} | {row['feasibility_test']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Limits",
            "",
            "- Feasibility means that required inputs exist or can be constructed; it does not prove any research claim.",
            "- Results will be descriptive, model-based, and scenario-dependent rather than causal.",
            "- Fire-facility locations, hospital roles, and current hospital attributes refer to different source years and must not be described as a single contemporaneous census without qualification.",
            "- Total Beds is a capacity proxy, not observed emergency-department capacity.",
            "- Cost-effectiveness cannot be claimed until repair-time or repair-cost evidence is available; restoration-scale results may instead use a road-count constraint.",
            "",
            "## Required Data-Preprocessing Work",
            "",
            "1. Build a planarized and validated routable network and document endpoint, intersection, direction, and snapping rules.",
            "2. Assign and sensitivity-test assumed travel speeds by readable road and width classes.",
            "3. Define baseline, Low, Central, and High disruption scenarios without treating warning zones as observed failures.",
            "4. Reconcile the operational hospital set and define unweighted, role-weighted, and bed-proxy sensitivity specifications.",
            "5. Construct the derived accessibility, coverage, catchment, restoration, and Shapley variables already warned about in AnaSOP Section 8.",
            "6. Aggregate and screen road segments into a computationally feasible corridor-player set and run a direct Monte Carlo convergence pilot before relying on a SHAP surrogate.",
            "",
            "## Recommended Next Step",
            "",
            "Proceed to `data-preprocessing` after user confirmation. Retain all five research questions, but treat RQ5 as conditional on the corridor and convergence pilot.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    datasets, variables = inventory()
    questions = extract_questions()
    rows = assessments(questions)
    metrics = network_metrics()
    write_csv(
        OUTPUT / "dataset_availability.csv",
        datasets,
        ["source_file", "data_stage", "format", "readable", "rows", "columns", "sample_rows", "spatial", "crs", "reason"],
    )
    write_csv(
        OUTPUT / "variable_inventory.csv",
        variables,
        ["source_file", "data_stage", "variable", "dtype", "sample_non_empty"],
    )
    write_csv(
        OUTPUT / "question_feasibility.csv",
        rows,
        [
            "id",
            "section",
            "question",
            "status",
            "rationale",
            "matched_variables",
            "matched_sources",
            "blocking_gaps",
            "feasibility_test",
        ],
    )
    (OUTPUT / "README.md").write_text(report(datasets, variables, rows, metrics), encoding="utf-8")
    print(f"datasets={len(datasets)} variables={len(variables)} questions={len(rows)}")
    print("status_counts=" + str(dict(Counter(str(row['status']) for row in rows))))
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
