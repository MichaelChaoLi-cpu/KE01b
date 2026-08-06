#!/usr/bin/env python3
"""Road-Section Accessibility Consequence and Expected Risk.

Plan: Map every junction-to-junction road section. The upper row shows
potential population-access loss at 15, 30, and 45 minutes; the lower row
shows probability-weighted 30-minute expected risk at 1%, 3%, and 5% severity.
Framework: AnaSOP Sections 5.3, 6.5, and Analytical Workflow step 7.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pyproj import Transformer
from shapely.geometry import LineString


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
EXPERIMENT = ROOT / "data" / "exp" / "road_section_accessibility_consequence"
OUTPUT = (
    ROOT
    / "data"
    / "results"
    / "figures"
    / "Figure_road_section_accessibility_consequence_and_expected_risk.png"
)
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
THRESHOLDS = (15, 30, 45)
SEVERITIES = (1, 3, 5)
MAJOR_CATEGORIES = {
    "National Expressway or Equivalent",
    "National Highway",
    "Prefectural Road",
}
VALUE_CMAP = LinearSegmentedColormap.from_list(
    "BlueGreenYellowRed",
    ["#2166ac", "#1a9850", "#fee08b", "#d73027"],
    N=256,
)


def graticule_values(lower: float, upper: float, step: float) -> list[float]:
    start = math.ceil((lower - 1e-9) / step) * step
    stop = math.floor((upper + 1e-9) / step) * step
    count = int(round((stop - start) / step)) + 1
    return [round(start + index * step, 8) for index in range(max(0, count))]


def add_graticule(
    axis: plt.Axes,
    geographic_bounds: tuple[float, float, float, float],
    step: float = 0.25,
) -> None:
    longitude_minimum, latitude_minimum, longitude_maximum, latitude_maximum = (
        geographic_bounds
    )
    longitudes = graticule_values(longitude_minimum, longitude_maximum, step)
    latitudes = graticule_values(latitude_minimum, latitude_maximum, step)
    samples = 160
    lines: list[LineString] = []
    for longitude in longitudes:
        lines.append(
            LineString(
                zip(
                    np.full(samples, longitude),
                    np.linspace(
                        latitude_minimum - step,
                        latitude_maximum + step,
                        samples,
                    ),
                    strict=True,
                )
            )
        )
    for latitude in latitudes:
        lines.append(
            LineString(
                zip(
                    np.linspace(
                        longitude_minimum - step,
                        longitude_maximum + step,
                        samples,
                    ),
                    np.full(samples, latitude),
                    strict=True,
                )
            )
        )
    gpd.GeoSeries(lines, crs=GEOGRAPHIC_CRS).to_crs(MAP_CRS).plot(
        ax=axis,
        color="#7d8992",
        linewidth=0.42,
        linestyle=(0, (2.5, 3.5)),
        alpha=0.48,
        zorder=4.5,
    )

    transformer = Transformer.from_crs(GEOGRAPHIC_CRS, MAP_CRS, always_xy=True)
    centre_latitude = (latitude_minimum + latitude_maximum) / 2
    centre_longitude = (longitude_minimum + longitude_maximum) / 2
    label_style = {"fontsize": 6.8, "color": "#3f4a52", "clip_on": False}
    for longitude in longitudes:
        x_position, _ = transformer.transform(longitude, centre_latitude)
        axis.text(
            x_position,
            -0.014,
            f"{longitude:.2f}°E",
            transform=axis.get_xaxis_transform(),
            ha="center",
            va="top",
            **label_style,
        )
    for latitude in latitudes:
        _, y_position = transformer.transform(centre_longitude, latitude)
        axis.text(
            -0.012,
            y_position,
            f"{latitude:.2f}°N",
            transform=axis.get_yaxis_transform(),
            ha="right",
            va="center",
            **label_style,
        )
    axis.set_xticks([])
    axis.set_yticks([])
    for spine in axis.spines.values():
        spine.set_visible(True)
        spine.set_color("#303a40")
        spine.set_linewidth(0.85)
        spine.set_zorder(20)


def style_map(
    axis: plt.Axes,
    bounds: tuple[float, float, float, float],
    geographic_bounds: tuple[float, float, float, float],
) -> None:
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    axis.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    axis.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    axis.set_aspect("equal")
    add_graticule(axis, geographic_bounds)


def draw_network_surface(
    axis: plt.Axes,
    boundary: gpd.GeoDataFrame,
    roads: gpd.GeoDataFrame,
    major_roads: gpd.GeoDataFrame,
    value_column: str,
    norm: LogNorm,
) -> tuple[int, float]:
    values = roads[value_column].to_numpy(dtype=float)
    zero = values == 0
    positive = values > 0

    boundary.plot(ax=axis, color="#e7eaec", edgecolor="none", zorder=0)
    roads.plot(
        ax=axis,
        color="#555f65",
        linewidth=0.31,
        alpha=0.58,
        rasterized=True,
        zorder=1.0,
    )
    roads.loc[zero].plot(
        ax=axis,
        color="white",
        linewidth=0.15,
        alpha=0.98,
        rasterized=True,
        zorder=1.2,
    )
    roads.loc[positive].plot(
        ax=axis,
        column=value_column,
        cmap=VALUE_CMAP,
        norm=norm,
        linewidth=0.64,
        alpha=0.98,
        rasterized=True,
        zorder=2.5,
    )
    major_positive = major_roads[value_column].gt(0)
    major_roads.loc[major_positive].plot(
        ax=axis,
        column=value_column,
        cmap=VALUE_CMAP,
        norm=norm,
        linewidth=0.93,
        alpha=1.0,
        rasterized=True,
        zorder=2.8,
    )
    boundary.boundary.plot(
        ax=axis,
        color="#343c41",
        linewidth=0.31,
        alpha=0.88,
        zorder=4,
    )
    return int(positive.sum()), float(values[positive].max())


def annotation(
    axis: plt.Axes,
    heading: str,
    positive_count: int,
    maximum: float,
    maximum_label: str,
) -> None:
    axis.text(
        0.975,
        0.975,
        f"{heading}\nPositive-value sections: {positive_count:,}\n{maximum_label}: {maximum:,.2f}",
        transform=axis.transAxes,
        ha="right",
        va="top",
        fontsize=7.6,
        linespacing=1.35,
        bbox={
            "facecolor": "white",
            "edgecolor": "#bdbdbd",
            "alpha": 0.94,
            "boxstyle": "round,pad=0.30",
        },
        zorder=9,
    )


def main() -> None:
    result = pd.read_parquet(
        EXPERIMENT / "road_section_accessibility_consequence.parquet"
    )
    roads = gpd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=["Road Section ID", "Road Category", "Geometry"],
    )
    boundary = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Geometry"],
    ).to_crs(MAP_CRS)
    roads["Road Section ID"] = roads["Road Section ID"].astype(str)
    result["Road Section ID"] = result["Road Section ID"].astype(str)
    value_columns = [
        *[f"Potential Access Loss {threshold} Minutes" for threshold in THRESHOLDS],
        *[f"Expected Risk 30 Minutes {severity} Percent" for severity in SEVERITIES],
    ]
    roads = roads.merge(
        result[["Road Section ID", *value_columns]],
        on="Road Section ID",
        how="left",
        validate="one_to_one",
    )
    if roads[value_columns].isna().any().any():
        raise RuntimeError("Road geometry join left missing consequence values")
    roads = gpd.GeoDataFrame(roads, geometry="Geometry", crs=GEOGRAPHIC_CRS).to_crs(
        MAP_CRS
    )
    major_roads = roads.loc[roads["Road Category"].isin(MAJOR_CATEGORIES)]

    potential_maximum = float(
        roads[[f"Potential Access Loss {value} Minutes" for value in THRESHOLDS]]
        .to_numpy(dtype=float)
        .max()
    )
    risk_values = roads[
        [f"Expected Risk 30 Minutes {value} Percent" for value in SEVERITIES]
    ].to_numpy(dtype=float)
    positive_risk = risk_values[risk_values > 0]
    risk_minimum = float(positive_risk.min())
    risk_maximum = float(positive_risk.max())
    potential_norm = LogNorm(vmin=1.0, vmax=potential_maximum, clip=True)
    risk_norm = LogNorm(vmin=risk_minimum, vmax=risk_maximum, clip=True)

    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)
    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(17.2, 12.7), constrained_layout=True)
    grid = fig.add_gridspec(
        3,
        6,
        height_ratios=(1.0, 1.0, 0.050),
        hspace=0.055,
        wspace=0.055,
    )
    axes = np.array(
        [
            [fig.add_subplot(grid[0, 0:2]), fig.add_subplot(grid[0, 2:4]), fig.add_subplot(grid[0, 4:6])],
            [fig.add_subplot(grid[1, 0:2]), fig.add_subplot(grid[1, 2:4]), fig.add_subplot(grid[1, 4:6])],
        ]
    )
    potential_colorbar_axis = fig.add_subplot(grid[2, 0:3])
    risk_colorbar_axis = fig.add_subplot(grid[2, 3:6])

    diagnostics: list[dict[str, float | int | str]] = []
    for axis, threshold in zip(axes[0], THRESHOLDS, strict=True):
        column = f"Potential Access Loss {threshold} Minutes"
        positive_count, maximum = draw_network_surface(
            axis, boundary, roads, major_roads, column, potential_norm
        )
        annotation(
            axis,
            f"Timely-access threshold: {threshold} minutes",
            positive_count,
            maximum,
            "Maximum potential loss",
        )
        diagnostics.append(
            {
                "panel": f"potential_{threshold}",
                "positive_sections": positive_count,
                "maximum": maximum,
            }
        )
        style_map(axis, bounds, geographic_bounds)

    for axis, severity in zip(axes[1], SEVERITIES, strict=True):
        column = f"Expected Risk 30 Minutes {severity} Percent"
        positive_count, maximum = draw_network_surface(
            axis, boundary, roads, major_roads, column, risk_norm
        )
        annotation(
            axis,
            f"Expected failed road length: {severity}%",
            positive_count,
            maximum,
            "Maximum expected risk",
        )
        diagnostics.append(
            {
                "panel": f"risk_{severity}_percent",
                "positive_sections": positive_count,
                "maximum": maximum,
            }
        )
        style_map(axis, bounds, geographic_bounds)

    potential_scalar = plt.cm.ScalarMappable(norm=potential_norm, cmap=VALUE_CMAP)
    potential_scalar.set_array([])
    potential_colorbar = fig.colorbar(
        potential_scalar,
        cax=potential_colorbar_axis,
        orientation="horizontal",
    )
    potential_ticks = [1, 10, 100, 1_000, 10_000, potential_maximum]
    potential_ticks = sorted(set(value for value in potential_ticks if value <= potential_maximum))
    potential_colorbar.set_ticks(potential_ticks)
    potential_colorbar.set_ticklabels([f"{value:,.0f}" for value in potential_ticks])
    potential_colorbar.set_label(
        "Potential population losing timely access after single-section removal (log scale)",
        fontsize=8.6,
    )
    potential_colorbar.ax.tick_params(labelsize=7.7, length=2)

    risk_scalar = plt.cm.ScalarMappable(norm=risk_norm, cmap=VALUE_CMAP)
    risk_scalar.set_array([])
    risk_colorbar = fig.colorbar(
        risk_scalar,
        cax=risk_colorbar_axis,
        orientation="horizontal",
    )
    risk_candidates = [
        0.001,
        0.01,
        0.1,
        1,
        10,
        100,
        1_000,
        risk_maximum,
    ]
    risk_ticks = sorted(
        set(value for value in risk_candidates if risk_minimum <= value <= risk_maximum)
    )
    risk_colorbar.set_ticks(risk_ticks)
    risk_colorbar.set_ticklabels(
        [f"{value:,.3g}" if value < 1 else f"{value:,.0f}" for value in risk_ticks]
    )
    risk_colorbar.set_label(
        "30-minute expected risk: failure probability × potential population loss (log scale)",
        fontsize=8.6,
    )
    risk_colorbar.ax.tick_params(labelsize=7.7, length=2)

    axes[0, 0].legend(
        handles=[
            Line2D(
                [0],
                [0],
                color="#555f65",
                linewidth=2.4,
                label="Road-section outline",
            ),
            Line2D(
                [0],
                [0],
                color="white",
                markeredgecolor="#555f65",
                linewidth=2.0,
                label="Zero value",
            ),
            Patch(
                facecolor="#e7eaec",
                edgecolor="#343c41",
                linewidth=0.7,
                label="Kumamoto municipalities",
            ),
        ],
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=7.4,
    )

    for label, axis in zip("abcdef", axes.flat, strict=True):
        axis.text(
            -0.04,
            1.02,
            label,
            transform=axis.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    print(pd.DataFrame(diagnostics).to_string(index=False))


if __name__ == "__main__":
    main()
