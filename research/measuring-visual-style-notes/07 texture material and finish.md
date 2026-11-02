# Texture, material appearance and rendering finish

Validated **14 primary-source documents/pages**, including 2026 Materialist evidence. No installs, model downloads, image uploads, or untrusted repository execution. Main uncertainty: no validated universal metric or independently controllable prompt parameter exists for “painterliness,” perceived material, or rendering finish across arbitrary stylized illustrations.

Research cutoff and source access date: **2026-10-31**.

Scope: describing, measuring and selectively correcting surface appearance in flattened stylized RGB illustrations. This note distinguishes **visible image evidence** from **inferred physical materials or production processes**. Formulas and recommended operating ranges below are an engineering proposal unless explicitly attributed; they are not universal perceptual thresholds.

## 1. What surface/rendering axes can an illustration support?

### Takeaway

Represent surface style as several appearance axes—not a single “texture” or “roughness” score. Pixel statistics can be measured deterministically, but their interpretation as brushwork, metallicity, subsurface scattering, physical roughness, or an actual painting medium is conditional or underdetermined.

### Cited Findings

#### Physical materials are not uniquely identifiable from appearance

A material’s appearance changes with illumination, viewpoint and shape. Fleming’s material-perception review explicitly argues that perceived gloss need not involve recovering BRDF parameters; observers can use combinations of low- and mid-level appearance measurements instead. This supports an **appearance-first vocabulary**, not conversion of RGB statistics directly into physical roughness. **Confidence: high** for the ambiguity; the proposed vocabulary below is an engineering inference. — Fleming, *Visual perception of materials and their properties*, published January 2014: https://pubmed.ncbi.nlm.nih.gov/24291494/

Blender’s Principled BSDF documents separate controls for microfacet roughness, metallicity, IOR/specular intensity, subsurface scattering, transmission, coat, sheen and normals. These controls describe a forward shading model. Their existence does **not** imply that each value can be independently recovered from one arbitrary RGB image. **Confidence: high.** — Blender 4.5 LTS manual: https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html

Materialist is current evidence of **prior-conditioned inverse rendering**, not proof of unique recovery. Its January 2025 preprint was revised in May 2026 and appeared in IJCV in 2026. It predicts initial material properties and optimizes them through differentiable rendering. Its repository explicitly warns that its transparency-editing implementation approximates light paths and can produce inaccurate refraction. **Confidence: high** for method and disclosed limitation; stylized-illustration applicability remains unvalidated here. — Paper: https://arxiv.org/abs/2501.03717 ; implementation: https://github.com/lez-s/Materialist

#### Separate these latent causes before naming measurements

The following is a proposed working decomposition, informed by the ambiguity above:

| Layer | What belongs here | Common misleading interpretation |
|---|---|---|
| Intrinsic surface/material | Reflectance, transmission, scattering, microgeometry; material-bound pigment/fibre patterns | Treating every bright patch as specular reflection |
| Shape and illustration construction | Facets, folds, hand-painted gradients, outlines, hatch marks, painted highlights | Calling faceted shading “high material roughness” |
| Illumination/environment | Light size and direction, reflected environment, cast shadows, rim light, atmospheric glow | Calling a large soft-light reflection “rough plastic” |
| Camera/optical appearance | Defocus, motion smear, flare, aberration, vignetting | Assuming a generated illustration had a physical lens |
| Processing/export | Grain/noise overlays, sharpening, bloom, tone curves, resize ringing, compression | Treating sharpening residue as brush texture |
| Content/semantics | Hair, foliage, grass, scales, lettering, repeated architectural detail | Calling a busy subject “more painterly” |

This is a **diagnostic decomposition**, not an identifiable factorization of every input.

#### Prompt-ready appearance vocabulary

Use localized descriptions with explicit exclusions. These are proposed prompting terms, **not validated numerical controls**.

