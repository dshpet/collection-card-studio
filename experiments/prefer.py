"""Can anything predict which of two versions of one card the producer finds closer to the real cards?

Pairs come from ratings already given, so content is equal within a pair:
    closest    the producer's pick among redraws of one real card, against each other redraw
    trial      two drawings of one twin with different grades
    set        two versions of one set card (old, blockout, soft, photo) with different mean grades
Judges, each scored on pairs the producer decided:
    csd        the version more similar to the real card(s) in CSD, no training
    probe      logistic regression on CSD and DINOv3 differences, trained on the producer's pairs, one object held
               out at a time
    reviewers  the nine specialists and the art director, asked A or B beside the real card(s)

With --target works the truth is the producer's works / slightly off / broken label instead of the grade, closest picks
drop out, and the director is asked which drawing is built right. Results go to runs/prefer_works. The construction
and perspective checkers tested there, at chance, were removed (commit 8bee565 has them).

    prefer.py embed       features and the two numeric judges
    prefer.py reviewers   about 270 model calls
    prefer.py report
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import itertools
import os
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from common import ROOT, load_json, save_json

import numpy as np
from PIL import Image

from review import judge_sheet as sheet

OUT = ROOT / "runs" / "prefer"
BATCH = 8
TRIAL_PER_OBJECT = 10
# Shown to the reviewers with the producer's answer and note, and kept out of every result.
LESSONS = {"set/horror/v1_09": "too glossy, looks like a statue",
           "set/western/v1_09": "too texture-y; real cards are smoother, but not ultra-smooth",
           "set/western/v1_07": "the preferred saddle is built right and reads like the real cards"}
WORKS = {"yes": 2, "slight": 1, "no": 0}
WORKS_LESSONS = {"set/sci-fi/v1_10": "the other dome's ladder leads nowhere and its raised entry makes no sense",
                 "set/horror/v1_04": "the other pot looks broken and its fire is laughable"}
TARGET = "look"


def value(rating):
    if TARGET == "works":
        return WORKS.get(rating.get("works"))
    return rating.get("grade")


def versions():
    """Each object, its real reference cards and every graded version of it."""
    from rate_ui import items

    ratings = {v["id"]: v for v in load_json(ROOT / "runs" / "ratings.json").values() if v.get("rater") == "me"}
    objects = defaultdict(lambda: {"references": [], "versions": defaultdict(list), "picked": None})
    for item in items():
        rating = ratings.get(item["id"])
        if not rating:
            continue
        parts = item["id"].split("/")
        if item["kind"] == "closest" and TARGET == "look":
            group = objects[f"closest/{parts[1]}"]
            group["references"] = item["images"][:1]
            for style, path in zip(item["styles"], item["images"][1:]):
                group["versions"][path] = []
                if style == rating["style"]:
                    group["picked"] = path
        elif item["kind"] == "trial":
            group = objects[f"trial/{parts[2].split('_')[0]}"]
            group["references"] = item["images"][:1]
            if value(rating) is not None:
                group["versions"][item["images"][1]].append(value(rating))
        elif item["kind"] in ("redraw", "soft"):
            group = objects[f"set/{parts[2]}/{parts[3]}"]
            group["references"] = item["images"][1:]
            if value(rating) is not None:
                group["versions"][item["images"][0]].append(value(rating))
    return objects


def pairs():
    rng = random.Random(5)
    result = []
    for key, group in sorted(versions().items()):
        if key.startswith("closest/"):
            found = [(group["picked"], other) for other in group["versions"] if other != group["picked"]]
        else:
            graded = {path: np.mean(g) for path, g in group["versions"].items() if g}
            found = [(a, b) if graded[a] > graded[b] else (b, a)
                     for a, b in itertools.combinations(sorted(graded), 2) if graded[a] != graded[b]]
            if key.startswith("trial/"):
                rng.shuffle(found)
                found = found[:TRIAL_PER_OBJECT]
        for better, worse in found:
            first = rng.random() < 0.5
            result.append({"object": key, "references": group["references"], "A": better if first else worse,
                           "B": worse if first else better, "user": "A" if first else "B",
                           "lesson": (WORKS_LESSONS if TARGET == "works" else LESSONS).get(key)})
    for index, pair in enumerate(result):
        pair["pair"] = f"p{index:03d}"
    return result


def embed(rows):
    import torch

    from embed import MODELS, load_csd, load_hf

    files = sorted({f for r in rows for f in (r["A"], r["B"], *r["references"])})
    vectors = {}
    for name in ("csd", "dinov3"):
        encode = load_csd(MODELS[name]) if name == "csd" else load_hf(MODELS[name], torch.float32)
        chunks = []
        with torch.inference_mode():
            for start in range(0, len(files), 8):
                batch = [Image.open(ROOT / f).convert("RGB") for f in files[start:start + 8]]
                chunks.append(torch.nn.functional.normalize(encode(batch).float(), dim=-1).cpu().numpy())
        vectors[name] = dict(zip(files, np.concatenate(chunks)))
        del encode
        torch.cuda.empty_cache()
    np.savez(OUT / "features.npz", files=np.array(files), **{n: np.stack([v[f] for f in files]) for n, v in vectors.items()})


def numeric_judges(rows):
    from sklearn.linear_model import LogisticRegression

    stored = np.load(OUT / "features.npz")
    index = {f: i for i, f in enumerate(stored["files"])}

    def feature(name, path, references):
        vector = stored[name][index[path]]
        return vector, float(np.mean([vector @ stored[name][index[r]] for r in references]))

    test = [r for r in rows if not r["lesson"]]
    answers = {"csd": {}, "probe": {}}
    for row in test:
        a, b = feature("csd", row["A"], row["references"])[1], feature("csd", row["B"], row["references"])[1]
        answers["csd"][row["pair"]] = "A" if a > b else "B"

    def pair_vector(row, flip=False):
        parts = []
        for name in ("csd", "dinov3"):
            (va, sa), (vb, sb) = feature(name, row["A"], row["references"]), feature(name, row["B"], row["references"])
            parts += [va - vb, [sa - sb]]
        vector = np.concatenate(parts)
        return -vector if flip else vector

    objects = sorted({r["object"] for r in test})
    for held in objects:
        train = [r for r in test if r["object"] != held]
        # Each pair both ways round, so the probe cannot learn a side.
        x = [pair_vector(r) for r in train] + [pair_vector(r, True) for r in train]
        y = [r["user"] == "A" for r in train] + [r["user"] != "A" for r in train]
        model = LogisticRegression(C=0.05, max_iter=3000).fit(np.array(x), y)
        for row in [r for r in test if r["object"] == held]:
            answers["probe"][row["pair"]] = "A" if model.predict_proba([pair_vector(row)])[0, 1] > 0.5 else "B"
    save_json(OUT / "numeric.json", answers)


def reviewers(rows, rater, director_rater, workers):
    from review import ROLES, array, ask, role_prompt, strict, text

    folder = OUT / "sheets"
    folder.mkdir(parents=True, exist_ok=True)
    lessons = []
    for row in [r for r in rows if r["lesson"]]:
        labels = ("A, preferred", "B") if row["user"] == "A" else ("A", "B, preferred")
        lessons.append((sheet(row, folder / f"lesson_{row['pair']}.png", labels), row["lesson"]))
    test = [r for r in rows if not r["lesson"]]
    random.Random(9).shuffle(test)
    batches = [test[i:i + BATCH] for i in range(0, len(test), BATCH)]
    sheets = {r["pair"]: sheet(r, folder / f"{r['pair']}.png") for r in test}
    first = len(lessons) + 1

    def schema(batch):
        return strict({"pairs": array(strict({
            "pair": {"type": "string", "enum": [r["pair"] for r in batch]},
            "closer": {"type": "string", "enum": ["A", "B", "neither"]},
            "confidence": {"type": "integer", "minimum": 1, "maximum": 5}, "why": text()}))})

    def preamble(batch):
        lesson_list = "; ".join(f"image {i + 1}: {note}" for i, (_, note) in enumerate(lessons))
        listing = ", ".join(f"{r['pair']} is image {i + first}" for i, r in enumerate(batch))
        return (f"Each image shows real cards from the game on top, marked REAL, and below them two drawings of the same "
                f"object, A and B, made by an image model. Images 1 to {first - 1} are lessons: the art lead marked the "
                f"drawing they found {'built more correctly' if TARGET == 'works' else 'closer to the real cards'} "
                f"({lesson_list}). Learn which way the differences run "
                f"from them, and trust them over any idea of what game art should look like. Then judge the test "
                f"pairs ({listing}).")

    def one(job):
        role, index = job
        out = OUT / "reviewers" / role / f"{index:02d}.json"
        if out.exists():
            return
        batch = batches[index]
        built = ("Which drawing is built right: could the object exist and do its job, with every part attached, "
                 "resting on something and drawn from one consistent camera? Real cards simplify objects but never get "
                 "them wrong. Answer A, B or neither, with confidence 1-5, and say why in one sentence, naming the part.")
        if TARGET == "works":
            brief = (ROOT / "analysis" / "agents" / "art_director.md").read_text("utf-8")
            prompt = f"{brief}\n{preamble(batch)} {built}"
            model = director_rater
        elif role == "art_director":
            brief = (ROOT / "analysis" / "agents" / "art_director.md").read_text("utf-8")
            prompt = (f"{brief}\n{preamble(batch)} Which drawing is closer in look to the real cards above it: "
                      "rendering, shape, color, light, finish, and whether it is built like a real object? Answer A, B "
                      "or neither, with confidence 1-5, and say why in one sentence.")
            model = director_rater
        else:
            prompt = (f"{role_prompt(role)}\n{preamble(batch)} On your vector only: which drawing is closer to the real "
                      "cards above it? Answer A, B or neither when your vector gives no reason, with confidence 1-5, "
                      "and say why in one sentence.")
            model = rater
        result = ask(model, prompt, [path for path, _ in lessons] + [sheets[r["pair"]] for r in batch], schema(batch))
        if result:
            save_json(out, result)
            print(role, index, flush=True)

    roles = ("art_director",) if TARGET == "works" else (*ROLES, "art_director")
    jobs = [(role, i) for role in roles for i in range(len(batches))]
    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, jobs))


def report(rows):
    from scipy.stats import binomtest

    key = {r["pair"]: r for r in rows if not r["lesson"]}
    sources = ("trial", "set") if TARGET == "works" else ("closest", "trial", "set")
    judges = load_json(OUT / "numeric.json") if (OUT / "numeric.json").exists() else {}
    for folder in sorted((OUT / "reviewers").glob("*")) if (OUT / "reviewers").exists() else []:
        judges[folder.name] = {p["pair"]: p["closer"] for path in folder.glob("*.json") for p in load_json(path)["pairs"]}
    if TARGET == "look" and any(name not in ("csd", "probe") for name in judges):
        votes = defaultdict(list)
        for name, answers in judges.items():
            if name not in ("csd", "probe", "art_director"):
                for pair, answer in answers.items():
                    votes[pair].append(answer)
        judges["specialist_vote"] = {}
        for pair, answers in votes.items():
            a, b = answers.count("A"), answers.count("B")
            judges["specialist_vote"][pair] = "A" if a > b else "B" if b > a else "neither"
    summary = {}
    print(f"{'judge':22} {'agree':>7} {'decided':>8} {'rate':>6} {'p':>6}   " + "  ".join(sources))
    for name, answers in judges.items():
        decided = [p for p, a in answers.items() if a != "neither" and p in key]
        agree = sum(answers[p] == key[p]["user"] for p in decided)
        by_source = {}
        for source in sources:
            these = [p for p in decided if key[p]["object"].startswith(source)]
            by_source[source] = f"{sum(answers[p] == key[p]['user'] for p in these)}/{len(these)}"
        p_value = binomtest(agree, len(decided), 0.5, alternative="greater").pvalue if decided else 1
        summary[name] = {"agree": agree, "decided": len(decided), "of": len(key), "p": round(p_value, 4), **by_source}
        print(f"{name:22} {agree:>7} {len(decided):>8} {agree / max(len(decided), 1):>6.2f} {p_value:>6.3f}   "
              + "  ".join(by_source.values()))
    save_json(OUT / "summary.json", summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("embed", "reviewers", "report"))
    parser.add_argument("--rater", default="claude-sonnet-5-5")
    parser.add_argument("--director", default="claude-opus-5-5")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--target", choices=("look", "works"), default="look")
    args = parser.parse_args()
    global OUT, TARGET
    if args.target == "works":
        OUT, TARGET = ROOT / "runs" / "prefer_works", "works"
    rows = pairs()
    save_json(OUT / "pairs.json", rows)
    if args.mode == "embed" and TARGET != "works":
        embed(rows)
        numeric_judges(rows)
    elif args.mode == "reviewers":
        reviewers(rows, args.rater, args.director, args.workers)
    report(rows)


if __name__ == "__main__":
    main()
