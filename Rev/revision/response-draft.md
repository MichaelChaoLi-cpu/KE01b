# Response to reviewers and editors of manuscript number [MANUSCRIPT ID]

# Revision Summary

Thank you for the editor’s and reviewers’ careful review of our manuscript, “Length-Dependent Road Failure and Two-Stage Emergency Medical Access in Kumamoto Prefecture.”

[The revision summary will be completed after the revisions and detailed responses are finalized.]

# Editor

Thank you for submitting your manuscript to International Journal of Disaster Risk Reduction.

The referees have reviewed your paper, as listed above. Their comments, reproduced  indicate that it would benefit from substantial revision. Hence, I invite you to revise and resubmit your manuscript. Please carefully address the issues raised in the comments.

To view your reviewer feedback, please log in as an author at https://www.editorialmanager.com/ijdrr/ and navigate to your manuscript in the " Submissions Needing Revision " folder under the Author Main Menu. 
 
When revising your manuscript, please consider all issues mentioned in the reviewers' comments carefully. Please note that your revised submission may need to be re-reviewed.

**Response:**
[Response to be completed.]

"[Exact revised manuscript text, where applicable.]"
(Page XX, Lines XX–XX)

# Reviewer 1

## Overall Comment

The manuscript presents a well-structured and timely analysis of post-earthquake emergency medical access in Kumamoto Prefecture. The framework is logical and the simulation design is clearly described. However, several issues, primarily related to modeling assumptions and presentation details, should be addressed before publication. My specific comments are as follows:

**Response:**
[Response to be completed.]

"[Exact revised manuscript text, where applicable.]"
(Page XX, Lines XX–XX)

## Comment 1

The authors state that standard road centerlines were used as input. However, for roads with a central median, a single centerline may not accurately represent the two separate carriageways. In such cases, the left and right road sections should be modeled separately to reflect realistic routing constraints. Please clarify how this was handled, or discuss it as a limitation.

**Response:** Thank you for highlighting this issue. The revised “Emergency-Care Network and Analysis Units” section clarifies that the network follows the supplied centerlines, does not construct separate carriageways where the source contains a single line, and represents each road connection as bidirectional. The “Limitations and Future Research” section explains how omitted carriageway directions and median restrictions can affect travel times, timely-access coverage, and road-section rankings, and identifies the data needed to assess these effects.

"The network follows the supplied road-centerline geometry and does not construct separate carriageways where the source represents a divided road with a single line. Each road connection is traversable in both directions with the same travel time; carriageway-specific directions, median-crossing restrictions, and turn restrictions are not explicitly modeled."
(Pages 10–11, Lines 193–197)

"On divided roads, the bidirectional centerline representation can admit movements that require a detour in practice because of carriageway direction or median restrictions, potentially understating travel times and overstating timely-access coverage. These constraints may also change section-level consequence rankings. Carriageway-specific geometry and directional and turn-restriction data are needed to assess these effects."
(Pages 26–27, Lines 546–551)

"The estimates do not include ambulance availability, dispatch processing, on-scene treatment, congestion, hospital clinical capacity, engineering fragility, repair duration, or restoration cost."
(Page 27, Lines 551–553)

## Comment 2

The assumed travel speeds for different road types should be more explicitly differentiated. Emergency vehicles, especially ambulances, may have different operational speeds on expressways, national highways, and municipal roads. The uniform speed assumption or the current classification may not fully capture this variation. Please either justify the chosen speed values with empirical evidence or discuss the potential impact of this simplification.

**Response:** Thank you for highlighting the importance of road-type speed differences. The revised “Emergency-Care Network and Analysis Units” section specifies the category speeds and width caps and identifies them as modeling assumptions. The Methods and Results sections on “Convergence and Sensitivity Analysis” now describe two category-specific 20% speed reductions evaluated through 1,000 paired replicates at each failure severity, with both routing stages recomputed. These comparisons quantify changes in timely coverage, grid access probabilities, and hospital allocation beyond those captured by uniform speed scaling. The “Limitations and Future Research” section identifies ambulance movement records as a basis for empirical speed calibration.

"Base speeds are 80 km/h for national expressways or equivalent roads, 50 km/h for national highways, 40 km/h for prefectural roads, 30 km/h for municipal roads or equivalent roads, and 20 km/h for other or unknown categories. Width-based caps are 20, 30, 50, 60, and 80 km/h for widths below 3 m, 3 to below 5.5 m, 5.5 to below 13 m, 13 to below 19.5 m, and at least 19.5 m, respectively; unknown width receives a 20 km/h cap. Each edge uses the lower of its category speed and width cap. These values are modeling assumptions rather than empirically calibrated ambulance operating speeds."
(Page 11, Lines 201–208)

