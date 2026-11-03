"""Construction trial: the same twins drawn four ways, for a blind human rating.

control    the brief as make_set.py draws it
how        the brief with one line on how the object works, from runs/trial/trial.json
blockout   a Blender blockout (scripts/blockout.py, models in runs/trial/models) restyled by the image model
blockout2  the same with models2: framed on the main body, sturdier thin parts, soft parts with real ends,
           no modelled light beams. Drawn after seeing the six real cards, so not fully blind

    trial.py draw [--arms control how blockout blockout2] [--draws 2]
    trial.py check      construction and perspective checkers on every drawing
"""

import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, load_json, save_json

from PIL import Image

from draw import draw
from make_set import SIZE, card_brief
from style import PATTERNS

RUN = ROOT / "runs" / "trial"
ARMS = ("control", "how", "blockout", "blockout2")
MODELS = {"blockout": "models", "blockout2": "models2"}
BLOCKOUT = """The attached images are real cards from the game, except the last one, which is a 3D blockout of a new card. The blockout is right about the object's shape, its parts, where each part attaches and what it rests on, and about the camera and the framing.
Redraw the blockout as a finished card that could sit beside the real cards unnoticed: the same rendering, lighting, finish, color and level of detail. Keep every part, every connection, the pose, the camera and the framing exactly. Change only the surfaces: materials, bevels, shading and small details, and draw the backdrop and setting.
Each material looks like itself, with a little quiet detail and natural local color. Shiny materials carry one soft highlight. Cloth, cord and wood stay matte.
Draw only what the subject names. No text, letters, numbers, frame, border or watermark."""


def briefs():
    how = load_json(RUN / "trial.json")
    return [{**b, "how": how[b["id"]]} for b in load_json(ROOT / "runs" / "twins40" / "briefs.json") if b["id"] in how]


def blockout(arm, brief):
    out = RUN / arm / f"{brief['id']}.png"
    if not out.exists():
        subprocess.run(["blender", "-b", "--factory-startup", "--python", str(ROOT / "scripts" / "blockout.py"), "--",
                        str(RUN / MODELS[arm] / f"{brief['id']}.py"), str(out)], check=True, capture_output=True)
    return out


def prompt(arm, brief):
    card = brief["card"]
    if arm == "control":
        return card_brief(card)
    if arm == "how":
        return card_brief(card).replace(f"Subject: {card['subject']}", f"Subject: {card['subject']}\nHow it works: {brief['how']}")
    lines = [BLOCKOUT, f"Subject: {card['subject']}", f"Hero colors: {card['hero_colors']}.",
             f"Backdrop: {PATTERNS[card['pattern']].format(topic='simple')} in {card['backdrop_colors']}."]
    if card["surface_or_setting"]:
        lines.append(f"Surface or setting: {card['surface_or_setting']}.")
    return "\n".join(lines)


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
    for tries_left in (1, 0):
        try:
            draw(text, references, full)
            out.parent.mkdir(exist_ok=True)
            Image.open(full).convert("RGB").resize(SIZE, Image.LANCZOS).save(out)
            print(f"{arm} {try_id} done", flush=True)
            return
        except Exception as error:
            print(f"{arm} {try_id}: {type(error).__name__} {str(error)[:160]}", flush=True)


def check():
    from estimate import write_masks
    from review import CHECKS, check_cards, try_record

    groups = {arm: [try_record(RUN / arm, p.stem, key=f"{arm}_{p.stem}") for p in sorted((RUN / arm / "tries").glob("*.png"))]
              for arm in ARMS}
    # The blockout renders themselves. Their flags are checker false alarms or flaws in the models.
    for arm, group in (("blockout", "renders"), ("blockout2", "renders2")):
        groups[group] = [{"id": f"render_{b['id']}", "file": f"runs/trial/{arm}/{b['id']}.png", "real": False,
                          "derived": RUN / arm / "derived", "full": RUN / arm / f"{b['id']}.png"} for b in briefs()]
    found = {}
    for group, records in groups.items():
        write_masks(records, "cuda", records[0]["derived"] / "masks")
        reports = check_cards(f"trial_{group}", records)
        found[group] = {r["id"]: [{"check": c, "severity": e["severity"], "what": e["what"]}
                                  for c in CHECKS for e in (reports[c].get(r.get("key", r["id"])) or {}).get("errors", [])]
                        for r in records}
        errors = [e for card in found[group].values() for e in card]
        print(f"{group}: {sum(1 for e in found[group].values() if e)} of {len(records)} flagged, {len(errors)} errors, "
              f"{sum(e['severity'] == 'major' for e in errors)} major", flush=True)
    save_json(RUN / "checks.json", found)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("draw", "check"))
    parser.add_argument("--arms", nargs="+", default=list(ARMS), choices=ARMS)
    parser.add_argument("--draws", type=int, default=2)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.mode == "check":
        return check()
    jobs = [(arm, brief, n) for n in range(1, args.draws + 1) for arm in args.arms for brief in briefs()]
    with ThreadPoolExecutor(args.workers) as pool:
        list(pool.map(draw_one, jobs))


if __name__ == "__main__":
    main()
