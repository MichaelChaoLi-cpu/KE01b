#!/usr/bin/env python3
"""Nested Length-Dependent Road Failure Realizations.

Plan: Show one reproducible paired replicate at the 1%, 3%, and 5% main
scenarios and the 10% stress scenario.
Framework: AnaSOP Sections 5.1, 6.6, and Analytical Workflow step 3.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
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
    / "Figure_nested_length_dependent_road_failure_realizations.png"
)
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
LEVELS = (1, 3, 5, 10)
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
        zorder=1,
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
    sections = gpd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=["Road Section ID", "Road Category", "Geometry"],
    )
    realization = pd.read_parquet(
        EXPERIMENT / "nested_failure_realization_replicate_001.parquet"
    ).drop(columns=["Road Category"], errors="ignore")
    sections["Road Section ID"] = sections["Road Section ID"].astype(str)
    realization["Road Section ID"] = realization["Road Section ID"].astype(str)
    sections = sections.merge(
        realization,
        on="Road Section ID",
        how="left",
        validate="one_to_one",
    )
    if sections[[f"Road Failure Indicator {level}%" for level in LEVELS]].isna().any().any():
        raise RuntimeError("Some road sections lack replicate-001 failure states")
    sections = sections.to_crs(MAP_CRS)
    major = sections["Road Category"].isin(MAJOR_CATEGORIES)

    failure_columns = [f"Road Failure Indicator {level}%" for level in LEVELS]
    for previous, current in zip(failure_columns[:-1], failure_columns[1:], strict=True):
        if not sections.loc[sections[previous], current].all():
            raise RuntimeError("Replicate-001 failure states are not nested")

    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)
    total_length = float(sections["Road Section Length (m)"].sum())

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12.4, 11.5),
        constrained_layout=True,
    )
    diagnostics: list[dict[str, float | int]] = []
    for axis, level in zip(axes.flat, LEVELS, strict=True):
        failure_column = f"Road Failure Indicator {level}%"
        failed = sections[failure_column].astype(bool)
        available = ~failed
        available_major = available & major
        failed_sections = sections.loc[failed]
        realized_share = (
            float(failed_sections["Road Section Length (m)"].sum()) / total_length
        )
        diagnostics.append(
            {
                "expected_percent": level,
                "failed_sections": int(failed.sum()),
                "realized_percent": 100.0 * realized_share,
            }
        )

        boundary.plot(ax=axis, color="#f7f7f2", edgecolor="none", zorder=0)
        sections.loc[available].plot(
            ax=axis,
            color="#41ab5d",
            linewidth=0.11,
            alpha=0.62,
            rasterized=True,
            zorder=2,
        )
        sections.loc[available_major].plot(
            ax=axis,
            color="#006d2c",
            linewidth=0.27,
            alpha=0.90,
            rasterized=True,
            zorder=2.2,
        )
        failed_sections.plot(
            ax=axis,
            color="white",
            linewidth=1.05,
            alpha=0.98,
            rasterized=True,
            zorder=3,
        )
        failed_sections.plot(
            ax=axis,
            color="#d7301f",
            linewidth=0.58,
            alpha=0.98,
            rasterized=True,
            zorder=3.2,
        )
        boundary.boundary.plot(
            ax=axis,
            color="#40484d",
            linewidth=0.32,
            alpha=0.88,
            zorder=4,
        )
        style_map(axis, bounds, geographic_bounds)
        axis.text(
            0.975,
            0.975,
            (
                f"Expected failed length: {level}%\n"
                f"Failed sections: {int(failed.sum()):,}\n"
                f"Realized failed length: {100.0 * realized_share:.2f}%"
            ),
            transform=axis.transAxes,
            ha="right",
            va="top",
            fontsize=8.2,
            linespacing=1.35,
            bbox={
                "facecolor": "white",
                "edgecolor": "#bdbdbd",
                "alpha": 0.94,
                "boxstyle": "round,pad=0.32",
            },
            zorder=8,
        )

    for label, axis in zip("abcd", axes.flat, strict=True):
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
    axes[1, 1].legend(
        handles=[
            Line2D(
                [0], [0], color="#41ab5d", linewidth=1.5, label="Available road"
            ),
            Line2D(
                [0], [0], color="#006d2c", linewidth=1.8, label="Available major road"
            ),
            Line2D(
                [0], [0], color="#d7301f", linewidth=2.0, label="Failed road section"
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
