#!/usr/bin/env python3
"""Replay formal road-failure states for uniform travel-speed sensitivity."""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from monte_carlo_emergency_routing import (
    CompactEmergencyNetwork,
    build_compact_emergency_network,
)
from run_length_weighted_monte_carlo_full import calibrate_intensity


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
FORMAL = ROOT / "data" / "exp" / "monte_carlo_length_weighted_full_1000"
DEFAULT_OUTPUT = ROOT / "data" / "exp" / "monte_carlo_speed_sensitivity_1000"
SEVERITIES = np.array([0.01, 0.03, 0.05, 0.10], dtype=np.float64)
SPEED_MULTIPLIERS = np.array([0.8, 1.0, 1.2], dtype=np.float64)
THRESHOLDS = np.array([15, 30, 45], dtype=np.int16)
BASE_SEED = 20260806
REPLICATES = 1000

_WORKER_NETWORK: CompactEmergencyNetwork | None = None
_WORKER_PROBABILITIES: np.ndarray | None = None
_WORKER_BASELINE_TIME: np.ndarray | None = None
_WORKER_POPULATION: np.ndarray | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=min(10, os.cpu_count() or 1))
    parser.add_argument("--chunk-size", type=int, default=4)
    return parser.parse_args()


def worker_replicate(replicate: int) -> list[dict[str, float | int]]:
    if (
        _WORKER_NETWORK is None
        or _WORKER_PROBABILITIES is None
        or _WORKER_BASELINE_TIME is None
        or _WORKER_POPULATION is None
    ):
        raise RuntimeError("Worker state is not initialized")
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, replicate]))
    uniform_score = rng.random(_WORKER_NETWORK.road_section_count)
    baseline_finite = np.isfinite(_WORKER_BASELINE_TIME)
    total_population = float(_WORKER_POPULATION.sum())
    rows: list[dict[str, float | int]] = []
    previous_failed = np.zeros(_WORKER_NETWORK.road_section_count, dtype=bool)
    for severity_index, severity in enumerate(SEVERITIES):
        failed = uniform_score < _WORKER_PROBABILITIES[severity_index]
        if not np.all(failed[previous_failed]):
            raise RuntimeError("Nested failure sets failed in speed-sensitivity replay")
        state = _WORKER_NETWORK.route(failed=failed, assign_hospitals=False)
        newly_disconnected = float(
            _WORKER_POPULATION[baseline_finite & ~np.isfinite(state.total_time)].sum()
        )
        for speed_multiplier in SPEED_MULTIPLIERS:
            baseline_scaled = _WORKER_BASELINE_TIME / speed_multiplier
            disrupted_scaled = state.total_time / speed_multiplier
            for threshold in THRESHOLDS:
                baseline_timely = baseline_scaled <= threshold
                disrupted_timely = disrupted_scaled <= threshold
                population_within = float(
                    _WORKER_POPULATION[disrupted_timely].sum()
                )
                population_loss = float(
                    _WORKER_POPULATION[baseline_timely & ~disrupted_timely].sum()
                )
                rows.append(
                    {
                        "Simulation Replicate": int(replicate),
                        "Expected Failed Road Length Share": float(severity),
                        "Assumed Speed Multiplier": float(speed_multiplier),
                        "Timely Access Threshold (min)": int(threshold),
                        "Population within Timely Access": population_within,
                        "Population-Weighted Timely Access Share": (
                            population_within / total_population
                        ),
                        "Population Losing Baseline Timely Access": population_loss,
                        "Population Newly Disconnected": newly_disconnected,
                    }
                )
        previous_failed = failed
    return rows


