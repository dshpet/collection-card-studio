"""Does edge-preserving smoothing of the full-size drawings take out the grain the outside rater saw?

She found ours "grainier and more textured" than the real cards: material texture on simple shapes, where real cards
keep large surfaces smooth. measure.py's micro_texture and detail fields mix that texture with the edges of parts, so
three fields here leave out pixels near strong edges (Sobel > 0.08, as measure.py's edge lines, widened by 2 px):
fine texture |L - blur(L, 1)|, mottle |blur(L, 1) - blur(L, 3)|, and the share of flat pixels (local deviation of
lightness under 0.006). Measured on the 81 pre-final cards she graded and the 160 real cards, at 430x480.

Then each drawing is smoothed at full size (1187x1325) and downscaled as draw() does: a self-guided filter (He et al.
2013) at two strengths and OpenCV's domain-transform filter (Gastal and Oliveira 2011). Part edges kept is the mean
Sobel strength on the unsmoothed card's interior edge pixels, after over before. Also: do briefs that name a material
(felt, leather, wood...) come out more textured?

With --twins, the same arms on the forty final-style twins, judged as the project judges a change: CSD to each twin's
own real card, and the texture fields against that card, paired. It also gives each style round's flat share against
the twins' own real cards at three thresholds, and whether that gap tells which twins the producer caught blind.
--flat does the flat share alone for any twins40 rounds, each paired against the first round named. --pairs scores it
as a judge on the pairs the producer decided, as experiments/prefer.py scores CSD.

    smooth_check.py                  -> runs/smooth_check/summary.json, cards.json, sheets/
    smooth_check.py --twins          -> runs/smooth_check/twins.json
    smooth_check.py --flat n0 ns nc  -> runs/smooth_check/flat-n0-ns-nc.json
    smooth_check.py --pairs          -> runs/smooth_check/pairs.json
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import re

from common import ANALYSIS, ROOT, SIZE, cards, load_json, save_json
from measure import measure_card, to_oklab

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.stats import mannwhitneyu, spearmanr, wilcoxon
from skimage import filters, morphology

OUT = ROOT / "runs" / "smooth_check"
MATERIAL = re.compile(r"\b(felt|leather|wool|woolen|knit|fabric|cloth|canvas|linen|velvet|silk|lace|tweed|burlap|"
                      r"suede|fur|furry|straw|wicker|wood|wooden|grain|parchment|paper|rope|hemp|cotton|denim)\b", re.I)


def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255


def load_mask(path):
    return np.asarray(Image.open(path).convert("L")) > 127


def guided(image, radius, eps):
    """Self-guided filter per channel, on [0, 1] floats."""
    box = lambda x: cv2.boxFilter(x, -1, (2 * radius + 1, 2 * radius + 1))
    mean = box(image)
    variance = box(image * image) - mean * mean
    a = variance / (variance + eps)
    b = mean - a * mean
    return box(a) * image + box(b)


ARMS = {
    "none": lambda rgb: rgb,
    "guided_light": lambda rgb: guided(rgb, 4, 0.0004),
    "guided_strong": lambda rgb: guided(rgb, 8, 0.0016),
    "domain": lambda rgb: cv2.edgePreservingFilter((rgb * 255).astype(np.uint8), flags=cv2.RECURS_FILTER,
                                                   sigma_s=30, sigma_r=0.12).astype(np.float32) / 255,
}


def texture_fields(rgb, mask):
    lightness = to_oklab(rgb)[..., 0]
    edges = morphology.dilation(filters.sobel(lightness) > 0.08, morphology.disk(2))
    interior = morphology.erosion(mask, morphology.disk(8))
    surface = interior & ~edges
    fine = np.abs(lightness - ndimage.gaussian_filter(lightness, 1))
    mottle = np.abs(ndimage.gaussian_filter(lightness, 1) - ndimage.gaussian_filter(lightness, 3))
    local = np.sqrt(np.maximum(ndimage.uniform_filter(lightness ** 2, 3) - ndimage.uniform_filter(lightness, 3) ** 2, 0))
    return {"fine_off_edges": float(fine[surface].mean()), "mottle_off_edges": float(mottle[surface].mean()),
            "flat_share": float((local[surface] < 0.006).mean()), "surface_share": float(surface.sum() / max(interior.sum(), 1))}


def part_edges(lightness, mask):
    return (filters.sobel(lightness) > 0.08) & morphology.erosion(mask, morphology.disk(4))


def ours():
    items = load_json(ROOT / "runs" / "prefinal" / "outside" / "items.json")["cards"]
    ratings = load_json(ROOT / "runs" / "prefinal" / "outside" / "ratings.json")
    rows = []
    for card in items:
        path = ROOT / card["image"]
        run = path.parent.parent
        brief = next(b for b in load_json(run / "briefs.json") if b["id"] == path.stem.rsplit("_", 1)[0])
        rating = ratings.get(f"{card['id']}|reviewer 2", {})
        rows.append({"id": card["id"], "file": card["image"], "full": str((run / "full" / path.name).relative_to(ROOT)),
                     "mask": run / "derived" / "masks" / path.name, "grade": rating.get("grade"),
                     "material_named": bool(MATERIAL.search(f"{brief['card']['subject']} {brief['card'].get('hero_colors', '')}")),
                     "words": sorted({m.lower() for m in MATERIAL.findall(f"{brief['card']['subject']} {brief['card'].get('hero_colors', '')}")})})
    return rows


def auc(a, b):
    statistic, p = mannwhitneyu(a, b, alternative="two-sided")
    return round(statistic / (len(a) * len(b)), 3), round(float(p), 4)


def surface_deviation(rgb, mask):
    """Local deviation of lightness (3x3) on surface pixels: inside the subject, away from strong edges."""
    lightness = to_oklab(rgb)[..., 0]
    surface = morphology.erosion(mask, morphology.disk(8)) & ~morphology.dilation(filters.sobel(lightness) > 0.08, morphology.disk(2))
    return np.sqrt(np.maximum(ndimage.uniform_filter(lightness ** 2, 3) - ndimage.uniform_filter(lightness, 3) ** 2, 0))[surface]


def real_surface(card_id):
    """surface_deviation of a real card."""
    return surface_deviation(load_rgb(ROOT / "materials" / "card_examples" / f"{card_id}.png"),
                             load_mask(ANALYSIS / "derived" / "masks" / f"{card_id}.png"))


def flat_gaps(styles=("old", "final", "r3", "r9")):
    """Flat share of each twin minus its own real card, by style round and flatness threshold, on the drawn cards.
    A round without masks gets BiRefNet masks in this script's own folder."""
    from estimate import write_masks

    result, per_style = {}, {}
    for style in styles:
        tries = sorted((ROOT / "runs" / "twins40" / style / "tries").glob("m*_1.png"))
        if not (ROOT / "runs" / "twins40" / style / "derived" / "masks").exists():
            write_masks([{"id": t.stem, "file": str(t.relative_to(ROOT))} for t in tries], "cuda",
                        OUT / "derived" / f"masks-{style}")
        gaps = {t: [] for t in (0.004, 0.006, 0.01)}
        for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json"):
            drawn = ROOT / "runs" / "twins40" / style / "tries" / f"{brief['id']}_1.png"
            mask = drawn.parent.parent / "derived" / "masks" / drawn.name
            mask = mask if mask.exists() else OUT / "derived" / f"masks-{style}" / drawn.name
            if not (drawn.exists() and mask.exists()):
                continue
            ours, real = surface_deviation(load_rgb(drawn), load_mask(mask)), real_surface(brief["real"])
            for threshold in gaps:
                gaps[threshold].append(float((ours < threshold).mean() - (real < threshold).mean()))
            per_style.setdefault(style, {})[brief["id"]] = gaps[0.004][-1]
        result[style] = {str(t): {"median": round(float(np.median(g)), 3), "twin_flatter": f"{sum(x > 0 for x in g)}/{len(g)}",
                                  "p": round(float(wilcoxon(g).pvalue), 4)} for t, g in gaps.items()}
        # Twins whose brief names a material (felt, leather, wood...) against the rest, at 0.004
        named = {b["id"] for b in load_json(ROOT / "runs" / "twins40" / "briefs.json")
                 if MATERIAL.search(f"{b['card']['subject']} {b['card'].get('hero_colors', '')}")}
        split = [[g for i, g in per_style[style].items() if (i in named) == want] for want in (True, False)]
        result[style]["material_named"] = {"n": [len(x) for x in split], "median": [round(float(np.median(x)), 3) for x in split],
                                           "auc_p": auc(*split)}
    control = per_style[styles[0]]
    for style in styles[1:]:  # paired against the first round named: is the twin's flat share nearer its real card?
        shared = sorted(set(control) & set(per_style[style]))
        nearer = [abs(control[i]) - abs(per_style[style][i]) for i in shared]
        result[style][f"nearer_than_{styles[0]}"] = {"twins": f"{sum(n > 0 for n in nearer)}/{len(nearer)}",
                                                     "p": round(float(wilcoxon(nearer).pvalue), 4)}
    return result


