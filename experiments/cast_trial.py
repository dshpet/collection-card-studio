"""Cast trial: can the game's own characters appear on new cards and stay themselves?

Six character cards for the film genres, two draws per arm:
    direct   the card in one go, with real cutouts of the character as references
    paste    the character pre-generated alone in its outfit and pose (scripts/cast.py), the setting drawn empty, the
             character pasted in at the real cards' layout, then redrawn once with small corrections
    paste2   the same figures and settings, the body (not its props) scaled to the real cards' size and cut by the
             bottom edge, and the redraw allowed to adjust the pose where it touches the setting
    figure   the card in one go, with the pre-generated figure as the character reference
Identity is measured by cutting the character out of each result with SAM 3 and comparing it with the real cutouts
in DINOv2, against the other cast members as a baseline.

    cast_trial.py draw
    cast_trial.py measure     identity, by SAM 3 cutouts against the real cutouts in DINOv2
    cast_trial.py judge       the art director's pairwise preference between arms
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, ROOT, SIZE, load_json, save_json

import numpy as np
from PIL import Image

from cast import CAST, GREY, LIBRARY, LOOKS, identity_references, on_grey
from draw import draw

RUN = ROOT / "runs" / "cast_trial"
ARMS = ("direct", "paste", "paste2", "figure")
DRAWS = 2
BOTTOM = 0.97  # median bottom of the one-character boxes in analysis/cast.json
# paste2: body height and bottom edge of the card, from analysis/cast.json (median one-character box 68% high, its
# bottom cut by the card edge on 10 of 23 cards). Pairs keep their own sizes.
PASTE2 = {"height": 0.74, "bottom": 1.03}
FIGURE = """The attached images show one character from a mobile game, cut out of real cards. Draw the same character again, unchanged: the same face, eyes, {look}, body shape, proportions, colors and rendering.
{action}
Full body, alone, on a transparent background. Draw only what is named. No shadow, no ground, no text."""
PLATE = """The attached images are real cards from the game. Draw the setting of one new card that could sit beside them unnoticed: the same rendering, lighting, finish, color and level of detail.
Setting: {setting}
There is no character in it. Keep the middle of the card open, where a character will stand. The setting is a real place, simple and calm: a few large soft shapes. Draw only what is named. No text, letters, numbers, frame, border or watermark."""
BLEND = """The first images are real cards from the game. The last one is a draft of a new card: a character was pasted onto a drawn setting. Redraw the draft as one finished card that could sit beside the real cards unnoticed.
Make only small corrections: light and color on the character from the setting's light, a soft contact shadow where it touches the ground, clean edges, and {interaction}
Keep the character exactly: its face, body, proportions, colors and outfit. Keep the setting, the camera and the framing."""
DIRECT = """The first images show {who} from a mobile game, cut out of real cards. The last images are real cards from the game. Draw one new card that could sit beside the real cards unnoticed: the same rendering, lighting, finish, color and level of detail. {same} stays exactly the same: face, body, proportions and colors.
Subject: {subject}
Setting: {setting}
The characters are central and large. The setting is a real place, simple and calm: a few large soft shapes. Draw only what is named. No text, letters, numbers, frame, border or watermark."""
CARDS = [
    {"id": "western_pig", "genre": "western", "cast": {"pig": {
        "action": "The pig wears a brown cowboy hat and swings a rope lasso over its head; the loop has caught its own curly tail. It looks back at it, surprised.",
        "center": 0.47, "height": 0.72}},
     "subject": "The pig in a brown cowboy hat swings a rope lasso, and the loop has caught its own curly tail. It looks back at it, surprised.",
     "setting": "a dusty ranch corral with a wooden rail fence, sandy ground and orange desert mesas under a clear blue sky.",
     "interaction": "the rope reads as one rope from the pig's hoof to the loop."},
    {"id": "western_man", "genre": "western", "cast": {"man": {
        "action": "The man is dressed as a sheriff: a tan cowboy hat, a brown leather vest and a plain gold star badge. He leans on one elbow and sips a glass of milk, eyes closed with a big satisfied smile.",
        "center": 0.47, "height": 0.80}},
     "subject": "The man, dressed as a sheriff in a tan cowboy hat, a brown vest and a plain gold star badge, leans on the bar and sips a glass of milk, eyes closed with a big satisfied smile.",
     "setting": "the inside of a wooden saloon: a polished wooden bar counter in front, shelves of bottles and a swinging door behind, warm lamp light.",
     "interaction": "his elbow rests on the bar counter."},
    {"id": "scifi_sheep", "genre": "sci-fi", "cast": {"sheep": {
        "action": "The sheep wears a white space suit with an open round glass helmet, and its curly fleece puffs out of the helmet. It floats weightless, legs spread, reaching with one hoof, with a delighted face.",
        "center": 0.45, "height": 0.70}},
     "subject": "The sheep in a white space suit floats weightless, its curly fleece puffing out of the open glass helmet; it reaches with one hoof for a floating orange carrot.",
     "setting": "inside a round spaceship cabin with a large round porthole showing stars and a ringed planet; a small orange carrot floats in the air.",
     "interaction": "its hoof reaches toward the floating carrot."},
    {"id": "scifi_rooster", "genre": "sci-fi", "cast": {"rooster": {
        "action": "The rooster wears a small round silver space helmet. It stands upright and presses down with one wing, eyes wide and excited.",
        "center": 0.42, "height": 0.62}},
     "subject": "The rooster in a small round silver space helmet stands at a spaceship control panel and presses a big red button with its wing, eyes wide and excited.",
     "setting": "a spaceship cockpit: a curved control panel with glowing screens and one big red button in front, a wide window onto deep blue space with stars.",
     "interaction": "its wing presses the big red button on the panel."},
    {"id": "horror_cow", "genre": "horror", "cast": {"cow": {
        "action": "The cow wears a white bedsheet as a ghost costume with two round eye holes, but its big orange muzzle, horns and spotted legs poke out. It raises both front hooves to look scary, grinning.",
        "center": 0.47, "height": 0.76}},
     "subject": "The cow wears a white bedsheet as a ghost costume, but its big orange muzzle, horns and spotted legs poke out; it raises both hooves to look scary, grinning.",
     "setting": "a moonlit front garden at night: a wooden porch with three carved glowing pumpkins on the steps, a big round moon in a deep purple sky.",
     "interaction": "it stands on the garden path in front of the porch."},
    {"id": "horror_pair", "genre": "horror", "cast": {
        "man": {"action": "The man holds a flashlight under his chin to make a spooky face, grinning, in a dark green hoodie.",
                "center": 0.40, "height": 0.82},
        "rooster": {"action": "The rooster jumps back startled, feathers puffed, wings up, eyes wide.",
                    "center": 0.76, "height": 0.42}},
     "subject": "The man holds a flashlight under his chin to make a spooky face, and the rooster beside him jumps back, startled, feathers puffed.",
     "setting": "a forest campsite at night: an orange tent, tall dark pine trees and a big round moon in a deep blue sky.",
     "interaction": "the flashlight lights the man's face from below and the rooster stands on the ground beside him."},
]
BLEND2 = """The first images are real cards from the game. The last one is a draft of a new card: a character was pasted onto a drawn setting. Redraw the draft as one finished card that could sit beside the real cards unnoticed.
Make the character belong in the setting: light and color from the setting's light, a soft contact shadow, clean edges, and {interaction} You may adjust the pose a little where the character touches the setting.
Keep the character's face, body, proportions, colors and outfit, and keep it this large. Keep the setting and the camera."""
FIGURE_DIRECT = """The first image shows {who} as approved for this card: its face, body, outfit and pose. The last images are real cards from the game. Draw one new card that could sit beside the real cards unnoticed: the same rendering, lighting, finish, color and level of detail. {same} stays exactly as approved.
Subject: {subject}
Setting: {setting}
The characters are central and large. The setting is a real place, simple and calm: a few large soft shapes. Draw only what is named. No text, letters, numbers, frame, border or watermark."""


