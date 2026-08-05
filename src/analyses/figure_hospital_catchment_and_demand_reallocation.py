#!/usr/bin/env python3
"""Hospital Catchment and Demand Reallocation.

Plan: Map Central-scenario hospital assignment changes, hospital catchment-demand
change, and other eligible hospitals within complete 30-minute two-stage access.
Framework: Section 6.4 confirmed primary specification and Section 7 Step 5.
"""

from __future__ import annotations

import math
import re
import unicodedata
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pyproj import Transformer
from shapely.geometry import LineString

from emergency_routing import compute_hospital_catchment_access, scenario_availability_mask


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "figures" / "Figure_hospital_catchment_and_demand_reallocation.png"
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
FIGURE_DPI = 300
PRIMARY_SCENARIO = "Central"
PRIMARY_THRESHOLD = 30
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

CATEGORY_ORDER = [
    "Retained assigned hospital",
    "Reassigned to another hospital",
    "Lost complete ambulance chain",
    "No baseline complete chain",
]
CATEGORY_COLORS = {
    "Retained assigned hospital": "#238b45",
    "Reassigned to another hospital": "#fdae61",
    "Lost complete ambulance chain": "#d73027",
    "No baseline complete chain": "#bdbdbd",
}
ROLE_MARKERS = {
    "Tertiary emergency hospital": "*",
    "Rotation hospital": "D",
    "Other eligible hospital": "o",
}
EXPLICIT_HOSPITAL_RENAMES = {
    "公立玉名中央病院": "くまもと県北病院",
    "荒尾市民病院": "荒尾市立有明医療センター",
}


