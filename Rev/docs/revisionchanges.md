# Manuscript Revision Changes

Schema: `kila-revision-changes/v1`

## reviewer-1/comment-1

### part-01

- Location: Materials and Methods / Emergency-Care Network and Analysis Units, first paragraph.
- Reason: Explain what vertical-level processing does and what the routing graph actually represents.
- Kila decisions: KILA-D-20260930-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T06:31:46Z
- Author: Kila
- Markup SHA-256 before: `73dcf1b5bc681c11b9d6ddc05df78ecda826976b094382d3e1166c559162fe4c`
- Markup SHA-256 after: `1da0842bb9d4a8ac1c9356c4d9f1889aa03e3b38ded7526e62a77cc2fa6fa8ea`
- Revision IDs: `1`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T153146254452.reviewer-1-comment-1.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Grade-aware nodes therefore prevent crossings at different levels from becoming false junctions.
~~~~

- After:

~~~~text
Grade-aware nodes therefore prevent crossings at different levels from becoming false junctions. The network follows the supplied road-centerline geometry and does not construct separate carriageways where the source represents a divided road with a single line. Each road connection is traversable in both directions with the same travel time; carriageway-specific directions, median-crossing restrictions, and turn restrictions are not explicitly modeled.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The network follows the supplied road-centerline geometry and does not construct separate carriageways where the source represents a divided road with a single line. Each road connection is traversable in both directions with the same travel time; carriageway-specific directions, median-crossing restrictions, and turn restrictions are not explicitly modeled."

### part-02

- Location: Discussion / Limitations and Future Research, opening sentence.
- Reason: State a concrete limitation without asserting an unmeasured effect size or claiming that all source carriageways are collapsed.
- Kila decisions: KILA-D-20260930-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T06:32:01Z
- Author: Kila
- Markup SHA-256 before: `1da0842bb9d4a8ac1c9356c4d9f1889aa03e3b38ded7526e62a77cc2fa6fa8ea`
- Markup SHA-256 after: `54b25af0976c450c3239d706e5098fd29cf2a079722c19a268b53d650312f6e9`
- Revision IDs: `2`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T153202058940.reviewer-1-comment-1.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The estimates depend on the represented road topology, connector rules, category-based speeds, fixed eligible-hospital roster, nearest-feasible-hospital assignment, and independent length-dependent failure mechanism.
~~~~

- After:

~~~~text
The estimates depend on the represented road topology, connector rules, category-based speeds, fixed eligible-hospital roster, nearest-feasible-hospital assignment, and independent length-dependent failure mechanism. On divided roads, the bidirectional centerline representation can admit movements that require a detour in practice because of carriageway direction or median restrictions, potentially understating travel times and overstating timely-access coverage. These constraints may also change section-level consequence rankings. Carriageway-specific geometry and directional and turn-restriction data are needed to assess these effects.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " On divided roads, the bidirectional centerline representation can admit movements that require a detour in practice because of carriageway direction or median restrictions, potentially understating travel times and overstating timely-access coverage. These constraints may also change section-level consequence rankings. Carriageway-specific geometry and directional and turn-restriction data are needed to assess these effects."

### part-03

- Location: Discussion / Limitations and Future Research, sentence after the added carriageway limitation
- Reason: Clarify the original pronoun after the approved insertion about required data; supplemental approval received.
- Kila decisions: KILA-D-20260930-002
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T06:37:02Z
- Author: Kila
- Markup SHA-256 before: `54b25af0976c450c3239d706e5098fd29cf2a079722c19a268b53d650312f6e9`
- Markup SHA-256 after: `df107fee27e85a1f605401ee59c804daa2ad61d8a0ec31f4f6ee241d2c387d41`
- Revision IDs: `3, 4`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T153703176314.reviewer-1-comment-1.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
They do not include ambulance availability, dispatch processing, on-scene treatment, congestion, hospital clinical capacity, engineering fragility, repair duration, or restoration cost.
~~~~

- After:

~~~~text
The estimates do not include ambulance availability, dispatch processing, on-scene treatment, congestion, hospital clinical capacity, engineering fragility, repair duration, or restoration cost.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "They"
     - After: "The estimates"

