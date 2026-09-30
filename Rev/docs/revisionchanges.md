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

## reviewer-1/comment-3


### figure-01

- Timestamp: 2026-09-30T10:03:58Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 1. Population demand and emergency-care network across Kumamoto
- Before: media/image1.png; preserved within tracked deletion 13.
- After: data/exp/r1c3_revised_figures/Figure_01.png, SHA-256 11ff9241921c8582d7ea307575f0c771763be6aa3dd44bc2243bed69bc51da9b; tracked insertion 14.
- Markup SHA-256 before: ba355fe3c302ec1c4869fb63cd8d4c332cafc817fa84c68a53cd46eae7d6e229
- Markup SHA-256 after: b1cfeb97bae35f3a3d3a7afaf559bdcf1e2e154713fcde0dd1c034e21eeea9cb
- Backup: Rev/revision/.kila-backups/R1C3-figure-01-ba355fe3c302.docx
- Extent: 5486400 x 5465064 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-02

- Timestamp: 2026-09-30T10:03:59Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 2. Baseline dispatch, hospital transport, and total emergency travel times
- Before: media/image2.png; preserved within tracked deletion 15.
- After: data/exp/r1c3_revised_figures/Figure_02.png, SHA-256 071fdca7a8b5f1fc855cb4cd89d95ccf545cbf586ecc37f2da2be8e11010925c; tracked insertion 16.
- Markup SHA-256 before: b1cfeb97bae35f3a3d3a7afaf559bdcf1e2e154713fcde0dd1c034e21eeea9cb
- Markup SHA-256 after: 57bd275006915f5dbc2dbc22029487fed7befe78c63ba7e330004f6d47396fc8
- Backup: Rev/revision/.kila-backups/R1C3-figure-02-b1cfeb97bae3.docx
- Extent: 5486400 x 6077712 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-03

- Timestamp: 2026-09-30T10:04:00Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 3. Emergency-access response to increasing failed road length
- Before: media/image3.png; preserved within tracked deletion 17.
- After: data/exp/r1c3_revised_figures/Figure_03.png, SHA-256 5473d4a08a477e1b9d0390aa5758797027bcc09e32a7437dc1c1f15842745dc3; tracked insertion 18.
- Markup SHA-256 before: 57bd275006915f5dbc2dbc22029487fed7befe78c63ba7e330004f6d47396fc8
- Markup SHA-256 after: e6c1ba7ac509d4db7616d0e6667ef05faaa889d6881e0531c809d16afb2fe58e
- Backup: Rev/revision/.kila-backups/R1C3-figure-03-57bd27500691.docx
- Extent: 5486400 x 2685288 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-04

- Timestamp: 2026-09-30T10:04:00Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 4. Nested road-failure realizations across main and stress severities
- Before: media/image4.png; preserved within tracked deletion 19.
- After: data/exp/r1c3_revised_figures/Figure_04.png, SHA-256 9401d1b6b47da0947c3350dd1447a85b407b243d3fa084e2cb73b9baf753c351; tracked insertion 20.
- Markup SHA-256 before: e6c1ba7ac509d4db7616d0e6667ef05faaa889d6881e0531c809d16afb2fe58e
- Markup SHA-256 after: bd1fabfb9ee5da062f2dec1cf8b77e0529e934fabbdc45bb4a4186800f76d8d7
- Backup: Rev/revision/.kila-backups/R1C3-figure-04-e6c1ba7ac509.docx
- Extent: 5486400 x 5401056 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-05

- Timestamp: 2026-09-30T10:04:02Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 5. Grid probability of losing baseline 30-minute emergency access
- Before: media/image5.png; preserved within tracked deletion 21.
- After: data/exp/r1c3_revised_figures/Figure_05.png, SHA-256 1be49969da4fe8136623157772d51ab48855895eca7b527c6f513ce61f67b498; tracked insertion 22.
- Markup SHA-256 before: bd1fabfb9ee5da062f2dec1cf8b77e0529e934fabbdc45bb4a4186800f76d8d7
- Markup SHA-256 after: 94313db6bcdc75bd681ff9c481ebcc153e76114cb2bdc869d7dff9e7c72c8f67
- Backup: Rev/revision/.kila-backups/R1C3-figure-05-bd1fabfb9ee5.docx
- Extent: 5486400 x 5716524 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-06

- Timestamp: 2026-09-30T10:04:03Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 6. Population coverage retained across failure severity and thresholds
- Before: media/image6.png; preserved within tracked deletion 23.
- After: data/exp/r1c3_revised_figures/Figure_06.png, SHA-256 71fe7fc018de66fd0ca4c3e1d11a4040559b8878684b216611bb175b40d6a4dd; tracked insertion 24.
- Markup SHA-256 before: 94313db6bcdc75bd681ff9c481ebcc153e76114cb2bdc869d7dff9e7c72c8f67
- Markup SHA-256 after: f0b1a65e63ee8df2366b2a3dacd16405dfa014dff3cd5ed58f1efc7700a71a2e
- Backup: Rev/revision/.kila-backups/R1C3-figure-06-94313db6bcdc.docx
- Extent: 5486400 x 3009900 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-07