| Appearance axis | Prompt-ready descriptions | Keep separate from |
|---|---|---|
| Smoothness of image finish | “Clean uninterrupted colour fields”; “smooth airbrushed transitions”; “no visible surface grain” | Physical microfacet roughness |
| Visible brush marking | “Sparse visible tapered strokes”; “broken dry-brush marks”; “broad overlapping directional strokes” | Generic high-frequency noise |
| Stroke scale | “Fine bristle marks”; “medium-width strokes”; “large chunky strokes readable at thumbnail size” | Subject size and export resolution |
| Stroke organization | “Strokes follow surface curvature”; “crosshatched marks”; “loosely varied stroke directions” | Anisotropic specular reflection |
| Impasto-like appearance | “Raised paint-ridge appearance with tiny paired highlights and shadows” | Proof of thick physical paint |
| Pigment/paper appearance | “Subtle irregular paper tooth”; “mottled pigment pooling”; “soft granulation inside washes” | Sensor noise or JPEG damage |
| Shape shading | “Two broad cel-shaded tone regions”; “soft continuous volume gradients”; “faceted planar shading” | Material roughness |
| Matte/gloss appearance | “Low-contrast broad highlights”; “small crisp white highlights”; “soft satin reflections” | A recoverable BRDF value |
| Metal-like appearance | “Coloured reflective highlights and strong environment-colour variation” | Definitive metal identification |
| Wax/skin-like softness | “Soft warm light spread at thin edges”; “gentle colour bleed into shadow” | Proven subsurface scattering |
| Transmission-like appearance | “Visible background through the object”; “distorted background seen through the surface” | Alpha transparency alone |
| Grain/noise | “Fine low-amplitude monochrome grain”; “coarser clustered grain”; “no chroma speckling” | Brushwork |
| Highlight surround | “Restrained soft glow around brightest highlights”; “subtle warm fringe around highlights” | Confirmed optical bloom or film halation |
| Acutance | “Crisp contours without bright/dark halos”; “soft edges with no sharpening fringe” | True spatial resolution |
| Directional blur | “Short directional smearing confined to the moving object” | Painterly streaks or camera motion |

For example:

> Preserve the silhouettes, palette, composition, lighting direction and broad shadow shapes. Change only the interior surface finish: use sparse medium-width strokes following form, with low-amplitude pigment variation. Keep contours crisp; do not add global grain, bloom or glossy highlights.

“Painterly,” “oil painting,” “cinematic” and “3D render” are broad bundles. They can change colour, composition, geometry and lighting as well as finish. Prefer the observable description when axis isolation matters.

#### Verdict categories

| Requested output | Verdict |
|---|---|
| Local variance, band energy, GLCM, LBP or Fourier statistics under fixed preprocessing | **Deterministic measurement** |
| Relative texture scale or orientation within comparable masked regions | **Conditional descriptor** |
| “This looks smoother / more stroke-marked / glossier” | **Conditional perceptual judgment** |
| Roughness, metallic, normal or illumination maps from an inverse-rendering network | **Learned, prior-conditioned estimate** |
| Actual BRDF roughness, actual metallic composition, true subsurface coefficient | **Underdetermined from arbitrary stylized RGB** |
| Physical oil versus acrylic versus digitally simulated brush medium | **Underdetermined without provenance** |
| Lens, film stock, camera motion or codec inferred solely from simulated artifacts | **Underdetermined provenance** |

The category distinction follows the difference between measurable image representation, perception and inverse rendering. — Fleming: https://pubmed.ncbi.nlm.nih.gov/24291494/ ; Blender: https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html ; Materialist: https://arxiv.org/abs/2501.03717

### Inferences

- Store **surface appearance**, **shape shading**, and **image finish** in separate feature groups.
- Report “gloss-like highlight evidence” rather than “roughness = 0.27” unless geometry, lighting, rendering model and calibration make that estimate meaningful.
- An image may be smooth but matte, smooth and glossy, strongly brush-marked but visually matte, or brush-marked with impasto-like highlights.
- Physical shader anisotropy, directional brushwork and motion blur are different causes of directional image structure. One orientation score cannot identify which caused it.

### Gaps

- No source validated a universal scalar “painterliness” scale for arbitrary stylized illustration.
- No retrieved evidence justified identifying a true painting medium, physical roughness, or material composition from a flattened stylized RGB image alone.
- Highlight geometry and warm edge-light effects can support a description, but do not establish their physical origin.

## 2. Which numerical features are useful, and under what preprocessing?

### Takeaway

Use **multiscale, region-conditioned feature distributions**, retaining both texture amplitude and structure. A whole-image texture score is usually confounded by subject detail, silhouettes, lighting, resolution and export history.

### Cited Findings

#### Why multiscale and higher-order statistics?

Portilla–Simoncelli represents texture using multiscale oriented filters and statistics involving nearby positions, orientations and scales. Its author-maintained description includes pixel moments, correlations of coefficients and magnitudes, and relative phase. The authors use synthesis to test the representation rather than relying only on classification. This is strong prior art against assuming that a histogram or radial power spectrum fully describes texture. **Confidence: high.** — Portilla & Simoncelli, IJCV 2000; project page updated September 2024: https://www.cns.nyu.edu/~lcv/texture/

Gatys et al. represent textures through correlations between CNN feature maps at several layers. Their abstract explicitly notes that deeper representations also make object information more explicit. Consequently, learned “style features” are not automatically content-free. **Confidence: high.** — *Texture Synthesis Using Convolutional Neural Networks*, 2015: https://arxiv.org/abs/1505.07376

