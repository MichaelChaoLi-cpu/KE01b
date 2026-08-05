#!/usr/bin/env python3
"""Municipal Emergency Accessibility Loss.

Plan: Map the confirmed Central-scenario municipal mean access-time increase and
the share of baseline-covered population age 65+ losing 30-minute access.
Framework: Section 6.3 confirmed municipal estimands and Section 7 Step 4.
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
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_municipal_emergency_accessibility_loss.png"
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
PRIMARY_SCENARIO = "Central"
PRIMARY_THRESHOLD = 30


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
    """Apply the common map extent and geographic frame."""
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    ax.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    ax.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    ax.set_aspect("equal")
    add_graticule(ax, geographic_bounds)


def municipality_lookup(
    features: gpd.GeoDataFrame,
    identifier: str,
    municipalities: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """Assign each demand support to one of the 49 administrative units."""
    points = features[[identifier, "Geometry"]].to_crs(MAP_CRS).copy()
    points["Geometry"] = points.geometry.representative_point()
    administrative = municipalities[["Municipality Code", "Municipality Label", "Geometry"]]
    joined = gpd.sjoin(points, administrative, how="left", predicate="within")
    if joined[identifier].duplicated().any():
        raise RuntimeError(f"Ambiguous municipality assignment for {identifier}")
    missing = joined["Municipality Code"].isna()
    if missing.any():
        nearest = gpd.sjoin_nearest(
            points.loc[missing, [identifier, "Geometry"]],
            administrative,
            how="left",
            max_distance=1_000.0,
        )
        nearest = nearest.set_index(identifier)
        joined = joined.set_index(identifier)
        joined.loc[nearest.index, ["Municipality Code", "Municipality Label"]] = nearest[
            ["Municipality Code", "Municipality Label"]
        ]
        joined = joined.reset_index()
    if joined["Municipality Code"].isna().any():
        raise RuntimeError(f"Unassigned municipality for {identifier}")
    return joined[[identifier, "Municipality Code", "Municipality Label"]]


def municipal_estimates(
    baseline: pd.DataFrame,
    central: pd.DataFrame,
    municipalities: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """Evaluate the two confirmed Section 6.3 municipal estimands."""
    mesh_geometry = gpd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet",
        columns=["Mesh Code", "Geometry"],
    )
    group_geometry = gpd.read_parquet(
        PROCESSED / "kumamoto_population_disclosure_groups_preprocessed.parquet",
        columns=["Disclosure Group Code", "Geometry"],
    )
    mesh_lookup = municipality_lookup(mesh_geometry, "Mesh Code", municipalities)
    group_lookup = municipality_lookup(group_geometry, "Disclosure Group Code", municipalities)

    baseline_mesh = baseline.loc[
        baseline["Demand Support"].eq("mesh"),
        ["Mesh Code", "Total Population", "Total Emergency Access Time"],
    ].rename(columns={"Total Emergency Access Time": "Baseline Time"})
    central_mesh = central.loc[
        central["Demand Support"].eq("mesh"),
        ["Mesh Code", "Total Emergency Access Time"],
    ].rename(columns={"Total Emergency Access Time": "Central Time"})
    mesh = baseline_mesh.merge(central_mesh, on="Mesh Code", validate="one_to_one").merge(
        mesh_lookup, on="Mesh Code", validate="one_to_one"
    )
    finite_pair = np.isfinite(mesh["Baseline Time"]) & np.isfinite(mesh["Central Time"])
    mesh["Comparable Population"] = mesh["Total Population"].where(finite_pair, 0)
    mesh["Weighted Increase"] = (
        mesh["Total Population"] * (mesh["Central Time"] - mesh["Baseline Time"])
    ).where(finite_pair, 0)
    time_summary = mesh.groupby("Municipality Code", as_index=False).agg(
        **{
            "Comparable Population": ("Comparable Population", "sum"),
            "Weighted Increase": ("Weighted Increase", "sum"),
        }
    )
    time_summary["Mean Access Time Increase (min)"] = (
        time_summary["Weighted Increase"] / time_summary["Comparable Population"].replace(0, np.nan)
    )

    baseline_group = baseline.loc[
        baseline["Demand Support"].eq("group"),
        ["Disclosure Group Code", "Population Age 65+", "Total Emergency Access Time"],
    ].rename(columns={"Total Emergency Access Time": "Baseline Time"})
    central_group = central.loc[
        central["Demand Support"].eq("group"),
        ["Disclosure Group Code", "Total Emergency Access Time"],
    ].rename(columns={"Total Emergency Access Time": "Central Time"})
    group = baseline_group.merge(
        central_group,
        on="Disclosure Group Code",
        validate="one_to_one",
    ).merge(group_lookup, on="Disclosure Group Code", validate="one_to_one")
    baseline_timely = group["Baseline Time"].le(PRIMARY_THRESHOLD)
    central_timely = group["Central Time"].le(PRIMARY_THRESHOLD)
    group["Baseline-Covered Population Age 65+"] = group["Population Age 65+"].where(
        baseline_timely, 0
    )
    group["Population Age 65+ Losing 30-Minute Access"] = group["Population Age 65+"].where(
        baseline_timely & ~central_timely, 0
    )
    loss_summary = group.groupby("Municipality Code", as_index=False).agg(
        **{
            "Baseline-Covered Population Age 65+": (
                "Baseline-Covered Population Age 65+",
                "sum",
            ),
            "Population Age 65+ Losing 30-Minute Access": (
                "Population Age 65+ Losing 30-Minute Access",
                "sum",
            ),
        }
    )
    loss_summary["Population Age 65+ Coverage Loss Rate (%)"] = 100.0 * (
        loss_summary["Population Age 65+ Losing 30-Minute Access"]
        / loss_summary["Baseline-Covered Population Age 65+"].replace(0, np.nan)
    )
    return time_summary.merge(loss_summary, on="Municipality Code", validate="one_to_one")


def add_colorbar(
    fig: plt.Figure,
    colorbar_ax: plt.Axes,
    norm: Normalize,
    cmap: str,
    label: str,
) -> None:
    """Add a horizontal municipal-estimate colorbar."""
    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=colorbar_ax, orientation="horizontal")
    colorbar.set_label(label, fontsize=8.7)
    colorbar.ax.tick_params(labelsize=8, length=2)


def main() -> None:
    print("Computing Baseline access for both population supports...", flush=True)
    baseline = compute_emergency_access(
        PROCESSED,
        scenario="Baseline",
        demand_support="combined",
    ).demand
    print("Computing Central access for both population supports...", flush=True)
    central = compute_emergency_access(
        PROCESSED,
        scenario=PRIMARY_SCENARIO,
        demand_support="combined",
    ).demand

    municipalities = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Municipality Code", "Municipality Label", "Geometry"],
    ).to_crs(MAP_CRS)
    estimates = municipal_estimates(baseline, central, municipalities)
    municipalities = municipalities.merge(
        estimates,
        on="Municipality Code",
        how="left",
        validate="one_to_one",
    )
    if len(municipalities) != 49:
        raise RuntimeError("Municipal output must retain 49 administrative units")

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
    available = scenario_availability_mask(roads, PRIMARY_SCENARIO)
    major_mask = roads["Road Category"].isin(
        {"National Expressway or Equivalent", "National Highway", "Prefectural Road"}
    ) | roads["Width Category"].isin(
        {"5.5 to Under 13 m", "13 to Under 19.5 m", "19.5 m or More"}
    )
    national_mask = roads["Road Category"].isin(
        {"National Expressway or Equivalent", "National Highway"}
    )
    available_major = roads.loc[available & major_mask]
    available_national = roads.loc[available & national_mask]
    unavailable = roads.loc[roads["Network Analysis Eligible"] & ~available]

    bounds = tuple(municipalities.total_bounds)
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    panel_specs = [
        (
            "Mean Access Time Increase (min)",
            "YlOrRd",
            Normalize(
                vmin=0,
                vmax=max(1.0, float(np.ceil(municipalities["Mean Access Time Increase (min)"].max()))),
            ),
            "Central: total-population weighted mean access-time increase (minutes)",
        ),
        (
            "Population Age 65+ Coverage Loss Rate (%)",
            "magma",
            Normalize(vmin=0, vmax=100),
            "Central: baseline-covered population age 65+ losing 30-minute access (%)",
        ),
    ]

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(15.2, 8.4), constrained_layout=True)
    grid = fig.add_gridspec(2, 2, height_ratios=(1.0, 0.045), hspace=0.035, wspace=0.055)
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(2)])
    colorbar_axes = [fig.add_subplot(grid[1, column]) for column in range(2)]

    for ax, colorbar_ax, (variable, cmap_name, norm, label) in zip(
        axes,
        colorbar_axes,
        panel_specs,
        strict=True,
    ):
        municipalities.plot(
            ax=ax,
            column=variable,
            cmap=cmap_name,
            norm=norm,
            linewidth=0.38,
            edgecolor="#555e63",
            missing_kwds={"color": "#c7c9cc", "edgecolor": "#555e63"},
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
        unavailable.plot(
            ax=ax,
            color="#0072b2",
            linewidth=0.28,
            alpha=0.92,
            rasterized=True,
            zorder=3.6,
        )
        municipalities.boundary.plot(
            ax=ax,
            color="#424a4f",
            linewidth=0.42,
            alpha=0.9,
            zorder=4,
        )
        style_map(ax, bounds, geographic_bounds)
        add_colorbar(fig, colorbar_ax, norm, cmap_name, label)

    axes[1].legend(
        handles=[
            Line2D([0], [0], color="#238b45", linewidth=1.4, label="Central-available major road"),
            Line2D([0], [0], color="#0072b2", linewidth=1.4, label="Central-unavailable road"),
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
    for label, ax in zip("ab", axes, strict=True):
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
    for variable in [
        "Mean Access Time Increase (min)",
        "Population Age 65+ Coverage Loss Rate (%)",
    ]:
        print(variable)
        print(
            municipalities.nlargest(5, variable)[["Municipality Label", variable]].to_string(
                index=False
            )
        )


if __name__ == "__main__":
    main()

