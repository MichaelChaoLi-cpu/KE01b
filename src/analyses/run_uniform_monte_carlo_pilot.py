#!/usr/bin/env python3
"""Run the seeded uniform random road-failure pilot or full experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from monte_carlo_emergency_routing import build_compact_emergency_network


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUTPUT = ROOT / "data" / "exp" / "monte_carlo_uniform_pilot_100"
FAILURE_RATES = np.array([0.05, 0.10, 0.20], dtype=np.float64)
THRESHOLDS = np.array([15, 30, 45], dtype=np.int16)
PRIMARY_THRESHOLD_INDEX = 1
RANDOM_FAILURE_MODEL = "Uniform Random"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=100)
    parser.add_argument("--base-seed", type=int, default=20260805)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def _importance_statistics(
    failed_count: np.ndarray,
    failed_sum: np.ndarray,
    failed_sum_of_squares: np.ndarray,
    system_values: np.ndarray,
) -> dict[str, np.ndarray]:
    """Compute conditional road-importance statistics from sufficient statistics."""
    replicates = len(system_values)
    available_count = replicates - failed_count
    total_sum = float(system_values.sum())
    total_sum_of_squares = float(np.square(system_values).sum())
    available_sum = total_sum - failed_sum
    available_sum_of_squares = total_sum_of_squares - failed_sum_of_squares

    failed_mean = np.full(len(failed_count), np.nan, dtype=np.float64)
    available_mean = np.full(len(failed_count), np.nan, dtype=np.float64)
    has_failed = failed_count > 0
    has_available = available_count > 0
    failed_mean[has_failed] = failed_sum[has_failed] / failed_count[has_failed]
    available_mean[has_available] = (
        available_sum[has_available] / available_count[has_available]
    )
    importance = available_mean - failed_mean

    failed_variance = np.full(len(failed_count), np.nan, dtype=np.float64)
    available_variance = np.full(len(failed_count), np.nan, dtype=np.float64)
    enough_failed = failed_count > 1
    enough_available = available_count > 1
    failed_variance[enough_failed] = np.maximum(
        0.0,
        (
            failed_sum_of_squares[enough_failed]
            - np.square(failed_sum[enough_failed]) / failed_count[enough_failed]
        )
        / (failed_count[enough_failed] - 1),
    )
    available_variance[enough_available] = np.maximum(
        0.0,
        (
            available_sum_of_squares[enough_available]
            - np.square(available_sum[enough_available])
            / available_count[enough_available]
        )
        / (available_count[enough_available] - 1),
    )
    standard_error = np.sqrt(
        failed_variance / failed_count + available_variance / available_count
    )
    precision_eligible = (failed_count >= 30) & (available_count >= 30)
    return {
        "available_count": available_count,
        "importance": importance,
        "standard_error": standard_error,
        "confidence_low": importance - 1.96 * standard_error,
        "confidence_high": importance + 1.96 * standard_error,
        "precision_eligible": precision_eligible,
    }


def _top_indices(values: np.ndarray, count: int = 20) -> np.ndarray:
    """Return deterministic indices of the largest finite values."""
    finite = np.flatnonzero(np.isfinite(values))
    if not len(finite):
        return np.empty(0, dtype=np.int64)
    order = np.lexsort((finite, -values[finite]))
    return finite[order[:count]]


def _rank_vector(values: np.ndarray) -> np.ndarray:
    """Return deterministic one-based ranks, with nonfinite values ranked last."""
    ranks = np.full(len(values), len(values) + 1, dtype=np.int32)
    finite = np.flatnonzero(np.isfinite(values))
    if len(finite):
        order = np.lexsort((finite, -values[finite]))
        ranks[finite[order]] = np.arange(1, len(finite) + 1, dtype=np.int32)
    return ranks


def _linear_p90_with_unreachable(
    replicate_times: np.ndarray,
    finite_count: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return empirical P90, marking grids with at least 10% disconnection."""
    replicates = replicate_times.shape[0]
    unreachable = (replicates - finite_count) >= int(np.ceil(0.10 * replicates))
    ordered = np.sort(replicate_times, axis=0)
    position = 0.90 * (replicates - 1)
    lower = int(np.floor(position))
    upper = int(np.ceil(position))
    weight = position - lower
    p90 = ordered[lower] * (1.0 - weight) + ordered[upper] * weight
    p90 = p90.astype(np.float64)
    p90[unreachable] = np.nan
    return p90, unreachable


