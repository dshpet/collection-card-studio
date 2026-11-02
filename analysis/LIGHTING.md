# “How does this lighting/shading look?”

The useful result is a supported description: where values change, how broad a shadow transition is, which highlights articulate form, and which interpretations remain uncertain. Neither the whole-image histogram nor a learned decomposition uniquely recovers lamps, exposure, physical roughness, or kelvin. See [vocabulary](VOCABULARY.md#lighting-and-shading) and [tool lookup](TOOLS.md).

## 1. Fix the image and separate regions

Record native dimensions, artwork crop, file hash, profile handling, and any alpha/background choice. The CLI EXIF-transposes and converts usable ICC profiles to sRGB; missing profiles are recorded assumptions. Use the same preparation for comparisons. Do not enlarge a 59×67 crop and interpret the new samples as fine shadow evidence.

Review distinct masks/landmarks for the visible subject, same-material surface patches, receiver, cast shadow, highlights, background, and effects. A subject union is not a lighting-region label. A contact shadow is relevant to a grounded object, not mandatory for a floating card. Keep a material boundary or painted dark stripe out of a purported illumination comparison.

## 2. Measure rendered value groups with `summary`

Run `summary` separately with each reviewed grayscale mask, using identical dimensions and values ≥128 for selection. Inspect `value_color.luminance_Y` and its p10/p50/p90/spread; Oklab L is a separate lightness coordinate. Compare comparable material/receiver regions, not the entire light background against the entire colored subject. Retain masked geometry and sample counts.

Describe “the shadow-side region is darker” or “broad shading remains legible.” A lit/shadow patch ratio mixes reflectance, orientation, illumination, specularity, and grading. Call it a **rendered patch luminance ratio**, not key/fill. Source conventions K/F and (K+F)/F are different even in controlled setups. No exact physical ratio follows from these pixels.

## 3. Locate shadows and highlights before interpreting direction

For an appropriate receiver, mark an object/contact anchor and a shadow displacement endpoint. In raster coordinates x-right/y-down, an explicitly image-plane angle is `atan2(-dy, dx)`. Report the chosen landmarks and convention. It is not a 3D light azimuth; receiver orientation, perspective, multiple lights, and painted conventions confound inversion.

Inspect form shading and highlight placement as corroborating cues. A narrow bright silhouette band may be a rim, but a continuous painted outline is not proof of backlighting. Bright patches can be white paint or emission. Keep “plausible broad upper-left illumination” in H interpretation, not D measurement.

## 4. Profile a reviewed shadow boundary

Use `profile` across the boundary approximately normal to it, spanning reasonably stable shadow and lit plateaus on the **same receiver material**. Choose a linewidth that averages local noise without crossing another feature; document it. Read `profile.distance_px` and `profile.luminance_Y`. The CLI samples linear relative Y with order 1 interpolation, averages across linewidth, and can reflect at image edges. Stay away from edges if reflection would invent support.

For a sufficiently contrasted, approximately monotonic transition, estimate representative plateau levels from reviewed endpoint windows, not automatically from the minimum/maximum. Normalize

\[
t(s)=\frac{Y(s)-Y_{shadow}}{Y_{lit}-Y_{shadow}},\qquad
w_{10-90}=|s_{0.9}-s_{0.1}|.
\]

Interpolate threshold crossings within a single justified transition. For a descending profile retain signed endpoint normalization or reverse the sample order explicitly. Reject insufficient contrast, missing plateaus, multiple crossings, receiver texture/color boundaries, contact zones, clipped endpoints, and overlapping shadows. Do not force the formula to return a number. Record rejected profiles and variation among accepted nearby profiles; report native pixels and, only with a valid reviewed subject scale, normalized width.

**Separate contrast from softness.** A weak sharp transition and a strong broad transition can have similar gradient magnitude. Report endpoint contrast and width separately. A measured transition can include antialiasing, defocus, processing blur, resampling, or painted softness. It does not identify emitter size or blocker distance. The CLI returns samples, **not automatic softness**.

## 5. Add a learned layer only if it answers the question

If image variation cannot be interpreted locally, Marigold IID-Lighting is a source-only candidate for **estimated albedo, diffuse shading, and non-diffuse residual**. Its [runner](../.slim/clonedeps/repos/prs-eth__Marigold/script/iid/run.py) defaults to IID-Appearance; that is not the shading checkpoint. The intended candidate is `prs-eth/marigold-iid-lighting-v1-1`. Normals require the separate normals pipeline/checkpoint. See [gates](RECIPES.md#source-only-models-not-enabled).

These maps are L estimates influenced by training priors and processing, not recovered layers from the original artwork. Agreement among learned maps is not independent physical confirmation. No model dependencies or weights are enabled here, and CPU/AMD inference remains unverified.

## Illustrative record — no measurements claimed

```yaml
question: describe shadow and form-shading appearance
input: user_selected_image
regions: reviewed subject / receiver / shadow / highlight masks
preprocessing: record native size, ICC handling, explicit alpha backdrop
observations:
  regional_Y: calculate summary with separately reviewed masks
  profile: select same-material boundary and endpoint windows
  contrast_and_width: report separately; abstain if profile invalid
  image_shadow_angle: only after reviewed landmarks; not 3D azimuth
interpretation:
  illumination_organization: hypothesis, not measured lamp arrangement
  source_count: not_identified
  key_fill_ratio: not_identified
  source_temperature_kelvin: not_identified
optional_estimator: not_run
```

This is an illustrative worksheet, not an image result. The [ready synthetic example](examples/README.md) demonstrates the arithmetic on a 256×96 RGB8 ramp: the recorded profile spans x=0…255 at y=48, linewidth 5. Its unquantized expected 10–90% width is 96 px; the stored 8-bit fixture gives 96.82192026779823 px using reviewed endpoint windows. See the [measurement record](examples/shadow_measurement.json) and [23-check verification](verification.json). This validates sample/threshold mechanics and quantization effects, not real-shadow physics or lighting inference on project references. The [card summary](examples/card_summary.json) describes a 59×67 whole frame, not a detected subject or lighting region.

Source basis: [existing lighting note](../research_notes/Measuring%20and%20controlling%20visual%20style/01%20lighting%20and%20value.md), [W3C relative luminance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), and [PBRT area lights](https://www.pbr-book.org/4ed/Light_Sources/Area_Lights). No universal contrast/width acceptance threshold is prescribed.
