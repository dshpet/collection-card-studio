"""Parameter loop on the forty twins: find a style parameter the redraws get wrong, change one line, measure again.

Each parameter is read two ways on every twin against its own real card, so content is equal:
    pixels   measure_card fields plus highlight, rim and silhouette measures, from the image, mask and normals
    eyes     Opus answers which of two cards has more of the parameter, asked twice with sides swapped.
             It never judges which card is right: the real card is the target, so a model's taste cannot invert it.
A parameter counts when the redraws sit on one side of their real cards in most twins (paired sign test) and the
readings agree with themselves.

    param.py read final                    read the twins of runs/twins40/final against their real cards
    param.py draw p1 --replace OLD NEW     redraw the twins with one style line changed, into runs/twins40/p1
    param.py read p1
    param.py compare final p1              which parameters moved, and how far toward the real cards
"""

import argparse
import random
from concurrent.futures import ThreadPoolExecutor

from common import DERIVED, ROOT, load_json, save_json

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.stats import binomtest, wilcoxon
from skimage import morphology

TWINS = ROOT / "runs" / "twins40"
OUT = ROOT / "runs" / "param"
BATCH = 5
QUESTIONS = {
    "highlight_breadth": "Which card's highlights are broader and softer, rather than small and sharp?",
    "highlight_white": "Which card's highlights are whiter, rather than tinted by the surface color?",
    "gloss": "Which object looks glossier, more lacquered or plastic?",
    "bevel": "Which object has rounder, more bevelled edges and corners, rather than crisper ones?",
    "inflation": "Which object looks more inflated or puffy, its forms swelling outward?",
    "surface_texture": "Which object's surfaces carry more texture and small surface marks?",
    "detail": "Which object has more small parts and details?",
    "form_contrast": "Which object has a stronger contrast between its lit side and its shaded side?",
    "shadow_color": "Which object's shadows are more saturated and colorful, rather than grey or dark?",
    "saturation": "Which card has more saturated colors overall?",
    "outline": "Which object has a darker edge or outline along its silhouette?",
    "thin_parts": "Which object's thin parts (handles, rims, legs, cords) are thicker?",
    "camera_height": "Which object is seen from a higher camera, looking down on it more?",
    "rendered": "Which card looks more like a 3D model rendered by a computer, rather than a painted illustration of one?",
}


def briefs():
    return load_json(TWINS / "briefs.json")


def records(label):
    """Real and redrawn record for each twin."""
    pairs = []
    for brief in briefs():
        drawn = TWINS / label / "tries" / f"{brief['id']}_1.png"
        if drawn.exists():
            pairs.append((brief["id"], {"id": brief["real"], "file": f"materials/card_examples/{brief['real']}.png",
                                        "derived": DERIVED},
                          {"id": f"{brief['id']}_1", "file": str(drawn.relative_to(ROOT)), "derived": TWINS / label / "derived"}))
    return pairs


def extra_fields(record):
    """Highlight shape, rim darkening and silhouette softness, which measure_card lacks."""
    from measure import to_oklab

    rgb = np.asarray(Image.open(ROOT / record["file"]).convert("RGB"), dtype=np.float64) / 255
    lab = to_oklab(rgb)
    lightness, chroma = lab[..., 0], np.hypot(lab[..., 1], lab[..., 2])
    mask = np.asarray(Image.open(record["derived"] / "masks" / f"{record['id']}.png").convert("L")) > 127
    interior = morphology.erosion(mask, morphology.disk(12))
    rim = mask & ~morphology.erosion(mask, morphology.disk(8)) & morphology.erosion(mask, morphology.disk(2))
    values = lightness[mask]
    peak = np.percentile(values, 99.5)
    top = mask & (lightness >= np.percentile(values, 99))
    boundary = mask & ~morphology.erosion(mask, morphology.disk(1))
    raw = ndimage.gaussian_gradient_magnitude(lightness, 0.7)
    blurred = ndimage.gaussian_gradient_magnitude(lightness, 2.0)
    fields = {
        "highlight_breadth": float((values > peak - 0.08).mean()),
        "highlight_tint": float(chroma[top].mean() / max(chroma[mask].mean(), 1e-6)),
        "highlight_edge": float(raw[top & ~morphology.erosion(top, morphology.disk(1))].mean()) if top.any() else None,
        "rim_darkening": float(lightness[interior].mean() - lightness[rim].mean()) if interior.any() else None,
        "silhouette_softness": float(blurred[boundary].mean() / max(raw[boundary].mean(), 1e-6)),
        "shadow_depth": float(np.percentile(values, 5)),
    }
    normals_path = record["derived"] / "normals" / f"{record['id']}.npy"
    if normals_path.exists() and interior.any():
        normals = np.load(normals_path).astype(np.float64)
        bend = np.sqrt(sum(np.square(np.gradient(normals, axis=axis)).sum(-1) for axis in (0, 1)))
        fields["surface_bend"] = float(np.median(bend[interior]))
        fields["facing_share"] = float((normals[..., 2][mask] > 0.9).mean())
    return fields


