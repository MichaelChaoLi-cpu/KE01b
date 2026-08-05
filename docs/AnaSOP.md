# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Central Research Question

- Research question: Under nested 5%, 10%, and 20% random failures of standardized 100 m road units, how reliably can each population grid complete the fire-station-to-grid-to-hospital emergency chain, and which road units contribute most to maintaining timely emergency access across Kumamoto Prefecture?
- Why it matters: Emergency managers need evidence on both where ambulance access is fragile and which road sections should receive continuity protection, inspection, or restoration priority when many road failures can occur simultaneously.
- Data support currently visible: The current evidence represents population demand, older populations, candidate fire-station dispatch bases, eligible emergency hospitals, a routable road network, road and route attributes, administrative geography, and hazard information suitable for random-failure and sensitivity designs.
- Key readable variables or data scope: Geometry, Total Population, Population Age 65+, Candidate Dispatch Base, Eligible Emergency Hospital, Dispatch Travel Time, Hospital Transport Time, Total Emergency Access Time, Road Failure Unit ID, Failure Rate, Simulation Replicate, Road Failure Indicator, Random Failure Model, and Road Failure Importance.
- What would verify it: Repeated full-network routing should yield reproducible grid-level access probabilities and uncertainty intervals; failure severity should produce ordered system deterioration; and high-importance road rankings should stabilize as replicate counts increase.
- What would falsify or weaken it: The study would weaken if baseline topology is unreliable, the full emergency chain cannot be computed for most represented population, 1,000 replicates remain computationally infeasible, Monte Carlo estimates fail to converge, or road rankings are determined mainly by the arbitrary 100 m segmentation rule.
- Required next feasibility check: Validate the 100 m network, benchmark an optimized two-source-family shortest-path engine, complete a 100-replicate pilot, and test convergence and sensitivity to uniform versus spatially clustered failures.

### Supporting Research Questions

The four supporting questions deepen the central applied question through grid reliability, population distribution, hospital service stability, and road-priority robustness.

#### Grid-Level Emergency Access Reliability

- Role relative to central point: establish the primary reliability outcome.
- Research question: How do 5%, 10%, and 20% road failure change each grid's probability of completing the emergency chain within 15, 30, and 45 minutes and its upper-tail emergency travel time?
- Why it matters: Expected time alone can hide rare but severe disconnections; grid-level probabilities and P90 time reveal both routine degradation and reliability risk.
- Data support currently visible: Population-grid connectors, dispatch-base connectors, hospital connectors, road travel times, and network topology support repeated multi-source shortest-path estimation.
- Key readable variables or data scope: Analysis Unit ID, Demand Node ID, Dispatch Base Node ID, Hospital Node ID, Failure Rate, Simulation Replicate, Total Emergency Access Time, Timely Access Probability, and P90 Emergency Access Time.
- What would verify it: Access probability should be bounded, reproducible, and non-increasing across nested failure levels except for negligible Monte Carlo variation.
- What would falsify or weaken it: Results would weaken if many grids lack baseline network access or if upper-tail estimates remain unstable at 1,000 replicates.
- Required next feasibility check: Confirm connector handling when its 100 m access unit fails and verify paired nested draws preserve comparable grid samples.

#### Population, Older-Population, and Municipal Reliability

- Role relative to central point: assess distributional and geographic heterogeneity.
- Research question: Which population groups and municipalities experience the largest expected and upper-tail losses of timely emergency access under random road failure?
- Why it matters: A road system can appear robust in aggregate while leaving older populations or peripheral municipalities with high disconnection risk.
- Data support currently visible: Total and older-population measures and municipal geography support population-weighted aggregation on their valid spatial supports.
- Key readable variables or data scope: Total Population, Population Age 65+, Population Age 75+, Population Age 85+, Municipality Name, Failure Rate, Timely Access Probability, Population Losing Timely Access, and Older Population Losing Timely Access.
- What would verify it: Monte Carlo intervals should identify persistent differences across population supports and municipalities rather than isolated replicate-specific extremes.
- What would falsify or weaken it: Claims would weaken if disclosure aggregation prevents defensible older-population localization or municipal ranks are highly unstable.
- Required next feasibility check: Retain separate spatial support for older-population estimates and measure municipal rank stability across replicate counts.

#### Hospital Service Reliability

- Role relative to central point: identify the hospital-side service mechanism.
- Research question: How do random road failures change the probability that each eligible hospital remains the nearest feasible destination and the distribution of its population catchment?
- Why it matters: Hospital emergency value depends on road-supported reachability and substitution, not only on beds or formal designation.
- Data support currently visible: Eligible hospital locations, roles, capacity descriptors, population demand, and labelled multi-source routing support replicate-specific hospital assignment and catchment estimation.
- Key readable variables or data scope: Hospital Name, Eligible Emergency Hospital, Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability, Hospital Role Weight, Hospital Capacity Weight, Failure Rate, and Simulation Replicate.
- What would verify it: Hospital assignment probabilities and catchment intervals should be reproducible and identify facilities with persistently large or volatile service roles.
- What would falsify or weaken it: Interpretation would weaken if eligibility rules or missing capacity data reverse results or if nearest-hospital assignment is an inadequate proxy for actual emergency destination choice.
- Required next feasibility check: Keep unweighted eligible-hospital routing primary and treat role or capacity weighting as separately labelled sensitivity analysis.

#### Road Failure Importance and Robustness

- Role relative to central point: translate network reliability into road-priority evidence.
- Research question: Which 100 m road units have the largest randomized failure effect on population-weighted timely emergency access, and are their values and ranks stable across failure levels, replicate counts, and uniform versus spatially clustered failure models?
- Why it matters: Random-failure accessibility maps locate vulnerable demand, but road management requires uncertainty-aware identification of the road units associated with the greatest system loss.
- Data support currently visible: Standardized road geometry, route information, nested randomized failures, and replicate-level emergency-access outcomes support randomized conditional importance estimates.
- Key readable variables or data scope: Road Failure Unit ID, Route Name, Road Failure Indicator, Road Failure Importance, Road Importance Standard Error, Confidence Interval, Rank Stability, Random Failure Model, and Monte Carlo Convergence Status.
- What would verify it: High-ranked units should have nontrivial effects, adequately narrow intervals, stable ranks, and coherent contiguous spatial patterns under plausible failure models.
- What would falsify or weaken it: Priority claims would fail if conditional estimates are too sparse, confidence intervals overlap broadly, rankings do not converge, or 100 m results cannot be aggregated into interpretable road sections.
- Required next feasibility check: Use the 100-replicate pilot to measure effective failed and available observations per unit, then increase replicates or aggregate units when precision is insufficient.

