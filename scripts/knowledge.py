"""Compile the reference analysis into the one file the generation pipeline reads."""

from collections import defaultdict

from common import ANALYSIS, load_json, pattern, save_json

import numpy as np

from style import BANDS

STYLE_FLOOR = 0.58


def value(card, path):
    section, name = path.split(".")
    return card["measured"][section][name]


def bands(cards):
    groups = defaultdict(list)
    for card in cards:
        groups[card["form"]["staging"]["art_category"]].append(card)
    return {category: {path: [round(float(v), 3) for v in np.percentile(
        [value(c, path) for c in members], [2, 98])] for path in BANDS}
        for category, members in groups.items()}


def style_floor():
    """How close a card must be to its nearest real neighbour in the style space.

    The floor sits between the best off-style control (0.54) and the worst good card on new topics (0.62).
    New topics have no close neighbour by content, so the real cards' own range would reject good art.
    """
    vectors = np.load(ANALYSIS / "embeddings" / "csd_whole.npy")
    similarity = vectors @ vectors.T
    np.fill_diagonal(similarity, -1)
    nearest = similarity.max(axis=1)
    return {"min": STYLE_FLOOR, "median": round(float(np.median(nearest)), 3), "copy": round(float(nearest.max()) + 0.02, 3)}


def main():
    cards = load_json(ANALYSIS / "cards.json")
    sets = load_json(ANALYSIS / "sets.json")
    by_id = {card["id"]: card for card in cards}
    character_free = [s for s in sets if "5" not in s["metrics"]["categories"]
                      and not any(by_id[i]["gold_frame"] for i in s["cards"])]
    examples = [{"title": s["title"], "cards": [
        {"name": by_id[i]["name"], "subject": by_id[i]["form"]["identity"]["subject"],
         "object_class": by_id[i]["form"]["identity"]["object_class"],
         "category": by_id[i]["form"]["staging"]["art_category"],
         "pattern": pattern(by_id[i])} for i in s["cards"]]} for s in character_free]
    metrics = [s["metrics"] for s in character_free]
    save_json(ANALYSIS / "knowledge.json", {
        "bands": bands(cards),
        "style": style_floor(),
        "example_sets": examples,
        "set_ranges": {key: [min(m[key] for m in metrics), max(m[key] for m in metrics)]
                       for key in ("object_classes", "scale_classes", "background_hues")},
    })
    print("knowledge:", [s["title"] for s in character_free])


if __name__ == "__main__":
    main()
