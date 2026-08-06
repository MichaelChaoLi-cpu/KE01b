#!/usr/bin/env python3
"""Validate and audit road-section accessibility-consequence estimates."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import geopandas as gpd
import numpy as np
import pandas as pd

from monte_carlo_emergency_routing import build_compact_emergency_network


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
EXPERIMENT = ROOT / "data" / "exp" / "road_section_accessibility_consequence"
RESULT_PATH = EXPERIMENT / "road_section_accessibility_consequence.parquet"
THRESHOLDS = (15, 30, 45)
SEVERITIES = (1, 3, 5)


def connector_counts(edge_to_section: pd.Series) -> pd.DataFrame:
    sources = {
        "Population Connector Count": (
            "kumamoto_population_mesh_network_access_preprocessed.parquet",
            None,
        ),
        "Dispatch Connector Count": (
            "kumamoto_dispatch_base_network_access_preprocessed.parquet",
            "Candidate Dispatch Base",
        ),
        "Hospital Connector Count": (
            "kumamoto_hospital_network_access_preprocessed.parquet",
            "Eligible Emergency Hospital",
        ),
    }
    frames: list[pd.DataFrame] = []
    for output_column, (filename, eligibility) in sources.items():
        columns = ["Access Road Edge ID", "Network Snap Accepted"]
        if eligibility is not None:
            columns.append(eligibility)
        frame = pd.read_parquet(PROCESSED / filename, columns=columns)
        keep = frame["Network Snap Accepted"].fillna(False)
        if eligibility is not None:
            keep &= frame[eligibility].fillna(False)
        frame = frame.loc[keep & frame["Access Road Edge ID"].notna()].copy()
        frame["Road Section ID"] = (
            frame["Access Road Edge ID"].astype(str).map(edge_to_section)
        )
        if frame["Road Section ID"].isna().any():
            raise RuntimeError(f"Accepted {output_column} has an unmapped road edge")
        count = (
            frame.groupby("Road Section ID", sort=False)
            .size()
            .rename(output_column)
            .reset_index()
        )
        frames.append(count)
    combined = frames[0]
    for frame in frames[1:]:
        combined = combined.merge(frame, on="Road Section ID", how="outer")
    count_columns = list(sources)
    combined[count_columns] = combined[count_columns].fillna(0).astype(int)
    combined["Total Connector Count"] = combined[count_columns].sum(axis=1)
    return combined


def independent_recomputation(result: pd.DataFrame) -> dict[str, object]:
    started = perf_counter()
    network = build_compact_emergency_network(
        PROCESSED, include_population_groups=False
    )
    baseline = network.route(assign_hospitals=False)
    baseline_timely = np.stack(
        [baseline.total_time <= threshold for threshold in THRESHOLDS]
    )
    population = network.demand_population

    loss_columns = [f"Potential Access Loss {value} Minutes" for value in THRESHOLDS]
    top_indices = set()
    for column in loss_columns:
        top_indices.update(result.nlargest(4, column)["Section Index"].astype(int))
    positive_pool = result.loc[result[loss_columns].gt(0).any(axis=1), "Section Index"]
    zero_candidate_pool = result.loc[
        result["Candidate for Rerouting"] & result[loss_columns].eq(0).all(axis=1),
        "Section Index",
    ]
    screened_zero_pool = result.loc[
        ~result["Candidate for Rerouting"], "Section Index"
    ]
    rng = np.random.default_rng(20260806)
    sample_indices = set(top_indices)
    for pool, sample_size in (
        (positive_pool, 16),
        (zero_candidate_pool, 12),
        (screened_zero_pool, 12),
    ):
        values = pool.to_numpy(dtype=np.int32)
        chosen = rng.choice(values, size=min(sample_size, len(values)), replace=False)
        sample_indices.update(int(value) for value in chosen)

    result_by_index = result.set_index("Section Index")
    checks: list[dict[str, object]] = []
    failed = np.zeros(network.road_section_count, dtype=bool)
    for section_index in sorted(sample_indices):
        failed[section_index] = True
        state = network.route(failed=failed, assign_hospitals=False)
        disrupted_timely = np.stack(
            [state.total_time <= threshold for threshold in THRESHOLDS]
        )
        losses = ((baseline_timely & ~disrupted_timely) * population[None, :]).sum(
            axis=1
        )
        stored = result_by_index.loc[section_index, loss_columns].to_numpy(dtype=float)
        checks.append(
            {
                "Section Index": int(section_index),
                "Road Section ID": str(network.road_section_ids[section_index]),
                "Stored Losses": stored.tolist(),
                "Recomputed Losses": losses.astype(float).tolist(),
                "Exact Match": bool(np.array_equal(stored, losses)),
            }
        )
        failed[section_index] = False
    return {
        "sample_size": len(checks),
        "all_exact_matches": all(bool(row["Exact Match"]) for row in checks),
        "elapsed_seconds": perf_counter() - started,
        "checks": checks,
    }


def main() -> None:
    result = pd.read_parquet(RESULT_PATH)
    sections = gpd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=[
            "Road Section ID",
            "Section From Node ID",
            "Section To Node ID",
            "Network Component ID",
            "Road Section Length (m)",
            "Road Edge Count",
            "Geometry",
        ],
    )
    edges = pd.read_parquet(
        PROCESSED / "kumamoto_routable_road_edges_preprocessed.parquet",
        columns=["Road Edge ID", "Road Section ID"],
    )
    edges["Road Edge ID"] = edges["Road Edge ID"].astype(str)
    edges["Road Section ID"] = edges["Road Section ID"].astype(str)
    edge_to_section = edges.drop_duplicates("Road Edge ID").set_index(
        "Road Edge ID"
    )["Road Section ID"]
    counts = connector_counts(edge_to_section)

    if len(result) != len(sections) or not result["Road Section ID"].is_unique:
        raise RuntimeError("All-section result must contain one row per road section")
    loss_columns = [f"Potential Access Loss {value} Minutes" for value in THRESHOLDS]
    if result[loss_columns].isna().any().any() or (result[loss_columns] < 0).any().any():
        raise RuntimeError("Potential losses must be complete and nonnegative")

    for severity in SEVERITIES:
        probability = result[f"Section Failure Probability {severity} Percent"]
        expected = result[f"Expected Risk 30 Minutes {severity} Percent"]
        if not probability.between(0, 1).all():
            raise RuntimeError(f"Invalid {severity}% section failure probability")
        if not np.allclose(
            expected,
            probability * result["Potential Access Loss 30 Minutes"],
            rtol=0,
            atol=1e-12,
        ):
            raise RuntimeError(f"Invalid {severity}% expected-risk calculation")

    topology = sections.copy()
    topology["Road Section ID"] = topology["Road Section ID"].astype(str)
    topology["Geometry Valid"] = topology.geometry.is_valid
    topology["Geometry Empty"] = topology.geometry.is_empty
    topology["Distinct Section Endpoints"] = topology[
        "Section From Node ID"
    ].astype(str).ne(topology["Section To Node ID"].astype(str))
    topology["Closed Loop Section"] = ~topology["Distinct Section Endpoints"]
    topology = topology.merge(counts, on="Road Section ID", how="left")
    count_columns = [
        "Population Connector Count",
        "Dispatch Connector Count",
        "Hospital Connector Count",
        "Total Connector Count",
    ]
    topology[count_columns] = topology[count_columns].fillna(0).astype(int)

    upper_tail_parts: list[pd.DataFrame] = []
    cutoffs: dict[str, float] = {}
    for threshold, column in zip(THRESHOLDS, loss_columns, strict=True):
        positive = result.loc[result[column] > 0, column]
        cutoff = float(positive.quantile(0.99))
        cutoffs[str(threshold)] = cutoff
        selected = result.loc[result[column] >= cutoff].copy()
        selected.insert(0, "Audited Threshold (min)", threshold)
        selected.insert(1, "Upper-Tail Cutoff", cutoff)
        upper_tail_parts.append(selected)
    upper_tail = pd.concat(upper_tail_parts, ignore_index=True)
    upper_tail = upper_tail.merge(
        topology.drop(columns="Geometry"),
        on="Road Section ID",
        how="left",
        suffixes=("", " Audit"),
        validate="many_to_one",
    )
    upper_tail["Topology Audit Status"] = np.where(
        upper_tail["Geometry Valid"]
        & ~upper_tail["Geometry Empty"]
        & (
            upper_tail["Distinct Section Endpoints"]
            | (
                upper_tail["Closed Loop Section"]
                & upper_tail["Road Edge Count Audit"].ge(2)
            )
        )
        & upper_tail["Road Section Length (m) Audit"].gt(0)
        & upper_tail["Road Edge Count Audit"].ge(1)
        & upper_tail["Network Component ID Audit"].notna(),
        "Pass",
        "Review",
    )
    upper_tail_path = EXPERIMENT / "upper_tail_topology_connector_audit.parquet"
    upper_tail.to_parquet(upper_tail_path, index=False)

    recomputation = independent_recomputation(result)
    if not recomputation["all_exact_matches"]:
        raise RuntimeError("Independent sample recomputation did not match stored losses")

    summary = {
        "all_section_rows": int(len(result)),
        "unique_road_section_ids": bool(result["Road Section ID"].is_unique),
        "loss_values_complete_nonnegative": True,
        "expected_risk_formula_checks_pass": True,
        "positive_upper_tail_definition": "Top 1% among positive-loss sections by threshold",
        "positive_upper_tail_cutoffs": cutoffs,
        "upper_tail_audit_rows": int(len(upper_tail)),
        "upper_tail_unique_sections": int(upper_tail["Road Section ID"].nunique()),
        "upper_tail_topology_all_pass": bool(
            upper_tail["Topology Audit Status"].eq("Pass").all()
        ),
        "upper_tail_sections_with_connectors": int(
            upper_tail.loc[upper_tail["Total Connector Count"] > 0, "Road Section ID"].nunique()
        ),
        "upper_tail_closed_loop_sections": int(
            upper_tail.loc[upper_tail["Closed Loop Section"], "Road Section ID"].nunique()
        ),
        "independent_recomputation": recomputation,
    }
    summary_path = EXPERIMENT / "audit_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved: {upper_tail_path.relative_to(ROOT)}")
    print(f"Saved: {summary_path.relative_to(ROOT)}")
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "independent_recomputation"},
            indent=2,
        )
    )
    print(
        "Independent recomputation:",
        recomputation["sample_size"],
        "sections; all exact matches =",
        recomputation["all_exact_matches"],
    )


if __name__ == "__main__":
    main()
