"""Overnight arms, 2026-11-07/08: one change per arm against a shared control, before the final sets.

The twins' style lines run through param.py (runs/twins40/n0, ns, nc). This script covers what param.py cannot:

    night.py palette ARM       the forty twins, colored by the planner from a colorless subject: old rule, new
                               (more hues, no black) or rich (new, plus a rich body hue);
                               new+smooth draws the new rule's colors with the smooth line
    night.py blockout ARM      24 pre-final blockout cards redrawn: smooth (the smooth-surface line) or fill (re-rendered
                               at the real cards' frame size), or both, fill+smooth or fill+smooth2 (the smooth line
                               without "sheen"); the control is each card's first
                               pre-final candidate
    night.py perspective ARM   the nine cards graded broken: cam (the one-camera line) or model (a blockout for the four
                               drawn without one); the control is their pre-final candidates
    night.py read              measure every arm against the real cards; CSD to the twin's own real card
    night.py eyes ARM          blockout arm against its control by eye, both orders: which has more surface texture
    night.py plans             the final's plan files: the best pre-final variant of each genre, and six cast cards
    night.py recolor           the final plans' colors under the adopted rich-color rule

Results go to runs/night/.
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import random
import re
import shutil
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, JUDGE, PLANNER, ROOT, load_json, save_json, strict, text

import numpy as np

OUT = ROOT / "runs" / "night"
TWINS = ROOT / "runs" / "twins40"
PREFINAL = ROOT / "runs" / "prefinal"
SMOOTH = ("Each material looks like itself, with a little quiet detail and natural local color.",
          "Each material looks like itself by its color and sheen, in natural local color. Large surfaces stay smooth, "
          "with no grain, weave, nap or pores: detail lives in the parts.")
# Round 2: the smooth line without "and sheen", which made cards glossier in round 1
SMOOTH2 = (SMOOTH[0], "Each material looks like itself by its color, in natural local color. Large surfaces stay smooth, "
                      "with no grain, weave, nap or pores: detail lives in the parts.")
CAMERA = ("The object and the surface under it are seen from that one camera, so every rim, brim, opening and tabletop "
          "opens by the same amount.")
# The real cards' median frame size against the blockout's box, by art category (analysis/measurements.json)
FILL = {"1": 1.04, "2": 1.07, "3": 1.10, "4": 1.12}
OLD_HERO = ("- hero_colors are the object's natural colors. Nearly all real cards also show one small accent in another "
            "hue, on a part the object really has, such as a hat's band.")
NEW_HERO = ("- hero_colors name three or four colors for the object's parts, as the real cards do: its natural colors, "
            "clean and rich, plus one small accent in another hue on a part the object really has, such as a hat's "
            "band. Black, charcoal and dark brown are rare on real cards: a dark part takes a deep rich hue instead, "
            "such as navy, plum, forest green or red-brown.")
RICH_HERO = NEW_HERO + (" The main body takes a rich, saturated hue, as on the real cards; white, grey and silver go on "
                        "small parts, or on an object that is white by nature, such as a sail.")
BROKEN = [("detective", "v3_10"), ("western", "v2_03"), ("sci-fi", "v3_07"), ("detective", "v2_03"),
          ("horror", "v3_05"), ("period-drama", "v1_09"), ("period-drama", "v2_03"), ("horror", "v1_09"),
          ("western", "v1_01")]
FIELDS = ["color_palette.hue_families", "color_palette.chroma_subject", "color_palette.shadow_chroma_kept",
          "color_palette.chroma_background", "composition_hierarchy.margin_min", "composition_hierarchy.subject_area",
          "composition_hierarchy.box_width", "composition_hierarchy.box_height", "value_contrast.lightness_mean",
          "value_contrast.lightness_p5", "value_contrast.rms_contrast", "surface_finish.micro_texture",
          "surface_finish.detail_subject", "surface_finish.gloss_share", "surface_finish.form_contrast"]


def color_rules(hero):
    """The planner's color bullets, with the hero_colors bullet set to hero."""
    from make_set import plan_prompt

    prompt = plan_prompt("Test", "", 1, load_json(ANALYSIS / "knowledge.json"))
    keep = ("- hero_colors", "- backdrop_colors", "- By category", "- Use about six backdrop colors")
    return "\n".join(hero if line.startswith("- hero_colors") else line
                      for line in prompt.splitlines() if line.startswith(keep))


