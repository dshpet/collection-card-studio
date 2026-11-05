"""Turn a theme and producer wishes into ten-card set variants, with no manual steps.

Stages: plan, references, model, draw candidates, check, choose, review, edit, deliver. README.md describes each.
Results land in runs/<slug>/, or the folder named by --run. Finished work is kept, so a rerun continues where it stopped.
"""

import argparse
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # every local model is already cached

from common import ANALYSIS, ROOT, best_try, load_json, save_json

import numpy as np
import torch
from PIL import Image

from cast import LOOKS, identity_references
from draw import draw
from estimate import write_masks
from experience import collect as collect_experience, lessons
from form import CARD_FORM, card_schema
from measure import measure_card
from rate import ask_claude, ask_codex, card_prompt
from style import BLOCKOUT, CAST_STYLE, CATEGORY_RULES, EDIT, PATTERNS, STYLE

SIZE = (430, 480)
CANDIDATES = 3
MODEL_ROUNDS = 2
REVIEW_ROUNDS = 1  # a second round kept 0 of 11 edits, the first 6 of 11 (analysis/experience.json, 2026-11-05)
ALLOWED_MISSES = 2
RATED = ["identity", "staging"]
EXAMPLE_MODELS = ANALYSIS / "agents" / "models"  # two models from the construction trial
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
    "hero_colors": text(), "backdrop_colors": text(), "surface_or_setting": text(), "build_model": {"type": "boolean"},
})
# From the user's ratings: a Blender model fixed the chair, clock, pier and saddle, and took the charm out of the cat,
# boot and witch hat (analysis/STYLE_GAPS.md).
MODEL_RULE = ("build_model: true for a built object of several rigid parts that must connect or stand, such as furniture, "
              "clocks, vehicles, machines, buildings, piers, frames, or anything with legs, hinges, wheels, straps or "
              "rigging. false for a simple or organic form: an animal, plant, food, garment, hat, boot, a single solid "
              "or a soft object. A 3D model fixes how parts connect but strips the charm from simple forms.")
DECIDE_SCHEMA = strict({"cards": {"type": "array", "items": strict({"id": text(), "build_model": {"type": "boolean"}})}})


def plan_schema(cast=0):
    """The plan's form. With cast cards, a card may be category 5 and names the cast members it shows."""
    card = CARD_SCHEMA
    if cast:
        card = strict({**CARD_SCHEMA["properties"],
                       "object_class": {"type": "string", "enum": OBJECT_CLASSES + ["character"]},
                       "category": {"type": "string", "enum": ["1", "2", "3", "4", "5"]},
                       "cast": {"type": "array", "items": {"type": "string", "enum": list(LOOKS)}}})
    return strict({"title": text(), "story": text(),
                   "variants": {"type": "array", "items": strict({"cards": {"type": "array", "items": card}})}})


MODEL_SCHEMA = strict({"model": text()})
SENSITIVE_SCHEMA = strict({"flagged": {"type": "array", "items": strict({"name": text(), "why": text()})}})
LOOK_SCHEMA = strict({"ok": {"type": "boolean"}, "problems": {"type": "array", "items": text()}, "model": text()})


def decide_models(briefs):
    """For plans made before build_model existed: one call decides every card."""
    listing = "\n".join(f"c{i:02d}: {b['card']['name']}, {b['card']['subject']}" for i, b in enumerate(briefs))
    answer = ask_claude(f"For each card of a mobile game, decide whether to build a 3D model before drawing it.\n"
                        f"{MODEL_RULE}\n\nCards:\n{listing}\nAnswer for every card, by its key.", None, DECIDE_SCHEMA)
    decided = {c["id"]: c["build_model"] for c in answer["cards"]}
    missing = [f"c{i:02d}" for i in range(len(briefs)) if f"c{i:02d}" not in decided]
    if missing:
        raise RuntimeError(f"no model decision for {missing}. Rerun to continue")
    for i, brief in enumerate(briefs):
        brief["card"]["build_model"] = decided[f"c{i:02d}"]


def cast_rule(cast):
    if not cast:
        return "No characters or people"
    looks = "; ".join(f"the {name}, {look}" for name, look in LOOKS.items())
    count = "one card in each version shows" if cast == 1 else f"{cast} cards in each version show"
    return (f"Exactly {count} the game's own cast, as the real sets' "
            f"late character cards do: {looks}. A character card is category 5 with pattern full_scene and "
            "object_class character. cast names the one or two who appear, subject is a small, funny moment from this "
            "topic in one sentence, and they may wear the topic's outfit. Every other card shows no character or person "
            "and has an empty cast")