### Scope of Analysis

- Topics: Random road-network failure, ambulance dispatch, patient transport, hospital reachability, population emergency-access reliability, hospital service stability, and road continuity priority.
- Spatial scope: Kumamoto Prefecture, with network connectors and any necessary cross-boundary links retained only when they affect feasible emergency paths.
- Operational chain: Candidate fire-station dispatch base to population grid, followed by population grid to the nearest feasible eligible emergency hospital.
- Units of analysis: 100 m road-failure unit, population grid, older-population disclosure group, candidate dispatch base, eligible emergency hospital, municipality, failure rate, random-failure model, and simulation replicate.
- Period: Cross-sectional network simulation using the confirmed source vintages; it is not an observed longitudinal disaster-response study.
- Experimental scope: Nested 5%, 10%, and 20% failure levels, 1,000 target replicates per level, uniform random failure as the primary benchmark, and spatially clustered failure as required sensitivity analysis.

### Study Design Declaration

- Research type: applied
- Study design: Applied Monte Carlo network-reliability and emergency-access simulation study.
- Primary estimand: Grid-level probability of timely completion of the two-stage emergency chain and randomized failure importance of a standardized 100 m road unit under a declared failure-rate distribution.
- Interpretation limit: Results describe the specified random-failure models and routing assumptions. They do not reconstruct an observed earthquake, predict engineering failure probabilities, measure ambulance availability or on-scene delay, establish clinical capacity, or identify causal effects of an actual repair intervention.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

Research type: applied
Section focus: Empirical context, practical problem, and cautious interpretation limits.

### Research Gap

- Existing accessibility summaries can show where travel times are high under one assumed road state, but they do not quantify the probability distribution of emergency access across many simultaneous road-failure configurations.
- Fixed-path attribution can allocate dependence along one baseline route without testing the complete network after each failure draw. The practical gap is therefore a full-rerouting reliability framework that connects randomized road failures to grid access, population coverage, hospital service stability, and uncertainty-aware road priority.
- Verified event-specific closure probabilities and ambulance-operation records are not currently available, so the study estimates scenario reliability under transparent random-failure models rather than earthquake-specific risk.

### Conceptual Framework

- Standardizing roads into failure units defines the experimental exposure scale. A replicate-specific random draw determines which units are unavailable, while nested failure sets make 5%, 10%, and 20% severities directly comparable.
- Road availability determines the feasible graph. Two multi-source shortest-path calculations determine dispatch access from fire stations and hospital access to the nearest eligible hospital. Their sum defines the complete emergency travel time for each grid.
- Repeated routing transforms scenario-specific times into grid reliability, timely-access probabilities, upper-tail travel times, population coverage distributions, hospital assignment probabilities, and catchment uncertainty.
- Random assignment of road failures supports conditional road-importance estimation within the declared failure distribution. Uncertainty intervals, replicate-count convergence, rank stability, and spatially clustered sensitivity determine whether a road-priority claim is supportable.
- Scope boundary: Road Failure Importance is a model-based reliability importance measure, not an engineering failure probability, repair cost, asset price, or causal estimate from observed interventions.

### Problem Formulation

