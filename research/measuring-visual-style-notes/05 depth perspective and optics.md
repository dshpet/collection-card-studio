# Measuring and controlling depth, perspective, viewpoint, optics and blur

Research cutoff and verification date: **2026-10-31**. Scope: stylized object/card illustration, especially categories 1–4 in `materials/03_art_guide.md`. This note distinguishes directly observable image evidence, conditional geometric inference, and proposed workflow heuristics. No reference images were measured and no models were executed.

## 1. What can be observed, measured and expressed precisely?

### Takeaway

Treat perspective, depth ordering, atmospheric separation, object-relative viewpoint, projection type, framing and blur as separate axes. **Changing focal length at a fixed viewpoint does not change the scene’s perspective relationships:** it changes image magnification/FOV; the familiar “telephoto compression” usually comes from moving farther away to preserve framing.

### Cited Findings

#### Geometry versus camera specification

The pinhole model is

\[
s\,p=K[R|t]P,\qquad
u=f_xX_c/Z_c+c_x,\quad v=f_yY_c/Z_c+c_y.
\]

Here \(R,t\) describe scene-to-camera pose; \(f_x,f_y\) are focal lengths **in pixels**, not millimeters. Lens distortion is a separate model. Resizing requires corresponding changes to focal lengths and principal point. — [OpenCV calibration documentation](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

**Consequence derived from that model:** for unchanged camera center, orientation and scene, changing \(f_x,f_y\) produces image scaling about the principal point. Perspective size ratios are unchanged. A suitably cropped/rescaled image from the same viewpoint has the same geometric perspective, disregarding real-lens distortion, entrance-pupil changes, resolution and optical effects. Nikon independently describes focal length as controlling angle of view and magnification—not as a replacement for camera positioning. — [OpenCV model](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html); [Nikon, updated December 2025](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length)

For equally sized, front-facing objects at axial distances \(Z_f,Z_b\),

\[
h_b/h_f=Z_f/Z_b.
\]

If their separation is \(\Delta\), this is \(Z_f/(Z_f+\Delta)\), approaching one as camera distance increases. This is the distance-related origin of compression under matched subject framing; focal length cancels from the ratio. **Do not prescribe “increase focal length” alone when the correction needed is reduced near–far exaggeration.** — Analytic consequence of the [OpenCV projection equations](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

Perspective projection makes distant objects smaller and parallel spatial directions converge. Orthographic projection has no distance-related size diminution and preserves parallelism. Blender exposes both projection types, focal length/FOV, orthographic scale and lens shift. Lens shift is equivalent to an off-center crop from a larger view, rather than camera rotation. — [Blender camera manual, retrieved 2026-10-31](https://docs.blender.org/manual/en/latest/render/cameras.html)

#### Axis definitions and prompt-ready wording

The wording below is an **operational vocabulary proposed for this project**, not a claim that text-to-image systems obey numeric instructions exactly. Its geometric basis is the camera model and rendering controls above.

| Axis | Definition / observable evidence | Prompt-ready wording |
|---|---|---|
| Linear perspective | Convergence of image lines representing parallel scene directions; distinguish one-, two- and three-direction systems. | “Gentle two-point perspective; vertical edges remain parallel; weak convergence of receding edges.” |
| Horizon / eye level | Vanishing line of a specified horizontal plane. It can lie outside the image and is not necessarily a visible background boundary. | “Eye-level horizon above the object; show its top surface; no visible horizon line.” |
| Foreshortening | Shortening of projected dimensions because an axis points toward/away from the viewer, combined with perspective size change along depth. | “Strongly foreshortened handle pointing toward the viewer; preserve the handle’s physical length.” |
| Occlusion / depth order | Which surface hides which other surface; ordinal rather than metric. | “The front ribbon crosses in front of the box; the rear loop remains behind it.” |
| Atmospheric perspective | Depth-related attenuation and airlight, or its stylistic analogue: weaker distant contrast and convergence toward an atmosphere color. | “Distant scenery has lower contrast and shifts toward the pale warm background; foreground remains crisp.” |
| Azimuth | Camera direction around a defined object/world vertical axis. | “Three-quarter front-left view, showing the front and right side.” Define whose left/right. |
| Elevation | Angle of camera position above the chosen horizontal plane, distinct from camera pitch if not aimed at the object center. | “View from slightly above; a modest amount of the top surface is visible.” |
| Roll | Rotation around the viewing axis. | “Upright composition, zero camera roll; object verticals stay upright.” |
| Orthographic / weak perspective | Parallel or near-parallel recession and little near–far scaling. | “Orthographic-like product illustration; nearly parallel edges, minimal near–far size difference.” |
| Close-view perspective | Camera close relative to object depth; foreground parts become disproportionately large. | “Close viewpoint with an enlarged near end and visibly smaller far end.” |
| Framing / crop | Subject occupancy and margins, not a unique camera solution. | “Entire object visible, occupying 70% of image height, with clear margins on all sides.” |
| Depth of field | Range around a focus distance considered acceptably sharp; out-of-focus regions may blur. | “Whole object sharp; background softly defocused, with no blur on the object silhouette.” |
| Image blur | Loss/spread of image detail, irrespective of physical cause. | “A soft background only; no global Gaussian softness, motion streaks or smeared object edges.” |

“Three-quarter view,” “isometric” and “85 mm look” are insufficient measurements by themselves. True isometric rendering is a particular orthographic orientation; three-quarter is a broad appearance label; focal length in millimeters is incomplete without sensor dimensions and framing assumptions. — Operational interpretation of [Blender projection controls](https://docs.blender.org/manual/en/latest/render/cameras.html) and [Nikon focal-length definitions](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length)

#### Atmospheric perspective is not synonymous with blue tint or blur

Narasimhan and Nayar model direct transmission attenuation and additive airlight; their airlight term contains \(1-e^{-\beta d}\). Their paper explicitly discusses illumination assumptions and errors from atmospheric illumination occlusion. — [Vision and the Atmosphere, IJCV 2002, author PDF](https://cave.cs.columbia.edu/old/publications/pdfs/Narasimhan_IJCV02.pdf)

A useful simplified appearance model is

\[
I(x)=J(x)t(x)+A(1-t(x)),\qquad t=e^{-\beta d}.
\]

Here \(J\) is clear appearance and \(A\) the atmosphere color. Use this as a controllable rendering/appearance approximation, not as a depth-recovery guarantee. Unknown reflectance, illumination, atmosphere and artistic color choices prevent unique depth recovery; the atmosphere need not be blue. The paper’s full model contains additional assumptions and terms, so this compact equation should not be presented as its complete formulation. — Simplification informed by [Narasimhan–Nayar](https://cave.cs.columbia.edu/old/publications/pdfs/Narasimhan_IJCV02.pdf)

#### Depth of field versus blur

Blender separately controls focus object/distance and aperture F-stop; lower F-stop increases depth-of-field blur. Aperture blade count, rotation and ratio affect bokeh shape. Thus “softness,” “bokeh,” “shallow depth of field” and “blurred background” are not interchangeable specifications. — [Blender camera manual](https://docs.blender.org/manual/en/latest/render/cameras.html)

For a thin-lens approximation, an out-of-focus point at distance \(z\), with focus at \(s\), has a sensor-plane blur-disk diameter

\[
c=\frac{f^2|z-s|}{N\,z(s-f)},
\]

where \(f,s,z\) use the same length units and \(N\) is F-number. This is an **analytic thin-lens model**, not a way to uniquely infer those four quantities from painted blur. Compare \(c/W_{\rm sensor}\) to image-width-normalized blur. The model ignores aberrations, diffraction, non-thin lenses and nonphysical artistic blur. — Analytic optics interpretation consistent with the [focus/aperture controls documented by Blender](https://docs.blender.org/manual/en/latest/render/cameras.html)

Blur detection research uses gradient, Fourier-domain and learned local-filter evidence rather than equating a single sharpness number with optical defocus. — [Shi, Xu and Jia, CVPR 2014](https://openaccess.thecvf.com/content_cvpr_2014/html/Shi_Discriminative_Blur_Detection_2014_CVPR_paper.html)

### Inferences

#### Measurement conventions

The following are proposed reproducible measurements, **not standardized perceptual style metrics**.

- Retain original \(W,H\), aspect ratio, crop and any resampling history.
- For layout use \(u=x/W,\ v=y/H\).
- For geometric distances and angles, avoid independently normalizing the axes: use isotropic coordinates such as
  \[
  q=((x-c_x)/D,(y-c_y)/D),\quad D=\sqrt{W^2+H^2}.
  \]
  Independent \(x/W,y/H\) scaling changes angles when aspect ratio is not square.
- Report silhouette occupancy as bounding-box width/\(W\), height/\(H\), object area/\(WH\), centroid and margins.
- Report local blur width as pixels **and** width/\(D\), with the measurement resolution.
- Separate `observed`, `conditional inference`, `model prediction` and `unknown` fields.

#### Deterministic vanishing-point measurement

OpenCV documents deterministic Hough line voting,

\[
\rho=x\cos\theta+y\sin\theta,
\]

and probabilistic segment output with line-length/gap thresholds. This detects image lines; it does not by itself identify which lines are parallel in 3D or recover a camera. — [OpenCV Hough tutorial](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html)

Proposed procedure:

1. Select actual geometric edge segments manually or with edge detection plus Hough/line-segment detection.
2. Exclude lettering, painted stripes, cast shadows, reflections and decorative rays unless their scene geometry is known.
3. Assign plausible spatial direction families; do not force all lines into Manhattan-world axes.
4. Represent endpoints homogeneously and form \(l_i=p_i\times q_i\); a candidate VP is \(v=l_i\times l_j\).
5. Fit each family using robust angular residuals. To ensure repeatability, use exhaustive fitting or a fixed random seed if using RANSAC.
6. For segment midpoint \(m_i\), compare its tangent with
   \[
   r_i=(v_x-v_wm_{ix},\,v_y-v_wm_{iy}).
   \]
   The acute angle is meaningful even for VPs at infinity (\(v_w=0\)).
7. Form a candidate horizon \(h=v_1\times v_2\) **only if** those two spatial directions belong to the horizontal reference plane.
8. Report median angular residual, segment support, segment lengths and sensitivity to endpoint perturbation.

A distant VP is unstable in ordinary Cartesian coordinates. Prefer line-angle evidence and uncertainty over a huge point coordinate presented with false precision.

Under a pinhole model, zero skew, square pixels, known principal point \(c\), and two **known orthogonal** directions with finite VPs,

\[
f_{\rm px}^2=-(v_1-c)\cdot(v_2-c).
\]

This is a conditional calibration identity derived from the pinhole model. Negative \(f^2\), incompatible direction families or large residuals should trigger rejection/uncertainty, not a forced lens estimate. — Geometric derivation from [OpenCV’s camera model](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

#### Viewpoint and foreshortening proxies

- Record visible top/front/side regions, characteristic landmark positions, ellipse aspect ratios, edge slopes and near–far size ratios.
- Under orthographic/weak-perspective projection of a **known circular disk**, \(b/a\approx|\cos\theta|\), where \(\theta\) is the angle between its normal and the viewing direction.
- Under weak perspective, a straight axis inclined by \(\alpha\) away from the image plane has projected length proportional to \(L\cos\alpha\).
- These are conditional proxies, not general pose estimators: a drawn oval may not be a projected circle; stylized geometry may intentionally stretch one face.
- An object-relative camera azimuth and a compensating object rotation can produce the same isolated-object view. In a full scene they affect different relationships to background and lighting.

#### Occlusion measurements

- Annotate a directed graph \(A\rightarrow B\) meaning “A is in front of B at the specified shared boundary.”
- Record T-junction locations, boundary ownership, contact locations, interruptions of contours and uncertainty.
- **Visible segmentation masks of separate opaque objects do not supply an overlap area:** their interiors normally do not overlap. An overlap percentage requires an amodal/full-shape estimate, which is an inference.
- Do not infer metric separation from an ordering edge.
- Interlocking objects can have locally changing order; allow region-specific relations rather than forcing one global order for each object pair.
- An opaque 3D proxy render can produce exact z-buffer order and object-ID masks for the proxy, but not ground-truth geometry of the original illustration.

#### Deterministic blur measurements

- Measure several clean edges in the object interior, object silhouette and background separately.
- Sample intensity normal to each edge and estimate a 10–90% transition width after accounting for local contrast.
- For a Gaussian-blurred ideal step, \(w_{10-90}\approx2.563\sigma\). This is a mathematical calibration for that assumed edge/PSF, not a statement that the artwork used Gaussian blur.
- Record median and spread of \(w/D\), edge orientation and sampling resolution.
- Inspect directional asymmetry: motion smear can be directional, while simple defocus is more isotropic; aperture-shaped highlights add evidence but do not uniquely identify optics.
- Variance of the Laplacian or high-frequency energy can support controlled same-content comparisons. They are confounded by texture density, contrast, noise, sharpening, outlines, antialiasing and resizing.
- A smooth gradient background is **not measurable evidence of defocus** merely because it contains little high-frequency detail.
- Soft shading, bloom, motion blur, painterly simplification and optical defocus can coexist. Report apparent blur first, cause second.

These operational cautions are consistent with the distinction between multiple feature representations and blur scales in [Shi et al.](https://openaccess.thecvf.com/content_cvpr_2014/html/Shi_Discriminative_Blur_Detection_2014_CVPR_paper.html); the specific workflow and formulas above are analytical proposals.

### Gaps

- A single uncalibrated illustration usually cannot uniquely supply millimeter focal length, sensor size, camera distance in meters, metric depth or complete object shape.
- Pinhole projection is unchanged if all scene-to-camera positions are multiplied by the same positive scale. More generally, unknown shape, camera and depth can compensate for one another.
- Physical focal length needs sensor information; a fitted \(f_{\rm px}\) is not automatically an actual camera specification.
- A cropped image changes effective FOV and principal-point location. The original uncropped camera cannot generally be recovered uniquely.
- “Nearly orthographic” appearance can arise from orthographic rendering, a distant perspective camera, a shallow object, or deliberate drawing conventions.
- A visible floor–wall seam is not generally the horizon. A gradient background supplies no horizon calibration.
- Stylized illustrations may use locally inconsistent vanishing points, enlarged top faces, impossible ellipses or mixed projection. In that case the appropriate target is a documented local appearance, not a single physically valid camera.
- No universal validated mapping from these measured quantities to reliable text-only generation commands was established.

## 2. Which tools are defensible, current and practical?

### Takeaway

Start with manual geometric annotations and CPU-capable image measurements. Learned depth, normals and calibration can propose useful controls, but even “metric” models remain learned estimators—not measurements of an unknown stylized world.

### Cited Findings

Verification below means official paper/repository/license documentation was inspected on **2026-10-31**. GitHub `pushed_at` is a repository metadata timestamp, not proof of a recent substantive release or continuing support. None of these models was installed, downloaded or benchmarked.

| Tool | Evidence and appropriate role | License / current-state evidence | CPU / AMD caveat |
|---|---|---|---|
| **OpenCV** | Pinhole geometry, edge/line operations, deterministic measurements. [Calibration](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), [Hough](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html). | Official documentation resolved to 4.13.0. Library-license audit was outside this check. | Suitable CPU baseline; no model weights required for the proposed methods. |
| **Depth Anything V2** | Official 2024 paper/repo; relative-depth models and separate metric variants. Small has 24.8M parameters. [Repo/paper links](https://github.com/DepthAnything/Depth-Anything-V2). | README explicitly: **Small Apache-2.0; Base/Large/Giant CC-BY-NC-4.0**. Nonarchived; pushed 2026-03-24. | Official example explicitly falls back to CPU. AMD acceleration untested. Good lightweight candidate, not guaranteed art metrology. |
| **Depth Anything 3** | Released 2025-11-14. Main models predict depth and camera information from one or multiple views; dedicated monocular relative and metric series exist. [Official repo](https://github.com/ByteDance-Seed/Depth-Anything-3), [paper](https://arxiv.org/abs/2511.10647). | Code Apache-2.0. Model table: Small/Base, Metric-Large and Mono-Large Apache-2.0; Large/Giant/Nested and listed `-1.1` large variants CC-BY-NC-4.0. Current README deprecates original Large/Giant/Nested checkpoints in favor of bug-fixed `-1.1` versions. Repository push timestamp not verified. | README example uses CUDA; CPU/ROCm operation not verified. Main Small ≈80M, Base ≈120M parameters. Do not confuse estimated multiview camera pose with an isolated object’s semantic azimuth. |
| **MoGe, especially MoGe-2 / MoGe-3** | MoGe-2 predicts metric point/depth maps, optional normals and FOV. **MoGe-3 is current 2026 prior art**: July 2026 preprint, repo announces release 2026-08-18, using sparse 3D refinement for fine detail. [Repo](https://github.com/microsoft/MoGe), [MoGe-3 paper](https://arxiv.org/abs/2607.17967). | Code MIT, DINOv2 component Apache-2.0. Checked model-card metadata for `Ruicheng/moge-2-vits-normal` and `Ruicheng/moge-3-vitl`: MIT. Nonarchived; pushed 2026-10-31. | Current main installation pins a CUDA 13.0 index and MoGe-3 depends on FlexGEMM/Triton. CLI lists `cpu`, but this does **not** verify all versions work on CPU/AMD. Prefer evaluating a pinned MoGe-2 path before assuming latest-main portability. |
| **Metric3Dv2** | Metric depth and surface normals; paper 2024. Repo warns distorted point clouds can result from incorrect focal length and explicitly notes rare-object/view failures. [Official repo](https://github.com/YvanYin/Metric3D), [paper](https://arxiv.org/abs/2404.15506). | Code BSD-2-Clause. Independent checkpoint license coverage was not conclusively established; README invites commercial inquiries. Nonarchived; pushed 2025-03-13. | ONNX support documented. End-to-end CPU/AMD path not tested. Intrinsics/focal assumptions must be retained with results. |
| **GeoCalib** | ECCV 2024: estimates intrinsics and gravity using learned perspective fields plus geometric optimization; supports pinhole and radial models. **Current principal point is assumed at image center and not optimized.** [Repo](https://github.com/cvg/GeoCalib), [paper](https://arxiv.org/abs/2409.06704). | Code Apache-2.0; trained weights CC-BY-4.0. Nonarchived; pushed 2026-10-29. | Official example explicitly chooses CUDA or CPU. AMD untested. Gravity/pitch/roll are not semantic object azimuth or metric camera translation. |
| **Perspective Fields** | CVPR 2023: per-pixel up vectors and latitude; conditional recovery of roll, pitch, FOV and principal point. Separate centered and uncentered models are documented. [Official repo](https://github.com/jinlinyi/PerspectiveFields), [paper](https://arxiv.org/abs/2212.03239). | **Adobe Research License: noncommercial only; no redistribution.** Do not call this permissive commercial tooling. Nonarchived; pushed 2024-11-02. | README uses `.cuda()` and old CUDA/PyTorch instructions. CPU/AMD compatibility unverified. Useful research precedent, not the recommended commercial default. |
| **Marigold** | Original CVPR 2024 monocular-depth work; 2025 extension adds normals and intrinsic-image tasks. [Official repo](https://github.com/prs-eth/Marigold), [2025 paper](https://arxiv.org/abs/2505.09358). | **Code Apache-2.0; models RAIL++-M / `openrail++`, not Apache-2.0.** Nonarchived; pushed 2026-09-06. Verified depth/normals v1.1 model-card licenses. | Official depth runner contains CPU fallback and warns CPU will be slow. AMD/ROCm untested. Diffusion-based predictions add runtime/stochasticity considerations. |
| **MiDaS** | Established relative-depth and scale/shift-invariant training baseline; important for old ControlNet depth/normal conventions. [Official repo](https://github.com/isl-org/MiDaS), [paper full text](https://arxiv.org/html/1907.01341v3). | MIT; **repository archived**, last pushed 2024-08-23. Historical baseline rather than a default “currently maintained” choice. | CPU/OpenVINO options documented. Do not mistake relative inverse-depth output for meters. |
| **ControlNet** | ICCV 2023 spatial conditioning, including depth and normal maps. Original normal annotator is computed from MiDaS depth plus a background threshold—not necessarily a directly estimated physical normal map. [Official repo](https://github.com/lllyasviel/ControlNet), [paper](https://arxiv.org/abs/2302.05543). | Code Apache-2.0; base generator/checkpoint/detector licenses require separate checks. Nonarchived; pushed 2024-02-25. Original implementation is old prior art, not evidence of best current generator support. | Original examples are GPU-centric. Exact compatible checkpoint, preprocessing and AMD backend require a later implementation test. |
| **Shi–Xu–Jia blur features** | CVPR 2014 primary evidence for gradient/Fourier/local-filter blur discrimination. [Paper](https://openaccess.thecvf.com/content_cvpr_2014/html/Shi_Discriminative_Blur_Detection_2014_CVPR_paper.html). | Paper verified; no maintained implementation or implementation license verified here. | Useful method precedent, not an install recommendation. |

Two especially consequential implementation details:

1. **DA3 metric output is focal-dependent.** Its README specifies
   `metric_depth = focal * net_output / 300.`
   for `DA3METRIC-LARGE`, with focal length in pixels; the Nested output is described as already in meters. Do not treat all model variants and raw tensors as interchangeable. — [DA3 model-card notes](https://github.com/ByteDance-Seed/Depth-Anything-3#-model-cards)

2. **MoGe ONNX does not include the entire inference pipeline.** Official documentation says exported graphs contain the raw forward pass; focal/shift recovery and reprojection require separate postprocessing. — [MoGe ONNX documentation](https://github.com/microsoft/MoGe/blob/main/docs/onnx.md)

MiDaS explicitly addresses disparity/inverse-depth outputs with scale/shift-invariant alignment. Its least-squares alignment chooses \(s,t\) minimizing

\[
\sum_i(s d_i+t-d_i^*)^2.
\]

Its robust normalization uses the median and mean absolute deviation from the median. — [MiDaS paper, section V](https://arxiv.org/html/1907.01341v3)

MoGe-3’s authors explicitly identify remaining fine-geometry difficulties in preceding models: thin structures, small objects, and feature mixing across depth discontinuities. Its reported improvements do not establish solved performance for Playrix-style isolated artwork. — [MoGe-3 abstract and paper](https://arxiv.org/abs/2607.17967)

### Inferences

#### Comparison: geometry estimate versus ground truth

Use separate evaluation protocols:

- **Rendered or calibrated metric ground truth available:** retain physical units, camera convention and valid masks; evaluate absolute depth and normals without silently aligning away wrong scale.
- **Two relative predictions:** compare in the output’s documented representation. An affine transform of inverse depth is not an affine transform of depth.
- **Only two stylized RGB images:** learned maps are model-conditioned proxies. Describe map agreement, not geometric accuracy.

For compatible relative predictions \(p_i\) and reference proxy \(r_i\), over a valid mask \(M\),

\[
(a^*,b^*)=\arg\min_{a>0,b}\sum_{i\in M}w_i(ap_i+b-r_i)^2.
\]

Report the aligned residual **and** the fitted \(a,b\), mask, representation and excluded pixels. The positive-scale constraint preserves ordering. The invariant-loss motivation is established prior art; using it as a style-matching diagnostic is a proposed application. — [MiDaS](https://arxiv.org/html/1907.01341v3)

A robust normalization option is

\[
\tilde p_i=
\frac{p_i-\operatorname{median}(p)}
{\operatorname{mean}|p-\operatorname{median}(p)|+\epsilon}.
\]

Do not normalize each object independently if inter-object depth separation matters: that erases the relationship being measured.

Additional proposed metrics:

- Ordinal pair accuracy on explicitly annotated near/far pairs; allow uncertain/tied pairs.
- Depth-boundary agreement with a tolerance expressed as a fraction of \(D\).
- Silhouette and landmark error after a **specified limited** alignment.
- Median normal angular difference:
  \[
  \theta_i=\arccos(\mathrm{clip}(n_i\cdot n_i',-1,1)).
  \]
  Match coordinate frame, handedness and surface-normal sign conventions first.
- VP-family angular residual and horizon-line orientation/position.
- Blur-profile differences measured at matched region types and resolution.

Avoid unrestricted image warping: it can hide the viewpoint or shape error that the test is supposed to detect. Report both full-frame composition matching and object-aligned diagnostic matching if both are useful.

#### CPU / AMD deployment interpretation

- CPU documentation is strongest here for the deterministic stack, Depth Anything V2, GeoCalib and Marigold’s fallback.
- A README using `torch.device("cuda")` neither proves NVIDIA-only implementation nor proves ROCm support. Backend-specific kernels and dependencies must be checked separately.
- Do not recommend TensorRT/CUDA packages as if they were the workstation’s default path.
- A small permissively licensed model with documented CPU fallback is a safer initial experiment than a newly released sparse-kernel stack.
- Pin versions and check exact model licenses before commercial production. Repository license badges alone are insufficient.

### Gaps

- No runtime, memory, accuracy or ROCm compatibility measurements were performed.
- No exact semantic object-pose model was verified for arbitrary stylized objects. General scene calibration is not that tool.
- No reliable benchmark specifically covering these category 1–4 illustrations was established. General zero-shot or open-domain claims cannot be converted into a numeric accuracy claim for them.
- Current DA3 push/activity metadata was not verified; its live README and licensing table were verified.
- Metric3D checkpoint-specific licensing remains unresolved.
- Current original-ControlNet GPU/backend and checkpoint compatibility were not tested.
- The Oxford Single View Metrology PDF timed out; its publisher page redirected to a blocked identity flow. It was not used as decisive evidence.
- The Cambridge in Colour perspective demonstration was Cloudflare-blocked. The perspective conclusion above instead follows directly from the official pinhole model and is consistent with Nikon’s FOV/magnification explanation.

## 3. How should reference extraction become controllable matching and targeted correction?

### Takeaway

Use a small set of observable constraints as the contract, with optional depth/normal maps or 3D proxies to enforce it. Match the reference’s appearance—including intentional geometric inconsistency—rather than treating a guessed physical camera as truth.

### Cited Findings

ControlNet establishes depth/normal/edge-conditioned generation as prior art, while Blender provides explicit projection, camera and focus controls for building controlled proxy images. These are separate roles: an estimator proposes geometry, a renderer produces known proxy geometry, and a conditional generator interprets the control image. — [ControlNet](https://github.com/lllyasviel/ControlNet); [Blender cameras](https://docs.blender.org/manual/en/latest/render/cameras.html)

Depth and normals are not interchangeable: the original ControlNet documentation contrasts their geometric effects and notes that the normal preprocessor is depth-derived. MoGe and Metric3D provide newer direct normal/geometry prediction options, subject to their own model assumptions. — [ControlNet normal-map section](https://github.com/lllyasviel/ControlNet); [MoGe](https://github.com/microsoft/MoGe); [Metric3D](https://github.com/YvanYin/Metric3D)

### Inferences

#### Applicability to the project’s actual categories

The category definitions below come from the inspected local project guide, `materials/03_art_guide.md`, lines 5–29. Recommendations are proposed applications, not externally validated category-specific performance.

| Category | Available evidence | Recommended controls / measurements | Failure modes |
|---|---|---|---|
| **1: simple object floating against a simple background** | Silhouette, visible faces, internal overlaps, ellipses and landmarks. Usually no scene horizon or support plane. | Object-relative view, occupancy, local foreshortening, internal occlusion; manual annotation before learned depth. | Gradient/rays/patterns mistaken for geometry; fictitious ground/horizon; spherical or symmetric objects with indeterminate azimuth. |
| **2: simple object on a surface with simple vertical background** | Category 1 cues plus contact, support and possibly a surface/background seam. | Contact location, visible top amount, support orientation, silhouette and object-relative camera view. | Seam mistaken for horizon; shading/contact shadow mistaken for depth measurement; a textureless plane provides too few vanishing directions. |
| **3: object integrated into a realistic surface with simple background** | Surface texture/recession, stronger contact and depth cues. | Surface-edge/texture directions, contact, relative-depth map, localized normals. | Texture direction need not represent parallel 3D lines; decorative texture can bias calibration; surface relief confounded with material/shading. |
| **4: central object in realistic surroundings** | More potential parallel families, multiple occlusions and foreground/background layers. | VP families and horizon where justified; ordinal scene graph; optional learned depth/calibration; atmosphere and blur measured separately. | More evidence can also mean conflicting geometry, model distraction by background, and an inaccurate full-scene score hiding a wrong central object. |

Small isolated objects are especially unfavorable for automatic camera recovery: too few long straight lines, weak scale variation, unknown canonical shape and limited texture. A useful output can simply be “top surface visible; front-right view; nearly parallel recession; no calibratable horizon.”

#### Minimal stack

1. Original-resolution reference and candidate images.
2. Manual object masks, a few landmarks, meaningful edge segments and an occlusion list.
3. CPU deterministic geometry and edge-profile measurements.
4. A compact feature sheet with confidence and “not identifiable” entries.
5. Plain-language correction prompts, changed one axis at a time.

Optional first learned addition: **Depth Anything V2 Small**, if an approved installation/weights acquisition is later authorized. CPU fallback and Apache-2.0 Small weights are documented. This is a practical starting hypothesis, **not** a claim it outperforms all newer models. — [Official DAV2 README](https://github.com/DepthAnything/Depth-Anything-V2)

#### Advanced stack

- A simple 3D proxy with known object dimensions **in arbitrary scene units**.
- Explicit orthographic/perspective camera and a controlled framing target.
- RGB, object-ID/silhouette, axial-depth, normal and optional atmosphere/focus outputs.
- Compatible depth/normal/layout conditioning for a chosen generator.
- Optional GeoCalib, MoGe-2/3, DA3 or Marigold estimates to initialize hypotheses, not declare truth.
- A manual path for local geometric departures when one rigid 3D model cannot match the illustration.

Do not make multi-view reconstruction the default for a single reference. Multiple generated “views” are not independent observations of the original object.

#### Suggested feature record

```yaml
coordinate_convention:
  image: "x right, y down"
  layout_units: "fractions of width and height"
  geometric_length_unit: "image diagonal"
  object_front: "defined by named semantic feature"

observed:
  visible_faces: ["front", "right", "small top"]
  object_bbox_fraction: "measure from actual image"
  landmark_positions: "normalized coordinates with uncertainty"
  line_families: "segments plus angular residuals"
  occlusions: "front loop > box, at annotated boundary"
  blur_profiles: "object / silhouette / background, at fixed resolution"

conditional_inferences:
  projection_appearance: "weak perspective; orthographic not proven"
  camera_elevation: "qualitative unless calibrated"
  horizon: "unknown unless supported by horizontal directions"
  relative_depth_method: "model + version + representation"
  camera_estimate: "model assumptions and confidence"

unknown:
  sensor_size: true
  physical_focal_length: true
  camera_distance_m: true
  object_metric_dimensions: true
```

The example contains no measured reference values.

#### Matching sequence

1. **Separate appearance from physical hypotheses.** Annotate the silhouette, visible faces, key occlusions, framing and sharpness before estimating a camera.
2. **Fit projection/viewpoint appearance.** Compare orthographic and perspective hypotheses only if meaningful evidence exists.
3. **Fit occupancy without changing relative geometry unnecessarily.** Use crop/FOV/orthographic scale as appropriate; record which adjustment was made.
4. **Fit depth order and contacts.** They often matter more perceptually than a globally smooth depth map.
5. **Add atmosphere and focus separately.** Neither should repair a wrong silhouette or viewpoint.
6. **Generate with matched preprocessing.** Check depth polarity, normalization, clipping, masks, image size and normal coordinate conventions required by the exact checkpoint.
7. **Compare the same feature sheet.** A pleasing but differently framed or differently viewed object is not a match.
8. **Change one primary axis per diagnostic iteration.** Preserve seed/model/settings where the generator permits.

#### Targeted corrections and cross-axis effects

| Observed mismatch | Precise correction | Important coupling / trap |
|---|---|---|
| Too much top face visible | Lower the object-relative viewing elevation; preserve azimuth and occupancy. | Camera pitch and camera height are different if the camera is not aimed at the same target. Shape edits can imitate the same change. |
| Near end too large | Move the camera farther relative to object depth; increase focal length/reframe to retain occupancy. | Increasing focal length **alone** at fixed viewpoint does not repair the perspective ratio. |
| Object too small but shape/view match | Tighten framing/crop or change orthographic scale. | Do not move the perspective camera closer unless stronger perspective is acceptable. |
| Receding edges converge too strongly | Reduce perspective exaggeration using a farther camera with matched framing, or use an orthographic proxy if appropriate. | Orthographic projection removes all depth-dependent scaling, not merely “a little convergence.” |
| Object leans while scene should be upright | Correct roll, or distinguish actual object tilt from camera roll. | Rotating the whole image changes crop and does not independently fix skewed object geometry. |
| Wrong side visible | Correct relative azimuth. | Horizontal mirroring also reverses handed details, text, lighting and asymmetric design. |
| Ribbon crosses behind instead of in front | Edit the local occlusion/layout mask or regenerate that region with explicit boundary ownership. | A text-only “more depth” instruction is underspecified. |
| Background feels too close | Adjust relative background scale/separation, overlap, atmosphere or blur according to the diagnosed cue. | These are different mechanisms; none uniquely identifies true distance. |
| Object is globally soft | Remove global blur; preserve crisp silhouette and use background-only softening. | Sharpening may create halos rather than restore correct geometry. |
| Entire object should be sharp | Increase DOF / use all-in-focus rendering or a separate background blur pass. | Lower F-number does the opposite. |
| Background has too much contrast | Reduce background contrast or blend toward a chosen atmosphere color. | Do not automatically cool it or add defocus; those alter other style axes. |
| Depth control introduces lumps | Simplify or replace the estimated map, preserve contour/order, reduce overconstraint. | Model shading/texture errors can become imposed geometry. |

#### Prior art, novelty and negative findings

- Relative depth, invariant comparison, single-image calibration and spatially conditioned diffusion are established prior art, not a novel pipeline by themselves. — [MiDaS](https://arxiv.org/html/1907.01341v3), [GeoCalib](https://github.com/cvg/GeoCalib), [ControlNet](https://github.com/lllyasviel/ControlNet)
- A current account must include **DA3 (2025)** and **MoGe-3 (2026)** rather than implying DAV2/Metric3D alone describe the frontier. Their existence does not establish suitability for these assets. — [DA3](https://github.com/ByteDance-Seed/Depth-Anything-3), [MoGe-3](https://arxiv.org/abs/2607.17967)
- An opportunity worth testing is the project-specific combination of confidence-tagged geometric annotations, category-aware applicability, appearance matching and targeted corrections. No novelty claim or validated performance result is justified yet.
- A physically consistent reconstruction is not always a better match: a stylized reference can intentionally favor readability over projective consistency.
- No universal scalar “depth style” score, exact single-image focal-length recovery method, or validated all-category automatic pipeline was established by this research.
- Using the same estimator on reference and generated images improves procedural consistency, but can also produce correlated errors. It does not turn their agreement into ground truth.

### Gaps

- No particular generation engine, compatible current control checkpoint, or expected numeric prompt adherence was specified or benchmarked.
- The minimal and advanced stacks are recommendations for later testing, not completed implementations.
- No reference-specific measurements, accuracy scores or render matches were produced.
- **Research spend:** nine ordinary Kagi search queries, public official-document/repository/model-card reads and GitHub metadata checks. No Kagi Assistant, Perplexity, paid Deep Research, uploads, installs, downloaded weights, model runs or execution of repository code.
- **Source coverage:** 15 selected primary-source families: OpenCV calibration; OpenCV Hough; Blender; Nikon; Narasimhan–Nayar; Shi–Xu–Jia; MiDaS; DAV2; DA3; MoGe; Metric3D; GeoCalib; Perspective Fields; Marigold; ControlNet. Linked papers, licenses and model cards are companion evidence within those families.
