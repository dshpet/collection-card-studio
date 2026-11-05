"""Does the planner's "plain" lesson stop the image model inventing a jewel on the sheriff star?

The Sheriff Star of runs/western-2 got a red jewel in every draw. Three draws per arm, same references and staging:
    before   the subject and hero colors as planned then: "golden yellow with a small red gem in the center"
    plain    the subject in the lesson's wording, "plain ... and no gem", hero colors unchanged
    accent   the plain subject, and the red accent on a part the subject names: the ring

    plain_check.py
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

from concurrent.futures import ThreadPoolExecutor

from common import ROOT, load_json

from make_set import contact_sheet, draw_card

RUN = ROOT / "runs" / "plain_check"
PLAIN = "A plain five-pointed star badge with a ball tip on each point and a ring around the edge, and no gem."
ACCENT = "golden yellow, with the ring around the edge in red."


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    star = next(b for b in load_json(ROOT / "runs" / "western-2" / "briefs.json") if b["card"]["name"] == "Sheriff Star")
    arms = {"before": star, "plain": {**star, "card": {**star["card"], "subject": PLAIN}},
            "accent": {**star, "card": {**star["card"], "subject": PLAIN, "hero_colors": ACCENT}}}
    jobs = [({**brief, "id": arm}, n) for arm, brief in arms.items() for n in (1, 2, 3)]
    with ThreadPoolExecutor(3) as pool:
        done = list(pool.map(lambda job: draw_card(RUN, job[0], job[1], [], True), jobs))
    contact_sheet([RUN / "tries" / f"{d}.png" for d in done if d], RUN / "sheet.png", columns=3)
    print("drew", sum(bool(d) for d in done), "of", len(jobs), "->", RUN / "sheet.png")


if __name__ == "__main__":
    main()
