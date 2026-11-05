"""One uniform score for every card the user rated, checked against the user's grades.

Each card gets, on one shared list:
    twins        each twins40 redraw against its own real card, so content is equal (runs/score/pair_similarity.json)
    embeddings   how real it looks to CSD (a style model), DINOv3 and SigLIP 2: mean similarity to its ten nearest
                 real cards, as a percentile among real cards scored the same way. 0.5 means like a real card.
                 A card's own twin and its reference cards are left out of its neighbours, so content does not count.
    classifier   P(real) from DINOv3, trained on real cards against the first run.
    specialists  each of the nine style specialists scores 1-10 on its vector, the art director 1-10 overall.
                 All see the same real cards and the same graded lessons, and hidden real cards are mixed in.

    score.py embed          embeddings and classifier, minutes on the GPU
    score.py specialists    model scores, about 250 calls
    score.py report         how each score tracks the user's grades and twin picks
"""

import argparse
import os
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from common import ANALYSIS, ROOT, load_json, save_json

import numpy as np
from PIL import Image

OUT = ROOT / "runs" / "score"
RATINGS = ROOT / "runs" / "ratings.json"
GRADED = ("trial", "redraw", "soft", "card")
EMBEDDERS = ("csd", "dinov3", "siglip2")
K = 10
BATCH = 10
# Lessons for the specialists: the user's grade and note, kept out of every result.
LESSONS = {
    "redraw/new/horror/v1_09": "too glossy, looks like a statue",
    "redraw/new/western/v1_09": "too texture-y; real cards are smoother, but not ultra-smooth",
    "redraw/old/western/v1_08": "too round",
    "redraw/new/western/v1_08": "a little too realistic; needs a touch of smoothness and stylizing",
    "soft/old/western/v1_02": "",
    "soft/remodel/western/v1_07": "",
}
LESSON_REAL = 2
CONTROLS = 24


def real_pool():
    return [c for c in load_json(ANALYSIS / "cards.json") if c["form"]["staging"]["art_category"] != "5"]


def dataset():
    """Every rated image once, with all its grades, plus hidden real cards as controls."""
    from rate_ui import items

    ratings = {v["id"]: v for v in load_json(RATINGS).values() if v.get("rater") == "me"}
    images = {}
    used_real = set()

    def entry(path, arm, exclude):
        record = images.setdefault(path, {"file": path, "arms": set(), "grades": [], "works": [], "detected": [],
                                          "exclude": set(), "ids": []})
        record["arms"].add(arm)
        record["exclude"] |= exclude
        return record

    for item in items():
        rating = ratings.get(item["id"])
        if not rating or item["kind"] not in ("twin", *GRADED):
            continue
        reals = {p.split("/")[-1][:-4] for p in item["images"] if p.startswith("materials/")}
        used_real |= reals
        if item["kind"] == "twin":
            drawn = item["images"][0 if item["generated"] == "A" else 1]
            record = entry(drawn, f"twins40/{item['id'].split('/')[1]}", reals)
            record["detected"].append(rating["answer"] == item["generated"])
        else:
            drawn = next(p for p in item["images"] if p.startswith("runs/"))
            arm = "/".join(item["id"].split("/")[:2])
            record = entry(drawn, arm, reals)
            record["grades"].append(rating["grade"])
            record["works"].append(rating.get("works"))
        record["ids"].append(item["id"])
        if item["id"] in LESSONS:
            record["lesson"] = LESSONS[item["id"]]
    rng = random.Random(7)
    spare = [c["id"] for c in real_pool() if c["id"] not in used_real]
    rng.shuffle(spare)
    for card_id in spare[:CONTROLS + LESSON_REAL]:
        record = entry(f"materials/card_examples/{card_id}.png", "real", {card_id})
        if len([r for r in images.values() if r["arms"] == {"real"} and "lesson" in r]) < LESSON_REAL:
            record["lesson"] = "REAL"
    rows = []
    for index, record in enumerate(images.values()):
        record.update(key=f"c{index:03d}", arms=sorted(record["arms"]), exclude=sorted(record["exclude"]))
        rows.append(record)
    return rows


