#!/usr/bin/env python3
"""Population Coverage under Length-Dependent Road Failure.

Plan: Compare total and older-population emergency-access coverage at the 15-,
30-, and 45-minute thresholds across the main and stress scenarios.
Framework: AnaSOP Sections 5.2, 6.3, and Analytical Workflow step 5.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "data" / "exp" / "monte_carlo_length_weighted_full_1000"
OUTPUT = (
    ROOT
    / "data"
    / "results"
    / "figures"
    / "Figure_population_coverage_under_length_dependent_road_failure.png"
)
FIGURE_DPI = 300
THRESHOLDS = (15, 30, 45)
TOTAL_COLOR = "#2166ac"
OLDER_COLOR = "#d95f0e"


def summarize(values: pd.DataFrame, column: str) -> pd.DataFrame:
    return (
        values.groupby("Expected Failed Road Length Share", sort=True)[column]
        .agg(
            Mean="mean",
            P05=lambda series: series.quantile(0.05),
            P95=lambda series: series.quantile(0.95),
        )
        .reset_index()
    )


def plot_group(
    axis: plt.Axes,
    summary: pd.DataFrame,
    color: str,
) -> None:
    x = 100.0 * summary["Expected Failed Road Length Share"].to_numpy(float)
    mean = summary["Mean"].to_numpy(float)
    low = summary["P05"].to_numpy(float)
    high = summary["P95"].to_numpy(float)
    axis.fill_between(x, low, high, color=color, alpha=0.17, linewidth=0)
    axis.plot(x, mean, color=color, linewidth=2.1, zorder=3)
    main = np.isin(x, [1.0, 3.0, 5.0])
    stress = np.isclose(x, 10.0)
    axis.scatter(
        x[main],
        mean[main],
        marker="o",
        s=34,
        facecolor=color,
        edgecolor=color,
        linewidth=1.0,
        zorder=4,
    )
    axis.scatter(
        x[stress],
        mean[stress],
        marker="D",
        s=44,
        facecolor=color,
        edgecolor=color,
        linewidth=1.0,
        zorder=4,
    )


def main() -> None:
    metrics = pd.read_parquet(EXPERIMENT / "replicate_metrics.parquet")
    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(12.2, 4.25),
        sharex=True,
        sharey=True,
    )
    diagnostics: list[dict[str, float | int | str]] = []

    for axis, threshold in zip(axes, THRESHOLDS, strict=True):
        total_coverage = f"Population within {threshold} Minutes"
        total_loss = f"Population Losing Baseline {threshold}-Minute Access"
        older_coverage = f"Older Population within {threshold} Minutes"
        older_loss = (
            f"Older Population Losing Baseline {threshold}-Minute Access"
        )
        baseline_total_values = metrics[total_coverage] + metrics[total_loss]
        baseline_older_values = metrics[older_coverage] + metrics[older_loss]
        baseline_total_unique = baseline_total_values.unique()
        baseline_older_unique = baseline_older_values.unique()
        if len(baseline_total_unique) != 1 or len(baseline_older_unique) != 1:
            raise RuntimeError(
                f"Baseline coverage is not invariant for {threshold} minutes"
            )
        baseline_total = float(baseline_total_unique[0])
        baseline_older = float(baseline_older_unique[0])
        analysis = metrics[
            [
                "Expected Failed Road Length Share",
                total_coverage,
                older_coverage,
            ]
        ].copy()
        analysis["Total Retained Share"] = (
            100.0 * analysis[total_coverage] / baseline_total
        )
        analysis["Older Retained Share"] = (
            100.0 * analysis[older_coverage] / baseline_older
        )
        total_summary = summarize(analysis, "Total Retained Share")
        older_summary = summarize(analysis, "Older Retained Share")
        plot_group(axis, total_summary, TOTAL_COLOR)
        plot_group(axis, older_summary, OLDER_COLOR)
        axis.axhline(
            100.0,
            color="#4d4d4d",
            linestyle="--",
            linewidth=1.0,
            zorder=1,
        )
        axis.set_xlabel("Expected failed road length (%)")
        axis.set_xticks([1, 3, 5, 10])
        axis.set_ylim(89.0, 100.45)
        axis.grid(axis="y", color="#d9d9d9", linewidth=0.65)
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(direction="out")
        axis.text(
            0.975,
            0.06,
            (
                f"Threshold: {threshold} minutes\n"
                f"Baseline total: {baseline_total:,.0f}\n"
                f"Baseline age 65+: {baseline_older:,.0f}"
            ),
            transform=axis.transAxes,
            ha="right",
            va="bottom",
            fontsize=8.0,
            linespacing=1.35,
            bbox={
                "facecolor": "white",
                "edgecolor": "#bdbdbd",
                "alpha": 0.94,
                "boxstyle": "round,pad=0.30",
            },
            zorder=6,
        )
        for _, row in total_summary.iterrows():
            diagnostics.append(
                {
                    "threshold_minutes": threshold,
                    "population_group": "Total population",
                    "expected_failed_length_percent": float(
                        100 * row["Expected Failed Road Length Share"]
                    ),
                    "mean_retained_percent": float(row["Mean"]),
                    "p05_retained_percent": float(row["P05"]),
                    "p95_retained_percent": float(row["P95"]),
                }
            )
        for _, row in older_summary.iterrows():
            diagnostics.append(
                {
                    "threshold_minutes": threshold,
                    "population_group": "Population age 65+",
                    "expected_failed_length_percent": float(
                        100 * row["Expected Failed Road Length Share"]
                    ),
                    "mean_retained_percent": float(row["Mean"]),
                    "p05_retained_percent": float(row["P05"]),
                    "p95_retained_percent": float(row["P95"]),
                }
            )

    axes[0].set_ylabel("Baseline-covered population retained (%)")
    for label, axis in zip("abc", axes, strict=True):
        axis.text(
            0.02,
            0.98,
            label,
            transform=axis.transAxes,
            fontsize=11,
            fontweight="bold",
            va="top",
            ha="left",
        )

    legend_handles = [
        Line2D(
            [0], [0], color=TOTAL_COLOR, linewidth=2.1, marker="o",
            markersize=5.5, label="Total population"
        ),
        Line2D(
            [0], [0], color=OLDER_COLOR, linewidth=2.1, marker="o",
            markersize=5.5, label="Population age 65+"
        ),
        Line2D(
            [0], [0], color="#555555", linewidth=0, marker="D",
            markersize=5.5, label="10% stress scenario"
        ),
        Line2D(
            [0], [0], color="#4d4d4d", linestyle="--", linewidth=1.0,
            label="Baseline coverage"
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.025),
        ncol=4,
        frameon=False,
        fontsize=8,
        handlelength=2.0,
        columnspacing=1.5,
    )
    fig.tight_layout(rect=(0, 0.10, 1, 1), w_pad=1.4)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    print(pd.DataFrame(diagnostics).to_string(index=False))


if __name__ == "__main__":
    main()
