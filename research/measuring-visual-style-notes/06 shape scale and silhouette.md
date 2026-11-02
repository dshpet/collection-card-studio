# Shape, scale, silhouette readability, and apparent volume

Research cutoff and source access date: **2026-10-31**.

Scope: object masks, relative object size, contour geometry, proportions, recognizable silhouette structure, and the distinction between projected shape and shaded form. Overall composition, fine texture, and general attention models are outside this note except where they confound these measurements.

Evidence labels:

- **Established:** documented mathematical measurement, supported implementation, or published finding.
- **Proposed protocol:** practical synthesis for object-card production; not a published universal style metric.
- **Conditional:** interpretation requires a correct mask, semantic correspondence, viewpoint, class baseline, or controlled display.
- **Unidentified:** not uniquely recoverable from the supplied image.

## 1. What can be measured, and under which conditions?

### Takeaway

Measure projected geometry reproducibly, but do not confuse reproducibility with semantic correctness. **Matching the same object and transferring style between different objects require different comparisons:** a generated watering can may be compared with a reference watering can’s corresponding parts; a watering can should not be penalized for failing to share a reference apple’s silhouette.

### Cited findings

#### 1.1 Four distinct measurement classes

| Class | Meaning | Examples | Main limitation |
|---|---|---|---|
| **D — direct raster/metadata** | Computable without inferring object identity | Canvas dimensions; supplied object-ID layer; alpha coverage of an explicitly isolated object | An alpha layer may include shadow, glow, or multiple objects; transparency is not automatically semantic object membership |
| **M — mask-conditional deterministic** | Deterministic once a foreground mask and conventions are fixed | Occupied area, bounding box, compactness, solidity, principal axes, holes, skeleton | Correct arithmetic on a wrong mask remains a wrong object measurement |
| **L — learned/observer-conditioned** | Depends on a model, taxonomy, training distribution, or human test | Automatic masks, class predictions, semantic similarity, apparent-volume judgments | Scores are not universal or necessarily calibrated to human readability |
| **N — nonidentifiable without additional evidence** | Multiple underlying explanations fit the same image | True physical size, hidden geometry, unique depth/volume, degree of exaggeration without a class baseline | Requires additional views, known scale, geometry, annotations, or declared priors |

The deterministic measurements below correspond to established region, contour, and morphology operations documented by scikit-image and OpenCV. The separation of observability classes is a proposed reporting convention. [S1–S3]

**Important:** a learned segmenter followed by deterministic geometry is an **L→M pipeline**, not an entirely direct measurement.

#### 1.2 Define the measurement regions before calculating features

Use the same definitions for reference and candidate:

- **Card region \(C\):** the intended artwork viewport, excluding editor chrome, outer screenshot padding, and unrelated UI. Let dimensions be \(W\times H\) pixels.
- **Visible semantic object mask \(M\):** visible pixels belonging to the designated object. Include attached parts such as a spout, stem, or handle. Exclude cast/contact shadow, glow, particles, and unrelated decoration unless explicitly measuring their combined footprint.
- **Part masks \(M_i\):** named, corresponding semantic parts—for example body, handle, spout, lid. These require annotation or a validated part-recognition method.
- **Shadow mask \(S\):** separate annotation for cast/contact shadow when relevant.
- **Filled mask \(F\):** \(M\) with enclosed background holes filled. Retain both \(M\) and \(F\); a handle opening can be a critical recognition cue.
- **Convex hull \(K\):** hull of the declared mask geometry.
- **Boundary \(\partial M\):** record whether the measurement includes only outer boundaries or also hole boundaries.
- **Amodal mask \(M_a\):** hypothesized complete projection behind occlusion. This is an annotation/model hypothesis, not observed ground truth.

An object can have multiple visible components because of occlusion or because it is genuinely multipart. Do not automatically discard all but the largest connected component. Conversely, do not union unrelated objects simply because a background-removal model returns them together. Region labeling and contour hierarchy are explicitly supported by the documented libraries. [S1, S3]

For transparent objects, distinguish **semantic extent** from **opacity coverage**. A glass vessel can occupy a substantial semantic region while transmitting much of its background. The compositing relationship \(I=\alpha F+(1-\alpha)B\) does not itself supply a semantic object mask. [S8]

#### 1.3 Measurement conventions

For the table:

- \(A=|M|\), measured as foreground pixel area in px².
- \(B\) is the axis-aligned bounding box, with width \(w\) and height \(h\).
- \(A_K\) is hull area.
- \(P_{\mathrm{out}}\) is outer-boundary perimeter; \(P_{\mathrm{all}}\) includes hole boundaries.
- \(d_A=2\sqrt{A/\pi}\) is equivalent-circle diameter.
- Use isotropic pixels; preserve image aspect ratio.
- Raw lengths are in px, areas in px², and normalized ratios are dimensionless.
- State the raster resolution, alpha/mask threshold, connectivity, perimeter estimator, smoothing scale, and treatment of holes.
- Distinguish raster-count area from polygon-contour area. OpenCV explicitly warns that `contourArea` and the number of filled raster pixels can differ. [S3]

**Formula provenance:** the underlying geometry in the table is established; explicitly marked profiles, survival tests, and aggregation choices are proposed diagnostics. None is a validated universal style or readability score. [S1–S3]

#### 1.4 Rigorous feature table

