[Read the synthesis](SYNTHESIS.md) · [Read the generation brief](GENERATION_BRIEF.md)

# Reference pilot 01 — complete, with qualifications

Nine aspect reports and a separate fresh synthesis are complete. The generation brief is **untested**; no images were generated and no generation-quality improvement is demonstrated.

## Scope and available references

- Analyzed: **four of 102 already available larger cards**, R1–R4 at 430×480, plus S1 (2796×1290 set/UI context) and G1/G2 (733×1034 reduced-resolution category guides). The other **98 available cards were not analyzed**; broader coverage can start with this existing local pack. R1–R4 are not an asserted complete product set. G2 gold-category character design is excluded from general non-gold requirements.
- Existing inventory: 122 larger files recorded as locally hash-verified: **102 cards, 16 sets, four templates**. Another **58 cards remain unretrieved** behind the public Miro signup gate. Those missing cards do not block further analysis of the local pack. Native-source provenance remains qualified.
- Larger files were already present, not downloaded for this run; **new browser acquisitions: 0**. Old thumbnails were untouched. The primary images used here are 430×480, not the old approximately 59×67 thumbnails.
- [Frozen inputs](inputs.json) and [checksum](inputs.sha256) fix this seven-image pack. Classical evidence is available; source-only learned estimators have no enabled weights or inference.

## Independent roles and separate synthesis

Each aspect used its own fresh native **observer** session: nine role-specific agents in nine sessions, not nine globally registered agents or nine different model types. First-pass isolation and subsequent own-role corrections/enrichments are recorded in the [session index](session_index.json); no other-role exposure is asserted for those enrichments. Read-path records support invocation provenance, not proof of successful visual access or absence of inherited context.

Synthesis ran in another fresh observer session: `ses_e68dd53bcffe4JlX7sg7Veh1ov`. Its [full unmodified response](raw_synthesis.md) and [capture metadata](validation/synthesis_capture.json) are retained. The readable synthesis changes only the required coverage clarification and adds evidence navigation; no art-analysis claims were rewritten.

## Report sources

| Role | Normalized source | Full raw response | Parsed source |
|---|---|---|---|
| lighting_shading | [JSON](reports/normalized/lighting_shading.json) | [raw](reports/raw/lighting_shading.md) | [JSON](reports/parsed/lighting_shading.json) |
| value_contrast | [JSON](reports/normalized/value_contrast.json) | [raw](reports/raw/value_contrast.md) | [JSON](reports/parsed/value_contrast.json) |
| color_palette | [JSON](reports/normalized/color_palette.json) | [raw](reports/raw/color_palette.md) | [JSON](reports/parsed/color_palette.json) |
| composition_hierarchy | [JSON](reports/normalized/composition_hierarchy.json) | [raw](reports/raw/composition_hierarchy.md) | [JSON](reports/parsed/composition_hierarchy.json) |
| shape_proportions | [JSON](reports/normalized/shape_proportions.json) | [raw](reports/raw/shape_proportions.md) | [JSON](reports/parsed/shape_proportions.json) |
| viewpoint_depth | [JSON](reports/normalized/viewpoint_depth.json) | [raw](reports/raw/viewpoint_depth.md) | [JSON](reports/parsed/viewpoint_depth.json) |
| edges_linework | [JSON](reports/normalized/edges_linework.json) | [raw](reports/raw/edges_linework.md) | [JSON](reports/parsed/edges_linework.json) |
| surface_finish | [JSON](reports/normalized/surface_finish.json) | [raw](reports/raw/surface_finish.md) | [JSON](reports/parsed/surface_finish.json) |
| rhythm_staging | [JSON](reports/normalized/rhythm_staging.json) | [raw](reports/raw/rhythm_staging.md) | [JSON](reports/parsed/rhythm_staging.json) |

## Enrichment history

- Lighting: [first full report](reports/history/lighting_shading/terminal_01.md), [parsed first report](reports/history/lighting_shading/terminal_01.json), [intermediate measurement request](reports/history/lighting_shading/terminal_02.md). Latest revision is in the source table.
- Color: [initial partial report](reports/history/color_palette/terminal_01.md), [parsed initial report](reports/history/color_palette/terminal_01.json), with the full four-summary revision in the source table.

## Evidence and checks

- **64 localized observations and 14 metric records** across nine roles. [Independent report checks](validation/parent_report_checks.json) confirm unchanged semantic fields for all nine normalized reports, canonical metadata, and unchanged image/raw-evidence hashes.
- [Mechanical collection audit](report_validation.json), [analysis-preservation hashes](validation/analysis_preservation.json), [immutable hashes](validation/immutable_hashes.json), [first-pass collection checks](validation/final_checks.json), and [synthesis checks](validation/synthesis_final_checks.json) retain stage-specific provenance. Earlier validation and its checksum ledger describe the pre-synthesis collection; they were not rewritten as final status.
- Input metadata repairs, including wrong/truncated hashes and a path typo, were audited without changing analysis. Value lists four inputs and edges five; neither was padded to seven. Shape retains its honest partial-analysis status. Symbolic metric references resolve to separate real files, not invented single-file evidence.
- Lighting O10/O11 boxes are approximate. Raw profile coordinates govern measurements. **LP2’s 16.32 px diagnostic span is not an accepted shadow width.** No accepted penumbra width or recovered physical lighting/camera is claimed.
- [Runtime observation](runtime_observations.json): actual PyWavelets module 1.8.0 versus distribution metadata 1.10.0 remains unresolved; reproduction is qualified. Neither version was edited.

Raw tool artifacts:
- [LP1_profile.json](raw_evidence/LP1_profile.json)
- [LP2_profile.json](raw_evidence/LP2_profile.json)
- [R1_whole_frame_summary.json](raw_evidence/R1_whole_frame_summary.json)
- [R2_whole_frame_summary.json](raw_evidence/R2_whole_frame_summary.json)
- [R3_whole_frame_summary.json](raw_evidence/R3_whole_frame_summary.json)
- [R4_whole_frame_summary.json](raw_evidence/R4_whole_frame_summary.json)
- [lighting_probe_statistics.json](raw_evidence/lighting_probe_statistics.json)

No new expert analysis, research, downloads, model execution, or image generation was performed during final assembly.
