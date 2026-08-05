#!/usr/bin/env python3
"""Emergency Access under Road Disruption Scenarios.

Plan: Compare baseline total two-stage emergency travel time with the nested Low,
Central, and High road-disruption stress tests.
Framework: Section 5 nested disruption contrasts, Section 6.1 scenario graphs,
Section 6.2 two-stage access, and Section 7 Step 3.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from pyproj import Transformer
from shapely.geometry import LineString

from emergency_routing import compute_emergency_access, scenario_availability_mask


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_emergency_access_under_road_disruption_scenarios.png"
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
SCENARIOS = ("Baseline", "Low", "Central", "High")


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
    label_style = {"fontsize": 7.2, "color": "#3f4a52", "clip_on": False}
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
        spine.set_zorder(10)


def style_map(
    ax: plt.Axes,
    bounds: tuple[float, float, float, float],
    geographic_bounds: tuple[float, float, float, float],
) -> None:
    """Apply the common extent and geographic frame."""
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    ax.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    ax.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    ax.set_aspect("equal")
    add_graticule(ax, geographic_bounds)


def add_colorbar(
    fig: plt.Figure,
    colorbar_ax: plt.Axes,
    norm: Normalize,
    cmap: str,
    scenario: str,
) -> None:
    """Add a scenario-labelled colorbar using the common time scale."""
    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=colorbar_ax, orientation="horizontal", extend="max")
    colorbar.set_ticks([0, 5, 10, 15, 30, 45])
    label = (
        "Baseline total two-stage travel time (minutes)"
        if scenario == "Baseline"
        else f"{scenario} disruption total two-stage travel time (minutes)"
    )
    colorbar.set_label(label, fontsize=9)
    colorbar.ax.tick_params(labelsize=8, length=2)


def main() -> None:
    mesh = gpd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet",
        columns=["Mesh Code", "Total Population", "Geometry"],
    ).to_crs(MAP_CRS)
    diagnostics: dict[str, dict[str, float | int]] = {}
    for scenario in SCENARIOS:
        print(f"Computing {scenario} scenario...", flush=True)
        result = compute_emergency_access(PROCESSED, scenario=scenario)
        diagnostics[scenario] = result.diagnostics
        time_values = result.demand[["Mesh Code", "Total Emergency Access Time"]].rename(
            columns={"Total Emergency Access Time": f"{scenario} Total Time"}
        )
        mesh = mesh.merge(time_values, on="Mesh Code", how="left", validate="one_to_one")

    boundary = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Geometry"],
    ).to_crs(MAP_CRS)
    roads = gpd.read_parquet(
        PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=[
            "Road Category",
            "Width Category",
            "Road Available",
            "Network Analysis Eligible",
            "Hazard Exposure Class",
            "Road State",
            "Geometry",
        ],
    ).to_crs(MAP_CRS)

    arterial_categories = {
        "National Expressway or Equivalent",
        "National Highway",
        "Prefectural Road",
    }
    wider_categories = {
        "5.5 to Under 13 m",
        "13 to Under 19.5 m",
        "19.5 m or More",
    }
    major_mask = roads["Road Category"].isin(arterial_categories) | roads["Width Category"].isin(
        wider_categories
    )
    national_mask = roads["Road Category"].isin(
        {"National Expressway or Equivalent", "National Highway"}
    )

    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)
    cmap_name = "YlOrRd"
    cmap = plt.get_cmap(cmap_name).copy()
    cmap.set_bad("#c7c9cc")
    norm = Normalize(vmin=0.0, vmax=45.0, clip=False)

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(13.4, 12.2), constrained_layout=True)
    grid = fig.add_gridspec(
        4,
        2,
        height_ratios=(1.0, 0.045, 1.0, 0.045),
        hspace=0.035,
        wspace=0.055,
    )
    axes = np.array(
        [
            fig.add_subplot(grid[0, 0]),
            fig.add_subplot(grid[0, 1]),
            fig.add_subplot(grid[2, 0]),
            fig.add_subplot(grid[2, 1]),
        ]
    )
    colorbar_axes = [
        fig.add_subplot(grid[1, 0]),
        fig.add_subplot(grid[1, 1]),
        fig.add_subplot(grid[3, 0]),
        fig.add_subplot(grid[3, 1]),
    ]

    for ax, colorbar_ax, scenario in zip(axes, colorbar_axes, SCENARIOS, strict=True):
        available = scenario_availability_mask(roads, scenario)
        available_major = roads.loc[available & major_mask]
        available_national = roads.loc[available & national_mask]
        unavailable = roads.loc[roads["Network Analysis Eligible"] & ~available]

        boundary.plot(ax=ax, color="#f2f2f2", edgecolor="none", zorder=0)
        mesh.plot(
            ax=ax,
            column=f"{scenario} Total Time",
            cmap=cmap,
            norm=norm,
            linewidth=0,
            missing_kwds={"color": "#c7c9cc"},
            rasterized=True,
            zorder=1,
        )
        available_major.plot(
            ax=ax,
            color="#238b45",
            linewidth=0.22,
            alpha=0.80,
            rasterized=True,
            zorder=3,
        )
        available_national.plot(
            ax=ax,
            color="white",
            linewidth=0.78,
            alpha=0.88,
            rasterized=True,
            zorder=3.2,
        )
        available_national.plot(
            ax=ax,
            color="#005a32",
            linewidth=0.42,
            alpha=0.96,
            rasterized=True,
            zorder=3.3,
        )
        if not unavailable.empty:
            unavailable.plot(
                ax=ax,
                color="#0072b2",
                linewidth=0.28,
                alpha=0.92,
                rasterized=True,
                zorder=3.6,
            )
        boundary.boundary.plot(
            ax=ax,
            color="#4d4d4d",
            linewidth=0.30,
            alpha=0.82,
            zorder=4,
        )
        style_map(ax, bounds, geographic_bounds)
        add_colorbar(fig, colorbar_ax, norm, cmap_name, scenario)

    axes[3].legend(
        handles=[
            Line2D([0], [0], color="#238b45", linewidth=1.4, label="Available major road"),
            Line2D([0], [0], color="#0072b2", linewidth=1.4, label="Scenario-unavailable road"),
            Line2D(
                [0], [0], marker="s", color="none", markerfacecolor="#c7c9cc",
                markeredgecolor="#8c8c8c", markersize=7, label="Not estimated"
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

    for label, ax in zip("abcd", axes, strict=True):
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
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    for scenario in SCENARIOS:
        scenario_diagnostics = diagnostics[scenario]
        total_population = int(scenario_diagnostics["total_population"])
        finite_population = int(scenario_diagnostics["finite_total_population"])
        print(
            f"{scenario}: available edges={int(scenario_diagnostics['available_road_edges']):,}; "
            f"finite two-stage population={finite_population:,}/{total_population:,} "
            f"({100.0 * finite_population / total_population:.2f}%)"
        )


if __name__ == "__main__":
    main()