def main() -> None:
    global _WORKER_NETWORK, _WORKER_PROBABILITIES
    global _WORKER_BASELINE_TIME, _WORKER_POPULATION

    args = parse_args()
    if not args.output_dir.is_absolute():
        args.output_dir = ROOT / args.output_dir
    if args.workers < 1 or args.chunk_size < 1:
        raise ValueError("workers and chunk-size must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = perf_counter()

    network = build_compact_emergency_network(
        PROCESSED, include_population_groups=False
    )
    baseline = network.route(assign_hospitals=False)
    sections = pd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=["Road Section ID", "Road Section Length (m)"],
    )
    sections["Road Section ID"] = sections["Road Section ID"].astype(str)
    sections = sections.set_index("Road Section ID").loc[
        network.road_section_ids
    ].reset_index()
    lengths = sections["Road Section Length (m)"].to_numpy(dtype=np.float64)
    intensities = np.array(
        [calibrate_intensity(target, lengths) for target in SEVERITIES]
    )
    probabilities = np.vstack(
        [-np.expm1(-intensity * lengths) for intensity in intensities]
    )
    if not np.all(np.diff(probabilities, axis=0) >= -1e-15):
        raise RuntimeError("Section failure probabilities are not nested")

    partial_path = args.output_dir / "speed_sensitivity_metrics_partial.parquet"
    completed = pd.DataFrame()
    if partial_path.exists():
        completed = pd.read_parquet(partial_path)
    completed_replicates = set(
        completed.get("Simulation Replicate", pd.Series(dtype=int)).astype(int)
    )
    remaining = [
        replicate
        for replicate in range(1, REPLICATES + 1)
        if replicate not in completed_replicates
    ]
    print(
        f"Replaying {len(remaining):,} remaining of {REPLICATES:,} replicates "
        f"with {args.workers} worker(s)",
        flush=True,
    )

    _WORKER_NETWORK = network
    _WORKER_PROBABILITIES = probabilities
    _WORKER_BASELINE_TIME = baseline.total_time
    _WORKER_POPULATION = network.demand_population
    frames = [completed] if not completed.empty else []
    buffered_rows: list[dict[str, float | int]] = []
    checkpoint_replicates = 0

    if args.workers == 1:
        iterator = map(worker_replicate, remaining)
        pool = None
    else:
        context = mp.get_context("fork")
        pool = context.Pool(processes=args.workers)
        iterator = pool.imap_unordered(
            worker_replicate,
            remaining,
            chunksize=args.chunk_size,
        )
    try:
        for rows in iterator:
            buffered_rows.extend(rows)
            checkpoint_replicates += 1
            if checkpoint_replicates >= 100 or len(buffered_rows) == len(remaining) * 36:
                if buffered_rows:
                    frames.append(pd.DataFrame(buffered_rows))
                    buffered_rows = []
                checkpoint = pd.concat(frames, ignore_index=True)
                checkpoint.to_parquet(partial_path, index=False)
                print(
                    f"Completed {checkpoint['Simulation Replicate'].nunique():,}/"
                    f"{REPLICATES:,} replicates in {perf_counter() - started:.1f}s",
                    flush=True,
                )
                checkpoint_replicates = 0
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    if buffered_rows:
        frames.append(pd.DataFrame(buffered_rows))

    metrics = pd.concat(frames, ignore_index=True)
    metrics = metrics.drop_duplicates(
        [
            "Simulation Replicate",
            "Expected Failed Road Length Share",
            "Assumed Speed Multiplier",
            "Timely Access Threshold (min)",
        ],
        keep="last",
    ).sort_values(
        [
            "Simulation Replicate",
            "Expected Failed Road Length Share",
            "Assumed Speed Multiplier",
            "Timely Access Threshold (min)",
        ]
    )
    expected_rows = REPLICATES * len(SEVERITIES) * len(SPEED_MULTIPLIERS) * len(THRESHOLDS)
    if len(metrics) != expected_rows:
        raise RuntimeError(f"Expected {expected_rows} rows; found {len(metrics)}")

    formal = pd.read_parquet(FORMAL / "replicate_metrics.parquet")
    baseline_speed = metrics.loc[metrics["Assumed Speed Multiplier"].eq(1.0)].copy()
    formal_long = formal.melt(
        id_vars=[
            "Simulation Replicate",
            "Expected Failed Road Length Share",
            "Population Newly Disconnected",
        ],
        value_vars=[f"Population within {value} Minutes" for value in THRESHOLDS],
        var_name="Coverage Variable",
        value_name="Formal Population within Timely Access",
    )
    formal_long["Timely Access Threshold (min)"] = formal_long[
        "Coverage Variable"
    ].str.extract(r"(\d+)").astype(int)
    comparison = baseline_speed.merge(
        formal_long,
        on=[
            "Simulation Replicate",
            "Expected Failed Road Length Share",
            "Timely Access Threshold (min)",
        ],
        how="inner",
        validate="one_to_one",
        suffixes=("", " Formal"),
    )
    coverage_match = np.array_equal(
        comparison["Population within Timely Access"].to_numpy(),
        comparison["Formal Population within Timely Access"].to_numpy(),
    )
    disconnection_match = np.array_equal(
        comparison["Population Newly Disconnected"].to_numpy(),
        comparison["Population Newly Disconnected Formal"].to_numpy(),
    )
    if not coverage_match or not disconnection_match:
        raise RuntimeError("The 1.0x replay does not reproduce formal experiment metrics")

    final_path = args.output_dir / "speed_sensitivity_metrics.parquet"
    metrics.to_parquet(final_path, index=False)
    summary = {
        "status": "pass",
        "replicates": REPLICATES,
        "network_states_replayed": REPLICATES * len(SEVERITIES),
        "expected_failed_road_length_shares": SEVERITIES.tolist(),
        "assumed_speed_multipliers": SPEED_MULTIPLIERS.tolist(),
        "timely_access_thresholds_minutes": THRESHOLDS.tolist(),
        "paired_nested_draws": True,
        "baseline_speed_coverage_exactly_matches_formal_experiment": coverage_match,
        "baseline_speed_disconnection_exactly_matches_formal_experiment": disconnection_match,
        "uniform_speed_scaling_note": (
            "All edge and connector travel times are divided by the common speed "
            "multiplier, so shortest-path assignments remain unchanged within a road state."
        ),
        "network_build_seconds": network.build_seconds,
        "elapsed_seconds": perf_counter() - started,
    }
    summary_path = args.output_dir / "experiment_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved: {final_path.relative_to(ROOT)}")
    print(f"Saved: {summary_path.relative_to(ROOT)}")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
