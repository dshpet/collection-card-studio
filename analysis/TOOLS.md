# Question → existing tool → bounded evidence

**Status:** installed classical libraries are usable offline in `.venv`; source-only estimators are not enabled. The [manifest](../.slim/clonedeps.json) records eight read-only sparse source checkouts and exact commits. Public import paths below differ from internal source filenames. The [CLI](../scripts/image_evidence.py) wraps only the explicitly described subset, not every API in this table.

## Installed and inspectable

| Question | Tool/API and checked local source | Output | Guardrail |
|---|---|---|---|
| Is a reviewed object small/off-center? | `skimage.measure.regionprops_table`; [region properties](../.slim/clonedeps/repos/scikit-image__scikit-image/src/skimage/measure/_regionprops.py) | Area, bbox, centroid, axes, solidity | Mask geometry, not perceived balance. CLI uses one union label, not connected-component selection. |
| What is the boundary transition? | `skimage.measure.profile_line`; [profile.py](../.slim/clonedeps/repos/scikit-image__scikit-image/src/skimage/measure/profile.py) | Samples along a selected path | API takes row/column; CLI takes x/y. Not automatic shadow softness. |
| What are rendered lightness/color groups? | `colour.sRGB_to_XYZ`, `XYZ_to_Oklab`, `delta_E`; [sRGB](../.slim/clonedeps/repos/colour-science__colour/colour/models/rgb/common.py), [Oklab](../.slim/clonedeps/repos/colour-science__colour/colour/models/oklab.py), [differences](../.slim/clonedeps/repos/colour-science__colour/colour/difference/__init__.py) | Y, lightness/chroma, named color distances | sRGB decoding occurs inside the conversion. Y is not Lab L*, nits, or incident light. |
| How do two role palettes differ? | `ot.emd2(a,b,M)`; [POT solver](../.slim/clonedeps/repos/PythonOT__POT/ot/lp/_network_simplex.py) | Optimal transport cost for supplied masses/costs | Declare ground distance and units; not automatically squared perceptual error. Quantize/sample, not all-pixel square matrices. |
| At which scales is variation concentrated? | `pywt.swt2`; [SWT source](../.slim/clonedeps/repos/PyWavelets__pywt/pywt/_swt.py) | H/V/D coefficient energies | Record wavelet, normalization, padding, support. CLI reports only Haar level 1; not brushwork/material recognition. |
| Is a patch granular or directionally organized? | `graycomatrix`, `graycoprops`, `local_binary_pattern`; [texture.py](../.slim/clonedeps/repos/scikit-image__scikit-image/src/skimage/feature/texture.py); `structure_tensor`, [corner.py](../.slim/clonedeps/repos/scikit-image__scikit-image/src/skimage/feature/corner.py) | Co-occurrence, local-pattern, orientation descriptors | Not CLI features. Quantization/scale matter; GLCM pairs need both pixels in the intended region. |
| Are contours compact, or explicit strokes thick? | `perimeter_crofton`, [utilities](../.slim/clonedeps/repos/scikit-image__scikit-image/src/skimage/measure/_regionprops_utils.py); `medial_axis`, [skeleton source](../.slim/clonedeps/repos/scikit-image__scikit-image/src/skimage/morphology/_skeletonize.py) | Conditional shape/perimeter or stroke-mask distances | An edge detector's chain thickness is not stroke width. No automatic stroke mask here. |

Pillow handles image/profile decoding; NumPy/SciPy supply statistics, erosion, and numerical operations. Stable imports are `skimage.*`, not development `_skimage2` examples found in older notes.

### Existing CLI contract

`summary IMAGE [--mask MASK] [--background R G B]` reports native dimensions; whole-frame or reviewed-mask-union geometry; Y/Oklab quantiles; the top six fixed **8×8×8 encoded-RGB bins** and remaining mass; Sobel magnitude; Haar SWT level 1 energy. No mask means no subject identification. Color/geometry use the un-eroded region; edge/detail aggregation uses a two-pixel eroded interior after full-image filtering. Thin regions can leave no valid interior.

`profile IMAGE --start X Y --end X Y [--width N] [--background R G B]` returns `distance_px` and `luminance_Y`. It uses order 1 interpolation, mean reduction across linewidth, and reflected edge sampling. It does not classify the line as a shadow, calculate transition widths, or estimate light direction.

Both EXIF-transpose, stay at native resolution, convert usable embedded ICC profiles to sRGB, and record missing-profile sRGB assumptions. Nonopaque alpha requires an explicit background, composited in linear sRGB; alpha is not a semantic mask. Unsupported/malformed inputs fail rather than silently quantize. Masks must be grayscale and exactly match analysis dimensions; values ≥128 select pixels. Output is stdout JSON, with no automatic file writes, editing, or downloads. Colour's missing-Matplotlib warning on stderr is nonblocking; plotting is not required.

