#!/usr/bin/env python3
"""Road-Hospital Shapley Value Matrix.

Plan: Map total corridor values and compare their hospital-specific decompositions.
Framework: Section 6.6 exact path and hospital decomposition and Section 7 Step 8.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.lines import Line2D
from matplotlib.ticker import LogFormatter, LogLocator

from emergency_routing import scenario_availability_mask
from figure_critical_medical_corridors import corridor_width, style_map
from medical_corridor_path_shapley import (
    PathShapleyResult,
    build_baseline_path_context,
    compute_path_shapley,
)


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = (
    ROOT
    / "data"
    / "results"
    / "figures"
    / "Figure_road_hospital_shapley_value_matrix.png"
)
FIGURE_DPI = 300
MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:6668"
PRIMARY_THRESHOLD = 30
SCENARIOS = ["Low", "Central", "High"]
ROAD_VALUE = "Path-Dependency Road Shapley Value"
ROAD_HOSPITAL_VALUE = "Path-Dependency Road-Hospital Shapley Value"
TOP_CORRIDORS = 20
TOP_HOSPITALS = 15
MISSING_TEXT = {"", "--", "-", "none", "nan", "<na>"}
JAPANESE_CHARACTER_PATTERN = re.compile(
    r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]"
)
HOSPITAL_ENGLISH_OVERRIDES = {
    "HOSPITAL-0000006": "Mimori Cardiovascular and Respiratory Hospital",
    "HOSPITAL-0000010": "Hori Hospital",
    "HOSPITAL-0000012": "Public Tamana Central Hospital",
    "HOSPITAL-0000018": "Minamata City General Medical Center",
    "HOSPITAL-0000025": "Amakusa Daiichi Hospital",
    "HOSPITAL-0000026": "Uki General Hospital",
    "HOSPITAL-0000031": "Yamaga City Medical Center",
    "HOSPITAL-0000032": "Okabe Hospital",
    "HOSPITAL-0000048": "Saiseikai Misumi Hospital",
    "HOSPITAL-0000052": "Kumamoto Chuo Hospital",
    "HOSPITAL-0000060": "JCHO Hitoyoshi Medical Center",
    "HOSPITAL-0000061": "Kumamoto Rosai Hospital",
    "HOSPITAL-0000063": "JCHO Amakusa Chuo General Hospital",
    "HOSPITAL-0000065": "Kuma District Public Taragi Hospital",
    "HOSPITAL-0000068": "Kikuchi Chuo Hospital",
}
ROUTE_ENGLISH_NAMES = {
    "九州自動車道": "Kyushu Expressway",
    "九州横断自動車道": "Kyushu Cross Expressway",
    "南九州西回り自動車道": "Minami-Kyushu Expressway",
}


def valid_text(value: object) -> str | None:
    """Normalize text and reject source missing-value placeholders."""
    if pd.isna(value):
        return None
    cleaned = str(value).strip()
    if cleaned.casefold() in MISSING_TEXT:
        return None
    return cleaned


def normalized_name(value: object) -> str:
    """Normalize Japanese facility names for deterministic record linkage."""
    cleaned = valid_text(value)
    if cleaned is None:
        return ""
    normalized = unicodedata.normalize("NFKC", cleaned).casefold()
    return re.sub(r"[\s・·.,，。、()（）\-]", "", normalized)


def english_route_name(value: object) -> str | None:
    """Translate only route-name forms with a reliable English rule."""
    cleaned = valid_text(value)
    if cleaned is None:
        return None
    if cleaned in ROUTE_ENGLISH_NAMES:
        return ROUTE_ENGLISH_NAMES[cleaned]
    national_route = re.fullmatch(r"国道\s*(\d+)\s*号", cleaned)
    if national_route:
        return f"National Route {national_route.group(1)}"
    port_road = re.fullmatch(r"(\d+)\s*号臨港道路", cleaned)
    if port_road:
        return f"Port Road No. {port_road.group(1)}"
    return None


def hospital_english_names(network_hospitals: pd.DataFrame) -> dict[str, str]:
    """Link network hospitals to the confirmed Romanized hospital-name field."""
    reference = pd.read_parquet(
        PROCESSED / "kumamoto_hospitals_2026_preprocessed.parquet",
        columns=["Hospital Name", "Hospital Name Romanized"],
    ).dropna(subset=["Hospital Name Romanized"])
    reference["_Normalized Name"] = reference["Hospital Name"].map(normalized_name)
    reference = reference.loc[reference["_Normalized Name"].ne("")].copy()
    exact = dict(
        zip(
            reference["_Normalized Name"],
            reference["Hospital Name Romanized"].astype(str).str.strip(),
            strict=True,
        )
    )
    reference_pairs = list(
        zip(
            reference["_Normalized Name"],
            reference["Hospital Name Romanized"].astype(str).str.strip(),
            strict=True,
        )
    )

    labels: dict[str, str] = {}
    for row in network_hospitals.itertuples(index=False):
        hospital_node_id = str(row[0])
        facility_name = row[1]
        if hospital_node_id in HOSPITAL_ENGLISH_OVERRIDES:
            labels[hospital_node_id] = HOSPITAL_ENGLISH_OVERRIDES[hospital_node_id]
            continue
        normalized_facility = normalized_name(facility_name)
        romanized = exact.get(normalized_facility)
        if romanized is None:
            candidates = [
                (len(reference_name), reference_romanized)
                for reference_name, reference_romanized in reference_pairs
                if len(reference_name) >= 5
                and (
                    reference_name in normalized_facility
                    or normalized_facility in reference_name
                )
            ]
            if candidates:
                romanized = sorted(candidates, key=lambda item: (-item[0], item[1]))[0][1]
        if romanized is None:
            romanized = f"Hospital {hospital_node_id.replace('HOSPITAL-', '')}"
        labels[hospital_node_id] = str(romanized)

    for hospital_node_id, label in labels.items():
        if JAPANESE_CHARACTER_PATTERN.search(label):
            raise RuntimeError(
                f"Japanese characters remain in hospital label {hospital_node_id}: {label}"
            )
    return labels


def first_nonmissing(values: pd.Series) -> str | None:
    """Return the first nonempty string in stable source order."""
    for value in values:
        cleaned = valid_text(value)
        if cleaned is not None:
            return cleaned
    return None


def modal_nonmissing(values: pd.Series) -> str | None:
    """Return a deterministic modal nonempty string."""
    cleaned = values.map(valid_text).dropna()
    if cleaned.empty:
        return None
    counts = cleaned.value_counts()
    return sorted(counts.loc[counts.eq(counts.max())].index)[0]


def corridor_labels(selected_corridors: list[str]) -> dict[str, str]:
    """Build concise route-first labels for selected medical corridors."""
    edges = pd.read_parquet(
        PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=[
            "Medical Corridor ID",
            "Route Name",
            "Emergency Route Membership",
            "Road Category",
        ],
    )
    edges = edges.loc[edges["Medical Corridor ID"].isin(selected_corridors)]
    attributes = (
        edges.groupby("Medical Corridor ID", sort=False)
        .agg(
            {
                "Route Name": first_nonmissing,
                "Emergency Route Membership": first_nonmissing,
                "Road Category": modal_nonmissing,
            }
        )
        .reset_index()
    )

    labels: dict[str, str] = {}
    for row in attributes.itertuples(index=False):
        corridor_id = str(row[0])
        route_name = valid_text(row[1])
        emergency_membership = valid_text(row[2])
        road_category = valid_text(row[3])
        descriptor = None
        translated_route = english_route_name(route_name)
        if translated_route is not None:
            descriptor = translated_route
        elif emergency_membership is not None:
            descriptor = str(emergency_membership)
        elif road_category is not None:
            descriptor = str(road_category).replace(" or Equivalent", "")
        else:
            descriptor = "Road corridor"
        labels[corridor_id] = f"{descriptor} · {corridor_id.replace('CORR-', '')}"
    for corridor_id, label in labels.items():
        if JAPANESE_CHARACTER_PATTERN.search(label):
            raise RuntimeError(
                f"Japanese characters remain in corridor label {corridor_id}: {label}"
            )
    return labels


def validate_hospital_decomposition(result: PathShapleyResult) -> None:
    """Verify that the complete hospital matrix sums to each corridor road value."""
    hospital_totals = (
        result.hospital_values.groupby("Medical Corridor ID", sort=False)[
            ROAD_HOSPITAL_VALUE
        ]
        .sum()
        .reindex(result.values["Medical Corridor ID"], fill_value=0.0)
        .to_numpy(dtype=float)
    )
    road_totals = result.values[ROAD_VALUE].to_numpy(dtype=float)
    if not np.allclose(hospital_totals, road_totals, rtol=0, atol=1e-5):
        raise RuntimeError(f"{result.scenario} hospital decomposition does not add up")


def select_display_sets(
    results: list[PathShapleyResult],
) -> tuple[list[str], list[str], pd.DataFrame]:
    """Select stable rows and columns without changing the complete calculations."""
    road_values = pd.concat([result.values for result in results], ignore_index=True)
    corridor_scores = (
        road_values.groupby("Medical Corridor ID", sort=False)[ROAD_VALUE]
        .max()
        .rename("Maximum Scenario Road Value")
        .reset_index()
        .sort_values(
            ["Maximum Scenario Road Value", "Medical Corridor ID"],
            ascending=[False, True],
            kind="stable",
        )
    )
    selected_corridors = corridor_scores.head(TOP_CORRIDORS)[
        "Medical Corridor ID"
    ].astype(str).tolist()

    hospital_values = pd.concat(
        [result.hospital_values for result in results], ignore_index=True
    )
    selected_values = hospital_values.loc[
        hospital_values["Medical Corridor ID"].isin(selected_corridors)
    ].copy()
    hospital_scores = (
        selected_values.groupby("Hospital Node ID", sort=False)[ROAD_HOSPITAL_VALUE]
        .sum()
        .rename("Selected-Corridor Association")
        .reset_index()
        .sort_values(
            ["Selected-Corridor Association", "Hospital Node ID"],
            ascending=[False, True],
            kind="stable",
        )
    )
    selected_hospitals = hospital_scores.head(TOP_HOSPITALS)["Hospital Node ID"].astype(
        str
    ).tolist()
    return selected_corridors, selected_hospitals, selected_values


def build_matrix(
    result: PathShapleyResult,
    selected_corridors: list[str],
    selected_hospitals: list[str],
) -> pd.DataFrame:
    """Return one scenario matrix with shared row and column ordering."""
    return (
        result.hospital_values.pivot_table(
            index="Medical Corridor ID",
            columns="Hospital Node ID",
            values=ROAD_HOSPITAL_VALUE,
            aggfunc="sum",
            fill_value=0.0,
        )
        .reindex(index=selected_corridors, columns=selected_hospitals, fill_value=0.0)
        .astype(float)
    )


def main() -> None:
    print("Building the shared baseline two-stage path context...", flush=True)
    context = build_baseline_path_context(PROCESSED)
    results: list[PathShapleyResult] = []
    for scenario in SCENARIOS:
        print(f"Computing {scenario} road-hospital path values...", flush=True)
        result = compute_path_shapley(
            PROCESSED,
            context,
            scenario=scenario,
            threshold=PRIMARY_THRESHOLD,
        )
        validate_hospital_decomposition(result)
        results.append(result)
        print(
            f"{scenario}: {len(result.values):,} positive corridors; "
            f"{len(result.hospital_values):,} positive corridor-hospital pairs; "
            f"decomposition total {result.diagnostics['shapley_total']:,.0f}",
            flush=True,
        )

    selected_corridors, selected_hospitals, _ = select_display_sets(results)
    matrices = [
        build_matrix(result, selected_corridors, selected_hospitals)
        for result in results
    ]
    selected_positive = np.concatenate(
        [matrix.to_numpy(dtype=float).ravel() for matrix in matrices]
    )
    selected_positive = selected_positive[selected_positive > 0]
    if selected_positive.size == 0:
        raise RuntimeError("No positive Road-Hospital Shapley values in the display set")

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
    selected_geometry = roads.loc[
        roads["Medical Corridor ID"].isin(selected_corridors),
        ["Medical Corridor ID", "Geometry"],
    ].dissolve(by="Medical Corridor ID", as_index=False)
    if len(selected_geometry) != len(selected_corridors):
        raise RuntimeError(
            "Not every displayed Medical Corridor ID has map geometry: "
            f"{len(selected_geometry)} of {len(selected_corridors)}"
        )
    selected_map_positive = np.concatenate(
        [
            result.values.loc[
                result.values["Medical Corridor ID"].isin(selected_corridors), ROAD_VALUE
            ].to_numpy(dtype=float)
            for result in results
        ]
    )
    selected_map_positive = selected_map_positive[selected_map_positive > 0]
    if selected_map_positive.size == 0:
        raise RuntimeError("No positive total Road Shapley values in the display set")
    map_minimum = float(selected_map_positive.min())
    map_maximum = float(selected_map_positive.max())
    map_norm = LogNorm(vmin=map_minimum, vmax=map_maximum)
    map_panels = []
    for result in results:
        available = scenario_availability_mask(roads, result.scenario)
        available_all = roads.loc[available]
        available_major = roads.loc[available & major_mask]
        unavailable = roads.loc[
            roads["Network Analysis Eligible"].fillna(False) & ~available
        ]
        selected = selected_geometry.merge(
            result.values[["Medical Corridor ID", ROAD_VALUE]],
            on="Medical Corridor ID",
            how="left",
            validate="one_to_one",
        )
        selected[ROAD_VALUE] = selected[ROAD_VALUE].fillna(0.0)
        positive_selected = selected.loc[selected[ROAD_VALUE].gt(0)].copy()
        zero_selected = selected.loc[selected[ROAD_VALUE].le(0)].copy()
        if len(positive_selected):
            positive_selected["Line Width"] = corridor_width(
                positive_selected[ROAD_VALUE].to_numpy(dtype=float),
                map_minimum,
                map_maximum,
            )
        map_panels.append(
            (
                result,
                available_all,
                available_major,
                unavailable,
                positive_selected,
                zero_selected,
            )
        )

    hospitals = gpd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=[
            "Hospital Node ID",
            "Facility Name",
            "Eligible Emergency Hospital",
            "Geometry",
        ],
    ).to_crs(MAP_CRS)
    eligible_hospital_count = int(hospitals["Eligible Emergency Hospital"].fillna(False).sum())
    hospital_names = hospital_english_names(
        hospitals[["Hospital Node ID", "Facility Name"]]
    )
    missing_names = [identifier for identifier in selected_hospitals if identifier not in hospital_names]
    if missing_names:
        raise RuntimeError(f"Missing names for selected hospitals: {missing_names}")
    corridor_names = corridor_labels(selected_corridors)
    displayed_hospitals = hospitals.loc[
        hospitals["Hospital Node ID"].astype(str).isin(selected_hospitals)
    ]

    sns.set_theme(context="paper", style="white", font_scale=0.95)
    mpl.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
    heat_color_map = LinearSegmentedColormap.from_list(
        "blue_green_yellow_red",
        ["#2166ac", "#1a9850", "#fee08b", "#d73027"],
        N=256,
    )
    heat_color_map.set_bad("white")
    heat_norm = LogNorm(
        vmin=float(selected_positive.min()),
        vmax=float(selected_positive.max()),
    )

    bounds = tuple(municipalities.total_bounds)
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    fig = plt.figure(figsize=(24.0, 17.2), constrained_layout=True)
    grid = fig.add_gridspec(
        4,
        3,
        height_ratios=[0.82, 0.038, 1.0, 0.042],
        hspace=0.055,
        wspace=0.10,
    )
    map_axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    map_colorbar_ax = fig.add_subplot(grid[1, :])
    heat_axes = np.array([fig.add_subplot(grid[2, column]) for column in range(3)])
    heat_colorbar_ax = fig.add_subplot(grid[3, :])

    for panel_label, ax, panel in zip(
        "abc", map_axes, map_panels, strict=True
    ):
        (
            result,
            available_all,
            available_major,
            unavailable,
            positive_selected,
            zero_selected,
        ) = panel
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
        if len(zero_selected):
            zero_selected.plot(
                ax=ax,
                color="white",
                linewidth=1.55,
                alpha=0.96,
                zorder=5.8,
            )
            zero_selected.plot(
                ax=ax,
                color="#4d4d4d",
                linewidth=0.82,
                linestyle=(0, (3.0, 2.0)),
                alpha=0.96,
                zorder=6,
            )
        if len(positive_selected):
            positive_selected.plot(
                ax=ax,
                color="white",
                linewidth=positive_selected["Line Width"] + 0.95,
                alpha=0.98,
                zorder=6.5,
            )
            positive_selected.plot(
                ax=ax,
                column=ROAD_VALUE,
                cmap="YlOrRd",
                norm=map_norm,
                linewidth=positive_selected["Line Width"],
                alpha=0.99,
                zorder=7,
            )
        displayed_hospitals.plot(
            ax=ax,
            marker="^",
            color="#762a83",
            edgecolor="white",
            linewidth=0.38,
            markersize=15,
            alpha=0.98,
            zorder=8,
        )
        municipalities.boundary.plot(
            ax=ax,
            color="#424a4f",
            linewidth=0.38,
            alpha=0.90,
            zorder=9,
        )
        style_map(ax, bounds, geographic_bounds)
        ax.set_xlabel(
            f"{result.scenario} scenario — total corridor value across all hospitals",
            fontsize=9.0,
            labelpad=14,
        )
        ax.text(
            -0.04,
            1.02,
            panel_label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
            clip_on=False,
        )

    map_axes[0].legend(
        handles=[
            Line2D(
                [0], [0], color="#a6dba0", linewidth=1.2,
                label="Assumed available road"
            ),
            Line2D(
                [0], [0], color="#1b7837", linewidth=1.5,
                label="Assumed available major road"
            ),
            Line2D(
                [0], [0], color="#0072b2", linewidth=1.4,
                label="Assumed unavailable road"
            ),
            Line2D(
                [0], [0], color="#4d4d4d", linewidth=1.2,
                linestyle=(0, (3.0, 2.0)), label="Displayed corridor with zero value"
            ),
            Line2D(
                [0], [0], color="#d7301f", linewidth=2.6,
                label="Displayed corridor with positive value"
            ),
            Line2D(
                [0], [0], marker="^", color="none", markerfacecolor="#762a83",
                markeredgecolor="white", markersize=6, label="Displayed hospital"
            ),
        ],
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        borderaxespad=0.0,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="#bdbdbd",
        fontsize=6.7,
    )

    map_scalar = mpl.cm.ScalarMappable(norm=map_norm, cmap="YlOrRd")
    map_colorbar = fig.colorbar(
        map_scalar,
        cax=map_colorbar_ax,
        orientation="horizontal",
        extend="neither",
    )
    map_colorbar.locator = LogLocator(base=10, subs=(1.0, 2.0, 5.0))
    map_colorbar.formatter = LogFormatter(base=10, labelOnlyBase=False)
    map_colorbar.update_ticks()
    map_colorbar.ax.tick_params(labelsize=7.2, length=2.5)
    map_colorbar.set_label(
        "Path-dependency Road Shapley Value "
        "(people across all 75 eligible hospitals; logarithmic positive-value scale)",
        fontsize=9.1,
    )

    row_labels = [corridor_names[corridor] for corridor in selected_corridors]
    column_labels = [hospital_names[hospital] for hospital in selected_hospitals]
    for panel_label, scenario, matrix, ax in zip(
        "def", SCENARIOS, matrices, heat_axes, strict=True
    ):
        masked = np.ma.masked_equal(matrix.to_numpy(dtype=float), 0.0)
        ax.imshow(
            masked,
            cmap=heat_color_map,
            norm=heat_norm,
            interpolation="nearest",
            aspect="auto",
        )
        ax.set_xticks(np.arange(len(column_labels)))
        ax.set_xticklabels(column_labels, rotation=63, ha="right", fontsize=6.2)
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_yticklabels(row_labels, fontsize=6.6)
        ax.set_xlabel(
            f"{scenario} scenario — baseline Assigned Hospital",
            fontsize=9.2,
            labelpad=8,
        )
        ax.set_ylabel("Medical corridor", fontsize=9.2)
        ax.set_xticks(np.arange(-0.5, len(column_labels), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
        ax.grid(which="minor", color="#d4d9dc", linestyle="-", linewidth=0.38)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.tick_params(which="major", length=0)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#424a4f")
            spine.set_linewidth(0.75)
        ax.text(
            -0.075,
            1.025,
            panel_label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
            clip_on=False,
        )

    heat_scalar = mpl.cm.ScalarMappable(norm=heat_norm, cmap=heat_color_map)
    heat_colorbar = fig.colorbar(
        heat_scalar,
        cax=heat_colorbar_ax,
        orientation="horizontal",
        extend="neither",
    )
    heat_colorbar.locator = LogLocator(base=10, subs=(1.0, 2.0, 5.0))
    heat_colorbar.formatter = LogFormatter(base=10, labelOnlyBase=False)
    heat_colorbar.update_ticks()
    heat_colorbar.ax.tick_params(labelsize=7.2, length=2.5)
    heat_colorbar.set_label(
        "Path-dependency Road-Hospital Shapley Value "
        "(people; logarithmic positive-value scale; white = 0)",
        fontsize=9.2,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Eligible hospitals computed: {eligible_hospital_count:,}")
    print(f"Displayed corridors: {len(selected_corridors):,}")
    print(f"Displayed hospitals: {len(selected_hospitals):,}")
    print("Selected corridor IDs: " + ", ".join(selected_corridors))
    print("Selected hospital IDs: " + ", ".join(selected_hospitals))
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
