#!/usr/bin/env python3
"""Extend confirmed preprocessing decisions with network and model-ready variables."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "data" / "exp" / "data-preprocessing"
DECISIONS = EXP / "decisions.json"
VARIABLE_LIST = EXP / "variable_list.csv"
README = EXP / "README.md"
LOGICAL_PREFIX = "logical:analysis_"

ROAD_STRUCTURE = [
    "Road Edge ID", "From Node ID", "To Node ID", "Network Component ID", "Medical Corridor ID",
    "Road Length (m)", "Assumed Speed (km/h)", "Baseline Edge Travel Time (min)",
    "Hazard Exposure Class", "Emergency Route Membership", "Road Available", "Network Analysis Eligible",
]
NETWORK_ACCESS = [
    "Analysis Unit ID", "Demand Node ID", "Dispatch Base Node ID", "Hospital Node ID",
    "Network Snap Distance (m)", "Operational Hospital Set", "Hospital Role Weight", "Hospital Capacity Weight",
]
ACCESSIBILITY = [
    "Disruption Scenario", "Timely Access Threshold (min)", "Dispatch Travel Time", "Hospital Transport Time",
    "Total Emergency Access Time", "Access Time Increase", "Timely Access Status", "Assigned Hospital",
    "Alternative Hospital Count", "Hospital Catchment Population", "Hospital Demand Change",
    "Population Losing Timely Access", "Older Population Losing Timely Access",
]
RESTORATION = [
    "Restored Population", "Restored Older Population", "Travel Time Reduction", "Connected Hospital Count",
    "Network Redundancy Value", "Restoration Scale", "Restoration Budget", "Coverage Recovery",
    "Marginal Restoration Benefit", "Restoration Rank", "Scenario Priority Rank", "Priority Selection Frequency",
]
SHAPLEY = [
    "Road Shapley Value", "Hospital Shapley Value", "Road-Hospital Shapley Value", "Shapley Standard Error",
    "Monte Carlo Permutations", "Shapley Convergence Status", "Surrogate Prediction Error",
    "Direct-Surrogate Rank Difference",
]
APPROVED_VARIABLES = ROAD_STRUCTURE + NETWORK_ACCESS + ACCESSIBILITY + RESTORATION + SHAPLEY
REFERENCE_FIELDS = ["Network Node ID", "Network Snap Accepted", "Access Road Edge ID", "Access Edge Fraction"]
GROUP_REFERENCE_FIELD = "Representative Mesh Code"


def variable(name: str, final: bool = True, preprocessing: list[str] | None = None) -> dict[str, object]:
    full_name = name.replace(" ID", " Identifier") if name.endswith(" ID") else name
    return {
        "original_name": f"derived:{name}",
        "readable_name": name,
        "full_name": full_name,
        "is_final_variable": "yes" if final else "no",
        "preprocessing": preprocessing or [],
    }


def item(source: str, output: str | None, script: str | None, names: list[str], stage: str) -> dict[str, object]:
    return {
        "source": source,
        "output": output,
        "script": script,
        "materialization_stage": stage,
        "variables": [variable(name, final=name != "Restoration Budget") for name in names],
    }


def extend_decisions() -> dict[str, object]:
    payload = json.loads(DECISIONS.read_text(encoding="utf-8"))
    datasets = payload["datasets"]
    for key in [key for key in datasets if key.startswith(LOGICAL_PREFIX)]:
        del datasets[key]
    datasets.update({
        "logical:analysis_routable_road_edges": item(
            "Derived from confirmed Standard Road centerlines, emergency routes, and landslide zones",
            "data/processed/kumamoto_routable_road_edges_preprocessed.parquet",
            "src/preprocessing/preprocess_routable_road_network.py",
            ROAD_STRUCTURE,
            "preprocessing",
        ),
        "logical:analysis_routable_road_nodes": item(
            "Derived one-metre grade-aware network nodes",
            "data/processed/kumamoto_routable_road_nodes_preprocessed.parquet",
            "src/preprocessing/preprocess_routable_road_network.py",
            REFERENCE_FIELDS[:1] + ["Network Component ID", "Network Analysis Eligible"],
            "preprocessing",
        ),
        "logical:analysis_dispatch_access": item(
            "Candidate fire-station dispatch bases snapped to the eligible road network",
            "data/processed/kumamoto_dispatch_base_network_access_preprocessed.parquet",
            "src/preprocessing/preprocess_emergency_network_access.py",
            ["Dispatch Base Node ID", "Network Snap Distance (m)"] + REFERENCE_FIELDS[1:],
            "preprocessing",
        ),
        "logical:analysis_hospital_access": item(
            "Eligible emergency hospitals snapped to the eligible road network",
            "data/processed/kumamoto_hospital_network_access_preprocessed.parquet",
            "src/preprocessing/preprocess_emergency_network_access.py",
            ["Hospital Node ID", "Network Snap Distance (m)", "Operational Hospital Set", "Hospital Role Weight", "Hospital Capacity Weight"] + REFERENCE_FIELDS[1:],
            "preprocessing",
        ),
        "logical:analysis_population_mesh_access": item(
            "Population-mesh centroids snapped to the eligible road network",
            "data/processed/kumamoto_population_mesh_network_access_preprocessed.parquet",
            "src/preprocessing/preprocess_emergency_network_access.py",
            ["Analysis Unit ID", "Demand Node ID", "Network Snap Distance (m)"] + REFERENCE_FIELDS[1:],
            "preprocessing",
        ),
        "logical:analysis_population_group_access": item(
            "Aggregation-destination mesh centroids snapped without reallocating older-population counts to meshes",
            "data/processed/kumamoto_population_group_network_access_preprocessed.parquet",
            "src/preprocessing/preprocess_emergency_network_access.py",
            ["Analysis Unit ID", "Demand Node ID", "Network Snap Distance (m)"] + REFERENCE_FIELDS[1:] + [GROUP_REFERENCE_FIELD],
            "preprocessing",
        ),
        "logical:analysis_estimation_output_contract": item(
            "Approved variables to be computed during accessibility, restoration, and Shapley estimation",
            None,
            None,
            ACCESSIBILITY + RESTORATION + SHAPLEY,
            "estimation",
        ),
    })
    # Connector fields are retained for reproducibility but not article-facing.
    for dataset in datasets.values():
        for entry in dataset["variables"]:
            if entry["readable_name"] in REFERENCE_FIELDS + [GROUP_REFERENCE_FIELD]:
                entry["is_final_variable"] = "no"
    payload["schema_version"] = 2
    payload["confirmed_analysis_variable_count"] = len(APPROVED_VARIABLES)
    payload["notes"] = [
        "The 53 approved analysis variables are defined here; accessibility, restoration, and Shapley outcomes are not estimated during preprocessing.",
        "Restoration Budget is retained as a non-final reference until empirical repair cost or duration data are available.",
    ]
    DECISIONS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def extend_variable_list(payload: dict[str, object]) -> None:
    with VARIABLE_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = [row for row in reader if not row["source_dataset"].startswith(LOGICAL_PREFIX)]
    for key, dataset in payload["datasets"].items():
        if not key.startswith(LOGICAL_PREFIX):
            continue
        for entry in dataset["variables"]:
            rows.append({
                "source_dataset": key,
                "original_name": entry["original_name"],
                "dtype": "derived",
                "non_null_count": "",
                "null_pct": "",
                "sample_values": "",
                "feasibility_status": "planned" if dataset["materialization_stage"] == "estimation" else "partly-testable",
                "readable_name": entry["readable_name"],
                "full_name": entry["full_name"],
                "is_final_variable": entry["is_final_variable"],
            })
    with VARIABLE_LIST.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_readme(payload: dict[str, object]) -> None:
    text = README.read_text(encoding="utf-8")
    datasets = payload["datasets"]
    decisions_count = sum(len(dataset["variables"]) for dataset in datasets.values())
    processed_count = sum(bool(dataset.get("output")) for dataset in datasets.values())
    text = re.sub(r"- Confirmed logical datasets: \d+", f"- Confirmed logical datasets: {len(datasets)}", text, count=1)
    text = re.sub(r"- Confirmed variable decisions: \d+", f"- Confirmed variable decisions: {decisions_count}", text, count=1)
    text = re.sub(r"- Processed Parquet/GeoParquet outputs: \d+", f"- Processed Parquet/GeoParquet outputs: {processed_count}", text, count=1)
    layer_specs = [
        ("Routable Standard Road edges", "kumamoto_routable_road_edges_preprocessed.parquet", "Core network"),
        ("Grade-aware road nodes", "kumamoto_routable_road_nodes_preprocessed.parquet", "Core network"),
        ("Dispatch-base network access", "kumamoto_dispatch_base_network_access_preprocessed.parquet", "Core network access"),
        ("Emergency-hospital network access", "kumamoto_hospital_network_access_preprocessed.parquet", "Core network access"),
        ("Population-mesh network access", "kumamoto_population_mesh_network_access_preprocessed.parquet", "Core network access"),
        ("Population-group network access", "kumamoto_population_group_network_access_preprocessed.parquet", "Core older-population access"),
    ]
    layer_rows: list[str] = []
    for label, filename, status in layer_specs:
        metadata = pq.read_metadata(ROOT / "data/processed" / filename)
        layer_rows.append(f"| {label} | {metadata.num_rows:,} | {metadata.num_columns} | {status} |")
    rows = "\n".join(layer_rows)
    marker_start = "<!-- ANALYSIS-LAYERS-START -->"
    marker_end = "<!-- ANALYSIS-LAYERS-END -->"
    block = (
        f"{marker_start}\n{rows}\n{marker_end}\n\n"
        "### Second-stage network preprocessing\n\n"
        "- Confirmed analysis-facing variables: 53 (road structure, network access, accessibility, restoration, and Shapley validation).\n"
        "- Ambulance routing uses Standard Road centerlines only; endpoints and same-level intersections are snapped/noded on a 1 m grid in EPSG:6670.\n"
        "- All valid Standard Road components remain eligible so island and remote-area demand is not silently deleted; component IDs preserve disconnected-network status.\n"
        "- Facility access is accepted within 150 m and population access within 250 m; rejected snaps remain in the files with an explicit flag.\n"
        "- Medical corridors are connected road-category subnetworks within secondary meshes; Shapley screening remains capped at 2,000 candidate corridors.\n"
        "- Accessibility, restoration, and Shapley outputs are schema contracts at this stage and have not been estimated.\n"
        "- Older-population disclosure groups use their source-defined aggregation-destination mesh centroid; group counts are not duplicated or proportionally imputed to 125 m meshes.\n"
    )
    if marker_start in text:
        text = re.sub(re.escape(marker_start) + r".*?(?=Validation notes:)", block + "\n", text, flags=re.S)
    else:
        text = text.replace("Validation notes:\n", block + "\nValidation notes:\n", 1)
    README.write_text(text, encoding="utf-8")


def main() -> None:
    payload = extend_decisions()
    extend_variable_list(payload)
    update_readme(payload)
    print(
        f"Extended decisions to {len(payload['datasets'])} logical datasets; "
        f"confirmed analysis variables: {len(APPROVED_VARIABLES)}"
    )


if __name__ == "__main__":
    main()
