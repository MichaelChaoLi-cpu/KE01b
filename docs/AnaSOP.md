# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Central Research Question

- Research question: Under length-dependent failures of continuous junction-to-junction road sections, how reliably can each population grid complete the fire-station-to-grid-to-hospital emergency chain, and where are the road sections whose loss most reduces timely emergency access across Kumamoto Prefecture?
- Why it matters: Emergency managers need evidence on both where ambulance access is fragile and which road sections should receive continuity protection, inspection, or restoration priority when many road failures can occur simultaneously.
- Data support currently visible: The evidence represents population demand, older populations, candidate fire-station dispatch bases, eligible emergency hospitals, 343,844 junction-to-junction road sections, road and route attributes, administrative geography, and hazard information. The 100-replicate calibration produced an ordered severity response at 0.5%, 1%, 2%, 3%, 5%, and 10% expected failed road length.
- Key readable variables or data scope: Geometry, Total Population, Population Age 65+, Candidate Dispatch Base, Eligible Emergency Hospital, Road Section ID, Road Section Length (m), Expected Failed Road Length Share, Section Failure Probability, Total Emergency Access Time, Grid Access Loss Probability, Road-Section Potential Access Loss, and Road-Section Expected Risk.
- What would verify it: Repeated full-network routing should produce reproducible and non-increasing access reliability as expected failed road length rises, while network-wide road-loss maps should identify spatially coherent high-consequence sections without relying on an arbitrary Top-20 cutoff.
- What would falsify or weaken it: The study would weaken if baseline topology or connectors are unreliable, the full emergency chain cannot be computed for most represented population, Monte Carlo accessibility estimates fail to converge, or road-section results are dominated by implausibly long sections or unverified routing assumptions.
- Required next feasibility check: Complete 1,000 paired replicates for the confirmed 1%, 3%, and 5% main scenarios and the 10% stress scenario, then verify convergence and inspect the full distribution of section lengths and failure probabilities.

### Supporting Research Questions

The four supporting questions deepen the central applied question through grid reliability, population distribution, hospital service stability, and network-wide road consequences.

#### Grid-Level Emergency Access Reliability

- Role relative to central point: establish the primary reliability outcome.
- Research question: How do 1%, 3%, and 5% expected failed road length change each grid's probability of completing the emergency chain within 15, 30, and 45 minutes and its upper-tail emergency travel time, and how much further deterioration occurs in the 10% stress scenario?
- Why it matters: Expected time alone can hide rare but severe disconnections; grid-level probabilities and P90 time reveal both routine degradation and reliability risk.
- Data support currently visible: Population-grid connectors, dispatch-base connectors, hospital connectors, road travel times, and network topology support repeated multi-source shortest-path estimation.
- Key readable variables or data scope: Analysis Unit ID, Demand Node ID, Dispatch Base Node ID, Hospital Node ID, Expected Failed Road Length Share, Simulation Replicate, Total Emergency Access Time, Timely Access Probability, Grid Access Loss Probability, and P90 Emergency Access Time.
- What would verify it: Access probability should be bounded, reproducible, and non-increasing across nested failure levels except for negligible Monte Carlo variation.
- What would falsify or weaken it: Results would weaken if many grids lack baseline network access or if upper-tail estimates remain unstable at 1,000 replicates.
- Required next feasibility check: Verify that failure of a Road Section ID closes all of its internal routing fragments and attached connectors, and that paired uniform scores preserve nested section failures across severity levels.

#### Population, Older-Population, and Municipal Reliability

- Role relative to central point: assess distributional and geographic heterogeneity.
- Research question: Which population groups and municipalities experience the largest expected and upper-tail losses of timely emergency access under random road failure?
- Why it matters: A road system can appear robust in aggregate while leaving older populations or peripheral municipalities with high disconnection risk.
- Data support currently visible: Total and older-population measures and municipal geography support population-weighted aggregation on their valid spatial supports.
- Key readable variables or data scope: Total Population, Population Age 65+, Population Age 75+, Population Age 85+, Municipality Name, Expected Failed Road Length Share, Timely Access Probability, Population Losing Timely Access, Older Population Losing Timely Access, and Population Newly Disconnected.
- What would verify it: Monte Carlo intervals should identify persistent differences across population supports and municipalities rather than isolated replicate-specific extremes.
- What would falsify or weaken it: Claims would weaken if disclosure aggregation prevents defensible older-population localization or municipal ranks are highly unstable.
- Required next feasibility check: Retain separate spatial support for older-population estimates and measure municipal rank stability across replicate counts.

#### Hospital Service Reliability

- Role relative to central point: identify the hospital-side service mechanism.
- Research question: How do random road failures change the probability that each eligible hospital remains the nearest feasible destination and the distribution of its population catchment?
- Why it matters: Hospital emergency value depends on road-supported reachability and substitution, not only on beds or formal designation.
- Data support currently visible: Eligible hospital locations, roles, capacity descriptors, population demand, and labelled multi-source routing support replicate-specific hospital assignment and catchment estimation.
- Key readable variables or data scope: Hospital Name, Eligible Emergency Hospital, Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability, Hospital Role Weight, Hospital Capacity Weight, Expected Failed Road Length Share, and Simulation Replicate.
- What would verify it: Hospital assignment probabilities and catchment intervals should be reproducible and identify facilities with persistently large or volatile service roles.
- What would falsify or weaken it: Interpretation would weaken if eligibility rules or missing capacity data reverse results or if nearest-hospital assignment is an inadequate proxy for actual emergency destination choice.
- Required next feasibility check: Keep unweighted eligible-hospital routing primary and treat role or capacity weighting as separately labelled sensitivity analysis.

#### Road-Section Consequences and Expected Risk

- Role relative to central point: translate network reliability into road-priority evidence.
- Research question: How much timely emergency access could be lost if each junction-to-junction road section failed, and how does its length-dependent failure probability translate that consequence into expected risk under the main severity scenarios?
- Why it matters: Grid reliability maps locate vulnerable demand, while full-network road maps show where maintaining continuity can prevent the greatest accessibility loss without imposing an arbitrary ranking cutoff.
- Data support currently visible: Junction-defined road geometry, section length, route attributes, baseline travel times, and repeated full-network routing support both single-section potential-loss calculations and probability-weighted expected-risk maps.
- Key readable variables or data scope: Road Section ID, Road Section Length (m), Route Name, Timely Access Threshold (min), Section Failure Probability, Road-Section Potential Access Loss, Road-Section Expected Risk, Total Population, and Population Age 65+.
- What would verify it: Road consequences should be nonnegative, spatially coherent, reproducible, and interpretable at all 343,844 sections, with expected risk changing consistently across the 1%, 3%, and 5% scenarios.
- What would falsify or weaken it: Road-priority interpretation would weaken if most estimated consequences are numerically indistinguishable from zero, if isolated values are driven by topology errors, or if results change materially under plausible travel-speed and hospital-set sensitivity specifications.
- Required next feasibility check: Compute leave-one-section-out potential loss for every eligible section and verify that the full-network color scale preserves both zero values and the upper tail.

### Scope of Analysis

