# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Central Research Question

- Research question: Under plausible road-disruption and restoration scenarios, which road corridors and eligible emergency hospitals have the greatest marginal contribution to maintaining population-weighted timely ambulance access across Kumamoto Prefecture?
- Why it matters: Emergency road-protection and restoration resources are limited, so decision-makers need priorities that reflect the complete ambulance chain and the populations and hospitals that each road helps keep reachable.
- Data support currently visible: The processed evidence includes a 125 m population mesh, age-specific population measures, candidate ambulance dispatch bases, eligible emergency hospitals and hospital roles, road geometry and classifications, municipal boundaries, and landslide-warning information for scenario construction.
- Key readable variables or data scope: Geometry, Total Population, Population Age 65+, Population Age 75+, Candidate Dispatch Base, Eligible Emergency Hospital, Hospital Name, Total Beds, Emergency Road Class, Road Type, Route Name, Hazard Type, Warning Zone Class, and Municipality Name.
- What would verify it: A routable network must produce stable baseline and disrupted two-stage travel times, and direct Monte Carlo Shapley estimates must converge sufficiently to distinguish high-value corridors and hospitals across scenarios.
- What would falsify or weaken it: The question would be weakened if network topology cannot be validated, plausible disruption scenarios do not materially change emergency accessibility, or corridor and hospital rankings remain too unstable for defensible prioritization.
- Required next feasibility check: Validate network construction, travel-time assumptions, corridor aggregation, hospital eligibility, scenario definitions, and the computational feasibility and convergence of direct Shapley estimation.

### Supporting Research Questions

The four supporting questions deepen the central applied question through system performance, equity, hospital redundancy, and methodological robustness.

#### Emergency Accessibility under Road Disruption

- Role relative to central point: deepen the system-performance evidence.
- Research question: How do Low, Central, and High road-disruption scenarios change ambulance dispatch time, incident-to-hospital transport time, total emergency access time, and the population reachable within 15, 30, and 45 minutes?
- Why it matters: Road value can only be interpreted after establishing how disruption changes the two stages of emergency response and the resulting timely-access coverage.
- Data support currently visible: Candidate dispatch bases, eligible hospitals, detailed road geometry and classifications, population meshes, and hazard-zone information provide the required origin, intermediate, destination, network, demand, and scenario inputs.
- Key readable variables or data scope: Geometry, Candidate Dispatch Base, Eligible Emergency Hospital, Road Type, Width Category, Road State, Hazard Type, Warning Zone Class, and Total Population.
- What would verify it: Valid shortest paths and consistent scenario rules should yield reproducible changes in stage-specific travel times and timely-access population coverage.
- What would falsify or weaken it: The evidence would weaken if large shares of origins remain disconnected in the baseline network, speed assumptions dominate results, or disruption scenarios cannot be distinguished from baseline conditions.
- Required next feasibility check: Confirm planarized network connectivity, routing direction and speed rules, fire-station and hospital snapping tolerances, and the defensibility of the three disruption intensities.

#### Distributional Effects on Older Populations and Municipalities

- Role relative to central point: assess spatial and demographic heterogeneity.
- Research question: Which municipalities and older-population groups experience the largest losses of timely emergency access under each road-disruption scenario?
- Why it matters: A restoration strategy based only on total population may overlook municipalities and age groups with greater emergency vulnerability and fewer alternative routes.
- Data support currently visible: The population evidence includes total population and age 65+, 75+, and 85+ measures, while administrative geometry supports municipal aggregation.
- Key readable variables or data scope: Geometry, Municipality Name, Total Population, Population Age 65+, Population Age 65+ Share, Population Age 75+, Population Age 75+ Share, Population Age 85+, and Population Age 85+ Share.
- What would verify it: Scenario results should identify reproducible differences in coverage loss, access-time increase, and restoration benefit across municipalities and age groups.
- What would falsify or weaken it: The distributional claim would weaken if age-specific population disclosure or aggregation prevents reliable local estimates, or if subgroup rankings are highly threshold-dependent.
- Required next feasibility check: Validate suppressed-mesh handling, municipal assignment, population-weighted aggregation, and sensitivity to 15-, 30-, and 45-minute thresholds.

#### Hospital Value, Catchment Reallocation, and Redundancy

- Role relative to central point: identify the hospital-side mechanism and redundancy structure.
- Research question: How much marginal emergency-access value does each eligible hospital provide, and how do road disruptions change hospital catchments, potential demand, and access to alternative hospitals?
- Why it matters: A hospital with many beds is not necessarily the hospital with the greatest marginal network value; location, road dependence, role, and substitution possibilities also determine its contribution.
- Data support currently visible: Current hospital locations, emergency and disaster designations, tertiary and rotation roles, bed measures, and matched healthcare-plan records support hospital eligibility and sensitivity analyses.
- Key readable variables or data scope: Geometry, Hospital Name, Eligible Emergency Hospital, Emergency Designated, Disaster Base Designation, Tertiary Emergency Hospital, Rotation Hospital, Total Beds, General Beds, Match Status, and Name Match Score.
- What would verify it: Hospital-specific Shapley estimates, catchment changes, and alternative-hospital counts should consistently identify hospitals whose availability preserves substantial population-weighted timely access.
- What would falsify or weaken it: The interpretation would weaken if hospital-role reconciliation is unreliable, Total Beds is a poor proxy for emergency capacity, or estimated hospital values change radically under reasonable eligibility rules.
- Required next feasibility check: Resolve the remaining hospital-name review and rotation-hospital count discrepancy, define primary and sensitivity eligibility sets, and keep capacity-weighted results separate from unweighted coverage results.

#### Road Shapley Value and Ranking Robustness

- Role relative to central point: evaluate road prioritization and methodological robustness.
- Research question: Which candidate medical corridors have the highest direct Monte Carlo Shapley value, how do their contributions vary by hospital and disruption scenario, and can a SHAP surrogate reproduce the direct rankings when scaling is necessary?
- Why it matters: Road contributions are complementary and scenario-dependent, while the full road network is too large for naive enumeration; priority decisions therefore require both a defensible cooperative-game estimand and computational validation.
- Data support currently visible: Detailed road geometry, route and emergency-road classifications, population demand, candidate dispatch bases, eligible hospitals, and the confirmed road-hospital output plan support corridor screening and contribution analysis.
- Key readable variables or data scope: Geometry, Route Name, Route ID, Emergency Road Class, Road Type, Width Category, Candidate Dispatch Base, Hospital Name, Total Population, and Population Age 65+.
- What would verify it: Direct estimates should converge with acceptable Monte Carlo uncertainty, high-value corridors should remain reasonably stable across scenarios, and any surrogate should achieve low prediction error and small rank differences against direct estimates on a validation subset.
- What would falsify or weaken it: The method would weaken if corridor definitions drive the rankings, direct estimates fail to converge, interaction effects make individual attribution unstable, or the surrogate cannot reproduce direct values and rankings.
- Required next feasibility check: Define corridor players, pre-screen the feasible player set, select convergence criteria and uncertainty reporting, and specify direct-versus-surrogate validation metrics before estimation.