- Decision problem: Identify population grids and hospitals with fragile emergency access and prioritize road units whose continuity most strongly preserves population-weighted timely completion of the fire-station-to-grid-to-hospital chain.
- Experimental unit: Road Failure Unit ID, constructed as a routable road piece no longer than 100 m while retaining true intersections, grade separation, route attributes, and connector references.
- Randomization: Within replicate \(r\), one deterministic-seed random ordering or equivalent uniform score is assigned to all road-failure units. The 5%, 10%, and 20% failure sets are nested cuts of that ordering. A spatially clustered model forms a required alternative assignment mechanism.
- Primary grid outcome: Timely Access Probability for completing the two-stage chain within 30 minutes. The 15- and 45-minute thresholds and P90 Emergency Access Time are complementary outcomes.
- Primary system outcome: Total Population retaining timely access in each replicate. Older-population measures use their valid disclosure-group support.
- Primary road outcome: Road Failure Importance, defined from the difference in expected population-weighted timely access between randomized states in which a unit is available and failed under the same declared failure rate, with uncertainty and convergence diagnostics.
- Interpretation limit: Conditional road importance may be imprecise for rarely failed units and can reflect interactions with other failures. Definitive ranking requires adequate effective sample size, stable confidence intervals, and robustness to failure-model and segmentation choices.

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
| Disruption Scenario | Disruption Scenario | scenario identifier | Identifier of the baseline, Low, Central, High, or restoration network state. | Assigned during scenario estimation from Road Available configurations. | yes |
| District Name | District Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Eligible Emergency Hospital | Eligible Emergency Hospital | hospital supply | Indicator equal to one for a hospital with emergency designation or core/regional disaster-base designation. | Constructed from the confirmed emergency-hospital inclusion rule. | yes |
| Emergency Designated | Emergency Designated | hospital role | Indicator that the facility appears on the prefectural emergency-designated hospital list. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Designation | Emergency Designation | hospital role | Reported emergency-care designation assigned to the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Designation Code | Emergency Designation Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Road Class | Emergency Road Class | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Road Class Code | Emergency Road Class Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Emergency Route Membership | Emergency Route Membership | network priority | Emergency transport road class associated with a compatible route alignment. | Assigned from the nearest emergency-route centreline within 30 m only when its Road Type matches the routable edge's Road Category; otherwise coded None. | yes |
| External Reference | External Reference | source provenance | Indicator that a listed facility is retained as an out-of-prefecture reference rather than Kumamoto supply. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Facility Name | Facility Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Failure Rate | Failure Rate | experimental treatment | Target share of Road Failure Unit ID values set unavailable in a Monte Carlo network state. | Prespecified at 0.05, 0.10, and 0.20; the three levels are nested within Simulation Replicate. | yes |
| Fire Facility Name | Fire Facility Name | ambulance supply | Fire-service facility, staffing, or jurisdiction attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Fire Facility Type | Fire Facility Type | ambulance supply | Fire-service facility, staffing, or jurisdiction attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Fire Facility Type Code | Fire Facility Type Code | ambulance supply | Fire-service facility, staffing, or jurisdiction attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| From Node ID | From Node Identifier | network topology | Identifier of the first endpoint node of a routable edge. | Constructed from the endpoint coordinate and Vertical Level after one-metre snapping. | yes |
| General Beds | General Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| General Households | General Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Geometry | Geometry | spatial index | Point, line, or polygon geometry represented in JGD2011. | Standardized to JGD2011 (EPSG:6668). | yes |
| Hazard Exposure Class | Hazard Exposure Class | disruption risk | Highest landslide warning-zone class intersected by a road edge. | Coded Special Warning Zone, Warning Zone, or None from polygon intersection; it is scenario exposure rather than observed earthquake failure. | yes |
| Hazard Type | Hazard Type | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hazard Type Code | Hazard Type Code | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Assignment Probability | Hospital Assignment Probability | hospital reliability outcome | Probability that an eligible hospital is the replicate-specific Assigned Hospital for a demand unit or represented population. | Estimated as the assignment frequency across Monte Carlo replicates within Failure Rate and Random Failure Model. | yes |
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
| Monte Carlo Convergence Status | Monte Carlo Convergence Status | convergence diagnostic | Indicator that prespecified access-estimate and road-rank stability conditions are satisfied. | Evaluated at the declared replicate checkpoints and reported separately by Failure Rate and Random Failure Model. | yes |
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
| P90 Emergency Access Time | P90 Emergency Access Time | reliability outcome | Ninetieth percentile of Total Emergency Access Time across Monte Carlo replicates. | Computed within Failure Rate, Random Failure Model, and demand unit; disconnected outcomes remain explicitly unreachable and are not converted to ordinary travel times. | yes |
| Plan Hospital Name | Plan Hospital Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 65+ | Population Age 65+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 65+ Share | Population Age 65+ Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 75+ | Population Age 75+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 75+ Share | Population Age 75+ Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 85+ | Population Age 85+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Age 85+ Share | Population Age 85+ Share | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Population Losing Timely Access | Population Losing Timely Access | primary outcome | Population timely in baseline but not timely in the disruption scenario. | Sum of Total Population over units whose Timely Access Status changes from one to zero. | yes |
| Prefecture Code | Prefecture Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Prefecture Name | Prefecture Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Psychiatric Beds | Psychiatric Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Random Failure Model | Random Failure Model | simulation specification | Named mechanism used to assign simultaneous road failures. | Coded Uniform Random for the primary benchmark and Spatially Clustered for required sensitivity analysis. | yes |
| Rank Stability | Rank Stability | convergence diagnostic | Stability of a road unit's importance rank across replicate checkpoints or failure models. | Summarized from rank ranges, top-set overlap, and checkpoint-to-checkpoint rank changes. | yes |
| Reference Date | Reference Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Registration Date | Registration Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Road Available | Road Available | scenario state | Indicator that an edge is traversable in a specified network scenario. | Initialized to one for baseline; disruption and restoration scenarios update the indicator during estimation. | yes |
| Road Category | Road Category | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Category Code | Road Category Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Centerline Type | Road Centerline Type | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Centerline Type Code | Road Centerline Type Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Edge ID | Road Edge Identifier | network identifier | Unique identifier for a routable Standard Road edge and Monte Carlo failure unit. | Assigned deterministically after same-level noding, one-metre endpoint snapping, and splitting every topological edge into pieces no longer than 100 m in EPSG:6670. | yes |
| Road Failure Importance | Road Failure Importance | primary road outcome | Expected loss of population-weighted timely emergency access associated with failure rather than availability of one road-failure unit under a declared randomization distribution. | Estimated from replicate outcomes conditional on Road Failure Indicator, with the comparison made within Failure Rate and Random Failure Model. | yes |
| Road Failure Indicator | Road Failure Indicator | experimental treatment | Indicator that a Road Failure Unit ID is unavailable in a replicate and failure-rate state. | Set from the nested random ordering for the uniform model or from the declared spatial-cluster assignment for the clustered model. | yes |
| Road Failure Unit ID | Road Failure Unit Identifier | experimental unit | Unique identifier for a routable road piece subject to one simulated available or failed state. | Assigned one-to-one with each final Road Edge ID after deterministic splitting to a maximum length of 100 m. | yes |
| Road Importance Standard Error | Road Importance Standard Error | uncertainty diagnostic | Standard error of Road Failure Importance. | Calculated from the declared randomized conditional-effect estimator with effective failed and available replicate counts reported. | yes |
| Road Length (m) | Road Length (m) | network impedance | Projected length of the routable edge in metres. | Calculated in JGD2011 / Japan Plane Rectangular CS II (EPSG:6670). | yes |
| Road State | Road State | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road State Code | Road State Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Type | Road Type | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Type Code | Road Type Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Rotation Hospital | Rotation Hospital | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Route ID | Route Identifier | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Route Name | Route Name | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Secondary Mesh Code | Secondary Mesh Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
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
| Timely Access Probability | Timely Access Probability | primary reliability outcome | Monte Carlo probability that a demand unit completes the fire-station-to-grid-to-hospital chain within a declared threshold. | Mean of Timely Access Status across executed replicates within Failure Rate, Random Failure Model, demand unit, and threshold. | yes |
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

### Design Principle

This study uses an applied randomized computational experiment. It holds population demand, dispatch-base locations, hospital locations, hospital eligibility, road topology, and baseline impedance rules fixed while randomly changing Road Failure Indicator across standardized Road Failure Unit ID values. Randomization identifies an average failure association within the declared Monte Carlo assignment distribution; it does not identify the causal effect of an observed earthquake or an actual repair intervention.

The analytical chain is Candidate Dispatch Base to population grid to Eligible Emergency Hospital. Each Road Failure Unit ID is one routable road piece no longer than 100 m. All valid Standard Road components marked by Network Analysis Eligible are retained, including disconnected island and remote components. From Node ID, To Node ID, Network Component ID, Road Length (m), and Baseline Edge Travel Time (min) define topology and impedance. Dispatch Base Node ID, Demand Node ID, and Hospital Node ID define virtual connectors. Network Snap Distance (m) contributes connector travel; failed snaps remain explicit and their represented population is reported.

