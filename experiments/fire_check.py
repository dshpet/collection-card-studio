"""Can the image model draw a convincing fire, given words and references taken from the game's real fire?

The producer called the fires weak: the cauldron's tiny flame and the meteor's tail. The real Campfire Cook card has a
bright fire: yellow-white core, orange tips, glowing log ends and warm light on the pot above. Two objects, three
arms, three draws each, all drawn from the brief without a blockout:
    before   the brief as planned: the horror Cauldron (runs/horror v1_04) and the western Campfire (runs/western-2 v1_10)
    words    the subject describes the fire as on the real card
    refs     words, plus the real Campfire Cook and Lantern cards as the first references

    fire_check.py        the sheet has one row per object and arm, in the order above
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, load_json

from make_set import contact_sheet, draw_card

RUN = ROOT / "runs" / "fire_check"
FIRE_CARDS = ["3458764679576193978", "3458764679576006875"]  # Campfire Cook, Lantern
FIRE = ("The fire is big and bright: a yellow-white glowing core, orange flame tips curling upward, glowing orange "
        "ends on the logs, and warm orange light cast on {lit}.")
WORDS = {
    "Cauldron": ("A round black pot with three short legs, two side handles and bubbling liquid at the top, standing over "
                 "a small fire of crossed logs. " + FIRE.format(lit="the pot's underside and the floor"),
                 "black iron, bright green bubbling potion, yellow and orange fire"),
    "Campfire": ("A campfire of crossed logs in a ring of stones, with a black cooking pot hanging on a tripod above it. "
                 + FIRE.format(lit="the pot, the stones and the ground"),
                 "brown logs and black pot with bright yellow and orange fire"),
}


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    RUN.mkdir(parents=True, exist_ok=True)
    briefs = [next(b for b in load_json(ROOT / "runs" / run / "briefs.json") if b["id"] == card_id)
              for run, card_id in (("horror", "v1_04"), ("western-2", "v1_10"))]
    jobs = []
    for brief in briefs:
        subject, colors = WORDS[brief["card"]["name"]]
        worded = {**brief, "card": {**brief["card"], "subject": subject, "hero_colors": colors}}
        arms = {"before": brief, "words": worded, "refs": {**worded, "references": FIRE_CARDS + brief["references"]}}
        name = brief["card"]["name"].lower()
        jobs += [({**b, "id": f"{name}-{arm}"}, n) for arm, b in arms.items() for n in (1, 2, 3)]
    with ThreadPoolExecutor(3) as pool:
        done = list(pool.map(lambda job: draw_card(RUN, job[0], job[1], [], True), jobs))
    contact_sheet([RUN / "tries" / f"{d}.png" for d in done if d], RUN / "sheet.png", columns=3)
    print("drew", sum(bool(d) for d in done), "of", len(jobs), "->", RUN / "sheet.png")


if __name__ == "__main__":
    main()