def draw_figure(name, action, out):
    """Pre-generate a character in a new pose or outfit, alone on a transparent ground."""
    return draw(FIGURE.format(look=LOOKS[name].split(" with ", 1)[-1], action=action), identity_references(name), out,
                transparent=True)


def body_box(path, name, find):
    """The character's own body inside a pre-drawn figure, without the props it holds, from SAM 3."""
    figure = Image.open(path).convert("RGBA")
    ground = Image.new("RGB", figure.size, GREY)
    ground.paste(figure, (0, 0), figure)
    found = find(ground, name)
    if not found:
        return None
    ys, xs = np.nonzero(max(found, key=lambda f: f[1].sum())[1])
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def paste(plate, figures, size=SIZE):
    """Figures on a setting. Each figure: path, center across, height share and bottom, all of the card, and the body
    box inside the figure (body_box). The body, not the props it holds, is scaled to the height."""
    card = Image.open(plate).convert("RGB").resize(size, Image.LANCZOS)
    for figure in figures:
        image = Image.open(figure["path"]).convert("RGBA")
        x0, y0, x1, y1 = figure.get("body") or image.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()
        scale = figure["height"] * size[1] / (y1 - y0)
        image = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
        left = round(figure["center"] * size[0] - (x0 + x1) / 2 * scale)
        top = round(figure.get("bottom", BOTTOM) * size[1] - y1 * scale)
        card.paste(image, (left, top), image)
    return card


