"""Review the final plans against their alternatives before the final draw.

For each final genre: every card of the three pre-final variants with the outside rater's grade, the producer's grades
of the same object in earlier runs, and the pipeline's checks of its drawing; the set numbers of each variant against
the real sets (scripts/compare.py); the planner's rule and sensitivity checks on the chosen variant; and a lessons
check by the judge model, which may propose swaps from the other variants. Grades are the evidence; the model's
proposals are suggestions.

    plan_review.py            writes runs/night/plan_review.json and prints the tables
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from collections import defaultdict

from common import ANALYSIS, JUDGE, ROOT, best_try, load_json, save_json, strict, text

FINAL = {"western": 1, "period-drama": 3, "detective": 2}
OUT = ROOT / "runs" / "night" / "plan_review.json"


def outside_grades():
    ratings = load_json(ROOT / "runs" / "prefinal" / "outside" / "ratings.json")
    return {k.split("|")[0][len("card/"):]: v for k, v in ratings.items() if k.startswith("card/")}


def producer_grades():
    """The producer's grades of set cards, by card name, from runs/ratings.json."""
    by_name = defaultdict(list)
    for entry in load_json(ROOT / "runs" / "ratings.json").values():
        if entry.get("kind") != "card" or not entry.get("grade"):
            continue
        run, brief_id = entry["id"].split("/")[1], entry["id"].split("/")[2]
        briefs = ROOT / "runs" / run / "briefs.json"
        if briefs.exists():
            brief = next((b for b in load_json(briefs) if b["id"] == brief_id), None)
            if brief:
                by_name[brief["card"]["name"].lower()].append((run, entry["grade"], entry.get("comment", "")))
    return by_name


def evidence(genre, outside, producer):
    run = ROOT / "runs" / "prefinal" / genre
    history = load_json(run / "check.json")
    edits = {e["edit"]: e for e in load_json(run / "edits.json")} if (run / "edits.json").exists() else {}
    rows = []
    for brief in load_json(run / "briefs.json"):
        card, tries = brief["card"], history.get(brief["id"], [])
        best = best_try(tries) if tries else {}
        graded = outside.get(f"prefinal/{genre}/{brief['id']}", {})
        rows.append({"id": brief["id"], "variant": brief["variant"], "name": card["name"], "category": card["category"],
                     "pattern": card["pattern"], "model": (run / "models" / f"{brief['id']}.png").exists(),
                     "subject": card["subject"], "hero_colors": card["hero_colors"],
                     "backdrop_colors": card["backdrop_colors"], "surface_or_setting": card["surface_or_setting"],
                     "outside_grade": graded.get("grade"), "outside_broken": bool(graded.get("broken")),
                     "outside_comment": graded.get("comment", ""),
                     "producer_before": producer.get(card["name"].lower(), []),
                     "check": {"passed": best.get("passed"), "issues": best.get("issues"), "unsure": best.get("unsure"),
                               "edited": best.get("try_id") in edits},
                     "image": f"runs/prefinal/{genre}/tries/{best['try_id']}.png" if best else None})
    return rows


def set_numbers(genre):
    from compare import real_rows, set_row
    from embed import MODELS, load_csd

    encode = load_csd(MODELS["csd"])
    run = f"prefinal/{genre}"
    briefs = load_json(ROOT / "runs" / run / "briefs.json")
    variants = sorted({b["variant"] for b in briefs})
    ours = {v: set_row(run, [b["id"] for b in briefs if b["variant"] == v], encode) for v in variants}
    real = real_rows()
    ranges = {key: (min(r[key] for r in real), max(r[key] for r in real))
              for key in ("object_classes", "scale_classes", "background_hues", "style_similarity")}
    return {"variants": ours, "real_ranges": ranges}