- Topics: Random road-network failure, ambulance dispatch, patient transport, hospital reachability, population emergency-access reliability, hospital service stability, and road continuity priority.
- Spatial scope: Kumamoto Prefecture, with network connectors and any necessary cross-boundary links retained only when they affect feasible emergency paths.
- Operational chain: Candidate fire-station dispatch base to population grid, followed by population grid to the nearest feasible eligible emergency hospital.
- Units of analysis: Junction-to-junction road section, population grid, older-population disclosure group, candidate dispatch base, eligible emergency hospital, municipality, expected failed road-length level, and simulation replicate.
- Period: Cross-sectional network simulation using the confirmed source vintages; it is not an observed longitudinal disaster-response study.
- Experimental scope: Nested 1%, 3%, and 5% expected failed road-length levels with 1,000 target replicates per level; 10% is an extreme stress sensitivity scenario, while 0.5% remains a near-baseline calibration check. Section failure probability increases with section length.

### Study Design Declaration

- Research type: applied
- Study design: Applied Monte Carlo network-reliability and emergency-access simulation study.
- Primary estimand: Grid-level probability of timely completion of the two-stage emergency chain and the population-weighted potential accessibility loss and expected risk associated with every junction-to-junction road section.
- Interpretation limit: Results describe the specified random-failure models and routing assumptions. They do not reconstruct an observed earthquake, predict engineering failure probabilities, measure ambulance availability or on-scene delay, establish clinical capacity, or identify causal effects of an actual repair intervention.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

Research type: applied
Section focus: Empirical context, practical problem, and cautious interpretation limits.

### Research Gap

- Existing accessibility summaries can show where travel times are high under one assumed road state, but they do not quantify the probability distribution of emergency access across many simultaneous road-failure configurations.
- Fixed-path attribution can allocate dependence along one baseline route without testing the complete network after each failure draw. The practical gap is therefore a full-rerouting reliability framework that connects length-dependent road failures to grid access, population coverage, hospital service stability, and network-wide road consequences.
- Verified event-specific closure probabilities and ambulance-operation records are not currently available, so the study estimates scenario reliability under transparent random-failure models rather than earthquake-specific risk.

### Conceptual Framework

- Continuous road sections between true same-level junctions define the experimental exposure scale. A section's probability of containing at least one failure rises with its length, while one shared random score per section makes increasing severity states directly comparable within each replicate.
- Road availability determines the feasible graph. Two multi-source shortest-path calculations determine dispatch access from fire stations and hospital access to the nearest eligible hospital. Their sum defines the complete emergency travel time for each grid.
- Repeated routing transforms scenario-specific times into grid reliability, timely-access probabilities, upper-tail travel times, population coverage distributions, hospital assignment probabilities, and catchment uncertainty.
- Leave-one-section-out routing measures each section's potential accessibility consequence, and multiplication by its scenario-specific Section Failure Probability produces a probability-weighted expected-risk surface across the whole network.
- Scope boundary: Road-Section Potential Access Loss and Road-Section Expected Risk are model-based accessibility measures, not observed engineering failure probabilities, repair costs, asset values, or causal estimates from actual interventions.

### Problem Formulation

- Decision problem: Identify population grids and hospitals with fragile emergency access and map every junction-to-junction road section by the accessibility loss that its failure could cause.
- Experimental unit: Road Section ID, constructed as a maximal continuous road chain between true same-level junctions. Internal geometry fragments are retained only for routing and connectors; all fragments in one section share the same failure state.
- Randomization: Within replicate \(r\), one deterministic-seed uniform score is assigned to every Road Section ID. Section Failure Probability follows \(q_s(\lambda)=1-\exp(-\lambda L_s)\), where \(L_s\) is Road Section Length (m), and \(\lambda\) is calibrated so the expected failed road-length share equals 1%, 3%, 5%, or 10%. Shared scores guarantee nested failure states.
- Primary grid outcome: Timely Access Probability for completing the two-stage chain within 30 minutes. The 15- and 45-minute thresholds and P90 Emergency Access Time are complementary outcomes.
- Primary system outcome: Total Population retaining timely access in each replicate. Older-population measures use their valid disclosure-group support.
- Primary road outcome: Road-Section Potential Access Loss, defined as the decline in population-weighted timely access after removing one section from the otherwise available baseline network, and Road-Section Expected Risk, defined by weighting that consequence by Section Failure Probability.
- Interpretation limit: Single-section potential loss isolates direct network consequence but does not reproduce all interactions among simultaneous failures. Expected risk inherits the assumed length-dependent failure model, and the full-network maps support spatial prioritization rather than a definitive engineering repair order.

## 3. Data Overview

### Data Scope

- Data sources reviewed: 6
- Variables summarized: 196
- Distribution plots generated: 24
- Files skipped during briefing: 0
- Geospatial layers profiled separately: 12
- Geospatial features profiled: 1,249,722
- Geospatial attributes catalogued: 117

| Data source | Rows | Columns |
| --- | ---: | ---: |
| Data source 1 | 2102 | 12 |
| Data source 2 | 112 | 54 |
| Data source 3 | 7715 | 65 |
| Data source 4 | 250824 | 36 |
| Data source 5 | 36657 | 19 |
| Data source 6 | 62945 | 10 |

### Time-Series Candidates

No obvious time-series columns were detected.

### Data Limitations

- No skipped files were recorded by the briefing script.
- The FDMA CSV and prefectural hospital workbook use multi-row headers. Their
  automatically generated `Unnamed:*` labels and distribution plots are not
  analytical variables; preprocessing must rebuild the headers first.
- The P17 fire-facility layer is from 2012. The 2024 FDMA totals indicate that
  the point roster requires completeness validation before dispatch modelling.
- N13 provides road centerlines but no node-link topology. The five source
  meshes must be clipped to Kumamoto, planarized at valid intersections, and
  checked for disconnected components before routing.
- P04 emergency/disaster designations are from 2020. Hospital names and roles
  must be reconciled to the 2026 MHLW facility roster and the prefectural
  2024-2029 healthcare plan.
- The 2025 prefectural hospital workbook excludes Kumamoto City; the nationwide
  MHLW file is therefore the complete current hospital-location source.
- A33 is suitable for scenario construction and screening, not proof that a
  particular road segment failed in the earthquake.
- Treat this section as exploratory; final variable decisions belong to Section 4.
- AnaSOP intentionally avoids raw dataset names, source file paths, and original column names.

## 4. Variable Construction  /  Key Variables