scikit-image provides GLCM, LBP, structure tensors and multiscale basic features. Its GLCM interface requires nonnegative integer grey levels and exposes distance, angle, symmetry and normalization choices. These settings are part of the measurement definition, not interchangeable defaults. **Confidence: high.** — Official feature API: https://scikit-image.org/docs/stable/api/skimage.feature.html

PyWavelets’ stationary wavelet transform avoids coefficient decimation, giving shift invariance at the cost of redundancy. For an orthogonal wavelet with the documented normalization and retained-coefficient settings, energy is conserved and variance partitions across scales. Dimensions must be compatible with the requested decomposition level, or padded. **Confidence: high.** — Official SWT documentation: https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html

#### Proposed preprocessing contract

The following is a reproducible operating specification, **not a published universal standard**.

1. **Keep the original raster untouched.** Record dimensions, colour profile, alpha treatment and known export/resizing history.
2. **Use a declared colour representation.**
   - For appearance matching, retain an sRGB/display-referred branch.
   - For linear filtering experiments, optionally use decoded linear-light RGB.
   - Never compare numbers from different transfer-function branches without identifying the difference.
3. **Keep luminance and chromatic texture separate.** For linear sRGB, a conventional luminance calculation is  
   \(Y=0.2126R+0.7152G+0.0722B\).  
   Apply that formula to gamma-encoded RGB only if explicitly labelling the result as a luma-like proxy rather than linear luminance.
4. **Compare at native and standardized viewing scale.**
   - Native scale exposes export artifacts.
   - A common output/viewing scale supports perceptual matching.
   - A subject-normalized scale supports comparison of strokes relative to the depicted object.
5. **Specify interpolation and antialiasing.** scikit-image documents antialiasing support for downsampling; range preservation must also be explicit. — Official documentation/release notes: https://github.com/scikit-image/scikit-image/blob/main/doc/source/release_notes/release_0.14.rst
6. **Do not sharpen, denoise or equalize histograms before the primary measurements.** Those operations can remove or manufacture the axis being measured. Use separately labelled diagnostic branches if needed.
7. **Save masks and all measurement settings** alongside each feature vector.

scikit-image’s documentation warns that dtype conversion and intensity-range conventions matter; simply casting an 8-bit array to floating point does not normalize its values. Current development documentation also differs from stable APIs, so pin the installed version instead of copying unversioned `main` examples. — Official API and source documentation: https://scikit-image.org/docs/stable/api/skimage.feature.html

#### Required masks

Use separate masks, rather than one universal “subject” mask:

- **Subject/background masks:** prevent background texture from dominating.
- **Material/semantic region masks:** compare skin-like regions with skin-like regions, fabric with fabric, sky with sky.
- **Interior masks:** exclude silhouette and major internal-boundary contamination.
- **Low-structure/flat-region masks:** estimate grain and residual texture away from text, fine content, strong shading edges and highlights.
- **Highlight/transition masks:** measure highlight width, softness and surrounding glow separately.
- **Protected-detail masks:** preserve eyes, facial features, lettering, line art and small design accents during correction.
- **Artifact diagnostic regions:** include suitable edges and flat patches; do not rely on material masks alone.

**Important:** Define flat regions from a coarsely smoothed image or manual selection. Selecting them by low raw variance would preferentially reject textured patches and bias the result toward smoothness.

For filters with finite support, retain only pixels whose full support lies inside the relevant mask. A practical implementation can erode the mask by the filter support radius. For GLCM, require **both endpoints** of each pair inside the mask. For LBP, require the full sampling ring inside. For CNN features, account for receptive-field leakage: blacking out the background is not equivalent to measuring only the foreground.

#### Spatial scales: proposed starting settings

These are **measurement-grid examples**, not universal style categories.

- At a standardized 1024-pixel short side, examine detail widths approximately **2–4, 4–8, 8–16, 16–32 and 32–64 pixels**.
- Retain the native-pixel view for approximately one-pixel artifacts.
- For an object of extent \(D\), additionally express width as \(w/D\). This distinguishes a large stroke on a small object from the same pixel width on a large object.
- Use candidate crop widths such as **64, 128 and 256 pixels**, selecting only scales with enough texture repetitions and valid interior area.
- Do not report a coarse-scale result when its filter support approaches the available region size.
- Do not interpret features lost during downsampling as observed absence of texture in the source.

#### Feature specification

Let \(M\) be a valid interior mask, \(Y\) a declared luminance/luma branch, and \(\langle\cdot\rangle_M\) masked averaging.

**A. Multiscale residual amplitude**

\[
B_s = G_{\sigma_s}*Y-G_{\sigma_{s+1}}*Y
\]

\[
E_s=\langle B_s^2\rangle_M,\qquad
e_s=\frac{E_s}{\sum_t E_t+\epsilon}.
\]