def recolor(cards, hero):
    """Hero and backdrop colors for each card, written by the planner under the color rules. cards: id to card."""
    from rate import ask_claude

    listing = "\n".join(f"{key}: {card['name']}: {card['subject']} [category {card['category']}, {card['pattern']}"
                        f"{', on ' + card['surface_or_setting'] if card['surface_or_setting'] else ''}]"
                        for key, card in cards.items())
    schema = strict({"cards": {"type": "array", "items": strict({"id": {"type": "string", "enum": list(cards)},
                                                                 "hero_colors": text(), "backdrop_colors": text()})}})
    answer = ask_claude(f"""You are the lead producer of card collections for a cozy mobile game. Write hero_colors and backdrop_colors for each card below, by these rules learned from the game's real cards:
{color_rules(hero)}

Cards, one per line as id: name: subject [art category, backdrop pattern]:
{listing}""", None, schema, PLANNER)
    return {item["id"]: {"hero_colors": item["hero_colors"], "backdrop_colors": item["backdrop_colors"]}
            for item in answer["cards"]}


def palette(arm, workers):
    from make_set import draw_card
    from rate import ask_claude

    twins = load_json(TWINS / "briefs.json")
    folder = OUT / "palette"
    subjects_path = folder / "subjects.json"
    if not subjects_path.exists():
        schema = strict({"items": {"type": "array", "items": strict({"id": text(), "subject": text()})}})
        listing = "\n".join(f"{t['id']}: {t['card']['subject']}" for t in twins)
        answer = ask_claude("Rewrite each sentence without any color word (no hues, no black, white, grey, gold or "
                            "silver, no light or dark), keeping everything else: the object, its parts and materials. "
                            f"One per line as id: sentence.\n{listing}", None, schema, PLANNER)
        save_json(subjects_path, {item["id"]: item["subject"] for item in answer["items"]})
    subjects = load_json(subjects_path)
    run = folder / arm
    rule, *style = arm.split("+")  # such as new+smooth: the new rule's colors, drawn with the smooth line
    colors_path = folder / rule / "colors.json"
    if not colors_path.exists():
        cards = {t["id"]: {**t["card"], "subject": subjects[t["id"]]} for t in twins}
        save_json(colors_path, recolor(cards, {"old": OLD_HERO, "new": NEW_HERO, "rich": RICH_HERO}[rule]))
    colors = load_json(colors_path)
    if "smooth" in style:
        patched(SMOOTH)
    if "smooth2" in style:
        patched(SMOOTH2)
    briefs = [{**t, "card": {**t["card"], "subject": subjects[t["id"]], **colors[t["id"]]}} for t in twins]
    save_json(run / "briefs.json", briefs)
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(lambda brief: draw_card(run, brief, 1, [], True), briefs))
    print(f"palette {arm}: drew {sum(bool(d) for d in done)} of {len(done)}")


def prefinal_briefs(pairs):
    """Pre-final briefs with ids unique across genres, such as western-v1_03."""
    out = []
    for genre, brief_id in pairs:
        brief = next(b for b in load_json(PREFINAL / genre / "briefs.json") if b["id"] == brief_id)
        out.append({**brief, "id": f"{genre}-{brief_id}", "source": f"runs/prefinal/{genre}", "source_id": brief_id})
    return out


def blockout_cards():
    """24 pre-final cards drawn from a blockout, from the three final genres, fixed by seed."""
    pool = [(genre, b["id"]) for genre in ("western", "period-drama", "detective")
            for b in load_json(PREFINAL / genre / "briefs.json") if (PREFINAL / genre / "models" / f"{b['id']}.png").exists()]
    return sorted(random.Random(8).sample(pool, 24))


def patched(change):
    """Apply a text change to both card prompts. change: (old, new) for the style lines."""
    import make_set

    old, new = change
    assert old in make_set.STYLE and old in make_set.BLOCKOUT, "the line to change is not in the prompts"
    make_set.STYLE, make_set.BLOCKOUT = make_set.STYLE.replace(old, new), make_set.BLOCKOUT.replace(old, new)


