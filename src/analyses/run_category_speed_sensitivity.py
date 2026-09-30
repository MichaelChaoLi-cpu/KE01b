#!/usr/bin/env python3
"""Paired R1C2 speed perturbations with full two-stage rerouting.

Run a 100-replicate pilot or 1000-replicate extension into separate output
directories. Main-model data and existing experimental outputs are read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from monte_carlo_emergency_routing import build_compact_emergency_network
from run_length_weighted_monte_carlo_full import calibrate_intensity

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
FORMAL = ROOT / "data/exp/monte_carlo_length_weighted_full_1000"
SEVERITIES = [0.01, 0.03, 0.05, 0.10]
SEED = 20260806
SCENARIOS = {
    "baseline": None,
    "A_expressway_national_0.8": {
        "National Expressway or Equivalent": 0.8, "National Highway": 0.8,
    },
    "B_prefectural_municipal_0.8": {
        "Prefectural Road": 0.8, "Municipal Road or Equivalent": 0.8,
    },
}
NETWORKS = []
PROBABILITIES = None
BASELINE_FINITE = None


def evaluate(replicate):
    """One paired replicate, or undamaged comparison for replicate zero."""
    net = NETWORKS[0]
    pop = net.demand_population
    scores = np.random.default_rng(np.random.SeedSequence([SEED, replicate])).random(net.road_section_count)
    rows, grids, assignments = [], [], []
    previous = np.zeros(net.road_section_count, dtype=bool)
    for si, severity in enumerate([0.0] if replicate == 0 else SEVERITIES):
        failed = np.zeros(net.road_section_count, dtype=bool) if replicate == 0 else scores < PROBABILITIES[si]
        assert np.all(failed[previous])
        previous = failed
        reference = None
        for scenario, network in zip(SCENARIOS, NETWORKS, strict=True):
            state = network.route(failed, assign_hospitals=True)
            finite = np.isfinite(state.total_time)
            timely = state.total_time <= 30
            if reference is None:
                reference = state
            ref_finite = np.isfinite(reference.total_time)
            assert np.array_equal(finite, ref_finite), "Speed changes cannot change connectivity"
            assert np.all(state.total_time[finite] >= reference.total_time[finite] - 1e-8)
            assert np.all(~timely | (reference.total_time <= 30))
            changed = finite & (state.assigned_hospital_index != reference.assigned_hospital_index)
            assert np.all(state.assigned_hospital_index[finite] >= 0)
            coverage = float(pop[timely].sum())
            rows.append({
                "replicate": replicate, "severity": severity, "scenario": scenario,
                "population_within_30": coverage,
                "paired_coverage_change": coverage - float(pop[reference.total_time <= 30].sum()),
                "newly_disconnected_population": float(pop[BASELINE_FINITE & ~finite].sum()),
                "reachable_population": float(pop[finite].sum()),
                "hospital_reassigned_population": float(pop[changed].sum()),
                "hospital_reassigned_share_reachable": float(pop[changed].sum() / pop[finite].sum()) if pop[finite].sum() else 0.0,
            })
            # Probability denominators are all replicates, including unreachable states.
            grids.append(np.stack([timely, finite, changed]))
            assignments.append(np.bincount(state.assigned_hospital_index[finite], weights=pop[finite], minlength=len(net.hospital_ids)))
    return rows, np.asarray(grids, dtype=np.uint8), np.asarray(assignments)


def main():
    global NETWORKS, PROBABILITIES, BASELINE_FINITE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, choices=[100, 1000], default=100)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Use an empty output directory; existing results are never overwritten")
    started = perf_counter()
    for name, multipliers in SCENARIOS.items():
        NETWORKS.append(build_compact_emergency_network(PROCESSED, category_speed_multipliers=multipliers))
        print(f"Built {name} after {perf_counter()-started:.1f}s", flush=True)
    net = NETWORKS[0]
    for other in NETWORKS[1:]:
        for attribute in ["road_section_ids", "demand_ids", "demand_population", "hospital_ids", "arc_road_section", "arc_group_starts", "demand_node_index"]:
            assert np.array_equal(getattr(net, attribute), getattr(other, attribute)), attribute
        assert np.array_equal(net.graph.indices, other.graph.indices)
        assert np.array_equal(net.graph.indptr, other.graph.indptr)
        assert np.all(other.arc_base_weight >= net.arc_base_weight - 1e-12)
        assert np.all(other.arc_base_weight <= net.arc_base_weight / 0.8 + 1e-12)
    lengths = pd.read_parquet(PROCESSED / "kumamoto_road_sections_preprocessed.parquet", columns=["Road Section ID", "Road Section Length (m)"]).set_index("Road Section ID").loc[net.road_section_ids, "Road Section Length (m)"].to_numpy()
    PROBABILITIES = np.array([-np.expm1(-calibrate_intensity(s, lengths)*lengths) for s in SEVERITIES])
    BASELINE_FINITE = np.isfinite(net.route().total_time)
    undamaged_rows, _, _ = evaluate(0)
    pd.DataFrame(undamaged_rows).to_parquet(output / "undamaged_metrics.parquet", index=False)
    rows = []
    grid_sum = np.zeros((12, 3, len(net.demand_ids)), dtype=np.uint32)
    hospital_sum = np.zeros((12, len(net.hospital_ids)), dtype=float)
    with mp.get_context("fork").Pool(args.workers) as pool:
        for count, (records, grids, hospital) in enumerate(pool.imap(evaluate, range(1, args.replicates+1)), 1):
            rows.extend(records)
            grid_sum += grids
            hospital_sum += hospital
            if count % 25 == 0:
                print(f"Completed {count}/{args.replicates} after {perf_counter()-started:.1f}s", flush=True)
    metrics = pd.DataFrame(rows).sort_values(["replicate", "severity", "scenario"])
    assert len(metrics) == args.replicates * 12
    assert not metrics.duplicated(["replicate", "severity", "scenario"]).any()
    formal = pd.read_parquet(FORMAL / "replicate_metrics.parquet")
    comparison = metrics.loc[metrics.scenario.eq("baseline")].merge(formal, left_on=["replicate", "severity"], right_on=["Simulation Replicate", "Expected Failed Road Length Share"], validate="one_to_one")
    assert len(comparison) == args.replicates * 4
    assert np.array_equal(comparison.population_within_30, comparison["Population within 30 Minutes"])
    assert np.array_equal(comparison.newly_disconnected_population, comparison["Population Newly Disconnected"])
    metrics.to_parquet(output / "replicate_metrics.parquet", index=False)
    summaries, grid_frames, hospital_frames = [], [], []
    for si, severity in enumerate(SEVERITIES):
        for ci, scenario in enumerate(SCENARIOS):
            position = si*3+ci
            counts = grid_sum[position]
            subset = metrics.loc[metrics.severity.eq(severity) & metrics.scenario.eq(scenario)]
            assert np.isclose(np.dot(counts[0]/args.replicates, net.demand_population), subset.population_within_30.mean())
            assert np.isclose(hospital_sum[position].sum()/args.replicates, subset.reachable_population.mean())
            grid_frames.append(pd.DataFrame({"demand_id": net.demand_ids, "population": net.demand_population, "severity": severity, "scenario": scenario, "timely_probability": counts[0]/args.replicates, "reachable_probability": counts[1]/args.replicates, "hospital_reassignment_probability": counts[2]/args.replicates}))
            hospital_frames.append(pd.DataFrame({"hospital_id": net.hospital_ids, "severity": severity, "scenario": scenario, "mean_assigned_population": hospital_sum[position]/args.replicates}))
            entry = {"severity": severity, "scenario": scenario}
            for field in ["population_within_30", "paired_coverage_change", "hospital_reassigned_population", "hospital_reassigned_share_reachable"]:
                values = subset[field]
                entry.update({field+"_mean": float(values.mean()), field+"_p5": float(values.quantile(.05)), field+"_p95": float(values.quantile(.95)), field+"_mcse": float(values.std(ddof=1)/np.sqrt(len(values)))})
            summaries.append(entry)
    pd.concat(grid_frames, ignore_index=True).to_parquet(output / "grid_probabilities.parquet", index=False)
    pd.concat(hospital_frames, ignore_index=True).to_parquet(output / "hospital_catchments.parquet", index=False)
    paths = [PROCESSED / n for n in ["kumamoto_routable_road_edges_preprocessed.parquet", "kumamoto_road_sections_preprocessed.parquet", "kumamoto_population_mesh_network_access_preprocessed.parquet", "kumamoto_dispatch_base_network_access_preprocessed.parquet", "kumamoto_hospital_network_access_preprocessed.parquet"]]
    paths += [FORMAL / "replicate_metrics.parquet", Path(__file__), Path(__file__).with_name("monte_carlo_emergency_routing.py")]
    report = {"status": "pass", "replicates": args.replicates, "seed": SEED, "scenarios": SCENARIOS, "severity": SEVERITIES, "threshold_minutes": 30, "elapsed_seconds": perf_counter()-started, "baseline_exactly_matches_formal": True, "input_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}, "definition": "Perturb effective width-capped speeds; reroute edges and referenced connectors. Hospital changes compare with baseline-speed assignment in the SAME failed state, among complete-chain reachable demands; grid reassignment probability uses all replicates. P5/P95 are replicate-distribution quantiles, not confidence intervals. Floating-point ties may affect hospital identity. No section-consequence ranking experiment is included.", "summary": summaries}
    (output / "experiment_summary.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k in ["status", "replicates", "elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
