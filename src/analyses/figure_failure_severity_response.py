#!/usr/bin/env python3
"""Failure Severity Response.

Plan: Show the response of 30-minute coverage, baseline coverage loss, and newly
disconnected population to increasing expected failed road length.
Framework: AnaSOP Sections 5.1, 6.6, and Analytical Workflow step 2.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "exp" / "length_weighted_severity_calibration_100"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_failure_severity_response.png"


def summarize(frame: pd.DataFrame, outcome: str) -> pd.DataFrame:
    return (
        frame.groupby("Target Expected Failed Road Length Share", sort=True)[outcome]
        .agg(
            Mean="mean",
            P05=lambda values: values.quantile(0.05),
            P95=lambda values: values.quantile(0.95),
        )
        .reset_index()
    )


def draw_response(
    axis: plt.Axes,
    frame: pd.DataFrame,
    outcome: str,
    color: str,
    scale: float,
    ylabel: str,
) -> None:
    values = summarize(frame, outcome)
    x = 100.0 * values["Target Expected Failed Road Length Share"].to_numpy(float)
    mean = values["Mean"].to_numpy(float) / scale
    low = values["P05"].to_numpy(float) / scale
    high = values["P95"].to_numpy(float) / scale

    axis.fill_between(x, low, high, color=color, alpha=0.18, linewidth=0)
    axis.plot(x, mean, color=color, linewidth=2.1, zorder=3)

    calibration = np.isin(x, [0.5, 2.0])
    main = np.isin(x, [1.0, 3.0, 5.0])
    stress = np.isclose(x, 10.0)
    axis.scatter(
        x[calibration],
        mean[calibration],
        s=34,
        marker="o",
        facecolor="white",
        edgecolor=color,
        linewidth=1.4,
        zorder=4,
    )
    axis.scatter(
        x[main],
        mean[main],
        s=34,
        marker="o",
        facecolor=color,
        edgecolor=color,
        linewidth=1.0,
        zorder=4,
    )
    axis.scatter(
        x[stress],
        mean[stress],
        s=44,
        marker="D",
        facecolor=color,
        edgecolor=color,
        linewidth=1.0,
        zorder=4,
    )

    axis.set_xlabel("Expected failed road length (%)")
    axis.set_ylabel(ylabel)
    axis.set_xticks(x)
    axis.set_xticklabels([f"{value:g}" for value in x], rotation=30, ha="right")
    axis.grid(axis="y", color="#d9d9d9", linewidth=0.65)
    axis.spines[["top", "right"]].set_visible(False)
    axis.tick_params(direction="out")


def main() -> None:
    metrics = pd.read_parquet(SOURCE / "replicate_metrics.parquet")
    report = json.loads((SOURCE / "calibration_report.json").read_text(encoding="utf-8"))
    baseline_30 = float(report["baseline_population_within_minutes"]["30"])

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0), sharex=True)
    draw_response(
        axes[0],
        metrics,
        "Population within 30 Minutes",
        "#2166ac",
        1_000_000.0,
        "Population retaining 30-minute access (million)",
    )
    axes[0].axhline(
        baseline_30 / 1_000_000.0,
        color="#4d4d4d",
        linestyle="--",
        linewidth=1.0,
        zorder=1,
    )
    draw_response(
        axes[1],
        metrics,
        "Population Losing Baseline 30-Minute Access",
        "#d95f0e",
        1_000.0,
        "Population losing baseline 30-minute access (thousand)",
    )
    draw_response(
        axes[2],
        metrics,
        "Population Newly Disconnected",
        "#762a83",
        1_000.0,
        "Population newly disconnected (thousand)",
    )

    for label, axis in zip("abc", axes):
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
        Line2D([0], [0], color="#555555", linewidth=2.0, label="Mean"),
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="white",
            markeredgecolor="#555555",
            markersize=5.5,
            label="Calibration level",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor="#555555",
            markeredgecolor="#555555",
            markersize=5.5,
            label="Main scenario",
        ),
        Line2D(
            [0],
            [0],
            marker="D",
            color="none",
            markerfacecolor="#555555",
            markeredgecolor="#555555",
            markersize=5.5,
            label="Stress scenario",
        ),
        Line2D(
            [0],
            [0],
            color="#4d4d4d",
            linestyle="--",
            linewidth=1.0,
            label="Baseline (panel a)",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.035),
        ncol=5,
        frameon=False,
        fontsize=8,
        handlelength=2.0,
        columnspacing=1.4,
    )
    fig.tight_layout(rect=(0, 0.10, 1, 1), w_pad=1.5)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
