"""Turn a theme and producer wishes into ten-card set variants, with no manual steps.

Stages: plan, brief, draw, check, correct, deliver. Results land in runs/<slug>/ and finished work is kept.
"""

import argparse
import json
import os
import random
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # every local model is already cached

from common import ANALYSIS, ROOT, load_json, save_json

import numpy as np
import torch
from PIL import Image

from draw import draw
from estimate import write_masks
from form import CARD_FORM, card_schema
from measure import measure_card
from rate import ask_claude, ask_codex, card_prompt
from style import CATEGORY_RULES, FIXES, PATTERNS, STYLE

SIZE = (430, 480)
ROUNDS = 3
ALLOWED_MISSES = 2
RATED = ["identity", "staging"]
GROUPS = {"1": "floating", "2": "standing", "3": "standing", "4": "environment", "5": "environment"}
OBJECT_CLASSES = [c for c in CARD_FORM["identity"]["object_class"]["options"] if c != "character"]


def text():
    return {"type": "string"}


def strict(properties):
    return {"type": "object", "additionalProperties": False,
            "properties": properties, "required": list(properties)}


CARD_SCHEMA = strict({
    "name": text(), "subject": text(), "object_class": {"type": "string", "enum": OBJECT_CLASSES},
    "category": {"type": "string", "enum": ["1", "2", "3", "4"]},
    "pattern": {"type": "string", "enum": list(PATTERNS)},
    "hero_colors": text(), "backdrop_colors": text(), "surface_or_setting": text(),
})
PLAN_SCHEMA = strict({
    "title": text(), "story": text(),
    "variants": {"type": "array", "items": strict({"cards": {"type": "array", "items": CARD_SCHEMA}})},
})


def plan_prompt(theme, wishes, variants, knowledge):
    examples = "\n".join(
        f"{example['title']}: " + "; ".join(
            f"{card['name']} [{card['object_class']}, cat {card['category']}, {card['pattern']}]"
            for card in example["cards"]) for example in knowledge["example_sets"])
    return f"""You are the lead producer of card collections for a cozy mobile game.
Theme: {theme}
Producer wishes: {wishes or "none"}

Design {variants} clearly different versions of one ten-card set for this theme.

Rules learned from the game's real sets:
- title: 1-3 plain words that name the topic. A story behind the set is optional. Give it in one line or leave it empty.
- Card names: 1-2 plain words.
- Pick the first things anyone would name for the topic: instantly recognizable objects with a simple, distinctive silhouette.
- Every object must belong to this specific topic, not to the wider collection. A film genre set shows that genre's world, not generic cinema items such as film reels or popcorn.
- No characters, people or animal heroes, no brands, logos or real franchises. Keep dark topics playful and cute, never gory or violent.
- Real sets use {knowledge['set_ranges']['object_classes'][0]}-{knowledge['set_ranges']['object_classes'][1]} object classes and {knowledge['set_ranges']['scale_classes'][0]}-{knowledge['set_ranges']['scale_classes'][1]} real-world sizes, from handheld things to vehicles and buildings.
- Every version uses all four art categories: 1 floating object, 2 object on a plain ledge, 3 object on a real surface, 4 object in an environment. Use 2-4 of category 1, 1-2 of category 2, 2-4 of category 3 and 1-5 of category 4.
- For category 4 use pattern full_scene. Otherwise pick a graphic pattern.
- subject: one sentence on what to draw, with the two or three features that make it recognizable.
- Give every card a different color pairing. hero_colors must oppose backdrop_colors.
- surface_or_setting: the surface for categories 2-3 and the place for category 4, empty for category 1.
- Versions may share at most 5 objects.

Real sets from the game, as examples:
{examples}"""


def plan_problems(plan):
    problems = []
    if len(plan["title"].split()) > 3:
        problems.append("the title must be 1-3 words")
    names = []
    for index, variant in enumerate(plan["variants"], 1):
        cards = variant["cards"]
        names.append({card["name"].lower() for card in cards})
        if len(cards) != 10:
            problems.append(f"version {index} must have exactly ten cards")
        if {card["category"] for card in cards} != {"1", "2", "3", "4"}:
            problems.append(f"version {index} must use all four categories")
        if len(names[-1]) != len(cards):
            problems.append(f"version {index} repeats a card")
        problems += [f"card name too long: {c['name']}" for c in cards if len(c["name"].split()) > 2]
    for first in range(len(names)):
        for second in range(first + 1, len(names)):
            if len(names[first] & names[second]) > 5:
                problems.append(f"versions {first + 1} and {second + 1} share too many objects")
    return problems


def make_plan(theme, wishes, variants, knowledge):
    prompt = plan_prompt(theme, wishes, variants, knowledge)
    plan = ask_claude(prompt, None, PLAN_SCHEMA)
    problems = plan_problems(plan)
    if problems:
        plan = ask_claude(f"{prompt}\n\nYour last answer had these problems, fix them: {problems}\n"
                          f"Last answer: {json.dumps(plan)}", None, PLAN_SCHEMA)
    plan["problems"] = plan_problems(plan)
    return plan