## reviewer-1/comment-2

### part-01

- Location: Materials and Methods / Emergency-Care Network and Analysis Units.
- Reason: Document the actual nonuniform specification without inventing empirical justification.
- Kila decisions: KILA-D-20260930-004, KILA-D-20260930-005
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T07:40:20Z
- Author: Kila
- Markup SHA-256 before: `df107fee27e85a1f605401ee59c804daa2ad61d8a0ec31f4f6ee241d2c387d41`
- Markup SHA-256 after: `f58d7ad8d5ca55592626615fd5589f29d734ff5219400a271da53e7efe4a94b2`
- Revision IDs: `5`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T164020655387.reviewer-1-comment-2.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Each routable edge receives a baseline travel time derived from its length and the assumed speed for its road category and width.
~~~~

- After:

~~~~text
Each routable edge receives a baseline travel time derived from its length and the assumed speed for its road category and width. Base speeds are 80 km/h for national expressways or equivalent roads, 50 km/h for national highways, 40 km/h for prefectural roads, 30 km/h for municipal roads or equivalent roads, and 20 km/h for other or unknown categories. Width-based caps are 20, 30, 50, 60, and 80 km/h for widths below 3 m, 3 to below 5.5 m, 5.5 to below 13 m, 13 to below 19.5 m, and at least 19.5 m, respectively; unknown width receives a 20 km/h cap. Each edge uses the lower of its category speed and width cap. These values are modeling assumptions rather than empirically calibrated ambulance operating speeds.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Base speeds are 80 km/h for national expressways or equivalent roads, 50 km/h for national highways, 40 km/h for prefectural roads, 30 km/h for municipal roads or equivalent roads, and 20 km/h for other or unknown categories. Width-based caps are 20, 30, 50, 60, and 80 km/h for widths below 3 m, 3 to below 5.5 m, 5.5 to below 13 m, 13 to below 19.5 m, and at least 19.5 m, respectively; unknown width receives a 20 km/h cap. Each edge uses the lower of its category speed and width cap. These values are modeling assumptions rather than empirically calibrated ambulance operating speeds."

### part-02

- Location: Materials and Methods / Monte Carlo Convergence and Sensitivity Analysis.
- Reason: Define the added analysis, paired comparison and assumptions without changing the primary model.
- Kila decisions: KILA-D-20260930-004, KILA-D-20260930-005
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T07:40:29Z
- Author: Kila
- Markup SHA-256 before: `f58d7ad8d5ca55592626615fd5589f29d734ff5219400a271da53e7efe4a94b2`
- Markup SHA-256 after: `cda87d2a9a744997deaf05ca807eb966e22013e705927369f410a8d680111d2b`
- Revision IDs: `6`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T164029360586.reviewer-1-comment-2.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Monte Carlo standard error is reported as a precision diagnostic rather than an additional pass condition.
~~~~

- After:

~~~~text
Monte Carlo standard error is reported as a precision diagnostic rather than an additional pass condition. Two additional scenarios reduce effective, width-capped speeds by 20% on either national expressways and national highways (A) or prefectural and municipal roads (B), leaving other categories unchanged. Connector speeds follow their referenced access edges. Both routing stages are recomputed for each scenario using the same 1,000 failure draws at each expected failed-road-length share of 1%, 3%, 5%, and 10%. Paired comparisons assess 30-minute population coverage, grid access probabilities, and hospital reassignment among residents with a reachable complete emergency chain. The perturbation magnitude is a sensitivity setting, not an estimated speed error.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Two additional scenarios reduce effective, width-capped speeds by 20% on either national expressways and national highways (A) or prefectural and municipal roads (B), leaving other categories unchanged. Connector speeds follow their referenced access edges. Both routing stages are recomputed for each scenario using the same 1,000 failure draws at each expected failed-road-length share of 1%, 3%, 5%, and 10%. Paired comparisons assess 30-minute population coverage, grid access probabilities, and hospital reassignment among residents with a reachable complete emergency chain. The perturbation magnitude is a sensitivity setting, not an estimated speed error."

### part-03