def plan_prompt(theme, wishes, variants, knowledge, cast=0):
    examples = "\n".join(
        f"{example['title']}: " + "; ".join(
            f"{card['name']} [{card['object_class']}, cat {card['category']}, {card['pattern']}]"
            for card in example["cards"]) for example in knowledge["example_sets"])
    return f"""You are the lead producer of card collections for a cozy mobile game.
Theme: {theme}
Producer wishes: {wishes or "none"}

Design {variants} clearly different versions of one ten-card set for this theme.

Rules learned from the game's real sets:
- title: the topic itself, in 1-2 plain words, like "Beach" or "Road Trip", without the collection's name: "Horror", not "Horror Movie". A story behind the set is optional. Give it in one line or leave it empty.
- Card names: 1-2 plain words.
- Pick the first things anyone would name for the topic: instantly recognizable objects with a simple, distinctive silhouette.
- Every object must belong to this specific topic, not to the wider collection. A film genre set shows that genre's world, not generic cinema items such as film reels or popcorn.
- {cast_rule(cast)}. No brands, logos or real franchises. An animal may appear as an object, at most once in a set. No weapons of any kind, toy or sci-fi ones included. No blood or gore. Keep dark topics playful.
- Cards carry no text, so skip objects that need readable words to make sense.
- Real sets use {knowledge['set_ranges']['object_classes'][0]}-{knowledge['set_ranges']['object_classes'][1]} object classes and {knowledge['set_ranges']['scale_classes'][0]}-{knowledge['set_ranges']['scale_classes'][1]} real-world sizes, from handheld things to vehicles and buildings.
- Every version uses all four art categories: 1 floating object, 2 object on a plain ledge, 3 object on a real surface, 4 object in an environment. Use 2-4 of category 1, 1-2 of category 2, 2-4 of category 3 and 1-5 of category 4{' besides the character cards' if cast else ''}.
- For category 4 use pattern full_scene. Otherwise pick a graphic pattern.
- subject: one plain sentence on what to draw, with the two or three features that make it recognizable. Name the object and its parts only, with no mood, style or props.
- hero_colors are the object's natural colors plus one small accent in another hue, which nearly all real cards have. Give every card a backdrop whose color contrasts with the hero, and use at least six different backdrop hues across a set.
- backdrop_colors are bright and clean, as in the real cards: sky blue, cyan, yellow, orange, purple, pink, grass green. Never dusty, muted, dull or dark. Skies stay clear and bright, even on dark topics.
- surface_or_setting: the surface for categories 2-3 and the place for category 4, empty for category 1. Real sets reuse one or two ground materials across their cards, so reuse them too.
- Versions may share at most 5 objects.
- {MODEL_RULE}

Lessons from the producer's ratings:
{chr(10).join(lessons('Planning'))}

Real sets from the game, as examples:
{examples}"""


def plan_problems(plan, cast=0):
    problems = []
    if len(plan["title"].split()) > 3:
        problems.append("the title must be 1-3 words")
    names = []
    for index, variant in enumerate(plan["variants"], 1):
        cards = variant["cards"]
        names.append({card["name"].lower() for card in cards})
        if len(cards) != 10:
            problems.append(f"version {index} must have exactly ten cards")
        if {card["category"] for card in cards} - {"5"} != {"1", "2", "3", "4"}:
            problems.append(f"version {index} must use all four categories")
        characters = [card for card in cards if card["category"] == "5"]
        if len(characters) != cast or any(not 1 <= len(set(card["cast"])) == len(card["cast"]) <= 2 for card in characters):
            problems.append(f"version {index} must have exactly {cast} character card{'' if cast == 1 else 's'}, "
                            "each naming one or two of the cast")
        if any(card.get("cast") or card["object_class"] == "character" for card in cards if card["category"] != "5"):
            problems.append(f"version {index}: only category 5 cards show the cast or have object_class character")
        if len(names[-1]) != len(cards):
            problems.append(f"version {index} repeats a card")
        problems += [f"card name too long: {c['name']}" for c in cards if len(c["name"].split()) > 2]
    for first in range(len(names)):
        for second in range(first + 1, len(names)):
            if len(names[first] & names[second]) > 5:
                problems.append(f"versions {first + 1} and {second + 1} share too many objects")
    return problems


