#!/usr/bin/env python3
"""Monte Carlo Convergence and Stress Sensitivity.

Plan: Show convergence across replicate checkpoints, distinguish the 1%, 3%,
and 5% main scenarios from the 10% stress state, and evaluate uniform travel-
speed multipliers of 0.8, 1.0, and 1.2.
Framework: AnaSOP Sections 6.6-6.7 and Analytical Workflow step 8.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "data" / "exp" / "monte_carlo_length_weighted_full_1000"
SPEED = ROOT / "data" / "exp" / "monte_carlo_speed_sensitivity_1000"
OUTPUT = (
    ROOT
    / "data"
    / "results"
    / "figures"
    / "Figure_monte_carlo_convergence_and_stress_sensitivity.png"
)
FIGURE_DPI = 300
SEVERITIES = (0.01, 0.03, 0.05, 0.10)
SEVERITY_COLORS = {
    0.01: "#2166ac",
    0.03: "#1a9850",
    0.05: "#f39c34",
    0.10: "#d73027",
}
SEVERITY_LABELS = {
    0.01: "1% main",
    0.03: "3% main",
    0.05: "5% main",
    0.10: "10% stress",
}


def thousands(value: float, _: int) -> str:
    return f"{value / 1_000:,.0f}"


def summarize_distribution(
    frame: pd.DataFrame,
    groups: list[str],
    value: str,
) -> pd.DataFrame:
    return (
        frame.groupby(groups, as_index=False)[value]
        .agg(
            Mean="mean",
            P05=lambda series: series.quantile(0.05),
            P95=lambda series: series.quantile(0.95),
        )
        .sort_values(groups)
    )


def line_style(severity: float) -> str:
    return "--" if severity == 0.10 else "-"


def main() -> None:
    convergence = pd.read_parquet(FORMAL / "convergence_summary.parquet")
    metrics = pd.read_parquet(FORMAL / "replicate_metrics.parquet")
    speed = pd.read_parquet(SPEED / "speed_sensitivity_metrics.parquet")

    final = convergence.loc[
        convergence["Simulation Replicate Checkpoint"].eq(1000)
    ]
    if not final["Monte Carlo Convergence Status"].eq("Stable").all():
        raise RuntimeError("Not all final severity outcomes passed convergence")
    if speed["Simulation Replicate"].nunique() != 1000:
        raise RuntimeError("Speed sensitivity does not contain 1,000 replicates")

    baseline_speed = speed.loc[
        speed["Assumed Speed Multiplier"].eq(1.0)
        & speed["Timely Access Threshold (min)"].eq(30)
    ].copy()
    severity_loss = summarize_distribution(
        baseline_speed,
        ["Expected Failed Road Length Share"],
        "Population Losing Baseline Timely Access",
    )
    severity_disconnection = summarize_distribution(
        baseline_speed,
        ["Expected Failed Road Length Share"],
        "Population Newly Disconnected",
    )
    speed30 = speed.loc[speed["Timely Access Threshold (min)"].eq(30)].copy()
    speed_summary = summarize_distribution(
        speed30,
        ["Expected Failed Road Length Share", "Assumed Speed Multiplier"],
        "Population within Timely Access",
    )

    sns.set_theme(context="paper", style="whitegrid", font_scale=1.05)
    fig, axes = plt.subplots(2, 2, figsize=(14.2, 9.4), constrained_layout=True)
    axes = np.asarray(axes)

    axis = axes[0, 0]
    for severity in SEVERITIES:
        subset = convergence.loc[
            convergence["Expected Failed Road Length Share"].eq(severity)
        ].sort_values("Simulation Replicate Checkpoint")
        x = subset["Simulation Replicate Checkpoint"].to_numpy(dtype=float)
        mean = subset["Mean Population within 30 Minutes"].to_numpy(dtype=float)
        p05 = subset["Population Coverage P05"].to_numpy(dtype=float)
        p95 = subset["Population Coverage P95"].to_numpy(dtype=float)
        axis.fill_between(
            x,
            p05,
            p95,
            color=SEVERITY_COLORS[severity],
            alpha=0.10,
            linewidth=0,
        )
        axis.plot(
            x,
            mean,
            color=SEVERITY_COLORS[severity],
            linestyle=line_style(severity),
            marker="o",
            markersize=4.2,
            linewidth=1.7,
            label=SEVERITY_LABELS[severity],
        )
    axis.set_xlabel("Simulation replicate checkpoint")
    axis.set_ylabel("Population within 30 minutes (thousands)")
    axis.yaxis.set_major_formatter(FuncFormatter(thousands))
    axis.set_xticks([100, 250, 500, 750, 1000])
    axis.legend(
        loc="lower right",
        frameon=True,
        framealpha=0.95,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=8,
        ncol=2,
    )
    axis.text(
        0.02,
        0.98,
        "Lines: running means\nShading: running P5–P95",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox={
            "facecolor": "white",
            "edgecolor": "#bdbdbd",
            "alpha": 0.94,
            "boxstyle": "round,pad=0.30",
        },
    )

    axis = axes[0, 1]
    for severity in SEVERITIES:
        subset = convergence.loc[
            convergence["Expected Failed Road Length Share"].eq(severity)
        ].sort_values("Simulation Replicate Checkpoint")
        stable = subset["Monte Carlo Convergence Status"].eq("Stable")
        axis.plot(
            subset["Simulation Replicate Checkpoint"],
            subset["Population Coverage Standard Error"],
            color=SEVERITY_COLORS[severity],
            linestyle=line_style(severity),
            linewidth=1.7,
            zorder=2,
        )
        axis.scatter(
            subset.loc[stable, "Simulation Replicate Checkpoint"],
            subset.loc[stable, "Population Coverage Standard Error"],
            s=31,
            facecolor=SEVERITY_COLORS[severity],
            edgecolor="white",
            linewidth=0.55,
            zorder=3,
        )
        not_stable = subset["Monte Carlo Convergence Status"].eq("Not stable")
        axis.scatter(
            subset.loc[not_stable, "Simulation Replicate Checkpoint"],
            subset.loc[not_stable, "Population Coverage Standard Error"],
            s=34,
            facecolor="white",
            edgecolor=SEVERITY_COLORS[severity],
            linewidth=1.2,
            zorder=3,
        )
        reference = subset["Monte Carlo Convergence Status"].eq(
            "Reference checkpoint"
        )
        axis.scatter(
            subset.loc[reference, "Simulation Replicate Checkpoint"],
            subset.loc[reference, "Population Coverage Standard Error"],
            s=34,
            marker="s",
            facecolor="#bdbdbd",
            edgecolor="white",
            linewidth=0.55,
            zorder=3,
        )
    axis.set_xlabel("Simulation replicate checkpoint")
    axis.set_ylabel("Monte Carlo standard error (people)")
    axis.set_xticks([100, 250, 500, 750, 1000])
    axis.set_ylim(bottom=0)
    status_legend = axis.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="s",
                linestyle="none",
                markerfacecolor="#bdbdbd",
                markeredgecolor="white",
                markersize=6.5,
                label="Reference",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor="#59646a",
                markeredgecolor="white",
                markersize=6.5,
                label="Stable",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor="white",
                markeredgecolor="#59646a",
                markersize=6.5,
                label="Not stable",
            ),
        ],
        loc="upper right",
        frameon=True,
        framealpha=0.95,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=8,
    )
    axis.add_artist(status_legend)
    axis.text(
        0.98,
        0.52,
        "All severities stable\nat 1,000 replicates",
        transform=axis.transAxes,
        ha="right",
        va="center",
        fontsize=8,
        bbox={
            "facecolor": "white",
            "edgecolor": "#bdbdbd",
            "alpha": 0.94,
            "boxstyle": "round,pad=0.30",
        },
    )

    axis = axes[1, 0]
    axis.axvspan(7.5, 10.5, color="#f4cccc", alpha=0.34, zorder=0)
    for summary, color, marker, label in (
        (
            severity_loss,
            "#6a3d9a",
            "o",
            "Lost baseline 30-minute access",
        ),
        (
            severity_disconnection,
            "#d73027",
            "s",
            "Newly disconnected",
        ),
    ):
        x = summary["Expected Failed Road Length Share"].to_numpy(dtype=float) * 100
        mean = summary["Mean"].to_numpy(dtype=float)
        lower = mean - summary["P05"].to_numpy(dtype=float)
        upper = summary["P95"].to_numpy(dtype=float) - mean
        axis.errorbar(
            x,
            mean,
            yerr=np.vstack([lower, upper]),
            color=color,
            marker=marker,
            markersize=5.2,
            linewidth=1.7,
            capsize=3.0,
            label=label,
            zorder=2,
        )
    axis.axvline(7.5, color="#9d4444", linewidth=0.8, linestyle=(0, (3, 3)))
    axis.set_xlabel("Expected failed road length (%)")
    axis.set_ylabel("Affected population (thousands)")
    axis.yaxis.set_major_formatter(FuncFormatter(thousands))
    axis.set_xticks([1, 3, 5, 10])
    axis.set_xlim(0.3, 10.5)
    axis.set_ylim(bottom=0)
    axis.legend(
        loc="upper left",
        frameon=True,
        framealpha=0.95,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=8,
    )
    axis.text(
        0.98,
        0.98,
        "Baseline speed: 1.0×\nError bars: P5–P95\nShaded region: stress scenario",
        transform=axis.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        bbox={
            "facecolor": "white",
            "edgecolor": "#bdbdbd",
            "alpha": 0.94,
            "boxstyle": "round,pad=0.30",
        },
    )

    axis = axes[1, 1]
    for severity in SEVERITIES:
        subset = speed_summary.loc[
            speed_summary["Expected Failed Road Length Share"].eq(severity)
        ].sort_values("Assumed Speed Multiplier")
        x = subset["Assumed Speed Multiplier"].to_numpy(dtype=float)
        mean = subset["Mean"].to_numpy(dtype=float)
        p05 = subset["P05"].to_numpy(dtype=float)
        p95 = subset["P95"].to_numpy(dtype=float)
        axis.fill_between(
            x,
            p05,
            p95,
            color=SEVERITY_COLORS[severity],
            alpha=0.11,
            linewidth=0,
        )
        axis.plot(
            x,
            mean,
            color=SEVERITY_COLORS[severity],
            linestyle=line_style(severity),
            marker="o",
            markersize=4.5,
            linewidth=1.7,
            label=SEVERITY_LABELS[severity],
        )
    axis.axvline(1.0, color="#4d555a", linewidth=0.8, linestyle=(0, (3, 3)))
    axis.set_xlabel("Uniform assumed-speed multiplier")
    axis.set_ylabel("Population within 30 minutes (thousands)")
    axis.yaxis.set_major_formatter(FuncFormatter(thousands))
    axis.set_xticks([0.8, 1.0, 1.2])
    axis.set_xticklabels(["0.8×", "1.0×", "1.2×"])
    axis.legend(
        loc="lower right",
        frameon=True,
        framealpha=0.95,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=8,
        ncol=2,
    )
    axis.text(
        0.02,
        0.98,
        "Lines: means\nShading: P5–P95",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox={
            "facecolor": "white",
            "edgecolor": "#bdbdbd",
            "alpha": 0.94,
            "boxstyle": "round,pad=0.30",
        },
    )

    for label, axis in zip("abcd", axes.flat, strict=True):
        axis.text(
            -0.09,
            1.04,
            label,
            transform=axis.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
        )
        axis.grid(True, color="#d8dde0", linewidth=0.55, alpha=0.72)
        for spine in axis.spines.values():
            spine.set_visible(True)
            spine.set_color("#39434a")
            spine.set_linewidth(0.8)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    print(
        "Final convergence:",
        final[
            [
                "Expected Failed Road Length Share",
                "Monte Carlo Convergence Status",
            ]
        ].to_dict(orient="records"),
    )
    print(
        "Speed sensitivity mean 30-minute coverage:",
        speed_summary[
            [
                "Expected Failed Road Length Share",
                "Assumed Speed Multiplier",
                "Mean",
            ]
        ].to_dict(orient="records"),
    )


if __name__ == "__main__":
    main()