All names below are analysis-facing English names. Source-specific names and paths are retained only in the preprocessing decision record.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Access Time Increase | Access Time Increase | accessibility outcome | Increase in total emergency access time relative to baseline. | Constructed as scenario Total Emergency Access Time minus baseline Total Emergency Access Time for the same analysis unit. | yes |
| Address | Address | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Aggregated Source Mesh Codes | Aggregated Source Mesh Codes | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Aggregation Destination Mesh Code | Aggregation Destination Mesh Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Alternative Hospital Count | Alternative Hospital Count | network redundancy | Number of additional operational hospitals reachable within the specified threshold. | Counted after excluding Assigned Hospital under the same scenario and threshold. | yes |
| Analysis Unit ID | Analysis Unit Identifier | demand identifier | Identifier of the population mesh or disclosure group represented by an access point. | Copied from the confirmed mesh or disclosure-group identifier. | yes |
| Assigned Hospital | Assigned Hospital | hospital allocation | Hospital minimizing the feasible second-stage transport objective for an analysis unit. | Selected from the Operational Hospital Set under the scenario-specific road graph. | yes |
| Assumed Speed (km/h) | Assumed Speed (km/h) | network impedance | Scenario-neutral assumed ambulance travel speed for an edge in kilometres per hour. | Uses category speeds of 80, 50, 40, 30, and 20 km/h for expressway, national, prefectural, municipal, and other roads, capped by width at 20, 30, 50, 60, or 80 km/h; sensitivity multipliers are 0.8, 1.0, and 1.2. | yes |
| Baseline Edge Travel Time (min) | Baseline Edge Travel Time (min) | network impedance | Baseline traversal time of an edge in minutes. | Constructed as \(60 L_e / (1000 v_e)\), where \(L_e\) is Road Length (m) and \(v_e\) is Assumed Speed (km/h). | yes |
| Baseline Section Travel Time (min) | Baseline Section Travel Time (min) | network impedance | Total baseline traversal time of a road section in minutes. | Constructed by summing Baseline Edge Travel Time (min) over all internal fragments assigned to Road Section ID. | yes |
| Bed Count | Bed Count | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Branch ID | Branch Identifier | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Candidate Dispatch Base | Candidate Dispatch Base | ambulance supply | Indicator equal to one for a fire station, branch, or outpost considered as a candidate ambulance dispatch base. | Constructed from the confirmed fire-facility inclusion rule. | yes |
| Closed on Holidays | Closed on Holidays | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Confidence Interval | Confidence Interval | uncertainty diagnostic | Interval estimate for a Monte Carlo reliability or road-importance estimand. | Reported at 95% using the estimator-specific standard error or a declared replicate bootstrap when analytic approximation is inadequate. | yes |
| Demand Node ID | Demand Node Identifier | network connector | Identifier of the virtual road-network connector for a demand unit. | Assigned when the population centroid is within 250 m of an eligible road edge. | yes |
| Designation Date | Designation Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Disaster Base Designation | Disaster Base Designation | hospital role | Reported designation of a hospital as a disaster medical base. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Disaster Base Designation Code | Disaster Base Designation Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Disclosure Group Code | Disclosure Group Code | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Disclosure Group Size | Disclosure Group Size | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Disclosure Status | Disclosure Status | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Dispatch Base Node ID | Dispatch Base Node Identifier | network connector | Identifier of the virtual road-network connector for a candidate ambulance dispatch base. | Assigned when a confirmed fire station, branch, or outpost is within 150 m of an eligible road edge. | yes |
| Dispatch Travel Time | Dispatch Travel Time | accessibility outcome | Shortest network travel time from an available dispatch base to a demand unit. | Calculated on the scenario-specific road graph, including connector offsets. | yes |
| Disruption Scenario | Disruption Scenario | scenario identifier | Identifier of the baseline or a declared calibrated road-disruption network state. | Assigned during scenario estimation after the failure-severity response curve is reviewed; candidate levels are not automatically treated as final scenarios. | yes |
| District Name | District Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Eligible Emergency Hospital | Eligible Emergency Hospital | hospital supply | Indicator equal to one for a hospital with emergency designation or core/regional disaster-base designation. | Constructed from the confirmed emergency-hospital inclusion rule. | yes |
| Emergency Designated | Emergency Designated | hospital role | Indicator that the facility appears on the prefectural emergency-designated hospital list. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Designation | Emergency Designation | hospital role | Reported emergency-care designation assigned to the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Designation Code | Emergency Designation Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Road Class | Emergency Road Class | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Road Class Code | Emergency Road Class Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Route Membership | Emergency Route Membership | network priority | Emergency transport road class associated with a compatible route alignment. | Assigned from the nearest emergency-route centreline within 30 m only when its Road Type matches the routable edge's Road Category; otherwise coded None. | yes |
| Expected Failed Road Length Share | Expected Failed Road Length Share | experimental treatment | Target expected share of total road-section length unavailable in a Monte Carlo state. | For each candidate level, calibrate failure intensity \(\lambda\) so \(\sum_s L_s[1-\exp(-\lambda L_s)]/\sum_s L_s\) equals the target; calibration tests 0.5%, 1%, 2%, 3%, 5%, and 10%. | yes |
| External Reference | External Reference | source provenance | Indicator that a listed facility is retained as an out-of-prefecture reference rather than Kumamoto supply. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Facility Name | Facility Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Failure Intensity per Metre | Failure Intensity per Metre | simulation parameter | Length-scaled failure intensity used to generate section probabilities. | Solved numerically for each Expected Failed Road Length Share and held fixed across paired replicates at that level. | yes |
| Fire Facility Name | Fire Facility Name | ambulance supply | Fire-service facility, staffing, or jurisdiction attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Fire Facility Type | Fire Facility Type | ambulance supply | Fire-service facility, staffing, or jurisdiction attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Fire Facility Type Code | Fire Facility Type Code | ambulance supply | Fire-service facility, staffing, or jurisdiction attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| From Node ID | From Node Identifier | network topology | Identifier of the first endpoint node of a routable edge. | Constructed from the endpoint coordinate and Vertical Level after one-metre snapping. | yes |
| General Beds | General Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| General Households | General Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Geometry | Geometry | spatial index | Point, line, or polygon geometry represented in JGD2011. | Standardized to JGD2011 (EPSG:6668). | yes |
| Grid Access Loss Probability | Grid Access Loss Probability | primary spatial outcome | Probability that a population grid loses baseline timely emergency access under a declared severity level. | Mean across replicates of the indicator that a grid is timely in baseline but not timely in the disrupted state. | yes |
| Hazard Exposure Class | Hazard Exposure Class | disruption risk | Highest landslide warning-zone class intersected by a road edge. | Coded Special Warning Zone, Warning Zone, or None from polygon intersection; it is scenario exposure rather than observed earthquake failure. | yes |
| Hazard Type | Hazard Type | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hazard Type Code | Hazard Type Code | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Assignment Probability | Hospital Assignment Probability | hospital reliability outcome | Probability that an eligible hospital is the replicate-specific Assigned Hospital for a demand unit or represented population. | Estimated as assignment frequency across Monte Carlo replicates within Expected Failed Road Length Share and Random Failure Model. | yes |
| Hospital Capacity Weight | Hospital Capacity Weight | hospital weight | Nonnegative hospital capacity weight used in weighted accessibility analyses. | Uses reported Bed Count without normalization during preprocessing; missing bed counts remain missing. | yes |
| Hospital Catchment Population | Hospital Catchment Population | hospital demand | Population assigned to a hospital under a specified scenario. | Sum of Total Population over analysis units for which that hospital is Assigned Hospital. | yes |
| Hospital Demand Change | Hospital Demand Change | hospital demand | Change in assigned hospital catchment population relative to baseline. | Scenario Hospital Catchment Population minus baseline Hospital Catchment Population. | yes |
| Hospital ID | Hospital Identifier | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Name | Hospital Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Name Kana | Hospital Name Kana | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Name Romanized | Hospital Name Romanized | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Node ID | Hospital Node Identifier | network connector | Identifier of the virtual road-network connector for an eligible emergency hospital. | Assigned when the hospital is within 150 m of an eligible road edge. | yes |
| Hospital Role Weight | Hospital Role Weight | hospital weight | Weight applied to a hospital's emergency-care role in weighted sensitivity analyses. | Initialized to 1.0 for the unweighted baseline; alternative role weights are estimated only in declared sensitivity specifications. | yes |
| Hospital Transport Time | Hospital Transport Time | accessibility outcome | Shortest network travel time from the demand unit to an operational eligible hospital. | Calculated on the same scenario-specific road graph after ambulance arrival. | yes |
| Households with Member Age 65+ | Households with Member Age 65+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Infectious Disease Beds | Infectious Disease Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Institution Type Code | Institution Type Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Insured Long-Term Care Beds | Insured Long-Term Care Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Latitude | Latitude | spatial index | Reported geographic coordinate. | Coerced to numeric and used to construct JGD2011 point geometry where applicable. | yes |
| Long-Term Care Beds | Long-Term Care Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Longitude | Longitude | spatial index | Reported geographic coordinate. | Coerced to numeric and used to construct JGD2011 point geometry where applicable. | yes |
| Match Status | Match Status | record linkage | Outcome category from reconciling the healthcare-plan hospital name to the MHLW hospital roster. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Matched Hospital Name | Matched Hospital Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Departments 1 | Medical Departments 1 | clinical service scope | First reported group of medical departments provided by the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Departments 2 | Medical Departments 2 | clinical service scope | Second reported group of medical departments provided by the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Departments 3 | Medical Departments 3 | clinical service scope | Third reported group of medical departments provided by the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Facility Class | Medical Facility Class | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Facility Class Code | Medical Facility Class Code | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Mesh Code | Mesh Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Monte Carlo Convergence Status | Monte Carlo Convergence Status | convergence diagnostic | Indicator that prespecified accessibility estimates are stable across replicate checkpoints. | Evaluated from changes in population-access means, quantiles, and grid loss probabilities at declared replicate checkpoints within each severity level. | yes |
| Municipality Code | Municipality Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Municipality Label | Municipality Label | administrative descriptor | Published municipality label associated with the record. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Municipality Name | Municipality Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Name Match Score | Name Match Score | record linkage | Normalized similarity score used to review hospital-name reconciliation. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Network Analysis Eligible | Network Analysis Eligible | sample definition | Indicator that a valid Standard Road edge or node is retained for network analysis. | Set to one for every valid Standard Road component; component IDs preserve disconnected-network status without deleting island demand. | yes |
| Network Component ID | Network Component Identifier | network topology | Identifier of the connected Standard Road subnetwork containing the edge or node. | Computed by union-find over grade-aware edge endpoints; disconnected island components are retained. | yes |
| Network Snap Distance (m) | Network Snap Distance (m) | spatial linkage | Euclidean distance in metres from the source point or centroid to its nearest eligible road edge. | Calculated in EPSG:6670; missing values are not imputed and rejected records remain explicit. | yes |
| Notes | Notes | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Nursing-Care Long-Term Beds | Nursing-Care Long-Term Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Older Couple Household Share | Older Couple Household Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Older Couple Households | Older Couple Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Older Population Losing Timely Access | Older Population Losing Timely Access | equity outcome | Population age 65 or older timely in baseline but not timely in the disruption scenario. | Computed at disclosure-group level without duplicating or imputing older-population counts to meshes. | yes |
| Older Single-Person Household Share | Older Single-Person Household Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Older Single-Person Households | Older Single-Person Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| One-Person Households | One-Person Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Operational Hospital Set | Operational Hospital Set | hospital supply | Named hospital inclusion set used in an accessibility scenario. | Baseline set contains hospitals meeting the confirmed emergency or disaster-base designation rule. | yes |
| Operator Class Code | Operator Class Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Other Closure Dates | Other Closure Dates | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| P90 Emergency Access Time | P90 Emergency Access Time | reliability outcome | Ninetieth percentile of Total Emergency Access Time across Monte Carlo replicates. | Computed within Expected Failed Road Length Share, Random Failure Model, and demand unit; disconnected outcomes remain explicitly unreachable. | yes |
| Plan Hospital Name | Plan Hospital Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 65+ | Population Age 65+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 65+ Share | Population Age 65+ Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 75+ | Population Age 75+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 75+ Share | Population Age 75+ Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 85+ | Population Age 85+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 85+ Share | Population Age 85+ Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Losing Timely Access | Population Losing Timely Access | primary outcome | Population timely in baseline but not timely in the disruption scenario. | Sum of Total Population over units whose Timely Access Status changes from one to zero. | yes |
| Population Newly Disconnected | Population Newly Disconnected | primary outcome | Population connected to both stages of the emergency chain in baseline but disconnected in a disruption state. | Sum of Total Population over units with finite baseline Total Emergency Access Time and infinite disruption-state Total Emergency Access Time. | yes |
| Prefecture Code | Prefecture Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Prefecture Name | Prefecture Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Psychiatric Beds | Psychiatric Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Random Failure Model | Random Failure Model | simulation specification | Named mechanism used to assign simultaneous road-section failures. | Coded Length-Dependent Independent for the primary calibration; additional clustered mechanisms require a separately declared sensitivity specification. | yes |
| Realized Failed Road Length Share | Realized Failed Road Length Share | simulation diagnostic | Observed share of total road-section length failed in one replicate and severity state. | Total Road Section Length (m) over failed sections divided by total length over all eligible road sections. | yes |
| Reference Date | Reference Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Registration Date | Registration Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Road Available | Road Available | scenario state | Indicator that an edge is traversable in a specified network scenario. | Initialized to one for baseline; disruption and restoration scenarios update the indicator during estimation. | yes |
| Road Category | Road Category | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Category Code | Road Category Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Centerline Type | Road Centerline Type | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Centerline Type Code | Road Centerline Type Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Edge Count | Road Edge Count | network diagnostic | Number of internal routing fragments composing a road section. | Counted within Road Section ID; values above one arise from source-attribute or connector-preserving fragmentation rather than separate failure units. | yes |
| Road Edge ID | Road Edge Identifier | network identifier | Unique identifier for an internal routable Standard Road geometry fragment. | Assigned deterministically after same-level noding and one-metre endpoint snapping in EPSG:6670; it preserves source-attribute and connector split positions but is not the failure unit. | yes |
| Road Failure Indicator | Road Failure Indicator | experimental treatment | Indicator that a Road Section ID is unavailable in a replicate and severity state. | For each replicate, compare one uniform random score per section with the level-specific Section Failure Probability; shared scores make higher-severity states nested. | yes |
| Road Length (m) | Road Length (m) | network impedance | Projected length of the routable edge in metres. | Calculated in JGD2011 / Japan Plane Rectangular CS II (EPSG:6670). | yes |
| Road Section ID | Road Section Identifier | experimental unit | Unique identifier for one continuous road section between true same-level junctions. | Assigned to each maximal graph chain whose internal nodes have degree two; all internal routing fragments share one simultaneous failure state. | yes |
| Road Section Length (m) | Road Section Length (m) | experimental exposure | Total length in metres of a junction-to-junction road section. | Constructed by summing Road Length (m) over all internal routing fragments assigned to Road Section ID. | yes |
| Road State | Road State | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road State Code | Road State Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Type | Road Type | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Type Code | Road Type Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road-Section Expected Risk | Road-Section Expected Risk | primary road outcome | Probability-weighted expected accessibility consequence of a road section under a declared severity and timely-access threshold. | Section Failure Probability multiplied by Road-Section Potential Access Loss, reported for every eligible road section. | yes |
| Road-Section Potential Access Loss | Road-Section Potential Access Loss | primary road outcome | Population-weighted timely-access loss caused by failure of one junction-to-junction road section with other roads available. | Computed for every eligible Road Section ID and Timely Access Threshold (min) as baseline covered population minus covered population after removing only that section; mapped continuously without a Top-20 cutoff. | yes |
| Rotation Hospital | Rotation Hospital | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Route ID | Route Identifier | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Route Name | Route Name | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Secondary Mesh Code | Secondary Mesh Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Section Failure Probability | Section Failure Probability | experimental treatment | Probability that a junction-to-junction road section is unavailable in a declared severity state. | Constructed as \(q_s(\lambda)=1-\exp(-\lambda L_s)\), so longer road sections have greater probability of containing at least one failure. | yes |
| Section From Node ID | Section From Node Identifier | network topology | Identifier of one terminal junction of a road section. | Copied from the first terminal node of the deterministic junction-to-junction chain. | yes |
| Section To Node ID | Section To Node Identifier | network topology | Identifier of the other terminal junction of a road section. | Copied from the second terminal node of the deterministic junction-to-junction chain; closed degree-two cycles retain one repeated anchor node. | yes |
| Service Status | Service Status | service availability | Reported operating or service-availability status of the facility. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Short Name | Short Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Short Name Kana | Short Name Kana | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Simulation Replicate | Simulation Replicate | simulation identifier | Integer identifying one reproducible Monte Carlo randomization draw. | Assigned from 1 to the executed replicate count with a recorded deterministic random seed. | yes |
| Source Date | Source Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Source Name | Source Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Special Warning Zone Pending | Special Warning Zone Pending | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Special Warning Zone Pending Code | Special Warning Zone Pending Code | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Subprefecture Name | Subprefecture Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Suppressed Source Mesh Count | Suppressed Source Mesh Count | demand disclosure | Number of source meshes combined because population values were disclosure-suppressed. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Tertiary Emergency Hospital | Tertiary Emergency Hospital | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Timely Access Probability | Timely Access Probability | primary reliability outcome | Monte Carlo probability that a demand unit completes the fire-station-to-grid-to-hospital chain within a declared threshold. | Mean of Timely Access Status across executed replicates within Expected Failed Road Length Share, Random Failure Model, demand unit, and threshold. | yes |
| Timely Access Status | Timely Access Status | primary outcome | Indicator that Total Emergency Access Time does not exceed the selected threshold. | Coded separately for each Disruption Scenario and Timely Access Threshold (min). | yes |
| Timely Access Threshold (min) | Timely Access Threshold (min) | accessibility threshold | Maximum total emergency access time defining timely service, in minutes. | Evaluated at the prespecified 15, 30, and 45 minute thresholds. | yes |
| To Node ID | To Node Identifier | network topology | Identifier of the second endpoint node of a routable edge. | Constructed from the endpoint coordinate and Vertical Level after one-metre snapping. | yes |
| Toll Category | Toll Category | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Toll Category Code | Toll Category Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Total Beds | Total Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Total Emergency Access Time | Total Emergency Access Time | primary outcome | Two-stage emergency travel time from dispatch base through the demand unit to the assigned hospital. | Constructed as Dispatch Travel Time plus Hospital Transport Time. | yes |
| Total Households | Total Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Total Population | Total Population | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Tuberculosis Beds | Tuberculosis Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Vertical Level | Vertical Level | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Ward Name | Ward Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Warning Zone Class | Warning Zone Class | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Warning Zone Class Code | Warning Zone Class Code | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Website | Website | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Week 1 Closed Friday | Week 1 Closed Friday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 1 Closed Monday | Week 1 Closed Monday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 1 Closed Saturday | Week 1 Closed Saturday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 1 Closed Sunday | Week 1 Closed Sunday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 1 Closed Thursday | Week 1 Closed Thursday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 1 Closed Tuesday | Week 1 Closed Tuesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 1 Closed Wednesday | Week 1 Closed Wednesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Friday | Week 2 Closed Friday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Monday | Week 2 Closed Monday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Saturday | Week 2 Closed Saturday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Sunday | Week 2 Closed Sunday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Thursday | Week 2 Closed Thursday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Tuesday | Week 2 Closed Tuesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 2 Closed Wednesday | Week 2 Closed Wednesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Friday | Week 3 Closed Friday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Monday | Week 3 Closed Monday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Saturday | Week 3 Closed Saturday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Sunday | Week 3 Closed Sunday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Thursday | Week 3 Closed Thursday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Tuesday | Week 3 Closed Tuesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 3 Closed Wednesday | Week 3 Closed Wednesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Friday | Week 4 Closed Friday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Monday | Week 4 Closed Monday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Saturday | Week 4 Closed Saturday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Sunday | Week 4 Closed Sunday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Thursday | Week 4 Closed Thursday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Tuesday | Week 4 Closed Tuesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 4 Closed Wednesday | Week 4 Closed Wednesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Friday | Week 5 Closed Friday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Monday | Week 5 Closed Monday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Saturday | Week 5 Closed Saturday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Sunday | Week 5 Closed Sunday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Thursday | Week 5 Closed Thursday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Tuesday | Week 5 Closed Tuesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Week 5 Closed Wednesday | Week 5 Closed Wednesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Friday | Weekly Closed Friday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Monday | Weekly Closed Monday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Saturday | Weekly Closed Saturday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Sunday | Weekly Closed Sunday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Thursday | Weekly Closed Thursday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Tuesday | Weekly Closed Tuesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Weekly Closed Wednesday | Weekly Closed Wednesday | service availability | Reported specialty, consultation, reception, or closure-schedule attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Width Category | Width Category | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Width Category Code | Width Category Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Zone ID | Zone Identifier | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Zone Name | Zone Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
## 5. Identification Strategy

