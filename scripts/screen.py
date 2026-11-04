"""Place a finished set into the game's collection window. The window is Playrix art, so results stay out of git.

    screen.py western --variant 1 --color blue
    screen.py western --cards v1_01 v2_01 ... --color blue      any ten cards of a run
"""

import argparse

from common import ROOT, best_try, load_json

import numpy as np
from PIL import Image, ImageDraw, ImageFont


TEMPLATES = {"purple": "3458764679659989297", "blue": "3458764679659989298", "orange": "3458764679659989299",
             "magenta": "3458764679659989300"}
SLOTS = [(x, 782) for x in (1410, 1973, 2534, 3096, 3657)] + [(x, 1559) for x in (1410, 1973, 2534, 3096, 3655)]
SLOT = (413, 470)
TITLE_BOX = (2240, 120, 3260, 320)
FONT = "DejaVuSans-Bold.ttf"


def erase(window, box):
    """Paint over baked-in text by blending each row between the colors just outside it."""
    x0, y0, x1, y1 = box
    pixels = np.asarray(window).astype(float)
    blend = np.linspace(0, 1, x1 - x0)[None, :, None]
    pixels[y0:y1, x0:x1] = pixels[y0:y1, x0 - 1:x0] * (1 - blend) + pixels[y0:y1, x1:x1 + 1] * blend
    return Image.fromarray(pixels.astype(np.uint8))


def fitted(text, width, size):
    while ImageFont.truetype(FONT, size).getlength(text) > width:
        size -= 2
    return ImageFont.truetype(FONT, size)


def compose(run, variant, color, cards=None):
    folder = ROOT / "runs" / run
    plan, history = load_json(folder / "plan.json"), load_json(folder / "check.json")
    briefs = {brief["id"]: brief for brief in load_json(folder / "briefs.json")}
    cards = cards or [f"v{variant}_{index:02d}" for index in range(1, 11)]
    window = Image.open(ROOT / f"materials/result_templates/{TEMPLATES[color]}.png").convert("RGBA")
    window = erase(window, TITLE_BOX)
    canvas = Image.new("RGBA", window.size, (0, 0, 0, 0))
    labels = []
    for card, (x, y) in zip(cards, SLOTS):
        best = best_try(history[card])
        art = Image.open(folder / "tries" / f"{best['try_id']}.png").convert("RGBA").resize(SLOT, Image.LANCZOS)
        canvas.paste(art, (x, y))
        plate = (x + 24, y + 484, x + SLOT[0] - 24, y + 570)
        window = erase(window, plate)
        labels.append((briefs[card]["card"]["name"].upper(), plate))
    canvas.alpha_composite(window)
    draw = ImageDraw.Draw(canvas)
    font = fitted(plan["title"].upper(), TITLE_BOX[2] - TITLE_BOX[0], 150)
    draw.text(((TITLE_BOX[0] + TITLE_BOX[2]) / 2, 220), plan["title"].upper(), font=font, anchor="mm",
              fill=(255, 205, 40), stroke_width=8, stroke_fill=(120, 60, 10))
    for name, box in labels:
        draw.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), name, font=fitted(name, box[2] - box[0] - 12, 44),
                  anchor="mm", fill="white")
    out = folder / f"screen_{variant}.png"
    canvas.crop((900, 0, 4600, 2529)).convert("RGB").resize((1850, 1264), Image.LANCZOS).save(out)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run")
    parser.add_argument("--variant", type=int, default=1)
    parser.add_argument("--color", choices=TEMPLATES, default="blue")
    parser.add_argument("--cards", nargs=10, help="ten card ids instead of a variant")
    args = parser.parse_args()
    print(compose(args.run, args.variant, args.color, args.cards))


if __name__ == "__main__":
    main()
