"""Tune the art director's judging notes on pairs the producer decided, and check them on pairs it never saw.

The pairs of experiments/prefer.py split by object into a tuning half and a held-out half. Each round the director judges
the tuning half with the current notes, an editor sees its mistakes with the producer's own comments and proposes one
change, and the change stays only if agreement rises by more than MARGIN pairs. At the end the tuned notes and the
untouched prompt each judge the held-out half once. None held out (analysis/STYLE_GAPS.md).

    tune.py --rounds 6
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from common import JUDGE, ROOT, load_json, save_json, strict, text

from prefer import BATCH, OUT as PAIRS, pairs
from review import array, ask, judge_sheet

OUT = ROOT / "runs" / "tune"
MARGIN = 3
SHOWN_MISTAKES = 8


def split(rows):
    test = [r for r in rows if not r["lesson"]]
    tuning, held = [], []
    rng = random.Random(21)
    for source in ("closest", "trial", "set"):
        objects = sorted({r["object"] for r in test if r["object"].startswith(source)})
        rng.shuffle(objects)
        half = set(objects[::2])
        tuning += [r for r in test if r["object"] in half]
        held += [r for r in test if r["object"].startswith(source) and r["object"] not in half]
    return tuning, held


def comments():
    """The producer's notes, by image and by closest-pick object."""
    found = defaultdict(list)
    from rate_ui import items
    ratings = {v["id"]: v for v in load_json(ROOT / "runs" / "ratings.json").values() if v.get("comment")}
    for item in items():
        rating = ratings.get(item["id"])
        if not rating:
            continue
        if item["kind"] == "closest":
            found[f"closest/{item['id'].split('/')[1]}"].append(rating["comment"])
        else:
            for path in item["images"]:
                if path.startswith("runs/"):
                    found[path].append(rating["comment"])
    return found


def lessons(rows):
    folder = PAIRS / "sheets"
    out = []
    for row in [r for r in rows if r["lesson"]]:
        labels = ("A, preferred", "B") if row["user"] == "A" else ("A", "B, preferred")
        out.append((judge_sheet(row, folder / f"lesson_{row['pair']}.png", labels), row["lesson"]))
    return out


def schema(batch):
    return strict({"pairs": array(strict({
        "pair": {"type": "string", "enum": [r["pair"] for r in batch]},
        "closer": {"type": "string", "enum": ["A", "B", "neither"]},
        "confidence": {"type": "integer", "minimum": 1, "maximum": 5}, "why": text()}))})


def judge(rows, notes, taught, rater, label, workers):
    """The director's answers on rows, cached under label."""
    folder = OUT / "judged" / label
    batches = [rows[i:i + BATCH] for i in range(0, len(rows), BATCH)]
    brief = (ROOT / "analysis" / "agents" / "art_director.md").read_text("utf-8")
    first = len(taught) + 1
    lesson_list = "; ".join(f"image {i + 1}: {note}" for i, (_, note) in enumerate(taught))
    extra = f"\nJudging notes, learned from the art lead's past choices:\n{notes}\n" if notes.strip() else ""

    def one(index):
        out = folder / f"{index:02d}.json"
        if out.exists():
            return load_json(out)
        batch = batches[index]
        listing = ", ".join(f"{r['pair']} is image {i + first}" for i, r in enumerate(batch))
        prompt = (f"{brief}{extra}\nEach image shows real cards from the game on top, marked REAL, and below them two "
                  f"drawings of the same object, A and B, made by an image model. Images 1 to {first - 1} are lessons: "
                  f"the art lead marked the drawing they found closer to the real cards ({lesson_list}). Learn which way "
                  "the differences run from them, and trust them over any idea of what game art should look like. Then "
                  f"judge the test pairs ({listing}). Which drawing is closer in look to the real cards above it: "
                  "rendering, shape, color, light, finish, and whether it is built like a real object? Answer A, B or "
                  "neither, with confidence 1-5, and say why in one sentence.")
        result = ask(rater, prompt, [p for p, _ in taught] + [PAIRS / "sheets" / f"{r['pair']}.png" for r in batch],
                     schema(batch))
        if result:
            save_json(out, result)
        return result

    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(one, range(len(batches))))
    return {p["pair"]: p for result in results if result for p in result["pairs"]}


