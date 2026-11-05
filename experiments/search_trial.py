"""Reference trials on the forty twins: which references bring a drawing closer to the hidden real card?

Each twin is a real card redrawn with that card hidden. Arms, one draw per twin:
    labels   the three references picked by labels when the twins were made (the control)
    search   three picked by search.py likeness within the backdrop pattern, the rule tested on 2026-11-05
    five     the control's three plus the next two by the pipeline's rule, as Codex takes up to five images
Closeness to the hidden real card is measured with CSD, the one measure that tracked the user on twins
(analysis/STYLE_GAPS.md), and judged pairwise by the art director with the real card shown.

    search_trial.py draw --arm search
    search_trial.py measure --arms labels search
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, ROOT, load_json, save_json

import numpy as np

RUN = ROOT / "runs" / "search_trial"


def by_likeness(card, cards, likeness):
    """The rule tested on 2026-11-05: same category, backdrop pattern first, then likeness."""
    pool = [c for c in cards if c["form"]["staging"]["art_category"] == card["category"]
            and "staging.art_category" not in c["disputed"]]
    return sorted(pool, key=lambda c: (c["form"]["backdrop"]["pattern"] != card["pattern"], -likeness[c["id"]]))


def briefs(arm):
    """Every twin's brief for an arm, kept in briefs.json so a rerun draws what was planned."""
    from search import Search, pick_references

    saved = load_json(RUN / "briefs.json") if (RUN / "briefs.json").exists() else []
    if any(b["arm"] == arm for b in saved):
        return saved
    twins = load_json(ROOT / "runs" / "twins40" / "briefs.json")
    cards = load_json(ANALYSIS / "cards.json")
    likeness = Search().confidence([twin["card"]["subject"] for twin in twins])
    for twin, chance in zip(twins, likeness):
        others = [c for c in cards if c["id"] != twin["real"]]
        if arm == "search":
            found = [c["id"] for c in by_likeness(twin["card"], others, chance)[:3]]
            if set(found) == set(twin["references"]):
                continue
            arms = (("labels", twin["references"]), ("search", found))
        else:
            extra = [c["id"] for c in pick_references(twin["card"], others, chance, count=8)
                     if c["id"] not in twin["references"]][:2]
            arms = (("five", twin["references"] + extra),)
        saved += [{**twin, "id": f"{twin['id']}-{name}", "twin": twin["id"], "arm": name, "references": references}
                  for name, references in arms if not any(b["id"] == f"{twin['id']}-{name}" for b in saved)]
    save_json(RUN / "briefs.json", saved)
    return saved


def draw_all(arm, workers):
    from make_set import draw_card

    jobs = [b for b in briefs(arm) if b["arm"] == arm or (arm == "search" and b["arm"] == "labels")]
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(lambda brief: draw_card(RUN, brief, 1, [], True), jobs))
    print(f"drew {sum(bool(d) for d in done)} of {len(jobs)}")


def measure(first, second):
    import torch
    from scipy.stats import binomtest, wilcoxon

    from embed import MODELS, load_csd
    from review import judge_pairs
    from PIL import Image

    jobs = load_json(RUN / "briefs.json")
    twins = sorted({j["twin"] for j in jobs if all((RUN / "tries" / f"{j['twin']}-{a}_1.png").exists()
                                                    for a in (first, second))})
    real = {j["twin"]: j["real"] for j in jobs}
    encode = load_csd(MODELS["csd"])
    files = [ROOT / f"materials/card_examples/{real[t]}.png" for t in twins] + [
        RUN / "tries" / f"{t}-{arm}_1.png" for arm in (first, second) for t in twins]
    with torch.inference_mode():
        vectors = torch.cat([encode([Image.open(f).convert("RGB") for f in files[i:i + 8]]).float()
                             for i in range(0, len(files), 8)])
    vectors = torch.nn.functional.normalize(vectors, dim=-1).cpu().numpy()
    n = len(twins)
    a = np.sum(vectors[:n] * vectors[n:2 * n], axis=1)
    b = np.sum(vectors[:n] * vectors[2 * n:], axis=1)
    label = "closer" if (first, second) == ("labels", "search") else f"closer_{first}_{second}"
    contests = [(t, f"{t}-{first}_1", f"{t}-{second}_1", [real[t]]) for t in twins]
    wins = judge_pairs(RUN, label, contests)
    director = {second: sum(wins[f"{t}-{second}_1"] > wins[f"{t}-{first}_1"] for t in twins),
                first: sum(wins[f"{t}-{first}_1"] > wins[f"{t}-{second}_1"] for t in twins)}
    decided = director[first] + director[second]
    result = {"twins": n, f"csd_{first}": round(float(a.mean()), 4), f"csd_{second}": round(float(b.mean()), 4),
              f"{second}_closer": int((b > a).sum()), "wilcoxon_p": round(float(wilcoxon(b, a).pvalue), 4),
              "director": director,
              "director_p": round(float(binomtest(director[second], decided, 0.5).pvalue), 4) if decided else None,
              "by_twin": {t: [round(float(x), 3), round(float(y), 3)] for t, x, y in zip(twins, a, b)}}
    save_json(RUN / ("result.json" if label == "closer" else f"result_{first}_{second}.json"), result)
    print({k: v for k, v in result.items() if k != "by_twin"})


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("draw", "measure"))
    parser.add_argument("--arm", choices=("search", "five"), default="search")
    parser.add_argument("--arms", nargs=2, default=["labels", "search"])
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.mode == "draw":
        draw_all(args.arm, args.workers)
    else:
        measure(*args.arms)


if __name__ == "__main__":
    main()