def scene_references(card):
    """Real character cards whose cast matches this card, for the look of a scene. Cards without one fill in."""
    catalog = load_json(ANALYSIS / "cast.json")
    wanted = set(card["cast"])
    by_card = {}
    for record in catalog:
        if record.get("labels", {}).get("is_character"):
            by_card.setdefault(record["card"], set()).add(record["character"])
    ranked = sorted(by_card, key=lambda c: (-len(by_card[c] & wanted), c))
    return [ROOT / f"materials/card_examples/{c}.png" for c in ranked[:2]]


def saved(path):
    Image.open(path).convert("RGB").resize(SIZE, Image.LANCZOS).save(RUN / "tries" / f"{path.stem}.png")


def direct(card, n):
    out = RUN / "full" / f"{card['id']}_direct_{n}.png"
    if out.exists():
        return
    who = " and ".join(f"the {name}" for name in card["cast"])
    identity = [p for name in card["cast"] for p in identity_references(name, 3 if len(card["cast"]) == 1 else 2)]
    references = identity[:3] + scene_references(card)
    same = "The character" if len(card["cast"]) == 1 else "Each character"
    draw(DIRECT.format(who=who, same=same, subject=card["subject"], setting=card["setting"]), references, out)
    saved(out)


def pasted(card, n):
    out = RUN / "full" / f"{card['id']}_paste_{n}.png"
    if out.exists():
        return
    figures = []
    for name, part in card["cast"].items():
        figure = LIBRARY / "drawn" / f"{card['id']}_{name}_{n}.png"
        if not figure.exists():
            figure.parent.mkdir(parents=True, exist_ok=True)
            draw_figure(name, part["action"], figure)
        figures.append({"path": figure, "center": part["center"], "height": part["height"]})
    plate = RUN / "plates" / f"{card['id']}_{n}.png"
    if not plate.exists():
        draw(PLATE.format(setting=card["setting"]), scene_references(card), plate)
    composite = RUN / "composites" / f"{card['id']}_{n}.png"
    composite.parent.mkdir(parents=True, exist_ok=True)
    paste(plate, figures).save(composite)
    references = scene_references(card) + [identity_references(name, 1)[0] for name in card["cast"]]
    draw(BLEND.format(interaction=card["interaction"]), references[:4] + [composite], out)
    saved(out)