def pixel_fields(record):
    from drift import numbers
    from measure import measure_card

    fields = numbers(measure_card(record, record["derived"]))
    fields.update({f"extra.{k}": v for k, v in extra_fields(record).items()})
    return fields


def ensure_maps(label):
    from estimate import write_marigold, write_masks

    drawn = [r[2] for r in records(label)]
    missing = [r for r in drawn if not (r["derived"] / "masks" / f"{r['id']}.png").exists()]
    if missing:
        write_masks(missing, "cuda", drawn[0]["derived"] / "masks")
    missing = [r for r in drawn if not (r["derived"] / "normals" / f"{r['id']}.npy").exists()]
    if missing:
        write_marigold(missing, "cuda", drawn[0]["derived"])


def pair_sheet(real, drawn, real_first, out):
    font = ImageFont.load_default(30)
    sheet = Image.new("RGB", (430 * 2 + 12, 480), "white")
    for i, record in enumerate((real, drawn) if real_first else (drawn, real)):
        sheet.paste(Image.open(ROOT / record["file"]).convert("RGB").resize((430, 480), Image.LANCZOS), (i * 442, 0))
        draw = ImageDraw.Draw(sheet)
        draw.rectangle((i * 442, 0, i * 442 + 44, 44), fill="white")
        draw.text((i * 442 + 10, 4), "AB"[i], fill="black", font=font)
    sheet.save(out)
    return out


def eye_readings(label, rater, workers):
    from review import array, ask, strict, text

    folder = OUT / label
    (folder / "sheets").mkdir(parents=True, exist_ok=True)
    pairs = records(label)
    jobs = []
    for order in (0, 1):
        rng = random.Random(order)
        laid = []
        for twin, real, drawn in pairs:
            real_first = (rng.random() < 0.5) != bool(order)
            path = pair_sheet(real, drawn, real_first, folder / "sheets" / f"{twin}_{order}.png")
            laid.append((twin, path, "A" if real_first else "B"))
        jobs += [(order, i, laid[i:i + BATCH]) for i in range(0, len(laid), BATCH)]
    answer = {"type": "string", "enum": ["A", "B", "same"]}
    questions = "\n".join(f"- {key}: {question}" for key, question in QUESTIONS.items())

    def one(job):
        order, index, batch = job
        out = folder / "eyes" / f"{order}_{index:02d}.json"
        if out.exists():
            return load_json(out)
        listing = ", ".join(f"{twin} is image {i + 1}" for i, (twin, _, _) in enumerate(batch))
        prompt = ("You compare two mobile-game cards, A and B, that show the same object. Do not judge which is better "
                  "or which is real. For each property below, say which card has more of it, or same when you cannot "
                  f"see a difference. Look closely at the object.\n{questions}\nPairs: {listing}.")
        schema = strict({"pairs": array(strict({"pair": {"type": "string", "enum": [t for t, _, _ in batch]},
                                                **{key: answer for key in QUESTIONS}, "note": text()}))})
        result = ask(rater, prompt, [path for _, path, _ in batch], schema)
        if result:
            save_json(out, result)
        return result

    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(one, jobs))
    real_side = {(order, twin): side for order, _, batch in jobs for twin, _, side in batch}
    # +1: the redraw has more of it than its real card, -1 less, 0 same or no answer.
    readings = {}
    for (order, _, batch), result in zip(jobs, results):
        for item in (result or {}).get("pairs", []):
            side = real_side[(order, item["pair"])]
            for key in QUESTIONS:
                value = 0 if item[key] == "same" else (-1 if item[key] == side else 1)
                readings.setdefault(item["pair"], {}).setdefault(key, [None, None])[order] = value
    return readings


def read(label, rater, workers):
    ensure_maps(label)
    pixels = {}
    for twin, real, drawn in records(label):
        pixels[twin] = {"real": pixel_fields(real), "drawn": pixel_fields(drawn)}
    eyes = eye_readings(label, rater, workers)
    save_json(OUT / label / "readings.json", {"pixels": pixels, "eyes": eyes})
    summary = summarize(label)
    for row in summary[:16]:
        print(f"{row['source']:6} {row['field']:42} redraw more in {row['more']:>2}, less in {row['less']:>2}, "
              f"p {row['p']:.4f}" + (f", self-agreement {row['consistent']}" if "consistent" in row else ""))