- Location: Results / Convergence and Sensitivity Analysis, closing sentence.
- Reason: Report supported magnitudes and local variation, rather than claiming invariance from a uniform speed test. Ranges span the four failure severities, not uncertainty intervals.
- Kila decisions: KILA-D-20260930-004, KILA-D-20260930-005
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T07:40:38Z
- Author: Kila
- Markup SHA-256 before: `cda87d2a9a744997deaf05ca807eb966e22013e705927369f410a8d680111d2b`
- Markup SHA-256 after: `dd3709d4f7e71fc0b0c32b5575d323723c81553e6ad19228b8a656cda8f96ede`
- Revision IDs: `7`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T164038408365.reviewer-1-comment-2.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The convergence result supports use of the full experiment for substantive comparisons and uncertainty summaries.
~~~~

- After:

~~~~text
The convergence result supports use of the full experiment for substantive comparisons and uncertainty summaries. Under category-specific speed reductions, mean 30-minute coverage decreases relative to original speeds in the same failed networks by 18,955–25,788 residents in scenario A and 31,494–39,449 in scenario B across the four failure severities. The corresponding population-weighted probability reductions are 1.09–1.48 and 1.81–2.27 percentage points. Hospital assignments change for an average of 3.60–3.85% and 2.76–2.87% of reachable residents, respectively, while network disconnection remains unchanged. Grid-level effects are more concentrated: the 95th percentile of absolute access-probability reductions across grids ranges from 3.0 to 13.9 percentage points in A and 13.2 to 35.0 in B. These comparisons show sensitivity of timely coverage and hospital allocation to relative road-type speeds, which uniform speed scaling does not capture.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Under category-specific speed reductions, mean 30-minute coverage decreases relative to original speeds in the same failed networks by 18,955–25,788 residents in scenario A and 31,494–39,449 in scenario B across the four failure severities. The corresponding population-weighted probability reductions are 1.09–1.48 and 1.81–2.27 percentage points. Hospital assignments change for an average of 3.60–3.85% and 2.76–2.87% of reachable residents, respectively, while network disconnection remains unchanged. Grid-level effects are more concentrated: the 95th percentile of absolute access-probability reductions across grids ranges from 3.0 to 13.9 percentage points in A and 13.2 to 35.0 in B. These comparisons show sensitivity of timely coverage and hospital allocation to relative road-type speeds, which uniform speed scaling does not capture."

### part-04

- Location: Discussion / Limitations and Future Research.
- Reason: Identify the data needed to calibrate the assumed speeds while preserving the original discussion.
- Kila decisions: KILA-D-20260930-004, KILA-D-20260930-005
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T07:40:58Z
- Author: Kila
- Markup SHA-256 before: `dd3709d4f7e71fc0b0c32b5575d323723c81553e6ad19228b8a656cda8f96ede`
- Markup SHA-256 after: `829158defce8a9a834bd9af3fd1c820f01877b45f26f0cbc43d3a3b743b72e95`
- Revision IDs: `8`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T164059181658.reviewer-1-comment-2.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Ambulance movement records could refine dispatch and destination behavior, and complete hospital capacity data could support explicitly weighted alternatives to minimum-time assignment.
~~~~

- After:

~~~~text
Ambulance movement records could calibrate category-specific speeds and refine dispatch and destination behavior, and complete hospital capacity data could support explicitly weighted alternatives to minimum-time assignment.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " calibrate category-specific speeds and"

## reviewer-1/comment-4

### part-01

- Location: Methods / Length-Dependent Road-Failure Experiment, opening paragraph.
- Reason: State exactly how the current model treats structure types rather than implying that mapped attributes enter the probability model.
- Kila decisions: KILA-D-20260930-007
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T07:56:37Z
- Author: Kila
- Markup SHA-256 before: `829158defce8a9a834bd9af3fd1c820f01877b45f26f0cbc43d3a3b743b72e95`
- Markup SHA-256 after: `377c7e89baaeb431e0037aa076c0f3580d1186c2fd7913550b9dacb30c593e82`
- Revision IDs: `9`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T165637821271.reviewer-1-comment-4.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
This functional form compares sections within a transparent random-failure scenario; mapped hazard categories are used for grouped interpretation rather than substituted for an unavailable engineering fragility model.
~~~~

