# Lighting and value: measuring, specifying, evaluating, and correcting collectible-card images

**Research cutoff and access date:** 2026-10-31.  
**Scope:** lighting, shadows, luminance, exposure, contrast, and value only.  

**Project context:** the brief requires reference-compatible collectible-object artwork, consistent sets, autonomous generation, and explicit comparison against references. The art guide distinguishes floating objects, objects resting on surfaces, and objects within environments. Consequently, **contact shadows are category-dependent**, not universally required. These are requirements from the locally inspected `materials/01_task_description.md` and `materials/03_art_guide.md`, not conclusions extracted from reference images.

**Evidence labels used below:**

- **Established:** standards, mathematical results, or documented implementation behavior.
- **Published empirical:** findings reported by a paper’s authors under their evaluation conditions.
- **Documented capability:** an official repository or manual describes the feature; it was not executed here.
- **Proposed:** a project-specific measurement, specification, or workflow requiring validation.
- **Unknown:** not established by the inspected evidence.

**Central conclusion — high confidence:** build a deterministic **image-appearance measurement system**, not a purported physical-lighting detector. Use explicit lighting descriptions and, where available, renderer or relighting controls. Treat recovered normals, depth, shading, materials, and illumination as **conditional estimates**, not ground truth. A single flattened stylized image generally does not uniquely determine the scene that produced it. [S1–S6, S14–S21]

---

## 1. What do lighting and value terms mean, and which quantities can one flattened image actually reveal?

### Takeaway

Separate **lighting roles**, **source directions**, **source geometry**, **image tonal organization**, and **historical style descriptions**. These are related but not interchangeable. A flattened image permits reproducible measurements of its pixels; it does not generally permit unique recovery of its original lights, materials, geometry, exposure, or rendering pipeline. [S1–S10]

### Cited findings

#### 1.1 Lighting roles are not directions

The following is an operational vocabulary for the project. Key/fill terminology is consistent with the inspected filmmaking reference; physical light types and size controls are documented by Blender and PBRT. The project should preserve these distinctions explicitly in its schema. [S5, S6, S9]

| Term | Meaning for a specification | Prompt-ready wording | Do not equate it with |
|---|---|---|---|
| **Key light** | Principal illumination responsible for the intended form modeling or dominant light/shadow organization | “A dominant broad key models the object from the upper left.” | A particular direction; an overhead light; the brightest visible pixel |
| **Fill** | Illumination that opens shadow regions; may come from a fixture, sky, bounce, or surrounding environment | “Gentle frontal fill keeps the shadow side readable.” | Necessarily a second lamp; global brightness |
| **Rim light** | A narrow illuminated boundary that separates a silhouette from its surroundings | “A restrained rim along the upper-right silhouette.” | A required light on every edge; a white outline |
| **Backlight** | A source located behind the subject relative to the camera | “A soft rear light separates the object from the background.” | Guaranteed visible rim; background lighting |
| **Background light** | Illumination primarily affecting the background | “Keep the background softly illuminated without increasing the subject’s highlights.” | Backlight on the subject |
| **Practical** | A visible, diegetic light fixture or luminous object within the depicted scene | “The visible lamp motivates the local pool of illumination.” | Necessarily the dominant real illumination source |
| **Ambient/environment illumination** | Broad illumination arriving from the surroundings, potentially directional and spatially varying | “Broad environmental fill; no strongly isolated secondary shadow.” | A single uniform scalar in the original scene |
| **Negative fill** | Reduction of surrounding bounce or fill, rather than emission of “negative light” | “Reduce fill on the right side while retaining the existing key direction.” | A black source or a global contrast filter |

**Directions** form a separate vocabulary:

- **Front:** illumination arrives approximately from the camera side.
- **Side:** approximately lateral to the viewing direction.
- **Overhead/top:** high elevation.
- **Underlight:** negative elevation.
- **Rear/back:** behind the subject relative to the camera.
- **Three-quarter:** an explicitly intermediate direction; specify which side and whether front or rear.

A source can simultaneously be **key + side + high elevation + large apparent size**. “Key,” “side,” and “soft” therefore belong in different fields. Blender’s physical source types—point, spot, area, sun—are another separate classification. [S5, S9]

#### 1.2 Declare coordinate conventions instead of assuming universal angle meanings

**Proposed project convention:** describe a source direction from the subject **toward the source**, in camera-relative coordinates:

- \(x\): image right;
- \(y\): image up;
- \(z\): toward the camera;
- azimuth \(a=0^\circ\): frontal, toward the camera;
- \(a=+90^\circ\): image right;
- \(a=-90^\circ\): image left;
- \(a=\pm180^\circ\): behind the subject;
- elevation \(e=0^\circ\): horizontal;
- \(e=+90^\circ\): directly overhead.

A compatible unit vector is

\[
\mathbf l(a,e)=
(\cos e\sin a,\;\sin e,\;\cos e\cos a).
\]

Angles must be converted consistently to radians for numerical trigonometry.

This is a **chosen control convention**, not something extracted unambiguously from the artwork. A renderer may use a different world axis, rotation order, or light-emission direction; an adapter must translate between conventions. Blender documents source-dependent direction behavior, making the distinction practically important. [S5]

For screen-space shadow measurements, use a separately declared image-plane convention. For example, with image coordinates increasing downward:

\[
\theta_{\rm image}=\operatorname{atan2}(-\Delta y,\Delta x).
\]

This gives \(0^\circ\) right and \(90^\circ\) up. It is a **2D direction**, not a recovered 3D light azimuth.

#### 1.3 Apparent emitter size, softness, and penumbra are related but not identical

Blender documents larger light-source size as producing softer shadows, while PBRT explains area-light illumination through integration over the emitter. PBRT’s examples also show that increasing source extent changes body shading and highlight appearance—not only shadow boundaries. [S5, S6]

For a centered, face-on circular emitter of diameter \(D\), viewed from distance \(d\), its angular diameter is

\[
\theta=2\arctan\left(\frac{D}{2d}\right).
\]

- \(D,d\): matching length units.
- \(\theta\): radians, or converted to degrees.
- **Verdict:** computable when geometry is known; not uniquely recoverable from a painted shadow.

Useful distinctions:

| Quantity | Meaning | Main confounders in a flattened image |
|---|---|---|
| **Physical emitter size** | Length/area of the source | Source distance and orientation |
| **Apparent/angular size** | Source extent seen from a shaded point | Position on the object, occlusion |
| **Penumbra** | Partial-visibility transition between illuminated and occluded regions | Blocker–receiver distance, emitter shape, multiple sources |
| **Observed edge softness** | Measured image transition width | Penumbra plus painting, antialiasing, blur, resampling, bloom, compression |
| **Form-shading softness** | Gradual tonal change across the object | Geometry, material, lighting distribution, painted gradients |
| **Spot-beam edge softness** | Transition at a spotlight’s illumination footprint | Not the same as cast-shadow softness |

A particularly useful official warning: Blender states that spotlight **Blend/Size affect the beam boundary, not object-shadow softness**. Changing spotlight falloff is therefore not equivalent to enlarging the emitter. [S5]

**Conditional geometric illustration:** for a simple parallel-plane arrangement, source diameter \(D\), source–receiver separation \(L\), and blocker height \(h\), geometric penumbra width scales approximately as

\[
w_{\rm penumbra}\approx \frac{Dh}{L-h}.
\]

This is a simplified geometric relationship, not a fitting formula for arbitrary artwork. It also does **not** say that a measured 10–90% image-transition width equals the full geometric penumbra width. Its role here is to demonstrate the ambiguity: similar softness can arise from different source sizes and blocker distances. [S6; proposed geometric illustration]

#### 1.4 Shadow vocabulary

