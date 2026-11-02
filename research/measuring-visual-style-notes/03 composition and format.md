# 03 — Composition and format

**Checks:** primary sources retrieved; geometry proposals distinguished from published findings; current 2026 approaches included; no installs, downloads, image uploads, or machine-code execution. Research used **5 Exa searches and 5 batch-fetch calls**, with no Perplexity or Kagi Assistant. Two fetches failed; their claims remain explicitly unverified.

Research cutoff and access date: **2026-10-31**.

Scope: dimensions, aspect ratio, framing, subject placement and scale, margins, cropping, positive–negative space, mass balance, symmetry, descriptive arrangements, nested frames, and spatial relations. This chapter does **not** establish universal aesthetic quality rules.

Evidence labels:

- **D — deterministic:** directly calculated from a specified raster, coordinate system, or supplied annotation.
- **C — conditional:** deterministic only after an explicit choice of subject, mask, frame, role, or interpretation.
- **L — learned:** inferred by a trained model; downstream calculations inherit its errors.
- **N — not identifiable from the final image alone:** intent, unseen geometry, causal production settings, or universal aesthetic merit.

“Conditional” and “learned” are not mutually exclusive pipeline properties: occupancy can be calculated deterministically **conditional on** a mask produced by a learned segmenter.

## 1. What can composition measurements establish objectively?

### Takeaway

Image dimensions are clean pixel geometry; “subject occupancy,” “negative space,” and “visual balance” require additional definitions. A reproducible system should expose those definitions and their uncertainty rather than disguise a segmentation or aesthetic judgment as an objective measurement.

### Cited Findings