def summarize(label):
    readings = load_json(OUT / label / "readings.json")
    rows = []
    fields = sorted({f for v in readings["pixels"].values() for f in v["real"]})
    for field in fields:
        diffs = [v["drawn"][field] - v["real"][field] for v in readings["pixels"].values()
                 if v["real"].get(field) is not None and v["drawn"].get(field) is not None]
        more, less = sum(d > 0 for d in diffs), sum(d < 0 for d in diffs)
        if more + less < 10:
            continue
        spread = np.std([v["real"][field] for v in readings["pixels"].values() if v["real"].get(field) is not None])
        rows.append({"source": "pixels", "field": field, "more": more, "less": less,
                     "p": float(wilcoxon(diffs).pvalue) if any(diffs) else 1.0,
                     "shift": float(np.median(diffs) / max(spread, 1e-9))})
    for key in QUESTIONS:
        votes = [v[key] for v in readings["eyes"].values() if key in v and None not in v[key]]
        agreed = [a for a, b in votes if a == b]
        more, less = sum(a > 0 for a in agreed), sum(a < 0 for a in agreed)
        rows.append({"source": "eyes", "field": key, "more": more, "less": less,
                     "p": float(binomtest(more, more + less).pvalue) if more + less else 1.0,
                     "consistent": f"{len(agreed)}/{len(votes)}"})
    rows.sort(key=lambda row: row["p"])
    save_json(OUT / label / "summary.json", rows)
    return rows


def draw_variant(label, replace, workers):
    from make_set import card_brief, draw_card
    import make_set

    old, new = replace
    assert old in make_set.STYLE, "the text to replace is not in the style"
    original = make_set.card_brief

    def changed(card):
        return original(card).replace(old, new)

    make_set.card_brief = changed
    run = TWINS / label
    run.mkdir(parents=True, exist_ok=True)
    save_json(run / "change.json", {"old": old, "new": new})
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(lambda brief: draw_card(run, brief, 1, [], True), briefs()))
    print("drew", sum(bool(d) for d in done), "of", len(done))


def compare(base, label):
    """For each parameter, the median distance to the real card in both runs, on twins drawn in both."""
    a, b = load_json(OUT / base / "readings.json"), load_json(OUT / label / "readings.json")
    twins = sorted(set(a["pixels"]) & set(b["pixels"]))
    rows = []
    for field in sorted(a["pixels"][twins[0]]["real"]):
        gaps = [(a["pixels"][t]["drawn"].get(field), b["pixels"][t]["drawn"].get(field), a["pixels"][t]["real"].get(field))
                for t in twins]
        gaps = [(x - r, y - r) for x, y, r in gaps if None not in (x, y, r)]
        if len(gaps) < 10:
            continue
        before, after = np.array(gaps).T
        closer = int((np.abs(after) < np.abs(before)).sum())
        rows.append({"field": field, "median_gap_before": float(np.median(before)), "median_gap_after": float(np.median(after)),
                     "closer": f"{closer}/{len(gaps)}", "p": float(wilcoxon(np.abs(after) - np.abs(before)).pvalue)})
    for key in QUESTIONS:
        signed = [(a["eyes"].get(t, {}).get(key), b["eyes"].get(t, {}).get(key)) for t in twins]
        before = [x[0] for x, y in signed if x and y and x[0] == x[1] and y[0] == y[1]]
        after = [y[0] for x, y in signed if x and y and x[0] == x[1] and y[0] == y[1]]
        rows.append({"field": f"eyes.{key}", "redraw_more_before": sum(v > 0 for v in before),
                     "redraw_less_before": sum(v < 0 for v in before), "redraw_more_after": sum(v > 0 for v in after),
                     "redraw_less_after": sum(v < 0 for v in after), "twins": len(before)})
    save_json(OUT / f"compare_{base}_{label}.json", rows)
    for row in sorted(rows, key=lambda r: r.get("p", 1)):
        print(row)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("read", "draw", "compare"))
    parser.add_argument("labels", nargs="+")
    parser.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"))
    parser.add_argument("--rater", default="claude-opus-5-5")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.mode == "read":
        read(args.labels[0], args.rater, args.workers)
    elif args.mode == "draw":
        draw_variant(args.labels[0], args.replace, args.workers)
    else:
        compare(*args.labels[:2])


if __name__ == "__main__":
    main()
