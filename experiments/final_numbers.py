"""Numbers for the final sets of 2026-11-08 against the real sets and the pre-final variants they came from.

Set numbers as scripts/compare.py defines them; style similarity again on grey copies of the cards, to see how much of
it is color; and medians of the measured gaps the outside artist's sample showed, on the 30 final cards, the 30
pre-final cards of the same variants and the real object cards.

    final_numbers.py       -> runs/final3/set_numbers.json
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse

from common import ANALYSIS, ROOT, best_try, load_json, save_json

import numpy as np

SETS = {"Western": ("final3/western", "prefinal/western", 1), "Period Drama": ("final3/period-drama-2", "prefinal/period-drama", 3),
        "Detective": ("final3/detective-3", "prefinal/detective", 2)}
FIELDS = [("color_palette", "chroma_subject"), ("color_palette", "hue_families"), ("color_palette", "shadow_chroma_kept"),
          ("composition_hierarchy", "margin_min"), ("composition_hierarchy", "subject_area")]
OUT = ROOT / "runs" / "final3" / "set_numbers.json"


def chosen(run, variant):
    history = load_json(ROOT / "runs" / run / "check.json")
    ids = [b["id"] for b in load_json(ROOT / "runs" / run / "briefs.json") if b["variant"] == variant]
    return ids, [best_try(history[i])["try_id"] for i in ids]


def grey_similarity(paths, encode):
    import torch
    from PIL import Image

    with torch.inference_mode():
        vectors = encode([Image.open(p).convert("L").convert("RGB") for p in paths])
    vectors = (vectors / vectors.norm(dim=-1, keepdim=True)).float().cpu().numpy()
    return round(float((vectors @ vectors.T)[np.triu_indices(len(paths), 1)].mean()), 3)


def medians(measured):
    return {name: round(float(np.median([m[group][name] for m in measured if m.get(group, {}).get(name) is not None])), 3)
            for group, name in FIELDS}


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    from compare import real_rows, set_row
    from embed import MODELS, load_csd
    from measure import measure_card

    encode = load_csd(MODELS["csd"])
    cards = {c["id"]: c for c in load_json(ANALYSIS / "cards.json")}
    real_sets = {r["title"] for r in real_rows()}
    result = {"real": {}, "sets": {}}
    for item in load_json(ANALYSIS / "sets.json"):
        if item["title"] in real_sets:
            result["real"][item["title"]] = {
                "style_similarity": item["metrics"]["style_similarity"],
                "grey_similarity": grey_similarity([ROOT / f"materials/card_examples/{i}.png" for i in item["cards"]], encode)}
    measured = {"final": [], "pre-final": []}
    for title, (final, source, variant) in SETS.items():
        entry = result["sets"][title] = {}
        for label, run, number in (("final", final, 1), ("pre-final", source, variant)):
            ids, tries = chosen(run, number)
            paths = [ROOT / "runs" / run / "tries" / f"{t}.png" for t in tries]
            entry[label] = {"run": run, "variant": number, **set_row(run, ids, encode), "grey_similarity": grey_similarity(paths, encode)}
            measured[label] += [measure_card({"id": t, "file": f"runs/{run}/tries/{t}.png"}, ROOT / "runs" / run / "derived")
                                for t in tries]
    real_cards = [m for i, m in load_json(ANALYSIS / "measurements.json").items()
                  if i in cards and cards[i]["form"]["staging"]["art_category"] != "5" and not cards[i]["gold_frame"]]
    result["medians"] = {"real": medians(real_cards), "pre-final": medians(measured["pre-final"]), "final": medians(measured["final"]),
                         "cards": {"real": len(real_cards), "pre-final": len(measured["pre-final"]), "final": len(measured["final"])}}
    save_json(OUT, result)
    for title, entry in result["sets"].items():
        for label, row in entry.items():
            print(f"{title} {label}: classes {row['object_classes']}, scales {row['scale_classes']}, hues {row['background_hues']}, "
                  f"style {row['style_similarity']}, grey {row['grey_similarity']}")
    print("real:", result["real"])
    print("medians:", result["medians"])


if __name__ == "__main__":
    main()
