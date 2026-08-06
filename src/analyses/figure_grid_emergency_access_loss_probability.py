#!/usr/bin/env python3
"""Grid Emergency Access Loss Probability.

Plan: Map the probability that a baseline-timely population grid loses
30-minute emergency access under the 1%, 3%, and 5% main scenarios.
Framework: AnaSOP Sections 5.2, 6.2, and Analytical Workflow step 4.
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
EXPERIMENT = ROOT / "data" / "exp" / "monte_carlo_length_weighted_full_1000"
OUTPUT = (
    ROOT
    / "data"
    / "results"
    / "figures"
    / "Figure_grid_emergency_access_loss_probability.png"
)
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
LEVELS = (0.01, 0.03, 0.05)
PROBABILITY_COLUMN = "Grid Access Loss Probability 30 Minutes"
MAJOR_CATEGORIES = {
    "National Expressway or Equivalent",
    "National Highway",
    "Prefectural Road",
}


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
        zorder=2.5,
    )

    transformer = Transformer.from_crs(GEOGRAPHIC_CRS, MAP_CRS, always_xy=True)
    centre_latitude = (latitude_minimum + latitude_maximum) / 2
    centre_longitude = (longitude_minimum + longitude_maximum) / 2
    label_style = {"fontsize": 7.2, "color": "#3f4a52", "clip_on": False}
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
        spine.set_zorder(10)


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


def main() -> None:
    boundary = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Geometry"],
    ).to_crs(MAP_CRS)
    mesh = gpd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet",
        columns=["Mesh Code", "Geometry"],
    )
    reliability = pd.read_parquet(
        EXPERIMENT / "grid_reliability.parquet",
        columns=[
            "Mesh Code",
            "Expected Failed Road Length Share",
            "Total Population",
            PROBABILITY_COLUMN,
        ],
    )
    roads = gpd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=["Road Category", "Geometry"],
    ).to_crs(MAP_CRS)
    major_roads = roads.loc[roads["Road Category"].isin(MAJOR_CATEGORIES)]

    mesh["Mesh Code"] = mesh["Mesh Code"].astype(str)
    reliability["Mesh Code"] = reliability["Mesh Code"].astype(str)
    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)
    cmap = LinearSegmentedColormap.from_list(
        "blue_green_yellow_red",
        ["#2166ac", "#1a9850", "#fee08b", "#d73027"],
        N=256,
    )
    norm = LogNorm(vmin=0.001, vmax=1.0)

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(17.2, 6.9), constrained_layout=True)
    grid = fig.add_gridspec(
        2,
        3,
        height_ratios=(1.0, 0.055),
        hspace=0.045,
        wspace=0.055,
    )
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    colorbar_axis = fig.add_subplot(grid[1, :])
    diagnostics: list[dict[str, float | int]] = []

    for axis, level in zip(axes, LEVELS, strict=True):
        values = reliability.loc[
            reliability["Expected Failed Road Length Share"].eq(level)
        ].copy()
        if len(values) != len(mesh):
            raise RuntimeError(f"Unexpected grid count for severity {level}")
        mapped = mesh.merge(
            values,
            on="Mesh Code",
            how="left",
            validate="one_to_one",
        ).to_crs(MAP_CRS)
        if mapped[PROBABILITY_COLUMN].isna().any():
            raise RuntimeError(f"Missing grid probabilities for severity {level}")
        zero = mapped[PROBABILITY_COLUMN].eq(0)
        positive = mapped[PROBABILITY_COLUMN].gt(0)
        expected_population_loss = float(
            (
                mapped["Total Population"]
                * mapped[PROBABILITY_COLUMN]
            ).sum()
        )
        diagnostics.append(
            {
                "expected_percent": int(round(100 * level)),
                "positive_probability_grids": int(positive.sum()),
                "expected_population_loss": expected_population_loss,
            }
        )

        boundary.plot(ax=axis, color="#e8ecef", edgecolor="none", zorder=0)
        mapped.loc[zero].plot(
            ax=axis,
            color="white",
            linewidth=0,
            rasterized=True,
            zorder=1,
        )
        mapped.loc[positive].plot(
            ax=axis,
            column=PROBABILITY_COLUMN,
            cmap=cmap,
            norm=norm,
            linewidth=0,
            rasterized=True,
            zorder=1.2,
        )
        roads.plot(
            ax=axis,
            color="#5f666b",
            linewidth=0.075,
            alpha=0.25,
            rasterized=True,
            zorder=2,
        )
        major_roads.plot(
            ax=axis,
            color="#2f3437",
            linewidth=0.19,
            alpha=0.48,
            rasterized=True,
            zorder=2.2,
        )
        boundary.boundary.plot(
            ax=axis,
            color="#40484d",
            linewidth=0.30,
            alpha=0.86,
            zorder=3,
        )
        style_map(axis, bounds, geographic_bounds)
        axis.text(
            0.975,
            0.975,
            (
                f"Expected failed length: {100 * level:g}%\n"
                f"Grids with positive loss probability: {int(positive.sum()):,}\n"
                f"Expected population loss: {expected_population_loss:,.0f}"
            ),
            transform=axis.transAxes,
            ha="right",
            va="top",
            fontsize=8.0,
            linespacing=1.35,
            bbox={
                "facecolor": "white",
                "edgecolor": "#bdbdbd",
                "alpha": 0.94,
                "boxstyle": "round,pad=0.32",
            },
            zorder=8,
        )

    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar.set_array([])
    colorbar = fig.colorbar(
        scalar,
        cax=colorbar_axis,
        orientation="horizontal",
    )
    ticks = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
    colorbar.set_ticks(ticks)
    colorbar.set_ticklabels(["0.1%", "0.3%", "1%", "3%", "10%", "30%", "100%"])
    colorbar.set_label(
        "Probability of losing baseline 30-minute emergency access (log scale)",
        fontsize=9,
    )
    colorbar.ax.tick_params(labelsize=8, length=2)

    for label, axis in zip("abc", axes, strict=True):
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
    axes[2].legend(
        handles=[
            Patch(
                facecolor="#e8ecef",
                edgecolor="#90979c",
                linewidth=0.7,
                label="No represented population grid",
            ),
            Patch(
                facecolor="white",
                edgecolor="#90979c",
                linewidth=0.7,
                label="Zero loss probability",
            ),
            Line2D(
                [0], [0], color="#5f666b", linewidth=1.0, label="Road network"
            ),
            Line2D(
                [0], [0], color="#2f3437", linewidth=1.6, label="Major road"
            ),
        ],
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=8,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    print(pd.DataFrame(diagnostics).to_string(index=False))


if __name__ == "__main__":
    main()