This study is an applied randomized computational experiment. Population demand, candidate dispatch bases, eligible hospitals, road topology, and baseline travel impedance are held fixed. Road availability changes across reproducible Monte Carlo states. The design identifies accessibility reliability and road consequence within the declared simulation model; it does not identify the causal effect of an observed earthquake, an actual road repair, or an operational ambulance intervention.

### 5.1 Experimental Unit and Failure Assignment

Road Section ID is the failure and analysis unit. Each section is a continuous chain between true same-level junctions. Internal Road Edge ID fragments are retained only to preserve routing impedance, source attributes, and connector positions; all fragments assigned to one Road Section ID share one Road Failure Indicator.

For road section \(s\) with Road Section Length (m) \(L_s\), Section Failure Probability is

\[
q_s(\lambda_d)=1-\exp(-\lambda_d L_s).
\]

Here, \(q_s(\lambda_d)\) is the probability that section \(s\) fails at severity \(d\), and \(\lambda_d\) is Failure Intensity per Metre. For each Expected Failed Road Length Share \(d\), \(\lambda_d\) solves

\[
\frac{\sum_{s \in S} L_s q_s(\lambda_d)}
{\sum_{s \in S} L_s}=d.
\]

Here, \(S\) is the set of eligible road sections. One reproducible uniform score \(U_{s,r}\) is drawn for each section \(s\) and Simulation Replicate \(r\). Road Failure Indicator is

