"""Find real cards by text. SigLIP 2 links a phrase to every card image and gives a confidence, so no vision model has
to look at the cards at query time.

    search.py "a wooden barrel" "a pig"     the cards most likely to show each phrase
    search.py test                           hidden-card test of reference picks: random, labels, labels then search

The card images were embedded once by embed.py (analysis/embeddings/siglip2_whole.npy). The confidence is SigLIP's own
sigmoid: the chance that the phrase describes the card. It is low for a partial match and near 0 for no match.
"""

import argparse
import os
import random
from collections import Counter

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from common import ANALYSIS, cards as manifest_cards, load_json, pattern, save_json

import numpy as np
import torch

REPO = "google/siglip2-giant-opt-patch16-384"


class Search:
    def __init__(self):
        from transformers import AutoModel, AutoTokenizer

        self.model = AutoModel.from_pretrained(REPO, dtype=torch.float16).cuda().eval()
        self.tokenizer = AutoTokenizer.from_pretrained(REPO)
        self.ids = [record["id"] for record in manifest_cards()]
        self.images = np.load(ANALYSIS / "embeddings" / "siglip2_whole.npy")
        self.scale, self.bias = self.model.logit_scale.exp().item(), self.model.logit_bias.item()

    def confidence(self, phrases):
        """{card id: confidence} for each phrase, in order."""
        tokens = self.tokenizer([p.lower() for p in phrases], padding="max_length", max_length=64, truncation=True,
                                return_tensors="pt").to("cuda")
        with torch.inference_mode():
            text = self.model.get_text_features(**tokens)
        text = torch.nn.functional.normalize(getattr(text, "pooler_output", text).float(), dim=-1).cpu().numpy()
        chance = 1 / (1 + np.exp(-(self.images @ text.T * self.scale + self.bias)))
        return [dict(zip(self.ids, column.tolist())) for column in chance.T]


def pick_references(card, cards, likeness, count=3, taken=()):
    """Real cards to attach to a new card's prompt: the same art category, then the same backdrop pattern and object
    class, as labelled, and among equals the cards most likely to show the same kind of object (likeness, from Search).

    Ranking by likeness alone brought references nearer hidden real cards (search.py test) but made no difference to
    the drawings (experiments/search_trial.py), so likeness only breaks the label rule's ties, which were random.
    The first pick is the real card a blind review sets beside this one, so it avoids taken: the first picks of the
    other cards in the variant."""
    pool = [c for c in cards if c["form"]["staging"]["art_category"] == card["category"]
            and "staging.art_category" not in c["disputed"]]
    ranked = sorted(pool, key=lambda c: (pattern(c) != card["pattern"],
                                         c["form"]["identity"]["object_class"] != card.get("object_class"),
                                         -likeness[c["id"]]))
    first = next((c for c in ranked if c["id"] not in taken), ranked[0])
    return [first] + [c for c in ranked if c is not first][:count - 1]


def label_picks(card, cards, rng, count=3):
    """The rule before search: same category, then backdrop pattern and object class labels, ties at random."""
    pool = [c for c in cards if c["form"]["staging"]["art_category"] == card["category"]
            and "staging.art_category" not in c["disputed"]]
    return sorted(pool, key=lambda c: (c["form"]["backdrop"]["pattern"] != card["pattern"],
                                       c["form"]["identity"]["object_class"] != card["object_class"], rng.random()))[:count]


def test():
    """Hide each real card in turn, ask for references from its own description, and see how alike they are."""
    cards = [c for c in load_json(ANALYSIS / "cards.json") if c["form"]["staging"]["art_category"] != "5"]
    ids = [record["id"] for record in manifest_cards()]
    row = {card_id: index for index, card_id in enumerate(ids)}
    spaces = {name: np.load(ANALYSIS / "embeddings" / f"{name}.npy") for name in ("dinov2_subject", "csd_whole")}
    search = Search()
    queries = [c["form"]["identity"]["subject"] for c in cards]
    likeness = search.confidence(queries)
    results = {arm: Counter() for arm in ("random", "labels", "search")}
    for card, chance in zip(cards, likeness):
        target = {"category": card["form"]["staging"]["art_category"], "pattern": card["form"]["backdrop"]["pattern"],
                  "object_class": card["form"]["identity"]["object_class"]}
        others = [c for c in cards if c["id"] != card["id"]]
        for arm in ("random", "labels", "search"):
            pool = [c for c in others if c["form"]["staging"]["art_category"] == target["category"]]
            picks = (random.Random(card["id"]).sample(pool, 3) if arm == "random" else
                     label_picks(target, others, random.Random(card["id"])) if arm == "labels" else
                     pick_references(target, others, chance))
            for name, vectors in spaces.items():
                results[arm][name] += float(np.mean([vectors[row[card["id"]]] @ vectors[row[p["id"]]] for p in picks]))
            results[arm]["same_class"] += sum(p["form"]["identity"]["object_class"] == target["object_class"]
                                              for p in picks) / len(picks)
            results[arm]["same_pattern"] += sum(p["form"]["backdrop"]["pattern"] == target["pattern"]
                                                for p in picks) / len(picks)
    summary = {arm: {key: round(value / len(cards), 3) for key, value in counts.items()}
               for arm, counts in results.items()}
    save_json(ANALYSIS / "search_test.json", {"cards": len(cards), **summary})
    for arm, row_ in summary.items():
        print(arm, row_)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("phrases", nargs="+", help='phrases to look up, or "test"')
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()
    if args.phrases == ["test"]:
        test()
        return
    names = {c["id"]: c["name"] for c in load_json(ANALYSIS / "cards.json")}
    for phrase, chance in zip(args.phrases, Search().confidence(args.phrases)):
        best = sorted(chance, key=chance.get, reverse=True)[:args.top]
        print(phrase + ":", ", ".join(f"{names[i]} {chance[i]:.2f}" for i in best))


if __name__ == "__main__":
    main()
