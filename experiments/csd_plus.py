"""Does hubness-corrected CSD (CSD+, CSLS) follow the producer's pairwise choices better than raw CSD?

Raw CSD cosine to a real card favours drawings that are close to every real card, "hubs". CSLS (Frochte 2026, after
Conneau et al. 2018) subtracts each drawing's mean similarity to its k nearest real cards, so what counts is closeness
to this object's real card over closeness to the game in general. Scored on the pairs of experiments/prefer.py, which
the producer decided, with the CSD vectors it saved; the pair's own real cards are left out of the neighbourhood.

    csd_plus.py            -> runs/prefer/csd_plus.json
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse

from common import ANALYSIS, ROOT, cards, load_json, save_json

import numpy as np
from scipy.stats import binomtest


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    stored = np.load(ROOT / "runs" / "prefer" / "features.npz")
    index = {f: i for i, f in enumerate(stored["files"])}
    vectors = stored["csd"]
    pool = np.load(ANALYSIS / "embeddings" / "csd_whole.npy")
    pool = pool / np.linalg.norm(pool, axis=1, keepdims=True)
    pool_files = [r["file"] for r in cards()]
    rows = [r for r in load_json(ROOT / "runs" / "prefer" / "pairs.json") if not r["lesson"]]

    def scores(path, references, k):
        vector = vectors[index[path]]
        to_reference = np.mean([vector @ vectors[index[r]] for r in references])
        others = np.array([vector @ p for p, f in zip(pool, pool_files) if f not in references])
        return to_reference, 2 * to_reference - np.sort(others)[-k:].mean()

    result = {}
    for k in (5, 10, 20):
        hits = {"csd": [], "csd_plus": []}
        groups = {}
        for row in rows:
            (raw_a, plus_a), (raw_b, plus_b) = scores(row["A"], row["references"], k), scores(row["B"], row["references"], k)
            for name, a, b in (("csd", raw_a, raw_b), ("csd_plus", plus_a, plus_b)):
                right = ("A" if a > b else "B") == row["user"]
                hits[name].append(right)
                groups.setdefault(f"{name}/{row['object'].split('/')[0]}", []).append(right)
        result[f"k{k}"] = {name: {"agree": int(sum(h)), "of": len(h),
                                  "p": round(float(binomtest(sum(h), len(h), 0.5).pvalue), 4)} for name, h in hits.items()}
        result[f"k{k}"]["by_kind"] = {g: f"{sum(h)}/{len(h)}" for g, h in sorted(groups.items())}
    save_json(ROOT / "runs" / "prefer" / "csd_plus.json", result)
    for k, row in result.items():
        print(k, {n: f"{v['agree']}/{v['of']} p {v['p']}" for n, v in row.items() if n != "by_kind"}, row["by_kind"])


if __name__ == "__main__":
    main()