- \(E_s\): absolute band energy; nonnegative.
- \(e_s\): relative band allocation, approximately summing to one across the included bands.
- Report both: normalization alone hides whether the image is almost textureless.
- Add median absolute residual and upper quantiles to distinguish pervasive texture from sparse strong marks.
- Fix Gaussian convention, boundary treatment and scale grid.

**Interpretation:** useful for “more midscale surface variation” versus “mostly fine grain.” It cannot distinguish grain from tiny leaves without masks.

This proposal follows the multiscale representation principle, not an exact reproduction of Portilla–Simoncelli. — https://www.cns.nyu.edu/~lcv/texture/

**B. Wavelet energy and coefficient distributions**

For scale \(s\) and orientation \(o\):

\[
E_{s,o}=\langle |W_{s,o}|^2\rangle_M.
\]

Retain orientation energies, coefficient quantiles, and optionally cross-scale correlations of coefficient magnitudes.

- Ordinary decimated DWT is shift-sensitive.
- SWT is a practical CPU option when translation stability matters.
- A standard separable 2D wavelet has limited orientation selectivity; it is not equivalent to a many-orientation steerable pyramid.
- Match normalization and padding before comparing energies.

— PyWavelets: https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html ; Portilla–Simoncelli: https://www.cns.nyu.edu/~lcv/texture/

**C. Power spectrum and autocorrelation**

On a rectangular, detrended patch \(r\), with a declared window \(w\):

\[
P(u,v)=|\mathcal F\{w\,r\}(u,v)|^2.
\]

Measure:

- Radial band-energy distribution.
- Angular energy distribution.
- Dominant periodic peaks.
- Spatial autocorrelation length and directional dependence.
- Optional fitted spectral slope over a declared frequency interval.

Frequencies should be expressed in **cycles/pixel**, and optionally cycles/object. Along an image axis, the Nyquist limit is 0.5 cycles/pixel; do not quietly extend radial comparisons into inconsistently supported corner frequencies.

**Mask warning:** directly FFT-transforming a hard, irregular masked image adds the spectrum of the mask. Prefer valid rectangular crops, appropriate tapering, or a documented masked-correlation estimator.

**Interpretation:** useful for coarse/fine, periodic/stochastic and isotropic/directional distinctions. Power discards phase, so equal spectra do not establish equal brushwork or perceptual texture. The higher-order statistics used by Portilla–Simoncelli address information absent from simple second-order summaries. — https://www.cns.nyu.edu/~lcv/texture/

**D. Local orientation/coherence**

Use a smoothed structure tensor:

\[
J=G_\rho*
\begin{bmatrix}
Y_x^2&Y_xY_y\\Y_xY_y&Y_y^2
\end{bmatrix}.
\]

For eigenvalues \(\lambda_1\ge\lambda_2\ge0\):

\[
C=\frac{\lambda_1-\lambda_2}{\lambda_1+\lambda_2+\epsilon}.
\]

- Coherence is approximately in \([0,1]\).
- Near zero: isotropic or weakly structured.
- Near one: locally one-directional.
- Exclude near-zero tensor-energy pixels; otherwise orientation is unstable.
- Report distributions, not just the mean.
- The dominant tensor eigenvector describes gradient direction; stroke tangent is generally perpendicular.
- Global orientation cancellation does not imply absence of locally coherent curved strokes.

scikit-image provides structure-tensor functions; interpretation as brush direction is conditional. — https://scikit-image.org/docs/stable/api/skimage.feature.html

**E. GLCM**

Quantize a declared intensity interval into \(L\) levels. A starting experiment might use \(L=16\) or \(32\), offsets \(d=\{1,2,4,8\}\) pixels and angles \(\{0,\pi/4,\pi/2,3\pi/4\}\). These are comparison settings, not empirically established brush scales.

For normalized pair probabilities \(p(i,j)\):

\[
\text{contrast}=\sum_{ij}(i-j)^2p(i,j)
\]

\[
\text{homogeneity}=\sum_{ij}\frac{p(i,j)}{1+(i-j)^2}
\]

\[
\text{ASM}=\sum_{ij}p(i,j)^2,\qquad
\text{energy}=\sqrt{\text{ASM}}.
\]

Contrast lies between 0 and \((L-1)^2\). Dividing by that maximum makes its numeric scale easier to compare, but **does not remove quantization dependence**. Entropy depends on log base; use one declared convention.

- Preserve directional measurements if anisotropy matters.
- Per-crop min–max scaling changes the question and can inflate weak noise. Prefer fixed/shared bins for amplitude-sensitive comparisons.
- The standard `graycomatrix` API has no material-mask argument; implement valid pair selection or use clean rectangular interior crops.
- A silhouette crossing the crop can dominate the matrix.

— Official GLCM definitions and API: https://scikit-image.org/docs/stable/api/skimage.feature.html

