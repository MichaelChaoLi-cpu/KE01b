#!/usr/bin/env python3
"""Estimate leave-one-road-section-out emergency-access consequences.

The script implements AnaSOP Section 6.5. It first applies an exact zero-loss
screen: a section not used by either selected baseline shortest-path tree for
any demand unit timely within 45 minutes cannot increase that unit's travel
time when removed, because its complete selected baseline path remains
available. Every retained candidate is then removed individually and the full
dispatch-to-demand-to-hospital chain is rerouted.
"""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from scipy.sparse.csgraph import dijkstra

from monte_carlo_emergency_routing import (
    CompactEmergencyNetwork,
    build_compact_emergency_network,
)
from run_length_weighted_monte_carlo_full import calibrate_intensity


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUTPUT = ROOT / "data" / "exp" / "road_section_accessibility_consequence"
THRESHOLDS = np.array([15, 30, 45], dtype=np.int16)
SEVERITIES = np.array([0.01, 0.03, 0.05], dtype=np.float64)
CHECKPOINT_INTERVAL = 1_000

_WORKER_NETWORK: CompactEmergencyNetwork | None = None
_WORKER_BASELINE_TIMELY: np.ndarray | None = None
_WORKER_POPULATION: np.ndarray | None = None
_WORKER_BASELINE_DISPATCH: np.ndarray | None = None
_WORKER_BASELINE_HOSPITAL: np.ndarray | None = None
_WORKER_STAGE_FLAGS: np.ndarray | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument("--chunk-size", type=int, default=20)
    parser.add_argument(
        "--screen-only",
        action="store_true",
        help="Build the network and report the exact candidate set without rerouting.",
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=None,
        help="Optional diagnostic cap; capped runs never create the final result.",
    )
    return parser.parse_args()


def expected_failed_length_share(intensity: float, lengths: np.ndarray) -> float:
    probabilities = -np.expm1(-intensity * lengths)
    return float(np.dot(lengths, probabilities) / lengths.sum())


def selected_tree_pair_keys(
    predecessor: np.ndarray,
    starting_nodes: np.ndarray,
    node_count: int,
) -> np.ndarray:
    """Collect unique directed graph pairs in selected source-to-demand paths."""
    visited = np.zeros(node_count, dtype=bool)
    pairs: list[int] = []
    for starting_node in starting_nodes:
        node = int(starting_node)
        while node >= 0 and not visited[node]:
            previous = int(predecessor[node])
            if previous < 0:
                visited[node] = True
                break
            visited[node] = True
            pairs.append(previous * node_count + node)
            node = previous
    return np.unique(np.asarray(pairs, dtype=np.int64))


