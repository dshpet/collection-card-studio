"""Does a measured backdrop grade bring drawings closer to their real cards?

Real backdrops are darker toward the corners, with light pooled behind the object. Ours are lighter and flatter, and
the image model ignored the words for it (analysis/STYLE_GAPS.md, Batches graded by the producer). This learns the gap
instead: the median difference in background lightness (L*) between each real card and its twin, by distance from the
object, and adds it to the twin's background through a soft mask. The object is untouched.

Tested on the forty final-style twins in two folds by object, so no twin is graded with a profile it helped fit.
Closeness is CSD against the twin's own real card, the measure that tracked the producer (analysis/STYLE_GAPS.md).

    grade.py                        -> runs/grade/<fold>/<twin>.png, runs/grade/result.json
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, gaussian_filter
from skimage.color import lab2rgb, rgb2lab

from common import DERIVED, ROOT, SIZE, load_json, save_json

RUN = ROOT / "runs" / "grade"
TWINS = ROOT / "runs" / "twins40"
BINS = np.linspace(0, 1, 11)


def load(image, mask):
    rgb = np.asarray(Image.open(image).convert("RGB").resize(SIZE, Image.LANCZOS), dtype=float) / 255
    subject = np.asarray(Image.open(mask).convert("L").resize(SIZE)) > 127
    return rgb, subject


def radius(subject):
    """Each pixel's distance from the object's box centre, 0 there and 1 at the farthest card corner."""
    ys, xs = np.nonzero(subject) if subject.any() else (np.array([240]), np.array([215]))
    cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    yy, xx = np.mgrid[:subject.shape[0], :subject.shape[1]]
    far = max(np.hypot(cy - y, cx - x) for y in (0, subject.shape[0]) for x in (0, subject.shape[1]))
    return np.hypot(yy - cy, xx - cx) / far


def profile(rgb, subject):
    """Median background L* in each distance bin."""
    light = rgb2lab(rgb)[..., 0]
    background = ~binary_dilation(subject, iterations=6)
    r = radius(subject)
    return np.array([np.median(light[background & (r >= lo) & (r < hi)]) if (background & (r >= lo) & (r < hi)).sum() > 200
                     else np.nan for lo, hi in zip(BINS[:-1], BINS[1:])])


def grade(rgb, subject, shift):
    """Add the L* shift by distance to the background, feathered at the object's edge."""
    lab = rgb2lab(rgb)
    centres = (BINS[:-1] + BINS[1:]) / 2
    filled = np.where(np.isnan(shift), np.nanmedian(shift), shift)
    delta = np.interp(radius(subject), centres, filled)
    weight = gaussian_filter((~binary_dilation(subject, iterations=3)).astype(float), 4)
    lab[..., 0] = np.clip(lab[..., 0] + delta * weight, 0, 100)
    return np.clip(lab2rgb(lab), 0, 1)


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    import torch
    from scipy.stats import wilcoxon

    from embed import MODELS, load_csd

    twins = load_json(TWINS / "briefs.json")
    rows = []
    for twin in twins:
        drawn = TWINS / "final" / "tries" / f"{twin['id']}_1.png"
        rgb, subject = load(drawn, TWINS / "final" / "derived" / "masks" / f"{twin['id']}_1.png")
        real_rgb, real_subject = load(ROOT / f"materials/card_examples/{twin['real']}.png", DERIVED / "masks" / f"{twin['real']}.png")
        rows.append({"twin": twin["id"], "real": twin["real"], "category": twin["card"]["category"], "rgb": rgb,
                     "subject": subject, "gap": profile(real_rgb, real_subject) - profile(rgb, subject)})

    folds = {0: [r for i, r in enumerate(rows) if i % 2 == 0], 1: [r for i, r in enumerate(rows) if i % 2 == 1]}
    shifts = {}
    for fold, held in folds.items():
        fitted = np.nanmedian([r["gap"] for r in folds[1 - fold]], axis=0)
        shifts[fold] = fitted
        (RUN / f"fold{fold}").mkdir(parents=True, exist_ok=True)
        for row in held:
            row["graded"] = grade(row["rgb"], row["subject"], fitted)
            Image.fromarray((row["graded"] * 255).round().astype(np.uint8)).save(RUN / f"fold{fold}" / f"{row['twin']}.png")

    encode = load_csd(MODELS["csd"])
    images = ([Image.open(ROOT / f"materials/card_examples/{r['real']}.png").convert("RGB") for r in rows]
              + [Image.fromarray((r["rgb"] * 255).round().astype(np.uint8)) for r in rows]
              + [Image.fromarray((r["graded"] * 255).round().astype(np.uint8)) for r in rows])
    with torch.inference_mode():
        vectors = torch.cat([encode(images[i:i + 8]).float() for i in range(0, len(images), 8)])
    vectors = torch.nn.functional.normalize(vectors, dim=-1).cpu().numpy()
    n = len(rows)
    before = np.sum(vectors[:n] * vectors[n:2 * n], axis=1)
    after = np.sum(vectors[:n] * vectors[2 * n:], axis=1)
    by_category = {c: f"{int((after > before)[[r['category'] == c for r in rows]].sum())} of "
                      f"{sum(r['category'] == c for r in rows)}" for c in sorted({r["category"] for r in rows})}
    result = {"twins": n, "csd_before": round(float(before.mean()), 4), "csd_after": round(float(after.mean()), 4),
              "closer": int((after > before).sum()), "wilcoxon_p": round(float(wilcoxon(after, before).pvalue), 4),
              "closer_by_category": by_category,
              "shift_by_distance": {f"fold{f}": [round(float(v), 1) for v in s] for f, s in shifts.items()},
              "by_twin": {r["twin"]: [round(float(b), 3), round(float(a), 3)] for r, b, a in zip(rows, before, after)}}
    save_json(RUN / "result.json", result)
    print({k: v for k, v in result.items() if k != "by_twin"})


if __name__ == "__main__":
    main()
