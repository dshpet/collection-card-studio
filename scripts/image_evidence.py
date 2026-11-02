#!/usr/bin/env python3
"""image_evidence.py -- offline descriptive image evidence, one JSON object.

Tone/geometry/palette/edge/scale-band observations via Pillow, NumPy, SciPy,
scikit-image, colour-science, PyWavelets. Descriptive only: no aesthetic/style
score, no inference of original scene, lighting, capture or materials. Errors
-> stderr + nonzero exit. Native resolution; no resize, no files written.
Coords are x,y in EXIF-transposed native pixels.

    image_evidence.py summary IMAGE [--mask MASK] [--background R G B]
    image_evidence.py profile IMAGE --start X Y --end X Y [--width N] [--background R G B]
"""

import argparse, hashlib, io, json, math, sys

import numpy as np
import PIL
from PIL import Image, ImageCms, ImageOps
import colour, pywt, scipy, skimage
from scipy.ndimage import binary_erosion
from skimage.filters import sobel
from skimage.measure import profile_line, regionprops

SMALL_IMAGE_LIMIT = 128
MASK_THRESHOLD = 128
SUPPORTED_MODES = ("RGB", "RGBA", "L", "LA", "P")


class EvidenceError(Exception):
    """Clean user-facing failure (stderr + nonzero exit)."""


def fail(msg):
    raise EvidenceError(msg)


def num(value):
    """Finite Python float, or clean failure."""
    v = float(value)
    if not math.isfinite(v):
        fail("non-finite value produced by computation")
    return v


def srgb_eotf(c):  # encoded sRGB -> linear light (piecewise IEC 61966-2-1)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def srgb_oetf(c):  # linear light -> encoded sRGB (piecewise IEC 61966-2-1)
    return np.where(c <= 0.0031308, 12.92 * c,
                    1.055 * np.power(np.clip(c, 0.0, None), 1 / 2.4) - 0.055)


def sha256_of(path):
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                digest.update(chunk)
    except OSError as exc:
        fail(f"cannot read {path!r}: {exc}")
    return digest.hexdigest()


def validate_background(values):
    bg = [int(v) for v in values]
    if len(bg) != 3 or any(v < 0 or v > 255 for v in bg):
        fail("--background must be three integers in 0..255")
    return bg


def apply_icc(image, icc_profile):
    """Embedded ICC -> sRGB via ImageCms; fail if malformed/unsupported."""
    try:
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc_profile))
        dst = ImageCms.createProfile("sRGB")
        if image.mode == "RGBA":  # keep alpha through color management
            alpha = image.getchannel("A")
            rgb = ImageCms.profileToProfile(image.convert("RGB"), src, dst,
                                            outputMode="RGB")
            out = Image.merge("RGBA", (*rgb.split(), alpha))
        else:
            out = ImageCms.profileToProfile(image, src, dst, outputMode="RGB")
    except Exception as exc:
        fail(f"embedded ICC profile is malformed or unsupported: {exc}")
    return out, "converted from embedded ICC profile to sRGB via PIL.ImageCms"


def load_rendered(path):
    """Open, EXIF-transpose and color-manage an image at native resolution."""
    digest = sha256_of(path)
    try:
        with Image.open(path) as raw:
            raw.load()
            original_mode = raw.mode
            icc_profile = raw.info.get("icc_profile")
            image = ImageOps.exif_transpose(raw)
            image.load()
    except EvidenceError:
        raise
    except Exception as exc:
        fail(f"cannot decode image {path!r}: {exc}")
    if image.mode not in SUPPORTED_MODES and image.mode != "CMYK":
        fail(f"unsupported image mode {image.mode!r}; supported 8-bit modes: RGB, "
             "RGBA, L, LA, P (CMYK only with usable embedded ICC); high-bit/float "
             "modes rejected, not silently quantized")
    if image.mode == "P":
        image = image.convert("RGBA")  # preserves palette transparency
    elif image.mode == "L":
        image = image.convert("RGB")
    elif image.mode == "LA":
        image = image.convert("RGBA")
    if icc_profile is not None:
        image, note = apply_icc(image, icc_profile)
        icc_flag = True
    elif image.mode == "CMYK":
        fail("CMYK image without a usable embedded ICC profile; refusing to guess")
    else:
        note = "no embedded ICC profile; sRGB assumed (assumption recorded)"
        icc_flag = False
    meta = {"sha256": digest, "original_mode": original_mode,
            "icc": icc_flag, "color_note": note}
    return image, meta