- Timestamp: 2026-09-30T10:04:04Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 7. Hospital catchment reliability under increasing road failure
- Before: media/image7.png; preserved within tracked deletion 25.
- After: data/exp/r1c3_revised_figures/Figure_07.png, SHA-256 c0407754f4e5ed8895f51635d12d627ef3088383b22c05950e8ee6d08c05b533; tracked insertion 26.
- Markup SHA-256 before: f0b1a65e63ee8df2366b2a3dacd16405dfa014dff3cd5ed58f1efc7700a71a2e
- Markup SHA-256 after: 9f4898fbfdd51af7a68624765d3a790dd82d6a6cd8f62759a9981b34007702e2
- Backup: Rev/revision/.kila-backups/R1C3-figure-07-f0b1a65e63ee.docx
- Extent: 5486400 x 5873496 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-08

- Timestamp: 2026-09-30T10:04:06Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 8. Road-section accessibility consequence and expected risk surfaces
- Before: media/image8.png; preserved within tracked deletion 27.
- After: data/exp/r1c3_revised_figures/Figure_08.png, SHA-256 0f6e6c274f583a1b56becf76e107924f007edc57e368ad7a58601b4d2af5ce4b; tracked insertion 28.
- Markup SHA-256 before: 9f4898fbfdd51af7a68624765d3a790dd82d6a6cd8f62759a9981b34007702e2
- Markup SHA-256 after: 13ee0830d02849dc664d7173de244539f9ab4ec5c6e0bb7e85690800d012b547
- Backup: Rev/revision/.kila-backups/R1C3-figure-08-9f4898fbfdd5.docx
- Extent: 5486400 x 4829556 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.


### figure-09

- Timestamp: 2026-09-30T10:04:08Z
- Mode: authorized-tracked-picture-replacement
- Decision: KILA-D-20260930-015
- Location: image preceding Figure 9. Monte Carlo convergence, stress severity, and speed sensitivity
- Before: media/image9.png; preserved within tracked deletion 29.
- After: data/exp/r1c3_revised_figures/Figure_09.png, SHA-256 f86c3041cbf17303ceaf580e4b786cd7c4e3ec2063a384942bdffdff92c17e87; tracked insertion 30.
- Markup SHA-256 before: 13ee0830d02849dc664d7173de244539f9ab4ec5c6e0bb7e85690800d012b547
- Markup SHA-256 after: 2b91cc8aba62d6cdec0422a428a1a867f29acb0235066be30c392f6c43ad317a
- Backup: Rev/revision/.kila-backups/R1C3-figure-09-13ee0830d028.docx
- Extent: 5486400 x 4453128 EMU, six-inch width, preserved aspect ratio.
- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.

## reviewer-2/comment-3


### part-01

- Mode: authorized-tracked-insertion
- Decision: KILA-D-20260930-020
- Location: After Materials and Methods; before Study Area and Data Sources
- Timestamp: 2026-09-30T11:21:51Z
- Before: no inserted content at this location
- After:

~~~~text
Figure 1 summarizes the methodological workflow. Spatial inputs are integrated into a junction-to-junction road network to establish baseline dispatch-to-patient and patient-to-hospital travel times. Two complementary analyses then use this common baseline: paired length-dependent road-failure simulations quantify grid, population, and hospital reliability, whereas separate removal of each road section measures potential accessibility loss and its probability-weighted expected risk. Convergence and speed-sensitivity checks assess the simulation estimates.
~~~~

- Revision IDs: [31, 32]
- Markup SHA-256 before: 2b91cc8aba62d6cdec0422a428a1a867f29acb0235066be30c392f6c43ad317a
- Markup SHA-256 after: 77cb959dc77f047537f01982750454b08d1118b3e867f17a3be3bdb3fc41308f
- Backup: Rev/revision/.kila-backups/R2C3-part-01-2b91cc8aba62.docx
- Checks: existing XML restored by removal of inserted paragraphs; original media, endnotes and prior revisions preserved; source paragraph/run styles reused.

### part-02

- Location: Methods/Results figure callout, current clean paragraph index 33 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:21:52Z
- Author: Kila
- Markup SHA-256 before: `77cb959dc77f047537f01982750454b08d1118b3e867f17a3be3bdb3fc41308f`
- Markup SHA-256 after: `bede85b391d3e03fd4fdf5c477f7ae5508ce6373ee2876cd3ccd8a241a651174`
- Revision IDs: `33, 34`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202153861850.reviewer-2-comment-3.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 1 maps these demand supports together with the road network, primary and secondary emergency roads, candidate dispatch bases, and eligible hospitals.
~~~~

- After:

~~~~text
Figure 2 maps these demand supports together with the road network, primary and secondary emergency roads, candidate dispatch bases, and eligible hospitals.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "1"
     - After: "2"

### part-03

- Location: Methods/Results figure callout, current clean paragraph index 97 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:21:54Z
- Author: Kila
- Markup SHA-256 before: `bede85b391d3e03fd4fdf5c477f7ae5508ce6373ee2876cd3ccd8a241a651174`
- Markup SHA-256 after: `dad9a23f56e0d3972add2cbcef626712496c5140a7d7a7bb2c2fd1fdb8f623a0`
- Revision IDs: `35, 36`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202155482891.reviewer-2-comment-3.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 2 shows that the dispatch, hospital-transport, and combined two-stage surfaces have related but nonidentical spatial patterns.
~~~~

- After:

~~~~text
Figure 3 shows that the dispatch, hospital-transport, and combined two-stage surfaces have related but nonidentical spatial patterns.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "2"
     - After: "3"

