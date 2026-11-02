# Color and palette: measuring and controlling chromatic style in collectible-card art

**Research cutoff:** 2026-10-31.  

**Scope:** Color representation, measurement, comparison, and correction. Luminance, material, and lighting appear only where necessary to explain chromatic ambiguity or editing side effects.

**Evidence convention:** “Established” describes supported definitions or published methods. “Proposed” identifies a practical measurement/control design, not a standard or validated aesthetic model. All acceptance thresholds require calibration to the reference collection and intended display size.

## 1. Which color coordinates and terms support precise, reproducible descriptions?

### Takeaway

Use color-managed pixels, explicitly distinguish nonlinear RGB from linear light, and describe stylized art primarily through **role-conditioned lightness, chroma, hue, and color distributions**. These coordinates permit reproducible measurements; they do not uniquely recover an illustration’s materials, illumination, intended warmth, or aesthetic harmony.

### Cited Findings

#### 1.1 RGB values require an encoding contract

An RGB triplet alone is insufficient: interpretation depends on primaries, white point, transfer function, and any embedded profile. W3C explicitly requires tagged images to be interpreted in their specified color space; its browser compatibility rule treats untagged images as sRGB. That compatibility rule is a defensible fallback for unknown web references, **not evidence that the original artwork was authored in sRGB**. — [W3C CSS Color 4, §§3.4–3.5, 2026-10-29](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#tagged-images)

Distinguish:

- **Assigning a profile:** changes the interpretation of existing numbers.
- **Converting between profiles:** transforms numbers to represent corresponding colors.
- **Rendering intent:** determines how source colors, white, and gamut are treated during reproduction.

ICC distinguishes absolute colorimetric reproduction, media-relative white mapping, and perceptual re-optimization. Different profile versions and intents can produce different results. Therefore “convert everything to sRGB” is incomplete unless the conversion policy is recorded. — [ICC sRGB profiles](https://registry.color.org/rgb-registry/srgbprofiles)

**Recommended analysis contract — proposed:**

1. Preserve the original file and metadata.
2. Record embedded ICC or equivalent color-space tags, bit depth, alpha, and whether the image is a screenshot.
3. Convert tagged inputs through a documented color-management path.
4. If untagged, record **“assumed sRGB”**, rather than silently treating that assumption as ground truth.
5. Specify rendering intent and black-point-compensation policy.
6. Retain sufficient precision during analysis and editing; quantize only for delivery.
7. Record the destination gamut separately from the analysis space.

This contract follows the interpretation and transformation distinctions in [W3C](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#tagged-images) and [ICC](https://registry.color.org/rgb-registry/srgbprofiles); the particular workflow is a proposal.

A screenshot can already contain display conversion, compositing, scaling, compression, and other processing. Its pixels characterize the **observed screenshot artifact**, not necessarily the source asset. Accordingly, an unknown-profile reference should carry a provenance limitation rather than false numerical precision. This is a methodological inference from the color-management requirements above.

#### 1.2 Linear and nonlinear processing answer different questions

For normalized, nonnegative sRGB encoded components \(c\in[0,1]\), the decoding function is:

\[
c_{\mathrm{lin}}=
\begin{cases}
c/12.92,&c\leq0.04045\\
((c+0.055)/1.055)^{2.4},&c>0.04045.
\end{cases}
\]

For linear-light sRGB:

\[
Y=0.2126R_{\mathrm{lin}}+0.7152G_{\mathrm{lin}}+0.0722B_{\mathrm{lin}}.
\]

Here \(Y\) is **relative luminance**, normalized to reference white—not an absolute measurement in cd/m² unless the display’s absolute output is known. W3C supplies the transfer functions and RGB/XYZ conversion matrices. — [W3C conversion code](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-conversion-code)

Use:

| Operation | Appropriate interpretation |
|---|---|
| Adding modeled light contributions or physically motivated exposure | Linear-light RGB/XYZ |
| Energy-based averaging or compositing | Linear-light representation with explicit alpha handling |
| Measuring hue, lightness, or chroma | A specified perceptual/model space |
| Artistic interpolation or grading | The operator’s documented space; not automatically linear RGB |
| Comparing what a delivered image looks like | Color-managed, display-referred image under stated viewing assumptions |

W3C distinguishes additive linear-light spaces from gamma-encoded spaces and separately discusses perceptual interpolation. Thus **“all image operations must be linear” is too broad**, just as averaging nonlinear RGB and calling it average emitted light is incorrect. — [W3C terminology](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#terminology), [interpolation spaces](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#interpolation-space)

**Double-decoding pitfall:** a conversion function that accepts encoded sRGB may already perform transfer-function decoding. Do not linearize the image first and then pass it to such a function. Conversely, Ottosson’s direct RGB→Oklab implementation explicitly takes **linear sRGB**. — [scikit-image color-conversion source](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/color/colorconv.py), [Ottosson’s Oklab implementation](https://bottosson.github.io/posts/oklab/)

#### 1.3 Terminology: distinguish the perceptual attribute from the coordinate

| Term | Precise meaning and appropriate usage | Common mistake |
|---|---|---|
| **Hue** | Chromatic direction; often represented as a cyclic angle in a specified model. | Treating degrees as comparable between HSV, CIELCh, and OKLCh. |
| **Luminance** | A photometric quantity; relative \(Y\) can be derived from characterized RGB. | Calling HSV value, HSL lightness, or Lab \(L^*\) luminance. |
| **Brightness** | Perceived intensity of an area. | Assuming it is identical to \(Y\). |
| **Lightness** | Perceived brightness relative to a similarly illuminated white/highly transmitting area. | Treating an arbitrary “brightness” slider as a lightness-preserving operator. |
| **Colourfulness** | How chromatic an area appears. | Assuming it is independent of viewing conditions or luminance. |
| **Chroma** | Colourfulness judged relative to an appropriate similarly illuminated reference. Lab/OKLab chroma are model coordinates intended to describe this dimension. | Using “chroma” and every software “saturation” channel interchangeably. |
| **Saturation** | In CIE terminology, colourfulness judged relative to the area’s own brightness. HSV saturation is a particular RGB-derived coordinate, not a complete perceptual measurement. | Treating equal HSV saturation as equal perceived chromatic intensity. |
| **Chromaticity** | A specification with intensity factored out, such as \(x,y\). | Treating chromaticity as perceptually uniform hue/chroma coordinates. |

Primary definitions: [CIE lightness, 2020](https://cie.co.at/eilvterm/17-22-063), [colourfulness](https://cie.co.at/eilvterm/17-22-072), [saturation](https://cie.co.at/eilvterm/17-22-073), [chroma](https://cie.co.at/eilvterm/17-22-074). Coordinate and hue-angle distinctions: [W3C color spaces](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#lab-colors), [hue](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#hue-syntax).

**Concrete HSV counterexample.** Encoded sRGB red \((1,0,0)\) and blue \((0,0,1)\) both have HSV \(V=1\) and \(S=1\). Their relative luminances are nevertheless approximately \(0.2126\) and \(0.0722\). Equal HSV value is not equal luminance; equal HSV saturation is not equal chroma. This example follows directly from the RGB/XYZ coefficients in [W3C](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-conversion-code) and the documented HSV conversion in [scikit-image](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/color/colorconv.py).

#### 1.4 Choosing CIELAB, Oklab, or CAM16

| Representation | Useful role | Required assumptions and limitations |
|---|---|---|
| **CIELAB / CIELCh** | Established lightness/chroma/hue reporting; CIEDE2000 comparisons; interoperability. | Requires reference white and observer convention. Uniformity is approximate; hue and chroma behavior are imperfect, especially in some blue regions. |
| **Oklab / OKLCh** | Simple SDR image analysis and editing; approximately perceptual coordinates; inexpensive CPU implementation. | Uses D65-referenced colorimetry. Does not explicitly model a particular surround or adaptation state. Uniformity is not exact. |
| **CAM16 appearance correlates** | Analysis where white, adaptation luminance, background, and surround are meaningfully specified. | More parameters do not imply more truth when viewing conditions are unknown. |
| **CAM16-UCS** | Appearance-conditioned approximately uniform coordinates \(J',a',b'\) and distances. | Depends on the CAM16 viewing-condition contract; coordinate scales differ from Oklab. |
| **HSV/HSL** | Familiar UI controls, legacy features, compatibility with published methods. | Not perceptually uniform and unsuitable as the sole basis for luminance/chroma claims. |
| **XYZ / linear RGB** | Colorimetric interchange, luminance calculation, physically motivated operations. | Euclidean coordinate distance is not a perceptual color-difference metric. |

Sources: [W3C Lab/Oklab](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#lab-colors), [Ottosson, 2020; updated 2021/2025](https://bottosson.github.io/posts/oklab/), [Li et al., CAM16, 2017](https://doi.org/10.1002/col.22131), [Colour CAM16-UCS documentation](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html).

**Important white-point implementation trap.** CSS Lab is D50-referenced; scikit-image’s `rgb2lab` defaults to D65/2°. Those outputs must not be mixed without an explicit white-point/adaptation convention. Moreover, the inspected scikit-image implementation is:

```python
return xyz2lab(rgb2xyz(rgb), illuminant, observer)
```

Changing its `illuminant` argument is therefore not equivalent to inserting a complete D65→D50 chromatic-adaptation transform. For an ICC/CSS-style D50 workflow, perform the appropriate adaptation explicitly or use a verified color-managed conversion path. — [scikit-image source](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/color/colorconv.py), [W3C conversion guidance and code](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-conversion-code)

**CAM16 scale trap.** Colour’s direct `XYZ_to_CAM16UCS` documentation takes XYZ on scale 1 and warns that `XYZ_w` must use the same scale. Its lower-level appearance-model examples use a different conventional scale. Pin the actual API and explicit parameters instead of copying numerical defaults across functions. — [Colour CAM16-UCS API](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html)

#### 1.5 Current-through-cutoff detail: Oklab distance variants

The **29 October 2026 W3C Candidate Recommendation Draft** includes:

\[
\Delta E_{\mathrm{OK}}
=\sqrt{\Delta L^2+\Delta a^2+\Delta b^2}
\]

and

\[
\Delta E_{\mathrm{OK2}}
=\sqrt{\Delta L^2+4\Delta a^2+4\Delta b^2}.
\]

It also describes \(\Delta E_{\mathrm{OKr2}}\), replacing \(L\) by a toe-adjusted lightness before applying the doubled chromatic coordinates. The draft explains that these are **additional distance metrics, not a redefinition of Oklab**. It reports improved agreement with CIEDE2000; this is not independent validation on collectible-card art. — [W3C color-difference code, §§20.3–20.5](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-difference-OK)

Consequences:

- Record the exact distance name, formula, and coordinate scale.
- Do not silently replace an existing metric during longitudinal evaluation.
- Do not transfer CIEDE2000 numerical thresholds to Oklab distances.
- Treat the October 2026 document as a **Candidate Recommendation Draft**, not a final W3C Recommendation. — [W3C document status](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#status)

#### 1.6 Warm/cool balance is not generally illuminant temperature

CIE defines correlated color temperature as the temperature of the Planckian radiator with chromaticity nearest the test source under a specified chromaticity-distance construction. It explicitly limits use when the test-source chromaticity is too far from the Planckian locus. CCT is expressed in kelvin. — [CIE CCT definition, 2020](https://cie.co.at/eilvterm/17-23-068)

An arbitrary illustration’s average color is not necessarily an illuminant estimate. An orange dragon, violet fog, blue frame, and green spell can produce a computable average without implying a physical light source of that chromaticity. Illuminant estimation is already underconstrained for photographs because surface reflectance and illumination are confounded; stylized paintings can also violate the assumed image-formation model. — [Gijsenij, Gevers & van de Weijer, 2011](https://staff.fnwi.uva.nl/th.gevers/pub/GeversTIP11.pdf)

Therefore distinguish:

- **Warm/cool palette:** an artistic description.
- **Warm highlight/cool shadow relationship:** a conditional chromatic pattern.
- **White-balance or temperature-slider setting:** an operation in a particular application.
- **Estimated illuminant CCT:** a physical-model estimate requiring appropriate evidence.
- **Known light-source CCT:** metadata or measured source information.

Do not report **“this illustration is 4300 K”** from its mean RGB. If a source estimate is genuinely warranted, report its chromaticity, method, model assumptions, and distance from the Planckian locus—not CCT alone. This recommendation follows [CIE’s domain restriction](https://cie.co.at/eilvterm/17-23-068) and the [color-constancy identifiability problem](https://staff.fnwi.uva.nl/th.gevers/pub/GeversTIP11.pdf).

#### 1.7 Color constancy and artistic grading have different objectives

Computational color constancy estimates or compensates illumination to recover a more illumination-independent representation. Published approaches rely on assumptions such as gray-world statistics, white patches, restricted gamuts, or learned priors. The survey documents that these assumptions can fail and that no discussed method is universal. — [Gijsenij et al., 2011](https://staff.fnwi.uva.nl/th.gevers/pub/GeversTIP11.pdf)

For reference-style matching, automatically neutralizing every image can remove precisely the deliberate cast that defines the style. A gray-world correction of a predominantly red illustration may “correct” the intended palette rather than an unwanted illuminant.

**Proposed policy:** preserve the delivered grade for style measurement. If a separate normalization experiment is useful, keep it as an additional branch and label it “normalized appearance under method X,” not recovered ground-truth object color. Basis: [color-constancy assumptions](https://staff.fnwi.uva.nl/th.gevers/pub/GeversTIP11.pdf).

### Inferences

#### Prompt-ready vocabulary

These are **proposed descriptions**, not promises that a text-to-image model implements the corresponding coordinates.

| Ambiguous instruction | More operational wording |
|---|---|
| “Make it more saturated.” | “Increase chroma in the character’s red cloth; preserve its lightness pattern, highlights, and the background palette.” |
| “Make the picture warmer.” | “Shift background midtones toward amber; retain blue-violet shadows and neutral metallic highlights.” |
| “Use a limited palette.” | “Use a narrow blue-green background hue family, a warm red-orange subject family, and a small gold accent; retain natural shading within each family.” |
| “Make the colors harmonious.” | “Use an analogous blue–cyan background family with one opposing orange accent; avoid introducing unrelated high-chroma magenta.” |
| “Make the subject pop.” | “Increase subject/background chromatic separation by reducing background chroma; preserve subject lightness and existing light direction.” |
| “Use brighter blue.” | “Increase blue-region lightness,” or “increase its chroma,” depending on the actual target. |
| “Match these five colors exactly.” | “Match these hue families and approximate role-specific area shares while preserving shading; use supplied swatches as midtone anchors, not as the only allowed pixel values.” |

Numeric specifications should accompany, rather than replace, ordinary language when the system accepts structured controls:

> **Illustrative target, not a standard:** background OKLCh chroma median reduced by 10% relative to the current image; preserve its lightness quantiles; retain the hero’s red-cloth hue family; do not alter gold accents.

For a model without numeric color conditioning, use such values as **evaluation targets**, not claims about prompt compliance.

#### Recommended coordinate policy

- **Baseline:** color-managed SDR inputs; Oklab/OKLCh for interpretable color features; relative \(Y\) as a separate diagnostic.
- **Compatibility branch:** CIELAB with explicitly declared white/observer and CIEDE2000.
- **Advanced branch:** CAM16-UCS only when the intended viewing conditions are specified or subjected to sensitivity analysis.
- **Legacy branch:** HSV features only when required by an existing method, with names that preserve their actual meaning.

These are engineering recommendations based on the documented scope and limitations of [Oklab](https://bottosson.github.io/posts/oklab/), [CIELAB/W3C](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#lab-colors), and [CAM16-UCS](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html).

### Gaps

- Unknown source profiles, screenshot processing, and display calibration cannot be reconstructed reliably from small RGB crops alone.
- No source checked establishes one perceptual color space as universally best for stylized collectible-card artwork.
- Actual viewing adaptation cannot be inferred simply by selecting CAM16 defaults.
- The mathematical glyphs describing the CIE CCT domain boundary were not fully exposed by text extraction. No numerical boundary is reproduced here.
- No claim is made that text prompting alone enforces exact hue, chroma, area, or lightness constraints.

## 2. Which measurements support valid generated/reference comparisons?

### Takeaway

A dominant palette is only a compact summary. Compare **weighted distributions within corresponding semantic roles**, retain joint lightness/chroma/hue information, and use reference-to-reference variability and mask/provenance sensitivity to calibrate uncertainty. Deterministic measurement does not establish perceptual validity, causal identifiability, or aesthetic merit.

### Cited Findings

#### 2.1 Dominant swatches, distributions, and spatial assignments are different objects

A palette can omit color proportions, within-family variation, and spatial assignment. Recent palette-conditioned diffusion research explicitly identifies non-uniqueness and instability: different distributions and images can share a palette. Its proposed histogram, entropy, and palette-distance controls address some of this ambiguity but remain non-spatial conditioning. — [Porat et al., *Palette Aligned Image Diffusion*, 2025](https://arxiv.org/html/2509.02000)

Classical harmonization work likewise shows that neighboring colors require spatially coherent treatment; independent hue reassignment can split a continuous region. Its graph-cut approach still cannot automatically know that disconnected regions belong to the same object. — [Cohen-Or et al., 2006](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf)

**Implication:** the same global color histogram can describe:

- a red hero on a blue background;
- a blue hero on a red background;
- a checkerboard of red and blue.

No histogram-only comparison distinguishes these assignments. Role conditioning and spatial summaries are therefore necessary for the stated control goal. This is a direct mathematical consequence of discarding pixel location, supported by the ambiguities described in [palette conditioning](https://arxiv.org/html/2509.02000) and [spatial harmonization](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf).

#### 2.2 Feature contract and notation

The table below is a **proposed reproducible feature set**, combining established coordinates/distances with explicitly defined project features.

Let:

- \(x_i=(L_i,a_i,b_i)\): Oklab color unless otherwise stated.
- \(C_i=\sqrt{a_i^2+b_i^2}\).
- \(h_i=\operatorname{atan2}(b_i,a_i)\bmod2\pi\).
- \(m_{ir}\in[0,1]\): membership of pixel \(i\) in role \(r\).
- \(w_i\): pixel weight, incorporating the chosen role/visibility policy.
- \(p_i=w_i/\sum_jw_j\).
- \(Q_q\): weighted quantile.
- \(d_\circ(\alpha,\beta)=|\operatorname{atan2}(\sin(\alpha-\beta),\cos(\alpha-\beta))|\).

Possible roles include **subject, background, principal accent, frame/UI**, and selected material regions. These role labels are a proposed annotation scheme, not standard categories.

**Shared preprocessing:**

1. Resolve the color-management contract.
2. Decide whether transparent pixels are excluded or composited over a specified background.
3. Use float arrays with explicitly normalized channel scales.
4. Exclude frame/text/UI from the art-only branch; optionally report a separate whole-card branch.
5. Preserve a native-resolution branch. If downsampling is used, document filtering and analysis scale.
6. Record masks, mask version, and boundary policy.
7. Use one coordinate convention across references and generated images.

The coordinate foundations are documented by [W3C](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-conversion-code) and [Ottosson](https://bottosson.github.io/posts/oklab/); role/mask policy is proposed.

#### 2.3 Feature table: formula, units, range, and preprocessing

| Feature | Formula / output | Unit and range | Preprocessing and interpretation |
|---|---|---|---|
| **Relative luminance** | \(Y=0.2126R_l+0.7152G_l+0.0722B_l\) | Relative; normally \([0,1]\) for bounded SDR sRGB | Linear-light sRGB only. Not cd/m² without calibration. [W3C](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-conversion-code) |
| **Lightness distribution** | \(Q_{0.1}(L),Q_{0.5}(L),Q_{0.9}(L)\), or an explicitly chosen quantile grid | Oklab \(L\), normally \([0,1]\) for SDR | Report by role. Quantile choices are analysis settings, not perceptual standards. [Oklab](https://bottosson.github.io/posts/oklab/) |
| **CIELAB lightness** | \(L^*=116f(Y/Y_n)-16\), with standard Lab \(f\) | \(L^*\), nominally \(0\)–\(100\) | Specify white and observer. Do not compare directly with Oklab \(L\). [W3C Lab](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#cie-lab) |
| **Chroma distribution** | \(C=\sqrt{a^2+b^2}\); weighted quantiles | Oklab chroma; \(\ge0\), no universal normalized maximum | Destination gamut bounds depend on \(L,h\). Not a percentage saturation. [W3C polar conversion](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#lab-to-lch) |
| **Hue** | \(h=\operatorname{atan2}(b,a)\bmod2\pi\) | Radians \([0,2\pi)\) or degrees \([0,360)\) | Undefined at \(C=0\); unstable near neutral. Specify color space. [W3C hue](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#hue-syntax) |
| **Circular hue difference** | \(d_\circ(h_1,h_2)\) | \(0\)–\(\pi\), or \(0\)–\(180^\circ\) | Never use ordinary absolute subtraction across the wrap boundary. Derived from cyclic hue. [W3C hue handling](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#hue-interpolation) |
| **Hue concentration** — proposed summary | \(R=|\sum_i\tilde p_i e^{ih_i}|\) | \([0,1]\) | Use chroma-qualified weights \(\tilde p_i\). \(R\approx0\) can mean broad hues **or opposed narrow modes**; it is not “no color.” Basis: [cyclic hue](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#hue-syntax). |
| **Neutral-area share** — proposed | \(\sum_i p_i\,1[C_i<\tau_C]\) | Fraction \([0,1]\) | \(\tau_C\) is calibration-dependent. Report sensitivity to it. Basis: [powerless hue](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#powerless). |
| **High-chroma area share** — proposed | \(\sum_i p_i\,1[C_i>\tau_H]\) | Fraction \([0,1]\) | \(\tau_H\) is project-specific; stratify by lightness where useful. Basis: [Oklab coordinates](https://bottosson.github.io/posts/oklab/). |
| **Dominant palette** | Centers/medoids \(c_k\) with masses \(\pi_k\) | Color coordinates + fractions summing to 1 | Fix space, \(k\), sampling, seed/initialization, and sorting/matching policy. A palette is not the full distribution. [Palette ambiguity](https://arxiv.org/html/2509.02000) |
| **Quantization residual** — proposed | \(E_K=\sum_i p_i\min_k d(x_i,c_k)\) | Units of selected ground distance; \(\ge0\) | Report with \(k\). Small residual can reflect flat/posterized art, not better art. Basis: [palette/distribution distinction](https://arxiv.org/html/2509.02000). |
| **Binned color entropy** | \(H=-\sum_b p_b\log_2p_b\) | Bits; \(0\)–\(\log_2B\) | Fix space, bin edges, sample count policy, and smoothing. Not a binning-independent measure of “richness.” [Palette Aligned Image Diffusion](https://arxiv.org/html/2509.02000) |
| **Role area share** — proposed | \(A_r=\sum_i m_{ir}/N\) | Fraction \([0,1]\) | Report separately from within-role color. Otherwise a larger red cloak can masquerade as a chroma change. Basis: [non-spatial ambiguity](https://arxiv.org/html/2509.02000). |
| **Conditional color distribution** — proposed | \(P(L,a,b\mid r)\), optionally \(P(a,b\mid r,L\text{-band})\) | Probability distribution | Use shared lightness-band definitions and role semantics; disclose missing roles. Basis: [CAM/coordinate distinctions](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html), [spatial limitations](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf). |
| **Warm/cool projection** — proposed | \(W_r=\sum_i p_i(a_i\cos\theta_w+b_i\sin\theta_w)\) | Oklab chromatic-coordinate units; signed | \(\theta_w\) is a declared artistic axis. Not kelvin; not a universal warmth metric. Basis: [Oklab](https://bottosson.github.io/posts/oklab/), [CCT limits](https://cie.co.at/eilvterm/17-23-068). |
| **Warm-area share** — proposed | Fraction in declared hue sector(s), with neutral exclusion | \([0,1]\) | Publish sectors and color space. Different definitions can disagree. Basis: [space-dependent hue angles](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#hue-syntax). |
| **Subject/background chromatic separation** — proposed | Distance between role distributions in \(a,b\), optionally conditional on \(L\) | Selected distance units; \(\ge0\) | Separates chromatic contrast from lightness contrast imperfectly; distribution overlap remains informative. Basis: [color-difference definitions](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-difference-code). |
| **Complementary deviation** — proposed | \(|\pi-d_\circ(h_1,h_2)|\) | Radians \(0\)–\(\pi\) | Measures opposition in the chosen wheel—not physical additive complementarity or aesthetic quality. [W3C hue](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#hue-syntax), [Schloss & Palmer](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf) |
| **Analogous-family spread** — proposed | Smallest circular arc containing a declared weighted mass | Degrees \(0\)–\(360\) | State retained mass and neutral handling. No universal “analogous enough” threshold. Basis: [hue templates](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf). |
| **Harmony-template residual** | Minimum weighted angular distance to allowed template sectors, optimizing orientation | Angular units; \(\ge0\) | Original method uses HSV saturation weighting. An OKLCh adaptation is a new variant, not the published score. [Cohen-Or et al.](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf) |
| **Palette spatial centroid** — proposed | \(\mu_k=\sum_iq_{ik}(u_i,v_i)/\sum_iq_{ik}\) | Normalized image coordinates, normally \([0,1]^2\) | Requires color assignments and coordinate normalization. Valid mainly for comparable layouts. Basis: [spatial harmonization](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf). |
| **Pre-mapping gamut violation** — proposed | Fraction whose destination linear-RGB components leave \([0,1]\), with stated numerical tolerance | \([0,1]\) | Measure before clipping/mapping. An encoded in-gamut file cannot reveal previously discarded colors. [W3C gamut mapping](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#gamut-mapping) |
| **Endpoint occupancy** — proposed | Fraction near encoded channel endpoints | \([0,1]\) | A diagnostic, **not proof of clipping**; intentional pure colors can hit endpoints. Basis: [clipping definition](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#GM-clip). |

**Low-chroma hue instability is structural, not merely software noise.** For \(h=\operatorname{atan2}(b,a)\),

\[
\nabla h=\left(-\frac{b}{C^2},\frac{a}{C^2}\right),
\qquad \|\nabla h\|=\frac1C.
\]

Thus fixed small coordinate perturbations can produce very large angular changes near neutral. This is a mathematical derivation from the polar-coordinate definition, consistent with W3C’s explicit “powerless hue” treatment. — [W3C polar coordinates and powerless components](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#powerless)

**Proposed handling:** retain a neutral bucket; exclude or smoothly downweight low-chroma pixels in hue-only statistics; disclose the weighting function and threshold; never assign gray a meaningful “red hue” merely because an implementation returns zero.

#### 2.4 Complementary/analogous scores are descriptive, not universal aesthetic laws

Cohen-Or et al. operationalize harmony using selected hue-wheel templates and optimize an image’s agreement with them. Their score is deterministic once the template family, hue representation, weights, and optimizer are fixed. The paper also reports semantic and spatial limitations, including colors collapsing together and disconnected object regions being treated differently. — [Cohen-Or et al., 2006](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf)

Schloss and Palmer empirically distinguish **pair preference, harmony, similarity, and preference for a figure against a ground**. Their experiments did not find an overall increase in pair harmony or pair preference for complementary hues; figural color preference could instead benefit from contrasting backgrounds. These findings contradict any simple rule that complementary pairs are universally more harmonious or preferred. — [Schloss & Palmer, 2011](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf)

Two meanings of “complement” must also be separated:

1. **Opposite hue coordinates:** approximately \(180^\circ\) apart in a selected wheel.
2. **Additive colorimetric complements:** colors whose appropriately weighted mixture is neutral relative to a specified white.

They are not interchangeable, and hue angles differ between spaces. — [W3C chromaticity, mixing, and hue definitions](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#terminology)

**Recommended reporting:** “fits an opposed-hue template,” “narrow analogous family,” or “subject/background hue opposition.” Avoid “objective harmony quality: 92%.”

#### 2.5 Color-difference families and their appropriate comparison units

**CIELAB \(\Delta E_{76}\):**

\[
\Delta E_{76}=\sqrt{(\Delta L^*)^2+(\Delta a^*)^2+(\Delta b^*)^2}.
\]

**CIE94 and CMC:** weight lightness/chroma/hue terms differently and require their particular parameter and reference/sample conventions. They should not be pooled with CIEDE2000 under the generic label “DeltaE.” Official library implementations expose these as distinct methods. — [Colour difference implementation](https://github.com/colour-science/colour/blob/develop/colour/difference/delta_e.py)

**CIEDE2000:**

\[
\Delta E_{00}=
\sqrt{
\left(\frac{\Delta L'}{k_LS_L}\right)^2+
\left(\frac{\Delta C'}{k_CS_C}\right)^2+
\left(\frac{\Delta H'}{k_HS_H}\right)^2+
R_T
\left(\frac{\Delta C'}{k_CS_C}\right)
\left(\frac{\Delta H'}{k_HS_H}\right)
}.
\]

Its primed quantities, hue branches, weighting functions, and interaction term matter. Sharma et al. provide supplementary test pairs specifically because implementations can be subtly incorrect; their page explicitly says its supplied implementation is **not an official CIE implementation**. — [Sharma, Wu & Dalal, 2005, implementation and test data](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/)

**Oklab distances:** report whether the formula is ordinary \(\Delta E_{\mathrm{OK}}\), doubled-chroma \(\Delta E_{\mathrm{OK2}}\), or toe-adjusted \(\Delta E_{\mathrm{OKr2}}\). — [W3C, October 2026](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#color-difference-OK)

**CAM16-UCS:** a Euclidean distance in the specified \(J',a',b'\) coordinates is meaningful only with the viewing-condition and scaling contract retained. — [Colour CAM16-UCS documentation](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html)

**Critical validity boundary:** pixelwise DeltaE requires meaningful correspondence. Applying it between independently composed card images penalizes different object placement as though it were a color error. Use it for registered recolors, swatch pairs, or corresponding material samples—not as a universal whole-image style metric. This is a methodological inference from the paired-color definition of [CIEDE2000](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/).

Do not import a universal rule such as **“\(\Delta E<2\) means the style matches.”** Patch discrimination, artwork-level similarity, and brand/material acceptance are different tasks. No source checked validates such a cutoff for this use case.

#### 2.6 Distribution distances

For weighted color distributions

\[
P=\sum_i p_i\delta_{x_i},\qquad
Q=\sum_j q_j\delta_{y_j},
\]

a useful transport cost is:

\[
W_1(P,Q)=
\min_{\gamma\ge0}
\sum_{ij}\gamma_{ij}d(x_i,y_j),
\]

subject to \(\sum_j\gamma_{ij}=p_i\) and \(\sum_i\gamma_{ij}=q_j\).

With a genuine metric ground cost and appropriate distributions, this is a Wasserstein-1 construction. With an arbitrary perceptual dissimilarity matrix, describe it more carefully as an **optimal-transport color cost** rather than assuming every metric property. POT supports exact EMD/transport and sliced-Wasserstein methods. — [POT official documentation](https://pythonot.github.io/)

Useful options:

| Comparison | Advantages | Limitations |
|---|---|---|
| **Weighted palette OT** | Compact; accounts for color masses and cross-color distances. | Depends on palette extraction and \(k\); loses within-cluster detail. |
| **Sampled full-color OT** | Retains more distribution information. | Pairwise costs can be expensive; sampling policy matters. |
| **Sliced Wasserstein** | Efficient projected comparisons; used in recent color-guided diffusion. | Finite projection directions introduce an approximation; fix directions/seed for reproducibility. |
| **Histogram JS divergence** | Bounded and easy to compare when bin definitions match. | Ordinary binwise comparison ignores that adjacent colors are more similar than distant ones. |
| **Marginal quantile differences** | Easy to interpret for \(L\) or \(C\). | Matching marginals does not match joint color relationships. |

Sources: [POT](https://pythonot.github.io/), [SW-Guidance official repository](https://github.com/alobashev/sw-guidance), [palette/histogram ambiguity](https://arxiv.org/html/2509.02000).

For base-2 logarithms,

\[
JS(P,Q)=\tfrac12 KL(P\|M)+\tfrac12 KL(Q\|M), \quad M=(P+Q)/2,
\]

lies in \([0,1]\); \(\sqrt{JS}\) is a different reported quantity. This is a mathematical property of the specified construction, not an artwork acceptance scale.

**POT API naming pitfall:** `ot.emd2(a, b, M)` returns the optimal transport **cost for the supplied matrix \(M\)**. The function name does not itself mean the result is squared perceptual DeltaE or Wasserstein-2. — [POT examples](https://pythonot.github.io/)

#### 2.7 Gamut mapping and clipping can change the axes being controlled

W3C distinguishes channel clipping, closest-color approaches, and chroma-reduction approaches. Channel clipping can change hue/lightness; chroma reduction is designed to preserve other coordinates more closely but still alters the intended chroma. Gamut boundaries depend on the destination space and color. — [W3C gamut mapping](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#gamut-mapping)

**Proposed evaluation rule:** report both:

1. Requested/intermediate colors and their out-of-gamut rate.
2. Final mapped delivery colors and achieved feature changes.

Otherwise a requested chroma increase can disappear at export while the analysis incorrectly reports success from pre-export coordinates.

### Inferences

#### 2.8 Determinism versus validity and identifiability: verdict

| Measurement | Deterministic? | Valid interpretation | Not identifiable from it |
|---|---|---|---|
| Profile conversion, RGB→XYZ/Lab/Oklab | Yes, conditional on profiles, implementation, intent, precision | Coordinates under the declared contract | Original appearance when provenance is unknown |
| Lightness/chroma quantiles | Yes for fixed pixels/masks | Distribution summaries in the chosen space | Material reflectance or intended lighting |
| Hue histogram | Yes after neutral policy is fixed | Chromatic-direction distribution | Meaningful hues of nearly neutral pixels |
| Extracted palette | Repeatable with controlled algorithm/seed | One compact quantization | Unique “true artistic palette” |
| OT/histogram distance | Yes, or reproducible approximation | Difference between declared distributions | Subject/background assignment when unconditioned |
| Warm/cool score | Yes once defined | Agreement with a declared chromatic axis/sector | Physical illuminant temperature |
| Harmony-template fit | Yes once model is fixed | Geometric template agreement | Universal beauty or preference |
| CCT computed from mean image color | Numerically repeatable | At most a mathematical result for that chosen chromaticity | Generally not the illustration’s illuminant |
| Role-conditioned comparison | Repeatable given masks | More specific comparison of corresponding areas | Correct semantics if masks are wrong |
| One small reference crop | Yes, as an artifact | What that crop contains | Full-card palette, collection variation, hidden regions |

The verdict follows the source distinctions above; the table is the proposed interpretation framework, not a published benchmark.

#### 2.9 Statistical comparison protocol

**Proposed protocol; no thresholds below are standards.**

1. **Separate the sampling units.**  
   Pixels describe a particular image; reference cards/images describe variation across the collection. A million pixels from one crop are not a million independent examples of the style.

2. **Define role correspondence before measuring.**  
   Compare background with background, principal subject with principal subject, and accent with accent. If one card lacks a corresponding role, report it as absent rather than matching an unrelated region.

3. **Compute per-image summaries first.**  
   Avoid pooling all reference pixels by default: a larger image or larger background would dominate. Preserve both image-level features and role area shares.

4. **Estimate reference variability.**  
   For feature \(f\), report per-reference values, a robust center, spread, and sample count. For distribution distance, report generated-to-reference distances alongside reference-to-reference distances.

5. **Use a reference baseline rather than an invented universal cutoff.**  
   A leave-one-reference-out distance provides an interpretable “how unusual is this among references?” diagnostic. With few references, show the individual values rather than implying a stable population percentile.

6. **Treat masks and provenance as uncertainty sources.**  
   Recompute with plausible boundary erosion/dilation, alternative manual masks, and defensible profile assumptions. Report whether the conclusion changes.

7. **Bootstrap at the appropriate level, if warranted.**  
   For collection-level conclusions, resample independent images—or higher-level groups when cards share an artist, set, or source. A pixel bootstrap alone does not capture between-card variation. With very few independent references, bootstrap intervals are weak evidence; label them exploratory.

8. **Evaluate generation variability.**  
   Repeat across multiple seeds and relevant prompts. For edit methods, use paired before/after images and preserve the generation settings. Report the distribution of target improvement and collateral drift.

9. **Keep a feature vector, not an unexplained scalar grade.**  
   At minimum, retain role-specific lightness, chroma, hue-family masses, color-distribution distance, area shares, and gamut diagnostics.

10. **Calibrate against human judgments on this artwork domain.**  
    Have reviewers compare controlled variations at the intended card display size. Use that calibration to choose practically meaningful tolerances.

This design responds to the non-uniqueness of [palette conditioning](https://arxiv.org/html/2509.02000), the contextual distinctions in [color preference/harmony](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf), and the parameter dependence of the documented color models. It has not been validated here as a statistical benchmark.

**Example report — illustrative structure, not measured results:**

> Background chroma is above the reference range under both tested masks. Subject hue-family masses overlap the references. Global OT distance improves after desaturating the background, but subject/background lightness separation changes slightly after gamut mapping. The evidence supports a background-chroma correction, not a global saturation reduction.

#### 2.10 Preserve joint and conditional information

Matching \(P(L)\), \(P(C)\), and \(P(h)\) independently is insufficient: one image can put orange in highlights and blue in shadows while another reverses that relationship.

**Proposed hierarchy:**

1. Global color distribution.
2. Role-conditioned distribution \(P(L,a,b\mid r)\).
3. Lightness-conditioned chromatic distributions \(P(a,b\mid r,L\text{-band})\).
4. Where needed, coarse spatial maps or corresponding material regions.

Use fixed or explicitly reference-defined lightness bands. Per-image percentile bands answer a different question: they compare each image’s relative shadows/midtones/highlights and can conceal absolute lightness differences.

#### 2.11 Tiny reference-crop pitfalls

- **Area bias:** a crop containing mostly a cloak cannot estimate whole-card red prevalence.
- **Missing roles:** a subject crop says little about background hue or subject/background separation.
- **Rare-accent omission:** tiny gold, eye, or spell accents can disappear under cropping/downsampling.
- **Compression and resampling:** small artifacts can disproportionately affect low-chroma hue and histogram entropy.
- **Spatial dependence:** adjacent pixels are strongly related; pixel count exaggerates evidential strength.
- **Palette instability:** several clusterings may fit a tiny crop similarly well.
- **UI contamination:** a frame, mana symbol, or text box can dominate an extracted palette.
- **Unavailable pixels:** masked, occluded, and cropped material colors cannot be recovered from the crop.
- **Scale effects:** downsampling creates mixtures and changes distributions even when filtering is technically appropriate.

**Proposed policy:** report native crop dimensions, art-only bounds, available roles, mask confidence, extraction settings, and sensitivity across plausible analysis scales. Do not use AI upscaling as a way to manufacture additional reference evidence.

### Gaps

- No reference images were provided or measured in this research pass; no feature values, fitted thresholds, or confidence intervals are claimed.
- No verified public benchmark found in this pass establishes perceptual acceptance thresholds for stylized collectible-card color matching.
- Role masks require validation; automatic segmentation accuracy on this specific art domain is unknown.
- Entropy, palette cardinality, warmth, and harmony-template residuals remain definition-dependent.
- Color-distribution agreement alone cannot establish material, illumination, or complete visual-style agreement.

## 3. Which correction methods and tools can change color while limiting collateral drift?

### Takeaway

For an existing image, begin with deterministic, masked color transforms and explicit invariants; use generative recoloring when the change requires semantic adaptation. Palette conditioning and recent region-aware diffusion are established prior art, but neither guarantees independent color axes, exact constraints, usable licensing, or AMD compatibility.

### Cited Findings

#### 3.1 Deterministic correction methods

**Hue/chroma editing in a perceptual space.** A simple role-masked operation is:

\[
L'_i=L_i,\qquad
(a'_i,b'_i)=g_i R(\theta_i)(a_i,b_i),
\]

where \(R\) is a 2D rotation, \(g_i\) controls chroma, and parameters are spatially masked or smoothly conditioned.

Before gamut mapping, this preserves numerical Oklab lightness exactly and exposes interpretable hue/chroma controls. It does **not** guarantee exact luminance preservation, unchanged perceived contrast, or unchanged material appearance. The distinction follows from the coordinate definitions and documented gamut/perceptual limitations. — [Ottosson](https://bottosson.github.io/posts/oklab/), [W3C gamut mapping](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#gamut-mapping)

**Palette-based recoloring.** Chang et al. provide established prior art for extracting a palette and recoloring an image by editing its palette. Their system combines an interface, palette extraction, and a color-transfer algorithm and was evaluated with a user study. This supports palette editing as a practical interaction model, not a guarantee of complete axis independence. — [Chang et al., SIGGRAPH 2015](https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/index.php)

**Spatially constrained harmonization.** Cohen-Or et al. allow selected regions to remain unchanged and use spatial coherence to avoid discontinuous hue reassignment. Their limitations explicitly include semantic separation and altered apparent contrast. — [Cohen-Or et al., 2006](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf)

**Statistical transfer and grading.** A generic per-channel mean/standard-deviation transform,

\[
z'_k=\mu_{t,k}+
\frac{\sigma_{t,k}}{\sigma_{s,k}+\epsilon}(z_k-\mu_{s,k}),
\]

is deterministic once its space, source/target region, and parameters are fixed. It matches selected marginal statistics, not joint distributions or semantic roles. It should not be described as “matching the reference palette completely.” Global transfer limitations and earlier statistical transfer work are discussed in [Palette Aligned Image Diffusion](https://arxiv.org/html/2509.02000).

For this project, applying such a transform only to chromatic coordinates or matched roles is a **proposed modification**, not the original historical algorithm.

#### 3.2 Current generative prior art

| Work | Verified contribution/status by cutoff | Relevance and boundary |
|---|---|---|
| **SW-Guidance**, Lobashev et al., 2025 | Official repository describes training-free color-conditional diffusion using differentiable sliced 1-Wasserstein guidance; records NeurIPS 2025 spotlight acceptance. | Shows distribution-based color guidance is prior art. Non-spatial distribution matching does not itself enforce role assignment or axis independence. [Official repo](https://github.com/alobashev/sw-guidance) |
| **Palette Aligned Image Diffusion**, Porat et al., 2025 | Palette-Adapter conditions an SDXL-based model using palettes/histograms, entropy, palette-distance controls, and negative histograms. | Directly relevant to interpretable controls. Authors acknowledge text/color tradeoffs and overlap between entropy and distance controls. Their examples show palette changes can change content. [Paper](https://arxiv.org/html/2509.02000) |
| **Exploring Palette based Color Guidance in Diffusion Models / Palette2Image**, ACM MM 2025 | Official implementation presents palette-based guidance for image colorization. | Useful prior art, but task scope is colorization rather than a guarantee of general color-only editing. README specifies one NVIDIA A100-80G. [Official repo](https://github.com/CyberAgentAILab/Palette2Image) |
| **ColourCrafter: Recolour What Matters**, 2026 | Official ECCV 2026 page and project describe RGB color-token fusion, masked region-aware editing, Lab-space loss, and ColourfulSet. Repository announces code release on 2026-07-03. | Strong evidence that continuous, local color controls and structural preservation are active prior art. “State of the art” remains an author claim, not an independent finding here. [ECCV page](https://eccv.ecva.net/virtual/2026/poster/4439), [project](https://yangyuqi317.github.io/ColourCrafter.github.io/), [repo](https://github.com/YangYuqi317/ColourCrafter) |
| **Inference-Time Loss-Guided Colour Preservation in Diffusion Sampling**, Ahuja, 2026 | Preprint submitted 2026-01-24; combines ROI inpainting, background-latent re-imposition, Lab/linear-RGB losses, and tail-error penalties. | Relevant design ideas, but limited evidence: inspected text lacks a convincing repeated-sample uncertainty analysis and reports substantial residual color errors. Treat as exploratory, not a validated solution. [Abstract](https://arxiv.org/abs/2601.17259), [full text](https://arxiv.org/html/2601.17259v1) |

**Source-quality warning:** some recent papers/project descriptions use “luminance” loosely for Lab’s \(L^*\). In this note, Lab \(L^*\) remains **lightness**; actual relative luminance is \(Y\). This correction follows the primary terminology and conversion definitions in [CIE](https://cie.co.at/eilvterm/17-22-063) and [W3C](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#terminology).

**Metric-optimization warning:** Palette Aligned Image Diffusion reports that the lowest palette distance need not coincide with the best perceived image quality and discusses severe quantization as a degenerate palette-matching outcome. Its benchmark is evidence of a tradeoff, not a universal ranking for card art. — [Paper, evaluation and limitations](https://arxiv.org/html/2509.02000)

#### 3.3 Official deterministic tools, licenses, maintenance, and hardware feasibility

Maintenance observations below are point-in-time public repository/release checks, not guarantees of future support. No packages were installed and no pipelines were executed.

| Tool | Relevant documented capability | License evidence | Maintenance observed by cutoff | CPU / AMD verdict |
|---|---|---|---|---|
| **Colour / colour-science** | RGB/XYZ, Oklab, Lab, CAM16/CAM16-UCS, color differences, adaptation. | BSD-3-Clause. [License](https://github.com/colour-science/colour/blob/develop/LICENSE) | v0.4.7 released 2025-12-06; public repository activity 2026-10-29. [Releases](https://github.com/colour-science/colour/releases), [repo metadata](https://api.github.com/repos/colour-science/colour) | NumPy-oriented analysis is CPU-feasible; no NVIDIA requirement for this measurement stack. GPU/ROCm acceleration not established here. |
| **scikit-image** | `rgb2lab`, HSV conversion, CIEDE2000 and other image-processing utilities. | Predominantly BSD-3-Clause, with file-specific BSD/MIT notices; GitHub’s generic license classification is insufficient. [Actual license](https://github.com/scikit-image/scikit-image/blob/main/LICENSE.txt) | v0.26.0 stable released 2025-12-20; v0.27.0rc1 on 2026-10-27. [Releases](https://github.com/scikit-image/scikit-image/releases) | CPU-feasible. Automatic profile interpretation is not supplied by `rgb2lab`; input must already be mapped appropriately. [Source](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/color/colorconv.py) |
| **Pillow / ImageCms** | ICC profile-to-profile transforms through its color-management interface. | MIT-CMU, not simply assume ordinary MIT from a badge. [License](https://github.com/python-pillow/Pillow/blob/main/LICENSE) | 13.0.0 released 2026-10-16; repository activity through 2026-10-31. [Releases](https://github.com/python-pillow/Pillow/releases), [metadata](https://api.github.com/repos/python-pillow/Pillow) | CPU-feasible. Verify supported image modes/precision for the actual path; this is not a blanket float/HDR pipeline endorsement. |
| **POT / Python Optimal Transport** | Exact EMD, transport plans/costs, sliced Wasserstein, multiple array backends. | MIT core; optional dependencies can add other obligations. Official docs specifically flag GPL-licensed `cvxopt` in optional installation. [Docs](https://pythonot.github.io/), [license](https://github.com/PythonOT/POT/blob/master/LICENSE) | 0.9.7.post1 released 2026-07-29; repository activity 2026-10-28. [Releases](https://github.com/PythonOT/POT/releases), [metadata](https://api.github.com/repos/PythonOT/POT) | CPU NumPy path is sufficient for sampled/quantized card-color analysis. Backend support does not mean every solver is GPU-native or AMD-tested. |
| **Sharma supplementary code/data** | CIEDE2000 reference test pairs; MATLAB and spreadsheet implementations. | Page permits personal/research use with citation; do not infer a general permissive commercial license. [Author page](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/) | Historical verification resource, not assessed as an actively maintained package. | Test data are hardware-independent. MATLAB runtime availability is separate. |

**Exact API checks from official sources:**

```python
# scikit-image: assumes appropriately mapped sRGB input
rgb2lab(rgb, illuminant="D65", observer="2", *, channel_axis=-1)

# CIEDE2000: Lab coordinates, explicit weighting convention
deltaE_ciede2000(lab1, lab2, kL=1, kC=1, kH=1, *, channel_axis=-1)
```

— [scikit-image official source](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/color/colorconv.py), [difference source](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/color/delta_e.py)

```python
# Pillow: do not rely on a guessed rendering intent or flags default
ImageCms.profileToProfile(
    im, inputProfile, outputProfile,
    renderingIntent=ImageCms.Intent.PERCEPTUAL,
    outputMode=None, inPlace=False,
    flags=ImageCms.Flags.NONE,
)
```

`inPlace=True` returns `None`; the normal path returns a new image. — [Pillow ImageCms documentation](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html)

**Documentation corroboration mattered:** one Context7-generated Pillow snippet disagreed about defaults and return behavior. The direct official documentation/source was used to resolve it. Likewise, license badges and page summaries were not accepted without checking actual files.

#### 3.4 Generative-code licensing and AMD feasibility

| Project | Checked licensing/availability | Practical feasibility verdict |
|---|---|---|
| **Palette2Image** | Actual code `LICENSE` is MIT. Checkpoint and dependency/base-model terms require separate review. [License](https://github.com/CyberAgentAILab/Palette2Image/blob/main/LICENSE) | README specifies A100-80G. No AMD or 24-GB feasibility claim is supported. [Repo](https://github.com/CyberAgentAILab/Palette2Image) |
| **SW-Guidance** | A fetched page summary claimed MIT, but repository-root inspection and GitHub’s license endpoint did **not** establish an actual license file. Treat licensing as unresolved, not verified MIT. [Repo contents](https://api.github.com/repos/alobashev/sw-guidance/contents), [license endpoint](https://api.github.com/repos/alobashev/sw-guidance/license) | Source exists for SD/SDXL variants. ROCm support and performance were not verified. |
| **Palette-Adapter paper** | Inspected paper says code/model release is planned; no verified runnable release/license was established in this pass. [Paper](https://arxiv.org/html/2509.02000) | Do not budget it as an immediately available local tool without a separate availability check. |
| **ColourCrafter** | README shows an MIT badge, but the root listing lacks the linked `LICENSE` file and the license endpoint returned 404. A placeholder model link is also present. Licensing/checkpoint readiness remain unresolved. [Repo](https://github.com/YangYuqi317/ColourCrafter), [contents](https://api.github.com/repos/YangYuqi317/ColourCrafter/contents), [license endpoint](https://api.github.com/repos/YangYuqi317/ColourCrafter/license) | README specifies Python 3.10, PyTorch 2.5.1, torchvision 0.20.1, diffusers 0.36.0, and FLUX.1-Kontext-dev checkpoints. No verified AMD support or 24-GB memory budget. |
| **Ahuja preprint** | No code URL/license established from inspected text. [Full text](https://arxiv.org/html/2601.17259v1) | Author reports Tesla T4 experiments, not AMD validation. Extra decode/backprop work increases inference cost. |

For an AMD workstation, the **deterministic measurement and grading stack does not require ROCm**. Generative research code requires a separate compatibility review of tensor operations, precision, attention implementations, dependencies, memory, and model terms. Neither a PyTorch dependency nor a CUDA-named device string alone establishes whether a project works correctly under ROCm.

#### 3.5 Source register: date, claim mapping, and confidence

Nineteen primary-source families were used because the requested scope spans standards, perception, algorithms, software, and current generative methods.

| ID | Source and date | Claims supported / confidence |
|---|---|---|
| **S01** | CIE S 017:2020 public terminology: [lightness](https://cie.co.at/eilvterm/17-22-063), [colourfulness](https://cie.co.at/eilvterm/17-22-072), [saturation](https://cie.co.at/eilvterm/17-22-073), [chroma](https://cie.co.at/eilvterm/17-22-074), [CCT](https://cie.co.at/eilvterm/17-23-068). Published 2020-12. | Authoritative definitions. **High**; CCT mathematical glyph extraction incomplete. |
| **S02** | [ICC sRGB profiles](https://registry.color.org/rgb-registry/srgbprofiles), accessed at cutoff. | Rendering intents, profile-version distinctions, profile licensing. **High**. |
| **S03** | [W3C CSS Color 4, 2026-10-29 snapshot](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/). | Encodings, transfer functions, white points, conversion code, hue, gamut mapping, DeltaE variants. **High for what the draft specifies**; draft status retained. |
| **S04** | [Ottosson, Oklab](https://bottosson.github.io/posts/oklab/), original 2020-12-23; matrices updated 2021-01-25; introduction added 2025. | Model design, implementation, intended uses and limitations. **High for author specification**; comparisons are not independent domain validation. |
| **S05** | [Li et al., 2017](https://doi.org/10.1002/col.22131), corroborated by [official Colour CAM16-UCS docs](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_CAM16UCS.html). | CAM16/CAT16/CAM16-UCS identity and implementation contract. **High for existence/API**; publisher full text blocked. |
| **S06** | [Sharma, Wu & Dalal, 2005](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/). | CIEDE2000 implementation issues, test pairs, usage terms. **High**. |
| **S07** | [Cohen-Or et al., Color Harmonization, 2006](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf). | HSV template model, spatial optimization, limitations. PDF text inspected. **High** for method; not universal harmony validity. |
| **S08** | [Schloss & Palmer, 2011](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf). | Distinction between harmony, preference, similarity, and figure-ground preference. PDF text inspected. **High within experiment scope**. |
| **S09** | [Chang et al., Palette-based Photo Recoloring, July 2015](https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/index.php). | Established interactive palette-recoloring prior art. **High** for project/task description. |
| **S10** | [Gijsenij, Gevers & van de Weijer, September 2011](https://staff.fnwi.uva.nl/th.gevers/pub/GeversTIP11.pdf). | Illuminant/reflectance ambiguity and color-constancy assumptions. PDF text inspected. **High**. |
| **S11** | [Colour official repository](https://github.com/colour-science/colour), docs, license and releases, checked 2026-10-31. | Algorithms, scales, license, maintenance. **High for inspected artifacts**. |
| **S12** | [scikit-image official repository](https://github.com/scikit-image/scikit-image), source/license/releases, checked 2026-10-31. | RGB/Lab API contract, DeltaE implementation, licensing. **High**. |
| **S13** | [Pillow official ImageCms docs](https://pillow.readthedocs.io/en/stable/reference/ImageCms.html), license/releases, checked 2026-10-31. | ICC transform behavior and package terms. **High**. |
| **S14** | [POT official docs](https://pythonot.github.io/), license/releases, checked 2026-10-31. | EMD/transport/sliced methods, backends, license. **High**. |
| **S15** | [Palette Aligned Image Diffusion, 2025](https://arxiv.org/html/2509.02000). | Palette ambiguity; histogram, entropy, distance and negative-color controls; limitations. **Moderate** for performance claims; strong evidence of prior art. |
| **S16** | [SW-Guidance official repository](https://github.com/alobashev/sw-guidance), 2025 publication/repository evidence. | Training-free sliced-Wasserstein guidance and release identity. **High** for existence; license/AMD readiness unresolved. |
| **S17** | [Palette2Image official repository](https://github.com/CyberAgentAILab/Palette2Image), ACM MM 2025. | Palette-guided colorization, actual MIT code license, stated hardware. **High for repository claims**; no independent reproduction. |
| **S18** | [ColourCrafter ECCV 2026 page](https://eccv.ecva.net/virtual/2026/poster/4439), [project](https://yangyuqi317.github.io/ColourCrafter.github.io/), [repository](https://github.com/YangYuqi317/ColourCrafter). | Region-aware continuous-color editing; code announcement and dependencies. **High** for publication/method existence; moderate for efficacy; licensing unresolved. |
| **S19** | [Ahuja, 2026-01-24 preprint](https://arxiv.org/abs/2601.17259), [full text](https://arxiv.org/html/2601.17259v1). | ROI guidance, background re-imposition, distribution-tail objectives. **Low-to-moderate** efficacy evidence; exploratory prior art. |

### Inferences

#### 3.6 Select corrections by the diagnosed mismatch

| Observed mismatch | Preferred first intervention — proposed | Preserve/check explicitly |
|---|---|---|
| Hue family wrong, lightness/chroma acceptable | Masked hue rotation or palette-anchor shift | Lightness distribution, chroma, gamut changes |
| Background too colorful | Background-only chroma reduction | Subject, accents, boundary appearance |
| Accent color occupies too much area | Recolor selected accent regions or edit placement | Merely reducing global saturation does not fix area share |
| Subject/background colors swapped | Role-conditioned recolor or masked generative edit | Global histogram can already look correct |
| Highlights have unwanted cast | Lightness-conditioned, role-aware chromatic edit | Material highlight behavior; avoid treating every bright pixel alike |
| Palette families correct but distributions too broad | Narrow selected chromatic distributions gradually | Avoid posterization and merged material identities |
| Palette too quantized | Restore within-family variation, not necessarily new hue families | Do not maximize histogram entropy indiscriminately |
| Entire image has an intentional-but-wrong grade | Controlled global grading, followed by role checks | Protected material colors and highlight neutrality |
| Needed color change requires new material/content interpretation | Region-aware generative recoloring | Structural and semantic drift; seed variability |

The intervention logic is based on the distinctions established by [palette recoloring](https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/index.php), [spatial harmonization](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf), and [current palette-conditioned generation](https://arxiv.org/html/2509.02000). It is not an empirically validated decision tree.

#### 3.7 “Without moving other axes” is a constrained goal, not an absolute promise

For a fixed image, a useful proposed optimization is:

\[
\min_\theta
D_{\mathrm{target}}(F_T(I_\theta),F_T(R))
+\lambda_LD_L(I_\theta,I_0)
+\lambda_PD_P(I_\theta,I_0)
+\lambda_GG(I_\theta),
\]

where:

- \(F_T\): targeted color features;
- \(D_L\): protected lightness or luminance drift;
- \(D_P\): protected-role color drift;
- \(G\): gamut violation/mapping penalty.

Specify whether the protected quantity is **\(Y\), Lab \(L^*\), Oklab \(L\), or a distribution statistic**. They are not interchangeable.

Important couplings:

- Holding Oklab \(L\) fixed does not guarantee exact \(Y\).
- Gamut mapping can reduce achieved chroma or move other coordinates.
- Simultaneous contrast can change appearance even when an object’s pixels remain unchanged.
- Recoloring specular highlights can alter perceived material.
- Global histogram matching can move unrelated materials together.
- Mask feathering changes boundary mixtures.
- Generative color conditioning can change content and composition.
- Strong distribution losses can flatten color variation or damage texture.

Sources establishing these limitations include [W3C gamut mapping](https://www.w3.org/TR/2026/CRD-css-color-4-20261029/#gamut-mapping), [Schloss & Palmer’s contextual effects](https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf), [Cohen-Or’s reported contrast/semantic limitations](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf), and [Palette-Adapter’s content/control tradeoffs](https://arxiv.org/html/2509.02000).

**Practical acceptance report — proposed:**

- Target feature improvement.
- Protected lightness/luminance drift.
- Protected-role chromatic drift.
- Boundary/halo observations.
- Pre/post-mapping gamut diagnostics.
- Human review at intended card size.
- Across-seed variability if generative editing was used.

Choose tolerances using reference variation and controlled reviewer calibration—not invented universal DeltaE, hue-angle, or percentage thresholds.

#### 3.8 Minimal stack

**Recommended first implementation, CPU-only:**

1. **Pillow/ImageCms** for input metadata and explicit ICC conversion.
2. **NumPy plus Colour or scikit-image** for conversion and deterministic features.
3. **Oklab/OKLCh** summaries with separate relative-\(Y\) diagnostics.
4. **Manual role masks** for a small reference collection.
5. **Weighted palettes and role histograms** with fixed extraction settings.
6. **POT**, only if transport comparisons materially improve on simpler summaries.
7. **Masked deterministic hue/chroma edits** and explicit gamut mapping.
8. **Versioned metric configuration and before/after reports.**

This stack addresses the current measurement/control goal without training a model or relying on unverified AMD generative compatibility.

#### 3.9 Advanced stack

Add only when the minimal stack demonstrates a need:

- Joint and lightness-conditioned role distributions.
- Multiple plausible masks and profile-assumption sensitivity.
- Sampled OT or fixed-projection sliced Wasserstein.
- Reference-group resampling and repeated-seed comparisons.
- Calibrated CAM16-UCS sensitivity under specified display/surround conditions.
- Palette-anchor editing with smooth spatial constraints.
- ROI inpainting with protected-background reinsertion.
- Distribution-aware color objectives and tail-error reporting.
- Local generative pipelines only after license, checkpoint, memory, and ROCm verification.

Avoid combining all of these into an opaque “style score.” Preserve diagnostic outputs so a correction can be attributed to a particular mismatch.

#### 3.10 Current prior-art verdict and useful opportunity

**Established prior art:**

- Perceptual color coordinates and color-difference formulas.
- Palette extraction and interactive palette recoloring.
- Hue-template fitting and spatially coherent harmonization.
- Color-distribution transfer and optimal transport.
- Palette/histogram-conditioned diffusion.
- Training-free distribution guidance.
- Region-aware continuous-color diffusion editing.

Therefore **“measure color and guide a generator with a palette” is not a novel research premise by itself**. Sources: [Chang 2015](https://gfx.cs.princeton.edu/pubs/Chang_2015_PPR/index.php), [Cohen-Or 2006](https://www.cs.tau.ac.il/~dcor/articles/2006/Color-Harmonization.pdf), [SW-Guidance](https://github.com/alobashev/sw-guidance), [Palette-Adapter](https://arxiv.org/html/2509.02000), [ColourCrafter 2026](https://eccv.ecva.net/virtual/2026/poster/4439).

**Potentially useful integration opportunity—not established novelty:**

A provenance-aware, role-conditioned workflow that translates reference measurements into precise editing language, chooses a narrow correction, and reports **achieved target change versus protected-axis drift**, especially under tiny-crop uncertainty.

The practical value would lie in calibration, interpretability, reproducibility, and domain-specific evaluation—not in claiming that color harmony or palette matching has become an objective aesthetic law.

### Gaps

#### Verification and evidence limitations

- No tools or generative models were installed, executed, benchmarked, or reproduced.
- No AMD/ROCm generative compatibility or memory feasibility was verified.
- No private assets or reference crops were uploaded or analyzed.
- CAM16 publisher full text was blocked; official implementation documentation corroborated model/API facts, not independent perceptual performance.
- Two attempted historical PDF reads failed certificate validation; their inaccessible contents were not used as inspected evidence.
- Some fetched page summaries overstated license certainty. Actual license files/API evidence were checked, and unresolved cases remain unresolved.
- Recent generative papers’ performance claims are not validated for collectible-card art.
- Newer source availability was checked through the cutoff, but the investigation is not an exhaustive literature census.
- Tiny-crop statistical identifiability remains a limitation even with perfect deterministic code.

#### Research spend and artifact handoff

- **21 Kagi search queries across five batches.**
- **Six Context7 CLI operations:** three library resolutions and three documentation queries.
- **One GitHub code-pattern search.**
- Direct reads of public standards, papers, official documentation, repository metadata, license files, and release records.
- **Nineteen primary-source families**, with associated official code/docs.
- **No Perplexity, Deep Research, Kagi Assistant, model downloads, package installs, or external agent dispatches.**
