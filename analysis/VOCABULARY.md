# Art-analysis vocabulary → evidence

Use these terms to describe an image, not as a proposed generator API. **D** means an observable deterministic descriptor under stated preprocessing; **C** requires reviewed regions, landmarks, correspondence, or calibration; **L** means learned estimate; **H** means interpretation/perceptual judgment; **N** means the underlying cause is generally not identifiable from this image. Labels describe the claim, not software prestige. A predicted mask followed by exact area arithmetic is **L→C**.

Tool shorthand: **summary** and **profile** are the existing [CLI](../scripts/image_evidence.py); **regionprops**, texture, and morphology are installed scikit-image APIs; **Colour**, **PyWavelets**, and **POT** are installed libraries. “Review” means no automatic tool here establishes the term. See [TOOLS](TOOLS.md) for paths and [RECIPES](RECIPES.md) for use.

## Lighting and shading

Roles, directions, source extent, and visible effects are different fields. A key can be upper-left, frontal, broad, and dominant simultaneously. Describing that appearance does not identify the historical lamps.

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Illumination | Light incident on surfaces; distinguish its hypothesized organization from delivered colors. | H/L hypothesis; original parameters N. |
| Shading | Image variation depicting form and light–surface interaction, including illustrated conventions. | C reviewed material-region profiles; optional L Marigold. |
| Diffuse shading | A component modeling diffuse illumination response under a declared decomposition; not every broad gradient. | L Marigold IID-Lighting estimate; C same-material profiles supply appearance evidence, not a unique decomposition. |
| Key | Dominant organizing illumination role, not a direction or lamp type. | H interpretation from several cues; no exact detector. |
| Fill | Illumination opening shadows; not simply a brighter image background. | C shadow-side appearance via summary; physical contribution N. |
| Negative fill | Reduced surrounding bounce or fill, not emission of negative light. | H lighting interpretation; C reviewed shadow-side evidence, no automatic detector. |
| Bounce/reflected fill | Indirect light reflected from surrounding surfaces that contributes to illumination. | H/L hypothesis; C regional evidence cannot identify its unique contribution. |
| Backlight | Illumination from behind the subject relative to the viewer. | H/L hypothesis; check silhouette and shadow cues. |
| Practical | A depicted visible light source, not necessarily the dominant source. | H identify depicted lamp; power contribution N. |
| Environment light | Broad surrounding illumination, rather than one isolated accent. | H description; whole-image average cannot establish it. |
| Light direction | Direction toward a hypothesized source in a declared frame. | C image shadow vector; 3D direction generally N. |
| Apparent source extent | Angular size of a source as seen by a surface point. | Authored-scene quantity; inverse inference N without geometry. |
| Form/attached shadow | Darker object surface turned away from illumination, not necessarily cast onto another surface. | C same-material review and profile; dark paint confounds. |
| Cast shadow | Occlusion of illumination on a receiving surface. | C receiver/shadow masks, coverage, direction, extent. |
| Contact darkening | Local darkening where surfaces meet or approach; supports grounding. | C/H reviewed contact gap; not automatic ambient-occlusion recovery. |
| Umbra | Region fully occluded from a specified extended light source. | H physical explanation; dark pixels alone are insufficient. |
| Penumbra | Region with partial visibility of an extended source. | C reviewed transition appearance; blur can imitate it. |
| Shadow softness | Breadth of a shadow transition, separately from its darkness. | C profile 10–90% width with valid plateaus. |
| Specular highlight | View-dependent reflected-light appearance, or its painted depiction. | C/H annotated shape/area; bright pixels are not proof. |
| Specular reflection | Directionally concentrated reflection whose appearance depends on surface, illumination, and view. | H/L interpretation from reviewed highlights; no automatic physical separator. Intrinsic residuals are not exclusively specular. |
| Rim | Illuminated-looking band near a silhouette, often associated with rear/side light. | C/H boundary coverage/width; distinguish graphic outlines. |
| Albedo | Reflectance/base-color concept, separate from illumination in a declared model. | L intrinsic estimate; not the observed palette or recovered truth. |