### part-04

- Location: Methods/Results figure callout, current clean paragraph index 100 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:21:56Z
- Author: Kila
- Markup SHA-256 before: `dad9a23f56e0d3972add2cbcef626712496c5140a7d7a7bb2c2fd1fdb8f623a0`
- Markup SHA-256 after: `972f10c5986465c5ce2f7f23e3b0894dd74a7279f1b3d6f03983948116e1ad52`
- Revision IDs: `37, 38`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202157093331.reviewer-2-comment-3.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 3 reports an ordered response across the calibration range.
~~~~

- After:

~~~~text
Figure 4 reports an ordered response across the calibration range.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "3"
     - After: "4"

### part-05

- Location: Methods/Results figure callout, current clean paragraph index 100 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:21:57Z
- Author: Kila
- Markup SHA-256 before: `972f10c5986465c5ce2f7f23e3b0894dd74a7279f1b3d6f03983948116e1ad52`
- Markup SHA-256 after: `51c3737c90ee01352959f97a0f0ab1a77cb1ea8238473e958a55f9b58c5ef565`
- Revision IDs: `39, 40`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202158665507.reviewer-2-comment-3.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The paired realization in Figure 4 confirms the intended nesting visually.
~~~~

- After:

~~~~text
The paired realization in Figure 5 confirms the intended nesting visually.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "4"
     - After: "5"

### part-06

- Location: Methods/Results figure callout, current clean paragraph index 103 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:21:59Z
- Author: Kila
- Markup SHA-256 before: `51c3737c90ee01352959f97a0f0ab1a77cb1ea8238473e958a55f9b58c5ef565`
- Markup SHA-256 after: `d66754ea42313580a3e88a5031d6b393561f299d310b32afce4a868b58345173`
- Revision IDs: `41, 42`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202200245074.reviewer-2-comment-3.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 5 maps a marked expansion in the population exposed to loss of baseline 30-minute access.
~~~~

- After:

~~~~text
Figure 6 maps a marked expansion in the population exposed to loss of baseline 30-minute access.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "5"
     - After: "6"

### part-07

- Location: Methods/Results figure callout, current clean paragraph index 106 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:00Z
- Author: Kila
- Markup SHA-256 before: `d66754ea42313580a3e88a5031d6b393561f299d310b32afce4a868b58345173`
- Markup SHA-256 after: `46a196e5d474efb459359742db603e8c0e410394654351b4a313bc8f9f8bb7d7`
- Revision IDs: `43, 44`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202201805746.reviewer-2-comment-3.part-07.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 6 shows monotonic declines in retained baseline coverage at all three timely thresholds.
~~~~

- After:

~~~~text
Figure 7 shows monotonic declines in retained baseline coverage at all three timely thresholds.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "6"
     - After: "7"

### part-08

- Location: Methods/Results figure callout, current clean paragraph index 109 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:02Z
- Author: Kila
- Markup SHA-256 before: `46a196e5d474efb459359742db603e8c0e410394654351b4a313bc8f9f8bb7d7`
- Markup SHA-256 after: `8446015d35f0f31a150f06f006bdf0175c18d4f13cdc5a1fb0eec5d866d93f25`
- Revision IDs: `45, 46`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202203370796.reviewer-2-comment-3.part-08.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 7 shows simultaneous positive and negative changes in mean hospital catchments.
~~~~

- After:

~~~~text
Figure 8 shows simultaneous positive and negative changes in mean hospital catchments.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "7"
     - After: "8"

### part-09

- Location: Methods/Results figure callout, current clean paragraph index 112 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:04Z
- Author: Kila
- Markup SHA-256 before: `8446015d35f0f31a150f06f006bdf0175c18d4f13cdc5a1fb0eec5d866d93f25`
- Markup SHA-256 after: `d4d244e7158d05f191f3d962293d56b5c5001489868317cb13912581a0313c72`
- Revision IDs: `47, 48`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202204997277.reviewer-2-comment-3.part-09.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 8 maps nonzero potential loss for 41,178 sections at the 15-minute threshold, 55,192 at 30 minutes, and 55,717 at 45 minutes.
~~~~

- After:

~~~~text
Figure 9 maps nonzero potential loss for 41,178 sections at the 15-minute threshold, 55,192 at 30 minutes, and 55,717 at 45 minutes.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "8"
     - After: "9"

### part-10

- Location: Methods/Results figure callout, current clean paragraph index 116 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:05Z
- Author: Kila
- Markup SHA-256 before: `d4d244e7158d05f191f3d962293d56b5c5001489868317cb13912581a0313c72`
- Markup SHA-256 after: `f791579050cbaeb610db4d998302595c075e441535de3bbae23969f9ec68f00a`
- Revision IDs: `49, 50`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202206582338.reviewer-2-comment-3.part-10.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 9 shows nearly flat running coverage means after the early checkpoints and declining Monte Carlo standard errors as replicates accumulate.
~~~~

- After:

~~~~text
Figure 10 shows nearly flat running coverage means after the early checkpoints and declining Monte Carlo standard errors as replicates accumulate.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "9"
     - After: "10"

### part-11