| Feature | Formula / implementation | Units and normalization | Region and interpretation | Class / cautions |
|---|---|---|---|---|
| **Occupied card area** | \(f_A=A/(WH)\) | Fraction; multiply by 100 for percent | Semantic object \(M\) within \(C\) | **M**. Not physical size or visual importance. Shadow inclusion changes the result |
| **Soft coverage** | \(f_\alpha=\sum_{p\in C}\alpha(p)/(WH)\) | Fraction | Supplied isolated-object alpha | **D** for that channel, not necessarily semantic area; transparency/glow confound interpretation |
| **Width/height occupancy** | \(f_w=w/W,\ f_h=h/H\) | Fractions | Object bounding box | **M**. Thin protrusions can enlarge the box without adding much mass |
| **Equivalent diameter** | \(d_A=2\sqrt{A/\pi}\); report \(d_A/\sqrt{WH}\) | px or dimensionless | Same-area circular size proxy | **M**. Not a diameter of the actual object |
| **Relative size of two objects** | \(A_i/A_j\), or linear-equivalent \(\sqrt{A_i/A_j}\) | Dimensionless | Two separately annotated objects in the same declared frame | **M**. Perspective and occlusion prevent interpretation as real-world size |
| **Axis-aligned aspect** | \(r_B=w/h\) | Dimensionless | Whole object or named part | **M**. Changes with in-plane rotation and viewpoint |
| **Oriented aspect** | Long/short side of `minAreaRect` | Dimensionless | Declared object contour | **M**. Different from moment-based elongation |
| **Extent** | \(E=A/(wh)\) | Fraction | Foreground within its axis-aligned box | **M**. Depends on orientation, holes, and protrusions |
| **Centroid** | \(\bar x=A^{-1}\sum_M x,\ \bar y=A^{-1}\sum_M y\) | px; normalize as \((\bar x/W,\bar y/H)\) | Uniform mask, not brightness weighting | **M**. Report as a scale-edit preservation check; not an attention center |
| **Principal axes** | \(Q=A^{-1}\sum_M(p-\bar p)(p-\bar p)^T\); eigenvalues \(\lambda_1\geq\lambda_2\) and eigenvectors | Eigenvalues px²; orientation rad or degrees | Uniform object mask | **M**. Orientation is modulo \(180^\circ\); unstable for nearly equal eigenvalues |
| **Moment elongation** | \(r_Q=\sqrt{\lambda_1/\lambda_2}\); eccentricity \(e=\sqrt{1-\lambda_2/\lambda_1}\) | Dimensionless | Moment-equivalent ellipse | **M**. Not literal anatomical or mechanical axis lengths |
| **Equivalent ellipse axes** | \(a=4\sqrt{\lambda_1},\ b=4\sqrt{\lambda_2}\), under the continuous filled-ellipse convention | px; optionally divide by \(d_A\) | Second-moment shape approximation | **M**. Raster discretization matters; libraries provide equivalent-axis properties |
| **Perimeter** | Fixed estimator: polygon arc length or `perimeter_crofton(..., directions=4)` | px; report \(P/\sqrt A\) when scale normalization is needed | Specify outer-only versus all boundaries | **M**. Estimators and raster resolutions are not interchangeable |
| **Circularity** | \(C=4\pi A/P^2\) | Dimensionless | Declare which perimeter is used | **M**. Continuous circle gives 1; raster estimates can violate the ideal bound slightly. Low values can mean elongation, concavity, holes, or jaggedness—not one unique defect |
| **Inverse compactness** | \(P^2/(4\pi A)=1/C\) | Dimensionless | Same conventions as circularity | **M**. State which convention is called “compactness”; terminology varies |
| **Solidity** | \(A/A_K\) | Fraction | Object versus hull | **M**. Low for many legitimate handles, branches, and openings; high does not mean “good style” |
| **Perimeter convexity** | \(P_K/P_{\mathrm{out}}\) | Dimensionless | A single connected silhouette, consistently measured | **M**. Do not assume the usual bounded interpretation for widely separated components |
| **Convexity defects** | Distances from contour recesses to corresponding hull edges | px; divide depth by \(d_A\) | Outer contour | **M**. Useful for handle/body separations and notches; OpenCV defect depth uses fixed-point representation and requires conversion |
| **Hole area** | \((|F|-A)/|F|\) | Fraction | Enclosed background regions | **M**. Deliberately separates openings from outer contour concavity |
| **Topology** | Connected-component count \(n_c\), hole count \(n_h\), Euler characteristic \(\chi=n_c-n_h\) in 2D | Integer counts | Record connectivity | **M**. Tiny threshold changes can create or remove holes/connections |
| **Contour simplification profile** | \(N(\epsilon)\): number of vertices after Douglas–Peucker approximation, with \(\epsilon=q\sqrt A\) | Vertex count over dimensionless \(q\) values | Equal-scale contours | **M**, proposed profile. A single arbitrary epsilon is not a universal complexity measure |
| **Curvature profile** | \(\kappa=d\theta/ds\); normalize as \(\kappa\sqrt A\), after fixed-scale smoothing | px⁻¹ or dimensionless | Arc-length-resampled contour | **M**. Highly resolution/smoothing sensitive; corner rounding is not equivalent to high global circularity |
| **Total turning complexity** | \((2\pi)^{-1}\int|\kappa|\,ds\) | Dimensionless | Simple closed outer contour under declared smoothing | **M**, diagnostic. Smooth convex shapes share the same total absolute turning despite different roundness |
| **Skeleton length** | Sum graph-edge lengths; orthogonal steps 1, diagonal steps \(\sqrt2\), with documented graph construction | px; normalize by \(\sqrt A\) | `skeletonize(M)` or medial axis | **M**. Skeletons are algorithm-dependent; pixel graph junctions need cleanup |
| **Skeleton topology** | Endpoint count; clustered junction count; branch lengths | Counts and normalized px | Pruned skeleton graph | **M**. Boundary noise can create spurious branches; a 2D skeleton is not automatically an object’s semantic structure |
| **Local projected thickness** | Approximate width \(t(p)=2D(p)\) on medial axis, where \(D\) is distance to background | px; normalize by \(d_A\); report quantiles or part-specific values | Declared branch/part | **M**. A 2D width estimate, not physical depth |
| **Part proportion** | \(r_{ij}=l_i/l_j\) or \(A_i/A_j\) | Dimensionless | Corresponding named parts under compatible view | **M** if annotated; **L→M** if detected |
| **Exaggeration factor** | \(X_{ij}=r_{ij}/r^{\mathrm{baseline}}_{ij}\) | Dimensionless | Same class, part definition, and view baseline | **Conditional**. Without a baseline, “20% exaggerated” is not identifiable |
| **Mirror symmetry** | IoU between \(M\) and its reflection around a declared/aligned axis | Fraction | Suitable class/view only | **M**. Perspective, pose, and functional asymmetry can make symmetry inappropriate |
| **Same-object overlap** | \(\operatorname{IoU}(M_r,M_g)=|M_r\cap M_g|/|M_r\cup M_g|\) | Fraction | Registered corresponding object masks | **M**, comparison-conditional. Not a cross-object style score |
| **Boundary discrepancy** | Symmetric mean nearest-boundary distance; optionally Hausdorff maximum | px; normalize by \(d_A\) or card diagonal | Registered corresponding boundaries | **M**. Mean can hide a missing diagnostic part; maximum is outlier-sensitive |
| **Hu descriptors** | Seven normalized central-moment invariants; library implementation | Dimensionless vector | Binary mask or explicitly declared contour convention | **M**. Global summary, not unique identity or readability; raster invariance is approximate |
| **Thumbnail part survival** | Presence/width/area of a named opening or protrusion after actual downsampling | px, fraction, or categorical observation | Target-size rendered object and annotated parts | **M/observer-conditioned**, proposed diagnostic. Must name the feature and display pipeline |
| **Class recognition** | Accuracy/confusion matrix or learned class-score margin | Fraction or model-specific score | Fixed taxonomy, target size, controlled task | **L / human-conditioned**. Not interchangeable with silhouette similarity |
| **True volume / physical size** | No unique single-image formula | Would require physical units and additional evidence | Underlying 3D object | **N**. Projected area and perceived fullness do not identify true volume |