def blockout(arm, workers):
    from make_set import draw_card, render_model

    run = OUT / "blockout" / arm
    (run / "models").mkdir(parents=True, exist_ok=True)
    briefs = prefinal_briefs(blockout_cards())
    save_json(run / "briefs.json", briefs)
    for brief in briefs:
        source = ROOT / brief["source"] / "models" / f"{brief['source_id']}"
        target = run / "models" / f"{brief['id']}.png"
        if target.exists():
            continue
        if "fill" in arm.split("+"):
            error, _ = render_model(source.with_suffix(".py"), target, "plain", FILL[brief["card"]["category"]])
            if error:
                print(brief["id"], "render failed:", error[-200:])
        else:
            shutil.copy(source.with_suffix(".png"), target)
    if "smooth" in arm.split("+"):
        patched(SMOOTH)
    if "smooth2" in arm.split("+"):
        patched(SMOOTH2)
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(lambda brief: draw_card(run, brief, 1, [], True), briefs))
    print(f"blockout {arm}: drew {sum(bool(d) for d in done)} of {len(done)}")


def perspective(arm, workers):
    from make_set import draw_card, model_card

    run = OUT / "perspective" / arm
    (run / "models").mkdir(parents=True, exist_ok=True)
    briefs = prefinal_briefs(BROKEN)
    for brief in briefs:
        source = ROOT / brief["source"] / "models" / f"{brief['source_id']}.png"
        if source.exists():
            shutil.copy(source, run / "models" / f"{brief['id']}.png")
    if arm == "model":
        briefs = [b for b in briefs if not (run / "models" / f"{b['id']}.png").exists()]
        with ThreadPoolExecutor(workers) as pool:
            renders = list(pool.map(lambda brief: model_card(run, brief, JUDGE), briefs))
        print("models rendered:", sum(r is not None for r in renders), "of", len(briefs))
    else:
        import make_set

        anchor = "Keep its true proportions and mild perspective, from a low camera, so openings and rims are thin ovals."
        held = "Keep every part, every connection, the pose, the camera and the framing exactly."
        assert anchor in make_set.STYLE and held in make_set.BLOCKOUT
        make_set.STYLE = make_set.STYLE.replace(anchor, f"{anchor} {CAMERA}")
        make_set.BLOCKOUT = make_set.BLOCKOUT.replace(held, f"{held} {CAMERA}")
    save_json(run / "briefs.json", briefs)
    jobs = [(brief, attempt) for brief in briefs for attempt in (1, 2, 3)]
    with ThreadPoolExecutor(workers) as pool:
        done = list(pool.map(lambda job: draw_card(run, job[0], job[1], [], True), jobs))
    print(f"perspective {arm}: drew {sum(bool(d) for d in done)} of {len(done)}")


def value(measured, path):
    section, name = path.split(".")
    return measured.get(section, {}).get(name)


def measure_files(records, derived):
    """records: dicts with id and file. Masks first, then the pipeline's measured fields."""
    from estimate import write_masks
    from measure import measure_card

    missing = [r for r in records if not (derived / "masks" / f"{r['id']}.png").exists()]
    if missing:
        write_masks(missing, "cuda", derived / "masks")
    out = {}
    for record in records:
        try:
            out[record["id"]] = measure_card(record, derived)
        except Exception as error:
            print(record["id"], "not measured:", type(error).__name__)
    return out


def csd(pairs):
    """CSD cosine of each (drawn, real) file pair."""
    import torch
    from PIL import Image

    from embed import MODELS, load_csd

    encode = load_csd(MODELS["csd"])
    files = [p for pair in pairs for p in pair]
    with torch.inference_mode():
        vectors = torch.cat([encode([Image.open(f).convert("RGB") for f in files[i:i + 8]]).float()
                             for i in range(0, len(files), 8)])
    vectors = torch.nn.functional.normalize(vectors, dim=-1).cpu().numpy()
    return [float(vectors[2 * i] @ vectors[2 * i + 1]) for i in range(len(pairs))]


