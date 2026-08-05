#!/usr/bin/env python3
"""Baseline Two-Stage Emergency Travel Time.

Plan: Map baseline ambulance dispatch, incident-to-hospital transport, and total
two-stage travel time for populated 125 m meshes.
Framework: Section 5 baseline accessibility contrast, Section 6.2 two-stage
shortest-path equations at m=1.0, and Section 7 Step 2.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from pyproj import Transformer
from shapely.geometry import LineString

from emergency_routing import compute_baseline_access


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_baseline_two_stage_emergency_travel_time.png"
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300


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
    """Apply a common extent, geographic frame, and aspect ratio."""
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
    label: str,
) -> None:
    """Add a stage-specific colorbar using the common 0-45 minute scale."""
    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=colorbar_ax, orientation="horizontal", extend="max")
    colorbar.set_ticks([0, 5, 10, 15, 30, 45])
    colorbar.set_label(label, fontsize=9)
    colorbar.ax.tick_params(labelsize=8, length=2)


def main() -> None:
    baseline = compute_baseline_access(PROCESSED)
    mesh = gpd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet",
        columns=["Mesh Code", "Total Population", "Geometry"],
    ).to_crs(MAP_CRS)
    time_columns = [
        "Mesh Code",
        "Dispatch Travel Time",
        "Hospital Transport Time",
        "Total Emergency Access Time",
    ]
    mesh = mesh.merge(
        baseline.demand[time_columns],
        on="Mesh Code",
        how="left",
        validate="one_to_one",
    )
    boundary = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Geometry"],
    ).to_crs(MAP_CRS)
    dispatch = gpd.read_parquet(
        PROCESSED / "kumamoto_dispatch_base_network_access_preprocessed.parquet",
        columns=["Candidate Dispatch Base", "Network Snap Accepted", "Geometry"],
    ).to_crs(MAP_CRS)
    dispatch = dispatch.loc[dispatch["Candidate Dispatch Base"] & dispatch["Network Snap Accepted"]]
    hospitals = gpd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=["Eligible Emergency Hospital", "Network Snap Accepted", "Geometry"],
    ).to_crs(MAP_CRS)
    hospitals = hospitals.loc[
        hospitals["Eligible Emergency Hospital"] & hospitals["Network Snap Accepted"]
    ]
    roads = gpd.read_parquet(
        PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=["Road Category", "Width Category", "Geometry"],
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
    major_roads = roads.loc[
        roads["Road Category"].isin(arterial_categories)
        | roads["Width Category"].isin(wider_categories)
    ]
    national_roads = roads.loc[
        roads["Road Category"].isin(
            {"National Expressway or Equivalent", "National Highway"}
        )
    ]

    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)
    cmap_name = "YlOrRd"
    cmap = plt.get_cmap(cmap_name).copy()
    cmap.set_bad("#c7c9cc")
    norm = Normalize(vmin=0.0, vmax=45.0, clip=False)
    panels = [
        ("Dispatch Travel Time", "Dispatch travel time (minutes)"),
        ("Hospital Transport Time", "Hospital transport time (minutes)"),
        ("Total Emergency Access Time", "Total two-stage travel time (minutes)"),
    ]

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(17.2, 6.6), constrained_layout=True)
    grid = fig.add_gridspec(2, 3, height_ratios=(1.0, 0.045), hspace=0.035, wspace=0.055)
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    colorbar_axes = [fig.add_subplot(grid[1, column]) for column in range(3)]

    for panel_number, (ax, colorbar_ax, (variable, label)) in enumerate(
        zip(axes, colorbar_axes, panels, strict=True)
    ):
        boundary.plot(ax=ax, color="#f2f2f2", edgecolor="none", zorder=0)
        mesh.plot(
            ax=ax,
            column=variable,
            cmap=cmap,
            norm=norm,
            linewidth=0,
            missing_kwds={"color": "#c7c9cc"},
            rasterized=True,
            zorder=1,
        )
        major_roads.plot(
            ax=ax,
            color="#45545e",
            linewidth=0.22,
            alpha=0.72,
            rasterized=True,
            zorder=3,
        )
        national_roads.plot(
            ax=ax,
            color="white",
            linewidth=0.78,
            alpha=0.88,
            rasterized=True,
            zorder=3.2,
        )
        national_roads.plot(
            ax=ax,
            color="#17242c",
            linewidth=0.42,
            alpha=0.96,
            rasterized=True,
            zorder=3.3,
        )
        boundary.boundary.plot(ax=ax, color="#4d4d4d", linewidth=0.28, alpha=0.8, zorder=4)
        if panel_number in (0, 2):
            dispatch.plot(
                ax=ax,
                marker="^",
                color="#2166ac",
                edgecolor="white",
                linewidth=0.35,
                markersize=20,
                alpha=0.95,
                zorder=6,
            )
        if panel_number in (1, 2):
            hospitals.plot(
                ax=ax,
                marker="P",
                color="#762a83",
                edgecolor="white",
                linewidth=0.35,
                markersize=23,
                alpha=0.95,
                zorder=7,
            )
        style_map(ax, bounds, geographic_bounds)
        add_colorbar(fig, colorbar_ax, norm, cmap_name, label)

    axes[2].legend(
        handles=[
            Line2D(
                [0], [0], color="#45545e", linewidth=1.4,
                label="Major routable road"
            ),
            Line2D(
                [0], [0], marker="^", color="none", markerfacecolor="#2166ac",
                markeredgecolor="white", markersize=7, label="Candidate dispatch base"
            ),
            Line2D(
                [0], [0], marker="P", color="none", markerfacecolor="#762a83",
                markeredgecolor="white", markersize=7, label="Eligible emergency hospital"
            ),
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
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    for key, value in baseline.diagnostics.items():
        print(f"{key}: {value:,}")


if __name__ == "__main__":
    main()