Supporting implementations and definitions: scikit-image region properties, moments, perimeter and topology; scikit-image skeletonization/medial axis; OpenCV contours, hulls, defects, polygon approximation and shape matching. [S1–S3]

#### 1.5 Normalization depends on the question

**Same semantic object, compatible view**

Maintain two comparisons:

1. **Card-space comparison:** retains occupied size, placement, orientation, and crop.
2. **Shape-normalized comparison:** removes only explicitly permitted translation, isotropic scale, and possibly in-plane rotation.

Do not use anisotropic scaling to “align” a proportion check: it can erase exactly the width/height error under investigation. Do not use unrestricted nonrigid alignment before deciding whether part proportions match.

Report the transformation used. A shape-normalized IoU can look excellent while the object is much too small on the actual card.

**Same class, different instance**

Use corresponding part ratios and a class/view-conditioned reference range. Whole-mask overlap is weaker evidence because legitimate instances can differ.

**Different semantic objects, shared style**

Do **not** minimize apple-to-watering-can IoU, Hu distance, skeleton distance, or contour correspondence.

Instead compare potentially transferable design tendencies:

- object occupancy under a declared card convention;
- coarse versus intricate contour structure at matched resolution;
- corner treatment and curvature at comparable feature scales;
- thickness of secondary parts relative to their own object body;
- degree of proportion exaggeration relative to each class’s baseline;
- whether diagnostic openings and protrusions survive at deployment size;
- apparent roundedness under a separate, controlled shaded-form assessment.

These are proposed style-analysis choices, not proof that every class should have identical descriptor values. The documented shape descriptors measure geometry; they do not supply a content-independent definition of style. [S1–S3]

A branchy plant and a round fruit may legitimately share a style while occupying very different locations in solidity–compactness space.

#### 1.6 Shape is not shaded form

A black silhouette preserves foreground extent and openings while removing internal surface cues. It therefore cannot distinguish, for example, a flat circular token from a similarly projected rounded object.

Hayward and colleagues’ experiments support an important role for outline shape in recognition across depth rotation, but also show that visual representations include additional information. Their study does **not** establish a universal silhouette-only recognition requirement for all objects. [S11]

The generalized bas-relief result demonstrates ambiguity in recovering 3D structure under its specified Lambertian, orthographic, unknown-lighting conditions: transformed geometry, albedo, and lighting can produce identical images, including cast and attached shadows. This is a rigorous warning against claiming unique physical volume from an ordinary illustration—not a claim that every perceptual cue is useless. [S12]

Therefore separate:

- **Projected shape:** mask geometry.
- **Apparent form/fullness:** observer- or model-conditioned interpretation of shading, overlap, perspective, and contour.
- **Actual geometry/volume:** unknown without additional evidence.