**F. LBP**

\[
LBP_{P,R}(x)=
\sum_{p=0}^{P-1}
\mathbf1[I(x_p)\ge I(x)]\,2^p.
\]

Starting experiments: \((P,R)=(8,1),(16,2),(24,3)\), with integer intensity input and normalized histograms.

- Rotation-invariant LBP is useful when orientation should be ignored.
- Retain non-rotation-invariant measurements when direction is itself a style axis.
- LBP chiefly captures local comparison patterns; it does not retain texture amplitude.
- Tiny fluctuations in an almost-flat region can change codes.
- Compare histogram distances alongside residual amplitude, never alone.

— Official LBP interface and methods: https://scikit-image.org/docs/stable/api/skimage.feature.html

**G. Grain/noise appearance**

On manually validated or low-structure interior regions, form a residual \(r=Y-\widehat Y\). A robust scale descriptor is:

\[
\widehat\sigma_{\rm appearance}
=1.4826\,\mathrm{median}|r-\mathrm{median}(r)|.
\]

The factor is a Gaussian-consistency convention, not proof of Gaussian noise. Filtering alters residual variance; call this **residual amplitude**, not a calibrated sensor-noise estimate.

Also measure:

- Residual autocorrelation/coarseness.
- Luminance versus chromatic residual energy.
- Interchannel correlation.
- Amplitude versus local brightness.
- Stationarity across unrelated flat regions.

darktable’s grain module is explicit evidence that grain is controllable independently of a scene material: it processes the Lab lightness channel and exposes coarseness and strength. — https://docs.darktable.org/usermanual/4.2/en/module-reference/processing-modules/grain/

**H. Highlight and finish descriptors**

These are proposed appearance diagnostics requiring manual/conditional region selection:

- Highlight area relative to its material region.
- Peak-to-surround contrast.
- Edge-spread width or highlight half-maximum width, normalized by object extent.
- Highlight elongation and orientation.
- Colour difference between highlight and surrounding region.
- Broad surrounding glow versus narrow fringe.
- Frequency of small isolated glints.

They are **not direct roughness measurements**: shape, source size, exposure, clipping and hand-painted design can produce similar changes. — Fleming: https://pubmed.ncbi.nlm.nih.gov/24291494/ ; Blender: https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html

**I. Artifact diagnostics**

Use these as hypotheses, not provenance classifiers:

| Appearance | Proposed diagnostic | Main confounder |
|---|---|---|
| Sharpening halos | Bright/dark overshoot across suitable isolated edges | Deliberately painted rim accents |
| Blocking/ringing | Periodic discontinuities, edge-adjacent oscillation, native-resolution inspection | Repeated content; resampling |
| Motion-like smear | Directional edge spreading and spectral attenuation | Long strokes; directional texture |
| Defocus-like softness | Broadened transitions over comparable boundaries | Airbrushing; low source resolution |
| Chromatic fringe | Channel displacement near contrast boundaries | Deliberate coloured outlines |
| Highlight glow | Surrounding intensity profile around selected bright features | Painted light; atmosphere; bloom |
| Warm “halation-like” fringe | Warm surround conditioned on bright edges | Artistic colour accents; no evidence of actual film |

darktable documents that sharpening can magnify noise and chromatic aberrations, that excessive settings can create halos/fringes, and that its diffusion inversion does **not** reverse motion blur. Its radii are expressed in full-resolution pixels, and output assessment changes with viewing/export scale. — https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/diffuse/

#### Comparing texture descriptors with perceptual judgments

**DISTS:** The authors describe a full-reference IQA metric that combines structure and texture similarity and tolerates texture variation and mild geometric changes. Its documented input is RGB in \([0,1]\), with shape \(N,C,H,W\). This makes it useful as a complementary diagnostic, not a texture-only style score. **Confidence: high** for documented purpose; no universal stylized-illustration validity established. — https://github.com/dingkeyan93/DISTS

Implementation traps were verified in the official source:

```python
vgg_pretrained_features = models.vgg16(pretrained=True).features
```

and its example preprocessing:

```python
if resize and min(image.size)>256:
    image = transforms.functional.resize(image,256)
```

The example also selects CPU when CUDA is unavailable. Therefore, record whether preprocessing resized the image: fine finish can disappear before evaluation. Initialization may require pretrained weights, so do not instantiate it under a no-download constraint unless weights are already available. — https://github.com/dingkeyan93/DISTS/blob/master/DISTS_pytorch/DISTS_pt.py

**Gram statistics:** For feature maps \(F_l\in\mathbb R^{C_l\times N_l}\), a common normalized descriptor is:

\[
G_l=\frac{F_lF_l^\top}{N_l}.
\]

