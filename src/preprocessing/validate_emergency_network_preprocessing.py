#!/usr/bin/env python3
"""Validate reproducibility and invariants of the emergency-network preprocessing."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import geopandas as gpd
import numpy as np

from extend_analysis_layer_decisions import APPROVED_VARIABLES


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
EXP = ROOT / "data" / "exp" / "data-preprocessing"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_ascii_columns(frame: gpd.GeoDataFrame) -> None:
    normalized: set[str] = set()
    for column in frame.columns:
        assert column.isascii(), f"Non-ASCII column: {column}"
        key = re.sub(r"\s+", " ", column.strip()).casefold()
        assert key not in normalized, f"Duplicate readable column: {column}"
        normalized.add(key)


def main() -> None:
    report: dict[str, object] = {"checks": {}}
    checks = report["checks"]

    manifest = json.loads((ROOT / "data/raw/emergency_access/source_manifest.json").read_text(encoding="utf-8"))
    checked_sources = 0
    for source in manifest["sources"]:
        path = ROOT / source["local_path"]
        assert path.exists(), f"Missing raw source: {path}"
        assert path.stat().st_size == source["bytes"], f"Raw byte-size mismatch: {path}"
        assert _sha256(path) == source["sha256"], f"Raw checksum mismatch: {path}"
        checked_sources += 1
    checks["raw_source_checksums"] = {"status": "pass", "sources": checked_sources}

    edge_path = PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet"
    node_path = PROCESSED / "kumamoto_routable_road_nodes_preprocessed.parquet"
    edges = gpd.read_parquet(edge_path)
    nodes = gpd.read_parquet(node_path)
    assert edges.crs.to_epsg() == 6668 and nodes.crs.to_epsg() == 6668
    assert len(edges) == edges["Road Edge ID"].nunique()
    assert edges["Road Edge ID"].notna().all()
    assert edges["Road Available"].all() and edges["Network Analysis Eligible"].all()
    assert (edges["Road Length (m)"] > 0).all()
    assert (edges["Assumed Speed (km/h)"] > 0).all()
    expected_time = edges["Road Length (m)"] / (edges["Assumed Speed (km/h)"] * 1000.0 / 60.0)
    assert np.allclose(edges["Baseline Edge Travel Time (min)"], expected_time)
    node_ids = set(nodes["Network Node ID"])
    assert set(edges["From Node ID"]).issubset(node_ids)
    assert set(edges["To Node ID"]).issubset(node_ids)
    assert nodes["Network Node ID"].is_unique
    assert edges["Medical Corridor ID"].notna().all()
    for frame in [edges, nodes]:
        _assert_ascii_columns(frame)
        assert frame.geometry.notna().all() and frame.geometry.is_valid.all()
    checks["road_network"] = {
        "status": "pass",
        "edges": len(edges),
        "nodes": len(nodes),
        "components": int(edges["Network Component ID"].nunique()),
        "largest_component_edges": int(edges["Network Component ID"].value_counts().iloc[0]),
        "medical_corridors": int(edges["Medical Corridor ID"].nunique()),
        "self_loop_edges": int((edges["From Node ID"] == edges["To Node ID"]).sum()),
    }

    access_specs = {
        "dispatch": ("kumamoto_dispatch_base_network_access_preprocessed.parquet", 81, 150.0, "Dispatch Base Node ID"),
        "hospital": ("kumamoto_hospital_network_access_preprocessed.parquet", 75, 150.0, "Hospital Node ID"),
        "population_mesh": ("kumamoto_population_mesh_network_access_preprocessed.parquet", 62945, 250.0, "Demand Node ID"),
        "population_group": ("kumamoto_population_group_network_access_preprocessed.parquet", 36657, 250.0, "Demand Node ID"),
    }
    access_report: dict[str, object] = {}
    for label, (filename, expected_rows, threshold, id_column) in access_specs.items():
        frame = gpd.read_parquet(PROCESSED / filename)
        _assert_ascii_columns(frame)
        assert frame.crs.to_epsg() == 6668 and len(frame) == expected_rows
        accepted = frame["Network Snap Accepted"]
        assert frame.loc[accepted, id_column].notna().all()
        assert frame.loc[~accepted, id_column].isna().all()
        assert (frame.loc[accepted, "Network Snap Distance (m)"] <= threshold + 1e-8).all()
        assert (frame.loc[~accepted, "Network Snap Distance (m)"] > threshold).all()
        access_report[label] = {
            "rows": len(frame),
            "accepted": int(accepted.sum()),
            "rejected": int((~accepted).sum()),
            "maximum_distance_m": float(frame["Network Snap Distance (m)"].max()),
        }
    checks["network_access"] = {"status": "pass", "layers": access_report}

    decisions = json.loads((EXP / "decisions.json").read_text(encoding="utf-8"))
    analysis_entries: dict[str, list[dict[str, object]]] = {}
    for key, dataset in decisions["datasets"].items():
        if not key.startswith("logical:analysis_"):
            continue
        for entry in dataset["variables"]:
            analysis_entries.setdefault(entry["readable_name"], []).append(entry)
    assert len(APPROVED_VARIABLES) == 53 and len(set(APPROVED_VARIABLES)) == 53
    assert set(APPROVED_VARIABLES).issubset(analysis_entries)
    for name in APPROVED_VARIABLES:
        assert name.isascii()
        statuses = {entry["is_final_variable"] for entry in analysis_entries[name]}
        expected = {"no"} if name == "Restoration Budget" else {"yes"}
        assert statuses == expected, f"Unexpected final status for {name}: {statuses}"
    checks["decision_dictionary"] = {
        "status": "pass",
        "logical_datasets": len(decisions["datasets"]),
        "all_variable_decisions": sum(len(dataset["variables"]) for dataset in decisions["datasets"].values()),
        "approved_analysis_variables": len(APPROVED_VARIABLES),
    }

    anasop = (ROOT / "docs/AnaSOP.md").read_text(encoding="utf-8")
    section = re.search(r"(?ms)^## 4\. Variable Construction  /  Key Variables\n.*?(?=^## |\Z)", anasop)
    assert section is not None
    section_text = section.group(0)
    assert "TBD" not in section_text
    assert "data/raw" not in section_text and "source_dataset" not in section_text
    for name in APPROVED_VARIABLES:
        if name != "Restoration Budget":
            assert f"| {name} |" in section_text
    checks["anasop_section_4"] = {
        "status": "pass",
        "final_variable_rows": section_text.count("\n| ") - 1,
        "contains_tbd": False,
    }

    report["status"] = "pass"
    output = EXP / "network_validation.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