def embed(rows):
    import torch

    from drift import matched
    from embed import MODELS, load_csd, load_hf

    real = real_pool()
    files = [f"materials/card_examples/{c['id']}.png" for c in real] + [r["file"] for r in rows]
    vectors = {}
    for name in EMBEDDERS:
        encode = load_csd(MODELS[name]) if name == "csd" else load_hf(
            MODELS[name], torch.float32 if name == "dinov3" else torch.float16)
        chunks = []
        with torch.inference_mode():
            for start in range(0, len(files), 8):
                batch = [Image.open(ROOT / f).convert("RGB") for f in files[start:start + 8]]
                chunks.append(torch.nn.functional.normalize(encode(batch).float(), dim=-1).cpu().numpy())
        vectors[name] = np.concatenate(chunks)
        print(name, vectors[name].shape, flush=True)
        if name == "dinov3":
            cache = np.load(ROOT / "runs" / "drift" / "first_run.npz")
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler
            matched_features = []
            with torch.inference_mode():
                for start in range(0, len(rows), 8):
                    batch = [matched(Image.open(ROOT / r["file"]).convert("RGB")) for r in rows[start:start + 8]]
                    matched_features.append(encode(batch).float().cpu().numpy())
            matched_features = np.concatenate(matched_features)
            held = {e for r in rows for e in r["exclude"]}
            keep = np.array([c["id"] not in held for c in load_json(ANALYSIS / "cards.json")
                             if c["form"]["staging"]["art_category"] != "5"])
            stored_real = cache["real"]
            model = make_pipeline(StandardScaler(), LogisticRegression(C=0.01, max_iter=2000, class_weight="balanced"))
            model.fit(np.concatenate((stored_real[keep], cache["first"])),
                      np.array([1] * keep.sum() + [0] * len(cache["first"])))
            p_real = model.predict_proba(matched_features)[:, 1]
        del encode
        torch.cuda.empty_cache()
    ids = [c["id"] for c in real]
    scores = {}
    for name, matrix in vectors.items():
        real_vectors, test = matrix[:len(real)], matrix[len(real):]
        similarity = real_vectors @ real_vectors.T
        np.fill_diagonal(similarity, -np.inf)
        baseline = np.sort(np.sort(similarity, axis=1)[:, -K:].mean(axis=1))
        for row, vector in zip(rows, test):
            near = real_vectors @ vector
            near[[i for i, card_id in enumerate(ids) if card_id in row["exclude"]]] = -np.inf
            value = np.sort(near)[-K:].mean()
            scores.setdefault(row["key"], {})[name] = round(float(np.searchsorted(baseline, value) / len(baseline)), 3)
    for row, value in zip(rows, p_real):
        scores[row["key"]]["classifier"] = round(float(value), 3)
    save_json(OUT / "embeddings.json", scores)


def pair_similarity():
    """Content held equal: each twins40 redraw against its own real card, per style."""
    import torch

    from embed import MODELS, load_csd, load_hf

    briefs = load_json(ROOT / "runs" / "twins40" / "briefs.json")
    styles = sorted(p.name for p in (ROOT / "runs" / "twins40").iterdir() if p.is_dir())
    result = {}
    for name in EMBEDDERS:
        encode = load_csd(MODELS[name]) if name == "csd" else load_hf(
            MODELS[name], torch.float32 if name == "dinov3" else torch.float16)
        result[name] = {}
        for brief in briefs:
            paths = [ROOT / f"materials/card_examples/{brief['real']}.png"] + [
                ROOT / f"runs/twins40/{s}/tries/{brief['id']}_1.png" for s in styles]
            present = [s for s, p in zip(styles, paths[1:]) if p.exists()]
            with torch.inference_mode():
                v = torch.nn.functional.normalize(encode(
                    [Image.open(p).convert("RGB") for p in paths if p.exists()]).float(), dim=-1).cpu().numpy()
            result[name][brief["id"]] = {s: float(v[0] @ v[i + 1]) for i, s in enumerate(present)}
        del encode
        torch.cuda.empty_cache()
    save_json(OUT / "pair_similarity.json", result)


def score_schema(keys):
    from review import array, strict, text
    return strict({"scores": array(strict({"card": {"type": "string", "enum": keys},
                                           "score": {"type": "integer", "minimum": 1, "maximum": 10},
                                           "tell": text()}))})