def make_plan(theme, wishes, variants, knowledge, cast=0):
    prompt = plan_prompt(theme, wishes, variants, knowledge, cast)
    schema = plan_schema(cast)
    plan = ask_claude(prompt, None, schema)
    problems = plan_problems(plan, cast)
    if problems:
        plan = ask_claude(f"{prompt}\n\nYour last answer had these problems, fix them: {problems}\n"
                          f"Last answer: {json.dumps(plan)}", None, schema)
    plan["problems"] = plan_problems(plan, cast)
    flagged = sensitive_cards(plan)
    if flagged:
        plan = ask_claude(f"{prompt}\n\nThese cards may upset players, replace them with other objects and keep every "
                          f"rule: {flagged}\nLast answer: {json.dumps(plan)}", None, schema)
        plan["problems"] = plan_problems(plan, cast)
        plan["sensitive"] = sensitive_cards(plan)
    plan["cast"] = cast
    return plan


def sensitive_cards(plan):
    """A separate check that no card could offend or upset a wide, casual audience."""
    names = sorted({card["name"] for variant in plan["variants"] for card in variant["cards"]})
    answer = ask_claude(f"""A cozy mobile game for a wide, casual audience of every age, culture and faith shows these collection cards for the set "{plan['title']}": {names}.
Flag every card that could offend, upset or sadden some players: death and burial (coffins, graves, tombstones, skulls), religious symbols, illness or injury, drugs, weapons, politics, national or cultural stereotypes, or anything a parent would not want a child to see. Playful spooky or fantasy objects are fine. Give the card name and a short reason. Flag nothing if all are fine.""", None, SENSITIVE_SCHEMA)
    return answer["flagged"]


def cast_brief(card):
    """The brief for a character card: the cast cutouts come first among the attached images."""
    who = " and ".join(f"the {name}" for name in card["cast"])
    same = "The character" if len(card["cast"]) == 1 else "Each character"
    return "\n".join([CAST_STYLE.format(who=who, same=same), f"Subject: {card['subject']}",
                      f"Staging: {CATEGORY_RULES['5']}", f"Setting: {card['surface_or_setting']}, under {card['backdrop_colors']}."])


def card_brief(card):
    if card["category"] == "5":
        return cast_brief(card)
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
    """Render a model file with scripts/blockout.py. Returns Blender's error or None, and the parts that touch nothing."""
    out.unlink(missing_ok=True)
    done = subprocess.run(["blender", "-b", "--factory-startup", "--python-exit-code", "1", "--python",
                           str(ROOT / "scripts" / "blockout.py"), "--", str(source), str(out), look],
                          capture_output=True, text=True, timeout=600)
    loose = next((json.loads(line[7:]) for line in done.stdout.splitlines() if line.startswith("LOOSE: ")), [])
    return (None if out.exists() and not done.returncode else (done.stdout + done.stderr)[-1500:]), loose


def loose_note(loose):
    """The geometry check, in words for the modeller. Parts are named by their center and size."""
    if not loose:
        return ""
    parts = "; ".join(f"a {p['part'].lower()} centered at {tuple(p['at'])}, size {tuple(p['size'])}" for p in loose)
    return (f" A geometry check of the file found parts that touch nothing holding them: {parts}. Attach each to what "
            "should hold it, unless it floats by design, such as a planet's ring or mist inside glass.")


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
    examples = "\n\n".join(f"```python\n{path.read_text('utf-8')}```" for path in sorted(EXAMPLE_MODELS.glob("*.py")))
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
        error, loose = render_model(candidate, folder / f"{brief['id']}_{round_number}.png", look)
        log.append({"round": round_number, "error": error, "loose": loose, "problems": answer.get("problems", [])})
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
                            f"on its main body and read at once as the named object?{loose_note(loose)} If all is right, "
                            "ok is true and model is empty. Otherwise list the problems and return the whole fixed file.",
                            folder / f"{brief['id']}_{round_number}.png", LOOK_SCHEMA, rater)
        if answer["ok"]:
            break
    save_json(folder / f"{brief['id']}.json", log)
    if good is None:
        return None
    source.write_text((folder / f"{brief['id']}_{good}.py").read_text("utf-8"), "utf-8")
    (folder / f"{brief['id']}_{good}.png").replace(render)
    return render


