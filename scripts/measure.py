"""Measured fields per card, computed from pixels, the subject mask and model estimates."""

from common import ANALYSIS, DERIVED, ROOT, cards, save_json

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import filters, measure, morphology
from sklearn.cluster import KMeans

SAMPLE = 20000
PLANAR = 0.012


# sRGB to Oklab (Ottosson 2020). Matches colour-science's sRGB_to_XYZ and XYZ_to_Oklab within 0.0002.
LMS = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]])
OKLAB = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099],
                  [0.0259040371, 0.7827717662, -0.8086757660]])


def to_oklab(rgb):
    rgb = np.asarray(rgb, dtype=float)
    linear = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return np.cbrt(linear @ LMS.T) @ OKLAB.T


def palette(rgb, lab, k):
    """The k main colours of a region, as hex with their share."""
    if len(lab) < k:
        return []
    picks = np.random.default_rng(0).choice(len(lab), min(SAMPLE, len(lab)), replace=False)
    model = KMeans(k, n_init=4, random_state=0).fit(lab[picks])
    shares = np.bincount(model.labels_, minlength=k) / len(picks)
    colors = []
    for cluster in np.argsort(-shares):
        mean = np.clip(rgb[picks][model.labels_ == cluster].mean(axis=0), 0, 1)
        colors.append({"hex": "#" + "".join(f"{round(v * 255):02x}" for v in mean),
                       "share": round(float(shares[cluster]), 3)})
    return colors


def hue_families(lab):
    """Effective number of distinct hues, weighted by chroma."""
    chroma = np.hypot(lab[..., 1], lab[..., 2])
    hue = (np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) + 360) % 360
    weights = np.histogram(hue, bins=12, range=(0, 360), weights=chroma)[0]
    weights = weights[weights > 0] / weights.sum()
    return float(np.exp(-(weights * np.log(weights)).sum()))


def warm_share(lab):
    """Share of chromatic pixels on the warm side of the Oklab a/b plane."""
    chroma = np.hypot(lab[:, 1], lab[:, 2])
    hue = (np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) + 360) % 360
    colored = chroma > 0.03
    warm = (hue < 110) | (hue > 330)
    return float((warm & colored).sum() / max(colored.sum(), 1))


def plane_tilt(values, mask):
    """Direction in which values rise across the mask: x right, y up, in units per card width."""
    ys, xs = np.nonzero(mask)
    height, width = mask.shape
    design = np.column_stack((xs / width, -ys / height, np.ones(len(xs))))
    solution, *_ = np.linalg.lstsq(design, values[mask], rcond=None)
    return float(solution[0]), float(solution[1])


def light_fit(lightness, normals, mask):
    """Fit lightness = a + l·n across the subject: the direction the rendering implies."""
    design = np.column_stack((normals[mask], np.ones(mask.sum())))
    target = lightness[mask]
    solution, *_ = np.linalg.lstsq(design, target, rcond=None)
    residual = target - design @ solution
    fit = 1 - residual.var() / max(target.var(), 1e-9)
    direction = solution[:3] / (np.linalg.norm(solution[:3]) + 1e-9)
    return {"light_azimuth": round(float(np.degrees(np.arctan2(direction[1], direction[0]))) % 360, 1),
            "light_elevation": round(float(np.degrees(np.arcsin(np.clip(direction[2], -1, 1)))), 1),
            "light_fit": round(float(fit), 3)}


def contour_shape(mask):
    """Share of the silhouette that runs straight, and its sharp corners per card width."""
    smooth = ndimage.gaussian_filter(mask.astype(float), 1.5)
    contour = max(measure.find_contours(smooth, 0.5), key=len)
    arc = np.r_[0, np.hypot(*np.diff(contour, axis=0).T).cumsum()]
    spots = np.arange(0, arc[-1], 2.0)
    line = np.column_stack([np.interp(spots, arc, contour[:, axis]) for axis in (0, 1)])
    ahead, behind = np.roll(line, -6, 0) - line, line - np.roll(line, 6, 0)
    cross = behind[:, 0] * ahead[:, 1] - behind[:, 1] * ahead[:, 0]
    turn = np.degrees(np.abs(np.arctan2(cross, (behind * ahead).sum(1))))
    return float((turn < 6).mean()), float(measure.label(turn > 50).max() / (arc[-1] / mask.shape[1]))