### Scope of Analysis

- Topics: Emergency medical accessibility, road-network disruption and restoration, ambulance dispatch, hospital reachability and redundancy, vulnerable-population coverage, cooperative-game valuation, and repair prioritization.
- Spatial scope: Kumamoto Prefecture, retaining necessary cross-boundary road connections and external-reference facilities only when they affect feasible emergency paths.
- Operational chain: Candidate fire-station ambulance dispatch base to incident or population mesh, followed by incident or mesh to eligible emergency hospital.
- Units of analysis: 125 m population mesh, candidate dispatch base, eligible emergency hospital, routable road segment or aggregated medical corridor, municipality, and disruption or restoration scenario.
- Period: A cross-sectional scenario study assembled from sources with reference years between 2012 and 2026; it is not a longitudinal before-and-after design.
- Scenario scope: Baseline plus Low, Central, and High road-disruption scenarios, followed by ordered restoration portfolios and sensitivity analyses.

### Study Design Declaration

- Research type: applied
- Study design: Applied computational network-accessibility and cooperative-game simulation study.
- Primary estimand: Scenario-specific marginal contribution of a road corridor or eligible hospital to population-weighted timely emergency access.
- Primary method: Direct Monte Carlo Shapley estimation; a machine-learning surrogate with SHAP attribution is permitted only for scaling and must be validated against direct estimates.
- Interpretation limit: Results are model-based, scenario-dependent planning evidence. They do not identify causal effects, prove that a road failed in an observed earthquake, measure actual ambulance response operations, or establish clinical emergency capacity from bed counts alone.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

Research type: applied
Section focus: Empirical context, practical problem, and cautious interpretation limits.

### Research Gap

- The practical gap is the absence of an integrated decision framework that links road disruption to the complete ambulance chain, population and older-population coverage, hospital substitution, and corridor-level restoration priority for Kumamoto Prefecture.
- A single-road removal score does not fully allocate value when roads work as complements or substitutes. The adopted Shapley framework addresses this planning gap by averaging each corridor's or hospital's marginal contribution across restoration coalitions and reporting scenario dependence and uncertainty.
- The current evidence supports scenario modelling rather than reconstruction of observed earthquake operations because verified event-specific closures, ambulance dispatch records, emergency-department capacity, and repair-time or repair-cost observations are not currently available.

### Conceptual Framework

- Hazard exposure and scenario assumptions determine which road corridors are unavailable or restorable.
- Road availability and network topology determine the feasible dispatch-base-to-incident and incident-to-hospital paths and their travel times.
- Stage-specific travel times determine timely emergency accessibility for the total and older populations and reshape hospital catchments and substitution options.
- Population-weighted timely accessibility defines the system value allocated to road corridors and hospitals through direct Monte Carlo Shapley estimation.
- Scenario-specific road, hospital, and road-hospital contributions inform continuity protection, restoration ranking, and budget-constrained portfolio comparisons.
- Equity enters through separate population weights and subgroup reporting rather than an unobserved clinical-risk score.
- Scope boundary: The framework represents geographic access and network support for emergency care, not ambulance availability, on-scene treatment time, hospital congestion, clinical quality, structural hospital damage, or patient outcomes.

### Problem Formulation