def make_briefs(plan, cards):
    """Each card with its three real reference cards, found by search.py from the card's subject."""
    from search import Search, pick_references

    planned = [(variant, index, card) for variant, entry in enumerate(plan["variants"], 1)
               for index, card in enumerate(entry["cards"], 1)]
    likeness = Search().confidence([card["subject"] for _, _, card in planned])
    torch.cuda.empty_cache()  # SigLIP is done; the GPU is needed for masks and shading later
    briefs, firsts = [], defaultdict(set)
    for (variant, index, card), chance in zip(planned, likeness):
        brief = {"id": f"v{variant}_{index:02d}", "variant": variant, "card": {**card, "topic": plan["title"]}}
        if card["category"] == "5":
            # Codex takes five images: cutouts of the cast first, then two real character cards
            each = 3 if len(card["cast"]) == 1 else 2
            found = {name: identity_references(name, each) for name in card["cast"]}
            if not all(found.values()) or not all(p.exists() for paths in found.values() for p in paths):
                raise RuntimeError("cast cutouts are missing: run scripts/cast.py find, then label")
            cutouts = [str(p.relative_to(ROOT)) for paths in found.values() for p in paths][:3]
            brief["cast_references"] = cutouts
            # the cards the cutouts come from would repeat them, and the review would pair the card with its source
            sources = {Path(path).stem.rsplit("_", 1)[0] for path in cutouts}
            pool = [c for c in cards if c["id"] not in sources]
            brief["references"] = [c["id"] for c in pick_references(card, pool, chance, 5 - len(cutouts), firsts[variant])]
        else:
            brief["references"] = [c["id"] for c in pick_references(card, cards, chance, taken=firsts[variant])]
        firsts[variant].add(brief["references"][0])
        briefs.append(brief)
    return briefs


def draw_card(run, brief, attempt, notes, use_references, edit=None):
    """Draw a card from its brief, or with edit set to a draft, change only what the notes name."""
    try_id = f"{brief['id']}_{attempt}"
    out, full = run / "tries" / f"{try_id}.png", run / "full" / f"{try_id}.png"
    if out.exists():
        return try_id
    references = [ROOT / f"materials/card_examples/{i}.png" for i in brief["references"]] if use_references else []
    if brief.get("cast_references") and not edit:
        references = [ROOT / path for path in brief["cast_references"]] + references
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


def run_name(run):
    """A run's folder under runs/, nested ones included."""
    return str(run.relative_to(ROOT / "runs")) if run.is_relative_to(ROOT / "runs") else run.name


def number(try_id):
    """The attempt number at the end of a try id: candidates first, then one number per review round."""
    return int(try_id.rsplit("_", 1)[1])


