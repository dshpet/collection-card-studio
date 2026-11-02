"""Compile the reference analysis into the one file the generation pipeline reads."""

from collections import Counter, defaultdict

from common import ANALYSIS, load_json, save_json

import numpy as np

from style import BANDS


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


def modes(cards, section, field):
    counts = defaultdict(Counter)
    for card in cards:
        counts[card["form"]["staging"]["art_category"]][card["form"][section][field]] += 1
    return {category: dict(count.most_common(4)) for category, count in counts.items()}


def style_floor(cards):
    """How close each real card is to its nearest neighbour in the style space."""
    vectors = np.load(ANALYSIS / "embeddings" / "csd_whole.npy")
    similarity = vectors @ vectors.T
    np.fill_diagonal(similarity, -1)
    nearest = similarity.max(axis=1)
    return {"min": round(float(np.percentile(nearest, 2)), 3), "median": round(float(np.median(nearest)), 3),
            "copy": round(float(nearest.max()) + 0.02, 3)}


def main():
    cards = load_json(ANALYSIS / "cards.json")
    sets = load_json(ANALYSIS / "sets.json")
    by_id = {card["id"]: card for card in cards}
    character_free = [s for s in sets if "5" not in s["metrics"]["categories"]
                      and not any(by_id[i]["gold_frame"] for i in s["cards"])]
    examples = [{"title": s["title"], "cards": [
        {"name": by_id[i]["name"], "object_class": by_id[i]["form"]["identity"]["object_class"],
         "category": by_id[i]["form"]["staging"]["art_category"],
         "pattern": by_id[i]["form"]["backdrop"]["pattern"]} for i in s["cards"]]} for s in character_free]
    metrics = [s["metrics"] for s in character_free]
    save_json(ANALYSIS / "knowledge.json", {
        "bands": bands(cards),
        "style": style_floor(cards),
        "patterns": modes(cards, "backdrop", "pattern"),
        "example_sets": examples,
        "set_ranges": {key: [min(m[key] for m in metrics), max(m[key] for m in metrics)]
                       for key in ("object_classes", "scale_classes", "background_hues")},
    })
    print("knowledge:", [s["title"] for s in character_free])


if __name__ == "__main__":
    main()