- Decision problem: Select road corridors for continuity protection or restoration so that the ambulance chain preserves the greatest population-weighted timely access to eligible emergency hospitals under a stated disruption scenario.
- Network inputs: Candidate Dispatch Base, Eligible Emergency Hospital, Geometry, Road Type, Width Category, Road State, Emergency Road Class, Hazard Type, and Warning Zone Class.
- Demand and equity inputs: Total Population and the available older-population counts and shares.
- Hospital inputs: Hospital Name, emergency and disaster roles, tertiary and rotation roles, and bed measures used only in explicit sensitivity specifications.
- Primary outcome family: Dispatch travel time, hospital transport time, total emergency access time, timely-access status, covered and uncovered population, hospital catchment allocation, and restoration benefit. These derived variables require definition and final-variable confirmation before estimation.
- Cooperative-game players: Pre-screened and aggregated medical road corridors for the road game and eligible hospitals for the hospital game. A hospital-specific road game provides the road-hospital contribution matrix.
- Primary comparison: Baseline versus Low, Central, and High disruption scenarios, followed by marginal restoration contributions and cumulative restoration portfolios.
- Robustness requirements: Alternative time thresholds, total versus older-population weights, hospital eligibility and capacity rules, corridor aggregation, scenario severity, Monte Carlo convergence, and direct-versus-surrogate agreement.
- Interpretation limit: Shapley values allocate the value of the specified model and coalition distribution. They are not intrinsic asset prices or causal effects, and cost-effectiveness claims require repair-cost or repair-time evidence that is not currently available.

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
| Connected Hospital Count | Connected Hospital Count | restoration benefit | Number of operational hospitals newly connected to relevant demand after restoration. | Difference in reachable operational-hospital count before and after restoration. | yes |
| Coverage Recovery | Coverage Recovery | restoration outcome | Share of disruption-induced timely-access loss recovered by restoration. | Constructed as Restored Population divided by Population Losing Timely Access before restoration when the denominator is positive. | yes |
| Demand Node ID | Demand Node Identifier | network connector | Identifier of the virtual road-network connector for a demand unit. | Assigned when the population centroid is within 250 m of an eligible road edge. | yes |
| Designation Date | Designation Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Direct-Surrogate Rank Difference | Direct-Surrogate Rank Difference | validation diagnostic | Difference between a candidate's rank under direct-network and surrogate-based Shapley estimates. | Computed for the validation subset with deterministic rank handling. | yes |
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
| Emergency Route Membership | Emergency Route Membership | network priority | Emergency transport road class associated with the nearest route alignment. | Assigned from the nearest emergency-route centreline within 30 m; otherwise coded None. | yes |
| External Reference | External Reference | source provenance | Indicator that a listed facility is retained as an out-of-prefecture reference rather than Kumamoto supply. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Facility Name | Facility Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
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
| Hospital Capacity Weight | Hospital Capacity Weight | hospital weight | Nonnegative hospital capacity weight used in weighted accessibility analyses. | Uses reported Bed Count without normalization during preprocessing; missing bed counts remain missing. | yes |
| Hospital Catchment Population | Hospital Catchment Population | hospital demand | Population assigned to a hospital under a specified scenario. | Sum of Total Population over analysis units for which that hospital is Assigned Hospital. | yes |
| Hospital Demand Change | Hospital Demand Change | hospital demand | Change in assigned hospital catchment population relative to baseline. | Scenario Hospital Catchment Population minus baseline Hospital Catchment Population. | yes |
| Hospital ID | Hospital Identifier | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Name | Hospital Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Name Kana | Hospital Name Kana | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Name Romanized | Hospital Name Romanized | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Hospital Node ID | Hospital Node Identifier | network connector | Identifier of the virtual road-network connector for an eligible emergency hospital. | Assigned when the hospital is within 150 m of an eligible road edge. | yes |
| Hospital Role Weight | Hospital Role Weight | hospital weight | Weight applied to a hospital's emergency-care role in weighted sensitivity analyses. | Initialized to 1.0 for the unweighted baseline; alternative role weights are estimated only in declared sensitivity specifications. | yes |
| Hospital Shapley Value | Hospital Shapley Value | hospital value output | Average marginal contribution of retaining an operational hospital to the declared emergency-access value function. | Estimated over hospital coalitions for the declared disruption scenario and outcome. | yes |
| Hospital Transport Time | Hospital Transport Time | accessibility outcome | Shortest network travel time from the demand unit to an operational eligible hospital. | Calculated on the same scenario-specific road graph after ambulance arrival. | yes |
| Households with Member Age 65+ | Households with Member Age 65+ | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Infectious Disease Beds | Infectious Disease Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Institution Type Code | Institution Type Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Insured Long-Term Care Beds | Insured Long-Term Care Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Latitude | Latitude | spatial index | Reported geographic coordinate. | Coerced to numeric and used to construct JGD2011 point geometry where applicable. | yes |
| Long-Term Care Beds | Long-Term Care Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Longitude | Longitude | spatial index | Reported geographic coordinate. | Coerced to numeric and used to construct JGD2011 point geometry where applicable. | yes |
| Marginal Restoration Benefit | Marginal Restoration Benefit | restoration outcome | Incremental emergency-access benefit from adding one restoration action to a selected set. | Difference in the declared restoration objective with and without the candidate edge or corridor. | yes |
| Match Status | Match Status | record linkage | Outcome category from reconciling the healthcare-plan hospital name to the MHLW hospital roster. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Matched Hospital Name | Matched Hospital Name | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Corridor ID | Medical Corridor Identifier | Shapley player | Identifier of a connected road-category subnetwork within one secondary mesh. | Aggregates edge-level players into spatially coherent candidates before the maximum 2,000-player Shapley screen. | yes |
| Medical Departments 1 | Medical Departments 1 | clinical service scope | First reported group of medical departments provided by the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Departments 2 | Medical Departments 2 | clinical service scope | Second reported group of medical departments provided by the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Departments 3 | Medical Departments 3 | clinical service scope | Third reported group of medical departments provided by the hospital. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Facility Class | Medical Facility Class | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Medical Facility Class Code | Medical Facility Class Code | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Mesh Code | Mesh Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Monte Carlo Permutations | Monte Carlo Permutations | estimation diagnostic | Number of sampled player permutations used for a Shapley estimate. | Recorded for every reported estimate and increased until the convergence rule or computation cap is reached. | yes |
| Municipality Code | Municipality Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Municipality Label | Municipality Label | administrative descriptor | Published municipality label associated with the record. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Municipality Name | Municipality Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Name Match Score | Name Match Score | record linkage | Normalized similarity score used to review hospital-name reconciliation. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Network Analysis Eligible | Network Analysis Eligible | sample definition | Indicator that a valid Standard Road edge or node is retained for network analysis. | Set to one for every valid Standard Road component; component IDs preserve disconnected-network status without deleting island demand. | yes |
| Network Component ID | Network Component Identifier | network topology | Identifier of the connected Standard Road subnetwork containing the edge or node. | Computed by union-find over grade-aware edge endpoints; disconnected island components are retained. | yes |
| Network Redundancy Value | Network Redundancy Value | restoration benefit | Gain in alternative feasible hospital paths or routes produced by restoration. | Measured from the increase in Alternative Hospital Count and declared path-redundancy sensitivity metrics. | yes |
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
| Priority Selection Frequency | Priority Selection Frequency | robustness outcome | Share of sensitivity specifications in which a road edge or corridor enters the priority set. | Number of specifications selecting the candidate divided by the total evaluated specifications. | yes |
| Psychiatric Beds | Psychiatric Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Reference Date | Reference Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Registration Date | Registration Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Restoration Rank | Restoration Rank | policy ranking | Ordinal rank of a road edge or corridor by restoration benefit under a declared objective. | Ranked within scenario and restoration scale using deterministic tie handling. | yes |
| Restoration Scale | Restoration Scale | policy constraint | Number of road edges or medical corridors restored in a policy scenario. | Primary policy constraint because empirical repair cost and duration data are not yet available. | yes |
| Restored Older Population | Restored Older Population | equity restoration benefit | Population age 65 or older regaining timely access after restoration. | Disclosure-group older population whose Timely Access Status returns from zero to one. | yes |
| Restored Population | Restored Population | restoration benefit | Population regaining timely access after a road edge or corridor is restored. | Difference in timely covered population before and after the specified restoration action. | yes |
| Road Available | Road Available | scenario state | Indicator that an edge is traversable in a specified network scenario. | Initialized to one for baseline; disruption and restoration scenarios update the indicator during estimation. | yes |
| Road Category | Road Category | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Category Code | Road Category Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Centerline Type | Road Centerline Type | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Centerline Type Code | Road Centerline Type Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Edge ID | Road Edge Identifier | network identifier | Unique identifier for a routable Standard Road edge. | Assigned deterministically after same-level noding and one-metre endpoint snapping in EPSG:6670. | yes |
| Road Length (m) | Road Length (m) | network impedance | Projected length of the routable edge in metres. | Calculated in JGD2011 / Japan Plane Rectangular CS II (EPSG:6670). | yes |
| Road Shapley Value | Road Shapley Value | primary explanatory output | Average marginal contribution of a road edge or medical corridor to the declared emergency-access value function. | Estimated over sampled player permutations after screening at most 2,000 candidate corridors. | yes |
| Road State | Road State | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road State Code | Road State Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Type | Road Type | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road Type Code | Road Type Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Road-Hospital Shapley Value | Road-Hospital Shapley Value | interaction output | Hospital-specific marginal contribution of a road edge or medical corridor to emergency-access value. | Estimated for screened road players and eligible hospitals using the declared conditional value function. | yes |
| Rotation Hospital | Rotation Hospital | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Route ID | Route Identifier | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Route Name | Route Name | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Scenario Priority Rank | Scenario Priority Rank | policy ranking | Scenario-specific ordinal priority of a road edge or corridor. | Computed separately for Low, Central, and High disruption scenarios. | yes |
| Secondary Mesh Code | Secondary Mesh Code | identifier/classification | Identifier or categorical code retained as a string or integer as appropriate. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Service Status | Service Status | service availability | Reported operating or service-availability status of the facility. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Shapley Convergence Status | Shapley Convergence Status | estimation diagnostic | Indicator or category reporting whether the prespecified Shapley convergence criterion is met. | Determined from stability of values, ranks, and Monte Carlo standard errors across permutation batches. | yes |
| Shapley Standard Error | Shapley Standard Error | estimation uncertainty | Monte Carlo standard error of an estimated Shapley value. | Calculated from permutation-level marginal contributions with the declared sampling design. | yes |
| Short Name | Short Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Short Name Kana | Short Name Kana | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Source Date | Source Date | temporal metadata | Reference, registration, opening, designation, or source date. | Parsed to a machine-readable date where the source format permits. | yes |
| Source Name | Source Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Special Warning Zone Pending | Special Warning Zone Pending | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Special Warning Zone Pending Code | Special Warning Zone Pending Code | disruption risk | Landslide warning-zone classification used for disruption scenarios. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Subprefecture Name | Subprefecture Name | descriptor | Human-readable identity or descriptive attribute. | Leading and trailing whitespace removed; missing values preserved. | yes |
| Suppressed Source Mesh Count | Suppressed Source Mesh Count | demand disclosure | Number of source meshes combined because population values were disclosure-suppressed. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Surrogate Prediction Error | Surrogate Prediction Error | validation diagnostic | Out-of-sample prediction error of a surrogate model for the direct network value function. | Computed on held-out coalitions using the prespecified loss metric. | yes |
| Tertiary Emergency Hospital | Tertiary Emergency Hospital | hospital supply | Hospital or medical-facility identity, classification, or role attribute. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Timely Access Status | Timely Access Status | primary outcome | Indicator that Total Emergency Access Time does not exceed the selected threshold. | Coded separately for each Disruption Scenario and Timely Access Threshold (min). | yes |
| Timely Access Threshold (min) | Timely Access Threshold (min) | accessibility threshold | Maximum total emergency access time defining timely service, in minutes. | Evaluated at the prespecified 15, 30, and 45 minute thresholds. | yes |
| To Node ID | To Node Identifier | network topology | Identifier of the second endpoint node of a routable edge. | Constructed from the endpoint coordinate and Vertical Level after one-metre snapping. | yes |
| Toll Category | Toll Category | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Toll Category Code | Toll Category Code | network | Road-segment classification or network descriptor used for routing and corridor prioritization. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Total Beds | Total Beds | hospital capacity | Reported hospital bed capacity for the stated bed category. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Total Emergency Access Time | Total Emergency Access Time | primary outcome | Two-stage emergency travel time from dispatch base through the demand unit to the assigned hospital. | Constructed as Dispatch Travel Time plus Hospital Transport Time. | yes |
| Total Households | Total Households | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Total Population | Total Population | demand | Population or household count/share for the represented spatial unit. | Retained under the confirmed cleaning rules without missing-value imputation or outlier transformation. | yes |
| Travel Time Reduction | Travel Time Reduction | restoration benefit | Population-weighted reduction in Total Emergency Access Time caused by restoration. | Computed as pre-restoration minus post-restoration total access time under the same disruption scenario. | yes |
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