def pasted2(card, n, bodies):
    out = RUN / "full" / f"{card['id']}_paste2_{n}.png"
    if out.exists():
        return
    figures = []
    for name, part in card["cast"].items():
        path = LIBRARY / "drawn" / f"{card['id']}_{name}_{n}.png"
        single = len(card["cast"]) == 1
        figures.append({"path": path, "center": part["center"], "body": bodies[str(path.relative_to(ROOT))],
                        "height": PASTE2["height"] if single else part["height"] * 0.95,
                        "bottom": PASTE2["bottom"] if single or name == "man" else 0.97})
    composite = RUN / "composites" / f"{card['id']}_paste2_{n}.png"
    paste(RUN / "plates" / f"{card['id']}_{n}.png", figures).save(composite)
    references = scene_references(card) + [identity_references(name, 1)[0] for name in card["cast"]]
    draw(BLEND2.format(interaction=card["interaction"]), references[:4] + [composite], out)
    saved(out)


def figured(card, n):
    out = RUN / "full" / f"{card['id']}_figure_{n}.png"
    if out.exists():
        return
    grey = []
    for name in card["cast"]:
        path = RUN / "figures" / f"{card['id']}_{name}_{n}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        on_grey(LIBRARY / "drawn" / f"{card['id']}_{name}_{n}.png").save(path)
        grey.append(path)
    who = " and ".join(f"the {name}" for name in card["cast"])
    same = "The character" if len(card["cast"]) == 1 else "Each character"
    draw(FIGURE_DIRECT.format(who=who, same=same, subject=card["subject"], setting=card["setting"]),
         grey + scene_references(card), out)
    saved(out)


def draw_all(workers, arms):
    (RUN / "tries").mkdir(parents=True, exist_ok=True)
    bodies = {}
    if "paste2" in arms:
        from cast import segmenter

        find = segmenter()
        for card in CARDS:
            for name in card["cast"]:
                for n in range(1, DRAWS + 1):
                    path = LIBRARY / "drawn" / f"{card['id']}_{name}_{n}.png"
                    if path.exists():
                        bodies[str(path.relative_to(ROOT))] = body_box(path, name, find)
        save_json(RUN / "bodies.json", bodies)

    def paste2(card, n):
        return pasted2(card, n, bodies)

    functions = {"direct": direct, "paste": pasted, "paste2": paste2, "figure": figured}
    jobs = [(functions[arm], card, n) for card in CARDS for n in range(1, DRAWS + 1) for arm in arms
            if arm not in ("paste2", "figure") or all((LIBRARY / "drawn" / f"{card['id']}_{name}_{n}.png").exists()
                                                       for name in card["cast"])]

    def one(job):
        arm, card, n = job
        for attempt in (1, 2):
            try:
                arm(card, n)
                return
            except Exception as error:
                print(card["id"], arm.__name__, n, attempt, type(error).__name__, str(error)[:160],
                      flush=True)

    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, jobs))
    save_json(RUN / "cards.json", CARDS)


