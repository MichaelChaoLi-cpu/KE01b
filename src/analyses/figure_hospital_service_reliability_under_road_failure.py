#!/usr/bin/env python3
"""Hospital Service Reliability under Road Failure.

Plan: Map changes in eligible-hospital catchment population and service
reliability under the 1%, 3%, and 5% main road-failure scenarios.
Framework: AnaSOP Sections 5.2, 6.4, and Analytical Workflow step 6.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, Normalize
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
    / "Figure_hospital_service_reliability_under_road_failure.png"
)
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
LEVELS = (0.01, 0.03, 0.05)
MAJOR_CATEGORIES = {
    "National Expressway or Equivalent",
    "National Highway",
    "Prefectural Road",
}
DEMAND_CHANGE_CMAP = LinearSegmentedColormap.from_list(
    "BlueGreenWhiteYellowRed",
    [
        (0.00, "#2166ac"),
        (0.32, "#1a9850"),
        (0.50, "#ffffff"),
        (0.68, "#fee08b"),
        (1.00, "#d73027"),
    ],
)


class SignedLogTwoSlopeNorm(Normalize):
    """Place zero at the color-map midpoint and log-compress both tails."""

    def __init__(
        self,
        vmin: float,
        vmax: float,
        linthresh: float = 50.0,
        clip: bool = False,
    ) -> None:
        if not vmin < 0 < vmax:
            raise ValueError("Signed-log bounds must straddle zero")
        if linthresh <= 0:
            raise ValueError("linthresh must be positive")
        super().__init__(vmin=vmin, vmax=vmax, clip=clip)
        self.linthresh = float(linthresh)
        self.negative_scale = float(np.log1p(abs(vmin) / self.linthresh))
        self.positive_scale = float(np.log1p(vmax / self.linthresh))

    def __call__(self, value: object, clip: bool | None = None) -> object:
        result, is_scalar = self.process_value(value)
        data = result.data.astype(float)
        if clip if clip is not None else self.clip:
            data = np.clip(data, self.vmin, self.vmax)
        mapped = np.full(data.shape, 0.5, dtype=float)
        negative = data < 0
        positive = data > 0
        mapped[negative] = 0.5 - 0.5 * (
            np.log1p(-data[negative] / self.linthresh) / self.negative_scale
        )
        mapped[positive] = 0.5 + 0.5 * (
            np.log1p(data[positive] / self.linthresh) / self.positive_scale
        )
        output = np.ma.array(mapped, mask=np.ma.getmaskarray(result), copy=False)
        return output[0] if is_scalar else output

    def inverse(self, value: object) -> object:
        values = np.ma.asarray(value)
        data = values.data.astype(float)
        restored = np.zeros(data.shape, dtype=float)
        negative = data < 0.5
        positive = data > 0.5
        restored[negative] = -self.linthresh * np.expm1(
            2.0 * (0.5 - data[negative]) * self.negative_scale
        )
        restored[positive] = self.linthresh * np.expm1(
            2.0 * (data[positive] - 0.5) * self.positive_scale
        )
        output = np.ma.array(restored, mask=np.ma.getmaskarray(values), copy=False)
        return output.item() if np.isscalar(value) else output


def graticule_values(lower: float, upper: float, step: float) -> list[float]:
    """Return stable longitude or latitude values within the map extent."""
    start = math.ceil((lower - 1e-9) / step) * step
    stop = math.floor((upper + 1e-9) / step) * step
    count = int(round((stop - start) / step)) + 1
    return [round(start + index * step, 8) for index in range(max(0, count))]


def add_graticule(
    axis: plt.Axes,
    geographic_bounds: tuple[float, float, float, float],
    step: float = 0.25,
) -> None:
    """Draw and label longitude/latitude graticules on a projected map."""
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
        spine.set_zorder(20)


def style_map(
    axis: plt.Axes,
    bounds: tuple[float, float, float, float],
    geographic_bounds: tuple[float, float, float, float],
) -> None:
    """Apply a common extent, aspect, graticule, and frame."""
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    axis.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    axis.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    axis.set_aspect("equal")
    add_graticule(axis, geographic_bounds)


def marker_size(catchment_population: pd.Series, maximum: float) -> np.ndarray:
    """Scale marker area by the square root of mean catchment population."""
    values = catchment_population.to_numpy(dtype=float)
    return 17.0 + 145.0 * np.sqrt(np.clip(values, 0.0, None) / maximum)


def edge_width(zero_frequency: pd.Series) -> np.ndarray:
    """Encode zero-catchment frequency as a visible marker-border width."""
    values = zero_frequency.to_numpy(dtype=float)
    return 0.35 + 30.0 * np.clip(values, 0.0, None)


def main() -> None:
    service = pd.read_parquet(
        EXPERIMENT / "hospital_service_reliability.parquet"
    )
    hospitals = gpd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=[
            "Hospital Node ID",
            "Eligible Emergency Hospital",
            "Geometry",
        ],
    )
    boundary = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Geometry"],
    ).to_crs(MAP_CRS)
    roads = gpd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=["Road Category", "Geometry"],
    ).to_crs(MAP_CRS)
    major_roads = roads.loc[roads["Road Category"].isin(MAJOR_CATEGORIES)]

    service = service.loc[
        service["Expected Failed Road Length Share"].isin(LEVELS)
    ].copy()
    if service["Simulation Replicates"].nunique() != 1 or int(
        service["Simulation Replicates"].iloc[0]
    ) != 1000:
        raise RuntimeError("Hospital results do not contain the formal 1,000 replicates")
    expected_rows = len(LEVELS) * len(hospitals)
    if len(service) != expected_rows:
        raise RuntimeError(
            f"Expected {expected_rows} hospital-scenario rows; found {len(service)}"
        )
    hospitals["Hospital Node ID"] = hospitals["Hospital Node ID"].astype(str)
    service["Hospital Node ID"] = service["Hospital Node ID"].astype(str)

    mapped = hospitals.merge(
        service,
        on="Hospital Node ID",
        how="inner",
        validate="one_to_many",
    )
    mapped = gpd.GeoDataFrame(mapped, geometry="Geometry", crs=hospitals.crs).to_crs(
        MAP_CRS
    )
    if len(mapped) != expected_rows:
        raise RuntimeError("Hospital geometry join is incomplete")

    mapped["Hospital Role"] = np.where(
        mapped["Disaster Base Designation"].ne("Not Designated"),
        "Disaster-base hospital",
        "Other eligible emergency hospital",
    )
    role_markers = {
        "Disaster-base hospital": "*",
        "Other eligible emergency hospital": "o",
    }
    maximum_catchment = float(mapped["Mean Hospital Catchment Population"].max())
    minimum_change = float(mapped["Hospital Demand Change"].min())
    maximum_change = float(mapped["Hospital Demand Change"].max())
    rounded_negative = min(-100.0, math.floor(minimum_change / 500.0) * 500.0)
    rounded_positive = max(100.0, math.ceil(maximum_change / 500.0) * 500.0)
    change_norm = SignedLogTwoSlopeNorm(
        vmin=rounded_negative,
        vmax=rounded_positive,
        linthresh=50.0,
    )

    bounds = tuple(boundary.total_bounds)
    geographic_bounds = tuple(boundary.to_crs(GEOGRAPHIC_CRS).total_bounds)
    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(17.2, 8.0), constrained_layout=True)
    grid = fig.add_gridspec(
        3,
        3,
        height_ratios=(1.0, 0.045, 0.115),
        hspace=0.045,
        wspace=0.055,
    )
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    colorbar_axis = fig.add_subplot(grid[1, :])
    legend_axis = fig.add_subplot(grid[2, :])
    diagnostics: list[dict[str, float | int]] = []

    for axis, level in zip(axes, LEVELS, strict=True):
        values = mapped.loc[
            mapped["Expected Failed Road Length Share"].eq(level)
        ].copy()
        if len(values) != len(hospitals):
            raise RuntimeError(f"Unexpected hospital count for severity {level}")

        boundary.plot(ax=axis, color="#f1f2f2", edgecolor="none", zorder=0)
        roads.plot(
            ax=axis,
            color="#6f777c",
            linewidth=0.075,
            alpha=0.25,
            rasterized=True,
            zorder=1.0,
        )
        major_roads.plot(
            ax=axis,
            color="#343a3e",
            linewidth=0.20,
            alpha=0.52,
            rasterized=True,
            zorder=1.2,
        )
        boundary.boundary.plot(
            ax=axis,
            color="#40484d",
            linewidth=0.32,
            alpha=0.88,
            zorder=3,
        )
        for role, marker in role_markers.items():
            subset = values.loc[values["Hospital Role"].eq(role)]
            axis.scatter(
                subset.geometry.x,
                subset.geometry.y,
                c=subset["Hospital Demand Change"],
                s=marker_size(
                    subset["Mean Hospital Catchment Population"],
                    maximum_catchment,
                ),
                marker=marker,
                cmap=DEMAND_CHANGE_CMAP,
                norm=change_norm,
                edgecolors="#20282d",
                linewidths=edge_width(subset["Zero Catchment Frequency"]),
                alpha=0.96,
                zorder=6,
            )

        total_change = float(values["Hospital Demand Change"].sum())
        high_zero_frequency = int((values["Zero Catchment Frequency"] >= 0.01).sum())
        diagnostics.append(
            {
                "expected_failed_length_percent": int(round(100 * level)),
                "mean_unassigned_population": max(0.0, -total_change),
                "hospitals_zero_catchment_frequency_ge_1pct": high_zero_frequency,
            }
        )
        axis.text(
            0.975,
            0.975,
            (
                f"Expected failed length: {100 * level:g}%\n"
                f"Mean unassigned population: {max(0.0, -total_change):,.0f}\n"
                f"Hospitals with zero catchment in ≥1% of runs: "
                f"{high_zero_frequency}"
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
            zorder=9,
        )
        style_map(axis, bounds, geographic_bounds)

    scalar = plt.cm.ScalarMappable(norm=change_norm, cmap=DEMAND_CHANGE_CMAP)
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=colorbar_axis, orientation="horizontal")
    tick_candidates = [
        rounded_negative,
        -2_000.0,
        -1_000.0,
        -500.0,
        -100.0,
        0.0,
        100.0,
        500.0,
        1_000.0,
        rounded_positive,
    ]
    ticks = sorted(
        {
            value
            for value in tick_candidates
            if rounded_negative <= value <= rounded_positive
        }
    )
    colorbar.set_ticks(ticks)
    colorbar.set_ticklabels([f"{value:+,.0f}" if value else "0" for value in ticks])
    colorbar.set_label(
        "Mean hospital catchment change from baseline (people; signed-log color scale)",
        fontsize=9,
    )
    colorbar.ax.tick_params(labelsize=8, length=2)

    legend_axis.axis("off")
    role_legend = legend_axis.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker=marker,
                linestyle="none",
                markerfacecolor="#8f9aa1",
                markeredgecolor="#20282d",
                markeredgewidth=0.7,
                markersize=8.5,
                label=role,
            )
            for role, marker in role_markers.items()
        ],
        title="Eligible hospital role",
        loc="center",
        bbox_to_anchor=(0.17, 0.5),
        frameon=False,
        fontsize=8,
        title_fontsize=8.4,
    )
    legend_axis.add_artist(role_legend)

    catchment_examples = [5_000.0, 25_000.0, 75_000.0]
    size_legend = legend_axis.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor="#8f9aa1",
                markeredgecolor="#20282d",
                markeredgewidth=0.7,
                markersize=float(
                    np.sqrt(marker_size(pd.Series([value]), maximum_catchment)[0])
                ),
                label=f"{value:,.0f}",
            )
            for value in catchment_examples
        ],
        title="Mean catchment population",
        loc="center",
        bbox_to_anchor=(0.50, 0.5),
        ncol=3,
        frameon=False,
        fontsize=8,
        title_fontsize=8.4,
        handletextpad=0.5,
        columnspacing=1.5,
    )
    legend_axis.add_artist(size_legend)

    frequency_examples = [0.0, 0.03, 0.06]
    frequency_legend = legend_axis.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="none",
                markerfacecolor="white",
                markeredgecolor="#20282d",
                markeredgewidth=float(edge_width(pd.Series([value]))[0]),
                markersize=8.5,
                label=f"{100 * value:.0f}%",
            )
            for value in frequency_examples
        ],
        title="Zero-catchment frequency",
        loc="center",
        bbox_to_anchor=(0.83, 0.5),
        ncol=3,
        frameon=False,
        fontsize=8,
        title_fontsize=8.4,
        handletextpad=0.5,
        columnspacing=1.5,
    )
    legend_axis.add_artist(frequency_legend)

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

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    print(pd.DataFrame(diagnostics).to_string(index=False))


if __name__ == "__main__":
    main()