Use separate fields for:

- **Cast shadow:** projected onto another receiving surface.
- **Attached/form shadow:** the unilluminated or less illuminated region on the object itself.
- **Contact region:** the local meeting or near-meeting of object and receiver.
- **Penumbra:** partial occlusion of an extended source.
- **Occlusion darkening:** reduced access to surrounding illumination; not automatically a direct-light shadow from one named source.
- **Painted grounding shadow:** an image-space convention that may imitate contact without representing consistent physical geometry.

The last distinction is essential for stylized cards: a small oval under an object may be an intentional graphic grounding device, not evidence from which to reconstruct a light. Area-light shadow formation is established; interpretation of an individual stylized mark remains conditional. [S6; inference]

**Prompt-ready descriptions:**

- “A short, soft cast shadow falls down-right on the receiving plane.”
- “The shadow begins at the contact point, with no detached dark halo.”
- “Retain a compact grounding shadow; do not create a long environmental shadow.”
- “Floating object: no surface contact shadow.”
- “Keep contact darkening restrained and distinct from the object’s outline.”

These are proposed controls, not claims about the uninspected visual references.

#### 1.5 Key-to-fill ratios: specify the convention and the measured quantity

Two commonly encountered definitions differ:

\[
r_{\rm source}=\frac{K}{F}
\]

versus

\[
r_{\rm sides}=\frac{K+F}{F}=r_{\rm source}+1.
\]

The second assumes, approximately, that fill reaches both sides while key contributes mainly to the lit side. Both conventions were explicitly documented in the inspected sources. [S9, S10]

For separately measured contributions:

\[
\Delta_{\rm sources}=\log_2(K/F).
\]

For the simplified lit-side/shadow-side ratio:

\[
\Delta_{\rm sides}=\log_2((K+F)/F).
\]

Example:

- \(K/F=4\): source contributions differ by **2 stops**.
- \((K+F)/F=5\): simplified sides differ by approximately **2.32 stops**.

Therefore, “4:1 lighting” is underspecified.

**What should \(K\) and \(F\) mean?** Prefer separately measured incident contributions at a declared subject location and orientation, or explicitly defined renderer contributions. Do not silently substitute lamp watts, dimmer percentages, source radiance, or sampled image brightness: geometry and transport intervene. Blender documents distance-dependent illumination and size/power normalization behavior; the community ratio descriptions are useful evidence of terminology, not guarantees that fixture power equals incident contribution. [S5, S9, S10]

A pixel ratio between two object patches additionally depends on their reflectance, orientation, specularity, occlusion, rendering, and grading. It should be labeled **image-patch luminance ratio**, not “measured key-to-fill ratio.” [S4–S6, S14]

#### 1.6 High/low key, contrast, and exposure are different axes

For this project, use these operational distinctions:

- **High-key image appearance:** much of the relevant image region occupies light values.
- **Low-key image appearance:** much occupies dark values.
- **Contrast:** separation or variation among values, under a declared statistic and spatial scale.
- **Exposure:** a physical capture variable or a specified image/render scaling operation—not a synonym for mean pixel brightness.

Photographic terminology varies. The inspected Fstoppers article explicitly discusses disagreement over strict definitions and ultimately favors a predominance-based interpretation. It is an opinion-based community source, **not a standard establishing a 50% histogram threshold**. Its useful contribution is documenting that these labels are contested and should not replace measurements. [S11]

A bright background with a dark subject can have a high overall median and substantial subject/background contrast. A predominantly dark image can retain strong small highlights. Consequently, store **tonal placement and contrast separately** rather than encoding “high key” as “low contrast.” [S1, S11; proposed measurement convention]

Blender defines a light’s exposure parameter as multiplication by \(2^{\rm exposure}\). That is an explicit control operation. It does not justify recovering an original camera exposure from the final PNG. [S5]

#### 1.7 Relative luminance, luma, perceptual lightness, and “value”

