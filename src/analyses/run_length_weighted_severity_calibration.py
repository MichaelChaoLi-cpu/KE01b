#!/usr/bin/env python3
"""Calibrate length-dependent road failures and trace accessibility responses."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from monte_carlo_emergency_routing import build_compact_emergency_network


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUTPUT = ROOT / "data" / "exp" / "length_weighted_severity_calibration_100"
TARGET_SHARES = np.array([0.005, 0.01, 0.02, 0.03, 0.05, 0.10], dtype=np.float64)
THRESHOLDS = (15, 30, 45)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260806)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def expected_failed_length_share(intensity: float, lengths: np.ndarray) -> float:
    probabilities = -np.expm1(-intensity * lengths)
    return float(np.dot(lengths, probabilities) / lengths.sum())


def calibrate_intensity(target: float, lengths: np.ndarray) -> float:
    """Solve for intensity so expected failed length equals the target share."""
    if not 0.0 < target < 1.0:
        raise ValueError(f"Target share must lie in (0, 1), got {target}")
    low = 0.0
    high = 1.0 / float(np.median(lengths))
    while expected_failed_length_share(high, lengths) < target:
        high *= 2.0
    for _ in range(80):
        midpoint = 0.5 * (low + high)
        if expected_failed_length_share(midpoint, lengths) < target:
            low = midpoint
        else:
            high = midpoint
    return 0.5 * (low + high)


def summarize_calibration(
    targets: np.ndarray,
    intensities: np.ndarray,
    probabilities: np.ndarray,
    lengths: np.ndarray,
) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    for index, target in enumerate(targets):
        probability = probabilities[index]
        rows.append(
            {
                "Target Expected Failed Road Length Share": float(target),
                "Failure Intensity per Metre": float(intensities[index]),
                "Expected Failed Road Length Share": expected_failed_length_share(
                    intensities[index], lengths
                ),
                "Expected Failed Road Section Share": float(probability.mean()),
                "Section Failure Probability P05": float(np.quantile(probability, 0.05)),
                "Section Failure Probability P50": float(np.quantile(probability, 0.50)),
                "Section Failure Probability P95": float(np.quantile(probability, 0.95)),
                "Section Failure Probability Maximum": float(probability.max()),
            }
        )
    return pd.DataFrame(rows)


def summarize_replicates(metrics: pd.DataFrame) -> pd.DataFrame:
    outcome_columns = [
        "Realized Failed Road Length Share",
        "Failed Road Sections",
        "Population within 15 Minutes",
        "Population within 30 Minutes",
        "Population within 45 Minutes",
        "Population Losing Baseline 15-Minute Access",
        "Population Losing Baseline 30-Minute Access",
        "Population Losing Baseline 45-Minute Access",
        "Disconnected Population",
        "Population Newly Disconnected",
        "Routing Seconds",
    ]
    rows: list[dict[str, float | str]] = []
    for target, group in metrics.groupby(
        "Target Expected Failed Road Length Share", sort=True
    ):
        for outcome in outcome_columns:
            values = group[outcome].to_numpy(np.float64)
            rows.append(
                {
                    "Target Expected Failed Road Length Share": float(target),
                    "Outcome": outcome,
                    "Mean": float(values.mean()),
                    "P05": float(np.quantile(values, 0.05)),
                    "P50": float(np.quantile(values, 0.50)),
                    "P95": float(np.quantile(values, 0.95)),
                    "Standard Deviation": float(values.std(ddof=1)),
                }
            )
    return pd.DataFrame(rows)


def plot_response_curve(
    summary: pd.DataFrame,
    baseline_30: float,
    output: Path,
) -> None:
    outcomes = [
        ("Population within 30 Minutes", "Population retaining 30-minute access"),
        (
            "Population Losing Baseline 30-Minute Access",
            "Population losing baseline 30-minute access",
        ),
        ("Population Newly Disconnected", "Population newly disconnected"),
    ]
    colors = ["#2166ac", "#d95f0e", "#762a83"]
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.8), sharex=True)
    for panel_index, (axis, (outcome, ylabel), color) in enumerate(
        zip(axes, outcomes, colors)
    ):
        frame = summary.loc[summary["Outcome"] == outcome].sort_values(
            "Target Expected Failed Road Length Share"
        )
        x = 100.0 * frame["Target Expected Failed Road Length Share"].to_numpy(float)
        mean = frame["Mean"].to_numpy(float) / 1_000_000.0
        low = frame["P05"].to_numpy(float) / 1_000_000.0
        high = frame["P95"].to_numpy(float) / 1_000_000.0
        axis.fill_between(x, low, high, color=color, alpha=0.18, linewidth=0)
        axis.plot(x, mean, color=color, linewidth=2.0, marker="o", markersize=4.2)
        if panel_index == 0:
            axis.axhline(
                baseline_30 / 1_000_000.0,
                color="#4d4d4d",
                linestyle="--",
                linewidth=1.0,
                label="Baseline",
            )
            axis.legend(frameon=False, loc="lower left", fontsize=8)
        axis.text(
            0.02,
            0.98,
            chr(ord("a") + panel_index),
            transform=axis.transAxes,
            va="top",
            ha="left",
            fontsize=11,
            fontweight="bold",
        )
        axis.set_ylabel(f"{ylabel} (million)")
        axis.set_xlabel("Expected failed road length (%)")
        axis.set_xticks(x)
        axis.set_xticklabels(
            [f"{value:g}" for value in x], rotation=30, ha="right"
        )
        axis.grid(axis="y", color="#d9d9d9", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(w_pad=1.4)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    if args.replicates < 1:
        raise ValueError("Replicates must be positive")
    if not args.output.is_absolute():
        args.output = ROOT / args.output
    args.output.mkdir(parents=True, exist_ok=True)
    started = perf_counter()

    network = build_compact_emergency_network(PROCESSED)
    sections = pd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=["Road Section ID", "Road Section Length (m)"],
    )
    sections["Road Section ID"] = sections["Road Section ID"].astype(str)
    lengths_by_id = sections.set_index("Road Section ID")["Road Section Length (m)"]
    lengths = lengths_by_id.reindex(network.road_section_ids).to_numpy(np.float64)
    if not np.isfinite(lengths).all() or np.any(lengths <= 0):
        raise ValueError("Every routed road section must have one positive section length")

    intensities = np.array(
        [calibrate_intensity(target, lengths) for target in TARGET_SHARES]
    )
    probabilities = np.vstack(
        [-np.expm1(-intensity * lengths) for intensity in intensities]
    )
    if not np.all(np.diff(probabilities, axis=0) >= -1e-15):
        raise AssertionError("Failure probabilities must be nested by severity")
    calibration = summarize_calibration(
        TARGET_SHARES, intensities, probabilities, lengths
    )

    baseline = network.route()
    population = network.demand_population.astype(np.float64)
    baseline_finite = np.isfinite(baseline.total_time)
    baseline_timely = {
        threshold: baseline_finite & (baseline.total_time <= threshold)
        for threshold in THRESHOLDS
    }
    baseline_population = {
        threshold: float(population[status].sum())
        for threshold, status in baseline_timely.items()
    }

    rows: list[dict[str, float | int]] = []
    for replicate in range(1, args.replicates + 1):
        rng = np.random.default_rng(np.random.SeedSequence([args.seed, replicate]))
        uniform_score = rng.random(network.road_section_count)
        previous_failed = np.zeros(network.road_section_count, dtype=bool)
        for severity_index, target in enumerate(TARGET_SHARES):
            failed = uniform_score < probabilities[severity_index]
            if not np.all(failed[previous_failed]):
                raise AssertionError("Paired road-section failures are not nested")
            state = network.route(failed)
            finite = np.isfinite(state.total_time)
            row: dict[str, float | int] = {
                "Simulation Replicate": replicate,
                "Target Expected Failed Road Length Share": float(target),
                "Failure Intensity per Metre": float(intensities[severity_index]),
                "Realized Failed Road Length Share": float(
                    lengths[failed].sum() / lengths.sum()
                ),
                "Failed Road Sections": int(failed.sum()),
                "Disconnected Population": float(population[~finite].sum()),
                "Population Newly Disconnected": float(
                    population[baseline_finite & ~finite].sum()
                ),
                "Routing Seconds": float(state.routing_seconds),
            }
            for threshold in THRESHOLDS:
                timely = finite & (state.total_time <= threshold)
                row[f"Population within {threshold} Minutes"] = float(
                    population[timely].sum()
                )
                row[
                    f"Population Losing Baseline {threshold}-Minute Access"
                ] = float(population[baseline_timely[threshold] & ~timely].sum())
            rows.append(row)
            previous_failed = failed
        if replicate == 1 or replicate % 10 == 0 or replicate == args.replicates:
            print(f"Completed replicate {replicate}/{args.replicates}", flush=True)

    metrics = pd.DataFrame(rows)
    response = summarize_replicates(metrics)
    calibration.to_parquet(args.output / "severity_calibration.parquet", index=False)
    metrics.to_parquet(args.output / "replicate_metrics.parquet", index=False)
    response.to_parquet(args.output / "severity_response_summary.parquet", index=False)
    calibration.to_csv(args.output / "severity_calibration.csv", index=False)
    response.to_csv(args.output / "severity_response_summary.csv", index=False)
    figure = args.output / "Figure_failure_severity_response_curve.png"
    plot_response_curve(response, baseline_population[30], figure)

    report = {
        "status": "pass",
        "interpretation": "Calibration evidence only; no final failure levels are selected.",
        "failure_model": "q_s(lambda) = 1 - exp(-lambda * section_length_s)",
        "paired_nested_draws": True,
        "replicates_per_level": args.replicates,
        "seed": args.seed,
        "target_expected_failed_road_length_shares": TARGET_SHARES.tolist(),
        "road_sections": network.road_section_count,
        "total_road_length_km": float(lengths.sum() / 1_000.0),
        "baseline_population_within_minutes": {
            str(key): value for key, value in baseline_population.items()
        },
        "network_build_seconds": network.build_seconds,
        "elapsed_seconds": perf_counter() - started,
        "figure": str(figure.relative_to(ROOT)),
    }
    (args.output / "calibration_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