### Nested Random-Failure Contrasts

Baseline sets Road Available to one for every Network Analysis Eligible unit. For Simulation Replicate \(r\), the primary Uniform Random model assigns one seeded random ordering to all \(N\) road-failure units. The nested failed sets are

\[
F_{r,p} = \left\{e : \operatorname{rank}_r(e) \leq \lfloor pN \rfloor\right\},
\qquad p \in \{0.05,0.10,0.20\}.
\]

Here, \(F_{r,p}\) is the failed-unit set, \(e\) indexes Road Failure Unit ID, \(N\) is the number of eligible units, and \(p\) is Failure Rate. This construction guarantees \(F_{r,0.05}\subset F_{r,0.10}\subset F_{r,0.20}\). Road Failure Indicator equals one for units in \(F_{r,p}\), and Road Available equals zero for those units in that replicate state. One reproducible replicate is displayed in Nested Random Road Failure Realizations.

The required Spatially Clustered sensitivity draws seeded units and expands through network-adjacent units until the same failed-unit counts are reached. Hazard Exposure Class, Road State, Road Category, and Emergency Route Membership describe where failures and estimated importance concentrate; they do not alter the primary uniform assignment probability. Any hazard-weighted assignment must be separately labelled and cannot be presented as an empirical earthquake-failure probability.

### Estimands and Evidence Chain

The primary grid estimand is Timely Access Probability after combining replicate-specific Dispatch Travel Time and Hospital Transport Time. The primary system estimand is the Monte Carlo distribution of Total Population retaining 30-minute access. The primary hospital estimands are Hospital Assignment Probability and the distribution of Hospital Catchment Population. The primary road estimand is Road Failure Importance: the difference in expected population-weighted 30-minute access between randomized states in which a Road Failure Unit ID is available and failed, evaluated within Failure Rate and Random Failure Model. Road Importance Standard Error, Confidence Interval, effective failed and available replicate counts, Rank Stability, and Monte Carlo Convergence Status determine whether ranking is supportable.

| research question | identifying contrast or allocation | principal variables | planned evidence | interpretation |
|---|---|---|---|---|
| Grid emergency-access reliability | Nested 5%, 10%, and 20% Road Failure Indicator states within Simulation Replicate | Dispatch Travel Time, Hospital Transport Time, Total Emergency Access Time, Timely Access Probability, P90 Emergency Access Time | Grid Emergency Access Reliability; Emergency Access Reliability by Failure Rate and Threshold | Full-network reliability under the declared random-failure distribution. |
| Distributional reliability | Replicate outcomes aggregated with total and older-population weights and Municipality Name | Population Losing Timely Access, Older Population Losing Timely Access, Total Population, Population Age 65+, Population Age 75+, Population Age 85+ | Population Coverage under Random Road Failure; Municipal Monte Carlo Reliability | Spatial and demographic heterogeneity, not individual clinical risk. |
| Hospital service reliability | Replicate-specific nearest feasible hospital assignment and population catchment | Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability | Hospital Service Reliability under Random Road Failure; Hospital Service Reliability | Road-supported service stability; capacity weighting remains sensitivity analysis. |
| Road failure importance | Randomized conditional difference between Road Failure Indicator states | Road Failure Unit ID, Road Failure Importance, Road Importance Standard Error, Confidence Interval | 100 m Road Segment Failure Importance; Top Road Segment Effects and Uncertainty; Priority 100 m Road Segments | Importance conditional on failure rate, assignment model, sample size, and segmentation. |
| Robustness and convergence | Uniform versus clustered failures and replicate checkpoints | Random Failure Model, Simulation Replicate, Rank Stability, Monte Carlo Convergence Status | Failure-Model Sensitivity and Monte Carlo Convergence; Road-Importance Stability and Convergence | Priority evidence is supportable only when estimates and ranks stabilize. |

### Identification and Interpretation Limits

- The analysis is cross-sectional and simulation-based. It cannot establish that a road failed, that restoring it would cause the estimated real-world benefit, or that travel time equals observed ambulance response time.
- Assumed Speed (km/h) represents routing impedance and excludes dispatch delay, vehicle availability, on-scene time, congestion, and emergency driving behaviour not represented in the data.
- Hospital Role Weight and Hospital Capacity Weight do not measure clinical emergency capacity. The unweighted Operational Hospital Set is primary; weighted results are labelled sensitivity analyses.
- Older-population outcomes use their disclosure-group analysis units. They are not imputed to 125 m meshes, so fine-scale total-population and older-population results have different spatial support.
- Uniform independent spatial sampling is a benchmark, not an engineering earthquake model. Spatially clustered failure is mandatory sensitivity analysis.
- A 100 m unit makes exposure scale comparable but can create sparse conditional samples and adjacent fragments of one operational road. Publication rankings must report uncertainty and may aggregate contiguous high-importance units without recomputing their unit-level estimates.
- A disconnected result remains unreachable. It is not assigned an arbitrary finite time for reliability or timely-access calculations.

## 6. Main Estimation Framework

### 6.1 Replicate-Specific Road Graph and Impedance

For Simulation Replicate \(r\), Failure Rate \(p\), and Random Failure Model \(g\), define the available graph as

\[
G_{r,p,g} = (V,E_{r,p,g}), \qquad
E_{r,p,g} = \left\{e \in E : Z_{e,r,p,g}=0\right\}.
\]

Here, \(G_{r,p,g}\) is the replicate-specific road graph, \(V\) is the set of grade-aware road and virtual connector nodes, \(E\) is the complete set of Network Analysis Eligible Road Failure Unit ID values, \(E_{r,p,g}\) is the available subset, and \(Z_{e,r,p,g}\) is Road Failure Indicator for unit \(e\). Baseline uses \(Z_{e,0}=0\) for every eligible unit.

The travel-time impedance for available edge \(e\) under speed sensitivity multiplier \(m\) is

\[
c_e(m) = \frac{60 L_e}{1000 m v_e}.
\]

Here, \(c_e(m)\) is unit travel time in minutes, \(L_e\) is Road Length (m), \(v_e\) is Assumed Speed (km/h), and \(m\) is the speed multiplier. The primary value is \(m=1.0\); \(0.8\) and \(1.2\) are sensitivities. Baseline Edge Travel Time (min) equals \(c_e(1.0)\).