**Linear-light relative luminance.** For normalized sRGB channel values \(c'\in[0,1]\), decode:

\[
c=
\begin{cases}
c'/12.92,&c'\le0.04045\\
((c'+0.055)/1.055)^{2.4},&c'>0.04045.
\end{cases}
\]

Then:

\[
Y=0.2126R+0.7152G+0.0722B.
\]

This is the W3C sRGB-relative-luminance computation. \(Y\) is dimensionless relative to the encoding’s reference white. [S1]

**Critical qualification:** decoding a flattened sRGB image gives a **linear-light representation of its rendered/display-referred values**. It does not undo tone mapping, recover scene radiance, reverse artistic grading, or make the result scene-linear HDR. [S1, S2, S19–S21; inference]

**Encoded-channel luma/luma-like grayscale.** A weighted sum of nonlinear encoded channels is not the same calculation:

\[
Y'_{\rm weighted}=w_RR'+w_GG'+w_BB'.
\]

The weights and transfer function must be named. A weighted sum of sRGB-encoded channels should not be casually identified with a complete Rec.709 video-luma pipeline.

**Verified implementation trap:** inspected `scikit-image` source implements `rgb2gray` as:

```python
rgb = _prepare_colorarray(rgb)
coeffs = np.array([0.2125, 0.7154, 0.0721], dtype=rgb.dtype)
return rgb @ coeffs
```

There is no sRGB decoding in this function. On encoded sRGB input, this is therefore not the W3C linear-light \(Y\), despite documentation using the word “luminance.” [S12]

**CIELAB perceptual lightness.** With \(t=Y/Y_n\):

\[
L^*=116f(t)-16,
\]

\[
f(t)=
\begin{cases}
t^{1/3},&t>(6/29)^3\\
t/[3(6/29)^2]+4/29,&\text{otherwise}.
\end{cases}
\]

- \(Y_n\): declared reference-white luminance in matching relative units.
- \(L^*\): lightness units, typically 0–100 for ordinary reference-relative SDR values.
- This is a perceptual lightness correlate, not a direct measurement of subjective brightness under every viewing condition.

Colour implements the CIE 1976 lightness relationship; `scikit-image.rgb2lab` documents its sRGB input assumptions and reference illuminant/observer. [S12, S13]

**“Value.”** In art discussion, use “value” as an umbrella for light–dark organization, then name the numerical operationalization: \(Y\), \(L^*\), encoded grayscale, or another declared quantity. Do not silently use HSV “V” as luminance: its channel-maximum definition is a different construct.

**Absolute luminance and exposure.** Physical luminance is expressed in \(\mathrm{cd/m^2}\), commonly “nits.” A normalized image channel is not a nit measurement. Conversion requires a specified display/output mapping and calibration; original scene luminance and capture exposure require further information. The inspected W3C sources support normalized relative colorimetry and distinguish physical emitted/reflected color from encoded representations; they do not supply a universal PNG-to-nits conversion. [S1, S2]

#### 1.8 Chiaroscuro and tenebrism are historical descriptions, not numeric light parameters

Tate defines chiaroscuro as the balance and pattern of light and shade, usually remarked upon when contrasts are especially prominent. The National Gallery describes tenebrism as important details illuminated against a predominantly dark setting. Neither definition specifies an azimuth, emitter diameter, exposure value, or key-to-fill ratio. [S7, S8]

Translate these labels into an operational description before generation:

- **Chiaroscuro-like:** “pronounced light–dark modeling of the main form; deliberate separation of illuminated and shadowed masses.”
- **Tenebrist organization:** “predominantly dark surroundings, with selected important details isolated in light.”

Do not automatically append either term to a collectible-card prompt: it can introduce dark backgrounds, dramatic storytelling, or historical-painting associations beyond the requested lighting correction. [S7, S8; proposed control caution]

#### 1.9 Why one image cannot determine the physical lighting

Belhumeur, Kriegman, and Yuille establish a generalized bas-relief ambiguity: under their Lambertian, orthographic, distant-light assumptions, transformed geometry, albedo, and lighting can produce identical images. Their abstract explicitly includes cast and attached shadows in the ambiguity result. This is stronger evidence than merely observing that a neural model sometimes makes errors. [S4]

Even a simplified intrinsic model illustrates ambiguity:

\[
I(x)=A(x)S(x).
\]

For positive \(c\),

\[
I(x)=(cA(x))(S(x)/c).
\]

Without additional constraints, reflectance and shading scale are not uniquely determined. More realistic images include specular, emissive, transmission, indirect-light, and postprocessing terms. The inspected Intrinsic and PIXLRelight work explicitly model or discuss some of these additional components and the limitations of coarse reconstruction. [S14, S19–S21]

A model can produce the same answer repeatedly and still select only one plausible explanation among many.

### Inferences

**Recommended specification split:**

1. **Observed appearance:** “left side lighter,” “broad soft shadow,” “background median lower than subject.”
2. **Interpretation with confidence:** “consistent with a large upper-left key.”
3. **Desired control:** “use a large upper-left key with readable shadow-side fill.”

This avoids turning an uncertain explanation into a falsely measured physical fact.

For each inferred light direction, retain a confidence label or interval and the supporting cues. Conflicting highlights, cast shadows, and form shading may reflect multiple lights, materials, or intentional stylization; do not force a single-light explanation.

### Gaps

- No visual reference images were analyzed in this lane; no project-specific light direction, tonal threshold, or target ratio has been established.
- Original lighting roles and source count are generally not uniquely recoverable from one flattened stylized image.
- Source size, source distance, physical light ratio, actual exposure, scene luminance, and display nits require additional assumptions or calibration.
- Historical labels and high-/low-key terminology have no universal numerical mapping suitable for automatic compliance tests.

---

## 2. Which features and tools are usable, and what does each measurement actually establish?

### Takeaway

A practical baseline can deterministically measure **rendered tonal distributions and spatial relationships** on CPU. Semantic measurements require masks or annotations. Intrinsic decomposition, normal/depth estimation, inverse lighting, and learned relighting are optional model-dependent layers with important licensing and deployment constraints. [S1–S6, S12–S23]

### Cited findings

#### 2.1 Preprocessing contract

The following is a **proposed project measurement contract**, grounded in the color-space requirements documented by W3C, Colour, and `scikit-image`. It must be identical for references and generated candidates. [S1, S2, S12, S13]

1. **Declare the analyzed asset.**
   - Analyze artwork rather than the card frame, UI, labels, or rarity border.
   - Preserve the original alongside the analysis crop.
   - Record crop and output dimensions.

2. **Resolve color encoding.**
   - Honor an embedded ICC profile where available.
   - Convert to a declared common space, preferably sRGB for SDR delivered assets.
   - If untagged, record an explicit sRGB assumption rather than treating it as known.

3. **Handle transparency intentionally.**
   - Transparent RGB can contain arbitrary values and must not contribute as visible pixels.
   - Distinguish straight from premultiplied alpha.
   - For appearance on a background, composite against the declared background in a consistent linear-light workflow.
   - For object-intrinsic image statistics, use a declared opacity/coverage rule and an interior mask.

4. **Produce separately named channels.**
   - Encoded RGB \(R',G',B'\).
   - Decoded linear-light RGB.
   - Relative luminance \(Y\).
   - CIELAB \(L^*\), with reference white and conversion implementation recorded.

5. **Define regions.**
   - Whole artwork.
   - Subject.
   - Subject interior, optionally eroded to exclude outline/antialiasing.
   - Background.
   - Receiving surface.
   - Shadow, highlight, or material patches only when reviewed annotations exist.

6. **Standardize scale.**
   - Report spatial widths both in pixels and normalized to image size or subject bounding-box diagonal.
   - Use common analysis resolutions for multiscale metrics.
   - Record resampling and smoothing choices.

7. **Preserve the display transform.**
   - Do not independently auto-expose or histogram-normalize every reference before measuring tonal placement.
   - If exposure-normalized comparison is additionally useful, report it as a second analysis, not a replacement for delivered appearance.

8. **Record provenance.**
   - Asset identifier, color assumption, masks, thresholds, analysis scale, code version, and estimator/checkpoint identifiers.
   - No external upload is necessary for baseline measurements.

**Important limitation:** a deterministic measurement conditional on a learned mask still inherits mask error. Report both the deterministic calculation and the conditional nature of the region selection.

#### 2.2 Feature verdict legend

- **D — Direct deterministic pixel measurement:** reproducible from the declared image/preprocessing; no claim of physical-light truth.
- **C — Conditional:** deterministic after masks, landmarks, calibration, or a scene model are supplied.
- **L — Learned proxy:** depends on trained priors; output is an estimate.
- **N — Not identifiable:** cannot generally be uniquely determined from one flattened image.

A feature can have a deterministic appearance measurement and a non-identifiable physical interpretation.

#### 2.3 Measurable-feature catalogue

All formulas below are explicit proposed project definitions unless identified as a standard formula. They are not published thresholds for collectible-card style.

Let \(M\) be an analysis region, \(N=|M|\), \(Y_i\) its relative-luminance samples, and \(Q_p\) their \(p\)-quantile.

| Feature | Exact definition / units | Verdict | What it establishes; limitations |
|---|---|---|---|
| **Relative-luminance distribution** | Histogram/CDF of W3C \(Y\), plus \(Q_{05},Q_{10},Q_{50},Q_{90},Q_{95}\). Dimensionless, normally 0–1 for SDR | D; C for semantic regions | Delivered tonal placement. Not source illumination or exposure. [S1] |
| **Lightness distribution** | Same summaries of CIELAB \(L^*\). Lightness units | D/C | Perceptually motivated tonal organization under declared conversion; not universal subjective brightness. [S12, S13] |
| **Mean luminance** | \(\mu_Y=N^{-1}\sum_iY_i\) | D/C | Average rendered value; strongly affected by subject area, background, palette, and crop |
| **Tonal spread** | \(Q_{90}-Q_{10}\), or separately \(Q_{95}-Q_{05}\) | D/C | Robust global spread; ignores spatial arrangement |
| **RMS contrast** | \(\sigma_Y=\sqrt{N^{-1}\sum_i(Y_i-\mu_Y)^2}\) | D/C | Variation at the chosen domain and scale; material texture and outlines contribute |
| **Normalized RMS contrast** | \(\sigma_Y/\max(\mu_Y,\epsilon)\); report \(\epsilon\) | D/C | Relative variation; unstable for dark regions and not interchangeable with RMS contrast |
| **Percentile luminance ratio** | \(r_Y=Q_{90}/Q_{10}\), only when denominator is above a declared floor | D/C | Image-distribution ratio, **not key-to-fill ratio** |
| **Percentile log-range** | \(\Delta_Y=\log_2(Q_{90}/Q_{10})\), with validity floor | D/C | Stops-like description of rendered luminance range; not capture dynamic range or lamp ratio |
| **Dark/mid/light occupancy** | Fractions below/within/above declared \(Y\) or \(L^*\) thresholds | D/C | Useful value-group signature. Thresholds must be learned from references or chosen explicitly |
| **Endpoint occupancy** | Fraction of pixels/channels at or near encoding minimum/maximum; specify “any channel” versus luminance | D/C | Output endpoint use. Does not prove sensor clipping or lost original HDR detail |
| **Subject/background separation** | \(\Delta L^*=\operatorname{median}(L^*_{\rm subject})-\operatorname{median}(L^*_{\rm background})\) | C | Region value separation, not perceived separation in every local neighborhood |
| **Local silhouette separation** | Median signed/absolute \(L^*\) difference between paired inside/outside boundary bands | C | More local than whole-region medians; depends on masks and band width |
| **Spatial value field** | Median \(Y\) or \(L^*\) in a declared grid, e.g. subject-relative cells | D/C | Preserves coarse placement lost by histograms; geometry and material markings remain confounders |
| **Multiscale local contrast** | Local standard deviation or residual \(|Y-G_\sigma*Y|\), aggregated at declared normalized scales | D/C | Distinguishes broad modeling from fine tonal variation; neither component is uniquely “lighting” |
| **Bright-region area** | Area where \(Y>t\), or reviewed highlight-mask fraction | D or C | Bright-pixel coverage; a fixed threshold is not a specularity detector |
| **Bright-region centroid** | \(\sum_iw_i(x_i,y_i)/\sum_iw_i\), with declared \(w_i\), e.g. \(\max(Y_i-t,0)\) | D/C | Where brightness is concentrated; not light position |
| **Shadow coverage** | Reviewed shadow-mask area divided by receiving-surface or subject area | C; L if mask predicted | Depends on what counts as cast shadow rather than dark material, outline, or pattern |
| **Shadow displacement/direction** | Vector from annotated contact/anchor point to a declared shadow landmark or centroid; px, normalized length, degrees | C | Screen-space shadow organization. Perspective and object shape prevent direct 3D inference |
| **Contact gap** | Declared distance between object contact landmark and beginning of its associated shadow | C | Flags detached grounding under appropriate categories; not required for floating objects |
| **Observed shadow-edge width** | 10–90% transition distance across reviewed shadow boundaries; px and normalized width | C | Image-edge softness, not uniquely emitter size |
| **Matched-patch shadow attenuation** | \(a=\operatorname{median}(Y_{\rm shadow})/\operatorname{median}(Y_{\rm lit})\) for comparable receiver material | C | Rendered attenuation only; requires comparable material and geometry |
| **Form-shading amplitude** | Quantile range or fitted low-frequency variation within a reviewed approximately uniform-material patch | C | A conditional appearance measure; albedo changes, curvature, and specularities confound |
| **Rim coverage/width** | Reviewed luminous-boundary length divided by silhouette length; band width normalized to subject size | C; L if detected | Rim-like appearance, not proof of a rear lamp |
| **Source azimuth/elevation** | Physical direction estimate from a declared model | L/C; generally N without assumptions | Must report scene assumptions and uncertainty |
| **Emitter angular/physical size** | \(\theta=2\arctan(D/(2d))\) when geometry known | C; generally N from flat image | Observed softness alone does not identify it |
| **Physical K/F ratio** | Separately measured contributions under a declared convention | C with calibration; N from arbitrary artwork | Cannot substitute arbitrary bright/dark pixel ratios |
| **Original exposure / scene luminance / display nits** | Physical quantities requiring capture/render/display information | N from an ordinary uncalibrated flattened image | Image statistics remain valid, but do not supply these physical quantities |

The physical-interpretation limitations follow from image-formation ambiguity, documented area-light behavior, and learned decomposition/reconstruction assumptions. [S4–S6, S14–S21]

#### 2.4 A reproducible shadow-softness procedure

**Proposed conditional algorithm:**

1. Annotate a cast-shadow boundary on a reasonably uniform receiving surface.
2. Exclude corners, texture changes, contact zones, overlapping shadows, and specular patches.
3. Sample short profiles normal to the boundary.
4. Estimate local lit and shadow baselines \(Y_{\rm lit}\) and \(Y_{\rm sh}\).
5. Normalize each profile:

\[
t(s)=\frac{Y(s)-Y_{\rm sh}}{Y_{\rm lit}-Y_{\rm sh}}.
\]

6. Find positions where the transition crosses 0.1 and 0.9.
7. Record

\[
w_{10-90}=|s_{0.9}-s_{0.1}|.
\]

8. Aggregate using median and interquartile range; retain the number and location of valid profiles.
9. Report both pixels and \(w_{10-90}/d_{\rm subject}\).

Reject profiles with insufficient contrast or strong non-monotonicity rather than forcing an answer.

**Interpretation:** this measures the delivered edge transition. Physical penumbra, brush softness, blur, and resampling all contribute. PBRT and Blender support the source-size/soft-shadow relationship, but neither licenses the inverse conclusion “measured width uniquely gives emitter size.” [S5, S6]

A universal thresholding method cannot reliably tell every painted shadow from every dark material patch. A deterministic threshold can be useful **after** the region and task are constrained; that is not a universal shadow-understanding tool. [S4, S14; inference]

#### 2.5 Spherical harmonics: useful representation, not automatic truth

Ramamoorthi and Hanrahan study diffuse objects under distant environment illumination. Their low-frequency spherical-harmonic approximation uses nine coefficients through degree two; the paper reports approximately 1% average error under its studied conditions. [S3]

A representation is

\[
L(\omega)\approx
\sum_{\ell=0}^{2}\sum_{m=-\ell}^{\ell}
c_{\ell m}Y_{\ell m}(\omega).
\]

Important qualifications:

- Nine coefficients are **per scalar channel**; RGB lighting normally means 27 scalar coefficients.
- The useful diffuse irradiance approximation exploits low-pass behavior of Lambertian reflection.
- It does not encode every sharp cast shadow, localized near light, specular reflection, or spatially varying illumination effect.
- Computing coefficients from a known environment map is a forward analytical operation.
- Estimating them from one unknown stylized object is an inverse problem involving uncertain normals, reflectance, visibility, and scale.
- Coefficient signs, normalization, ordering, coordinate frame, and RGB/white conventions must match before comparison.
- The reported 1% is not a universal accuracy guarantee for inverse lighting or stylized cards. [S3, S4]

**Project role:** SH can be a compact advanced control or diagnostic for broad diffuse illumination. It is a poor replacement for explicit shadow geometry and cannot establish original light count or original K/F ratio.

#### 2.6 Tool and repository matrix

**Verification level:** documentation, source snippets, repository roots, license texts, and default-branch commit metadata were inspected. No repository code or model inference was executed. Dates below describe inspected repository state, not a maintenance guarantee.

| Tool / source | Actual useful role | License and pretrained dependency | CPU / AMD assessment | Maintenance / limits |
|---|---|---|---|---|
| **scikit-image** [S12] | Color conversion, filtering, morphology, region measurements; supports deterministic appearance analysis | Predominantly BSD-3-Clause, with per-file notices including BSD-2-Clause components. No pretrained model required for these operations | CPU baseline; GPU not necessary | Default-branch commit inspected: **2026-10-30**. Do not treat `rgb2gray(encoded_sRGB)` as decoded luminance. Pin the package/API version |
| **Colour** [S13] | Explicit transfer functions, color-space conversion, CIE lightness calculations | BSD-3-Clause; no pretrained dependency for these calculations | CPU baseline sufficient | Inspected develop commit **2026-10-27**; repository pushed **2026-10-29**. Domain/range and white-point conventions still need configuration |
| **Blender / Cycles** [S5, S22, S23] | Author known geometry, light positions/types/sizes, and render passes; controlled experiments or conditioning renders | Blender distribution GPL; Cycles component Apache-2.0. No pretrained model required for conventional rendering. Blender states artwork can be used commercially | CPU rendering available. Official manual supports HIP on Linux and RX 7000-series hardware; actual workstation configuration was **not tested** | Current official manual inspected. Provides known control values in an authored scene, not recovered original scene truth |
| **PBRT area-light implementation / textbook** [S6] | Analytical reference for light transport and area-light/shadow behavior | Implementation license not separately audited here; textbook used as evidence, not selected as a deployable package | No project deployment assessed | Strong conceptual source; not an automatic image-analysis service |
| **compphoto/Intrinsic** [S14] | Learned albedo, diffuse shading, and residual decomposition; 2023/2024 research implementation | **Academic use only** license; patent warning. Requires pretrained models. Not an unrestricted production dependency | Official CPU/AMD deployment path not established here | Latest default commit inspected: **2026-04-03**, dependency pin. Outputs are estimates, even though components are linear |
| **DSINE** [S15] | Learned surface-normal estimation; uncertainty-estimating checkpoints are documented | Custom license restricts use to non-commercial/internal/academic research; pretrained checkpoints required | README specifies a CUDA-oriented setup. CPU/ROCm feasibility not verified; do not infer impossibility solely from that recipe | Default commit inspected **2024-05-17**; repository pushed **2024-07-10**. Camera intrinsics assumed; missing intrinsics approximated using 60° FOV |
| **Depth Anything V2** [S16] | Learned relative depth as an optional coarse geometry proxy | Small weights Apache-2.0; Base/Large/Giant weights **CC-BY-NC-4.0**. Checkpoint required | README explicitly includes CPU fallback. AMD performance/compatibility not tested | Default commit **2026-03-24**. Model preprocessing/resampling affects outputs. Not metric scene geometry by default |
| **IC-Light** [S17] | Text- and background-conditioned learned foreground relighting | Repository Apache-2.0. Pretrained models automatically downloaded by demo; underlying model/checkpoint terms must be checked separately | README uses NVIDIA CUDA package setup; AMD/ROCm operation and practical CPU performance not established here | Latest default commit inspected **2025-02-20**. Official “Lighting Preference” is an **initial latent pattern**, not a calibrated azimuth |
| **LightLab** [S18] | Published 2025 approach for intensity/color control of visible lights, ambient change, and virtual-light insertion | No root license found in inspected repository. Runnable model/checkpoint availability not established there | Not established | Root contained site assets, README, HTML, and `resize.py`; **not a demonstrated runnable inference release**. Latest commit **2025-05-15** |
| **PIXLRelight** [S19–S21] | 2026 feed-forward relighting conditioned by target intrinsics from a photograph or Blender render passes | Code **MIT**; model weights **CC-BY-NC-4.0**. Requires checkpoints; RGB-target path uses Marigold-IID-Lighting. Full reconstructed-scene workflow adds geometry/material estimators | README defaults to `cuda` and exposes `--device`; actual CPU or AMD pipeline feasibility/performance unverified | Default commit **2026-05-20**. Current paper is an arXiv preprint. Authors’ speed/quality claims are not a stylized-card or AMD benchmark |

**License findings that materially change selection:**

- Intrinsic’s license states: “This software is for academic use only.” [S14]
- DSINE includes a non-commercial-use restriction; it is not equivalent to a permissive open-source license. [S15]
- Depth Anything V2’s repository license does **not** imply every model size has the same checkpoint license. [S16]
- PIXLRelight’s permissive code license does **not** make its NC pretrained weights suitable for an unrestricted commercial production pipeline. [S21]
- A missing license is **unknown permission**, not permission to use the code commercially. LightLab’s inspected repository is additionally not sufficient evidence of an available executable model. [S18]

For PyTorch-based candidates, an NVIDIA-oriented setup is evidence of the documented path, not proof that AMD is impossible. Conversely, the existence of a configurable device argument does not establish ROCm support. Dependency kernels, precision support, memory, and checkpoint behavior require a separate authorized compatibility test.

#### 2.7 Current 2026 research: what PIXLRelight adds, and what it does not solve

PIXLRelight is relevant prior art because it bridges **explicit PBR lighting controls** and learned image synthesis rather than relying only on loose text prompts. The project describes:

1. estimating coarse geometry using Depth Anything 3;
2. estimating materials using Marigold-IID-Appearance;
3. authoring target illumination in Blender;
4. rendering target intrinsic maps with Cycles;
5. producing the relit output through a learned model. [S19, S20]

The runnable repository documents an alternative target-RGB path and a render-pass path. The latter accepts linear HDR EXRs including diffuse, glossy, transmission, volume, emission, and environment passes, with some groups optional. It exposes preprocessing size, crop/pad mode, dtype, device, and normalization controls. [S21]

**Published empirical claim:** the authors report state-of-the-art relighting quality and sub-0.1-second model inference. Do not translate that into end-to-end reconstruction/rendering latency, CPU/AMD speed, physically exact transport, or validated preservation of collectible-card style. [S19–S21]

The paper itself acknowledges that recovering reliable geometry and materials from photographs is difficult and that coarse reconstructions introduce artifacts. Its learned stage is designed to absorb reconstruction imperfections, not certify the reconstruction as true. [S19]

### Inferences

#### 2.8 Deterministic tools exist—but the task must be stated correctly

**Yes:**

- Exact decoding and relative-luminance calculations.
- Histograms, quantiles, spatial grids, contrast statistics.
- Conditional edge-profile and shadow-mask measurements.
- Forward calculations in a known scene.
- SH projection of a known environment map.

**No evidence of a general exact solution:**

- “Recover the true lights and their roles from any flattened stylized illustration.”
- “Infer original camera exposure from a delivered PNG.”
- “Obtain true depth/normals/materials by running a pretrained model.”
- “Measure physical K/F by dividing bright and dark object pixels.”
- “Make a text prompt’s numeric light ratio a calibrated physical control.”

The fundamental ambiguity result independently supports the negative conclusion; it does not depend on the current quality of any one model. [S4]

#### 2.9 Separate numerical repeatability from epistemic confidence

Store two fields:

```text
measurement_repeatability: deterministic / stochastic / implementation-dependent
physical_interpretation: observed / conditional / learned / not-identifiable
```

For example:

```text
feature: shadow_edge_width
value: 0.012 subject_diagonals
measurement_repeatability: deterministic_given_annotations
physical_interpretation: observed_image_transition
emitter_size_inference: not_identified
```

The number above is illustrative, not a measured project reference or recommended target.

### Gaps

- No benchmark in the inspected evidence establishes these learned estimators’ accuracy on the project’s collectible-card style.
- No model or GPU pipeline was run on the RX 7900 XTX.
- Original scene/camera calibration, reference masks, and reference-image measurements are absent.
- IC-Light’s complete checkpoint/base-model license chain was not audited.
- DSINE and Intrinsic are not unrestricted production recommendations.
- LightLab’s research claims should not be mistaken for an accessible licensed implementation.
- PIXLRelight’s NC weights are a concrete production restriction even though its code is MIT.
- Current depth research is not exhausted by Depth Anything V2; PIXLRelight already uses Depth Anything 3. V2 is included because its inspected documentation gives a clear CPU fallback and model-specific licensing, not because it was established as the best 2026 estimator.

---

## 3. How should references become controls, comparisons, and targeted corrections without disturbing other axes?

### Takeaway

Use a two-layer representation: **measured appearance targets** plus **interpreted lighting controls**. Correct the smallest diagnosed mismatch, then remeasure both the intended change and collateral changes. This workflow is a project proposal grounded in the established distinctions above; no inspected paper validates a universal collectible-card scoring function. [S1–S6, S12–S23]

### Cited findings

#### 3.1 What existing prior art supports

- Standards and libraries support explicit, reproducible colorimetric calculations. [S1, S2, S12, S13]
- Rendering tools expose controllable source types, sizes, intensity/exposure, and directions in a known scene. [S5, S22]
- Area-light changes can affect shadows, body shading, and highlights together; lighting axes are not perfectly isolated. [S6]
- Learned decomposition supports illumination-aware editing, but its components are estimates. [S14]
- IC-Light offers learned foreground relighting, while documenting that its directional preference is latent initialization rather than calibrated geometry. [S17]
- LightLab reports fine-grained source controls in its paper/project description, but the inspected repository does not establish a deployable release. [S18]
- PIXLRelight demonstrates a 2026 research route from PBR controls and intrinsic conditioning to learned output. [S19–S21]
- Chiaroscuro and tenebrism provide useful verbal descriptions of light–dark organization, not numeric control specifications. [S7, S8]

These support assembling a practical workflow. They do **not** establish that the assembled workflow will preserve this project’s style without evaluation.

### Inferences

#### 3.2 Reference extraction: use a structured “lighting/value card”

**Proposed per-reference record:**

```yaml
appearance:
  analysis_space: sRGB_decoded_relative_Y_and_CIELAB_Lstar
  regions:
    subject: reviewed_mask
    background: reviewed_mask
    receiver: optional_reviewed_mask

  subject_value_quantiles: measured
  background_value_quantiles: measured
  subject_background_separation: measured
  tonal_spread: measured
  spatial_value_grid: measured

  cast_shadow:
    present: yes_no_or_not_applicable
    direction_2d: measured_if_annotated
    normalized_extent: measured_if_annotated
    edge_width_10_90: measured_if_valid
    contact_gap: measured_if_applicable

  rim:
    appearance: absent_restrained_strong_or_uncertain
    reviewed_coverage: optional

interpretation:
  dominant_key_direction: plausible_direction_or_unknown
  direction_confidence: low_medium_high
  apparent_source_size: small_medium_large_or_unknown
  fill_description: open_readable_deep_or_unknown
  inferred_source_count: unknown_unless_supported

control_intent:
  prompt_description: explicit_words
  renderer_parameters: only_if_authored
  prohibited_collateral_changes: explicit_list
```

Do not fill unknown physical fields merely to make the schema look complete.

For a set, summarize each reference **as an image**, rather than pooling all pixels across cards. Pooling can let one large background or high-resolution image dominate the target. Keep category-specific groups: floating-object references should not impose missing-contact penalties, and environmental references should not determine every simple-background card’s histogram.

#### 3.3 Reference comparison and uncertainty

**Proposed comparison protocol:**

1. Match asset crop, background treatment, color encoding, mask rules, and analysis scale.
2. Compare subject, background, and shadow regions separately.
3. Compare delivered appearance first.
4. Add exposure-normalized or material-controlled analyses only as explicitly separate diagnostics.
5. Review coarse spatial fields as well as histograms: equal histograms do not imply equal light placement.
6. Inspect full-size and delivery-size images; resampling can alter small penumbrae, rims, and contact accents.

For feature \(f\), a robust reference center/spread can be

\[
m_f=\operatorname{median}_j f_j
\]

and

\[
s_f=1.4826\,\operatorname{median}_j|f_j-m_f|.
\]

A proposed normalized deviation is

\[
z_f=\frac{|f_{\rm candidate}-m_f|}
{\max(s_f,\tau_f)},
\]

where \(\tau_f\) is an explicit tolerance floor in the feature’s units.

**Cautions:**

- With few references, MAD can be zero or misleadingly small; the tolerance floor must not be hidden.
- Reference variation is not the same as estimator uncertainty.
- Pixels within an image are not independent reference artworks.
- If resampling uncertainty across references, resample images rather than treating millions of correlated pixels as independent observations.
- Do not call an empirical reference range a universal style law.

For comparing 1D luminance distributions, an optional CDF-based distance is

\[
W_1\approx\sum_b|F_{\rm ref}(b)-F_{\rm cand}(b)|\,\Delta b.
\]

This gives an interpretable distribution distance on a declared axis, but still ignores spatial organization and can penalize intentional differences in object color or background area.

**Recommended reporting:** a small feature dashboard and explicit failure reasons, not an unexplained composite “lighting score.”

#### 3.4 Compile measurements into concrete prompts without inventing calibration

A prompt-facing specification should express:

1. dominant direction;
2. broadness/apparent source size;
3. shadow-side readability;
4. shadow organization;
5. subject/background value separation;
6. highlight restraint;
7. preservation constraints.

**Example: soft collectible-object lighting**

> Preserve the object’s geometry, material identity, palette, camera, silhouette, and painted rendering style. Change lighting only: a broad upper-left frontal key with gentle fill, readable shadow-side detail, restrained highlights, and a compact soft shadow extending down-right on the existing surface. Keep the subject’s value separation from the background comparable to the reference. Do not add a luminous outline, new light fixture, bloom, or dramatic dark environment.

**Example: reduce tonal flatness without hardening shadows**

> Increase broad light–dark modeling across the existing form while retaining the same large soft key, shadow direction, and soft cast-shadow edges. Reduce shadow-side fill moderately; do not sharpen the emitter or increase fine texture contrast.

**Example: floating-object category**

> Retain the floating presentation. Use broad upper-left modeling and open shadow values. Do not introduce a receiving surface, contact shadow, or environmental vignette.

These are proposed instructions. A text-only generator may not obey exact numeric angle or ratio values. Where numeric physical control matters, author it in a renderer or another calibrated interface, and evaluate the result rather than treating the prompt as an instrument. [S5, S17, S21]

**Keep two representations when needed:**

```text
Artist-facing:
“broad upper-left key; open shadows; restrained rim”

Renderer-facing:
explicit authored coordinates, source shape/size,
contributions, exposure, and display transform
```

A numeric renderer specification is a chosen reconstruction or control setup—not a declaration that the original reference used those values.

#### 3.5 Targeted corrections and cross-axis side effects

| Diagnosed mismatch | Smallest plausible correction | Verify afterward | Likely side effects / confounders |
|---|---|---|---|
| Entire artwork too bright, including subject and background | Adjust delivered tonal placement or an explicit global exposure-like transform | Subject/background quantiles, endpoint occupancy, separation | Highlight compression; changed color appearance; cannot restore clipped detail |
| Subject too dark but background correct | Subject-masked adjustment or subject-lighting edit | Subject quantiles, silhouette separation, background invariance | Mask halos, altered material appearance |
| Shadows too deep while highlights already match | Increase fill or selectively lift shadow values | Shadow-side patches and highlight stability | Reduced modeling; different apparent material roughness; local grade may not reproduce transport |
| Form too flat while shadow softness is correct | Reduce fill or strengthen broad directional modeling without shrinking source | Broad spatial field, shadow-side readability, unchanged edge widths | Increased contrast can accentuate texture and outlines |
| Cast-shadow edge too sharp | Increase apparent emitter extent in a controlled scene, or perform localized shadow editing | Edge profiles, contact region, shadow extent | Larger sources also alter highlights/body shading; generic blur damages texture |
| Cast shadow too long | Change light elevation only in a suitable scene model, or edit shadow extent | Direction, length, contact, form shading | Relighting can move highlights and attached shadows; length alone does not identify elevation |
| Cast shadow points the wrong way | Relight/edit the associated shadow consistently | 2D direction plus form-shading cues | A shadow-only edit may contradict object highlights |
| Object appears ungrounded in a surface-standing category | Repair contact alignment and local grounding | Contact gap, receiving-plane consistency, edge halos | Excess darkening looks dirty; adding contact is wrong for floating categories |
| Rim too strong or too extensive | Reduce rear/rim contribution or edit only the relevant boundary band | Rim width/coverage and silhouette readability | Loss of separation; confusion with an intentional outline |
| Highlights too large or numerous | Diagnose source extent versus material/specular changes before editing | Highlight coverage plus material identity | Lighting-only instructions may change roughness or metallic appearance |
| Subject disappears into background | Adjust local value separation around the silhouette or background level | Boundary-band contrast and reference distribution | Can become an outline, halo, or vignette rather than lighting |
| Image looks “cinematic” but unlike the set | Remove broad dramatic labels; specify actual target value structure | Regional distributions, background darkness, selective highlight emphasis | Genre/style words can alter palette, composition, setting, or texture |

The physical coupling between emitter size, shadows, shading, and highlights is documented; the specific correction policy is proposed. [S5, S6]

**Do not claim perfect axis isolation.** Lighting changes legitimately alter perceived material and color. A low-change operation is not automatically a physically correct relighting, while a physically plausible relighting may change many image features.

#### 3.6 Preservation strategy

**Proposed guardrails, not guarantees:**

- Retain original input, generation parameters, and edit history.
- Request one diagnosed correction per iteration.
- Use the same crop, camera, and composition.
- Keep explicit “do not change” constraints for silhouette, material identity, palette, texture treatment, and object details.
- Use fixed stochastic settings where supported to improve comparison, without claiming that a fixed seed guarantees content preservation.
- Prefer a small masked tone correction for a genuinely tonal mismatch.
- Prefer a lighting-aware edit or authored scene change for a directional/shadow-transport mismatch.
- Evaluate both:
  - **target delta:** did the failed lighting/value feature move toward the reference?
  - **collateral delta:** did protected content or other appearance features move unnecessarily?
- Reject edits that pass a histogram test by altering object colors, deleting detail, enlarging highlights, changing the background, or changing subject size.

A correction record can be:

```text
Failure:
Subject shadow-side values below the reference range;
highlight range and cast-shadow edge width already acceptable.

Requested change:
Lift shadow-side fill only.

Protected:
Key direction, emitter softness, object silhouette, material,
palette, texture, camera, background.

Acceptance:
Shadow-side feature improves;
highlight range and edge width remain within tolerance;
protected-content review passes.
```

No numeric acceptance threshold has yet been calibrated for this project.

#### 3.7 Minimal feasible stack

**Recommended first implementation — proposed:**

1. **CPU colorimetry and statistics**
   - Explicit sRGB decoding.
   - Relative \(Y\) and \(L^*\).
   - Regional quantiles, occupancy, spread, and separation.
   - Coarse spatial value grids.

2. **Reviewed masks**
   - Subject/background initially.
   - Receiver and shadow only where applicable.
   - Manual review is acceptable during calibration; do not hide it behind claims of full automation.

3. **Small reference schema**
   - Observed appearance.
   - Confidence-tagged lighting interpretation.
   - Prompt-ready control intent.
   - Category-specific applicability.

4. **Prompt compilation**
   - Use concrete directional/softness/fill/shadow descriptions.
   - Avoid unspecified “cinematic,” “dramatic,” or historical labels.

5. **Evaluation and one-change correction**
   - Compare regional features and spatial organization.
   - Keep a human-readable failure report.
   - Reject collateral changes.

**Why this first:** it needs no pretrained checkpoints, does not assume CUDA, avoids the identified academic/NC model restrictions, and directly measures the delivered artifact. `scikit-image` and Colour are suitable building blocks, provided their conventions are handled explicitly. [S1, S12, S13]

**Not established:** whether this baseline alone predicts human judgments of reference compatibility. That is a project hypothesis to test, not a literature result.

#### 3.8 Advanced stack

Add only after a demonstrated baseline failure:

**A. Known-scene lighting controls**

- Author coarse geometry and receiver surfaces in Blender.
- Control source directions, angular sizes, fill, and exposure explicitly.
- Render diagnostic passes and, if useful, broad SH illumination.
- Use CPU or the documented HIP path; validate the actual machine separately. [S5, S22]

This gives controllable **authored lighting**, not recovered reference truth.

**B. Learned scene proxies**

- Optional relative depth.
- Optional normals.
- Optional intrinsic shading/albedo/residual estimates.
- Keep model/version, input preprocessing, and uncertainty.
- Use these to suggest controls or explain mismatches, not certify physics. [S14–S16]

Respect licensing: the inspected Intrinsic and DSINE licenses make them poor defaults for an unrestricted production tool.

**C. Learned relighting**

- IC-Light is an accessible documented relighting candidate, but directional preferences are not calibrated angles and deployment/license chains require checking. [S17]
- PIXLRelight is especially relevant to explicit 2026 PBR-to-image control research, but its NC pretrained weights restrict production suitability. [S19–S21]
- LightLab is relevant research prior art, not an established runnable dependency from the inspected repository. [S18]

**D. Validation with controlled synthetic data**

Use known Blender scenes to test whether the proposed analysis detects intended changes:

- move azimuth while holding the rest fixed;
- change elevation;
- change emitter size with declared power normalization;
- change fill contribution;
- change a global exposure-like scale;
- change material reflectance without lighting.

The final material-change test is important: an evaluator that calls every darker material “lower exposure” fails the intended distinction.

These experiments are proposed and were not performed. Success on synthetic scenes would validate aspects of the measurement implementation, not prove correctness on stylized reference artwork.

#### 3.9 Evidence and confidence summary

| Claim | Classification | Confidence / boundary |
|---|---|---|
| Correctly decoded sRGB supports deterministic relative-luminance calculation | Established standard | High; conditional on color-space interpretation |
| `rgb2gray` does not itself perform sRGB decoding in inspected implementation | Verified code behavior | High for inspected source revision |
| Unknown geometry/material/light configurations can produce identical images | Established mathematical result | High within stated model assumptions; strongly cautions against unrestricted recovery claims |
| Nine SH coefficients approximate distant diffuse irradiance well in the cited work | Published analytical/empirical result | High for the stated setting; not an inverse-lighting guarantee |
| Larger area sources can soften shadows and alter shading/highlights | Established rendering behavior | High; geometry/material conditions still matter |
| Intrinsic/normal/depth outputs are estimates | Documented methods plus inverse-problem analysis | High |
| PIXLRelight provides PBR-conditioned learned relighting | Documented capability / 2026 preprint | High that interface exists; project fitness untested |
| Current learned methods preserve this card style under isolated lighting edits | Unestablished project hypothesis | Unknown |
| Proposed feature dashboard predicts set compatibility | Proposed project hypothesis | Unknown until reference/human validation |
| CPU baseline is feasible without pretrained models | Engineering inference from analytical operations and libraries | High; exact throughput unbenchmarked |
| RX 7900 XTX can use Blender’s documented HIP family support | Official documented support | High at supported-family level; local runtime not tested |

### Gaps

#### Material negative findings

1. **No universal deterministic physical-light extractor was established.** Deterministic appearance analysis is available; unrestricted physical recovery is a different problem.
2. **No reference-derived numeric targets exist yet.** Avoid inventing a universal “correct collectible-card” luminance, ratio, softness, or exposure.
3. **No single scalar metric is enough.** Histograms lose spatial structure; edge width loses semantics; learned intrinsic maps inherit priors.
4. **No automatic causal diagnosis is guaranteed.** Dark pixels can result from dark materials, occlusion, lighting, grading, or intentional painting.
5. **No evaluated isolated-edit guarantee exists for this project.** Prompt constraints are requests, not hard preservation mechanisms.
6. **No GPU deployment claims were tested.** Official Blender HIP support is not a benchmark of the installed system or of PyTorch relighting models.
7. **Research availability is not production suitability.** Academic-use software, NC checkpoints, missing licenses, and website-only repositories are material distinctions.
8. **No exhaustive 2026 survey is claimed.** The inspected current work establishes relevant prior art, not that every new relighting paper or model has been compared.

#### Source register

All sources below were accessed **2026-10-31**. The original research inspected 21 principal documents/repositories; the corrected handoff added only two material-gap checks: official Blender GPU support and licensing. Repository license and commit endpoints were additionally inspected.

**Standards, analytical foundations, and terminology**

- **S1 — W3C, Understanding SC 1.4.3 / WCAG 2.2.**  
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html  
  Supports exact sRGB decoding threshold and relative-luminance formula. Accessibility contrast thresholds are **not** proposed as artwork-style thresholds.

- **S2 — W3C, CSS Color Module Level 4.**  
  https://www.w3.org/TR/css-color-4/  
  Inspected version identified itself as a **2026-10-29 Candidate Recommendation Draft**, not a final Recommendation. Supports color-space/reference interpretation and the distinction between physical color and representations.

- **S3 — Ramamoorthi and Hanrahan, “An Efficient Representation for Irradiance Environment Maps.”**  
  https://graphics.stanford.edu/papers/envmap/  
  Primary research page. Supports nine-coefficient low-frequency diffuse irradiance representation and the authors’ reported approximation accuracy under stated assumptions.

- **S4 — Belhumeur, Kriegman, and Yuille, “The Bas-Relief Ambiguity,” IJCV, 1999.**  
  https://link.springer.com/article/10.1023/A:1008154927611  
  Supports non-unique geometry/albedo/lighting reconstruction, including the stated treatment of cast and attached shadows.

- **S5 — Blender Manual, Light Objects.**  
  https://docs.blender.org/manual/en/latest/render/lights/light_object.html  
  Official documentation. Supports source types, size/softness effects, exposure multiplication, normalization, and the distinction between spotlight footprint softness and shadow softness.

- **S6 — Pharr, Jakob, and Humphreys, PBRT 4th edition, Area Lights.**  
  https://www.pbr-book.org/4ed/Light_Sources/Area_Lights  
  Primary technical reference. Supports area-light integration and coupled effects on penumbrae, body shading, and highlights.

- **S7 — Tate, Chiaroscuro.**  
  https://www.tate.org.uk/art/art-terms/c/chiaroscuro  
  Museum terminology. Supports light–dark balance/pattern and prominent contrasts, not numerical physical parameters.

- **S8 — National Gallery, Tenebrism.**  
  https://www.nationalgallery.org.uk/paintings/glossary/tenebrism  
  Museum terminology. Supports selectively illuminated details against predominantly dark settings. A Tate tenebrism URL failed retrieval; this inspected National Gallery source is used instead.

- **S9 — How To Film School, Key-to-Fill Ratio.**  
  https://howtofilmschool.com/dictionary/key-to-fill-ratio/  
  Community filmmaking reference. Explicitly distinguishes \(K:F\) from \((K+F):F\). Used for terminology evidence, not as a photometric standard.

- **S10 — PhotoCalcs, Key-to-Fill Ratio Calculator.**  
  https://photocalcs.uk/lighting/key-to-fill-ratio-calculator/  
  Community tool documenting the additive convention and stop conversion. Its raw power-percentage framing should not be substituted for calibrated incident illumination.

- **S11 — Fstoppers, “A Closer Look at High Key and Low Key Photography.”**  
  https://fstoppers.com/education/closer-look-high-key-and-low-key-photography-547770  
  Community/opinion source. Documents differing definitions and distinguishes tonal predominance from over-/underexposure. Its proposed strict thresholds are not adopted.

**Libraries and learned estimators**

- **S12 — scikit-image repository, implementation, and license.**  
  https://github.com/scikit-image/scikit-image  
  Inspected color-conversion implementation:  
  https://github.com/scikit-image/scikit-image/blob/51b3367761a52ab9111bdbd9537272d7dd2eccde/src/_skimage2/color/colorconv.py  
  License: https://github.com/scikit-image/scikit-image/blob/main/LICENSE.txt  
  Supports `rgb2gray` behavior, `rgb2lab` assumptions, analytical image-processing building blocks, and license distinctions. Current documentation was also queried through installed Context7 CLI.

- **S13 — Colour repository and license.**  
  https://github.com/colour-science/colour  
  License: https://github.com/colour-science/colour/blob/develop/LICENSE  
  Supports CIE lightness and transfer-function utilities. Current documentation was also queried through installed Context7 CLI.

- **S14 — Careaga and Aksoy / Computational Photography Lab, Intrinsic.**  
  https://github.com/compphoto/Intrinsic  
  License: https://github.com/compphoto/Intrinsic/blob/main/LICENSE  
  Official implementation for 2023 ordinal-shading and 2024 colorful intrinsic-decomposition papers. Supports estimated albedo/shading/residual outputs and academic-use restriction.

- **S15 — Bae and Davison, DSINE.**  
  https://github.com/baegwangbin/DSINE  
  License: https://github.com/baegwangbin/DSINE/blob/main/LICENSE  
  Official CVPR 2024 implementation. Supports learned normals, camera-intrinsics assumptions, uncertainty-checkpoint availability, pretrained dependency, and restrictive license.

- **S16 — Depth Anything V2.**  
  https://github.com/DepthAnything/Depth-Anything-V2  
  Supports relative-depth inference, explicit CPU fallback, preprocessing caveats, and different licenses for Small versus larger checkpoints.

**Relighting prior art and current 2026 work**

- **S17 — Official IC-Light repository.**  
  https://github.com/lllyasviel/IC-Light  
  License: https://github.com/lllyasviel/IC-Light/blob/main/LICENSE  
  Supports text/background relighting, automatic model download, CUDA-oriented setup, and latent-initialization interpretation of lighting preference.

- **S18 — Magar et al., LightLab repository/project materials.**  
  https://github.com/NadMag/LightLab  
  Supports the authors’ 2025 research claims about parametric source controls. Inspected repository contents did not establish a runnable released model; no root license found.

- **S19 — Farinha and Clark, “PIXLRelight: Controllable Relighting via Intrinsic Conditioning,” 2026 preprint.**  
  https://arxiv.org/abs/2605.18735  
  Supports the PBR/intrinsic-conditioning approach, reconstruction limitations, and authors’ empirical claims. Peer-reviewed acceptance was not established.

- **S20 — PIXLRelight project page.**  
  https://mlfarinha.github.io/pixl-relight/  
  Supports the described Depth Anything 3 / Marigold / Blender reconstruction-and-rendering pipeline.

- **S21 — PIXLRelight official implementation.**  
  https://github.com/mlfarinha/pixlrelight  
  License: https://github.com/mlfarinha/pixlrelight/blob/main/LICENSE  
  Supports target-image and linear-EXR render-pass interfaces, configurable device/dtype/preprocessing, automatic checkpoint dependency, MIT code, and CC-BY-NC-4.0 weights.

**Two follow-up checks filling deployment/license gaps**

- **S22 — Blender Manual, GPU Rendering.**  
  https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html  
  Official support documentation. Lists Linux HIP support and Radeon RX 7000-series GPUs. Does not establish the local installation’s working state.

- **S23 — Blender licensing.**  
  https://www.blender.org/about/license/  
  Official licensing explanation. Distinguishes Blender GPL licensing, Cycles Apache-2.0, and freedom to use created artwork commercially.

#### Research spend and validation record

- **12 Kagi ordinary-search queries** across three batches.
- **Two Context7 library resolutions and two documentation queries.**
- **One Exa batch fetch** for 15 known/source-discovered pages.
- Direct public-source fetches and GitHub metadata/license/source inspection.
- Two additional official Blender page fetches for the corrected handoff.
- **No Perplexity Deep Research, Kagi Assistant, software installation, model-weight download, private-image upload, or untrusted repository-code execution.**
- No generated/reference images were measured; no throughput, visual-quality, or GPU benchmark was performed.

**Recommended decision:** implement the CPU appearance-measurement baseline first. Preserve an explicit boundary between **what the pixels show**, **what a model hypothesizes**, and **what a chosen control system can author**.