def rendered_rgb(image, background):
    """Encoded sRGB float array (H,W,3) in [0,1] plus alpha provenance."""
    arr = np.asarray(image, dtype=np.uint8)
    if arr.ndim != 3 or arr.shape[2] not in (3, 4):
        fail("unexpected decoded array shape")
    has_alpha = arr.shape[2] == 4
    nonopaque = int(np.count_nonzero(arr[..., 3] < 255)) if has_alpha else 0
    rgb = arr[..., :3].astype(np.float64) / 255.0
    record = {"mode_had_alpha": has_alpha, "nonopaque_pixels": nonopaque,
              "background_rgb8": None, "treatment": "none; fully opaque"}
    if nonopaque:
        if background is None:
            fail("image has non-opaque alpha pixels; explicit --background R G B "
                 "is required")
        alpha = arr[..., 3].astype(np.float64) / 255.0
        backdrop = srgb_eotf(np.asarray(background, dtype=np.float64) / 255.0)
        linear = srgb_eotf(rgb) * alpha[..., None] + backdrop * (1 - alpha[..., None])
        rgb = srgb_oetf(linear)
        record.update({"background_rgb8": [int(v) for v in background],
                       "treatment": "composited over explicit --background in LINEAR "
                                    "sRGB (piecewise EOTF, blend, OETF re-encode); "
                                    "backdrop recorded; alpha not a semantic mask"})
    elif background is not None:
        record["treatment"] = "none; fully opaque (--background supplied, unused)"
    return rgb, record


def luminance_oklab(rgb):
    """Relative luminance Y, Oklab L and chroma from encoded sRGB.

    colour.sRGB_to_XYZ decodes encoded sRGB by default, so values are passed
    encoded exactly once (no double decoding).
    """
    xyz = colour.sRGB_to_XYZ(rgb)
    lab = colour.XYZ_to_Oklab(xyz)
    return xyz[..., 1], lab[..., 0], np.hypot(lab[..., 1], lab[..., 2])


def provenance(path, meta, alpha_record, width, height):
    return {"path": path, "sha256": meta["sha256"], "width": width, "height": height,
            "decoded_at_native_resolution": True, "exif_transpose_applied": True,
            "original_mode": meta["original_mode"],
            "color": {"icc_profile_embedded": meta["icc"],
                      "handling": meta["color_note"],
                      "reporting": "encoded sRGB kept for palette/reporting; "
                                   "linearized only inside colour.sRGB_to_XYZ "
                                   "(single decode) and the EOTF in compositing"},
            "alpha": alpha_record,
            "libraries": {"pillow": PIL.__version__, "numpy": np.__version__,
                          "scipy": scipy.__version__, "scikit-image": skimage.__version__,
                          "colour-science": colour.__version__, "pywavelets": pywt.__version__}}


def load_mask(path, width, height):
    """8-bit grayscale mask in analysis coordinates; exact size match required."""
    digest = sha256_of(path)
    try:
        with Image.open(path) as m:
            m.load()
            if m.mode == "1":
                m = m.convert("L")
            if m.mode != "L":
                fail(f"mask must be 8-bit grayscale (mode L or 1), got {m.mode!r}")
            arr = np.asarray(m, dtype=np.uint8)
    except EvidenceError:
        raise
    except Exception as exc:
        fail(f"cannot decode mask {path!r}: {exc}")
    if arr.shape != (height, width):
        fail(f"mask is {arr.shape[1]}x{arr.shape[0]} but image is {width}x{height}; "
             "exact match in analysis coordinates required (no resize)")
    selected = arr >= MASK_THRESHOLD
    if not selected.any():
        fail("mask selects zero pixels; empty region rejected")
    info = {"source": path, "sha256": digest, "loaded_in_analysis_coordinates": True,
            "threshold": MASK_THRESHOLD,
            "rule": "pixel selected when 8-bit mask value >= 128",
            "selected_pixels": int(selected.sum())}
    return selected, info