- After:

~~~~text
This functional form compares sections within a transparent random-failure scenario; mapped hazard categories are used for grouped interpretation rather than substituted for an unavailable engineering fragility model. At a given severity, sections of equal length receive the same failure probability, without a separate adjustment for bridges or elevated roads.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " At a given severity, sections of equal length receive the same failure probability, without a separate adjustment for bridges or elevated roads."

### part-02

- Location: Discussion / Limitations and Future Research.
- Reason: Explicitly acknowledge the omission, explain its model implications without asserting an unmeasured direction or magnitude, and identify a path to refinement.
- Kila decisions: KILA-D-20260930-007
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T07:57:07Z
- Author: Kila
- Markup SHA-256 before: `377c7e89baaeb431e0037aa076c0f3580d1186c2fd7913550b9dacb30c593e82`
- Markup SHA-256 after: `8a05924b5be2a69a059113776c986a5846dcd4628101ba08e4b09f0a177f9aa0`
- Revision IDs: `10, 11`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T165707935823.reviewer-1-comment-4.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Future work can replace scenario probabilities with verified engineering fragility or observed closure data while retaining the routing and outcome framework.
~~~~

- After:

~~~~text
Differences in bridge and elevated-road fragility are not represented by the length-only failure model. Such heterogeneity could change the spatial pattern of road disruption and the resulting probability-weighted emergency-access losses, even at the same expected failed-road-length share. Future work can replace scenario probabilities with verified engineering fragility or observed closure data while retaining the routing and outcome framework. Bridge and elevated-road inventories linked to structural-condition, shaking-intensity, and fragility data would support this refinement.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "Differences in bridge and elevated-road fragility are not represented by the length-only failure model. Such heterogeneity could change the spatial pattern of road disruption and the resulting probability-weighted emergency-access losses, even at the same expected failed-road-length share. "
  2. `insert`
     - Before: ""
     - After: " Bridge and elevated-road inventories linked to structural-condition, shaking-intensity, and fragility data would support this refinement."

## reviewer-1/comment-5

### part-01

- Location: Methods / Study Area and Data Sources, first sentence.
- Reason: Provide verified geographic, population and modeled road network context requested by reviewer.
- Kila decisions: KILA-D-20260930-009
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T08:09:21Z
- Author: Kila
- Markup SHA-256 before: `8a05924b5be2a69a059113776c986a5846dcd4628101ba08e4b09f0a177f9aa0`
- Markup SHA-256 after: `ba355fe3c302ec1c4869fb63cd8d4c332cafc817fa84c68a53cd46eae7d6e229`
- Revision IDs: `12`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T170921319768.reviewer-1-comment-5.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The study covers Kumamoto Prefecture and represents emergency access as a cross-sectional network simulation.
~~~~

- After:

~~~~text
The study covers Kumamoto Prefecture and represents emergency access as a cross-sectional network simulation. Located in central Kyushu, the prefecture includes mountainous terrain to the east and south, the Aso caldera, and western coastal and island areas facing the Ariake and Yatsushiro seas. The study's 2020 population baseline comprises 1,738,301 residents in 62,945 populated 125 m meshes. The eligible modeled road network spans 42,949 km across 343,844 junction-to-junction sections. By represented road length, municipal roads or equivalent roads account for 88.9%, prefectural roads for 7.1%, national highways for 3.0%, national expressways or equivalent roads for 0.6%, and other roads for 0.4%.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Located in central Kyushu, the prefecture includes mountainous terrain to the east and south, the Aso caldera, and western coastal and island areas facing the Ariake and Yatsushiro seas. The study's 2020 population baseline comprises 1,738,301 residents in 62,945 populated 125 m meshes. The eligible modeled road network spans 42,949 km across 343,844 junction-to-junction sections. By represented road length, municipal roads or equivalent roads account for 88.9%, prefectural roads for 7.1%, national highways for 3.0%, national expressways or equivalent roads for 0.6%, and other roads for 0.4%."