def caught():
    """Does a twin's flat-share gap tell which twins the producer caught blind (final and old style)?"""
    ratings = load_json(ROOT / "runs" / "ratings.json")
    gaps = {True: [], False: []}
    for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json"):
        for style in ("final", "old"):
            rating = ratings.get(f"twin/{style}/{brief['id']}|me", {})
            if rating.get("answer") not in ("A", "B"):  # "neither" is no pick
                continue
            drawn = ROOT / "runs" / "twins40" / style / "tries" / f"{brief['id']}_1.png"
            ours = surface_deviation(load_rgb(drawn), load_mask(drawn.parent.parent / "derived" / "masks" / drawn.name))
            real = real_surface(brief["real"])
            gaps[rating["correct"]].append(float((ours < 0.004).mean() - (real < 0.004).mean()))
    return {"caught_median": round(float(np.median(gaps[True])), 3), "missed_median": round(float(np.median(gaps[False])), 3),
            "n": [len(gaps[True]), len(gaps[False])], "auc_p": auc(gaps[True], gaps[False])}


def pairs():
    """The flat share as a pairwise judge, on the pairs of experiments/prefer.py the producer decided (raw CSD: 128 of
    218). Nearer: the drawing whose flat share is nearer its real cards' wins. Flatter: the flatter drawing wins."""
    from estimate import write_masks
    from scipy.stats import binomtest

    rows = load_json(ROOT / "runs" / "prefer" / "pairs.json")
    drawn = sorted({row[side] for row in rows for side in "AB"})
    mask_of = lambda path: (ROOT / path).parent.parent / "derived" / "masks" / Path(path).name
    missing = [{"id": path.replace("/", "_")[:-4], "file": path} for path in drawn if not mask_of(path).exists()]
    write_masks(missing, "cuda", OUT / "derived" / "masks-pairs")
    flat = {}
    for path in drawn:
        mask = mask_of(path) if mask_of(path).exists() else OUT / "derived" / "masks-pairs" / f"{path.replace('/', '_')[:-4]}.png"
        flat[path] = float((surface_deviation(load_rgb(ROOT / path), load_mask(mask)) < 0.004).mean())
    for path in sorted({r for row in rows for r in row["references"]}):
        mask = ANALYSIS / "derived" / "masks" / f"{Path(path).stem}.png"
        flat[path] = float((surface_deviation(load_rgb(ROOT / path), load_mask(mask)) < 0.004).mean())
    result = {}
    for name, group in (("decided", [r for r in rows if not r["lesson"]]),
                        ("texture_lessons", [r for r in rows if r["lesson"] and "texture" in r["lesson"]])):
        for judge in ("nearer", "flatter"):
            hits, kinds = [], {}
            for row in group:
                target = np.mean([flat[r] for r in row["references"]])
                a, b = flat[row["A"]], flat[row["B"]]
                pick = ("A" if abs(a - target) < abs(b - target) else "B") if judge == "nearer" else ("A" if a > b else "B")
                hits.append(pick == row["user"])
                kinds.setdefault(row["object"].split("/")[0], []).append(pick == row["user"])
            result[f"{name}/{judge}"] = {"agree": f"{sum(hits)}/{len(hits)}", "p": round(float(binomtest(sum(hits), len(hits)).pvalue), 4),
                                         "by_kind": {k: f"{sum(v)}/{len(v)}" for k, v in sorted(kinds.items())}}
    return result


