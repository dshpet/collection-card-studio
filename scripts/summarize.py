"""Join everything into one record per card and per set, and compute agreement and distributions."""

import colorsys
import string
from collections import Counter, defaultdict
from itertools import combinations

from common import ANALYSIS, cards, load_json, manifest, save_json

import numpy as np
from sklearn.metrics import cohen_kappa_score

from form import CARD_FORM, SET_FORM

RATERS = ("codex", "claude", "qwen3.8", "gemma4")
TEXT = "text"


def load_ratings(prefix, records):
    """Every rater that covers nearly all records, best rater first."""
    found = {}
    for rater in RATERS:
        folder = ANALYSIS / "ratings" / f"{prefix}{rater}"
        files = {r["id"]: folder / f"{r['id']}.json" for r in records}
        ready = {key: load_json(path) for key, path in files.items() if path.exists()}
        if len(ready) >= 0.9 * len(records):
            found[rater] = ready
    return found


def merge(form, answers):
    """Median for scales, majority for choices, ties to the first rater. Lists disputed fields."""
    merged, disputed = {}, []
    for section, fields in form.items():
        merged[section] = {}
        for name, field in fields.items():
            values = [a[section][name] for a in answers if section in a]
            if field["kind"] == "scale":
                numbers = [v for v in values if isinstance(v, int)]
                merged[section][name] = float(np.median(numbers))
                if max(numbers) - min(numbers) >= 3:
                    disputed.append(f"{section}.{name}")
            elif field["kind"] == "choice":
                top = Counter(values).most_common(1)[0][1]
                winner = next(v for v in values if values.count(v) == top)
                merged[section][name] = winner
                if top * 2 <= len(values):
                    disputed.append(f"{section}.{name}")
            else:
                merged[section][name] = values[0]
    return merged, disputed


def pair_scores(form, first, second):
    shared = sorted(set(first) & set(second))
    scores = {}
    for section, fields in form.items():
        if section not in first[shared[0]] or section not in second[shared[0]]:
            continue
        for name, field in fields.items():
            if field["kind"] == TEXT:
                continue
            a = [first[key][section][name] for key in shared]
            b = [second[key][section][name] for key in shared]
            if field["kind"] == "scale":
                match = float(np.mean([abs(x - y) <= 1 for x, y in zip(a, b)]))
                kappa = cohen_kappa_score(a, b, weights="quadratic", labels=[1, 2, 3, 4, 5])
            else:
                match = float(np.mean([x == y for x, y in zip(a, b)]))
                kappa = cohen_kappa_score(a, b)
            scores[f"{section}.{name}"] = (field["kind"], match, float(np.nan_to_num(kappa)))
    return scores


def agreement(form, ratings):
    """Field agreement averaged over rater pairs, and overall agreement per pair."""
    pairs = {f"{a} + {b}": pair_scores(form, ratings[a], ratings[b])
             for a, b in combinations(ratings, 2)}
    fields = {}
    if pairs:
        paths = {path: scores[path][0] for scores in pairs.values() for path in scores}
        for path, kind in paths.items():
            rows = [p[path] for p in pairs.values() if path in p]
            fields[path] = {"kind": kind, "match": round(float(np.mean([r[1] for r in rows])), 3),
                            "kappa": round(float(np.mean([r[2] for r in rows])), 3)}
    overall = {name: {"choice_match": round(float(np.mean([v[1] for v in p.values() if v[0] == "choice"])), 3),
                      "scale_within_1": round(float(np.mean([v[1] for v in p.values() if v[0] == "scale"])), 3),
                      "mean_kappa": round(float(np.mean([v[2] for v in p.values()])), 3)}
               for name, p in pairs.items()}
    return fields, overall


def distributions(records):
    fields = defaultdict(Counter)
    by_category = defaultdict(lambda: defaultdict(Counter))
    for record in records:
        category = record["form"]["staging"]["art_category"]
        for section, values in CARD_FORM.items():
            for name, field in values.items():
                if field["kind"] == TEXT:
                    continue
                value = record["form"][section][name]
                value = str(round(value)) if field["kind"] == "scale" else value
                fields[f"{section}.{name}"][value] += 1
                by_category[f"{section}.{name}"][category][value] += 1
    return {key: {"all": dict(count), "by_category": {c: dict(v) for c, v in by_category[key].items()}}
            for key, count in fields.items()}


