"""Compare our sets with the real character-free sets, on the same definitions.

    compare.py                                  the final sets, runs/final6/sets.json -> runs/final6/compare.json
    compare.py --sets runs/final3/sets.json     another {run: picks} file -> compare.json beside it
"""

import argparse
import os
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from common import ANALYSIS, FINAL_SETS, ROOT, best_try, load_json, save_json

import numpy as np
import torch
from PIL import Image

from embed import MODELS, load_csd
from measure import measure_card
from summarize import hue_bin


def real_rows():
    by_id = {card["id"]: card for card in load_json(ANALYSIS / "cards.json")}
    rows = []
    for item in load_json(ANALYSIS / "sets.json"):
        members = [by_id[i] for i in item["cards"]]
        if "5" not in item["metrics"]["categories"] and not any(m["gold_frame"] for m in members):
            rows.append({"title": item["title"], "title_words": len(item["title"].split()),
                         "name_words": max(len(m["name"].split()) for m in members), **item["metrics"]})
    return rows


def set_row(run, picks, encode):
    folder = ROOT / "runs" / run
    plan, history = load_json(folder / "plan.json"), load_json(folder / "check.json")
    briefs = {brief["id"]: brief for brief in load_json(folder / "briefs.json")}
    cards = [briefs[pick]["card"] for pick in picks]
    tries = [best_try(history[pick]) for pick in picks]
    paths = [folder / "tries" / f"{t['try_id']}.png" for t in tries]
    records = [{"id": t["try_id"], "file": str(path.relative_to(ROOT))} for t, path in zip(tries, paths)]
    measured = [measure_card(record, folder / "derived") for record in records]
    with torch.inference_mode():
        vectors = encode([Image.open(path).convert("RGB") for path in paths])
    vectors = (vectors / vectors.norm(dim=-1, keepdim=True)).float().cpu().numpy()
    similarity = vectors @ vectors.T
    seen = [t["seen"]["identity"] for t in tries if t.get("seen")]
    categories = {c: sum(card["category"] == c for card in cards) for c in "1234"}
    return {"title": plan["title"], "title_words": len(plan["title"].split()),
            "name_words": max(len(card["name"].split()) for card in cards),
            "object_classes": len({card["object_class"] for card in cards}),
            "scale_classes": len({item["real_world_scale"] for item in seen}),
            "background_hues": len({hue_bin(m["color_palette"]["palette_background"][0]["hex"]) for m in measured}),
            "categories": {key: value for key, value in categories.items() if value},
            "style_similarity": round(float(similarity[np.triu_indices(len(picks), 1)].mean()), 3)}


def main(sets):
    encode = load_csd(MODELS["csd"])
    rows = real_rows()
    ours = [set_row(run, picks, encode) for run, picks in load_json(sets).items()]
    print("| Set | Title words | Name words | Object classes | Scales | Backdrop hues | Categories 1/2/3/4 | Style similarity |")
    print("|---|---:|---:|---:|---:|---:|---|---:|")
    for row in rows + ours:
        mix = "/".join(str(row["categories"].get(c, 0)) for c in "1234")
        print(f"| {row['title']} | {row['title_words']} | {row['name_words']} | {row['object_classes']} | {row['scale_classes']} "
              f"| {row['background_hues']} | {mix} | {row['style_similarity']} |")
    save_json(sets.parent / "compare.json", {"real": rows, "ours": ours})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sets", type=Path, default=FINAL_SETS, help="a {run: picks} file")
    main(parser.parse_args().sets.resolve())