def distribution(measured, real):
    """Median and AUC against the real cards (above 0.5: ours higher) for each field."""
    from sklearn.metrics import roc_auc_score

    rows = {}
    for path in FIELDS:
        ours = [v for v in (value(m, path) for m in measured.values()) if v is not None]
        theirs = [v for v in (value(m, path) for m in real) if v is not None]
        if len(ours) > 3:
            rows[path] = {"median": round(float(np.median(ours)), 4), "real": round(float(np.median(theirs)), 4),
                          "auc": round(float(roc_auc_score([0] * len(theirs) + [1] * len(ours), theirs + ours)), 3)}
    return rows


def paired(base, arm, target=None):
    """Per card: does the arm sit closer to the target (each card's real values) than the base? Or, with no target,
    how often the arm is higher. Wilcoxon on the paired differences."""
    from scipy.stats import wilcoxon

    rows = {}
    for path in FIELDS:
        keys = [k for k in base if k in arm and value(base[k], path) is not None and value(arm[k], path) is not None
                and (target is None or value(target[k], path) is not None)]
        if len(keys) < 8:
            continue
        a, b = np.array([value(base[k], path) for k in keys]), np.array([value(arm[k], path) for k in keys])
        if target is None:
            d = b - a
            rows[path] = {"higher": f"{int((d > 0).sum())}/{len(keys)}", "median_shift": round(float(np.median(d)), 4),
                          "p": round(float(wilcoxon(d).pvalue), 4) if d.any() else 1.0}
        else:
            t = np.array([value(target[k], path) for k in keys])
            d = np.abs(b - t) - np.abs(a - t)
            rows[path] = {"closer": f"{int((d < 0).sum())}/{len(keys)}", "median_gap_base": round(float(np.median(a - t)), 4),
                          "median_gap_arm": round(float(np.median(b - t)), 4),
                          "p": round(float(wilcoxon(d).pvalue), 4) if d.any() else 1.0}
    return rows


def read():
    cards = {c["id"]: c for c in load_json(ANALYSIS / "cards.json")}
    measurements = load_json(ANALYSIS / "measurements.json")
    objects = [m for i, m in measurements.items() if cards[i]["form"]["staging"]["art_category"] in "1234"]
    twins = load_json(TWINS / "briefs.json")
    real_twin = {t["id"]: measurements[t["real"]] for t in twins if t["real"] in measurements}
    result = {}

    # Twins: the style arms from param.py and the palette arms, each against the twin's own real card
    arms = {label: TWINS / label / "tries" for label in ("n0", "ns", "nc", "ns2")}
    arms.update({f"palette-{a}": OUT / "palette" / a / "tries" for a in ("old", "new", "rich", "rich+smooth2")})
    measured = {}
    for label, folder in arms.items():
        records = [{"id": f"{t['id']}_1", "file": str((folder / f"{t['id']}_1.png").relative_to(ROOT))}
                   for t in twins if (folder / f"{t['id']}_1.png").exists()]
        if not records:
            continue
        found = measure_files(records, folder.parent / "derived")
        measured[label] = {k.rsplit("_", 1)[0]: v for k, v in found.items()}
        scores = csd([(ROOT / r["file"], ROOT / f"materials/card_examples/{t['real']}.png")
                      for r in records for t in twins if r["id"] == f"{t['id']}_1"])
        result[label] = {"n": len(records), "csd_own_real": round(float(np.mean(scores)), 4),
                         "csd_by_twin": {r["id"].rsplit("_", 1)[0]: round(s, 4) for r, s in zip(records, scores)},
                         "distribution": distribution(measured[label], objects)}
    for base, arm in (("n0", "ns"), ("n0", "nc"), ("n0", "ns2"), ("palette-old", "palette-new"), ("n0", "palette-old"),
                      ("palette-old", "palette-rich"), ("palette-rich", "palette-rich+smooth2")):
        if base in measured and arm in measured:
            common = sorted(set(result[base]["csd_by_twin"]) & set(result[arm]["csd_by_twin"]))
            x = np.array([result[base]["csd_by_twin"][k] for k in common])
            y = np.array([result[arm]["csd_by_twin"][k] for k in common])
            result[f"{base}->{arm}"] = {"to_own_real": paired(measured[base], measured[arm], real_twin),
                                        "csd_closer": f"{int((y > x).sum())}/{len(common)}",
                                        "csd_mean": [round(float(x.mean()), 4), round(float(y.mean()), 4)]}

    # Blockout arms against each card's first pre-final candidate, and against the real cards of the same categories
    briefs = prefinal_briefs(blockout_cards())
    control = [{"id": b["id"], "file": f"{b['source']}/tries/{b['source_id']}_1.png"} for b in briefs]
    blocks = {"control": measure_files(control, OUT / "blockout" / "control" / "derived")}
    for arm in ("smooth", "fill", "fill+smooth", "fill+smooth2"):
        folder = OUT / "blockout" / arm
        records = [{"id": b["id"], "file": str((folder / "tries" / f"{b['id']}_1.png").relative_to(ROOT))}
                   for b in briefs if (folder / "tries" / f"{b['id']}_1.png").exists()]
        if records:
            blocks[arm] = measure_files(records, folder / "derived")
    categories = {b["card"]["category"] for b in briefs}
    same = [m for i, m in measurements.items() if cards[i]["form"]["staging"]["art_category"] in categories]
    for arm, found in blocks.items():
        result[f"blockout-{arm}"] = {"n": len(found), "distribution": distribution(found, same)}
        if arm != "control":
            result[f"blockout-control->{arm}"] = paired(blocks["control"], found)
    save_json(OUT / "read.json", result)
    for key, row in result.items():
        if "->" in key:
            print(key, {k: v for k, v in row.items() if k != "to_own_real"})
            for path, r in (row.get("to_own_real") or row).items():
                if isinstance(r, dict) and r.get("p", 1) < 0.2:
                    print("   ", path, r)
        else:
            print(key, "n", row["n"], "csd", row.get("csd_own_real"))


