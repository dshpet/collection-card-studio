# Shared first-pass report contract

## Isolation and permitted work

One role means one fresh vision-agent session. Receive original image paths **as absolute paths**, a fixed input manifest, this contract, your own role prompt, and relevant local vocabulary/tool/recipe excerpts. Do not inspect prior conversation, other role files/reports, synthesis conclusions, research notes, or unrelated directories. Do not follow document links into the research corpus. Use actual local image files, not secret/signed-URL metadata. Read images only when your available tools actually support it; otherwise report unavailable visual access.

First pass is read-only: no child file writes, image modification, uploads, installs, downloads, model loading, or agent delegation. Return your complete response to the orchestrator. Classical libraries are installed; BiRefNet, DAV2, and Marigold remain source-only, not enabled estimators. Tool availability is session-specific. Request unavailable measurements from the orchestrator, stating image, region, recipe, and question; never pretend a request was executed. Semantic reading without numbers is valid.

## Shared coordinates and provenance

The finalized manifest records input ID, absolute path, SHA-256, native pixel dimensions, EXIF orientation/analysis dimensions, resolution status, crop/aperture, ICC handling, and explicit alpha backdrop where needed. Missing metadata remains missing, not guessed. Every observation names its image ID and normalized bbox `[x0,y0,x1,y1]`: origin top-left, x-right, y-down, bounds 0…1 in the declared EXIF-transposed native analysis frame. Whole-frame observations use `[0,0,1,1]`. Add a crop/artifact reference only if one actually exists; no silent resampling or new crop writes.

The orchestrator computes and attaches canonical hashes, paths, and metadata; specialists need not manually retype 64-character hashes. Return declared input IDs with null hashes and a canonical manifest reference when appropriate. Validation may repair metadata typos from that manifest with a before/after audit, preserving raw responses and all analytic content. Unknown image IDs or content mismatches block reconciliation; typos alone do not establish that the correct image was viewed. Retain available image-read path evidence and its limitations.

Distinguish normalized extents from CLI native-pixel coordinates and exclusive integer bbox maxima. Declare angle units, frame, and sign; `atan2(-dy,dx)` is an image-plane convention, not a recovered 3D azimuth. Measurements must share image/backdrop/region conventions; masks need their own provenance. Do not equate alpha with subject extent.

For measurements, numerical profile coordinates and linewidth in raw tool artifacts take precedence over approximate visual boxes. Mark such boxes approximate; do not treat them as measured apertures.

## Evidence and claims

Use **D** for calculated observable evidence with declared preprocessing; **C** for measurement conditional on reviewed regions/landmarks; **L** for actual learned estimates; **H** for visual/perceptual interpretation. Repeatable neural output remains L. Looking at an image does not turn a semantic judgment into D. Keep **N/not identifiable** in the hypothesis/limits record for hidden causes. No light counts, physical roughness, exposure, or kelvin from image averages.

Separate concise observations from hypotheses. Each hypothesis cites observation IDs, states confidence with reasons, and retains plausible alternatives. Use high/moderate/low or unknown, never fabricated confidence percentages. Coarse references cannot establish fine-finish traits. Distinguish N/A, insufficient resolution, missing region evidence, and unavailable tools. A role may flag an adjacent question, but must not supply the other role's answer.

## Minimal response template

Return one structured report; this JSON is a **template**, not observed data. Replace placeholders and retain empty lists/nulls honestly. Explanatory prose is allowed after it if linked by IDs.

Use report status complete/partial/unavailable and applicability applicable/not_applicable/uncertain. Observation IDs are unique within a role; synthesis identifies evidence by run, role, input, and observation together.

```json
{
  "role": "ROLE_ID",
  "run_id": "RUN_ID",
  "input_manifest": "ABSOLUTE_CANONICAL_MANIFEST_PATH_REQUIRED",
  "input_manifest_sha256": null,
  "status": "partial",
  "applicability": "uncertain",
  "inputs": [{"id": "INPUT_ID", "file": "ABSOLUTE_PATH_REQUIRED", "sha256": null,
              "native_size_px": null, "resolution_status": "unverified"}],
  "observations": [{"id": "O1", "image_id": "INPUT_ID", "normalized_bbox": null,
                    "crop_ref": null, "kind": "H", "art_labels": [], "description": "FILL_FROM_EVIDENCE"}],
  "metrics": [{"tool": null, "version": null, "settings": {}, "region": null,
               "unit": null, "value": null, "artifact_ref": null, "run_status": "not_run"}],
  "hypotheses": [],
  "not_assessable": [],
  "generation_language_hints": [],
  "cross_domain_questions": [],
  "tools_actually_used": []
}
```

For each metric, record actual settings, region source, units, version, run status, and raw artifact reference. Never report suggested numbers as results. Hypotheses contain claim, supporting observations, confidence/reason, and alternatives. Missing-information entries explain what would resolve them. Hints contain plain-language intent, supporting observations, protected properties, and permitted consequences—not guaranteed backend parameters. Cross-domain questions name the receiving role and motivating observations. Role/input IDs must match the fixed manifest; supplied non-null hashes must match it, while nulls explicitly defer to canonical metadata. Flag discrepancies.