def main() -> None:
    args = parse_args()
    if args.replicates < 2:
        raise ValueError("The pilot requires at least two replicates")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    overall_started = perf_counter()
    network = build_compact_emergency_network(PROCESSED)
    print(
        f"Built compact graph: {network.node_count:,} nodes, "
        f"{network.road_section_count:,} road sections in {network.build_seconds:.2f}s",
        flush=True,
    )
    baseline = network.route(assign_hospitals=True)
    baseline_timely = np.stack(
        [baseline.total_time <= threshold for threshold in THRESHOLDS]
    )

    replicate_count = args.replicates
    rate_count = len(FAILURE_RATES)
    demand_count = len(network.demand_ids)
    road_count = network.road_section_count
    hospital_count = len(network.hospital_ids)
    population = network.demand_population
    total_population = float(population.sum())

    time_store_path = args.output_dir / ".total_times_working.float32"
    all_times = np.memmap(
        time_store_path,
        mode="w+",
        shape=(rate_count, replicate_count, demand_count),
        dtype=np.float32,
    )
    finite_counts = np.zeros((rate_count, demand_count), dtype=np.uint16)
    timely_counts = np.zeros(
        (rate_count, len(THRESHOLDS), demand_count), dtype=np.uint16
    )
    hospital_catchment = np.zeros(
        (rate_count, replicate_count, hospital_count), dtype=np.float64
    )
    failed_counts = np.zeros((rate_count, road_count), dtype=np.uint16)
    failed_system_sum = np.zeros((rate_count, road_count), dtype=np.float64)
    failed_system_sum_of_squares = np.zeros(
        (rate_count, road_count), dtype=np.float64
    )
    system_values = np.zeros((rate_count, replicate_count), dtype=np.float64)
    metrics: list[dict[str, float | int | str]] = []
    monotonic_pass = True
    exact_count_pass = True
    nested_pass = True
    formal_checkpoints = [
        checkpoint
        for checkpoint in (100, 250, 500, 750, 1000)
        if checkpoint <= replicate_count
    ]
    if replicate_count not in formal_checkpoints:
        formal_checkpoints.append(replicate_count)
    formal_checkpoints = sorted(set(formal_checkpoints))
    checkpoint_importance: dict[int, list[np.ndarray]] = {}

    simulation_started = perf_counter()
    for replicate_offset in range(replicate_count):
        replicate = replicate_offset + 1
        rng = np.random.default_rng(
            np.random.SeedSequence([args.base_seed, replicate])
        )
        order = rng.permutation(road_count)
        failed = np.zeros(road_count, dtype=bool)
        previous_failed_count = 0
        previous_time = baseline.total_time

        for rate_index, failure_rate in enumerate(FAILURE_RATES):
            failed_count = int(np.floor(failure_rate * road_count))
            failed[order[previous_failed_count:failed_count]] = True
            exact_count_pass &= int(failed.sum()) == failed_count
            nested_pass &= bool(
                np.all(failed[order[:previous_failed_count]])
            )
            state = network.route(failed, assign_hospitals=True)
            finite = np.isfinite(state.total_time)
            finite_both = np.isfinite(previous_time) & finite
            no_shorter = np.all(
                state.total_time[finite_both] + 1e-10 >= previous_time[finite_both]
            )
            no_reconnection = not np.any(~np.isfinite(previous_time) & finite)
            monotonic_pass &= bool(no_shorter and no_reconnection)

            all_times[rate_index, replicate_offset] = state.total_time.astype(
                np.float32
            )
            finite_counts[rate_index] += finite
            timely_states = np.stack(
                [state.total_time <= threshold for threshold in THRESHOLDS]
            )
            timely_counts[rate_index] += timely_states
            covered_population = np.array(
                [population[timely].sum() for timely in timely_states],
                dtype=np.float64,
            )
            lost_population = np.array(
                [
                    population[baseline_timely[index] & ~timely_states[index]].sum()
                    for index in range(len(THRESHOLDS))
                ],
                dtype=np.float64,
            )
            primary_value = covered_population[PRIMARY_THRESHOLD_INDEX]
            system_values[rate_index, replicate_offset] = primary_value
            failed_indices = order[:failed_count]
            failed_counts[rate_index, failed_indices] += 1
            failed_system_sum[rate_index, failed_indices] += primary_value
            failed_system_sum_of_squares[rate_index, failed_indices] += (
                primary_value * primary_value
            )

            assigned = state.assigned_hospital_index
            if assigned is None:
                raise RuntimeError("Hospital assignment was not returned")
            assigned_valid = assigned >= 0
            hospital_catchment[rate_index, replicate_offset] = np.bincount(
                assigned[assigned_valid],
                weights=population[assigned_valid],
                minlength=hospital_count,
            )

            row: dict[str, float | int | str] = {
                "Random Failure Model": RANDOM_FAILURE_MODEL,
                "Base Seed": args.base_seed,
                "Simulation Replicate": replicate,
                "Failure Rate": float(failure_rate),
                "Failed Road Sections": failed_count,
                "Finite Demand Units": int(finite.sum()),
                "Finite Population": int(population[finite].sum()),
                "Routing Seconds": float(state.routing_seconds),
            }
            for threshold_index, threshold in enumerate(THRESHOLDS):
                row[f"Population within {int(threshold)} min"] = int(
                    covered_population[threshold_index]
                )
                row[f"Population Losing Baseline {int(threshold)} min Access"] = int(
                    lost_population[threshold_index]
                )
            metrics.append(row)
            previous_failed_count = failed_count
            previous_time = state.total_time

        if replicate in formal_checkpoints:
            checkpoint_importance[replicate] = []
            for rate_index in range(rate_count):
                checkpoint_statistics = _importance_statistics(
                    failed_counts[rate_index],
                    failed_system_sum[rate_index],
                    failed_system_sum_of_squares[rate_index],
                    system_values[rate_index, :replicate],
                )
                checkpoint_values = checkpoint_statistics["importance"].copy()
                checkpoint_values[
                    ~checkpoint_statistics["precision_eligible"]
                ] = np.nan
                checkpoint_importance[replicate].append(
                    checkpoint_values.astype(np.float32)
                )
            print(f"Recorded convergence checkpoint {replicate}", flush=True)
        progress_interval = 10 if replicate_count <= 100 else 50
        if replicate % progress_interval == 0 or replicate == replicate_count:
            elapsed = perf_counter() - simulation_started
            print(
                f"Completed {replicate}/{replicate_count} replicates "
                f"({3 * replicate} states) in {elapsed:.2f}s",
                flush=True,
            )

    simulation_seconds = perf_counter() - simulation_started
    metrics_frame = pd.DataFrame(metrics)
    metrics_frame.to_parquet(
        args.output_dir / "replicate_metrics.parquet", index=False
    )

    demand_dimension = pd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_network_access_preprocessed.parquet",
        columns=["Mesh Code", "Analysis Unit ID", "Demand Node ID", "Total Population"],
    )
    if not np.array_equal(
        demand_dimension["Demand Node ID"].astype("string").fillna("").astype(str),
        network.demand_ids,
    ):
        raise RuntimeError("Demand order changed between graph build and output assembly")
    grid_frames: list[pd.DataFrame] = []
    for rate_index, failure_rate in enumerate(FAILURE_RATES):
        p90, p90_unreachable = _linear_p90_with_unreachable(
            all_times[rate_index], finite_counts[rate_index]
        )
        frame = demand_dimension.copy()
        frame["Random Failure Model"] = RANDOM_FAILURE_MODEL
        frame["Failure Rate"] = float(failure_rate)
        frame["Simulation Replicates"] = replicate_count
        frame["Finite Access Probability"] = (
            finite_counts[rate_index] / replicate_count
        )
        for threshold_index, threshold in enumerate(THRESHOLDS):
            frame[f"Timely Access Probability {int(threshold)} min"] = (
                timely_counts[rate_index, threshold_index] / replicate_count
            )
        frame["P90 Emergency Access Time"] = p90
        frame["P90 Unreachable"] = p90_unreachable
        grid_frames.append(frame)
    pd.concat(grid_frames, ignore_index=True).to_parquet(
        args.output_dir / "grid_reliability.parquet", index=False
    )
    del all_times
    time_store_path.unlink(missing_ok=True)

    hospital_dimension = pd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=["Hospital Node ID", "Facility Name", "Eligible Emergency Hospital"],
    )
    hospital_dimension = hospital_dimension.loc[
        hospital_dimension["Eligible Emergency Hospital"].fillna(False)
    ].copy()
    hospital_dimension["Hospital Node ID"] = hospital_dimension[
        "Hospital Node ID"
    ].astype(str)
    hospital_dimension = hospital_dimension.set_index("Hospital Node ID").loc[
        network.hospital_ids
    ].reset_index()
    hospital_frames: list[pd.DataFrame] = []
    for rate_index, failure_rate in enumerate(FAILURE_RATES):
        catchment = hospital_catchment[rate_index]
        frame = hospital_dimension.copy()
        frame["Random Failure Model"] = RANDOM_FAILURE_MODEL
        frame["Failure Rate"] = float(failure_rate)
        frame["Simulation Replicates"] = replicate_count
        frame["Mean Hospital Catchment Population"] = catchment.mean(axis=0)
        frame["Hospital Catchment Standard Deviation"] = catchment.std(
            axis=0, ddof=1
        )
        quantiles = np.quantile(catchment, [0.05, 0.50, 0.95], axis=0)
        frame["Hospital Catchment P5"] = quantiles[0]
        frame["Hospital Catchment P50"] = quantiles[1]
        frame["Hospital Catchment P95"] = quantiles[2]
        frame["Zero Catchment Frequency"] = (catchment == 0).mean(axis=0)
        frame["Population-Weighted Hospital Assignment Probability"] = (
            catchment.mean(axis=0) / total_population
        )
        hospital_frames.append(frame)
    pd.concat(hospital_frames, ignore_index=True).to_parquet(
        args.output_dir / "hospital_service_reliability.parquet", index=False
    )

    road_dimension = pd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet",
        columns=[
            "Road Section ID",
            "Road Section Length (m)",
            "Route Name",
            "Road Category",
        ],
    )
    if not np.array_equal(
        road_dimension["Road Section ID"].astype(str),
        network.road_section_ids,
    ):
        raise RuntimeError("Road-section order changed during experiment")
    road_dimension.to_parquet(
        args.output_dir / "road_section_dimension.parquet", index=False
    )

    importance_frames: list[pd.DataFrame] = []
    importance_by_rate: list[dict[str, np.ndarray]] = []
    for rate_index, failure_rate in enumerate(FAILURE_RATES):
        statistics = _importance_statistics(
            failed_counts[rate_index],
            failed_system_sum[rate_index],
            failed_system_sum_of_squares[rate_index],
            system_values[rate_index],
        )
        importance_by_rate.append(statistics)
        importance_frames.append(
            pd.DataFrame(
                {
                    "Road Section ID": network.road_section_ids,
                    "Random Failure Model": RANDOM_FAILURE_MODEL,
                    "Failure Rate": float(failure_rate),
                    "Simulation Replicates": replicate_count,
                    "Failed Replicate Count": failed_counts[rate_index],
                    "Available Replicate Count": statistics["available_count"],
                    "Road Failure Importance": statistics["importance"],
                    "Road Importance Standard Error": statistics["standard_error"],
                    "Confidence Interval Low": statistics["confidence_low"],
                    "Confidence Interval High": statistics["confidence_high"],
                    "Precision Eligible": statistics["precision_eligible"],
                }
            )
        )
    road_importance_name = (
        "road_importance.parquet"
        if replicate_count >= 1000
        else "road_importance_pilot.parquet"
    )
    pd.concat(importance_frames, ignore_index=True).to_parquet(
        args.output_dir / road_importance_name, index=False
    )

    coverage_checkpoint_diagnostics: list[dict[str, float | int]] = []
    coverage_lookup: dict[tuple[int, int], dict[str, float | int]] = {}
    for checkpoint in formal_checkpoints:
        for rate_index, failure_rate in enumerate(FAILURE_RATES):
            values = system_values[rate_index, :checkpoint]
            standard_error = float(values.std(ddof=1) / np.sqrt(checkpoint))
            diagnostic: dict[str, float | int] = {
                "checkpoint": checkpoint,
                "failure_rate": float(failure_rate),
                "mean_30_minute_population": float(values.mean()),
                "standard_error_population": standard_error,
                "ci_half_width_percentage_points": 100.0
                * 1.96
                * standard_error
                / total_population,
            }
            coverage_checkpoint_diagnostics.append(diagnostic)
            coverage_lookup[(checkpoint, rate_index)] = diagnostic

    transition_diagnostics: list[dict[str, float | int | None]] = []
    transition_lookup: dict[
        tuple[int, int, int], dict[str, float | int | None]
    ] = {}
    for previous_checkpoint, current_checkpoint in zip(
        formal_checkpoints[:-1], formal_checkpoints[1:], strict=True
    ):
        for rate_index, failure_rate in enumerate(FAILURE_RATES):
            previous_values = checkpoint_importance[previous_checkpoint][rate_index]
            current_values = checkpoint_importance[current_checkpoint][rate_index]
            previous_top = set(_top_indices(previous_values).tolist())
            current_top = set(_top_indices(current_values).tolist())
            union = previous_top | current_top
            jaccard = (
                len(previous_top & current_top) / len(union) if union else np.nan
            )
            median_rank_change = np.nan
            if union:
                selected = np.fromiter(union, dtype=np.int64, count=len(union))
                previous_ranks = _rank_vector(previous_values)
                current_ranks = _rank_vector(current_values)
                median_rank_change = float(
                    np.median(
                        np.abs(
                            previous_ranks[selected].astype(np.int64)
                            - current_ranks[selected].astype(np.int64)
                        )
                    )
                )
            previous_mean = float(
                coverage_lookup[(previous_checkpoint, rate_index)][
                    "mean_30_minute_population"
                ]
            )
            current_mean = float(
                coverage_lookup[(current_checkpoint, rate_index)][
                    "mean_30_minute_population"
                ]
            )
            transition: dict[str, float | int | None] = {
                "previous_checkpoint": previous_checkpoint,
                "current_checkpoint": current_checkpoint,
                "failure_rate": float(failure_rate),
                "coverage_change_percentage_points": 100.0
                * abs(current_mean - previous_mean)
                / total_population,
                "top_20_jaccard": float(jaccard) if np.isfinite(jaccard) else None,
                "median_absolute_rank_change": (
                    float(median_rank_change)
                    if np.isfinite(median_rank_change)
                    else None
                ),
            }
            transition_diagnostics.append(transition)
            transition_lookup[(previous_checkpoint, current_checkpoint, rate_index)] = (
                transition
            )

    road_diagnostics: list[dict[str, float | int | bool | None]] = []
    convergence_by_rate: list[dict[str, float | int | bool | str | None]] = []
    previous_final_checkpoint = (
        formal_checkpoints[-2] if len(formal_checkpoints) >= 2 else None
    )
    for rate_index, failure_rate in enumerate(FAILURE_RATES):
        statistics = importance_by_rate[rate_index]
        final_rank_values = checkpoint_importance[replicate_count][rate_index]
        top_full = _top_indices(final_rank_values)
        top_failed_min = int(failed_counts[rate_index, top_full].min()) if len(top_full) else 0
        top_available_min = (
            int(statistics["available_count"][top_full].min()) if len(top_full) else 0
        )
        final_transition = None
        if previous_final_checkpoint is not None:
            final_transition = transition_lookup[
                (previous_final_checkpoint, replicate_count, rate_index)
            ]
        final_coverage = coverage_lookup[(replicate_count, rate_index)]
        coverage_change = (
            float(final_transition["coverage_change_percentage_points"])
            if final_transition is not None
            else np.nan
        )
        jaccard = (
            final_transition["top_20_jaccard"]
            if final_transition is not None
            else None
        )
        median_rank_change = (
            final_transition["median_absolute_rank_change"]
            if final_transition is not None
            else None
        )
        coverage_change_met = bool(
            np.isfinite(coverage_change) and coverage_change <= 0.5
        )
        coverage_ci_met = bool(
            float(final_coverage["ci_half_width_percentage_points"]) <= 0.5
        )
        jaccard_met = bool(jaccard is not None and float(jaccard) >= 0.80)
        rank_change_met = bool(
            median_rank_change is not None and float(median_rank_change) <= 2.0
        )
        effective_count_met = bool(
            len(top_full) == 20 and top_failed_min >= 30 and top_available_min >= 30
        )
        formally_assessed = replicate_count >= 1000 and previous_final_checkpoint == 750
        convergence_met = bool(
            formally_assessed
            and coverage_change_met
            and coverage_ci_met
            and jaccard_met
            and rank_change_met
            and effective_count_met
        )
        road_diagnostics.append(
            {
                "failure_rate": float(failure_rate),
                "minimum_failed_count": int(failed_counts[rate_index].min()),
                "median_failed_count": float(
                    np.median(failed_counts[rate_index])
                ),
                "maximum_failed_count": int(failed_counts[rate_index].max()),
                "precision_eligible_units": int(
                    statistics["precision_eligible"].sum()
                ),
                "top_20_minimum_failed_count": top_failed_min,
                "top_20_minimum_available_count": top_available_min,
                "final_adjacent_top_20_jaccard": jaccard,
                "final_adjacent_median_absolute_rank_change": median_rank_change,
            }
        )
        convergence_by_rate.append(
            {
                "failure_rate": float(failure_rate),
                "formally_assessed": formally_assessed,
                "coverage_change_rule_met": coverage_change_met,
                "coverage_ci_half_width_rule_met": coverage_ci_met,
                "top_20_jaccard_rule_met": jaccard_met,
                "median_rank_change_rule_met": rank_change_met,
                "top_20_effective_count_rule_met": effective_count_met,
                "monte_carlo_convergence_met": convergence_met,
                "status": (
                    "Met"
                    if convergence_met
                    else (
                        "Not met"
                        if formally_assessed
                        else "Pilot complete; formal convergence not assessed"
                    )
                ),
            }
        )

    full_convergence_met = bool(
        replicate_count >= 1000
        and all(item["monte_carlo_convergence_met"] for item in convergence_by_rate)
    )
    summary = {
        "design": {
            "random_failure_model": RANDOM_FAILURE_MODEL,
            "base_seed": args.base_seed,
            "replicates": replicate_count,
            "failure_rates": FAILURE_RATES.tolist(),
            "network_states": int(replicate_count * rate_count),
        },
        "network": {
            "road_sections": road_count,
            "nodes": network.node_count,
            "directed_node_pairs": network.directed_pair_count,
            "demand_units": demand_count,
            "hospitals": hospital_count,
            "graph_build_seconds": network.build_seconds,
            "baseline_routing_seconds": baseline.routing_seconds,
        },
        "checks": {
            "exact_failed_counts": bool(exact_count_pass),
            "nested_failure_sets": bool(nested_pass),
            "travel_time_monotone_after_removal": bool(monotonic_pass),
            "replicate_rows": int(len(metrics_frame)),
            "expected_replicate_rows": int(replicate_count * rate_count),
        },
        "coverage_checkpoint_diagnostics": coverage_checkpoint_diagnostics,
        "checkpoint_transition_diagnostics": transition_diagnostics,
        "road_diagnostics": road_diagnostics,
        "runtime": {
            "simulation_seconds": simulation_seconds,
            "total_seconds": perf_counter() - overall_started,
            "mean_state_routing_seconds": float(
                metrics_frame["Routing Seconds"].mean()
            ),
            "estimated_1000_replicate_core_seconds": float(
                network.build_seconds
                + simulation_seconds * 1000.0 / replicate_count
            ),
        },
        "convergence_assessment": {
            "checkpoint_sequence": formal_checkpoints,
            "by_failure_rate": convergence_by_rate,
            "all_failure_rates_converged": full_convergence_met,
        },
        "outputs": {
            "replicate_metrics": "replicate_metrics.parquet",
            "grid_reliability": "grid_reliability.parquet",
            "hospital_service_reliability": "hospital_service_reliability.parquet",
            "road_section_dimension": "road_section_dimension.parquet",
            "road_importance": road_importance_name,
        },
    }
    if not all(summary["checks"][key] for key in (
        "exact_failed_counts",
        "nested_failure_sets",
        "travel_time_monotone_after_removal",
    )):
        raise RuntimeError("A required experiment correctness check failed")
    summary_name = (
        "experiment_summary.json"
        if replicate_count >= 1000
        else "pilot_summary.json"
    )
    (args.output_dir / summary_name).write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
