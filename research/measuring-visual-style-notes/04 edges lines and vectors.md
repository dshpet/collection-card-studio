# Measuring and controlling edges, lines, contours, and directional structure

Research cutoff and access date: **2026-10-31**.

Scope: reference extraction → prompt vocabulary → generated-image evaluation → narrowly scoped correction. Particular attention is given to **outline-free, polished, dimensional casual-game art**, not only ink drawing or vector illustration.

**Evidence classes used throughout**

- **Direct:** an observable image property or a documented algorithmic operation. Direct measurement does not automatically establish artistic intent.
- **Conditional:** interpretable only under stated assumptions, such as an isolated monotonic boundary, a correct segmentation, or an independently identified stroke.
- **Learned:** dependent on training data, model architecture, checkpoint, preprocessing, and inference settings.
- **Underdetermined:** the raster alone does not uniquely establish the proposed explanation, intention, or perceptual effect.

Mathematical definitions below are proposed operational measurements unless explicitly attributed to a source. They are **not universal aesthetic standards**.

## 1. What can be measured reliably, and what remains ambiguous?

### Takeaway

The useful unit of analysis is not a single “edge sharpness” score. It is a **region-specific profile of boundary contrast, transition width, localization, continuity, geometric shape, and orientation**, with explicit stroke measurements added only where strokes have been established independently.

A deterministic detector finds changes in image values. It does **not** establish that those changes are drawn outlines, that its output thickness equals line weight, or that its orientations predict a viewer’s gaze.

### Cited Findings

#### 1.1 Five different things commonly called an edge or line

| Object | What it actually represents | Evidence class | Principal caution |
|---|---|---|---|
| Raster intensity/color edge | A spatial change in image values | Direct | Can arise from silhouettes, shadows, highlights, texture, strokes, compression, or resampling |
| Detector edge map | Features selected by an algorithm and its settings | Direct algorithmic output | Not an inventory of artistic strokes |
| Segmentation contour | Boundary of a selected object/region mask | Direct geometry; conditional or learned mask provenance | Can exist where the image has little or no visible boundary contrast |
| Drawn stroke | An intentional or convincingly stroke-like mark with a centerline, width, color, and endpoints/junctions | Conditional; intention often underdetermined | Its two flanks can generate two detector edges |
| Implied directional relation | Alignment, gesture, repeated objects, a path, an eyeline, or a compositional relationship | Conditional/semantic | May have no continuous geometric line in the raster |