\[
Z_{s,r,d}=\mathbf{1}\{U_{s,r}<q_s(\lambda_d)\}.
\]

Because the same \(U_{s,r}\) is reused across severity levels and \(q_s(\lambda_d)\) increases with \(d\), failed-section sets are nested within replicate. The main scenarios use \(d \in \{0.01,0.03,0.05\}\). The \(d=0.10\) state is an extreme stress sensitivity, and \(d=0.005\) remains a near-baseline calibration check rather than a main scenario.

### 5.2 Accessibility Comparison

The operational chain is Candidate Dispatch Base to population grid to Eligible Emergency Hospital. Every network state is fully rerouted, so an alternative route, dispatch base, or hospital may replace the baseline assignment. Primary comparisons are within the same demand unit and paired Simulation Replicate across nested severity states.

The primary grid estimand is Timely Access Probability at 30 minutes. The 15- and 45-minute thresholds, P90 Emergency Access Time, and Grid Access Loss Probability are complementary outcomes. System estimands are Total Population, Population Age 65+, and Population Newly Disconnected. Hospital estimands are Hospital Assignment Probability and the distribution of Hospital Catchment Population.

### 5.3 Road Consequence and Risk Interpretation

Road-Section Potential Access Loss is estimated by removing one Road Section ID from the otherwise available baseline graph and recomputing population-weighted timely access. This leave-one-section-out quantity measures potential network consequence. Road-Section Expected Risk multiplies that consequence by Section Failure Probability for a declared severity.