"Two additional scenarios reduce effective, width-capped speeds by 20% on either national expressways and national highways (A) or prefectural and municipal roads (B), leaving other categories unchanged. Connector speeds follow their referenced access edges. Both routing stages are recomputed for each scenario using the same 1,000 failure draws at each expected failed-road-length share of 1%, 3%, 5%, and 10%. Paired comparisons assess 30-minute population coverage, grid access probabilities, and hospital reassignment among residents with a reachable complete emergency chain. The perturbation magnitude is a sensitivity setting, not an estimated speed error."
(Page 19, Lines 373–381)

"Under category-specific speed reductions, mean 30-minute coverage decreases relative to original speeds in the same failed networks by 18,955–25,788 residents in scenario A and 31,494–39,449 in scenario B across the four failure severities. The corresponding population-weighted probability reductions are 1.09–1.48 and 1.81–2.27 percentage points. Hospital assignments change for an average of 3.60–3.85% and 2.76–2.87% of reachable residents, respectively, while network disconnection remains unchanged. Grid-level effects are more concentrated: the 95th percentile of absolute access-probability reductions across grids ranges from 3.0 to 13.9 percentage points in A and 13.2 to 35.0 in B. These comparisons show sensitivity of timely coverage and hospital allocation to relative road-type speeds, which uniform speed scaling does not capture."
(Page 24, Lines 490–499)

"Ambulance movement records could calibrate category-specific speeds and refine dispatch and destination behavior, and complete hospital capacity data could support explicitly weighted alternatives to minimum-time assignment."
(Page 28, Lines 580–583)

## Comment 3

The resolution of several figures, particularly the maps, could be improved for readability. Important details, such as road networks and grid-level probabilities, are not clearly visible in the current version. Please provide higher-resolution versions.

**Response:** Thank you for this suggestion. Figures 2–10 now use 600-dpi images at their six-inch display width, with revised panel layouts, clearer labels and legends, and reduced unused space to improve readability. In particular, the three-panel maps in Figures 2, 3, 6, and 8 use two columns, giving each map more space; map annotations, hospital symbols, and colorbar labels are repositioned or resized to reduce crowding. These presentation changes preserve the underlying numerical results, geographic extents, and color-scale definitions. The updated figures appear on pages 33–41. The following unchanged figure titles identify the locations of the revised artwork:

"Figure 2. Population demand and emergency-care network across Kumamoto"
(Page 33, Lines 11–11)

"Figure 4. Emergency-access response to increasing failed road length"
(Page 35, Lines 25–25)

"Figure 6. Grid probability of losing baseline 30-minute emergency access"
(Page 37, Lines 39–39)

"Figure 8. Hospital catchment reliability under increasing road failure"
(Page 39, Lines 53–53)

"Figure 9. Road-section accessibility consequence and expected risk surfaces"
(Page 40, Lines 60–60)

## Comment 4

The Monte Carlo simulation uses a length-dependent random failure model. While this is a transparent approach, it does not account for the fact that certain road types (e.g., bridges, elevated sections) are inherently more vulnerable to earthquake damage. This omission should be explicitly acknowledged and discussed in the limitations section.

**Response:** Thank you for this comment. The revised “Length-Dependent Road-Failure Experiment” section explicitly states that equal-length sections receive the same failure probability without separate adjustments for bridges or elevated roads. The “Limitations and Future Research” section now acknowledges the omitted structural heterogeneity, explains its implications for the spatial distribution of disruption and probability-weighted emergency-access losses, and identifies the data needed for refinement.

"At a given severity, sections of equal length receive the same failure probability, without a separate adjustment for bridges or elevated roads."
(Page 13, Lines 246–248)

"Differences in bridge and elevated-road fragility are not represented by the length-only failure model. Such heterogeneity could change the spatial pattern of road disruption and the resulting probability-weighted emergency-access losses, even at the same expected failed-road-length share. Future work can replace scenario probabilities with verified engineering fragility or observed closure data while retaining the routing and outcome framework. Bridge and elevated-road inventories linked to structural-condition, shaking-intensity, and fragility data would support this refinement."
(Page 28, Lines 581–587)

## Comment 5

