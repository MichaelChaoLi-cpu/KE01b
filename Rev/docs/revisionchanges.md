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

