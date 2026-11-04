"""Turn a theme and producer wishes into ten-card set variants, with no manual steps.

Stages: plan, brief, model, draw candidates, check, choose, review, edit, deliver.
Results land in runs/<slug>/ and finished work is kept.
"""

import argparse
import json
import os
import random
import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # every local model is already cached

from common import ANALYSIS, ROOT, best_try, load_json, save_json

import numpy as np
import torch
from PIL import Image

from draw import draw
from estimate import write_masks
from form import CARD_FORM, card_schema
from measure import measure_card
from rate import ask_claude, ask_codex, card_prompt
from style import BLOCKOUT, CATEGORY_RULES, EDIT, PATTERNS, STYLE

SIZE = (430, 480)
CANDIDATES = 3
MODEL_ROUNDS = 2
REVIEW_ROUNDS = 2
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
MODEL_SCHEMA = strict({"model": text()})
SENSITIVE_SCHEMA = strict({"flagged": {"type": "array", "items": strict({"name": text(), "why": text()})}})
LOOK_SCHEMA = strict({"ok": {"type": "boolean"}, "problems": {"type": "array", "items": text()}, "model": text()})


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
- title: the topic itself, in 1-2 plain words, like "Beach" or "Road Trip". A story behind the set is optional. Give it in one line or leave it empty.
- Card names: 1-2 plain words.
- Pick the first things anyone would name for the topic: instantly recognizable objects with a simple, distinctive silhouette.
- Every object must belong to this specific topic, not to the wider collection. A film genre set shows that genre's world, not generic cinema items such as film reels or popcorn.
- Each card alone must make someone name the topic. Skip ordinary objects that fit only next to the others, such as an armchair in a horror set.
- The audience is wide and casual, of every age and faith. Nothing morbid, sad or divisive: no death or burial objects (coffins, graves, tombstones, skulls, bones), no religious symbols (crosses, holy books, altars), no illness, injury, drugs or politics. Haunted-house fun is fine: a pumpkin, a cauldron, a friendly ghost sheet.
- No characters or people, no brands, logos or real franchises. An animal may appear as an object, at most once in a set. No weapons of any kind, toy or sci-fi ones included. No blood or gore. Keep dark topics playful.
- Cards carry no text, so skip objects that need readable words to make sense.
- Real sets use {knowledge['set_ranges']['object_classes'][0]}-{knowledge['set_ranges']['object_classes'][1]} object classes and {knowledge['set_ranges']['scale_classes'][0]}-{knowledge['set_ranges']['scale_classes'][1]} real-world sizes, from handheld things to vehicles and buildings.
- Every version uses all four art categories: 1 floating object, 2 object on a plain ledge, 3 object on a real surface, 4 object in an environment. Use 2-4 of category 1, 1-2 of category 2, 2-4 of category 3 and 1-5 of category 4.
- For category 4 use pattern full_scene. Otherwise pick a graphic pattern.
- subject: one plain sentence on what to draw, with the two or three features that make it recognizable. Name the object and its parts only, with no mood, style or props.
- hero_colors are the object's natural colors plus one small accent in another hue, which nearly all real cards have. Give every card a backdrop whose color contrasts with the hero, and use at least six different backdrop hues across a set.
- backdrop_colors are bright and clean, as in the real cards: sky blue, cyan, yellow, orange, purple, pink, grass green. Never dusty, muted, dull or dark. Skies stay clear and bright, even on dark topics.
- surface_or_setting: the surface for categories 2-3 and the place for category 4, empty for category 1. Real sets reuse one or two ground materials across their cards, so reuse them too.
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
    flagged = sensitive_cards(plan)
    if flagged:
        plan = ask_claude(f"{prompt}\n\nThese cards may upset players, replace them with other objects and keep every "
                          f"rule: {flagged}\nLast answer: {json.dumps(plan)}", None, PLAN_SCHEMA)
        plan["problems"] = plan_problems(plan)
        plan["sensitive"] = sensitive_cards(plan)
    return plan


def sensitive_cards(plan):
    """A separate check that no card could offend or upset a wide, casual audience."""
    names = sorted({card["name"] for variant in plan["variants"] for card in variant["cards"]})
    answer = ask_claude(f"""A cozy mobile game for a wide, casual audience of every age, culture and faith shows these collection cards for the set "{plan['title']}": {names}.
Flag every card that could offend, upset or sadden some players: death and burial (coffins, graves, tombstones, skulls), religious symbols, illness or injury, drugs, weapons, politics, national or cultural stereotypes, or anything a parent would not want a child to see. Playful spooky or fantasy objects are fine. Give the card name and a short reason. Flag nothing if all are fine.""", None, SENSITIVE_SCHEMA)
    return answer["flagged"]


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