### Inferences

#### 1.7 Occlusion, background, and shadow safeguards

Proposed protocol:

- Report geometry as **visible-mask geometry** when the object is occluded.
- Do not silently infer an invisible spout, lower body, or handle.
- If an amodal annotation is needed, store it separately and mark its provenance.
- Flag contact with the card boundary: a clipped contour is not the complete silhouette. scikit-image documents that contours reaching image/mask boundaries can remain open. [S1]
- Keep contact shadow outside object occupancy. An attached dark patch may still fool segmentation and human interpretation; compare mask overlays against the original.
- Test real-background readability separately from a neutral silhouette plate. A clear black silhouette can conceal poor object/background separation in the delivered artwork.
- Separate genuine geometric openings from painted dark regions that merely look like holes.
- Compare mask thresholds and annotation alternatives when soft edges materially affect the answer.
- Preserve an unmodified mask. Closing holes or removing “small objects” may destroy the handle gap or stem being evaluated.

For uncertain boundaries, report a **sensitivity range**, not a fictitious statistical confidence interval: recompute selected features using plausible alternative masks or a declared small erosion/dilation. Such perturbations do not capture all segmentation uncertainty and can themselves change topology.

#### 1.8 No universal pass thresholds

There is no evidence here for universal rules such as “solidity above 0.9,” “circularity above 0.7,” or “80% occupied area” guaranteeing successful stylized card art.

Use class/view-matched accepted references and explicit production requirements. With a small reference set, report observed values/ranges rather than presenting estimated quantiles as stable population limits.

Useful disagreement patterns:

- Correct occupancy, wrong width/height → investigate proportions or view.
- Correct box, low occupied area → investigate holes, thinness, or sparse appendages.
- High solidity, failed recognition → diagnostic concavity/opening may have been erased.
- Good global overlap, failed recognition → a small but important part may be missing.
- Good silhouette, flat shaded result → investigate apparent form rather than contour.
- Good silhouette plate, poor delivered thumbnail → investigate background, shading, or display-size interaction.

### Gaps

- No reference images, target classes, or actual UI display sizes were supplied for this research lane; no asset-specific measurements or acceptance ranges were derived.
- No single scalar in the examined sources certifies recognizability or content-independent shape style.
- True hidden shape, physical scale, and unique volume remain unidentified from a single ordinary object-card image.

## 2. Which tools and prior art are suitable as of 2026-10-31?

### Takeaway

The minimal robust stack is **a reviewed mask plus CPU region geometry/morphology and actual-size recognition checks**. Learned segmentation and recognition are optional accelerators; their licenses, checkpoints, hardware assumptions, and domain accuracy require separate validation.

### Cited findings

#### 2.1 Tool comparison

| Tool / source status | Appropriate role | License and maintenance evidence | CPU / AMD caveats |
|---|---|---|---|
| **scikit-image — official library** | Labeling, region properties, moments, Crofton perimeter, contours, morphology, skeleton and medial axis | Stable documentation retrieved identifies **0.26.0**. Main project license is BSD-3-Clause with listed per-file exceptions. [S1, S2] | Suitable CPU baseline; these geometry operations do not require a learned model or CUDA. No local timing was measured |
| **OpenCV — official library** | Contour hierarchy, polygon approximation, hulls, convexity defects, rotated rectangles, Hu shape matching | **4.13.0** documentation and tagged Apache-2.0 license verified. [S3] | Core contour/geometry APIs can be used on CPU. Do not assume CUDA is needed or available |
| **SAM 2 / SAM 2.1 — Meta official** | Point/box-guided object masks; interactive mask refinement | Official repository documents SAM 2.1 checkpoints, Apache-2.0 code/checkpoints, and later predictor updates. [S4] | Examples and speed results are CUDA-oriented. Builder accepts a device; optional CUDA mask-postprocessing can be skipped. CPU operation is a possible engineering route, not a validated latency promise. AMD compatibility was not tested |
| **SAM 3 / 3.1 — Meta official, current development** | Concept/text or exemplar-conditioned instance segmentation; potentially useful for selecting a semantic object among several | Official repository documents SAM 3 and **SAM 3.1 release on 2026-03-27**. Custom **SAM License**, not Apache/MIT; checkpoints require access acceptance/authentication. [S5] | Official prerequisites specify CUDA-compatible GPU and CUDA ≥12.6. Do not recommend as a ready-to-run RX 7900 XTX/ROCm baseline |
| **BiRefNet — authors’ official implementation** | Foreground/dichotomous segmentation; high-resolution object extraction | Repository identifies the 2024 paper and later model/development updates. Code MIT; examined official `ZhengPeng7/BiRefNet` checkpoint card also declares MIT. [S6] | Published examples/benchmarks are GPU-oriented. ONNX routes exist, but export/operator/backend combinations must be checked. NVIDIA throughput figures do not predict AMD or CPU performance |
| **rembg — community integration project** | Convenient local foreground-mask extraction using selectable models, including BiRefNet | Wrapper MIT; **each model has its own license**. Current README documents CPU, CUDA, and ROCm routes. [S7] | CPU path is explicit. AMD route requires compatible ONNX Runtime ROCm setup; this was not validated on Arch/RX 7900 XTX. Select a model explicitly and avoid unintended first-use downloads |
| **CLIP — OpenAI official research implementation** | Secondary class-confusion/ranking check with a fixed candidate taxonomy | MIT repository; official model card explicitly calls for task-specific/in-domain evaluation and documents limitations. Treat as established research tooling, not a newly validated 2026 card-readability solution. [S8, S9] | CPU use is documented. Model loading can download weights. ROCm execution was not tested; do not equate a `cuda` device string in an example with proof of NVIDIA-only or AMD support |

