"""Do cast cards keep the outfits of the cutouts they were drawn from?

runs/cast-check drew the three character cards of runs/plans/western-cast.json. The cow came out in the red life vest
and sunglasses of the jet-ski card its cutout came from, and the man in the hiker's backpack. This redraws the same
cards, with the same references, with one sentence added to the cast prompt.

    outfit_check.py
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

from concurrent.futures import ThreadPoolExecutor

from common import ROOT, load_json

import make_set
from make_set import contact_sheet, draw_card

RUN = ROOT / "runs" / "outfit_check"
SENTENCE = " The cutouts show who each character is, not what it wears: dress it only as the subject says."


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    first, rest = make_set.CAST_STYLE.split("\n", 1)
    make_set.CAST_STYLE = first + SENTENCE + "\n" + rest
    briefs = load_json(ROOT / "runs" / "cast-check" / "briefs.json")
    with ThreadPoolExecutor(3) as pool:
        done = [d for d in pool.map(lambda brief: draw_card(RUN, brief, 1, [], True), briefs) if d]
    paths = [ROOT / "runs" / "cast-check" / "tries" / f"{b['id']}_1.png" for b in briefs]
    contact_sheet(paths + [RUN / "tries" / f"{d}.png" for d in done], RUN / "sheet-cast.png", columns=len(briefs))
    print("drew", len(done), "of", len(briefs), "->", RUN / "sheet-cast.png")


if __name__ == "__main__":
    main()
