#!/usr/bin/env python3
"""Independently validate the R1C2 pilot/extension and attach stable grid IDs."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", type=Path, required=True)
    parser.add_argument("--full", type=Path, required=True)
    args = parser.parse_args()
    pilot = pd.read_parquet(args.pilot / "replicate_metrics.parquet")
    full = pd.read_parquet(args.full / "replicate_metrics.parquet")
    keys = ["replicate", "severity", "scenario"]
    pd.testing.assert_frame_equal(pilot.sort_values(keys).reset_index(drop=True), full.loc[full.replicate <= 100].sort_values(keys).reset_index(drop=True), check_exact=True)
    pd.testing.assert_frame_equal(pd.read_parquet(args.pilot / "undamaged_metrics.parquet"), pd.read_parquet(args.full / "undamaged_metrics.parquet"), check_exact=True)
    report = json.loads((args.full / "experiment_summary.json").read_text())
    assert report["status"] == "pass" and report["replicates"] == 1000
    for name, expected in report["input_sha256"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    assert len(full) == 12000 and not full.duplicated(keys).any()
    assert (full.paired_coverage_change <= 0).all()
    assert full.groupby(["replicate", "severity"]).newly_disconnected_population.nunique().max() == 1
    grid = pd.read_parquet(args.full / "grid_probabilities.parquet")
    source = pd.read_parquet(ROOT / "data/processed/kumamoto_population_mesh_network_access_preprocessed.parquet", columns=["Mesh Code", "Analysis Unit ID", "Demand Node ID", "Total Population"])
    assert source["Analysis Unit ID"].notna().all() and source["Analysis Unit ID"].is_unique
    frames = []
    probability_differences = []
    for (severity, scenario), frame in grid.groupby(["severity", "scenario"], sort=False):
        frame = frame.reset_index(drop=True)
        assert len(frame) == len(source)
        np.testing.assert_array_equal(frame.demand_id, source["Demand Node ID"].astype("string").fillna("").astype(str))
        np.testing.assert_array_equal(frame.population, source["Total Population"].fillna(0))
        frame["mesh_code"] = source["Mesh Code"].to_numpy()
        frame["analysis_unit_id"] = source["Analysis Unit ID"].to_numpy()
        frame["source_row_index"] = np.arange(len(source))
        frames.append(frame)
        base = grid.loc[grid.severity.eq(severity) & grid.scenario.eq("baseline")].reset_index(drop=True)
        delta = frame.timely_probability - base.timely_probability
        assert (delta <= 1e-12).all()
        pop = frame.population.to_numpy()
        probability_differences.append({"severity": float(severity), "scenario": scenario, "population_weighted_timely_probability_change_pp": float(100*np.dot(delta, pop)/pop.sum()), "grid_absolute_probability_change_p95_pp": float(100*np.quantile(abs(delta), .95)), "grids_with_lower_probability": int((delta < -1e-12).sum())})
    identified = pd.concat(frames, ignore_index=True)
    assert not identified.duplicated(["severity", "scenario", "analysis_unit_id"]).any()
    identified.to_parquet(args.full / "grid_probabilities_identified.parquet", index=False)
    validation = {"status": "pass", "pilot_first_100_exact_match": True, "undamaged_exact_match": True, "input_hashes_verified": True, "rows": len(full), "unique_grids": len(source), "total_population": float(source["Total Population"].sum()), "stable_grid_identifier": "analysis_unit_id (source Analysis Unit ID); demand_id can be empty for rejected connectors", "grid_changes": probability_differences}
    (args.full / "validation_summary.json").write_text(json.dumps(validation, indent=2)+"\n")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
