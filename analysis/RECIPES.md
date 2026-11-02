# Offline recipes from the project root

No install step, network call, model, plotting package, or automatic download is needed below. These examples reuse installed APIs and the checked local CLI helpers. All four executable shell blocks passed the recorded [local verification](verification.json). Examples on reduced references demonstrate mechanics, not fine-finish evidence or calibrated style interpretation.

## Geometry and rendered color: existing CLI

```sh
.venv/bin/python -B scripts/image_evidence.py summary materials/card_examples/3458764679576006333.png --background 255 255 255
```

Without a mask, geometry describes the entire frame. To measure a subject, add `--mask` with your reviewed grayscale mask file: exactly the EXIF-transposed analysis dimensions, values ≥128 selected. Disconnected selected parts form one union, not separately chosen instances. Read `geometry.selected_fraction`, exclusive bbox, centroid, normalized margins, and `value_color` quantiles. The top-six palette leaves `remaining_share`; do not pretend six bins represent all color mass.

## Profile a line, then review its meaning

```sh
.venv/bin/python -B scripts/image_evidence.py profile materials/card_examples/3458764679576006333.png --start 5 30 --end 50 30 --width 3 --background 255 255 255
```

These coordinates merely demonstrate a valid path, not a shadow annotation. Replace them with a reviewed same-material shadow crossing. CLI coordinates are x/y; `skimage.measure.profile_line` internally uses row/column. `distance_px` and `luminance_Y` are samples, not softness. Apply the endpoint/plateau and rejection procedure in [LIGHTING](LIGHTING.md#4-profile-a-reviewed-shadow-boundary); no automatic width/direction option exists. JSON goes to stdout; shell redirection is an explicit user choice, not `--output`.

## Colour, scale evidence, and reviewed classical QIPs

The local helpers below reuse EXIF, ICC, and linear-alpha handling. They are snapshot functions in this project, not a versioned library API. `colour.sRGB_to_XYZ` decodes encoded sRGB once; do not feed it an already decoded image with decoding still enabled.

```sh
.venv/bin/python -B - <<'PY'
import sys
import numpy as np
import pywt
from scripts.image_evidence import load_rendered, rendered_rgb, luminance_oklab

image, meta = load_rendered('materials/card_examples/3458764679576006333.png')
rgb, alpha = rendered_rgb(image, [255, 255, 255])
y, lightness, chroma = luminance_oklab(rgb)
print('relative Y / Oklab L / Oklab chroma medians:',
      *[float(np.median(a)) for a in (y, lightness, chroma)])

# Whole-image scale evidence: pad to a multiple of 2**2, not merely even.
h, w = y.shape
pad = ((0, (-h) % 4), (0, (-w) % 4))
yp = np.pad(y, pad, mode='reflect')
coefficients = pywt.swt2(yp, 'haar', level=2, norm=True)
print('reflect padding:', pad)
for level, (_, bands) in zip((2, 1), coefficients):
    print('H/V/D mean-square, level', level,
          [float(np.mean(b[:h, :w] ** 2)) for b in bands])

# Import ONLY the reviewed classical module, not the UI or machine script.
sys.path.insert(0, '.slim/clonedeps/repos/RBartho__Aesthetics-Toolbox')
from AT.color_and_simple_qips import aspect_ratio, std_channels, shannonentropy_channels
print('aspect:', aspect_ratio(rgb))
print('Y standard deviation:', std_channels(y))
print('Y entropy, this function\'s per-input-max normalization:',
      shannonentropy_channels(y))
PY
```

For regional wavelets, filter the full image first, crop padded coefficients back, and aggregate only valid interior support. The CLI's two-pixel erosion applies to its **level 1** recipe; it is not a generic support rule for higher levels. Reject tiny inputs unsuitable for reflect padding. H/V labels follow the API's array-axis convention. Scale energy does not establish brush identity or material; the QIP entropy rescales each input by its maximum before 256-level rounding, unlike a shared fixed-bin histogram.

## POT palette/distribution comparison

This runnable example compares **whole-image** fixed-bin color distributions; use corresponding reviewed roles to answer an art question. It rebuilds full masses rather than renormalizing the CLI's truncated six-bin display. Bin centers, not palette medoids, define the support here.

```sh
.venv/bin/python -B - <<'PY'
import numpy as np
import colour
import ot
from scripts.image_evidence import load_rendered, rendered_rgb

def distribution(path):
    image, _ = load_rendered(path)
    rgb, _ = rendered_rgb(image, [255, 255, 255])
    bins = np.minimum(np.floor(rgb.reshape(-1, 3) * 8).astype(int), 7)
    ids = (bins[:, 0] << 6) | (bins[:, 1] << 3) | bins[:, 2]
    count = np.bincount(ids, minlength=512).astype(float)
    active = np.flatnonzero(count)
    center = (np.column_stack((active >> 6, (active >> 3) & 7, active & 7)) + .5) / 8
    points = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(center))
    return count[active] / count.sum(), points

a, x = distribution('materials/card_examples/3458764679576006333.png')
b, z = distribution('materials/card_examples/3458764679576006335.png')
cost = np.linalg.norm(x[:, None, :] - z[None, :, :], axis=-1)
print('transport cost, unsquared Euclidean Oklab ground distance:',
      float(ot.emd2(a, b, cost)))
PY
```

`emd2` returns the supplied cost's optimum, not automatically a squared color distance. Different content, role areas, palette binning, or backdrops can dominate this result. It is not a style similarity percentage or acceptance threshold. Pixelwise `colour.delta_E` instead needs corresponding patches and the appropriate input space for the selected method.

## Source-only models: NOT enabled

Do not run these upstream entrypoints as part of the recipes. PyTorch/transformer/diffusion dependencies and weights are not installed; hub loaders can download artifacts. Any future dependency/weight retrieval requires separate authorization and component-term review.

| Candidate | Exact source/asset to inspect before a separately authorized setup |
|---|---|
| BiRefNet mask | `models/birefnet.py` in its [checkout](../.slim/clonedeps/repos/ZhengPeng7__BiRefNet/README.md); selected `ZhengPeng7/BiRefNet` checkpoint, not arbitrary variants. |
| DAV2 Small relative depth | [run.py](../.slim/clonedeps/repos/DepthAnything__Depth-Anything-V2/run.py), encoder `vits`, expected `checkpoints/depth_anything_v2_vits.pth`; default runner selects larger `vitl`, so do not run unchanged. |
| Marigold shading | [script/iid/run.py](../.slim/clonedeps/repos/prs-eth__Marigold/script/iid/run.py), `prs-eth/marigold-iid-lighting-v1-1`; default is appearance, not lighting. |
| Marigold normals | [script/normals/run.py](../.slim/clonedeps/repos/prs-eth__Marigold/script/normals/run.py), `prs-eth/marigold-normals-v1-1`; distinct output/task. |

No weights are supplied and no consumer-AMD inference is verified. Relighting/generation is outside this analysis pack.