def card_brief(card):
    backdrop = PATTERNS[card["pattern"]].format(topic=card.get("topic", "simple"))
    lines = [STYLE, f"Subject: {card['subject']}", f"Hero colors: {card['hero_colors']}.",
             f"Staging: {CATEGORY_RULES[card['category']]}",
             f"Backdrop: {backdrop} in {card['backdrop_colors']}."]
    if card["surface_or_setting"]:
        lines.append(f"Surface or setting: {card['surface_or_setting']}.")
    return "\n".join(lines)


def blockout_brief(card):
    """The brief for restyling a blockout. Staging comes from the blockout itself."""
    backdrop = PATTERNS[card["pattern"]].format(topic=card.get("topic", "simple"))
    lines = [BLOCKOUT, f"Subject: {card['subject']}", f"Hero colors: {card['hero_colors']}.",
             f"Backdrop: {backdrop} in {card['backdrop_colors']}."]
    if card["surface_or_setting"]:
        lines.append(f"Surface or setting: {card['surface_or_setting']}.")
    return "\n".join(lines)


def render_model(source, out, look="plain"):
    """Render a model file with scripts/blockout.py. Returns Blender's error, or None."""
    out.unlink(missing_ok=True)
    done = subprocess.run(["blender", "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                           str(ROOT / "scripts" / "blockout.py"), "--", str(source), str(out), look],
                          capture_output=True, text=True, timeout=600)
    return None if out.exists() and not done.returncode else (done.stdout + done.stderr)[-1500:]


def model_card(run, brief, rater, look="plain", photos=()):
    """Write a Blender blockout of the card's object, render it and fix what the render shows.

    photos: real photos of the object, shown to the modeller for its construction only.
    Returns the render, or None when no model rendered, and the card is drawn from its brief alone."""
    folder = run / "models"
    source, render = folder / f"{brief['id']}.py", folder / f"{brief['id']}.png"
    if render.exists():
        return render
    folder.mkdir(parents=True, exist_ok=True)
    card = brief["card"]
    examples = "\n\n".join(f"```python\n{(ROOT / 'runs/trial/models2' / f'{name}.py').read_text('utf-8')}```"
                           for name in ("m16", "m36"))
    task = (f"{(ANALYSIS / 'agents' / 'modeller.md').read_text('utf-8')}\n\nTwo models from the trial, as examples of the "
            f"file:\n{examples}\n\nThe card: {card['name']}. {card['subject']}\nCategory {card['category']}: "
            f"{CATEGORY_RULES[card['category']]}\nHero colors: {card['hero_colors']}.\nBackdrop colors: "
            f"{card['backdrop_colors']}.\nSurface or setting: {card['surface_or_setting'] or 'none'}.")
    references = [ROOT / f"materials/card_examples/{i}.png" for i in brief["references"]]
    seen = (f"The first {len(references)} images are real cards of the same category, of other objects. Match their camera, "
            "framing and how much setting shows.")
    if photos:
        seen += (f" The last {len(photos)} are photos of the real object. Take from them only how it is built: its parts, "
                 "their counts and proportions, and how they connect and rest. Simplify it as the game does.")
    answer = ask_claude(f"{task}\n\n{seen} Write the model file.", references + list(photos), MODEL_SCHEMA, rater)
    log, good = [], None
    for round_number in range(MODEL_ROUNDS + 1):
        candidate = folder / f"{brief['id']}_{round_number}.py"
        candidate.write_text(answer["model"], "utf-8")
        error = render_model(candidate, folder / f"{brief['id']}_{round_number}.png", look)
        log.append({"round": round_number, "error": error, "problems": answer.get("problems", [])})
        if not error:
            good = round_number
        if round_number == MODEL_ROUNDS:
            break
        if error:
            answer = ask_claude(f"{task}\n\nYour model file:\n```python\n{answer['model']}```\nBlender failed:\n{error}\n"
                                "Fix it and return the whole file. ok is false.", None, LOOK_SCHEMA, rater)
            continue
        answer = ask_claude(f"{task}\n\nYour model file:\n```python\n{answer['model']}```\nThe image is its render, from the "
                            "card's camera. Check it against every rule above: could the object be built and work, does "
                            "every part attach or rest where it should, are the counts and proportions true, is it framed "
                            "on its main body and read at once as the named object? If all is right, ok is true and model "
                            "is empty. Otherwise list the problems and return the whole fixed file.",
                            folder / f"{brief['id']}_{round_number}.png", LOOK_SCHEMA, rater)
        if answer["ok"]:
            break
    save_json(folder / f"{brief['id']}.json", log)
    if good is None:
        return None
    source.write_text((folder / f"{brief['id']}_{good}.py").read_text("utf-8"), "utf-8")
    (folder / f"{brief['id']}_{good}.png").replace(render)
    return render


def make_briefs(plan, cards, seed):
    rng = random.Random(seed)
    used = Counter()
    briefs = []
    for variant, entry in enumerate(plan["variants"], 1):
        for index, card in enumerate(entry["cards"], 1):
            picks = pick_references(card, cards, used, rng)
            briefs.append({"id": f"v{variant}_{index:02d}", "variant": variant, "card": {**card, "topic": plan["title"]},
                           "references": [c["id"] for c in picks]})
    return briefs


def draw_card(run, brief, attempt, notes, use_references, edit=None):
    """Draw a card from its brief, or with edit set to a draft, change only what the notes name."""
    try_id = f"{brief['id']}_{attempt}"
    out, full = run / "tries" / f"{try_id}.png", run / "full" / f"{try_id}.png"
    if out.exists():
        return try_id
    references = [ROOT / f"materials/card_examples/{i}.png" for i in brief["references"]] if use_references else []
    blockout = run / "models" / f"{brief['id']}.png"
    if edit:
        prompt = EDIT.format(notes="\n".join(notes))
        references.append(edit)
    elif blockout.exists():
        prompt = blockout_brief(brief["card"])
        references.append(blockout)
    else:
        prompt = card_brief(brief["card"])
    (run / "prompts").mkdir(exist_ok=True)
    (run / "prompts" / f"{try_id}.txt").write_text(prompt, "utf-8")
    for tries_left in (1, 0):
        try:
            draw(prompt, references, full)
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
    same += [True] * (len(tries) - len(same))  # a short answer must not drop cards

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
            name = re.sub(r"\W+", "_", brief["card"]["name"].lower()).strip("_")
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
    parser.add_argument("--candidates", type=int, default=CANDIDATES, help="drawings per card to choose from")
    parser.add_argument("--review-rounds", type=int, default=REVIEW_ROUNDS, help="0 skips the specialists")
    parser.add_argument("--rater", default="claude-opus-5-5")
    parser.add_argument("--plan", help="reuse the plan.json of an earlier run")
    parser.add_argument("--no-references", action="store_true", help="draw from text alone, as a control")
    parser.add_argument("--no-blockouts", action="store_true", help="draw from the brief without a Blender model first")
    args = parser.parse_args()

    slug = re.sub(r"\W+", "-", args.theme.lower()).strip("-") + ("-noref" if args.no_references else "")
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

    if not args.no_blockouts:
        with ThreadPoolExecutor(args.workers) as pool:
            renders = list(pool.map(lambda brief: model_card(run, brief, args.rater), briefs))
        print(f"models: {sum(r is not None for r in renders)} of {len(briefs)} rendered", flush=True)

    history = defaultdict(list, load_json(run / "check.json") if (run / "check.json").exists() else {})

    def draw_and_check(jobs, attempt):
        """jobs: (brief, notes, draft). Finished tries stay in the history."""
        with ThreadPoolExecutor(args.workers) as pool:
            done = list(pool.map(lambda job: draw_card(run, job[0], attempt, job[1], not args.no_references, job[2]), jobs))
        seen = {t["try_id"] for tries in history.values() for t in tries}
        tries = [{"try_id": try_id, "brief_id": job[0]["id"], "card": job[0]["card"]}
                 for job, try_id in zip(jobs, done) if try_id and try_id not in seen]
        for entry in check_tries(run, tries, knowledge, args.workers) if tries else []:
            history[entry["brief_id"]].append(entry)
        save_json(run / "check.json", history)
        return tries

    for attempt in range(1, args.candidates + 1):
        tries = draw_and_check([(b, [], None) for b in briefs], attempt)
        print(f"candidates {attempt}: drew {len(tries)}, passed {sum(t.get('passed', False) for t in tries)}", flush=True)

    if args.review_rounds:
        from review import choose, review_variant

        for variant in range(1, len(plan["variants"]) + 1):
            chosen = [b for b in briefs if b["variant"] == variant]
            if not any(t.get("chosen") for b in chosen for t in history[b["id"]]):
                choose(run, chosen, history)
            save_json(run / "check.json", history)
            for round_number in range(1, args.review_rounds + 1):
                notes = review_variant(run, variant, round_number, chosen, history, args.rater)
                print(f"variant {variant} review {round_number}: {len(notes)} of {len(chosen)} cards need edits", flush=True)
                if not notes:
                    break
                drafts = {b["id"]: run / "tries" / f"{best_try(history[b['id']])['try_id']}.png" for b in chosen}
                attempt = args.candidates + round_number
                jobs = [(b, [notes[b["id"]]], drafts[b["id"]]) for b in chosen if b["id"] in notes]
                for entry in draw_and_check(jobs, attempt):
                    if entry.get("passed") or not entry.get("issues"):
                        for old in history[entry["brief_id"]]:
                            old.pop("chosen", None)
                        entry["chosen"] = True
                save_json(run / "check.json", history)

    deliver(run, plan, briefs, history)
    print("done:", run / "report.md")


if __name__ == "__main__":
    main()