**License distinction:** library license, model-checkpoint license, dataset terms, fonts/demo assets, and hosted-service terms are different layers. In particular:

- SAM 2’s official README explicitly distinguishes Apache-2.0 model/code licensing from demo font licenses. [S4]
- SAM 3 uses a custom license covering its defined materials. Do not infer SAM 2’s license applies to SAM 3. [S5]
- rembg’s MIT wrapper does not make every bundled/selectable model commercially permissive. Its current README explicitly warns about model-specific terms and identifies commercial restrictions for its documented BRIA default. [S7]
- The examined BiRefNet checkpoint’s MIT metadata should not be generalized to arbitrary forks, conversions, or unrelated checkpoints. [S6]

No software, dependencies, model weights, or remote inference services were installed or used during this research.

#### 2.2 Official implementation details worth preserving

**scikit-image**

`regionprops`/`regionprops_table` expose area, bounding box, extent, convex area, solidity, major/minor equivalent axes, eccentricity, orientation, Euler number, and related measurements. Coordinate conventions are row/column; documented orientation is measured relative to the row axis, not a casually assumed Cartesian horizontal. [S1]

`perimeter_crofton` is an established perimeter estimator, not a promise of exact resolution-independent contour length. Use the same method and resolution on both images. [S1]

`skeletonize` reduces the foreground while preserving connectivity according to its algorithm. The official example distinguishes thinning skeletons from medial axes and uses medial-axis distance information to estimate local width. It explicitly recommends `skeletonize` when fewer branches are desired. [S2]

**OpenCV**

`findContours` retrieval modes differ: `RETR_EXTERNAL` omits internal hole contours; `RETR_TREE` retains hierarchy. This choice matters for handles, rings, and other diagnostic openings. [S3]

`approxPolyDP` uses a declared maximum approximation distance. Count vertices only after normalizing that distance to object scale. [S3]

`matchShapes` uses Hu-based comparisons. It is not a style-recognition or human-readability API. [S3]

#### 2.3 Minimal deterministic measurement sketch

Illustrative, **not executed or benchmarked**. It assumes an already reviewed binary semantic mask, with no shadow.

```python
import numpy as np
from skimage.measure import regionprops, perimeter_crofton

def basic_shape_features(mask):
    M = np.asarray(mask, dtype=bool)
    H, W = M.shape
    A = int(M.sum())

    if A == 0:
        return {"status": "empty_mask"}

    # One semantic object ID, even if its visible mask is disconnected.
    region = regionprops(M.astype(np.uint8))[0]
    r0, c0, r1, c1 = region.bbox
    h, w = r1 - r0, c1 - c0

    # Total binary-mask perimeter; record treatment of holes.
    P = float(perimeter_crofton(M, directions=4))

    return {
        "area_px2": A,
        "occupied_fraction": A / (W * H),
        "width_fraction": w / W,
        "height_fraction": h / H,
        "aspect_wh": w / h,
        "extent": float(region.extent),
        "solidity": float(region.solidity),
        "eccentricity": float(region.eccentricity),
        "perimeter_crofton_px": P,
        "circularity": 4 * np.pi * A / P**2 if P else None,
    }
```

The underlying APIs are documented in [S1]. Padding, border contact, connectivity, mask cleaning, versions, and target-size rendering should be explicit in a production implementation.

#### 2.4 Literature and established prior art

1. **Region geometry and mathematical morphology are established prior art.** Current libraries already implement most required objective geometry. A bespoke learned “shape quality” metric is not necessary to begin measuring occupancy, proportions, contour complexity, and openings. [S1–S3]

2. **Skeletonization is established topology/structure extraction, not semantic understanding.** The official scikit-image example documents Zhang–Suen and Lee methods and a medial-axis route. The skeleton’s branches must not automatically be interpreted as object parts. [S2]

3. **Silhouette recognition has experimental support, but is conditional.** Hayward et al. (1999) found an important role for outline shape across depth rotation while also demonstrating contributions beyond outline. This supports silhouette testing as a diagnostic—not a universal requirement that all classes be recognized from outlines alone. [S11]

4. **A classifier’s success is not evidence that it used shape.** Geirhos et al. showed strong texture bias in the studied ImageNet-trained CNNs and increased shape bias through Stylized-ImageNet training. The paper does not establish that all contemporary models have the same bias, but it directly undermines the assumption “high classifier confidence proves readable silhouette.” [S10]

5. **Single-image form recovery has fundamental ambiguities.** Belhumeur, Kriegman, and Yuille’s generalized bas-relief result supplies a principled boundary on claims about recovered physical depth. [S12]

6. **Spatial conditioning of generation is established.** ControlNet demonstrated edge, depth, segmentation, and other conditioning for diffusion models. This supports using a contour/segmentation guide when available, rather than expecting prose alone to specify exact geometry. It does not guarantee preservation of every other visual axis. [S13]

7. **The current segmentation landscape is not limited to SAM 1/2.** Official SAM 3/3.1 sources establish concept-conditioned segmentation and a 2026 update, with materially different licensing and hardware prerequisites. Newer does not automatically mean more appropriate for a small CPU/AMD card-art measurement workflow. [S5]