def quantile_stats(values):
    p10, p50, p90 = np.quantile(np.asarray(values, dtype=np.float64), [0.10, 0.50, 0.90])
    return {"p10": num(p10), "p50": num(p50), "p90": num(p90), "p90_p10": num(p90 - p10)}


def palette(rgb, region):
    """Deterministic palette: fixed 8 bins per encoded sRGB channel."""
    px = rgb[region]
    bins = np.minimum((px * 8.0).astype(np.int64), 7)
    ids = (bins[:, 0] << 6) | (bins[:, 1] << 3) | bins[:, 2]
    counts = np.bincount(ids, minlength=512)
    order = sorted((b for b in range(512) if counts[b] > 0),
                   key=lambda b: (-int(counts[b]), b))
    top = order[:6]
    total = int(px.shape[0])
    entries = [{"bin_id": int(b),
                "mean_rgb8": [int(round(min(max(float(v), 0.0), 1.0) * 255.0))
                              for v in px[ids == b].mean(axis=0)],
                "share": num(counts[b] / total)} for b in top]
    remaining = 1.0 - float(sum(int(counts[b]) for b in top)) / total
    return {"method": "deterministic fixed quantization: 8 bins per encoded sRGB "
                       "channel, bin=min(floor(c*8),7), bin_id=(r<<6)|(g<<3)|b; six "
                      "most populous bins, ties by ascending bin_id; not kmeans",
            "sampled_pixels": total, "bins": entries, "remaining_share": num(remaining)}


def wavelet_bands(y, interior):
    """Haar SWT level-1 band energy on the full image (never mask-zeroed first)."""
    h, w = y.shape
    base = {"method": "pywt.swt2 Haar level 1, norm=True, on full linear Y "
                      "reflect-padded to even dims; coefficients cropped back to "
                      "original extent; mask never zeroed before filtering",
            "label": "native-pixel band energy (mean squared detail coefficient, "
                     "squared linear-luminance units); not brushwork/material/beauty"}
    if h < 2 or w < 2:
        return {**base, "status": "abstained",
                "reason": "a dimension is < 2 px; reflect padding unsafe, band "
                          "energy not reported"}
    pad_h, pad_w = h % 2, w % 2
    try:
        padded = np.pad(y, ((0, pad_h), (0, pad_w)), mode="reflect")
        c_h, c_v, c_d = pywt.swt2(padded, "haar", level=1, norm=True)[0][1]
    except Exception as exc:
        return {**base, "status": "abstained",
                "reason": f"reflect padding / swt2 failed: {exc}"}
    c_h, c_v, c_d = c_h[:h, :w], c_v[:h, :w], c_d[:h, :w]
    full = {"H": num(np.mean(c_h ** 2)), "V": num(np.mean(c_v ** 2)),
            "D": num(np.mean(c_d ** 2))}
    if interior.any():
        inter = {"mean_sq": {"H": num(np.mean(c_h[interior] ** 2)),
                             "V": num(np.mean(c_v[interior] ** 2)),
                             "D": num(np.mean(c_d[interior] ** 2))}}
    else:
        inter = {"mean_sq": None, "reason": "no valid eroded interior pixels"}
    return {**base, "status": "ok",
            "reflect_padding": {"bottom": int(pad_h), "right": int(pad_w)},
            "interior_mean_sq": inter, "full_extent_mean_sq": full}


def limitations(width, height):
    notes = [
        "Descriptive statistics of the rendered image only; no aesthetic/style "
        "score, no inference of original scene, capture, lighting or materials.",
        "Tone values are dimensionless, display-referred (D65); no nits, Kelvin, "
        "key/fill ratio or physical roughness is implied.",
        "Region outputs describe the user-supplied mask union or the whole frame; "
        "not a detected subject or lighting region.",
        "Edge/wavelet values are native-pixel descriptive energy, not outline "
        "width, brushwork, readability or quality.",
    ]
    if min(width, height) < SMALL_IMAGE_LIMIT:
        notes.append(f"native image < {SMALL_IMAGE_LIMIT} px in a dimension; "
                     "fine-detail/material conclusions unsupported (arithmetic "
                     "still reported)")
    return notes