The manuscript would benefit from a brief overview of the study area's geographic and demographic context. Information such as total population, road network length, composition of road types, and key topographic features would help readers better interpret the simulation results. This could be added to the study area description.

**Response:**
Thank you for this suggestion. The revised Study Area and Data Sources section now describes Kumamoto's geographic setting, the 2020 population baseline, and the length and road-type composition of the eligible modeled network to provide context for interpreting the simulations.

"Located in central Kyushu, the prefecture includes mountainous terrain to the east and south, the Aso caldera, and western coastal and island areas facing the Ariake and Yatsushiro seas. The study's 2020 population baseline comprises 1,738,301 residents in 62,945 populated 125 m meshes. The eligible modeled road network spans 42,949 km across 343,844 junction-to-junction sections. By represented road length, municipal roads or equivalent roads account for 88.9%, prefectural roads for 7.1%, national highways for 3.0%, national expressways or equivalent roads for 0.6%, and other roads for 0.4%."
(Pages 9–10, Lines 168–175)

# Reviewer 2

## Overall Comment

Following comments are supplied in order to improve the paper.

**Response:**
[Response to be completed.]

"[Exact revised manuscript text, where applicable.]"
(Page XX, Lines XX–XX)

## Comment 1

Lines 92-108: It is not clear on the research gap and contribution of this paper, please rephrase.

**Response:** Thank you for this comment. The revised Introduction defines the research gap as connecting reliability of the complete dispatch-to-patient-to-hospital chain under multiple road failures with the accessibility consequence of individual road sections, and states three linked contributions: multi-level emergency-access reliability, a separate all-section consequence and expected-risk assessment, and their combined use for continuity protection and restoration screening. The objective and intended planning use are aligned with this scope. The revised text reads as follows.

"A primary objective of this study is therefore to identify road sections whose loss most reduces continuous emergency medical access from dispatch base to patient to hospital, providing evidence for continuity protection and post-disaster restoration screening."
(Pages 5–6, Lines 81–84)

"The resulting prefecture-wide maps are accordingly intended as a screening layer for road inspection, continuity protection, and restoration planning, to be updated as field-verified damage information becomes available."
(Page 6, Lines 89–91)

"These approaches establish tools for disruption assessment, but they answer different questions about operations, network vulnerability, and link criticality. The specific problem addressed here is how to connect reliability of the complete dispatch-to-patient-to-hospital chain under multiple road failures with the accessibility consequence of each road section, using a common network and population baseline. We address this problem with a reproducible, paired network experiment in which continuous junction-to-junction sections fail with probabilities that increase with their lengths. The study makes three linked contributions. First, every simulated state is fully rerouted through both emergency-care stages, linking grid access, population and municipal coverage, and hospital catchment stability within the same disrupted networks. Second, a separate single-section-removal analysis maps potential access loss for every eligible section and distinguishes this consequence from its probability-weighted expected risk under each declared scenario. Third, these complementary outputs connect the locations and populations exposed to unreliable emergency access with road-section evidence for continuity protection and restoration screening. Kumamoto demonstrates this reusable framework with locally specified inputs and failure scenarios."
(Pages 6–7, Lines 102–117)

## Comment 2

In the Literature Review section, each statement is supported by one or more references. While it is nice to attribute credit to prior work, the authors do not offer critical commentary on these studies. Considering that the objective of a literature review is to evaluate existing research and identify unresolved research gaps, this reviewer suggests the authors to provide critical assessment in order to pinpoint the limitations of current studies.

**Response:** Thank you for this suggestion. The three Literature Review subsections now compare the objectives, modeling choices, and planning implications of existing approaches. The revised text distinguishes operational ambulance and hospital-assignment models from disrupted-chain accessibility assessment, contrasts single-section and spatially clustered failures, and explains how emergency medical coverage loss differs from evacuation-oriented critical-link measures. These comparisons clarify the methodological choices underlying the present study while acknowledging the capabilities of prior work.

"The operational detail of ambulance-routing and hospital-assignment models is valuable for managing congestion and treatment delays, as illustrated by the model of Chou et al. (2022). That objective differs from identifying where repeated road failures prevent completion of the dispatch-to-patient-to-hospital chain. For the latter question, travel-time and coverage measures need to be recalculated jointly for both stages in each disrupted network, with losses distinguished across population groups and receiving hospitals."
(Page 8, Lines 129–134)

