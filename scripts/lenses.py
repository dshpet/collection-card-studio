"""What each reviewer sees besides the card: a lens per specialist and a geometry panel per checker.

Geometry is measured from pixels: straight edges (LSD), ellipses fitted to curves, the skeleton of thin parts.
It points a reviewer at a place to look. It does not decide anything.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from skimage import measure, morphology

from common import ROOT

SIZE = (430, 480)
FAMILY_COLORS = ((230, 30, 30), (20, 110, 240), (0, 160, 60), (230, 140, 0), (170, 40, 210))
OTHER = (150, 150, 150)


def card_image(card):
    return Image.open(ROOT / card["file"]).convert("RGB").resize(SIZE, Image.LANCZOS)


def mask_of(card):
    return Image.open(card["derived"] / "masks" / f"{card['id']}.png").convert("L").resize(SIZE)


def object_crop(card, pad=12):
    """The object cut from the full-size drawing when there is one, at most 860×960, with its mask."""
    mask = mask_of(card)
    box = mask.point(lambda v: 255 if v > 127 else 0).getbbox() or (0, 0, *SIZE)
    box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, SIZE[0]), min(box[3] + pad, SIZE[1]))
    source = Image.open(card["full"]).convert("RGB") if card.get("full") else card_image(card)
    scale = source.width / SIZE[0]
    crop = source.crop(tuple(round(v * scale) for v in box))
    crop.thumbnail((SIZE[0] * 2, SIZE[1] * 2), Image.LANCZOS)
    return crop, np.asarray(mask.crop(box).resize(crop.size)) > 127


def font(image):
    return ImageFont.load_default(max(14, max(image.size) // 40))


def faded(image, amount=0.6):
    return Image.blend(image, Image.new("RGB", image.size, "white"), amount)


def with_legend(image, rows):
    """The image with a white strip below it: a swatch and a line of text per row."""
    text = font(image)
    step = text.size + 8
    out = Image.new("RGB", (image.width, image.height + step * len(rows) + 8), "white")
    out.paste(image)
    draw = ImageDraw.Draw(out)
    for i, (color, line) in enumerate(rows):
        y = image.height + 6 + i * step
        draw.rectangle((8, y + 3, 8 + text.size, y + text.size), fill=color)
        draw.text((16 + text.size, y), line, fill="black", font=text)
    return out


# Specialist lenses, each the size of a card.

def grey_groups(card):
    grey = ImageOps.grayscale(card_image(card))
    return grey.point(lambda v: min(v // 51, 4) * 63).convert("RGB")


def flat_colors(card):
    return card_image(card).quantize(8, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")


def silhouette(card):
    return Image.composite(Image.new("RGB", SIZE, "black"), Image.new("RGB", SIZE, "white"), mask_of(card))


def normals(card):
    return Image.open(card["derived"] / "normals" / f"{card['id']}.png").convert("RGB").resize(SIZE)


def shading(card):
    return Image.open(card["derived"] / "shading" / f"{card['id']}.png").convert("RGB").resize(SIZE)


def edge_map(card):
    grey = np.asarray(ImageOps.grayscale(card_image(card)), dtype=float)
    strength = np.hypot(*np.gradient(grey))
    return Image.fromarray(255 - np.clip(strength * 6, 0, 255).astype(np.uint8)).convert("RGB")


def hero_crop(card):
    box = mask_of(card).point(lambda v: 255 if v > 127 else 0).getbbox() or (0, 0, *SIZE)
    x, y = min((box[0] + box[2]) // 2, SIZE[0] - 108), min((box[1] + box[3]) // 2, SIZE[1] - 120)
    x, y = max(x, 107), max(y, 120)
    return card_image(card).crop((x - 107, y - 120, x + 108, y + 120)).resize(SIZE, Image.LANCZOS)


def thumbnail(card):
    canvas = Image.new("RGB", SIZE, (128, 128, 128))
    small = card_image(card).resize((129, 144), Image.LANCZOS)
    canvas.paste(small, ((SIZE[0] - 129) // 2, (SIZE[1] - 144) // 2))
    return canvas


def background_alone(card):
    return Image.composite(Image.new("RGB", SIZE, (128, 128, 128)), card_image(card), mask_of(card))


# Geometry.

def segments(grey, region, min_length):
    """Straight edges whose middle lies in the region, as rows of x1, y1, x2, y2."""
    found = cv2.createLineSegmentDetector().detect(grey)[0]
    lines = found.reshape(-1, 4) if found is not None else np.zeros((0, 4))
    length = np.hypot(lines[:, 2] - lines[:, 0], lines[:, 3] - lines[:, 1])
    middle = ((lines[:, :2] + lines[:, 2:]) / 2).astype(int)
    inside = region[middle[:, 1].clip(0, region.shape[0] - 1), middle[:, 0].clip(0, region.shape[1] - 1)]
    return lines[(length >= min_length) & inside]


def families(lines, tolerance=8, count=5):
    """Edges grouped by direction in the picture, strongest first: (angles, label per edge, -1 for none).
    Angles are degrees counterclockwise from horizontal."""
    angle = np.degrees(np.arctan2(lines[:, 1] - lines[:, 3], lines[:, 2] - lines[:, 0])) % 180
    length = np.hypot(lines[:, 2] - lines[:, 0], lines[:, 3] - lines[:, 1])
    gap = lambda a: np.minimum(abs(angle - a), 180 - abs(angle - a))
    label = np.full(len(lines), -1)
    peaks = []
    while len(peaks) < count:
        free = label < 0
        best = int(np.argmax([length[free & (gap(a) <= tolerance)].sum() for a in range(180)]))
        members = free & (gap(best) <= tolerance)
        if members.sum() < 3:
            break
        label[members] = len(peaks)
        peaks.append(best)
    return peaks, label


def ellipse_fit(curve, size):
    """A curve that is a true ellipse: rims, wheels, round faces, holes. None for other shapes."""
    if len(curve) < 30:
        return None
    (cx, cy), (a, b), angle = cv2.fitEllipse(curve)
    major, minor = max(a, b) / 2, min(a, b) / 2
    if major < size * 0.03 or minor < 4 or major > size:
        return None
    points = curve[:, 0, :].astype(float) - (cx, cy)
    t = np.radians(angle)
    x = (points[:, 0] * np.cos(t) + points[:, 1] * np.sin(t)) / (a / 2)
    y = (points[:, 1] * np.cos(t) - points[:, 0] * np.sin(t)) / (b / 2)
    off = np.percentile(np.abs(np.hypot(x, y) - 1), 90) * minor / major
    coverage = len(np.unique((np.arctan2(y, x) / (2 * np.pi) * 36).astype(int) % 36)) / 36
    both_sides = min(((y > 0.3) if a >= b else (x > 0.3)).mean(), ((y < -0.3) if a >= b else (x < -0.3)).mean())
    if coverage < 0.5 or off * major > max(0.015 * major, 0.75) or both_sides < 0.15 or minor / major < 0.1:
        return None  # 0.75 px allows for pixel noise on small rims. An open arc or a straight run fits a thin ellipse too
    return {"center": (cx, cy), "axes": (a / 2, b / 2), "angle": angle, "ratio": minor / major, "off": off,
            "minor_angle": (-angle - (90 if a >= b else 0)) % 180}


def ellipses(grey, region, mask, limit=8):
    """True ellipses among the drawn curves and the outline, one per place."""
    size = max(grey.shape)
    edges = cv2.Canny(cv2.GaussianBlur(grey, (5, 5), 0), 30, 90)
    edges[~region] = 0
    curves = [*cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0],
              *cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]]
    kept = []
    for fit in sorted(filter(None, (ellipse_fit(curve, size) for curve in curves)), key=lambda e: e["off"]):
        if all(np.hypot(fit["center"][0] - k["center"][0], fit["center"][1] - k["center"][1]) > 0.1 * max(k["axes"])
               or abs(max(fit["axes"]) - max(k["axes"])) > 0.12 * max(k["axes"]) for k in kept):
            kept.append(fit)
    return sorted(kept[:limit], key=lambda e: (e["center"][1], e["center"][0]))


def thin_parts(mask):
    """Thin parts of the object (cables, ropes, rails, legs), their skeleton, where they end and where they branch."""
    size = max(mask.shape)
    thin = mask & ~morphology.opening(mask, morphology.disk(max(4, size // 70)))
    thin = morphology.remove_small_objects(thin, max_size=size)
    skeleton = morphology.skeletonize(mask) & morphology.dilation(thin, morphology.disk(2))
    skeleton = morphology.remove_small_objects(skeleton, max_size=size // 25, connectivity=2)
    neighbours = cv2.filter2D(skeleton.astype(np.uint8), -1, np.ones((3, 3), np.float32)) - skeleton
    ends = np.argwhere(skeleton & (neighbours == 1))
    forks = [region.centroid for region in measure.regionprops(measure.label(skeleton & (neighbours >= 3)))]
    return thin, skeleton, ends, forks


def mark_ellipses(draw, found, text):
    """Each ellipse in black with its short axis, numbered. Returns legend rows."""
    rows = []
    for number, e in enumerate(found, 1):
        (cx, cy), (a, b) = e["center"], e["axes"]
        outline = cv2.ellipse2Poly((int(cx), int(cy)), (int(a), int(b)), int(e["angle"]), 0, 360, 4)
        draw.line([tuple(p) for p in outline] + [tuple(outline[0])], fill="black", width=2)
        t, short = np.radians(e["minor_angle"]), min(a, b)
        draw.line([(cx - np.cos(t) * short, cy + np.sin(t) * short), (cx + np.cos(t) * short, cy - np.sin(t) * short)],
                  fill="black", width=2)
        draw.text((cx + 6, cy - text.size - 4), f"E{number}", fill="black", font=text, stroke_width=3, stroke_fill="white")
        rows.append(((0, 0, 0), f"E{number}: width ratio {e['ratio']:.2f}, short axis at {e['minor_angle']:.0f}°, "
                                f"off a true ellipse by {e['off'] * 100:.1f}%"))
    return rows


def legible(crop, mask):
    """Small crops, as of real cards, are doubled so the marks stay readable."""
    if max(crop.size) >= 700:
        return crop, mask
    double = (crop.width * 2, crop.height * 2)
    return crop.resize(double, Image.LANCZOS), np.asarray(Image.fromarray(mask).resize(double)) > 0


def perspective_panel(card):
    """Straight edges coloured by direction, and true ellipses with their short axis, on the enlarged object."""
    image, mask = legible(*object_crop(card))
    grey = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    region = morphology.dilation(mask, morphology.disk(6))
    lines = segments(grey, region, max(grey.shape) * 0.03)
    peaks, label = families(lines)
    panel = faded(image)
    draw = ImageDraw.Draw(panel)
    for (x1, y1, x2, y2), family in zip(lines, label):
        draw.line([(x1, y1), (x2, y2)], fill=FAMILY_COLORS[family] if family >= 0 else OTHER,
                  width=max(2, max(image.size) // 220))
    rows = [(FAMILY_COLORS[i], f"edges near {angle}°") for i, angle in enumerate(peaks)] + [(OTHER, "other edges")]
    rows += mark_ellipses(draw, ellipses(grey, region, mask), font(image))
    return with_legend(panel, rows)


def construction_panel(card):
    """Thin parts with their ends and branch points, and true ellipses, on the enlarged object."""
    image, mask = legible(*object_crop(card))
    thin, skeleton, ends, forks = thin_parts(mask)
    pixels = np.asarray(faded(image)).copy()
    pixels[thin] = (pixels[thin] * 0.5 + np.array(FAMILY_COLORS[2]) * 0.5).astype(np.uint8)
    pixels[morphology.dilation(skeleton, morphology.disk(1))] = (0, 110, 0)
    panel = Image.fromarray(pixels)
    draw = ImageDraw.Draw(panel)
    mark = max(8, max(image.size) // 80)
    for y, x in ends:
        draw.ellipse((x - mark, y - mark, x + mark, y + mark), outline=FAMILY_COLORS[4], width=3)
    for y, x in forks:
        draw.rectangle((x - mark, y - mark, x + mark, y + mark), outline="black", width=3)
    grey = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    rows = [(FAMILY_COLORS[2], "thin parts, with their centre line"), (FAMILY_COLORS[4], "circle: a thin part ends"),
            ((0, 0, 0), "square: thin parts branch")]
    rows += mark_ellipses(draw, ellipses(grey, morphology.dilation(mask, morphology.disk(6)), mask), font(image))
    return with_legend(panel, rows)


PANELS = {"construction": construction_panel, "perspective": perspective_panel}
