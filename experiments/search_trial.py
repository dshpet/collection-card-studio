"""Search trial: do references found by search.py make drawings closer to the real card than label picks did?

Each of the forty twins (a real card redrawn with that card hidden) is drawn once with its old label-picked references
and once with the references search.py picks from its subject. Twins whose picks do not change are skipped.
Closeness to the hidden real card is measured with CSD, the one measure that tracked the user on twins
(analysis/STYLE_GAPS.md), and judged pairwise by the art director with the real card shown.

    search_trial.py draw
    search_trial.py measure
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, ROOT, load_json, save_json

import numpy as np

RUN = ROOT / "runs" / "search_trial"


def briefs():
    """Both arms of every twin whose references change."""
    from search import Search, pick_references

    twins = load_json(ROOT / "runs" / "twins40" / "briefs.json")
    cards = load_json(ANALYSIS / "cards.json")
    likeness = Search().confidence([twin["card"]["subject"] for twin in twins])
    out = []
    for twin, chance in zip(twins, likeness):
        others = [c for c in cards if c["id"] != twin["real"]]
        found = [c["id"] for c in pick_references(twin["card"], others, chance)]
        if set(found) == set(twin["references"]):
            continue
        for arm, references in (("labels", twin["references"]), ("search", found)):
            out.append({**twin, "id": f"{twin['id']}-{arm}", "twin": twin["id"], "arm": arm, "references": references})
    return out


def draw_all(workers):
    from make_set import draw_card

    jobs = briefs()
    save_json(RUN / "briefs.json", jobs)
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(lambda brief: draw_card(RUN, brief, 1, [], True), jobs))
    print(f"drew {sum(bool(d) for d in done)} of {len(jobs)}")


def measure():
    import torch
    from scipy.stats import wilcoxon

    from embed import MODELS, load_csd
    from review import judge_pairs
    from PIL import Image

    jobs = [j for j in load_json(RUN / "briefs.json") if (RUN / "tries" / f"{j['id']}_1.png").exists()]
    twins = sorted({j["twin"] for j in jobs if all((RUN / "tries" / f"{j['twin']}-{a}_1.png").exists()
                                                    for a in ("labels", "search"))})
    real = {j["twin"]: j["real"] for j in jobs}
    encode = load_csd(MODELS["csd"])
    files = [ROOT / f"materials/card_examples/{real[t]}.png" for t in twins] + [
        RUN / "tries" / f"{t}-{arm}_1.png" for arm in ("labels", "search") for t in twins]
    with torch.inference_mode():
        vectors = torch.cat([encode([Image.open(f).convert("RGB") for f in files[i:i + 8]]).float()
                             for i in range(0, len(files), 8)])
    vectors = torch.nn.functional.normalize(vectors, dim=-1).cpu().numpy()
    n = len(twins)
    labels = np.sum(vectors[:n] * vectors[n:2 * n], axis=1)
    search = np.sum(vectors[:n] * vectors[2 * n:], axis=1)
    contests = [(t, f"{t}-labels_1", f"{t}-search_1", [real[t]]) for t in twins]
    wins = judge_pairs(RUN, "closer", contests)
    director = {"search": sum(wins[f"{t}-search_1"] > wins[f"{t}-labels_1"] for t in twins),
                "labels": sum(wins[f"{t}-labels_1"] > wins[f"{t}-search_1"] for t in twins)}
    result = {"twins": n, "csd_labels": round(float(labels.mean()), 4), "csd_search": round(float(search.mean()), 4),
              "search_closer": int((search > labels).sum()),
              "wilcoxon_p": round(float(wilcoxon(search, labels).pvalue), 4) if n > 5 else None,
              "director": director, "by_twin": {t: [round(float(a), 3), round(float(b), 3)]
                                                for t, a, b in zip(twins, labels, search)}}
    save_json(RUN / "result.json", result)
    print({k: v for k, v in result.items() if k != "by_twin"})


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("draw", "measure"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.mode == "draw":
        draw_all(args.workers)
    else:
        measure()


if __name__ == "__main__":
    main()
