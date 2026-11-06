"""Did the second batch move toward the real cards on what the reference passes found?

runs/<genre>-batch2 was drawn after the planner learned the real backdrop color logic and the second reference pass
(analysis/SYNTHESIS.md, "Second pass"). Its delivered cards are measured against the first batch (runs/<genre>-batch)
and the real cards, the same way for all three, on categories 1-4:
    mirror      a near-mirror silhouette (IoU of the subject mask with its own flip, 0.85 or more), categories 1 and 3
    light pool  background beside the subject brighter than the top corners by more than 5 L*, categories 2 and 3
    cut         the subject touches a card edge, category 4
    warm->cool  a warm hero on a cool backdrop; floating on cyan, blue or green; Oklab backdrop chroma
    bands       the pipeline's own checks: candidates inside the real cards' measured bands

    batch2_check.py
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules
sys.path.insert(1, str(Path(__file__).resolve().parent))

import argparse
from collections import defaultdict

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
from skimage.color import rgb2lab

from color_logic import lch, warm
from colors import colors
from common import DERIVED, ROOT, best_try, load_json

GENRES = ("western", "sci-fi", "horror")
CANDIDATES = 3  # make_set.CANDIDATES; edits are numbered after the candidates


def mirror(mask):
    """IoU of the silhouette with its own mirror image about its centre column."""
    xs = np.nonzero(mask)[1]
    shift = int(round(xs.mean() * 2 - (mask.shape[1] - 1)))
    flipped = np.roll(mask[:, ::-1], shift, axis=1)
    return (mask & flipped).sum() / (mask | flipped).sum()


def shape(image, mask_path):
    mask = np.asarray(Image.open(mask_path).convert("L")) > 127
    light = rgb2lab(np.asarray(Image.open(image).convert("RGB").resize(mask.shape[::-1]), dtype=float) / 255)[..., 0]
    height, width = mask.shape
    near = binary_dilation(mask, iterations=25) & ~binary_dilation(mask, iterations=6)
    near[int(height * 0.6):] = False  # above the ground
    corner = np.zeros_like(mask)
    corner[:int(height * .15), :int(width * .15)] = corner[:int(height * .15), -int(width * .15):] = True
    corner &= ~binary_dilation(mask, iterations=6)
    pool = float(np.median(light[near]) - np.median(light[corner])) if near.sum() > 50 and corner.sum() > 50 else None
    edge = mask[:3].any() or mask[-3:].any() or mask[:, :3].any() or mask[:, -3:].any()
    return {"mirror": float(mirror(mask)), "pool": pool, "cut": bool(edge)}


def cards():
    for card in load_json(ROOT / "analysis" / "cards.json"):
        category = card["form"]["staging"]["art_category"]
        if category != "5":
            image, mask = ROOT / "materials" / "card_examples" / f"{card['id']}.png", DERIVED / "masks" / f"{card['id']}.png"
            yield "real", category, card["name"], image, mask
    for group in ("batch", "batch2"):
        for genre in GENRES:
            run = ROOT / "runs" / f"{genre}-{group}"
            history = load_json(run / "check.json")
            for brief in load_json(run / "briefs.json"):
                category = brief["card"]["category"]
                if category != "5" and history.get(brief["id"]):
                    try_id = best_try(history[brief["id"]])["try_id"]
                    yield group, category, brief["card"]["name"], run / "tries" / f"{try_id}.png", \
                        run / "derived" / "masks" / f"{try_id}.png"


def bands(group):
    passed = total = 0
    for genre in GENRES:
        for tries in load_json(ROOT / "runs" / f"{genre}-{group}" / "check.json").values():
            candidates = [t for t in tries if int(t["try_id"].rsplit("_", 1)[1]) <= CANDIDATES]
            passed += sum(t["passed"] for t in candidates)
            total += len(candidates)
    return passed, total


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    rows = defaultdict(list)
    for group, category, name, image, mask in cards():
        rows[group].append({"category": category, "name": name, **shape(image, mask), **colors(image, mask)})
    print("group   mirror>=0.85 (cat 1,3) | light pool >5 (cat 2,3) | cut by edge (cat 4) | warm->cool | floating on "
          "cyan/blue/green | backdrop chroma")
    for group in ("real", "batch", "batch2"):
        r = rows[group]
        sym = [x for x in r if x["category"] in ("1", "3")]
        pool = [x for x in r if x["category"] in ("2", "3") and x["pool"] is not None]
        cut = [x for x in r if x["category"] == "4"]
        hot = [x for x in r if lch(x["hero"])[1] >= 0.04 and warm(lch(x["hero"])[2])]
        floating = [x for x in r if x["category"] == "1"]
        print(f"{group:7} {sum(x['mirror'] >= 0.85 for x in sym):3}/{len(sym):<3}"
              f"                | {sum(x['pool'] > 5 for x in pool):3}/{len(pool):<3}"
              f"                  | {sum(x['cut'] for x in cut):3}/{len(cut):<3}"
              f"              | {sum(not warm(lch(x['backdrop'])[2]) for x in hot):3}/{len(hot):<3}"
              f"    | {sum(x['backdrop_family'] in ('cyan', 'blue', 'green') for x in floating):3}/{len(floating):<3}"
              f"                     | {np.mean([x['chroma'] for x in r]):.3f}")
    for group in ("batch", "batch2"):
        passed, total = bands(group)
        print(f"{group}: candidates inside the real bands {passed} of {total}")
        print("  near-mirror: " + ", ".join(x["name"] for x in rows[group]
                                            if x["category"] in ("1", "3") and x["mirror"] >= 0.85))


if __name__ == "__main__":
    main()
