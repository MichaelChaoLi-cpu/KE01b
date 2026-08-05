#!/usr/bin/env python3
"""Road-Hospital Shapley Value Matrix.

Plan: Compare hospital-specific corridor path-dependency values across disruption scenarios.
Framework: Section 6.6 exact baseline-Assigned-Hospital decomposition and Section 7 Step 8.
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
from matplotlib.ticker import LogFormatter, LogLocator

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
    edges = gpd.read_parquet(
        PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=[
            "Medical Corridor ID",
            "Emergency Route Membership",
            "Road Category",
            "Geometry",
        ],
    )
    edges = edges.loc[edges["Medical Corridor ID"].isin(selected_corridors)].to_crs(
        MAP_CRS
    )
    attributes = (
        edges.groupby("Medical Corridor ID", sort=False)
        .agg(
            {
                "Emergency Route Membership": first_nonmissing,
                "Road Category": modal_nonmissing,
            }
        )
        .reset_index()
    )
    dissolved = edges[["Medical Corridor ID", "Geometry"]].dissolve(
        by="Medical Corridor ID", as_index=False
    )

    routes = gpd.read_parquet(
        PROCESSED / "kumamoto_emergency_transport_roads_2024_preprocessed.parquet",
        columns=["Route Name", "Geometry"],
    ).to_crs(MAP_CRS)
    routes["Route Name"] = routes["Route Name"].map(valid_text)
    routes = routes.loc[routes["Route Name"].notna()].copy()
    nearest = gpd.sjoin_nearest(
        dissolved,
        routes,
        how="left",
        max_distance=40.0,
        distance_col="_Route Distance",
    )
    nearest = (
        nearest.sort_values(
            ["Medical Corridor ID", "_Route Distance", "Route Name"],
            na_position="last",
            kind="stable",
        )
        .drop_duplicates("Medical Corridor ID", keep="first")
        [["Medical Corridor ID", "Route Name"]]
    )
    attributes = attributes.merge(
        nearest, on="Medical Corridor ID", how="left", validate="one_to_one"
    )

    labels: dict[str, str] = {}
    for row in attributes.itertuples(index=False):
        corridor_id = str(row[0])
        emergency_membership = row[1]
        road_category = row[2]
        route_name = row[3]
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

    hospitals = pd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=["Hospital Node ID", "Facility Name", "Eligible Emergency Hospital"],
    )
    eligible_hospital_count = int(hospitals["Eligible Emergency Hospital"].fillna(False).sum())
    hospital_names = hospital_english_names(
        hospitals[["Hospital Node ID", "Facility Name"]]
    )
    missing_names = [identifier for identifier in selected_hospitals if identifier not in hospital_names]
    if missing_names:
        raise RuntimeError(f"Missing names for selected hospitals: {missing_names}")
    corridor_names = corridor_labels(selected_corridors)

    sns.set_theme(context="paper", style="white", font_scale=0.95)
    mpl.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
    color_map = LinearSegmentedColormap.from_list(
        "blue_green_yellow_red",
        ["#2166ac", "#1a9850", "#fee08b", "#d73027"],
        N=256,
    )
    color_map.set_bad("white")
    color_norm = LogNorm(
        vmin=float(selected_positive.min()),
        vmax=float(selected_positive.max()),
    )

    fig = plt.figure(figsize=(24.0, 10.4), constrained_layout=True)
    grid = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.045], hspace=0.03, wspace=0.10)
    axes = np.array([fig.add_subplot(grid[0, column]) for column in range(3)])
    colorbar_ax = fig.add_subplot(grid[1, :])

    row_labels = [corridor_names[corridor] for corridor in selected_corridors]
    column_labels = [hospital_names[hospital] for hospital in selected_hospitals]
    for panel_label, scenario, matrix, ax in zip(
        "abc", SCENARIOS, matrices, axes, strict=True
    ):
        masked = np.ma.masked_equal(matrix.to_numpy(dtype=float), 0.0)
        ax.imshow(
            masked,
            cmap=color_map,
            norm=color_norm,
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

    scalar_mappable = mpl.cm.ScalarMappable(norm=color_norm, cmap=color_map)
    colorbar = fig.colorbar(
        scalar_mappable,
        cax=colorbar_ax,
        orientation="horizontal",
        extend="neither",
    )
    colorbar.locator = LogLocator(base=10, subs=(1.0, 2.0, 5.0))
    colorbar.formatter = LogFormatter(base=10, labelOnlyBase=False)
    colorbar.update_ticks()
    colorbar.ax.tick_params(labelsize=7.2, length=2.5)
    colorbar.set_label(
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