def pick_references(card, cards, used, rng):
    pool = [c for c in cards if c["form"]["staging"]["art_category"] == card["category"]
            and "staging.art_category" not in c["disputed"]]
    ranked = sorted(pool, key=lambda c: (
        c["form"]["backdrop"]["pattern"] != card["pattern"],
        c["form"]["identity"]["object_class"] != card["object_class"],
        used[c["id"]], rng.random()))
    picks = ranked[:3]
    used.update(c["id"] for c in picks)
    return picks


def card_brief(card, fixes=()):
    backdrop = PATTERNS[card["pattern"]]
    lines = [STYLE, f"Subject: {card['subject']}", f"Hero colors: {card['hero_colors']}.",
             f"Staging: {CATEGORY_RULES[card['category']]}",
             f"Backdrop: {backdrop} in {card['backdrop_colors']}."]
    if card["surface_or_setting"]:
        lines.append(f"Surface or setting: {card['surface_or_setting']}.")
    lines += fixes
    return "\n".join(lines)


def make_briefs(plan, cards, seed):
    rng = random.Random(seed)
    used = Counter()
    briefs = []
    for variant, entry in enumerate(plan["variants"], 1):
        for index, card in enumerate(entry["cards"], 1):
            picks = pick_references(card, cards, used, rng)
            briefs.append({"id": f"v{variant}_{index:02d}", "variant": variant, "card": card,
                           "references": [c["id"] for c in picks]})
    return briefs


def draw_card(run, brief, attempt, fixes, use_references):
    try_id = f"{brief['id']}_{attempt}"
    out, full = run / "tries" / f"{try_id}.png", run / "full" / f"{try_id}.png"
    if out.exists():
        return try_id
    references = [ROOT / f"materials/card_examples/{i}.png" for i in brief["references"]]
    prompt = card_brief(brief["card"], fixes)
    (run / "prompts").mkdir(exist_ok=True)
    (run / "prompts" / f"{try_id}.txt").write_text(prompt, "utf-8")
    for tries_left in (1, 0):
        try:
            draw(prompt, references if use_references else [], full)
            out.parent.mkdir(exist_ok=True)
            Image.open(full).convert("RGB").resize(SIZE, Image.LANCZOS).save(out)
            return try_id
        except Exception as error:
            print(f"{try_id}: {type(error).__name__} {str(error)[:160]}", flush=True)
            if not tries_left:
                return None


def rate_blind(path):
    """A stuck or failed rating marks the card unrated, and never stops the run."""
    for attempt in (1, 2):
        try:
            return ask_codex(card_prompt(RATED), path, card_schema(RATED), timeout=180)
        except Exception as error:
            print(f"{path.stem} rating attempt {attempt}: {type(error).__name__}", flush=True)
    return None


def judge_names(pairs):
    schema = strict({"same": {"type": "array", "items": {"type": "boolean"}}})
    listing = "\n".join(f"{i}. asked for: {asked} | seen: {seen}" for i, (asked, seen) in enumerate(pairs))
    prompt = ("A rater saw each image without knowing what it should show. For each line, is what they "
              f"saw the same kind of thing as what was asked for? Answer one boolean per line.\n{listing}")
    return ask_claude(prompt, None, schema)["same"]


def check_tries(run, tries, knowledge, workers):
    """Run new tries through the same analysis as the references, and list what fails."""
    from embed import MODELS, load_csd

    records = [{"id": t["try_id"], "file": str((run / "tries" / f"{t['try_id']}.png").relative_to(ROOT))}
               for t in tries]
    write_masks(records, "cuda", run / "derived" / "masks")
    encode = load_csd(MODELS["csd"])
    references = np.load(ANALYSIS / "embeddings" / "csd_whole.npy")
    images = [Image.open(ROOT / r["file"]).convert("RGB") for r in records]
    with torch.inference_mode():
        vectors = encode(images)
        vectors = (vectors / vectors.norm(dim=-1, keepdim=True)).float().cpu().numpy()
    nearest = (vectors @ references.T).max(axis=1)
    with ThreadPoolExecutor(workers) as pool:
        ratings = list(pool.map(lambda r: rate_blind(ROOT / r["file"]), records))
    same = judge_names([(t["card"]["subject"], r["identity"]["subject"] if r else "nothing")
                         for t, r in zip(tries, ratings)])

    for entry, record, score, rating, named in zip(tries, records, nearest, ratings, same):
        category = entry["card"]["category"]
        measured = measure_card(record, run / "derived")
        misses = [path for path, (low, high) in knowledge["bands"][category].items()
                  if not low <= measured[path.split(".")[0]][path.split(".")[1]] <= high]
        issues = []
        if float(score) < knowledge["style"]["min"]:
            issues.append("style")
        if float(score) > knowledge["style"]["copy"]:
            issues.append("copy")
        if rating is None:
            issues.append("unrated")
        elif GROUPS[rating["staging"]["art_category"]] != GROUPS[category]:
            issues.append("art_category")
        if rating and not named:
            issues.append("identity")
        entry.update(style=round(float(score), 3), misses=misses, issues=issues, seen=rating,
                     passed=not issues and len(misses) <= ALLOWED_MISSES)
    return tries