Sources: [Blender light roles/types](https://docs.blender.org/manual/en/latest/render/lights/light_object.html), [PBRT area lights](https://www.pbr-book.org/4ed/Light_Sources/Area_Lights), and the [lighting note](../research_notes/Measuring%20and%20controlling%20visual%20style/01%20lighting%20and%20value.md). Multiple geometry/reflectance/light explanations can fit the same image: [bas-relief ambiguity](https://link.springer.com/article/10.1023/A:1008154927611).

## Tone and value

Name a representation and region before comparing light–dark appearance. The tool's Y, Oklab L, and chroma fields are different coordinates, not interchangeable sliders.

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Value | Artistic light–dark placement or grouping; specify its numerical proxy separately. | H organization; D/C summary Y or lightness. |
| Relative luminance Y | Linear-light, reference-relative photometric coordinate derived from characterized RGB. | D/C Colour → summary; dimensionless, not nits. |
| Brightness | Perceived intensity of an area, affected by context. | H; Y supplies evidence, not identical perception. |
| Value grouping | Organization into broad light, middle, and dark masses. | H/C reviewed regions; thresholds must be declared. |
| High/low key | Predominantly light/dark appearance under an artistic convention. | H supported by quantiles; high key need not mean low contrast. |
| Contrast | Difference or variation between specified image values at a specified scale. | D/C quantile spread or paired regions; not softness. |
| Roll-off | How tonal values approach highlights or shadows, rather than an abrupt endpoint. | C profiles/histograms; original tone curve N. |
| Clipping | Values reaching an encoding/output bound after processing. | D endpoint occupancy; prior discarded detail N. |
| Chiaroscuro/tenebrism | Prominent light–shade organization / illuminated details against a largely dark setting. | H historical descriptors, not key/fill or lamp measurements. |

Sources: [W3C relative luminance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [Tate chiaroscuro](https://www.tate.org.uk/art/art-terms/c/chiaroscuro), [National Gallery tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism). Decode encoded sRGB before Y; Colour performs that decoding in `sRGB_to_XYZ`, so do not decode twice.

## Color and palette

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Hue | Chromatic direction, often a cyclic angle in a named space. | D/C Colour/Oklab; unstable near neutral, no ordinary wrap subtraction. |
| Chroma | Colorfulness relative to an appropriate similarly illuminated reference. | D/C model coordinate, e.g. sqrt(a²+b²); not a percentage. |
| Saturation | Colorfulness relative to the area's own brightness; HSV S is one software coordinate. | H or named-model D; not interchangeable with chroma. |
| Lightness | Perceived brightness relative to an appropriate similarly illuminated white reference. | H; CIELAB L* and Oklab L are distinct model correlates. |
| Palette | Selected image colors and their masses/roles, not material albedo or a light spectrum. | D/C summary fixed bins; POT role-distribution comparison. |
| Neutral share | Fraction judged or defined as weakly chromatic in a named space. | C declared chroma rule; no universal neutrality cutoff. |
| Warm/cool relationship | Contextual chromatic relationship between regions or accents. | H/C declared hue convention; not kelvin. |
| Color difference | Distance between specified color samples under a declared formula. | C Colour `delta_E`; corresponding patches required. |
| Gamut | Colors representable by a specified encoding/device. | D known space; clipping history not inferable from final pixels. |

Sources: CIE [lightness](https://cie.co.at/eilvterm/17-22-063), [saturation](https://cie.co.at/eilvterm/17-22-073), [chroma](https://cie.co.at/eilvterm/17-22-074); [Oklab](https://bottosson.github.io/posts/oklab/). Average image RGB cannot establish [source CCT](https://cie.co.at/eilvterm/17-23-068).

## Composition, hierarchy, and space

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Framing | Selection of artwork aperture, crop, and relation to canvas boundaries. | D/C dimensions and reviewed aperture; exclude UI/frame. |
| Occupancy | Selected subject area divided by declared aperture area. | C mask union → summary; no mask means whole frame. |
| Margins | Clearances between selected extent and aperture boundaries. | C summary bounding-box margins; transparent glow policy matters. |
| Negative space | Space around/between positive forms; can be textured or active. | C/H reviewed regions, not merely white pixels. |
| Balance | Distribution of visual weight in a composition. | H; region centroids are evidence, not perceived balance. |
| Hierarchy | Ordering of perceptual/communicative importance. | H; regional contrast/detail supports review, not attention truth. |
| Emphasis | Means used to make a focal feature stand out. | H/C local contrast, placement, isolation; no universal score. |
| Separation | Distinguishability of subject from adjacent context. | C/H region contrast and intended-size recognition review. |

Sources: Getty [formal analysis](https://www.getty.edu/education/teachers/classroom_resources/formal_analysis.html) and [design principles](https://www.getty.edu/education/teachers/building_lessons/principles_design.pdf). A contrast map is not measured fixation, comprehension, or recognition.

## Shape and silhouette

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Silhouette | Projected outer shape with an explicit treatment of holes and attached parts. | C reviewed mask; not hidden geometry. |
| Proportion | Relative size of named parts or landmarks. | C landmark ratios; object-category baseline required. |
| Aspect/elongation | Width/height or principal-axis ratio, which must be distinguished. | D canvas aspect; C regionprops axis geometry. |
| Compactness | Area–perimeter relationship under a declared formula. | C Crofton perimeter/area; resolution and contour noise matter. |
| Solidity | Mask area divided by convex-hull area. | C regionprops; not recognition or aesthetic quality. |
| Openings/negative gaps | Interior holes or spaces between diagnostic parts. | C topology/landmarks; preserve handles and prongs explicitly. |
| Apparent volume | Perceived three-dimensional fullness. | H/L shading/shape cues; physical volume N. |

Measurement definitions and domain cautions: [shape note](../research_notes/Measuring%20and%20controlling%20visual%20style/06%20shape%20scale%20and%20silhouette.md). Do not make plants and geometric tools share one ideal compactness.

## Edges, contours, and marks

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Edge | Local transition in image values, regardless of cause. | D gradients/Sobel; not necessarily a drawn line. |
| Contour | Boundary describing shape or a selected region. | C mask boundary; distinguish internal transitions. |
| Outline | Explicit contour-like graphic treatment around a form. | H/C reviewed stroke mask; not necessarily rim illumination. |
| Stroke | A mark with footprint, width, trajectory, and possibly taper. | C medial axis/distance on a stroke mask, not Canny thickness. |
| Hard/soft edge | Narrow/broad transition at a declared scale and contrast. | C profile; native-pixel width is not a universal style label. |
| Lost edge | Boundary with weak/absent visible separation in context. | H/C reviewed correspondence; detector absence alone is insufficient. |
| Sfumato | Gradual tonal modulation avoiding harsh outlines. | H historical technique; not synonymous with Gaussian blur. |

Sources: [National Gallery sfumato](https://www.nationalgallery.org.uk/paintings/glossary/sfumato), [edge note](../research_notes/Measuring%20and%20controlling%20visual%20style/04%20edges%20lines%20and%20vectors.md). Edge density does not count strokes or identify artistic economy.

## Texture, markmaking, and material finish

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Texture | Spatial organization of repeated/local appearance variation. | D/C wavelets, GLCM, LBP on valid interior support. |
| Grain | Fine granular variation; specify spatial scale and region. | D/C scale energy; may be compression/noise rather than medium. |
| Stipple | Dot-like mark construction or its visible depiction. | C/H reviewed motifs; energy alone does not identify dots. |
| Hatching | Organized line marks encoding tone, form, or material. | C/H orientation/spacing; not any directional texture. |
| Brush scale | Mark size relative to native pixels or subject extent. | C reviewed marks/multiscale evidence; one Haar level is insufficient. |
| Mark direction | Orientation field of visible marks. | C structure tensor/review; not necessarily gaze direction. |
| Matte/glossy | Weakly pronounced versus pronounced specular-looking appearance in context. | H/C reviewed highlights; physical roughness N. |
| Metallic-looking | Appearance suggesting metal through reflectance/color cues. | H/L; not measured metallic composition. |
| Translucent-looking | Appearance suggesting light transport through/scattering within a material. | H/L; not equivalent to image alpha. |

Sources and measurement contracts: [surface/finish note](../research_notes/Measuring%20and%20controlling%20visual%20style/07%20texture%20material%20and%20finish.md), [PBRT](https://www.pbr-book.org/4ed/Light_Sources/Area_Lights). Filter the whole image before regional aggregation; zeroing a mask first creates artificial boundaries.

## Depth, viewpoint, and perspective

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Occlusion/overlap | One visible form covers another. | C annotated order/masks; ambiguous boundaries require review. |
| Projection | Rule mapping geometry to an image, e.g. perspective or orthographic. | H/L hypothesis; original camera model generally N. |
| Perspective convergence | Projected parallel directions meeting toward vanishing points. | C reviewed line families; not arbitrary scene lines. |
| Horizon | Image line associated with a chosen world-horizontal plane at eye level. | C calibrated/justified geometry; not simply a floor seam. |
| Viewpoint | Camera–object relationship determining visible faces. | C/H landmarks/face ratios; depth alone does not recover it. |
| Foreshortening | Reduced projected extent along a receding direction. | C known or comparable part geometry; not just small size. |
| Atmospheric perspective | Distance-related appearance separation through scattering or its artistic depiction. | H/C contrast/color trends; not necessarily blue tint. |
| Blur/depth of field | Image unsharpness / focus-related depth dependence. | C edge profiles; blur does not identify aperture or lens. |

Source: [depth/perspective note](../research_notes/Measuring%20and%20controlling%20visual%20style/05%20depth%20perspective%20and%20optics.md). DAV2 relative depth and Marigold normals are L hypotheses, not meters or original camera metadata.

## Rhythm and staging

| Term | Precise use | Evidence / tool route |
|---|---|---|
| Motif/pattern | Recurring element / arrangement of repeated elements. | C reviewed detections; FFT alone does not identify motifs. |
| Pitch/gap | Center-to-center repeat distance / boundary-to-boundary separation. | C landmarks or masks; distinguish the two measurements. |
| Alternation/progression | Ordered category changes / systematic variation along a sequence. | C labels/size sequence; not histogram proportions alone. |
| Rhythm | Organized recurrence and variation producing a sense of movement. | C recurrence evidence; H effect, no emotional “BPM.” |
| Staging | Arrangement making an action or relation legible. | C/H support, contact, overlap, tilt, and instance relations. |
| Gesture/expression | Organized action cues / visible expressive configurations. | C landmarks; H interpretation, actual intention/emotion N. |

Sources: [Getty principles](https://www.getty.edu/education/teachers/building_lessons/principles_design.pdf), [rhythm note](../research_notes/Measuring%20and%20controlling%20visual%20style/09%20rhythm%20pattern%20and%20repetition.md), [staging note](../research_notes/Measuring%20and%20controlling%20visual%20style/10%20gesture%20expression%20and%20staging.md).

**Resolution rule:** approximately 59×67 project crops support coarse object/composition observations, not fine penumbra, brushwork, or material-finish conclusions. Upscaling adds samples, not evidence. Retain “not assessable” instead of converting every term into a number.
