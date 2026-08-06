#!/usr/bin/env python3
"""Run the formal length-dependent emergency-access Monte Carlo experiment."""

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
DEFAULT_OUTPUT = ROOT / "data" / "exp" / "monte_carlo_length_weighted_full_1000"
TARGETS = np.array([0.01, 0.03, 0.05, 0.10], dtype=np.float64)
THRESHOLDS = np.array([15, 30, 45], dtype=np.int16)
RANDOM_FAILURE_MODEL = "Length-Dependent Independent"
CHECKPOINT_CANDIDATES = (100, 250, 500, 750, 1000)
COVERAGE_MEAN_CHANGE_SHARE_MAXIMUM = 0.005
GRID_PROBABILITY_P95_ABSOLUTE_CHANGE_MAXIMUM = 0.05
HOSPITAL_CATCHMENT_P95_CHANGE_SHARE_MAXIMUM = 0.005


def expected_failed_length_share(intensity: float, lengths: np.ndarray) -> float:
    probabilities = -np.expm1(-intensity * lengths)
    return float(np.dot(lengths, probabilities) / lengths.sum())


def calibrate_intensity(target: float, lengths: np.ndarray) -> float:
    low = 0.0
    high = 1.0 / float(np.median(lengths))
    while expected_failed_length_share(high, lengths) < target:
        high *= 2.0
    for _ in range(80):
        midpoint = 0.5 * (low + high)
        if expected_failed_length_share(midpoint, lengths) < target:
            low = midpoint
        else:
            high = midpoint
    return 0.5 * (low + high)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=1000)
    parser.add_argument("--base-seed", type=int, default=20260806)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def reliability_arrays(
    times: np.ndarray,
    baseline_time: np.ndarray,
    chunk_size: int = 5000,
) -> dict[str, np.ndarray]:
    """Aggregate replicate travel times without loading a full severity cube."""
    replicates, demand_count = times.shape
    finite_probability = np.empty(demand_count, dtype=np.float32)
    timely_probability = np.empty((len(THRESHOLDS), demand_count), dtype=np.float32)
    loss_probability = np.empty((len(THRESHOLDS), demand_count), dtype=np.float32)
    p90 = np.empty(demand_count, dtype=np.float32)
    p90_unreachable = np.empty(demand_count, dtype=bool)
    baseline_timely = np.stack(
        [baseline_time <= threshold for threshold in THRESHOLDS]
    )
    unreachable_cutoff = int(np.ceil(0.10 * replicates))

    for start in range(0, demand_count, chunk_size):
        stop = min(start + chunk_size, demand_count)
        block = np.asarray(times[:, start:stop], dtype=np.float32)
        finite = np.isfinite(block)
        finite_count = finite.sum(axis=0)
        finite_probability[start:stop] = finite_count / replicates
        unreachable = (replicates - finite_count) >= unreachable_cutoff
        p90_unreachable[start:stop] = unreachable
        block_p90 = np.full(stop - start, np.nan, dtype=np.float32)
        quantile_columns = ~unreachable
        if quantile_columns.any():
            ordered = np.sort(block[:, quantile_columns], axis=0)
            position = 0.90 * (replicates - 1)
            lower = int(np.floor(position))
            upper = int(np.ceil(position))
            weight = position - lower
            block_p90[quantile_columns] = (
                ordered[lower] * (1.0 - weight) + ordered[upper] * weight
            )
        p90[start:stop] = block_p90
        for threshold_index, threshold in enumerate(THRESHOLDS):
            probability = (block <= threshold).mean(axis=0)
            timely_probability[threshold_index, start:stop] = probability
            loss_probability[threshold_index, start:stop] = np.where(
                baseline_timely[threshold_index, start:stop],
                1.0 - probability,
                0.0,
            )
    return {
        "finite_probability": finite_probability,
        "timely_probability": timely_probability,
        "loss_probability": loss_probability,
        "p90": p90,
        "p90_unreachable": p90_unreachable,
    }