Potential loss is not a conditional Monte Carlo coefficient or a Shapley decomposition. It isolates the consequence of one section when all other sections remain available, whereas simultaneous failures can interact. Expected risk depends on the length-dependent failure model and is therefore scenario-specific. Both measures are mapped for every eligible section; no Top-20 cutoff is used.

### 5.4 Identification Limits

Results are conditional on the Standard Road topology, assumed travel speeds, connector rules, eligible hospital set, and length-dependent independent-failure mechanism. They do not measure ambulance availability, dispatch delay, on-scene treatment, congestion, hospital clinical capacity, engineering fragility, repair duration, or repair cost. Hospital capacity and role weights are sensitivity descriptors rather than observed destination-choice behavior. Hazard Exposure Class is used for interpretation and sensitivity grouping, not as proof that a section failed.

## 6. Main Estimation Framework

### 6.1 Baseline Emergency Network

Let \(G_0=(V,E)\) denote the eligible baseline road graph, where \(V\) contains grade-aware road and virtual connector nodes and \(E\) contains routable internal edges. Each edge \(e\) has Baseline Edge Travel Time (min)

\[
t_e=\frac{60L_e}{1000v_e}.
\]

Here, \(L_e\) is Road Length (m), and \(v_e\) is Assumed Speed (km/h). Connector time uses Network Snap Distance (m) and the speed of the referenced access edge. Rejected connectors remain explicit and receive infinite network travel time.

For demand unit \(i\), replicate \(r\), and severity \(d\), Dispatch Travel Time and Hospital Transport Time are

\[
D_{i,r,d}=\min_{f \in F} d_{r,d}(f,i),
\qquad
H_{i,r,d}=\min_{h \in H} d_{r,d}(i,h),
\]

where \(F\) is the set of Candidate Dispatch Base nodes, \(H\) is the Operational Hospital Set, and \(d_{r,d}(u,v)\) is the shortest travel time between nodes \(u\) and \(v\) after sections with \(Z_{s,r,d}=1\) are removed. Total Emergency Access Time is

\[
T_{i,r,d}=D_{i,r,d}+H_{i,r,d}.
\]

If either stage is unreachable, \(T_{i,r,d}\) is infinite.

### 6.2 Grid Reliability

For Timely Access Threshold (min) \(\tau \in \{15,30,45\}\), Timely Access Status is

\[
A_{i,r,d}(\tau)=\mathbf{1}\{T_{i,r,d}\leq \tau\}.
\]

With \(R\) executed replicates, Timely Access Probability is

\[
\widehat{\pi}_{i,d}(\tau)=\frac{1}{R}\sum_{r=1}^{R}A_{i,r,d}(\tau).
\]

P90 Emergency Access Time is the empirical 90th percentile of finite \(T_{i,r,d}\), while the share of infinite outcomes is reported separately. For a grid timely in baseline, Grid Access Loss Probability is

\[
\widehat{\ell}_{i,d}(\tau)
=
\frac{1}{R}
\sum_{r=1}^{R}
\mathbf{1}\{A_{i,0}(\tau)=1,\ A_{i,r,d}(\tau)=0\}.
\]

Here, \(A_{i,0}(\tau)\) is baseline Timely Access Status.

### 6.3 Population Coverage and Disconnection

For population weight \(w_i\), replicate-specific timely coverage is

\[
C_{r,d}(\tau)=\sum_i w_i A_{i,r,d}(\tau).
\]

Primary \(w_i\) is Total Population. Population Age 65+ is evaluated on its valid disclosure-group support without duplication or mesh-level imputation. Population Losing Timely Access is

\[
L_{r,d}(\tau)=\sum_i w_i
\mathbf{1}\{A_{i,0}(\tau)=1,\ A_{i,r,d}(\tau)=0\}.
\]

Population Newly Disconnected uses finite baseline Total Emergency Access Time and infinite disrupted Total Emergency Access Time. For each severity and threshold, report the mean, standard deviation, P5, P50, P95, and Monte Carlo confidence interval across replicates.

### 6.4 Hospital Service Reliability

Assigned Hospital is the eligible hospital minimizing Hospital Transport Time in each network state. For eligible hospital \(h\), Hospital Catchment Population is

\[
K_{h,r,d}=\sum_i w_i\mathbf{1}\{h_{i,r,d}=h\},
\]

where \(h_{i,r,d}\) is Assigned Hospital for demand unit \(i\). Hospital Assignment Probability is the population-weighted or demand-unit-weighted assignment frequency, clearly labelled. Report the distribution of \(K_{h,r,d}\), Hospital Demand Change relative to baseline, and the probability that a baseline catchment becomes disconnected. Unweighted eligible-hospital routing is primary; Hospital Role Weight and Hospital Capacity Weight are separate sensitivity specifications.

### 6.5 Road-Section Potential Access Loss

