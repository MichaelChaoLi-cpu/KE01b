#!/usr/bin/env python3
"""Critical Medical Corridors.

Plan: Map Low, Central, and High scenario path-dependency Road Shapley Values.
Framework: Section 6.6 exact fixed-baseline-chain estimator and Section 7 Steps 7-8.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from pyproj import Transformer
from shapely.geometry import LineString

from emergency_routing import scenario_availability_mask
from medical_corridor_path_shapley import (
    build_baseline_path_context,
    compute_path_shapley,
)


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_critical_medical_corridors.png"
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
PRIMARY_THRESHOLD = 30
SCENARIOS = ["Low", "Central", "High"]
SHAPLEY_COLUMN = "Path-Dependency Road Shapley Value"


def graticule_values(lower: float, upper: float, step: float) -> list[float]:
    """Return stable graticule values within a geographic extent."""
    start = math.ceil((lower - 1e-9) / step) * step
    stop = math.floor((upper + 1e-9) / step) * step
    count = int(round((stop - start) / step)) + 1
    return [round(start + index * step, 8) for index in range(max(0, count))]


def add_graticule(
    ax: plt.Axes,
    geographic_bounds: tuple[float, float, float, float],
    step: float = 0.25,
) -> None:
    """Draw and label longitude/latitude graticules on projected map axes."""
    longitude_minimum, latitude_minimum, longitude_maximum, latitude_maximum = geographic_bounds
    longitudes = graticule_values(longitude_minimum, longitude_maximum, step)
    latitudes = graticule_values(latitude_minimum, latitude_maximum, step)
    samples = 160
    lines: list[LineString] = []
    for longitude in longitudes:
        lines.append(
            LineString(
                zip(
                    np.full(samples, longitude),
                    np.linspace(latitude_minimum - step, latitude_maximum + step, samples),
                    strict=True,
                )
            )
        )
    for latitude in latitudes:
        lines.append(
            LineString(
                zip(
                    np.linspace(longitude_minimum - step, longitude_maximum + step, samples),
                    np.full(samples, latitude),
                    strict=True,
                )
            )
        )
    gpd.GeoSeries(lines, crs=GEOGRAPHIC_CRS).to_crs(MAP_CRS).plot(
        ax=ax,
        color="#7d8992",
        linewidth=0.42,
        linestyle=(0, (2.5, 3.5)),
        alpha=0.48,
        zorder=2,
    )

    transformer = Transformer.from_crs(GEOGRAPHIC_CRS, MAP_CRS, always_xy=True)
    centre_latitude = (latitude_minimum + latitude_maximum) / 2
    centre_longitude = (longitude_minimum + longitude_maximum) / 2
    label_style = {"fontsize": 7.0, "color": "#3f4a52", "clip_on": False}
    for longitude in longitudes:
        x_position, _ = transformer.transform(longitude, centre_latitude)
        ax.text(
            x_position,
            -0.014,
            f"{longitude:.2f}°E",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            **label_style,
        )
    for latitude in latitudes:
        _, y_position = transformer.transform(centre_longitude, latitude)
        ax.text(
            -0.012,
            y_position,
            f"{latitude:.2f}°N",
            transform=ax.get_yaxis_transform(),
            ha="right",
            va="center",
            **label_style,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#303a40")
        spine.set_linewidth(0.85)
        spine.set_zorder(20)


def style_map(
    ax: plt.Axes,
    bounds: tuple[float, float, float, float],
    geographic_bounds: tuple[float, float, float, float],
) -> None:
    """Apply one aligned extent and geographic frame."""
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    ax.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    ax.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    ax.set_aspect("equal")
    add_graticule(ax, geographic_bounds)


def corridor_width(values: np.ndarray, global_minimum: float, global_maximum: float) -> np.ndarray:
    """Scale positive corridor widths by their common logarithmic value range."""
    logged = np.log10(values)
    lower = math.log10(global_minimum)
    upper = math.log10(global_maximum)
    if upper <= lower + 1e-12:
        return np.full(len(values), 2.0)
    return 0.65 + 2.25 * (logged - lower) / (upper - lower)


def main() -> None:
    print("Building the shared baseline two-stage path context...", flush=True)
    context = build_baseline_path_context(PROCESSED)
    results = []
    for scenario in SCENARIOS:
        print(f"Computing {scenario} path-dependency Shapley values...", flush=True)
        results.append(
            compute_path_shapley(
                PROCESSED,
                context,
                scenario=scenario,
                threshold=PRIMARY_THRESHOLD,
            )
        )

    roads = gpd.read_parquet(
        PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=[
            "Medical Corridor ID",
            "Road Category",
            "Width Category",
            "Road Available",
            "Network Analysis Eligible",
            "Hazard Exposure Class",
            "Road State",
            "Geometry",
        ],
    ).to_crs(MAP_CRS)
    municipalities = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Municipality Code", "Geometry"],
    ).to_crs(MAP_CRS)
    major_mask = roads["Road Category"].isin(
        {"National Expressway or Equivalent", "National Highway", "Prefectural Road"}
    ) | roads["Width Category"].isin(
        {"5.5 to Under 13 m", "13 to Under 19.5 m", "19.5 m or More"}
    )

    positive_values = np.concatenate(
        [result.values[SHAPLEY_COLUMN].to_numpy(dtype=float) for result in results]
    )
    positive_values = positive_values[positive_values > 0]
    if not len(positive_values):
        raise RuntimeError("No positive path-dependency corridor values were identified")
    global_minimum = float(positive_values.min())
    global_maximum = float(positive_values.max())
    color_norm = LogNorm(vmin=global_minimum, vmax=global_maximum)
    panel_data = []
    for result in results:
        available = scenario_availability_mask(roads, result.scenario)
        available_all = roads.loc[available]
        available_major = roads.loc[available & major_mask]
        unavailable = roads.loc[roads["Network Analysis Eligible"].fillna(False) & ~available]
        critical = unavailable.loc[
            unavailable["Medical Corridor ID"].isin(result.values["Medical Corridor ID"])
        ].dissolve(by="Medical Corridor ID", as_index=False)
        critical = critical.merge(
            result.values[
                ["Medical Corridor ID", SHAPLEY_COLUMN, "Scenario Priority Rank"]
            ],
            on="Medical Corridor ID",
            validate="one_to_one",
        )
        critical["Line Width"] = corridor_width(
            critical[SHAPLEY_COLUMN].to_numpy(dtype=float),
            global_minimum,
            global_maximum,
        )
        panel_data.append((result, available_all, available_major, unavailable, critical))

    bounds = tuple(municipalities.total_bounds)
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(20.0, 8.1), constrained_layout=True)
    grid = fig.add_gridspec(2, 3, height_ratios=(1.0, 0.045), hspace=0.035, wspace=0.055)
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    colorbar_ax = fig.add_subplot(grid[1, :])

    for ax, (result, available_all, available_major, unavailable, critical) in zip(
        axes, panel_data, strict=True
    ):
        municipalities.plot(
            ax=ax,
            color="#f3f2ee",
            edgecolor="#62696d",
            linewidth=0.32,
            zorder=1,
        )
        available_all.plot(
            ax=ax,
            color="#a6dba0",
            linewidth=0.08,
            alpha=0.42,
            rasterized=True,
            zorder=2.7,
        )
        available_major.plot(
            ax=ax,
            color="#1b7837",
            linewidth=0.24,
            alpha=0.88,
            rasterized=True,
            zorder=3,
        )
        unavailable.plot(
            ax=ax,
            color="#0072b2",
            linewidth=0.30,
            alpha=0.88,
            rasterized=True,
            zorder=4,
        )
        critical.plot(
            ax=ax,
            color="white",
            linewidth=critical["Line Width"] + 0.95,
            alpha=0.96,
            zorder=6,
        )
        critical.plot(
            ax=ax,
            column=SHAPLEY_COLUMN,
            cmap="YlOrRd",
            norm=color_norm,
            linewidth=critical["Line Width"],
            alpha=0.98,
            zorder=7,
        )
        municipalities.boundary.plot(
            ax=ax, color="#424a4f", linewidth=0.38, alpha=0.9, zorder=8
        )
        style_map(ax, bounds, geographic_bounds)
        ax.legend(
            handles=[
                Line2D([0], [0], color="#a6dba0", linewidth=1.2, label="Assumed available road"),
                Line2D([0], [0], color="#1b7837", linewidth=1.5, label="Assumed available major road"),
                Line2D([0], [0], color="#0072b2", linewidth=1.4, label="Assumed unavailable road"),
                Line2D(
                    [0], [0], color="#d7301f", linewidth=2.5,
                    label="Unavailable critical corridor (positive value)"
                ),
            ],
            title=f"{result.scenario} scenario",
            loc="upper left",
            bbox_to_anchor=(0.015, 0.985),
            borderaxespad=0.0,
            frameon=True,
            framealpha=0.94,
            facecolor="white",
            edgecolor="#bdbdbd",
            fontsize=7.4,
            title_fontsize=7.8,
        )

    scalar = plt.cm.ScalarMappable(norm=color_norm, cmap="YlOrRd")
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=colorbar_ax, orientation="horizontal")
    colorbar.set_label(
        "30-minute path-dependency Road Shapley Value (people, logarithmic color scale)",
        fontsize=8.7,
    )
    colorbar.ax.tick_params(labelsize=8, length=2)
    for label, ax in zip("abc", axes, strict=True):
        ax.text(
            -0.04,
            1.02,
            label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}", flush=True)
    for result in results:
        print(f"{result.scenario} diagnostics: {result.diagnostics}", flush=True)
        print(
            result.values.head(10)[
                ["Medical Corridor ID", SHAPLEY_COLUMN, "Scenario Priority Rank"]
            ].to_string(index=False),
            flush=True,
        )


if __name__ == "__main__":
    main()