For a snapped dispatch base, demand unit, or hospital \(x\), connector time is

\[
q_x(m) = \frac{60 d_x}{1000 m v_{e(x)}}.
\]

Here, \(q_x(m)\) is connector time in minutes, \(d_x\) is Network Snap Distance (m), and \(v_{e(x)}\) is Assumed Speed (km/h) on the Road Failure Unit ID to which connector \(x\) is attached. If that unit fails, the connector is unavailable in that replicate state. The shortest road-network time between virtual connector positions \(u\) and \(v\) is denoted by \(d_{r,p,g}(u,v;m)\). If no path exists, the time is infinite and the unit is reported as disconnected.

### 6.2 Two-Stage Emergency Access

For analysis unit \(i\), replicate-specific ambulance dispatch time is

\[
D_{i,r,p,g}(m) = \min_{b \in B_{r,p,g}} \left\{q_b(m) + d_{r,p,g}(b,i;m) + q_i(m)\right\}.
\]

Here, \(D_{i,r,p,g}(m)\) is Dispatch Travel Time, \(i\) indexes Analysis Unit ID, \(b\) indexes Dispatch Base Node ID, and \(B_{r,p,g}\) is the set of accepted candidate dispatch bases whose access unit remains available.

The second-stage hospital transport time is

\[
H_{i,r,p,g}(m) = \min_{h \in H_{r,p,g}} \left\{q_i(m) + d_{r,p,g}(i,h;m) + q_h(m)\right\}.
\]

Here, \(H_{i,r,p,g}(m)\) is Hospital Transport Time, \(h\) indexes Hospital Node ID, and \(H_{r,p,g}\) is the Operational Hospital Set whose access units remain available. Assigned Hospital is the minimizing hospital, with deterministic identifier ordering used to break exact ties.

Total two-stage access time is

\[
T_{i,r,p,g}(m) = D_{i,r,p,g}(m) + H_{i,r,p,g}(m).
\]

Here, \(T_{i,r,p,g}(m)\) is Total Emergency Access Time. This specification counts the demand connector once when the ambulance reaches the grid and once when it returns to the road for hospital transport. Access Time Increase is \(T_{i,r,p,g}(m)-T_{i,0}(m)\) when both times are finite. Newly disconnected units are reported separately and are not assigned an arbitrary finite increase.

Each replicate state requires one multi-source shortest-path calculation from all available dispatch bases and one labelled multi-source calculation from all available eligible hospitals. This produces the complete two-stage outcome without estimating a separate shortest path for every origin-facility pair.

### 6.3 Timely Coverage and Distributional Loss

For Timely Access Threshold (min) \(\tau\), timely status is

\[
I_{i,r,p,g,\tau}(m) = \mathbf{1}\left\{T_{i,r,p,g}(m) \leq \tau\right\},
\qquad \tau \in \{15,30,45\}.
\]

Here, \(I_{i,r,p,g,\tau}(m)\) is Timely Access Status and \(\mathbf{1}\{\cdot\}\) is the indicator function. An infinite Total Emergency Access Time has status zero.

For \(R_g\) executed replicates of model \(g\), grid-level Timely Access Probability is

\[
\widehat{P}_{i,p,g,\tau}(m)
=
\frac{1}{R_g}\sum_{r=1}^{R_g} I_{i,r,p,g,\tau}(m).
\]

Here, \(\widehat{P}_{i,p,g,\tau}(m)\) is Timely Access Probability. The primary threshold is \(\tau=30\); \(15\) and \(45\) are prespecified complementary thresholds.

P90 Emergency Access Time is the empirical extended-real quantile

\[
\widehat{T}^{90}_{i,p,g}(m)
=
\operatorname{Quantile}_{0.90}
\left\{T_{i,r,p,g}(m):r=1,\ldots,R_g\right\}.
\]

Here, \(\widehat{T}^{90}_{i,p,g}(m)\) is P90 Emergency Access Time. If at least 10% of replicate outcomes are disconnected, the P90 is reported as unreachable rather than converted to a finite cap.

Replicate-specific covered population and population losing baseline timely access are

\[
A_{r,p,g,\tau}(m)
=
\sum_i w_i I_{i,r,p,g,\tau}(m),
\qquad
L_{r,p,g,\tau}(m)
=
\sum_i w_i I_{i,0,\tau}(m)
\left[1-I_{i,r,p,g,\tau}(m)\right].
\]

Here, \(A_{r,p,g,\tau}(m)\) is covered population, \(L_{r,p,g,\tau}(m)\) is Population Losing Timely Access, and \(w_i\) is Total Population for the primary mesh analysis. Older Population Losing Timely Access uses Population Age 65+, Population Age 75+, or Population Age 85+ on disclosure-group units without reallocating those counts to 125 m grids.

Municipal Monte Carlo Reliability applies the same expressions after restricting \(i\) to Municipality Code \(j\). It reports the mean and P5, P50, and P95 of replicate-level coverage, Timely Access Probability aggregated with valid population weights, P90 Emergency Access Time, disconnection frequency, and Rank Stability. The five Kumamoto City wards remain separate published units. Grid Emergency Access Reliability maps \(\widehat{P}_{i,p,g,30}(1.0)\) and \(\widehat{T}^{90}_{i,p,g}(1.0)\); Population Coverage under Random Road Failure displays the replicate distributions of \(A_{r,p,g,\tau}(1.0)\) and \(L_{r,p,g,\tau}(1.0)\).

### 6.4 Hospital Assignment and Service Reliability

Let \(h^*_{i,r,p,g}(m)\) be Assigned Hospital, the eligible hospital attaining the minimum in Section 6.2 when a finite hospital path exists. Grid-to-hospital assignment probability is

\[
\widehat{\pi}_{i,h,p,g}(m)
=
\frac{1}{R_g}
\sum_{r=1}^{R_g}
\mathbf{1}\left\{h^*_{i,r,p,g}(m)=h\right\}.
\]

Here, \(\widehat{\pi}_{i,h,p,g}(m)\) is Hospital Assignment Probability for demand unit \(i\) and hospital \(h\). The probabilities across hospitals sum to the probability that unit \(i\) has a finite hospital path; they need not sum to one when disconnection occurs.

