# Rhythm, pattern, and repetition

Research: **10 primary-source families**, including 2025–2026 prior art; 14 Kagi search queries, 6 Context7 lookups, 1 GitHub code search, direct documentation/repository checks. No Perplexity, Kagi Assistant, installations, model downloads, image uploads, or project modifications. Algorithms were not executed on illustrations.

Scope: still stylized illustrations and object cards; evidence checked through **2026-10-31**. All linked sources accessed **2026-10-31**.

This direction concerns **recurrence and its variation**: what repeats, how often, at which spatial intervals, under which transformations, and where an established rule is interrupted. It is not a substitute for general composition, texture, or emotional interpretation.

## 1. What does visual rhythm mean, and which existing methods actually measure its components?

### Takeaway

Treat visual rhythm as a **multicomponent description**, not a universal scalar. Existing tools measure periodicity, motif locations, counts, orientations, symmetry, and deviations; none of the inspected sources establishes a validated, end-to-end “visual tempo” score and corrective editor for stylized object cards.

### Cited Findings

#### Primary-source register and evidence boundaries

**[S1] Getty Museum — design vocabulary, not a numerical perceptual model.**

Getty defines pattern as repetition of an object or symbol and rhythm as repeated design elements producing “a feeling of organized movement.” Its educational text explicitly associates rhythm with mood and musical/dance analogy. This supports the vocabulary, **not an objective conversion from image frequency to emotional speed**. — [Getty, Principles of Design](https://www.getty.edu/education/teachers/building_lessons/principles_design.pdf)

Relevant quotations:

> “Pattern is the repeating of an object or symbol all over the work of art.”

> “Rhythm is created when one or more elements of design are used repeatedly to create a feeling of organized movement.”

**[S2] SciPy — deterministic Fourier and correlation foundations.**

Official documentation describes Fourier analysis as expressing a function through periodic components, supplies 2-D FFT implementations, explains discrete-frequency coordinates, and warns about the periodic extension implicit in the DFT. Its spectral-analysis documentation explains leakage and the trade-off in windowing: reduced sidelobes at the cost of a wider main lobe. — [FFT tutorial](https://docs.scipy.org/doc/scipy/tutorial/fft.html), [spectral analysis](https://docs.scipy.org/doc/scipy/tutorial/signal.html#tutorial-spectralanalysis)

Practical tools: `scipy.fft.fft2`, `ifft2`, `fftfreq`, correlation/convolution routines, windows, spatial distances, optimization.

License: BSD-3-Clause. Repository metadata showed a nonarchived repository with a push on 2026-10-31; this is an activity observation, not a maintenance guarantee. — [Official repository/API metadata](https://api.github.com/repos/scipy/scipy)

**[S3] scikit-image — deterministic motif extraction and measurement.**

`match_template` uses normalized cross-correlation. The official example explicitly says multiple occurrences require proper peak finding; the default response coordinates identify the template’s top-left origin, not necessarily its center. — [Official template-matching example](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_template.html)

Official tests demonstrate an actual repeated-target workflow:

```python
result = match_template(image, target)
positions = peak_local_max(result, min_distance=delta)
```

— [Official test implementation](https://github.com/scikit-image/scikit-image/blob/main/tests/skimage/feature/test_template.py)

`regionprops`/`regionprops_table` expose centroid, area, equivalent diameter, orientation, eccentricity, and other region descriptors. Orientation is the major-axis angle relative to the row axis, in radians; pixel spacing affects geometric quantities. — [Official implementation/docstrings](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/measure/_regionprops.py)

License: predominantly BSD-3-Clause, with documented file-level BSD-2-Clause/MIT exceptions. Do not interpret GitHub’s repository-wide `NOASSERTION` classification as “unlicensed”; the official license documentation is explicit. — [License documentation](https://scikit-image.org/docs/stable/license.html)

Maintenance snapshot: stable documentation identified version 0.26.0; repository metadata showed activity on 2026-10-30. Context7 also returned development-tree `_skimage2` paths: **pin and check installed versions rather than copying development import paths**. — [Repository metadata](https://api.github.com/repos/scikit-image/scikit-image)

**[S4] PyWavelets — multiscale/local recurrence analysis.**

The official CWT documentation distinguishes Fourier’s global frequency description from wavelets’ localized scale/frequency description. `pywt.cwt` is **one-dimensional**: for this application, use it on an explicitly defined spatial profile or path, not as an unspecified 2-D image-rhythm detector. It documents low-scale aliasing, sensitivity to wavelet parameters, and known CWT implementation issues. — [CWT documentation](https://pywavelets.readthedocs.io/en/latest/ref/cwt.html)

The stationary wavelet transform avoids decimation and is shift-invariant at the cost of redundant coefficients. The documentation specifies padding/divisibility requirements and conditions for energy conservation: orthogonal wavelet, `norm=True`, and `trim_approx=True`. — [Stationary wavelet documentation](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html)

License: MIT. Repository metadata showed activity on 2026-10-01. — [License](https://github.com/PyWavelets/pywt/blob/main/LICENSE), [metadata](https://api.github.com/repos/PyWavelets/pywt)

**[S5] spatstat — spatial point-pattern analysis with boundary-aware inference.**

The maintained R toolbox includes nearest-neighbor statistics, K-functions, pair correlation, marked/multitype patterns, simulations, and simulation envelopes. CRAN listed version 3.6-3, published 2026-09-28, under GPL ≥2. The umbrella package’s “NeedsCompilation: no” does **not** establish that all dependencies avoid compiled code. — [Official CRAN package page](https://cran.r-project.org/package=spatstat)

`Kest` documents an edge-corrected estimator, stationarity assumptions, and small-sample limitations. It warns that bias may be appreciable below 15 points and recommends limiting radius for rectangular windows. — [K-function documentation](https://search.r-project.org/CRAN/refmans/spatstat.explore/html/Kest.html)

`pcf` estimates the pair correlation function by kernel smoothing, documents bandwidth and edge correction, and distinguishes inhibition from clustering. — [Pair-correlation documentation](https://search.r-project.org/CRAN/refmans/spatstat.explore/html/pcf.ppp.html)

The inspected function-manual pages identify an older package version than the current CRAN umbrella page. The mathematical definitions are usable; verify current parameters before implementation.

**[S6] Qu et al., 2025 — actual repeated-tile detection prior art.**

*Efficient and Effective Detection of Repeated Pattern from Fronto-Parallel Images with Unknown Visual Contents* combines pretrained CNN features, initial repeat-size proposals, and optimization. The stated target includes fronto-parallel textile and nontextile images. This is genuine prior art for discovering a repeat unit, **not evidence of general stylized-card motif understanding**. — [Author repository and paper citation](https://github.com/ZoeQU/Efficient-and-Effective-Detection-of-Repeated-Patterns), [paper](https://www.mdpi.com/2624-6120/6/1/4)

The README states “All rights reserved by authors”; no repository license was detected in GitHub metadata. Therefore do not assume commercial reuse permission. Model weights are linked separately; none were downloaded. Repository activity was observed through 2026-03-29. — [Repository](https://github.com/ZoeQU/Efficient-and-Effective-Detection-of-Repeated-Patterns), [metadata](https://api.github.com/repos/ZoeQU/Efficient-and-Effective-Detection-of-Repeated-Patterns)

**[S7] Amini-Naieni and Zisserman — CountGD++, CVPR 2026.**

CountGD++ extends open-world counting with positive and negative text/visual prompts, external exemplars, and automatically obtained pseudo-exemplars. The paper’s second version is dated 2026-05-30; the official repository identifies CVPR 2026. — [Paper](https://arxiv.org/abs/2512.23351), [official repository](https://github.com/niki-amini-naieni/CountGDPlusPlus)

This is useful for estimating **which instances belong to a motif class**, especially where “count leaves, not sparkles” matters. Counting is not itself a spacing, orientation, or rhythm score. — [Paper](https://arxiv.org/abs/2512.23351)

The documented setup requires CUDA tooling, GroundingDINO custom operations, and detectron2. It also notes that pseudo-exemplars and adaptive cropping are not implemented in the demonstration interface. **No supported AMD/ROCm or CPU deployment was verified.** — [Official setup and demo limitations](https://github.com/niki-amini-naieni/CountGDPlusPlus)

Repository code license: MIT; upstream components and weights still require their own review. Repository activity was observed on 2026-10-27. — [License](https://github.com/niki-amini-naieni/CountGDPlusPlus/blob/main/LICENSE), [metadata](https://api.github.com/repos/niki-amini-naieni/CountGDPlusPlus)

**[S8] Yang et al., 2025 — CLIPSym learned symmetry detection.**

CLIPSym combines CLIP image/language encoders with a rotation-equivariant decoder to detect reflection and rotational symmetry. The paper reports experiments on DENDI, SDRW, and LDRS. These are symmetry results, not a validated metric of repetition or stylized-card tempo. — [Paper](https://arxiv.org/abs/2508.14197)

The official repository provides reproduction/training instructions. No permissive license was detected in repository metadata; AMD/CPU execution, pretrained ease of use, and production maintenance were not established. The observed last push was 2025-07-30. — [Repository](https://github.com/timyoung2333/CLIPSym), [metadata](https://api.github.com/repos/timyoung2333/CLIPSym)

**[S9] Zhang et al., ICCV 2023 — ControlNet spatial conditioning.**

The official implementation supports conditioning on edges, scribbles, segmentation, depth, and other spatial inputs. This supplies an existing route from a deliberately drawn repeat layout to image generation; it does not guarantee exact count, exact spacing, or unchanged protected pixels. — [Official repository/paper link](https://github.com/lllyasviel/ControlNet)

Code license: Apache-2.0; base models and weights have separate terms. The inspected original repository’s last push was 2024-02-25, so distinguish foundational code from an actively maintained current integration. AMD compatibility and performance were not tested. — [License](https://github.com/lllyasviel/ControlNet/blob/main/LICENSE), [metadata](https://api.github.com/repos/lllyasviel/ControlNet)

**[S10] W3C SVG — deterministic repeat control already exists.**

SVG patterns repeat a graphical tile at fixed x/y intervals. `patternUnits`, `patternContentUnits`, `patternTransform`, tile origin, width, and height explicitly control coordinates, scale, placement, and transformation. This is a standards-based constructive solution when exact regularity matters; no learned model is required to create the layout. — [SVG 2, patterns](https://www.w3.org/TR/SVG2/pservers.html#Patterns)

This is a specification, not a particular renderer’s license or compatibility guarantee.

### Inferences

The following are **proposed operational definitions**, not claims that art terminology has one scientifically standardized numerical implementation.

#### Three evidence levels

1. **Direct deterministic measurements:** distances, counts from agreed instance masks, occupancy, cross-correlation, Fourier spectra, geometric symmetry residuals.
2. **Estimated semantic measurements:** learned detection, segmentation, motif grouping, correspondence, or symmetry. Downstream arithmetic may be exact, but its inputs remain uncertain.
3. **Interpretations:** “calm,” “playful,” “busy,” “stately,” “hurried,” or “syncopated.” These may describe an intended response; they are not definitive objective scalars.

A measurement record should preserve this distinction. For example:

> “Median motif pitch = 0.12 card short-sides, spacing CV = 0.08, one omitted slot” is measurable.  
> “A calm, slow rhythm” is an interpretation that may be supported by those choices, not proved by them.

#### Operational rhythm vocabulary

| Vocabulary | Proposed observable structure |
|---|---|
| Regular | Repeated motif class with nearly constant pitch, scale, and transformation |
| Irregular | Dispersion in pitch, scale, orientation, or motif identity; specify which |
| Alternating | Ordered ABAB, ABCABC, or another declared mark sequence |
| Progressive | Systematic change in size, spacing, orientation, or density along a declared coordinate |
| Flowing | Recurrence along a curve, often with orientation related to its tangent |
| Broken/interrupted | Local deviation from an otherwise supported repeat rule |
| Clustered | Locally dense groups separated by larger gaps |
| Radial | Motif centers arranged by angular/radial relationships about a declared center |

Do not classify a progression as accidental irregularity merely because its raw spacing variance is high. Fit the intended progression first and inspect its **residual variation**.

#### Internal image rhythm versus set rhythm

- **Internal:** recurrence within one background, border, object surface, or supporting decoration.
- **Across a set:** consistency or variation in each card’s recurrence descriptor.
- **Across an ordered set:** ABAB card classes, gradual density changes, or deliberate exceptional cards.
- An unordered collection has a distribution of descriptors, **not an intrinsic temporal order**.
- Do not estimate card-set rhythm by taking the FFT of a contact sheet: the layout grid and card borders introduce their own strong periodicity.

### Gaps

- No inspected source supplies a validated universal scalar for emotional visual tempo in still stylized illustrations.
- No integrated reference → prompt → measurement → isolated-correction tool was established for this specific application.
- No stylized-object-card benchmark validating CountGD++, CLIPSym, or the repeated-tile detector was found in this bounded search.
- These are **bounded negative findings**, not proof that no relevant product or paper exists.
- Renderer behavior, local package availability, CPU timing, and AMD/ROCm compatibility were not tested.

## 2. Which features, formulas, normalizations, comparison metrics, and uncertainty checks are defensible?

### Takeaway

Use a **region-conditioned feature vector** combining motif-instance geometry with image-domain periodicity. Report units, masks, semantic definitions, sample size, and sensitivity; a numerical match without those conditions is not a reliable style match.

### Cited Findings

- Fourier methods provide periodic components and spatial-frequency coordinates, but finite windows, periodic extension, leakage, and sampling constrain interpretation. — [SciPy FFT](https://docs.scipy.org/doc/scipy/tutorial/fft.html), [spectral analysis](https://docs.scipy.org/doc/scipy/tutorial/signal.html#tutorial-spectralanalysis)
- Normalized template matching and labeled-region descriptors are existing deterministic building blocks for detecting and measuring repeat instances. — [scikit-image example](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_template.html), [region-property implementation](https://github.com/scikit-image/scikit-image/blob/main/src/_skimage2/measure/_regionprops.py)
- Spatial K and pair-correlation statistics require explicit observation windows and edge correction; homogeneous estimators assume stationarity. — [Kest](https://search.r-project.org/CRAN/refmans/spatstat.explore/html/Kest.html), [pcf](https://search.r-project.org/CRAN/refmans/spatstat.explore/html/pcf.ppp.html)
- Wavelet parameters, insufficient sampling, boundary effects, and coefficient normalization affect multiscale comparisons. — [PyWavelets CWT](https://pywavelets.readthedocs.io/en/latest/ref/cwt.html), [SWT](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html)

### Inferences

Everything below is an **engineering proposal grounded in those methods**, not a validated illustration-style standard.

#### A. Define the measurement contract first

For image width \(W\), height \(H\), choose isotropic scale

\[
L=\min(W,H).
\]

Use coordinates \(\tilde{x}=x/L,\ \tilde{y}=y/L\), optionally translated to a declared origin.

- Lengths: pixels and **card-short-side units**.
- Areas: pixels² and \(L^2\)-normalized area.
- Frequencies: cycles/pixel or cycles/card-short-side.
- Angles: radians internally; degrees for artist-facing reports.
- Counts: instances, with the motif definition attached.

Avoid independently normalizing x by W and y by H when measuring Euclidean distances: that changes geometry on nonsquare cards.

Declare:

- Region: whole card, background, border, object surface, supporting ornament.
- Region mask \(R\), area \(A_R\).
- Motif class and instance rule: whole flowers, petals, dots, highlights, etc.
- Inclusion rule: centroid inside region, fully contained instance, or another fixed convention.
- Handling of overlap, occlusion, clipping, and partial motifs.
- View: final display resolution and, if useful, original resolution.
- Whether measurements are card-relative or object-relative.

**Do not pool leaves, sparkles, and brush marks solely because they share an apparent diameter.** Geometry is conditional on what counts as one motif.

Object-relative normalization can be useful, but distinguish:

- Larger motifs relative to the card.
- Larger motifs relative to the central object.
- A larger central object with unchanged card-space decoration.

These are different changes.

#### B. Motif counts, size, density, and coverage

For \(n\) accepted instances:

\[
\rho = \frac{n}{A_R},
\qquad
\tilde{\rho}=\frac{nL^2}{A_R}.
\]

Units: instances/pixel² or instances/card-short-side².

For instance area \(a_i\), equivalent diameter:

\[
d_i = 2\sqrt{a_i/\pi},
\qquad
\tilde d_i=d_i/L.
\]

Use median and quantiles of \(d_i\), not only the mean.

Coverage:

\[
\phi=\frac{\left|\bigcup_i M_i\cap R\right|}{A_R}.
\]

Use **union area**, not the sum of mask areas, when instances overlap.

Count, density, coverage, and motif scale are not interchangeable. Enlarging motifs raises coverage without increasing count; shrinking the eligible background around a larger object raises conditional density without adding decoration.

#### C. Spacing and its regularity

For centroids \(p_i\):

\[
r_i=\min_{j\ne i}\|p_i-p_j\|.
\]

Report median nearest-neighbor distance, quantiles, and normalized values \(r_i/L\).

For a declared ordered row/path with arc positions \(s_i\):

\[
\Delta_i=s_{i+1}-s_i,
\qquad
CV_\Delta=\frac{\operatorname{sd}(\Delta_i)}
{\operatorname{mean}(\Delta_i)}.
\]

Specify the standard-deviation convention and number of intervals.

Also report pitch relative to motif size:

\[
q=\frac{\operatorname{median}(\Delta_i)}
{\operatorname{median}(d_i)}.
\]

**Center-to-center pitch is not edge-to-edge gap.** If motif size changes, constant pitch can produce changing visible gaps. For complex silhouettes, measure boundary separation or a clearly defined projected extent rather than assuming circles.

Limitations:

- Nearest-neighbor CV does not establish a lattice.
- Different arrangements can share identical nearest-neighbor distances.
- With fewer than two motifs, nearest-neighbor spacing is undefined.
- With very few intervals, CV is descriptive and unstable, not a confident population estimate.
- Border points have missing neighbors outside the observation region.

#### D. Orientation and symmetry

For axial motif orientations \(\theta_i\), where a 180° turn is equivalent:

\[
R_2=\left|\frac1n\sum_i e^{2\mathrm{i}\theta_i}\right|,
\qquad
V_2=1-R_2.
\]

- \(R_2\) near 1: aligned axes.
- \(V_2\): dimensionless axial dispersion.
- Use \(e^{\mathrm{i}\theta}\) for genuinely directed orientations, such as arrowheads.
- Near-circular motifs have poorly defined major-axis orientation; exclude or flag them.

For a declared transformation \(T\), a mask-based geometric symmetry descriptor can be

\[
S_T=\operatorname{IoU}(M,T(M)).
\]

Declare transformation center/axis and interpolation. For instance sets, use correspondence residuals instead of pixel IoU if appearance varies.

**Symmetry is not repetition:** a single bilateral object may be highly symmetric but contain no repeated ornament sequence. Conversely, an irregular row of repeated leaves may lack global symmetry.

#### E. Alternation and progression

After explicitly ordering instances, compare class marks \(c_i\) with a proposed period-\(k\) sequence \(t\):

\[
A_k=\max_{\text{phase}}\frac1n
\sum_i \mathbf{1}\{c_i=t_{(i+\text{phase})\bmod k}\}.
\]

Report the chosen sequence and phase. A balanced count of A and B does not establish ABAB alternation.

For size progression:

\[
\log d_i=\alpha+\beta t_i+\epsilon_i,
\quad t_i\in[0,1].
\]

- \(\beta\): log end-to-end scale ratio under this model.
- \(\exp(\beta)\): predicted endpoint size ratio.
- Report fit residual dispersion and monotonicity, not only slope.
- A spacing progression can similarly fit \(\Delta_i/L\) against normalized path position.

A high raw variance can coexist with a highly regular progression. The relevant “irregularity” is then the residual around the progression.

For flowing rhythms, estimate a path and compare motif orientation with the local tangent. Path estimation itself is a model choice; it must not silently invent an ordering for a scattered field.

#### F. Mask-aware autocorrelation

For displacement \(h\), use only valid pairs

\[
\Omega_h=\{p:p\in R,\ p+h\in R\}.
\]

A bounded normalized descriptor is the Pearson correlation of the two overlapping samples:

\[
C(h)=
\frac{\sum_{\Omega_h}(I(p)-\mu_{0,h})
(I(p+h)-\mu_{1,h})}
{\sqrt{
\sum_{\Omega_h}(I(p)-\mu_{0,h})^2
\sum_{\Omega_h}(I(p+h)-\mu_{1,h})^2
}}.
\]

- Dimensionless, in \([-1,1]\), when the denominator is nonzero.
- Zero variance means **undefined**, not “perfect regularity.”
- Exclude zero lag and the immediate self-similarity neighborhood when locating repeats.
- Report displacement vectors \(h/L\), peak height, peak width, and overlap support.
- Reject lags with insufficient valid overlap using a declared rule.

For speed, FFT correlations can compute products, overlap counts, and moments. However,

\[
\operatorname{IFFT}(|\operatorname{FFT}(I)|^2)
\]

alone is **not** the complete mask-aware, overlap-normalized Pearson calculation.

For linear rather than circular image correlation, pad sufficiently—at least \(2H-1\) by \(2W-1\) for full self-correlation.

A high peak may come from the central object’s silhouette or repeated shading features. Run the calculation on a semantically appropriate representation:

- Background crop.
- Motif occupancy map.
- Centroid impulse map with declared smoothing.
- Object-surface region.
- Selected color/edge channel.

These representations answer different questions.

#### G. Fourier periodicity

With documented preprocessing, define a nonnegative power map:

\[
P(f_x,f_y)=|\mathcal{F}\{w(I-\mu)\}|^2.
\]

Here \(w\) is a declared window; a Hann window is a practical option, not a universal best choice.

For a simple stripe-like component with frequency-vector magnitude \(f\) in cycles/pixel:

\[
p_{\mathrm{px}}=1/f,
\qquad
\tilde p=1/(fL).
\]

**Important:** Fourier orientation is the frequency-vector direction, normal to stripe direction. For a skew 2-D lattice, recover direct-lattice geometry from reciprocal-lattice vectors; taking the reciprocal magnitude of one arbitrary peak is not a general nearest-neighbor estimator.

Useful proposed descriptors:

- Dominant frequency vectors.
- Their relative powers.
- Peak width.
- Power in declared scale/orientation bands.
- Peak concentration:

\[
Q=\frac{\sum_{f\in \mathcal N}P(f)}
{\sum_{f\in B}P(f)}.
\]

\(\mathcal N\) is a fixed neighborhood around selected peaks; \(B\) is the declared analysis band.

- Normalized spectral entropy:

\[
H_P=-\frac{\sum_{b=1}^{m}p_b\log p_b}{\log m},
\quad
p_b=P_b/\sum P_b.
\]

Use identical bins, channels, frequency range, and preprocessing. This entropy is not a validated emotional-tempo score.

Critical pitfalls:

- A strong harmonic can be mistaken for the fundamental pitch.
- Motif shape contributes spectral structure.
- Translation changes phase without necessarily changing power.
- Radial averaging discards orientation and can hide differences between stripe and grid layouts.
- Zero filling an irregular mask multiplies the image by that mask and introduces mask-related spectral structure.
- Windowing reduces leakage but broadens peaks.
- Zero padding samples the spectrum more densely; it does not create additional observed repeats or resolve fundamentally missing evidence.
- Aliasing occurs near the sampling limit; inspect the delivered display resolution.
- Uniform resizing preserves normalized frequency only with suitable resampling and sufficient source detail.

For a width-\(W\) observation, ordinary x-frequency bin spacing is \(1/W\) cycles/pixel. A first-order period sensitivity is approximately

\[
|\delta p|\approx p^2|\delta f|.
\]

Long periods estimated from only a few cycles therefore warrant substantial uncertainty.

#### H. Local scale changes and wavelets

For 2-D wavelet detail coefficients, a practical proposed feature is valid-region mean squared coefficient magnitude:

\[
E_{j,o}=
\frac{1}{N_{j,o}}
\sum_{p\in R_{j,o}}|D_{j,o}(p)|^2,
\qquad
e_{j,o}=E_{j,o}/\sum_{j,o}E_{j,o}.
\]

Record wavelet, level, orientation band, padding, normalization, and valid-support mask.

Use local maps to distinguish:

- Uniform repeat size.
- Motifs becoming progressively finer.
- One dense corner.
- Local disruption hidden by a strong global spectrum.

Wavelet energy alone is **not proof of semantic repetition**. A single large edge also produces coefficients.

For a 1-D motif/path profile, CWT output frequency is spatial frequency when sample spacing is spatial. Calling it Hz or converting it to BPM would incorrectly introduce time.

The official documentation warns that low scales can alias and coefficient magnitudes are not directly comparable across wavelet families. Keep the wavelet family and sampling convention fixed.

#### I. Spatial point-pattern statistics

For motif centers in an observation window of area \(A_R\):

\[
\widehat K(r)=
\frac{A_R}{n(n-1)}
\sum_{i\ne j}
\mathbf1\{d_{ij}\le r\}e_{ij}.
\]

Here \(e_{ij}\) is the chosen boundary-correction weight.

Units:

- \(r\): length.
- \(K\): length².
- \(L_c(r)=\sqrt{K(r)/\pi}-r\): length.
- \(g(r)=K'(r)/(2\pi r)\): dimensionless.

For stationary Poisson points:

\[
K(r)=\pi r^2,\quad g(r)=1.
\]

Inhibitory/exclusion behavior can produce \(g<1\); clustering can produce \(g>1\). Neither is automatically an artistic defect.

For comparison, use \(r/L\) and \(K/L^2\), or a declared density-relative coordinate \(r\sqrt{\rho}\). These answer different questions: card-space similarity versus spacing relative to point density.

Do not use unrestricted uniform randomness as the only baseline if the design excludes:

- The central-object silhouette and its halo.
- Card margins.
- Motif overlaps.
- Certain colors or motif classes from particular regions.

Simulate the **same eligible window and relevant constraints**. For a deliberately progressive density field, homogeneous K can confuse intensity variation with interaction; stratify or use an appropriate inhomogeneous model.

For small decorative counts, annotated spacing and direct layout fitting are usually more interpretable than formal spatial inference.

#### J. Pattern breaks

Fit the repeat rule first. For predicted visible slots \(\hat p_j\), match observed instances with a declared tolerance and correspondence method.

Record separately:

- Missing eligible slot.
- Extra instance.
- Positional residual.
- Scale residual.
- Orientation residual.
- Wrong motif class.
- Deliberate mark/color exception.

Example normalized positional error:

\[
e_j=\|p_j-\hat p_j\|/\hat\Delta.
\]

An interruption rate can be defined as violated eligible slots divided by eligible slots. **Slots hidden behind the central object or intentionally excluded by a halo must not count as missing.**

A one-off exception can be compositionally meaningful despite barely changing a global spectrum. Conversely, a low correlation patch can be caused by lighting, clipping, or motif appearance rather than a missing repeat.

#### K. Comparison and uncertainty

Recommended comparison report:

| Feature | Useful comparison |
|---|---|
| Count | Absolute difference, alongside motif class and eligible area |
| Median size/pitch | Absolute log ratio, for positive defined quantities |
| Size/spacing distributions | Wasserstein distance with shared normalized units |
| Orientation | Circular/axial distribution distance |
| Spectral distribution | Jensen–Shannon divergence with identical bins |
| ACF or pair-correlation curves | Integrated discrepancy over a shared supported lag range |
| Known layout | Assignment residuals plus unmatched instances |
| Alternation | Sequence agreement and explicit violations |
| Breaks | Count, type, normalized location, intended versus unintended |

Do not combine these immediately into an opaque “rhythm similarity” score. If a weighted score is later needed, publish its weights, missing-feature policy, calibration set, and sensitivity.

Uncertainty protocol:

1. Show detected motifs and excluded regions.
2. Compare manual annotation with automatic outputs on representative cards.
3. Perturb thresholds, masks, detection confidence, resizing, and analysis windows.
4. Report resulting sensitivity ranges.
5. Distinguish those ranges from statistical confidence intervals.
6. Bootstrap independent reference cards when inferring a reference-set distribution.
7. Do not treat all motif pairs as independent observations.
8. Use block/replicate-aware methods or appropriate simulations for dependent spatial data.
9. Report \(n\), valid area, number of intervals, observed repeat cycles, and supported radii.
10. Mark unsupported features as unavailable rather than assigning zero.

### Gaps

- No universal acceptable spacing-CV, spectral-peak, or break-rate threshold was established for stylized object cards.
- No universal minimum motif count establishes all forms of rhythm. Method-specific warnings are more defensible than one cutoff.
- The formulas above require application-specific validation and reference calibration.
- Learned confidence scores are not automatically calibrated probabilities of correct motif identity.
- No experiments established how strongly these descriptors predict viewers’ mood, perceived busyness, or eye movements.

## 3. How should references become prompts, quantitative targets, and isolated corrective controls?

### Takeaway

Use a closed loop: **annotate references → describe explicit repeat structure → set region-conditioned target ranges → generate or construct → measure → correct only the offending layer/instances**. Exact count and spacing are better enforced by geometry or compositing than by descriptive prompting alone.

### Cited Findings

- Getty’s definitions distinguish repeating elements, organized movement, variety, and emphasis, supporting a vocabulary that separates recurrence from interpretation. — [Getty](https://www.getty.edu/education/teachers/building_lessons/principles_design.pdf)
- Existing normalized template matching can find multiple motif occurrences when combined with peak detection. — [Official example](https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_template.html), [official tests](https://github.com/scikit-image/scikit-image/blob/main/tests/skimage/feature/test_template.py)
- CountGD++ provides semantic/exemplar-conditioned counting, including exclusions, but is not itself an image editor or complete rhythm analyzer. — [Paper and code](https://github.com/niki-amini-naieni/CountGDPlusPlus)
- SVG patterns supply explicit deterministic tiling parameters. — [W3C SVG patterns](https://www.w3.org/TR/SVG2/pservers.html#Patterns)
- ControlNet supplies an existing spatial-conditioning route from edges/scribbles/segmentation to generated imagery, without establishing exact preservation or repeat compliance. — [Official implementation](https://github.com/lllyasviel/ControlNet)

### Inferences

The workflow and numerical examples below are **proposed controls**, not measured properties of a reference set.

#### A. Reference extraction

For every reference, record:

```text
region: background / border / object surface / supporting ornament
motif: what counts as one instance
arrangement: row / grid / radial / curve / scattered field
scale: motif diameter relative to card and/or object
density: instances per eligible normalized area
spacing: median pitch, edge gap, dispersion
orientation: aligned / alternating / radial / tangent-following / varied
sequence: AA / ABAB / ABC / other
progression: size, spacing, angle, or density trend
exceptions: number, type, location
protected area: central-object silhouette and readability halo
interpretation: intended calm/playful/busy/etc., separately labeled
```

Derive empirical ranges from several comparable references. Do not average unrelated content classes until the motif definition and normalization are compatible.

Reference matching should preserve both:

- **Within-card structure:** pitch, alternation, local exceptions.
- **Across-card consistency:** the distribution of those descriptors.

#### B. Prompt vocabulary with measurable anchors

Prefer:

> “Sparse, evenly spaced leaf motifs in the background, approximately 0.04 card-width in size, with center-to-center spacing around three motif widths. Keep a clear undecorated halo around the central object.”

Over:

> “A calm rhythmic background.”

Useful prompt clauses:

- **Scale:** “large repeated scallops”; “fine repeated dots”; “motifs about one-twentieth of the card’s short side.”
- **Density:** “six supporting motifs”; “sparse corner-only repetition”; “a dense border, empty center.”
- **Spacing regularity:** “nearly equal center spacing”; “moderate positional variation, no tight clusters.”
- **Sequence:** “alternate leaf and berry motifs”; “repeat an ABC sequence.”
- **Progression:** “motifs become gradually smaller toward the upper edge”; “spacing widens smoothly from left to right.”
- **Orientation:** “all upright”; “alternate ±15°”; “follow the curve’s tangent.”
- **Interruption:** “one deliberately omitted repeat near the upper-right edge”; “one larger accent among otherwise matching motifs.”
- **Protection:** “no motif crosses the object silhouette or its surrounding empty halo.”

Numerical prompt language communicates intent; it is not a hard guarantee. Use “approximately” unless the layout is explicitly constructed or independently checked.

Avoid negative prompts such as “no repetition” when the intended change is merely lower density. They can destroy useful ornament structure.

#### C. Example target specification

Illustrative, not a universal aesthetic prescription:

```text
Region: eligible background, excluding central object and halo.
Motif: one whole four-point sparkle.
Count: 8–12.
Median equivalent diameter: 0.025–0.040 short-side units.
Median nearest-neighbor spacing: 0.12–0.18 short-side units.
No unwanted overlaps.
Orientation: report only if sparkle shape has a meaningful axis.
Exceptions: one intentionally larger sparkle; no missing-slot penalty
            unless a repeat lattice is actually specified.
Protected central-object pixels: unchanged.
```

Do not simultaneously impose incompatible count, density, area, pitch, and size targets. They constrain one another.

#### D. Isolated correction table

| Diagnosis | Smallest useful intervention | Preserve/check |
|---|---|---|
| Motifs too large; spacing acceptable | Scale individual motifs about their centers | Count, centers, central object |
| Density too high | Remove selected motifs or reduce eligible coverage intentionally | Remaining sizes and style |
| Spacing too irregular | Move instances toward fitted row/grid/path positions | Appearance, size, class |
| Pattern too mechanically regular | Add bounded, seeded position/orientation jitter | Mean density and object halo |
| ABAB sequence broken | Replace only the incorrect motif class | Centers, sizes, other marks |
| Progression inconsistent | Adjust only sizes or intervals to the fitted trend | Other progression axes |
| One accidental gap | Restore one eligible missing slot | Deliberate gaps and occlusions |
| Too much repetition | Remove a declared subset or introduce specific controlled variation | Central-object readability |
| Motifs compete with object | Remove/relocate motifs near its contour; reduce ornament prominence if needed | Object silhouette and identity |
| Set feels inconsistent | Correct outlier descriptor(s) on particular cards | Content-specific intentional differences |

For positional correction, one possible proposal is

\[
p_i^{new}=(1-\alpha)p_i+\alpha\hat p_i,
\quad 0\le\alpha\le1.
\]

This makes correction strength explicit. It is not automatically valid if correspondence is ambiguous or movement causes overlap.

To add organic variation:

\[
p_i^{new}=\hat p_i+\epsilon_i
\]

with a declared bounded jitter distribution, fixed seed, minimum separation, and protected-region rejection. This is **constrained irregularity**, not unspecified randomness.

#### E. Protect central-object readability structurally

Let \(O\) be the central-object mask. Expand it by halo distance \(h\):

\[
O_h=\operatorname{dilate}(O,h),
\qquad
E=B\setminus O_h.
\]

Here \(B\) is the allowed background region and \(E\) the editable region.

- Construct, move, or inpaint motifs only inside \(E\).
- Preserve the original object layer.
- After generative editing, composite protected pixels from the original.
- Check minimum motif-to-object clearance and unintended contour tangencies at final display size.
- If the target motifs are **on the object surface**, define a separate interior edit region instead of applying a blanket background rule.

A prompt saying “preserve the object” is weaker than a locked layer and final compositing. Fixed random seeds improve experimental control but do not guarantee unchanged pixels.

Useful preservation checks:

\[
D_O=\operatorname{mean}_{p\in O}
\|I_{\text{after}}(p)-I_{\text{before}}(p)\|_1.
\]

Exact copied protected pixels should give \(D_O=0\), subject to a consistent pixel/color representation. For edits restricted to \(E\), also compare all pixels outside \(E\).

Pixel preservation does not by itself prove readability: surrounding ornament can still crowd or visually compete with the object. Retain human inspection at delivery size.

#### F. Practical algorithm choices

**Known flat graphic motifs**

1. Use authoring-layer instances when available.
2. Otherwise use color/alpha segmentation and connected components.
3. Measure labeled regions.
4. Use template matching if segmentation is unreliable but appearance is stable.
5. Apply nonmaximum suppression/peak separation appropriate to motif size.
6. Review a detection overlay before trusting counts.

**Known motif, varying rotation/scale**

- Search an explicit template bank over rotation/scale.
- Deduplicate detections across templates.
- Report transformation range and residual detection failures.
- Avoid claiming invariance from ordinary single-template matching.

**Unknown but regular fronto-parallel pattern**

- Autocorrelation/Fourier proposals followed by spatial verification.
- Consider the 2025 repeated-tile detector as research prior art, subject to license and domain constraints.
- Verify whether the inferred tile is a fundamental unit or a larger repeated supertile.

**Semantic motifs with variable appearance**

- Manual annotation remains a strong baseline for a small card set.
- CountGD++ is an advanced candidate for prompted/exemplar-driven instance proposals.
- Inspect confusion between whole motifs and their parts.
- Do not derive reliable orientation or silhouette spacing from boxes alone if masks are required.

**Approximate symmetry**

- Start with declared-axis geometric reflection/rotation comparisons.
- Consider CLIPSym only when learned semantic symmetry is actually needed and its deployment/license gaps are resolved.

**Progressive/local recurrence**

- Ordered motif geometry first.
- Local FFT or wavelet profiles when a spatial intensity signal is meaningful.
- Do not add wavelets merely because the image contains fine detail.

#### G. Minimal stack versus advanced stack

**Minimal recommended stack**

- Existing image/instance annotations.
- NumPy/SciPy for distances, correlations, FFTs, assignments.
- scikit-image for segmentation, normalized template matching, and region measurements.
- A standard SVG-capable or layered image editor for deterministic instance placement.

This stack can run its conventional NumPy-backed analysis on CPU and does not require NVIDIA hardware or neural weights. No timings or installed-package checks were performed.

Start with:

1. Count.
2. Median motif diameter.
3. Coverage.
4. Median spacing and spacing CV.
5. Orientation/sequence only where meaningful.
6. Explicit exception list.
7. Optional masked ACF/FFT confirmation.

**Advanced additions only when justified**

- PyWavelets: local scale changes or nonstationary spatial profiles.
- spatstat: sufficiently populated point patterns, mask-aware spatial inference, marked relationships, simulations.
- CountGD++: difficult semantic instance proposals.
- CLIPSym: learned reflection/rotation proposals.
- Repeat-unit detector: unknown regular fronto-parallel tiling.
- ControlNet-compatible generation: rendering a prescribed spatial guide into illustration, followed by measurement and preservation checks.

For SVG, a single tile repeats any jitter embedded inside it. A “randomized” supertile is still periodic at the supertile scale. Use separately controlled instances when true nonrepeating placement variation is intended.

#### H. Validation experiment for the parent synthesis owner

Create or annotate a small controlled set with one change at a time:

1. Same motifs, doubled pitch.
2. Same centers, larger motifs.
3. Same count and size, increased position jitter.
4. Same geometry, ABAB versus shuffled labels.
5. Smooth size progression versus randomly permuted sizes.
6. One omitted motif.
7. Same internal pattern, different central-object size.
8. Same card features, different card ordering.
9. Same source image, multiple delivered resolutions.

Expected discriminations:

- Count unchanged under pure scale/position changes.
- Coverage changes under motif enlargement.
- Pitch changes under geometric spacing changes.
- Alternation detects ordering, not just class proportions.
- Progression residuals distinguish orderly variation from shuffled variation.
- Break detection localizes an omission.
- Region-conditioned density accounts for changing available background.
- Set-order descriptors change without falsely changing individual-card geometry.
- Resolution tests reveal aliasing and unstable motif detection.

These are proposed checks, **not completed results**.

### Gaps

- No generative prompting method inspected guarantees exact count, regularity, or isolated preservation.
- AMD/ROCm and CPU viability of the learned research repositories remains unverified; CountGD++ explicitly documents CUDA-oriented setup.
- Licenses for learned weights, upstream components, datasets, and commercial deployment need separate review.
- No target illustrations were processed, no detector accuracy was measured, and no corrective workflow was tested.
- Emotional interpretation should remain an explicitly attributed artistic judgment or a separately validated human-response study—not a deterministic output of spectral frequency.