This study uses an applied computational identification strategy. It identifies scenario-specific network dependence by holding population demand, dispatch-base locations, hospital locations, hospital eligibility, and baseline travel-speed rules fixed while changing only Road Available and, in declared sensitivity analyses, the speed multiplier, Timely Access Threshold (min), population weight, Operational Hospital Set, and hospital weighting rule. The contrast therefore isolates consequences within the specified network model; it does not identify a causal effect of an observed earthquake or actual restoration intervention.

The analytical chain is Candidate Dispatch Base to demand location to eligible emergency hospital. All valid Standard Road components marked by Network Analysis Eligible are retained, including disconnected island and remote components. From Node ID, To Node ID, Network Component ID, Road Length (m), and Baseline Edge Travel Time (min) define routing topology and impedance. Dispatch Base Node ID, Demand Node ID, and Hospital Node ID define virtual network connectors. Network Snap Distance (m) is incorporated as connector travel rather than treated as a reason to move an observation silently; units that fail the confirmed snap threshold remain explicit and are excluded only from network-time estimation, with their population reported.

### Baseline and Nested Disruption Contrasts

The baseline sets Road Available to one for every Network Analysis Eligible edge. The primary nested stress tests use transparent classifications rather than claiming observed failure:

- Low disruption makes edges in the Special Warning Zone Hazard Exposure Class unavailable.
- Central disruption makes edges in either the Warning Zone or Special Warning Zone Hazard Exposure Class unavailable.
- High disruption applies the Central rule and additionally makes Bridge or Elevated and Tunnel edges unavailable.

Emergency Route Membership is used for descriptive stratification, corridor screening, and priority interpretation, not as evidence that a road is physically less likely to fail. These nested scenarios support Emergency Access under Road Disruption Scenarios and Accessibility Loss by Disruption Scenario. Because Hazard Exposure Class is a susceptibility-screening input, scenario estimates are planning stress tests rather than event reconstruction.

### Estimands and Evidence Chain

The primary accessibility estimand is the scenario change in population-weighted Timely Access Status after combining Dispatch Travel Time and Hospital Transport Time. The primary road estimand is Road Shapley Value for Medical Corridor ID within a scenario-specific screened restoration game. The hospital estimand is Hospital Shapley Value for the Operational Hospital Set. Road-Hospital Shapley Value identifies which screened corridors support timely access to each hospital.

| research question | identifying contrast or allocation | principal variables | planned evidence | interpretation |
|---|---|---|---|---|
| Emergency accessibility under disruption | Baseline versus Low, Central, and High Road Available configurations | Dispatch Travel Time, Hospital Transport Time, Total Emergency Access Time, Timely Access Threshold (min), Timely Access Status | Baseline Two-Stage Emergency Travel Time; Emergency Access under Road Disruption Scenarios; Baseline Emergency Accessibility by Municipality; Accessibility Loss by Disruption Scenario | Modelled change in geographic access under stated stress tests. |
| Distributional effects | Scenario changes aggregated with total and older-population weights and Municipality Name | Population Losing Timely Access, Older Population Losing Timely Access, Access Time Increase, Total Population, Population Age 65+, Population Age 75+, Population Age 85+ | Population Losing Timely Emergency Access; Municipal Emergency Accessibility Loss; Vulnerable Population Accessibility Loss | Spatial and demographic heterogeneity, not individual clinical risk. |
| Hospital value and redundancy | Hospital catchment reassignment and hospital-coalition marginal contribution | Assigned Hospital, Hospital Catchment Population, Hospital Demand Change, Alternative Hospital Count, Hospital Shapley Value | Hospital Catchment and Demand Reallocation; Hospital Catchment Reallocation Estimates; Hospital Emergency Accessibility Value | Network-supported hospital value; bed-based weighting remains a sensitivity analysis. |
| Road value and ranking robustness | Corridor-coalition marginal contribution and direct-versus-surrogate comparison | Medical Corridor ID, Road Shapley Value, Road-Hospital Shapley Value, Shapley Standard Error, Direct-Surrogate Rank Difference | Critical Medical Corridors; Road-Hospital Shapley Value Matrix; Priority Medical Roads; Road Priority Robustness across Scenarios | Value conditional on scenario, corridor definition, candidate screen, and coalition distribution. |
| Restoration priority | Sequential restoration from each disrupted network | Restored Population, Restored Older Population, Travel Time Reduction, Coverage Recovery, Marginal Restoration Benefit, Restoration Rank | Emergency Access Recovery by Restoration Budget; Restoration Portfolio Performance | Road-count restoration scale, not monetary cost-effectiveness. |

