"""What logic picks a real card's backdrop color, and how is the backdrop built?

Follows experiments/colors.py (run it first: this reads runs/colors/colors.json). The producer asked to match the real
cards' color logic, complementary or otherwise. Each hypothesis is tested on the real cards against the same cards
with backdrops shuffled between them:
    hue        is the backdrop the hero's complement?
    warmth     does a warm hero get a cool backdrop, and the reverse?
    echo       does the backdrop repeat one of the hero's secondary colors?
    lightness  is the backdrop lighter or darker than the hero?
Then which family each category takes, the set-level tint and neighbours, and the backdrop's inner structure
(light-dark banding, hue drift, glow near the subject) for real cards and ours, categories 1-3.

    color_logic.py
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from collections import Counter, defaultdict

import numpy as np
from PIL import Image
from skimage import morphology

from common import DERIVED, ROOT, best_try, load_json
from measure import to_oklab

WARM = (330, 115)  # Oklab hue angles from pink through red, orange and yellow
SIZE = (215, 240)


def lch(hex_color):
    lab = to_oklab(np.array([int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]))
    return float(lab[0]), float(np.hypot(lab[1], lab[2])), float(np.degrees(np.arctan2(lab[2], lab[1])) % 360)


def gap(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def warm(hue):
    return hue >= WARM[0] or hue < WARM[1]


def structure(image, mask, category):
    """Backdrop light-dark spread (p90-p10), hue drift (circular sd, degrees) and glow near the subject."""
    rgb = np.asarray(Image.open(image).convert("RGB").resize(SIZE), dtype=float) / 255
    subject = np.asarray(Image.open(mask).convert("L").resize(SIZE)) > 127
    lab = to_oklab(rgb)
    light, chroma, hue = lab[..., 0], np.hypot(lab[..., 1], lab[..., 2]), np.arctan2(lab[..., 2], lab[..., 1])
    back = ~morphology.dilation(subject, morphology.disk(4))
    if category in ("2", "3"):
        back[SIZE[1] // 2:] = False  # the backdrop above the ground
    if back.sum() < 1500:
        return None
    turns = np.exp(1j * hue[back & (chroma > 0.04)])
    drift = float(np.degrees(np.sqrt(-2 * np.log(abs(turns.mean()))))) if turns.size else np.nan
    near = morphology.dilation(subject, morphology.disk(25)) & back
    corners = np.zeros_like(subject)
    corners[:30, :30] = corners[:30, -30:] = True
    if category == "1":
        corners[-30:, :30] = corners[-30:, -30:] = True
    corners &= back
    glow = light[near].mean() - light[corners].mean() if near.sum() > 100 and corners.sum() > 100 else np.nan
    return float(np.percentile(light[back], 90) - np.percentile(light[back], 10)), drift, glow


def ours():
    final = load_json(ROOT / "runs" / "final.json")
    for genre in ("western", "sci-fi", "horror"):
        for run, ids in ((f"{genre}-batch", None), (genre, final[genre])):
            history = load_json(ROOT / "runs" / run / "check.json")
            for brief in load_json(ROOT / "runs" / run / "briefs.json"):
                if (ids and brief["id"] not in ids) or not history.get(brief["id"]):
                    continue
                try_id = best_try(history[brief["id"]])["try_id"]
                yield brief["card"]["category"], ROOT / "runs" / run / "tries" / f"{try_id}.png", \
                    ROOT / "runs" / run / "derived" / "masks" / f"{try_id}.png"


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    rng = np.random.default_rng(0)
    rows = [row for row in load_json(ROOT / "runs" / "colors" / "colors.json") if row["group"] == "real"]
    measured = load_json(ROOT / "analysis" / "measurements.json")
    slots = {card["id"]: card["slot"] for card in load_json(ROOT / "analysis" / "cards.json")}
    hero = np.array([lch(row["hero"]) for row in rows])
    back = np.array([lch(row["backdrop"]) for row in rows])
    colored = hero[:, 1] >= 0.04

    print(f"Hero main colors near grey (Oklab chroma under 0.04): {(~colored).sum()} of {len(rows)}")
    real = np.array([gap(h, b) for h, b in zip(hero[colored, 2], back[colored, 2])])
    shuffled = np.array([gap(h, b) for _ in range(200) for h, b in zip(hero[colored, 2], rng.permutation(back[colored, 2]))])
    edges = [0, 30, 60, 90, 120, 150, 180]
    print("\nhue: gap from hero to backdrop, colored heroes")
    for low, high, r, s in zip(edges, edges[1:], np.histogram(real, edges)[0] / len(real),
                               np.histogram(shuffled, edges)[0] / len(shuffled)):
        print(f"  {low:3}-{high:3} degrees: real {r:.2f}, shuffled {s:.2f}")

    hero_warm = np.array([warm(h) for h in hero[:, 2]])
    back_warm = np.array([warm(h) for h in back[:, 2]])
    print(f"\nwarmth: warm heroes on a cool backdrop {1 - back_warm[colored & hero_warm].mean():.2f} "
          f"(n {(colored & hero_warm).sum()}); cool heroes on a warm backdrop {back_warm[colored & ~hero_warm].mean():.2f} "
          f"(n {(colored & ~hero_warm).sum()}); warm backdrops overall {back_warm.mean():.2f}")

    def secondaries(card_id):
        return [lch(p["hex"])[2] for p in measured[card_id]["color_palette"]["palette_subject"][1:]
                if lch(p["hex"])[1] > 0.06 and p["share"] >= 0.03]
    others = [secondaries(row["id"]) for row in rows]
    near = [min((gap(b, h) for h in o), default=None) for b, o in zip(back[:, 2], others)]
    near_shuffled = [min((gap(b, h) for h in o), default=None) for _ in range(100)
                     for b, o in zip(rng.permutation(back[:, 2]), others)]
    share = lambda values: np.mean([v < 20 for v in values if v is not None])
    print(f"echo: backdrop within 20 degrees of a secondary hero color: real {share(near):.2f}, "
          f"shuffled {share(near_shuffled):.2f}")
    print(f"lightness: |hero - backdrop| median real {np.median(abs(hero[:, 0] - back[:, 0])):.3f}, "
          f"shuffled {np.median([np.median(abs(hero[:, 0] - rng.permutation(back[:, 0]))) for _ in range(100)]):.3f}")

    print("\nBackdrop family by category, warm colored heroes")
    table = defaultdict(Counter)
    for row, h, w in zip(rows, hero, hero_warm):
        if h[1] >= 0.04 and w:
            table[row["category"]][row["backdrop_family"]] += 1
    for category in sorted(table):
        print(f"  category {category}: " + ", ".join(f"{n} {c}" for n, c in table[category].most_common()))
    print("Backdrop family by hero family, cool and grey heroes")
    table = defaultdict(Counter)
    for row in rows:
        if row["hero_family"] in ("green", "cyan", "blue", "purple", "neutral"):
            table[row["hero_family"]][row["backdrop_family"]] += 1
    for name in table:
        print(f"  {name}: " + ", ".join(f"{n} {c}" for n, c in table[name].most_common()))

    by_set = defaultdict(list)
    for row in rows:
        by_set[row["set"]].append((slots[row["id"]], row["backdrop_family"]))
    same, total, chance = 0, 0, []
    for cards in by_set.values():
        families = [f for _, f in sorted(cards)]
        same += sum(a == b for a, b in zip(families, families[1:]))
        total += len(families) - 1
        chance += [np.mean([a == b for a, b in zip(p, p[1:])]) for p in (rng.permutation(families) for _ in range(200))]
    print(f"\nNeighbouring slots share a backdrop family: real {same / total:.2f}, shuffled within the set {np.mean(chance):.2f}")
    print(f"Most used family per set covers {np.mean([Counter(f for _, f in v).most_common(1)[0][1] for v in by_set.values()]):.1f} of 10 cards")

    print("\nBackdrop structure, median: light-dark spread | hue drift | glow near the subject")
    groups = defaultdict(list)
    for card in load_json(ROOT / "analysis" / "cards.json"):
        category = card["form"]["staging"]["art_category"]
        if category in ("1", "2", "3"):
            groups[("real", category)].append(structure(ROOT / "materials" / "card_examples" / f"{card['id']}.png",
                                                        DERIVED / "masks" / f"{card['id']}.png", category))
    for category, image, mask in ours():
        if category in ("1", "2", "3"):
            groups[("ours", category)].append(structure(image, mask, category))
    for (group, category), values in sorted(groups.items()):
        values = np.array([v for v in values if v])
        print(f"  {group} category {category} ({len(values)}): {np.nanmedian(values[:, 0]):.3f} | "
              f"{np.nanmedian(values[:, 1]):.1f} | {np.nanmedian(values[:, 2]):+.3f}")


if __name__ == "__main__":
    main()