def eyes(arm, rater="claude-opus-5-5"):
    """Blockout arm against its control, by eye, both orders. +1: the arm has more of it."""
    from param import pair_sheet
    from review import array, ask

    questions = {"surface_texture": "Which object's surfaces carry more material texture: grain, weave, nap, pores or small surface marks?",
                 "smooth_render": "Which object looks more like a clean, smooth 3D render rather than a textured illustration?",
                 "gloss": "Which object looks glossier, more lacquered or plastic?",
                 "detail": "Which object has more small parts and details?",
                 "lighter": "Which card is lighter overall?"}
    folder = OUT / "blockout" / arm
    briefs = [b for b in prefinal_briefs(blockout_cards()) if (folder / "tries" / f"{b['id']}_1.png").exists()]
    (folder / "sheets").mkdir(exist_ok=True)
    answer = {"type": "string", "enum": ["A", "B", "same"]}
    votes = {}
    for order in (0, 1):
        laid = []
        for i, b in enumerate(briefs):
            arm_first = (i + order) % 2 == 0
            control = {"file": f"{b['source']}/tries/{b['source_id']}_1.png"}
            drawn = {"file": str((folder / "tries" / f"{b['id']}_1.png").relative_to(ROOT))}
            # pair_sheet puts its second argument first when real_first is false
            path = pair_sheet(control, drawn, not arm_first, folder / "sheets" / f"{b['id']}_{order}.png")
            laid.append((b["id"], path, "A" if arm_first else "B"))
        for start in range(0, len(laid), 5):
            batch = laid[start:start + 5]
            out = folder / "eyes" / f"{order}_{start:02d}.json"
            if not out.exists():
                listing = ", ".join(f"{key} is image {i + 1}" for i, (key, _, _) in enumerate(batch))
                schema = strict({"pairs": array(strict({"pair": {"type": "string", "enum": [k for k, _, _ in batch]},
                                                        **{q: answer for q in questions}}))})
                result = ask(rater, "You compare two mobile-game cards, A and B, that show the same object. Do not judge "
                             "which is better. For each property, say which card has more of it, or same when you cannot "
                             "see a difference. Look closely at the object.\n" +
                             "\n".join(f"- {k}: {q}" for k, q in questions.items()) + f"\nPairs: {listing}.",
                             [p for _, p, _ in batch], schema)
                if result:
                    save_json(out, result)
            result = load_json(out) if out.exists() else {"pairs": []}
            sides = {k: s for k, _, s in batch}
            for item in result["pairs"]:
                for q in questions:
                    v = 0 if item[q] == "same" else (1 if item[q] == sides[item["pair"]] else -1)
                    votes.setdefault(item["pair"], {}).setdefault(q, [None, None])[order] = v
    summary = {}
    for q in questions:
        agreed = [v[q][0] for v in votes.values() if q in v and v[q][0] == v[q][1] and v[q][0] is not None]
        summary[q] = {"arm_more": sum(a > 0 for a in agreed), "arm_less": sum(a < 0 for a in agreed),
                      "consistent": f"{len(agreed)}/{len(votes)}"}
    save_json(folder / "eyes.json", {"summary": summary, "votes": votes})
    print(arm, summary)