- Location: Figures section, current clean paragraph index 149 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:07Z
- Author: Kila
- Markup SHA-256 before: `f791579050cbaeb610db4d998302595c075e441535de3bbae23969f9ec68f00a`
- Markup SHA-256 after: `b1b7b6887daeeec065fc31afb8246e57e71241ce5643e4a608f79921bb4707dc`
- Revision IDs: `51, 52`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202208142463.reviewer-2-comment-3.part-11.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 1. Population demand and emergency-care network across Kumamoto
~~~~

- After:

~~~~text
Figure 2. Population demand and emergency-care network across Kumamoto
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "1"
     - After: "2"

### part-12

- Location: Figures section, current clean paragraph index 153 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:08Z
- Author: Kila
- Markup SHA-256 before: `b1b7b6887daeeec065fc31afb8246e57e71241ce5643e4a608f79921bb4707dc`
- Markup SHA-256 after: `088e2670a8cbab6d1b379d49c8c4eb68b3b434a808ac5c6923b50e92bc6454cf`
- Revision IDs: `53, 54`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202209690577.reviewer-2-comment-3.part-12.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 2. Baseline dispatch, hospital transport, and total emergency travel times
~~~~

- After:

~~~~text
Figure 3. Baseline dispatch, hospital transport, and total emergency travel times
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "2"
     - After: "3"

### part-13

- Location: Figures section, current clean paragraph index 157 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:10Z
- Author: Kila
- Markup SHA-256 before: `088e2670a8cbab6d1b379d49c8c4eb68b3b434a808ac5c6923b50e92bc6454cf`
- Markup SHA-256 after: `b14edb1ca43a765e6f003a5d8254ddb208cf40d3f182159b69995ada3309c91d`
- Revision IDs: `55, 56`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202211239414.reviewer-2-comment-3.part-13.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 3. Emergency-access response to increasing failed road length
~~~~

- After:

~~~~text
Figure 4. Emergency-access response to increasing failed road length
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "3"
     - After: "4"

### part-14

- Location: Figures section, current clean paragraph index 161 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:11Z
- Author: Kila
- Markup SHA-256 before: `b14edb1ca43a765e6f003a5d8254ddb208cf40d3f182159b69995ada3309c91d`
- Markup SHA-256 after: `26c6bc0fc1f35944df722402e8bfb158d4fbba34abeaea897414e17061a0c12a`
- Revision IDs: `57, 58`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202212838716.reviewer-2-comment-3.part-14.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 4. Nested road-failure realizations across main and stress severities
~~~~

- After:

~~~~text
Figure 5. Nested road-failure realizations across main and stress severities
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "4"
     - After: "5"

### part-15

- Location: Figures section, current clean paragraph index 165 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:13Z
- Author: Kila
- Markup SHA-256 before: `26c6bc0fc1f35944df722402e8bfb158d4fbba34abeaea897414e17061a0c12a`
- Markup SHA-256 after: `65cbc9895c3a9c477e6cc8c7a83978e8212c9b35659a0b9c3f40f78d081de985`
- Revision IDs: `59, 60`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202214415070.reviewer-2-comment-3.part-15.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 5. Grid probability of losing baseline 30-minute emergency access
~~~~

- After:

~~~~text
Figure 6. Grid probability of losing baseline 30-minute emergency access
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "5"
     - After: "6"

### part-16

- Location: Figures section, current clean paragraph index 169 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:15Z
- Author: Kila
- Markup SHA-256 before: `65cbc9895c3a9c477e6cc8c7a83978e8212c9b35659a0b9c3f40f78d081de985`
- Markup SHA-256 after: `d9b893f2e6555e74107512b4b3723fc017349861c1aec26d98ab87ae737f4056`
- Revision IDs: `61, 62`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202216012598.reviewer-2-comment-3.part-16.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 6. Population coverage retained across failure severity and thresholds
~~~~

- After:

~~~~text
Figure 7. Population coverage retained across failure severity and thresholds
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "6"
     - After: "7"

### part-17

- Location: Figures section, current clean paragraph index 173 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:16Z
- Author: Kila
- Markup SHA-256 before: `d9b893f2e6555e74107512b4b3723fc017349861c1aec26d98ab87ae737f4056`
- Markup SHA-256 after: `a54c97273fb90a47da538d7dbeaa79dc9c60693ab5e2889196f6f7ebb150df41`
- Revision IDs: `63, 64`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202217684600.reviewer-2-comment-3.part-17.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 7. Hospital catchment reliability under increasing road failure
~~~~

- After:

~~~~text
Figure 8. Hospital catchment reliability under increasing road failure
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "7"
     - After: "8"

### part-18

- Location: Figures section, current clean paragraph index 177 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:18Z
- Author: Kila
- Markup SHA-256 before: `a54c97273fb90a47da538d7dbeaa79dc9c60693ab5e2889196f6f7ebb150df41`
- Markup SHA-256 after: `5f61a3c8bcc423d2bbbdc21bbb050ab4c7d907a2525345b5585fdb12872e5ca7`
- Revision IDs: `65, 66`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202219279482.reviewer-2-comment-3.part-18.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 8. Road-section accessibility consequence and expected risk surfaces
~~~~

- After:

~~~~text
Figure 9. Road-section accessibility consequence and expected risk surfaces
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "8"
     - After: "9"

### part-19

