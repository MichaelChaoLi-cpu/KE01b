#!/usr/bin/env python3
"""Validate and benchmark one nested Monte Carlo road-failure replicate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from time import perf_counter

import numpy as np

from emergency_routing import compute_emergency_access
from monte_carlo_emergency_routing import (
    build_compact_emergency_network,
    summarize_state,
)


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUTPUT = ROOT / "data" / "exp" / "monte_carlo_engine_smoke_test.json"
FAILURE_RATES = (0.05, 0.10, 0.20)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--skip-networkx-baseline",
        action="store_true",
        help="Skip the slower independent baseline-equivalence check.",
    )
    return parser.parse_args()


def monotone_after_removal(previous: np.ndarray, current: np.ndarray) -> bool:
    """Return true when further edge removals never shorten a demand path."""
    finite_both = np.isfinite(previous) & np.isfinite(current)
    no_shorter = np.all(current[finite_both] + 1e-10 >= previous[finite_both])
    no_reconnection = not np.any(~np.isfinite(previous) & np.isfinite(current))
    return bool(no_shorter and no_reconnection)


def main() -> None:
    args = parse_args()
    report: dict[str, object] = {
        "seed": args.seed,
        "failure_rates": list(FAILURE_RATES),
        "checks": {},
    }

    network = build_compact_emergency_network(PROCESSED)
    report["network"] = {
        "road_sections": network.road_section_count,
        "nodes": network.node_count,
        "directed_node_pairs": network.directed_pair_count,
        "demand_units": int(len(network.demand_ids)),
        "build_seconds": round(network.build_seconds, 6),
    }

    baseline = network.route()
    baseline_summary = summarize_state(network, baseline, 0.0, 0)
    report["baseline"] = baseline_summary

    checks = report["checks"]
    assert isinstance(checks, dict)
    if not args.skip_networkx_baseline:
        started = perf_counter()
        reference = compute_emergency_access(PROCESSED, "Baseline", "mesh")
        reference_seconds = perf_counter() - started
        reference_total = reference.demand["Total Emergency Access Time"].to_numpy(float)
        finite_match = np.array_equal(
            np.isfinite(baseline.total_time), np.isfinite(reference_total)
        )
        finite_both = np.isfinite(baseline.total_time) & np.isfinite(reference_total)
        maximum_difference = (
            float(np.max(np.abs(baseline.total_time[finite_both] - reference_total[finite_both])))
            if finite_both.any()
            else 0.0
        )
        checks["networkx_baseline_finite_status_match"] = finite_match
        checks["networkx_baseline_maximum_absolute_difference_minutes"] = maximum_difference
        checks["networkx_baseline_equivalent"] = bool(
            finite_match and maximum_difference <= 1e-8
        )
        report["networkx_baseline_seconds"] = round(reference_seconds, 6)

    rng = np.random.default_rng(args.seed)
    order = rng.permutation(network.road_section_count)
    failed = np.zeros(network.road_section_count, dtype=bool)
    previous_time = baseline.total_time
    previous_failed = np.zeros(network.road_section_count, dtype=bool)
    states: list[dict[str, float | int]] = []
    nested_checks: list[bool] = []
    monotonic_checks: list[bool] = []
    reproducibility_checks: list[bool] = []

    for failure_rate in FAILURE_RATES:
        failed_count = int(np.floor(failure_rate * network.road_section_count))
        failed[:] = False
        failed[order[:failed_count]] = True
        nested_checks.append(bool(np.all(failed[previous_failed])))
        state = network.route(failed)
        state_summary = summarize_state(
            network,
            state,
            failure_rate,
            failed_count,
        )
        states.append(state_summary)
        monotonic_checks.append(monotone_after_removal(previous_time, state.total_time))

        repeated = network.route(failed)
        reproducibility_checks.append(
            bool(np.array_equal(state.total_time, repeated.total_time, equal_nan=True))
        )
        previous_failed = failed.copy()
        previous_time = state.total_time

    checks["exact_failed_counts"] = all(
        state["failed_units"]
        == int(np.floor(state["failure_rate"] * network.road_section_count))
        for state in states
    )
    checks["nested_failure_sets"] = all(nested_checks)
    checks["travel_time_monotone_after_removal"] = all(monotonic_checks)
    checks["same_seed_state_reproducible"] = all(reproducibility_checks)
    report["states"] = states
    report["all_checks_pass"] = all(
        bool(value)
        for key, value in checks.items()
        if not key.endswith("minutes")
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["all_checks_pass"]:
        raise SystemExit("Monte Carlo routing smoke test failed")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"smoke_test_monte_carlo_engine failed: {exc}", file=sys.stderr)
        raise
