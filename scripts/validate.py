"""Test the pipeline itself. Rerun after changing the generator or the check.

off-style: can the check reject images that are plainly the wrong style?
acceptance: can vision models pick out one generated card hidden among nine real ones?
"""

import argparse
import random
from collections import Counter

from make_set import (ANALYSIS, ROOT, SIZE, Image, ThreadPoolExecutor, ask_claude, ask_codex, best_try,
                      check_tries, contact_sheet, draw, load_json, save_json, strict, text)

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
    run = ROOT / "runs" / "controls-off-style"
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
    run = ROOT / "runs" / "acceptance"
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
    for index, (genre, name, path) in enumerate(rng.sample(generated, trials)):
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("test", choices=("off-style", "acceptance"))
    parser.add_argument("--runs", nargs="+", default=["western", "sci-fi", "horror"])
    parser.add_argument("--trials", type=int, default=24)
    args = parser.parse_args()
    if args.test == "off-style":
        off_style(args.runs[0])
    else:
        acceptance(args.runs, args.trials)


if __name__ == "__main__":
    main()