- Location: Figures section, current clean paragraph index 181 (zero-based; exact text is the locator).
- Reason: Renumber existing figure after workflow Figure 1 insertion.
- Kila decisions: KILA-D-20260930-020
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:22:19Z
- Author: Kila
- Markup SHA-256 before: `5f61a3c8bcc423d2bbbdc21bbb050ab4c7d907a2525345b5585fdb12872e5ca7`
- Markup SHA-256 after: `096f99fac0bc6eeff7f5d71efcc94fbbf2601af61d6a0ffcde226a1435161c9f`
- Revision IDs: `67, 68`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20260930T202220859153.reviewer-2-comment-3.part-19.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 9. Monte Carlo convergence, stress severity, and speed sensitivity
~~~~

- After:

~~~~text
Figure 10. Monte Carlo convergence, stress severity, and speed sensitivity
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "9"
     - After: "10"


### part-20

- Mode: authorized-tracked-insertion
- Decision: KILA-D-20260930-020
- Location: Figures section, before the previous first figure
- Timestamp: 2026-09-30T11:22:47Z
- Before: no inserted content at this location
- After:

~~~~text
[Workflow PNG: eeaada6a2908d04dc0d5168df7e245a76f9093a9b649d21529d5fd67ae79b219]
Figure 1. Methodological workflow for two-stage emergency medical access
Note: The shared network and baseline support two complementary analyses. Random-failure simulations use 1,000 paired replicates at 1%, 3%, and 5% expected failed road length, with 10% as a stress scenario. Single-section analysis removes each section separately from the baseline network and combines potential population loss with the section failure probability to calculate expected risk. Timely access is evaluated at 15, 30, and 45 minutes, with 30 minutes as the primary threshold.
~~~~

- Revision IDs: [69, 70, 71, 72, 73, 74]
- Markup SHA-256 before: 096f99fac0bc6eeff7f5d71efcc94fbbf2601af61d6a0ffcde226a1435161c9f
- Markup SHA-256 after: 2af639ba4120034f2e87767e4ef8372d9fdf9e499215e574c6381ccc34c7617e
- Backup: Rev/revision/.kila-backups/R2C3-part-20-096f99fac0bc.docx
- Checks: existing XML restored by removal of inserted paragraphs; original media, endnotes and prior revisions preserved; source paragraph/run styles reused.

## reviewer-2/comment-6

### part-01

- Location: Abstract, second sentence.
- Reason: state the method-level positioning at the start of the paper without changing numerical findings.
- Kila decisions: KILA-D-20260930-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:44:37Z
- Author: Kila
- Markup SHA-256 before: `2af639ba4120034f2e87767e4ef8372d9fdf9e499215e574c6381ccc34c7617e`
- Markup SHA-256 after: `e6fd9225f42557e8c2830de377591135c7c12855b33d6390ab912ff1e09fd9f1`
- Revision IDs: `75, 76, 77`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T204439102177.reviewer-2-comment-6.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `d8896a5d8a384489adf05857f50ad8f501569380b48ab49b37858cd7b58c8d6b`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Following the 28 July 2026 Kumamoto earthquake (M7.1), we assess this complete chain across Kumamoto Prefecture, Japan.
~~~~

- After:

~~~~text
We present a reusable network framework for assessing this complete chain and demonstrate it in Kumamoto Prefecture, Japan, following the 28 July 2026 Kumamoto earthquake (M7.1).
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Following"
     - After: "We present a reusable network framework for assessing this complete chain and demonstrate it in Kumamoto Prefecture, Japan, following"
  2. `delete`
     - Before: ", we assess this complete chain across Kumamoto Prefecture, Japan"
     - After: ""

### part-02

