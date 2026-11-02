# Style fingerprints, cross-axis validity, statistical calibration, and acceptance design

**Critical findings:** deterministic descriptors are feasible, definitive style truth is not; CSD’s official repository currently warns of released-weight discrepancies; October 2026 ASTRA is directly relevant but not validated for collectible-card acceptance. No installs, weights, image uploads, or repository execution performed.

Research cutoff: **2026-10-31**.

Scope: integrative measurement validity and evaluation design—not individual image-axis extraction tools or image-generation techniques.

Evidence labels:
- **Published finding:** attributed result within the source’s evaluated setting.
- **Proposed recipe/inference:** recommended project design, not a published validated collectible-card evaluation system.
- **Gap:** unverified applicability, implementation, licensing, or statistical assumption.

## 1. What can a reference-style fingerprint validly claim?

### Takeaway

Build a **versioned, region- and category-conditioned measurement profile with uncertainty**, not a definitive numerical reconstruction of “the style.” A reproducible number answers a precisely defined computational question; it does not automatically identify an underlying artistic, semantic, or physical cause.

### Cited Findings

#### Terminology: formal analysis is not synonymous with interpretation-free measurement

Getty describes formal analysis as identifying elements and design principles and evaluating their compositional roles. Duke’s university writing guide explicitly says visual analysis can include interpretation and “does not simply record your observations”—it makes a claim about the work. Terminology varies between assignments and traditions; therefore, “formal analysis cannot include interpretation” is too categorical. **Confidence: high.** — [Getty: Understanding Formal Analysis](https://www.getty.edu/education/teachers/classroom_resources/formal_analysis.html); [Duke: Visual Analysis](https://wrp.duke.edu/sites/twp.duke.edu/files/file-attachments/visual-analysis.original.pdf)

Useful project terminology:

- **Formal/visual analysis:** structured discussion of visible organization, potentially including interpretation.
- **Quantitative image description:** explicitly defined measurements of image data.
- **Operationalized style profile:** selected descriptors used as proxies for a declared notion of style.
- **Acceptance specification:** a normative decision about which deviations the art direction permits.

The last two are proposed distinctions for this project, not claims that art history supplies a universal numerical taxonomy.

#### Style definitions already embed judgments and labeling choices

CSD defines style through characteristics associated with artists or movements, including color, brushwork, composition, and perspective. Its training labels are derived from artist, medium, and movement tags rather than direct physical measurement of an independently observable “true style.” ALADIN uses weak supervision from online fine-grained style groupings. **Confidence: high.** — [CSD, ECCV 2024](https://arxiv.org/html/2404.01292v1); [ALADIN, ICCV 2021](https://arxiv.org/abs/2103.09776)

The October 2026 ASTRA preprint explicitly frames style-transfer ground truth as ill-defined: several outputs may be perceptually valid, and some content–style combinations may not admit an obvious ideal result. Its “ground truth” consists of rankings derived from a specified human-comparison protocol—not a uniquely correct image. **Confidence: high concerning what the paper claims; transfer to this project unvalidated.** — [ASTRA, 2026-10-07](https://arxiv.org/html/2610.10003v1)

#### Identifiability is different from repeatability

Inverse rendering has inherent ambiguity because geometry, materials, and lighting are coupled. IntrinsicAnything addresses this with learned priors, including when posed images are available. Such priors regularize a solution; they do not make arbitrary image formation uniquely invertible. **Confidence: high.** — [IntrinsicAnything, ECCV 2024](https://arxiv.org/abs/2404.11593)

Consequently, a bright painted rim is evidence of a bright image boundary—not definitive evidence of one light source, a particular roughness, a specific material, or a renderer’s lighting parameter. Stylized art may additionally depart deliberately from physically consistent rendering. This is an inference from the inverse-rendering limitation, not a measured finding about the supplied card references.

#### Preprocessing is part of the measurement

ICC profiles describe transformations between device-dependent and device-independent color spaces. Comparing color numbers without recording their interpretation can compare incompatible quantities. **Confidence: high.** — [ICC: Introduction to the ICC profile format](https://www.color.org/iccprofile.xalter)

Clean-FID demonstrates substantial evaluation changes caused by resizing implementations and image compression, including changes between images that appear perceptually very similar. SSIM’s authors likewise emphasize the dependence of appropriate analysis scale on resolution and viewing distance. **Confidence: high.** — [Clean-FID, CVPR 2022](https://github.com/GaParmar/clean-fid); [SSIM official project](https://ece.uwaterloo.ca/~z70wang/research/ssim/)

### Inferences

#### Proposed validity model

For every descriptor, distinguish:

1. **Repeatability:** same bytes, masks, implementation, and settings produce the same or numerically equivalent result.
2. **Reproducibility:** another supported environment reproduces the result within declared tolerance.
3. **Construct validity:** the descriptor actually tracks the intended aspect of style.
4. **Discriminant validity:** it does not primarily track an unwanted factor, such as subject identity.
5. **Decision validity:** a threshold predicts the project’s acceptance decisions at an acceptable error rate.
6. **Identifiability:** the observation uniquely determines the inferred property.

Passing the first two does not establish the remaining four.

A useful conceptual model is:

`observed descriptor = f(style-relevant appearance, subject/content, composition, acquisition/preprocessing, measurement choices)`

This is a design abstraction, not a validated additive decomposition.

#### Sources of uncertainty to record separately

| Source | Example | Proposed treatment |
|---|---|---|
| Region definition | Whether a glow belongs to the subject or background | Compare approved alternative masks; inspect boundaries |
| Mask algorithm | Thin appendages or translucent effects disappear | Mask-version provenance; boundary/core sensitivity analysis |
| Color interpretation | Missing profile versus embedded profile | Convert consistently; label assumptions when metadata is absent |
| Resolution/filter | Edge and texture descriptors move after resampling | Fixed canonical pipeline plus approved-scale sensitivity checks |
| Composition/content | A close-up has more face pixels than a full-body card | Condition on framing/category/region |
| Feature extractor | Different checkpoint or layer changes similarity | Pin model, weights, layer, normalization, pooling |
| Reference selection | A small board omits valid stylistic variants | Report sample support and known exclusions |
| Scene inference | Painted shading admits multiple lighting explanations | Store alternatives; avoid definitive physical parameter claims |
| Evaluator | Human or agent judges disagree | Measure reliability; preserve disagreements |

Perturbation-derived ranges are **sensitivity envelopes**, not automatically confidence intervals. Random statistical intervals require a declared sampling model.

Do not “normalize away” a desired axis. For example, automatic color matching before palette evaluation would erase the very deviation being tested.

#### Example structured record

Illustrative values below are invented to show schema design; they are not measurements of project assets.

```yaml
record_id: illustrative-card-001
schema_version: "proposal-1"
asset:
  image_hash: "<hash>"
  category: creature
  framing: full_body
  source_profile: unknown
  color_assumption: sRGB_assumed
  canonicalization_version: "<version>"

measurement:
  region:
    name: subject_core
    mask_id: "<mask-version>"
    boundary_policy: "<declared-policy>"

  observable_image_descriptor:
    name: normalized_bright_edge_fraction
    definition: "<versioned mathematical definition>"
    value: 0.13
    unit: fraction
    sensitivity_range: [0.10, 0.16]
    sensitivity_causes:
      - approved_mask_variants
      - approved_resampling_variants
    evidence:
      - "<overlay-or-crop-id>"
      - "<measurement-log-id>"

  inferred_scene_property:
    claim: possible_back_or_side_rim_illumination
    alternatives:
      - painted_outline
      - composited_glow
      - material_highlight
    physical_parameter_identified: false
    confidence:
      kind: qualitative
      level: low

  prompt_target:
    instruction: >
      Preserve the subject silhouette and broad value grouping;
      reduce the visible bright edging toward approved examples.
    linked_observable: normalized_bright_edge_fraction
    intended_axis: edge_treatment
    physical_parameter_claim: none

comparison:
  reference_group: creature_full_body_subject_core
  independent_reference_count: 4
  target:
    kind: provisional_art_directed_band
    range: [0.08, 0.15]
    statistically_validated: false
  confidence:
    descriptor_repeatability: tested
    acceptance_probability: null
    reason: insufficient_labeled_calibration_data
  decision: review
```

Important separation: the **observable descriptor**, **inferred scene explanation**, and **requested prompt change** are different objects. A prompt is an intervention proposal, not a recovered physical truth.

### Gaps

- No project images or masks were analyzed. No actual descriptor, acceptable band, threshold, or hardware runtime is established here.
- No cited source validates a definitive, independently controllable numerical style fingerprint for this collectible-card domain.
- A single reference cannot establish within-style variation or distinguish incidental properties from style-defining properties.

## 2. What do the candidate metrics actually measure, and what current prior art matters?

### Takeaway

Use complementary metrics for specific jobs: aligned-image regression checks, content preservation, texture/style retrieval, and human-calibrated style fidelity. None of the reviewed metrics supplies a universal per-card style-acceptance threshold.

### Cited Findings

#### Metric interpretation and limits

| Metric/family | Supported interpretation | Misinterpretation to avoid |
|---|---|---|
| **Gram/neural style statistics** | Correlations among feature channels over spatial locations, across selected layers | Complete style identity or exact spatial organization |
| **SSIM** | Full-reference local image-quality similarity, sensitive to luminance, contrast, structure and scale | Content-independent style similarity |
| **LPIPS** | Learned perceptual distance between image patches/images, calibrated using human distortion judgments | “Percentage of style mismatch” |
| **DISTS** | Full-reference structure-and-texture distance with explicit tolerance to texture resampling | Pure style distance or proof that all geometric drift is harmless |
| **CLIP** | Similarity in a representation trained through image–text matching | A style-only feature space or calibrated acceptance probability |
| **DINO-family features** | General-purpose self-supervised visual representations; useful semantic/dense correspondence cues | Guaranteed content-only or style-only representation |
| **ALADIN** | Learned artistic-style retrieval embedding | Universal calibrated perceptual acceptance |
| **CSD** | Contrastively trained style descriptor evaluated on retrieval and style-attribution tasks | Definitive artist attribution, absence/presence proof, or universal thresholds |
| **ASTRA-Score** | Learned prediction of study-derived content/style/overall preferences for style-transfer triplets | A validated judge of arbitrary collectible-card art |
| **StyleDecoupler** | Proposed content-suppressed style representation with reported retrieval/evaluation improvements | Proven universal semantic/style independence |
| **FID/KID/ArtFID** | Comparisons of feature distributions, with ArtFID additionally incorporating content comparison | Acceptance of an individual card |

Sources and qualifications follow.

**Gram matrices.** Gatys et al. describe their representation as stationary and multiscale, capturing texture information but not global arrangement. For a feature matrix `F`, `G = F Fᵀ` is invariant to permutations of the feature-map spatial columns. This algebraic invariance does **not** mean that arbitrary pixel permutations before the CNN preserve the result. **Confidence: high.** — [Gatys et al., 2015 / CVPR 2016 lineage](https://arxiv.org/abs/1508.06576)

Proposed use: region-conditioned texture/mark statistics, provided tests show useful sensitivity. Subject matter can still alter channel correlations; feature pooling does not establish semantic independence.

**SSIM.** The official project defines it as a quality measure when one image is treated as the reference. It discusses scale selection and reports grayscale evaluations. Use it to guard aligned, supposedly unchanged image areas—not to reject a different subject merely because its layout differs. Higher generally means more similar; identity scores 1. Do not assume every implementation’s score is a probability or confined to `[0,1]`. **Confidence: high.** — [SSIM, IEEE TIP 2004; official project](https://ece.uwaterloo.ca/~z70wang/research/ssim/)

**LPIPS.** The official implementation states: “Higher means further/more different. Lower means more similar.” Its BAPPS dataset uses two-alternative forced-choice and just-noticeable-difference judgments on reference/distortion patches. The implementation expects RGB tensors scaled to `[-1,1]`; network and metric version matter. **Confidence: high.** — [LPIPS, CVPR 2018; official implementation](https://github.com/richzhang/PerceptualSimilarity)

This supports perceptual-change checks. It does not validate comparison between unrelated reference and candidate subjects as a style-only test.

**DISTS.** The authors explicitly optimize tolerance to resampling of texture regions and combine structure and texture terms. They report relative insensitivity to some geometric transformations. The official implementation expects RGB in `[0,1]`. Lower distance means closer under this model. **Confidence: high.** — [DISTS, 2020 preprint / TPAMI 2021](https://arxiv.org/abs/2004.07728); [official implementation](https://github.com/dingkeyan93/DISTS)

Tolerance is task-dependent: a metric designed to ignore harmless texture rearrangement can also be insufficiently strict for a region where exact markings must remain unchanged.

**CLIP.** The original work trains image representations by predicting which caption matches an image, using 400 million image–text pairs. Consequently, image–image or text–image similarity may reflect subject, context, text, and style together. The official API’s logits are scaled cosine similarities, not acceptance probabilities. **Confidence: high.** — [CLIP, ICML 2021](https://proceedings.mlr.press/v139/radford21a.html); [official implementation](https://github.com/openai/CLIP)

**DINO.** DINOv2 is documented as a general-purpose visual representation. DINOv3 was released in 2025 and is a current alternative as of this cutoff. Its presence does not establish that replacing DINOv2 improves this particular style decision. **Confidence: high.** — [DINOv2 official repository](https://github.com/facebookresearch/dinov2); [DINOv3 official repository](https://github.com/facebookresearch/dinov3)

Neither “self-supervised” nor “semantic” proves complete style invariance. Check the exact model, pooling, layer, and preprocessing locally.

**ALADIN.** This ICCV 2021 approach learns fine-grained artistic-style similarity through weak supervision from a 2.62-million-image dataset containing approximately 310,000 style groupings. Its evidence concerns retrieval, not a universal binary acceptance criterion. **Confidence: high.** — [ALADIN paper](https://arxiv.org/abs/2103.09776)

**CSD.** The ECCV 2024 framework combines style-oriented self-supervision and style-label supervision. It explicitly recognizes subjectivity in style. Its artist-prototype approach is a useful precedent, but an artist-average embedding should not be imported as the project’s only representation. **Confidence: high.** — [CSD paper](https://arxiv.org/html/2404.01292v1)

**Important operational warning:** the official repository currently says:

> “We are currently investigating an issue with our uploaded model weights due to which there is some discrepancy with the reported numbers in the paper.”

This was confirmed through a direct live fetch, not only search snippets. **Confidence: high.** — [CSD official repository](https://github.com/learn2phoenix/CSD)

The paper’s suggested scores below `0.5` and above `0.8` are explicitly presented as a **hypothesis following inspection of generations for 96 artists**. They are not portable collectible-card acceptance thresholds. Weight discrepancies make uncritical reuse even less defensible. — [CSD §2](https://arxiv.org/html/2404.01292v1)

#### Newer style-specific work

**ASTRA, 2026-10-07: especially relevant.** The preprint constructs:
- 12 style references;
- 6 content references;
- 12 stylization methods;
- 864 generated results;
- separate content, style, and overall pairwise judgments.

Its retained study responses produce 34,608 votes. ASTRA-Score uses frozen visual features and separately trained prediction heads. **Confidence: high concerning reported design.** — [ASTRA full paper](https://arxiv.org/html/2610.10003v1)

Crucial limitations and useful results:

- Its primary intended deployment evaluates **new methods on the fixed benchmark references**.
- It also reports leave-one-content-out and leave-one-style-out robustness tests.
- Reported leave-one-style-out Spearman correlations are `0.711` for content, `0.700` for style, and `0.658` overall.
- Reannotation agreement is imperfect: reported style Cohen’s κ is `0.547` within content–style pairs and `0.389` across different pairs.
- It distinguishes style-transfer fidelity from general aesthetic appeal.
- It finds style-dependent content/style tradeoffs—not one universal tradeoff curve.

These are benchmark-specific results, not independent validation for this project. **Confidence: high concerning reported results; project applicability unknown.** — [ASTRA §§4–5](https://arxiv.org/html/2610.10003v1)

**StyleDecoupler, 2026-01-25.** This preprint proposes removing content-correlated components from multimodal representations using aligned DINO features and generated style/content descriptions. It introduces WeART and reports improved retrieval and human alignment. **Confidence: high that the paper makes these claims; lower confidence in generalization beyond its experiments.** — [StyleDecoupler](https://arxiv.org/html/2601.17697v1)

Do not repeat “training-free” without qualification:
- the method keeps the original VLM frozen;
- it nevertheless trains an alignment component;
- its text descriptions use GPT-4o;
- its description gives inconsistent alignment-data counts: 500,000 pairs in §3.1 versus “2000,000” in §4.1.

Also, removing one estimated content direction does not mathematically establish removal of every semantic factor. The paper’s “pure style” terminology is an author claim, not a validated guarantee. — [StyleDecoupler §§3–4](https://arxiv.org/html/2601.17697v1)

#### Why FID/KID do not decide individual-card acceptance

FID evaluates discrepancies between feature distributions summarized through Gaussian statistics. Chong and Forsyth show finite-sample bias that depends on the evaluated model; merely using the same sample count does not remove it. **Confidence: high.** — [Chong & Forsyth, CVPR 2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Chong_Effectively_Unbiased_FID_and_Inception_Score_and_Where_to_Find_CVPR_2020_paper.html)

KID uses an MMD-based comparison in Inception features and admits an unbiased estimator of the population squared discrepancy under its sampling assumptions. Unbiased does not mean low variance, correct domain representation, or reliable tiny-sample ranking. An unbiased finite-sample estimate can be negative even though the population discrepancy is nonnegative. **Confidence: high.** — [Bińkowski et al., ICLR 2018](https://arxiv.org/abs/1801.01401)

ArtFID is explicitly a complementary neural-style-transfer evaluation metric. Its official implementation compares content and generated images in pairs and computes style-related distribution comparisons. This is relevant prior art, but not a per-card acceptance oracle. **Confidence: high.** — [ArtFID, GCPR 2022](https://arxiv.org/abs/2207.12280); [official implementation](https://github.com/matthias-wright/art-fid)

Practical consequences, inferred from these definitions:

- One card does not provide a meaningful estimate of a broad style distribution.
- With `n` samples, an empirical feature covariance has rank at most `n−1`; high-dimensional tiny-sample estimates are particularly fragile.
- Matching collection statistics can hide individual defective cards.
- Changing category proportions can move a score without changing rendering style.
- KID’s unbiasedness does not manufacture missing reference diversity.
- Single-image spatial-feature methods such as SIFID change the sampling unit; they do not transform image patches into independent cards or prove style acceptance. ASTRA also evaluates SIFID and reports limitations in perceptual alignment. — [ASTRA](https://arxiv.org/html/2610.10003v1)

#### Existing projects already resemble the proposed loop

**Only-Style, June 2025** localizes reference-content leakage and adaptively tunes style-alignment strength. It additionally proposes coarse encoder-based and fine-grained LVLM-based leakage evaluation. This is direct prior art for measuring an unwanted effect and adjusting a style-control parameter. **Confidence: high.** — [Only-Style](https://arxiv.org/abs/2506.09916)

**EdiVal-Agent, 2025 preprint / ICLR 2026** decomposes image-edit evaluation into instruction following, consistency of unchanged content, and visual quality. It tracks object pools over editing turns and combines detection with semantic verification. This closely matches the proposed need for “make the requested correction and verify everything else.” **Confidence: high.** — [EdiVal-Agent paper](https://arxiv.org/html/2509.13399v3); [official implementation](https://github.com/TianyuCodings/EdiVal)

**MIRA, first submitted 2025-11-26**, explicitly uses an iterative perception–reasoning–action loop, atomic edits, intermediate visual feedback, and a stop decision. This establishes that broad agentic visual-correction orchestration is existing research, not an unexplored invention. It does not establish isolated, independently controllable style axes. **Confidence: high.** — [MIRA version history and abstract](https://arxiv.org/abs/2511.21087v1)

#### Official implementation, licensing, and feasibility notes

No software was installed or executed. License statements describe the inspected project; dependencies, weights, and datasets require their own checks.

| Implementation | License evidence | Maintenance/readiness observation | CPU / AMD assessment |
|---|---|---|---|
| [LPIPS](https://github.com/richzhang/PerceptualSimilarity) | BSD-2-Clause repository | Established reference implementation; pin network and metric version | CPU path documented; AMD runtime not tested |
| [DISTS](https://github.com/dingkeyan93/DISTS) | MIT repository | Official PyTorch/TensorFlow/MATLAB implementations; old minimum dependencies are not a current compatibility guarantee | CPU inference plausible; exact stack/AMD untested |
| [OpenAI CLIP](https://github.com/openai/CLIP) | MIT repository | Official implementation; automatic downloads possible | CPU explicitly documented; AMD untested |
| [DINOv2](https://github.com/facebookresearch/dinov2) | Apache-2.0 for standard repository/model release; some specialized additions have different terms | Repository documents updates and newer DINOv3 | CPU backbone inference plausible; full evaluation stack may assume GPU dependencies; AMD untested |
| [DINOv3](https://github.com/facebookresearch/dinov3) | Custom DINOv3 terms, not automatically Apache/MIT | Current official implementation; gated weight-access procedure documented | Small backbones are candidates, not a tested recommendation; AMD untested |
| [CSD](https://github.com/learn2phoenix/CSD) | MIT repository | Live weight-discrepancy disclaimer and stale pending-release text | Official scripts contain direct `.cuda()` calls; CPU requires code-path review/adaptation |
| [ArtFID](https://github.com/matthias-wright/art-fid) | MIT repository | Official implementation, explicit CPU device option | CPU documented; AMD untested |
| [Clean-FID](https://github.com/GaParmar/clean-fid) | MIT repository | Established implementation addressing preprocessing compatibility | Runtime configuration not tested here |
| [EdiVal](https://github.com/TianyuCodings/EdiVal) | Exact license not verified in this pass | Official setup targets CUDA 12.1 and multiple model dependencies | Not an out-of-box AMD/CPU recommendation |
| ASTRA / StyleDecoupler / ALADIN | Code/weight licensing not fully verified | Research evidence does not establish maintained turnkey tooling | No runtime claims justified |

CSD code inspection found, for example:

```python
samples = samples.cuda(non_blocking=True)
index = index.cuda(non_blocking=True)
```

— [Official `utils.py`](https://github.com/learn2phoenix/CSD/blob/main/utils.py)

PyTorch ROCm commonly exposes GPU operations through `torch.cuda`; therefore `.cuda()` alone does **not** prove NVIDIA-only operation. Conversely, it does not prove compatibility with this machine, auxiliary kernels, or the complete dependency stack. Treat AMD feasibility as unverified.

### Inferences

- Keep **style retrieval**, **content preservation**, **defect detection**, **aesthetic preference**, and **acceptance** separate.
- Use a descriptor vector and evidence overlays; do not relabel an embedding cosine as “style accuracy.”
- Treat newer learned metrics as candidates in a local benchmark, not automatic replacements for human calibration.
- Reuse existing evaluation principles and implementations where appropriate. The project-specific contribution is the carefully validated reference ontology, region/category conditioning, acceptance rules, and regression-controlled workflow—not the generic idea of a visual feedback loop.

### Gaps

- No head-to-head metric experiment on the supplied card art was performed.
- No independent replication of the October 2026 ASTRA or January 2026 StyleDecoupler results was established.
- ASTRA’s code/weights availability and license were not confirmed.
- Current repository availability is not evidence of active support or compatibility with the user’s AMD workstation.

## 3. How should calibration, acceptance, and iterative correction work?

### Takeaway

Use human-approved, condition-specific ranges and held-out evaluation, with explicit abstention when support is weak. Optimize one requested change at a time, but **remeasure the whole protected vector**: “one edit” is not evidence that only one visual axis changed.

### Cited Findings

Bootstrap percentile intervals can badly undercover in small samples. More resamples improve Monte Carlo precision of the resampling calculation, not the representativeness of the original data. **Confidence: high.** — [Hesterberg, 2014 preprint / 2015 article](https://arxiv.org/abs/1411.5279)

Conformal prediction provides finite-sample marginal coverage under its assumptions, using held-out calibration data and corrected quantiles. It does not automatically guarantee conditional coverage for every category or every selected image. **Confidence: high.** — [Angelopoulos & Bates, first posted 2021](https://arxiv.org/abs/2107.07511)

ASTRA’s controlled pairwise comparisons, separate criteria, reannotation reliability checks, and held-out method/content/style tests provide a relevant evaluation-design precedent. Its imperfect agreement and style-dependent tradeoffs argue against assuming a universally definitive numerical verdict. **Confidence: high.** — [ASTRA](https://arxiv.org/html/2610.10003v1)

EdiVal provides a relevant precedent for explicitly tracking unchanged content through multiple editing turns. Only-Style demonstrates that style strength and content leakage can require joint monitoring. **Confidence: high.** — [EdiVal](https://arxiv.org/html/2509.13399v3); [Only-Style](https://arxiv.org/abs/2506.09916)

### Inferences

The following is a **proposed project recipe**, not a published validated protocol for collectible-card art.

#### A. Define acceptance before choosing metrics

For each axis, declare:

- what visual property matters;
- applicable categories and regions;
- allowed variation;
- failure severity;
- whether it is a hard invariant, soft preference, or review-only judgment;
- whether its numerical direction is “higher is better,” “lower is better,” or “inside a band is better.”

“More similar” is not always desirable. A candidate can be too smooth, too saturated, or too close to a particular reference subject.

Distinguish:

1. **Specification band:** art director says what is allowed.
2. **Reference variation:** what appears among sampled approved assets.
3. **Predictive range:** an estimate for a future approved asset.
4. **Confidence interval for a mean:** uncertainty about an average.

A confidence interval for the mean is **not** an acceptance interval for individual images.

#### B. Build a reference index with independent units

Record category, framing, region applicability, resolution, profile, source provenance, duplicates, and known substyles.

Use reference distributions such as:

`P(descriptor vector | style family, card category, region, framing)`

Do not impose one universal reference mean across:
- characters, creatures, equipment, and environments;
- face, metal, cloth, foliage, background, and effects;
- close-up and full-body framing.

Start with only distinctions that have clear art-direction meaning. Excessive stratification creates empty or tiny cells.

Averages can fall between valid modes. For example, two approved edge-treatment regimes need not imply that their arithmetic midpoint is desirable.

#### C. Separate development, calibration, and final evaluation

- **Development references:** define descriptors and debug the pipeline.
- **Calibration cases:** set bands or decision thresholds and fit confidence models.
- **Held-out test cases:** estimate final acceptance errors and generalization.

Split by independent card/source family where possible. Crops, resized copies, and iterations of one image should not leak across partitions.

With very few independent cards:
- use leave-one-card-out diagnostics;
- call results provisional;
- preserve a genuinely untouched final set if possible;
- collect more references instead of manufacturing certainty through resampling.

Repeatedly examining a holdout while changing the system turns it into development data.

#### D. Estimate variation honestly with small samples

Report:
- independent image count;
- actual individual values;
- median and spread;
- which references are excluded or missing;
- uncertainty/sensitivity due to preprocessing.

Suggested caution:
- one reference: exemplar only, not a distribution;
- a handful: descriptive observed range and expert guidance;
- larger samples: empirical quantiles and uncertainty, subject to dependence and sampling checks.

These are practical cautions, not universal sample-size thresholds.

For bootstrap analyses:
- resample **cards**, not individual pixels;
- preserve before/after pairing;
- cluster correlated crops and repeated edits under their source image;
- resample raters as appropriate for the claimed population;
- do not treat all pairwise distances as independent observations.

`N` cards can yield many pairwise distances, but not that many independent cards.

Bootstrap cannot discover an omitted subtype. Tiny-stratum tail estimates remain weak even after thousands of resamples. Partial pooling across related strata is an option only if the similarity assumption is defensible and sensitivity is reported.

#### E. Validate each metric using controlled perturbations

Build a small, human-reviewed perturbation set from approved images:

- intended style changes;
- content substitutions with style held approximately constant;
- style changes with content held approximately constant;
- benign encoding/resampling changes;
- masking variations;
- deliberately defective local changes.

Then test:

- **Sensitivity:** does the descriptor respond to the intended change?
- **Specificity:** does it stay stable under irrelevant changes?
- **Monotonicity:** does increasing perturbation usually move it as expected?
- **Content leakage:** does same-subject/different-style outrank different-subject/same-style?
- **Scale stability:** are conclusions preserved at actual display size?
- **Region robustness:** do plausible masks change the decision?

A perturbation that is isolated in code is not necessarily isolated perceptually. Obtain human confirmation that “only saturation changed” remains an appropriate interpretation.

Use these experiments to construct a cross-axis response table:

`J[i,j] ≈ change in descriptor i caused by controlled intervention j`

This local sensitivity table diagnoses coupling. It is not a globally valid causal inverse model.

#### F. Conduct paired content/style tests

Include at least:

1. Same content, different style.
2. Different content, same approved style.
3. Same style, different category.
4. Correct style with a local artifact.
5. Incorrect style with matching palette.
6. Close reference copy with unwanted semantic leakage.
7. Subtle valid style variation that should be accepted.

Compare candidate metrics against **the same cases and judgments**. Report pairwise ranking accuracy and uncertainty, not just aggregate correlation.

A metric that rewards copying the reference subject should not be called a successful style metric.

#### G. Calibrate humans and agents

Use separate questions:

- Does the candidate fit the reference style?
- Is the intended content correct?
- Are protected details preserved?
- Are there visible defects?
- Is this acceptable for release?

Randomize presentation order and left/right placement. Hide generator identity and iteration number. Include repeated items and known failures.

For humans, report agreement and disagreement with appropriate statistics and intervals—not only majority vote.

For agents:
- pin model, prompt, image preprocessing, and comparison layout;
- test sensitivity to order and prompt wording;
- measure agreement with human judgments on held-out cases;
- log concrete evidence regions;
- retain “uncertain” and “not assessable.”

Several calls to the same model are not independent expert opinions. Agent self-reported confidence is not calibrated correctness probability.

Do not collapse genuine taste disagreement into fictitious ground truth.

#### H. Correct threshold logic

For a **distance**, lower is usually better:

`pass if distance ≤ calibrated upper threshold`

For a **similarity**, higher is usually better:

`pass if similarity ≥ calibrated lower threshold`

For a **banded descriptor**:

`pass if lower ≤ descriptor ≤ upper`

The threshold must be local to the checkpoint, preprocessing, region, category, and intended decision.

With an estimated uncertainty interval `[l,u]`:

- **Distance:** robust pass if `u ≤ threshold`; robust fail if `l > threshold`; otherwise review.
- **Similarity:** robust pass if `l ≥ threshold`; robust fail if `u < threshold`; otherwise review.
- **Allowed band `[L,U]`:** robust pass if `[l,u]` lies wholly inside the band; robust fail if wholly outside; otherwise review.

These rules are conservative engineering choices. Their statistical guarantees depend on how the intervals were constructed.

An unknown or missing metric is **not a pass**. Neither is “inside the observed reference range” proof of artistic acceptability.

A robust standardized deviation can be useful for display:

`z = (value − reference median) / robust scale`

But:
- a near-zero scale needs an explicit fallback;
- correlated descriptors should not be counted as independent evidence;
- `|z| < 2` is not a universal artistic rule.

Nearest-reference distance is also sample-count dependent: a larger reference bank offers more chances for a close match. Calibrate using matched reference-bank sizes and leave-one-out reference checks.

#### I. Confidence and abstention

If enough labeled cases exist, estimate acceptance probability using a small calibrated model and evaluate:
- false accepts;
- false rejects;
- calibration;
- review rate;
- subgroup behavior;
- errors on unfamiliar categories.

Reserve probability language for empirically checked probabilities.

With few examples, report evidence and support rather than invented numbers such as “93% style confidence.”

Conformal anomaly scoring is a possible later addition:

- freeze the score definition using development data;
- obtain independent calibration scores;
- compute the corrected calibration quantile;
- treat the result as an inlier/outlier check under exchangeability.

For simple split-conformal thresholding, quantile rank is:

`k = ceil((n + 1) × (1 − alpha))`

If `k > n`, use an uninformative threshold rather than silently clipping to an optimistic finite value. At nominal 95% coverage, `n = 19` is only the boundary at which the maximum observed score can supply a finite threshold; it is **not** a recommendation that 19 examples provide strong calibration.

Coverage is marginal, not a guarantee that a particular accepted card is artistically correct. Adaptive generation and repeated score-based selection can invalidate naïvely imported guarantees. — Statistical basis: [Angelopoulos & Bates](https://arxiv.org/abs/2107.07511)

Abstain when:
- category support is insufficient;
- masks are unreliable;
- metric and human evidence conflict;
- the candidate is out of distribution;
- uncertainty straddles the decision boundary;
- a requested property is not observable.

#### J. Keep a vector, not a magic aggregate

Recommended output:

```text
style fidelity: provisional pass
content compliance: pass
protected-region preservation: fail
local defects: review
descriptor support: low
overall decision: review
```

An aggregate may help rank already-eligible alternatives, but should not permit excellent palette matching to cancel a missing required object or damaged face.

If combining scores:
- predeclare weights and transformations;
- keep hard gates separate;
- show the full vector;
- test ranking sensitivity to weights;
- avoid presenting the sum as an objective quantity.

#### K. Iteration with invariants and regression guards

For each proposed correction:

1. Save the baseline and full measurement vector.
2. Declare the intended improvement and protected properties.
3. State expected cross-axis effects.
4. Produce a candidate.
5. Remeasure all affected and protected axes.
6. Compare candidate and baseline under identical measurement conditions.
7. Accept only if target improvement is practically meaningful and regressions remain within approved limits.
8. Otherwise revert, branch, or request a tradeoff decision.

Compare protected properties against both:
- the previous accepted iteration, to detect immediate damage;
- the original approved baseline, to detect accumulated drift.

“Invariant” does not always mean exact pixel identity. Define whether preservation means identical pixels, unchanged subject identity, stable silhouette, unchanged composition, or tolerable perceptual deviation.

Global stylistic changes may necessarily affect multiple descriptors. Correlated axes and style-specific Pareto tradeoffs should be surfaced rather than described as agent failure to follow an impossible independence promise. ASTRA supplies relevant empirical precedent, but does not prove every tradeoff is unavoidable. — [ASTRA](https://arxiv.org/html/2610.10003v1)

#### L. Goodhart effects and reward hacking

Treat these as anticipated failure modes:

- copying reference content to improve embedding similarity;
- blurring detail to reduce a distance;
- altering region area so global color statistics improve;
- adding repeated high-response texture;
- optimizing the judge’s favored aesthetic rather than the target style;
- exploiting a mask boundary;
- selecting the best score among many noisy attempts.

Mitigations:
- independent content and defect checks;
- hidden or periodically refreshed audit cases;
- human review of high-scoring unusual outputs;
- randomized controlled challenges;
- separate development and acceptance metrics where useful;
- checkpointing and full lineage;
- no repeated tuning against an allegedly untouched final set.

An ensemble is useful only to the extent its errors are complementary; several correlated embeddings do not establish independent confirmation.

#### M. Stopping rules

Declare stopping rules before running the loop:

- all hard constraints satisfied;
- target metrics within approved bands;
- no unacceptable protected-axis regression;
- human/agent evidence sufficient for the decision;
- no practically meaningful improvement over a specified number of attempts;
- iteration, time, or cost budget exhausted;
- repeated oscillation between coupled objectives;
- uncertainty too large to justify another automatic correction.

Stopping may mean **accept**, **retain best candidate**, **request review**, or **collect better evidence**. It should not always mean “keep optimizing until every score improves.”

#### What cannot honestly be fully automated here

Without further validation, do not promise:
- a uniquely correct decomposition of style;
- recovery of exact physical lighting/material parameters from stylized pixels;
- universal thresholds across categories and styles;
- causal independence of edit axes;
- calibrated probabilities from raw embedding scores or agent confidence;
- reliable tail estimates from a tiny reference board;
- automated resolution of genuine aesthetic disagreements;
- artifact detection with zero misses;
- guaranteed convergence to an acceptable image.

The defensible goal is **auditable assisted evaluation with calibrated limits**, not definitive numerical art judgment.

### Gaps

- The entire practical recipe requires local validation against the actual card taxonomy, references, display conditions, and art director.
- Available independent reference counts, category coverage, and annotation budget remain unknown.
- No actual false-accept/false-reject rates, minimum detectable improvements, or stopping thresholds can be justified yet.
- Parent remains synthesis/verification owner; this note validates cited claims, not an implemented pipeline.

#### Source-date and verification summary

Core evidence spans:
- SSIM: 2004.
- Bootstrap caution: 2014 preprint / 2015 article.
- Gatys neural style: 2015 / 2016.
- KID and LPIPS: 2018.
- FID finite-sample bias and DISTS: 2020; DISTS journal publication 2021.
- CLIP, ALADIN, conformal introduction: 2021.
- ArtFID and Clean-FID: 2022.
- DINOv2: 2023; DINOv3: 2025.
- CSD and IntrinsicAnything: 2024.
- Only-Style, EdiVal, MIRA initial releases: 2025.
- StyleDecoupler: January 2026.
- ASTRA: **October 7, 2026**, within cutoff.

Approximately **22 primary research works**, supplemented by official educational, standards, and implementation sources. Live verification specifically confirmed the CSD disclaimer and checked ASTRA’s evaluation setting and StyleDecoupler’s implementation qualifications.

**Research spend:** 32 Kagi discovery queries, four Exa batch-fetch calls, direct source-page verification, one GitHub code search, and one relevant Memory lookup. No Perplexity, Kagi Assistant, Deep Research job, external image upload, software installation, model-weight download, or untrusted code execution.