### Inferences

#### 2.5 Recommended stacks

**Minimal stack**

1. Manually reviewed object mask or trusted isolated-object layer.
2. NumPy plus **one** primary geometry library, preferably scikit-image.
3. Occupancy, aspect, extent, solidity, perimeter convention, hole/topology report.
4. Named-part annotations for class-critical proportions.
5. Thumbnail sheets and controlled human recognition checks.
6. Optional OpenCV only for contour-specific operations that are genuinely needed.

**Advanced options, justified by workload**

- BiRefNet/rembg for batch initial masks, followed by review.
- SAM 2.1 for interactive ambiguous boundaries or instance selection.
- SAM 3 for concept-level instance selection where its licensing, access, and hardware fit.
- Skeleton branch/thickness profiles for thin or articulated objects.
- Curvature/simplification profiles for contour-language analysis.
- Fixed-taxonomy CLIP comparisons as a secondary confusion signal.
- Edge/segmentation-conditioned generation or localized editing where supported.

Do not add a segmentation service, large model, or depth-estimation pipeline merely to calculate a foreground area ratio.

### Gaps

- No local CPU, ROCm, ONNX, or model-inference benchmark was performed.
- Source inspection establishes documented capabilities and licensing statements, not successful execution on this workstation.
- Current repository branches are mutable. Production use should record exact package versions, checkpoint identity, and source revision.
- A focused current search did not establish a generally accepted, validated metric for **stylized object-card silhouette readability across unrelated classes**. A surfaced icon-design benchmark page was not text-accessible and was not used as evidence.
- SAGE full text was blocked; the Hayward claim is bounded to the accessible PubMed abstract. The bas-relief claim was checked against the authors’ institutional abstract.

## 3. How should reference features become prompts, checks, and targeted edits?

### Takeaway

Use a loop of **semantic interpretation → measured target → concrete instruction → generated-image measurement → localized correction**. Preserve a short list of protected axes, and treat wording and numerical prompt compliance as hypotheses to test rather than guaranteed controls.

### Cited findings

#### 3.1 Thumbnail recognition cannot be certified by one scalar

Neither classical shape descriptors nor learned semantic scores supply a universal readability certificate:

- A global descriptor can omit a small diagnostic feature. [S1, S3]
- Outline is important but not the only available recognition information. [S11]
- Learned recognition can exploit cues other than shape; the studied CNN texture-bias results give a concrete example. [S10]
- CLIP’s official model card documents taxonomy-dependent behavior and calls for task-specific testing. [S9]

Thus report a **diagnostic vector plus a recognition task**, not “readability = 0.84.”

#### 3.2 Proposed recognition-test protocol

This is a practical protocol, not a published universal threshold standard.

**Fix the deployment conditions**

- Use actual artwork display dimensions and production resampling.
- Distinguish artwork pixels from CSS/logical dimensions and device pixel ratio.
- Display at native size; do not judge a small thumbnail after enlarging it.
- If testing multiple sizes, choose actual product sizes. An exploratory 32/64/128-pixel ladder is only an example, not a standard.
- Keep background, contrast, exposure duration, and instructions documented.

**Use separate diagnostic renderings**

1. **Actual delivered image:** real card background and shadow.
2. **Semantic silhouette:** solid fill with genuine openings preserved.
3. **Hole-filled silhouette:** deliberately removes openings to test their contribution.
4. **Grayscale shaded image:** retains internal form cues without original color.
5. **Neutral-background cutout:** helps isolate object/background separation from geometry.

Do not interpret success in condition 2 as proof that condition 1 succeeds.

**Ask both identification and discrimination questions**

- Free response: “What object is this?”
- Fixed-choice response among relevant confusing classes, with an “unclear/other” option where appropriate.
- Same-instance matching only when same-instance fidelity is the requirement.
- Record wrong answers, not just correct-answer rate.
- Avoid giving viewers the intended noun before the free-response test.
- Randomize order and use separate viewers or counterbalancing to reduce learning from one condition to the next.

**Record**

- Correct/incorrect/unclear counts.
- Confusion matrix by class.
- Recognition rate by displayed size and condition.
- Response time if the task needs it.
- Observer familiarity and the number of observers/images.
- Uncertainty with its sampling assumptions; repeated trials from one observer are not automatically independent evidence.

A class may legitimately need an internal cue: a flat round object could be a coin, plate, button, or fruit slice. Record “requires internal cue under this taxonomy” rather than forcing an arbitrary protrusion to make its outline unique.

#### 3.3 Proposed reference-to-control worksheet

For each reference, record:

```text
Object class / instance:
Viewpoint and pose:
Card region:
Mask source and reviewed status:
Occlusion / border contact:
Object occupancy:
Width/height occupancy:
Aspect and principal-axis convention:
Named diagnostic parts and openings:
Part/body ratios:
Contour simplification / curvature scale:
Thumbnail recognition conditions and confusions:
Apparent-form observations:
Transferable style properties:
Class-specific properties NOT to transfer:
Protected axes for the next edit:
```

The distinction between transferable style and class-specific geometry is an analytical decision; the measurement libraries do not make it automatically. [S1–S3]

#### 3.4 Prompt terms and correction controls

The following are **proposed operational wording**, not experimentally established guarantees.