FINAL = {"western": 1, "period-drama": 3, "detective": 2}  # the outside rater's best variant of each kept genre
# The final cards, after experiments/plan_review.py: (source run, brief id, changed fields, why). Grades: the producer's
# from runs/ratings.json, the outside rater's from runs/prefinal/outside.
PICKS = {
    "western": [
        ("western-batch2", "v1_01", {}, "Cowboy Hat: the producer's 5 in batch 2; the pre-final hat was graded broken."),
        ("western-blockout", "v1_05", {"name": "Sheriff Star", "subject": "A gold five-pointed sheriff star badge with a "
                                       "small ball on each tip and a raised rim along its edges.", "hero_colors": "warm gold",
                                       "pattern": "concentric_rings", "backdrop_colors": "rich purple", "build_model": True},
         "Sheriff Star replaces the Gold Pan (outside 2): the genre's badge, absent from all three variants. It rose from 2 "
         "to 4 with a Blender model; no accent, since a red gem drew a jewel (lessons)."),
        ("western-batch2", "v1_03", {"pattern": "waves", "backdrop_colors": "pink"},
         "Harmonica: the producer's 5 in batch 2, with that wording; on v1's pink waves, the set's one pink."),
        ("western-batch", "v1_03", {"pattern": "diamonds"}, "Bandana replaces the Barrel (the producer's 1): the producer's 5 in batch 1."),
        ("prefinal/western", "v1_04", {"name": "Cowboy Boots", "backdrop_colors": "grass green"},
         "Cowboy Boots: a pair with spurs and no stitched stars, as the producer asked in batch 2 (5); outside 4 on v3's twin."),
        ("prefinal/western", "v3_05", {}, "Saddle on a fence rail (v3) instead of on a hay bale (v1), which drew one stirrup and "
                                          "an awkward perch; built objects gained most from blockouts."),
        ("prefinal/western", "v1_06", {}, "Cactus: outside 4, the producer's 4, 5 and 5 on earlier wordings."),
        ("prefinal/western", "v1_08", {}, "Covered Wagon: outside 3, the producer's 4 and 3; four wheels, tongue on the ground."),
        ("western-batch", "v1_08", {"build_model": True},
         "Windmill with a solid tapering tower (the producer's 4 in batch 1) instead of v1's open truss, which the lessons "
         "advise against."),
        ("western-batch2", "v1_09", {"subject": "A bright fire with a yellow-white glowing core, orange flame tips curling "
                                     "upward, glowing orange ends on the logs, and warm orange light cast on what stands near "
                                     "it; the logs sit in a ring of grey stones, with a grey enamel coffee pot with a red rim "
                                     "on a flat stone beside it.",
                                     "hero_colors": "orange flames, wood brown logs, grey enamel coffee pot with a red rim, "
                                                    "grey stones"},
         "Campfire: the producer's 5 in batch 2, with v1's grey enamel pot instead of a black one."),
    ],
    "period-drama": [
        ("prefinal/period-drama", "v3_01", {}, "Tea Cup: outside 3, as its twins in v1 and v2."),
        ("prefinal/period-drama", "v3_02", {"subject": "A tall round hat box with a shallow flat lid overlapping the top edge "
                                            "and a cream cord handle looped through two holes in the lid.",
                                            "hero_colors": "burgundy red with a cream cord handle"},
         "Hat Box: outside 4, reworded because its ribbon and bow drew a gift box."),
        ("prefinal/period-drama", "v3_03", {}, "Top Hat: outside 5, the best grade of the three variants; v2's grey hat was broken."),
        ("prefinal/period-drama", "v3_04", {}, "Parasol: outside 3, as in v2."),
        ("prefinal/period-drama", "v1_04", {}, "Pocket Watch replaces the Violin (outside 3), which names music, not the period."),
        ("prefinal/period-drama", "v3_06", {}, "Folding Fan: ungraded; no graded alternative is better."),
        ("prefinal/period-drama", "v3_07", {}, "Cake Stand: afternoon tea without a second cup."),
        ("prefinal/period-drama", "v3_08", {"subject": "A flat-topped rectangular steamer trunk with two leather straps "
                                            "buckled around it, brass corner guards, a brass latch at the front and a leather "
                                            "handle on each end, standing on a stone station platform.",
                                            "hero_colors": "wood brown with tan leather straps and brass fittings",
                                            "surface_or_setting": "stone station platform"},
         "Steamer Trunk: reworded with a flat top and straps, because its rounded lid drew a treasure chest."),
        ("prefinal/period-drama", "v3_09", {}, "Pearl Necklace: lying on velvet, seen from above."),
        ("prefinal/period-drama", "v3_10", {}, "Piano: the set's one place card."),
    ],
    "detective": [
        ("prefinal/detective", "v2_01", {}, "Flashlight: outside 3."),
        ("prefinal/detective", "v2_02", {}, "Flash Camera: its twins in v1 and v3 got 3."),
        ("prefinal/detective", "v3_01", {}, "Magnifier, floating, replaces the Map Magnifier (outside 2, broken: a lens drawn "
                                            "front-on while lying flat)."),
        ("prefinal/detective", "v2_04", {}, "Fedora: the genre's hat, on a floor."),
        ("prefinal/detective", "v2_05", {}, "Badge Wallet: the badge, lying flat in its wallet."),
        ("prefinal/detective", "v2_06", {}, "Evidence Bag: outside 3."),
        ("prefinal/detective", "v1_05", {}, "Steel Safe replaces the Tape Roll (outside 3), which without text is only tape; "
                                            "the safe got outside 4."),
        ("prefinal/detective", "v2_08", {}, "Doorknob Print: the small object in its exact spot."),
        ("prefinal/detective", "v2_09", {}, "Squad Car: outside 4; carries the set's one emblem."),
        ("prefinal/detective", "v2_10", {}, "Bloodhound: outside 3 in v1; the set's one animal."),
    ],
}
FIELDS_KEPT = ("name", "subject", "object_class", "category", "pattern", "hero_colors", "backdrop_colors",
               "surface_or_setting", "build_model")