def lesson_images(rows, folder):
    from review import labelled
    paths, notes = [], []
    for row in [r for r in rows if "lesson" in r]:
        label = "REAL" if row["lesson"] == "REAL" else f"grade {round(np.mean(row['grades']))} of 5"
        path = folder / f"lesson_{row['key']}.png"
        labelled(Image.open(ROOT / row["file"]).convert("RGB").resize((430, 480), Image.LANCZOS), label).save(path)
        paths.append(path)
        notes.append(f"{label}" + (f": {row['lesson']}" if row["lesson"] not in ("", "REAL") else ""))
    return paths, notes


SCALE = ("10 cannot be told from a real card, 8 close with one small tell, 6 clearly near but off, 4 clearly off, "
         "2 a different style. Use the whole range where cards differ, and score real-looking cards high.")


def specialists(rows, rater, director_rater, workers):
    from review import ROLES, anchor, ask, role_prompt

    folder = OUT / "sheets"
    folder.mkdir(parents=True, exist_ok=True)
    test = [r for r in rows if "lesson" not in r]
    random.Random(3).shuffle(test)
    batches = [test[i:i + BATCH] for i in range(0, len(test), BATCH)]
    anchor_path = anchor(folder, {e for r in rows for e in r["exclude"]})
    taught, notes = lesson_images(rows, folder)
    cards = {}
    for row in test:
        path = folder / f"{row['key']}.png"
        if not path.exists():
            Image.open(ROOT / row["file"]).convert("RGB").resize((430, 480), Image.LANCZOS).save(path)
        cards[row["key"]] = path
    first = len(taught) + 2

    def preamble(batch):
        listing = ", ".join(f"{r['key']} is image {i + first}" for i, r in enumerate(batch))
        lesson_list = "; ".join(f"image {i + 2}: {n}" for i, n in enumerate(notes))
        return (f"Image 1 shows real cards from the game. Images 2 to {first - 1} are lessons, each labelled with the "
                f"art lead's overall grade against real cards ({lesson_list}). REAL means a card from the game. Learn "
                "which way the differences run from them, and trust them over any idea of what game art should look "
                f"like. The remaining images are test cards ({listing}). Some are real cards from the game, the rest "
                "were drawn by an image model.")

    def one(job):
        role, index = job
        out = OUT / "specialists" / role / f"{index:02d}.json"
        if out.exists():
            return
        batch = batches[index]
        prompt = (f"{role_prompt(role)}\n{preamble(batch)} On your vector only, score each test card 1-10 for how "
                  f"closely it matches the real cards: {SCALE} In tell, name what gives it away and where, or 'none'.")
        result = ask(rater, prompt, [anchor_path, *taught, *(cards[r["key"]] for r in batch)],
                     score_schema([r["key"] for r in batch]))
        if result:
            save_json(out, result)
            print(role, index, flush=True)

    def direct(index):
        out = OUT / "specialists" / "art_director" / f"{index:02d}.json"
        if out.exists():
            return
        batch = batches[index]
        reports = []
        for role in ROLES:
            path = OUT / "specialists" / role / f"{index:02d}.json"
            if path.exists():
                for s in load_json(path)["scores"]:
                    reports.append(f"{role} {s['card']}: {s['score']}, {s['tell']}")
        brief = (ROOT / "analysis" / "agents" / "art_director.md").read_text("utf-8")
        prompt = (f"{brief}\n{preamble(batch)} Your specialists scored them 1-10 on their vectors:\n"
                  + "\n".join(reports) + f"\nScore each test card 1-10 overall for how closely its style matches the "
                  f"real cards: {SCALE} Trust a specialist only where you can see it. In tell, name the main tell.")
        result = ask(director_rater, prompt, [anchor_path, *taught, *(cards[r["key"]] for r in batch)],
                     score_schema([r["key"] for r in batch]))
        if result:
            save_json(out, result)
            print("art_director", index, flush=True)

    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, [(role, i) for role in ROLES for i in range(len(batches))]))
        list(pool.map(direct, range(len(batches))))