- Location: Materials and Methods / Study Area and Data Sources, opening sentence.
- Reason: make transfer requirements explicit within the method description rather than relying solely on the Discussion.
- Kila decisions: KILA-D-20260930-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:44:50Z
- Author: Kila
- Markup SHA-256 before: `e6fd9225f42557e8c2830de377591135c7c12855b33d6390ab912ff1e09fd9f1`
- Markup SHA-256 after: `835f3b0277f798a02cae47f31152df96b7817183d834ca82e3dcc258ef888731`
- Revision IDs: `78, 79, 80, 81`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T204451872418.reviewer-2-comment-6.part-02.docx`
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
The framework represents emergency access as a cross-sectional network simulation, with Kumamoto Prefecture as the case study. Its core inputs are a routable road network, spatial population demand, eligible dispatch bases, and eligible hospitals. The junction-based section definition, two-stage rerouting, paired failure simulation, and accessibility indicators are reusable across study areas; road speeds, connector rules, facility eligibility, timely-access thresholds, and failure-scenario parameters require local specification.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "study covers Kumamoto Prefecture and"
     - After: "framework"
  2. `insert`
     - Before: ""
     - After: ", with Kumamoto Prefecture as the case study"
  3. `insert`
     - Before: ""
     - After: " Its core inputs are a routable road network, spatial population demand, eligible dispatch bases, and eligible hospitals. The junction-based section definition, two-stage rerouting, paired failure simulation, and accessibility indicators are reusable across study areas; road speeds, connector rules, facility eligibility, timely-access thresholds, and failure-scenario parameters require local specification."

### part-03

- Location: Discussion / Limitations and Future Research, final sentence.
- Reason: explain how to transfer the method without transferring Kumamoto-specific results or assuming identical emergency-service organization.
- Kila decisions: KILA-D-20260930-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:45:03Z
- Author: Kila
- Markup SHA-256 before: `835f3b0277f798a02cae47f31152df96b7817183d834ca82e3dcc258ef888731`
- Markup SHA-256 after: `5531eb1af83ed070d76fe3a09ceab142629a403e41b004db2092438d2a176d35`
- Revision IDs: `82`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T204504631514.reviewer-2-comment-6.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The present network experiment provides the baseline quantities required for those extensions.
~~~~

- After:

~~~~text
The present network experiment provides the baseline quantities required for those extensions. Application elsewhere follows the same routing and outcome calculations after replacing the spatial inputs and specifying local service and failure assumptions. Dispatch bases can represent the locally responsible ambulance service rather than necessarily fire stations. Local validation of road connectivity, travel times, and facility eligibility supports that transfer; coverage estimates and section priorities must be recalculated for each study area.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Application elsewhere follows the same routing and outcome calculations after replacing the spatial inputs and specifying local service and failure assumptions. Dispatch bases can represent the locally responsible ambulance service rather than necessarily fire stations. Local validation of road connectivity, travel times, and facility eligibility supports that transfer; coverage estimates and section priorities must be recalculated for each study area."

### part-04

- Location: Conclusion, final sentence.
- Reason: align the closing statement with the Abstract and Methods positioning.
- Kila decisions: KILA-D-20260930-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T11:45:29Z
- Author: Kila
- Markup SHA-256 before: `5531eb1af83ed070d76fe3a09ceab142629a403e41b004db2092438d2a176d35`
- Markup SHA-256 after: `b93acbcb09b22aa19a3f1ef97290176582af395aa6becd29175449d0b64fa872`
- Revision IDs: `83, 84, 85, 86`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T204530755775.reviewer-2-comment-6.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The same framework also provides a reusable basis for future emergency preparedness across Kumamoto Prefecture.
~~~~

- After:

~~~~text
The same framework also provides a reusable basis for future emergency preparedness in Kumamoto and for assessments in other regions using locally specified network, demand, facility, and failure-scenario inputs.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "across"
     - After: "in"
  2. `replace`
     - Before: "Prefecture"
     - After: "and for assessments in other regions using locally specified network, demand, facility, and failure-scenario inputs"

## reviewer-2/comment-2

### part-01

- Location: Literature Review / Emergency Medical Service Accessibility, final sentence.
- Reason: evaluate the scope and tradeoffs of existing approaches and connect them to the present study without overstating novelty.
- Kila decisions: KILA-D-20260930-024
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T12:02:10Z
- Author: Kila
- Markup SHA-256 before: `b93acbcb09b22aa19a3f1ef97290176582af395aa6becd29175449d0b64fa872`
- Markup SHA-256 after: `67799f4fd8b65dd2f894b1ea00678eef85fd8c3184d7f195b02c4d88ed2fd942`
- Revision IDs: `87`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T210211442723.reviewer-2-comment-2.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Distributional analysis is therefore a distinct component of emergency-access assessment rather than a descriptive add-on (Utkarsh et al., 2022).
~~~~

- After:

~~~~text
Distributional analysis is therefore a distinct component of emergency-access assessment rather than a descriptive add-on (Utkarsh et al., 2022). The operational detail of ambulance-routing and hospital-assignment models is valuable for managing congestion and treatment delays, as illustrated by the model of Chou et al. (2022). That objective differs from identifying where repeated road failures prevent completion of the dispatch-to-patient-to-hospital chain. For the latter question, travel-time and coverage measures need to be recalculated jointly for both stages in each disrupted network, with losses distinguished across population groups and receiving hospitals.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The operational detail of ambulance-routing and hospital-assignment models is valuable for managing congestion and treatment delays, as illustrated by the model of Chou et al. (2022). That objective differs from identifying where repeated road failures prevent completion of the dispatch-to-patient-to-hospital chain. For the latter question, travel-time and coverage measures need to be recalculated jointly for both stages in each disrupted network, with losses distinguished across population groups and receiving hospitals."

### part-02

- Location: Literature Review / Road-Network Reliability under Disruption, final sentence.
- Reason: evaluate the scope and tradeoffs of existing approaches and connect them to the present study without overstating novelty.
- Kila decisions: KILA-D-20260930-024
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T12:02:23Z
- Author: Kila
- Markup SHA-256 before: `67799f4fd8b65dd2f894b1ea00678eef85fd8c3184d7f195b02c4d88ed2fd942`
- Markup SHA-256 after: `45aa69697f81660e4de002427b72f38c82d80d1997e2532f265a10302f928752`
- Revision IDs: `88`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T210224617647.reviewer-2-comment-2.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Repeated or scenario-based road-network analysis can characterize performance degradation and connectivity or accessibility consequences under disruption (Anthony et al., 2002; Erik & Lars‐Göran, 2012; Xiangdong et al., 2018).
~~~~

- After:

~~~~text
Repeated or scenario-based road-network analysis can characterize performance degradation and connectivity or accessibility consequences under disruption (Anthony et al., 2002; Erik & Lars‐Göran, 2012; Xiangdong et al., 2018). Area-covering disruption analysis shows why the impact of a single closure cannot stand in for the loss of several nearby alternatives: the spatial distribution of vulnerability changes with the disruption pattern. This makes the failure representation a substantive modeling choice, not simply a computational detail. The present independent length-dependent experiment complements spatially clustered disruption scenarios by isolating network response under a declared exposure rule; it does not reproduce their spatial dependence. Pairing repeated-failure estimates with separate single-section removals allows system reliability and individual-section consequence to be interpreted without conflating them.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Area-covering disruption analysis shows why the impact of a single closure cannot stand in for the loss of several nearby alternatives: the spatial distribution of vulnerability changes with the disruption pattern. This makes the failure representation a substantive modeling choice, not simply a computational detail. The present independent length-dependent experiment complements spatially clustered disruption scenarios by isolating network response under a declared exposure rule; it does not reproduce their spatial dependence. Pairing repeated-failure estimates with separate single-section removals allows system reliability and individual-section consequence to be interpreted without conflating them."

### part-03

- Location: Literature Review / Critical-Road Identification for Emergency Planning, final sentence.
- Reason: evaluate the scope and tradeoffs of existing approaches and connect them to the present study without overstating novelty.
- Kila decisions: KILA-D-20260930-024
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T12:02:50Z
- Author: Kila
- Markup SHA-256 before: `45aa69697f81660e4de002427b72f38c82d80d1997e2532f265a10302f928752`
- Markup SHA-256 after: `ebc0985e1f05d5be58697361e431d76bcbc53c13d532bc4249f5140d9aacb778`
- Revision IDs: `89`
- Backup: `Rev/revision/.kila-backups/KE01b.rev.markup.20260930T210251729480.reviewer-2-comment-2.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Critical-road and restoration analyses can screen links for protection, retrofit, inspection, or post-disaster reconnection, while operational restoration requires additional field information (Vahid et al., 2021).
~~~~