The exact layer selection and normalization must be fixed. Gram statistics summarize feature correlations, not stroke positions or independent material parameters. Content leakage remains possible, especially at deeper layers. — Gatys et al.: https://arxiv.org/abs/1505.07376

**Recommended comparison protocol, proposed rather than benchmarked:**

1. Compare semantically matched interior crops.
2. Retain deterministic descriptors for explanatory diagnosis.
3. Use DISTS or Gram features as a secondary check with fixed preprocessing.
4. Ask humans separate questions:
   - Same texture scale?
   - Same amount of visible brush marking?
   - Same matte/gloss appearance?
   - Same grain/glow/sharpness?
   - Were content and lighting preserved?
5. Evaluate both intended display size and native-pixel details.
6. Use multiple references to estimate an acceptable range; one image cannot estimate a population distribution.

### Inferences

- A high-frequency energy increase can mean grain, sharpening, hair, foliage or brush detail. It is meaningful only with region and scale context.
- A global FFT slope or mean GLCM contrast is insufficient to define a material or style.
- Lower resolution can merge distinct stroke patterns into the same smooth appearance. Upsampling does not restore the lost evidence.
- Learned metrics may better tolerate texture rearrangement, but that tolerance can also hide spatial mistakes important to illustration.
- Every feature report should include **mask coverage, valid crop count, scale and preprocessing**, plus “not measurable” when evidence is insufficient.

### Gaps

- No universal acceptance thresholds were found for these features on stylized illustration.
- The proposed scale grids, masks and feature combinations require validation against the project’s reference set.
- No inspected benchmark established that a scalar learned similarity score can isolate finish while ignoring palette, content, lighting and composition.
- Artifact diagnosis cannot establish the actual camera, codec or production pipeline from an arbitrary generated image.

## 3. How should measurements drive prompts and targeted corrections?

### Takeaway

Treat prompts and editing controls as **model-dependent actuators**, then calibrate their actual effects. Use deterministic postprocessing for simple finish changes; use masked regeneration or forward material/rendering controls when the requested change depends on form, highlights, transmission or coherent brush structure.

### Cited Findings

#### Existing controllability is useful but not axis-perfect

IP-Adapter combines image and text conditioning and documents image-to-image, inpainting and structural-conditioning examples. Its reference-conditioning scale affects reference consistency versus diversity. Its README also warns that default CLIP preprocessing centre-crops non-square images, potentially discarding peripheral information. **Confidence: high.** — Official repository: https://github.com/tencent-ailab/IP-Adapter

InstantStyle is direct prior art for reducing reference-content leakage and separating style/layout injection. Its authors identify particular SDXL attention blocks for style and layout and provide per-block and masked-conditioning examples. However, the repository describes style as including **colour, material and atmosphere**: this does not constitute a texture-only actuator. **Confidence: high** for documented mechanism; independent texture-only preservation remains conditional. — Official repository, introduced April 2024: https://github.com/instantX-research/InstantStyle

A relevant official example:

```python
scale = {
    "up": {"block_0": [0.0, 1.0, 0.0]},
}
pipeline.set_ip_adapter_scale(scale)
```

This demonstrates a control mechanism, not a portable setting for every architecture. — https://github.com/instantX-research/InstantStyle

Blender’s shader controls provide more explicit forward material parameters when a scene exists. Roughness, metallicity, coat, transmission, subsurface scattering and normals are separately configurable, although their visible effects still depend on scene lighting and geometry. — https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html

#### Proposed reference → features → controls loop

**Step 1 — Record appearance targets.**

For each relevant region, store:

- Human-readable description.
- Region/material identity.
- Texture scale relative to object and image.
- Absolute and relative band energy.
- Orientation/coherence distribution.
- Optional GLCM/LBP distributions.
- Grain amplitude/coarseness.
- Highlight/edge/glow descriptors.
- Confidence and known confounders.

Keep provenance claims separate.

**Step 2 — Translate into a narrow intervention.**

Example:

> Reference: clean contours, low fine-grain energy, moderate midscale directional marks, matte-looking broad highlights.

Possible correction:

> Preserve composition, palette, object proportions, contours, lighting direction and existing shadow layout. Reduce only fine speckled texture inside the jacket. Retain its larger directional marks and broad matte highlights. Do not smooth facial features or add glow.

Do not equate “reduce fine residual energy by 20%” with a universal prompt weight. The numerical target belongs to the evaluator, not automatically to the generator.

**Step 3 — Calibrate the actuator.**

Hold model/version, seed set, input, mask, output size, scheduler and other settings constant. Sweep one control:

- Prompt phrase or weight.
- Image-to-image strength.
- Adapter strength.
- Per-block adapter scale.
- Local denoising.
- Texture overlay opacity/scale.
- Shader parameter.

Measure target change **and collateral change** across several seeds. A seed fixes a comparison condition, not a guarantee of feature preservation.