Let \(C_0(\tau)\) be baseline population coverage. Let \(C_{-s}(\tau)\) be coverage after removing only road section \(s\). Road-Section Potential Access Loss is

\[
P_s(\tau)=C_0(\tau)-C_{-s}(\tau).
\]

Compute \(P_s(\tau)\) for every eligible Road Section ID and each \(\tau \in \{15,30,45\}\). Nonnegative values are expected because removing a section cannot shorten a route. Zero values remain visible as zero in the mapped data and are visually separated from positive values.

For severity \(d\), Road-Section Expected Risk is

\[
R_{s,d}(\tau)=q_s(\lambda_d)P_s(\tau).
\]

Map \(P_s(\tau)\) for all three thresholds and \(R_{s,d}(30)\) for the 1%, 3%, and 5% main scenarios. These are continuous full-network surfaces, not ranked Top-20 outputs.

### 6.6 Severity Calibration, Uncertainty, and Convergence

The 100-replicate calibration evaluates 0.5%, 1%, 2%, 3%, 5%, and 10% Expected Failed Road Length Share. It reports mean response and P5-P95 intervals for population retaining 30-minute access, Population Losing Timely Access, and Population Newly Disconnected. The calibration selects 1%, 3%, and 5% as main scenarios and 10% as stress sensitivity.

The formal experiment targets 1,000 paired replicates per main and stress scenario. Convergence is evaluated at 100, 250, 500, 750, and 1,000 replicates. For checkpoint \(R_j\) and its preceding checkpoint \(R_{j-1}\), define

\[
\Delta_{C,j,d}=\frac{|\overline{C}_{R_j,d}(30)-\overline{C}_{R_{j-1},d}(30)|}{\sum_i w_i},
\]

\[
\Delta_{G,j,d}=Q_{0.95,i}\left(|\widehat{\pi}_{i,d,R_j}(30)-\widehat{\pi}_{i,d,R_{j-1}}(30)|\right),
\]

and

\[
\Delta_{H,j,d}=\frac{Q_{0.95,h}\left(|\overline{K}_{h,R_j,d}-\overline{K}_{h,R_{j-1},d}|\right)}{\sum_i w_i}.
\]

Here, \(\overline{C}_{R_j,d}(30)\) is mean population retaining 30-minute access over the first \(R_j\) paired replicates, \(Q_{0.95,i}\) is the 95th percentile across population grids, \(\widehat{\pi}_{i,d,R_j}(30)\) is Timely Access Probability estimated with the first \(R_j\) replicates, \(Q_{0.95,h}\) is the 95th percentile across eligible hospitals, and \(\overline{K}_{h,R_j,d}\) is mean Hospital Catchment Population over the first \(R_j\) replicates. For grids timely in baseline, the absolute change in Timely Access Probability equals the absolute change in Grid Access Loss Probability. Monte Carlo Convergence Status is Stable only when \(\Delta_{C,j,d}\leq0.005\), \(\Delta_{G,j,d}\leq0.05\), and \(\Delta_{H,j,d}\leq0.005\). Thus, the declared grid-probability tolerance is 5 percentage points, while the population-coverage and hospital-catchment tolerances are each 0.5% of Total Population. The 100-replicate checkpoint is the reference and is not classified. Population Coverage Standard Error is reported as a precision diagnostic but is not an additional pass/fail threshold. Quantities that fail at 1,000 replicates remain labelled inconclusive rather than being promoted to priority claims.

### 6.7 Sensitivity and Failure-Mode Checks

Required checks are:

- 10% Expected Failed Road Length Share as an extreme network-stress scenario.
- Assumed Speed (km/h) multipliers of 0.8 and 1.2 relative to baseline.
- Alternative Operational Hospital Set definitions and separately labelled Hospital Role Weight or Hospital Capacity Weight specifications.
- Road Section Length (m), Road Edge Count, Network Component ID, and connector audits, with special inspection of the upper tail of section length.
- Comparison of results by Emergency Route Membership, Road Category, and Hazard Exposure Class without interpreting these descriptors as observed failure causes.
- Replicate checkpoint comparisons for all primary population and grid-reliability outcomes.

## 7. Analytical Workflow

| step | variables used | formula/model used | generated figure/table title | theory or claim evaluated | support status |
|---|---|---|---|---|---|
| 1. Validate baseline network and study population | Road Section ID, Road Section Length (m), Road Edge Count, From Node ID, To Node ID, Network Component ID, Network Snap Distance (m), Candidate Dispatch Base, Eligible Emergency Hospital, Total Population | Section 6.1 network, impedance, component, and connector checks | Emergency Care Network and Population Demand; Baseline Two-Stage Emergency Travel Time; Network and Simulation Descriptive Summary | The complete fire-station-to-grid-to-hospital chain is represented on interpretable junction-defined road sections. | Partially supported: topology and connector checks pass; the formal simulation remains pending. |
| 2. Calibrate failure severity | Expected Failed Road Length Share, Failure Intensity per Metre, Road Section Length (m), Section Failure Probability, Realized Failed Road Length Share, Simulation Replicate | Section 5.1 calibration equation and paired nested assignment | Failure Severity Response; Network and Simulation Descriptive Summary | Lower severities reveal the onset and shape of emergency-access deterioration. | Supported for the 100-replicate calibration; formal scenario precision remains pending. |
| 3. Generate formal nested failures | Road Section ID, Section Failure Probability, Road Failure Indicator, Road Available, Simulation Replicate, Random Failure Model | Section 5.1 nested length-dependent failure assignment | Nested Length-Dependent Road Failure Realizations | Main severity states are comparable within paired replicates. | Pending formal 1,000-replicate experiment. |
| 4. Estimate grid reliability | Analysis Unit ID, Total Emergency Access Time, Timely Access Threshold (min), Timely Access Status, Timely Access Probability, Grid Access Loss Probability, P90 Emergency Access Time | Sections 6.1-6.2 two-stage routing and reliability estimators | Grid Emergency Access Loss Probability; Emergency Access Reliability by Severity and Threshold | Road failures create spatially heterogeneous loss of emergency access. | Inconclusive until formal simulation outputs are generated. |
| 5. Aggregate population and municipal outcomes | Total Population, Population Age 65+, Municipality Name, Population Losing Timely Access, Older Population Losing Timely Access, Population Newly Disconnected | Section 6.3 coverage and loss estimators | Population Coverage under Length-Dependent Road Failure; Municipal Emergency Access Reliability | Aggregate robustness can coexist with concentrated geographic or older-population loss. | Inconclusive until formal simulation outputs are generated. |
| 6. Estimate hospital service reliability | Hospital Name, Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability, Hospital Demand Change, Operational Hospital Set | Section 6.4 hospital assignment and catchment estimators | Hospital Service Reliability under Road Failure; Hospital Service Reliability | Hospital value depends on road-supported reachability and substitution across hospitals. | Inconclusive until formal simulation outputs are generated. |
| 7. Map every road section's consequence and expected risk | Road Section ID, Geometry, Timely Access Threshold (min), Section Failure Probability, Road-Section Potential Access Loss, Road-Section Expected Risk, Route Name | Section 6.5 leave-one-section-out consequence and probability weighting | Road-Section Accessibility Consequence and Expected Risk; Road-Section Loss by Network Characteristics | A small subset of spatially coherent sections may support disproportionate emergency access without requiring an arbitrary rank cutoff. | Inconclusive until all-section routing is completed. |
| 8. Evaluate uncertainty and sensitivity | Simulation Replicate, Monte Carlo Convergence Status, Expected Failed Road Length Share, Assumed Speed (km/h), Hospital Role Weight, Hospital Capacity Weight | Sections 6.6-6.7 checkpoint convergence comparisons using the declared 0.5%, 5-percentage-point, and 0.5% tolerances, plus sensitivity comparisons | Monte Carlo Convergence and Stress Sensitivity; Monte Carlo Convergence Summary | Main conclusions remain interpretable under simulation error and declared routing assumptions. | Supported: all four severity states pass the declared convergence rule at 1,000 replicates, and the travel-speed sensitivity remains explicitly reported. |

