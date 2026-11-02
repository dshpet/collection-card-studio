# `reference_art_analysis` — reusable workflow component

**First qualified pilot completed:** [analysis and generation brief](../runs/2026-11-01-reference-pilot-01/README.md), with nine fresh role sessions and a separate fresh synthesis session. These prompts remain reusable; each future run must fix and verify its own inputs. Existing larger files were used in this pilot, not newly downloaded; source nativeness remains qualified.

This is the reference-art component of the [whole workflow](../../WORKFLOW.md), not thematic planning or a generator. **Orchestration entrypoint: [RUN_PROTOCOL.md](RUN_PROTOCOL.md).** Use the existing native **observer** in nine fresh vision-capable aspect sessions, then one separate fresh synthesis session. These are project-local prompts, not globally registered agents, different model assignments, or an application framework. The same vision model may serve all sessions.

| Role prompt | Owns |
|---|---|
| [lighting_shading](lighting_shading.md) | Illumination cues, shadow/highlight appearance, shading construction. |
| [value_contrast](value_contrast.md) | Light–dark organization and regional contrast. |
| [color_palette](color_palette.md) | Role palettes and chromatic relationships. |
| [composition_hierarchy](composition_hierarchy.md) | Framing, placement, space, focal organization. |
| [shape_proportions](shape_proportions.md) | Silhouette, diagnostic parts, proportions. |
| [viewpoint_depth](viewpoint_depth.md) | Visible faces, projection/depth hypotheses. |
| [edges_linework](edges_linework.md) | Boundary treatment and explicit marks. |
| [surface_finish](surface_finish.md) | Texture, markmaking, material-like finish. |
| [rhythm_staging](rhythm_staging.md) | Repetition and legible spatial/action relationships; N/A allowed. |

[Synthesis prompt](synthesis.md) is used only after collection/validation of all nine aspects. [Shared contract](CONTRACT.md) defines coordinates, evidence, and aspect-report output. The synthesis is separate, not one agent changing hats through ten roles.

First passes receive only fixed images/manifest, their own prompt, the contract, and scoped toolbox excerpts. No prior conversation, other reports, research corpus, or judge conclusions. Finish all nine before writing their report artifacts; synthesis starts in another fresh session. If host context inheritance defeats this boundary, report the limitation rather than claim independence.

## Input and output contract

Inputs are a fixed manifest of actual image files (verified native/full-resolution when available, otherwise explicitly qualified), canonical paths/hashes/dimensions, crop/aperture/region scope, ICC/alpha/preprocessing and coordinate conventions, applicable art-guide revision, category coverage, and relevant tool routes. The orchestrator attaches provenance deterministically; specialists may use input IDs plus null hashes and the canonical manifest reference rather than retyping long hashes.

First passes are read-only and independent; explicit N/A or partial limits are valid. Do not invent evidence to fill a role. Tools are optional when useful: report actual execution, provided precomputed evidence, or not-run status honestly. No source-only learned model is implicitly enabled.

Use the existing per-run bundle, without a new schema or application layer:

```text
analysis/runs/<run_id>/
  inputs.json
  raw_evidence/
  reports/raw/       reports/parsed/       reports/normalized/
  session_index.json
  report_validation.json
  SYNTHESIS.md
  GENERATION_BRIEF.md
```

See the pilot's [manifest](../runs/2026-11-01-reference-pilot-01/inputs.json), [session index](../runs/2026-11-01-reference-pilot-01/session_index.json), [validation](../runs/2026-11-01-reference-pilot-01/report_validation.json), [art profile](../runs/2026-11-01-reference-pilot-01/SYNTHESIS.md), and [style guidance](../runs/2026-11-01-reference-pilot-01/GENERATION_BRIEF.md).

`SYNTHESIS.md` hands off evidence-backed constraints and exceptions. `GENERATION_BRIEF.md` hands off **reusable style guidance**, not an entire card-production prompt. The consumer joins it with theme/set planning, producer wishes, subject identity parts, category-specific requirements, and output constraints. Preserve citations and source qualifications; do not copy reference objects/palettes into every card or silently treat unassessed attributes as satisfied. No overall style-truth score is produced.

## Operating gates and reuse

**Ready:** fixed source/scope, all nine roles accounted for (explicit N/A/partial limits included), validated IDs/artifact references, completed synthesis, and visible uncertainties. Ready means the bundle is usable within scope, not demonstrated production quality.

**Qualified:** the same accounting and validation hold, but source quality, coverage, or assessment gaps limit use. Downstream briefs must explicitly carry and accept those limits. **Blocked:** missing required media, unavailable vision, unexplained wrong input/content, or required-role failure prevents the requested analysis; do not hide it behind a summary. These are stage-level gates, not retrospective edits to pilot report statuses.

Reuse a run for the same reference pack, art-guide revision, scope/category coverage, analysis-protocol revision, and preprocessing version. Record that run ID/manifests/revisions in the consuming brief; no cache engine is needed. Ordinary theme changes usually reuse the output. Uncovered categories, changed guide/source hashes/resolution/preprocessing/methods, or outcomes invalidating conclusions require a scoped refresh or new run version. Generated-card QA uses relevant brief axes, not all nine roles on every retry.
