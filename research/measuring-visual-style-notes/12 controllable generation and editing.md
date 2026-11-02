# Controllable generation, reference-style matching, and axis-targeted editing

Research cutoff: **2026-10-31**. Evidence labels: **Official** = documented interface; **Research** = authors’ reported method/results; **Proposal** = recommended experiment, not established universal practice. No generation, private-reference upload, model download, installation, or deployment test was performed.

## 1. What can be controlled independently, and with which mechanisms?

### Takeaway

There is no universal “style vector” whose coordinates correspond cleanly to lighting, palette, material, camera, and brushwork. Practical control comes from assigning each requested change to an appropriate mechanism—parameterized image processing, scene rendering, structural conditioning, reference conditioning, or generative editing—and explicitly testing collateral changes.

### Cited Findings

#### Separate the control vocabulary before selecting a generator

**Proposal:** use the following operational taxonomy. These categories describe user intent; they are not claims that a model internally disentangles them.

| Category | Examples | Important distinction |
|---|---|---|
| Content/identity | Object class, character identity, text, object count | Usually not “style”; reference conditioning can accidentally copy these |
| Scene/layout | Object arrangement, silhouette, occlusion, pose | Structural conditions help, but do not fix appearance |
| Camera/projection | Viewpoint, perspective, orthographic projection, crop, focal length | “Isometric-looking” prompting is not a calibrated camera |
| Geometry/material | Shape, bevels, surface roughness, transparency, metalness | Material appearance also depends on illumination and viewing angle |
| Illumination | Direction, source extent, key/fill balance, shadows | Not equivalent to brightness or color grading |
| Rendering/illustration style | Brushwork, line treatment, abstraction, shape language | Often entangled with palette, texture, and content |
| Tone/color/postprocess | Exposure, contrast, white balance, palette, saturation, grain, sharpening | Often best handled without regenerating the image |
| Output contract | Dimensions, alpha, color profile, file format, compression | Should normally be enforced by an exporter/validator, not prose alone |

