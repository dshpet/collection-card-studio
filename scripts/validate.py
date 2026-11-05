"""Test the pipeline itself. Rerun after changing the generator or the check.

off-style: can the check reject images that are plainly the wrong style? Drawn for the first card of a run's plan.
acceptance: can vision models pick out one generated card hidden among nine real ones? A weak test: see STYLE_GAPS.
The first run's results of both are in runs/first; new ones go to runs/off-style and runs/acceptance.
twins: redraw real cards with the card itself hidden, so style can be compared with content held equal.
"""

import argparse
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, ROOT, best_try, load_json, save_json

from PIL import Image

from draw import draw
from make_set import SIZE, check_tries, contact_sheet, draw_card, strict, text
from rate import ask_claude, ask_codex

STYLES = {"photo": "a real studio photograph, photorealistic, natural materials",
          "vector": "flat vector illustration with solid colors and no shading",
          "pixel": "16-bit pixel art with visible square pixels",
          "watercolor": "loose traditional watercolor painting on paper",
          "lineart": "black ink line drawing on white paper, no color",
          "clay": "dull grey clay sculpture on a plain grey background, muted colors"}
ACCEPTANCE_PROMPT = """This sheet shows ten mobile-game collection cards in two rows, slots 1-5 on top and 6-10 below.
Nine were made by the game's art team and one by a different production process, possibly AI.
Ignore the subject matter and theme. Judge only rendering, shading, finish, color and detail.
Which slot is the odd one out? Give your best guess even if unsure."""


def off_style(run_name):
    run = ROOT / "runs" / "off-style" / run_name.replace("/", "_")
    card = load_json(ROOT / "runs" / run_name / "plan.json")["variants"][0]["cards"][0]

    def one(name):
        out, full = run / "tries" / f"{name}.png", run / "full" / f"{name}.png"
        for _ in range(3):
            if out.exists():
                break
            try:
                style = STYLES[name]
                draw(f"{card['subject']} Floating in the center of a {style} image. "
                     f"Make the whole image in this style: {style}. No text.", [], full)
                out.parent.mkdir(exist_ok=True)
                Image.open(full).convert("RGB").resize(SIZE, Image.LANCZOS).save(out)
            except Exception as error:
                print(name, type(error).__name__, flush=True)
        return name

    with ThreadPoolExecutor(4) as pool:
        names = [n for n in pool.map(one, STYLES) if (run / "tries" / f"{n}.png").exists()]
    tries = check_tries(run, [{"try_id": n, "brief_id": n, "card": card} for n in names],
                        load_json(ANALYSIS / "knowledge.json"), 4)
    save_json(run / "check.json", tries)
    contact_sheet([run / "tries" / f"{n}.png" for n in names], run / "sheet.png", columns=6)
    for entry in tries:
        print(entry["try_id"], "pass" if entry["passed"] else "reject", entry["style"], entry["issues"])


def acceptance(run_names, trials):
    run = ROOT / "runs" / "acceptance" / "+".join(run_names).replace("/", "_")
    (run / "sheets").mkdir(parents=True, exist_ok=True)
    rng = random.Random(7)
    real = [c for c in load_json(ANALYSIS / "cards.json") if c["form"]["staging"]["art_category"] != "5"]
    generated = []
    for name in run_names:
        for tries in load_json(ROOT / "runs" / name / "check.json").values():
            best = best_try(tries)
            if best["passed"]:
                generated.append((name, best["card"]["name"], ROOT / "runs" / name / "tries" / f"{best['try_id']}.png"))
    schema = strict({"odd_slot": {"type": "integer"},
                     "confidence": {"type": "string", "enum": ["low", "medium", "high"]}, "reason": text()})
    jobs = []
    for index, (genre, name, path) in enumerate(rng.sample(generated, min(trials, len(generated)))):
        slot = rng.randrange(10)
        paths = [ROOT / f"materials/card_examples/{c['id']}.png" for c in rng.sample(real, 9)]
        paths.insert(slot, path)
        sheet = run / "sheets" / f"{index:02d}.png"
        contact_sheet(paths, sheet)
        jobs += [(rater, {"genre": genre, "name": name, "slot": slot + 1}, sheet) for rater in ("codex", "claude")]

    def ask(job):
        rater, trial, sheet = job
        call = ask_codex if rater == "codex" else ask_claude
        for _ in range(2):
            try:
                answer = call(ACCEPTANCE_PROMPT, sheet, schema)
                return {**trial, "rater": rater, **answer, "hit": answer["odd_slot"] == trial["slot"]}
            except Exception as error:
                print(type(error).__name__, flush=True)

    with ThreadPoolExecutor(4) as pool:
        results = [r for r in pool.map(ask, jobs) if r]
    save_json(run / "results.json", results)
    for rater in ("codex", "claude"):
        rows = [r for r in results if r["rater"] == rater]
        print(rater, "found", sum(r["hit"] for r in rows), "of", len(rows), "(chance 10%)")
    print("found by genre", Counter(r["genre"] for r in results if r["hit"]))


def twins(label):
    briefs = load_json(ROOT / "runs" / "twins" / "briefs.json")
    run = ROOT / "runs" / "twins" / label
    run.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(4) as pool:
        done = list(pool.map(lambda brief: draw_card(run, brief, 1, [], True), briefs))
    save_json(run / "check.json", {brief["id"]: [{"try_id": try_id, "card": brief["card"], "passed": True,
                                                  "issues": [], "misses": []}]
                                   for brief, try_id in zip(briefs, done) if try_id})
    drawn = [(brief, try_id) for brief, try_id in zip(briefs, done) if try_id]
    paths = [ROOT / f"materials/card_examples/{brief['real']}.png" for brief, _ in drawn]
    paths += [run / "tries" / f"{try_id}.png" for _, try_id in drawn]
    if drawn:
        contact_sheet(paths, run / "sheet.png", columns=len(drawn))
    print("drew", sum(bool(t) for t in done), "of", len(briefs))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("test", choices=("off-style", "acceptance", "twins"))
    parser.add_argument("--label", default="baseline")
    parser.add_argument("--runs", nargs="+", help="runs to test, for off-style and acceptance")
    parser.add_argument("--trials", type=int, default=24)
    args = parser.parse_args()
    if args.test != "twins" and not args.runs:
        parser.error(f"{args.test} needs --runs")
    if args.test == "off-style":
        off_style(args.runs[0])
    elif args.test == "twins":
        twins(args.label)
    else:
        acceptance(args.runs, args.trials)


if __name__ == "__main__":
    main()
