"""Construction trial: the same twins drawn four ways, for a blind human rating.

control    the brief as make_set.py draws it
how        the brief with one line on how the object works, from runs/trial/trial.json
blockout   a Blender blockout (scripts/blockout.py, models in runs/trial/models) restyled by the image model
blockout2  the same with models2: framed on the main body, sturdier thin parts, soft parts with real ends,
           no modelled light beams. Drawn after seeing the six real cards, so not fully blind

    trial.py draw [--arms control how blockout blockout2] [--draws 2]
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, SIZE, load_json

from PIL import Image

from draw import draw
from make_set import blockout_brief, card_brief, render_model

RUN = ROOT / "runs" / "trial"
ARMS = ("control", "how", "blockout", "blockout2")
MODELS = {"blockout": "models", "blockout2": "models2"}


def briefs():
    how = load_json(RUN / "trial.json")
    return [{**b, "how": how[b["id"]]} for b in load_json(ROOT / "runs" / "twins40" / "briefs.json") if b["id"] in how]


def blockout(arm, brief):
    out = RUN / arm / f"{brief['id']}.png"
    if not out.exists():
        error, _ = render_model(RUN / MODELS[arm] / f"{brief['id']}.py", out)
        if error:
            raise RuntimeError(error)
    return out


def prompt(arm, brief):
    card = brief["card"]
    if arm == "control":
        return card_brief(card)
    if arm == "how":
        return card_brief(card).replace(f"Subject: {card['subject']}", f"Subject: {card['subject']}\nHow it works: {brief['how']}")
    return blockout_brief(card)


def draw_one(job):
    arm, brief, number = job
    try_id = f"{brief['id']}_{number}"
    out, full = RUN / arm / "tries" / f"{try_id}.png", RUN / arm / "full" / f"{try_id}.png"
    if out.exists():
        return
    text = prompt(arm, brief)
    (RUN / arm / "prompts").mkdir(parents=True, exist_ok=True)
    (RUN / arm / "prompts" / f"{try_id}.txt").write_text(text, "utf-8")
    references = [ROOT / f"materials/card_examples/{i}.png" for i in brief["references"]]
    if arm in MODELS:
        references.append(blockout(arm, brief))
    for _ in range(2):
        try:
            draw(text, references, full)
            out.parent.mkdir(exist_ok=True)
            Image.open(full).convert("RGB").resize(SIZE, Image.LANCZOS).save(out)
            print(f"{arm} {try_id} done", flush=True)
            return
        except Exception as error:
            print(f"{arm} {try_id}: {type(error).__name__} {str(error)[:160]}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("draw",))
    parser.add_argument("--arms", nargs="+", default=list(ARMS), choices=ARMS)
    parser.add_argument("--draws", type=int, default=2)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    jobs = [(arm, brief, n) for n in range(1, args.draws + 1) for arm in args.arms for brief in briefs()]
    with ThreadPoolExecutor(args.workers) as pool:
        list(pool.map(draw_one, jobs))


if __name__ == "__main__":
    main()