- `skimage.measure.regionprops` distinguishes region area, bounding-box area, filled area, convex area, extent, geometric centroid, intensity-weighted centroid, and moment-based axes. Its bounding box uses **half-open** intervals and its coordinate ordering is **row, column**, not x, y. These distinctions directly matter to interoperable measurement schemas. — [Official measurement API](https://scikit-image.org/docs/stable/api/skimage.measure.html)

- Raw image moments support area and centroid calculations; geometric and intensity-weighted centroids are different quantities. A measurement therefore needs to specify the mass or weighting field rather than report an unexplained “center of visual weight.” — [Official measurement API](https://scikit-image.org/docs/stable/api/skimage.measure.html)

- SAM 2 predicts masks in response to prompts. Its image predictor supports points, boxes, multiple candidate masks, mask logits, and **predicted mask-quality scores**. These scores are model predictions, not independently measured correctness or proof that the selected region is the intended subject. — [Official predictor implementation](https://github.com/facebookresearch/sam2/blob/main/sam2/sam2_image_predictor.py)

- SAM 3 extends segmentation to open-vocabulary concepts specified by text or exemplars. This is useful for semantic selection, but it does not turn a semantic interpretation into direct pixel geometry. — [Official SAM 3 repository](https://github.com/facebookresearch/sam3)

- Amirshahi et al. compared calculated rule-of-thirds values with human judgments. Calculated values did not correlate with aesthetic ratings in their study, and only partially captured perceived adherence to the rule. This is evidence against treating a thirds score as a general aesthetic-quality score. — [*Evaluating the Rule of Thirds in Photographs and Paintings*, 2014](https://doi.org/10.1163/22134913-00002024)

- Hoh et al. found preferences for centered salient regions and surrounding non-salient borders in their investigated single-salient-region photographic conditions. The result is conditional on their stimuli and task; it is not a universal occupancy prescription for stylized cards. Their work explicitly leaves handling multiple salient regions for future work. — [*Salient-Centeredness and Saliency Size in Computational Aesthetics*, 2023](https://dl.acm.org/doi/10.1145/3588317)

- Current layout-generation evaluation explicitly separates **semantic alignment** from **spatial alignment**. The 2026 C-Bench/O-Bench work measures both because producing the requested object and placing it correctly are distinct capabilities. — [CVPR Findings 2026 paper](https://openaccess.thecvf.com/content/CVPR2026F/papers/Parolari_Benchmarking_Layout-Guided_Diffusion_Models_through_Unified_Semantic-Spatial_Evaluation_in_Closed_CVPRF_2026_paper.pdf)

### Inferences

The following is a **proposed project schema and mathematical operationalization**, not a published standard or validated aesthetic model. Region definitions build on the distinctions in the [official measurement API](https://scikit-image.org/docs/stable/api/skimage.measure.html).

#### Establish the coordinate contract first

Store separately:

1. **Delivered canvas:** decoded width \(W\), height \(H\), aspect \(r=W/H\).
2. **Card/interior analysis window:** rectangle \(R=(L,T,W_R,H_R)\).
3. **Valid region:** mask \(V\subseteq R\), allowing rounded corners, holes, or nonrectangular interiors.
4. **Subject instance masks:** \(M_i\subseteq V\), or explicitly documented amodal masks if available.
5. **Exclusion/decorative layers:** card frame, title, badges, decorative elements, shadow, and effects.

Normalize coordinates relative to the chosen rectangle:

\[
u=(x-L)/W_R,\qquad v=(y-T)/H_R.
\]

Use top-left origin; x/right and y/down. Store which domain a feature uses: `canvas`, `card_interior`, or another named frame.

For pixel-center calculations, use \(x=j+0.5,\ y=i+0.5\). For a raster mask’s box, use **pixel edges**:

\[
u_0=j_{\min}/W_R,\quad
u_1=(j_{\max}+1)/W_R
\]

and equivalent y expressions. This avoids counting a boundary-touching mask as having a one-pixel safety margin.

Preprocessing fields should record:

- orientation correction;
- source crop and crop transform;
- analysis window;
- validity mask;
- raster dimensions and any resizing;
- mask interpolation and threshold;
- treatment of transparency and antialiasing;
- inclusion/exclusion of shadows, glows, supports, handles, accessories, and detached parts;
- segmentation model/version and prompts, if applicable.

Do not silently center-crop rectangular cards into squares. Do not stretch them to a square before calculating orientation, symmetry, radial spacing, or Euclidean distances.

#### Separate three kinds of “subject mask”

Use distinct fields rather than one universal foreground mask:

- `subject_visible`: visible object surface, including thin structural parts.
- `subject_plus_attached`: explicitly selected accessories/supports belonging to the subject assembly.
- `presentation_footprint`: subject plus selected shadow/glow/effects.

A long shadow can materially move the footprint centroid without moving the object. A handle hole can legitimately contribute negative space. Filling all holes changes the quantity being measured.

Alpha is not necessarily a subject mask: a finished card can be opaque everywhere, while an exported object sprite can include translucent shadow pixels. Treat alpha as an available geometric channel, not automatic semantic ground truth.

#### Candidate feature registry

All formulas below are **proposed operational definitions**. Empty or unidentified masks should yield `null/undefined` plus a failure reason, not apparently valid zeros.

| Feature | Definition / units | Class | Interpretation and limitation |
|---|---|---|---|
| Canvas dimensions | \(W,H\), pixels | D | Exact delivered format after declared orientation handling. |
| Canvas aspect | \(W/H\); optional \(\log(W/H)\) | D | Not necessarily the aspect of the inner card aperture. |
| Interior frame | \(R\), plus valid mask \(V\) | D if supplied; C/L if inferred | Detecting a rectangle is not identifying its semantic function. |
| Instance count | Number of selected semantic instances | C/L | Connected-component count is not object count. |
| Visible bounding box | \(B=(u_0,v_0,u_1,v_1)\) | C; L upstream if segmented | Measures visible support, not necessarily complete object extent. |
| Box width/height | \(b_w=u_1-u_0,\ b_h=v_1-v_0\) | C | Keep both axes; area alone hides tall/narrow versus short/wide placement. |
| Box area | \(A_B=b_wb_h\), fraction of rectangular domain | C | Includes empty space inside the box. |
| Mask occupancy | \(A_R=\sum M/(W_RH_R)\) | C | Actual selected-mask coverage of the rectangle. |
| Valid-region occupancy | \(A_V=\sum M/\sum V\) | C | Different denominator; important for rounded or irregular apertures. |
| Extent | Selected mask pixels / box pixels | C | Shape/pose-sensitive; not solely composition. |
| Equivalent linear scale | \(\sqrt{A_R}\) | C | Useful area-derived size summary; does not replace width/height. |
| Box center | \(((u_0+u_1)/2,(v_0+v_1)/2)\) | C | Different from mask centroid. |
| Geometric centroid | \((\sum uM/\sum M,\sum vM/\sum M)\) | C | Uniform area mass, not perceived importance. |
| Center offset | \(c-(0.5,0.5)\) | C | Preserve signed x/y components. |
| Four margins | \(m_L=u_0,\ m_R=1-u_1,\ m_T=v_0,\ m_B=1-v_1\) | C | Relative to the declared rectangular frame. |
| Irregular-frame clearance | Minimum distance from subject to relevant boundary of \(V\) | C | Needed when rectangle margins miss rounded corners. |
| Minimum safety clearance | Minimum declared boundary clearance; normalized by short side or stored in pixels | C | Minimum is sensitive to thin tips and segmentation noise. |
| Edge contact | Per-side mask contact, or occupancy in a declared edge band | C | Evidence of contact, not proof of accidental cropping. |
| Intended cutoff | Human label or prescribed layout property | N from pixels alone | Distinguish deliberate bleed from a failed crop. |
| Missing subject fraction | Visible/amodal comparison, if trustworthy amodal annotation exists | C/L with amodal information; otherwise N | Cannot recover exact unseen area from visible pixels alone. |
| Negative-space fraction | \(1-A_V\), under declared positive-mask policy | C | “Not the subject” is not automatically perceptually empty. |
| Negative-space distribution | Fractions by side, quadrant, or fixed grid | C | More informative than a single fraction. |
| Geometric mass imbalance | Half-plane area differences divided by total selected mass | C | Descriptive geometric balance, not aesthetic balance. |
| Weighted center | \(\sum p\,w(p)/\sum w(p)\) | D for supplied weight field; C/L interpretation | Specify luminance, contrast, saliency, alpha, or another field. |
| Mirror overlap | IoU between selected mask and its reflected copy about a declared axis | C | Sensitive to pose and silhouette; can be high for a frame alone. |
| Dominant axis | Second-moment/PCA axis in physical image coordinates | C | Often poorly defined for nearly isotropic shapes. |
| Third-grid proximity | Distance from declared anchor to thirds lines/intersections | C | Alignment descriptor only. |
| Third-grid saliency mass | Saliency-weighted mass near a fixed thirds template | L, or C for supplied map | Not proof of subject selection, intention, or quality. |
| Golden-grid proximity | Analogous distance to declared golden-section lines | C | Not the rule of thirds; no quality inference. |
| Radial arrangement | Angular positions, radial distances, dispersion, angular gaps | C | Requires a declared center and meaningful selected instances. |
| Pyramidal arrangement | Residual to an explicitly selected apex/base or triangle hypothesis | C/L role selection | An unconstrained triangle can fit many unrelated layouts. |
| Frame-within-frame | Enclosure geometry and relative placement within a selected inner frame | C/L | Detecting enclosure does not establish intended framing. |
| Relation graph | Nodes with boxes/masks; edges for ordering, separation, containment, overlap | C/L | Depth, support, and semantic relations need additional evidence. |
| Designer intent / universal beauty | No unique pixel formula | N | Human interpretation or project preference must remain separate. |

#### Non-square formats need two coordinate systems

Use normalized \((u,v)\) for placement specifications, but preserve physical aspect for distances and angles.

For an aspect-correct, diagonal-normalized distance:

\[
d_r(p,q)=
\frac{\sqrt{r_R^2(u_p-u_q)^2+(v_p-v_q)^2}}
{\sqrt{r_R^2+1}},
\qquad r_R=W_R/H_R.
\]

A unit-square calculation makes horizontal and vertical movements look equivalent even when their pixel lengths differ.

Store box aspect in physical coordinates:

\[
r_B=\frac{W_Rb_w}{H_Rb_h}.
\]

Compute PCA angles and radial angular gaps in physical coordinates or coordinates divided by a common scalar, such as the short side—not independently normalized x and y.

#### Positive–negative space is a segmentation-dependent statement

For selected positive masks:

\[
M_+=\bigcup_i M_i,\qquad N=V\setminus M_+.
\]

This gives **geometric complement space**. It does not certify that \(N\) is visually quiet: background patterns, text, sparkles, or high-contrast frame ornaments can occupy it perceptually.

Store separately:

- geometric complement occupancy;
- interior holes in the subject;
- border-connected complement regions;
- intentionally reserved regions, such as title space;
- optional saliency or contrast distribution.

A reserved region \(Q\) can have a deterministic obstruction measure:

\[
o_Q=\frac{|M_+\cap Q|}{|Q|}.
\]

However, suitability for text also depends on features outside this chapter; do not equate low subject overlap with guaranteed readability.

Do not automatically discard detached components as noise. They may be a lid, handle segment, floating ingredient, or intentionally separate prop. Record the component-selection rule and retain reviewable overlays.

#### Card borders and frames can dominate otherwise sensible measurements

A thick decorative border can:

- become the largest connected component;
- force a detected foreground box to fill the canvas;
- make symmetry look excellent;
- add high edge density on every side;
- pull saliency toward corners or decorative badges;
- conceal the actual interior margins.

Recommended measurement separation:

1. full-canvas format;
2. card/frame geometry;
3. subject layout inside the card;
4. presentation-footprint layout;
5. optional full-image attention distribution.

Do not remove the border from every analysis. Its layout is part of card composition. Remove it only from measurements explicitly intended to describe **the subject**.

If an inner frame is inferred, retain its uncertainty. For asymmetric or partial frames, a single automatic inset can be misleading. Measure the declared aperture or request annotation rather than invent a symmetric inset.

#### Mass balance is not one universal center-of-mass calculation

For uniform mask mass, define:

\[
B_x=\frac{A_{\text{right}}-A_{\text{left}}}{A_{\text{total}}},
\qquad
B_y=\frac{A_{\text{bottom}}-A_{\text{top}}}{A_{\text{total}}}.
\]

These are signed geometric descriptors. They do not model semantic importance, gaze direction, apparent weight, or attention.

Report geometric and optional weighted variants separately. In particular:

- dark regions are not universally “heavier” under every context;
- a small high-contrast badge can draw attention despite small area;
- different saliency models can yield different balance estimates;
- equal left/right area does not imply equal moment arms;
- a centered centroid does not imply mirror symmetry.

Avoid an unlabeled scalar called `visual_balance_score`.

#### Thirds, golden sections, triangles, and radial arrangements are hypotheses

For thirds intersections:

\[
G_3=\{(1/3,1/3),(1/3,2/3),(2/3,1/3),(2/3,2/3)\}.
\]

A centroid-to-grid descriptor can be:

\[
d_3(c)=\min_{g\in G_3}d_r(c,g).
\]

For saliency map \(S\) and a **predeclared** grid-band template \(K_\sigma\):

\[
T_3=
\frac{\sum_{p\in V}S(p)K_\sigma(p)}
{\sum_{p\in V}S(p)}.
\]

Store the map model, template, band width, masking policy, and whether the template uses lines or intersections. Compare against the template’s uniform-area baseline: broad bands or large salient regions can produce high overlap without meaningful selective alignment.

A saliency centroid can fall between several salient regions, even in empty space. Retain component-level or full-map information where relevant.

For golden sections, \(\phi=(1+\sqrt5)/2\), with lines near \(1/\phi^2\) and \(1/\phi\), approximately 0.382 and 0.618. These are **not** thirds. A fitted golden grid is not evidence of historical intention or aesthetic superiority.

Likewise:

- “Pyramidal” needs specified apex and base roles, orientation, and allowable residual.
- “Radial” needs a meaningful center, selected spokes/instances, and physical-coordinate angles.
- A golden spiral fit needs a fixed family, orientation, origin, and fitting freedom. Searching many overlays and reporting the best is weak evidence.

Use labels such as `compatible_with_radial_hypothesis`, not `objectively_good_composition`.

### Gaps

- No reference cards or annotations were inspected. Their actual occupancy, crop policy, framing conventions, and acceptable variability remain unknown.
- The cited photographic preference studies do not validate universal thresholds for stylized game-object cards.
- No universal numerical boundary between “balanced,” “crowded,” “safe,” and “too empty” was established. Such targets must be calibrated to the project.
- Designer intent, exact unseen object extent, and the original camera/placement workflow are not uniquely recoverable from a finished raster.

## 2. How should reference features become prompts, evaluations, and isolated corrections?

### Takeaway

Use a small explicit layout contract, retain separate semantic and geometric evaluations, and correct the lowest-level controllable cause. Numeric box controls or deterministic canvas operations are more auditable than repeatedly asking for “better composition.”

### Cited Findings

- GLIGEN conditions generation on grounding inputs including text-linked boxes and supports grounded inpainting. It establishes practical prior art for controlling placement separately from a global text description. — [Official GLIGEN repository](https://github.com/gligen/GLIGEN)

- BoxDiff introduces training-free box-constrained diffusion. Its official examples bind phrases to boxes; the documented Diffusers example converts pixel boxes into normalized coordinates. This is an implementation pattern, not a guarantee of exact adherence. — [Official BoxDiff repository](https://github.com/showlab/BoxDiff)

- ControlNet supports spatial controls including edges, scribbles, segmentation, depth, and normals. These controls constrain more than a box: they can carry silhouette, pose, and internal geometry. — [Official ControlNet repository](https://github.com/lllyasviel/ControlNet)

- LayoutGPT separates layout planning from downstream image generation and provides separate layout and image evaluation. This is relevant prior art for an inspectable intermediate representation rather than a monolithic prose-only prompt. — [Official LayoutGPT repository](https://github.com/weixi-feng/LayoutGPT)

- ConsistCompose, published at CVPR 2026, binds normalized box coordinates directly into prompts using trained instance-coordinate binding. Its repository demonstrates syntax such as `<bbox>[…]</bbox>`. This is a **model-specific learned interface**, not evidence that arbitrary generators understand numeric coordinates reliably. — [CVPR 2026 paper](https://openaccess.thecvf.com/content/CVPR2026/html/Shi_ConsistCompose_Unified_Multimodal_Layout_Control_for_Image_Composition_CVPR_2026_paper.html); [official repository and examples](https://github.com/opensensenova/consistcompose)

- OverLayBench identifies overlapping boxes, particularly for semantically similar instances, as a difficult layout-generation regime. It reports blending, ambiguity, and distortion, and investigates amodal-mask supervision as an improvement direction. — [Primary paper, 2025](https://arxiv.org/html/2509.19282v1)

### Inferences

The workflow below is a **proposed engineering protocol**, informed by the cited layout-control interfaces. Its targets and acceptance limits require project calibration.

#### Reference schema: keep observations, targets, and interpretations separate

A useful record should contain:

| Group | Fields |
|---|---|
| Provenance | Reference ID, measurement date, source dimensions, annotation version |
| Format | Canvas dimensions/aspect; interior frame and valid-region definitions |
| Subject policy | Main subject role; attached parts; shadow/effect policy; visible versus amodal |
| Layout | Per-instance box, centroid, occupancy, four margins, edge-contact flags |
| Distribution | Reference-family distribution of width, height, occupancy, centers, and margins |
| Relations | Relative ordering, gaps, overlaps, containment, selected anchor alignments |
| Hypotheses | Centered, radial, pyramidal, thirds-compatible, nested-frame; confidence and annotator |
| Confidence | Mask source; model/version; prompts; candidate disagreement; human review |
| Targets | Desired values/ranges and their reference-derived provenance |
| Locks | Attributes that must not change during correction |
| Unknowns | Uncertain subject assignment, crop intent, frame aperture, depth order |

Keep **observed** and **requested** boxes separate. Otherwise a failed generation can overwrite the target it was supposed to meet.

For uncertainty, store at least:

- `subject_identification_status`;
- `mask_review_status`;
- `mask_quality_prediction`, if provided by the model;
- candidate-mask disagreement;
- feature sensitivity to reasonable mask variations;
- frame/crop ambiguity.

Do not combine all of these into an unexplained confidence percentage.

#### Calibrate a family, not one “ideal” card

Measure representative accepted references and preserve their size distribution:

- box width and height jointly;
- mask occupancy;
- center coordinates;
- each margin;
- aspect family;
- crop/contact frequency;
- object-count and arrangement family.

Use medians, quantiles, and observed ranges as summaries, not aesthetic laws. With very few references, report the sample size and show individual values.

Stratify where necessary:

- portrait versus landscape;
- single object versus multi-object assembly;
- tall/narrow versus broad/compact silhouette;
- intentional bleed versus fully contained subject;
- borderless versus heavily framed cards.

Do not force a thin tool and a round container to share mask-area occupancy merely because both are “single objects.” Their box placement can match while their silhouette fill differs.

Safety margins should reflect the intended export/display/crop pipeline and accepted references. A margin measured at source resolution may disappear after a later delivery crop.

#### Prompt-ready vocabulary

These are proposed, literal spatial descriptions—not empirically validated magic words.

| Axis | Useful vocabulary | Prefer over |
|---|---|---|
| Format | “portrait 4:5 canvas”; “landscape 3:2”; “square output” | “card-shaped” |
| Subject scale | “subject box spans approximately … of width and … of height” | “large” |
| Placement | “box center at …”; “shift the subject right without resizing” | “improve balance” |
| Full containment | “entire subject visible, including handle/tips/base”; “no edge contact” | “uncropped” alone |
| Negative space | “reserve a clear region above”; “keep the right-side region free of subject overlap” | “more breathing room” alone |
| Margins | “preserve the bottom clearance”; “equalize left/right box margins” | “center nicely” |
| Multiple objects | “A left of B with a visible gap”; “B contained within frame C” | “harmonious arrangement” |
| Nested framing | “center the subject within the inner aperture, not the outer canvas” | “centered” |
| Symmetry | “mirror-symmetric placement about the vertical frame axis” | “balanced” |
| Radial arrangement | “instances arranged around the specified center with specified angular spacing” | “dynamic radial composition” |
| Pyramidal arrangement | “one upper apex instance above two lower base instances” | “golden triangle” |
| Correction locks | “preserve identity, silhouette, pose, camera view, palette, materials, lighting and texture” | “everything else the same” |

Global prompt wording should avoid injecting unrelated content through composition language. For example, “product photography,” “cinematic close-up,” or “hero shot” may change lighting, camera presentation, and material rendering in addition to layout.

#### Worked example: illustrative numbers, not recommended thresholds

Suppose a project chooses an illustrative target:

- portrait 4:5 canvas;
- main visible-subject box \(B=[0.20,0.12,0.80,0.88]\);
- no clipping;
- shadow evaluated separately.

The target box has:

- width 0.60;
- height 0.76;
- center \((0.50,0.50)\);
- left/right margins 0.20;
- top/bottom margins 0.12;
- box area 0.456.

**It does not specify mask occupancy.** That depends on silhouette.

Prompt:

> Portrait 4:5 canvas. Show the complete existing subject, including its thin protrusions and base. Center its visible bounding box at the canvas center. The subject should span approximately 60% of canvas width and 76% of canvas height, leaving equal left/right and top/bottom box margins. Keep the cast shadow separate from the subject-size requirement. Preserve the established identity, silhouette, pose, camera view, palette, materials, lighting and texture.

For a box-conditioned model, send the actual box through its supported control interface. Prose percentages are a fallback communication channel, not an exact geometric API.

A correction prompt:

> Change horizontal placement only: move the subject right by 0.05 of the interior-frame width. Preserve its pixel scale, vertical position, shape, pose and camera view. Keep the card frame and background layout fixed.

The displacement is illustrative, not a quality threshold.

#### Composition-specific matching without copying content

Recommended matching tiers:

1. **Format matching:** dimensions, aspect, interior aperture.
2. **Role-layout matching:** main/supporting/ornamental instance boxes, centers, sizes, margins.
3. **Relation matching:** left/right, above/below, gaps, containment, overlap structure.
4. **Optional shape-distribution matching:** silhouette or mass-map agreement, explicitly marked content-sensitive.
5. **Separate aesthetic review:** project fit and perceived quality.

For role-layout comparisons, replace objects with neutral rectangles or ellipses carrying only layout information. This removes much content and texture dependence, though the initial assignment of semantic roles remains conditional.

Do not use silhouette IoU as the principal composition score across different object categories. A mug and a rake can have identical box placement but radically different silhouette IoU.

Do not permit translation/scale registration when those are the axes being evaluated. Aligning both subjects to the same center before scoring would erase the placement failure.

For multi-object scenes:

- use fixed instance IDs where possible;
- otherwise document a role-based matching procedure;
- report unmatched and extra instances separately;
- distinguish content failure from placement error for successfully identified instances;
- avoid selecting whichever detected object makes the score look best.

A proposed diagnostic vector is:

\[
e =
\left[
\left|\log\frac{r}{r^*}\right|,
\Delta c_x,\Delta c_y,
\log\frac{b_w}{b_w^*},
\log\frac{b_h}{b_h^*},
\Delta m_L,\Delta m_R,\Delta m_T,\Delta m_B,
\Delta A_R,
\text{edge contacts},
\text{relation violations}
\right].
\]

Not all components are independent: box width and margins are related. Keep that redundancy for explanation if useful, but avoid double-counting it in an aggregate score.

If aggregation is required, choose weights and tolerances from project priorities and reference variability. Do not present arbitrary constants as validated thresholds.

#### Segmentation uncertainty should propagate into measurements

Recommended checks:

- compare plausible candidate masks;
- test sensitivity to reasonable threshold changes;
- inspect whether thin tips, holes, shadows, and detached pieces are stable;
- compare learned masks against a reviewed subset;
- report feature intervals or disagreement ranges.

These are sensitivity ranges, **not statistical confidence intervals** unless a valid statistical procedure supports that interpretation.

A high predicted mask-quality score does not prove correct semantic selection. A perfectly outlined card frame is still the wrong mask for subject occupancy.

Exclude or flag unreliable measurements rather than letting a low-confidence mask trigger automated resizing.

#### Relation graphs: specify what an edge means

Recommended node fields:

- instance ID and role;
- box and visible mask;
- optional amodal annotation;
- anchor points;
- confidence.

Recommended geometric edges:

- `left_of`: define centroid ordering or complete-box separation;
- `above`: define y-ordering explicitly;
- `gap`: nearest-boundary distance or box gap;
- `overlaps_box`: box intersection;
- `contained_in`: mask/box containment fraction;
- `aligned_center_x/y`;
- `similar_scale`.

Keep these separate from:

- `in_front_of`;
- `supports`;
- `attached_to`;
- `looking_toward`;
- `semantically_related`.

Box overlap is not proof of occlusion or depth order. In a visible instance segmentation, mutually exclusive visible masks may have zero overlap while their boxes overlap substantially.

#### Lowest-collateral correction ladder

| Problem | First correction to consider | Expected coupling / risks |
|---|---|---|
| Wrong delivered dimensions only | Export/canvas setting | Resampling can affect fine detail. |
| Subject correctly rendered but off-center | Translate an existing layer or composite | Exposed background, shadow/contact mismatch, clipping. |
| Subject too large | Uniformly scale a separated subject around a declared anchor | Changes occupancy, margins, detail scale, and shadow relation together. |
| Insufficient space on one side | Extend canvas; regenerate only exposed background if needed | Outpainting can add unwanted objects or background structure. |
| Excess empty border | Explicit crop | Alters aspect, all normalized positions, and possibly cutoffs. |
| Wrong frame aperture | Adjust frame/matte independently | Can expose missing image regions or change usable space. |
| Wrong multi-object layout | Edit per-instance boxes/masks and regenerate locally | Occlusion order, shadows, contact, and identity can drift. |
| Box placement correct, silhouette wrong | Shape/edge/mask control | Stronger content/pose coupling than box control. |
| Background attention competes with subject | Edit the responsible region | This touches adjacent appearance axes; do not relabel it as purely geometric balance. |
| Camera view wrong | Camera/view conditioning or rerender | Not equivalent to a canvas translation or crop. |

“Without collateral drift” should mean **measured collateral drift under a stated edit**, not a promise of perfect disentanglement.

For deterministic scaling about anchor \(a\):

\[
p'=a+s(p-a)+t.
\]

For a crop with origin \(o\) and dimensions \(W_C,H_C\):

\[
u'=(x-o_x)/W_C,\qquad v'=(y-o_y)/H_C.
\]

These transformations explain why crop, scale, and translation can produce similar normalized boxes while having different consequences.

#### Camera crop versus placement

Keep separate controls for:

- camera orientation/elevation/perspective;
- rendered object scale;
- object placement on the canvas;
- final viewport/crop;
- canvas extension.

A phrase such as “zoom out” is ambiguous: a model might shrink the object, change the camera, invent surroundings, or alter perspective.

If the desired result is only a smaller unchanged object, say so explicitly and prefer a scale/layout operation. If the desired result is a different view, treat it as camera conditioning rather than a composition-only patch.

The final raster ordinarily cannot establish whether its placement came from camera movement, object movement, post-render scaling, or cropping.

#### Evaluate a correction as a paired experiment

Recommended protocol:

1. Preserve the original image and its feature record.
2. State the target axis and locked axes.
3. Apply one bounded operation or control change.
4. Recompute the same geometry under the same mask policy.
5. Review segmentation before interpreting changes.
6. Report target-axis improvement and collateral deltas separately.
7. Check at delivered aspect and display/crop conditions.

For stochastic generation, compare matched seeds/settings where supported, and sample more than one output when judging reliability. A fixed seed alone is not a guarantee that a prompt or control change preserves all other attributes.

### Gaps

- No project-specific target ranges, mask confidence gates, matching weights, or collateral-drift tolerances were established.
- No generator was tested for understanding the proposed prose vocabulary.
- No claim is made that a fixed seed or local edit guarantees identity, lighting, or texture preservation.
- Composition descriptors can reduce content dependence, but cannot make arbitrary object silhouettes geometrically equivalent.

## 3. Which tools and current approaches are practical, and what are their limits?

### Takeaway

Begin with reviewed masks and CPU geometry, then add layout-conditioned generation only where deterministic compositing or cropping is insufficient. Current research offers stronger instance-coordinate and overlap-aware control, but none of the reviewed evidence establishes turnkey reliability on this project’s stylized cards or AMD workstation.

### Cited Findings

#### Practical measurement baseline

**scikit-image**

- Official region measurements include area, centroid, bounding boxes, extent, second moments, and connected-region properties. These are appropriate building blocks for an auditable geometry baseline. — [Official API](https://scikit-image.org/docs/stable/api/skimage.measure.html)
- The project’s license file specifies BSD-3-Clause for the general codebase and lists file-level exceptions, including BSD-2-Clause and MIT portions. Do not simplify all bundled material to one undifferentiated license. — [Official license file](https://raw.githubusercontent.com/scikit-image/scikit-image/main/LICENSE.txt)

**Operational assessment:** use supplied or manually reviewed masks first. The arithmetic does not require learned inference or a GPU. This is the recommended baseline architecture, not a benchmark of the installed machine.

#### Learned mask assistance

**SAM 2 / SAM 2.1**

- Provides point/box-prompted image segmentation and automatic mask generation; the README lists SAM 2.1 updates from September 2024 and later video-related updates from December 2024. — [Official repository](https://github.com/facebookresearch/sam2)
- Code and checkpoints are Apache-2.0; demo fonts have separate font licenses. — [Official repository licensing section](https://github.com/facebookresearch/sam2)
- The documented installation includes a custom CUDA extension. The README says failure to build that extension can be ignored, with some postprocessing limitations. Its reported speed results are measured on an NVIDIA A100, not an RX 7900 XTX. — [Official requirements and benchmark notes](https://github.com/facebookresearch/sam2)

**Operational assessment:** useful assisted annotation, but AMD/CPU performance and compatibility remain untested here. Do not infer AMD support or speed from A100 measurements. The README’s dates do not by themselves establish abandonment or active maintenance.

**SAM 3 / SAM 3.1**

- Supports text/concept-prompted segmentation. The README records a SAM 3.1 update dated **2026-03-27**. — [Official repository](https://github.com/facebookresearch/sam3)
- Its documented prerequisites include Python 3.12+, PyTorch 2.7+, and a CUDA-compatible GPU with CUDA 12.6+. Checkpoints require requested access and authenticated download. — [Official prerequisites and access instructions](https://github.com/facebookresearch/sam3)
- It uses the custom **SAM License**, not SAM 2’s Apache-2.0 license. The license includes substantive conditions; availability should not be treated as identical licensing. — [Official license](https://github.com/facebookresearch/sam3/blob/main/LICENSE)

**Operational assessment:** current semantic-selection prior art, but not the simplest baseline for this task. The documented CUDA route, access requirements, and custom license are material adoption considerations. No access request, login, or download was performed.

#### Established layout control

**GLIGEN, CVPR 2023**

- Grounds frozen text-to-image generation using boxes and other inputs and supports inpainting. Its supplied checkpoints are based on Stable Diffusion 1.4. — [Official repository](https://github.com/gligen/GLIGEN)
- Repository code is identified as MIT, while model/demo use is additionally subject to Latent Diffusion/Stable Diffusion terms. Code license does not eliminate checkpoint obligations. — [Official repository terms](https://github.com/gligen/GLIGEN)

**Operational assessment:** clear box-conditioning baseline and useful research reference. The older checkpoint stack and application-domain gap require testing before adoption.

**BoxDiff, ICCV 2023**

- Training-free box constraints bind prompt phrases/tokens to spatial boxes. The README documents SD-XL-related work and a Diffusers community integration. — [Official repository](https://github.com/showlab/BoxDiff)
- The original setup says testing used PyTorch 1.12.0. The displayed Diffusers pipeline is explicitly a community example. — [Official repository](https://github.com/showlab/BoxDiff)

**Operational assessment:** “training-free” means no additional model training, not zero inference overhead or exact geometric enforcement. Original-stack age and integration differences are real reproducibility risks. The license was **not validated**: the attempted license-page fetch timed out. Do not assume permission merely from public availability.

**ControlNet, ICCV 2023**

- Provides edge, scribble, segmentation, depth, and normal conditioning. The official repository is Apache-2.0 and its displayed baseline documentation centers on the original Stable Diffusion-era implementation. — [Official repository](https://github.com/lllyasviel/ControlNet)

**Operational assessment:** useful when boxes are insufficient. Edge/silhouette controls can preserve unwanted object-specific shape; depth/normal controls can lock camera or geometry. A semantic segmentation control expects a particular annotation protocol—an arbitrary binary subject mask is not automatically interchangeable. Verify the chosen checkpoint and implementation, not just the method name.

#### Inspectable planning and current advanced control

**LayoutGPT, NeurIPS 2023**

- Plans layouts separately from downstream generation and supports distinct layout/image evaluation. Its repository documents dependencies on GLIGEN, GLIP, and ATISS; its news includes updates through March 2024. — [Official repository](https://github.com/weixi-feng/LayoutGPT)
- The repository is identified as MIT, but explicitly warns that downstream components retain their original terms. — [Official disclaimer](https://github.com/weixi-feng/LayoutGPT)

**Operational assessment:** strong architectural prior art for `description → layout → rendering → evaluation`. It is not evidence that an LLM planner’s proposed layout is aesthetically appropriate or constraint-satisfying. Validate coordinates and relations before generation. No external account/API use was performed.

**ConsistCompose, CVPR 2026**

- Embeds normalized coordinates into instance-bound textual prompts and supports multi-reference composition. The official repository records release of code, its BAGEL-based model, and dataset on **2026-02-27**. — [Official repository](https://github.com/opensensenova/consistcompose)
- The paper reports improved spatial accuracy on COCO-Position and MS-Bench while preserving identity-related performance in its evaluations. These are author-reported benchmark results, not stylized-card guarantees. — [CVPR paper](https://openaccess.thecvf.com/content/CVPR2026/html/Shi_ConsistCompose_Unified_Multimodal_Layout_Control_for_Image_Composition_CVPR_2026_paper.html)
- The repository states Apache-2.0 for framework/models; the dataset has additional terms for derived data. Its quickstart includes a pinned FlashAttention dependency. — [Official repository](https://github.com/opensensenova/consistcompose)

**Operational assessment:** materially current prior art for the desired feature-schema-to-concrete-control pipeline. Do not transplant its `<bbox>` syntax into an unrelated model and expect equivalent control. No verified RX 7900 XTX compatibility, memory fit, or CPU practicality was established.

**OverLayBench / CreatiLayout-AM, 2025**

- Studies dense overlapping layouts and combines box IoU with caption similarity in OverLayScore. It investigates amodal-mask supervision to reduce overlap-related artifacts. — [Primary paper](https://arxiv.org/html/2509.19282v1)

**Operational assessment:** important for cards containing stacked or overlapping components. **OverLayScore is not content-independent composition similarity:** caption embeddings are explicitly part of it. It is a model-difficulty descriptor, not a beauty score. The paper is evidence of an approach, not verified deployability; implementation licensing and AMD behavior were not validated.

#### Current evaluation prior art

**C-Bench/O-Bench, CVPR Findings 2026**

- Separates semantic and spatial evaluation and includes scenarios for small boxes, overlaps, object relations, and complex compositions. The official repository contains evaluation tools and six model setups. — [Primary paper](https://openaccess.thecvf.com/content/CVPR2026F/papers/Parolari_Benchmarking_Layout-Guided_Diffusion_Models_through_Unified_Semantic-Spatial_Evaluation_in_Closed_CVPRF_2026_paper.pdf); [official repository](https://github.com/lparolari/cobench)
- The proposed evaluation uses learned semantic/spatial components, including a zero-shot object detector. It is not a substitute for direct geometry from trustworthy masks or annotations. — [Primary paper](https://openaccess.thecvf.com/content/CVPR2026F/papers/Parolari_Benchmarking_Layout-Guided_Diffusion_Models_through_Unified_Semantic-Spatial_Evaluation_in_Closed_CVPRF_2026_paper.pdf)

**Operational assessment:** reuse its separation of failure modes and scenario design, not necessarily its full combined score. Repository licensing was not established from the retrieved README.

#### CPU and AMD considerations

- AMD’s retrieved ROCm 7.2.2 compatibility matrix documents supported GPU targets, framework versions, and operating systems. It explicitly directs Radeon users to Radeon-specific compatibility information. It also identifies itself as **not the latest** documentation. — [Official AMD matrix, dated 2026-04-23](https://rocm.docs.amd.com/en/docs-7.2.2/compatibility/compatibility-matrix.html)

**Operational assessment:**

- CPU mask geometry avoids CUDA/ROCm concerns and should be the initial implementation target.
- ROCm framework support does not establish compatibility of a repository’s custom CUDA kernels, pinned dependencies, or FlashAttention path.
- CachyOS/Arch is not listed in the retrieved matrix; do not describe this workstation as vendor-certified on that evidence.
- No inference model was run, so neither GPU memory fit nor throughput is established.
- Do not replace documentation gaps with claims that CUDA-oriented repositories “will work on AMD.”
- Do not install or download models just to establish a baseline whose geometry can be measured without them.

### Inferences

#### Recommended minimum viable pipeline

1. Manually define canvas/interior-frame policy.
2. Obtain reviewed subject masks for representative references.
3. Calculate dimensions, boxes, widths/heights, centroids, margins, occupancy, edge contacts, and simple relation graphs.
4. Establish reference-family distributions and explicit unknowns.
5. Turn selected targets into a compact layout specification.
6. Use deterministic placement/scale/canvas operations where possible.
7. Otherwise use supported box or mask conditioning.
8. Re-segment/review outputs and compare geometry.
9. Report content correctness, geometry adherence, and aesthetic/project judgment separately.

This is simpler and more auditable than starting with a universal aesthetic predictor.

#### Advanced pipeline when multi-object control is demonstrably needed

\[
\text{reference annotations}
\rightarrow
\text{role/relation graph}
\rightarrow
\text{validated boxes/masks}
\rightarrow
\text{layout-conditioned generation}
\rightarrow
\text{semantic check + geometric check}
\rightarrow
\text{bounded correction}.
\]

Before rendering, validate:

- box bounds and permitted intentional bleed;
- aspect-sensitive sizes;
- minimum project-calibrated clearances;
- required object count;
- relation consistency;
- overlap and occlusion policy;
- frame/aperture containment.

Use amodal information only when available and clearly labeled. A model’s inferred hidden shape must not silently become ground-truth geometry.

Escalate from boxes to masks/edges only when box control fails the actual requirement; stronger control can produce stronger collateral shape or pose constraints.

#### Source validation and maintenance interpretation

Primary evidence reviewed comprises **13 core source families**: official measurement documentation, SAM 2, SAM 3, two empirical composition studies, GLIGEN, BoxDiff, ControlNet, LayoutGPT, ConsistCompose, OverLayBench, C-Bench/O-Bench, and AMD compatibility documentation. Supporting source pages include implementations, repositories, and license text.

All cited pages were accessed on **2026-10-31**. Repository pages are mutable snapshots; this research did not pin commits or establish latest commit activity. “README last lists an update in year X” is not equivalent to “project abandoned.”

Research spend: **5 Exa searches and 5 batch-fetch calls**. No Perplexity, Kagi Assistant, installs, model downloads, image uploads, or execution of downloaded code.

### Gaps

- The initially attempted Radeon-specific AMD documentation URL was not retrievable. The retrieved general matrix is explicitly versioned and not latest; a current workstation deployment decision needs a fresh Radeon-specific compatibility check.
- The BoxDiff license fetch timed out; its license remains unverified.
- C-Bench/O-Bench licensing, OverLayBench implementation licensing, and all relevant transitive checkpoint terms were not comprehensively audited.
- No reviewed repository was tested on CPU, ROCm, RX 7900 XTX, or CachyOS.
- No benchmark establishes an optimal method or target threshold for these particular stylized cards.