def measure():
    """Identity: each result's character, cut out by SAM 3, against the real cutouts of every cast member."""
    import torch

    from cast import cutout, segmenter
    from embed import MODELS, load_hf

    find = segmenter()
    crops = {}
    for card in CARDS:
        for path in sorted((RUN / "tries").glob(f"{card['id']}_*.png")) + sorted(
                (LIBRARY / "drawn").glob(f"{card['id']}_*.png")):
            image = Image.open(path).convert("RGB")
            arm = "drawn" if path.parent.name == "drawn" else path.stem.split("_")[-2]
            for name in card["cast"]:
                if path.parent.name == "drawn" and f"_{name}_" not in path.name:
                    continue
                found = find(image, name)
                if not found:
                    crops[(path.stem, name)] = None, arm
                    continue
                figure, _ = cutout(image, max(found, key=lambda f: f[0])[1])
                crop = RUN / "crops" / f"{path.stem}_{name}.png"
                crop.parent.mkdir(parents=True, exist_ok=True)
                figure.save(crop)
                crops[(path.stem, name)] = crop, arm
    real = [r for r in load_json(ANALYSIS / "cast.json") if r.get("labels", {}).get("is_character")]
    encode = load_hf(MODELS["dinov2"])
    files = [ROOT / r["file"] for r in real] + [c for c, _ in crops.values() if c]
    vectors = []
    with torch.inference_mode():
        for start in range(0, len(files), 8):
            batch = [on_grey(f) for f in files[start:start + 8]]
            vectors.append(torch.nn.functional.normalize(encode(batch).float(), dim=-1).cpu().numpy())
    vectors = np.concatenate(vectors)
    by_file = dict(zip(map(str, files), vectors))
    members = {name: np.stack([by_file[str(ROOT / r["file"])] for r in real if r["character"] == name]) for name in CAST}

    def likeness(vector, name, skip=None):
        sims = members[name] @ vector
        sims = np.sort(sims[sims < 0.999] if skip else sims)[::-1]
        return float(sims[:3].mean())

    rows = []
    baseline = []
    for record in real:
        vector = by_file[str(ROOT / record["file"])]
        own = likeness(vector, record["character"], skip=True)
        other = max(likeness(vector, n) for n in CAST if n != record["character"])
        baseline.append(own - other)
    for (stem, name), (crop, arm) in crops.items():
        if crop is None:
            rows.append({"image": stem, "arm": arm, "character": name, "found": False})
            continue
        vector = by_file[str(crop)]
        own, other = likeness(vector, name), max(likeness(vector, n) for n in CAST if n != name)
        rows.append({"image": stem, "arm": arm, "character": name, "found": True, "own": round(own, 3),
                     "best_other": round(other, 3), "margin": round(own - other, 3)})
    save_json(RUN / "identity.json", {"real_margin_median": round(float(np.median(baseline)), 3), "rows": rows})
    print("real cutouts, own minus best other, median:", round(float(np.median(baseline)), 3))
    for arm in ("drawn", *ARMS):
        mine = [r for r in rows if r["arm"] == arm]
        found = [r for r in mine if r["found"]]
        if found:
            print(arm, f"found {len(found)}/{len(mine)}", "own", round(float(np.mean([r["own"] for r in found])), 3),
                  "margin", round(float(np.mean([r["margin"] for r in found])), 3),
                  "margin>0", sum(r["margin"] > 0 for r in found))


def judge():
    """The art director compares arms two at a time, both orders, beside real cards with the same characters."""
    import itertools
    from collections import Counter

    from review import judge_pairs

    contests = []
    for card in CARDS:
        references = [path.stem for path in scene_references(card)]
        for n in range(1, DRAWS + 1):
            drawn = [arm for arm in ARMS if (RUN / "tries" / f"{card['id']}_{arm}_{n}.png").exists()]
            contests += [(card["id"], f"{card['id']}_{a}_{n}", f"{card['id']}_{b}_{n}", references)
                         for a, b in itertools.combinations(drawn, 2)]
    wins = judge_pairs(RUN, "arms", contests)
    duels = Counter()
    for _, a, b, _ in contests:
        if wins[a] != wins[b]:
            duels[(a.split("_")[-2], b.split("_")[-2], "first" if wins[a] > wins[b] else "second")] += 1
    total = Counter()
    for try_id, count in wins.items():
        total[try_id.split("_")[-2]] += count
    save_json(RUN / "judged.json", {"wins_by_arm": dict(total), "duels": {" ".join(k): v for k, v in duels.items()}})
    print("wins by arm:", dict(total))
    for (a, b, side), count in sorted(duels.items()):
        print(f"{a} vs {b}: {side} won {count}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("draw", "measure", "judge"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--arms", nargs="+", default=list(ARMS), choices=ARMS)
    args = parser.parse_args()
    if args.mode == "draw":
        draw_all(args.workers, args.arms)
    elif args.mode == "judge":
        judge()
    else:
        measure()


if __name__ == "__main__":
    main()