def plans():
    """The final's plan files in runs/plans/: one set per genre, composed after experiments/plan_review.py from the
    pre-final variants and the producer's earlier batches (PICKS), and six cast cards, two per genre. Western keeps its
    pre-final cast pair; Period Drama and Detective get two new ones each from a full plan with cast."""
    from make_set import make_plan, plan_problems, sensitive_cards

    knowledge = load_json(ANALYSIS / "knowledge.json")
    folder = ROOT / "runs" / "plans"
    for genre, variant in FINAL.items():
        plan = load_json(PREFINAL / genre / "plan.json")
        cards, notes = [], [f"Composed on 2026-11-08 from the outside rater's best variant (v{variant}) after a review "
                            "of all three pre-final variants and the producer's earlier grades "
                            "(experiments/plan_review.py, runs/night/plan_review.json)."]
        for run, brief_id, changes, why in PICKS[genre]:
            card = next(b["card"] for b in load_json(ROOT / "runs" / run / "briefs.json") if b["id"] == brief_id)
            cards.append({**{key: card.get(key) for key in FIELDS_KEPT}, **changes})
            notes.append(f"{why} Source: runs/{run} {brief_id}.")
        single = {"title": plan["title"], "story": plan["story"], "declined": plan["declined"],
                  "variants": [{"cards": cards}], "notes": notes, "cast": 0}
        single["problems"] = plan_problems(single, 0, 1)
        single["sensitive"] = sensitive_cards(single)
        print(genre, "| problems:", single["problems"] or "none", "| flagged:", single["sensitive"] or "none")
        save_json(folder / f"final-{genre}.json", single)
    path = folder / "final-cast.json"
    if path.exists():
        return
    bonus = load_json(PREFINAL / "cast" / "plan.json")
    cards = [card for card in bonus["variants"][0]["cards"] if card["topic"] == "Western"]
    sources = []
    for genre in ("Period Drama", "Detective"):
        plan = make_plan(genre, "A set for a Movie collection", 1, knowledge, cast=2)
        sources.append(plan)
        cards += [{**card, "topic": plan["title"]} for card in plan["variants"][0]["cards"] if card["category"] == "5"]
        print(genre, "|", plan["problems"], "|", plan["sensitive"], "|",
              [(c["name"], c["cast"], c["subject"]) for c in plan["variants"][0]["cards"] if c["category"] == "5"])
    save_json(path, {"title": "Movie cast", "story": "Bonus character cards with the game's cast, two per film genre.",
                     "declined": [], "variants": [{"cards": cards}], "problems": [], "sensitive": [], "cast": 2,
                     "sources": sources})


