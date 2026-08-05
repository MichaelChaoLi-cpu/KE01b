#!/usr/bin/env python3
"""Build AnaSOP Section 4 from confirmed readable variable decisions."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DECISIONS = ROOT / "data/exp/data-preprocessing/decisions.json"
ANASOP = ROOT / "docs/AnaSOP.md"
HEADING = "## 4. Variable Construction  /  Key Variables"


def classify(name: str) -> tuple[str, str, str]:
    lower = name.lower()
    construction = "Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation."
    analysis_exact = {
        "Road Edge ID": ("network identifier", "Unique identifier for a routable Standard Road edge and Monte Carlo failure unit.", "Assigned deterministically after same-level noding, one-metre endpoint snapping, and splitting every topological edge into pieces no longer than 100 m in EPSG:6670."),
        "Road Failure Unit ID": ("experimental unit", "Unique identifier for a routable road piece subject to one simulated available or failed state.", "Assigned one-to-one with each final Road Edge ID after deterministic splitting to a maximum length of 100 m."),
        "From Node ID": ("network topology", "Identifier of the first endpoint node of a routable edge.", "Constructed from the endpoint coordinate and Vertical Level after one-metre snapping."),
        "To Node ID": ("network topology", "Identifier of the second endpoint node of a routable edge.", "Constructed from the endpoint coordinate and Vertical Level after one-metre snapping."),
        "Network Component ID": ("network topology", "Identifier of the connected Standard Road subnetwork containing the edge or node.", "Computed by union-find over grade-aware edge endpoints; disconnected island components are retained."),
        "Road Length (m)": ("network impedance", "Projected length of the routable edge in metres.", "Calculated in JGD2011 / Japan Plane Rectangular CS II (EPSG:6670)."),
        "Assumed Speed (km/h)": ("network impedance", "Scenario-neutral assumed ambulance travel speed for an edge in kilometres per hour.", "Uses category speeds of 80, 50, 40, 30, and 20 km/h for expressway, national, prefectural, municipal, and other roads, capped by width at 20, 30, 50, 60, or 80 km/h; sensitivity multipliers are 0.8, 1.0, and 1.2."),
        "Baseline Edge Travel Time (min)": ("network impedance", "Baseline traversal time of an edge in minutes.", r"Constructed as \(60 L_e / (1000 v_e)\), where \(L_e\) is Road Length (m) and \(v_e\) is Assumed Speed (km/h)."),
        "Hazard Exposure Class": ("disruption risk", "Highest landslide warning-zone class intersected by a road edge.", "Coded Special Warning Zone, Warning Zone, or None from polygon intersection; it is scenario exposure rather than observed earthquake failure."),
        "Emergency Route Membership": ("network priority", "Emergency transport road class associated with a compatible route alignment.", "Assigned from the nearest emergency-route centreline within 30 m only when its Road Type matches the routable edge's Road Category; otherwise coded None."),
        "Road Available": ("scenario state", "Indicator that an edge is traversable in a specified network scenario.", "Initialized to one for baseline; disruption and restoration scenarios update the indicator during estimation."),
        "Network Analysis Eligible": ("sample definition", "Indicator that a valid Standard Road edge or node is retained for network analysis.", "Set to one for every valid Standard Road component; component IDs preserve disconnected-network status without deleting island demand."),
        "Analysis Unit ID": ("demand identifier", "Identifier of the population mesh or disclosure group represented by an access point.", "Copied from the confirmed mesh or disclosure-group identifier."),
        "Demand Node ID": ("network connector", "Identifier of the virtual road-network connector for a demand unit.", "Assigned when the population centroid is within 250 m of an eligible road edge."),
        "Dispatch Base Node ID": ("network connector", "Identifier of the virtual road-network connector for a candidate ambulance dispatch base.", "Assigned when a confirmed fire station, branch, or outpost is within 150 m of an eligible road edge."),
        "Hospital Node ID": ("network connector", "Identifier of the virtual road-network connector for an eligible emergency hospital.", "Assigned when the hospital is within 150 m of an eligible road edge."),
        "Network Snap Distance (m)": ("spatial linkage", "Euclidean distance in metres from the source point or centroid to its nearest eligible road edge.", "Calculated in EPSG:6670; missing values are not imputed and rejected records remain explicit."),
        "Operational Hospital Set": ("hospital supply", "Named hospital inclusion set used in an accessibility scenario.", "Baseline set contains hospitals meeting the confirmed emergency or disaster-base designation rule."),
        "Hospital Role Weight": ("hospital weight", "Weight applied to a hospital's emergency-care role in weighted sensitivity analyses.", "Initialized to 1.0 for the unweighted baseline; alternative role weights are estimated only in declared sensitivity specifications."),
        "Hospital Capacity Weight": ("hospital weight", "Nonnegative hospital capacity weight used in weighted accessibility analyses.", "Uses reported Bed Count without normalization during preprocessing; missing bed counts remain missing."),
        "Disruption Scenario": ("scenario identifier", "Identifier of the baseline, Low, Central, High, or restoration network state.", "Assigned during scenario estimation from Road Available configurations."),
        "Timely Access Threshold (min)": ("accessibility threshold", "Maximum total emergency access time defining timely service, in minutes.", "Evaluated at the prespecified 15, 30, and 45 minute thresholds."),
        "Dispatch Travel Time": ("accessibility outcome", "Shortest network travel time from an available dispatch base to a demand unit.", "Calculated on the scenario-specific road graph, including connector offsets."),
        "Hospital Transport Time": ("accessibility outcome", "Shortest network travel time from the demand unit to an operational eligible hospital.", "Calculated on the same scenario-specific road graph after ambulance arrival."),
        "Total Emergency Access Time": ("primary outcome", "Two-stage emergency travel time from dispatch base through the demand unit to the assigned hospital.", "Constructed as Dispatch Travel Time plus Hospital Transport Time."),
        "Access Time Increase": ("accessibility outcome", "Increase in total emergency access time relative to baseline.", "Constructed as scenario Total Emergency Access Time minus baseline Total Emergency Access Time for the same analysis unit."),
        "Timely Access Status": ("primary outcome", "Indicator that Total Emergency Access Time does not exceed the selected threshold.", "Coded separately for each Disruption Scenario and Timely Access Threshold (min)."),
        "Assigned Hospital": ("hospital allocation", "Hospital minimizing the feasible second-stage transport objective for an analysis unit.", "Selected from the Operational Hospital Set under the scenario-specific road graph."),
        "Alternative Hospital Count": ("network redundancy", "Number of additional operational hospitals reachable within the specified threshold.", "Counted after excluding Assigned Hospital under the same scenario and threshold."),
        "Hospital Catchment Population": ("hospital demand", "Population assigned to a hospital under a specified scenario.", "Sum of Total Population over analysis units for which that hospital is Assigned Hospital."),
        "Hospital Demand Change": ("hospital demand", "Change in assigned hospital catchment population relative to baseline.", "Scenario Hospital Catchment Population minus baseline Hospital Catchment Population."),
        "Population Losing Timely Access": ("primary outcome", "Population timely in baseline but not timely in the disruption scenario.", "Sum of Total Population over units whose Timely Access Status changes from one to zero."),
        "Older Population Losing Timely Access": ("equity outcome", "Population age 65 or older timely in baseline but not timely in the disruption scenario.", "Computed at disclosure-group level without duplicating or imputing older-population counts to meshes."),
        "Failure Rate": ("experimental treatment", "Target share of Road Failure Unit ID values set unavailable in a Monte Carlo network state.", "Prespecified at 0.05, 0.10, and 0.20; the three levels are nested within Simulation Replicate."),
        "Simulation Replicate": ("simulation identifier", "Integer identifying one reproducible Monte Carlo randomization draw.", "Assigned from 1 to the executed replicate count with a recorded deterministic random seed."),
        "Road Failure Indicator": ("experimental treatment", "Indicator that a Road Failure Unit ID is unavailable in a replicate and failure-rate state.", "Set from the nested random ordering for the uniform model or from the declared spatial-cluster assignment for the clustered model."),
        "Random Failure Model": ("simulation specification", "Named mechanism used to assign simultaneous road failures.", "Coded Uniform Random for the primary benchmark and Spatially Clustered for required sensitivity analysis."),
        "Timely Access Probability": ("primary reliability outcome", "Monte Carlo probability that a demand unit completes the fire-station-to-grid-to-hospital chain within a declared threshold.", "Mean of Timely Access Status across executed replicates within Failure Rate, Random Failure Model, demand unit, and threshold."),
        "P90 Emergency Access Time": ("reliability outcome", "Ninetieth percentile of Total Emergency Access Time across Monte Carlo replicates.", "Computed within Failure Rate, Random Failure Model, and demand unit; disconnected outcomes remain explicitly unreachable and are not converted to ordinary travel times."),
        "Hospital Assignment Probability": ("hospital reliability outcome", "Probability that an eligible hospital is the replicate-specific Assigned Hospital for a demand unit or represented population.", "Estimated as the assignment frequency across Monte Carlo replicates within Failure Rate and Random Failure Model."),
        "Road Failure Importance": ("primary road outcome", "Expected loss of population-weighted timely emergency access associated with failure rather than availability of one road-failure unit under a declared randomization distribution.", "Estimated from replicate outcomes conditional on Road Failure Indicator, with the comparison made within Failure Rate and Random Failure Model."),
        "Road Importance Standard Error": ("uncertainty diagnostic", "Standard error of Road Failure Importance.", "Calculated from the declared randomized conditional-effect estimator with effective failed and available replicate counts reported."),
        "Confidence Interval": ("uncertainty diagnostic", "Interval estimate for a Monte Carlo reliability or road-importance estimand.", "Reported at 95% using the estimator-specific standard error or a declared replicate bootstrap when analytic approximation is inadequate."),
        "Rank Stability": ("convergence diagnostic", "Stability of a road unit's importance rank across replicate checkpoints or failure models.", "Summarized from rank ranges, top-set overlap, and checkpoint-to-checkpoint rank changes."),
        "Monte Carlo Convergence Status": ("convergence diagnostic", "Indicator that prespecified access-estimate and road-rank stability conditions are satisfied.", "Evaluated at the declared replicate checkpoints and reported separately by Failure Rate and Random Failure Model."),
    }
    if name in analysis_exact:
        return analysis_exact[name]
    exact = {
        "Disaster Base Designation": (
            "hospital role",
            "Reported designation of a hospital as a disaster medical base.",
        ),
        "Emergency Designated": (
            "hospital role",
            "Indicator that the facility appears on the prefectural emergency-designated hospital list.",
        ),
        "Emergency Designation": (
            "hospital role",
            "Reported emergency-care designation assigned to the hospital.",
        ),
        "External Reference": (
            "source provenance",
            "Indicator that a listed facility is retained as an out-of-prefecture reference rather than Kumamoto supply.",
        ),
        "Match Status": (
            "record linkage",
            "Outcome category from reconciling the healthcare-plan hospital name to the MHLW hospital roster.",
        ),
        "Name Match Score": (
            "record linkage",
            "Normalized similarity score used to review hospital-name reconciliation.",
        ),
        "Medical Departments 1": (
            "clinical service scope",
            "First reported group of medical departments provided by the hospital.",
        ),
        "Medical Departments 2": (
            "clinical service scope",
            "Second reported group of medical departments provided by the hospital.",
        ),
        "Medical Departments 3": (
            "clinical service scope",
            "Third reported group of medical departments provided by the hospital.",
        ),
        "Municipality Label": (
            "administrative descriptor",
            "Published municipality label associated with the record.",
        ),
        "Service Status": (
            "service availability",
            "Reported operating or service-availability status of the facility.",
        ),
        "Suppressed Source Mesh Count": (
            "demand disclosure",
            "Number of source meshes combined because population values were disclosure-suppressed.",
        ),
    }
    if name in exact:
        role, definition = exact[name]
        return role, definition, construction
    if name == "Geometry":
        return "spatial index", "Point, line, or polygon geometry represented in JGD2011.", "Standardized to JGD2011 (EPSG:6668)."
    if "population" in lower or "household" in lower:
        return "demand", "Population or household count/share for the represented spatial unit.", construction
    if "bed" in lower:
        return "hospital capacity", "Reported hospital bed capacity for the stated bed category.", construction
    if "candidate dispatch base" in lower:
        return "ambulance supply", "Indicator equal to one for a fire station, branch, or outpost considered as a candidate ambulance dispatch base.", "Constructed from the confirmed fire-facility inclusion rule."
    if "fire" in lower or "jurisdiction" in lower:
        return "ambulance supply", "Fire-service facility, staffing, or jurisdiction attribute.", construction
    if "eligible emergency hospital" in lower:
        return "hospital supply", "Indicator equal to one for a hospital with emergency designation or core/regional disaster-base designation.", "Constructed from the confirmed emergency-hospital inclusion rule."
    if "hospital" in lower or "medical facility" in lower or "facility name" in lower:
        return "hospital supply", "Hospital or medical-facility identity, classification, or role attribute.", construction
    if "road" in lower or "route" in lower or "width" in lower or "toll" in lower or "vertical level" in lower:
        return "network", "Road-segment classification or network descriptor used for routing and corridor prioritization.", construction
    if "hazard" in lower or "warning zone" in lower:
        return "disruption risk", "Landslide warning-zone classification used for disruption scenarios.", construction
    if "closed" in lower or "consultation" in lower or "reception" in lower or "closure" in lower or "specialty" in lower:
        return "service availability", "Reported specialty, consultation, reception, or closure-schedule attribute.", construction
    if "date" in lower:
        return "temporal metadata", "Reference, registration, opening, designation, or source date.", "Parsed to a machine-readable date where the source format permits."
    if "code" in lower or lower.endswith(" id") or "identifier" in lower:
        return "identifier/classification", "Identifier or categorical code retained as a string or integer as appropriate.", construction
    if "latitude" in lower or "longitude" in lower:
        return "spatial index", "Reported geographic coordinate.", "Coerced to numeric and used to construct JGD2011 point geometry where applicable."
    if "name" in lower or "address" in lower or "website" in lower or "notes" in lower:
        return "descriptor", "Human-readable identity or descriptive attribute.", "Leading and trailing whitespace removed; missing values preserved."
    return "TBD", "TBD", construction


def main() -> None:
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["datasets"]
    variables: dict[str, str] = {}
    for dataset in decisions.values():
        for variable in dataset["variables"]:
            if variable["is_final_variable"] != "yes":
                continue
            name = variable["readable_name"]
            variables.setdefault(name, variable.get("full_name") or name)

    lines = [
        HEADING,
        "",
        "All names below are analysis-facing English names. Source-specific names and paths are retained only in the preprocessing decision record.",
        "",
        "| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |",
        "|---|---|---|---|---|---|",
    ]
    for name, full_name in sorted(variables.items(), key=lambda item: item[0].casefold()):
        role, definition, construction = classify(name)
        cells = [name, full_name, role, definition, construction, "yes"]
        lines.append("| " + " | ".join(cell.replace("|", "/") for cell in cells) + " |")
    section = "\n".join(lines) + "\n"

    text = ANASOP.read_text(encoding="utf-8") if ANASOP.exists() else "# AnaSOP\nAnalysis Standard Operating Procedure\n"
    pattern = re.compile(r"(?ms)^## 4\. Variable Construction  /  Key Variables\n.*?(?=^## |\Z)")
    if pattern.search(text):
        text = pattern.sub(section.rstrip() + "\n", text)
    else:
        text = text.rstrip() + "\n\n" + section
    ANASOP.write_text(text, encoding="utf-8")
    print(f"Updated AnaSOP Section 4 with {len(variables)} unique final readable variables")


if __name__ == "__main__":
    main()
