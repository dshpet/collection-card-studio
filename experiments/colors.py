"""Which backdrop colours do the real cards use, and do ours follow them?

Asked by the producer after the sand-coloured backdrop of the batch potion (horror-batch v1_07).

Measured per card: the backdrop is the background above the subject (top 35% of rows, the subject mask dilated), the
surface is the background in the bottom 20% of rows (used for categories 2 and 3, which stand on one), the hero is the
subject mask. Each gets its main colour by k-means in Oklab, as in scripts/measure.py, then a hue family
by HSV. Real cards, the batch (runs/<genre>-batch) and the earlier finals (runs/final.json) are measured the same way.

    colors.py     prints the tables and writes runs/colors/colors.json and runs/colors/sheet.png
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import colorsys
from collections import Counter, defaultdict

import numpy as np
from PIL import Image, ImageDraw
from skimage import morphology

from common import DERIVED, ROOT, best_try, load_json, save_json
from measure import palette, to_oklab

OUT = ROOT / "runs" / "colors"
GENRES = ("western", "sci-fi", "horror")
FAMILIES = ("red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink", "neutral")


def family(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hue, saturation, value = colorsys.rgb_to_hsv(*rgb)
    if saturation < 0.25 or value < 0.25:
        return "neutral"
    hue *= 360
    for name, top in (("red", 15), ("orange", 45), ("yellow", 70), ("green", 165), ("cyan", 200), ("blue", 250),
                      ("purple", 290), ("pink", 345)):
        if hue < top:
            return name
    return "red"


def oklch(hex_color):
    lab = to_oklab(np.array([int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]))
    return float(lab[0]), float(np.hypot(lab[1], lab[2])), float(np.degrees(np.arctan2(lab[2], lab[1])) % 360)


def colors(image, mask):
    rgb = np.asarray(Image.open(image).convert("RGB"), dtype=np.float64) / 255
    mask = np.asarray(Image.open(mask).convert("L").resize(rgb.shape[1::-1])) > 127
    lab = to_oklab(rgb)
    top = np.zeros_like(mask)
    top[: int(0.35 * len(mask))] = True
    backdrop = top & ~morphology.dilation(mask, morphology.disk(6))
    if backdrop.sum() < 2000:  # the subject fills the top: take every background pixel
        backdrop = ~mask
    bottom = np.zeros_like(mask)
    bottom[int(0.8 * len(mask)):] = True
    ground = bottom & ~morphology.dilation(mask, morphology.disk(6))
    back, hero = palette(rgb[backdrop], lab[backdrop], 2)[0]["hex"], palette(rgb[mask], lab[mask], 3)[0]["hex"]
    surface = palette(rgb[ground], lab[ground], 2)[0]["hex"] if ground.sum() > 2000 else back
    light, chroma, hue = oklch(back)
    gap, ground_gap = abs(hue - oklch(hero)[2]), abs(hue - oklch(surface)[2])
    return {"backdrop": back, "hero": hero, "surface": surface, "backdrop_family": family(back),
            "hero_family": family(hero), "surface_family": family(surface), "lightness": round(light, 3),
            "chroma": round(chroma, 3), "hue_gap": round(min(gap, 360 - gap), 1),
            "surface_gap": round(min(ground_gap, 360 - ground_gap), 1),
            "surface_lightness_gap": round(light - oklch(surface)[0], 3)}


def ours():
    final = load_json(ROOT / "runs" / "final.json")
    for genre in GENRES:
        for run, ids in ((f"{genre}-batch", None), (genre, final[genre])):
            folder = ROOT / "runs" / run
            history = load_json(folder / "check.json")
            for brief in load_json(folder / "briefs.json"):
                if (ids is not None and brief["id"] not in ids) or not history.get(brief["id"]):
                    continue
                try_id = best_try(history[brief["id"]])["try_id"]
                yield {"group": "batch" if ids is None else "earlier final", "run": run, "name": brief["card"]["name"],
                       "category": brief["card"]["category"], "planned": brief["card"]["backdrop_colors"],
                       **colors(folder / "tries" / f"{try_id}.png", folder / "derived" / "masks" / f"{try_id}.png")}


def table(rows, title):
    count = Counter(row["backdrop_family"] for row in rows)
    print(f"\n{title} ({len(rows)} cards): backdrop family share, mean Oklab lightness and chroma")
    for name in FAMILIES:
        picked = [row for row in rows if row["backdrop_family"] == name]
        if picked:
            print(f"  {name:8} {count[name] / len(rows):5.0%}  L {np.mean([r['lightness'] for r in picked]):.2f}"
                  f"  C {np.mean([r['chroma'] for r in picked]):.3f}")


def grounds(rows, title):
    """Categories 2 and 3: is the surface a different colour from the backdrop?"""
    rows = [row for row in rows if row["category"] in ("2", "3")]
    same = sum(row["surface_family"] == row["backdrop_family"] for row in rows)
    print(f"  {title}, categories 2-3 ({len(rows)}): surface in the backdrop's family {same}, "
          f"median hue gap surface to backdrop {np.median([r['surface_gap'] for r in rows]):.0f}, "
          f"median lightness gap {np.median([abs(r['surface_lightness_gap']) for r in rows]):.2f}")


def spread(rows, key, title):
    by_set = defaultdict(list)
    for row in rows:
        by_set[row[key]].append(row["backdrop_family"])
    print(f"  {title}: distinct backdrop families per set {np.mean([len(set(v)) for v in by_set.values()]):.1f}"
          f" of {np.mean([len(v) for v in by_set.values()]):.1f} cards, most repeated family "
          f"{np.mean([Counter(v).most_common(1)[0][1] for v in by_set.values()]):.1f}")


def sheet(groups, path):
    size, pad, per_row = 36, 4, 32
    rows = sum(-(-len(items) // per_row) for _, items in groups)
    image = Image.new("RGB", (per_row * (size + pad) + pad, rows * (size + pad) + len(groups) * 18 + pad), "white")
    draw, y = ImageDraw.Draw(image), pad
    for title, items in groups:
        draw.text((pad, y), title, fill="black")
        y += 16
        for index, item in enumerate(sorted(items, key=lambda r: (FAMILIES.index(r["backdrop_family"]), r["lightness"]))):
            x = pad + (index % per_row) * (size + pad)
            top = y + (index // per_row) * (size + pad)
            draw.rectangle((x, top, x + size, top + size), fill=item["backdrop"])
            draw.ellipse((x + 11, top + 11, x + size - 11, top + size - 11), fill=item["hero"], outline="white")
        y += -(-len(items) // per_row) * (size + pad) + 2
    image.save(path)


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    real = []
    for card in load_json(ROOT / "analysis" / "cards.json"):
        file = ROOT / "materials" / "card_examples" / f"{card['id']}.png"
        real.append({"group": "real", "id": card["id"], "name": card["name"], "set": card["set_id"],
                     "category": card["form"]["staging"]["art_category"], "pattern": card["form"]["backdrop"]["pattern"],
                     **colors(file, DERIVED / "masks" / f"{card['id']}.png")})
    mine = list(ours())
    save_json(OUT / "colors.json", real + mine)

    table(real, "Real cards")
    for category in sorted({row["category"] for row in real}):
        picked = [row for row in real if row["category"] == category]
        top = Counter(row["backdrop_family"] for row in picked).most_common(4)
        print(f"  category {category} ({len(picked)}): " + ", ".join(f"{n} {c}" for n, c in top)
              + f"; L {np.mean([r['lightness'] for r in picked]):.2f}, C {np.mean([r['chroma'] for r in picked]):.3f}")
    print("\nReal cards: backdrop family by hero family (rows hero, counts)")
    pairs = defaultdict(Counter)
    for row in real:
        pairs[row["hero_family"]][row["backdrop_family"]] += 1
    for hero in FAMILIES:
        if pairs[hero]:
            print(f"  {hero:8} " + ", ".join(f"{n} {c}" for n, c in pairs[hero].most_common()))
    print(f"\nHue gap, hero to backdrop (Oklab degrees): real median {np.median([r['hue_gap'] for r in real]):.0f}")
    spread(real, "set", "Real sets")
    grounds(real, "Real")
    print(f"  Real backdrop chroma, all cards: mean {np.mean([r['chroma'] for r in real]):.3f}")
    light, chroma = np.array([r["lightness"] for r in real]), np.array([r["chroma"] for r in real])
    low_l, low_c = np.percentile(light, 5), np.percentile(chroma, 5)
    print(f"Real backdrops: lightness 5th-95th {low_l:.2f}-{np.percentile(light, 95):.2f}, "
          f"chroma 5th-95th {low_c:.3f}-{np.percentile(chroma, 95):.3f}")

    for group in ("earlier final", "batch"):
        rows = [row for row in mine if row["group"] == group]
        table(rows, f"Ours, {group}")
        print(f"  hue gap median {np.median([r['hue_gap'] for r in rows]):.0f}, "
              f"backdrop chroma mean {np.mean([r['chroma'] for r in rows]):.3f}")
        spread(rows, "run", f"{group} sets")
        grounds(rows, group)
        for row in rows:
            if row["category"] in ("2", "3") and row["surface_family"] == row["backdrop_family"]:
                print(f"    surface like backdrop: {row['run']} {row['name']} ({row['backdrop_family']})")
        for row in rows:
            flags = [f for f, bad in (("dull", row["chroma"] < low_c), ("dark", row["lightness"] < low_l)) if bad]
            if flags:
                print(f"  outside the real range ({', '.join(flags)}): {row['run']} {row['name']}, planned "
                      f"'{row['planned']}', measured {row['backdrop']} L {row['lightness']:.2f} C {row['chroma']:.3f}")
    sheet([("Real cards: backdrop square, main hero colour dot, by family", real),
           ("Earlier finals", [r for r in mine if r["group"] == "earlier final"]),
           ("Batch", [r for r in mine if r["group"] == "batch"])], OUT / "sheet.png")
    print("\n->", OUT / "colors.json", OUT / "sheet.png")


if __name__ == "__main__":
    main()