### Identification and Interpretation Limits

- The analysis is cross-sectional and simulation-based. It cannot establish that a road failed, that restoring it would cause the estimated real-world benefit, or that travel time equals observed ambulance response time.
- Assumed Speed (km/h) represents routing impedance and excludes dispatch delay, vehicle availability, on-scene time, congestion, and emergency driving behaviour not represented in the data.
- Hospital Role Weight and Hospital Capacity Weight do not measure clinical emergency capacity. The unweighted Operational Hospital Set is primary; weighted results are labelled sensitivity analyses.
- Older-population outcomes use their disclosure-group analysis units. They are not imputed to 125 m meshes, so fine-scale total-population and older-population results have different spatial support.
- Road Shapley Value is conditional on the screened Medical Corridor ID game. A non-converged estimate cannot support a definitive priority ranking.
- Restoration Budget remains non-final because repair cost and duration are unavailable. Planned budget-labelled outputs must be implemented and interpreted using Restoration Scale unless valid cost evidence is added later.

## 6. Main Estimation Framework

### 6.1 Scenario-Specific Road Graph and Impedance

For disruption scenario \(s\), define the available road graph as

\[
G_s = (V, E_s), \qquad E_s = \{e : a_{e,s} = 1\}.
\]

Here, \(G_s\) is the scenario-specific graph, \(V\) is the set of grade-aware road and virtual connector nodes, \(E_s\) is the set of available road edges, \(e\) indexes Road Edge ID, and \(a_{e,s}\) is Road Available for edge \(e\) in scenario \(s\).

The travel-time impedance for available edge \(e\) under speed sensitivity multiplier \(m\) is

\[
c_e(m) = \frac{60 L_e}{1000 m v_e}.
\]

Here, \(c_e(m)\) is edge travel time in minutes, \(L_e\) is Road Length (m), \(v_e\) is Assumed Speed (km/h), and \(m\) takes the values \(0.8\), \(1.0\), and \(1.2\), with \(1.0\) primary. Baseline Edge Travel Time (min) equals \(c_e(1.0)\).

For a snapped dispatch base, demand unit, or hospital \(x\), connector time is

\[
q_x(m) = \frac{60 d_x}{1000 m v_{e(x)}}.
\]

Here, \(q_x(m)\) is connector time in minutes, \(d_x\) is Network Snap Distance (m), and \(v_{e(x)}\) is Assumed Speed (km/h) on the edge to which \(x\) is connected. The shortest road-network time between two virtual connector positions \(u\) and \(v\) is denoted by \(d_s(u,v;m)\). If no path exists within the relevant Network Component ID, \(d_s(u,v;m)\) is infinite and the unit is reported as disconnected.

### 6.2 Two-Stage Emergency Access

For analysis unit \(i\), scenario-specific ambulance dispatch time is

\[
D_{i,s}(m) = \min_{b \in B} \left\{q_b(m) + d_s(b,i;m) + q_i(m)\right\}.
\]

Here, \(D_{i,s}(m)\) is Dispatch Travel Time, \(i\) indexes Analysis Unit ID, \(b\) indexes Dispatch Base Node ID, and \(B\) is the set of accepted candidate dispatch bases.

The second-stage hospital transport time is

\[
H_{i,s}(m) = \min_{h \in H_s} \left\{q_i(m) + d_s(i,h;m) + q_h(m)\right\}.
\]

Here, \(H_{i,s}(m)\) is Hospital Transport Time, \(h\) indexes Hospital Node ID, and \(H_s\) is the scenario-specific Operational Hospital Set. Assigned Hospital is the minimizing hospital, with deterministic identifier ordering used to break exact ties.

Total two-stage access time is

\[
T_{i,s}(m) = D_{i,s}(m) + H_{i,s}(m).
\]

Here, \(T_{i,s}(m)\) is Total Emergency Access Time. This specification counts the demand connector once when the ambulance reaches the incident and once when it returns to the road for hospital transport. Access Time Increase is \(T_{i,s}(m)-T_{i,0}(m)\) when both times are finite; newly disconnected units are reported separately and are not assigned an arbitrary finite increase.

### 6.3 Timely Coverage and Distributional Loss

For Timely Access Threshold (min) \(\tau\), timely status is

\[
I_{i,s,\tau}(m) = \mathbf{1}\left\{T_{i,s}(m) \leq \tau\right\}, \qquad \tau \in \{15,30,45\}.
\]

Here, \(I_{i,s,\tau}(m)\) is Timely Access Status and \(\mathbf{1}\{\cdot\}\) is the indicator function.

Population-weighted timely coverage and its rate are

\[
A_{s,\tau}(m) = \sum_i p_i I_{i,s,\tau}(m), \qquad R_{s,\tau}(m) = \frac{A_{s,\tau}(m)}{\sum_i p_i}.
\]

Here, \(A_{s,\tau}(m)\) is covered population, \(R_{s,\tau}(m)\) is the coverage rate, and \(p_i\) is Total Population for unit \(i\).

Population losing timely access is

\[
L_{s,\tau}(m) = \sum_i p_i I_{i,0,\tau}(m)\left[1-I_{i,s,\tau}(m)\right].
\]

Here, \(L_{s,\tau}(m)\) is Population Losing Timely Access relative to baseline scenario \(0\). Older Population Losing Timely Access uses the same expression on disclosure-group analysis units with Population Age 65+, Population Age 75+, or Population Age 85+ replacing \(p_i\). Municipality-level estimates sum the corresponding unit-level quantities by Municipality Name.

### 6.4 Hospital Catchments, Alternatives, and Hospital Value

For hospital \(h\), its scenario catchment population is

\[
C_{h,s}(m) = \sum_i p_i \mathbf{1}\left\{h^*_{i,s}(m)=h\right\}.
\]

Here, \(C_{h,s}(m)\) is Hospital Catchment Population and \(h^*_{i,s}(m)\) is Assigned Hospital. Hospital Demand Change is \(C_{h,s}(m)-C_{h,0}(m)\).

The number of alternative hospitals within threshold \(\tau\) is

\[
K_{i,s,\tau}(m) = \sum_{h \in H_s} \mathbf{1}\left\{D_{i,s}(m)+q_i(m)+d_s(i,h;m)+q_h(m) \leq \tau\right\} - I_{i,s,\tau}(m).
\]

Here, \(K_{i,s,\tau}(m)\) is Alternative Hospital Count after excluding Assigned Hospital when timely access is achieved. Negative values are set to zero.

The primary hospital analysis assigns equal Hospital Role Weight to every hospital. A declared sensitivity analysis may replace equal weights with Hospital Capacity Weight or an explicitly prespecified role rule, but weighted coverage is reported separately and never substituted for the primary population count. Missing Hospital Capacity Weight is not imputed; the complete-case hospital set and omitted hospitals must be reported.