"Area-covering disruption analysis shows why the impact of a single closure cannot stand in for the loss of several nearby alternatives: the spatial distribution of vulnerability changes with the disruption pattern. This makes the failure representation a substantive modeling choice, not simply a computational detail. The present independent length-dependent experiment complements spatially clustered disruption scenarios by isolating network response under a declared exposure rule; it does not reproduce their spatial dependence. Pairing repeated-failure estimates with separate single-section removals allows system reliability and individual-section consequence to be interpreted without conflating them."
(Page 9, Lines 152–160)

"The evacuation-risk approach of Nitheesh and Bhavathrathan (2025) also shows that critical-link identification already combines probability and consequence. The remaining issue for emergency medical access is therefore the service consequence being measured: evacuation traffic and topological exposure answer a different planning question from population loss along a dispatch-to-patient-to-hospital chain. Our assessment uses that complete-chain coverage loss and reports it separately from scenario-weighted risk. These outputs support continuity screening, while restoration optimization additionally requires repair resources, costs, and interactions among damaged sections."
(Page 10, Lines 177–185)

## Comment 3

In the Materials and Methods section, the authors provide a detailed description of the methods. However, an overview of the overall methodological workflow is missing, making it difficult for readers to follow the procedures. To further improve the readability and systematicity of the paper, we suggest that the authors refine the current method descriptions and develop a complete methodological flowchart to serve as a guide for the subsequent method presentation

**Response:** Thank you for this suggestion. The Materials and Methods section now opens with an overview linked to a new methodological flowchart (Figure 1), which organizes the shared network and baseline, random-failure simulations, and independent single-section analysis into three connected frames. The overview and figure note explain how these analyses lead to emergency-access reliability and road-section consequence and risk outputs. Existing figures and their text references are renumbered as Figures 2–10.

"Figure 1 summarizes the methodological workflow. Spatial inputs are integrated into a junction-to-junction road network to establish baseline dispatch-to-patient and patient-to-hospital travel times. Two complementary analyses then use this common baseline: paired length-dependent road-failure simulations quantify grid, population, and hospital reliability, whereas separate removal of each road section measures potential accessibility loss and its probability-weighted expected risk. Convergence and speed-sensitivity checks assess the simulation estimates."
(Pages 9–10, Lines 166–172)

"Note: The shared network and baseline support two complementary analyses. Random-failure simulations use 1,000 paired replicates at 1%, 3%, and 5% expected failed road length, with 10% as a stress scenario. Single-section analysis removes each section separately from the baseline network and combines potential population loss with the section failure probability to calculate expected risk. Timely access is evaluated at 15, 30, and 45 minutes, with 30 minutes as the primary threshold."
(Page 32, Lines 5–9)

The following figure titles show the updated numbering:

"Figure 2. Population demand and emergency-care network across Kumamoto"
(Page 33, Lines 11–11)

"Figure 3. Baseline dispatch, hospital transport, and total emergency travel times"
(Page 34, Lines 18–18)

"Figure 4. Emergency-access response to increasing failed road length"
(Page 35, Lines 25–25)

"Figure 6. Grid probability of losing baseline 30-minute emergency access"
(Page 37, Lines 39–39)

"Figure 7. Population coverage retained across failure severity and thresholds"
(Page 38, Lines 46–46)

"Figure 8. Hospital catchment reliability under increasing road failure"
(Page 39, Lines 53–53)

"Figure 9. Road-section accessibility consequence and expected risk surfaces"
(Page 40, Lines 60–60)

"Figure 10. Monte Carlo convergence, stress severity, and speed sensitivity"
(Page 41, Lines 68–68)

## Comment 4

In the Results section, the authors present abundant analytical findings. However, these results are not clearly or explicitly linked to the primary objective of this study, i.e, "to determine which road sections must be kept open, and, once damaged, restored first, in order to preserve continuous emergency medical access from dispatch base to patient to hospital", which is stated in the Introduction. Therefore, this reviewer recommends that the authors further interpret the results against this core research objective.

**Response:** Thank you for this comment. The revised Results explicitly connects grid and population reliability, hospital catchment changes, and individual road-section consequences to the road-continuity objective, while the Discussion explains their combined use for continuity protection and restoration screening. Potential loss provides the direct section-level measure of timely coverage supported by keeping a road available, and expected risk weights this consequence by the declared failure probability. The Conclusion now uses the same screening scope as the revised Introduction; an operational repair sequence additionally requires verified damage and resource constraints. The revised passages read as follows.