def lessons_check(genre, rows, chosen):
    """The judge model reads the lessons and the planner's rules, sees the three variants with their grades and
    proposes what to keep, reword or swap in the chosen variant."""
    from experience import lessons
    from make_set import plan_prompt
    from rate import ask_claude

    rules = [line for line in plan_prompt(genre.replace("-", " ").title(), "A set for a Movie collection", 3,
                                          load_json(ANALYSIS / "knowledge.json")).splitlines() if line.startswith("- ")]
    listing = "\n".join(
        f"{r['id']} (variant {r['variant']}{', CHOSEN' if r['variant'] == chosen else ''}): {r['name']} | category "
        f"{r['category']}, {r['pattern']} | {r['subject']} | colors: {r['hero_colors']} on {r['backdrop_colors']}"
        f"{' | ' + r['surface_or_setting'] if r['surface_or_setting'] else ''} | outside grade "
        f"{r['outside_grade'] or 'not graded'}{', BROKEN' if r['outside_broken'] else ''}"
        + (f" | producer's grades of this object before: {[g for _, g, _ in r['producer_before']]}" if r["producer_before"] else "")
        for r in rows)
    sheets = [ROOT / "runs" / "prefinal" / genre / f"variant_{v}.png" for v in (1, 2, 3)]
    schema = strict({
        "cards": {"type": "array", "items": strict({
            "id": {"type": "string", "enum": [r["id"] for r in rows if r["variant"] == chosen]},
            "verdict": {"type": "string", "enum": ["keep", "reword", "swap"]},
            "swap_for": text(), "why": text()})},
        "set_notes": text()})
    prompt = f"""You are the lead producer of card collections for a cozy mobile game, reviewing a film-genre set before its final drawing. The images are the three drafted variants of the {genre.replace('-', ' ').title()} set, variant 1 to 3, each ten cards in order. Variant {chosen} was chosen to be redrawn as the final set.

Every card of the three variants, with grades where they exist. Grades: 1-5 from an outside artist (half the cards were graded), and the producer's grades of the same object in earlier runs, which count most. BROKEN means the drawing was judged impossible to build or in broken perspective.
{listing}

The planner's rules:
{chr(10).join(rules)}

Lessons from the producer's grades:
{chr(10).join(lessons('Planning'))}

For each card of variant {chosen}: keep it, reword its subject (say how), or swap it for a card of another variant (give its id) that is better on the evidence. A swap must keep the set within the category rules (every category used; 2-4 of category 1, 1-2 of category 2, 2-4 of category 3, 1-5 of category 4), must not repeat an object, and must keep about six backdrop colors across the set. Judge the plan, not the drawing's style: is each object iconic for the genre, recognizable alone, buildable, and does the set hold together? Prefer the evidence of grades over your own taste. set_notes: one or two sentences on the set as a whole."""
    return ask_claude(prompt, sheets, schema, JUDGE)


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    from make_set import plan_problems, sensitive_cards

    outside, producer = outside_grades(), producer_grades()
    result = load_json(OUT) if OUT.exists() else {}
    for genre, chosen in FINAL.items():
        entry = result.setdefault(genre, {})
        entry["chosen"] = chosen
        entry["cards"] = rows = evidence(genre, outside, producer)
        if "numbers" not in entry:
            entry["numbers"] = set_numbers(genre)
        plan = load_json(ROOT / "runs" / "plans" / f"final-{genre}.json")
        entry["problems"] = plan_problems(plan, 0, 1)
        if "sensitive" not in entry:
            entry["sensitive"] = sensitive_cards(plan)
        if "lessons" not in entry:
            entry["lessons"] = lessons_check(genre, rows, chosen)
        save_json(OUT, result)

        print(f"\n## {genre}: chosen variant {chosen}")
        for v, row in entry["numbers"]["variants"].items():
            print(f"variant {v}: classes {row['object_classes']}, scales {row['scale_classes']}, backdrop hues "
                  f"{row['background_hues']}, categories {row['categories']}, style similarity {row['style_similarity']}")
        print("real ranges:", entry["numbers"]["real_ranges"])
        for r in rows:
            mark = "*" if r["variant"] == chosen else " "
            before = ", ".join(f"{run} {g}" for run, g, _ in r["producer_before"])
            print(f"{mark} {r['id']} {r['name']:16} cat {r['category']} {'model' if r['model'] else '     '} outside "
                  f"{r['outside_grade'] or '-'}{' BROKEN' if r['outside_broken'] else ''}"
                  + (f" | producer before: {before}" if before else "")
                  + (f" | issues {r['check']['issues']}" if r["check"]["issues"] else ""))
        print("rule problems:", entry["problems"] or "none", "| sensitive:", entry["sensitive"] or "none")
        for card in entry["lessons"]["cards"]:
            print(f"  {card['id']}: {card['verdict']} {card['swap_for']} | {card['why']}")
        print("  set:", entry["lessons"]["set_notes"])


if __name__ == "__main__":
    main()