def collected():
    scores = defaultdict(dict)
    for path in (OUT / "specialists").glob("*/*.json"):
        for s in load_json(path)["scores"]:
            scores[s["card"]][path.parent.name] = s["score"]
    if (OUT / "embeddings.json").exists():
        for key, values in load_json(OUT / "embeddings.json").items():
            scores[key].update(values)
    return scores


def auc(positive, negative):
    from sklearn.metrics import roc_auc_score
    if not positive or not negative:
        return None
    return round(float(roc_auc_score([1] * len(positive) + [0] * len(negative), positive + negative)), 2)


def report(rows):
    from scipy.stats import spearmanr

    scores = collected()
    test = [r for r in rows if "lesson" not in r]
    measures = sorted({m for s in scores.values() for m in s},
                      key=lambda m: (m in EMBEDDERS or m == "classifier", m))
    if all(any(m in scores[r["key"]] for m in measures if m not in EMBEDDERS and m != "classifier") for r in test):
        for r in test:
            roles = [v for m, v in scores[r["key"]].items() if m not in EMBEDDERS and m not in ("classifier", "art_director")]
            scores[r["key"]]["specialist_mean"] = round(float(np.mean(roles)), 2) if roles else None
        measures.insert(0, "specialist_mean")
    graded = [r for r in test if r["grades"]]
    real = [r for r in test if r["arms"] == ["real"]]
    drawn = [r for r in test if r["arms"] != ["real"]]
    twins = [r for r in test if r["detected"]]
    table = {}
    for m in measures:
        have = [r for r in graded if scores[r["key"]].get(m) is not None]
        rho, p = spearmanr([np.mean(r["grades"]) for r in have], [scores[r["key"]][m] for r in have])
        table[m] = {
            "grade_rho": round(float(rho), 2), "grade_p": round(float(p), 3), "graded": len(have),
            "real_vs_drawn_auc": auc([scores[r["key"]][m] for r in real if m in scores[r["key"]]],
                                     [scores[r["key"]][m] for r in drawn if m in scores[r["key"]]]),
            # A higher score should mean the user was fooled more often.
            "twin_missed_auc": auc([scores[r["key"]][m] for r in twins if not all(r["detected"]) and m in scores[r["key"]]],
                                   [scores[r["key"]][m] for r in twins if all(r["detected"]) and m in scores[r["key"]]]),
            "by_arm": {}}
        arms = defaultdict(list)
        for r in test:
            if m in scores[r["key"]]:
                for arm in r["arms"]:
                    arms[arm].append(scores[r["key"]][m])
        table[m]["by_arm"] = {arm: round(float(np.mean(v)), 2) for arm, v in sorted(arms.items())}
    human = defaultdict(list)
    for r in graded:
        for arm in r["arms"]:
            human[arm].append(np.mean(r["grades"]))
    retest = [r["grades"] for r in graded if len(r["grades"]) > 1]
    summary = {"measures": table, "human_by_arm": {a: round(float(np.mean(v)), 2) for a, v in sorted(human.items())},
               "retest": {"images": len(retest), "same": sum(len(set(g)) == 1 for g in retest),
                          "mean_abs_diff": round(float(np.mean([abs(g[0] - g[1]) for g in retest])), 2) if retest else None,
                          "rho": round(float(spearmanr([g[0] for g in retest], [g[1] for g in retest])[0]), 2)
                          if len(retest) > 2 else None}}
    save_json(OUT / "summary.json", summary)
    print(f"{'measure':22} {'rho vs grade':>12} {'p':>6} {'n':>4} {'real/drawn AUC':>15} {'twin fooled AUC':>16}")
    for m, t in table.items():
        print(f"{m:22} {t['grade_rho']:>12} {t['grade_p']:>6} {t['graded']:>4} {str(t['real_vs_drawn_auc']):>15} "
              f"{str(t['twin_missed_auc']):>16}")
    print("retest", summary["retest"])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("embed", "specialists", "report"))
    parser.add_argument("--rater", default="claude-sonnet-5-5")
    parser.add_argument("--director", default="claude-opus-5-5")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    rows = dataset()
    save_json(OUT / "dataset.json", rows)
    if args.mode == "embed":
        embed(rows)
        pair_similarity()
    elif args.mode == "specialists":
        specialists(rows, args.rater, args.director, args.workers)
    report(rows)


if __name__ == "__main__":
    main()