Evidence supporting the separation: ControlNet exposes spatial conditions; InstantStyle specifically investigates reference-style/content leakage; current image APIs separately document output-format controls. None establishes that all the categories above are independently identifiable from one image. [ControlNet](https://github.com/lllyasviel/ControlNet), [InstantStyle](https://github.com/instantX-research/InstantStyle), [OpenAI image guide](https://developers.openai.com/api/docs/guides/image-generation).

#### Capability matrix: axis versus mechanism

The assessments below are engineering synthesis from the linked mechanisms, **not comparative benchmark results**.

| Target axis | Suitable controls | What can reasonably remain fixed | Limitations and cross-axis coupling |
|---|---|---|---|
| Exposure/contrast/white balance | Parameterized pixel editor; adjustment layers | Geometry, identity, object placement | Changes color relationships and clipping; cannot recover missing radiance |
| Palette/object recolor | Masked color transforms; material recolor in 3D; generative recoloring when needed | Raster geometry with non-generative transforms | Natural recoloring may require preserving shading/specular behavior; generative editing may redraw texture |
| Physical lighting direction/softness | Editable 3D lights; specialized relighting; image editor instruction | Exact scene geometry in an owned 3D scene | Shadows, highlights, reflections, and perceived material must change; preserving all tone is contradictory |
| Surface material | Shader parameters in 3D; local generative edit; reference conditioning | Camera and underlying mesh in 3D | Reflections, silhouette fuzz, shading, and color can change |
| Camera/viewpoint | 3D camera; depth/layout-conditioned reconstruction; instructed camera edit | Scene parameters when an actual scene exists | A single image does not contain unseen surfaces; generative camera changes hallucinate them |
| Layout/silhouette | Boxes, segmentation, edges, scribbles, depth; compositing | Some spatial relationships | Edges do not specify depth or material; depth does not specify appearance |
| Human pose | Pose/keypoint conditioning, possibly masks | Approximate skeletal configuration | Hands, garments, identity, and occlusion remain underconstrained |
| Brushwork/line/texture | Style reference, layer-selective adapter, LoRA, low-strength image-to-image | Approximate content/layout with additional conditions | High-frequency style can change boundaries; stronger conditioning may leak reference content |
| Character identity | Explicit identity reference or suitable adapter; localized editing | Approximate recognizable identity | Neither identity fidelity nor exact expression preservation follows automatically |
| Local object replacement | Inpainting, regional instructions/boxes, protected-region compositing | Untouched pixels **if copied explicitly** | Model masks alone are not necessarily exact; seams, shadows, and reflections may require a larger allowed region |
| Output size/alpha/encoding | Documented output options followed by deterministic export | File contract | Correct format does not establish correct depicted content or useful alpha boundaries |

Sources: spatial conditions and composability in [ControlNet](https://github.com/lllyasviel/ControlNet); style/layout adapter control in [Diffusers](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/ip_adapter.md); relighting in [IC-Light](https://github.com/lllyasviel/IC-Light); current regional editing in [BFL bounding-box documentation](https://docs.bfl.ml/flux_3/flux3_image_bounding_boxes.md); parameterized photo edits in [IEA](https://github.com/OpenDFM/Image_Edit_Agent).

#### Text prompts, negative prompts, and seeds

- **Official:** Diffusers image-to-image exposes `strength`, guidance, and negative prompts in supported pipelines. Strength controls how strongly the initial image is perturbed; it is not an axis-specific “style amount.” Changing guidance can also change the balance between image preservation and instruction following. [Diffusers image-to-image](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/img2img.md).
- **Official:** Diffusers documents `set_ip_adapter_scale(...)`, including per-layer style/layout configurations. This is more concrete than adding increasingly emphatic style adjectives, but the exact configuration is architecture-specific. [Diffusers IP-Adapter](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/ip_adapter.md).
- **Official:** identical seeds do **not** guarantee identical results across hardware/software configurations. Diffusers recommends CPU random generators when reproducibility matters, while explicitly retaining this qualification. [Diffusers reproducibility](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/reusing_seeds.md).
- **Inference:** a seed is an experimental nuisance-variable control, not an identity/layout lock. Negative prompts are conditioning, not logical exclusions. Unsupported negative-prompt fields must not be silently invented for hosted APIs.

#### Reference/style conditioning, adapters, and fine-tuning

- **Research:** IP-Adapter supplies image conditioning through a lightweight adapter alongside text conditioning; its repository describes a 22M-parameter adapter and combination with structural controls. A generic image reference can carry content as well as style. [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter).
- **Research:** InstantStyle reduces content leakage using feature subtraction and injection into selected attention blocks. Its SDXL observations associate different blocks with style and spatial layout; these are empirical findings for that architecture, not a universal decomposition of image style. [InstantStyle](https://github.com/instantX-research/InstantStyle).
- **Official:** LoRA trains a smaller added set of weights and is more memory/storage efficient than training all model weights. This does not make the learned adaptation content-independent or guarantee good results from a tiny, biased reference set. [Diffusers LoRA guide](https://github.com/huggingface/diffusers/blob/main/docs/source/en/training/lora.md).

**Proposal:** prefer training-free conditioning for a few references or rapidly changing art direction. Consider a style LoRA only after repeated tasks demonstrate that prompting/reference conditioning cannot achieve acceptable consistency. Require varied subjects and layouts in training examples, held-out subjects, and content-leakage evaluation. Full fine-tuning is an optional research-heavy escalation, not a prerequisite.

#### Attention control and real-image editing

- **Research, seminal older work:** Prompt-to-Prompt modifies cross-attention during generation, offering token replacement, refinement, and reweighting. Its actual controls include `cross_replace_steps`, `self_replace_steps`, and an attention equalizer. Null-text inversion extends this workflow toward real photographs by optimizing unconditional embeddings around an inversion trajectory. [Prompt-to-Prompt and Null-text inversion repository](https://github.com/google/prompt-to-prompt).
- **Inference:** these methods establish that internal attention interventions can improve edit locality/composition preservation. They do not imply that an arbitrary current hosted model exposes comparable internals, or that copying attention preserves every non-target attribute.

#### Relighting versus grading versus reconstruction

- **Research:** IC-Light provides foreground/text-conditioned and foreground/background-conditioned relighting. Its training imposes light-transport consistency; the repository discusses deriving normal-like information from multiple relightings. These are learned reconstructions, not ground-truth recovery of scene illumination or geometry. [IC-Light](https://github.com/lllyasviel/IC-Light).
- **Official/research implementation:** IEA instead controls 16 global retouching tools, including exposure, contrast, highlights, shadows, saturation, temperature, and sharpness. This is relevant prior art for an agent choosing interpretable edits rather than regenerating every image. [IEA](https://github.com/OpenDFM/Image_Edit_Agent).
- **Proposal:** distinguish “make it warmer” into at least: warmer white balance, warmer light source, warmer material color, or warmer illustration palette. These require different operations and different allowed side effects.

For an owned 3D scene, changing a light or camera while preserving mesh/material parameters provides substantially stronger **parameter-level** control than reconstructing a scene from a raster. Blender documents separate rendering passes for depth, normals, diffuse appearance, and light information. Full manual retrieval was blocked here; only the official indexed passage was inspected. [Blender passes](https://docs.blender.org/manual/en/latest/render/layers/passes.html).

### Inferences

#### Extracting references into actionable evidence

**Proposal:**

1. Assign each reference a role: **style**, **identity**, **layout**, **material**, or **lighting**. Permit multiple roles only explicitly.
2. Record observable properties, image region, confidence, and ambiguity—not only a global caption.
3. Separate observation from inferred cause: “soft-edged shadow” is observable; “large area light at 45°” is a hypothesis.
4. Use several references with different content to identify recurring stylistic properties.
5. Compile a short positive description, preservation instructions, and appropriate conditioning assets.
6. Ask for clarification when a reference’s distinctive appearance depends on content that should not transfer.

Example reference extraction:

> Rounded beveled forms; broad highlights; restrained microtexture; warm upper-left illumination; cool low-contrast shadows; clean silhouettes. Camera appears orthographic-like, but calibration is unknown.

Example axis-targeted instruction, **proposed wording, not a proven prompt**:

> Use Image 1 as the content and layout anchor. Use Image 2 only for surface treatment. Change the central object from glossy plastic to matte painted clay. Preserve its silhouette, position, camera framing, lettering, background, and light direction. Permit highlight width and local shading to change because they follow the material change. Do not introduce objects from Image 2.

This is more testable than “make it match the style perfectly.”

#### Guarantees must be typed

**Proposal:** distinguish:

- **Hard output guarantee:** exporter checks dimensions/encoding.
- **Hard protected-pixel guarantee:** explicit copy/composite outside an authorized region, before lossy encoding.
- **Scene-parameter guarantee:** scene graph fixes camera/mesh/material parameters not selected for editing.
- **Soft perceptual constraint:** generator is instructed to preserve identity/layout/style.

For a same-size raster composite,
`output = (1 − mask) × original + mask × generated`
preserves original pixel values where the mask is exactly zero, provided subsequent processing does not modify them. This mathematical property belongs to the compositor—not to the generative model. Feathered boundaries and physically necessary shadow/reflection regions must be included in the declared edit scope.

### Gaps

- No universal decomposition or independent-axis guarantee was established.
- No benchmark in this task measured actual coupling, reference leakage, or preservation quality.
- Single-image lighting, camera, and material inference remains ambiguous.
- Blender rendering and AMD deployment were not tested.

## 2. Which representative current systems expose meaningful controls?

### Takeaway

The live 2026 documentation materially updates comparisons based only on 2025 systems: OpenAI documents GPT Image 2.5, Google lists Nano Banana 2.1, and BFL documents FLUX 3 Image and Klein. Treat documented request fields as evidence of interface availability—not independent proof of fidelity, invariance, local feasibility, or commercial suitability.

### Cited Findings

#### Current capability and availability comparison

| Option | Verified useful controls | Availability/licensing evidence | Main qualifications |
|---|---|---|---|
| **OpenAI GPT Image 2.5 Sunburst / Flare** | Text/image editing, multiple references, masks, conversational iteration, size/quality/format/transparency options | Current official API guide names both models | Hosted/proprietary; masks are guidance; consistency/layout limitations remain |
| **Google Nano Banana 2.1 / Gemini 3 Pro Image** | Text/image editing, multi-reference input, conversational iteration, aspect ratio/resolution controls | Current Google guide lists model IDs and differences | Hosted/proprietary; do not assume Lite has the same sequential-edit capability |
| **BFL FLUX 3 Image** | Up to ten references; box-based layout/edit descriptions; exact-size options; grounding toggle | Official release notes: Image Oct 1, size/edit updates Oct 22, 2026 | Main endpoint does not expose a seed in inspected schema; “pixel-exact” is vendor language, untested here |
| **BFL FLUX 3 Image Klein** | Similar editing/layout interfaces; API seed/steps; open-weight Base and Distilled variants | Official release: Oct 15, 2026; docs name FLUX Kommunity License | License text could not be inspected; local prompt upsampler adds substantial memory |
| **FLUX.2 Klein 4B / 9B** | Text-to-image and single-/multi-reference editing; Base versus distilled variants | Official repository: Jan 15, 2026; 4B Apache-2.0, 9B non-commercial | Repository’s consumer-GPU examples are NVIDIA, not proof of ROCm compatibility |
| **Qwen-Image-Edit-2511** | Instruction editing, multi-image input; documented generator/guidance controls | Open model card declares Apache-2.0; weights released Dec 23, 2025 | Model improvements are author claims, not invariant guarantees |
| **SDXL + ControlNet + IP-Adapter/InstantStyle** | Exposed structural maps, masks, image-to-image strength, per-layer reference strength | Public code/docs; mature older control ecosystem | Component/base-model licenses differ; older backbone is not necessarily best visual quality |
| **IC-Light** | Specialized learned relighting from foreground plus text/background | Public repository | Not a general style editor; reconstruction may alter details |
| **Parameterized editor / 3D renderer** | Explicit tone/color operators or scene parameters | IEA demonstrates agent-controlled photo tools; Blender exposes scene/pass controls | Stronger control within its domain, not a replacement for missing geometry or arbitrary synthesis |

Sources: [OpenAI](https://developers.openai.com/api/docs/guides/image-generation), [Google](https://ai.google.dev/gemini-api/docs/image-generation), [BFL release notes](https://docs.bfl.ml/release-notes), [FLUX 3 Klein](https://docs.bfl.ml/flux_3/flux3_image_klein), [FLUX.2 repository](https://github.com/black-forest-labs/flux2), [Qwen model card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), [Diffusers adapter controls](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/ip_adapter.md), [IC-Light](https://github.com/lllyasviel/IC-Light), [IEA](https://github.com/OpenDFM/Image_Edit_Agent).

#### Verified syntax and model-specific traps

**OpenAI — Official**

The current guide uses:

```text
model: "gpt-image-2.5-sunburst"
model: "gpt-image-2.5-flare"
```

The Responses image tool supports `action: "auto"`, `"generate"`, or `"edit"`. Transparent output uses `background: "transparent"` with PNG or WebP. The guide explicitly states:

> “The model uses the mask as guidance, but may not follow its exact shape with complete precision.”

The `input_fidelity` discussion inspected concerns older `gpt-image-2`: it says to omit that parameter because fidelity is automatically high. **Do not carry older-model `input_fidelity` recipes into 2.5 without checking the specific request schema.** [OpenAI image guide](https://developers.openai.com/api/docs/guides/image-generation).

**Google — Official**

The current guide names `gemini-nano-banana-2.1`, `gemini-3-pro-image`, and other variants. Its Interactions examples use `previous_interaction_id` for continued editing and:

```json
{
  "response_format": {
    "type": "image",
    "mime_type": "image/png",
    "aspect_ratio": "16:9",
    "image_size": "2K"
  }
}
```

These are **Google-specific documented fields**, not a universal schema. The guide documents up to 14 reference images with model-specific role limits; Pro explicitly includes style-reference support. It also says Flash Lite is not optimized for multiple-reference or sequential editing. Generated images carry SynthID. [Google image guide](https://ai.google.dev/gemini-api/docs/image-generation).

**BFL FLUX 3 — Official**

The inspected live OpenAPI defines `prompt`, `images`, `aspect_ratio`, `resolution`, `width`, `height`, and `grounding` for `/v1/flux-3-image`. It sets `additionalProperties: false`; no `seed`, generic `style_strength`, mask, or negative-prompt field appeared in that request schema.

Klein’s separate request schema does expose `seed`, `steps`, and `output_format`. It does **not** share every field of the larger model; for example, Klein lacks `match_input`. [BFL live OpenAPI](https://api.bfl.ai/openapi.json).

Bounding boxes are appended as JSON **inside the prompt**, not supplied through an invented top-level `boxes` argument. Coordinates are `[top, left, bottom, right]`, integers on a 0–1000 grid. Editing rows use `id`, `from`, `src_bbox`, `tgt_bbox`, and `desc`; the first reference is `ref_image_0`. [BFL bounding-box tutorial](https://docs.bfl.ml/flux_3/flux3_image_bounding_boxes).

The tutorial and release notes use absolute preservation language, including “pixel-exact local edits.” **That is a vendor claim**, not a guarantee independently validated in this research. Equal output dimensions also do not prove equal protected pixels. [BFL release notes](https://docs.bfl.ml/release-notes).

**Qwen — Official**

The 2511 model card documents `QwenImageEditPlusPipeline`, `image`, `prompt`, `generator`, `true_cfg_scale`, `negative_prompt`, `num_inference_steps`, and `guidance_scale`. Do not equate `true_cfg_scale` with every other pipeline’s guidance parameter. [Qwen model card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511).

The current repository also announces **Qwen-Image-2.0 on February 10, 2026**. That announcement does not establish that its weights, license, or controls match Edit-2511; those were not verified here. [Qwen repository](https://github.com/QwenLM/Qwen-Image).

#### Privacy, licensing, cost, and workstation constraints

- **Official:** OpenAI API inputs are not used for training by default, but default abuse-monitoring retention can be up to 30 days, with exceptions and separately approved retention controls. “Not used for training” is not “never retained.” [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data).
- **Official:** Google distinguishes paid and unpaid services; unpaid-service terms generally allow improvement use and human review, with regional/account qualifications. Its terms warn against sending sensitive/confidential/personal information to unpaid services. [Google API terms](https://ai.google.dev/gemini-api/terms).
- **Official:** FLUX.2 **4B** Apache-2.0 must not be generalized to its **9B** or dev models, which the repository lists under non-commercial terms. Code license and weight license are separate checks. [FLUX.2 repository](https://github.com/black-forest-labs/flux2).
- **Official:** FLUX 3 Klein docs identify a **FLUX Kommunity License**. The linked model-card raw endpoint returned 401; no login or bypass was attempted. Commercial eligibility remains **unverified**, not Apache-2.0 by assumption. [Klein documentation](https://docs.bfl.ml/flux_3/flux3_image_klein).
- **Official:** Klein docs say its separate prompt upsampler adds about **28 GB GPU memory**. Consequently, “small generator fits a consumer GPU” does not establish that the complete recommended workflow fits the user’s 24 GB card. Sequential/offloaded operation was not tested. [Klein documentation](https://docs.bfl.ml/flux_3/flux3_image_klein).
- **Official:** AMD’s current compatibility matrix lists RX 7900 XTX/gfx1100. That is not proof that a specific model, attention backend, quantizer, or trainer works on CachyOS. The inspected matrix did not list CachyOS or Arch Linux. [AMD compatibility matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html).
- **Official:** FLUX.2’s reference implementation reports testing on GB200/CUDA. Its NVIDIA memory/performance examples cannot be reused as ROCm deployment claims. [FLUX.2 repository](https://github.com/black-forest-labs/flux2).

**Proposal:** private references stay local by default. Cloud adapters should require explicit per-task permission, naming the provider and reference assets. Local model use also requires checking optional remote encoders, prompt rewriting, telemetry, and downloaded workflow dependencies.

**Cost limitation:** no numerical price comparison is claimed. BFL’s retrieved pricing tables omitted rendered amounts. Budget against live quotes, resolution, image inputs, retries, and evaluator calls; local runs have engineering/time/energy costs. [BFL pricing](https://docs.bfl.ml/quick_start/pricing).

### Inferences

- Currentness is not a reason to discard older controllable pipelines: they may expose more inspectable controls than a newer hosted black box.
- Conversely, exposing many parameters does not establish better editing quality.
- A meaningful comparison should use the same reference roles, target axes, preservation rubric, and total attempt budget—not isolated vendor examples.

### Gaps

No account-specific availability, prices, FLUX 3 license eligibility, AMD end-to-end compatibility, or comparative output quality was verified.

## 3. What agent loop and backend-neutral specification are justified?

### Takeaway

Iterative visual critique and tool-mediated editing are established prior art. The proposed contribution should therefore be a transparent, constraint-aware control workflow—not merely “an agent generates, evaluates, and retries.” Experimental Jacobians and coordinate descent are plausible calibration strategies, but remain hypotheses for this application.

### Cited Findings

#### Existing loop prior art

- **Research, 2023/2024:** Idea2Img iterates prompt generation/revision, draft generation, selection, and visual feedback while retaining observations about the generator. This directly precedes generic agentic prompt-refinement proposals. [Idea2Img paper](https://arxiv.org/html/2310.08541v2).
- **Research, 2025:** RefineEdit-Agent describes instruction parsing, scene understanding, hierarchical planning, tool selection, and LVLM feedback in a closed loop. Its reported benchmark gains are authors’ results, not independent validation here. [RefineEdit-Agent](https://arxiv.org/abs/2508.17435).
- **Research, CVPR Findings 2026:** MIRA generates atomic edits through perception–reasoning–action with visual feedback. It uses a 150K tool-use dataset and SFT + GRPO training. This is not evidence that an untrained orchestration prompt automatically reproduces its results. [MIRA proceedings](https://openaccess.thecvf.com/content/CVPR2026F/html/Zeng_MIRA_Multimodal_Iterative_Reasoning_Agent_for_Image_Editing_CVPRF_2026_paper.html).
- **Research/current project:** IEA offers explicit global-retouching tool traces, demonstrating an alternative to generative reconstruction. [IEA](https://github.com/OpenDFM/Image_Edit_Agent).
- **Research, CVPR 2026 project:** JarvisEvo combines professional editing tools, generative editing, and visual feedback. Its repository lists inference/checkpoints and SFT code as released, but SEPO/RFT training code as unreleased. It declares a non-commercial license. [JarvisEvo](https://github.com/LYL1015/JarvisEvo).

### Inferences

#### Backend-neutral declarative spec — proposal, not an existing standard

```yaml
spec_version: proposal-0
references:
  - id: content_anchor
    role: content_layout
    asset: LOCAL_REFERENCE_ID
    cloud_allowed: false
  - id: style_reference
    role: surface_style
    asset: LOCAL_STYLE_REFERENCE_ID
    cloud_allowed: false

target:
  axis: material
  region: central_object
  desired: matte painted clay
  evidence:
    reference: style_reference
    confidence: medium

preserve:
  - identity
  - silhouette
  - camera
  - layout
  - lettering
  - background
  - light_direction

allowed_consequences:
  - local_highlight_shape
  - local_shading

output:
  width: 1024
  height: 1024
  format: png
  alpha: required

acceptance:
  target_improves: required
  protected_axes: no_material_regression
  protected_pixels: only_if_composited

budget:
  max_candidates: 8
  max_edit_rounds: 3
  cloud_spend_cap: unset
```

The fields are **internal proposal fields**, not valid vendor API parameters.

**Compiler proposal:**

1. Validate contradictions and missing permissions.
2. Resolve references by role; retain observed evidence and uncertainty.
3. Match intent to capabilities:
   - tone → parameterized editor;
   - exact camera/light control with available scene → renderer;
   - local semantic change → regional edit/inpainting;
   - structural preservation → compatible edge/depth/pose/layout conditioning;
   - style treatment → reference adapter or documented image editor.
4. Emit only backend-supported controls.
5. Report unsupported requirements instead of silently weakening them.
6. Save the effective prompt, model/version, rewrite/upsampler output, masks/maps, seed where supported, settings, lineage, cost, and evaluations.
7. Validate the output contract separately.

Evidence status: reference roles and compilation structure are **proposed engineering design**; individual control mechanisms are documented above. No evidence establishes a lossless universal compiler between these backends.

#### Agent evaluation contract

**Proposal:** evaluate each candidate against **the original anchor and reference**, not only its immediate predecessor.

Return:

- target-axis result;
- preservation result for every protected axis;
- authorized versus unauthorized changes;
- visible evidence and uncertainty;
- artifact/seam/text/alpha failures;
- recommendation: accept, revert, retry narrowly, switch tool, or ask a human.

Do not collapse these immediately into one aesthetic score. A more attractive image can still be a failed controlled edit. Keep a human-calibrated review set; agent critics can share generator biases or reward changes outside the task.

This note intentionally does not specify pixel-metric implementations.

#### Same-seed finite differences / experimental Jacobian

**Hypothesis:** estimate local control responses before expensive search.

Let \(y=f(x,u,s)\) be the output and \(m(y)\) an externally supplied vector of axis assessments. For a numeric control:

\[
J_{ij}\approx
\frac{m_i(f(x,u+\delta e_j,s))-m_i(f(x,u-\delta e_j,s))}
{2\delta}.
\]

Interpret diagonal responses as desired influence and off-diagonal responses as coupling.

Conditions and limitations:

- Recreate/reset RNG state for paired runs; reusing an advanced generator object does not preserve initial noise.
- Freeze model, scheduler, dimensions, preprocessing, effective rewritten prompt, and software environment.
- Measure repeated-request variability first.
- Repeat promising findings across several seeds and representative images.
- Treat natural-language edits as discrete interventions, not genuinely differentiable numeric coordinates.
- A hosted endpoint without seed/version pinning cannot support the same experiment identically.
- A local response estimate need not generalize across scenes, strengths, or model updates.

Same-seed pairing is motivated by reproducibility controls, but the proposed Jacobian workflow is **not established here as a universally effective image-editing recipe**. [Diffusers reproducibility](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/reusing_seeds.md).

#### Coordinate descent and masked editing

**Hypothesis:** edit one prioritized axis at a time, accept only improvements satisfying preservation checks, and branch from the best accepted state.

- Use deterministic edits before generative ones when they satisfy the intent.
- Keep the original anchor available to reduce cumulative drift.
- Regression-check all protected axes after every accepted edit.
- Permit necessary coupled effects explicitly.
- Revert failed candidates.
- Switch mechanisms when the task exceeds the current mechanism—for example grading cannot create physically correct new cast shadows.

Coordinate descent can fail when objectives conflict or controls are strongly coupled. A material/lighting change may require a joint step rather than alternating corrections indefinitely.

#### Bounded retries, stop rules, escalation

**Proposal; illustrative limits, not authorized spending:**

- Initial calibration: a few small candidates, not an unrestricted sweep.
- Cap total candidates, elapsed time, edit rounds, and external spend.
- Stop when the target is met and preservation checks pass.
- Stop a strategy after two successive rounds without credible improvement.
- Escalate if identical inputs show instability larger than the desired effect.
- Escalate after repeated protected-axis failures: tighter mask, stronger structure control, compositor, 3D proxy, different backend, then human clarification.
- Stop immediately on exhausted budget, unavailable permissions, unsupported hard constraints, or unusable outputs.
- Do not resubmit an asynchronous job merely because polling is slow.
- Preserve the best accepted candidate and failure trace; returning “unmet” is preferable to claiming convergence.

#### Minimal feasible pipeline versus research extensions

**Minimal research prototype:**

1. Human-approved taxonomy and reference-role extraction.
2. One generator/editor adapter with a documented capability manifest.
3. One parameterized tone/color editor.
4. Masks plus optional protected-region compositing.
5. Structured per-axis critique and human spot checks.
6. Small bounded search, rollback, provenance, and output validation.

**Optional, evidence-driven extensions:**

- ControlNet edge/depth/normal/pose maps.
- 3D proxy scene for camera/lighting/material experiments.
- Layer-selective style conditioning.
- Local response/Jacobian calibration.
- Style LoRA with held-out content tests.
- Attention intervention/inversion research.
- Trained planning/evaluation agents or reinforcement learning.

None should be adopted merely because a paper demonstrates it. Add each only after a measured failure of the simpler workflow.

### Gaps

- No production stack was selected.
- No proposed specification/compiler/optimizer was implemented or validated.
- Literature establishes substantial loop prior art, not this exact combination’s effectiveness or novelty.
- Paper-specific benchmarks do not establish reference-style matching quality for the user’s assets.

**Evidence checks and spend:** approximately 18 Kagi discovery queries; Context7 library resolution plus two documentation queries; three GitHub code searches; direct inspection of 30+ public primary documentation/repository/paper pages. Roughly 20 core source families support the note, with ancillary privacy/licensing/hardware references. No Perplexity, Kagi Assistant, paid generation, private uploads, installations, or model downloads. Several access/rendering gaps are recorded above.