def measured_stats(records):
    grouped = defaultdict(list)
    per_category = defaultdict(lambda: defaultdict(list))
    for record in records:
        category = record["form"]["staging"]["art_category"]
        for section, values in record["measured"].items():
            if not isinstance(values, dict):
                continue
            for name, value in values.items():
                if isinstance(value, (int, float)):
                    grouped[f"{section}.{name}"].append(value)
                    per_category[f"{section}.{name}"][category].append(value)
    summary = {}
    for key, values in grouped.items():
        low, middle, high = np.percentile(values, [10, 50, 90])
        summary[key] = {"p10": round(float(low), 3), "median": round(float(middle), 3),
                        "p90": round(float(high), 3),
                        "by_category": {c: round(float(np.median(v)), 3) for c, v in per_category[key].items()}}
    return summary


def tidy(text):
    return string.capwords(text) if text and text.isupper() else text


def hue_bin(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hue, saturation, _ = colorsys.rgb_to_hsv(*rgb)
    return "neutral" if saturation < 0.2 else int(hue * 12)


def set_metrics(members, style):
    picks = [m["index"] for m in members]
    similarity = style[picks] @ style[picks].T
    pairs = similarity[np.triu_indices(len(picks), 1)]
    return {
        "object_classes": len({m["form"]["identity"]["object_class"] for m in members}),
        "scale_classes": len({m["form"]["identity"]["real_world_scale"] for m in members}),
        "background_hues": len({hue_bin(m["measured"]["color_palette"]["palette_background"][0]["hex"])
                                for m in members}),
        "background_types": len({m["form"]["staging"]["background_type"] for m in members}),
        "categories": dict(sorted(Counter(m["form"]["staging"]["art_category"] for m in members).items())),
        "style_similarity": round(float(pairs.mean()), 3),
    }


def main():
    records = cards()
    set_map = load_json(ANALYSIS / "set_map.json")
    measured = load_json(ANALYSIS / "measurements.json")
    ratings = load_ratings("", records)
    screens = sorted(manifest("collection_examples"), key=lambda r: r["id"])
    set_ratings = load_ratings("sets_", screens)

    first_rater = next(iter(set_ratings.values()))
    readings = {(screen["id"], card["slot"]): card
                for screen in screens for card in first_rater.get(screen["id"], {}).get("cards", [])}

    joined = []
    for index, record in enumerate(records):
        card_id = record["id"]
        answers = [rater[card_id] for rater in ratings.values() if card_id in rater]
        if not answers or card_id not in measured:
            continue
        form, disputed = merge(CARD_FORM, answers)
        place = set_map[card_id]
        reading = readings.get((place["set_id"], place["slot"]), {})
        joined.append({
            "id": card_id, "index": index, "set_id": place["set_id"], "slot": place["slot"],
            "name": tidy(reading.get("name")), "gold_frame": reading.get("gold_frame"), "form": form, "disputed": disputed,
            "raters": {name: rater.get(card_id) for name, rater in ratings.items()},
            "measured": measured[card_id],
        })

    style_path = ANALYSIS / "embeddings" / "csd_whole.npy"
    style = np.load(style_path)
    set_records = []
    for screen in screens:
        members = sorted((c for c in joined if c["set_id"] == screen["id"]), key=lambda c: c["slot"])
        answers = [rater[screen["id"]] for rater in set_ratings.values() if screen["id"] in rater]
        if not members or not answers:
            continue
        form, disputed = merge(SET_FORM, answers)
        set_records.append({"id": screen["id"], "title": tidy(form["reading"]["title"]), "form": form,
                            "disputed": disputed, "cards": [m["id"] for m in members],
                            "metrics": set_metrics(members, style)})
    titles = {s["id"]: s["title"] for s in set_records}
    for card in joined:
        card["set"] = titles.get(card["set_id"])

    save_json(ANALYSIS / "cards.json", joined)
    save_json(ANALYSIS / "sets.json", set_records)
    field_agreement, pair_agreement = agreement(CARD_FORM, ratings)
    save_json(ANALYSIS / "stats.json", {
        "raters": list(ratings), "set_raters": list(set_ratings),
        "agreement": field_agreement, "rater_pairs": pair_agreement, "fields": distributions(joined),
        "measured": measured_stats(joined),
    })
    print(f"joined {len(joined)} cards and {len(set_records)} sets; raters {list(ratings)}")


if __name__ == "__main__":
    main()