def cmd_summary(args):
    image, meta = load_rendered(args.image)
    width, height = image.size
    background = validate_background(args.background) if args.background else None
    rgb, alpha_record = rendered_rgb(image, background)
    y, oklab_l, oklab_c = luminance_oklab(rgb)

    if args.mask is not None:
        region, mask_info = load_mask(args.mask, width, height)
        scope = "user-supplied reviewed mask region (not predicted semantics); no auto segmentation"
    else:
        region = np.ones((height, width), dtype=bool)
        mask_info = {"source": None, "scope": "whole frame (no --mask supplied)",
                     "selected_pixels": width * height}
        scope = ("whole-image (no user mask); describes the entire frame, not a "
                 "subject, lighting or any semantic region")
    mask_info["scope"] = scope

    label = region.astype(np.int32)
    prop = regionprops(label)[0]  # single union label; no component selection
    min_row, min_col, max_row, max_col = prop.bbox
    centroid_row, centroid_col = prop.centroid
    area = int(prop.area)
    geometry = {
        "scope": scope,
        "method": "skimage.measure.regionprops on the 0/1 mask cast to int (one "
                  "union label; no connected-component selection)",
        "selected_pixels": area, "canvas_pixels": width * height,
        "selected_fraction": num(area / (width * height)),
        "bbox_x0y0x1y1_exclusive": [int(min_col), int(min_row), int(max_col), int(max_row)],
        "centroid_xy": [num(centroid_col), num(centroid_row)],
        "bbox_margins_normalized_by_canvas": {"left": num(min_col / width),
                                              "top": num(min_row / height),
                                              "right": num((width - max_col) / width),
                                              "bottom": num((height - max_row) / height)}}

    value_color = {
        "scope": scope + "; rendered (composited) image, un-eroded mask union",
        "units": "dimensionless, display-referred D65; no nits, Kelvin, exposure, "
                 "key/fill ratio or physical roughness is implied",
        "luminance_Y": quantile_stats(y[region]),
        "oklab_L": quantile_stats(oklab_l[region]),
        "oklab_chroma": quantile_stats(oklab_c[region]),
        "definitions": {"luminance_Y": "relative luminance colour.sRGB_to_XYZ("
                                       "encoded sRGB)[...,1], linear, single decode",
                        "oklab_L": "colour.XYZ_to_Oklab L channel",
                        "oklab_chroma": "sqrt(a^2 + b^2) from Oklab"}}

    sobel_mag = sobel(y)  # full linear relative luminance BEFORE region masking
    interior = binary_erosion(region, iterations=2)
    n_interior = int(interior.sum())
    if n_interior:
        sobel_out = {"valid_pixels": n_interior,
                     "mean_magnitude": num(sobel_mag[interior].mean())}
    else:
        sobel_out = {"valid_pixels": 0, "mean_magnitude": None,
                     "reason": "region eroded by 2 native px leaves no valid interior"}
    edges_detail = {"sobel": {
        "computed_on": "full-image linear relative luminance Y before region "
                       "masking (skimage.filters.sobel)",
        "interior_rule": "region eroded by 2 native px (scipy.ndimage."
                         "binary_erosion, iterations=2, border_value=0)",
        **sobel_out,
        "interpretation": "mean gradient magnitude over valid interior; not outline "
                          "width or readability"},
        "wavelet": wavelet_bands(y, interior)}

    return {"command": "summary",
            "input": provenance(args.image, meta, alpha_record, width, height),
            "mask": mask_info, "geometry": geometry, "value_color": value_color,
            "palette": palette(rgb, region), "edges_detail": edges_detail,
            "conventions": {"coordinates": "x,y in EXIF-transposed native pixels; "
                                             "bbox x0,y0,x1,y1 with x1,y1 exclusive",
                            "canvas": f"{width}x{height}"},
            "limitations": limitations(width, height)}