**Step 4 — Optimize with protected-axis penalties.**

A proposed robust distance:

\[
d_{\rm target}
=\sum_i w_i
\frac{|f_i(x)-\operatorname{median}f_i(R)|}{s_i+\epsilon}.
\]

Here \(s_i\) is reference variability or empirically measured nuisance sensitivity—not an arbitrary scale chosen to make the score look good. With one reference, use a documented measurement-noise estimate or omit normalization.

A proposed selection objective:

\[
J(\theta)=
d_{\rm target}
+\lambda_c d_{\rm colour}
+\lambda_s d_{\rm structure}
+\lambda_l d_{\rm lighting}
+\lambda_p d_{\rm protected}.
\]

Prefer a Pareto comparison or explicit preservation gates over allowing a large target improvement to conceal unacceptable face/structure changes.

**Step 5 — Confirm at final export size.**

Re-measure after resizing and export. Retain the untouched input and change mask. Inspect both native detail and intended viewing size.

#### Correction tools and trade-offs

The table is an engineering recommendation. Documented capabilities are cited; exact preservation outcomes require local validation.

| Target mismatch | First intervention | Main trade-off / stop condition |
|---|---|---|
| Too much fine grain | Masked denoising or finest-band attenuation | Can erase dry-brush texture, pores, small accents |
| Too little fine grain | Controlled monochrome grain with explicit size and amplitude | Adds statistics, not convincing brush organization |
| Texture too coarse/fine | Change texture/stroke scale during generation, or rescale a separable texture layer | Whole-image resizing changes every axis |
| Overly sharp/haloed finish | Reduce sharpening; selectively attenuate affected high-frequency bands | Cannot reliably undo all prior sharpening |
| Smooth image should show form-following strokes | Masked image-to-image/inpainting with localized reference conditioning | May alter geometry, shading and colour |
| Strokes need coherent direction | Directional generation guidance or explicit surface-aware stroke construction | Global directional filtering can merely smear content |
| Plastic-looking highlights | Change material/light controls if a scene exists; otherwise localized highlight regeneration | Blur alone changes edges and texture without solving material cues |
| More impasto-like appearance | Generate coherent ridge/highlight/shadow appearance; use normal/displacement if a scene exists | A grain overlay does not create correct relief cues |
| Excessive glow | Reduce a separable glow layer or correct highlight surroundings locally | Flattened glow may overlap valid painted light |
| Missing transmission/refraction | Material control or localized generation with background/geometry constraints | Alpha blending alone is not refraction |
| Compression damage | Better original/export if available; conservative restoration otherwise | Restorers may invent plausible detail |
| Motion-like smear | Motion-aware restoration or local regeneration | Ordinary diffusion sharpening is not a general motion deblurrer |

darktable supports grain coarseness/strength, edge-aware diffusion, denoising, surface blur, bloom and multiscale sharpening. Its documentation explicitly notes resource cost, possible halos and noise amplification, resolution dependence, and the distinction from motion-blur inversion. — Grain: https://docs.darktable.org/usermanual/4.2/en/module-reference/processing-modules/grain/ ; diffusion/sharpening: https://docs.darktable.org/usermanual/development/en/module-reference/processing-modules/diffuse/

For a narrow overlay correction, a proposed form is:

\[
I'=I+\alpha M T,
\]

with zero-mean, explicitly band-limited texture \(T\). Declaring the colour space matters: adding to gamma-encoded RGB, linear RGB or a lightness channel produces different appearances. Feathering \(M\) avoids a hard seam but can leak texture outside the intended region. A fixed texture seed makes the edit reproducible.

#### Minimal versus advanced stack