def twins():
    from embed import MODELS, load_csd
    import torch

    encode = load_csd(MODELS["csd"])
    folder = OUT / "derived" / "twins"
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json"):
        drawn = ROOT / "runs" / "twins40" / "final" / "full" / f"{brief['id']}_1.png"
        mask_path = ROOT / "runs" / "twins40" / "final" / "derived" / "masks" / f"{brief['id']}_1.png"
        real_file = ROOT / "materials" / "card_examples" / f"{brief['real']}.png"
        if not (drawn.exists() and mask_path.exists()):
            continue
        real_mask = load_mask(ANALYSIS / "derived" / "masks" / f"{brief['real']}.png")
        row = {"id": brief["id"], "real": texture_fields(load_rgb(real_file), real_mask)}
        mask, full = load_mask(mask_path), load_rgb(drawn)
        images = [Image.open(real_file).convert("RGB")]
        for arm, smooth in ARMS.items():
            small = Image.fromarray((np.clip(smooth(full), 0, 1) * 255).round().astype(np.uint8)).resize(SIZE, Image.LANCZOS)
            small.save(folder / f"{brief['id']}-{arm}.png")
            row[arm] = texture_fields(np.asarray(small, dtype=np.float32) / 255, mask)
            images.append(small)
        with torch.inference_mode():
            vectors = torch.nn.functional.normalize(encode(images).float(), dim=-1).cpu().numpy()
        for index, arm in enumerate(ARMS):
            row[arm]["csd"] = float(vectors[0] @ vectors[index + 1])
        rows.append(row)
    result = {"n": len(rows), "flat_share_by_style": flat_gaps(), "caught": caught(), "none_minus_real": {}}
    for key in ("fine_off_edges", "flat_share"):
        gaps = [r["none"][key] - r["real"][key] for r in rows]
        result["none_minus_real"][key] = {"median": round(float(np.median(gaps)), 4), "above": f"{sum(g > 0 for g in gaps)}/{len(gaps)}",
                                          "p": round(float(wilcoxon(gaps).pvalue), 4)}
    for arm in ARMS:
        if arm == "none":
            continue
        gain = [r[arm]["csd"] - r["none"]["csd"] for r in rows]
        entry = {"csd_median": round(float(np.median([r[arm]["csd"] for r in rows])), 4),
                 "csd_none_median": round(float(np.median([r["none"]["csd"] for r in rows])), 4),
                 "csd_closer": f"{sum(g > 0 for g in gain)}/{len(gain)}", "csd_p": round(float(wilcoxon(gain).pvalue), 4)}
        for key in ("fine_off_edges", "flat_share"):
            closer = [abs(r[arm][key] - r["real"][key]) < abs(r["none"][key] - r["real"][key]) for r in rows]
            entry[f"{key}_closer_to_own_real"] = f"{sum(closer)}/{len(closer)}"
        result[arm] = entry
    save_json(OUT / "twins.json", result)
    print(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--twins", action="store_true", help="the arms on the forty final-style twins, by CSD")
    parser.add_argument("--flat", nargs="+", metavar="ROUND", help="flat share against the real cards for these twins40 rounds")
    parser.add_argument("--pairs", action="store_true", help="the flat share as a judge on the producer's decided pairs")
    options = parser.parse_args()
    if options.flat:
        result = flat_gaps(options.flat)
        save_json(OUT / f"flat-{'-'.join(options.flat)}.json", result)
        print(result)
        return
    if options.pairs:
        result = pairs()
        save_json(OUT / "pairs.json", result)
        print(result)
        return
    if options.twins:
        return twins()
    measured = load_json(ANALYSIS / "measurements.json")
    real = []
    for record in cards():
        mask_path = ANALYSIS / "derived" / "masks" / f"{record['id']}.png"
        real.append(texture_fields(load_rgb(ROOT / record["file"]), load_mask(mask_path))
                    | {k: measured[record["id"]]["surface_finish"][k] for k in ("micro_texture", "detail_subject")})
    rows = ours()
    (OUT / "derived" / "masks").mkdir(parents=True, exist_ok=True)
    for row in rows:
        mask, full = load_mask(row["mask"]), load_rgb(ROOT / row["full"])
        base = None
        for arm, smooth in ARMS.items():
            small = Image.fromarray((np.clip(smooth(full), 0, 1) * 255).round().astype(np.uint8)).resize(SIZE, Image.LANCZOS)
            name = row["id"].replace("/", "_")
            rgb = np.asarray(small, dtype=np.float32) / 255
            fields = texture_fields(rgb, mask)
            Image.fromarray(mask.astype(np.uint8) * 255).save(OUT / "derived" / "masks" / f"{name}-{arm}.png")
            path = OUT / "derived" / f"{name}-{arm}.png"
            small.save(path)
            finish = measure_card({"id": f"{name}-{arm}", "file": str(path.relative_to(ROOT))}, derived=OUT / "derived")["surface_finish"]
            fields |= {k: finish[k] for k in ("micro_texture", "detail_subject")}
            lightness = to_oklab(rgb)[..., 0]
            if base is None:
                base = (lightness, part_edges(lightness, mask))
            fields["part_edges_kept"] = float(filters.sobel(lightness)[base[1]].mean() / filters.sobel(base[0])[base[1]].mean())
            row[arm] = {k: round(v, 4) for k, v in fields.items()}
    keys = ["fine_off_edges", "mottle_off_edges", "flat_share", "micro_texture", "detail_subject"]
    summary = {"n": {"ours": len(rows), "real": len(real)}, "real_median": {k: round(float(np.median([r[k] for r in real])), 4) for k in keys}}
    for arm in ARMS:
        summary[arm] = {k: {"median": round(float(np.median([r[arm][k] for r in rows])), 4),
                            "auc_ours_over_real": auc([r[arm][k] for r in rows], [r[k] for r in real])} for k in keys}
        summary[arm]["part_edges_kept"] = round(float(np.median([r[arm]["part_edges_kept"] for r in rows])), 3)
    named, plain = [r for r in rows if r["material_named"]], [r for r in rows if not r["material_named"]]
    summary["material_named"] = {"n": [len(named), len(plain)], **{k: {
        "median_named_plain": [round(float(np.median([r["none"][k] for r in group])), 4) for group in (named, plain)],
        "auc_named_over_plain": auc([r["none"][k] for r in named], [r["none"][k] for r in plain])} for k in keys}}
    graded = [r for r in rows if r["grade"]]
    summary["grade_spearman"] = {k: round(float(spearmanr([r["none"][k] for r in graded],
                                                          [r["grade"] for r in graded]).statistic), 3) for k in keys}
    save_json(OUT / "cards.json", [{k: (str(v) if isinstance(v, Path) else v) for k, v in r.items()} for r in rows])
    save_json(OUT / "summary.json", summary)
    # A sheet per card for the most textured dozen: arms side by side, then a 2x crop of the centre
    (OUT / "sheets").mkdir(exist_ok=True)
    for row in sorted(rows, key=lambda r: -r["none"]["fine_off_edges"])[:12]:
        name = row["id"].replace("/", "_")
        tiles = [Image.open(OUT / "derived" / f"{name}-{arm}.png") for arm in ARMS]
        sheet = Image.new("RGB", (SIZE[0] * len(tiles), SIZE[1] * 2), "white")
        for index, tile in enumerate(tiles):
            sheet.paste(tile, (index * SIZE[0], 0))
            sheet.paste(tile.crop((107, 120, 322, 360)).resize(SIZE, Image.NEAREST), (index * SIZE[0], SIZE[1]))
        sheet.save(OUT / "sheets" / f"{name}.png")
    print(summary)


if __name__ == "__main__":
    main()
