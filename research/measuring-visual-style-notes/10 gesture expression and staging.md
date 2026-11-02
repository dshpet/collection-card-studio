# Gesture, expression, and staging: conditional measurement and targeted control

## 1. What can be measured objectively, and what must remain conditional or interpretive?

### Takeaway

Pose and staging are best represented as **annotated geometry plus explicitly qualified interpretations**, not a single “gesture energy,” “emotion,” or “style” score. Once landmarks, masks, identities, and coordinate conventions are fixed, many comparisons are deterministic; extracting those annotations from stylized art—and reconstructing hidden anatomy, depth, intention, or emotion—is not.

**Scope and date:** public-source research accessed **2026-10-31**. The requested Playrix asset sets exclude gold character cards. Consequently, human gesture and facial expression will often be **not applicable** to the current single-object cards. Object orientation, articulated prop configuration, component placement, separation, contact, and occlusion may still apply. Character-specific features are retained for future character assets, not asserted to exist in the supplied material. This applicability statement comes from the assignment; no project images were analyzed or uploaded.

### Cited Findings

- **Line of action is a useful artistic abstraction, not a directly observable anatomical structure.** Guay, Cani, and Ronfard describe it as a conceptual tool used by cartoonists and illustrators, and introduce a mathematical posing interface that aligns a 3D character to a user-specified line from a particular viewpoint. This supports using an annotated principal gesture curve while preserving its viewpoint dependence and author choice. — [The Line of Action, SIGGRAPH Asia 2013](https://team.inria.fr/imagine/the-line-of-action-an-intuitive-interface-for-expressive-character-posing/)

- **Pose estimators return model predictions, not ground-truth anatomy.** MediaPipe Pose Landmarker predicts 33 body landmarks, normalized image coordinates, estimated world coordinates, and optional segmentation masks. Its stated application domain includes on-device fitness applications and a human shape model; this does not establish performance on arbitrary cartoon bodies. — [Official Pose Landmarker guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)

- **Coordinate systems must not be conflated.** MediaPipe documents normalized image `x,y`, a hip-relative depth value with roughly the scale of normalized `x`, and separate world coordinates expressed in meters with the hip midpoint as origin. A model returning meter-valued predictions does not establish physical scale from an unconstrained cartoon drawing. — [Official Python output documentation](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/python)

- **Face geometry, animation coefficients, action units, and emotion labels are different representations.** MediaPipe Face Landmarker estimates 478 landmarks and 52 blendshape coefficients; OpenFace provides landmarks, head pose, action-unit recognition, and gaze estimation. Neither representation should silently be converted into a definitive emotional state. — [MediaPipe Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker); [OpenFace official repository](https://github.com/TadasBaltrusaitis/OpenFace)

- **Facial movement is not a reliable universal diagnostic of emotion.** Barrett and colleagues review substantial variation across people, contexts, and cultures. Their conclusions support describing depicted movements—smile, brow lowering, eyelid opening—rather than asserting an internal emotional state from the face alone. Their review concerns human facial behavior; extending an emotion classifier to stylized fictional faces requires additional validation, not less. — [Emotional Expressions Reconsidered, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/)

- **Stylized and nonhuman anatomy require explicit ontology choices.** Human-Art includes human keypoints and self-contact annotations across natural and artificial imagery. AP-10K defines a separate animal skeleton and even documents cross-species landmark naming conventions that do not always match the biological joint names literally. A shared label such as “knee” therefore does not guarantee identical anatomical semantics. — [Human-Art official repository](https://github.com/IDEA-Research/HumanArt); [AP-10K official repository](https://github.com/AlexTheBad/AP-10K)

- **Standard keypoint metrics encode assumptions.** COCO’s evaluator uses object area, per-keypoint tolerances, and annotation visibility flags. Its OKS computation includes:
  ```python
  vars = (sigmas * 2)**2
  e = (dx**2 + dy**2) / vars / (gt['area']+np.spacing(1)) / 2
  if k1 > 0:
      e = e[vg > 0]
  ```
  This is a defined benchmark comparison, not proof that the same sigmas or area normalization are appropriate for chibi proportions or small game cards. — [Official COCO evaluator source](https://raw.githubusercontent.com/cocodataset/cocoapi/master/PythonAPI/pycocotools/cocoeval.py)

### Inferences

The following is a **proposed project schema and measurement contract**, not a claim that an existing toolkit implements all of it. Its design is informed by the landmark, contact, and evaluation representations above.

#### 1.1 Separate three epistemic layers

| Layer | Examples | Appropriate claim |
|---|---|---|
| Deterministic given accepted annotations | Point distances, projected joint angles, component positions, mask clearance, annotated curve descriptors | “The annotated wrist is 0.08 torso units higher.” |
| Learned or human-estimated annotations | Landmark placement, object segmentation, instance association, approximate head orientation | “The detector proposes this elbow location; review needed.” |
| Nonidentifiable or interpretive properties | Hidden 3D pose, actual physical contact, intention, emotion, gesture “energy” | “This is one plausible reading/hypothesis.” |

“Objective” should mean **repeatable under a declared annotation protocol**, not independent of all choices or uncertainty.

A numeric score derived from a learned landmark inherits annotation errors. It is not made objective merely by applying trigonometry afterward.

#### 1.2 Required record structure

Each asset record should contain:

```text
asset_id
applicability_by_feature
image_size, content_frame, crop_and_resize_transform
coordinate_convention, mirrored_input
ontology_name_and_version
instances:
  instance_id, category, topology
  visible_mask, optional_amodal_mask
  mask_source, mask_review_status
  landmarks:
    semantic_name
    position
    status
    annotation_source
    detector_score_if_available
    review_status
    uncertainty
  pose_curve_if_applicable
  facial_features_if_applicable
relations:
  subject_id, predicate, object_id
  relation_scope, evidence, certainty
reference_group_id
measurement_version
```

Recommended applicability values:

- `applicable`
- `not_applicable`
- `unknown`
- `not_measurable_at_resolution`

Recommended landmark statuses:

- `visible`
- `occluded_but_annotated`
- `outside_frame`
- `ambiguous`
- `not_present_in_topology`
- `unlabeled`

Do not encode all these states as zero confidence or coordinates `(0,0)`. A three-fingered stylized hand does not have a “missing” fourth finger in the same sense as a failed human-hand detection.

Keep **annotation provenance**, **visibility**, **detector score**, and **review status** separate. A detector can confidently infer an invisible joint incorrectly.

#### 1.3 Coordinate conventions and normalization

Keep at least two coordinate frames:

1. **Canvas/layout frame:** necessary for staging and placement.
2. **Subject-relative frame:** useful for comparing articulated pose independently of placement.

For pixel coordinates \(p=(x,y)\) in an image of width \(W\), height \(H\):

\[
u=x/W,\qquad v=y/H.
\]

Declare origin and direction; a practical convention is top-left origin, positive \(x\) rightward, positive \(y\) downward.

Use these normalized coordinates for layout serialization. **Do not compute Euclidean angles directly in independently width/height-normalized coordinates when aspect ratios differ**: that applies anisotropic scaling.

For geometric calculations, use pixel coordinates or an isotropically normalized frame:

\[
\bar p=(p-c)/s,
\]

where \(c\) is a declared anchor and \(s>0\) is a scalar length.

Possible scales:

- subject bounding-box diagonal: broadly applicable, but changes with pose and crop;
- torso length: useful when reliably defined, but foreshortening-sensitive;
- head width: useful for facial or hand-to-face comparisons;
- fixed reference-rig dimensions: useful when a controlled rig exists.

Store the denominator and its provenance. Report layout and pose measurements separately rather than allowing normalization to conceal a placement change.

Canonicalization rules:

- Translation removal is appropriate for local pose matching, but not layout matching.
- Rotation removal is appropriate only when global lean is intentionally irrelevant.
- Reflection is **not** automatically acceptable: it swaps handedness, eyelines, contact sides, and compositional direction.
- Nonuniform scaling or aggressive Procrustes alignment can erase the exaggeration or asymmetry being evaluated.
- Preserve the original and any transformed measurements.
- If anchors are uncertain or absent, return a qualified alternative normalization or abstain.

“Left” and “right” should mean anatomical/character side unless explicitly marked “image-left” and “image-right.” MediaPipe’s face documentation explicitly warns that its left/right blendshapes refer to the subject, and mirrored inputs invert the interpretation. — [Official face guide](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker)

#### 1.4 Gesture and body-pose features

| Feature | Proposed representation / units | Interpretation limits |
|---|---|---|
| Line of action | Annotated spline/polyline, sampled at normalized arc length | Multiple legitimate curves may describe the same figure |
| Principal lean | Curve chord or torso-axis angle, degrees from declared vertical | Preserve whether lean was canonicalized away |
| Curve bending | Signed turning-angle sequence; total absolute turning in radians; arc/chord ratio | Not a universal “energy” measure |
| Joint flexion | Projected 2D angle, degrees | Not the true 3D joint angle |
| Limb orientation | Directed segment angle, degrees | Segment direction must be specified |
| Reach / spread | Wrist, ankle, or prop-anchor offsets divided by declared scale | Depends on body proportions and perspective |
| Shoulder–hip relationship | Separate shoulder and hip angles; relative angular difference | Does not uniquely recover 3D twist |
| Compression | Head–pelvis or shoulder–pelvis projected distance divided by an agreed scale | Confounds crouch, foreshortening, and proportion |
| Asymmetry | Left/right angle and endpoint differences | Intentional asymmetry is not inherently an error |
| Exaggeration | Difference or ratio relative to a matched character/rig reference | No universal neutral human baseline for cartoons |
| Support appearance | Annotated foot/paw anchors and projected body/support relationship | Visual plausibility cue, not physical stability proof |

Projected joint angle at \(b\), with endpoints \(a,c\):

\[
\theta_b=
\cos^{-1}
\left(
\frac{(a-b)\cdot(c-b)}
{\|a-b\|\|c-b\|}
\right).
\]

Return undefined when either segment is too short relative to annotation uncertainty.

Segment orientation:

\[
\phi_{ab}=\operatorname{atan2}(y_b-y_a,x_b-x_a).
\]

Compare angles using circular differences:

\[
\Delta\phi=\operatorname{atan2}
\big(\sin(\phi-\phi^\*),\cos(\phi-\phi^\*)\big).
\]

For a curve of length \(L\) and nonzero endpoint chord \(C\), \(L/C\) is a dimensionless bending descriptor. It is unstable when \(C\) approaches zero; mark such cases rather than allowing arbitrary extreme values.

Do not force a single principal curve onto a multi-limbed creature or an action with independently important torso, arm, and tail gestures. Store secondary gesture curves where they improve the correction task. This is consistent with the line-of-action paper’s extension to secondary lines. — [Guay et al.](https://team.inria.fr/imagine/the-line-of-action-an-intuitive-interface-for-expressive-character-posing/)

#### 1.5 Three-dimensional pose and ambiguity

Under perspective projection:

\[
p_i=\pi(K(RX_i+t)).
\]

Without known camera parameters, scale, anatomy, and depth constraints, different \(X_i,R,t,K\) can produce similar image landmarks. The equation explains why fitting the 2D landmarks does not uniquely recover the original 3D pose.

For stylized illustrations, additional ambiguity can come from intentionally nonrigid anatomy, inconsistent perspective, curved limbs, and shape changes introduced for readability.

Recommended representation:

- **Measured/annotated:** image-space points, visible contours, overlap boundaries.
- **Inferred:** joint-depth ordering, head orientation, plausible rig pose.
- **Known:** authored camera/rig parameters, if available from the actual asset pipeline.
- **Unknown:** hidden joint configuration unsupported by visible evidence.

Use local ordinal statements such as “near hand in front of torso at this crossing,” rather than inventing metric depth.

When two interpretations remain plausible, preserve hypotheses:

```text
hypothesis A: elbow projects forward
hypothesis B: shoulder rotates backward
shared evidence: same approximate 2D wrist and elbow locations
```

A model’s “world coordinates” are useful predictions in its declared representation, not independent evidence that a cartoon has that physical body or scale. — [MediaPipe output documentation](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/python)

#### 1.6 Facial features, expression, and eyelines

Prefer visible mechanisms:

- inner/outer brow position and slope;
- eyelid aperture and visible iris coverage;
- pupil or iris center within the visible eye;
- mouth width, opening height, and corner positions;
- smile/scowl asymmetry;
- cheek or muzzle deformation when the topology supports it;
- head roll, and qualified yaw/pitch estimates.

Suggested units:

- eye aperture / eye width;
- mouth opening / mouth width;
- brow-to-eye distance / eye width;
- mouth-corner vertical displacement / mouth width;
- left/right differences in the same units;
- orientation in degrees with declared axes.

Near-zero denominators require abstention. Side views and deliberately unequal cartoon eyes require side-specific measurements.

Separate:

1. **Landmark geometry:** positions and ratios.
2. **Blendshape coefficients:** native model-specific animation parameters.
3. **Action units:** coded facial movements with coder/tool-specific scales.
4. **Expression labels:** “smiling,” “brows raised,” “eyes narrowed.”
5. **Interpretive affect:** “reads as worried/playful to these reviewers.”

Blendshape coefficient `0.7` is not automatically AU intensity `0.7`, a 70% emotion probability, or a cross-character measurement.

For action units, record the AU vocabulary, intensity/presence convention, model, and scale. Do not compare native outputs from unrelated tools without validating the mapping.

For eyelines, distinguish:

- visible pupil displacement;
- inferred image-plane gaze direction;
- inferred 3D gaze ray;
- assigned target object;
- intended narrative attention.

A practical target feature is angular error between a reviewed image-plane eyeline and the vector to a specified object anchor. This remains a **depiction cue**, not measured real gaze. If pupils are dots without enough positional evidence, report “eyeline ambiguous.”

Emotion and “energy” may be retained as **reference-relative reviewer labels**, with agreement rates and examples. They must not become numeric truth claims. — [Barrett et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/)

#### 1.7 Spatial relations, separation, occlusion, and contact

Represent staging as an instance graph:

```text
character_A --holding--> cup
character_A.left_hand --image_contact--> cup.handle
cup --in_front_of_at_boundary--> torso
prop_B --image_right_of--> cup
character_A --looks_toward_depiction--> prop_B
```

Each relation needs:

- instance IDs;
- relevant parts or boundary region;
- whether it is image-space, inferred physical, or authored 3D;
- annotation source;
- certainty and alternatives.

Useful deterministic features, once masks and anchors are accepted:

- normalized center displacement;
- bounding-box size and aspect ratio;
- instance area fraction;
- minimum visible contour distance;
- projected overlap;
- containment;
- aligned edges or support anchors;
- negative-space width at a designated gap;
- annotated occlusion order;
- contact-anchor separation.

For visible masks \(M_i,M_j\), normalized clearance can be defined as:

\[
g_{ij}=
\frac{
\min_{a\in\partial M_i,b\in\partial M_j}\|a-b\|
}{s}.
\]

Also record whether masks intersect. A value of zero alone cannot distinguish touching, overlap, shared segmentation boundaries, or uncertain annotation.

**Important:** visible instance masks are normally disjoint in the occluded region because a pixel shows only the front surface. Their intersection is not a direct measurement of how much of the back object is occluded. Bounding-box overlap is also not occlusion.

A visible-fraction measure,

\[
f_{\mathrm{vis}}=|M_{\mathrm{visible}}|/|M_{\mathrm{amodal}}|,
\]

requires an accepted amodal mask. If the hidden extent is inferred, label the result inferred; do not manufacture the denominator.

Contact must distinguish:

- image-space proximity;
- depicted contact supported by contour/occlusion cues;
- semantically intended interaction, such as holding;
- verified physical contact from a known 3D scene.

A hand near a cup does not prove grasping, and a correct grasp cannot be evaluated from wrist position alone.

Use **local** front/back relations where appropriate. Interlocking or articulated objects can require different order at different image regions; a single global depth rank is not universally sufficient.

#### 1.8 Object-only cards

For the current scope, a useful minimal record may be:

```text
body_pose: not_applicable
facial_expression: not_applicable
object_staging:
  main_axis
  tilt
  component_anchors
  articulation
  part_separation
  contact_and_overlap_relations
  visible_side
```

Examples of relevant language:

- “Handle tilts farther image-left.”
- “Lid opens wider while the base remains fixed.”
- “Ribbon ends spread farther apart.”
- “Fruit pieces form a tighter cluster.”
- “Move the rear prop behind the main object without changing its scale.”
- “Keep a visible gap between the handle and the adjacent component.”

For approximately symmetric objects, a principal axis can be estimated from a reviewed mask’s second moments. Its orientation is axial—equivalent modulo \(180^\circ\)—unless an asymmetric part defines direction. For nearly circular shapes, orientation is poorly determined and should be marked ambiguous.

Do not call object tilt “gesture energy” unless that is an explicitly defined artistic reading with reference examples.

### Gaps

- No actual Playrix images were analyzed, so applicability, landmark detectability, and reference tolerances remain untested.
- There is no validated universal numeric conversion from line curvature, limb spread, or expression geometry to “energy,” personality, or emotional truth.
- A single drawing generally does not establish hidden 3D pose, physical scale, actual gaze, or true physical contact.
- The proposed schema and equations require implementation and annotation validation; they are not experimental results.

## 2. Which tools and research are suitable, including cartoons, licensing, maintenance, and CPU/AMD constraints?

### Takeaway

For the present object-card scope, **reviewed manual annotations plus deterministic geometry** are the strongest minimal baseline. Human landmark detection becomes an optional acceleration layer for suitable future assets; cartoon-domain checkpoints, nonhuman skeletons, and advanced generation controls require explicit domain, licensing, and runtime checks.

### Cited Findings

#### 2.1 Candidate tool and evidence matrix

| Tool / source | Useful capability | Stylization suitability | License and deployment qualification |
|---|---|---|---|
| MediaPipe Pose Landmarker | 33 body landmarks; image/world coordinates; optional segmentation | Human-body model; no demonstrated guarantee for exaggerated/nonhuman figures in the reviewed guide | Repository code Apache-2.0; exact model-bundle terms must be checked separately. CPU is a candidate baseline; no Arch/AMD performance test performed. |
| MediaPipe Face Landmarker | 478 landmarks, 52 blendshapes, facial transform | Potential starting point for human-like faces; not validated here for dot eyes, muzzles, extreme proportions, or profile caricatures | Repository code Apache-2.0; do not infer model-weight licensing from documentation/sample-code footers. |
| MMPose / RTMPose family | Multiple human, face, hand, whole-body, animal, and 3D tasks; configurable datasets | Appropriate advanced toolbox when the ontology/checkpoint matches the target | Toolbox Apache-2.0; checkpoint, detector, dataset, and dependency terms remain separate. |
| DWPose | Whole-body human pose; ONNX deployment paths; ControlNet preprocessing | Useful candidate for human-like stylized figures, not arbitrary creatures | Code Apache-2.0; reviewed weight-hosting page has an empty README, leaving a weight-license verification gap. |
| OpenFace | Landmarks, head pose, AUs, gaze | Human facial-behavior research tool; no cartoon guarantee established | Restrictive academic/nonprofit noncommercial research terms; commercial licensing route exists. Not a default for commercial game work. |
| AP-10K models through compatible toolboxes | Animal landmark ontology and benchmark | Better anatomical starting point for matching quadrupeds than forcing a human skeleton | Dataset states CC-BY-4.0; that does not independently verify every checkpoint’s terms. |
| Human-Art-trained checkpoints | Pose estimation across natural/artificial human imagery | Directly relevant evidence of domain adaptation for artwork humans | Dataset repository requests noncommercial authorization. Do not treat code licensing as clearance for dataset or checkpoint use. |

Sources: [MediaPipe pose](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker), [face](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker), [repository license](https://raw.githubusercontent.com/google-ai-edge/mediapipe/master/LICENSE), [MMPose](https://github.com/open-mmlab/mmpose), [DWPose](https://github.com/IDEA-Research/DWPose), [DWPose code license](https://raw.githubusercontent.com/IDEA-Research/DWPose/onnx/LICENSE), [DWPose weight host](https://huggingface.co/yzd-v/DWPose), [OpenFace copyright](https://raw.githubusercontent.com/TadasBaltrusaitis/OpenFace/master/Copyright.txt), [AP-10K](https://github.com/AlexTheBad/AP-10K), [Human-Art](https://github.com/IDEA-Research/HumanArt).

#### 2.2 Evidence that domain matching matters

Human-Art reports, under **ground-truth bounding boxes on its validation set**, ViTPose-S AP of `0.507` for the COCO-trained model versus `0.738` for the Human-Art/COCO model. This is useful evidence that artwork-domain training can materially affect results.

It is **not** a measured accuracy for Playrix cards, an end-to-end detector result, or proof of correctness on nonhuman characters. The repository’s description also includes an apparent typo in its breakdown of 2D/3D artificial scenarios; do not repeat that breakdown uncritically. — [Human-Art results and annotations](https://github.com/IDEA-Research/HumanArt)

DWPose reports separate whole-body benchmark results for body, feet, face, and hands. This supports evaluating the required parts separately rather than assuming “whole-body success” guarantees usable fingers or facial landmarks. Its published results are on human benchmarks, not the present asset set. — [DWPose official results](https://github.com/IDEA-Research/DWPose)

AP-10K states that heavily occluded images were removed during cleaning, and that some occluded keypoints were inferred by annotators while others were left unlabeled. This is a reminder that benchmark coverage and annotation certainty need examination before applying a model to heavily overlapped stylized scenes. — [AP-10K annotation and cleaning description](https://github.com/AlexTheBad/AP-10K)

#### 2.3 Segmentation and identity association are separate requirements

MediaPipe Pose Landmarker offers optional segmentation output, but a task-specific body mask does not establish a general solution for props, object parts, interacting figures, or persistent identity association. — [Official pose guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)

MMPose includes multi-person and whole-body capabilities, but this does not remove the need to associate each landmark set with the correct annotated instance and prop. — [MMPose supported tasks](https://github.com/open-mmlab/mmpose)

ControlPose explicitly identifies incorrect body-part assignment and multi-person ambiguity as shortcomings of holistic pose-map conditioning. Its design introduces global, individual, and hierarchical keypoint encoders with structured mask attention. This is current evidence that instance association remains consequential even in generation systems. — [ControlPose, CVPR Findings 2026](https://openaccess.thecvf.com/content/CVPR2026F/html/Du_ControlPose_High-Fidelity_Pose-Controlled_Image_Generation_with_Multi-Faceted_Pose_Disentanglement_CVPRF_2026_paper.html)

#### 2.4 Current control literature, through the access date

- **ControlNet, 2023:** established spatial conditioning using pose, edges, segmentation, depth, and related maps. Its official repository demonstrates composing multiple controls. These are useful control mechanisms, not independent guarantees of anatomy, identity preservation, or unchanged styling. — [Official implementation](https://github.com/lllyasviel/ControlNet)

- **InstanceDiffusion, CVPR 2024:** supports per-instance text paired with points, scribbles, boxes, and instance masks. The reviewed repository identifies itself as the first author’s reimplementation, warns of possible differences from paper results, and links community integrations. Its README explicitly describes a tradeoff between stronger location adherence and image quality. — [Official-author repository](https://github.com/frank-xwang/InstanceDiffusion)

- **ControlPose, CVPR Findings 2026:** directly relevant to multi-person pose association and fine-grained coordinate conditioning. The paper page reports Human-Art AP `61.66`; this is an author-reported benchmark result, not a local validation or assurance of commercial deployment readiness. No code/weight license was established in this review. — [Primary paper page](https://openaccess.thecvf.com/content/CVPR2026F/html/Du_ControlPose_High-Fidelity_Pose-Controlled_Image_Generation_with_Multi-Faceted_Pose_Disentanglement_CVPRF_2026_paper.html)

- **OccluRank, August 2026 preprint:** augments boxes with ordinal front/back rank. Its synthetic dataset derives occlusion order from known scene geometry rather than inferred image depth. This is particularly relevant to staging, while also underscoring that boxes alone do not specify occlusion order. Its evaluation includes MLLM judgments; those judgments are not definitive geometric truth. — [Primary preprint](https://arxiv.org/abs/2608.20932)

- **OccluRank availability limitation:** the reviewed repository says training/inference code is available, but checkpoints, datasets, and benchmark releases are still forthcoming. Its README also says the preprint link will be added later, despite the existing arXiv record: documentation and release state are not fully synchronized. Do not recommend it as ready-to-run pretrained tooling. — [Official repository](https://github.com/Wenyang-hong/OccluRank)

#### 2.5 Code licenses and model-weight licenses differ

The ControlNet repository code is Apache-2.0, while the reviewed `control_v11p_sd15_openpose` checkpoint card declares **CreativeML OpenRAIL-M** and documents its SD1.5 compatibility. This is a concrete example of why repository-license shorthand is insufficient. — [Code license](https://raw.githubusercontent.com/lllyasviel/ControlNet/main/LICENSE); [Checkpoint model card](https://huggingface.co/lllyasviel/control_v11p_sd15_openpose)

InstanceDiffusion states that most code is Apache-licensed but that CLIP, BLIP, Stable Diffusion, and GLIGEN retain separate terms. Its linked community ports should not automatically be treated as upstream-supported releases or assumed to inherit identical licensing. — [License and integration notes](https://github.com/frank-xwang/InstanceDiffusion)

OpenFace’s copyright begins:

> “ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY”

Its README separately links commercial licensing and notes training-dataset obligations. “Public source code” is therefore not synonymous with unrestricted commercial use. — [Copyright](https://raw.githubusercontent.com/TadasBaltrusaitis/OpenFace/master/Copyright.txt); [Repository](https://github.com/TadasBaltrusaitis/OpenFace)

#### 2.6 CPU, AMD, and maintenance evidence

MediaPipe’s Python `BaseOptions` documents CPU and GPU delegates; the reviewed API page limits GPU support to Ubuntu platforms. It does not establish supported GPU execution on this CachyOS/Arch workstation or a particular AMD card. — [Official BaseOptions API](https://developers.google.com/edge/api/mediapipe/python/mp/tasks/BaseOptions)

DWPose documents ONNX and OpenCV-ONNX paths, including a route avoiding the full MMCV dependency. This makes CPU-first exported inference a plausible evaluation route, not a measured speed or compatibility claim. — [DWPose deployment notes](https://github.com/IDEA-Research/DWPose)

InstanceDiffusion’s examples use CUDA-specific runtime paths. OccluRank’s reference environment specifies CUDA 12.8. Those examples are **not evidence of ROCm support**. — [InstanceDiffusion](https://github.com/frank-xwang/InstanceDiffusion); [OccluRank](https://github.com/Wenyang-hong/OccluRank)

The accessed MediaPipe guides were updated on 2026-10-09. The reviewed MMPose README highlights a January 2024 release, while DWPose’s displayed news is principally from 2023. These are documentation observations, not reliable last-maintained dates or proof that either repository is abandoned. — [MediaPipe pose guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker); [MMPose](https://github.com/open-mmlab/mmpose); [DWPose](https://github.com/IDEA-Research/DWPose)

### Inferences

#### 2.7 Recommended minimal stack

For a small asset set:

1. Review applicability manually.
2. Annotate only required points, curves, parts, and relations in an existing local image/vector editor.
3. Preserve original images and annotation transforms.
4. Calculate geometric features using existing project tooling.
5. Review overlays at native delivery size.
6. Perform deterministic layer movement, rig posing, or local redraw where available.

This avoids paying the complexity and uncertainty cost of a human detector when the assets are object-only or too stylized for its ontology.

No new annotation service, model download, fine-tuning pipeline, or dependency installation is justified solely by this research.

#### 2.8 Advanced stack, conditional on demonstrated need

For many human-like characters:

- shortlist MediaPipe or an appropriately licensed MMPose/RTMPose checkpoint;
- compare against reviewed manual annotations before adopting it;
- use a matching detector or manually supplied crops;
- add face/hand detection only if the correction task needs it;
- test exported CPU inference before assuming GPU infrastructure is necessary.

For animals or invented creatures:

- select or define a topology first;
- consider animal checkpoints only when landmark meanings genuinely correspond;
- retain custom anchors for tails, wings, muzzles, and articulated props;
- do not “repair” intentionally stylized anatomy toward human proportions.

For repeated 3D staging:

- prefer the actual rig/camera or a deliberately authored proxy scene;
- render pose, depth, instance masks, and contact markers from that known scene;
- treat the proxy as an authored control specification, not a reconstruction of unknowable original geometry.

#### 2.9 Deployment acceptance checklist

Before using any learned component commercially:

- pin repository version and checkpoint revision/hash;
- record code, weight, detector, base-model, and dataset terms separately;
- check inference dependencies and model-format compatibility;
- verify image orientation, color conversion, crop, padding, and resize inversion;
- measure CPU latency and memory on representative inputs;
- test actual ROCm execution if GPU use is proposed;
- check current issue/release history rather than relying on README age;
- verify that a community port supports the needed features;
- prevent silent automatic weight downloads during evaluation.

“Available in ONNX” means an interchange format exists, not that every runtime/provider or preprocessing implementation produces equivalent predictions.

### Gaps

- No software, dependencies, weights, or model inference were installed or run.
- No CPU throughput, AMD/ROCm compatibility, or Arch packaging claims were experimentally verified.
- Exact weight terms remain unresolved for several candidates, including the reviewed DWPose hosting page and exact MediaPipe task bundles.
- MediaPipe model-card PDF endpoints were reachable, but their full contents were not extracted in this session; they were not used to claim model-weight permissions.
- MagicCartoon was discovered as potentially relevant cartoon-specific 3D work, but OpenReview presented a browser challenge and ACM returned 403. Its methods, limitations, and availability were therefore not validated sufficiently for recommendation.
- The late-2026 search was bounded, not an exhaustive systematic review. No universal cartoon/nonhuman detector or collateral-free editing guarantee was established.

## 3. How should words become reference matching and targeted corrections without collateral changes?

### Takeaway

Translate artistic language into **named parts, measurable relations, matched references, and a small edit contract**. Use prompts to state intent, structured geometry to specify placement, and independent post-edit checks to detect both target improvement and unintended changes.

### Cited Findings

- The line-of-action interface demonstrates that a compact, user-authored gesture curve can guide expressive posing, while remaining viewpoint-dependent. — [Guay et al.](https://team.inria.fr/imagine/the-line-of-action-an-intuitive-interface-for-expressive-character-posing/)

- ControlNet provides pose and other spatial controls, but its own examples discuss modifications to image details and differences between depth- and normal-based preservation. Structural conditioning is not equivalent to freezing all other image properties. — [Official ControlNet repository](https://github.com/lllyasviel/ControlNet)

- The reviewed pose checkpoint supports hand/face inputs and is paired with a particular base-model family. A generic skeleton image is therefore not a universal interchange representation across all generators and checkpoints. — [Official checkpoint card](https://huggingface.co/lllyasviel/control_v11p_sd15_openpose)

- InstanceDiffusion supports local text/location conditions and iterative repositioning, but documents adherence–quality and computation tradeoffs. Its examples also use different box formats in different interfaces: normalized `xyxy` in the shown Diffusers example versus `xywh` for the CLI data path. Coordinate adapters must be explicit. — [Repository examples and parameter notes](https://github.com/frank-xwang/InstanceDiffusion)

- ControlPose’s 2026 design addresses instance-awareness and fine-grained coordinates, indicating that “correct-looking skeleton map supplied” does not by itself eliminate limb-assignment errors. — [Primary paper](https://openaccess.thecvf.com/content/CVPR2026F/html/Du_ControlPose_High-Fidelity_Pose-Controlled_Image_Generation_with_Multi-Faceted_Pose_Disentanglement_CVPRF_2026_paper.html)

- OccluRank separates object locations from ordinal occlusion order. This supports explicitly specifying front/back relations rather than expecting overlapping boxes to communicate them. Its proposed global rank remains a particular model representation, not a universal account of all interlocking scenes. — [Primary preprint](https://arxiv.org/abs/2608.20932); [Implementation format](https://github.com/Wenyang-hong/OccluRank)

### Inferences

The workflow below is a **recommended project protocol**, not a benchmarked guarantee.

#### 3.1 Build a vocabulary-to-feature dictionary

| Artistic wording | Operational description to agree with the user | Reference and correction target |
|---|---|---|
| “More dynamic” | More torso lean? Wider reach? Stronger gesture-curve bending? Greater asymmetry? | Choose named features; do not increase all of them |
| “Less stiff” | Reduce bilateral symmetry; alter shoulder/hip relationship; soften a selected limb curve | Match an approved example with the same action |
| “More exaggerated” | Increase a particular bend, reach, expression deformation, or shape ratio | Define baseline and magnitude for that character |
| “More alert” | Eyelid aperture, brow position, head orientation, body lean | Label as intended reading, not detected mental state |
| “Friendlier” | Selected mouth corners, eyelid shape, brow configuration | Compare approved expressions; preserve character design |
| “Look at the object” | Named pupil/eye/head cues directed toward a named target | Check target association and visible cues |
| “Separate the subjects” | Increase a particular silhouette gap; reduce an accidental tangent | Measure that gap at delivery resolution |
| “Hold the cup convincingly” | Hand/handle anchors, finger/muzzle topology, local front/back order | Review contact region, not wrist alone |
| “Cleaner staging” | Fewer tangencies, clearer overlaps, wider selected negative spaces | Use explicit relation graph and mask overlays |
| “Livelier object” | Specify tilt, articulation, component spread, or asymmetry | No human skeleton or emotion classifier needed |

The dictionary should be negotiated through examples. There is no reason to assume that “dynamic” means the same geometric change across an upright bottle, an opening chest, and a running character.

#### 3.2 Match references conditionally

Use reference strata:

- compatible topology;
- same or comparable action;
- comparable viewpoint and foreshortening;
- similar crop and intended display size;
- same interaction type;
- comparable expression topology;
- appropriate asset category.

Do not compare the pose of a seated character to the unconditional average of a board containing standing, running, and crouching figures.

Store:

- geometric pose matching;
- staging matching;
- character proportion/design matching;
- expression matching;
- reviewer interpretation.

These should remain separable. A shorter arm may be a design feature, not a pose error.

For feature \(k\), a reference median and robust spread can summarize a compatible group:

\[
m_k=\operatorname{median}(f_k),\qquad
r_k=\operatorname{median}|f_k-m_k|.
\]

A normalized residual may be:

\[
z_k=\frac{f_k-m_k}{1.4826r_k+\epsilon_k},
\]

where \(\epsilon_k\) is a declared floor based on annotation precision or art-direction tolerance. This is a descriptive reference-relative score—not a universal standard or necessarily a Gaussian z-score.

For tiny or multimodal reference sets, show individual examples or separate clusters rather than manufacturing a narrow “correct range.”

#### 3.3 Compare keypoints without hiding failures

For a fixed relevant joint set \(J\):

\[
E_{\mathrm{kp}}=
\frac{\sum_{j\in J'}w_j\|\bar p_j-\bar p_j^\*\|}
{\sum_{j\in J'}w_j},
\]

where \(J'\) is the subset with admissible correspondences.

Always report alongside it:

- required-joint coverage \(|J'|/|J|\);
- missing or unmatched instances;
- left/right swap count;
- visible versus inferred joint counts;
- part-specific errors;
- worst important-joint error.

Otherwise a detector can appear better by failing on difficult joints and scoring only the easy ones.

Use fixed task importance weights first. Detector confidence should not be treated as a calibrated error probability without checking it on this domain. A confidence-weighted average alone can suppress exactly the wrist or contact point the user asked to fix.

If geometry is ambiguous, return a range or alternative annotations. Uncertainty propagation through angles can be approximated by perturbing points within reviewed annotation uncertainty, but this procedure must not invent a probability distribution unsupported by the annotation protocol.

#### 3.4 Use an edit contract

Each correction should specify:

```text
Target:
  instance and named part/relation

Change:
  desired geometric delta or approved reference relationship

Preserve:
  instance identity and topology
  proportions not explicitly targeted
  camera/crop
  palette/material/shading
  untouched parts and background

Allowed consequences:
  named occlusion changes
  local background reveal
  necessary local shadow/contact adjustment

Control:
  layer transform / rig / local redraw / masked generation
  pose or layout map if supported

Acceptance:
  target tolerances
  coverage requirements
  forbidden side effects
```

**Illustrative pose correction:**

> Raise character A’s anatomical left wrist by approximately 0.08 torso lengths and move the elbow outward. Keep the shoulder, hand size, torso lean, right arm, camera, palette, and rendering unchanged. Maintain the hand–prop contact anchor.

This is not a measured recommendation for any actual asset.

**Illustrative expression correction:**

> Reduce the mouth opening while retaining its width and asymmetric corners. Keep the eyes, brows, head orientation, cheek shape, and colors unchanged.

This avoids “make less surprised,” which could change eyes, brows, mouth, and head simultaneously.

**Illustrative object-card correction:**

> Open the lid farther around the existing hinge. Keep the base silhouette, object scale, crop, colors, and material rendering unchanged. Preserve the hinge contact; allow only the newly revealed interior and corresponding local overlap/shadow changes.

Some collateral consequences are physically or pictorially necessary. “Change pose with absolutely nothing else changing” may be inconsistent when the edit reveals hidden surfaces or moves a contact shadow.

#### 3.5 Choose the least disruptive control

| Control | Best use | Side effects / limits |
|---|---|---|
| Existing layer transform | Move/rotate an isolated prop or part | Can reveal holes, detach contact, move baked shadows |
| Existing rig/IK | Articulated assets with known topology | Joint constraints and deformation may resist desired exaggeration |
| Local redraw/vector adjustment | Small stylized corrections | Requires manual consistency and cleanup |
| Text-only edit | Low-precision semantic revision | Ambiguous scope; may alter unrelated expression/style |
| Masked generative edit | Local geometry/expression reconstruction | Seams, identity drift, topology change, surrounding regeneration |
| Pose conditioning | Named joint arrangement | Does not fully specify volume, fingers, contact, identity, or depth |
| Per-instance points/boxes | Object location and count | Weak control over exact silhouette, contact, and occlusion |
| Instance masks/scribbles | Separation and outline placement | Can overconstrain contour or encourage copying unwanted shape |
| Depth/normal control | Qualified spatial structure | Estimated depth can be wrong; geometry changes can affect lighting |
| Authored 3D proxy | Repeated camera/occlusion/contact requirements | Requires setup and may impose overly realistic anatomy |

Prefer deterministic editing where the source representation supports it.

For masked generation, include enough context and edit extent to remove the old part and create the new one. A mask that covers only the destination may leave duplicate limbs; a mask that covers only the original may prevent the new silhouette. Necessary background repair should be explicitly authorized in the edit contract.

To guarantee unchanged pixels outside the edited region, preserve/composite the original outside that region. A prompt or seed alone does not provide that guarantee. Composite boundaries still require inspection.

#### 3.6 Keep conditioning compatible and coherent

Before generation:

- convert skeleton topology and landmark ordering deliberately;
- verify anatomical left/right;
- transform landmarks, masks, and depth through the same crop/resize;
- use the raster convention expected by the chosen checkpoint;
- remove stale controls that contradict the desired movement;
- associate every pose, mask, text description, and prop with the correct instance;
- specify front/back relationships separately where the interface supports them.

Do not combine an edited arm skeleton with an unchanged line-art control that still draws the old arm and then assume stronger conditioning will solve the conflict.

A human pose control trained for one skeleton cannot be assumed to understand a custom tail or wing connection. Raster control maps can discard semantic IDs; retain the structured annotation as the authoritative representation.

Use numerical coordinate interfaces when supported. A text model should not be assumed to obey “rotate 12 degrees” with engineering precision.

#### 3.7 Tune only a small number of variables

A reasonable local experiment:

1. Keep base model, reference, crop, and prompt fixed.
2. Change one target geometry or relation.
3. Compare a small set of control strengths or local edit strengths.
4. Inspect target and preservation criteria.
5. Accept, revise the annotation, or revert.

Do not simultaneously change pose map, seed, style prompt, reference weight, crop, and denoising strength if the purpose is to learn which control fixed the pose.

Stronger conditioning may improve adherence while hurting image quality; InstanceDiffusion documents this tradeoff explicitly. Do not assume monotonic overall improvement. — [Parameter notes](https://github.com/frank-xwang/InstanceDiffusion)

#### 3.8 Task-specific validation

Construct a small, stratified local evaluation set only when the parent has appropriate asset access.

Include:

- current object-only cards;
- simple human-like figures, if relevant;
- exaggerated/chibi proportions;
- nonhuman topology;
- profiles and foreshortening;
- occluded limbs and cropped subjects;
- multiple similar-looking instances;
- hand–prop contact;
- small faces at final delivery size.

Use reviewed annotations and retain disagreements. A detector should not be evaluated only on samples where it successfully found a person.

Measure separately:

**Detection and association**

- false person/face detections on object-only cards;
- instance recall;
- landmark-to-instance assignment errors;
- left/right swaps;
- topology mismatches;
- abstention rate and correctness of abstention.

**Geometry**

- normalized keypoint error;
- projected-angle error;
- part-specific error;
- line-of-action disagreement;
- layout-anchor displacement;
- silhouette gap and tangent changes;
- annotated occlusion-relation accuracy;
- contact-anchor error.

**Expression**

- landmark/ratio agreement;
- visible movement-label agreement;
- reviewer agreement on intended reading;
- no assertion of hidden emotional truth.

**Editing**

- target improvement;
- non-target joint/part drift;
- instance count and identity preservation;
- topology integrity;
- unchanged-region pixel differences where exact preservation is required;
- palette/material/shading changes;
- delivery-size readability.

No universal acceptance threshold is proposed. Set thresholds from art-direction tolerance, image scale, and annotation repeatability.

For example, an illustrative requirement of \(0.01W\) corresponds to only 1.28 pixels on a 128-pixel-wide card. If annotation disagreement already exceeds that, reporting fine decimal precision is misleading.

Where a target moves, evaluate preservation outside an agreed **edit envelope** covering the original location, destination, and necessary repair. Do not count required local reconstruction as an unexplained failure, or exempt the entire image and hide collateral changes.

Do not use the same unvalidated pose detector as both the sole conditioning source and sole quality judge. It can reward images that satisfy its own bias rather than the artist’s intended geometry.

#### 3.9 Practical decision rule

- **Single unarticulated object:** body gesture/expression N/A; check orientation and component staging.
- **Small articulated prop:** manual anchors and local editing usually suffice.
- **One human-like figure:** reviewed sparse landmarks first; detector optional.
- **Exaggerated/nonhuman figure:** ontology and manual validation before automation.
- **Multiple interacting subjects:** instance association, contact, and local occlusion graph become mandatory.
- **Repeated known 3D requirements:** authored rig/camera constraints may be more reliable than reconstructing a drawing.
- **Only “energy” or emotion differs:** obtain concrete approved examples and human judgments; do not invent a definitive score.

### Gaps

#### Evidence strength and limits

- **High confidence:** documented tool outputs; explicit code-license text; OpenFace’s restrictive terms; the distinction between geometric descriptors and emotion inference; cited release limitations.
- **Moderate confidence:** the proposed applicability and stack recommendations, conditional on the stated asset types.
- **Unvalidated proposals:** feature weights, normalization choices, edit envelopes, project acceptance thresholds, detector suitability, and end-to-end correction performance.
- No claim of collateral-free generative editing is supported.
- No reviewed evidence establishes a single automatic “Playrix gesture/style” metric.

#### Primary-source index

All accessed **2026-10-31**. Fourteen primary-source groups were materially used; associated documentation, license files, and model cards are linked inline.

1. Guay, Cani, Ronfard. **The Line of Action**, SIGGRAPH Asia 2013. [Project/paper abstract](https://team.inria.fr/imagine/the-line-of-action-an-intuitive-interface-for-expressive-character-posing/)
2. COCO authors. **Official keypoint evaluator.** [Source](https://raw.githubusercontent.com/cocodataset/cocoapi/master/PythonAPI/pycocotools/cocoeval.py)
3. Google. **MediaPipe Pose Landmarker.** [Guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)
4. Google. **MediaPipe Face Landmarker.** [Guide](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker)
5. OpenMMLab. **MMPose.** [Repository](https://github.com/open-mmlab/mmpose)
6. Yang et al. **DWPose**, 2023. [Repository](https://github.com/IDEA-Research/DWPose)
7. Baltrušaitis et al. **OpenFace.** [Repository](https://github.com/TadasBaltrusaitis/OpenFace)
8. Barrett et al. **Emotional Expressions Reconsidered**, 2019. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/)
9. Ju et al. **Human-Art**, CVPR 2023. [Repository](https://github.com/IDEA-Research/HumanArt)
10. Yu et al. **AP-10K**, NeurIPS Datasets and Benchmarks 2021. [Repository](https://github.com/AlexTheBad/AP-10K)
11. Zhang, Rao, Agrawala. **ControlNet**, 2023. [Repository](https://github.com/lllyasviel/ControlNet)
12. Wang et al. **InstanceDiffusion**, CVPR 2024. [Author reimplementation](https://github.com/frank-xwang/InstanceDiffusion)
13. Du et al. **ControlPose**, CVPR Findings 2026. [Paper page](https://openaccess.thecvf.com/content/CVPR2026F/html/Du_ControlPose_High-Fidelity_Pose-Controlled_Image_Generation_with_Multi-Faceted_Pose_Disentanglement_CVPRF_2026_paper.html)
14. Hong et al. **OccluRank**, August 2026 preprint. [Paper](https://arxiv.org/abs/2608.20932); [repository](https://github.com/Wenyang-hong/OccluRank)

#### Research execution and handoff

- Used eight Kagi discovery searches, one Context7 library resolution, two Context7 documentation queries, and public primary-page/source/license fetches.
- No Perplexity, Deep Research, Kagi Assistant, Exa, external image analysis, image uploads, package installation, model-weight downloads, or untrusted-code execution.
- Checked current 2026 sources, official output documentation, explicit license files, and repository release caveats.
- No project images or credential values were inspected.