def system_summary(values: np.ndarray) -> dict[str, float]:
    return {
        "Mean": float(values.mean()),
        "Standard Error": float(values.std(ddof=1) / np.sqrt(len(values))),
        "P05": float(np.quantile(values, 0.05)),
        "P50": float(np.quantile(values, 0.50)),
        "P95": float(np.quantile(values, 0.95)),
    }


def main() -> None:
    args = parse_args()
    if args.replicates < 2:
        raise ValueError("At least two replicates are required")
    if not args.output_dir.is_absolute():
        args.output_dir = ROOT / args.output_dir
    args.output_dir.mkdir(parents=True, exist_ok=True)
    overall_started = perf_counter()

    network = build_compact_emergency_network(
        PROCESSED, include_population_groups=True
    )
    baseline = network.route(assign_hospitals=True)
    mesh_mask = network.demand_type == "population_mesh"
    older_mask = network.demand_type == "older_population_group"
    mesh_count = int(mesh_mask.sum())
    older_count = int(older_mask.sum())
    if not np.array_equal(np.flatnonzero(mesh_mask), np.arange(mesh_count)):
        raise RuntimeError("Population mesh demand must precede older-population groups")
    if not np.array_equal(
        np.flatnonzero(older_mask), np.arange(mesh_count, mesh_count + older_count)
    ):
        raise RuntimeError("Older-population groups must follow population meshes")
    print(
        f"Built graph with {network.road_section_count:,} road sections, "
        f"{mesh_count:,} population grids, and {older_count:,} older-population groups "
        f"in {network.build_seconds:.2f}s",
        flush=True,
    )

    sections = pd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet"
    )
    sections["Road Section ID"] = sections["Road Section ID"].astype(str)
    sections = sections.set_index("Road Section ID").loc[
        network.road_section_ids
    ].reset_index()
    lengths = sections["Road Section Length (m)"].to_numpy(np.float64)
    intensities = np.array(
        [calibrate_intensity(target, lengths) for target in TARGETS]
    )
    probabilities = np.vstack(
        [-np.expm1(-intensity * lengths) for intensity in intensities]
    )
    if not np.all(np.diff(probabilities, axis=0) >= -1e-15):
        raise RuntimeError("Section failure probabilities are not nested")

    replicate_count = args.replicates
    severity_count = len(TARGETS)
    demand_count = len(network.demand_ids)
    hospital_count = len(network.hospital_ids)
    population = network.demand_population
    older_population = network.demand_older_population
    total_population = float(population.sum())
    total_older_population = float(older_population.sum())
    baseline_finite = np.isfinite(baseline.total_time)
    baseline_timely = np.stack(
        [baseline.total_time <= threshold for threshold in THRESHOLDS]
    )

    baseline_assigned = baseline.assigned_hospital_index
    if baseline_assigned is None:
        raise RuntimeError("Baseline hospital assignment was not returned")
    baseline_assigned_valid = baseline_assigned >= 0
    baseline_catchment = np.bincount(
        baseline_assigned[baseline_assigned_valid],
        weights=population[baseline_assigned_valid],
        minlength=hospital_count,
    )
    baseline_older_catchment = np.bincount(
        baseline_assigned[baseline_assigned_valid],
        weights=older_population[baseline_assigned_valid],
        minlength=hospital_count,
    )

    time_path = args.output_dir / ".total_times_working.float32"
    all_times = np.memmap(
        time_path,
        mode="w+",
        shape=(severity_count, replicate_count, demand_count),
        dtype=np.float32,
    )
    hospital_catchment = np.zeros(
        (severity_count, replicate_count, hospital_count), dtype=np.float64
    )
    hospital_older_catchment = np.zeros_like(hospital_catchment)
    coverage = np.zeros(
        (severity_count, replicate_count, len(THRESHOLDS)), dtype=np.float64
    )
    coverage_older = np.zeros_like(coverage)
    loss = np.zeros_like(coverage)
    loss_older = np.zeros_like(coverage)
    newly_disconnected = np.zeros((severity_count, replicate_count), dtype=np.float64)
    newly_disconnected_older = np.zeros_like(newly_disconnected)
    finite_population = np.zeros_like(newly_disconnected)
    realized_length_share = np.zeros_like(newly_disconnected)
    failed_section_count = np.zeros(
        (severity_count, replicate_count), dtype=np.int32
    )
    routing_seconds = np.zeros_like(newly_disconnected)
    timely30_counts = np.zeros((severity_count, demand_count), dtype=np.uint16)
    checkpoint_probabilities: dict[int, np.ndarray] = {}
    checkpoint_hospital_means: dict[int, np.ndarray] = {}
    first_replicate_failed = np.zeros(
        (severity_count, network.road_section_count), dtype=bool
    )
    correctness = {
        "nested_failure_sets": True,
        "travel_time_monotone_after_removal": True,
        "same_seed_reproducible": True,
    }
    checkpoints = [
        checkpoint
        for checkpoint in CHECKPOINT_CANDIDATES
        if checkpoint <= replicate_count
    ]
    if replicate_count not in checkpoints:
        checkpoints.append(replicate_count)
    checkpoints = sorted(set(checkpoints))

    simulation_started = perf_counter()
    for replicate_offset in range(replicate_count):
        replicate = replicate_offset + 1
        rng = np.random.default_rng(
            np.random.SeedSequence([args.base_seed, replicate])
        )
        uniform_score = rng.random(network.road_section_count)
        previous_failed = np.zeros(network.road_section_count, dtype=bool)
        previous_time = baseline.total_time
        for severity_index, target in enumerate(TARGETS):
            failed = uniform_score < probabilities[severity_index]
            correctness["nested_failure_sets"] &= bool(
                np.all(failed[previous_failed])
            )
            state = network.route(failed, assign_hospitals=True)
            finite = np.isfinite(state.total_time)
            finite_both = np.isfinite(previous_time) & finite
            no_shorter = np.all(
                state.total_time[finite_both] + 1e-10
                >= previous_time[finite_both]
            )
            no_reconnection = not np.any(~np.isfinite(previous_time) & finite)
            correctness["travel_time_monotone_after_removal"] &= bool(
                no_shorter and no_reconnection
            )

            all_times[severity_index, replicate_offset] = state.total_time.astype(
                np.float32
            )
            timely = np.stack(
                [state.total_time <= threshold for threshold in THRESHOLDS]
            )
            timely30_counts[severity_index] += timely[1]
            for threshold_index in range(len(THRESHOLDS)):
                coverage[severity_index, replicate_offset, threshold_index] = (
                    population[timely[threshold_index]].sum()
                )
                coverage_older[
                    severity_index, replicate_offset, threshold_index
                ] = older_population[timely[threshold_index]].sum()
                lost = baseline_timely[threshold_index] & ~timely[threshold_index]
                loss[severity_index, replicate_offset, threshold_index] = (
                    population[lost].sum()
                )
                loss_older[
                    severity_index, replicate_offset, threshold_index
                ] = older_population[lost].sum()
            disrupted_disconnection = baseline_finite & ~finite
            newly_disconnected[severity_index, replicate_offset] = population[
                disrupted_disconnection
            ].sum()
            newly_disconnected_older[
                severity_index, replicate_offset
            ] = older_population[disrupted_disconnection].sum()
            finite_population[severity_index, replicate_offset] = population[
                finite
            ].sum()
            realized_length_share[severity_index, replicate_offset] = (
                lengths[failed].sum() / lengths.sum()
            )
            failed_section_count[severity_index, replicate_offset] = int(
                failed.sum()
            )
            routing_seconds[severity_index, replicate_offset] = state.routing_seconds

            assigned = state.assigned_hospital_index
            if assigned is None:
                raise RuntimeError("Hospital assignment was not returned")
            assigned_valid = assigned >= 0
            hospital_catchment[severity_index, replicate_offset] = np.bincount(
                assigned[assigned_valid],
                weights=population[assigned_valid],
                minlength=hospital_count,
            )
            hospital_older_catchment[
                severity_index, replicate_offset
            ] = np.bincount(
                assigned[assigned_valid],
                weights=older_population[assigned_valid],
                minlength=hospital_count,
            )
            if replicate == 1:
                first_replicate_failed[severity_index] = failed
            if replicate == 1 and severity_index == 0:
                repeated = network.route(failed, assign_hospitals=True)
                correctness["same_seed_reproducible"] &= bool(
                    np.array_equal(
                        state.total_time, repeated.total_time, equal_nan=True
                    )
                )
            previous_failed = failed
            previous_time = state.total_time

        if replicate in checkpoints:
            checkpoint_probabilities[replicate] = (
                timely30_counts.astype(np.float32) / replicate
            ).copy()
            checkpoint_hospital_means[replicate] = hospital_catchment[
                :, :replicate
            ].mean(axis=1)
            all_times.flush()
            print(f"Recorded convergence checkpoint {replicate}", flush=True)
        if replicate == 1 or replicate % 25 == 0 or replicate == replicate_count:
            elapsed = perf_counter() - simulation_started
            print(
                f"Completed {replicate}/{replicate_count} replicates "
                f"({severity_count * replicate} states) in {elapsed:.1f}s",
                flush=True,
            )

    simulation_seconds = perf_counter() - simulation_started
    if not all(correctness.values()):
        raise RuntimeError(f"Formal experiment correctness check failed: {correctness}")

    metric_rows: list[dict[str, float | int | str]] = []
    for severity_index, target in enumerate(TARGETS):
        for replicate_offset in range(replicate_count):
            row: dict[str, float | int | str] = {
                "Random Failure Model": RANDOM_FAILURE_MODEL,
                "Base Seed": args.base_seed,
                "Simulation Replicate": replicate_offset + 1,
                "Expected Failed Road Length Share": float(target),
                "Failure Intensity per Metre": float(intensities[severity_index]),
                "Realized Failed Road Length Share": float(
                    realized_length_share[severity_index, replicate_offset]
                ),
                "Failed Road Sections": int(
                    failed_section_count[severity_index, replicate_offset]
                ),
                "Finite Population": float(
                    finite_population[severity_index, replicate_offset]
                ),
                "Population Newly Disconnected": float(
                    newly_disconnected[severity_index, replicate_offset]
                ),
                "Older Population Newly Disconnected": float(
                    newly_disconnected_older[severity_index, replicate_offset]
                ),
                "Routing Seconds": float(
                    routing_seconds[severity_index, replicate_offset]
                ),
            }
            for threshold_index, threshold in enumerate(THRESHOLDS):
                row[f"Population within {int(threshold)} Minutes"] = float(
                    coverage[severity_index, replicate_offset, threshold_index]
                )
                row[
                    f"Population Losing Baseline {int(threshold)}-Minute Access"
                ] = float(
                    loss[severity_index, replicate_offset, threshold_index]
                )
                row[f"Older Population within {int(threshold)} Minutes"] = float(
                    coverage_older[
                        severity_index, replicate_offset, threshold_index
                    ]
                )
                row[
                    f"Older Population Losing Baseline {int(threshold)}-Minute Access"
                ] = float(
                    loss_older[
                        severity_index, replicate_offset, threshold_index
                    ]
                )
            metric_rows.append(row)
    metrics = pd.DataFrame(metric_rows)
    metrics.to_parquet(args.output_dir / "replicate_metrics.parquet", index=False)

    mesh_dimension = pd.read_parquet(
        PROCESSED / "kumamoto_population_mesh_network_access_preprocessed.parquet",
        columns=["Mesh Code", "Analysis Unit ID", "Demand Node ID", "Total Population"],
    )
    older_dimension = pd.read_parquet(
        PROCESSED / "kumamoto_population_group_network_access_preprocessed.parquet",
        columns=[
            "Disclosure Group Code",
            "Analysis Unit ID",
            "Demand Node ID",
            "Population Age 65+",
            "Population Age 75+",
            "Population Age 85+",
        ],
    )
    if not np.array_equal(
        mesh_dimension["Demand Node ID"].astype("string").fillna("").astype(str),
        network.demand_ids[:mesh_count],
    ):
        raise RuntimeError("Population mesh order changed during output assembly")
    if not np.array_equal(
        older_dimension["Demand Node ID"].astype("string").fillna("").astype(str),
        network.demand_ids[mesh_count:],
    ):
        raise RuntimeError("Older-population group order changed during output assembly")

    grid_frames: list[pd.DataFrame] = []
    older_frames: list[pd.DataFrame] = []
    for severity_index, target in enumerate(TARGETS):
        grid_result = reliability_arrays(
            all_times[severity_index, :, :mesh_count],
            baseline.total_time[:mesh_count],
        )
        grid = mesh_dimension.copy()
        grid["Random Failure Model"] = RANDOM_FAILURE_MODEL
        grid["Expected Failed Road Length Share"] = float(target)
        grid["Simulation Replicates"] = replicate_count
        grid["Finite Access Probability"] = grid_result["finite_probability"]
        for threshold_index, threshold in enumerate(THRESHOLDS):
            grid[f"Timely Access Probability {int(threshold)} Minutes"] = (
                grid_result["timely_probability"][threshold_index]
            )
            grid[f"Grid Access Loss Probability {int(threshold)} Minutes"] = (
                grid_result["loss_probability"][threshold_index]
            )
        grid["P90 Emergency Access Time"] = grid_result["p90"]
        grid["P90 Unreachable"] = grid_result["p90_unreachable"]
        grid_frames.append(grid)

        older_result = reliability_arrays(
            all_times[severity_index, :, mesh_count:],
            baseline.total_time[mesh_count:],
        )
        older = older_dimension.copy()
        older["Random Failure Model"] = RANDOM_FAILURE_MODEL
        older["Expected Failed Road Length Share"] = float(target)
        older["Simulation Replicates"] = replicate_count
        older["Finite Access Probability"] = older_result["finite_probability"]
        for threshold_index, threshold in enumerate(THRESHOLDS):
            older[f"Timely Access Probability {int(threshold)} Minutes"] = (
                older_result["timely_probability"][threshold_index]
            )
            older[f"Grid Access Loss Probability {int(threshold)} Minutes"] = (
                older_result["loss_probability"][threshold_index]
            )
        older["P90 Emergency Access Time"] = older_result["p90"]
        older["P90 Unreachable"] = older_result["p90_unreachable"]
        older_frames.append(older)
        print(f"Aggregated demand reliability for target {100 * target:g}%", flush=True)

    pd.concat(grid_frames, ignore_index=True).to_parquet(
        args.output_dir / "grid_reliability.parquet", index=False
    )
    pd.concat(older_frames, ignore_index=True).to_parquet(
        args.output_dir / "older_population_reliability.parquet", index=False
    )

    hospital_dimension = pd.read_parquet(
        PROCESSED / "kumamoto_hospital_network_access_preprocessed.parquet",
        columns=[
            "Hospital Node ID",
            "Facility Name",
            "Emergency Designation",
            "Disaster Base Designation",
            "Hospital Role Weight",
            "Hospital Capacity Weight",
            "Eligible Emergency Hospital",
        ],
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
    for severity_index, target in enumerate(TARGETS):
        catchment = hospital_catchment[severity_index]
        older_catchment = hospital_older_catchment[severity_index]
        frame = hospital_dimension.copy()
        frame["Random Failure Model"] = RANDOM_FAILURE_MODEL
        frame["Expected Failed Road Length Share"] = float(target)
        frame["Simulation Replicates"] = replicate_count
        frame["Baseline Hospital Catchment Population"] = baseline_catchment
        frame["Mean Hospital Catchment Population"] = catchment.mean(axis=0)
        frame["Hospital Demand Change"] = (
            frame["Mean Hospital Catchment Population"] - baseline_catchment
        )
        frame["Hospital Catchment Standard Deviation"] = catchment.std(
            axis=0, ddof=1
        )
        quantiles = np.quantile(catchment, [0.05, 0.50, 0.95], axis=0)
        frame["Hospital Catchment P05"] = quantiles[0]
        frame["Hospital Catchment P50"] = quantiles[1]
        frame["Hospital Catchment P95"] = quantiles[2]
        frame["Zero Catchment Frequency"] = (catchment == 0).mean(axis=0)
        frame["Population-Weighted Hospital Assignment Probability"] = (
            catchment.mean(axis=0) / total_population
        )
        frame["Baseline Older Hospital Catchment Population"] = (
            baseline_older_catchment
        )
        frame["Mean Older Hospital Catchment Population"] = older_catchment.mean(
            axis=0
        )
        frame["Older Hospital Demand Change"] = (
            frame["Mean Older Hospital Catchment Population"]
            - baseline_older_catchment
        )
        hospital_frames.append(frame)
    pd.concat(hospital_frames, ignore_index=True).to_parquet(
        args.output_dir / "hospital_service_reliability.parquet", index=False
    )

    realization = sections[
        [
            "Road Section ID",
            "Road Section Length (m)",
            "Route Name",
            "Road Category",
            "Emergency Route Membership",
            "Hazard Exposure Class",
        ]
    ].copy()
    for severity_index, target in enumerate(TARGETS):
        label = f"{100 * target:g}%"
        realization[f"Section Failure Probability {label}"] = probabilities[
            severity_index
        ]
        realization[f"Road Failure Indicator {label}"] = first_replicate_failed[
            severity_index
        ]
    realization.to_parquet(
        args.output_dir / "nested_failure_realization_replicate_001.parquet",
        index=False,
    )

    convergence_rows: list[dict[str, float | int | str | bool]] = []
    previous_checkpoint: int | None = None
    for checkpoint in checkpoints:
        for severity_index, target in enumerate(TARGETS):
            values = coverage[severity_index, :checkpoint, 1]
            summary = system_summary(values)
            row: dict[str, float | int | str | bool] = {
                "Simulation Replicate Checkpoint": checkpoint,
                "Expected Failed Road Length Share": float(target),
                "Mean Population within 30 Minutes": summary["Mean"],
                "Population Coverage Standard Error": summary["Standard Error"],
                "Population Coverage P05": summary["P05"],
                "Population Coverage P50": summary["P50"],
                "Population Coverage P95": summary["P95"],
            }
            if previous_checkpoint is None:
                row.update(
                    {
                        "Coverage Mean Change Share": np.nan,
                        "Grid Probability Mean Absolute Change": np.nan,
                        "Grid Probability P95 Absolute Change": np.nan,
                        "Hospital Catchment P95 Absolute Change": np.nan,
                        "Monte Carlo Convergence Status": "Reference checkpoint",
                    }
                )
            else:
                previous_values = coverage[
                    severity_index, :previous_checkpoint, 1
                ]
                coverage_change = abs(values.mean() - previous_values.mean()) / (
                    total_population
                )
                probability_change = np.abs(
                    checkpoint_probabilities[checkpoint][severity_index, :mesh_count]
                    - checkpoint_probabilities[previous_checkpoint][
                        severity_index, :mesh_count
                    ]
                )
                hospital_change = np.abs(
                    checkpoint_hospital_means[checkpoint][severity_index]
                    - checkpoint_hospital_means[previous_checkpoint][severity_index]
                )
                grid_p95 = float(np.quantile(probability_change, 0.95))
                hospital_p95 = float(np.quantile(hospital_change, 0.95))
                stable = bool(
                    coverage_change <= COVERAGE_MEAN_CHANGE_SHARE_MAXIMUM
                    and grid_p95
                    <= GRID_PROBABILITY_P95_ABSOLUTE_CHANGE_MAXIMUM
                    and hospital_p95 / total_population
                    <= HOSPITAL_CATCHMENT_P95_CHANGE_SHARE_MAXIMUM
                )
                row.update(
                    {
                        "Coverage Mean Change Share": float(coverage_change),
                        "Grid Probability Mean Absolute Change": float(
                            probability_change.mean()
                        ),
                        "Grid Probability P95 Absolute Change": grid_p95,
                        "Hospital Catchment P95 Absolute Change": hospital_p95,
                        "Monte Carlo Convergence Status": (
                            "Stable" if stable else "Not stable"
                        ),
                    }
                )
            convergence_rows.append(row)
        previous_checkpoint = checkpoint
    convergence = pd.DataFrame(convergence_rows)
    convergence.to_parquet(
        args.output_dir / "convergence_summary.parquet", index=False
    )

    calibration_rows: list[dict[str, float]] = []
    for severity_index, target in enumerate(TARGETS):
        calibration_rows.append(
            {
                "Expected Failed Road Length Share": float(target),
                "Failure Intensity per Metre": float(intensities[severity_index]),
                "Expected Failed Road Section Share": float(
                    probabilities[severity_index].mean()
                ),
                "Mean Realized Failed Road Length Share": float(
                    realized_length_share[severity_index].mean()
                ),
                "P05 Realized Failed Road Length Share": float(
                    np.quantile(realized_length_share[severity_index], 0.05)
                ),
                "P95 Realized Failed Road Length Share": float(
                    np.quantile(realized_length_share[severity_index], 0.95)
                ),
                "Mean Failed Road Sections": float(
                    failed_section_count[severity_index].mean()
                ),
            }
        )
    calibration = pd.DataFrame(calibration_rows)
    calibration.to_parquet(
        args.output_dir / "severity_calibration_summary.parquet", index=False
    )

    del all_times
    time_path.unlink(missing_ok=True)
    final_checkpoint = checkpoints[-1]
    final_convergence = convergence.loc[
        convergence["Simulation Replicate Checkpoint"] == final_checkpoint
    ]
    summary = {
        "status": "pass",
        "design": {
            "random_failure_model": RANDOM_FAILURE_MODEL,
            "base_seed": args.base_seed,
            "replicates_per_severity": replicate_count,
            "expected_failed_road_length_shares": TARGETS.tolist(),
            "network_states": int(replicate_count * severity_count),
            "paired_nested_draws": True,
        },
        "network": {
            "road_sections": network.road_section_count,
            "population_grids": mesh_count,
            "older_population_groups": older_count,
            "eligible_hospitals": hospital_count,
            "total_population": total_population,
            "population_age_65_plus": total_older_population,
            "graph_build_seconds": network.build_seconds,
        },
        "checks": correctness,
        "convergence_thresholds": {
            "coverage_mean_change_share_maximum": (
                COVERAGE_MEAN_CHANGE_SHARE_MAXIMUM
            ),
            "grid_probability_p95_absolute_change_maximum": (
                GRID_PROBABILITY_P95_ABSOLUTE_CHANGE_MAXIMUM
            ),
            "hospital_catchment_p95_change_share_maximum": (
                HOSPITAL_CATCHMENT_P95_CHANGE_SHARE_MAXIMUM
            ),
        },
        "final_checkpoint_status": final_convergence[
            [
                "Expected Failed Road Length Share",
                "Monte Carlo Convergence Status",
            ]
        ].to_dict(orient="records"),
        "runtime": {
            "simulation_seconds": simulation_seconds,
            "total_seconds": perf_counter() - overall_started,
            "mean_state_routing_seconds": float(routing_seconds.mean()),
        },
        "outputs": {
            "replicate_metrics": "replicate_metrics.parquet",
            "grid_reliability": "grid_reliability.parquet",
            "older_population_reliability": "older_population_reliability.parquet",
            "hospital_service_reliability": "hospital_service_reliability.parquet",
            "nested_failure_realization": "nested_failure_realization_replicate_001.parquet",
            "convergence_summary": "convergence_summary.parquet",
            "severity_calibration_summary": "severity_calibration_summary.parquet",
        },
    }
    (args.output_dir / "experiment_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