def best_try(tries):
    return min(tries, key=lambda t: (not t["passed"], len(t["issues"]), len(t["misses"])))


def contact_sheet(paths, out, columns=5):
    tile = (258, 288)
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile[0], rows * tile[1]), "white")
    for index, path in enumerate(paths):
        sheet.paste(Image.open(path).convert("RGB").resize(tile), (index % columns * tile[0], index // columns * tile[1]))
    sheet.save(out)


def deliver(run, plan, briefs, history):
    lines = [f"# {plan['title']}", "", plan.get("story") or "", ""]
    counts = Counter()
    for variant in range(1, len(plan["variants"]) + 1):
        folder = run / f"variant_{variant}"
        folder.mkdir(exist_ok=True)
        paths = []
        lines += [f"## Variant {variant}", "", "| Card | Category | Tries | Style | Status | Open issues |",
                  "|---|---|---:|---:|---|---|"]
        for brief in [b for b in briefs if b["variant"] == variant]:
            tries = history[brief["id"]]
            best = best_try(tries)
            name = re.sub(r"[^a-z0-9]+", "_", brief["card"]["name"].lower()).strip("_")
            path = folder / f"{brief['id'][-2:]}_{name}.png"
            Image.open(run / "tries" / f"{best['try_id']}.png").save(path)
            paths.append(path)
            counts.update(best["misses"] + best["issues"])
            open_issues = ", ".join(best["issues"] + [m.split(".")[1] for m in best["misses"]]) or "none"
            lines.append(f"| {brief['card']['name']} | {brief['card']['category']} | {len(tries)} | {best['style']} | "
                         f"{'pass' if best['passed'] else 'review'} | {open_issues} |")
        contact_sheet(paths, run / f"variant_{variant}.png")
        lines.append("")
    lines += ["## Most common open issues", ""] + [f"- {key}: {value}" for key, value in counts.most_common(8)]
    (run / "report.md").write_text("\n".join(lines) + "\n", "utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme")
    parser.add_argument("--wishes", default="")
    parser.add_argument("--variants", type=int, default=3)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    parser.add_argument("--plan", help="reuse the plan.json of an earlier run")
    parser.add_argument("--no-references", action="store_true", help="draw from text alone, as a control")
    args = parser.parse_args()

    slug = re.sub(r"[^a-z0-9]+", "-", args.theme.lower()).strip("-") + ("-noref" if args.no_references else "")
    run = ROOT / "runs" / slug
    run.mkdir(parents=True, exist_ok=True)
    knowledge = load_json(ANALYSIS / "knowledge.json")
    cards = load_json(ANALYSIS / "cards.json")

    plan_path = run / "plan.json"
    if args.plan:
        save_json(plan_path, load_json(ROOT / args.plan))
    if not plan_path.exists():
        save_json(plan_path, make_plan(args.theme, args.wishes, args.variants, knowledge))
    plan = load_json(plan_path)
    print("plan:", plan["title"], "|", plan.get("problems") or "no problems", flush=True)

    briefs_path = run / "briefs.json"
    if not briefs_path.exists():
        save_json(briefs_path, make_briefs(plan, cards, seed=args.theme))
    briefs = load_json(briefs_path)

    history = defaultdict(list)
    for attempt in range(1, args.rounds + 1):
        waiting = [b for b in briefs if not any(t["passed"] for t in history[b["id"]])]
        if not waiting:
            break
        fixes = {b["id"]: sorted({FIXES[key] for t in history[b["id"]] for key in t["misses"] + t["issues"] if key in FIXES})
                 for b in waiting}
        with ThreadPoolExecutor(args.workers) as pool:
            done = list(pool.map(lambda b: draw_card(run, b, attempt, fixes[b["id"]], not args.no_references), waiting))
        tries = [{"try_id": try_id, "brief_id": b["id"], "card": b["card"]} for b, try_id in zip(waiting, done) if try_id]
        for entry in check_tries(run, tries, knowledge, args.workers):
            history[entry["brief_id"]].append(entry)
        save_json(run / "check.json", history)
        print(f"round {attempt}: drew {len(tries)}, passed {sum(t['passed'] for t in tries)}", flush=True)

    deliver(run, plan, briefs, history)
    print("done:", run / "report.md")


if __name__ == "__main__":
    main()