def recolor_final():
    """Rewrite the final plans' hero colors under the adopted rich-color rule (the palette arm), keeping each subject but
    its color words and each backdrop unless the temperature rule needs a change. Every change goes into the notes."""
    from rate import ask_claude

    for genre in FINAL:
        path = ROOT / "runs" / "plans" / f"final-{genre}.json"
        plan = load_json(path)
        if any(note.startswith("Colors rewritten") for note in plan["notes"]):
            continue
        cards = plan["variants"][0]["cards"]
        listing = "\n".join(f"c{i}: {c['name']}: {c['subject']} [category {c['category']}, {c['pattern']}] colors: "
                            f"{c['hero_colors']} on {c['backdrop_colors']}" for i, c in enumerate(cards))
        schema = strict({"cards": {"type": "array", "items": strict({
            "id": {"type": "string", "enum": [f"c{i}" for i in range(len(cards))]}, "subject": text(),
            "hero_colors": text(), "backdrop_colors": text()})}})
        answer = ask_claude(f"""You are the lead producer of card collections for a cozy mobile game. Rewrite the colors of each card below by these rules learned from the game's real cards:
{color_rules(RICH_HERO)}

Keep each subject word for word, except its color words, which must match the new hero colors. Keep backdrop_colors unless the new hero colors break the temperature rule. An object whose natural color is its identity keeps it, such as a gold badge, a green cactus or a white canvas.

Cards, one per line as id: name: subject [art category, backdrop pattern] colors: hero on backdrop:
{listing}""", None, schema, PLANNER)
        notes = []
        for item in answer["cards"]:
            card = cards[int(item["id"][1:])]
            changed = [f"{key} '{card[key]}' to '{item[key]}'" for key in ("subject", "hero_colors", "backdrop_colors")
                       if item[key].strip() != card[key].strip()]
            if changed:
                notes.append(f"{card['name']}: " + "; ".join(changed))
            card.update(subject=item["subject"], hero_colors=item["hero_colors"], backdrop_colors=item["backdrop_colors"])
        plan["notes"].append("Colors rewritten on 2026-11-08 under the rich-color rule adopted from the palette arm "
                             "(runs/night/read.json: CSD to the twin's own real card closer on 29 of 40). " + " | ".join(notes))
        save_json(path, plan)
        print(genre, "\n  " + "\n  ".join(notes))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("palette", "blockout", "perspective", "read", "eyes", "plans", "recolor"))
    parser.add_argument("arm", nargs="?")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.mode == "palette":
        palette(args.arm, args.workers)
    elif args.mode == "blockout":
        blockout(args.arm, args.workers)
    elif args.mode == "perspective":
        perspective(args.arm, args.workers)
    elif args.mode == "eyes":
        eyes(args.arm)
    elif args.mode == "plans":
        plans()
    elif args.mode == "recolor":
        recolor_final()
    else:
        read()


if __name__ == "__main__":
    main()