Analytical checkpoints:

1. Stop and repair preprocessing if section identifiers, section-length aggregation, topology, or connector references fail validation.
2. Stop scenario interpretation if realized failed road length is systematically inconsistent with Expected Failed Road Length Share or paired nesting fails.
3. Label grid, population, hospital, or municipal results inconclusive when Monte Carlo Convergence Status does not pass at 1,000 replicates.
4. Inspect every positive upper-tail Road-Section Potential Access Loss value against topology and connector placement before interpreting it.
5. Do not convert Road-Section Expected Risk into a repair order without separate repair-time, cost, engineering-condition, and operational evidence.

## 8. Figure and Table Plan

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---|---|---|
| Emergency Care Network and Population Demand | Shows the spatial structure of population demand, candidate ambulance dispatch bases, eligible emergency hospitals, and the road network. | map | 3 | Geometry, Total Population, Population Age 65+, Candidate Dispatch Base, Eligible Emergency Hospital, Emergency Road Class | done |
| Baseline Two-Stage Emergency Travel Time | Decomposes baseline ambulance dispatch, hospital transport, and total two-stage emergency travel time. | map | 3 | Geometry, Candidate Dispatch Base, Eligible Emergency Hospital, Road Type, Width Category | done |
| Failure Severity Response | Calibrates the relationship between expected failed road length and population retaining 30-minute access, Population Losing Timely Access, and Population Newly Disconnected using means and P5-P95 intervals. | line | 3 | Expected Failed Road Length Share, Realized Failed Road Length Share, Simulation Replicate, Timely Access Threshold (min), Total Population, Population Losing Timely Access, Population Newly Disconnected | done |
| Nested Length-Dependent Road Failure Realizations | Shows one reproducible paired replicate at the 1%, 3%, and 5% main scenarios and the 10% stress scenario, with available roads green and failed sections clearly distinguished. | map | 4 | Geometry, Road Section ID, Road Section Length (m), Expected Failed Road Length Share, Section Failure Probability, Simulation Replicate, Road Failure Indicator, Road Available | done |
| Grid Emergency Access Loss Probability | Maps the probability that a baseline-timely grid loses 30-minute emergency access under the 1%, 3%, and 5% main scenarios. | map | 3 | Geometry, Analysis Unit ID, Expected Failed Road Length Share, Timely Access Threshold (min), Grid Access Loss Probability, Total Population | done |
| Population Coverage under Length-Dependent Road Failure | Shows replicate distributions and uncertainty for total and older population retaining 15-, 30-, and 45-minute emergency access across main and stress scenarios. | line | 3 | Expected Failed Road Length Share, Simulation Replicate, Timely Access Threshold (min), Timely Access Status, Total Population, Population Age 65+, Population Losing Timely Access, Older Population Losing Timely Access, Population Newly Disconnected | done |
| Hospital Service Reliability under Road Failure | Maps changes in eligible-hospital catchment population and assignment stability under the 1%, 3%, and 5% main scenarios. | map | 3 | Geometry, Hospital Name, Eligible Emergency Hospital, Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability, Hospital Demand Change, Expected Failed Road Length Share | done |
| Road-Section Accessibility Consequence and Expected Risk | Maps every junction-to-junction road section: the upper row shows potential population-access loss at 15, 30, and 45 minutes, and the lower row shows 30-minute expected risk at 1%, 3%, and 5% severity. | map | 6 | Geometry, Road Section ID, Route Name, Road Section Length (m), Timely Access Threshold (min), Section Failure Probability, Road-Section Potential Access Loss, Road-Section Expected Risk | done |
| Monte Carlo Convergence and Stress Sensitivity | Shows convergence across replicate checkpoints and contrasts the main scenarios with the 10% stress state and declared travel-speed sensitivity. | line | 4 | Simulation Replicate, Expected Failed Road Length Share, Timely Access Probability, Population Losing Timely Access, Population Newly Disconnected, Assumed Speed (km/h), Monte Carlo Convergence Status | done |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Network and Simulation Descriptive Summary | Summarizes junction-defined road sections, population grids, dispatch bases, hospitals, failure calibration, and executed replicate counts. | approximately 35 | 8 | One network, demand, facility, connector, or simulation-design indicator. | Count, length, total, mean, standard deviation, P5, P50, and P95 as applicable. | done |
| Emergency Access Reliability by Severity and Threshold | Compares population-weighted emergency-access reliability across three main scenarios, the stress scenario, and three timely-access thresholds. | 12 | 12 | One Expected Failed Road Length Share and Timely Access Threshold (min) combination. | Replicates, mean coverage, Monte Carlo standard error, P5, P50, P95, Population Losing Timely Access, Older Population Losing Timely Access, and Population Newly Disconnected. | done |
| Municipal Emergency Access Reliability | Reports geographic heterogeneity in simulated emergency-access reliability. | approximately 180 | 12 | One Municipality Name and main or stress Expected Failed Road Length Share combination. | Total Population, Population Age 65+, Timely Access Probability, P90 Emergency Access Time, coverage loss, disconnection, and uncertainty measures. | done |
| Hospital Service Reliability | Reports hospital assignment and service-population stability under road failure. | approximately 300 | 12 | One eligible Hospital Name and main or stress Expected Failed Road Length Share combination. | Hospital role, mean Hospital Catchment Population, Hospital Assignment Probability, Hospital Demand Change, P5, P50, P95, and disconnection frequency. | done |
| Road-Section Loss by Network Characteristics | Summarizes the distribution of potential access loss and expected risk without selecting a Top-20 list. | approximately 60 | 12 | One Road Category, Emergency Route Membership, Hazard Exposure Class, and severity grouping. | Section count, road length, zero-loss share, mean, P50, P90, P95, P99, maximum potential loss, and expected risk. | done |
| Monte Carlo Convergence Summary | Reports stability of primary accessibility outcomes across replicate checkpoints and severity levels. | approximately 20 | 10 | One replicate checkpoint and Expected Failed Road Length Share combination. | Coverage mean, P5, P95, Monte Carlo standard error, change from previous checkpoint, grid-probability change, and Monte Carlo Convergence Status. | done |