def record_edits(run, round_number, drawn, before, notes, kept):
    """Every edit drawn and whether it beat its draft, for experience.py. An edit that failed its checks was not kept."""
    path = run / "edits.json"
    rows = [r for r in (load_json(path) if path.exists() else []) if r["edit"] not in {e["try_id"] for e in drawn}]
    rows += [{"run": run_name(run), "card": e["brief_id"], "name": e["card"]["name"],
              "round": round_number, "note": notes[e["brief_id"]], "draft": before[e["brief_id"]], "edit": e["try_id"],
              "kept": e["try_id"] in kept} for e in drawn]
    save_json(path, rows)


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
            tries = history.get(brief["id"])
            if not tries:
                lines.append(f"| {brief['card']['name']} | {brief['card']['category']} | 0 | | missing | every draw failed, rerun |")
                counts["missing"] += 1
                continue
            best = best_try(tries)
            name = re.sub(r"\W+", "_", brief["card"]["name"].lower()).strip("_")
            # The game's characters stay out of git: "-cast" marks them, and no card name can hold a hyphen here
            path = folder / f"{brief['id'][-2:]}{'-cast' if brief['card']['category'] == '5' else ''}_{name}.png"
            Image.open(run / "tries" / f"{best['try_id']}.png").save(path)
            paths.append(path)
            counts.update(best["misses"] + best["issues"])
            open_issues = ", ".join(best["issues"] + [m.split(".")[1] for m in best["misses"]]) or "none"
            lines.append(f"| {brief['card']['name']} | {brief['card']['category']} | {len(tries)} | {best['style']} | "
                         f"{'unsure pick' if best.get('unsure') else 'pass' if best['passed'] else 'review'} | {open_issues} |")
        if paths:
            cast = any(b["card"]["category"] == "5" for b in briefs if b["variant"] == variant)
            contact_sheet(paths, run / f"variant_{variant}{'-cast' if cast else ''}.png")
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
    parser.add_argument("--run", help="folder name under runs/, by default the theme")
    parser.add_argument("--cast", type=int, default=0, help="character cards per variant, drawn with the game's cast")
    args = parser.parse_args()

    slug = re.sub(r"\W+", "-", args.theme.lower()).strip("-") + ("-noref" if args.no_references else "")
    run = ROOT / "runs" / (args.run or slug)
    run.mkdir(parents=True, exist_ok=True)
    knowledge = load_json(ANALYSIS / "knowledge.json")
    cards = load_json(ANALYSIS / "cards.json")

    plan_path = run / "plan.json"
    if args.plan:
        save_json(plan_path, load_json(ROOT / args.plan))
    if not plan_path.exists():
        save_json(plan_path, make_plan(args.theme, args.wishes, args.variants, knowledge, args.cast))
    plan = load_json(plan_path)
    print("plan:", plan["title"], "|", plan.get("problems") or "no problems", flush=True)

    briefs_path = run / "briefs.json"
    if not briefs_path.exists():
        save_json(briefs_path, make_briefs(plan, cards))
    briefs = load_json(briefs_path)
    history = defaultdict(list, load_json(run / "check.json") if (run / "check.json").exists() else {})
    rounds_path = run / "rounds.json"
    if args.review_rounds and not rounds_path.exists() and any(
            number(t["try_id"]) > args.candidates for tries in history.values() for t in tries):
        raise SystemExit(f"{run.name} was reviewed by an older make_set.py, which kept no record of its rounds. Continue "
                         "it with --review-rounds 0, or start fresh with --run <new name>.")

    if not args.no_blockouts:
        if any("build_model" not in brief["card"] for brief in briefs):
            decide_models(briefs)
            save_json(briefs_path, briefs)
        built = [brief for brief in briefs if brief["card"]["build_model"] and brief["card"]["category"] != "5"]
        with ThreadPoolExecutor(args.workers) as pool:
            renders = list(pool.map(lambda brief: model_card(run, brief, args.rater), built))
        print(f"models: {sum(r is not None for r in renders)} of {len(built)} rendered, "
              f"{len(briefs) - len(built)} cards drawn from the brief alone", flush=True)

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
        from review import better_edits, choose, review_variant

        # Each round's notes, drafts, edit number and outcome, so a rerun neither reviews a round twice nor mistakes
        # one drawing for another
        rounds = load_json(rounds_path) if rounds_path.exists() else {}
        for variant in range(1, len(plan["variants"]) + 1):
            chosen = [b for b in briefs if b["variant"] == variant]
            waiting = [b["id"] for b in chosen if not history[b["id"]]]
            if waiting:  # picks and reviews are made for the whole variant at once
                print(f"variant {variant} waits for a drawing of {', '.join(waiting)}: rerun to continue", flush=True)
                continue
            if not any(t.get("chosen") for b in chosen for t in history[b["id"]]):
                choose(run, chosen, history)
            save_json(run / "check.json", history)
            for round_number in range(1, args.review_rounds + 1):
                state = rounds.setdefault(f"{variant}_{round_number}", {})
                if "kept" in state:
                    if not state["notes"]:
                        break
                    continue
                if "notes" not in state:
                    notes = review_variant(run, variant, round_number, chosen, history, args.rater)
                    print(f"variant {variant} review {round_number}: {len(notes)} of {len(chosen)} cards need edits",
                          flush=True)
                    state.update(notes=notes, before={b["id"]: best_try(history[b["id"]])["try_id"] for b in chosen},
                                 attempt=1 + max(number(t["try_id"]) for b in chosen for t in history[b["id"]]))
                    save_json(rounds_path, rounds)
                notes, before, attempt = state["notes"], state["before"], state["attempt"]
                kept = set()
                if notes:
                    jobs = [(b, [notes[b["id"]]], run / "tries" / f"{before[b['id']]}.png") for b in chosen if b["id"] in notes]
                    draw_and_check(jobs, attempt)
                    drawn = [t for b in chosen if b["id"] in notes for t in history[b["id"]]
                             if t["try_id"] == f"{b['id']}_{attempt}"]
                    edited = [e for e in drawn if e.get("passed") or not e.get("issues")]
                    # An edit is obeyed strongly and can make a card worse, so it stays only if it beats its draft
                    kept = better_edits(run, f"edit_{variant}_{round_number}",
                                        [(e["brief_id"], before[e["brief_id"]], e["try_id"]) for e in edited],
                                        {b["id"]: b["references"] for b in chosen}, args.rater)
                    for entry in edited:
                        if entry["try_id"] in kept:
                            for old in history[entry["brief_id"]]:
                                old.pop("chosen", None)
                            entry["chosen"] = True
                    record_edits(run, round_number, drawn, before, notes, kept)
                    print(f"variant {variant} review {round_number}: kept {len(kept)} of {len(drawn)} edits", flush=True)
                    save_json(run / "check.json", history)
                state["kept"] = sorted(kept)
                save_json(rounds_path, rounds)
                if not notes:
                    break

    deliver(run, plan, briefs, history)
    collect_experience()
    print("done:", run / "report.md")


if __name__ == "__main__":
    main()
