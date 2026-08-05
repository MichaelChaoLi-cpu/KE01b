#!/usr/bin/env python3
"""Population Losing Timely Emergency Access.

Plan: Compare total, age-65+, and age-75+ populations that lose baseline timely
access at 15-, 30-, and 45-minute thresholds under nested disruption scenarios.
Framework: Section 6.3 population-loss equation and Section 7 Step 4, using
125 m meshes for total population and disclosure groups for older populations.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.ticker import StrMethodFormatter

from emergency_routing import compute_emergency_access


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_population_losing_timely_emergency_access.png"
FIGURE_DPI = 300
SCENARIOS = ("Baseline", "Low", "Central", "High")
DISRUPTION_SCENARIOS = ("Low", "Central", "High")
THRESHOLDS = (15, 30, 45)


def loss_by_threshold(
    scenario_results: dict[str, pd.DataFrame],
    support: str,
    weight: str,
) -> pd.DataFrame:
    """Evaluate Section 6.3 loss relative to baseline on one spatial support."""
    baseline = scenario_results["Baseline"].loc[
        scenario_results["Baseline"]["Demand Support"].eq(support),
        ["Analysis Unit ID", "Total Emergency Access Time", weight],
    ].rename(columns={"Total Emergency Access Time": "Baseline Time"})
    records: list[dict[str, int | str]] = []
    for scenario in DISRUPTION_SCENARIOS:
        scenario_time = scenario_results[scenario].loc[
            scenario_results[scenario]["Demand Support"].eq(support),
            ["Analysis Unit ID", "Total Emergency Access Time"],
        ].rename(columns={"Total Emergency Access Time": "Scenario Time"})
        comparison = baseline.merge(
            scenario_time,
            on="Analysis Unit ID",
            how="left",
            validate="one_to_one",
        )
        population_weight = comparison[weight].fillna(0).astype(float)
        for threshold in THRESHOLDS:
            baseline_timely = comparison["Baseline Time"].le(threshold)
            scenario_timely = comparison["Scenario Time"].le(threshold)
            lost = int(population_weight.loc[baseline_timely & ~scenario_timely].sum())
            records.append(
                {
                    "Scenario": scenario,
                    "Threshold": threshold,
                    "Population Losing Timely Access": lost,
                }
            )
    result = pd.DataFrame(records)
    pivot = result.pivot(
        index="Threshold",
        columns="Scenario",
        values="Population Losing Timely Access",
    ).reindex(index=THRESHOLDS, columns=DISRUPTION_SCENARIOS)
    if not ((pivot["Low"] <= pivot["Central"]) & (pivot["Central"] <= pivot["High"])).all():
        raise RuntimeError(f"Non-monotone timely-access loss for {weight}")
    return pivot


def incremental_segments(absolute_loss: pd.DataFrame) -> pd.DataFrame:
    """Convert nested absolute losses to non-overlapping stacked segments."""
    return pd.DataFrame(
        {
            "Lost under Low": absolute_loss["Low"],
            "Additional loss under Central": absolute_loss["Central"] - absolute_loss["Low"],
            "Additional loss under High": absolute_loss["High"] - absolute_loss["Central"],
        },
        index=absolute_loss.index,
    )


def main() -> None:
    scenario_results: dict[str, pd.DataFrame] = {}
    for scenario in SCENARIOS:
        print(f"Computing {scenario} scenario for mesh and disclosure-group demand...", flush=True)
        scenario_results[scenario] = compute_emergency_access(
            PROCESSED,
            scenario=scenario,
            demand_support="combined",
        ).demand

    panel_specs = [
        ("mesh", "Total Population", "Total population losing timely access"),
        ("group", "Population Age 65+", "Population age 65+ losing timely access"),
        ("group", "Population Age 75+", "Population age 75+ losing timely access"),
    ]
    losses = [
        loss_by_threshold(scenario_results, support, weight)
        for support, weight, _ in panel_specs
    ]
    segments = [incremental_segments(loss) for loss in losses]

    colors = {
        "Lost under Low": "#fdae61",
        "Additional loss under Central": "#f46d43",
        "Additional loss under High": "#a50026",
    }
    sns.set_theme(context="paper", style="whitegrid", font_scale=1.0)
    fig, axes = plt.subplots(1, 3, figsize=(15.8, 5.6), constrained_layout=True)
    positions = np.arange(len(THRESHOLDS))

    for ax, (_, _, y_label), absolute_loss, segment_frame in zip(
        axes,
        panel_specs,
        losses,
        segments,
        strict=True,
    ):
        bottom = np.zeros(len(THRESHOLDS), dtype=float)
        for segment_name in colors:
            values = segment_frame[segment_name].to_numpy(dtype=float)
            ax.bar(
                positions,
                values,
                width=0.66,
                bottom=bottom,
                color=colors[segment_name],
                edgecolor="white",
                linewidth=0.65,
                zorder=3,
            )
            bottom += values
        for position, total in zip(positions, absolute_loss["High"], strict=True):
            ax.annotate(
                f"{int(total):,}",
                xy=(position, float(total)),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                color="#30343b",
            )
        ax.set_xticks(positions, [str(value) for value in THRESHOLDS])
        ax.set_xlabel("Timely-access threshold (minutes)")
        ax.set_ylabel(y_label)
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
        ax.grid(axis="x", visible=False)
        ax.grid(axis="y", color="#d7dce0", linewidth=0.55, linestyle="--", alpha=0.8)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.margins(y=0.13)

    for label, ax in zip("abc", axes, strict=True):
        ax.text(
            -0.10,
            1.03,
            label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
        )

    fig.legend(
        handles=[Patch(facecolor=color, edgecolor="white", label=label) for label, color in colors.items()],
        loc="upper center",
        bbox_to_anchor=(0.5, 1.035),
        ncol=3,
        frameon=True,
        framealpha=0.96,
        edgecolor="#c2c7cc",
        fontsize=8.5,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    for (_, weight, _), absolute_loss in zip(panel_specs, losses, strict=True):
        for threshold in THRESHOLDS:
            values = absolute_loss.loc[threshold]
            print(
                f"{weight}; {threshold} min: Low={int(values['Low']):,}; "
                f"Central={int(values['Central']):,}; High={int(values['High']):,}"
            )


if __name__ == "__main__":
    main()