class SignedLogTwoSlopeNorm(Normalize):
    """Map negative and positive signed-log values to separate color-map halves."""

    def __init__(
        self,
        vmin: float,
        vmax: float,
        linthresh: float = 100.0,
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


def normalize_hospital_name(value: object) -> str:
    """Normalize typography without deleting institutional name content."""
    normalized = unicodedata.normalize("NFKC", str(value))
    return re.sub(r"[\s・･,，.。()（）「」『』]+", "", normalized)


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
    """Apply a common extent and geographic frame to every map panel."""
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    padding_x = (maximum_x - minimum_x) * 0.018
    padding_y = (maximum_y - minimum_y) * 0.018
    ax.set_xlim(minimum_x - padding_x, maximum_x + padding_x)
    ax.set_ylim(minimum_y - padding_y, maximum_y + padding_y)
    ax.set_aspect("equal")
    add_graticule(ax, geographic_bounds)


def classify_assignment_change(baseline: pd.Series, central: pd.Series) -> pd.Series:
    """Apply the confirmed four-category assignment-change definition."""
    category = pd.Series("No baseline complete chain", index=baseline.index, dtype="string")
    baseline_complete = baseline.notna()
    central_complete = central.notna()
    category.loc[baseline_complete & ~central_complete] = "Lost complete ambulance chain"
    category.loc[baseline_complete & central_complete & baseline.ne(central)] = (
        "Reassigned to another hospital"
    )
    category.loc[baseline_complete & central_complete & baseline.eq(central)] = (
        "Retained assigned hospital"
    )
    return category


def hospital_metadata(hospitals: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Link network hospitals to audited role and 2026 bed records."""
    roles = pd.read_parquet(
        PROCESSED / "kumamoto_emergency_hospital_roles_2023_preprocessed.parquet",
        columns=[
            "Plan Hospital Name",
            "Hospital ID",
            "Matched Hospital Name",
            "Rotation Hospital",
            "Tertiary Emergency Hospital",
        ],
    )
    current = pd.read_parquet(
        PROCESSED / "kumamoto_hospitals_2026_preprocessed.parquet",
        columns=["Hospital ID", "Hospital Name", "Total Beds"],
    )
    candidates: dict[str, set[str]] = {}
    for row in roles.itertuples(index=False):
        hospital_id = str(row[1])
        for name in (row[0], row[2]):
            if pd.notna(name):
                candidates.setdefault(normalize_hospital_name(name), set()).add(hospital_id)
    current_name_to_id = {
        normalize_hospital_name(name): str(hospital_id)
        for hospital_id, name in current[["Hospital ID", "Hospital Name"]].itertuples(index=False)
        if pd.notna(name) and pd.notna(hospital_id)
    }

    linked_ids: list[str | pd.NA] = []
    methods: list[str] = []
    for facility_name in hospitals["Facility Name"]:
        normalized = normalize_hospital_name(facility_name)
        ids = set(candidates.get(normalized, set()))
        method = "normalized exact"
        if not ids:
            containing_ids: set[str] = set()
            for candidate_name, candidate_ids in candidates.items():
                if min(len(normalized), len(candidate_name)) >= 4 and (
                    candidate_name in normalized or normalized in candidate_name
                ):
                    containing_ids.update(candidate_ids)
            if len(containing_ids) == 1:
                ids = containing_ids
                method = "unique normalized containment"
        if not ids and str(facility_name) in EXPLICIT_HOSPITAL_RENAMES:
            renamed = normalize_hospital_name(EXPLICIT_HOSPITAL_RENAMES[str(facility_name)])
            hospital_id = current_name_to_id.get(renamed)
            if hospital_id is not None:
                ids = {hospital_id}
                method = "declared rename"
        if len(ids) == 1:
            linked_ids.append(next(iter(ids)))
            methods.append(method)
        else:
            linked_ids.append(pd.NA)
            methods.append("unmatched")

    enriched = hospitals.copy()
    enriched["Hospital ID"] = pd.Series(linked_ids, index=enriched.index, dtype="string")
    enriched["Hospital Link Method"] = methods
    role_unique = roles.drop_duplicates("Hospital ID")
    if role_unique["Hospital ID"].duplicated().any():
        raise RuntimeError("Hospital role records are not unique by Hospital ID")
    enriched = enriched.merge(
        role_unique[["Hospital ID", "Rotation Hospital", "Tertiary Emergency Hospital"]],
        on="Hospital ID",
        how="left",
        validate="many_to_one",
    ).merge(
        current[["Hospital ID", "Total Beds"]].drop_duplicates("Hospital ID"),
        on="Hospital ID",
        how="left",
        validate="many_to_one",
    )
    enriched["Hospital Role"] = "Other eligible hospital"
    enriched.loc[enriched["Rotation Hospital"].fillna(False), "Hospital Role"] = (
        "Rotation hospital"
    )
    enriched.loc[enriched["Tertiary Emergency Hospital"].fillna(False), "Hospital Role"] = (
        "Tertiary emergency hospital"
    )
    return gpd.GeoDataFrame(enriched, geometry="Geometry", crs=hospitals.crs)


def draw_central_roads(
    ax: plt.Axes,
    available_major: gpd.GeoDataFrame,
    available_national: gpd.GeoDataFrame,
    unavailable: gpd.GeoDataFrame,
) -> None:
    """Draw Central-available roads in green and unavailable roads in blue."""
    available_major.plot(
        ax=ax, color="#238b45", linewidth=0.22, alpha=0.80, rasterized=True, zorder=5
    )
    available_national.plot(
        ax=ax, color="white", linewidth=0.78, alpha=0.88, rasterized=True, zorder=5.2
    )
    available_national.plot(
        ax=ax, color="#005a32", linewidth=0.42, alpha=0.96, rasterized=True, zorder=5.3
    )
    unavailable.plot(
        ax=ax, color="#0072b2", linewidth=0.28, alpha=0.92, rasterized=True, zorder=5.6
    )


def add_horizontal_colorbar(
    fig: plt.Figure,
    ax: plt.Axes,
    norm: Normalize,
    cmap: str,
    label: str,
    ticks: list[float] | None = None,
) -> None:
    """Add a compact horizontal colorbar."""
    scalar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    scalar.set_array([])
    colorbar = fig.colorbar(scalar, cax=ax, orientation="horizontal", ticks=ticks)
    colorbar.set_label(label, fontsize=8.5)
    colorbar.ax.tick_params(labelsize=7.8, length=2)


def main() -> None:
    print("Computing Baseline hospital assignment...", flush=True)
    baseline_result = compute_hospital_catchment_access(
        PROCESSED,
        scenario="Baseline",
        threshold=PRIMARY_THRESHOLD,
        compute_alternatives=False,
    )
    print("Computing Central assignment and 30-minute hospital alternatives...", flush=True)
    central_result = compute_hospital_catchment_access(
        PROCESSED,
        scenario=PRIMARY_SCENARIO,
        threshold=PRIMARY_THRESHOLD,
        compute_alternatives=True,
    )
    baseline = baseline_result.demand
    central = central_result.demand

    demand = baseline[
        ["Mesh Code", "Total Population", "Assigned Hospital Node ID"]
    ].rename(columns={"Assigned Hospital Node ID": "Baseline Assigned Hospital"}).merge(
        central[
            ["Mesh Code", "Assigned Hospital Node ID", "Alternative Hospital Count"]
        ].rename(columns={"Assigned Hospital Node ID": "Central Assigned Hospital"}),
        on="Mesh Code",
        validate="one_to_one",
    )
    demand["Assignment Change"] = classify_assignment_change(
        demand["Baseline Assigned Hospital"], demand["Central Assigned Hospital"]
    )
    meshes = gpd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet",
        columns=["Mesh Code", "Geometry"],
    ).to_crs(MAP_CRS).merge(demand, on="Mesh Code", validate="one_to_one")

    baseline_catchment = baseline.groupby("Assigned Hospital Node ID", dropna=True)[
        "Total Population"
    ].sum()
    central_catchment = central.groupby("Assigned Hospital Node ID", dropna=True)[
        "Total Population"
    ].sum()
    hospitals = gpd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=[
            "Hospital Node ID",
            "Facility Name",
            "Eligible Emergency Hospital",
            "Geometry",
        ],
    ).to_crs(MAP_CRS)
    hospitals = hospital_metadata(hospitals)
    hospitals["Baseline Catchment Population"] = (
        hospitals["Hospital Node ID"].map(baseline_catchment).fillna(0)
    )
    hospitals["Central Catchment Population"] = (
        hospitals["Hospital Node ID"].map(central_catchment).fillna(0)
    )
    hospitals["Hospital Demand Change"] = (
        hospitals["Central Catchment Population"]
        - hospitals["Baseline Catchment Population"]
    )

    municipalities = gpd.read_parquet(
        PROCESSED / "kumamoto_administrative_areas_preprocessed.parquet",
        columns=["Municipality Code", "Geometry"],
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
    unavailable = roads.loc[roads["Network Analysis Eligible"].fillna(False) & ~available]

    bounds = tuple(municipalities.total_bounds)
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    demand_minimum = min(
        -1.0,
        float(np.floor(hospitals["Hospital Demand Change"].min() / 1_000.0) * 1_000.0),
    )
    demand_maximum = max(
        1.0,
        float(np.ceil(hospitals["Hospital Demand Change"].max() / 1_000.0) * 1_000.0),
    )
    demand_norm = SignedLogTwoSlopeNorm(
        vmin=demand_minimum,
        vmax=demand_maximum,
        linthresh=100.0,
    )
    alternative_maximum = max(1, int(meshes["Alternative Hospital Count"].max()))
    alternative_norm = Normalize(vmin=0, vmax=alternative_maximum)
    available_beds = hospitals["Total Beds"].dropna().astype(float)
    maximum_beds = max(1.0, float(available_beds.max()))
    hospitals["Marker Size"] = 22.0 + 145.0 * np.sqrt(
        hospitals["Total Beds"].astype(float) / maximum_beds
    )
    hospitals["Marker Size"] = hospitals["Marker Size"].fillna(18.0)

    sns.set_theme(context="paper", style="white", font_scale=1.0)
    fig = plt.figure(figsize=(20.0, 8.1), constrained_layout=True)
    grid = fig.add_gridspec(2, 3, height_ratios=(1.0, 0.045), hspace=0.035, wspace=0.055)
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    lower_axes = [fig.add_subplot(grid[1, column]) for column in range(3)]

    municipalities.plot(
        ax=axes[0], color="#f3f2ee", edgecolor="#62696d", linewidth=0.32, zorder=1
    )
    for category in CATEGORY_ORDER:
        meshes.loc[meshes["Assignment Change"].eq(category)].plot(
            ax=axes[0], color=CATEGORY_COLORS[category], linewidth=0, rasterized=True, zorder=3
        )
    draw_central_roads(axes[0], available_major, available_national, unavailable)
    municipalities.boundary.plot(ax=axes[0], color="#424a4f", linewidth=0.38, zorder=6)
    axes[0].legend(
        handles=[Patch(facecolor=CATEGORY_COLORS[item], label=item) for item in CATEGORY_ORDER],
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=7.5,
    )
    lower_axes[0].axis("off")

    municipalities.plot(
        ax=axes[1], color="#f3f2ee", edgecolor="#62696d", linewidth=0.32, zorder=1
    )
    draw_central_roads(axes[1], available_major, available_national, unavailable)
    for role, marker in ROLE_MARKERS.items():
        subset = hospitals.loc[hospitals["Hospital Role"].eq(role)]
        axes[1].scatter(
            subset.geometry.x,
            subset.geometry.y,
            c=subset["Hospital Demand Change"],
            s=subset["Marker Size"],
            marker=marker,
            cmap=DEMAND_CHANGE_CMAP,
            norm=demand_norm,
            edgecolors="white",
            linewidths=0.52,
            alpha=0.96,
            zorder=8,
        )
    role_legend = axes[1].legend(
        handles=[
            Line2D(
                [0], [0], marker=marker, linestyle="none", markerfacecolor="#7f8c8d",
                markeredgecolor="white", markeredgewidth=0.5, markersize=8, label=role
            )
            for role, marker in ROLE_MARKERS.items()
        ],
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=7.5,
    )
    axes[1].add_artist(role_legend)
    bed_examples = [(100, 4.8), (400, 7.2), (800, 9.8)]
    axes[1].legend(
        handles=[
            Line2D(
                [0], [0], marker="o", linestyle="none", markerfacecolor="none",
                markeredgecolor="#4c555a", markersize=marker_size,
                label=f"{value:,}"
            )
            for value, marker_size in bed_examples
            if value <= maximum_beds * 1.05
        ] + [
            Line2D(
                [0], [0], marker="o", linestyle="none", markerfacecolor="none",
                markeredgecolor="#4c555a", markersize=3.7, label="Total Beds unavailable"
            )
        ],
        title="Total Beds",
        loc="lower left",
        bbox_to_anchor=(0.015, 0.015),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=7.2,
        title_fontsize=7.5,
        borderpad=0.7,
        labelspacing=0.9,
        handlelength=1.5,
        handletextpad=0.7,
    )
    add_horizontal_colorbar(
        fig,
        lower_axes[1],
        demand_norm,
        DEMAND_CHANGE_CMAP,
        "Central minus baseline hospital catchment population (signed-log color scale)",
        ticks=sorted(
            {
                demand_minimum,
                demand_maximum,
                *[
                    value
                    for value in (-10_000.0, -1_000.0, -100.0, 0.0, 100.0, 1_000.0)
                    if demand_minimum <= value <= demand_maximum
                ],
            }
        ),
    )

    municipalities.plot(
        ax=axes[2], color="#f3f2ee", edgecolor="#62696d", linewidth=0.32, zorder=1
    )
    meshes.plot(
        ax=axes[2],
        column="Alternative Hospital Count",
        cmap="viridis",
        norm=alternative_norm,
        linewidth=0,
        rasterized=True,
        zorder=3,
    )
    draw_central_roads(axes[2], available_major, available_national, unavailable)
    municipalities.boundary.plot(ax=axes[2], color="#424a4f", linewidth=0.38, zorder=6)
    axes[2].legend(
        handles=[
            Line2D([0], [0], color="#238b45", linewidth=1.4, label="Central-available major road"),
            Line2D([0], [0], color="#0072b2", linewidth=1.4, label="Central-unavailable road"),
        ],
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=7.5,
    )
    alternative_ticks = sorted(
        set([0, alternative_maximum] + [int(round(alternative_maximum * value)) for value in (0.25, 0.5, 0.75)])
    )
    add_horizontal_colorbar(
        fig,
        lower_axes[2],
        alternative_norm,
        "viridis",
        "Other eligible hospitals within complete 30-minute Central access",
        ticks=alternative_ticks,
    )

    for label, ax in zip("abc", axes, strict=True):
        style_map(ax, bounds, geographic_bounds)
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
    print("Baseline diagnostics:", baseline_result.diagnostics, flush=True)
    print("Central diagnostics:", central_result.diagnostics, flush=True)
    print("Assignment-change population:", flush=True)
    print(
        demand.groupby("Assignment Change", dropna=False)["Total Population"]
        .sum()
        .reindex(CATEGORY_ORDER)
        .to_string(),
        flush=True,
    )
    print(
        f"Hospital metadata: {hospitals['Hospital ID'].notna().sum()}/75 linked; "
        f"{hospitals['Total Beds'].notna().sum()}/75 with Total Beds",
        flush=True,
    )
    print(
        hospitals.nlargest(5, "Hospital Demand Change")[
            ["Facility Name", "Hospital Demand Change"]
        ].to_string(index=False),
        flush=True,
    )
    print(
        hospitals.nsmallest(5, "Hospital Demand Change")[
            ["Facility Name", "Hospital Demand Change"]
        ].to_string(index=False),
        flush=True,
    )


if __name__ == "__main__":
    main()