Canny’s original formulation separates **detection**, **localization**, and **one response to a single edge**. These are detector-design criteria, not criteria for identifying drawn marks or evaluating an illustration’s style. Its abstract also describes a detection/localization trade-off and operators at multiple widths. — [Canny, 1986](https://pubmed.ncbi.nlm.nih.gov/21869365/)

OpenCV describes Canny as gradient calculation, non-maximum suppression, and hysteresis linking. The resulting thin binary map is a representation selected by that procedure. — [OpenCV Canny tutorial](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html)

**Important distinction:** a broad black stroke may yield two thin Canny chains, one at each flank. A sharp object silhouette may yield one thin chain without any stroke being present. Consequently:

> Detector-chain thickness is not source-stroke thickness. Detector-chain count is not pen-stroke count.

This distinction also applies to learned detectors. A model’s thin or “crisp” output describes its **prediction representation**, not necessarily the width or softness of the source image’s transition. The 2026 MEMO paper explicitly addresses thick predicted edge maps relative to single-pixel human annotations. — [MEMO, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Cheng_MEMO_Human-like_Crisp_Edge_Detection_Using_Masked_Edge_Prediction_CVPR_2026_paper.html)

#### 1.2 Boundary strength, softness, and localization are separate axes

A useful local analysis samples an image profile **normal to a boundary**, rather than relying only on a whole-image filter score.

Let:

- \(Y(x,y)\): normalized relative luminance;
- \(p(t)\): a sampled profile crossing an independently selected boundary;
- \(a,b\): representative values on its two sides;
- \(C=|b-a|\): local side-to-side contrast.

For an sRGB input, a defensible luminance analysis first decodes the transfer curve and then forms the weighted RGB sum. The W3C explanatory page gives the relative-luminance coefficients and notes the corrected sRGB breakpoint of \(0.04045\). This is a color-conversion reference, **not** an artistic-edge acceptability standard. — [W3C relative luminance](https://www.w3.org/WAI/GL/wiki/Relative_luminance)

| Feature | Operational measurement | Units/range | Interpretation and assumptions |
|---|---|---|---|
| Side-to-side contrast | \(C=|b-a|\) | Relative-luminance difference, usually \(0\ldots1\) | Measures separation, not softness |
| Peak gradient | \(g_{\max}=\max_t|dp/dt|\) | Luminance difference per pixel | Increases with contrast and decreases with transition width |
| Transition width | \(w_{10–90}=|t_{90}-t_{10}|\) | Pixels; also report \(w_{10–90}/D\) | Conditional on a resolved, reasonably monotonic transition with identifiable sides |
| Contrast-adjusted steepness | \(g_{\max}/C\) | \(1/\text{pixel}\) | Undefined or unstable when contrast is too small |
| Boundary location | Maximum gradient, fitted step center, or specified contour crossing | Pixel coordinates | Different conventions can disagree |
| Localization error | Distance to an independently defined target boundary | Pixels and fraction of \(D\) | Requires a target; otherwise it is not an error measurement |
| Overshoot/undershoot | Excursion beyond the two local side values, optionally divided by \(C\) | Luminance or dimensionless | Useful for diagnosing ringing and sharpening halos |
| Continuity | Supported boundary length divided by annotated relevant length | \(0\ldots1\) | Depends on what was annotated as relevant/visible |

Here \(D=\sqrt{W^2+H^2}\), the image diagonal in pixels. An object-scale denominator can additionally be used when objects occupy substantially different fractions of the frame; the denominator must be reported.

**Why separate contrast and softness?**

For the idealized model of an isolated step of amplitude \(C\), convolved with a Gaussian of standard deviation \(\sigma\):

\[
p(t)=a+C\Phi(t/\sigma)
\]

\[
w_{10–90}\approx2.563\sigma
\]

\[
g_{\max}=\frac{C}{\sqrt{2\pi}\sigma}
\]

These are analytical consequences of the model:

- increasing contrast can increase the peak gradient without narrowing the transition;
- increasing blur can widen the transition without changing its eventual plateau contrast;
- a weak sharp edge and a strong soft edge can have similar peak gradients.

These identities are useful for calibration fixtures, **not proof that an illustrated boundary was produced by Gaussian blur**.

Canny’s scale-dependent detection/localization behavior supports treating smoothing scale as a declared measurement setting rather than an invisible implementation detail. — [Canny, 1986](https://pubmed.ncbi.nlm.nih.gov/21869365/)

#### 1.3 Hard, soft, and lost edges: useful descriptions, conditional classifications

Use these as **relative descriptions tied to the reference and viewing size**, not fixed numerical classes.

| Description | Practical observable interpretation | What it does not prove |
|---|---|---|
| Hard/firm edge | Relatively narrow transition, usually clearly locatable at intended display size | Does not require black ink or high global contrast |
| Soft edge | A broader local transition across the boundary | Does not establish optical defocus, painterly blending, or a particular material |
| Lost edge | A semantically expected boundary locally merges with surrounding values/colors or becomes difficult to distinguish | A missing detector response alone does not establish an intentional lost edge |
| Found edge | A clearly articulated boundary segment, especially when contrasted with nearby merges | Does not require a continuous outline |
| Varied edges | Deliberate-looking distribution of firm, soft, and merged segments | Cannot be established merely by a wide global sharpness histogram |

A segmentation can help identify where a boundary is expected, but it may also impose a closed contour where the source has little visible separation. SAM-style masks are region predictions, not measurements of local edge visibility. — [SAM 2](https://github.com/facebookresearch/sam2); [SAM 3](https://github.com/facebookresearch/sam3)

**Operational lost-edge analysis**

1. Select or annotate the relevant object boundary.
2. Separate visible boundaries, occluded portions, uncertain portions, and intentional-looking merges.
3. Measure local contrast and transition behavior along the visible/merged portions in the **original image**.
4. Report the fraction of boundary length classified as merged under an explicitly calibrated rule.
5. Preserve uncertainty where segmentation or visibility is ambiguous.

Do not equate:

- low contrast with wide softness;
- occlusion with a lost edge;
- a failed threshold with intentional painterly merging;
- an inferred hidden object boundary with a visible contour.

#### 1.4 Sfumato is not synonymous with generic blur

The National Gallery defines sfumato through gradual tonal modulation without harsh outlines, including figures that almost fuse with their surroundings. It quotes Leonardo’s advice to paint “without lines.” — [National Gallery: Sfumato](https://www.nationalgallery.org.uk/paintings/glossary/sfumato)

For practical image analysis:

| Candidate explanation | Evidence to inspect | Limit |
|---|---|---|
| Sfumato-like treatment | Selective, form-aware tonal transitions and contour merging; retained structure elsewhere | Artistic process and intent cannot be recovered uniquely |
| Optical/defocus-like blur | Similar spreading of nearby details consistent with a focus treatment | A painted imitation can look similar |
| Uniform post-blur | Broad softening across unrelated silhouettes, texture, and small features | A final raster rarely reveals the exact processing history |
| Antialiasing | Coverage-like intermediate pixels around otherwise well-defined boundaries, strongly dependent on sampling scale | A small antialiased edge is not automatically a painterly soft edge |
| Resampling artifact | Stair-stepping, moiré, ringing, or filter-dependent overshoot | Requires attention to previous and current scaling |
| Compression artifact | Blocking or ringing near boundaries, possibly color-detail degradation | A single image may not identify all previous encodings |

ImageMagick’s resampling documentation discusses aliasing, blur, negative-lobe filters, and ringing near strong boundaries. It specifically notes that ringing can arise from resizing or compression and that sharper reconstruction filters involve trade-offs. — [ImageMagick resampling filters](https://usage.imagemagick.org/filter/)

**Recommended wording:** “sfumato-like, selectively merged tonal contours” is more precise than “blurry,” but neither phrase identifies the original production method.

#### 1.5 All-image edges versus segmentation contours

These answer different questions.

| Method | Good for | Misses or confounds |
|---|---|---|
| All-image gradients/Canny | Boundary activity, fine texture, seams, highlights, shadows, regional orientation | Mixes semantic boundaries with incidental image variation |
| Contours of a segmentation mask | Silhouette shape, perimeter, curvature, object-relative geometry | Omits most interior edges and may include visually weak or inferred boundaries |
| Edge measurements in a band around an object contour | Visible boundary contrast, softness, articulation, local merging | Depends on mask placement and band width |
| Confirmed stroke mask plus skeleton | Stroke width, taper, connectivity proxies, ink occupancy | Depends on actually separating strokes from fills/shadows |
| Semantic annotations of gesture/eyelines | Implied directional relations | Requires interpretation and cannot be replaced by an undifferentiated edge map |

OpenCV’s `findContours` traces a supplied binary representation; it does not decide that representation’s artistic meaning. Its shape tools include contour length and point-to-contour distance operations. — [OpenCV shape descriptors](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html)

`skimage.measure.find_contours` extracts iso-valued contours by marching squares with interpolation. The selected level and connectivity convention matter; contours can remain open at image or mask boundaries. — [scikit-image `find_contours`](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.find_contours)

**Critical trap:** applying `findContours` to a Canny map traces the binary edge representation. That is not equivalent to extracting an object’s segmentation silhouette.

#### 1.6 Explicit strokes: width, weight, taper, and economy

Only activate these axes after establishing that explicit strokes exist in the region being assessed.

A practical stroke representation contains:

- a stroke-like foreground mask;
- centerline or medial axis;
- width along that centerline;
- stroke color and local contrast;
- endpoints and junctions;
- outer-contour versus internal-detail role.

For an isolated, well-segmented band, a local width approximation is:

\[
w(s)\approx 2\,d(s,\text{background})
\]

evaluated on its medial axis.

`skimage.morphology.medial_axis(..., return_distance=True)` exposes the medial-axis and distance-transform ingredients. Its documentation also identifies pseudo-random tie-breaking, so fix the relevant seed when repeatability matters. — [scikit-image morphology](https://scikit-image.org/docs/0.26.x/api/skimage.morphology.html#skimage.morphology.medial_axis)

This width approximation is unreliable near:

- junctions;
- touching strokes;
- rounded caps;
- irregular filled shapes;
- uncertain antialiased boundaries;
- unresolved narrow marks.

| Stroke axis | Suggested descriptor | Interpretation limit |
|---|---|---|
| Typical weight | Median width, in pixels and normalized units | Requires a valid stroke mask |
| Weight variation | Width quantiles or IQR/median | Does not establish pressure-sensitive drawing |
| Outer/internal hierarchy | Typical outer-contour width divided by internal-stroke width | Requires role annotations |
| Taper | Width profile along a selected mark | Caps and resolution can mimic taper |
| Stroke contrast | Mark-to-adjacent-fill difference | Separate from mark width |
| Ink occupancy | Stroke-mask area / region area | Mixes width and number/length of marks |
| Centerline density | Total centerline length divided by a declared scale | Content-dependent |
| Connectivity | Endpoints, branches, connected components | Not original pen lifts or brush gestures |
| Economy | Semantic detail retained with comparatively few purposeful marks | Ultimately conditional on content and human judgment |

**Line economy is not “few Canny pixels.”** A stroke-free dimensional image can have many detector edges from lighting and geometry. An economical ink drawing can have long, high-contrast outlines.

Likewise, the `width` output from OpenCV’s line-segment detector concerns the supporting region of its detection. It must not be silently relabeled as painted stroke weight. — [OpenCV `LineSegmentDetector`](https://docs.opencv.org/4.13.0/db/d73/classcv_1_1LineSegmentDetector.html)

#### 1.7 Orientation fields, histograms, and structure tensors

Let \(G_x,G_y\) be image derivatives.

\[
\theta_n=\operatorname{atan2}(G_y,G_x)
\]

is the gradient/normal orientation. A local boundary tangent is:

\[
\theta_t=(\theta_n+\pi/2)\bmod\pi
\]

For unoriented lines, orientation is **axial**: \(0^\circ\) and \(180^\circ\) describe the same line alignment.

OpenCV explicitly notes that gradient direction is perpendicular to the edge. — [OpenCV Canny tutorial](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html)

**Coordinate convention must be declared.** With image \(x\) increasing rightward and \(y\) downward, angle signs differ from a conventional upward-positive mathematical coordinate system.

A regional orientation histogram can use:

- contour arc length as weights;
- detected segment length as weights;
- gradient magnitude as weights;
- uniformly weighted selected edge samples.

These are not interchangeable. Gradient weighting favors stronger-contrast boundaries; length weighting treats long boundaries as more influential.

For normalized histogram weights \(p_b\), possible descriptors include:

\[
H_\theta=-\frac{\sum_b p_b\log p_b}{\log B}
\]

and axial concentration:

\[
R=\left|\frac{\sum_i w_i e^{2j\theta_i}}{\sum_i w_i}\right|
\]

Both are dimensionless. \(R\) approaches one for a common axial alignment. Low \(R\) can mean multiple organized directions, corners, isotropic texture, or noise; it does not uniquely mean “no flow.”

**Local structure tensor**

A two-scale construction is:

\[
J=G_{\sigma_i}*
\begin{bmatrix}
Y_x^2 & Y_xY_y\\
Y_xY_y & Y_y^2
\end{bmatrix}
\]

where derivatives may first be computed on an image smoothed at a declared derivative scale \(\sigma_d\), and \(\sigma_i\) is the integration scale.

For eigenvalues \(\lambda_1\ge\lambda_2\ge0\):

\[
c=\frac{\lambda_1-\lambda_2}{\lambda_1+\lambda_2+\varepsilon}
\]

is a useful coherence descriptor, and:

\[
\theta_n=\frac12\operatorname{atan2}(2J_{xy},J_{xx}-J_{yy})
\]

gives the dominant gradient-normal orientation.

`skimage.feature.structure_tensor` and `structure_tensor_eigenvalues` provide the core operations. Its `sigma` describes the Gaussian weighting used for local summation; do not assume that a single parameter exposes two independent scales. — [scikit-image feature API](https://scikit-image.org/docs/stable/api/skimage.feature.html)

Practical safeguards:

- inspect tensor energy \(E=\lambda_1+\lambda_2\) as well as coherence;
- mask nearly flat regions where orientation is unstable;
- distinguish corners from coherent single-direction structures;
- keep derivative and integration scales in the measurement record;
- do not infer a stroke centerline’s direction from a zero-gradient ridge center without additional treatment.

**A structure tensor describes local directional variation. It does not produce a semantic arrow, attention path, or gaze direction.**

#### 1.8 Hough lines and line-segment detectors

For the standard line representation:

\[
\rho=x\cos\theta+y\sin\theta
\]

- \(\rho\): signed distance in pixels;
- \(\theta\): line-normal angle in radians;
- tangent orientation differs by \(\pi/2\).

OpenCV documents:

- `HoughLines`: accumulator resolutions in pixels and radians;
- `HoughLinesP`: line endpoints plus minimum length and maximum linking gap;
- `createLineSegmentDetector`: a local straight-segment detector with its own scale, angle, density, and refinement parameters. — [OpenCV feature detection API](https://docs.opencv.org/4.13.0/dd/d1a/group__imgproc__feature.html)

These tools suit architectural edges, rails, beams, and approximately straight alignments. They are less suitable for character gestures, organic S-curves, and disconnected implied leading lines.

Do not interpret:

- two flanks of a band as two intentional marks;
- many short segments on one curve as many artistic strokes;
- a Hough vote threshold as a style score;
- a detector’s statistical significance as artistic importance.

#### 1.9 Curvature and S-curves

For a smoothed parametric contour \((x(t),y(t))\):

\[
\kappa(t)=
\frac{x'y''-y'x''}
{(x'^2+y'^2)^{3/2}}
\]

- Units: inverse pixels when coordinates are in pixels.
- Dimensionless alternatives: \(\kappa D\), or an explicitly stated object-scale equivalent.
- Curvature sign depends on coordinate and traversal conventions.

Useful descriptors include:

- contour-length distribution;
- turning-angle distribution;
- sustained high-curvature corners;
- curvature variation along selected contours;
- stable inflection locations after declared smoothing.

An operational S-curve can be described as two sustained opposite-curvature lobes separated by an inflection. This is a **geometric description**, not a universal test of visual elegance.

Derivative-based curvature amplifies pixel stair-stepping. Resample the path by arc length and smooth at a declared geometric scale before comparing.

Do not substitute image-intensity Hessian descriptors for contour curvature. For example, scikit-image’s `shape_index` concerns the local image-intensity surface, not the shape of a selected object silhouette. — [scikit-image feature API](https://scikit-image.org/docs/stable/api/skimage.feature.html)

#### 1.10 Explicit geometry versus implied leading lines and eyelines

Keep separate records for:

1. **Explicit geometric lines:** rails, roof edges, rods, straight marks.
2. **Curved geometric paths:** roads, rivers, limbs, branches, silhouettes.
3. **Repeated alignments:** separated objects arranged along a direction.
4. **Gesture:** a character’s pose or action axis.
5. **Eyeline:** an interpreted relation between eyes/head and a target.
6. **Proposed viewing route:** an intended compositional reading.

Only the first two are directly represented as selected geometric paths.

An orientation histogram has no inherent start, destination, or arrow. A diagonal alignment can run in either direction. Gradient polarity indicates increasing image value, not viewer movement.

**No universal numeric measure of gaze direction from image lines is asserted here.** A proposed eyeline should be checked using visible eye/head relationships and the intended target, not a whole-image Hough transform.

Similarly, “diagonal,” “horizontal,” and “vertical” are valid descriptive measurements. Claims such as “diagonals inherently create excitement” are not established by these measurements. Emotional interpretations require context and appropriate perceptual evidence, not merely angle counts.

### Inferences

#### Recommended measurement contract

Before extracting any feature, record:

```text
Input
- native dimensions and crop
- color profile / assumed encoding
- alpha handling and compositing background
- known resizing or compression limitations
- effective resolution of the relevant object

Analysis
- image-level and object-level normalization
- luminance or color channels used
- derivative operator and normalization
- derivative / integration / contour-smoothing scales
- edge thresholds and boundary mode
- segmentation source and edits
- stroke-presence decision and confidence

Interpretation
- semantic region and boundary role
- evidence class
- unresolved ambiguities
```

**Color handling matters.** Grayscale-only analysis can miss equal-luminance color boundaries. A complementary color-gradient measurement may be useful, but its color space and channel scaling must be declared. A luminance gradient and a Lab-space gradient should not be compared as though they had identical units.

**Alpha handling matters.** Measuring transparent pixels against an unintended matte can create or suppress boundaries absent from the intended presentation.

#### Normalize size without inventing detail

For uniform image enlargement by factor \(s\), assuming geometrically equivalent sampling:

- lengths and widths scale by \(s\);
- curvature scales by \(1/s\);
- per-pixel gradients change with the sampling scale;
- raw edge-pixel count divided by image area is not generally scale-invariant.

Recommended normalized quantities include:

\[
w^*=w/D,\quad L^*=L/D,\quad \kappa^*=\kappa D
\]

For centerline length \(L\) within area \(A\), \(LD/A\) is a dimensionless density convention. The convention must remain fixed across comparisons.

Avoid separately stretching the image width and height: it changes angles, curvature, and line-weight relationships.

For gradients, either:

- compare at a common sampled resolution with the same operator; or
- explicitly convert derivatives to the declared normalized spatial coordinates.

A scale-normalized gradient such as \(\sigma|\nabla Y_\sigma|\) can help compare responses across smoothing scales, but remains contrast-dependent and is not an aesthetic score.

#### Low-resolution references

When a transition occupies only approximately a pixel or two, its original softness and stroke width may be unresolved. Antialiasing, subpixel placement, compression, and genuine softness can be confounded.

Recommended procedure:

1. Preserve the native reference.
2. Evaluate generated images additionally at the reference’s effective object resolution.
3. Use a declared, consistent downsampling method.
4. Measure only sufficiently resolved profiles.
5. Mark unresolved widths and stroke presence as uncertain.
6. Do not enlarge the reference and treat interpolation as recovered evidence.

Generative enhancement may produce plausible detail, but that detail is not independent evidence about the original reference.

### Gaps

- A final raster does not uniquely reveal whether a soft boundary was painted, optically blurred, resampled, or deliberately merged.
- Artistic intention, original pen lifts, and exact production tools are usually underdetermined.
- A boundary cannot have a meaningful localization **error** without an independent target or calibration fixture.
- No universal hard/soft/lost thresholds, line-economy score, gaze-from-lines metric, or angle-to-emotion mapping was validated.
- The proposed measurements have not been calibrated against the project’s actual reference images.

## 2. How should measurements become prompts, evaluations, and corrections?

### Takeaway

Translate measurements into **regional relationships**, not blanket adjectives. For polished dimensional casual art, the likely target is a combination of clear silhouettes, smooth contour geometry, broad form shading, selective firm contacts, controlled soft transitions, and sparse interior accents—not universal outlining or universal sharpness.

Corrections should specify the affected boundary class and explicitly protect composition, identity, geometry, palette, lighting, and material treatment. This is an experimental control strategy, not a guarantee of zero generative drift.

### Cited Findings

#### 2.1 Promptable controls are not interchangeable

ControlNet’s original repository distinguishes conditioning from:

- Canny edges;
- HED soft boundaries;
- M-LSD straight lines;
- segmentation maps.

It also acknowledges that line-drawing generation may modify image details. — [ControlNet](https://github.com/lllyasviel/ControlNet)

The current Diffusers documentation exposes Canny conditioning, multi-ControlNet combinations, and separate conditioning scales. It advises aligning control-image sizes and managing overlapping controls. — [Diffusers ControlNet guide](https://huggingface.co/docs/diffusers/using-diffusers/controlnet)

The native `StableDiffusionControlNetImg2ImgPipeline` source documents that:

- `controlnet_conditioning_scale` multiplies ControlNet outputs before their addition to UNet residuals;
- `control_guidance_start` and `control_guidance_end` specify fractions of the denoising schedule;
- higher img2img `strength` adds more noise;
- `strength=1` essentially ignores the starting image.

These are implementation-specific controls, not universal settings across all generators. — [Diffusers pipeline source](https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py)

ImageMagick documents sharpening/resampling trade-offs, including ringing. This supports distinguishing a raster-sharpness adjustment from a semantic restyling operation. — [ImageMagick resampling filters](https://usage.imagemagick.org/filter/)

### Inferences

#### 2.2 Practical extraction-to-prompt matrix

These phrases are **candidate vocabulary**, not empirically guaranteed mappings.

| Reference observation | Measurement/annotation | Candidate prompt language | Evaluation focus |
|---|---|---|---|
| Clear silhouette without ink | Contour-band contrast and resolved transition widths; stroke absence uncertain or confirmed | “Clearly separated silhouettes defined by color and value, without a continuous dark outline” | Silhouette readability without a new perimeter band |
| Firm overlaps, soft form shading | Boundary roles plus local width distributions | “Firm occlusion edges; broad, smooth transitions across rounded forms” | Contacts remain precise while volumes stay rounded |
| Selectively merged shadow-side contours | Annotated merge locations and local visibility | “Let selected shadow-side contours gently merge into nearby tones” | Merging occurs only in intended regions |
| Smooth but not blurred contour geometry | Curvature at fixed smoothing scale | “Clean, smooth contour shapes with controlled corners; retain local edge definition” | No jagged geometry and no blanket softening |
| Thick outer, thin inner strokes | Confirmed stroke masks and role-based width ratio | “Heavier outer contours, finer internal accents” | Actual mark widths, not Canny output thickness |
| Pressure-like taper | Width profiles of isolated marks | “Tapered, pressure-varied strokes with restrained endpoints” | Taper without added sketchiness |
| Sparse interior marks | Semantic mark inventory and normalized centerline density | “A few purposeful interior accents; omit redundant contour and texture lines” | Required details remain readable |
| Uniform outline style | Width distribution along confirmed marks | “Consistent monoline contours” | Width consistency without unwanted flattening |
| Soft colored outlines | Confirmed perimeter mark color/contrast | “Subtle colored contour accents integrated with the local palette” | No automatic conversion to black ink |
| Curved gesture | Annotated path and curvature sequence | “A broad S-shaped gesture through the pose” | Selected pose path, not whole-image angle count |
| Explicit architectural direction | Selected line segments and spatial endpoints | “Roof and rail edges align toward the upper-right structure” | Correct objects and alignments |
| Implied path | Semantic route annotation | “The path curves from the lower-left foreground toward the cottage” | Route continuity and destination |
| Eyeline | Eye/head/target annotation | “The character looks toward the lantern” | Eyes and head, not added graphic lines |

#### 2.3 A realistic target for outline-free dimensional casual art

An appropriate edge profile may include:

- **Silhouettes:** clear, well-shaped, often relatively firm, but not encircled by a uniform dark band.
- **Overlaps and contacts:** selectively firm where parts meet or occlude one another.
- **Rounded forms:** broad, low-frequency shading transitions.
- **Cast shadows:** softness varying by region rather than one global blur.
- **Small focal details:** precise eyes, mouth, clasps, and selected decorative accents.
- **Interior surfaces:** restrained edge activity, without indiscriminate microtexture.
- **Backgrounds:** potentially softer or less articulated, without making every background boundary disappear.
- **Geometry:** smooth intentional shapes, with corners where the design requires them.

This is a **testable proposed style decomposition**, not a claim that every casual-game reference shares it.

It also explains why a single global score is inadequate:

- high edge density can result from many objects rather than excessive linework;
- strong gradients can come from contact shadows rather than outlines;
- soft gradients can create dimensional modeling rather than poor focus;
- an outlined eye or mouth does not make the entire rendering an outlined style.

#### 2.4 Example prompt: edge treatment only

> Preserve the composition, subject identity, pose, proportions, palette, lighting direction, materials, and degree of dimensional modeling. Change only the edge treatment: define the major silhouettes through clean color and value separation, without adding a continuous dark perimeter. Keep firm edges at important overlaps and contacts, broad smooth shading across rounded forms, and selective softer transitions on shadow-side contours. Retain precise facial features and small focal details. Avoid sharpening halos, extra texture lines, and flattening the forms.

This is more constrained than “make it sharper” or “make it painterly.”

For an explicit-stroke reference:

> Preserve the existing shapes, fills, shading, and composition. Refine only the drawn marks: use heavier outer contours than internal accents, controlled taper on selected strokes, and fewer redundant interior lines. Keep the current palette and dimensional shading; do not convert the image into flat line art.

For directional structure:

> Preserve the camera, object placement, palette, and rendering. Adjust only the path geometry so that it curves from the lower-left foreground toward the cottage, with one broad change of curvature. Do not add graphic guide lines or alter the character’s gaze.

For an eyeline:

> Preserve the head shape, expression, pose, and lighting. Adjust only the eyes so the character looks toward the lantern. Do not rotate the entire head or add drawn eyeline marks.

Each remains a hypothesis requiring visual validation.

#### 2.5 Terms likely to cause collateral drift

| Broad wording | Possible unwanted interpretation | More controlled alternative |
|---|---|---|
| “Sharper” | More contrast, texture, halos, or outlines everywhere | Identify the specific silhouettes or contacts needing narrower transitions |
| “Clean vector style” | Flat fills and reduced volume | Ask for smooth contour geometry while preserving dimensional shading |
| “More line art” | Added outlines and internal marks | Specify whether the reference actually has strokes |
| “Softer” | Uniform blur or lost facial detail | Identify only the transitions to soften |
| “Painterly” | Brush texture, altered palette, looser shapes | Specify selective contour merging or tonal blending |
| “High contrast” | Global lighting and palette changes | Ask for local object/background separation |
| “Dynamic diagonals” | Pose or camera changes | Name the object alignments and their endpoints |
| “More detail” | Extra edge clutter | Name the particular missing feature |
| “Sfumato” alone | General haze or historical-painting restyling | “Selective sfumato-like tonal merging, retaining clear focal details” |

#### 2.6 Reference extraction protocol

**Step 1 — Establish comparability**

Record native resolution, object scale, crop, intended display size, and visible quality limitations. Do not compare a large close-up to a tiny full-scene object without accounting for that difference.

**Step 2 — Annotate boundary roles**

At minimum:

- outer silhouette;
- overlap/contact;
- cast shadow;
- internal form shading;
- material seam;
- highlight;
- texture;
- explicit stroke;
- uncertain.

A role can be ambiguous; retain that ambiguity rather than forcing every edge into one category.

**Step 3 — Use both regional and whole-image summaries**

Whole-image statistics locate broad differences. Regional measurements diagnose them.

Useful region groups include:

- face/focal details;
- main character silhouette;
- foreground props;
- background structures;
- foliage;
- sky or other low-detail regions.

**Step 4 — Extract a compact style profile**

For each role/region:

```text
Edge contrast:
Transition width:
Contour continuity:
Contour geometry:
Explicit strokes: present / absent / uncertain
Stroke hierarchy, if applicable:
Directional structure:
Resolution confidence:
```

**Step 5 — Translate only stable findings**

Prompt stable relationships such as “outer marks heavier than internal marks.” Do not translate uncertain subpixel measurements into confident line-weight instructions.

#### 2.7 Generated-image evaluation

Use two complementary evaluation modes.

**A. Same-content correction**

If composition and objects should remain unchanged:

- compare corresponding boundaries after only the allowed alignment;
- report silhouette displacement;
- compare local profiles at matched semantic locations;
- inspect stroke addition/removal;
- inspect protected features.

Do not use an aggressive registration that conceals a prohibited pose or shape change.

A symmetric boundary-distance descriptor is:

\[
d_{\mathrm{sym}}=
\frac12\left[
\frac{1}{|A|}\sum_{a\in A}\min_{b\in B}\|a-b\|
+
\frac{1}{|B|}\sum_{b\in B}\min_{a\in A}\|b-a\|
\right]
\]

Report pixels and normalized distance. Arc-length sampling is preferable to arbitrary vertex-density weighting.

Boundary precision/recall at tolerance \(\tau D\) can also be useful, but \(\tau\) must come from acceptable alignment/annotation uncertainty and task calibration—not a borrowed universal threshold.

**B. Different-content style comparison**

Do not demand pixelwise contour overlap. Compare distributions within matched semantic roles:

- transition widths on main silhouettes;
- contrast at overlaps;
- outline/internal width hierarchy where applicable;
- interior edge activity;
- contour curvature at the same normalized scale;
- regional orientation distributions.

A different object inventory can change all-image edge density without changing rendering style.

**Human review remains necessary**

Check at intended display size:

- Are subjects separated clearly?
- Are forms still dimensional?
- Have new dark outline bands appeared?
- Are focal details preserved?
- Do soft transitions look selective rather than globally smeared?
- Are important contacts readable?
- Has the intended path or eyeline actually changed?
- Did unrelated attributes drift?

Metrics should support these questions, not replace them with a single score.

#### 2.8 Correction decision table

| Observed mismatch | Narrow correction | What to protect |
|---|---|---|
| Silhouette looks smeared | Narrow selected silhouette transitions | Shape, local contrast, rounded interior shading |
| Silhouette lacks separation but is already sharp | Adjust local color/value separation | Edge width and global palette |
| New dark rim appears | Remove the perimeter band; retain separation through adjacent values/colors | Silhouette geometry and contact shadows |
| Image is crispy or haloed | Reduce overshoot/sharpening in affected regions | Genuine focal detail |
| Interior looks noisy | Simplify incidental texture/marks | Seams, eyes, mouth, essential design details |
| Image has become flat | Restore broad form shading | Existing clean contours and palette |
| Shadow-side boundary is too explicit | Merge selected shadow-side segments | Important overlaps and focal boundaries |
| Outline hierarchy is wrong | Adjust actual outer/internal mark widths | Fill shapes, shading, stroke color |
| Curves are angular | Smooth selected geometry at the appropriate scale | Intentional corners and pose |
| Directional route is wrong | Edit the relevant path/object alignment | Camera, unrelated objects, rendering |
| Eyeline is wrong | Edit eyes and, only if authorized, head orientation | Expression, head proportions, unrelated geometry |

#### 2.9 Sharpening versus restyling

**Raster sharpening can** increase local acutance or compensate for some resampling softness. It can also introduce overshoot and halos. — [ImageMagick filters](https://usage.imagemagick.org/filter/)

**Raster sharpening cannot by itself reliably:**

- remove a continuous drawn outline while reconstructing the underlying forms;
- establish selective lost edges according to object semantics;
- redesign stroke hierarchy;
- simplify redundant drawn marks;
- change the route of an implied leading line;
- restore reference detail that was never resolved.

Those are restyling, reconstruction, or geometry-editing tasks.

Conversely, generative restyling is excessive when the only problem is a modest, localized sampling/sharpening issue. Select the smallest operation that addresses the diagnosed mismatch.

#### 2.10 Structural conditioning: use the right representation

| Control representation | Suitable purpose | Risk |
|---|---|---|
| Canny | Preserve selected strong boundary geometry | Carries texture, shadows, compression artifacts, and unwanted outlines if left uncurated |
| Learned soft-edge map | Preserve selected boundary structure with a model-dependent representation | “Soft” may mean confidence, not source transition softness |
| Straight-line map | Preserve architecture or approximately straight alignments | Poor representation of organic curves and implied routes |
| Segmentation map | Preserve object layout and region organization | Does not encode exact edge softness, highlights, or line weight |
| Manually curated contour map | Protect only selected silhouettes/contacts | Requires judgment and can omit necessary details |
| Masked local edit | Restrict the requested change spatially | Context and boundary blending can still change |

ControlNet conditioning strength is not “percent original image preserved.” Img2img strength and ControlNet strength are separate mechanisms. The official pipeline source makes that distinction explicit. — [Diffusers pipeline source](https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py)

#### 2.11 Calibration instead of arbitrary thresholds

Build a small, authorized calibration set containing:

- representative references;
- accepted and rejected generated examples;
- paired examples differing in one intended edge property;
- synthetic edges and bands with known geometry.

Suggested deterministic fixtures:

1. A step with several known transition widths.
2. The same step at several contrasts, without clipping.
3. A band with known width and taper.
4. A curve rendered at several subpixel positions.
5. The same source downsampled with declared filters.
6. A clean boundary with controlled overshoot.
7. A straight segment and an S-curve at several sizes.

Use these to establish:

- operator scaling;
- bias in measured widths;
- sensitivity to contrast;
- sampling uncertainty;
- mask-threshold sensitivity;
- repeatability.

For artistic acceptability:

- derive tolerances from accepted/rejected examples;
- preserve role-specific reference variation;
- report ranges or distributions rather than only means;
- test whether conclusions survive reasonable analysis settings.

Do not adopt documentation examples such as Canny `100, 200`, a particular ControlNet scale, or a chosen Gaussian sigma as project-wide acceptance thresholds.

#### 2.12 Controlled correction experiment

1. Freeze the baseline and record the exact requested change.
2. Specify protected attributes.
3. Change one main edge-related factor.
4. Use a paired seed/settings comparison when supported.
5. Re-evaluate both the target axis and protected attributes.
6. Check additional seeds or examples before treating the wording as generally reliable.
7. Reject a correction that improves sharpness while damaging identity, geometry, palette, or volume.

A compact correction record:

```text
Target:
Region:
Proposed mechanism:
Expected measurable change:
Protected attributes:
Reference uncertainty:
Generator and settings:
Observed target change:
Observed collateral changes:
Accept / reject / revise:
```

### Gaps

- Prompt vocabulary has not been benchmarked on a particular generator or project reference set.
- No zero-drift guarantee is supported.
- Quantitative acceptance bands require project-specific calibration.
- Structural controls constrain representations; they do not independently guarantee the requested stroke style, edge softness, or artistic hierarchy.

## 3. Which tools and current sources are practical, and what was validated?

### Takeaway

Start with CPU-capable deterministic measurements and a small amount of semantic annotation. Add trained detectors or segmentation only when their output answers a concrete missing question.

Current 2026 work improves learned edge-map crispness and controllability, but does not remove the distinction between a model’s prediction and the source image’s artistic boundaries.

### Cited Findings

#### 3.1 Deterministic libraries and CLI

| Tool | Concrete operations | License | Maintenance evidence checked | CPU / AMD assessment |
|---|---|---|---|---|
| **OpenCV** | Canny, Sobel/Scharr, Hough lines, line segments, contour geometry, distance transforms | Current repository: Apache-2.0 | Default-branch commit observed **2026-10-31**; inspected documentation resolved to **4.13.0** | Conventional CPU route is appropriate; AMD CPU requires no ROCm. GPU/OpenCL behavior depends on build and operator; not tested |
| **scikit-image** | Canny, structure tensor/eigenvalues, marching-squares contours, medial axis, morphology | Primarily BSD-3-Clause; license file lists additional permissive notices | Default-branch commit observed **2026-10-30**; stable feature documentation identified **0.26.0** | CPU-first practical option. No AMD GPU acceleration is assumed for the cited functions |
| **ImageMagick** | CLI inspection, controlled resizing, diagnostic blur/sharpening and derivative artifacts | ImageMagick License; do not relabel simply as Apache-2.0 | Default-branch commit observed **2026-10-31** | CPU route suitable; acceleration is unnecessary for the proposed basic diagnostics and untested here |

Official sources: [OpenCV](https://github.com/opencv/opencv), [OpenCV feature API](https://docs.opencv.org/4.13.0/dd/d1a/group__imgproc__feature.html), [scikit-image](https://github.com/scikit-image/scikit-image), [scikit-image license](https://github.com/scikit-image/scikit-image/blob/main/LICENSE.txt), [ImageMagick](https://github.com/ImageMagick/ImageMagick), [ImageMagick license](https://imagemagick.org/license/).

**OpenCV Canny implementation detail**

The tutorial discusses Gaussian noise reduction as part of the overall procedure, but the inspected `canny.cpp` does not contain a `GaussianBlur` call and shows derivative computation from the supplied source. Therefore, specify and record any explicit pre-smoothing rather than assuming every `cv.Canny` invocation performs the tutorial’s stated Gaussian prefilter. — [OpenCV Canny source](https://github.com/opencv/opencv/blob/4.x/modules/imgproc/src/canny.cpp)

OpenCV’s image-input Canny API takes an 8-bit image; its derivative-input overload takes specified signed derivative arrays. Its thresholds concern the implementation’s derivative response, not simply a percentage of source brightness. — [OpenCV feature API](https://docs.opencv.org/4.13.0/dd/d1a/group__imgproc__feature.html)

`skimage.feature.canny` exposes Gaussian `sigma`, hysteresis thresholds, quantile-threshold mode, masking, and boundary handling. Quantile thresholds can aid some comparisons, but also adapt to each image’s response distribution and therefore must not be treated as fixed physical sensitivity. — [scikit-image feature API](https://scikit-image.org/docs/stable/api/skimage.feature.html)

**Minimal documented API inventory**

```python
# Illustrative API inventory, not an executed or calibrated pipeline.

cv.Canny(gray8, low_threshold, high_threshold, L2gradient=True)
cv.HoughLinesP(edge_map, rho, theta, vote_threshold,
               minLineLength=min_length, maxLineGap=max_gap)
cv.createLineSegmentDetector().detect(gray8)

feature.canny(gray_float, sigma=sigma,
              low_threshold=low, high_threshold=high,
              mode="reflect")

feature.structure_tensor(gray_float, sigma=integration_sigma,
                         order="xy")
feature.structure_tensor_eigenvalues(tensor_elements)

measure.find_contours(binary_mask, level=0.5)
morphology.medial_axis(stroke_mask, return_distance=True, rng=seed)
```

Pin the library version before implementing. Context7 can surface main-branch or older examples; those should not override the installed release’s signature.

ImageMagick is useful for explicitly controlled resampling diagnostics. Keep such outputs separate from the untouched reference; do not repeatedly sharpen/resave the evidence image. — [ImageMagick resampling filters](https://usage.imagemagick.org/filter/)

#### 3.2 Trained alternatives and current 2026 developments

| Tool/work | What it provides | License/access evidence | Maintenance/currentness | CPU / AMD limitations |
|---|---|---|---|---|
| **DexiNed, original repository** | Learned edge maps | Repository MIT license; inference requires a trained checkpoint | Inspected default-branch commit **2023-03-08**; README lists older tested PyTorch versions | Source includes CPU device selection. End-to-end CPU operation and ROCm not tested |
| **OpenCV Zoo DexiNed** | ONNX/OpenCV-DNN deployment | Model directory explicitly MIT; Zoo repository itself Apache-2.0 | Zoo default-branch commit **2026-10-20**; inspected model README currently requests OpenCV **≥5.0.0** | CPU deployment is a practical candidate; backend/target support and AMD GPU behavior require verification |
| **MEMO, CVPR 2026** | Learned crisp-edge prediction, with progressive inference and multiple checkpoints | Code Apache-2.0; checkpoint/base-model terms should be checked separately | Paper and repository inspected; default-branch commit **2026-04-01** | Repository includes ONNX deployment and precision variants; no CPU/AMD benchmark validated |
| **EasyControlEdge, 2026** | Foundation-model adaptation for edge detection; authors report inference guidance controlling edge density | Public preprint inspected; no official implementation/license verified in this research | Submitted **2026-02-18** | Hardware, CPU/AMD support, and operational cost not established |
| **SAM 2** | Promptable region masks, useful for contour extraction | Code/checkpoints Apache-2.0 with documented third-party exceptions | Default-branch commit **2024-12-16**; repository push metadata extends into 2026 | Builder accepts a device; official examples and custom extension are CUDA-oriented. CPU/ROCm not validated |
| **SAM 3 / 3.1** | Concept/text/visual-prompt segmentation; masks, boxes, scores | Custom **SAM License**, not Apache-2.0; checkpoints require access approval/authentication | SAM 3.1 announced **2026-03-27**; default-branch commit observed **2026-10-23** | Official prerequisites specify CUDA-compatible GPU and CUDA ≥12.6. No official CPU/AMD route validated |
| **ControlNet** | Structural conditioning from Canny, soft edges, lines, segmentation, etc. | Repository Apache-2.0; underlying generators/checkpoints may have separate terms | Original repository default-branch commit **2023-09-09** | Original CUDA-oriented examples are not evidence of AMD support |
| **Diffusers** | Maintained generation/editing pipelines, including ControlNet/img2img/inpainting | Library Apache-2.0; model terms remain separate | Default-branch commit observed **2026-10-31** | CPU paths appear in official examples. ROCm feasibility depends on the complete model/operator stack; not tested |

Sources: [DexiNed](https://github.com/xavysp/DexiNed), [DexiNed device selection](https://github.com/xavysp/DexiNed/blob/master/main.py), [OpenCV Zoo DexiNed](https://github.com/opencv/opencv_zoo/tree/main/models/edge_detection_dexined), [MEMO](https://github.com/cplusx/MEMO_Edge_Detection), [EasyControlEdge](https://arxiv.org/abs/2602.16238), [SAM 2](https://github.com/facebookresearch/sam2), [SAM 3](https://github.com/facebookresearch/sam3), [ControlNet](https://github.com/lllyasviel/ControlNet), [Diffusers](https://github.com/huggingface/diffusers).

**Maintenance interpretation:** the dates above are repository observations, not support guarantees. A recent push is not necessarily a recent default-branch code change. In particular, SAM 2’s push timestamp and its latest default-branch commit differ substantially.

##### DexiNed preprocessing can change the measurement

The inspected OpenCV Zoo wrapper:

- constructs a **512×512** input blob;
- returns results resized to the source dimensions;
- applies sigmoid and per-output min/max normalization.

Consequences:

- anisotropic input resizing can affect orientation-sensitive interpretation;
- output localization inherits the internal sampling/preprocessing;
- normalized output brightness is not automatically a calibrated probability comparable across images.

These details matter if learned edge-map strength is used as an evaluation feature. — [OpenCV Zoo DexiNed wrapper](https://github.com/opencv/opencv_zoo/blob/main/models/edge_detection_dexined/dexined.py)

##### Current 2026 papers do not establish artistic ground truth

**MEMO:** the authors report crisper, human-like predicted edge maps and improved crispness-aware evaluation. The repository itself notes that one later-epoch model is crisper while having a slightly lower fine-tuned benchmarking score. This is a useful reminder that prediction crispness and other evaluation criteria can trade off. — [MEMO paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cheng_MEMO_Human-like_Crisp_Edge_Detection_Using_Masked_Edge_Prediction_CVPR_2026_paper.html); [MEMO repository](https://github.com/cplusx/MEMO_Edge_Detection)

**EasyControlEdge:** the authors report controlling predicted edge density through inference guidance. Accordingly, the density of a learned edge map must be interpreted with its inference settings; it is not an immutable property of the source’s line economy. — [EasyControlEdge](https://arxiv.org/abs/2602.16238)

Neither inspected work establishes reliable identification of intentional strokes in outline-free casual illustration.

##### AMD: avoid both false positives and false negatives

PyTorch’s official HIP documentation states:

> “PyTorch for HIP intentionally reuses the existing `torch.cuda` interfaces.”

Therefore, encountering `.cuda()` or `device="cuda"` in generic PyTorch code does not alone prove that it is NVIDIA-only. Conversely, that naming compatibility does not prove that custom CUDA extensions, attention kernels, or the complete application work on AMD. — [PyTorch HIP semantics](https://github.com/pytorch/pytorch/blob/main/docs/source/notes/hip.rst)

For this project:

- deterministic CPU analysis is the lowest-friction baseline;
- do not assume ROCm compatibility from PyTorch compatibility alone;
- do not assume official SAM 3 CUDA prerequisites cover AMD;
- no GPU throughput, memory requirement, or compatibility claim was tested here.

##### Download and execution behavior requires attention

The inspected MEMO README documents automatic checkpoint downloading in its interactive tooling and automatic example-image fetching in some demos. Those are not appropriate to run under the present no-download/no-upload constraints. Inspection of the public documentation did **not** execute them. — [MEMO repository](https://github.com/cplusx/MEMO_Edge_Detection)

SAM 3 checkpoint access is gated. No access request, login, authentication, or checkpoint retrieval was attempted. — [SAM 3](https://github.com/facebookresearch/sam3)

#### 3.3 Primary-source register

**All sources accessed 2026-10-31.** There are **15 primary-source records** below; software records group closely related official documentation, source, and licensing pages.

| ID | Primary source | Claims supported | Confidence and limits |
|---|---|---|---|
| **S1** | [Canny, *A computational approach to edge detection*, 1986](https://pubmed.ncbi.nlm.nih.gov/21869365/) | Detection/localization/single-response criteria; scale trade-off; multiscale operators | High for the retrieved original abstract; no artistic-style validation |
| **S2** | [OpenCV feature API](https://docs.opencv.org/4.13.0/dd/d1a/group__imgproc__feature.html), [shape API](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html), [LSD](https://docs.opencv.org/4.13.0/db/d73/classcv_1_1LineSegmentDetector.html), [Canny source](https://github.com/opencv/opencv/blob/4.x/modules/imgproc/src/canny.cpp), [repository](https://github.com/opencv/opencv) | Parameters/units, binary edges, contour geometry, implementation detail, project license | High for documented/source behavior; no local execution |
| **S3** | [scikit-image feature API](https://scikit-image.org/docs/stable/api/skimage.feature.html), [measure API](https://scikit-image.org/docs/stable/api/skimage.measure.html), [morphology](https://scikit-image.org/docs/0.26.x/api/skimage.morphology.html), [license](https://github.com/scikit-image/scikit-image/blob/main/LICENSE.txt) | Canny, tensor analysis, iso-contours, medial axis/distance, licenses | High; stable/main version differences must be respected |
| **S4** | [ImageMagick resampling filters](https://usage.imagemagick.org/filter/), [license](https://imagemagick.org/license/), [repository](https://github.com/ImageMagick/ImageMagick) | Ringing, aliasing, blur/filter trade-offs, CLI suitability, licensing | High for documented behavior; not a calibrated diagnostic classifier |
| **S5** | [National Gallery, Sfumato](https://www.nationalgallery.org.uk/paintings/glossary/sfumato) | Art-historical definition, gradual modulation, absence of harsh outlines | High for terminology; not a computational definition |
| **S6** | [DexiNed repository](https://github.com/xavysp/DexiNed), [license](https://github.com/xavysp/DexiNed/blob/master/LICENSE), [runner source](https://github.com/xavysp/DexiNed/blob/master/main.py) | Learned edge model, MIT code, checkpoint requirement, CPU-selection path | High for source facts; hardware execution untested |
| **S7** | [OpenCV Zoo DexiNed](https://github.com/opencv/opencv_zoo/tree/main/models/edge_detection_dexined), [wrapper](https://github.com/opencv/opencv_zoo/blob/main/models/edge_detection_dexined/dexined.py) | ONNX deployment, model-directory license, current version requirement, preprocessing/postprocessing | High for inspected code; no inference benchmark |
| **S8** | [SAM 2 repository](https://github.com/facebookresearch/sam2), [builder](https://github.com/facebookresearch/sam2/blob/main/sam2/build_sam.py) | Masks, device parameter, CUDA-oriented setup, Apache licensing/exceptions | High for source facts; not proof of cross-device support |
| **S9** | [ControlNet repository](https://github.com/lllyasviel/ControlNet) | Canny/HED/MLSD/segmentation conditions; original control approach and stated detail changes | High for documented controls; old repository examples are not current hardware guarantees |
| **S10** | [Diffusers ControlNet guide](https://huggingface.co/docs/diffusers/using-diffusers/controlnet), [native img2img source](https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py), [repository](https://github.com/huggingface/diffusers) | Conditioning multiplier, control schedule, img2img strength, multi-control handling | High for the inspected pipeline; not universal across architectures |
| **S11** | [PyTorch HIP semantics](https://github.com/pytorch/pytorch/blob/main/docs/source/notes/hip.rst) | ROCm/HIP reuse of `torch.cuda` interfaces | High; complete application compatibility remains conditional |
| **S12** | [W3C relative-luminance explanatory page](https://www.w3.org/WAI/GL/wiki/Relative_luminance) | Linearized sRGB luminance calculation and breakpoint correction | High for the cited calculation; explanatory working-group page, not an artistic metric |
| **S13** | [MEMO, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Cheng_MEMO_Human-like_Crisp_Edge_Detection_Using_Masked_Edge_Prediction_CVPR_2026_paper.html), [official repository](https://github.com/cplusx/MEMO_Edge_Detection), [license](https://github.com/cplusx/MEMO_Edge_Detection/blob/main/LICENSE) | Prediction crispness, progressive inference, reported benchmark behavior, deployment options | High for authors’ published claims and code; independent stylized-art performance unknown |
| **S14** | [EasyControlEdge, 2026](https://arxiv.org/abs/2602.16238) | Foundation-model edge adaptation; authors’ reported density guidance and benchmark results | High for what the preprint states; independent validation, implementation license, and hardware unknown |
| **S15** | [SAM 3 repository](https://github.com/facebookresearch/sam3), [license](https://github.com/facebookresearch/sam3/blob/main/LICENSE) | Concept segmentation, masks/boxes/scores, 2026 update, CUDA prerequisites, custom license and gated checkpoints | High for official statements; no CPU/AMD execution validated |

#### 3.4 Source-validation observations

- OpenCV’s rolling documentation redirected to **4.13.0** during inspection.
- scikit-image’s fetched stable feature page identified **0.26.0**.
- Context7 returned a mixture of official source snippets, historical notes, and a community example located inside the official Diffusers repository. Exact Diffusers parameter semantics were therefore checked in the **native pipeline source**, not inferred from the community example.
- GitHub license metadata classified scikit-image and ImageMagick as “Other.” Their actual license text was inspected rather than treating the metadata label as the legal description.
- DexiNed’s extracted repository summary omitted licensing; the actual MIT license file was subsequently checked.
- The current OpenCV Zoo DexiNed README requests OpenCV ≥5.0.0, while the inspected OpenCV 4.x documentation resolved to 4.13.0. These should not be mixed into an assumed tested deployment.
- Some repository summaries and examples are dated. Maintenance observations were checked against public GitHub metadata rather than equating README age with current support.
- No community fork’s CPU or AMD support was attributed to an upstream project.

### Inferences

#### Recommended minimal implementation order

1. **Manual semantic boundary annotation plus deterministic CPU measurements.**
2. Add segmentation only when object contour geometry cannot be obtained adequately from existing masks or simple annotation.
3. Add a learned edge map only when it provides useful additional boundary proposals.
4. Keep learned outputs alongside—not in place of—the original image and deterministic measurements.
5. Introduce structural generation controls only after deciding which geometry must be protected.
6. Keep evaluation features separate from generation-control maps.

A practical first deliverable is a small per-reference table and annotated contact sheet, not a large custom analysis framework.

#### Verification status and research spend

**Performed**

- **10 Kagi searches** for discovery.
- **9 Context7 lookups:** four library resolutions and five documentation queries.
- Targeted public documentation/source fetches and GitHub REST metadata checks.
- One `gh_grep` query; it returned no matches and contributed no implementation evidence.
- One Memory search; no relevant project decision was established.
- Current CLI help checked for Kagi and Context7.

**Not performed**

- No Perplexity or Deep Research calls.
- No Kagi Assistant calls.
- No private uploads, account access, or new logins.
- No package installation, software upgrade, or model-weight download.
- No fetched repository code executed.
- No image-analysis benchmark or generator experiment.
- No numeric project acceptance thresholds established.

Kagi discovery used the ordinary subscription-backed search route. No separate paid synthesis or Assistant allowance was intentionally used; monetary cost was not independently calculated.

The parent owns integration and synthesis validation; this research validates the cited source claims and states the remaining implementation/calibration gaps.

### Gaps

- No actual project reference or generated image was inspected, so none of the proposed style characteristics should be represented as measured project findings.
- Low-resolution references may not support reliable distinction between narrow strokes, antialiasing, and soft transitions.
- No trained model was validated specifically on polished dimensional casual art.
- CPU/AMD feasibility beyond documented paths remains untested; no throughput or VRAM estimates are supplied.
- Checkpoint and underlying-model licenses require separate review where the repository license is insufficient.
- The 2026 survey is targeted, not an exhaustive ranking of every contemporary edge or segmentation model.
- Attempts to retrieve additional older scale-selection and curvilinear-detection literature encountered access/extraction problems; no claims here depend on inaccessible full texts.
- No validated universal mapping exists here from detector output to artistic intention, from diagonal orientation to emotion, or from image lines to viewer gaze.
