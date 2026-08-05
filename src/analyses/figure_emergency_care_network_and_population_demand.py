#!/usr/bin/env python3
"""Emergency Care Network and Population Demand.

Plan: Show the spatial structure of total and older-population demand, candidate
ambulance dispatch bases, eligible emergency hospitals, and the road network.
Framework: Section 5 baseline network representation, Section 6.1 graph and
connector definitions, and Section 7 Step 1 network and population validation.
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


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_emergency_care_network_and_population_demand.png"
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300


def read_layer(filename: str, columns: list[str] | None = None) -> gpd.GeoDataFrame:
    frame = gpd.read_parquet(PROCESSED / filename, columns=columns)
    return frame.to_crs(MAP_CRS)


def add_colorbar(fig: plt.Figure, colorbar_ax: plt.Axes, cmap: str, norm: LogNorm, label: str) -> None:
    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=colorbar_ax, orientation="horizontal")
    colorbar.set_label(label, fontsize=9)
    colorbar.ax.tick_params(labelsize=8, length=2)


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
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    ax.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    ax.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    ax.set_aspect("equal")
    add_graticule(ax, geographic_bounds)


def main() -> None:
    boundary = read_layer("kumamoto_administrative_areas_preprocessed.parquet", ["Geometry"])
    population = read_layer(
        "kumamoto_population_mesh_125m_preprocessed.parquet", ["Total Population", "Geometry"]
    )
    older = read_layer(
        "kumamoto_population_disclosure_groups_preprocessed.parquet", ["Population Age 65+", "Geometry"]
    )
    roads = read_layer(
        "kumamoto_routable_road_edges_preprocessed.parquet", ["Road Category", "Geometry"]
    )
    emergency_routes = read_layer(
        "kumamoto_emergency_transport_roads_2024_preprocessed.parquet",
        ["Emergency Road Class", "Geometry"],
    )
    dispatch = read_layer(
        "kumamoto_dispatch_base_network_access_preprocessed.parquet",
        ["Candidate Dispatch Base", "Network Snap Accepted", "Geometry"],
    )
    hospitals = read_layer(
        "kumamoto_hospital_network_access_preprocessed.parquet",
        ["Eligible Emergency Hospital", "Network Snap Accepted", "Geometry"],
    )

    dispatch = dispatch.loc[dispatch["Candidate Dispatch Base"] & dispatch["Network Snap Accepted"]]
    hospitals = hospitals.loc[hospitals["Eligible Emergency Hospital"] & hospitals["Network Snap Accepted"]]
    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(17.2, 6.6), constrained_layout=True)
    grid = fig.add_gridspec(2, 3, height_ratios=(1.0, 0.045), hspace=0.035, wspace=0.055)
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    colorbar_axes = [fig.add_subplot(grid[1, column]) for column in range(2)]
    spacer_ax = fig.add_subplot(grid[1, 2])
    spacer_ax.set_axis_off()

    boundary.plot(ax=axes[0], color="#f2f2f2", edgecolor="none")
    population_norm = LogNorm(vmin=1, vmax=float(population["Total Population"].quantile(0.995)))
    population.plot(
        ax=axes[0], column="Total Population", cmap="viridis", norm=population_norm,
        linewidth=0, rasterized=True,
    )
    boundary.boundary.plot(ax=axes[0], color="#4d4d4d", linewidth=0.28, alpha=0.8)
    add_colorbar(
        fig,
        colorbar_axes[0],
        "viridis",
        population_norm,
        "Total population per 125 m mesh (log scale)",
    )

    boundary.plot(ax=axes[1], color="#f2f2f2", edgecolor="none")
    older_positive = older.loc[older["Population Age 65+"] > 0].copy()
    older_norm = LogNorm(vmin=1, vmax=float(older_positive["Population Age 65+"].quantile(0.995)))
    older_positive.plot(
        ax=axes[1], column="Population Age 65+", cmap="magma", norm=older_norm,
        linewidth=0, rasterized=True,
    )
    boundary.boundary.plot(ax=axes[1], color="#4d4d4d", linewidth=0.28, alpha=0.8)
    add_colorbar(
        fig,
        colorbar_axes[1],
        "magma",
        older_norm,
        "Population age 65+ per disclosure group (log scale)",
    )

    boundary.plot(ax=axes[2], color="#fafafa", edgecolor="none")
    roads.plot(ax=axes[2], color="#aeb4ba", linewidth=0.10, alpha=0.48, rasterized=True)
    route_style = {
        "Primary Emergency Road": ("#d73027", 1.25),
        "Secondary Emergency Road": ("#fdae61", 0.85),
    }
    for route_class, (color, width) in route_style.items():
        emergency_routes.loc[emergency_routes["Emergency Road Class"].eq(route_class)].plot(
            ax=axes[2], color=color, linewidth=width, alpha=0.95, rasterized=True
        )
    dispatch.plot(
        ax=axes[2], marker="^", color="#2166ac", edgecolor="white", linewidth=0.35,
        markersize=22, alpha=0.95, zorder=5,
    )
    hospitals.plot(
        ax=axes[2], marker="P", color="#762a83", edgecolor="white", linewidth=0.35,
        markersize=25, alpha=0.95, zorder=6,
    )
    boundary.boundary.plot(ax=axes[2], color="#4d4d4d", linewidth=0.30, alpha=0.8)
    legend_items = [
        Line2D([0], [0], color="#aeb4ba", lw=1.0, label="Standard road network"),
        Line2D([0], [0], color="#d73027", lw=2.0, label="Primary emergency road"),
        Line2D([0], [0], color="#fdae61", lw=2.0, label="Secondary emergency road"),
        Line2D([0], [0], marker="^", color="none", markerfacecolor="#2166ac", markeredgecolor="white", markersize=7, label="Candidate dispatch base"),
        Line2D([0], [0], marker="P", color="none", markerfacecolor="#762a83", markeredgecolor="white", markersize=7, label="Eligible emergency hospital"),
    ]
    axes[2].legend(
        handles=legend_items, loc="upper left", bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0, frameon=True, framealpha=0.94,
        facecolor="white", edgecolor="#bdbdbd", fontsize=8,
    )

    for label, ax in zip("abc", axes.flat, strict=True):
        style_map(ax, bounds, geographic_bounds)
        ax.text(
            -0.04, 1.02, label, transform=ax.transAxes, fontsize=12,
            fontweight="bold", va="top", ha="left",
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    print(
        f"Mapped {int(population['Total Population'].sum()):,} residents, "
        f"{int(older['Population Age 65+'].sum()):,} residents age 65+, "
        f"{len(dispatch)} dispatch bases, and {len(hospitals)} hospitals."
    )


if __name__ == "__main__":
    main()