- After:

~~~~text
Critical-road and restoration analyses can screen links for protection, retrofit, inspection, or post-disaster reconnection, while operational restoration requires additional field information (Vahid et al., 2021). The evacuation-risk approach of Nitheesh and Bhavathrathan (2025) also shows that critical-link identification already combines probability and consequence. The remaining issue for emergency medical access is therefore the service consequence being measured: evacuation traffic and topological exposure answer a different planning question from population loss along a dispatch-to-patient-to-hospital chain. Our assessment uses that complete-chain coverage loss and reports it separately from scenario-weighted risk. These outputs support continuity screening, while restoration optimization additionally requires repair resources, costs, and interactions among damaged sections.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The evacuation-risk approach of Nitheesh and Bhavathrathan (2025) also shows that critical-link identification already combines probability and consequence. The remaining issue for emergency medical access is therefore the service consequence being measured: evacuation traffic and topological exposure answer a different planning question from population loss along a dispatch-to-patient-to-hospital chain. Our assessment uses that complete-chain coverage loss and reports it separately from scenario-weighted risk. These outputs support continuity screening, while restoration optimization additionally requires repair resources, costs, and interactions among damaged sections."

## reviewer-2/comment-1

### part-01

- Location: Introduction / Emergency Access and Road-Network Disruption, objective sentence.
- Reason: Replace the unestimated mandatory protection/repair-order claim with the actual section-consequence objective and its planning use.
- Kila decisions: KILA-D-20260930-026, KILA-D-20260930-027, KILA-D-20261001-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T22:44:05Z
- Author: Kila
- Markup SHA-256 before: `ebc0985e1f05d5be58697361e431d76bcbc53c13d532bc4249f5140d9aacb778`
- Markup SHA-256 after: `9691e8ab633b74f47a5937912192074eb4e5d51b37045d88a1f10876ac41b74c`
- Revision IDs: `90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20261001T074406592287.reviewer-2-comment-1.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `d8896a5d8a384489adf05857f50ad8f501569380b48ab49b37858cd7b58c8d6b`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
A primary objective of this study is therefore to determine which road sections must be kept open,  and, once damaged, restored first, in order to preserve continuous emergency medical access from dispatch base to patient to hospital.
~~~~

- After:

~~~~text
A primary objective of this study is therefore to identify road sections whose loss most reduces continuous emergency medical access from dispatch base to patient to hospital, providing evidence for continuity protection and post-disaster restoration screening.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "determine which"
     - After: "identify"
  2. `replace`
     - Before: "must"
     - After: "whose"
  3. `replace`
     - Before: "be"
     - After: "loss"
  4. `replace`
     - Before: "kept"
     - After: "most"
  5. `replace`
     - Before: "open,  and, once damaged, restored first, in order to preserve"
     - After: "reduces"
  6. `insert`
     - Before: ""
     - After: ", providing evidence for continuity protection and post-disaster restoration screening"

### part-02

- Location: Introduction / Emergency Access and Road-Network Disruption, final sentence.
- Reason: Replace only 'sequencing' with 'planning' to align the intended use with the objective.
- Kila decisions: KILA-D-20260930-026, KILA-D-20260930-027, KILA-D-20261001-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T22:44:18Z
- Author: Kila
- Markup SHA-256 before: `9691e8ab633b74f47a5937912192074eb4e5d51b37045d88a1f10876ac41b74c`
- Markup SHA-256 after: `ca69c8eb97e8975f9b35f7bdad3f191b5082b4b0784f187af9aa628ccbeca32c`
- Revision IDs: `101, 102`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20261001T074420331855.reviewer-2-comment-1.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `d8896a5d8a384489adf05857f50ad8f501569380b48ab49b37858cd7b58c8d6b`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The resulting prefecture-wide maps are accordingly intended as a screening layer for road inspection, continuity protection, and restoration sequencing, to be updated as field-verified damage information becomes available.
~~~~

- After:

~~~~text
The resulting prefecture-wide maps are accordingly intended as a screening layer for road inspection, continuity protection, and restoration planning, to be updated as field-verified damage information becomes available.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "sequencing"
     - After: "planning"

### part-03

- Location: Introduction / Research Gap and Contributions, final four sentences.
- Reason: Replace the undefined 'this gap' with a precise integration question and organize the existing analytical elements as three explicit contributions. Preserve the experiment description where useful; retain the preceding four literature-bearing sentences and their citations.
- Kila decisions: KILA-D-20260930-026, KILA-D-20260930-027, KILA-D-20261001-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-30T22:44:29Z
- Author: Kila
- Markup SHA-256 before: `ca69c8eb97e8975f9b35f7bdad3f191b5082b4b0784f187af9aa628ccbeca32c`
- Markup SHA-256 after: `5e6b54c393bfcdf4e9533ca23fc644fcfc22216b9078fcba965ced62c2fa97b4`
- Revision IDs: `103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155`
- Backup: `/Users/lichao/Research/KE01b/Rev/revision/.kila-backups/KE01b.rev.markup.20261001T074430612604.reviewer-2-comment-1.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
We address this gap with a reproducible, paired network experiment in which continuous junction-to-junction sections fail with probabilities that increase with their lengths. Every simulated state is fully rerouted, and the resulting evidence is organized at four connected levels: grid access, population and municipal coverage, hospital catchment stability, and road-section consequence. We also separate the potential access loss caused by removing one section from the probability-weighted expected risk of that section under a declared scenario. This structure supports full-network maps rather than an arbitrary short list of roads.
~~~~

