# Attention, readability, and economy of detail

Key checks: verified 2026 DeepGaze developments, licensing restrictions, TempSAL’s conflicting license notices, SALICON’s mouse-based provenance, and OpenCV’s 64×64 spectral-residual default. **15 primary-source entries; no models, weights, installs, or private uploads.**

Research cutoff and access date: **2026-10-31**.

Scope: attention hierarchy, focal dominance, foreground/background readability, regional detail allocation, and attention over time in stylized casual-game art. Composition geometry—camera, placement, symmetry, perspective, balance—is outside this note except where it must be controlled as a confound.

## 1. What can be measured, and what does each measurement actually establish?

### Takeaway

Use three separate evidence layers: **deterministic image descriptors**, **learned predictions of viewing behavior**, and **observed human behavior**. None substitutes for the others: an image can have concentrated contrast but an unclear subject, and a model’s saliency hotspot is not proof of where players actually look.

### Cited Findings

- Modern “saliency” sometimes means predicted fixations rather than exclusively bottom-up conspicuity. Consequently, a learned saliency model can incorporate semantic objects, context, and viewing biases; it should not automatically be described as a low-level contrast detector. — [S5](https://arxiv.org/html/1604.03605v2), [S6](https://arxiv.org/html/1704.08615v2).
- In eye-tracking experiments, task demands could eliminate or reverse a free-viewing bias toward high-contrast image regions. Thus “highest contrast receives attention first” is not a task-independent rule. — [S4](https://authors.library.caltech.edu/records/ywkb0-v8462).
- In a study using 20 photographic scenes and 30 analyzed viewers, rated semantic meaning predicted fixation distributions better than the tested GBVS image-salience model, including early fixations. This supports accounting for meaning; it does **not** establish that semantics always beats every modern learned model, nor validate the result for casual-game cards. — [S3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6690792/).
- Regional clutter is not equivalent to object count, edge count, or high-frequency energy. Rosenholtz and colleagues evaluated feature congestion, subband entropy, and edge density; their illustrations include imagery with similar edges/high-frequency content but different color variability. Target–distractor discriminability also matters for search performance. — [S2](https://jov.arvojournals.org/article.aspx?articleid=2122001).
- Saliency evaluation depends on viewing setup, map representation, smoothing, bias treatment, and the selected metric. Different metrics can rank the same maps differently. — [S5](https://arxiv.org/html/1604.03605v2), independently developed further in [S6](https://arxiv.org/html/1704.08615v2).
- Cross-dataset transfer remains material even for strong modern models. The 2025 DeepGaze MSDB paper reports an approximately 40% performance drop in its cross-dataset comparisons and identifies substantial dataset-specific bias. That number is specific to its experiments, not a forecast of error on this project. — [S8](https://openaccess.thecvf.com/content/ICCV2025/html/Kummerer_Modeling_Saliency_Dataset_Bias_ICCV_2025_paper.html).

### Inferences

#### Evidence classes

The following labels prevent a deterministic measurement from being mistaken for psychophysical validation.

| Label | Meaning | Appropriate claim |
|---|---|---|
| **D** | Deterministic descriptor, given fixed preprocessing and masks | “Background edge density is lower.” |
| **H** | Proposed engineering heuristic or feature construction | “This feature is a candidate control signal; predictive usefulness is unvalidated.” |
| **L** | Learned model prediction | “This model assigns more predicted fixation mass to the focal object.” |
| **B** | Behavioral measurement under a specified experiment | “Participants identified the object more accurately at this card size.” |
| **N** | Normative accessibility requirement, within its applicable scope | “The meaningful icon meets the specified adjacent-color contrast criterion.” |

**D is not B.** A learned model can run deterministically, but its interpretation remains **L**, not observed behavior. A human rating of “readability” is **B**, but differs from object-identification accuracy, response time, or measured gaze.

All feature definitions below are proposed operational definitions unless attributed directly to an existing algorithm. They are not published universal measures of “casual-game style.”

#### Establish the task before extracting features

Record:

- Intended subject and its semantic identity.
- Required reading task: recognize object category, identify character expression, distinguish reward tier, locate an interactive target, understand a narrative action, or appreciate an illustration.
- Actual display dimensions in **physical/display pixels**, not merely source-image resolution.
- Exposure duration and interaction context.
- Whether the image appears alone or among neighboring cards, labels, badges, and UI.
- Which details are identity-bearing versus decorative.
- Intended focal hierarchy, expressed as semantic roles: primary subject, secondary support, environment.
- Whether an illustration is meant to have one dominant focal group or several legitimate targets.

Do not assume that maximum focal concentration is always desirable. Hidden-object scenes, multi-item rewards, and narrative scenes can intentionally distribute attention.

#### Shared preprocessing and masks

Use a reproducible measurement manifest.

**Image treatment**

1. Record source dimensions, color profile, alpha handling, and compression.
2. Convert to a declared working sRGB representation.
3. Composite alpha against the actual intended backdrop for deployment tests. Separately preserve alpha/object masks.
4. Exclude padding, letterboxing, and areas outside the artwork using a valid-art mask \(V\).
5. For analytical scale comparisons, create an aspect-preserving image with **long side \(L=1024\) pixels**. This is a proposed working resolution, not a perceptual standard.
6. Also render at the actual deployment sizes. Do not infer small-card readability solely from the analytical image.
7. Use the same resampling method for references and candidates. Disable extra sharpening for the baseline comparison.
8. Do not histogram-match, independently equalize, or globally normalize each image’s contrast before measuring style differences. Such preprocessing can remove the differences of interest.

**Color**

For encoded sRGB channel \(c\in[0,1]\):

\[
c_{\mathrm{lin}}=
\begin{cases}
c/12.92,&c\le0.04045\\
((c+0.055)/1.055)^{2.4},&c>0.04045
\end{cases}
\]

Define relative luminance:

\[
Y=0.2126R_{\mathrm{lin}}+
0.7152G_{\mathrm{lin}}+
0.0722B_{\mathrm{lin}}.
\]

\(Y\) is dimensionless, nominally \([0,1]\); it is not measured display luminance in cd/m². These are the sRGB/WCAG relative-luminance definitions. — [S14](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

For chromatic descriptors, use a declared Lab conversion, preferably sRGB → XYZ D65 → CIELAB with D65 reference white. Record \(L^*,a^*,b^*\) units. Do not mix a library’s byte-encoded Lab arrays with conventional Lab values.

**Semantic masks**

Use manual annotation initially:

- \(F\): primary focal object or focal **group**.
- \(S_j\): secondary meaningful objects.
- \(C_j\): competing objects or decorative groups.
- \(B\): background/environment.
- \(U\): UI, text, frames, badges, logos.
- \(V\): valid artwork.

Define masks as disjoint visible-pixel assignments for regional accounting. A semantic focal group may contain several objects; do not confuse group count with object count.

Analyze the artwork without \(U\), then the full deployed card with \(U\). A bright badge can dominate deployment attention even when the isolated artwork reads well.

For each mask:

\[
A_M=\sum_x M(x),\qquad
a_M=A_M/A_V.
\]

Report \(A_M\) in pixels and \(a_M\) as a fraction or percentage. Mask area is primarily a **content/layout covariate**, not the attention-style target.

Use:

- **Interior masks** eroded sufficiently to exclude object boundaries when measuring internal texture.
- **Boundary samples** for foreground/background separation.
- **Local exterior rings**, excluding unrelated objects, for adjacent-background comparisons.
- Confidence flags for uncertain masks, translucency, hair, glow, cast shadow, and contact regions.

Compute filters on the image **before** applying regional masks. Filtering a blacked-out masked object introduces artificial edges.

#### Feature dictionary: contrast distribution and separation

Let \(d=\min(W,H)\) at the measurement resolution. Gaussian standard deviations below are in image pixels.

| Feature | Definition, units, scale and mask | Evidence and interpretation |
|---|---|---|
| **Regional luminance** | Median and 10th/90th percentiles of \(Y\) within \(M\). Dimensionless \([0,1]\). Report per \(F,S_j,B\). | **D**. Describes value allocation, not gaze. |
| **Regional RMS luminance variation** | \(\sigma_Y(M)=\sqrt{\operatorname{mean}_M[(Y-\bar Y_M)^2]}\). Same units as \(Y\). | **D**. Sensitive to shading, large value changes, and texture together. Not pure detail density. |
| **Multiscale luminance center–surround contrast** | \(C^Y_s(x)=|G_s*Y-G_{2s}*Y|/(G_{2s}*Y+0.05)\), with \(s/d\in\{0.005,0.01,0.02,0.04\}\). Report mean, p90, and regional mass separately at each scale. | **D/H**. Proposed normalized descriptor. The 0.05 floor is a fixed engineering choice, not a visual threshold. |
| **Chromatic center–surround contrast** | \(C^{ab}_s=\sqrt{(G_s*a^*-G_{2s}*a^*)^2+(G_s*b^*-G_{2s}*b^*)^2}\). Lab units; same scales. | **D/H**. Chromatic variation with lightness omitted; not full color difference and not guaranteed discriminability. |
| **Edge-contrast distribution** | On \(Y_\sigma=G_\sigma*Y\), use central differences \(g_x=[Y_\sigma(x+1)-Y_\sigma(x-1)]/2\), likewise \(g_y\); \(g=\sqrt{g_x^2+g_y^2}\). Units \(Y/\mathrm{pixel}\). Proposed \(\sigma=0.002d\). | **D/H**. Report regional mean/p90 and maps. Exact derivative and smoothing must be fixed. |
| **Local foreground/background value separation** | At boundary point \(p\), sample median luminance in an interior disk and adjacent exterior disk, centers displaced along the boundary normal. Proposed displacement \(r=0.01d\), disk radius \(r/2\). Define signed \(\Delta Y_p=Y_{\mathrm{in},p}-Y_{\mathrm{out},p}\). Report median signed difference and p10/median of \(|\Delta Y_p|\). | **D/H**. p10 exposes weak boundary sections that a whole-object average can conceal. Exclude occluding-object boundaries or label them separately. |
| **Local chromatic separation** | Same paired samples: \(\Delta ab_p=\sqrt{(\Delta a^*_p)^2+(\Delta b^*_p)^2}\). Lab units. | **D/H**. Pair with value separation. Equal-luminance hue contrast can disappear in grayscale or change under CVD simulation. |
| **Boundary weakness fraction** | Fraction of sampled boundary points with \(|\Delta Y_p|<t_Y\), optionally also \(\Delta ab_p<t_{ab}\). | **D/H**. Thresholds must be declared and calibrated to references/task; no universal pass threshold is established here. |
| **Internal-to-boundary contrast allocation** | Report internal gradient energy separately from paired boundary differences; compare the two-component profile rather than forcing them into an unstable ratio. | **D/H**. Distinguishes a well-separated simple subject from an internally busy subject that merges into the background. |

Boundary normals are unreliable at tiny details and corners. Store excluded-sample counts. Shadows and rim glows can improve separation while changing lighting/material style; annotate their contribution rather than silently treating every boundary as equivalent.

A chromatic map and a luminance map should remain separate. Combining them prematurely can hide whether a candidate achieves focal dominance by value, hue, or sharpness.

#### Feature dictionary: focal dominance and spatial concentration

For a nonnegative map \(q(x)\), define:

\[
p(x)=q(x)/\sum_{x\in V}q(x).
\]

This normalization creates a unit-sum distribution. It **does not** make an arbitrary contrast map a calibrated probability of human fixation.

If the map is identically zero, report “undefined/no map energy,” not an artificial uniform distribution.

| Feature | Definition | Units and interpretation |
|---|---|---|
| **Focal map mass** | \(m_F=\sum_{x\in F}p(x)\). | \([0,1]\), **D/H** for contrast maps; **L** for model-predicted fixation density. |
| **Area-adjusted focal enrichment** | \(e_F=m_F/a_F\). | Dimensionless. Uniform map gives 1. Distinguishes concentration from simply having a large focal mask. |
| **Focal/competitor dominance** | \(D_m=m_F/\max_j m_{C_j}\); additionally \(D_e=e_F/\max_j e_{C_j}\). | Dimensionless ratios. Report numerator/denominator and zero-denominator cases. Object/group masks must be comparable. |
| **Regional mass vector** | \((m_F,\sum_jm_{S_j},\sum_jm_{C_j},m_B,m_U)\), retaining separate maps/scales. | Role-based attention-allocation profile. Useful across different content; not a single quality score. |
| **Concentration area \(K_{80}\)** | Sort valid pixels by \(p\), find minimum number whose cumulative mass reaches 0.8, divide by \(A_V\). | Fraction \((0,1]\). Smaller means more concentrated map energy, not necessarily better art. |
| **Object-level competitive peaks** | For each semantic object/group, compute regional map mass and a robust local maximum after a fixed blur. Rank objects, rather than counting every tiny pixel maximum. | Rank/count, **D/H** or **L**. Avoids interpreting texture speckles as independent focal objects. |
| **Normalized map entropy** | \(H_p=-\sum p\log_2p/\log_2 A_V\), on the same evaluation grid. | Nominally \([0,1]\). Grid- and smoothing-dependent. Never compare differently resized maps without normalization. |

Do not independently min–max normalize every regional map before comparing mass: that destroys relative strength.

Use these features to describe **distribution of visual emphasis**, not to prescribe centering, moving objects, or changing their sizes.

#### Feature dictionary: detail economy and regional frequency

All these features are **D**, with **H** interpretation as style controls. None directly counts semantically meaningful details.

| Feature | Exact operational definition | Scale, masks, caveats |
|---|---|---|
| **Thresholded edge density** | \(E_M=\sum_{x\in M^\circ}\mathbf1[g(x)>\tau]/A_{M^\circ}\). | Fraction \([0,1]\). Proposed starting \(\tau=0.01\,Y/\mathrm{pixel}\) at the canonical resolution; calibrate once, freeze, and repeat a threshold-sensitivity check. Do not choose a fresh percentile threshold per image. |
| **Local luminance entropy** | Quantize \(Y\) to 32 fixed equal-width bins over \([0,1]\). For a square window, \(H=-\sum_{b=1}^{32}p_b\log_2p_b\). | Bits, \([0,5]\). Proposed window side nearest odd integer to \(0.05d\). Skip windows too small for a useful histogram; do not silently enlarge them and claim the same scale. |
| **Regional local-entropy summary** | Median/p90 of the window-entropy map whose windows lie entirely within \(M^\circ\). | Bits. Flat gradients can have high histogram entropy; spatial arrangement is not represented. |
| **Multiband detail energy** | \(D_s=G_s*Y-G_{2s}*Y\); \(E_{M,s}=\operatorname{mean}_{M^\circ}(D_s^2)\). Use \(s/d\in\{0.002,0.004,0.008,0.016,0.032\}\). | \(Y^2\). These overlapping DoG bands are not an orthogonal Fourier power decomposition. |
| **Fine-band share** | \(\rho_{\mathrm{fine},M}=(E_{M,s_1}+E_{M,s_2})/\sum_{k=1}^{5}E_{M,s_k}\). | \([0,1]\), unless total energy is zero, then undefined. Report absolute energy alongside the fraction. |
| **Focal/background detail allocation** | Compare \(E_{F,s}\) with \(E_{B,s}\), plus \(E_F^{\mathrm{edge}}\), \(E_B^{\mathrm{edge}}\), and entropy summaries. | Prefer a vector of differences or log-ratios with a declared floor, not an unsupported universal “ideal ratio.” |
| **Detail-budget share** | For a nonnegative detail map \(q_D\), \(b_F=\sum_Fq_D/\sum_Vq_D\), accompanied by \(b_F/a_F\). | Separates total allocated detail from area-adjusted density. |
| **Regional quiet-area fraction** | Fraction of windows in \(B\) below fixed edge-energy and local-contrast thresholds. | \([0,1]\), **D/H**. “Quiet” is threshold-defined, not empty of content. |

For interior frequency measurements, erode masks by at least the effective filter support—e.g. \(3(2s)\) for the larger Gaussian in each DoG pair. If a small focal object has no valid interior at a coarse scale, mark that measurement unavailable.

At low resolutions, omit frequency bands whose Gaussian scale falls below a declared minimum, such as 0.6 pixel, and mark the altered band set. Do not compare a five-band canonical ratio with a two-band thumbnail ratio as if identical.

**Key interpretation:** high edge density can arise from outlines, patterned materials, compression artifacts, grass, or many objects. High entropy can arise from a gradient or noise. A descriptor becomes an actionable style feature only after its cause is identified.

### Gaps

- No source reviewed establishes universal numerical targets for “Playrix-like” focal dominance, entropy, edge density, or fine-detail share.
- The proposed regional formulas need validation on the project’s reference set and tasks.
- Meaning-map studies predominantly use photographs. Their relevance to stylized cards is plausible but not directly established by these studies.
- Eye fixation is an operational measure of overt viewing, not a complete measurement of comprehension, preference, or covert attention.
- Foreground/background separation is not reducible to average luminance difference: semantic recognition, occlusion, shape, and context remain relevant.

## 2. Which deterministic and learned methods are useful, and how should they be validated?

### Takeaway

Begin with masks, multiscale contrast/detail maps, and actual-size recognition tests. Add learned saliency only when its extra semantic prediction is useful; add scanpath models or eye tracking only when the question genuinely concerns temporal attention flow.

### Cited Findings

#### Deterministic spectral-residual saliency

The inspected official OpenCV implementation:

- Initializes its internal resolution to **64×64**.
- Converts three-channel BGR input to grayscale.
- Resizes to that internal resolution.
- Computes Fourier magnitude and phase.
- Uses \(\log(1+\text{magnitude})\), subtracts a 3×3 average-filtered version, exponentiates, reconstructs with the original phase, applies an inverse transform, blurs magnitude, squares it, normalizes by the maximum, and resizes the result back to input dimensions.

Relevant source:

```cpp
resImWidth = 64;
resImHeight = 64;
```

```cpp
log( magnitude + Scalar( 1 ), logAmplitude );
blur( logAmplitude, logAmplitude_blur, Size( 3, 3 ), ... );
exp( logAmplitude - logAmplitude_blur, magnitude );
```

The exact implementation is therefore not interchangeable with every paper or library’s “spectral residual” variant. Its grayscale conversion is also not the same operation as the linear-sRGB \(Y\) definition above. — [S1](https://github.com/opencv/opencv_contrib/blob/5.x/modules/saliency/src/staticSaliencySpectralResidual.cpp).

For the inspected variant, a schematic formula is:

\[
F=\mathcal F(I),\quad
R=\log(1+|F|)-h_{3\times3}*\log(1+|F|),
\]

\[
T=\left|\mathcal F^{-1}\left(e^{R+i\arg F}\right)\right|,
\qquad
S=\frac{(G*T)^2}{\max (G*T)^2}.
\]

The source applies its Gaussian smoothing to reconstructed magnitude **before squaring**. An implementation that smooths squared magnitude instead is a different variant.

#### Learned models and implementation readiness, current to 2026-10-31

| Model | What it predicts and relevant evidence | License, maintenance, hardware findings |
|---|---|---|
| **DeepGaze IIE** | Spatial fixation-density prediction. Official example returns `log_density_prediction` and accepts an explicit center-bias map. — [S7](https://github.com/matthias-k/DeepGaze). | Repository latest inspected commit: **2026-08-25**, SHA `c7db17e2d1d7ea6468ffdee2cfaddf141095dcff`. No repository license was identified by the public GitHub license endpoint; do not assume commercial permission. CPU/AMD execution was not tested. |
| **DeepGaze III** | Predicts the next-fixation density conditioned on the image and previous fixations. This is materially different from a static map. — [S7](https://github.com/matthias-k/DeepGaze). | Same repository/license uncertainty. Official examples use `DEVICE='cuda'`; this alone neither proves NVIDIA-only implementation nor establishes ROCm compatibility. |
| **DeepGaze MSDB, ICCV 2025** | Combines CLIP and DINOv2 features with multiscale processing and dataset-specific parameters. Official API requests `pixel_per_dva`; unknown datasets can use averaged parameters. — [S7](https://github.com/matthias-k/DeepGaze), [S8](https://openaccess.thecvf.com/content/ICCV2025/html/Kummerer_Modeling_Saliency_Dataset_Bias_ICCV_2025_paper.html). | Current, scientifically relevant option for controlling viewing-scale/dataset effects. Same unresolved repository licensing. CPU feasibility and RX 7900 XTX/ROCm compatibility unmeasured. No memory or latency estimate is asserted. |
| **DeepGaze3.5-VL, 2026** | Autoregressive VLM scanpath model. Paper reports 2.18 bits IG on MIT1003 and a 46% improvement over DeepGaze III under its evaluation. These are author-reported benchmark results, not validation for game art. — [S9](https://arxiv.org/abs/2607.02083). | Official release uses an InternVL3.5-8B base plus LoRA adapters; latest inspected commit **2026-09-18**, SHA `5cd84d2225beb92e77617b1ee5c5480cae948ab7`. Code and named combined adapter are **non-commercial research use only**; base-model terms are separate. Official workflow requires a GPU. AMD/ROCm and CPU use are unverified. — [S10](https://github.com/Susmit-A/DeepGaze3.5-VL), [license](https://github.com/Susmit-A/DeepGaze3.5-VL/blob/master/LICENSE). |
| **TempSAL, CVPR 2023** | Predicts time-sliced and aggregate saliency. Official supplementary material describes one-second slices for static-image observation and approximate timestamp recovery. — [S11](https://github.com/IVRL/Tempsal), [S12](https://ivrl.github.io/Tempsal/). | Latest inspected commit **2025-03-11**, SHA `4bdf3d5f173f390da0f714dfd10873c701d7ca32`. Root `LICENSE` says MIT, but README says CC BY-SA 4.0: a material scope conflict, particularly for checkpoints/assets. CPU and AMD compatibility untested. — [license](https://github.com/IVRL/Tempsal/blob/main/LICENSE). |

Repository dates above were checked using public GitHub repository/commit endpoints. They establish recent repository activity, **not** a maintenance guarantee or support SLA.

Additional implementation caution: the inspected DeepGaze ShapeNet helper has explicit `.cuda()` calls in optional VGG/AlexNet loading branches, while its ResNet branch loads checkpoints with CPU map location. This does not establish that the focal DeepGaze variants are CPU-incompatible, but it prevents a blanket “all models are device-agnostic” claim without tracing the chosen execution path. — [implementation](https://github.com/matthias-k/DeepGaze/blob/main/deepgaze_pytorch/features/shapenet.py).

#### What is and is not gaze evidence

- SALICON’s original collection method uses a **mouse-contingent multiresolution paradigm instead of an eye tracker**. The authors validated the paradigm and proposed it as useful saliency ground truth, but mouse-derived observations should not be relabeled hardware eye-tracking measurements. — [S13](https://openaccess.thecvf.com/content_cvpr_2015/html/Jiang_SALICON_Saliency_in_2015_CVPR_paper.html).
- TempSAL’s supplement explains that fixation timestamps are approximated using spatial/temporal relationships to available points. Therefore its time-sliced predictions require extra caution when interpreted as precise eye-movement timing. — [S12](https://ivrl.github.io/Tempsal/).
- DeepGaze3.5-VL separates free-viewing and visual-search adapters. The documented search adapter was trained on the 18 COCO-Search18 target categories; generalizing it to a jewel, fantasy creature, or game-specific reward is not established by the release. Its release uses a 100×100 coordinate representation. — [S10](https://github.com/Susmit-A/DeepGaze3.5-VL).

#### Accessibility evidence

- WCAG 2.2 non-text contrast addresses visual information needed to identify UI components/states and graphical parts required for understanding, with **3:1 against adjacent colors**, subject to specified exceptions. It is not a requirement that every decorative painted edge in an illustration achieve 3:1. The guidance also warns that thin, antialiased graphics can be substantially less visible in practice than nominal colors imply. — [S14](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
- Machado et al.’s CVD model provides severity-dependent matrices for protan, deutan, and tritan simulations; its project page documents experimental validation and an equation erratum. The published supplementary matrices were computed using the correct equations. Simulation is a model of appearance, not an accessibility certificate for every viewer. — [S15](https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html).

### Inferences

#### Useful deterministic approaches

**1. Separate-channel multiscale contrast**

Compute the luminance, chromatic, and edge maps defined in Section 1. These are the most interpretable starting point because corrective edits can target the responsible channel.

If combining them into a diagnostic “conspicuity” map:

\[
q_s=w_Y\widetilde C^Y_s+
w_{ab}\widetilde C^{ab}_s+
w_E\widetilde C^E_s,
\]

freeze weights and scaling constants from a reference/calibration set. Do not normalize each candidate independently. Call the result **engineered conspicuity**, not predicted gaze.

**2. Spectral residual**

Useful as a cheap second opinion on visual irregularities. It is not a semantic subject detector. The default 64×64 internal processing can suppress small cues; forcing a non-square image into 64×64 also changes aspect ratio internally.

For production analysis:

- Pin the implementation/version and its internal dimensions.
- Preserve aspect ratio or document that the stock algorithm does not.
- Test sensitivity to internal resolution.
- Inspect whether a hotspot comes from a meaningful subject or an accidental texture/edge anomaly.
- Keep its result separate from the directly interpretable contrast maps.
- Handle flat/degenerate images explicitly rather than relying on maximum normalization.

**3. Feature congestion / subband entropy**

Potential advanced descriptors when edge density fails to distinguish reference and candidate. Use a verified implementation of Rosenholtz’s actual method if claiming “feature congestion.” A local Lab covariance determinant is only a proposed congestion-like proxy unless it reproduces the published algorithm.

**4. Regional frequency and edge analysis**

Usually more actionable than one global “complexity” number. Compute:

- Foreground interior detail.
- Background detail.
- Focal boundary contrast.
- Secondary-object detail.
- UI contamination.

This reveals whether the problem is excessive detail everywhere or poor allocation of an otherwise suitable detail budget.

#### Cross-scale tests

These are **diagnostic interventions**, not independently validated readability metrics.

| Test | Procedure | What a failure suggests | What it cannot establish |
|---|---|---|---|
| **Actual-size thumbnail** | Render at intended card sizes, using the production backdrop and neighboring UI. Ask the defined recognition question. | Identity-bearing cues are too small, weak, or crowded. | Why they failed without further inspection. |
| **Blur ladder** | Apply Gaussian blur at \(\sigma/d=\{0,0.005,0.01,0.02\}\), same for reference/candidate. | Focal hierarchy relies on fine detail rather than broad contrast structure. | A calibrated simulation of low vision or universal gaze. |
| **Grayscale** | Use declared luminance conversion, not arbitrary desaturation. | Separation depends heavily on chromatic differences. | That the original colored image is necessarily unreadable. |
| **Silhouette** | Show focal-group mask as a flat shape, then relevant object masks separately. Test category/action recognition if silhouette is important to the task. | Identity/action depends on internal details, or shape is ambiguous. | A requirement that all objects must be identifiable by silhouette. |
| **CVD simulation** | Apply a documented linear-color pipeline and declared model/severity; inspect essential cues at deployment size. | Hue-only encoding or fragile local separation. | Actual experience of all color-deficient viewers. |
| **Background suppression** | Temporarily replace background with a neutral field while preserving subject pixels. | If recognition improves, interference is background-related. | That removing background is an appropriate final stylistic edit. |

For a Gaussian blur, spatial frequencies are attenuated by:

\[
H(f)=e^{-2\pi^2\sigma^2f^2},
\]

with \(f\) in cycles/pixel and \(\sigma\) in pixels. This makes the blur ladder a reproducible frequency intervention; it does not make blur a substitute for viewing-distance or vision testing.

**Measure two scale systems separately**

1. **Relative-image scale:** same proportion of image width/height, useful for style.
2. **Actual display scale:** same final pixels or visual angle, necessary for readability.

A larger source image does not create additional readable detail after downsampling.

When physical presentation is known:

\[
\theta=2\arctan\left(\frac{w}{2z}\right)\frac{180}{\pi},
\qquad
\mathrm{pixels/degree}=\frac{W_{\mathrm{display\ pixels}}}{\theta},
\]

where physical displayed width \(w\) and viewing distance \(z\) use the same length units. Record assumptions; do not invent pixels/degree for unknown mobile viewing conditions.

**Low-resolution failure modes**

- Thin outlines and small highlights average away.
- Adjacent features merge.
- Fine patterns alias or shimmer across resize factors.
- Antialiasing reduces effective local contrast.
- JPEG ringing/blocking can inflate edges and entropy.
- Upscaled images can appear smooth but contain no recovered cue information.
- Learned models may resize or tile inputs internally, making their input scale different from the viewer’s.
- A coarse predicted map cannot reliably distinguish adjacent tiny targets.

Any proposed two- or three-pixel engineering margin for critical cues is a project rule to validate, not a universal perceptual threshold.

#### Validate learned predictions against behavior

If only image/model analysis is available, report:

> “The focal object has higher engineered contrast concentration and higher model-predicted fixation mass.”

Do not report:

> “Players will look at the focal object first.”

For a lightweight behavioral check:

- Randomize reference/candidate presentation order.
- Use independent viewers, not only the artist who knows the intended subject.
- Test the actual task and size.
- Predefine exposures, for example 200 ms, 500 ms, and 2 s; these are proposed experimental settings, not literature-derived game-art standards.
- Measure identification accuracy and confusion categories.
- Measure response time only under a consistent response protocol.
- Use separate participant/image splits if tuning feature thresholds.

A “click what you noticed first” task is a remembered report plus a motor response. It is **not** first-fixation measurement.

For eye tracking, record:

- Tracker sampling rate and calibration/validation error.
- Viewing distance, physical image size, and pixels/degree.
- Initial fixation procedure.
- Fixation segmentation/filtering.
- Whether the forced initial fixation is excluded.
- Task, duration, participant inclusion criteria.
- ROI definitions and uncertainty relative to ROI size.

Useful behavioral features:

\[
\mathrm{firstHit}_F=
\frac{\#\text{trials with first eligible fixation in }F}
{\#\text{eligible trials}},
\]

\[
\mathrm{dwellShare}_F=
\frac{\sum_{k:f_k\in F}d_k}
{\sum_kd_k},
\]

where \(d_k\) is fixation duration in milliseconds.

\[
\mathrm{TTFF}_F=\min_{k:f_k\in F}(t_k-t_{\mathrm{onset}}).
\]

Trials with no hit before presentation ends are **right-censored**, not assigned zero or silently discarded.

For attention flow between semantic ROIs:

\[
P_{ij}=
\frac{N(\mathrm{ROI}_t=i,\mathrm{ROI}_{t+1}=j)}
{\sum_jN(\mathrm{ROI}_t=i,\mathrm{ROI}_{t+1}=j)}.
\]

Report repeated fixations, returns, and duration separately. A desired primary→secondary sequence must be checked using sequences or time-conditioned data; a static saliency map contains no fixation order.

#### Saliency validation metrics

Given held-out fixations \(f_k\), normalized density \(p\), and baseline \(b\):

\[
IG=\frac1N\sum_k
\log_2\frac{p(f_k)}{b(f_k)}
\quad\text{bits/fixation}.
\]

Use regularization or a declared probability floor, then renormalize. Baselines must be fitted without test leakage.

For map \(q\):

\[
NSS=\frac1N\sum_k\frac{q(f_k)-\mu_q}{\sigma_q}.
\]

For unit-sum maps \(p,r\):

\[
SIM=\sum_x\min(p(x),r(x)),
\]

\[
KL(r\|p)=\sum_xr(x)\ln\frac{r(x)}{p(x)}.
\]

SIM is \([0,1]\); KL is in nats when using natural logarithms. CC is ordinary Pearson correlation over matching-grid map values, \([-1,1]\). Constant-map cases require explicit handling.

These definitions and the need to distinguish density from metric-specific map processing are supported by [S5](https://arxiv.org/html/1604.03605v2) and [S6](https://arxiv.org/html/1704.08615v2).

**Do not**:

- Call candidate/reference map similarity an accuracy score against human gaze.
- Compute fixation metrics without fixations and label the result behavioral validation.
- Compare raw log-density with unit-sum density.
- Compare heatmap colors after independent visualization normalization.
- Treat AUC alone as evidence of calibrated fixation probabilities.
- Ignore center bias or presentation-scale mismatch.

For DeepGaze log-density output, exponentiate and renormalize stably when computing ROI mass. Treat the supplied center bias as part of the model configuration, not a hidden implementation detail.

### Gaps

- No learned model was executed. CPU latency, memory, AMD/ROCm support, checkpoint integrity, and numerical reproducibility remain unverified.
- No model identified here is validated specifically for this project’s stylized casual-game references.
- DeepGaze repository licensing remains unresolved; public availability is not an affirmative commercial-use grant.
- TempSAL’s MIT root license versus CC BY-SA README notice requires artifact-specific clarification.
- DeepGaze3.5-VL’s non-commercial restriction makes it unsuitable as an assumed production default. Its repository’s “needs GPU” statement does not establish support for this workstation’s AMD GPU.
- Small-card first-fixation localization may be limited by eye-tracker error relative to target size.
- Free-viewing prediction does not establish visual-search or task-comprehension performance.
- No defensible universal participant count or readability threshold follows from the sources reviewed; determine study size from the intended inference and required precision.

## 3. How can measurements become prompt controls, reference-match evaluation, and corrective edits without unrelated drift?

### Takeaway

Use **role-conditioned, multiscale profiles**, not a single style score. Translate the largest supported mismatch into a localized edit while explicitly freezing content, geometry, palette identity, lighting direction, and rendering treatment that are already correct.

### Cited Findings

- Clutter measures can respond differently to contrast, orientation, color variability, and image structure; object count alone is an inadequate replacement. — [S2](https://jov.arvojournals.org/article.aspx?articleid=2122001).
- Task and semantic relevance affect viewing behavior independently of simple contrast ranking. — [S3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6690792/), [S4](https://authors.library.caltech.edu/records/ywkb0-v8462).
- Current saliency work explicitly models multiscale presentation and dataset bias, strengthening the case for scale-aware comparison rather than assuming one image-size-independent heatmap. — [S7](https://github.com/matthias-k/DeepGaze), [S8](https://openaccess.thecvf.com/content/ICCV2025/html/Kummerer_Modeling_Saliency_Dataset_Bias_ICCV_2025_paper.html).
- Static spatial saliency, next-fixation prediction, and time-sliced saliency are distinct outputs in the inspected implementations. — [S7](https://github.com/matthias-k/DeepGaze), [S10](https://github.com/Susmit-A/DeepGaze3.5-VL), [S12](https://ivrl.github.io/Tempsal/).

### Inferences

#### Separate subject/content from attention style

Use two parallel records.

**Content / nuisance record**

- Object and focal-group count.
- Object categories.
- Faces, eyes, readable text, and other potentially meaningful cues.
- Visible subject area.
- Occlusion.
- Pose/action.
- Camera and layout.
- Semantic task.
- Background category.

**Attention-style record**

- Contrast allocation by role and scale.
- Local focal/background separation.
- Edge sharpness allocation.
- Detail density by role.
- Fine/coarse frequency balance.
- Relative strength of primary, secondary, and decorative groups.
- Robustness across deployment sizes.
- Observed task performance, where available.

Do not lower object count to improve a “style” score while claiming the requested content was preserved. Likewise, do not penalize a many-item reward illustration for lacking single-object dominance if the reference task requires several readable items.

Prefer, in order:

1. Same content/layout, different renderings.
2. Matched pairs with similar subject categories and occupancy.
3. Role-conditioned reference distributions with recorded content covariates.
4. A larger statistical model only if the dataset justifies it.

For a larger dataset, a possible analysis is:

\[
y=
\beta_{\mathrm{style}}+
\beta_{\mathrm{count}}n+
\beta_{\mathrm{area}}a_F+
\beta_{\mathrm{faces}}n_{\mathrm{faces}}+
u_{\mathrm{content\ family}}+\epsilon.
\]

This is a proposed confound-control model, not a requirement or validated estimator. With a small reference collection, matched comparisons are more defensible than fitting many coefficients.

Raw pixelwise saliency-map comparison is appropriate mainly when content and layout are aligned. For different scenes, compare **semantic-role mass, enrichment, detail profiles, and rank relationships** instead.

#### Reference-match evaluation

For every reference and candidate, retain:

- Original image and deployment render.
- Masks and annotation confidence.
- Color conversion and resampling settings.
- Per-scale feature maps.
- Regional feature vector.
- Model/version/weights/license status if applicable.
- Human task results if available.

For feature \(k\), one possible robust reference distance is:

\[
z_k=
\frac{x_{k,\mathrm{candidate}}-
\operatorname{median}(x_{k,\mathrm{references}})}
{\max(1.4826\,MAD_k,\delta_k)},
\]

where:

\[
MAD_k=
\operatorname{median}
\left|x_{k,i}-\operatorname{median}(x_{k,\mathrm{references}})\right|,
\]

and \(\delta_k\) is a declared floor based on measurement stability or practical tolerance.

This is a proposed ranking aid. With few references, neither MAD nor the resulting \(z_k\) is a reliable population estimate.

Compare separate subprofiles:

1. Luminance hierarchy.
2. Chromatic hierarchy.
3. Edge hierarchy.
4. Regional detail allocation.
5. Small-size survival.
6. Learned predictions.
7. Behavioral outcomes.

Do not allow improvement in a speculative model score to compensate for a clear content violation or worse object recognition.

A weighted aggregate may prioritize inspection, but report the component changes and gates. Avoid presenting an arbitrary scalar as “87% style match.”

#### Prompt-ready controls

These are candidate instructions to test, not claims that image generators obey numerical constraints exactly.

| Measured issue | Concrete prompt language | What to hold fixed |
|---|---|---|
| Focal value contrast too weak | “Increase local light–dark separation between the [subject] and the immediately adjacent background; retain the existing hue families and overall exposure.” | Subject position/size, palette identity, lighting direction. |
| Background contrast competes | “Compress value variation and soften edge contrast in the background only; preserve the existing background objects and their placement.” | Object count, scene content, depth layout. |
| Excess chromatic competition | “Reserve the strongest chromatic accent for [focal role]; reduce saturation variation in secondary decorations without changing their base hues.” | Hue design, material identity. |
| Too much sharpness everywhere | “Keep the primary subject contour and identity-bearing features crisp; use softer transitions on distant/background details.” | Overall medium, outline design, object placement. |
| Fine detail overload | “Replace tiny background texture marks with broader grouped color shapes; preserve the large forms and all required objects.” | Content, silhouette, palette. |
| Subject internally busy | “Simplify decorative surface marks on the [subject], while preserving [specific identity cues], expression, and material shading.” | Identity, pose, key highlights. |
| Recognition fails after downsampling | “Strengthen the existing [eyes/handle/emblem] as a clear broad cue at small-card size; do not add new symbols or accessories.” | Meaning, design, count. |
| Unwanted secondary focal object | “Reduce the local brightness, saturation contrast, and micro-highlights of [competitor] only; keep it present and recognizable.” | Content and layout. |
| Flat subject after simplification | “Restore broad form shading and contact separation, without restoring microtexture or extra decorative marks.” | Detail budget, lighting direction. |
| Hue-only critical distinction | “Preserve the established colors, but reinforce the distinction using existing value and shape cues; do not introduce unrelated decoration.” | Brand/palette identity and semantics. |

A general control template:

> Preserve all objects, their count, identities, positions, scale, camera, pose, palette families, material treatment, and lighting direction. Modify only the attention hierarchy: make [primary role] carry the strongest local [value/chromatic/edge] contrast, keep [secondary role] subordinate, and reduce [specific detail type] in [specific mask]. Preserve [named identity-bearing cues]. Verify at [actual deployment size].

Avoid “make it cleaner,” “more readable,” or “add a focal point” without identifying the relevant mask and contrast/detail channel. Such phrases leave large freedom for unrelated drift.

#### Typical fixes, couplings, and failure checks

| Intervention | Intended effect | Common coupling / unintended drift | Recheck |
|---|---|---|---|
| Darken background behind subject | Increase value separation | Changes mood, depth, or apparent lighting | Local boundary contrast, global value distribution, reference lighting. |
| Brighten focal subject | Increase prominence | Clipping; loss of form; new material appearance | Highlight clipping, broad shading, small-size recognition. |
| Increase focal saturation | Increase chromatic distinction | Palette drift; CVD fragility; reduced value hierarchy | Chromatic and grayscale tests separately. |
| Add rim light/outline | Improve boundary readability | Sticker-like cutout appearance; rendering-style change | Boundary profile, outline width, reference edge treatment. |
| Blur background | Reduce competing edges | Photographic depth-of-field treatment unlike reference | Prefer simplified shapes/edges if references are sharply painted. |
| Reduce texture | Lower fine-band energy | Flat plastic surfaces; loss of material identity | Preserve broad shading and selected material cues. |
| Sharpen focal object | Increase edge hierarchy | Halos, ringing, excessive microdetail | Deployment render, high-frequency artifact map. |
| Remove a competing object | Reduce competition | Content violation | Reject as a style-only correction unless separately authorized. |
| Increase subject size or move it | Increase dominance | Geometry/content-layout drift | Outside this note’s control scope; flag rather than silently apply. |

Important couplings:

- Background simplification can improve focal contrast without changing subject pixels.
- Lowering saturation may or may not lower luminance contrast.
- Adding broad shading can improve form without increasing tiny-detail density.
- A brighter focal region may raise model-predicted saliency while making the intended object less recognizable.
- A new face or text label can change semantic attention independently of measured low-level contrast.
- Blur, outlines, and glows can achieve separation while departing strongly from reference rendering style.

#### Corrective loop

1. **Freeze the content contract.** Record required objects, identities, cues, and geometry.
2. **Measure reference profiles** at canonical and deployment scales.
3. **Measure candidate profiles** using the same settings.
4. **Inspect maps before interpreting numbers.** Determine whether extra energy is meaningful structure, texture, or an artifact.
5. **Identify the smallest supported mismatch.** Example: background fine-band energy is high, while focal boundary separation already matches.
6. **Issue one localized correction.** Example: simplify background microtexture, not “increase subject contrast.”
7. **Recompute target and guard features.**
8. **Check content and unrelated-style drift.** Use semantic review and unchanged-region inspection; pixel equality is not realistic for full regeneration.
9. **Run the relevant actual-size recognition check.**
10. **Stop when the target profile and task are adequate.** Do not chase maximum saliency or minimum entropy.

A useful edit specification has five fields:

```text
Target: background fine-scale detail only
Evidence: excess DoG fine-band energy and edge density at matched resolution
Change: group tiny marks into broader painted shapes
Freeze: objects, layout, palette families, materials, lighting, focal subject
Acceptance: closer regional detail profile; no loss of required content;
            no worse small-card identification
```

#### Minimal versus advanced stack

**Minimal, recommended first**

- Existing trusted image-processing tools; no new installation required by this note.
- Manual semantic masks.
- Declared color conversion and resampling.
- Regional luminance/chromatic/edge contrast.
- Edge density, DoG energy, local entropy.
- Thumbnail, blur, grayscale, silhouette, and CVD diagnostic renders.
- Small independent-viewer recognition checks.

This stack is CPU-suitable in principle because it consists of ordinary image operations; no runtime benchmark was performed.

**Intermediate**

- Pin and inspect spectral-residual implementation.
- Add feature congestion/subband entropy only if they explain a real mismatch.
- Add one legally usable learned saliency model.
- Report center-bias and presentation-scale sensitivity.
- Retain deterministic maps for correction attribution.

**Advanced**

- Eye-tracking validation on actual deployment conditions.
- Scale-aware saliency such as MSDB if licensing is clarified.
- Sequence-conditioned prediction or measured ROI transitions when temporal flow is genuinely relevant.
- Independent held-out images and observers.
- Optional model adaptation only when authorized data, tooling, licensing, and compute are available.

Do not introduce an 8B VLM scanpath stack merely to decide whether a background contains too many tiny highlights.

#### Current prior art and open opportunity

**Established prior art**

- Feature-based and spectral saliency.
- Clutter estimation through feature congestion and subband entropy.
- Semantic and task-dependent viewing.
- Probabilistic saliency evaluation with explicit bias treatment.
- Next-fixation and time-conditioned prediction.
- Scale/dataset-aware saliency modeling.
- VLM-based autoregressive scanpath prediction by 2026.

These are established components, not novel by themselves. — [S1–S13].

**Useful but unvalidated combination for this project**

A role-masked, cross-scale feature profile linked to a constrained edit vocabulary:

\[
\text{reference}
\rightarrow
\text{regional feature profile}
\rightarrow
\text{localized prompt control}
\rightarrow
\text{candidate}
\rightarrow
\text{same-profile comparison}
\rightarrow
\text{behavioral spot-check}.
\]

The contribution would be a validated workflow and dataset for stylized casual-game art, not the invention of saliency, entropy, or contrast analysis.

**Open gaps**

- Whether these regional descriptors predict expert judgments of reference-style match.
- Which features best predict actual-size object recognition for different game-art tasks.
- How reliably prompt instructions alter one feature without changing content or other style axes.
- How learned gaze models transfer to stylized, saturated, semantically unusual game assets.
- Which attention changes persist when cards appear among real UI and neighboring art.
- How to distinguish beneficial material detail from distracting microtexture automatically.
- Whether eye-tracking adds actionable information beyond task accuracy for each asset category.
- How robust the feature profile is to annotation uncertainty and production compression.

### Gaps

No project images were measured, no behavioral study was conducted, and no correction was tested. Numerical definitions above are reproducible proposals, **not validated project thresholds**. The parent must validate reference applicability and final synthesis.

#### Source register and claim mapping

All sources accessed **2026-10-31**. “High confidence” refers to the attributed source claim or inspected implementation, not automatic transfer to casual-game art.

| ID | Primary source | Main claim mapping / confidence |
|---|---|---|
| **S1** | [OpenCV official spectral-residual implementation](https://github.com/opencv/opencv_contrib/blob/5.x/modules/saliency/src/staticSaliencySpectralResidual.cpp) | Exact implementation, 64×64 default, grayscale/frequency operations. **High**. Inspected file carries its own permissive BSD-style notice; preserve applicable notices rather than relying solely on repository-level license metadata. |
| **S2** | [Rosenholtz, Li & Nakano, “Measuring visual clutter,” 2007](https://jov.arvojournals.org/article.aspx?articleid=2122001) | Feature congestion, subband entropy, edge density, target-discriminability dependence. **High** for attributed published findings; accessible extraction exposed mainly figures/captions. |
| **S3** | [Peacock, Hayes & Henderson, “The Role of Meaning in Attentional Guidance during Free Viewing of Real-world Scenes,” 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6690792/) | Meaning versus GBVS; experimental method and early-fixation results. **High**, with comparator/domain limitations. |
| **S4** | [Einhäuser, Rutishauser & Koch, task-demand experiment, 2008](https://authors.library.caltech.edu/records/ywkb0-v8462) | Task can override/reverse contrast-driven viewing bias. **High** for reported experiment. |
| **S5** | [Bylinskii et al., “What do different evaluation metrics tell us about saliency models?”](https://arxiv.org/html/1604.03605v2) | Metrics, smoothing, presentation setup, center bias, probabilistic versus intensity maps. **High**. |
| **S6** | [Kümmerer, Wallis & Bethge, “Saliency Benchmarking Made Easy”](https://arxiv.org/html/1704.08615v2) | Separation of density, derived map, and metric; metric-specific transformations. **High**. |
| **S7** | [Official DeepGaze repository](https://github.com/matthias-k/DeepGaze) | IIE/III/MSDB behavior, center-bias input, scaling notes, pixels/degree, current release pointers. **High** for documentation; runtime untested. |
| **S8** | [Kümmerer, Khanuja & Bethge, “Modeling Saliency Dataset Bias,” ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Kummerer_Modeling_Saliency_Dataset_Bias_ICCV_2025_paper.html) | Dataset transfer, multiscale/bias adaptation, author-reported benchmark results. **High** attribution; no independent project validation. |
| **S9** | [“DeepGaze3.5-VL: Modeling Scanpaths via Autoregressive Token Prediction,” 2026](https://arxiv.org/abs/2607.02083) | Current VLM scanpath prior art and reported benchmark performance. **High** attribution; paper’s performance claims not independently reproduced. |
| **S10** | [Official DeepGaze3.5-VL repository](https://github.com/Susmit-A/DeepGaze3.5-VL) | Architecture, adapters, target categories, coordinate grid, GPU workflow. **High**. [License](https://github.com/Susmit-A/DeepGaze3.5-VL/blob/master/LICENSE) confirms non-commercial research restriction. |
| **S11** | [Official TempSAL repository](https://github.com/IVRL/Tempsal) | Available workflow and aggregate/time-sliced predictions. **High** documentation confidence. [MIT root license](https://github.com/IVRL/Tempsal/blob/main/LICENSE) conflicts with README’s CC BY-SA notice; clearance unresolved. |
| **S12** | [TempSAL official supplementary material](https://ivrl.github.io/Tempsal/) | Static-image time slices and approximate fixation timestamp recovery. **High**. |
| **S13** | [Jiang et al., “SALICON: Saliency in Context,” CVPR 2015](https://openaccess.thecvf.com/content_cvpr_2015/html/Jiang_SALICON_Saliency_in_2015_CVPR_paper.html) | Mouse-contingent rather than hardware-eye-tracking collection. **High**. |
| **S14** | [W3C WCAG 2.2 Understanding Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | 3:1 scope, exceptions, adjacent colors, thin/antialiased graphics, relative-luminance definition. **High**, within web-accessibility scope. |
| **S15** | [Machado, Oliveira & Fernandes, CVD simulation project/paper materials](https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html) | Physiological simulation, severity matrices, validation, erratum. **High** for documented method; individual experience remains variable. |

**Corroboration:** task/semantic limitations are supported by independent experimental sources S3/S4; representation/metric cautions by S5/S6; scale/domain-transfer cautions by S7/S8. Implementation/license assertions were checked against official repositories and license text rather than search snippets.

**Research validation and limitations:** the original Hou PDF could not be retrieved reliably, so exact spectral-residual claims above rely on inspected official OpenCV code, not an asserted reproduction of the original paper. An MIT clutter-project page had a certificate problem; its published journal source was used instead. Incorrect/obsolete guessed URLs were discarded after discovery of canonical records.

**Material research spend:** 16 subscription-backed Kagi searches, three GitHub code searches, 27 web-fetch requests, and nine public GitHub repository/license/commit diagnostics. No Perplexity, Deep Research, Kagi Assistant, software installation, checkpoint download, model execution, private upload, or file modification.