### 6.5 Restoration Value and Portfolios

For a disrupted scenario \(s\), let \(N_s\) be the screened set of unavailable Medical Corridor ID players and let \(S\) be a restored subset of \(N_s\). The primary restoration value function is

\[
v_{s,\tau}(S;m) = A_{s,\tau}(S;m)-A_{s,\tau}(\varnothing;m).
\]

Here, \(v_{s,\tau}(S;m)\) is the Restored Population produced by coalition \(S\), \(A_{s,\tau}(S;m)\) is timely covered population after restoring \(S\), and \(\varnothing\) is the no-restoration state of disrupted scenario \(s\). Restored Older Population replaces Total Population with the declared older-population weight.

To avoid infinite arithmetic for disconnected units, population-weighted Travel Time Reduction uses threshold-capped time:

\[
\Delta \bar{T}_{s}(S;m) = \frac{\sum_i p_i\left[\min\{T_{i,s}(\varnothing;m),45\}-\min\{T_{i,s}(S;m),45\}\right]}{\sum_i p_i}.
\]

Here, \(\Delta \bar{T}_{s}(S;m)\) is mean Travel Time Reduction in minutes and \(45\) is the largest prespecified timely-access threshold. An infinite time is capped at \(45\) minutes for this secondary metric only; timely-status calculations continue to treat it as unreachable.

Coverage recovery is

\[
Q_{s,\tau}(S;m) = \frac{v_{s,\tau}(S;m)}{L_{s,\tau}(m)}
\]

when \(L_{s,\tau}(m)>0\). Here, \(Q_{s,\tau}(S;m)\) is Coverage Recovery. Marginal Restoration Benefit is the change in the declared value function after adding one corridor to \(S\). Connected Hospital Count and Network Redundancy Value are reported as separate mechanism measures rather than added to population coverage with arbitrary coefficients.

The primary portfolio constraint is Restoration Scale. Portfolios are evaluated after restoring \(1\), \(5\), \(10\), \(20\), \(50\), and \(100\) corridors, or all candidates when fewer are available. Restoration Rank is based on the primary Road Shapley Value, while a greedy direct-marginal portfolio is retained as a comparator. No ratio using Restoration Budget is reported without repair-cost or repair-duration evidence.

### 6.6 Direct Monte Carlo Shapley Estimation

For road corridor \(j \in N_s\), direct Monte Carlo Road Shapley Value is

\[
\widehat{\phi}_{j,s,\tau} = \frac{1}{M}\sum_{r=1}^{M}\left[v_{s,\tau}\left(P_r(j)\cup\{j\};1.0\right)-v_{s,\tau}\left(P_r(j);1.0\right)\right].
\]

Here, \(\widehat{\phi}_{j,s,\tau}\) is Road Shapley Value, \(M\) is Monte Carlo Permutations, \(r\) indexes a uniformly sampled player ordering, and \(P_r(j)\) is the set of corridors preceding \(j\) in ordering \(r\). The bracketed quantity is the permutation-level marginal contribution \(\Delta_{j,r}\).

Its Monte Carlo standard error is

\[
\widehat{SE}_{j} = \left[\frac{1}{M(M-1)}\sum_{r=1}^{M}\left(\Delta_{j,r}-\widehat{\phi}_{j,s,\tau}\right)^2\right]^{1/2}.
\]

Here, \(\widehat{SE}_{j}\) is Shapley Standard Error. Permutations are processed in batches of \(250\), with at least \(2{,}000\) and at most \(20{,}000\) permutations. Shapley Convergence Status is met only when, across three consecutive batches, the top-20 set has Jaccard overlap of at least \(0.90\), every top-20 estimate has relative standard error at most \(0.05\) when nonzero or absolute standard error at most \(0.001\) of baseline covered population when near zero, and no top-20 rank changes by more than two positions. Estimates that reach the cap without meeting all criteria are labelled non-converged and cannot support a definitive top-20 claim.

If more than \(2{,}000\) disrupted corridors are available, screening retains at most \(2{,}000\) corridors using the union of positive single-corridor Restored Population, baseline or disrupted shortest-path use, Emergency Route Membership, and direct single-corridor Travel Time Reduction, ordered primarily by Restored Population and then Travel Time Reduction. Road Shapley Value is explicitly interpreted as conditional on this screened game.

Hospital Shapley Value uses the same estimator with hospitals as players and timely coverage from the active hospital coalition as the value function. For Road-Hospital Shapley Value, the value function counts population with timely two-stage access to a specified hospital \(h\), so each road estimate is hospital-specific.

### 6.7 Surrogate Validation and Robustness

A surrogate is permitted only after direct values are obtained for a validation subset. Coalition membership predicts the direct network value function, and SHAP attribution is compared with direct Road Shapley Value. The surrogate passes only if Surrogate Prediction Error, measured as held-out root mean squared error divided by the observed value range, is at most \(0.05\), and the mean absolute Direct-Surrogate Rank Difference among the direct top 20 is at most two ranks. Failed validation prohibits substituting surrogate ranks for direct ranks.

Required robustness and failure-mode analyses are:

- Assumed Speed (km/h) multipliers of \(0.8\), \(1.0\), and \(1.2\).
- Timely Access Threshold (min) values of \(15\), \(30\), and \(45\).
- Total Population versus Population Age 65+, Population Age 75+, and Population Age 85+ weighting on their valid analysis units.
- Primary unweighted Operational Hospital Set versus clearly labelled hospital-role and complete-case Hospital Capacity Weight sensitivities.
- Low, Central, and High disruption severity and separate reporting by Network Component ID and Municipality Name.
- Medical Corridor ID screening and a constituent Road Edge ID ablation for the highest-ranked corridors.
- Direct Monte Carlo batch convergence, Shapley Standard Error, Scenario Priority Rank, and Priority Selection Frequency.
- Explicit counts and population totals for failed network snaps, baseline disconnections, and scenario-induced disconnections.

The framework fails to support priority claims if baseline routing is not stable, disruption scenarios yield negligible differences, speed sensitivity reverses principal conclusions, the screened game omits essential connectors, direct Shapley estimates do not converge, or surrogate validation fails when surrogate results are used.

## 7. Analytical Workflow