"For the road-continuity objective, these grid patterns locate demand exposed to unreliable access, while population and municipal summaries quantify the associated burden; the section-level analysis below identifies the consequence of individual road interruptions."
(Page 23, Lines 475–478)

"For continuity planning, the joint pattern of catchment gains, losses, and intermittent zero assignments identifies receiving facilities whose road-supported service areas merit closer examination alongside the section-consequence maps."
(Page 25, Lines 510–513)

"These section-level results directly address the continuity objective: potential loss measures the timely population coverage preserved by keeping an individual section available when the rest of the network remains intact, while expected risk weights that consequence by the section's scenario-specific failure probability."
(Page 26, Lines 532–536)

"Read together, the demand and hospital results indicate where service continuity is fragile, and the road-section surfaces show which individual interruptions have the largest modeled coverage consequences. This combination supports screening candidate corridors for continuity protection and field inspection; restoration sequencing then uses verified conditions and operational constraints."
(Page 29, Lines 610–614)

"The combined evidence identifies road sections with high modeled accessibility consequences for continuity protection and restoration screening."
(Pages 31–32, Lines 669–670)

## Comment 5

Lines 524-537: In the Discussion section, the authors restate the contributions of this work. I suggest that these claims be further aligned with the contributions presented earlier in the manuscript to ensure consistency.

**Response:** Thank you for this suggestion. The revised “Contributions to Network-Reliability Assessment” subsection now follows the same three contributions as the Introduction: complete-chain, multi-level reliability; separate road-section consequence and scenario-dependent expected risk; and their complementary use for continuity protection and restoration screening. It also explicitly distinguishes the repeated road-failure experiment from the separate leave-one-section-out analysis. The revised paragraph reads as follows.

"The framework makes three linked contributions, consistent with the Introduction. First, complete two-stage rerouting connects grid access, population and municipal coverage, and hospital catchment stability within the same paired road-failure experiment. Grid estimates locate fragile demand, population and municipal summaries describe distribution, and hospital catchments show destination substitution. These outcomes are derived from the feasible network in each replicate. Second, a separate leave-one-section-out analysis identifies road-section accessibility consequence when other roads remain available, and probability weighting expresses that consequence as scenario-dependent expected risk. This separation distinguishes repeated simultaneous-failure reliability from individual-section consequence. Third, the complementary demand, hospital, and road-section outputs connect service fragility with evidence for continuity protection and restoration screening. This distinction clarifies which output answers each planning question."
(Pages 29–30, Lines 617–629)

## Comment 6

Finally, is the proposed method only applicable to the Kumamoto Prefecture, or is it a generalizable approach? If the method is intended to be generalizable, the description of the methodology and the core positioning of this paper may be revised to frame it as a general method, with the Kumamoto Prefecture serving merely as a case study.

**Response:** Thank you for this comment. The revised Abstract, Materials and Methods, Discussion, and Conclusion present a reusable emergency-access framework with Kumamoto as the case study. The manuscript distinguishes the transferable routing, simulation, and outcome calculations from locally specified inputs and parameters, and explains how applications elsewhere accommodate local ambulance-service organization and recalculate coverage and road-section priorities.

"We present a reusable network framework for assessing this complete chain and demonstrate it in Kumamoto Prefecture, Japan, following the 28 July 2026 Kumamoto earthquake (M7.1)."
(Page 1, Lines 7–9)

"The framework represents emergency access as a cross-sectional network simulation, with Kumamoto Prefecture as the case study. Its core inputs are a routable road network, spatial population demand, eligible dispatch bases, and eligible hospitals. The junction-based section definition, two-stage rerouting, paired failure simulation, and accessibility indicators are reusable across study areas; road speeds, connector rules, facility eligibility, timely-access thresholds, and failure-scenario parameters require local specification."
(Page 10, Lines 175–181)

"The present network experiment provides the baseline quantities required for those extensions. Application elsewhere follows the same routing and outcome calculations after replacing the spatial inputs and specifying local service and failure assumptions. Dispatch bases can represent the locally responsible ambulance service rather than necessarily fire stations. Local validation of road connectivity, travel times, and facility eligibility supports that transfer; coverage estimates and section priorities must be recalculated for each study area."
(Page 29, Lines 611–617)

"The same framework also provides a reusable basis for future emergency preparedness in Kumamoto and for assessments in other regions using locally specified network, demand, facility, and failure-scenario inputs."
(Page 30, Lines 632–634)