def exact_candidate_sections(
    network: CompactEmergencyNetwork,
    baseline_total_time: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    """Return a safe superset of sections capable of positive timely-access loss."""
    dispatch_distance, dispatch_predecessor, _ = dijkstra(
        network.graph,
        directed=True,
        indices=network.dispatch_source_indices,
        return_predecessors=True,
        min_only=True,
    )
    hospital_distance, hospital_predecessor, _ = dijkstra(
        network.graph,
        directed=True,
        indices=network.hospital_source_indices,
        return_predecessors=True,
        min_only=True,
    )
    valid_demand = network.demand_node_index >= 0
    timely45 = baseline_total_time <= 45
    active_nodes = network.demand_node_index[valid_demand & timely45]
    if not np.all(np.isfinite(dispatch_distance[active_nodes])):
        raise RuntimeError("A baseline-timely demand has nonfinite dispatch distance")
    if not np.all(np.isfinite(hospital_distance[active_nodes])):
        raise RuntimeError("A baseline-timely demand has nonfinite hospital distance")

    dispatch_pairs = selected_tree_pair_keys(
        dispatch_predecessor, active_nodes, network.node_count
    )
    hospital_pairs = selected_tree_pair_keys(
        hospital_predecessor, active_nodes, network.node_count
    )
    graph_from = np.repeat(
        np.arange(network.node_count, dtype=np.int64),
        np.diff(network.graph.indptr),
    )
    graph_pair_keys = graph_from * network.node_count + network.graph.indices
    if np.any(graph_pair_keys[1:] < graph_pair_keys[:-1]):
        raise RuntimeError("CSR graph pairs are not in sorted row-column order")
    group_stops = np.r_[network.arc_group_starts[1:], len(network.arc_road_section)]
    group_sizes = group_stops - network.arc_group_starts

    def sections_for_pairs(pairs: np.ndarray) -> np.ndarray:
        group_indices = np.searchsorted(graph_pair_keys, pairs)
        if np.any(group_indices >= len(graph_pair_keys)) or not np.array_equal(
            graph_pair_keys[group_indices], pairs
        ):
            raise RuntimeError("A selected predecessor pair is absent from the graph")
        sections: list[int] = []
        for group_index in group_indices:
            start = int(network.arc_group_starts[group_index])
            stop = int(group_stops[group_index])
            weights = network.arc_base_weight[start:stop]
            minimum_weight = float(network.graph.data[group_index])
            minimum_sections = np.unique(
                network.arc_road_section[start:stop][weights == minimum_weight]
            )
            # A single-section failure changes this graph pair only when every
            # minimum-weight candidate belongs to the same road section.
            if len(minimum_sections) == 1 and minimum_sections[0] >= 0:
                sections.append(int(minimum_sections[0]))
        return np.unique(np.asarray(sections, dtype=np.int32))

    dispatch_sections = sections_for_pairs(dispatch_pairs)
    hospital_sections = sections_for_pairs(hospital_pairs)
    candidate_sections = np.union1d(dispatch_sections, hospital_sections).astype(np.int32)
    stage_flags = np.zeros(network.road_section_count, dtype=np.uint8)
    stage_flags[dispatch_sections] |= 1
    stage_flags[hospital_sections] |= 2
    used_pairs = np.union1d(dispatch_pairs, hospital_pairs)
    diagnostics = {
        "baseline_demand_units_within_45_minutes": int(len(active_nodes)),
        "selected_dispatch_graph_pairs": int(len(dispatch_pairs)),
        "selected_hospital_graph_pairs": int(len(hospital_pairs)),
        "selected_union_graph_pairs": int(len(used_pairs)),
        "candidate_road_sections": int(len(candidate_sections)),
        "dispatch_only_candidate_sections": int(
            (stage_flags[candidate_sections] == 1).sum()
        ),
        "hospital_only_candidate_sections": int(
            (stage_flags[candidate_sections] == 2).sum()
        ),
        "both_stage_candidate_sections": int(
            (stage_flags[candidate_sections] == 3).sum()
        ),
        "exact_zero_loss_road_sections": int(
            network.road_section_count - len(candidate_sections)
        ),
    }
    return candidate_sections, stage_flags, diagnostics


def worker_chunk(
    section_indices: list[int],
) -> list[tuple[int, float, float, float, float]]:
    """Reroute a chunk of single-section failures in one forked worker."""
    if (
        _WORKER_NETWORK is None
        or _WORKER_BASELINE_TIMELY is None
        or _WORKER_POPULATION is None
        or _WORKER_BASELINE_DISPATCH is None
        or _WORKER_BASELINE_HOSPITAL is None
        or _WORKER_STAGE_FLAGS is None
    ):
        raise RuntimeError("Worker state is not initialized")
    failed = np.zeros(_WORKER_NETWORK.road_section_count, dtype=bool)
    rows: list[tuple[int, float, float, float, float]] = []
    for section_index in section_indices:
        failed[section_index] = True
        route_started = perf_counter()
        available_arc = _WORKER_NETWORK.arc_road_section < 0
        road_arc = ~available_arc
        available_arc[road_arc] = ~failed[
            _WORKER_NETWORK.arc_road_section[road_arc]
        ]
        candidate_weight = np.where(
            available_arc,
            _WORKER_NETWORK.arc_base_weight,
            np.inf,
        )
        _WORKER_NETWORK.graph.data[:] = np.minimum.reduceat(
            candidate_weight,
            _WORKER_NETWORK.arc_group_starts,
        )
        stage_flag = int(_WORKER_STAGE_FLAGS[section_index])
        if stage_flag == 3:
            stage_distance = dijkstra(
                _WORKER_NETWORK.graph,
                directed=True,
                indices=np.array(
                    [
                        _WORKER_NETWORK.dispatch_super_index,
                        _WORKER_NETWORK.hospital_super_index,
                    ],
                    dtype=np.int32,
                ),
                return_predecessors=False,
                min_only=False,
                limit=45.0,
            )
            dispatch_distance = stage_distance[0]
            hospital_distance = stage_distance[1]
            dispatch_time = np.full(
                len(_WORKER_NETWORK.demand_node_index), np.inf, dtype=np.float64
            )
            hospital_time = np.full(
                len(_WORKER_NETWORK.demand_node_index), np.inf, dtype=np.float64
            )
            valid = _WORKER_NETWORK.demand_node_index >= 0
            dispatch_time[valid] = dispatch_distance[
                _WORKER_NETWORK.demand_node_index[valid]
            ]
            hospital_time[valid] = hospital_distance[
                _WORKER_NETWORK.demand_node_index[valid]
            ]
        elif stage_flag == 1:
            dispatch_distance = dijkstra(
                _WORKER_NETWORK.graph,
                directed=True,
                indices=_WORKER_NETWORK.dispatch_super_index,
                return_predecessors=False,
                limit=45.0,
            )
            dispatch_time = np.full(
                len(_WORKER_NETWORK.demand_node_index), np.inf, dtype=np.float64
            )
            valid = _WORKER_NETWORK.demand_node_index >= 0
            dispatch_time[valid] = dispatch_distance[
                _WORKER_NETWORK.demand_node_index[valid]
            ]
            hospital_time = _WORKER_BASELINE_HOSPITAL
        else:
            dispatch_time = _WORKER_BASELINE_DISPATCH
        if stage_flag == 2:
            hospital_distance = dijkstra(
                _WORKER_NETWORK.graph,
                directed=True,
                indices=_WORKER_NETWORK.hospital_super_index,
                return_predecessors=False,
                limit=45.0,
            )
            hospital_time = np.full(
                len(_WORKER_NETWORK.demand_node_index), np.inf, dtype=np.float64
            )
            valid = _WORKER_NETWORK.demand_node_index >= 0
            hospital_time[valid] = hospital_distance[
                _WORKER_NETWORK.demand_node_index[valid]
            ]
            dispatch_time = _WORKER_BASELINE_DISPATCH
        total_time = dispatch_time + hospital_time
        routing_seconds = perf_counter() - route_started
        disrupted_timely = np.stack(
            [total_time <= threshold for threshold in THRESHOLDS]
        )
        losses = (
            (_WORKER_BASELINE_TIMELY & ~disrupted_timely)
            * _WORKER_POPULATION[None, :]
        ).sum(axis=1)
        rows.append(
            (
                int(section_index),
                float(losses[0]),
                float(losses[1]),
                float(losses[2]),
                float(routing_seconds),
            )
        )
        failed[section_index] = False
    return rows


def chunked(values: list[int], size: int) -> list[list[int]]:
    return [values[start : start + size] for start in range(0, len(values), size)]


def write_partial(path: Path, rows: list[tuple[int, float, float, float, float]]) -> None:
    frame = pd.DataFrame(
        rows,
        columns=[
            "Section Index",
            "Potential Access Loss 15 Minutes",
            "Potential Access Loss 30 Minutes",
            "Potential Access Loss 45 Minutes",
            "Routing Seconds",
        ],
    ).sort_values("Section Index")
    frame.to_parquet(path, index=False)


def main() -> None:
    global _WORKER_NETWORK, _WORKER_BASELINE_TIMELY, _WORKER_POPULATION
    global _WORKER_BASELINE_DISPATCH, _WORKER_BASELINE_HOSPITAL, _WORKER_STAGE_FLAGS

    args = parse_args()
    if not args.output_dir.is_absolute():
        args.output_dir = ROOT / args.output_dir
    if args.workers < 1 or args.chunk_size < 1:
        raise ValueError("workers and chunk-size must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = perf_counter()

    network = build_compact_emergency_network(
        PROCESSED, include_population_groups=False
    )
    baseline = network.route(assign_hospitals=False)
    baseline_timely = np.stack(
        [baseline.total_time <= threshold for threshold in THRESHOLDS]
    )
    baseline_coverage = baseline_timely @ network.demand_population
    candidates, stage_flags, screening = exact_candidate_sections(
        network, baseline.total_time
    )
    screening.update(
        {
            "road_sections": network.road_section_count,
            "demand_units": int(len(network.demand_ids)),
            "baseline_population_within_15_minutes": float(baseline_coverage[0]),
            "baseline_population_within_30_minutes": float(baseline_coverage[1]),
            "baseline_population_within_45_minutes": float(baseline_coverage[2]),
            "network_build_seconds": float(network.build_seconds),
            "baseline_routing_seconds": float(baseline.routing_seconds),
        }
    )
    screening_path = args.output_dir / "screening_summary.json"
    screening_path.write_text(
        json.dumps(screening, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    np.save(args.output_dir / "candidate_section_indices.npy", candidates)
    np.save(args.output_dir / "candidate_stage_flags.npy", stage_flags)
    print(json.dumps(screening, indent=2), flush=True)
    if args.screen_only:
        print(f"Saved: {screening_path.relative_to(ROOT)}", flush=True)
        return

    selected_candidates = candidates.tolist()
    diagnostic_cap = args.max_candidates
    if diagnostic_cap is not None:
        if diagnostic_cap < 1:
            raise ValueError("max-candidates must be positive")
        selected_candidates = selected_candidates[:diagnostic_cap]

    partial_path = args.output_dir / "road_section_accessibility_consequence_partial.parquet"
    completed_rows: list[tuple[int, float, float, float, float]] = []
    if partial_path.exists():
        existing = pd.read_parquet(partial_path)
        completed_rows = list(
            existing[
                [
                    "Section Index",
                    "Potential Access Loss 15 Minutes",
                    "Potential Access Loss 30 Minutes",
                    "Potential Access Loss 45 Minutes",
                    "Routing Seconds",
                ]
            ].itertuples(index=False, name=None)
        )
        selected_candidate_set = set(selected_candidates)
        completed_rows = [
            row for row in completed_rows if int(row[0]) in selected_candidate_set
        ]
    completed_indices = {int(row[0]) for row in completed_rows}
    remaining = [
        section_index
        for section_index in selected_candidates
        if section_index not in completed_indices
    ]
    print(
        f"Rerouting {len(remaining):,} remaining of "
        f"{len(selected_candidates):,} selected candidate sections with "
        f"{args.workers} worker(s)",
        flush=True,
    )

    _WORKER_NETWORK = network
    _WORKER_BASELINE_TIMELY = baseline_timely
    _WORKER_POPULATION = network.demand_population
    _WORKER_BASELINE_DISPATCH = baseline.dispatch_time
    _WORKER_BASELINE_HOSPITAL = baseline.hospital_time
    _WORKER_STAGE_FLAGS = stage_flags
    tasks = chunked(remaining, args.chunk_size)
    processed_since_checkpoint = 0
    last_checkpoint_count = len(completed_rows)

    if args.workers == 1:
        iterator = map(worker_chunk, tasks)
        pool = None
    else:
        context = mp.get_context("fork")
        pool = context.Pool(processes=args.workers)
        iterator = pool.imap_unordered(worker_chunk, tasks, chunksize=1)
    try:
        for rows in iterator:
            completed_rows.extend(rows)
            processed_since_checkpoint += len(rows)
            if (
                len(completed_rows) - last_checkpoint_count >= CHECKPOINT_INTERVAL
                or processed_since_checkpoint >= len(remaining)
            ):
                write_partial(partial_path, completed_rows)
                last_checkpoint_count = len(completed_rows)
                elapsed = perf_counter() - started
                print(
                    f"Completed {len(completed_rows):,}/{len(selected_candidates):,} "
                    f"candidate sections in {elapsed:.1f}s",
                    flush=True,
                )
    finally:
        if pool is not None:
            pool.close()
            pool.join()

    if diagnostic_cap is not None and diagnostic_cap < len(candidates):
        print(
            "Diagnostic cap reached; final all-section result was not created.",
            flush=True,
        )
        return

    completed = pd.DataFrame(
        completed_rows,
        columns=[
            "Section Index",
            "Potential Access Loss 15 Minutes",
            "Potential Access Loss 30 Minutes",
            "Potential Access Loss 45 Minutes",
            "Routing Seconds",
        ],
    ).drop_duplicates("Section Index", keep="last")
    if len(completed) != len(candidates):
        raise RuntimeError(
            f"Expected {len(candidates)} completed candidate sections; found {len(completed)}"
        )

    sections = pd.read_parquet(
        PROCESSED / "kumamoto_road_sections_preprocessed.parquet"
    )
    sections["Road Section ID"] = sections["Road Section ID"].astype(str)
    sections = sections.set_index("Road Section ID").loc[
        network.road_section_ids
    ].reset_index()
    result = sections[
        [
            "Road Section ID",
            "Road Section Length (m)",
            "Road Edge Count",
            "Route Name",
            "Road Category",
            "Emergency Route Membership",
            "Hazard Exposure Class",
            "Network Component ID",
        ]
    ].copy()
    result.insert(1, "Section Index", np.arange(len(result), dtype=np.int32))
    result["Candidate for Rerouting"] = False
    result.loc[candidates, "Candidate for Rerouting"] = True
    completed_indexed = completed.set_index("Section Index")
    for column in (
        "Potential Access Loss 15 Minutes",
        "Potential Access Loss 30 Minutes",
        "Potential Access Loss 45 Minutes",
        "Routing Seconds",
    ):
        result[column] = 0.0
        result.loc[completed_indexed.index, column] = completed_indexed[column]

    lengths = result["Road Section Length (m)"].to_numpy(dtype=np.float64)
    intensities = np.array(
        [calibrate_intensity(target, lengths) for target in SEVERITIES]
    )
    probabilities = np.vstack(
        [-np.expm1(-intensity * lengths) for intensity in intensities]
    )
    potential30 = result["Potential Access Loss 30 Minutes"].to_numpy(dtype=float)
    for severity, intensity, probability in zip(
        SEVERITIES, intensities, probabilities, strict=True
    ):
        label = f"{100 * severity:g} Percent"
        result[f"Failure Intensity per Metre {label}"] = float(intensity)
        result[f"Section Failure Probability {label}"] = probability
        result[f"Expected Risk 30 Minutes {label}"] = probability * potential30

    loss_columns = [
        "Potential Access Loss 15 Minutes",
        "Potential Access Loss 30 Minutes",
        "Potential Access Loss 45 Minutes",
    ]
    if (result[loss_columns] < 0).any().any():
        raise RuntimeError("Potential access loss must be nonnegative")
    final_path = args.output_dir / "road_section_accessibility_consequence.parquet"
    result.to_parquet(final_path, index=False)

    summary = {
        **screening,
        "workers": int(args.workers),
        "candidate_sections_rerouted": int(len(candidates)),
        "positive_loss_sections": {
            str(threshold): int(
                (result[f"Potential Access Loss {threshold} Minutes"] > 0).sum()
            )
            for threshold in THRESHOLDS
        },
        "maximum_potential_access_loss": {
            str(threshold): float(
                result[f"Potential Access Loss {threshold} Minutes"].max()
            )
            for threshold in THRESHOLDS
        },
        "calibrated_failure_intensity_per_metre": {
            f"{100 * severity:g}%": float(intensity)
            for severity, intensity in zip(SEVERITIES, intensities, strict=True)
        },
        "expected_failed_length_share_check": {
            f"{100 * severity:g}%": expected_failed_length_share(intensity, lengths)
            for severity, intensity in zip(SEVERITIES, intensities, strict=True)
        },
        "total_elapsed_seconds": float(perf_counter() - started),
    }
    summary_path = args.output_dir / "experiment_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved: {final_path.relative_to(ROOT)}", flush=True)
    print(f"Saved: {summary_path.relative_to(ROOT)}", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
