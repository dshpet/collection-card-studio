"""Specialist reviewers and the art director. Roles and rules are in analysis/agents/.

    review.py study                 specialists read real cards and describe the style
    review.py twins r2              blind pairs: a run's twins against the real cards
"""

import argparse
import json
import random
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, DERIVED, ROOT, load_json, save_json

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from make_set import contact_sheet
from rate import ask_claude, ask_codex

AGENTS = ANALYSIS / "agents"
SIZE = (430, 480)
STUDY_CATEGORIES = "1234"
LESSONS = ("t02", "t04", "t09", "t11")  # one twin per category, shown with its answer


def text():
    return {"type": "string"}


def strict(properties):
    return {"type": "object", "additionalProperties": False, "properties": properties, "required": list(properties)}


def array(item):
    return {"type": "array", "items": item}


STUDY_SCHEMA = strict({
    "always": array(text()), "varies": array(text()), "never": array(text()),
    "generator_wording": text()})


def pairs_schema(ids):
    return strict({
        "pairs": array(strict({"pair": {"type": "string", "enum": ids},
                               "odd": {"type": "string", "enum": ["A", "B", "neither"]},
                               "confidence": {"type": "integer", "minimum": 1, "maximum": 5},
                               "difference": text(), "fix": text()})),
        "pattern": text()})


DIRECTOR_SCHEMA = strict({
    "issues": array(strict({"issue": text(), "specialists": array(text()), "instruction": text()})),
    "style_text": text(),
    "cards": array(strict({"pair": text(), "keep": {"type": "boolean"}, "note": text()})),
    "summary": text()})


def card_image(card):
    return Image.open(ROOT / card["file"]).convert("RGB").resize(SIZE, Image.LANCZOS)


def mask_of(card):
    return Image.open(card["derived"] / "masks" / f"{card['id']}.png").convert("L").resize(SIZE)


