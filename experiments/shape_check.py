"""Does naming the canonical shape keep a front-on clock round?

The user called the clock twin (twins40 m17) "not completely round" and "elongated" in every style. Its subject says
"a round wall clock seen straight on", while the style text asks for rims as thin ovals from a low camera. Three draws
per arm, same references:
    before   the subject as written
    circle   the subject plus "Its face is a perfect circle, not an oval."
Roundness is measured, not rated: SAM 3 cuts out the clock, and the axis ratio of its fitted ellipse is 1 for a circle.

    shape_check.py
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

from concurrent.futures import ThreadPoolExecutor

from common import ROOT, load_json, save_json

import numpy as np
from PIL import Image

from make_set import contact_sheet, draw_card

RUN = ROOT / "runs" / "shape_check"
CIRCLE = " Its face is a perfect circle, not an oval."


def roundness(path, find):
    """Minor over major axis of the clock's mask, from its second moments."""
    found = find(Image.open(path).convert("RGB"), "clock")
    if not found:
        return None
    ys, xs = np.nonzero(max(found, key=lambda f: f[1].sum())[1])
    axes = np.sqrt(np.linalg.eigvalsh(np.cov(np.stack([xs, ys]))))
    return round(float(axes[0] / axes[1]), 3)


def main():
    from cast import segmenter

    RUN.mkdir(parents=True, exist_ok=True)
    clock = next(b for b in load_json(ROOT / "runs" / "twins40" / "briefs.json") if b["id"] == "m17")
    arms = {"before": clock, "circle": {**clock, "card": {**clock["card"], "subject": clock["card"]["subject"] + CIRCLE}}}
    jobs = [({**brief, "id": arm}, n) for arm, brief in arms.items() for n in (1, 2, 3)]
    with ThreadPoolExecutor(3) as pool:
        done = [d for d in pool.map(lambda job: draw_card(RUN, job[0], job[1], [], True), jobs) if d]
    contact_sheet([RUN / "tries" / f"{d}.png" for d in done], RUN / "sheet.png", columns=3)
    find = segmenter()
    result = {"real": roundness(ROOT / f"materials/card_examples/{clock['real']}.png", find)}
    result.update({d: roundness(RUN / "tries" / f"{d}.png", find) for d in done})
    save_json(RUN / "roundness.json", result)
    print(result)


if __name__ == "__main__":
    main()