def cmd_profile(args):
    image, meta = load_rendered(args.image)
    width, height = image.size
    background = validate_background(args.background) if args.background else None
    rgb, alpha_record = rendered_rgb(image, background)
    y, _, _ = luminance_oklab(rgb)

    (x0, y0), (x1, y1) = args.start, args.end
    for name, v in (("start", x0), ("start", y0), ("end", x1), ("end", y1)):
        if not math.isfinite(v):
            fail(f"--{name} coordinate must be finite, got {v!r}")
    if not (0.0 <= x0 <= width - 1 and 0.0 <= y0 <= height - 1):
        fail(f"--start ({x0}, {y0}) outside image bounds {width}x{height}")
    if not (0.0 <= x1 <= width - 1 and 0.0 <= y1 <= height - 1):
        fail(f"--end ({x1}, {y1}) outside image bounds {width}x{height}")
    if args.width < 1:
        fail("--width must be a positive integer")

    samples = profile_line(y, (y0, x0), (y1, x1), linewidth=args.width,
                           order=1, mode="reflect", reduce_func=np.mean)
    samples = np.asarray(samples, dtype=np.float64).ravel()
    n = int(samples.shape[0])
    length = math.hypot(x1 - x0, y1 - y0)
    distance = np.linspace(0.0, length, n)

    return {"command": "profile",
            "input": provenance(args.image, meta, alpha_record, width, height),
            "profile": {
                "start_xy": [num(x0), num(y0)], "end_xy": [num(x1), num(y1)],
                "width": int(args.width), "order": 1, "mode": "reflect",
                "reduce_func": "mean",
                "sampled_channel": "linear relative luminance Y "
                                   "(colour.sRGB_to_XYZ), full image, not masked",
                "n_samples": n,
                "distance_px": [num(v) for v in distance],
                "luminance_Y": [num(v) for v in samples],
                "units": {"luminance_Y": "dimensionless relative luminance (linear "
                                          "light, D65), about [0,1] for sRGB content",
                          "distance_px": "native pixels along straight start->end "
                                         "path, linspace(0, hypot(dx,dy), n)"},
                "boundary_convention": "linewidth sampling may reflect at image "
                                       "edges (mode='reflect')",
                "zero_length_profile": bool(n == 1 and length == 0.0),
                "scope": "user-specified straight path; not labelled shadow/highlight; "
                         "no lamp-direction, softness or material inference"},
            "conventions": {"coordinates": "x,y in EXIF-transposed native pixels"},
            "limitations": limitations(width, height)}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="image_evidence.py",
        description="Offline descriptive image evidence as one JSON object on "
                    "stdout. No scores, no scene/style inference. Native resolution; "
                    "no artifacts written.")
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("summary", help="tone/geometry/palette/edge evidence for "
                                       "the whole image or a reviewed mask")
    s.add_argument("image", help="input image (8-bit RGB/RGBA/L/LA/P; CMYK only "
                                 "with usable embedded ICC)")
    s.add_argument("--mask", help="optional 8-bit grayscale mask, exactly the image "
                                  "dimensions, in analysis coordinates")
    s.add_argument("--background", nargs=3, type=int, metavar=("R", "G", "B"),
                   help="required for non-opaque alpha; composited in linear sRGB")
    p = sub.add_parser("profile", help="relative-luminance samples along a path")
    p.add_argument("image", help="input image")
    p.add_argument("--start", nargs=2, type=float, required=True, metavar=("X", "Y"),
                   help="start x,y in native pixels")
    p.add_argument("--end", nargs=2, type=float, required=True, metavar=("X", "Y"),
                   help="end x,y in native pixels")
    p.add_argument("--width", type=int, default=1, help="line width in native px "
                                                       "(positive integer)")
    p.add_argument("--background", nargs=3, type=int, metavar=("R", "G", "B"),
                   help="backdrop required for non-opaque alpha")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = cmd_summary(args) if args.command == "summary" else cmd_profile(args)
    except EvidenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # clean failure: stderr + nonzero, no traceback
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