def grey_groups(card):
    grey = ImageOps.grayscale(card_image(card))
    return grey.point(lambda v: min(v // 51, 4) * 63).convert("RGB")


def flat_colors(card):
    return card_image(card).quantize(8, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")


def silhouette(card):
    return Image.composite(Image.new("RGB", SIZE, "black"), Image.new("RGB", SIZE, "white"), mask_of(card))


def normals(card):
    return Image.open(card["derived"] / "normals" / f"{card['id']}.png").convert("RGB").resize(SIZE)


def shading(card):
    return Image.open(card["derived"] / "shading" / f"{card['id']}.png").convert("RGB").resize(SIZE)


def edge_map(card):
    grey = np.asarray(ImageOps.grayscale(card_image(card)), dtype=float)
    strength = np.hypot(*np.gradient(grey))
    return Image.fromarray(255 - np.clip(strength * 6, 0, 255).astype(np.uint8)).convert("RGB")


def hero_crop(card):
    box = mask_of(card).point(lambda v: 255 if v > 127 else 0).getbbox() or (0, 0, *SIZE)
    x, y = min((box[0] + box[2]) // 2, SIZE[0] - 108), min((box[1] + box[3]) // 2, SIZE[1] - 120)
    x, y = max(x, 107), max(y, 120)
    return card_image(card).crop((x - 107, y - 120, x + 108, y + 120)).resize(SIZE, Image.LANCZOS)


def thumbnail(card):
    canvas = Image.new("RGB", SIZE, (128, 128, 128))
    small = card_image(card).resize((129, 144), Image.LANCZOS)
    canvas.paste(small, ((SIZE[0] - 129) // 2, (SIZE[1] - 144) // 2))
    return canvas


def background_alone(card):
    return Image.composite(Image.new("RGB", SIZE, (128, 128, 128)), card_image(card), mask_of(card))


ROLES = {
    "shape_proportions": (silhouette, "Shape and silhouette", (
        "shape_proportions.straight_share", "shape_proportions.corner_rate", "shape_proportions.thin_share",
        "shape_proportions.solidity")),
    "viewpoint_depth": (normals, "Depth, viewpoint, and perspective", ("lighting_shading.planar_share",)),
    "lighting_shading": (shading, "Lighting and shading", (
        "lighting_shading.shading_range", "surface_finish.form_contrast", "lighting_shading.light_bias_strength")),
    "value_contrast": (grey_groups, "Tone and value", (
        "value_contrast.lightness_mean", "value_contrast.rms_contrast", "value_contrast.lightness_gap",
        "surface_finish.vignette")),
    "color_palette": (flat_colors, "Color and palette", (
        "color_palette.chroma_subject", "color_palette.chroma_background", "color_palette.warm_share",
        "color_palette.hue_families", "color_palette.shadow_chroma_kept")),
    "surface_finish": (hero_crop, "Texture, markmaking, and material finish", (
        "surface_finish.detail_subject", "surface_finish.micro_texture", "surface_finish.gloss_share",
        "surface_finish.highlight_share")),
    "edges_linework": (edge_map, "Edges, contours, and marks", (
        "edges_linework.edge_density_subject", "edges_linework.edge_density_background",
        "edges_linework.outline_darkness")),
    "composition_hierarchy": (thumbnail, "Composition, hierarchy, and space", (
        "composition_hierarchy.subject_area", "composition_hierarchy.box_width", "composition_hierarchy.box_height",
        "composition_hierarchy.margin_min")),
    "staging_detail": (background_alone, "Rhythm and staging", (
        "surface_finish.detail_background", "edges_linework.edge_density_background")),
}


def labelled(image, label):
    image = image.copy()
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(32)
    draw.rectangle((0, 0, draw.textlength(label, font) + 24, 44), fill="white")
    draw.text((12, 4), label, fill="black", font=font)
    return image


def pair_sheet(pair, role, out, labels=("A", "B")):
    a, b = pair["A"], pair["B"]
    lens = ROLES[role][0]
    sheet = Image.new("RGB", (SIZE[0] * 2 + 12, SIZE[1] * 2 + 12), "white")
    sheet.paste(labelled(card_image(a), labels[0]), (0, 0))
    sheet.paste(labelled(card_image(b), labels[1]), (SIZE[0] + 12, 0))
    sheet.paste(lens(a), (0, SIZE[1] + 12))
    sheet.paste(lens(b), (SIZE[0] + 12, SIZE[1] + 12))
    sheet.save(out)
    return out


def real_record(card):
    return {"id": card["id"], "file": f"materials/card_examples/{card['id']}.png", "derived": DERIVED,
            "name": card["name"], "category": card["form"]["staging"]["art_category"], "real": True,
            "measured": card["measured"]}


def real_cards():
    return [real_record(c) for c in load_json(ANALYSIS / "cards.json")
            if c["form"]["staging"]["art_category"] != "5"]


def anchor(folder, exclude, seed=5):
    """A sheet of real cards, three per category, that shows what 'the game' looks like."""
    rng = random.Random(seed)
    pool = [c for c in real_cards() if c["id"] not in exclude]
    picks = [card for category in STUDY_CATEGORIES
             for card in rng.sample([c for c in pool if c["category"] == category], 3)]
    path = folder / "anchor.png"
    contact_sheet([ROOT / c["file"] for c in picks], path, columns=4)
    return path


def ask(rater, prompt, images, schema):
    for attempt in (1, 2, 3):
        try:
            if rater == "codex":
                return ask_codex(prompt, images, schema, timeout=1200, effort="medium")
            return ask_claude(prompt, images, schema, model=rater)
        except Exception as error:
            print(f"attempt {attempt}: {type(error).__name__} {str(error)[:200]}", flush=True)
    return None


def role_prompt(role):
    rules = (AGENTS / "README.md").read_text("utf-8").split("## Rules for every specialist")[1].split("## Modes")[0]
    vocabulary = (ANALYSIS / "VOCABULARY.md").read_text("utf-8").split(f"## {ROLES[role][1]}\n")[1].split("\n## ")[0]
    brief = (AGENTS / f"{role}.md").read_text("utf-8")
    return f"You are a senior art specialist on a mobile game's art team.\n\n{brief}\n{rules}\nVocabulary:{vocabulary}"


def field(measured, path):
    section, name = path.split(".")
    return measured[section].get(name)


def evidence(role, pairs):
    """Measured numbers for the role's fields, per pair, with the real range for that category."""
    real = [c for c in load_json(ANALYSIS / "cards.json") if c["form"]["staging"]["art_category"] != "5"]
    lines = []
    for pair in pairs:
        category = next(c["category"] for c in (pair["A"], pair["B"]) if c.get("category"))
        pool = [c["measured"] for c in real if c["form"]["staging"]["art_category"] == category]
        for path in ROLES[role][2]:
            values = [field(pool_card, path) for pool_card in pool]
            low, high = np.percentile([v for v in values if v is not None], [10, 90])
            a, b = field(pair["A"]["measured"], path), field(pair["B"]["measured"], path)
            if a is not None and b is not None:
                lines.append(f"{pair['pair']} {path.split('.')[1]}: A {a}, B {b}, real cards {low:.3f} to {high:.3f}")
    return "\n".join(lines)


def study(rater):
    folder = ROOT / "runs" / "review" / "study"
    (folder / "sheets").mkdir(parents=True, exist_ok=True)
    rng = random.Random(11)
    pool = real_cards()
    picks = [card for category in STUDY_CATEGORIES
             for card in rng.sample([c for c in pool if c["category"] == category], 3)]
    pairs = [{"A": picks[i], "B": picks[i + 1]} for i in range(0, len(picks), 2)]

    def one(role):
        out = folder / f"{role}.json"
        if out.exists():
            return load_json(out)
        sheets = [pair_sheet(p, role, folder / "sheets" / f"{role}_{i}.png") for i, p in enumerate(pairs)]
        prompt = (f"{role_prompt(role)}\nEach image shows two real cards from the game, A and B, and below them your "
                  "lens on the same cards. Write what your vector always does across these cards, what varies, what "
                  "never happens, and generator_wording: at most 60 words that would make an image generator match "
                  "this vector. Be exact. Describe what these cards do, not what game art usually does.")
        result = ask(rater, prompt, sheets, STUDY_SCHEMA)
        if result:
            save_json(out, result)
        return result

    with ThreadPoolExecutor(5) as pool_:
        reports = dict(zip(ROLES, pool_.map(one, ROLES)))
    lines = ["# What the specialists see in the real cards", ""]
    for role, report in reports.items():
        if report:
            lines += [f"## {role}", "", report["generator_wording"], ""]
            lines += [f"- Always: {item}" for item in report["always"]] + [f"- Varies: {item}" for item in report["varies"]]
            lines += [f"- Never: {item}" for item in report["never"]] + [""]
    (folder / "notes.md").write_text("\n".join(lines), "utf-8")


def blind_pairs(entries, seed):
    """Shuffle sides, and keep the answer key apart from what specialists see."""
    rng = random.Random(seed)
    pairs = []
    for index, (generated, real) in enumerate(entries, 1):
        left, right = (generated, real) if rng.random() < 0.5 else (real, generated)
        odd = "neither" if generated["real"] else "A" if left is generated else "B"
        pairs.append({"pair": f"p{index:02d}", "A": left, "B": right, "odd": odd})
    return pairs


def lesson_sheets(lessons, role, folder):
    """Twins from an earlier round with their answers, so a reviewer learns which way differences run."""
    return [pair_sheet({"A": real, "B": generated}, role, folder / "sheets" / f"{role}_lesson{i}.png", ("REAL", "GENERATED"))
            for i, (generated, real) in enumerate(lessons)]


def specialists(name, pairs, lessons, exclude, rater, roles):
    folder = ROOT / "runs" / "review" / name
    (folder / "sheets").mkdir(parents=True, exist_ok=True)
    anchor_path = anchor(folder, exclude)

    def one(role):
        out = folder / f"{role}.json"
        if out.exists():
            return role, load_json(out)
        taught = lesson_sheets(lessons, role, folder)
        sheets = [pair_sheet(p, role, folder / "sheets" / f"{role}_{p['pair']}.png") for p in pairs]
        first = len(taught) + 2
        listing = ", ".join(f"{p['pair']} is image {i + first}" for i, p in enumerate(pairs))
        prompt = (f"{role_prompt(role)}\nImage 1 shows real cards from the game. Images 2 to {first - 1} are lessons: "
                  "the label on each card says which is REAL and which was GENERATED by an image model, with your lens "
                  "below. Study which way the differences run on your vector, and trust the lessons over any idea of "
                  f"what game art should look like. The remaining images are test pairs, A and B ({listing}). In each "
                  "pair one card may be generated, or both may be real. On your vector only: which card is the "
                  "generated one? Answer A, B or neither, with confidence 1-5. In difference, say what you see on each "
                  "card and where. In fix, give the generator wording that would correct the generated card, or leave "
                  "it empty. In pattern, name what still gives generated cards away.\n\nMeasured evidence, one line "
                  f"per field. Numbers support your eye, they do not replace it:\n{evidence(role, pairs)}")
        result = ask(rater, prompt, [anchor_path, *taught, *sheets], pairs_schema([p["pair"] for p in pairs]))
        if result:
            save_json(out, result)
        return role, result

    with ThreadPoolExecutor(5) as pool:
        return dict(pool.map(one, roles))


def score(pairs, reports):
    """Is each specialist better than chance? Keyed by role, then over all, plus false alarms on controls."""
    key = {p["pair"]: p["odd"] for p in pairs}
    rows = {}
    for role, report in reports.items():
        if not report:
            continue
        answers = {a["pair"]: a for a in report["pairs"]}
        generated = [p for p in key if key[p] != "neither"]
        controls = [p for p in key if key[p] == "neither"]
        rows[role] = {
            "caught": sum(answers[p]["odd"] == key[p] for p in generated if p in answers),
            "wrong": sum(answers[p]["odd"] not in ("neither", key[p]) for p in generated if p in answers),
            "abstained": sum(answers[p]["odd"] == "neither" for p in generated if p in answers),
            "false_alarms": sum(answers[p]["odd"] != "neither" for p in controls if p in answers),
            "pairs": len(generated), "controls": len(controls)}
    return rows


def direct(name, pairs, reports, style_text, rater):
    folder = ROOT / "runs" / "review" / name
    out = folder / "art_director.json"
    if out.exists():
        return load_json(out)
    unblinded = "\n".join(f"{p['pair']}: {p['A'].get('name') or p['B'].get('name')}: "
                          f"{'control, both real' if p['odd'] == 'neither' else p['odd'] + ' is generated'}"
                          for p in pairs)
    sheets = [folder / "sheets" / f"staging_detail_{p['pair']}.png" for p in pairs]
    prompt = (f"{(AGENTS / 'art_director.md').read_text('utf-8')}\n\nEach image is one pair of cards, A and B on top.\n"
              f"Answer key:\n{unblinded}\n\nThe generator's current style text:\n{style_text}\n\n"
              f"Specialist reports:\n{json.dumps(reports, ensure_ascii=False)}\n\n"
              "Return issues, ranked. Return style_text: a full replacement for the current text, at most 110 words. "
              "For each generated card return keep, or a note for its redraw. Summary: is this close to the real cards?")
    result = ask(rater, prompt, sheets, DIRECTOR_SCHEMA)
    if result:
        save_json(out, result)
    return result


def report(name, pairs, reports, direction):
    folder = ROOT / "runs" / "review" / name
    rows = score(pairs, reports)
    save_json(folder / "pairs.json", [{"pair": p["pair"], "odd": p["odd"], "A": p["A"]["id"], "B": p["B"]["id"]} for p in pairs])
    lines = [f"# Review: {name}", "", "| Specialist | Caught | Wrong | Abstained | False alarms |", "|---|---:|---:|---:|---:|"]
    for role, row in rows.items():
        lines.append(f"| {role} | {row['caught']}/{row['pairs']} | {row['wrong']} | {row['abstained']} | "
                     f"{row['false_alarms']}/{row['controls']} |")
        print(role, row, flush=True)
    if direction:
        lines += ["", "## Art director", "", direction["summary"], ""]
        lines += [f"{i}. **{issue['issue']}** {issue['instruction']}" for i, issue in enumerate(direction["issues"], 1)]
        lines += ["", "Style text:", "", direction["style_text"], ""]
        lines += [f"- {card['pair']}: {'keep' if card['keep'] else card['note']}" for card in direction["cards"]]
    (folder / "report.md").write_text("\n".join(lines) + "\n", "utf-8")


def twin_entries(label):
    """(generated, real) for every twin of a round, plus the real cards that must stay out of the anchor sheet."""
    run = ROOT / "runs" / "twins" / label
    real = {c["id"]: c for c in real_cards()}
    briefs = load_json(ROOT / "runs" / "twins" / "briefs.json")
    entries, chosen, measured = [], load_json(run / "check.json"), load_json(run / "measured.json")
    for brief in briefs:
        try_id = chosen[brief["id"]][-1]["try_id"]
        generated = {"id": try_id, "file": str((run / "tries" / f"{try_id}.png").relative_to(ROOT)), "twin": brief["id"],
                     "derived": run / "derived", "name": brief["card"]["name"], "real": False, "measured": measured[try_id]}
        entries.append((generated, real[brief["real"]]))
    return entries, {b["real"] for b in briefs}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("study", "twins"))
    parser.add_argument("run", nargs="?")
    parser.add_argument("--rater", default="claude-sonnet-5-5")
    parser.add_argument("--director", default="claude-opus-5-5")
    parser.add_argument("--roles", nargs="+", default=list(ROLES))
    parser.add_argument("--lessons", nargs="+", default=["baseline"], help="rounds whose labelled twins calibrate the reviewers")
    parser.add_argument("--no-director", action="store_true")
    parser.add_argument("--name")
    args = parser.parse_args()
    if args.mode == "study":
        study(args.rater)
        return
    from style import STYLE

    name = args.name or f"twins_{args.run}"
    entries, exclude = twin_entries(args.run)
    lessons = [entry for label in args.lessons for entry in twin_entries(label)[0] if entry[0]["twin"] in LESSONS]
    pairs = blind_pairs([entry for entry in entries if entry[0]["twin"] not in LESSONS], name)
    reports = specialists(name, pairs, lessons, exclude, args.rater, args.roles)
    direction = None if args.no_director else direct(name, pairs, reports, STYLE, args.director)
    report(name, pairs, reports, direction)


if __name__ == "__main__":
    main()