| step | variables used | formula or model used | generated figure/table title | theory or claim evaluated | support status before estimation |
|---|---|---|---|---|---|
| 1. Validate network and study population | Road Edge ID, From Node ID, To Node ID, Network Component ID, Network Analysis Eligible, Network Snap Distance (m), Candidate Dispatch Base, Eligible Emergency Hospital, Total Population, Population Age 65+ | Graph, component, connector-threshold, and completeness checks in Section 6.1 | Emergency Care Network and Population Demand; Data and Network Descriptive Summary | The complete ambulance chain can be represented on a usable baseline network. | Inconclusive until topology, snap failures, and baseline disconnections are reported. |
| 2. Estimate baseline two-stage access | Baseline Edge Travel Time (min), Dispatch Base Node ID, Demand Node ID, Hospital Node ID, Dispatch Travel Time, Hospital Transport Time, Total Emergency Access Time | Section 6.2 shortest-path equations with \(m=1.0\) | Baseline Two-Stage Emergency Travel Time; Baseline Emergency Accessibility by Municipality | Baseline geographic access can be decomposed into dispatch and hospital-transport stages. | Supported only if paths are reproducible and disconnected population is acceptably small and explicit. |
| 3. Construct nested disruption scenarios | Disruption Scenario, Road Available, Hazard Exposure Class, Road State, Emergency Route Membership | Section 5 nested Low, Central, and High rules and Section 6.1 graph construction | Emergency Access under Road Disruption Scenarios; Accessibility Loss by Disruption Scenario | Increasing road stress reduces emergency accessibility through the network mechanism. | Inconclusive; negligible or non-monotone changes weaken the mechanism. |
| 4. Estimate timely coverage and distributional loss | Timely Access Threshold (min), Timely Access Status, Access Time Increase, Population Losing Timely Access, Older Population Losing Timely Access, Total Population, Population Age 65+, Population Age 75+, Population Age 85+, Municipality Name | Section 6.3 coverage and loss equations | Population Losing Timely Emergency Access; Municipal Emergency Accessibility Loss; Vulnerable Population Accessibility Loss | Road disruption has heterogeneous demographic and municipal consequences. | Supported only when rankings are reasonably stable across thresholds and valid spatial supports. |
| 5. Estimate hospital catchments and redundancy | Operational Hospital Set, Assigned Hospital, Hospital Catchment Population, Hospital Demand Change, Alternative Hospital Count, Hospital Role Weight, Hospital Capacity Weight | Section 6.4 catchment and alternative-hospital equations | Hospital Catchment and Demand Reallocation; Hospital Catchment Reallocation Estimates | Network disruption reallocates potential hospital demand and changes substitution options. | Partially supported if catchments are stable but role or capacity sensitivity is not. |
| 6. Estimate hospital marginal value | Hospital Shapley Value, Shapley Standard Error, Monte Carlo Permutations, Shapley Convergence Status | Section 6.6 hospital-player Monte Carlo Shapley estimator | Hospital Emergency Accessibility Value | Hospital value depends on location and substitution, not bed count alone. | Supported only for converged estimates robust to Operational Hospital Set rules. |
| 7. Screen medical-corridor players | Medical Corridor ID, Road Edge ID, Emergency Route Membership, Hazard Exposure Class, Restored Population, Travel Time Reduction | Section 6.6 candidate-screening rule, capped at 2,000 players | Data and Network Descriptive Summary | A computationally feasible road game retains corridors with plausible emergency-access relevance. | Partially supported because all later road values are conditional on the screen. |
| 8. Estimate road and road-hospital contributions | Road Shapley Value, Road-Hospital Shapley Value, Shapley Standard Error, Shapley Convergence Status, Hospital Name | Section 6.6 road and hospital-specific value functions | Critical Medical Corridors; Road-Hospital Shapley Value Matrix; Priority Medical Roads | Complementary and substitutable roads have scenario- and hospital-specific marginal value. | Supported only for converged direct estimates; otherwise inconclusive. |
| 9. Build and compare restoration portfolios | Restoration Scale, Restored Population, Restored Older Population, Travel Time Reduction, Coverage Recovery, Marginal Restoration Benefit, Restoration Rank, Connected Hospital Count, Network Redundancy Value | Section 6.5 restoration value, capped-time, and coverage-recovery equations | Emergency Access Recovery by Restoration Budget; Restoration Portfolio Performance | Ordered restoration recovers emergency coverage and can reveal diminishing returns. | Supports scale-based prioritization only; cost-effectiveness remains unsupported. |
| 10. Evaluate robustness and surrogate scaling | Scenario Priority Rank, Priority Selection Frequency, Surrogate Prediction Error, Direct-Surrogate Rank Difference, Shapley Standard Error | Section 6.7 sensitivity and surrogate acceptance rules | Road Priority Robustness across Scenarios | Priority corridors remain stable across plausible assumptions, and a surrogate is usable only when it reproduces direct results. | Supported only if direct convergence and both surrogate thresholds are met. |

### Evidence Checkpoints

1. Baseline checkpoint: stop before disruption estimation if network construction cannot yield reproducible finite paths for the great majority of represented population or if connector exclusions are not fully reported.
2. Scenario checkpoint: treat the disruption mechanism as weak if nested scenarios do not produce ordered changes in Total Emergency Access Time or timely coverage.
3. Equity checkpoint: report total- and older-population results on their own valid analysis units; do not claim fine-grid older-population precision.
4. Hospital checkpoint: retain unweighted coverage as primary if Hospital Capacity Weight or hospital-role sensitivity materially changes rankings.
5. Shapley checkpoint: do not publish definitive corridor or hospital ranks when Shapley Convergence Status is not met.
6. Surrogate checkpoint: do not use surrogate results for scaling when Surrogate Prediction Error or Direct-Surrogate Rank Difference fails the Section 6.7 rule.
7. Decision checkpoint: report Restoration Scale as the actionable constraint; defer monetary or time-budget claims until Restoration Budget becomes a final, evidence-supported variable.