### Reviewed Aesthetics Toolbox functions

`aspect_ratio`, `std_channels`, and `shannonentropy_channels` in [AT/color_and_simple_qips.py](../.slim/clonedeps/repos/RBartho__Aesthetics-Toolbox/AT/color_and_simple_qips.py) passed the [local verification](verification.json), not the full UI. Pass NumPy arrays despite some Pillow-oriented docstrings. Standard deviation measures the supplied channel's variation, not lighting contrast universally. Entropy divides by each input's maximum before rounding to 256 levels; it is **not interchangeable with fixed-bin entropy across images**. [AT/balance_qips.py](../.slim/clonedeps/repos/RBartho__Aesthetics-Toolbox/AT/balance_qips.py) is available but unexecuted. Research basis: the [published toolbox paper](https://doi.org/10.3758/s13428-025-02632-3).

The [root license](../.slim/clonedeps/repos/RBartho__Aesthetics-Toolbox/LICENSE) contains MIT-style text bearing a **2018 Python Packaging Authority** copyright. That unusual notice is not blanket clearance of all assets, datasets, or weights. The sparse pack excludes the bundled AlexNet `.npy`; do not run an upstream entrypoint assuming all dependencies/assets are present.

## Source-only: add estimates only for a specific question

| Question | Local source / candidate | Output and status | Restriction |
|---|---|---|---|
| Propose a foreground mask? | [BiRefNet model](../.slim/clonedeps/repos/ZhengPeng7__BiRefNet/models/birefnet.py) | L foreground proposal; no weights/inference environment | MIT code; selected official checkpoint terms separate. Review shadows, glow, holes, and attached parts. |
| What depth ordering is plausible? | [DAV2 model](../.slim/clonedeps/repos/DepthAnything__Depth-Anything-V2/depth_anything_v2/dpt.py), [runner](../.slim/clonedeps/repos/DepthAnything__Depth-Anything-V2/run.py) | L relative-depth array; disabled | Small checkpoint Apache-2.0; larger checkpoints NC. Runner normalizes its visualization per image, not metric depth. |
| Which variation resembles shading? | [Marigold IID](../.slim/clonedeps/repos/prs-eth__Marigold/marigold/marigold_iid_pipeline.py), [runner](../.slim/clonedeps/repos/prs-eth__Marigold/script/iid/run.py) | L albedo/diffuse-shading/residual with IID-Lighting; disabled | Apache code; Open RAIL++-M task checkpoint, not Apache or automatically NC. |
| What surface orientations are plausible? | [Marigold normals](../.slim/clonedeps/repos/prs-eth__Marigold/marigold/marigold_normals_pipeline.py) | L normal field; separate checkpoint/pipeline | IID-Appearance predicts albedo/roughness/metallicity, **not normals**. |

No learned CPU/AMD throughput or complete RX 7900 XTX/ROCm execution is verified. Model loaders can fetch weights; source presence is not permission to run or download.

Marigold's [image-analysis extension](https://arxiv.org/abs/2505.09358) describes the depth, normal, and intrinsic-analysis tasks; it does not turn the estimates into recovered scene truth.

## Indexed, not cloned or installed

| Tool | When worth considering; why not a default |
|---|---|
| [OpenCV](https://docs.opencv.org/4.x/) | Contours, line/calibration tools; current installed stack already covers basic geometry/profiles, so no full clone needed. |
| [SAM2](https://github.com/facebookresearch/sam2) | Interactive instance selection after point/box input; optional when reviewed manual/BiRefNet proposals are insufficient. Apache code/checkpoints; full CPU/AMD path unvalidated. |
| [GeoCalib](https://github.com/cvg/GeoCalib) | Gravity/FOV hypotheses when perspective cues exist; not object azimuth. Apache code, CC-BY weights; optional scope. |
| [MoGe](https://github.com/microsoft/MoGe) | Alternative point/depth/normal estimates; version/dependency differences, including newer sparse/Triton components, need review. |
| [Intrinsic](https://github.com/compphoto/Intrinsic) | Useful shading/reflectance research; academic-use restrictions and patent notice, not mandatory unrestricted tooling. |
| [DSINE](https://github.com/baegwangbin/DSINE) | Normal estimation requiring intrinsics assumptions; noncommercial/internal/academic terms. |
| [PyIQA](https://github.com/chaofengc/IQA-PyTorch) | Named degradation/similarity metrics; current PolyForm Noncommercial code and applicable extra terms, possible weight downloads. Not a style oracle. |

Relighting and generators are not default analysis tools. The [lighting workflow](LIGHTING.md) starts with reviewed image evidence, not reconstruction or synthesis.