Replicate-specific hospital catchment population is

\[
C_{h,r,p,g}(m)
=
\sum_i w_i
\mathbf{1}\left\{h^*_{i,r,p,g}(m)=h\right\}.
\]

Here, \(C_{h,r,p,g}(m)\) is Hospital Catchment Population and \(w_i\) is Total Population in the primary analysis. Hospital Service Reliability reports its mean, standard deviation, P5, P50, and P95 across replicates, the frequency of a zero catchment, and the population-weighted average of \(\widehat{\pi}_{i,h,p,g}(m)\).

Hospital Service Reliability under Random Road Failure maps these quantities separately for 5%, 10%, and 20% failure under the Uniform Random model. The primary hospital analysis assigns equal Hospital Role Weight to every Eligible Emergency Hospital. Hospital Capacity Weight and prespecified emergency-role weights are separately labelled sensitivities; missing capacity values are not imputed and cannot alter the primary unweighted assignment.

### 6.5 Randomized Road Failure Importance

For the primary threshold \(\tau=30\), define replicate-level system value

\[
Y_{r,p,g}(m)
=
\sum_i w_i I_{i,r,p,g,30}(m).
\]

Here, \(Y_{r,p,g}(m)\) is Total Population completing the two-stage chain within 30 minutes. For Road Failure Unit ID \(e\), let \(R^{0}_{e,p,g}\) and \(R^{1}_{e,p,g}\) denote replicate sets in which \(e\) is available and failed. Road Failure Importance is

\[
\widehat{\theta}_{e,p,g}(m)
=
\frac{1}{|R^{0}_{e,p,g}|}
\sum_{r \in R^{0}_{e,p,g}}Y_{r,p,g}(m)
-
\frac{1}{|R^{1}_{e,p,g}|}
\sum_{r \in R^{1}_{e,p,g}}Y_{r,p,g}(m).
\]

Here, \(\widehat{\theta}_{e,p,g}(m)\) is Road Failure Importance. A positive value means that system coverage is higher, on average, when unit \(e\) is available. Because each failure set has a fixed total size, this is a randomized conditional importance under the declared assignment distribution, not the isolated effect of removing only \(e\).

The difference-in-means Road Importance Standard Error is

\[
\widehat{SE}_{e,p,g}
=
\left[
\frac{s^2_{0,e,p,g}}{|R^{0}_{e,p,g}|}
+
\frac{s^2_{1,e,p,g}}{|R^{1}_{e,p,g}|}
\right]^{1/2}.
\]

Here, \(s^2_{z,e,p,g}\) is the sample variance of \(Y_{r,p,g}(1.0)\) within Road Failure Indicator state \(z\). The primary 95% Confidence Interval is \(\widehat{\theta}_{e,p,g}\pm1.96\widehat{SE}_{e,p,g}\); a replicate bootstrap is reported when the pilot shows material non-normality.

Secondary importance outcomes replace \(w_i\) with Population Age 65+ on its valid support or replace \(Y\) with a hospital-specific replicate catchment. The 100 m Road Segment Failure Importance maps every estimable unit. Top Road Segment Effects and Uncertainty and Priority 100 m Road Segments report the top 20 at each Failure Rate with failed and available replicate counts, uncertainty, Route Name, and Rank Stability. Contiguous high-importance units may be grouped for display, but their unit-level estimates and identifiers remain traceable.

### 6.6 Monte Carlo Precision, Ranking, and Convergence

The primary Uniform Random experiment targets \(R_g=1000\) replicates, each containing nested 5%, 10%, and 20% states. The implementation first runs a 100-replicate pilot. Target checkpoints are \(100\), \(250\), \(500\), \(750\), and \(1000\) completed replicates. Every checkpoint uses the prefix of the same seeded replicate sequence so changes reflect added information rather than a different sample.

For a scalar replicate outcome \(X_r\), the Monte Carlo standard error of its mean is

\[
\widehat{SE}\left(\overline{X}\right)
=
\frac{s_X}{\sqrt{R_g}},
\]

where \(s_X\) is the replicate sample standard deviation. Quantile uncertainty uses a replicate bootstrap with deterministic seeds. Grid probabilities use binomial standard errors as diagnostics and replicate bootstrap intervals for mapped summaries when spatial aggregation is involved.

Rank Stability is evaluated from:

- top-20 Jaccard overlap between adjacent replicate checkpoints;
- absolute rank changes for units appearing in either adjacent top-20 set;
- Road Failure Importance and Confidence Interval stability;
- effective failed and available replicate counts for every reported road unit.

Monte Carlo Convergence Status is met for a Failure Rate and Random Failure Model only when all of the following hold at the final two checkpoints:

1. the population-weighted 30-minute coverage mean changes by no more than 0.5 percentage points;
2. its 95% Confidence Interval half-width is no more than 0.5 percentage points;
3. top-20 road Jaccard overlap is at least 0.80;
4. median absolute rank change within the union of the two top-20 sets is no more than two;
5. every reported top-20 unit has at least 30 failed and 30 available observations.

These are planning thresholds subject to the 100-replicate pilot. Any revision must be documented before inspecting the full 1,000-replicate ranking. Failure to converge requires additional replicates, coarser contiguous-road aggregation, or an explicit inconclusive result; it does not permit publishing an unstable ranking.

### 6.7 Computational Implementation and Robustness

The full Uniform Random target comprises 3,000 failed-network states and at least 6,000 multi-source shortest-path calculations. Rebuilding Python object graphs inside every state is not acceptable for the full experiment. The implementation must store topology and impedance once in compact arrays, apply Road Failure Indicator as an edge-availability mask, use a compiled shortest-path backend, and parallelize independent Simulation Replicate values. Every output retains Random Failure Model, Failure Rate, Simulation Replicate, and deterministic seed provenance.

The 100-replicate pilot benchmarks graph preparation, failure-mask generation, two-stage routing, result aggregation, memory use, and checkpoint reproducibility. The Spatially Clustered model is piloted separately and targets 1,000 replicates when runtime and convergence permit; otherwise its executed replicate count and wider uncertainty are explicit.

Required robustness and failure-mode analyses are:

- Assumed Speed (km/h) multipliers of \(0.8\), \(1.0\), and \(1.2\).
- Timely Access Threshold (min) values of \(15\), \(30\), and \(45\).
- Total Population versus Population Age 65+, Population Age 75+, and Population Age 85+ weighting on their valid analysis units.
- Primary unweighted Operational Hospital Set versus clearly labelled hospital-role and complete-case Hospital Capacity Weight sensitivities.
- Failure Rate values \(0.05\), \(0.10\), and \(0.20\), with nested ordering verified within every Simulation Replicate.
- Uniform Random versus Spatially Clustered Random Failure Model.
- Unit-level estimates versus contiguous aggregation of adjacent high-importance 100 m units for interpretation.
- Road Importance Standard Error, Confidence Interval, Rank Stability, effective conditional sample sizes, and Monte Carlo Convergence Status.
- Explicit counts and population totals for failed network snaps, baseline disconnections, and scenario-induced disconnections.

The framework fails to support priority claims if baseline routing is not stable, nested failures do not produce ordered aggregate deterioration beyond Monte Carlo uncertainty, the optimized pilot cannot reproduce the validated baseline, effective conditional samples are inadequate, confidence intervals remain too wide, road ranks do not converge, or uniform and clustered models imply incompatible priority sets without an interpretable mechanism.

## 7. Analytical Workflow

| step | variables used | formula or model used | generated figure/table title | theory or claim evaluated | support status before estimation |
|---|---|---|---|---|---|
| 1. Validate the 100 m network and study population | Road Edge ID, Road Failure Unit ID, Road Length (m), From Node ID, To Node ID, Network Component ID, Network Analysis Eligible, Network Snap Distance (m), Candidate Dispatch Base, Eligible Emergency Hospital | Section 6.1 topology, length-cap, component, connector, and completeness checks | Emergency Care Network and Population Demand; Simulation and Network Descriptive Summary | The complete ambulance chain can be represented on standardized failure units. | Supported only if all units are at most 100 m, identifiers are unique, connectors are valid, and exclusions are explicit. |
| 2. Reproduce baseline two-stage access | Baseline Edge Travel Time (min), Dispatch Base Node ID, Demand Node ID, Hospital Node ID, Dispatch Travel Time, Hospital Transport Time, Total Emergency Access Time | Section 6.2 baseline graph with \(m=1.0\) | Baseline Two-Stage Emergency Travel Time | Baseline geographic access can be decomposed into dispatch and hospital-transport stages. | Supported only if the optimized engine reproduces the validated baseline and disconnected population remains explicit. |
| 3. Generate nested random failures | Road Failure Unit ID, Failure Rate, Simulation Replicate, Road Failure Indicator, Random Failure Model, Road Available | Section 5 nested random ordering and clustered expansion | Nested Random Road Failure Realizations; Simulation and Network Descriptive Summary | Increasing road failure can be compared within paired replicate draws. | Supported only if exact failed counts, nesting, deterministic seeds, and model labels pass validation. |
| 4. Compute replicate-level emergency access | Dispatch Travel Time, Hospital Transport Time, Total Emergency Access Time, Assigned Hospital, Failure Rate, Simulation Replicate | Sections 6.1-6.2 two multi-source shortest-path calculations per failed-network state | Emergency Access Reliability by Failure Rate and Threshold | Full rerouting captures alternative paths after simultaneous failures. | Inconclusive until the 100-replicate performance and baseline-reproduction pilot passes. |
| 5. Estimate grid and population reliability | Timely Access Threshold (min), Timely Access Status, Timely Access Probability, P90 Emergency Access Time, Total Population, Population Age 65+, Population Age 75+, Population Age 85+ | Section 6.3 reliability, quantile, coverage, and loss equations | Grid Emergency Access Reliability; Population Coverage under Random Road Failure; Emergency Access Reliability by Failure Rate and Threshold; Municipal Monte Carlo Reliability | Random road failure produces spatially and demographically heterogeneous emergency-access risk. | Supported only with stable Monte Carlo intervals and valid population support. |
| 6. Estimate hospital service reliability | Hospital Name, Eligible Emergency Hospital, Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability, Hospital Role Weight, Hospital Capacity Weight | Section 6.4 assignment-probability and catchment-distribution equations | Hospital Service Reliability under Random Road Failure; Hospital Service Reliability | Hospital service roles depend on road-supported reachability and substitution. | Supported for unweighted eligible hospitals when assignment and catchment estimates converge; weighted results remain sensitivity analyses. |
| 7. Estimate road failure importance | Road Failure Unit ID, Route Name, Road Failure Indicator, Road Failure Importance, Road Importance Standard Error, Confidence Interval | Section 6.5 randomized conditional importance and uncertainty equations | 100 m Road Segment Failure Importance; Top Road Segment Effects and Uncertainty; Priority 100 m Road Segments | Road units differ in their contribution to maintaining population-weighted timely access. | Supported only for units with adequate failed and available observations and uncertainty narrow enough for ranking. |
| 8. Evaluate rank stability and convergence | Simulation Replicate, Failure Rate, Random Failure Model, Road Failure Importance, Rank Stability, Monte Carlo Convergence Status | Section 6.6 checkpoint, confidence-interval, and top-set stability rules | Failure-Model Sensitivity and Monte Carlo Convergence; Road-Importance Stability and Convergence | Priority evidence must remain stable as information accumulates. | Supported only when all declared convergence criteria pass; otherwise rankings are inconclusive or require more replicates. |
| 9. Evaluate robustness | Assumed Speed (km/h), Timely Access Threshold (min), Hospital Role Weight, Hospital Capacity Weight, Hazard Exposure Class, Road State, Random Failure Model | Section 6.7 speed, threshold, population-support, hospital-rule, and clustered-failure sensitivities | Failure-Model Sensitivity and Monte Carlo Convergence; Road-Importance Stability and Convergence | Principal reliability and road-priority conclusions should not depend on one arbitrary modelling choice. | Partially supported when mechanisms explain differences; unsupported when plausible specifications reverse priorities without explanation. |

### Evidence Checkpoints