## 8. Figure and Table Plan

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---|---|---|
| Emergency Care Network and Population Demand | Shows the spatial structure of population demand, candidate ambulance dispatch bases, eligible emergency hospitals, and the road network. | map | 3 | Geometry, Total Population, Population Age 65+, Candidate Dispatch Base, Eligible Emergency Hospital, Emergency Road Class | pending |
| Baseline Two-Stage Emergency Travel Time | Decomposes baseline ambulance dispatch, hospital transport, and total two-stage emergency travel time. | map | 3 | Geometry, Candidate Dispatch Base, Eligible Emergency Hospital, Road Type, Width Category | pending |
| Emergency Access under Road Disruption Scenarios | Compares total emergency travel time under baseline, Low, Central, and High road-disruption scenarios. | map | 4 | Geometry, Road State, Hazard Type, Warning Zone Class | pending |
| Population Losing Timely Emergency Access | Compares total and older populations losing 15-, 30-, and 45-minute emergency access across disruption scenarios. | stacked_bar | 3 | Total Population, Population Age 65+, Population Age 75+ | pending |
| Municipal Emergency Accessibility Loss | Shows municipal variation in emergency travel-time increases and population coverage losses. | map | 2 | Geometry, Municipality Name, Total Population, Population Age 65+ | pending |
| Hospital Catchment and Demand Reallocation | Shows changes in hospital catchments, potential demand, and alternative-hospital availability after road disruption. | map | 3 | Geometry, Hospital Name, Eligible Emergency Hospital, Tertiary Emergency Hospital, Rotation Hospital, Total Beds | pending |
| Critical Medical Corridors | Maps scenario-specific Road Shapley Value estimates for corridors that preserve fire-station-to-incident-to-hospital connectivity and population emergency coverage. | map | 3 | Geometry, Route Name, Emergency Road Class, Road Type, Total Population, Population Age 65+ | pending |
| Road-Hospital Shapley Value Matrix | Shows the marginal contribution of each candidate medical corridor to the emergency accessibility value of each eligible hospital under Low, Central, and High disruption scenarios. | heatmap | 3 | Route Name, Hospital Name, Eligible Emergency Hospital, Total Population, Population Age 65+ | pending |
| Emergency Access Recovery by Restoration Budget | Compares cumulative emergency-coverage recovery and travel-time benefits across restoration scales or budgets. | line | 2 | Total Population, Population Age 65+ | pending |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Data and Network Descriptive Summary | Summarizes the population, fire-service, emergency-hospital, road-network, and hazard-zone inputs. | approximately 25 | 7 | One data element or descriptive indicator. | Record count, total, mean, standard deviation, median, minimum, and maximum as applicable. | pending |
| Baseline Emergency Accessibility by Municipality | Compares baseline two-stage emergency travel times and timely-access coverage across municipalities. | 49 | 11 | One municipality. | Population, older population, dispatch time, hospital transport time, total time, and 15-, 30-, and 45-minute coverage measures. | pending |
| Accessibility Loss by Disruption Scenario | Compares emergency-access losses across road-disruption scenarios and travel-time thresholds. | 12 | 9 | One disruption-scenario and time-threshold combination. | Covered population, population losing coverage, older population losing coverage, coverage-rate change, and average travel-time increase. | pending |
| Vulnerable Population Accessibility Loss | Identifies municipalities with the largest emergency-access losses among older age groups. | 49 | 13 | One municipality. | Population Age 65+, Population Age 75+, Population Age 85+, population losing coverage by age group, loss rates, and total travel-time increase. | pending |
| Hospital Catchment Reallocation Estimates | Measures changes in service population, potential demand, and alternatives for each eligible emergency hospital. | approximately 75 | 11 | One eligible emergency hospital. | Hospital role, Total Beds, baseline catchment population, disrupted catchment population, demand change, and alternative-hospital count. | pending |
| Hospital Emergency Accessibility Value | Estimates the marginal contribution of maintaining each eligible emergency hospital to population-weighted timely emergency access under each disruption scenario. | approximately 75 | 12 | One eligible emergency hospital. | Hospital Name, hospital role, Total Beds, scenario-specific Hospital Shapley Value, Shapley Standard Error, covered population, older population, alternative-hospital count, and rank. | pending |
| Priority Medical Roads | Provides the uncertainty-aware ranked list of roads recommended for continuity protection or priority restoration. | 20 | 14 | One candidate critical road segment or corridor. | Route Name, Emergency Road Class, Road Shapley Value, Shapley Standard Error, restored population, restored older population, travel-time reduction, connected hospitals, redundancy value, and scenario rank. | pending |
| Restoration Portfolio Performance | Compares cumulative recovery outcomes across road-restoration scales or budget levels. | 6 | 10 | One restoration scale or budget level. | Restoration scale, cumulative restored population, recovered coverage, older-population benefit, travel-time benefit, and marginal benefit. | pending |
| Road Priority Robustness across Scenarios | Tests whether road-priority rankings remain stable across disruption scenarios and between direct Shapley estimates and the SHAP surrogate. | 20 | 10 | One highly ranked road. | Direct Shapley ranks, SHAP-surrogate ranks, scenario-specific ranks, Direct-Surrogate Rank Difference, mean rank, rank range, selection frequency, and robustness class. | pending |

### Variable Coverage Warning

⚠️ 警告：以下变量在 AnaSOP Section 4 中不存在或未标记为最终分析变量，建议返回 data-preprocessing 补充：

- Dispatch Travel Time （用于 Baseline Two-Stage Emergency Travel Time; Baseline Emergency Accessibility by Municipality）
- Hospital Transport Time （用于 Baseline Two-Stage Emergency Travel Time; Baseline Emergency Accessibility by Municipality）
- Total Emergency Access Time （用于 Baseline Two-Stage Emergency Travel Time; Emergency Access under Road Disruption Scenarios）
- Disruption Scenario （用于 Emergency Access under Road Disruption Scenarios; Accessibility Loss by Disruption Scenario; Road-Hospital Shapley Value Matrix; Hospital Emergency Accessibility Value）
- Access Time Increase （用于 Emergency Access under Road Disruption Scenarios; Municipal Emergency Accessibility Loss）
- Timely Access Status （用于 Population Losing Timely Emergency Access）
- Population Losing Timely Access （用于 Population Losing Timely Emergency Access; Municipal Emergency Accessibility Loss）
- Older Population Losing Timely Access （用于 Population Losing Timely Emergency Access; Vulnerable Population Accessibility Loss）
- Assigned Hospital （用于 Hospital Catchment and Demand Reallocation; Hospital Catchment Reallocation Estimates）
- Hospital Catchment Population （用于 Hospital Catchment and Demand Reallocation; Hospital Catchment Reallocation Estimates）
- Hospital Demand Change （用于 Hospital Catchment and Demand Reallocation; Hospital Catchment Reallocation Estimates）
- Alternative Hospital Count （用于 Hospital Catchment and Demand Reallocation; Hospital Catchment Reallocation Estimates; Hospital Emergency Accessibility Value）
- Road Shapley Value （用于 Critical Medical Corridors; Priority Medical Roads）
- Hospital Shapley Value （用于 Hospital Emergency Accessibility Value）
- Road-Hospital Shapley Value （用于 Road-Hospital Shapley Value Matrix）
- Shapley Standard Error （用于 Hospital Emergency Accessibility Value; Priority Medical Roads）
- Direct-Surrogate Rank Difference （用于 Road Priority Robustness across Scenarios）
- Restored Population （用于 Critical Medical Corridors; Priority Medical Roads; Restoration Portfolio Performance）
- Restored Older Population （用于 Critical Medical Corridors; Priority Medical Roads; Restoration Portfolio Performance）
- Travel Time Reduction （用于 Critical Medical Corridors; Emergency Access Recovery by Restoration Budget; Priority Medical Roads）
- Connected Hospital Count （用于 Priority Medical Roads）
- Network Redundancy Value （用于 Priority Medical Roads）
- Restoration Rank （用于 Emergency Access Recovery by Restoration Budget）
- Restoration Budget （用于 Emergency Access Recovery by Restoration Budget; Restoration Portfolio Performance）
- Coverage Recovery （用于 Emergency Access Recovery by Restoration Budget; Restoration Portfolio Performance）
- Marginal Restoration Benefit （用于 Restoration Portfolio Performance）
- Scenario Priority Rank （用于 Priority Medical Roads; Road Priority Robustness across Scenarios）
- Priority Selection Frequency （用于 Road Priority Robustness across Scenarios）