| Observed issue / target | Concrete prompt or edit instruction | Check afterward | Coupling / preservation warning |
|---|---|---|---|
| Object too small in card | “Increase the entire object uniformly; keep its proportions, angle, and center unchanged.” | Occupancy and width/height fractions | Changes margins and potentially shadow footprint; do not solve by thickening only the body |
| Correct outer span, body too thin | “Broaden the main body while preserving the handle opening and overall height.” | Named body width/height; total silhouette | May change apparent volume and part attachment |
| Secondary parts too fragile | “Thicken the handle and spout; preserve their lengths, attachment points, and open negative space.” | Part-local thickness and target-size survival | Can close holes or create tangencies |
| Diagnostic opening lost | “Restore a clearly open handle gap; retain the current body outline.” | Hole geometry, silhouette plate, thumbnail recognition | Dark shading is not equivalent to an actual visible opening |
| Contour has excessive tiny irregularities | “Simplify the outer contour into fewer broad curves; retain the stem, spout tip, and handle notch.” | Simplification profile at matched scale; named cues | Global smoothing can erase class identity |
| Corners too sharp for reference language | “Round the specified body corners with broad transitions; preserve the rectangular body proportion.” | Local curvature/corner regions | “More circular” would incorrectly change global shape |
| Too much blob-like simplification | “Reintroduce the distinct neck and shoulder break; keep broad, clean curves elsewhere.” | Named landmarks and confusions | Maximizing compactness/solidity is the wrong objective |
| Part proportions unlike reference | “Increase lid width relative to body width; do not enlarge the whole object.” | Corresponding part/body ratio | Requires same class and compatible view |
| Correct silhouette, looks flat | “Keep the outline unchanged; make the body read as rounded through broad form shading and a visible side/top plane consistent with the existing light.” | Silhouette invariance plus shaded-form review | This is a lighting/form edit, not silhouette repair |
| Poor actual-background separation | “Retain object geometry; separate the object boundary from the background locally.” | Actual thumbnail versus neutral silhouette | Changes color/value/lighting axis; hand off to that axis rather than deforming the object |
| Shadow mistaken for object mass | “Keep the object unchanged; separate and reduce the contact-shadow footprint.” | Object mask overlay and separate shadow mask | Grounding may weaken; shadow should not count toward object size |

**Avoid ungrounded generic commands:** “make it readable,” “make it premium,” “increase volume,” or “match the silhouette style” without naming the responsible feature.

#### 3.5 Converting an occupancy target to a geometric edit

For the same mask scaled uniformly inside a fixed card, without clipping:

\[
s=\sqrt{\frac{f_A^{\mathrm{target}}}{f_A^{\mathrm{current}}}}
\]

This follows from area scaling as \(s^2\). It is a geometric edit factor—not evidence that an image generator will obey a percentage.

Use:

- a deterministic transform for a pure size correction when the asset is isolated;
- a generator instruction such as “approximately \(s\) times the current linear size” only as a request;
- a mask/edge guide when supported and appropriate;
- a fresh measurement afterward.

If matching target height instead, \(s=f_h^{\mathrm{target}}/f_h^{\mathrm{current}}\). A height target and area target need not agree when proportions differ. Do not conceal that disagreement by stretching the image.

#### 3.6 Proposed targeted-edit loop

1. **Classify the comparison.** Same instance, same class, or unrelated objects sharing style.
2. **Review masks.** Especially openings, stems, occlusions, border contact, and shadow.
3. **Identify one primary error.** For example: undersized object, collapsed handle opening, narrow body, excessive fine contour complexity, or flat shaded form.
4. **Name protected properties.** Palette, material, lighting direction, viewpoint, center, object count, background, and unaffected parts.
5. **Choose the lowest-coupling intervention.**
   - Uniform raster transform for scale.
   - Local vector/mesh deformation for a known proportion change.
   - Localized regeneration for an incorrect part.
   - Shading edit for flatness with a correct outline.
6. **Check the intended feature.**
7. **Check regressions on protected axes.**
8. **Repeat the actual-size recognition test when identity-bearing geometry changed.**

The possibility of using edges/segmentation/depth as generation controls is established by ControlNet; the particular workflow and preservation checklist here are proposed production practice. [S13]

**Editing-mask caution:** an inpainting region must include enough surrounding space for the desired new contour. A tightly cropped edit region may prevent a handle from widening. Editing tools differ in whether they preserve pixels outside the mask exactly; do not promise exact preservation without checking the specific tool.

#### 3.7 Apparent-volume diagnostic sequence

Use this sequence to avoid editing the wrong axis:

1. **Silhouette already wrong?** Repair projected geometry first.
2. **Silhouette plausible, shaded image flat?** Inspect broad form cues, visible planes, overlaps, and lighting consistency.
3. **Only the shadow makes it seem “large”?** Separate grounding from body geometry.
4. **Changing the light changes perceived fullness strongly?** Record a lighting–form interaction, not recovered physical depth.
5. **Depth/normal model proposes a rounded shape?** Treat it as a learned interpretation. It does not resolve single-image nonidentifiability.
6. **Need actual physical volume?** Request geometry, calibrated views, or other appropriate evidence.

The distinction between outline information and additional recognition cues is supported by [S11]; the physical identifiability limitation is supported under explicit imaging assumptions by [S12].

### Inferences

#### 3.8 Practical acceptance structure

Do not collapse everything into a weighted “style score.” Use separate decisions:

- **Measurement valid?** Correct card region, object identity, mask, and conventions.
- **Scale suitable?** Occupancy and object span appropriate to the reference/task.
- **Shape suitable?** Class-conditioned proportions and contour treatment.
- **Identity retained?** Diagnostic features and deployment-size recognition.
- **Apparent form suitable?** Rounded/planar/fullness interpretation under the intended rendering.
- **Protected axes preserved?** No unintended shift of palette, lighting, material, background, or viewpoint.

An overall pass can be a task decision based on these findings, but it is not a discovered universal perceptual law.

#### 3.9 Source register

All links below were accessed **2026-10-31**. Thirteen primary source groups are used; licenses and implementation files are grouped with their parent projects.

- **[S1] scikit-image measurement documentation, 0.26.0 — official.** Region geometry, moments, topology, contours, perimeter conventions.  
  https://scikit-image.org/docs/stable/api/skimage.measure.html  
  Tagged license, including per-file exceptions:  
  https://github.com/scikit-image/scikit-image/blob/v0.26.0/LICENSE.txt  
  **Confidence:** high for documented definitions; no local execution validation.

- **[S2] scikit-image skeletonization example — official.** Thinning methods, medial axis, distance-based width estimation.  
  https://scikit-image.org/docs/stable/auto_examples/edges/plot_skeleton.html  
  **Confidence:** high.

- **[S3] OpenCV Structural Analysis and Shape Descriptors, 4.13.0 — official.** Contours, hierarchy, hulls, defects, simplification, moments and matching.  
  https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html  
  Tagged license:  
  https://github.com/opencv/opencv/blob/4.13.0/LICENSE  
  **Confidence:** high.

- **[S4] SAM 2 — Meta official repository and implementation.** SAM 2.1, licensing, CUDA-oriented examples, optional extension, device parameter.  
  https://github.com/facebookresearch/sam2  
  https://github.com/facebookresearch/sam2/blob/main/INSTALL.md  
  https://github.com/facebookresearch/sam2/blob/main/sam2/build_sam.py  
  **Confidence:** high for repository statements; CPU/AMD performance untested.

- **[S5] SAM 3 / 3.1 — Meta official repository and license.** Concept-conditioned segmentation; 2026-03-27 SAM 3.1 update; CUDA requirements; gated checkpoint access.  
  https://github.com/facebookresearch/sam3  
  https://github.com/facebookresearch/sam3/blob/main/LICENSE  
  **Confidence:** high; custom-license summary is not legal advice.

- **[S6] BiRefNet — authors’ official repository, license and checkpoint card.** High-resolution dichotomous segmentation; model variants; ONNX availability; MIT declarations.  
  https://github.com/ZhengPeng7/BiRefNet  
  https://github.com/ZhengPeng7/BiRefNet/blob/main/LICENSE  
  https://huggingface.co/ZhengPeng7/BiRefNet/blob/main/README.md  
  **Confidence:** high for source declarations; no transfer of vendor GPU benchmarks to this workstation.

- **[S7] rembg — project-maintained community integration documentation.** CPU/CUDA/ROCm routes, selectable models, model-specific licensing, first-use downloads.  
  https://github.com/danielgatis/rembg  
  **Confidence:** high for README statements; environment compatibility untested.

- **[S8] CLIP — OpenAI official repository and MIT license.** Image/text representations, fixed-candidate ranking, CPU usage, automatic model downloading.  
  https://github.com/openai/CLIP  
  https://github.com/openai/CLIP/blob/main/LICENSE  
  **Confidence:** high.

- **[S9] CLIP model card — OpenAI official.** Task-specific evaluation, taxonomy sensitivity, research scope and limitations.  
  https://github.com/openai/CLIP/blob/main/model-card.md  
  **Confidence:** high; model-card recommendations are distinguished from license permissions.

- **[S10] Geirhos et al., “ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness,” ICLR 2019.** Primary paper.  
  https://arxiv.org/abs/1811.12231  
  **Confidence:** high within the studied models/tasks; not generalized to all 2026 recognizers.

- **[S11] Hayward et al., “Recognizing silhouettes and shaded images across depth rotation,” Perception, 1999.** Primary-study abstract indexed by PubMed.  
  https://pubmed.ncbi.nlm.nih.gov/10694968/  
  DOI: https://doi.org/10.1068/p2971  
  **Confidence:** high for abstract-level findings; publisher full text unavailable during this research.

- **[S12] Belhumeur, Kriegman and Yuille, “The Bas-Relief Ambiguity,” IJCV, 1999.** Authors’ institutional publication page and abstract.  
  https://vision.ucsd.edu/publications/1999/bas-relief-ambiguity  
  **Confidence:** high, conditional on the paper’s stated imaging assumptions.

- **[S13] Zhang et al., “Adding Conditional Control to Text-to-Image Diffusion Models,” 2023.** Primary ControlNet paper.  
  https://arxiv.org/abs/2302.05543  
  **Confidence:** high for demonstrated conditioning categories; not a guarantee of exact or axis-isolated editing.

### Gaps

- Prompt phrases and editing procedures above are operational proposals, not validated universal controls.
- No universal class-independent silhouette, compactness, or recognition threshold was found or invented.
- Apparent-volume judgments remain conditional; unique physical volume is not identified.
- No generated/reference image pair was evaluated, and no user image was uploaded.
- **Research spend:** 12 Kagi search queries, one Context7 library resolution and one documentation query, plus public primary-source retrievals. No Perplexity, Kagi Assistant, paid synthesis, installs, model downloads, or inference.
