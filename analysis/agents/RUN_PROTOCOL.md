# Run protocol: fixed inputs, nine independent passes, separate synthesis

This is the single orchestration entrypoint for **`reference_art_analysis`** within the [whole workflow](../../WORKFLOW.md). Use the [module contract, gates, and reuse rules](README.md) before starting: reuse a suitable validated run or execute the bounded steps below. Do not substitute generic one-agent analysis when creating a new art-style brief.

**Completed example:** [qualified reference pilot 01](../runs/2026-11-01-reference-pilot-01/README.md). Nine fresh native observer sessions covered the nine roles; another fresh session performed synthesis. This reusable protocol does not register nine global agents or require nine model types.

## Prepare once

The orchestrator first verifies whether native originals are actually available. Do not infer recovery success from filenames or a parallel writer's activity, and do not alter that writer's files. If unavailable, explicitly choose a coarse pilot; retain resolution-related abstentions. Distinguish unanalyzed local files from unretrieved files: broader coverage can use an existing verified local pack without waiting for new acquisition.

Select a small representative pack spanning the art guide's object categories, plus **one complete ten-card set if available**. Confirm membership/completeness rather than manufacturing it. Avoid sending all 160 cards to every agent by default. Keep the same fixed pack for all roles; record any justified role-specific access limit. A contact sheet cannot silently replace individual originals.

Record hashes and basic metadata without resampling: original dimensions, EXIF orientation, analysis dimensions, ICC status, explicit alpha/background treatment, category/set provenance, and reviewed region/crop coordinates. The existing CLI supplies descriptive evidence, not automatic subject masks or lighting labels. Prepare only relevant shared evidence; keep interpretive conclusions out of the input packet.

Fix the applicable [art guide](../../materials/03_art_guide.md) revision and intended category coverage, plus protocol/preprocessing revisions, in the handoff alongside the manifest and run ID. Apply the module's ready/qualified/blocked gate to the requested scope; this is not a production-quality guarantee.

The orchestrator computes canonical paths/hashes/metadata; do not ask specialists to reproduce long hashes manually. Input IDs plus null hashes and a canonical manifest reference are valid. Audit metadata repairs without changing raw or analytic content. Unknown IDs or image-content mismatches block normalization; retain read-path evidence, which alone cannot prove correct visual access. Raw profile coordinates/linewidth govern measurements; label approximate visual boxes accordingly.

This **input-manifest template** deliberately has relative placeholder paths and no invented hashes. Before dispatch, resolve paths against the project root, verify assets, fill metadata, and freeze a uniquely identified manifest. Children receive finalized absolute paths, never this unfilled template.

```json
{
  "template": true,
  "run_id": "TEMPLATE_RUN",
  "coordinate_frame": "EXIF-transposed native pixels; x-right/y-down",
  "preprocessing": {"resampling": "none", "icc_handling": null, "alpha_backdrop": null},
  "images": [{"id": "TEMPLATE_CARD", "path": "PLACEHOLDER_RELATIVE/card.png",
              "sha256": null, "native_size_px": null, "analysis_size_px": null,
              "resolution_status": "unverified", "category": null, "set_id": null}],
  "regions": [],
  "raw_evidence": []
}
```

## Dispatch through available native tools

Use nine independent calls to the currently available native observer tool, not a custom Python launcher or global agent registration. The supplied native call shape is:

```text
functions.subagent(
  agent="observer",
  description="Independent lighting_shading first pass",
  prompt="Read /home/dshpet/Dev_Projects/playrix_testtask/analysis/agents/lighting_shading.md and /home/dshpet/Dev_Projects/playrix_testtask/analysis/agents/CONTRACT.md. Use only the finalized manifest and absolute original-image paths attached below. Relevant recipe: /home/dshpet/Dev_Projects/playrix_testtask/analysis/LIGHTING.md. [Attach finalized manifest, absolute image paths, and scoped toolbox excerpts here.]"
)
```

This documents the orchestrator's native tool call, not executable application code. Replace the attachment instruction before calling. Repeat with each of the nine indexed role prompts and relevant recipe paths. If the caller lacks that tool or a vision-capable observer, report a capability blocker; do not invent an endpoint. Confirm fresh-session semantics and no inherited conversation; if the host cannot provide them, do not label the result isolated.

Launch the nine calls in parallel when supported. Keep returned session IDs paired with roles and input-manifest identity. Await native completion hooks/notifications; do not poll, resume old research sessions, or reuse one session while changing hats. A child's missing tool request goes to the orchestrator; return actual raw evidence or an explicit unavailable status, never another role's conclusion.

## Collect before synthesis

Wait for all nine first-pass responses, including explicit partial/unavailable/N/A outcomes. Do not inject earlier conclusions into later lanes. Only then collect full terminal responses into report artifacts, preserving provenance and completeness. Keep shared raw measurement artifacts separate from interpretive reports so first-pass filesystem access cannot reveal another report. Record any unavoidable exposure.

Before synthesis, validate all nine reports against the manifest: known input/observation IDs, dimensions, bbox bounds (zero-width lines allowed), and real artifact paths. Preserve full raw responses and parsed values. Audit metadata-only normalized copies without altering observations, hypotheses, numbers, or hints; unknown IDs or unexplained content mismatches block, not autocorrect. Own-role enrichment with raw measurements is allowed and logged without peer reports. Save session/message provenance, original/enriched responses, and validation warnings in the module's existing run bundle. Source/measurement gaps must survive synthesis.

## Separate fresh synthesis prompt

Start another fresh vision-capable observer session with **[synthesis.md](synthesis.md)**, full absolute media paths, finalized canonical manifest, applicable art guide/scope, all nine validated reports, raw metrics, and validation qualifications—not earlier chat. Use the same native call shape above, with description `Fresh reference_art_analysis synthesis` and prompt path `/home/dshpet/Dev_Projects/playrix_testtask/analysis/agents/synthesis.md`; attach that complete packet. This is nine aspect sessions **plus one synthesis**, not a new globally registered agent.

The child remains read-only and returns two Markdown sections. The orchestrator preserves the full response and writes `SYNTHESIS.md` and `GENERATION_BRIEF.md` in the run folder, checks citations/links, and passes the bundle's stage gate. Hand off the run ID, revisions, profile/constraints, reusable style guidance, and unresolved limits to whole-workflow card-brief compilation; do not treat style guidance as a complete production prompt.

For a concrete unresolved conflict, request only a bounded targeted second pass from the relevant role in another fresh session. Supply original inputs, the specific conflict, and relevant evidence; label it adjudication rather than independent first-pass evidence. Retain original responses and exposure history. No oracle/council default.

The orchestrator owns completeness, contract/provenance checks, unresolved-item handling, and final handoff. This pack defines no model selection, host configuration, software framework, or actual image conclusions.