| Stack/component | Intended use | CPU / AMD feasibility | License and maintenance evidence |
|---|---|---|---|
| **Minimal: NumPy/SciPy plus scikit-image** | Masks, filters, residuals, GLCM/LBP, structure tensor, FFT-derived descriptors | CPU-sufficient; no GPU required for these proposed measurements | scikit-image repository was not archived and reported a 2026-10-30 push. GitHub license metadata returned `NOASSERTION`; a complete license audit was **not** performed |
| **Optional PyWavelets** | Multiscale SWT descriptors | CPU; no CUDA dependency needed for these transforms | GitHub metadata identified MIT; not archived; push reported 2026-10-01 |
| **Optional darktable** | Interactive grain, denoise, bloom, multiscale diffusion/sharpening | CPU available; documentation strongly recommends OpenCL for expensive diffusion. Actual AMD/OpenCL setup not tested | Official docs inspected; release/license history not audited here |
| **Optional Blender** | Forward shader/render controls when scene geometry exists | CPU rendering possible; exact AMD/HIP compatibility not tested in this research | Official 4.5 LTS shader documentation inspected; implementation/license audit not performed |
| **Advanced DISTS** | Complementary full-reference perceptual quality assessment | Official example has CPU fallback. ROCm execution was not tested | Repository metadata: MIT, not archived, last reported push 2020-05-22. Legacy pretrained-model API warrants compatibility checking |
| **Advanced IP-Adapter / Diffusers** | Reference-conditioned generation/inpainting and structure-preserving workflows | Full generation is relatively heavy on CPU. AMD feasibility depends on an already configured compatible PyTorch/ROCm stack; not tested | IP-Adapter metadata: Apache-2.0, not archived, push 2024-06-28. Model/checkpoint licenses must be checked separately |
| **Advanced InstantStyle** | Per-block style/layout reference conditioning | CUDA-oriented examples; ROCm portability not established here | Not archived; push 2024-09-18. Repository API supplied no license identification; checkpoint disclaimer refers to IP-Adapter licenses. Code license remains unverified |
| **Research-only Materialist** | Prior-conditioned material/light estimation and physically based editing | README explicitly requires CUDA-compatible GPU hardware. **Not a validated drop-in choice for RX 7900 XTX** | Apache-2.0 metadata; not archived; push 2026-09-28. Dependencies and pretrained components require separate checks |

Repository metadata is a **point-in-time observation**, not a support guarantee or complete license audit. A recent push does not establish compatibility or responsiveness.

Primary repository links:  
scikit-image: https://github.com/scikit-image/scikit-image  
PyWavelets: https://github.com/PyWavelets/pywt  
DISTS: https://github.com/dingkeyan93/DISTS  
IP-Adapter: https://github.com/tencent-ailab/IP-Adapter  
InstantStyle: https://github.com/instantX-research/InstantStyle  
Materialist: https://github.com/lez-s/Materialist

**Minimal recommendation:** Start with CPU measurements and manual masks. Add SWT only if simple band energies are insufficient. Add pretrained perceptual features or generative editing only when their incremental value is demonstrated and required software/weights are already authorized and available.

#### Current prior art and remaining opportunity

The underlying components are established:

- Statistical multiscale texture representation and synthesis: Portilla–Simoncelli, 2000. — https://www.cns.nyu.edu/~lcv/texture/
- Learned feature-correlation texture representation: Gatys et al., 2015. — https://arxiv.org/abs/1505.07376
- Joint structure/texture perceptual assessment: DISTS, 2020. — https://github.com/dingkeyan93/DISTS
- Reference image conditioning: IP-Adapter, 2023. — https://github.com/tencent-ailab/IP-Adapter
- Reduced content leakage and layer-specific style/layout conditioning: InstantStyle, 2024. — https://github.com/instantX-research/InstantStyle
- Single-image material estimation and physically based editing: Materialist, 2025 preprint / 2026 IJCV. — https://arxiv.org/abs/2501.03717

The useful project opportunity is therefore **not inventing texture statistics or reference-conditioned editing**. It is validating a practical, uncertainty-aware bridge:

> region-specific reference appearance → explicit prompt/control intervention → measured target change → preservation checks on non-target axes.

### Inferences

- Postprocessing is preferable when the mismatch is a separable, low-amplitude finish effect such as grain or excessive fine detail.
- Generation/material controls are preferable when the change requires form-aware marks, coherent highlights, reflection, relief, scattering or transmission.
- Strong control of one image axis does not prove disentanglement. The workflow needs explicit collateral-change measurements.
- “More painterly” should become a small set of observable changes: stroke width, density, directional organization, edge breakup, pigment variation and highlight treatment.
- Preserve untouched pixels where practical, but also verify transition zones and material boundaries; masking alone does not guarantee semantic or perceptual preservation.
- Use human judgments to validate what the numerical axes actually mean for the reference corpus.

### Gaps

- No inspected source supplies a universal mapping from these measured features to prompt weights.
- No end-to-end system was validated here for texture-only correction across arbitrary illustration styles.
- Numerical ranges and intervention strengths require project-specific calibration.
- AMD execution of the learned/generative tools was not tested. Materialist explicitly specifies CUDA hardware.
- Some code-license metadata was missing or ambiguous; checkpoint/dependency licensing remains separate.
- The current-literature search was bounded, not an exhaustive survey of every 2026 material-editing or style-transfer paper.

**Research accounting:** 15 Kagi subscription search queries; one Context7 library resolution and two documentation queries; primary-page/source reads; public GitHub metadata checks; one GitHub code search that returned no results. No Perplexity, Kagi Assistant, Deep Research, model inference, installs, model downloads or uploads. Two source reads failed (publisher challenge and an obsolete documentation URL); accessible primary alternatives were used. GitHub license endpoints subsequently returned 403, leaving the stated license-verification gaps.