1. Network checkpoint: stop if Road Failure Unit ID is not unique, any unit exceeds 100 m, topology or connectors are invalid, or baseline exclusions are not fully reported.
2. Engine checkpoint: stop before the full experiment if the optimized engine cannot reproduce baseline travel times and hospital assignments within numerical tolerance.
3. Randomization checkpoint: stop if failed counts are incorrect, 5%, 10%, and 20% sets are not nested within Simulation Replicate, or seeds are not reproducible.
4. Pilot checkpoint: use 100 replicates to report runtime, memory, effective conditional road samples, system-outcome uncertainty, and preliminary rank stability before authorizing 1,000 replicates.
5. Reliability checkpoint: treat the failure mechanism as weak or misspecified if nested severity does not produce ordered aggregate deterioration beyond Monte Carlo uncertainty.
6. Equity checkpoint: report total- and older-population results on their own valid spatial supports; do not claim 125 m older-population precision.
7. Hospital checkpoint: keep unweighted Eligible Emergency Hospital assignment primary; capacity- or role-weighted results remain labelled sensitivities.
8. Road-priority checkpoint: do not publish definitive ranks when effective samples, Confidence Interval, Rank Stability, or Monte Carlo Convergence Status fail the Section 6.6 requirements.
9. Failure-model checkpoint: explain and report priority differences between Uniform Random and Spatially Clustered models rather than averaging incompatible rankings.

## 8. Figure and Table Plan

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---|---|---|
| Emergency Care Network and Population Demand | Shows the spatial structure of population demand, candidate ambulance dispatch bases, eligible emergency hospitals, and the road network. | map | 3 | Geometry, Total Population, Population Age 65+, Candidate Dispatch Base, Eligible Emergency Hospital, Emergency Road Class | done |
| Baseline Two-Stage Emergency Travel Time | Decomposes baseline ambulance dispatch, hospital transport, and total two-stage emergency travel time. | map | 3 | Geometry, Candidate Dispatch Base, Eligible Emergency Hospital, Road Type, Width Category | done |
| Nested Random Road Failure Realizations | Shows one reproducible Monte Carlo draw with nested 5%, 10%, and 20% failed 100 m road units, so increasing failure severity can be interpreted directly. | map | 3 | Geometry, Road Failure Unit ID, Failure Rate, Simulation Replicate, Road Failure Indicator, Random Failure Model, Road Available | pending |
| Grid Emergency Access Reliability | Maps each grid's probability of completing the fire-station-to-grid-to-hospital chain within 30 minutes and its P90 total emergency access time under 5%, 10%, and 20% road failure. | map | 6 | Geometry, Failure Rate, Simulation Replicate, Total Emergency Access Time, Timely Access Threshold (min), Timely Access Probability, P90 Emergency Access Time, Total Population | pending |
| Population Coverage under Random Road Failure | Shows the Monte Carlo distributions of population and older population retaining 15-, 30-, and 45-minute emergency access at each road-failure level. | violin + interval | 3 | Failure Rate, Simulation Replicate, Timely Access Threshold (min), Timely Access Status, Total Population, Population Age 65+, Population Losing Timely Access, Older Population Losing Timely Access | pending |
| Hospital Service Reliability under Random Road Failure | Maps the stability of hospital assignment and service population across 1,000 replicates at 5%, 10%, and 20% road failure. | map | 3 | Geometry, Hospital Name, Eligible Emergency Hospital, Assigned Hospital, Hospital Catchment Population, Hospital Assignment Probability, Failure Rate, Simulation Replicate | pending |
| 100 m Road Segment Failure Importance | Maps the expected loss of 30-minute population-weighted emergency access associated with failure of each 100 m road unit at 5%, 10%, and 20% network failure. | map | 3 | Geometry, Road Failure Unit ID, Route Name, Failure Rate, Road Failure Indicator, Road Failure Importance, Total Population, Population Age 65+ | pending |
| Top Road Segment Effects and Uncertainty | Reports the top 20 road-failure units at each failure level with effect estimates, uncertainty intervals, and stable route identifiers. | forest | 3 | Road Failure Unit ID, Route Name, Failure Rate, Road Failure Importance, Road Importance Standard Error, Confidence Interval, Rank Stability | pending |
| Failure-Model Sensitivity and Monte Carlo Convergence | Compares uniform and spatially clustered failures and shows whether access and road-importance estimates stabilize as replicates increase from the pilot to 1,000. | line | 4 | Random Failure Model, Failure Rate, Simulation Replicate, Timely Access Probability, Road Failure Importance, Rank Stability, Monte Carlo Convergence Status | pending |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Simulation and Network Descriptive Summary | Summarizes the 100 m road-failure network, population grids, dispatch bases, hospitals, randomization design, and replicate counts. | approximately 30 | 7 | One network, demand, facility, or simulation-design indicator. | Count, length, total, mean, standard deviation, minimum, and maximum as applicable. | pending |
| Emergency Access Reliability by Failure Rate and Threshold | Compares population-weighted emergency-access reliability across three failure rates and three timely-access thresholds. | 9 | 12 | One Failure Rate and Timely Access Threshold (min) combination. | Replicates, mean coverage, standard error, P5, P50, P95, population loss, older-population loss, and disconnection measures. | pending |
| Municipal Monte Carlo Reliability | Reports geographic heterogeneity in simulated emergency-access reliability. | 147 | 12 | One Municipality Name and Failure Rate combination. | Population, older population, Timely Access Probability, P90 Emergency Access Time, coverage loss, uncertainty, and rank. | pending |
| Hospital Service Reliability | Reports hospital assignment and service-population stability under random road failure. | approximately 225 | 12 | One eligible hospital and Failure Rate combination. | Hospital Name, hospital role, mean catchment population, Hospital Assignment Probability, catchment variability, P5, P50, P95, and disconnection frequency. | pending |
| Priority 100 m Road Segments | Provides uncertainty-aware road-failure importance estimates for the top road units at each failure rate. | approximately 60 | 14 | One top-ranked Road Failure Unit ID and Failure Rate combination. | Route Name, location, Road Failure Importance, Road Importance Standard Error, Confidence Interval, total- and older-population effects, hospital effect, rank, and Rank Stability. | pending |
| Road-Importance Stability and Convergence | Tests whether road-importance rankings and system-access estimates remain stable across replicate counts and random-failure models. | approximately 60 | 12 | One high-ranked road unit, Failure Rate, and Random Failure Model combination. | Estimates at 100, 250, 500, 750, and 1,000 replicates, rank range, Rank Stability, and Monte Carlo Convergence Status. | pending |
