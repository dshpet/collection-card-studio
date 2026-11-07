# Measure visual style without inventing certainty

**A useful numerical style profile is feasible; a definitive, content-independent fingerprint with perfectly isolated controls is not.** Many image properties—dimensions, color coordinates, mask geometry, edge transitions, frequency distributions, and annotated spatial relationships—can be measured reproducibly. Their interpretation as lighting, material, artistic intention, readability, or stylistic compatibility requires additional assumptions, calibration, or human evidence. The strongest practical approach separates **what is visible, what is inferred, what is desired, and what a particular backend can actually control**. It then combines category-aware reference distributions, interpretable measurements, specialist critique, and bounded corrections with regression checks. Current research already covers structural conditioning, style disentanglement, localized recoloring, relighting, and agentic editing; the project opportunity is to validate their combination for these collectible cards, not to invent a universal style vector. The present reduced references support conceptual analysis and a qualitative brief, but **no reference measurements, calibrated thresholds, model benchmarks, or implementation results are claimed in this report**.

**Research cutoff:** 2026-10-31.  
**Status:** research synthesis and prototype recommendations, not an adopted architecture or implementation.

## Contents

| Section | Main question |
|---|---|
| [1. Separate measurable appearance from inferred causes](#1-separate-measurable-appearance-from-inferred-causes) | What can honestly receive a number? |
| [2. Organize style into stable, conditional axes](#2-organize-style-into-stable-conditional-axes) | What categories, terminology, features, and controls are useful? |
| [3. Match each intervention to an appropriate tool](#3-match-each-intervention-to-an-appropriate-tool) | Which tools and preservation guarantees are real? |
| [4. Calibrate acceptance before automating correction](#4-calibrate-acceptance-before-automating-correction) | How should evaluation, uncertainty, and iteration work? |
| [5. Prototype the smallest useful research system](#5-prototype-the-smallest-useful-research-system) | What should be investigated first? |
| [Conclusion](#conclusion) | What changes in the underlying approach? |
| [Primary-source bibliography](#primary-source-bibliography) | Which sources support which claims? |
| [Detailed research appendices](#detailed-research-appendices) | Where are all thirteen underlying notes? |

## 1. Separate measurable appearance from inferred causes

### A deterministic number is not automatically a valid property measurement

The proposed decomposition is valuable as an **analysis and control vocabulary**, but it should not be mistaken for a discovered set of independent physical variables. A descriptor can be exactly reproducible while measuring the wrong construct. A background gradient can produce high local entropy without containing meaningful detail. A Canny map can contain many edges without containing many drawn strokes. A large bright region can dominate a contrast map without being the intended subject.

“Formal analysis” is also broader than interpretation-free quantification. Getty describes identifying visual elements and evaluating their compositional roles; Duke’s visual-analysis guide explicitly includes claims about the work and allows interpretation. For this project, **quantitative image description** is the narrower term for numerical operations, while **formal/visual analysis** includes structured interpretation grounded in visible evidence. ([Getty](https://www.getty.edu/education/teachers/classroom_resources/formal_analysis.html); [Duke](https://wrp.duke.edu/sites/twp.duke.edu/files/file-attachments/visual-analysis.original.pdf))

The following verdicts should accompany proposed features.

| Verdict | Meaning | Examples | Appropriate claim |
|---|---|---|---|
| **D — direct deterministic** | Computed from declared pixels, metadata, or supplied layers | Width, height, encoded-channel histogram, known alpha coverage | “The delivered image is this size.” |
| **C — conditional deterministic** | Exact arithmetic after selecting masks, landmarks, regions, correspondence, or calibration | Subject occupancy, contour curvature, annotated joint angle | “Given this reviewed mask, occupancy is this fraction.” |
| **L — learned estimate** | Depends on model training, preprocessing, and domain fit | Predicted depth, masks, normals, fixation density | “This model predicts this map.” |
| **N — not identifiable** | Different underlying explanations can produce the same observation | Original light count, physical roughness, exact focal length without calibration | “The image does not uniquely determine this parameter.” |
| **H — human/task-calibrated** | Requires a specified perceptual task or acceptance policy | Recognition, expression readability, style compatibility, release acceptance | “Under this test, reviewers accepted or recognized it.” |

These are not mutually exclusive pipeline labels. Automatic segmentation followed by area calculation is **L→C**, not direct measurement. A deterministic implementation of a neural model remains a learned estimate. A human interpretation can be well supported without becoming a physical measurement.

### The feasibility matrix favors appearance-first evaluation

| Requested category | Strong numerical outputs | Conditional or learned outputs | Not established from arbitrary flattened art |
|---|---|---|---|
| Lighting and value | Relative-luminance distributions, tonal spread, regional contrast | Shadow masks, edge softness, rim coverage, inferred direction | Unique lights, incident key/fill ratio, source size/distance, original exposure |
| Color and palette | Characterized color coordinates, distributions, color differences | Semantic-role palettes, warm/cool convention, harmony-template fit | Unique illuminant CCT, universal harmony or preference |
| Composition and format | Dimensions and aspect ratio | Occupancy, margins, centroids, symmetry, relation graphs | Designer intention or universally optimal composition |
| Lines and edges | Gradients, detector maps, selected line geometry | Stroke width, lost-edge fraction, implied vectors | Original pen strokes, universal directional “energy” |
| Depth and optics | Selected line intersections, edge-spread profiles | Vanishing families, learned depth/normals, viewpoint hypotheses | Unique metric depth, sensor, focal length, camera distance |
| Shape and scale | Supplied-mask geometry | Part proportions, contour complexity, silhouette tests | True physical size, hidden geometry, unique volume |
| Texture and material | Multiscale energy, GLCM/LBP, spectra | Highlight descriptors, brush organization, gloss judgments | Actual BRDF, material composition, real painting medium |
| Attention and readability | Contrast/detail allocation | Predicted fixation density, task performance | Guaranteed first fixation or comprehension from one saliency map |
| Rhythm and repetition | Annotated count, spacing, orientation, recurrence | Motif recognition, pattern-rule hypotheses | Universal emotional tempo or visual “BPM” |
| Gesture, expression, staging | Accepted landmark and relation geometry | Pose/face estimates, perceived expression | Hidden anatomy, actual emotion, intention |
| Overall style | Versioned feature vector and retrieval similarities | Locally calibrated human acceptance | A universal “92% style match” |

The physical limitations are substantive, not merely current-model weaknesses. The generalized bas-relief result establishes non-unique geometry, reflectance, and lighting under its stated assumptions. Contemporary inverse-rendering systems address ambiguity with priors and optimization, not by making the original scene uniquely observable. ([Belhumeur, Kriegman, and Yuille, 1999](https://link.springer.com/article/10.1023/A:1008154927611); [IntrinsicAnything, 2024](https://arxiv.org/abs/2404.11593))

### The project needs category-conditioned consistency, not one reference average

The local art guide defines a progression: category 1 floats a relatively simple object; category 2 places it on a surface with a simple vertical backdrop; category 3 introduces realistic surface grounding; category 4 integrates the object into an environment while keeping it central. Category 5 introduces one or two characters acting out a simple scene and is outside the requested non-gold deliverables. All four object categories belong in a set regardless of rarity. ([Project art guide](../materials/03_art_guide.md); [task description](../materials/01_task_description.md))

Consequently, “simple background,” “contact shadow,” “scene depth,” and “detail budget” cannot have one target across the collection. A contact-shadow requirement appropriate to a grounded object would contradict a floating-object card. A realistic category-4 setting should not be penalized merely for having more environmental structure than category 1.

The reference-applicability lane records individual crops at approximately **59 × 67 pixels**, with one 58 × 67 crop. It supports coarse observations of focal prominence, broad category composition, and polished dimensional illustration, but not trustworthy fine-scale targets for material, texture, edge softness, or lighting. This report relies on that documented inspection rather than claiming a new visual analysis. ([Reference-applicability note](measuring-visual-style-notes/13%20reference%20applicability.md))

This does **not** make numerical geometry impossible. Canvas dimensions remain exact. A reviewed mask can produce an exact occupancy measurement **of that reduced raster**. The limitation is interpretation: that number is not automatically a trustworthy full-quality style target. Upscaling adds samples, not recovered evidence.

### One input contract prevents contradictory specialist measurements

Every specialist should receive the same measurement manifest. Otherwise, apparent disagreement can arise from different crops, color conversions, masks, or resolutions rather than different judgments.

| Contract component | Required information |
|---|---|
| Source | Asset identifier, immutable hash, provenance, known export/resampling history |
| Geometry | Native dimensions, orientation, artwork aperture, crop coordinates, coordinate transforms |
| Color | Embedded profile, assumed profile if absent, working space, transfer function, white point, precision |
| Transparency | Straight/premultiplied policy, semantic extent versus opacity, deployment backdrop |
| Regions | Visible subject, attached parts, background, support, shadows, effects, UI, protected details |
| Scale | Native analysis, common aspect-preserving scale, subject-relative scale, actual deployment sizes |
| Algorithms | Library/model/checkpoint versions, settings, random state, normalization, valid-support policy |
| Evidence | Overlays, selected profiles, landmark labels, excluded samples, uncertainty reasons |
| Applicability | Applicable, not applicable, unknown, or not measurable at this resolution |

**Do not equate alpha with a semantic object mask.** An opaque finished card has alpha everywhere; an isolated sprite can include translucent shadows or glow. Preserve visible-object geometry separately from its presentation footprint.

Filter the image before regional aggregation, or account explicitly for filter support. Blacking out the background before filtering manufactures a new boundary. Texture statistics should exclude silhouette contamination; GLCM pairs require both endpoints inside the region; CNN receptive fields can leak information across masks.

Maintain separate scales rather than one universal “canonical 1024.” Native pixels diagnose export artifacts; a common aspect-preserving scale supports cross-image comparison; object-relative scale compares marks relative to the object; deployment pixels test readability. The underlying notes propose different example canonical resolutions. Those are exploratory settings, **not conflicting standards to average together**.

Color management is equally structural. ICC profiles describe conversions between device-dependent and device-independent representations. Decoding sRGB provides linear-light values for the delivered rendering; it does not reverse tone mapping or recover scene radiance. Clean-FID demonstrates that resizing and compression can materially change evaluation results. ([ICC](https://www.color.org/iccprofile.xalter); [Clean-FID](https://github.com/GaParmar/clean-fid))

## 2. Organize style into stable, conditional axes

### A stable ontology separates visual intent from backend parameters

The following is a **proposed project ontology**, not an existing API or a claim about a generator’s internal representation.

| Stable group | Meaningful nested fields |
|---|---|
| `content_and_context` | Object identity, thematic role, instance count, category, required parts, exclusions |
| `lighting` | Source roles, directions, source geometry, fill, environment, shadows, rim, motivated lights |
| `value_and_tone` | Value placement, broad groups, contrast scales, highlight/shadow allocation, exposure operation, grade |
| `chromatic_design` | Working space, hue families, chroma, neutral share, role palettes, harmony relationships |
| `composition_and_format` | Canvas, aperture, framing, occupancy, margins, anchors, balance, positive/negative space |
| `edges_lines_and_vectors` | Boundary contrast/softness, contour articulation, explicit strokes, curvature, directional relations |
| `depth_viewpoint_and_optics` | Projection, object-relative view, convergence, occlusion, atmospheric separation, apparent blur |
| `shape_scale_and_form` | Silhouette, part ratios, thickness, corner language, exaggeration baseline, apparent volume |
| `surface_and_finish` | Material appearance, shading construction, mark scale, texture organization, grain, glow, acutance |
| `hierarchy_and_readability` | Focal roles, separation, detail allocation, competitors, deployment recognition |
| `rhythm_and_repetition` | Motifs, count, pitch, gaps, orientation, progression, alternation, exceptions |
| `gesture_expression_and_staging` | Action curves, landmarks, facial mechanisms, eyelines, contact, support, narrative relations |
| `delivery_and_provenance` | Dimensions, file format, profile, alpha, compression, lineage, permitted reference use |

Each field should distinguish **control intent**, **observed appearance**, **inferred explanation with confidence**, **evaluator features**, and **backend capability**. “Upper-left key” belongs to intent or inference; “left-side lightness exceeds right-side lightness” is an observation; a renderer light rotation is a backend control.

### Lighting requires roles, directions, and image values to remain separate

**Key is a role; front is a direction; soft is an appearance or source-extent relationship.** They are not alternatives in one enumeration.

| Lighting field | Meaning | Prompt-ready wording |
|---|---|---|
| Key | Dominant illumination organizing the form | “A broad upper-left key models the object.” |
| Fill | Illumination opening shadow regions | “Gentle frontal fill keeps the shadow side readable.” |
| Rim | Narrow illuminated boundary appearance | “A restrained rim on the rear-right edge, not a white outline.” |
| Backlight | Source behind the subject relative to camera | “Soft rear illumination separates the silhouette.” |
| Background light | Illumination primarily affecting the background | “Keep the backdrop softly lit without raising subject highlights.” |
| Ambient/environment | Broad surrounding illumination | “Broad environmental fill with no isolated secondary shadow.” |
| Practical | Visible depicted light source | “The visible lamp motivates the local illumination.” |
| Negative fill | Reduced surrounding bounce/fill | “Reduce right-side fill without moving the key.” |

A key can therefore be **frontal, high, broad, warm, and dominant** simultaneously. Source type—point, spot, area, sun—is another field. Blender and PBRT document these forward-rendering distinctions and their effects. ([Blender lights](https://docs.blender.org/manual/en/latest/render/lights/light_object.html); [PBRT area lights](https://www.pbr-book.org/4ed/Light_Sources/Area_Lights))

#### Declare a lighting coordinate convention

A useful proposed camera-relative convention describes the direction **from subject toward source**:

\[
x=\text{image right},\quad y=\text{image up},\quad z=\text{toward camera}.
\]

Set azimuth \(a=0^\circ\) frontal, \(+90^\circ\) image-right, \(-90^\circ\) image-left, and \(180^\circ\) behind. Elevation \(e=0^\circ\) is horizontal and \(+90^\circ\) overhead:

\[
\mathbf l(a,e)=
(\cos e\sin a,\;\sin e,\;\cos e\cos a).
\]

This is a **control convention**, not a recovered reference measurement. A renderer adapter must translate it into its own axes and distinguish source position from light-emission direction.

For a shadow vector measured in raster coordinates, where \(y\) increases downward, use a separately named image-plane angle:

\[
\theta_{\rm image}=\operatorname{atan2}(-\Delta y,\Delta x).
\]

It is not a 3D light azimuth.

#### Softness does not identify emitter size

For a known face-on circular source of diameter \(D_s\) at distance \(d_s\), angular diameter is

\[
\alpha=2\arctan\!\left(\frac{D_s}{2d_s}\right).
\]

Larger apparent sources generally soften shadows, but observed shadow transitions also depend on blocker–receiver separation, source shape, multiple illumination, painting, blur, and resampling. Enlarging an area source changes highlights and body shading as well as shadows. Spotlight beam blending is not the same as shadow softness. ([Blender lights](https://docs.blender.org/manual/en/latest/render/lights/light_object.html); [PBRT](https://www.pbr-book.org/4ed/Light_Sources/Area_Lights))

Measure appearance by sampling reviewed shadow boundaries on comparable receiving surfaces:

\[
t(s)=\frac{Y(s)-Y_{\rm shadow}}{Y_{\rm lit}-Y_{\rm shadow}},
\qquad
w_{10-90}=|s_{0.9}-s_{0.1}|.
\]

Report pixels, normalized width \(w_{10-90}/d_{\rm subject}\), spread, and valid profile count. Reject insufficient-contrast or strongly nonmonotonic profiles. This is **C**, not a physical source-size measurement.

#### “4:1 lighting” is underspecified

Two conventions occur:

\[
r_{\rm source}=K/F,\qquad
r_{\rm sides}=(K+F)/F.
\]

The second assumes fill reaches both sides while key contributes mainly to the lit side. Under that simplification, \(r_{\rm sides}=r_{\rm source}+1\). Thus \(K/F=4\) is a two-stop source difference, whereas \((K+F)/F=5\) is about 2.32 stops. These conventions are documented in filmmaking references, not established as a universal photometric shorthand. ([How To Film School](https://howtofilmschool.com/dictionary/key-to-fill-ratio/); [PhotoCalcs](https://photocalcs.uk/lighting/key-to-fill-ratio-calculator/))

Define contributions at a specified location/orientation or through a renderer’s separate light contributions. Lamp power percentages are not incident illumination ratios. A ratio between two image patches additionally mixes reflectance, orientation, specularity, occlusion, and grading. Label it **image-patch luminance ratio**, never measured key/fill.

#### Useful lighting features and controls

| Feature | Units/region | Verdict | Main use |
|---|---|---|---|
| Cast-shadow displacement | Pixels, subject-normalized length, degrees; annotated receiver | C | Short versus extended grounding |
| Shadow coverage/attenuation | Fraction; comparable receiver patches | C | Relative shadow appearance |
| Contact gap | Pixels or normalized distance | C | Detect detached grounding where applicable |
| Shadow-edge transition | Pixels and normalized width | C | Apparent softness |
| Rim coverage/width | Boundary fraction and normalized width | C | Rim-like articulation |
| Broad shading field | Regional lightness/low-frequency variation | C | Form-modeling appearance |
| Estimated normals/lighting | Model-native coordinates | L | Hypothesis or conditioning map |
| Actual source parameters | Renderer units | Known only in authored scene | Exact forward control |

CPU filters and reviewed annotations provide the deterministic baseline. Intrinsic decomposition, normals, and relighting are optional learned branches. IC-Light’s “Lighting Preference” is a latent initialization pattern, not a calibrated source azimuth. PIXLRelight’s 2026 work connects target intrinsic maps and PBR render passes to learned relighting, but does not uniquely recover the original scene. ([IC-Light](https://github.com/lllyasviel/IC-Light); [PIXLRelight](https://arxiv.org/abs/2605.18735))

A suitable correction says: “Shorten the soft cast shadow while retaining object placement and silhouette; allow the shadow region to change.” An unsuitable correction says: “Move the light but preserve every highlight, shadow, reflection, and tone.”

### Value and tone need explicit coordinates instead of one “tone” slider

“Tone” can mean light–dark organization, color cast, photographic tone reproduction, or mood. Replace it with named fields: **value placement**, **contrast**, **exposure operation**, **highlight/shadow roll-off**, and **color grade**.

For encoded sRGB \(c'\in[0,1]\),

\[
c=
\begin{cases}
c'/12.92,&c'\le0.04045\\
((c'+0.055)/1.055)^{2.4},&\text{otherwise},
\end{cases}
\]

then

\[
Y=0.2126R+0.7152G+0.0722B.
\]

This is dimensionless relative luminance, not display nits or original scene illumination. CIELAB \(L^*\) and Oklab \(L\) are different lightness coordinates; HSV \(V\) is different again. ([W3C relative luminance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html); [CSS Color 4](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/))

A useful vector contains regional \(Y\) or lightness quantiles, tonal spread \(Q_{90}-Q_{10}\), RMS variation, declared dark/mid/light occupancy, endpoint occupancy, and coarse spatial value fields. A percentile ratio or

\[
\Delta_Y=\log_2(Q_{90}/Q_{10})
\]

requires a valid denominator and is only a **rendered-value log-range**, not camera dynamic range or a lighting ratio.

High-key means predominantly light appearance under a declared convention; it does not necessarily mean low contrast. A bright backdrop and dark object can have both high median image value and strong separation. Exposure in a known linear operation multiplies by \(2^{EV}\); a final PNG does not reveal original exposure.

Scikit-image, Colour, and OpenCV provide the necessary CPU operations. One implementation trap matters: `rgb2gray` applied to encoded sRGB is a weighted encoded-channel sum, not automatic sRGB decoding followed by W3C \(Y\). Pin the intended conversion. ([Scikit-image color source](https://github.com/scikit-image/scikit-image/blob/51b3367761a52ab9111bdbd9537272d7dd2eccde/src/_skimage2/color/colorconv.py))

Prompt wording should name the desired effect: “Keep the broad three-value grouping; open the object’s shadow-side midtones without flattening the bright accents.” Curves and masked grading are preferable to regeneration when the mismatch is genuinely tonal. They preserve geometry, but can alter perceived material, palette, clipping, and hierarchy.

### Chromatic design needs distributions and semantic roles, not only swatches

Hue, chroma, saturation, brightness, and lightness are not interchangeable. Oklab/OKLCh offers a practical SDR analysis representation; CIELAB with a declared white/observer supports established color-difference workflows; CAM16 requires meaningful viewing-condition assumptions. More elaborate appearance modeling does not create known adaptation conditions. ([CIE terminology](https://cie.co.at/eilvterm/17-22-074); [Oklab](https://bottosson.github.io/posts/oklab/); [Colour CAM16-UCS](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html))

For Oklab:

\[
C=\sqrt{a^2+b^2},\qquad
h=\operatorname{atan2}(b,a)\bmod 2\pi.
\]

Chroma is not a normalized percentage, and its gamut limit depends on lightness and hue. Hue becomes unstable near neutral: small \(a,b\) perturbations produce angular changes proportional to \(1/C\). Retain a neutral bucket rather than assigning meaningful hue to gray.

| Feature | Representation | Qualification |
|---|---|---|
| Role palette | Swatches/medoids plus area masses | Fix clustering, sampling, initialization, and matching |
| Lightness/chroma | Quantiles by subject, background, accent, material | Separate role area from within-role color |
| Hue families | Circular histograms, concentration, retained-mass arc | Exclude/downweight low chroma |
| Palette diversity | Fixed-bin entropy, quantization residual at declared \(k\) | Neither is aesthetic quality |
| Warm/cool relationship | Declared hue sectors or chromatic projection | Artistic convention, not kelvin |
| Opposed/analogous scheme | Circular separations or template residual | Description, not universal harmony |
| Color discrepancy | Corresponding-patch \(\Delta E\), role-distribution transport | Requires compatible coordinates and comparison unit |

Pixelwise \(\Delta E\) needs meaningful correspondence. It is suitable for registered recolors or matched patches, not independently composed images. CIEDE2000 has nontrivial hue branches and weighting terms; Sharma’s test pairs exist because plausible implementations can be wrong. ([Sharma, Wu, and Dalal](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/))

For cross-content comparison, prefer role-conditioned distributions:

\[
P(L,a,b\mid \text{background}),\quad
P(L,a,b\mid \text{subject material}),\quad
P(a,b\mid \text{lightness band, role}).
\]

Weighted palette transport can compare both color locations and masses:

\[
\min_{\gamma\ge0}\sum_{ij}\gamma_{ij}d(x_i,y_j),
\]

with prescribed marginal masses. POT supplies transport tools, but `emd2` means the cost for the supplied matrix—not automatically squared perceptual distance. Fixed-bin Jensen–Shannon divergence is another option; it does not know adjacent bins are perceptually closer than distant bins. ([POT](https://pythonot.github.io/))

**Complementary colors are not universally more harmonious.** Empirical work distinguishes harmony, preference, similarity, and figure–ground preference. Harmony-template adherence is a model-specific descriptor. ([Cohen-Or et al., 2006](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf); [Schloss and Palmer, 2011](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf))

Likewise, an illustration’s average orange color does not establish an illuminant CCT. CCT concerns source chromaticity near the Planckian locus, not arbitrary object/palette averages. “Warm palette,” “warm highlights,” “temperature-slider adjustment,” and “known source CCT” need separate fields. ([CIE CCT](https://cie.co.at/eilvterm/17-23-068))

A precise request is: “Reduce background chroma while preserving its lightness pattern; retain the subject’s red-orange family and neutral highlights.” A masked Oklab chroma edit can preserve numerical \(L\) before gamut mapping, but not necessarily luminance or perceived contrast. Gamut mapping itself can change hue, chroma, and lightness.

Current prior art includes SW-Guidance, Palette Aligned Image Diffusion, and ColourCrafter. They demonstrate color-distribution or regional color control, not independent-axis guarantees. Palette matching can also be gamed through posterization. ([SW-Guidance](https://github.com/alobashev/sw-guidance); [Palette Aligned Image Diffusion, 2025](https://arxiv.org/html/2509.02000); [ColourCrafter, 2026](https://eccv.ecva.net/virtual/2026/poster/4439))

### Composition and format admit strong geometry but conditional aesthetic interpretation

Use a declared artwork rectangle \(R=(L,T,W_R,H_R)\), valid aperture \(V\), and subject mask \(M\). Normalize placement as

\[
u=(x-L)/W_R,\qquad v=(y-T)/H_R.
\]

For distances and angles, preserve physical aspect: use pixels or isotropic normalization, not independent x/y scaling. Distorting a rectangular card into a square changes angles and shape relationships.

| Feature | Formula/units | Interpretation |
|---|---|---|
| Format | \(W,H,W/H\) | Direct delivered geometry |
| Occupancy | \(|M|/|V|\) | Selected subject area, not its bounding-box area |
| Box extent | Width/\(W_R\), height/\(H_R\) | Retains tall/narrow versus broad/short |
| Centroid | \(\sum pM/\sum M\) | Uniform mask mass, not attention |
| Margins | Left/right/top/bottom fractions | Relative to declared aperture |
| Clearance | Minimum distance to aperture boundary | Sensitive to thin tips and mask error |
| Complement space | \(V\setminus M\) | Geometric “not subject,” not necessarily quiet |
| Symmetry | IoU with reflection around declared axis | Geometry, not beauty |
| Balance | Declared area/moment/contrast weighting | Different weights answer different questions |
| Arrangement | Anchors, radial gaps, apex/base, enclosure, relations | Explicit hypotheses, not automatic intention |

Scikit-image region properties and OpenCV contours implement the core operations. Their coordinate and perimeter conventions differ; library outputs should be translated into the project convention rather than copied blindly. ([Scikit-image measure](https://scikit-image.org/docs/stable/api/skimage.measure.html); [OpenCV shape](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html))

Thirds, golden sections, pyramidal composition, radial layouts, and frame-within-frame should all remain available vocabulary. Their numerical versions need specified anchors and fitting freedom. A best-fit golden spiral after searching many overlays is weak evidence. Research on rule-of-thirds scores does not support treating them as universal aesthetic-quality measures. ([Amirshahi et al., 2014](https://doi.org/10.1163/22134913-00002024))

Prompt-ready language is concrete: “Keep the entire object visible, centered as a focal group, with clear upper and side margins; the support remains subordinate.” Exact occupancy targets belong in layout geometry or evaluation, not in a promise that prose will deliver the percentage.

Deterministic compositing, scale, translation, padding, and cropping provide strong controls when layers exist. Generative box/mask conditioning is softer. GLIGEN, ControlNet, and ConsistCompose are relevant precedents; their spatial adherence does not certify semantic correctness or appealing balance. ([GLIGEN](https://github.com/gligen/GLIGEN); [ControlNet](https://github.com/lllyasviel/ControlNet); [ConsistCompose, 2026](https://github.com/opensensenova/consistcompose))

### Edges, strokes, contours, and directional vectors are different representations

A raster edge is an image-value transition. A segmentation contour is the boundary of a selected region. A drawn stroke is a mark with centerline, width, color, endpoints, and role. An implied vector can be an eyeline, gesture, path, or repeated alignment with no continuous raster line.

**Canny-chain thickness is not stroke width.** A dark band can produce two edge chains; a sharp silhouette can produce an edge without any outline. Learned crisp-edge maps have the same representational issue. ([Canny](https://pubmed.ncbi.nlm.nih.gov/21869365/); [OpenCV Canny](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html); [MEMO, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Cheng_MEMO_Human-like_Crisp_Edge_Detection_Using_Masked_Edge_Prediction_CVPR_2026_paper.html))

For a reviewed boundary profile \(p(t)\), retain side-to-side contrast \(C\), transition width \(w_{10-90}\), peak gradient, overshoot, and continuity separately. For an ideal Gaussian-blurred step,

\[
w_{10-90}\approx2.563\sigma,\qquad
g_{\max}=C/(\sqrt{2\pi}\sigma).
\]

These analytical identities explain why gradient strength alone mixes contrast and softness; they do not establish the artwork’s production history.

For genuine segmented strokes, medial-axis distance gives an approximate local width \(w\approx2d\), unreliable at junctions, caps, unresolved marks, and touching strokes. Record outer/internal role, width distribution, taper, centerline density, contrast, and connectivity. **Line economy is purposeful semantic communication with restrained marks**, not simply low edge density. ([Scikit-image morphology](https://scikit-image.org/docs/0.26.x/api/skimage.morphology.html))

Directional features can include tangent-orientation histograms, structure-tensor energy/coherence, selected line segments, and contour curvature. For axial orientations:

\[
R_2=\left|\frac{\sum_iw_i e^{2\mathrm i\theta_i}}{\sum_iw_i}\right|.
\]

Low concentration can indicate multiple organized directions rather than disorder. A structure tensor measures local variation; it does not produce an attention arrow. Hough angles are line-normal angles, not automatically tangent directions. ([Scikit-image features](https://scikit-image.org/docs/stable/api/skimage.feature.html); [OpenCV feature detection](https://docs.opencv.org/4.13.0/dd/d1a/group__imgproc__feature.html))

Curvature of a smoothed selected contour,

\[
\kappa=
\frac{x'y''-y'x''}{(x'^2+y'^2)^{3/2}},
\]

has units of inverse length. Normalize by a declared object scale and compare only after consistent smoothing. An S-curve can be operationalized as sustained opposite-curvature lobes with an inflection, but not as a universal elegance score.

Useful prompts distinguish “crisp silhouette without ink outline,” “soft internal transitions,” “selectively lost contours,” and “sparse tapered internal marks.” “Sfumato” means gradual tonal modulation and merging, not generic global blur. ([National Gallery](https://www.nationalgallery.org.uk/paintings/glossary/sfumato))

Sharpening can raise edge activity while creating halos and changing finish. Structural conditioning can preserve unwanted incidental edges. Learned edge detectors such as DexiNed or MEMO are optional annotation/conditioning aids, not direct artistic-style judges.

### Depth, viewpoint, and optics require geometric hypotheses

The pinhole relation

\[
u=f_xX_c/Z_c+c_x,\qquad v=f_yY_c/Z_c+c_y
\]

shows why focal length in pixels, principal point, camera pose, scene shape, and scale must be distinguished. At fixed viewpoint, changing focal length changes magnification/FOV, not near–far perspective ratios. “Telephoto compression” under matched framing principally involves moving the camera farther away. ([OpenCV calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html))

Keep separate fields for projection, object-relative azimuth/elevation, camera roll, visible faces, convergence, horizon hypothesis, foreshortening, occlusion, atmospheric perspective, focus treatment, and apparent blur. “85 mm look” is not a complete camera specification without sensor/framing assumptions. Orthographic-like appearance can result from orthographic rendering, distant perspective, shallow geometry, or drawing conventions. ([Blender cameras](https://docs.blender.org/manual/en/latest/render/cameras.html))

Selected lines can produce deterministic intersections:

\[
l_i=p_i\times q_i,\qquad v=l_i\times l_j.
\]

But deciding that lines represent parallel 3D directions is conditional. A horizon requires direction families belonging to the same horizontal plane; a floor–wall seam is not automatically a horizon. Report angular residuals and endpoint sensitivity, especially for distant vanishing points.

Useful features include visible-face proportions, ellipse ratios for known circular parts, reviewed near/far ordering, depth-boundary locations, and local blur profiles. A projected ellipse supplies orientation information only under assumptions about the original shape and projection. Visible instance masks normally do not overlap where one object hides another; occluded fraction requires an amodal hypothesis.

Atmospheric perspective combines attenuation and airlight, not necessarily blue tint or blur:

\[
I=Jt+A(1-t),\qquad t=e^{-\beta d}.
\]

Use this as an appearance-control model, not unique depth recovery. ([Narasimhan and Nayar](https://cave.cs.columbia.edu/old/publications/pdfs/Narasimhan_IJCV02.pdf))

Depth of field, global softness, motion smear, bloom, and painterly simplification also differ. A low-frequency background is not evidence of optical defocus. Edge-spread profiles, directional attenuation, and gradient/Fourier features describe apparent blur; the cause remains conditional. ([Shi, Xu, and Jia, 2014](https://openaccess.thecvf.com/content_cvpr_2014/html/Shi_Discriminative_Blur_Detection_2014_CVPR_paper.html))

Depth Anything V2/V3, MoGe, GeoCalib, and Marigold provide useful learned estimates. Their outputs require exact representation and licensing checks. A “metric” prediction is still a model estimate on stylized art; relative inverse depth is not meters, and affine alignment in inverse depth is not affine alignment in depth. ([Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2); [Depth Anything 3](https://github.com/ByteDance-Seed/Depth-Anything-3); [MoGe](https://github.com/microsoft/MoGe); [GeoCalib](https://github.com/cvg/GeoCalib); [Marigold](https://github.com/prs-eth/Marigold))

A useful request is: “Slightly elevated three-quarter view, modest top-face visibility, weak recession, whole object sharp, background softly simplified.” Exact camera control is strongest in an authored scene; generating a new view from one raster necessarily invents unseen surfaces.

### Shape, scale, silhouette, and apparent volume need separate tests

Projected size is measurable; physical size generally is not. A silhouette describes visible extent and openings, not shaded volume. A flat token and rounded object can share a projected outline.

For reviewed object area \(A\), perimeter \(P\), convex-hull area \(A_K\), and box \(w\times h\), useful descriptors include:

\[
f_A=A/(WH),\quad
E=A/(wh),\quad
S=A/A_K,\quad
C=4\pi A/P^2.
\]

Also retain oriented aspect, principal moments, topology, hole area, contour simplification across tolerances, normalized curvature, part thickness, and named part ratios. Circularity and solidity are descriptive: a branchy plant should not be forced toward a fruit’s values. Raster perimeter conventions can even slightly violate ideal continuous bounds. ([Scikit-image measure](https://scikit-image.org/docs/stable/api/skimage.measure.html); [OpenCV shape](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html))

An exaggeration factor requires a class/view baseline:

\[
X_{ij}=
\frac{(l_i/l_j)_{\rm candidate}}
     {(l_i/l_j)_{\rm baseline}}.
\]

Without that baseline, “20% exaggerated” is not identified. Corner roundness should be measured locally at meaningful scale, not inferred from one global circularity score.

For the same object, retain both card-space comparison and limited shape-normalized comparison. Translation/isotropic scale removal can diagnose shape, but should not hide placement errors. Anisotropic or nonrigid alignment can erase the proportion mismatch being tested. For different objects, do not minimize apple-to-calculator IoU or Hu distance as a style objective.

Prompt-ready terms include “thicker secondary parts,” “larger diagnostic opening,” “rounded beveled corners,” “compact proportions,” and “broad continuous volume gradients.” A silhouette plate and actual-size recognition test assess different things. Neither every object nor every action must be recognizable from silhouette alone.

A small geometry change can be exact when a layer or vector exists. If only a flattened scene exists, scaling an object exposes background and changes grounding. Apparent volume additionally depends on shading, perspective, overlap, and material cues; unique true volume remains unobservable.

### Surface, material appearance, and rendering finish should not collapse into “texture”

Material appearance depends jointly on illumination, viewpoint, shape, and processing. Perceived gloss does not require observers to recover BRDF parameters. Shader parameters are useful forward controls, not directly recoverable raster attributes. ([Fleming, 2014](https://pubmed.ncbi.nlm.nih.gov/24291494/); [Blender Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html))

Separate smoothness of image finish, visible marks, mark scale, directional organization, pigment/paper appearance, shading construction, matte/gloss appearance, transmission-like cues, grain, glow, and acutance.

| Appearance request | Operational wording | Incorrect substitute |
|---|---|---|
| Smooth dimensional finish | “Clean color fields and broad continuous gradients” | Physical roughness value |
| Visible brushwork | “Sparse medium-width strokes following form” | Add generic noise |
| Cel shading | “Two or three broad discrete tone regions” | Raise global contrast |
| Satin/gloss | “Broad restrained highlights” / “small crisp glints” | Unique BRDF recovery |
| Impasto-like | “Coherent ridge-like highlights and shadows” | Grain overlay |
| Transmission | “Background visible/distorted through the object” | Alpha alone |
| Crisp finish | “Clear contours without overshoot halos” | Maximum sharpening |

A practical multiscale descriptor uses

\[
B_s=G_{\sigma_s}*Y-G_{\sigma_{s+1}}*Y,\qquad
E_s=\operatorname{mean}_M(B_s^2).
\]

Retain absolute energy and relative allocation \(E_s/\sum_tE_t\). Relative fractions alone hide whether a surface is nearly textureless. Add coefficient quantiles, orientation/coherence, autocorrelation, and selected highlight profiles.

GLCM requires fixed intensity quantization, offsets, angles, and valid pairs. LBP captures local comparisons but largely discards amplitude; combine it with residual magnitude. Fourier power loses phase and can be contaminated by irregular mask edges. Portilla–Simoncelli’s higher-order multiscale statistics demonstrate why a histogram or power spectrum is incomplete. ([Portilla–Simoncelli](https://www.cns.nyu.edu/~lcv/texture/); [Scikit-image features](https://scikit-image.org/docs/stable/api/skimage.feature.html))

PyWavelets’ stationary transform supports shift-stable multiscale analysis with documented normalization and padding requirements. It is not equivalent to an arbitrarily oriented steerable pyramid. ([PyWavelets SWT](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html))

Masked denoising, grain layers, and frequency attenuation are appropriate for separable finish corrections. Form-following strokes, coherent reflections, refraction, and relief usually need stronger synthesis or scene controls. “Make it painterly” is too broad for isolated correction.

Materialist is relevant 2025/2026 inverse-rendering prior art, but its estimates remain prior-conditioned; its repository documents approximate light paths and possible inaccurate refraction in transparency editing. ([Materialist paper](https://arxiv.org/abs/2501.03717); [implementation](https://github.com/lez-s/Materialist))

### Hierarchy, attention, readability, and detail economy are related but distinct

The intended task determines evaluation. Recognizing the object, understanding an expression, searching for an item, and appreciating an illustration are different tasks. Actual display size, exposure duration, surrounding UI, and identity-bearing details matter.

Deterministic descriptors can quantify value/chroma separation, regional edge activity, multiscale detail energy, and contrast allocation. For a nonnegative map \(q\),

\[
p(x)=q(x)/\sum_{V}q(x),\qquad
m_F=\sum_Fp(x),\qquad
e_F=m_F/(|F|/|V|).
\]

Here \(m_F\) is focal map mass and \(e_F\) area-adjusted enrichment. Normalizing a contrast map to unit sum does **not** turn it into a calibrated fixation probability.

Local boundary separation is often more useful than subject/background mean difference: sample paired inside/outside neighborhoods and report the distribution of signed/absolute lightness and chromatic differences. Weak sections can disappear despite good overall means. Detail economy should similarly retain subject and background band energies, edge densities, quiet-area fractions, and identity-bearing exceptions.

Clutter is not simply object count or high-frequency energy. Feature congestion and target–distractor relationships contribute. Task demands can also alter attention; high contrast does not universally determine the first fixation. ([Rosenholtz et al.](https://jov.arvojournals.org/article.aspx?articleid=2122001); [attention-task evidence](https://authors.library.caltech.edu/records/ywkb0-v8462))

OpenCV spectral residual is a deterministic conspicuity heuristic with a documented internal 64×64 default in the inspected implementation. It is not a gaze sensor. DeepGaze predicts fixation distributions; DeepGaze III and DeepGaze3.5-VL address sequential viewing. Dataset and viewing-scale biases remain important. ([OpenCV source](https://github.com/opencv/opencv_contrib/blob/5.x/modules/saliency/src/staticSaliencySpectralResidual.cpp); [DeepGaze](https://github.com/matthias-k/DeepGaze); [MSDB, ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Kummerer_Modeling_Saliency_Dataset_Bias_ICCV_2025_paper.html); [DeepGaze3.5-VL, 2026](https://arxiv.org/abs/2607.02083))

A static map contains no viewing order. SALICON’s mouse-contingent collection method should not be relabeled hardware eye tracking. “Click what you noticed first” is also not a first-fixation measurement. ([SALICON, 2015](https://openaccess.thecvf.com/content_cvpr_2015/html/Jiang_SALICON_Saliency_in_2015_CVPR_paper.html))

Useful wording is: “Keep the object as the dominant focal group; reduce background microdetail and high-chroma accents; preserve the diagnostic handle and primary highlight.” Background simplification, selective contrast, and selective sharpening can help, but may change category realism, finish, or lighting shorthand.

Actual-size recognition, grayscale, silhouette, controlled blur, and background-suppression tests are complementary diagnostics—not universal readability certificates. For essential UI cues, apply relevant accessibility requirements separately; do not turn WCAG contrast thresholds into general artwork-style thresholds.

### Rhythm and repetition need motif geometry before emotional interpretation

Pattern repeats elements; rhythm organizes recurrence into perceived movement. Regular, alternating, progressive, flowing, clustered, radial, and interrupted patterns provide useful language, but no validated universal mapping converts spatial frequency into calmness, excitement, or “visual BPM.” ([Getty design principles](https://www.getty.edu/education/teachers/building_lessons/principles_design.pdf))

For accepted motif instances, retain count, eligible-area density, union coverage, size distribution, spacing, gap, orientation, sequence, progression, and exceptions. Along a declared path:

\[
\Delta_i=s_{i+1}-s_i,\qquad
CV_\Delta=\operatorname{sd}(\Delta)/\operatorname{mean}(\Delta).
\]

Center pitch differs from edge gap. Constant pitch with growing motifs reduces visible gaps. Fit intended progressions before labeling their variance irregular.

Mask-aware autocorrelation can find recurrent displacement, while FFT peaks describe periodic components. Frequency is in cycles/pixel or cycles/object; along an axis, period is \(1/f\). Windowing reduces leakage but broadens peaks; zero padding does not add observed repeats. Fourier orientation is normal to stripe direction. ([SciPy FFT and spectral analysis](https://docs.scipy.org/doc/scipy/tutorial/fft.html))

Template matching suits repeated known motifs; semantic counters such as CountGD++ can help decide which instances belong to a motif class. Counting alone does not measure spacing or rhythm. For sparse decorations, direct annotation is usually more interpretable than sophisticated spatial statistics. ([Scikit-image template matching](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_template.html); [CountGD++, CVPR 2026](https://github.com/niki-amini-naieni/CountGDPlusPlus))

An explicit repeat rule allows exact detection of missing, extra, displaced, misoriented, or wrong-class instances. Excluded slots behind the subject or inside a protected halo should not count as missing.

When exact repetition matters, construct it: SVG defines tile coordinates, spacing, scale, and transforms deterministically. Generate or author the motif once, then place it. ([SVG patterns](https://www.w3.org/TR/SVG2/pservers.html#Patterns))

Across a collection, compare recurrence distributions. An unordered set has no intrinsic temporal sequence. An FFT of the gallery contact sheet mostly measures the sheet grid and borders, not the artwork’s internal rhythm.

### Gesture, expression, and staging remain available even when currently inapplicable

Human gesture and facial expression are usually **not applicable to the requested object-only cards**. Retain them in the ontology for future characters rather than forcing pose detectors onto calculators or fruit. Object staging still includes tilt, articulated parts, support, contact, occlusion, and component separation.

A line of action is an artist-selected abstraction, not a hidden anatomical curve. Annotated curves can provide lean, curvature, arc/chord ratio, and secondary gestures. ([Guay, Cani, and Ronfard](https://team.inria.fr/imagine/the-line-of-action-an-intuitive-interface-for-expressive-character-posing/))

Given accepted landmarks \(a,b,c\), projected joint angle is

\[
\theta_b=\cos^{-1}
\frac{(a-b)\cdot(c-b)}
{\|a-b\|\|c-b\|}.
\]

It is a 2D angle, not a recovered 3D joint angle. Normalize distances by a declared scalar anchor; independently normalized width/height coordinates distort angles. Preserve anatomical left/right separately from image-left/right and mirrored input.

Facial features should describe mechanisms: eye aperture/width, brow position/slope, mouth opening/width, pupil position, asymmetry, and qualified head orientation. Landmarks, blendshapes, action units, expression labels, and emotion interpretations are different representations. A coefficient of 0.7 is not 70% happiness. Human expression research itself cautions against universal emotion inference from facial movement. ([MediaPipe face](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker); [Barrett et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/))

MediaPipe, MMPose, and DWPose supply candidate estimators, but topology and artwork-domain fit matter. Human-Art and AP-10K demonstrate the need for domain- and anatomy-specific annotation conventions. ([MediaPipe pose](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker); [MMPose](https://github.com/open-mmlab/mmpose); [DWPose](https://github.com/IDEA-Research/DWPose); [Human-Art](https://github.com/IDEA-Research/HumanArt); [AP-10K](https://github.com/AlexTheBad/AP-10K))

Represent staging as an instance/part graph: “handle in front of body at this boundary,” “cup supported by table,” or “depicted eyeline toward object.” Annotated contact-anchor distance and contour clearance are measurable; physical contact or grasping is not proved by proximity. Current ControlPose and OccluRank research addresses association and ordering, but does not establish solved deployment for these assets. ([ControlPose, 2026](https://openaccess.thecvf.com/content/CVPR2026F/html/Du_ControlPose_High-Fidelity_Pose-Controlled_Image_Generation_with_Multi-Faceted_Pose_Disentanglement_CVPRF_2026_paper.html); [OccluRank](https://arxiv.org/abs/2608.20932))

### Additional directions belong in the specification without becoming speculative scores

The useful “missing axes” are mostly cross-cutting: abstraction level, shape simplification, semantic diagnosticity, realism consistency, artifact control, thematic coherence, and set diversity. They should be attached to the groups above rather than create an uncontrolled list of vague style sliders.

Typography and symbols need explicit content checks when present on objects; exact text is not a texture descriptor. Transparency, reflections, and contact consistency need dedicated evidence regions. Set-level coherence should preserve varied object identities rather than reward repeated objects. Rarity should remain metadata unless the brief explicitly assigns visual consequences; it should not silently alter object rendering.

For casual collectible art, the initial priorities are therefore **recognizable focal objects, category-correct context, compact readable composition, coherent dimensional shading, restrained background competition, and deliberate detail allocation**. Exact lens, BRDF, or emotional-tempo estimates are lower-priority research questions, not prerequisites.

## 3. Match each intervention to an appropriate tool

### A CPU baseline can measure most observable descriptors

The baseline should use reviewed annotations and ordinary image-processing libraries. This avoids making learned-model deployment a prerequisite for geometry, color, or multiscale statistics.

| Tool | Actionable role | License/status evidence | Feasibility and caveat |
|---|---|---|---|
| NumPy/SciPy | Arrays, filtering, FFT, statistics, distances | Established permissive scientific stack; SciPy BSD-3-Clause | CPU baseline; no local runtime measured |
| [Pillow/ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html) | Decode, metadata, ICC conversion, export | MIT-CMU | CPU; verify mode/precision, not a blanket HDR endorsement |
| [Colour](https://github.com/colour-science/colour) | Explicit color conversion, adaptation, appearance models | BSD-3-Clause | CPU; domain/range and white-point configuration required |
| [Scikit-image](https://scikit-image.org/docs/stable/api/skimage.measure.html) | Regions, contours, morphology, texture, tensor features | Predominantly BSD-3-Clause with file-level exceptions | CPU; pin stable API rather than development paths |
| [OpenCV](https://docs.opencv.org/4.13.0/) | Edges, lines, shape, camera geometry | Apache-2.0 for inspected release | CPU core; contrib modules/version compatibility separate |
| [POT](https://pythonot.github.io/) | Color-distribution transport | MIT core; optional dependencies have separate terms | CPU sampled/quantized comparisons |
| [PyWavelets](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html) | Multiscale texture and recurrence | MIT | Optional CPU extension |
| SVG/vector construction | Exact motifs, layouts, contours | Standard, not a renderer license | Strong constructive control where vector assets exist |
| ImageMagick/darktable | Auditable resize, grading, grain, sharpening diagnostics | Project-specific licenses; darktable audit incomplete in notes | CPU options; expensive filters can benefit from OpenCL |
| Blender/Cycles | Authored geometry, camera, lights, materials, passes | Blender GPL; Cycles Apache-2.0; created artwork commercially usable | CPU rendering; Linux HIP support documented, local setup untested |

The notes inspected current documentation and repository artifacts, but not one fully installed, tested combined stack. Recent repository activity is not a support guarantee. Conversely, an old README date does not prove abandonment.

### Optional learned tools should earn their complexity

| Candidate | What it adds | License/readiness distinction | CPU/AMD status |
|---|---|---|---|
| SAM 2/2.1 | Point/box-guided mask assistance | Apache-2.0 code/checkpoints; ancillary exceptions | CPU route possible; CUDA-oriented examples; untested locally |
| SAM 3/3.1 | Concept/text/exemplar segmentation | Custom SAM License; gated checkpoints | Official CUDA prerequisites; not an established AMD baseline |
| BiRefNet/rembg | Foreground extraction | BiRefNet inspected code/checkpoint MIT; rembg wrapper MIT, model terms vary | rembg documents CPU/ROCm routes; actual compatibility untested |
| Depth Anything V2 | Relative-depth proxy | Small Apache-2.0; larger weights CC-BY-NC-4.0 | CPU fallback documented |
| Depth Anything 3 | Depth/camera estimates, variant-specific metric outputs | Apache code; checkpoint licenses vary | Complete CPU/ROCm path unverified |
| MoGe | Point/depth/FOV/normal estimates | Inspected code/model terms permissive; component-specific checks remain | Latest sparse/custom-kernel stack needs review |
| GeoCalib | Intrinsics/gravity hypothesis | Apache code; CC-BY-4.0 weights | CPU example documented; centered-principal-point assumption matters |
| Marigold | Depth/normals/intrinsics estimates | Apache code; RAIL++ model terms | CPU fallback documented, no speed claim |
| DexiNed/MEMO | Learned boundary proposals | DexiNed MIT; MEMO Apache code, other terms separate | ONNX routes; selected versions must be compatible |
| MediaPipe/MMPose/DWPose | Pose/face annotation assistance | Generally Apache code; bundle/checkpoint/dataset terms separate | CPU candidates; stylized-domain accuracy unvalidated |
| CLIP/DINO | Semantic/content features | CLIP MIT; standard DINOv2 Apache; DINOv3 custom terms | Smaller inference paths plausible; no local benchmark |
| LPIPS/DISTS | Perceptual regression diagnostics | LPIPS BSD-2-Clause; DISTS MIT | CPU paths available; weights required |
| CSD | Style-oriented retrieval features | MIT code; **released-weight discrepancy warning** | Script adaptation/device review needed |
| DeepGaze family | Predicted fixation/scanpath information | Main repository license unresolved; 3.5-VL research-only/NC | No validated AMD route or card-domain calibration |

Official repositories document these capabilities and qualifications. A wrapper’s license does not clear every selectable model. ([SAM 2](https://github.com/facebookresearch/sam2); [SAM 3](https://github.com/facebookresearch/sam3); [BiRefNet](https://github.com/ZhengPeng7/BiRefNet); [rembg](https://github.com/danielgatis/rembg))

Material restrictions particularly affect proposed production use. Intrinsic is academic-use-only; DSINE is noncommercial; PIXLRelight has MIT code but CC-BY-NC weights; Perspective Fields is under an Adobe noncommercial research license; OpenFace has restrictive research terms. LightLab’s inspected repository was a project-site release, not demonstrated runnable inference tooling. ColourCrafter and SW-Guidance had unresolved license/release details despite promising descriptions. ([Intrinsic](https://github.com/compphoto/Intrinsic); [DSINE](https://github.com/baegwangbin/DSINE); [PIXLRelight](https://github.com/mlfarinha/pixlrelight); [Perspective Fields](https://github.com/jinlinyi/PerspectiveFields); [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace); [LightLab](https://github.com/NadMag/LightLab))

The attention lane also found a concrete conflict: TempSAL’s root license says MIT while its README says CC BY-SA 4.0. Do not silently choose the more convenient notice, particularly for weights/assets. ([TempSAL](https://github.com/IVRL/Tempsal))

For the RX 7900 XTX workstation, deterministic CPU measurement does not require ROCm. PyTorch HIP intentionally reuses `torch.cuda` interfaces, so that name alone neither proves NVIDIA-only operation nor proves AMD compatibility. Custom kernels, precision, attention libraries, quantization, and OS support require separate tests. AMD GPU listing is not certification of an entire application on CachyOS/Arch. ([PyTorch HIP semantics](https://github.com/pytorch/pytorch/blob/main/docs/source/notes/hip.rst); [AMD compatibility](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html))

### Current generators expose different control surfaces

The research corpus documents substantial changes through October 2026. These are **interface capabilities and author/vendor claims**, not measured comparative performance.

| Backend family | Relevant documented controls | Important boundary |
|---|---|---|
| OpenAI GPT Image 2.5 Sunburst/Flare | Image editing, references, masks, conversational iteration, output controls | Mask is guidance, not exact boundary preservation |
| Google Nano Banana 2.1/Gemini 3 Pro Image | Reference input, editing, model-specific aspect/resolution and continuation controls | Capabilities differ by variant |
| BFL FLUX 3 Image/Klein | Multiple references, prompt-embedded boxes, output geometry; variant-specific controls | Main/Klein schemas differ; vendor “pixel-exact” claims unvalidated |
| Qwen-Image-Edit-2511 | Open instruction editing, multi-image input, documented pipeline controls | Apache model-card declaration does not prove hardware fit |
| FLUX.2 Klein | Open-weight editing variants | 4B Apache terms must not be generalized to NC 9B variants |
| SDXL + ControlNet/IP-Adapter | Inspectable structural maps, reference conditioning, inpainting, strength controls | Older ecosystem; component/checkpoint compatibility matters |

([OpenAI guide](https://developers.openai.com/api/docs/guides/image-generation); [Google guide](https://ai.google.dev/gemini-api/docs/image-generation); [BFL release notes](https://docs.bfl.ml/release-notes); [Qwen model card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511); [FLUX.2](https://github.com/black-forest-labs/flux2))

The synthesis rechecked the OpenAI guide and BFL documentation; it did not conduct new broad model research. Account-specific availability, prices, total workflow memory, and output quality remain unverified. FLUX 3 Klein’s cited custom license was not fully inspected in the original lane. Hosted-service data retention and permitted reference use also need task-appropriate review before any future uploads.

**Prompt language is an actuator request, not a numerical API.** A field named `key_azimuth_deg` in an internal specification does not mean a hosted endpoint accepts that parameter. Negative prompts are not logical exclusions; image-to-image strength is not “style amount”; reference-adapter scale is architecture-specific.

### Choose the least disruptive control that can perform the intended change

| Intervention level | Appropriate tasks | Strong preservation available | Remaining risk |
|---|---|---|---|
| Deterministic export/transform | Format, crop, layer placement, curves, masked chroma, grain | Declared geometry or untouched samples | Clipping, interpolation, perceptual coupling |
| Layer/vector construction | Exact motifs, spacing, outlines, component placement | Authored geometry and layer identity | Compositing integration |
| Local raster/generative edit | Semantic repair, coherent material marks, local replacement | Protected pixels if explicitly copied | Seams, shadows/reflections outside edit area |
| Reference/structural conditioning | Style treatment, layout, silhouette, depth, pose | Soft structural adherence | Content leakage, overconstraint, incidental copying |
| Specialized relighting/reconstruction | New coherent illumination | Model-conditioned consistency | Estimated geometry/material errors |
| Authored 3D proxy | Repeated exact camera/light/material experiments | Fixed scene parameters | Proxy may not match reference; stylization still needed |
| Training/fine-tuning | Repeated unresolved consistency failures | Learned adaptation, not invariants | Data bias, leakage, cost, maintenance |

An authored 3D proxy is warranted when repeated camera/lighting/material variation demands stronger forward control, or when conditioning renders materially help. It should **not** be the default response to every style mismatch.

Preservation guarantees must be typed. An exporter can guarantee dimensions. A compositor can preserve samples outside an edit mask. A scene graph can keep mesh/camera/material parameters unchanged. A generative instruction generally supplies only a soft perceptual constraint.

For edit mask \(M\),

\[
I_{\rm out}=(1-M)I_{\rm original}+MI_{\rm generated}
\]

preserves original samples where \(M=0\), provided subsequent processing does not modify them. Feathering, color conversion, resizing, and lossy export can weaken exact equality. This guarantee belongs to the compositor, not the model.

Necessary coupled effects should be authorized explicitly. Moving a light changes shadows and reflections. Changing roughness changes highlight structure. Moving an object can expose background and alter contact. Preserving all of these would contradict the requested change.

### A backend-neutral schema makes unsupported requirements visible

The following example is **a proposal with illustrative values, not real API parameters or measured reference values**.

```yaml
spec_version: research-proposal-1
asset:
  category: 3
  content: single ceramic cinema-themed prop
  applicability:
    human_pose: not_applicable
    contact_shadow: applicable

references:
  - id: content_anchor
    role: identity_and_layout
    asset: LOCAL_ASSET_ID
  - id: style_board
    role: rendering_treatment
    assets: [LOCAL_REFERENCE_A, LOCAL_REFERENCE_B]

intent:
  lighting:
    key:
      direction_convention: subject_to_source_camera_relative
      azimuth_deg: -35       # illustrative design intent
      elevation_deg: 40      # not inferred from the references
      source_extent: broad
    fill:
      appearance: readable_shadow_side
    shadows:
      appearance: compact_soft_grounding

  surface_and_finish:
    appearance: smooth_dimensional_illustration
    microtexture: restrained

observed_reference_evidence:
  - claim: broad dimensional shading
    region: subject
    confidence: medium
  - claim: exact source direction
    status: unknown

edit_contract:
  target_axis: chromatic_design.background_chroma
  requested_change: reduce_background_chroma
  protected:
    - subject_identity
    - subject_silhouette
    - subject_pixels
    - object_placement
    - contact_shadow_geometry
  allowed_consequences:
    - background_color
    - perceived_subject_background_separation
  edit_region: reviewed_background_mask
  exact_pixel_preservation: outside_mask_if_composited

evaluation:
  reference_group: category_3_object_cards
  features:
    - background_chroma_quantiles
    - background_lightness_quantiles
    - silhouette_boundary_separation
    - protected_pixel_difference
  decision_policy: calibrated_per_axis_gates
  unsupported_feature_policy: abstain

backend_capabilities:
  numeric_color_transform: unknown_until_selected
  reference_conditioning: unknown_until_selected
  seed_control: unknown_until_selected
  exact_mask_adherence: not_assumed

budget:
  candidate_limit: 4          # illustrative experimental cap
  edit_round_limit: 2
  external_spend_limit: not_authorized_by_this_example
```

A compiler first checks contradictions, resolves reference roles, selects a control mechanism, and emits only supported settings. For this particular request, it should prefer a masked chroma transform over new image synthesis. If a generative editor is needed, compiled wording could be:

> Use the supplied image as the identity and layout anchor. Reduce chromatic intensity only in the reviewed background region. Preserve its broad lightness pattern, the subject, object placement, silhouette, and compact contact shadow. Do not add texture, new objects, outlines, or new lighting. The intended result is stronger subject/background chromatic separation, not a new palette for the object.

The evaluation target remains numerical even when the actuator is prose. An unsupported hard requirement should cause an explicit capability failure, not silent conversion into “try to preserve.”

A structured measurement record should keep the layers separate:

```yaml
measurement_id: illustrative-record
feature:
  name: background_oklab_chroma_median
  region: reviewed_background
  definition: median(sqrt(a*a + b*b))
  units: Oklab_coordinate_units
  value: 0.06                  # illustrative, not a project result
  sensitivity_range: [0.05, 0.07]
  provenance: fixed_conversion_and_mask_version

inferred_explanation:
  claim: background_is_more_chromatic_than_desired
  physical_illuminant_claim: none
  confidence_kind: qualitative
  confidence: medium

prompt_target:
  request: reduce_background_chroma
  numeric_api_control: false

acceptance:
  target_band: unset_pending_calibration
  probability_of_acceptance: null
  decision: review

evidence:
  overlay: LOCAL_EVIDENCE_ID
  mask_version: reviewed-v1
  excluded_regions: [subject, contact_shadow, ui]
```

An axis-specific critique and edit difference should be equally explicit:

```diff
- Target: make the card less busy and more polished.
+ Target: reduce background fine-scale detail only.
+ Evidence: background interior band-energy map and reviewed crop.
+ Preserve: subject pixels, silhouette, placement, palette families,
+           contact-shadow geometry, broad background value grouping.
+ Permit: lower background microcontrast and fewer decorative marks.
+ Reject if: subject details disappear, category context is removed,
+            seams appear, or protected pixels change.
+ Decision if uncertain: retain baseline and request review.
```

This is more actionable than a specialist saying “lighting 8/10” or “style match 92%.”

## 4. Calibrate acceptance before automating correction

### Same-content preservation and cross-content style matching need different metrics

For editing the **same image**, correspondence is available. Pixel equality, registered \(\Delta E\), mask overlap, boundary distances, SSIM, LPIPS, and DISTS can detect particular regressions.

For **different objects in a shared style**, pixel correspondence usually does not exist. Compare category/role-conditioned distributions and design tendencies, not whole-image equality. An apple and a fan can share shading and detail allocation while differing legitimately in hue, contour complexity, and material.

| Metric | What it measures | Recommended role | What not to claim |
|---|---|---|---|
| SSIM | Full-reference luminance/contrast/structure similarity | Aligned preservation diagnostics | Content-independent style |
| LPIPS | Learned perceptual distance calibrated on distortion judgments | Same-content change guard | Percentage style mismatch |
| DISTS | Structure/texture similarity with texture-resampling tolerance | Complementary preservation/texture diagnostic | Exact detail preservation |
| Gram features | Feature-channel correlations across locations/layers | Texture/style evidence | Complete spatial or semantic style identity |
| CLIP | Image/text-related representation similarity | Content and broad semantic checks | Style-only or calibrated acceptance |
| DINO features | General-purpose visual representations | Correspondence/content proxy | Guaranteed content-only features |
| ALADIN/CSD | Learned style retrieval descriptors | Candidate style-ranking features | Universal acceptance threshold |
| ASTRA-Score | Human-preference-aligned style-transfer triplet evaluation | Relevant benchmark precedent/candidate | Validated card acceptance |
| FID/KID/ArtFID | Distribution comparisons | Later collection/model analysis | Individual-card release decision |

([SSIM](https://ece.uwaterloo.ca/~z70wang/research/ssim/); [LPIPS](https://github.com/richzhang/PerceptualSimilarity); [DISTS](https://github.com/dingkeyan93/DISTS); [Gatys](https://arxiv.org/abs/1508.06576); [CLIP](https://proceedings.mlr.press/v139/radford21a.html); [ALADIN](https://arxiv.org/abs/2103.09776))

For features \(F_l\), a normalized Gram matrix \(F_lF_l^\top/N_l\) discards feature-map spatial ordering. It still contains content-dependent activations. Spatial pooling is not proof of semantic disentanglement.

LPIPS expects its documented input scale and model/version; DISTS has different preprocessing. Their outputs are not probabilities, and their tolerance to some changes can hide details that matter to the art specification.

### Current style-specific metrics reinforce the need for local calibration

CSD is directly relevant style-retrieval prior art, but its official repository currently warns of disagreement between uploaded weights and reported paper numbers. Its suggested 0.5/0.8 interpretations were presented as a hypothesis after examining generations for 96 artists—not universal thresholds. ([CSD paper](https://arxiv.org/html/2404.01292v1); [official warning](https://github.com/learn2phoenix/CSD))

The **October 7, 2026 ASTRA preprint** is particularly useful because it separates content preservation, style fidelity, and overall preference using controlled pairwise comparisons. It studies 12 styles, six content images, and 12 methods, producing 864 results. Its main intended deployment evaluates unseen methods on its benchmark references; additional held-out-content/style tests provide robustness evidence, not broad proof of collectible-card validity. Its reported style agreement is imperfect, and its content/style tradeoffs depend on style. ([ASTRA](https://arxiv.org/html/2610.10003v1))

StyleDecoupler, January 2026, proposes suppressing content-correlated information using aligned DINO features and generated descriptions. “Pure style” remains the authors’ characterization. The method trains an alignment component despite frozen original VLM features, and the inspected text contains inconsistent alignment-data counts. Treat it as promising research, not a proven universal decomposition. ([StyleDecoupler](https://arxiv.org/html/2601.17697v1))

These sources support testing style-specific features against the actual task. They do not support replacing the art director with one embedding cosine.

### Distribution metrics cannot rescue individual acceptance or tiny samples

FID has finite-sample bias that depends on the model; equal sample counts do not remove that bias. KID offers an unbiased estimator of a population squared discrepancy under its assumptions, but unbiasedness does not guarantee low variance, adequate sample coverage, or a suitable feature space. ArtFID complements style-transfer evaluation with content comparisons and style-distribution assessment. ([Chong and Forsyth, 2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Chong_Effectively_Unbiased_FID_and_Inception_Score_and_Where_to_Find_CVPR_2020_paper.html); [KID](https://arxiv.org/abs/1801.01401); [ArtFID](https://github.com/matthias-wright/art-fid))

One card cannot estimate a broad card-style distribution. Many spatial patches are not many independent cards. With \(n\) images, empirical feature covariance rank is at most \(n-1\), making high-dimensional tiny-sample estimates fragile. A set score can also hide one unacceptable image or change because category proportions changed.

Use collection metrics only after establishing enough independent, appropriately conditioned samples and a reason they add information beyond per-card checks. Never adopt “FID below X” as a single-card acceptance rule.

### Reference ranges must represent allowed variation, not a universal mean

The target is better expressed as

\[
P(\mathbf m\mid
\text{style family, category, region, content class, view}),
\]

with only the conditioning variables the data can support. Excessive stratification produces empty cells; indiscriminate pooling confuses content with style.

Separate an art-directed specification band, observed reference range, predictive interval for future accepted images, and confidence interval for a mean. **The last is not an acceptance interval for an individual image.**

With one reference, report an exemplar. With a handful, show individual values and provisional ranges. Bootstrap independent cards or source families—not pixels or all pairwise distances. Preserve pairing for before/after tests and clustering for crops/iterations. Thousands of bootstrap replicates do not discover missing subtypes; small-sample percentile intervals can undercover. ([Hesterberg](https://arxiv.org/abs/1411.5279))

### Validate measurement sensitivity before using it as a reward

Construct human-reviewed controlled perturbations: masked chroma changes, broad tone changes, local edge softening, background-detail attenuation, object-scale shifts, motif-spacing changes, and selected semantic failures. Include benign resizing/encoding changes and mask alternatives.

Measure intended sensitivity, off-axis response, monotonicity, content leakage, and deployment-scale stability. A change isolated in code is not necessarily isolated perceptually.

A proposed local response matrix is

\[
J_{ij}\approx
\frac{
m_i(f(x,u+\delta e_j,s))-
m_i(f(x,u-\delta e_j,s))
}{2\delta}.
\]

Diagonal entries indicate intended influence; off-diagonal entries reveal coupling. This is an experimental diagnostic, not a globally valid inverse model. Natural-language edits are discrete interventions, not truly differentiable coordinates.

Paired seeds reduce one nuisance factor but do not guarantee invariance. Reset random state for each pair, freeze preprocessing and effective prompt, and repeat across seeds/assets. Identical seeds do not guarantee identical results across hardware/software configurations. Hosted endpoints without exposed seed/version control need a different repeatability protocol. ([Diffusers reproducibility](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/reusing_seeds.md))

### Human and agent reliability belong in the benchmark

Use blinded comparisons with generator identity and iteration number hidden, randomized order, repeated cases, and known failures. Ask separate questions about style, content, preservation, artifacts, and release acceptability. Include the same content in different styles and different content in the same style.

For readability, test the intended recognition task at actual display sizes and relevant context. Identification accuracy, confusion classes, response time, preference, and gaze are distinct outcomes. For eye tracking, record calibration, viewing distance, fixation parsing, and task; trials that never hit the focal region are censored, not zero-latency successes.

Agent specialists should provide semantic interpretation, evidence selection, contradiction detection, and bounded edit proposals. They should invoke deterministic measurements rather than estimate illuminance, source angles, or material roughness by intuition. Pin judge model/prompt/layout, test order sensitivity, compare with held-out human judgments, and retain uncertainty. Repeated calls to the same model are not independent expert votes.

### Per-axis gates support honest acceptance and abstention

For a calibrated distance, lower is usually better; for similarity, higher is usually better; many descriptors instead need an allowed band.

| Quantity | Robust pass using uncertainty interval \([l,u]\) | Robust fail |
|---|---|---|
| Distance with upper limit \(t\) | \(u\le t\) | \(l>t\) |
| Similarity with lower limit \(t\) | \(l\ge t\) | \(u<t\) |
| Descriptor allowed in \([L,U]\) | Entire interval inside band | Entire interval outside band |
| Missing/unreliable measurement | Never automatic pass | Review or explicit unavailable state |

These are conservative engineering rules, not statistical guarantees unless interval construction justifies them. Sensitivity envelopes from masks or resampling are not automatically confidence intervals.

Calibrated acceptance probabilities require labeled validation cases. Raw similarity, softmax, mask-quality scores, and agent confidence are not substitutes. Conformal methods can later supply marginal coverage under exchangeability and held-out calibration, but not guarantee artistic correctness for a selected candidate. Their corrected quantile uses

\[
k=\lceil(n+1)(1-\alpha)\rceil.
\]

When \(k>n\), an uninformative threshold is appropriate rather than optimistic clipping. At 95% coverage, 19 calibration examples only reach the finite-maximum boundary; that is not evidence of strong practical calibration. Adaptive score-driven generation/selection also complicates naïve coverage claims. ([Angelopoulos and Bates](https://arxiv.org/abs/2107.07511))

Keep hard gates separate from preferences. A beautiful palette cannot cancel a missing object part. Report a vector such as “style provisional pass; content pass; protected-region preservation fail; artifacts review,” not a compensating aggregate.

### A bounded loop should stop, revert, or change mechanisms

A proposed evaluation loop starts from the original anchor and best accepted state, records the complete vector, prioritizes one diagnosed mismatch, declares protected properties and allowed consequences, chooses the least disruptive actuator, evaluates the result, and accepts only a meaningful improvement without unacceptable regression.

Compare against both the preceding state and original anchor. Otherwise, small accepted changes can accumulate into large drift. Use local pixel checks where exact preservation is intended and semantic/shape checks where perceptual preservation is intended.

Stop when the target and all hard gates pass, when improvement is smaller than uncertainty or practical importance, when repeated attempts fail, when coupled objectives oscillate, or when candidate/time/spend limits are reached. Return the best accepted candidate and an unmet requirement when necessary. Repeated protected-axis failure is evidence to change the mask, control mechanism, or requirement—not merely intensify the prompt.

Goodhart risks include copying reference content, blurring away difficult detail, posterizing for palette scores, manipulating mask area, or exploiting a judge’s preferred aesthetic. Counter them with separate content checks, hidden audit cases, human review of unusual high scores, explicit lineage, and periodically revalidated metrics.

Coordinate-wise editing is therefore a **search strategy**, not proof of independent axes. Some changes require a joint step and an explicit Pareto tradeoff rather than endless alternation.

## 5. Prototype the smallest useful research system

### Existing work already covers the generic loop

ControlNet establishes spatial conditioning; IP-Adapter supplies image conditioning; InstantStyle and Only-Style address content leakage and style-specific control. Palette-based recoloring, color-guided diffusion, and relighting already provide more interpretable interventions than global style adjectives. ([ControlNet](https://github.com/lllyasviel/ControlNet); [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter); [InstantStyle](https://github.com/instantX-research/InstantStyle); [Only-Style](https://arxiv.org/abs/2506.09916); [palette recoloring](https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/index.php))

Agentic generation and editing are also established prior art. Idea2Img iterates prompts, drafts, selection, and visual feedback. MIRA uses atomic edits through perception–reasoning–action. IEA chooses explicit retouching operations. EdiVal separates instruction following, unchanged-content consistency, and visual quality across turns. Their existence refutes a novelty claim for “agents inspect an image and retry,” while their reported gains do not validate this project’s proposed orchestration. ([Idea2Img](https://arxiv.org/html/2310.08541v2); [MIRA, 2026 proceedings](https://openaccess.thecvf.com/content/CVPR2026F/html/Zeng_MIRA_Multimodal_Iterative_Reasoning_Agent_for_Image_Editing_CVPRF_2026_paper.html); [IEA](https://github.com/OpenDFM/Image_Edit_Agent); [EdiVal](https://arxiv.org/html/2509.13399v3))

The defensible project-specific opportunity is narrower and useful: **a category-aware reference ontology, validated explanatory descriptors, backend capability checking, and regression-controlled correction for collectible-card art**. Whether that combination improves acceptance or reduces attempts is an empirical question.

### Begin with a small feature set that answers actual production questions

| Initial feature family | Why it earns inclusion | Defer |
|---|---|---|
| Format/aperture | Exact delivery and crop checks | Automatic designer-intent inference |
| Reviewed subject geometry | Occupancy, margins, centroid, crop/contact | Universal shape-style score |
| Regional value | Broad tonal organization and boundary separation | Recovered exposure or key/fill |
| Role-based chroma | Background competition and palette roles | Physical CCT |
| Regional detail energy | Subject/background detail allocation | Universal painterliness |
| Category grounding/context | Floating versus supported versus integrated | Full scene reconstruction |
| Actual-size recognition | Tests the practical goal | Eye tracking unless needed |
| Same-content regression | Detects damaged protected regions | One aggregate style score |

The current thumbnails can support qualitative category and hierarchy annotation immediately. Higher-resolution originals are needed before fine texture, edge, and material targets become credible. Their absence is not a reason to stop ontology design, measurement definitions, or controlled synthetic calibration fixtures.

### Stage the research before committing to architecture

| Stage | Research activity | Deliverable | Decision criterion |
|---|---|---|---|
| A. Define evidence | Audit references, categories, apertures, roles, applicability | Reference index and short art-direction glossary | Reviewers agree what is being compared |
| B. Validate descriptors | Use known geometry/color fixtures and reviewed perturbations | Repeatability and cross-response report | Features detect intended differences without obvious confounds |
| C. Establish human targets | Blinded paired judgments and actual-size tasks | Provisional acceptance bands and disagreement record | Measurements predict useful decisions |
| D. Compare actuators | Deterministic edit versus one documented editor/control route | Paired target-improvement/preservation results | Added complexity earns measurable value |
| E. Test bounded iteration | Limited correction rounds with rollback | Attempt budget, acceptance, regression, and review rates | Loop improves outcomes over simpler baselines |
| F. Escalate selectively | Learned masks, style features, structural controls, 3D, or adaptation | Incremental-value experiment | Solves a demonstrated unresolved failure |

Do not begin by implementing thirteen autonomous specialists, a universal compiler, a large feature warehouse, and several model backends. First establish whether a small evidence-driven checklist plus a few measurements improves judgments over a plain reference-guided workflow.

### The benchmark should expose failure modes, not only rank attractive outputs

A compact benchmark should cover all four object categories, varied object identities/materials, and several independent references. Split by source/card family; keep crops and iterations together. Preserve development, calibration, and final test roles. When data is too small for a stable held-out estimate, report that limitation and use provisional leave-one-card-out diagnostics.

Include same-content/different-style and different-content/same-style pairs, correct style with a local defect, wrong style with matching palette, reference-content leakage, missing diagnostic parts, category-inappropriate backgrounds, contact-shadow failures, and subtle valid variation. Compare text-only/ref-only generation, one-shot targeted editing, deterministic correction where applicable, and bounded evaluated iteration under equal declared attempt budgets.

Measure target improvement, protected-axis regression, final acceptance, false accepts/rejects, abstention, reviewer agreement, actual-size recognition, and attempts/time/spend once genuinely measured. Do not publish projected runtimes, memory fit, or cost estimates as observations.

The benchmark should also test what the agent system adds. Compare semantic critique alone with critique plus deterministic evidence. If the numerical machinery does not change decisions or reduce failure, it should not be retained merely because it produces impressive-looking dashboards.

### Currentness and unresolved evidence remain explicit

The corpus contains current 2025/2026 work in segmentation, depth, relighting, color control, edge detection, layout, counting, scanpaths, agentic editing, and style evaluation. That breadth establishes relevant prior art, not a guarantee that all releases are mature, permissively licensed, or executable on the workstation.

High-confidence conclusions concern mathematical definitions, documented interfaces, and explicit limitations. Domain applicability and performance remain unvalidated. Some sources were available only as abstracts, project descriptions, or repository documentation; the appendices retain those access boundaries. Published `.pdf` URLs remain valid citations. No blanket exclusion of legitimate PDF publications is implied.

This synthesis used the thirteen notes, proportionate cross-checks against the local brief, and two official documentation rechecks. It did not perform new broad research, generate images, install dependencies, download weights, upload references, or run external repository code. The original lanes’ provider usage and individual verification limits remain documented in their appendices.

## Conclusion

The most productive reformulation is not “find one definitive tool for each artistic category,” but **define which observable evidence would justify a particular correction, then choose the least disruptive control capable of making it**. This preserves the value of formal decomposition while avoiding the false inference that named categories are independent numerical actuators.

A successful research prototype would demonstrate calibrated decisions and controlled improvements, including knowing when not to edit. Exactness should be concentrated where it is real—geometry, authored parameters, copied pixels, output contracts—and uncertainty exposed where interpretation and inverse problems remain. That boundary is not an obstacle to automation; it is what makes the resulting automation auditable.

## Primary-source bibliography

The following curated index maps principal claims to standards, original research, and official implementations. Dates identify publication or inspected documentation state, not guaranteed latest versions. Closely related documentation and code are grouped. Additional specialist sources and license evidence remain in the detailed notes.

### Foundations, terminology, and deterministic measurement

| Source | Date/status | Claim supported |
|---|---|---|
| [Getty: formal analysis](https://www.getty.edu/education/teachers/classroom_resources/formal_analysis.html) | Museum educational resource | Elements, principles, and compositional interpretation |
| [Duke: visual analysis](https://wrp.duke.edu/sites/twp.duke.edu/files/file-attachments/visual-analysis.original.pdf) | University guide | Analysis exceeds observation alone |
| [CSS Color 4 snapshot](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/) | 2026-10-29 Candidate Recommendation Draft | Color spaces, transfer functions, hue, gamut, distance conventions |
| [ICC profile introduction](https://www.color.org/iccprofile.xalter) | Standards organization documentation | Profile-dependent color interpretation |
| [CIE chroma](https://cie.co.at/eilvterm/17-22-074) and [CCT](https://cie.co.at/eilvterm/17-23-068) | 2020 terminology | Perceptual attributes versus source temperature |
| [W3C relative luminance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | WCAG 2.2 explanation | sRGB decoding and relative \(Y\), not artistic thresholds |
| [Oklab](https://bottosson.github.io/posts/oklab/) | 2020; later updates | Coordinate model and intended use |
| [CIEDE2000 test resource](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/) | Sharma et al., 2005 | Implementation pitfalls and reference pairs |
| [Color Harmonization](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf) | Cohen-Or et al., 2006 | Hue templates, spatial constraints, limitations |
| [Color combination preferences](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf) | Schloss and Palmer, 2011 | Harmony differs from preference and contrast |
| [Scikit-image measure](https://scikit-image.org/docs/stable/api/skimage.measure.html), [features](https://scikit-image.org/docs/stable/api/skimage.feature.html), [morphology](https://scikit-image.org/docs/0.26.x/api/skimage.morphology.html) | Inspected 2026 | Region, edge, texture, and morphology definitions |
| [OpenCV shape](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html), [features](https://docs.opencv.org/4.13.0/dd/d1a/group__imgproc__feature.html), [calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) | 4.13.0 documentation | Contours, lines, projection, calibration |
| [Pillow ImageCms](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html) and [Colour](https://github.com/colour-science/colour) | Inspected 2026 | Color-managed processing and explicit conversions |
| [POT](https://pythonot.github.io/) | Official documentation | Distribution transport and solver semantics |
| [SciPy FFT](https://docs.scipy.org/doc/scipy/tutorial/fft.html) and [PyWavelets SWT](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html) | Official documentation | Frequency, multiscale, padding, normalization |
| [SVG patterns](https://www.w3.org/TR/SVG2/pservers.html#Patterns) | SVG 2 | Exact constructive repetition |

### Lighting, geometry, material, and perception

| Source | Date/status | Claim supported |
|---|---|---|
| [Blender lights](https://docs.blender.org/manual/en/latest/render/lights/light_object.html) and [PBRT area lights](https://www.pbr-book.org/4ed/Light_Sources/Area_Lights) | Official manuals/textbook | Forward lighting controls and coupled appearance |
| [Bas-relief ambiguity](https://link.springer.com/article/10.1023/A:1008154927611) | Belhumeur et al., 1999 | Non-unique geometry/reflectance/lighting |
| [Irradiance environment maps](https://graphics.stanford.edu/papers/envmap/) | Ramamoorthi and Hanrahan, 2001 | Low-frequency diffuse SH representation |
| [Blender cameras](https://docs.blender.org/manual/en/latest/render/cameras.html) | Official documentation | Projection, framing, focus, aperture |
| [Vision and the Atmosphere](https://cave.cs.columbia.edu/old/publications/pdfs/Narasimhan_IJCV02.pdf) | Narasimhan and Nayar, 2002 | Attenuation and airlight |
| [Discriminative Blur Detection](https://openaccess.thecvf.com/content_cvpr_2014/html/Shi_Discriminative_Blur_Detection_2014_CVPR_paper.html) | Shi et al., 2014 | Blur evidence beyond one sharpness scalar |
| [Material perception](https://pubmed.ncbi.nlm.nih.gov/24291494/) | Fleming, 2014 | Appearance does not require BRDF recovery |
| [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) | Blender 4.5 | Separate forward material parameters |
| [Portilla–Simoncelli texture](https://www.cns.nyu.edu/~lcv/texture/) | 2000; maintained project page | Higher-order multiscale texture representation |
| [Measuring visual clutter](https://jov.arvojournals.org/article.aspx?articleid=2122001) | Rosenholtz et al., 2007 | Clutter differs from edge count |
| [Line of Action](https://team.inria.fr/imagine/the-line-of-action-an-intuitive-interface-for-expressive-character-posing/) | Guay et al., 2013 | View-dependent artistic gesture abstraction |
| [Emotional Expressions Reconsidered](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/) | Barrett et al., 2019 | Facial movement does not uniquely diagnose emotion |
| [Getty design principles](https://www.getty.edu/education/teachers/building_lessons/principles_design.pdf) | Educational resource | Pattern and rhythm terminology |
| [Rule-of-thirds evaluation](https://doi.org/10.1163/22134913-00002024) | Amirshahi et al., 2014 | Composition-rule scores are not universal quality |

### Learned estimators and current control research

| Source | Date/status | Claim supported |
|---|---|---|
| [SAM 2](https://github.com/facebookresearch/sam2) and [SAM 3](https://github.com/facebookresearch/sam3) | 2024–2026 | Prompted masks; different licenses/access requirements |
| [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) and [rembg](https://github.com/danielgatis/rembg) | Inspected 2026 | Foreground assistance; wrapper/model distinction |
| [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) and [V3](https://github.com/ByteDance-Seed/Depth-Anything-3) | 2024–2026 | Depth variants, representation and license differences |
| [MoGe](https://github.com/microsoft/MoGe) | Includes 2026 MoGe-3 | Learned geometry and deployment qualifications |
| [GeoCalib](https://github.com/cvg/GeoCalib) | ECCV 2024 | Learned-plus-geometric calibration |
| [Marigold](https://github.com/prs-eth/Marigold) | 2024–2025 extensions | Diffusion-based depth/normals/intrinsics |
| [MEMO](https://github.com/cplusx/MEMO_Edge_Detection) | CVPR 2026 | Crisp predicted edges, not source-stroke truth |
| [MediaPipe pose](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker) and [face](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker) | Guides inspected 2026 | Landmark and blendshape representations |
| [MMPose](https://github.com/open-mmlab/mmpose), [DWPose](https://github.com/IDEA-Research/DWPose), [Human-Art](https://github.com/IDEA-Research/HumanArt), [AP-10K](https://github.com/AlexTheBad/AP-10K) | 2021–2026 resources | Domain/topology-dependent pose estimation |
| [DeepGaze](https://github.com/matthias-k/DeepGaze) and [MSDB](https://openaccess.thecvf.com/content/ICCV2025/html/Kummerer_Modeling_Saliency_Dataset_Bias_ICCV_2025_paper.html) | Includes ICCV 2025 | Fixation prediction and dataset/viewing biases |
| [DeepGaze3.5-VL](https://arxiv.org/abs/2607.02083) | 2026 preprint | Current sequential attention research |
| [SALICON](https://openaccess.thecvf.com/content_cvpr_2015/html/Jiang_SALICON_Saliency_in_2015_CVPR_paper.html) | CVPR 2015 | Mouse-contingent saliency provenance |
| [CountGD++](https://github.com/niki-amini-naieni/CountGDPlusPlus) | CVPR 2026 | Prompted motif/instance counting |
| [ControlNet](https://github.com/lllyasviel/ControlNet) | ICCV 2023 | Structural conditioning |
| [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter), [InstantStyle](https://github.com/instantX-research/InstantStyle), [Only-Style](https://arxiv.org/abs/2506.09916) | 2023–2025 | Reference conditioning and content-leakage controls |
| [GLIGEN](https://github.com/gligen/GLIGEN) and [ConsistCompose](https://github.com/opensensenova/consistcompose) | 2023 / CVPR 2026 | Box/instance-bound layout control |
| [Palette-based Photo Recoloring](https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/index.php) | SIGGRAPH 2015 | Interpretable palette editing |
| [SW-Guidance](https://github.com/alobashev/sw-guidance) and [Palette Aligned Image Diffusion](https://arxiv.org/html/2509.02000) | 2025 | Distribution/palette-conditioned generation |
| [ColourCrafter](https://eccv.ecva.net/virtual/2026/poster/4439) | ECCV 2026 | Region-aware color editing; release caveats in notes |
| [IC-Light](https://github.com/lllyasviel/IC-Light) | 2024–2025 repository | Learned foreground relighting |
| [PIXLRelight paper](https://arxiv.org/abs/2605.18735) and [code](https://github.com/mlfarinha/pixlrelight) | 2026 preprint | Intrinsic/PBR conditioning; MIT code, NC weights |
| [Materialist](https://arxiv.org/abs/2501.03717) | 2025 preprint / 2026 journal | Prior-conditioned material editing |

### Backends, evaluation, and statistical validity

| Source | Date/status | Claim supported |
|---|---|---|
| [OpenAI image guide](https://developers.openai.com/api/docs/guides/image-generation) | Rechecked 2026-10-31 | Current models, editing, mask limitations |
| [Google image guide](https://ai.google.dev/gemini-api/docs/image-generation) | Inspected in lane 12 | Model-specific references/editing/output controls |
| [BFL release notes](https://docs.bfl.ml/release-notes) and [OpenAPI](https://api.bfl.ai/openapi.json) | October 2026 documentation | FLUX 3 controls and variant differences |
| [Qwen Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) and [FLUX.2](https://github.com/black-forest-labs/flux2) | 2025–2026 | Open editing options and model-specific terms |
| [Diffusers reproducibility](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/reusing_seeds.md) and [IP-Adapter controls](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/ip_adapter.md) | Official documentation | Seed limits and architecture-specific controls |
| [Idea2Img](https://arxiv.org/html/2310.08541v2) | 2023/2024 | Iterative visual feedback prior art |
| [MIRA](https://openaccess.thecvf.com/content/CVPR2026F/html/Zeng_MIRA_Multimodal_Iterative_Reasoning_Agent_for_Image_Editing_CVPRF_2026_paper.html) | 2026 proceedings | Atomic agentic edits |
| [IEA](https://github.com/OpenDFM/Image_Edit_Agent) and [EdiVal](https://arxiv.org/html/2509.13399v3) | 2025–2026 | Interpretable retouching and multi-turn evaluation |
| [SSIM](https://ece.uwaterloo.ca/~z70wang/research/ssim/) | 2004 | Full-reference image quality |
| [LPIPS](https://github.com/richzhang/PerceptualSimilarity) and [DISTS](https://github.com/dingkeyan93/DISTS) | 2018 / 2020–2021 | Perceptual structure/texture distances |
| [Gatys style representation](https://arxiv.org/abs/1508.06576) | 2015/2016 | Feature correlations and spatial-information limits |
| [CLIP](https://proceedings.mlr.press/v139/radford21a.html), [DINOv2](https://github.com/facebookresearch/dinov2), [DINOv3](https://github.com/facebookresearch/dinov3) | 2021–2025 | General representations, not style truth |
| [ALADIN](https://arxiv.org/abs/2103.09776) and [CSD](https://arxiv.org/html/2404.01292v1) | 2021 / 2024 | Style-oriented retrieval |
| [CSD repository warning](https://github.com/learn2phoenix/CSD) | Live warning checked in lane 11 | Released-weight discrepancy |
| [ASTRA](https://arxiv.org/html/2610.10003v1) | 2026-10-07 preprint | Human-aligned style-transfer evaluation and limits |
| [StyleDecoupler](https://arxiv.org/html/2601.17697v1) | 2026-01-25 preprint | Content-suppression proposal; methodological qualifications |
| [FID bias](https://openaccess.thecvf.com/content_CVPR_2020/html/Chong_Effectively_Unbiased_FID_and_Inception_Score_and_Where_to_Find_CVPR_2020_paper.html), [KID](https://arxiv.org/abs/1801.01401), [ArtFID](https://github.com/matthias-wright/art-fid), [Clean-FID](https://github.com/GaParmar/clean-fid) | 2018–2022 | Distribution evaluation, sampling and preprocessing limits |
| [Bootstrap cautions](https://arxiv.org/abs/1411.5279) and [conformal introduction](https://arxiv.org/abs/2107.07511) | 2014/2015; first posted 2021 | Small-sample uncertainty and coverage assumptions |
| [PyTorch HIP](https://github.com/pytorch/pytorch/blob/main/docs/source/notes/hip.rst), [AMD compatibility](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html), [Blender HIP](https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html) | Official documentation | Hardware/backend distinctions |
| [Blender licensing](https://www.blender.org/about/license/) | Official explanation | Software versus created-artwork rights |

## Detailed research appendices

These notes retain extended formulas, source registers, access limitations, licensing qualifications, alternative methods, and lane-specific research records. They are supporting evidence, not additional claims that the proposed pipeline has been implemented.

| Note | Detailed scope |
|---|---|
| [01 — Lighting and value](measuring-visual-style-notes/01%20lighting%20and%20value.md) | Roles, source geometry, shadow appearance, ratios, tonal analysis, relighting |
| [02 — Color and palette](measuring-visual-style-notes/02%20color%20and%20palette.md) | Color coordinates, distributions, harmony, transport, recoloring |
| [03 — Composition and format](measuring-visual-style-notes/03%20composition%20and%20format.md) | Apertures, occupancy, margins, balance, arrangements, layout control |
| [04 — Edges, lines, and vectors](measuring-visual-style-notes/04%20edges%20lines%20and%20vectors.md) | Boundary profiles, strokes, contours, orientation, curvature |
| [05 — Depth, perspective, and optics](measuring-visual-style-notes/05%20depth%20perspective%20and%20optics.md) | Projection, viewpoint, depth, atmosphere, blur, camera estimation |
| [06 — Shape, scale, and silhouette](measuring-visual-style-notes/06%20shape%20scale%20and%20silhouette.md) | Geometry, part proportions, topology, recognition, apparent volume |
| [07 — Texture, material, and finish](measuring-visual-style-notes/07%20texture%20material%20and%20finish.md) | Multiscale texture, material cues, brushwork, grain, artifacts |
| [08 — Attention, readability, and detail](measuring-visual-style-notes/08%20attention%20readability%20and%20detail.md) | Hierarchy, saliency, detail budgets, display-scale tests |
| [09 — Rhythm, pattern, and repetition](measuring-visual-style-notes/09%20rhythm%20pattern%20and%20repetition.md) | Motifs, spacing, spectra, recurrence, pattern rules |
| [10 — Gesture, expression, and staging](measuring-visual-style-notes/10%20gesture%20expression%20and%20staging.md) | Pose, facial mechanisms, eyelines, contact, instance relations |
| [11 — Style metrics and calibration](measuring-visual-style-notes/11%20style%20metrics%20and%20calibration.md) | Validity, perceptual/style metrics, uncertainty, acceptance design |
| [12 — Controllable generation and editing](measuring-visual-style-notes/12%20controllable%20generation%20and%20editing.md) | Backend capabilities, control mechanisms, agent loops, preservation |
| [13 — Reference applicability](measuring-visual-style-notes/13%20reference%20applicability.md) | Actual reference resolution, category relevance, observable limits |