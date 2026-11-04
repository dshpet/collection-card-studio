"""Soft-render and photo trial on final cards that lost to the old draws, for a blind human rating.

Finish cards lost on gloss and texture. Their existing models are rendered in the soft look and restyled:
    soft         existing model, soft render
Construction cards lost on how they are built. Each gets two fresh models, both rendered soft:
    remodel      modelled from the brief, as make_set.py does
    photo        modelled with real photos of the object (scripts/photos.py)
    photo_style  the photo model, restyled with its best photo also shown, labelled as an object reference
                 (Codex takes at most 5 images: 3 real cards, 1 photo, the blockout)

    trial2.py
"""

import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, load_json

from PIL import Image

from draw import draw
from make_set import SIZE, blockout_brief, model_card
from photos import fetch
from style import BLOCKOUT

RUN = ROOT / "runs" / "trial2"
FINISH = [("horror", "v1_09"), ("western", "v1_08"), ("sci-fi", "v1_02"), ("sci-fi", "v1_05"), ("western", "v1_02"),
          ("horror", "v1_02")]
BUILD = {("western", "v1_09"): "covered wagon", ("western", "v1_10"): "steam locomotive",
         ("western", "v1_03"): "lasso rope", ("western", "v1_07"): "western saddle",
         ("horror", "v1_04"): "cast iron cauldron", ("sci-fi", "v1_07"): "Mars rover",
         ("sci-fi", "v1_10"): "geodesic dome"}
FIRST = "The attached images are real cards from the game, except the last one, which is a 3D blockout of a new card."


def brief_of(run, card_id):
    return next(b for b in load_json(ROOT / "runs" / run / "briefs.json") if b["id"] == card_id)


def soft_render(run, card_id):
    new = next(b for b in load_json(ROOT / "runs" / f"{run}-blockout" / "briefs.json") if b["source"].endswith(f"/{card_id}"))
    out = RUN / "soft" / run / "models" / f"{card_id}.png"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["blender", "-b", "--factory-startup", "--python", str(ROOT / "scripts" / "blockout.py"), "--",
                        str(ROOT / "runs" / f"{run}-blockout" / "models" / f"{new['id']}.py"), str(out), "soft"],
                       check=True, capture_output=True)
    return out


def restyle(arm, run, brief, render, photos=()):
    out, full = RUN / arm / run / "tries" / f"{brief['id']}_1.png", RUN / arm / run / "full" / f"{brief['id']}_1.png"
    if out.exists() or render is None:
        return
    references = [ROOT / f"materials/card_examples/{i}.png" for i in brief["references"]]
    text = blockout_brief(brief["card"])
    if photos:
        text = text.replace(FIRST, (
            f"The first {len(references)} attached images are real cards from the game: take the rendering, lighting, "
            f"finish, color and level of detail only from them. The next is a photo of the real object: use it only to "
            "understand how it is built, never for its look. The last image is a 3D blockout of a new card."))
    assert FIRST in BLOCKOUT
    (RUN / arm / run / "prompts").mkdir(parents=True, exist_ok=True)
    (RUN / arm / run / "prompts" / f"{brief['id']}_1.txt").write_text(text, "utf-8")
    for tries_left in (1, 0):
        try:
            draw(text, references + list(photos) + [render], full)
            out.parent.mkdir(exist_ok=True)
            Image.open(full).convert("RGB").resize(SIZE, Image.LANCZOS).save(out)
            print(f"{arm} {run} {brief['id']} done", flush=True)
            return
        except Exception as error:
            print(f"{arm} {run} {brief['id']}: {type(error).__name__} {str(error)[:160]}", flush=True)


def finish_job(key):
    run, card_id = key
    restyle("soft", run, brief_of(run, card_id), soft_render(run, card_id))


def build_job(key, rater):
    run, card_id = key
    brief = brief_of(run, card_id)
    photos = fetch(BUILD[key], RUN / "photos" / f"{run}_{card_id}")
    print(f"{run} {card_id}: {len(photos)} photos", flush=True)
    plain = model_card(RUN / "remodel" / run, brief, rater, look="soft")
    seen = model_card(RUN / "photo" / run, brief, rater, look="soft", photos=photos)
    restyle("remodel", run, brief, plain)
    restyle("photo", run, brief, seen)
    restyle("photo_style", run, brief, seen, photos[:1])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rater", default="claude-opus-5-5")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    with ThreadPoolExecutor(args.workers) as pool:
        jobs = [pool.submit(finish_job, key) for key in FINISH] + [pool.submit(build_job, key, args.rater) for key in BUILD]
        for job in jobs:
            job.result()


if __name__ == "__main__":
    main()