def agreement(rows, answers, confident=1):
    key = {r["pair"]: r["user"] for r in rows}
    decided = [p for p, a in answers.items() if p in key and a["closer"] != "neither" and a["confidence"] >= confident]
    return sum(answers[p]["closer"] == key[p] for p in decided), len(decided)


def propose(notes, rows, answers, user_notes, rater, round_number):
    wrong = [r for r in rows if r["pair"] in answers and answers[r["pair"]]["closer"] not in ("neither", r["user"])]
    random.Random(round_number).shuffle(wrong)
    shown = wrong[:SHOWN_MISTAKES]
    lines = []
    for i, row in enumerate(shown, 1):
        said = [*user_notes.get(row["object"], []), *user_notes.get(row[row["user"]], [])]
        lines.append(f"image {i}: the director chose {answers[row['pair']]['closer']} because "
                     f"\"{answers[row['pair']]['why']}\". The art lead preferred {row['user']}."
                     + (f" The art lead's notes on these cards: {' | '.join(said)}" if said else ""))
    prompt = (f"You maintain the judging notes of an art director. The director sees real game cards and two drawings "
              f"of one object, and says which drawing is closer to the real cards. The art lead's choices are the "
              f"truth. The director agreed with them on {sum(1 for r in rows if r['pair'] in answers) - len(wrong)} "
              f"of {len(rows)} pairs this round. Current notes:\n{notes or '(none)'}\n\nThe images are pairs it got "
              f"wrong:\n" + "\n".join(lines) + "\n\nPropose exactly one change to the notes: add, rewrite or delete one "
              "note. It must name a pattern that holds across several mistakes, in plain visual words, never one "
              "object. Keep the whole list under 8 notes of at most 30 words each. Return the full new notes, one "
              "per line starting with '- ', and the change in one sentence.")
    return ask(rater, prompt, [PAIRS / "sheets" / f"{r['pair']}.png" for r in shown],
               strict({"change": text(), "notes": text()}))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rounds", type=int, default=6)
    parser.add_argument("--rater", default=JUDGE)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    rows = pairs()
    tuning, held = split(rows)
    taught = lessons(rows)
    user_notes = comments()
    log = load_json(OUT / "log.json") if (OUT / "log.json").exists() else []
    notes = log[-1]["kept_notes"] if log else ""
    answers = judge(tuning, notes, taught, args.rater, f"tune_{len(log):02d}_kept", args.workers)
    score = agreement(tuning, answers)[0]
    print(f"start: {score} of {len(tuning)}", flush=True)
    for round_number in range(len(log) + 1, args.rounds + 1):
        proposal = propose(notes, tuning, answers, user_notes, args.rater, round_number)
        if not proposal:
            continue
        trial = judge(tuning, proposal["notes"], taught, args.rater, f"tune_{round_number:02d}_try", args.workers)
        trial_score = agreement(tuning, trial)[0]
        kept = trial_score >= score + MARGIN
        if kept:
            notes, answers, score = proposal["notes"], trial, trial_score
        log.append({"round": round_number, "change": proposal["change"], "tried": trial_score, "kept": kept,
                    "score": score, "kept_notes": notes})
        save_json(OUT / "log.json", log)
        print(f"round {round_number}: {trial_score} {'kept' if kept else 'dropped'}: {proposal['change']}", flush=True)
    result = {"tuning": len(tuning), "held": len(held), "notes": notes}
    for label, text_ in (("held_untouched", ""), ("held_tuned", notes)):
        held_answers = judge(held, text_, taught, args.rater, label, args.workers)
        result[label] = {f"confidence>={c}": agreement(held, held_answers, c) for c in (1, 3, 4)}
    old = {p["pair"]: p for path in (PAIRS / "reviewers" / "art_director").glob("*.json") for p in load_json(path)["pairs"]}
    result["held_first_run"] = {f"confidence>={c}": agreement(held, old, c) for c in (1, 3, 4)}
    save_json(OUT / "result.json", result)
    print(result, flush=True)


if __name__ == "__main__":
    main()
