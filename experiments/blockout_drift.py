"""Do cards drawn from a Blender blockout break where the drawing leaves the blockout?

The restyle prompt says to keep the blockout's camera and parts exactly, yet five of the outside rater's nine
perspective breaks were drawn from blockouts. Two measures per card against its own render, both at 430x480: the
silhouette IoU (BiRefNet masks of the drawing and of the render, as the pipeline makes them) and the edge drift, the
mean distance in pixels from each edge of the render's object to the nearest edge of the drawing (Canny on lightness).
Labels: the outside rater's broken pre-final cards, the producer's works / slightly off / broken on the blockout
redraws and the construction trial's blockout arms.

    blockout_drift.py    -> runs/blockout_drift/scores.json, summary.json, broken.png (renders above drawings)
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse

from common import ROOT, SIZE, best_try, load_json, save_json
from estimate import write_masks

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.stats import mannwhitneyu

OUT = ROOT / "runs" / "blockout_drift"


def render_mask(render):
    rgb = np.asarray(Image.open(render).convert("RGB").resize(SIZE, Image.LANCZOS), dtype=np.float32)
    mask = np.asarray(Image.open(OUT / "derived" / "masks" / f"{render_key(render)}.png").convert("L").resize(SIZE)) > 127
    return (mask if mask.any() else None), rgb


def render_key(render):
    return str(render.relative_to(ROOT / "runs")).replace("/", "_")[:-4]


def edges(rgb, mask):
    gray = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    return (cv2.Canny(gray, 60, 140) > 0) & ndimage.binary_dilation(mask, iterations=3)


def score(drawing, render):
    mask_r, rgb_r = render_mask(render)
    mask_path = drawing.parent.parent / "derived" / "masks" / drawing.name
    if mask_r is None or not mask_path.exists():
        return None
    mask_d = np.asarray(Image.open(mask_path).convert("L").resize(SIZE)) > 127
    rgb_d = np.asarray(Image.open(drawing).convert("RGB"), dtype=np.float32)
    edges_r, edges_d = edges(rgb_r, mask_r), edges(rgb_d, mask_d)
    distance = ndimage.distance_transform_edt(~edges_d)
    return {"iou": round(float((mask_r & mask_d).sum() / (mask_r | mask_d).sum()), 3),
            "edge_drift": round(float(distance[edges_r].mean()), 2) if edges_r.any() else None,
            "render_area": round(float(mask_r.mean()), 3)}


def labelled():
    rows = []
    outside = load_json(ROOT / "runs" / "prefinal" / "outside" / "ratings.json")
    for card in load_json(ROOT / "runs" / "prefinal" / "outside" / "items.json")["cards"]:
        drawing = ROOT / card["image"]
        render = drawing.parent.parent / "models" / f"{drawing.stem.rsplit('_', 1)[0]}.png"
        rating = outside.get(f"{card['id']}|reviewer 2", {})
        if render.exists():
            rows.append({"id": card["id"], "file": card["image"], "render": str(render.relative_to(ROOT)),
                         "label": "broken" if rating.get("broken") else "ok", "rater": "outside", "grade": rating.get("grade")})
    ratings = load_json(ROOT / "runs" / "ratings.json")
    for run in ("western", "sci-fi", "horror"):
        new_run = ROOT / "runs" / f"{run}-blockout"
        history = load_json(new_run / "check.json")
        for brief in load_json(new_run / "briefs.json"):
            rating = ratings.get(f"redraw/new/{run}/{brief['source'].split('/')[1]}|me")
            if rating and history.get(brief["id"]):
                drawing = new_run / "tries" / f"{best_try(history[brief['id']])['try_id']}.png"
                rows.append({"id": rating["id"], "file": str(drawing.relative_to(ROOT)), "label": rating.get("works"),
                             "render": str((new_run / "models" / f"{brief['id']}.png").relative_to(ROOT)),
                             "rater": "producer", "grade": rating.get("grade")})
    for arm in ("blockout", "blockout2"):
        for drawing in sorted((ROOT / "runs" / "trial" / arm / "tries").glob("*.png")):
            rating = ratings.get(f"trial/{arm}/{drawing.stem}|me")
            render = ROOT / "runs" / "trial" / arm / f"{drawing.stem.split('_')[0]}.png"
            if rating and render.exists():
                rows.append({"id": rating["id"], "file": str(drawing.relative_to(ROOT)), "render": str(render.relative_to(ROOT)),
                             "label": rating.get("works"), "rater": "producer", "grade": rating.get("grade")})
    return rows


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    rows, labels = [], labelled()
    renders = {ROOT / row["render"] for row in labels}
    write_masks([{"id": render_key(r), "file": str(r.relative_to(ROOT))} for r in renders], "cuda", OUT / "derived" / "masks")
    for row in labels:
        result = score(ROOT / row["file"], ROOT / row["render"])
        if result:
            rows.append(row | result)
    save_json(OUT / "scores.json", rows)
    summary = {}
    for rater, bad, good in (("outside", ["broken"], ["ok"]), ("producer", ["no", "slight"], ["yes"]),
                             ("producer_no_only", ["no"], ["yes"])):
        group = [r for r in rows if r["rater"] == rater.split("_")[0]]
        for field in ("iou", "edge_drift"):
            a = [r[field] for r in group if r["label"] in bad and r[field] is not None]
            b = [r[field] for r in group if r["label"] in good and r[field] is not None]
            if a and b:
                statistic, p = mannwhitneyu(a, b, alternative="two-sided")
                summary[f"{rater}/{field}"] = {"bad_median": round(float(np.median(a)), 3), "good_median": round(float(np.median(b)), 3),
                                               "auc_bad_over_good": round(statistic / (len(a) * len(b)), 3),
                                               "p": round(float(p), 4), "n": [len(a), len(b)]}
    save_json(OUT / "summary.json", summary)
    broken = [r for r in rows if r["label"] in ("broken", "no")]
    tile = (SIZE[0] // 2, SIZE[1] // 2)
    sheet = Image.new("RGB", (tile[0] * len(broken), tile[1] * 2), "white")
    for index, row in enumerate(broken):
        for line, path in enumerate((row["render"], row["file"])):
            sheet.paste(Image.open(ROOT / path).convert("RGB").resize(tile, Image.LANCZOS), (index * tile[0], line * tile[1]))
    sheet.save(OUT / "broken.png")
    for key, value in summary.items():
        print(key, value)


if __name__ == "__main__":
    main()