- After:

~~~~text
These approaches establish tools for disruption assessment, but they answer different questions about operations, network vulnerability, and link criticality. The specific problem addressed here is how to connect reliability of the complete dispatch-to-patient-to-hospital chain under multiple road failures with the accessibility consequence of each road section, using a common network and population baseline. We address this problem with a reproducible, paired network experiment in which continuous junction-to-junction sections fail with probabilities that increase with their lengths. The study makes three linked contributions. First, every simulated state is fully rerouted through both emergency-care stages, linking grid access, population and municipal coverage, and hospital catchment stability within the same disrupted networks. Second, a separate single-section-removal analysis maps potential access loss for every eligible section and distinguishes this consequence from its probability-weighted expected risk under each declared scenario. Third, these complementary outputs connect the locations and populations exposed to unreliable emergency access with road-section evidence for continuity protection and restoration screening. Kumamoto demonstrates this reusable framework with locally specified inputs and failure scenarios.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "These approaches establish tools for disruption assessment, but they answer different questions about operations, network vulnerability, and link criticality. The specific problem addressed here is how to connect reliability of the complete dispatch-to-patient-to-hospital chain under multiple road failures with the accessibility consequence of each road section, using a common network and population baseline. "
  2. `replace`
     - Before: "gap"
     - After: "problem"
  3. `replace`
     - Before: "Every"
     - After: "The study makes three linked contributions. First, every"
  4. `insert`
     - Before: ""
     - After: " through both emergency-care stages"
  5. `replace`
     - Before: "and the resulting evidence is organized at four connected levels:"
     - After: "linking"
  6. `insert`
     - Before: ""
     - After: "and "
  7. `insert`
     - Before: ""
     - After: " within the same disrupted networks. Second"
  8. `replace`
     - Before: "and road-section consequence. We also"
     - After: "a"
  9. `replace`
     - Before: "the"
     - After: "single-section-removal analysis maps"
  10. `replace`
     - Before: "caused"
     - After: "for"
  11. `replace`
     - Before: "by"
     - After: "every"
  12. `replace`
     - Before: "removing one"
     - After: "eligible"
  13. `insert`
     - Before: ""
     - After: "and distinguishes this consequence "
  14. `replace`
     - Before: "the"
     - After: "its"
  15. `delete`
     - Before: "of that section "
     - After: ""
  16. `replace`
     - Before: "a"
     - After: "each"
  17. `replace`
     - Before: "This"
     - After: "Third,"
  18. `replace`
     - Before: "structure"
     - After: "these"
  19. `replace`
     - Before: "supports"
     - After: "complementary"
  20. `replace`
     - Before: "full-network"
     - After: "outputs"
  21. `replace`
     - Before: "maps"
     - After: "connect"
  22. `replace`
     - Before: "rather"
     - After: "the"
  23. `replace`
     - Before: "than"
     - After: "locations"
  24. `replace`
     - Before: "an"
     - After: "and"
  25. `replace`
     - Before: "arbitrary"
     - After: "populations"
  26. `replace`
     - Before: "short"
     - After: "exposed"
  27. `replace`
     - Before: "list"
     - After: "to"
  28. `replace`
     - Before: "of"
     - After: "unreliable"
  29. `replace`
     - Before: "roads"
     - After: "emergency access with road-section evidence for continuity protection and restoration screening"
  30. `insert`
     - Before: ""
     - After: " Kumamoto demonstrates this reusable framework with locally specified inputs and failure scenarios."