def planar_share(normals, region):
    """Share of the region whose surface normals barely change: flat faces, not inflated ones."""
    bend = np.sqrt(sum(np.square(np.gradient(normals, axis=axis)).sum(-1) for axis in (0, 1)))
    return float((bend[region] < PLANAR).mean())


def hue_of(hex_color):
    rgb = np.array([int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    lab = to_oklab(rgb)
    return float(np.degrees(np.arctan2(lab[2], lab[1])) % 360)


def measure_card(record, derived=DERIVED):
    """Works for reference and generated cards. Depth, attention and light need their model maps."""
    card_id = record["id"]
    rgb = np.asarray(Image.open(ROOT / record["file"]).convert("RGB"), dtype=np.float64) / 255
    lab = to_oklab(rgb)
    lightness = lab[..., 0]
    chroma = np.hypot(lab[..., 1], lab[..., 2])
    mask = np.asarray(Image.open(derived / "masks" / f"{card_id}.png").convert("L")) > 127
    background = ~mask
    height, width = mask.shape

    regions = measure.regionprops(measure.label(mask))
    main = max(regions, key=lambda region: region.area)
    y0, x0, y1, x1 = main.bbox
    convex_perimeter = measure.perimeter(main.image_convex)
    ys, xs = np.nonzero(mask)

    inner_ring = mask & ~morphology.erosion(mask, morphology.disk(4))
    outer_ring = morphology.dilation(mask, morphology.disk(4)) & ~mask
    interior = morphology.erosion(mask, morphology.disk(8))
    interior = interior if interior.any() else mask
    edges = filters.sobel(lightness)
    edge_line = edges > 0.08
    detail = np.abs(ndimage.laplace(lightness))

    tilt_x, tilt_y = plane_tilt(lightness, mask)
    straight, corners = contour_shape(mask)
    bright = morphology.white_tophat(lightness, morphology.disk(6))
    corner_zone = np.zeros_like(mask)
    for row, column in ((0, 0), (0, -1), (-1, 0), (-1, -1)):
        zone = (slice(None, 60) if row == 0 else slice(-60, None), slice(None, 60) if column == 0 else slice(-60, None))
        corner_zone[zone] = True

    lighting = {"light_bias_azimuth": round(float(np.degrees(np.arctan2(tilt_y, tilt_x))) % 360, 1),
                "light_bias_strength": round(float(np.hypot(tilt_x, tilt_y)), 3)}
    normals_path = derived / "normals" / f"{card_id}.npy"
    if normals_path.exists():
        normals = np.load(normals_path).astype(np.float64)
        lighting.update(light_fit(lightness, normals, mask))
        lighting["planar_share"] = round(planar_share(normals, interior), 3)
    shading_path = derived / "shading" / f"{card_id}.png"
    if shading_path.exists():
        shading = np.asarray(Image.open(shading_path).convert("L"), dtype=np.float64) / 255
        low, high = np.percentile(shading[mask], [5, 95])
        lighting["shading_range"] = round(float(high - low), 3)

    darkest = lightness[mask] <= np.percentile(lightness[mask], 25)
    colors = {"subject": palette(rgb[mask], lab[mask], 5), "background": palette(rgb[background], lab[background], 3)}
    hue_gap = abs(hue_of(colors["subject"][0]["hex"]) - hue_of(colors["background"][0]["hex"])) if all(colors.values()) else 0.0

    return {
        "color_palette": {
            "palette_subject": colors["subject"],
            "palette_background": colors["background"],
            "hue_gap": round(min(hue_gap, 360 - hue_gap), 1),
            "shadow_chroma_kept": round(float(chroma[mask][darkest].mean() / max(chroma[mask].mean(), 1e-6)), 3),
            "chroma_subject": round(float(chroma[mask].mean()), 4),
            "chroma_background": round(float(chroma[background].mean()), 4),
            "hue_families": round(hue_families(lab), 2),
            "warm_share": round(warm_share(lab.reshape(-1, 3)), 3),
        },
        "value_contrast": {
            "lightness_mean": round(float(lightness.mean()), 3),
            "lightness_p5": round(float(np.percentile(lightness, 5)), 3),
            "lightness_p95": round(float(np.percentile(lightness, 95)), 3),
            "lightness_p1": round(float(np.percentile(lightness, 1)), 3),
            "rms_contrast": round(float(lightness.std()), 3),
            "lightness_gap": round(float(lightness[mask].mean() - lightness[background].mean()), 3),
            "color_gap": round(float(np.linalg.norm(lab[mask].mean(0) - lab[background].mean(0))), 3),
            "boundary_contrast": round(float(np.linalg.norm(
                lab[inner_ring].mean(0) - lab[outer_ring].mean(0))), 3) if outer_ring.any() else None,
        },
        "composition_hierarchy": {
            "subject_area": round(float(mask.mean()), 3),
            "box_fill": round(float(main.area / main.area_bbox), 3),
            "center_x": round(float(xs.mean() / width), 3),
            "center_y": round(float(ys.mean() / height), 3),
            "margin_min": round(float(min(x0 / width, y0 / height, 1 - x1 / width, 1 - y1 / height)), 3),
            "box_width": round(float((x1 - x0) / width), 3),
            "box_height": round(float((y1 - y0) / height), 3),
        },
        "shape_proportions": {
            "solidity": round(float(main.solidity), 3),
            "eccentricity": round(float(main.eccentricity), 3),
            "compactness": round(float(min(1, 4 * np.pi * main.area / max(main.perimeter, 1) ** 2)), 3),
            "boundary_roughness": round(float(main.perimeter / max(convex_perimeter, 1)), 3),
            "holes": int(max(0, 1 - measure.euler_number(main.image, connectivity=2))),
            "straight_share": round(straight, 3),
            "corner_rate": round(corners, 3),
            "thin_share": round(float(1 - morphology.opening(mask, morphology.disk(5)).sum() / mask.sum()), 3),
        },
        "edges_linework": {
            "edge_density_subject": round(float(edge_line[mask].mean()), 3),
            "edge_density_background": round(float(edge_line[background].mean()), 3),
            "outline_darkness": round(float(lightness[interior].mean() - lightness[inner_ring].mean()), 3),
        },
        "surface_finish": {
            "detail_subject": round(float(detail[interior].mean()), 4),
            "detail_background": round(float(detail[background].mean()), 4),
            "highlight_share": round(float(((lightness > 0.9) & (chroma < 0.05))[mask].mean()), 3),
            "dark_share": round(float((lightness[mask] < 0.3).mean()), 3),
            "gloss_share": round(float((bright[interior] > 0.1).mean()), 3),
            "micro_texture": round(float(np.abs(lightness - ndimage.gaussian_filter(lightness, 1.5))[interior].mean()), 4),
            "form_contrast": round(float(np.subtract(*np.percentile(lightness[interior], [95, 5]))), 3),
            "vignette": round(float(np.median(lightness[background & ~corner_zone]) - np.median(lightness[background & corner_zone]))
                              if (background & corner_zone).any() else 0.0, 3),
        },
        "lighting_shading": lighting,
        **depth_fields(derived, card_id, mask, background),
        **attention_fields(derived, card_id, mask),
    }


def depth_fields(derived, card_id, mask, background):
    path = derived / "depth" / f"{card_id}.png"
    if not path.exists():
        return {}
    depth = np.asarray(Image.open(path), dtype=np.float64) / 65535
    return {"viewpoint_depth": {
        "subject_relief": round(float(np.percentile(depth[mask], 95) - np.percentile(depth[mask], 5)), 3),
        "background_depth_range": round(float(
            np.percentile(depth[background], 95) - np.percentile(depth[background], 5)), 3)}}


def attention_fields(derived, card_id, mask):
    path = derived / "attention" / f"{card_id}.npy"
    if not path.exists():
        return {}
    attention = np.load(path).astype(np.float64)
    attention = attention / attention.sum()
    peak_y, peak_x = np.unravel_index(np.argmax(attention), attention.shape)
    height, width = mask.shape
    density = attention[attention > 0]
    return {"attention": {
        "on_subject": round(float(attention[mask].sum()), 3),
        "peak_x": round(float(peak_x / width), 3),
        "peak_y": round(float(peak_y / height), 3),
        "spread": round(float(np.exp(-(density * np.log(density)).sum()) / attention.size), 3)}}


def main():
    result = {}
    for record in cards():
        if (DERIVED / "masks" / f"{record['id']}.png").exists():
            result[record["id"]] = measure_card(record)
    save_json(ANALYSIS / "measurements.json", result)
    print("measured", len(result))


if __name__ == "__main__":
    main()
