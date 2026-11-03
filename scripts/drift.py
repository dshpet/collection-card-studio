"""How far a generated batch has drifted from the references.

Field drift: each generated card's percentile among real cards of its category. No drift gives a mean of 0.5.
Classifier: can DINOv3 tell the batch from real cards, on the whole card, the subject or the background alone?
Both sides pass through the same preprocessing. "matched" also drops the finest octave, where resampling differs.
Real-likeness: how real the batch looks to a classifier that learned real cards against the first run.
Matched classifier: real cards against their own redraws, which holds content equal.

    drift.py western sci-fi horror
"""

import argparse
import os
from collections import defaultdict

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from common import ANALYSIS, DERIVED, ROOT, load_json, save_json

import numpy as np
import torch
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from embed import MODELS, NEUTRAL, load_hf
from estimate import write_marigold, write_masks
from measure import measure_card

FIRST_RUN = ("first/western", "first/sci-fi", "first/horror")
FIELDS = ("shape_proportions", "surface_finish", "color_palette", "value_contrast", "edges_linework",
          "composition_hierarchy", "lighting_shading")


def picked(run):
    """The best try of every card in a run."""
    from make_set import best_try

    folder = ROOT / "runs" / run
    records = []
    for tries in load_json(folder / "check.json").values():
        best = best_try(tries)
        records.append({"id": best["try_id"], "file": str((folder / "tries" / f"{best['try_id']}.png").relative_to(ROOT)),
                        "category": best["card"]["category"], "name": best["card"]["name"]})
    return folder, records


def real_cards():
    return [{"id": c["id"], "file": f"materials/card_examples/{c['id']}.png",
             "category": c["form"]["staging"]["art_category"], "measured": c["measured"]}
            for c in load_json(ANALYSIS / "cards.json") if c["form"]["staging"]["art_category"] != "5"]


def numbers(measured):
    return {f"{section}.{name}": value for section in FIELDS for name, value in measured.get(section, {}).items()
            if isinstance(value, (int, float)) and not isinstance(value, bool)}


def field_drift(cards, real):
    by_category = defaultdict(lambda: defaultdict(list))
    for card in real:
        for field, value in numbers(card["measured"]).items():
            by_category[card["category"]][field].append(value)
    ranks = defaultdict(list)
    for card in cards:
        for field, value in numbers(card["measured"]).items():
            pool = by_category[card["category"]].get(field)
            if pool:
                ranks[field].append(np.mean(np.array(pool) < value) + 0.5 * np.mean(np.array(pool) == value))
    rows = [{"field": field, "percentile": round(float(np.mean(r)), 3), "n": len(r),
             "z": round(float((np.mean(r) - 0.5) * np.sqrt(12 * len(r))), 1)} for field, r in ranks.items()]
    return sorted(rows, key=lambda row: -abs(row["z"]))


def views(record, derived):
    image = Image.open(ROOT / record["file"]).convert("RGB")
    yield "whole", image
    mask = Image.open(derived / "masks" / f"{record['id']}.png").convert("L")
    grey = Image.new("RGB", image.size, NEUTRAL)
    yield "subject", Image.composite(image, grey, mask)
    yield "background", Image.composite(grey, image, mask)


def matched(image):
    """Keep what survives at half size, so the two resampling histories no longer differ."""
    width, height = image.size
    return image.resize((width // 2, height // 2), Image.BOX).resize((width, height), Image.BICUBIC)


def classifier(cards, real, derived_of):
    encode = load_hf(MODELS["dinov3"], torch.float32)
    labels = np.array([1] * len(real) + [0] * len(cards))
    result = {}
    vectors = defaultdict(list)
    with torch.inference_mode():
        for card in real + cards:
            for view, image in views(card, derived_of(card)):
                for name, prepared in (("native", image), ("matched", matched(image))):
                    vectors[view, name].append(prepared)
        for (view, name), images in vectors.items():
            chunks = [encode(images[start:start + 16]).float().cpu().numpy() for start in range(0, len(images), 16)]
            features = np.concatenate(chunks)
            model = make_pipeline(StandardScaler(), LogisticRegression(C=0.01, max_iter=2000, class_weight="balanced"))
            folds = StratifiedKFold(5, shuffle=True, random_state=0)
            scores = cross_val_predict(model, features, labels, cv=folds, method="predict_proba")[:, 1]
            result[f"{view}/{name}"] = round(float(roc_auc_score(labels, scores)), 3)
    return result


def whole_features(records, encode):
    images = [matched(Image.open(ROOT / r["file"]).convert("RGB")) for r in records]
    with torch.inference_mode():
        chunks = [encode(images[start:start + 16]).float().cpu().numpy() for start in range(0, len(images), 16)]
    return np.concatenate(chunks)


def real_likeness(cards, real):
    """P(real) from a classifier of real cards against the first run. Twin originals stay out of training."""
    encode = load_hf(MODELS["dinov3"], torch.float32)
    cache = ROOT / "runs" / "drift" / "first_run.npz"
    if not cache.exists():
        first = [record for run in FIRST_RUN for record in picked(run)[1]]
        np.savez(cache, first=whole_features(first, encode), real=whole_features(real, encode))
    stored = np.load(cache)
    held = {b["real"] for b in load_json(ROOT / "runs" / "twins" / "briefs.json")}
    keep = np.array([card["id"] not in held for card in real])
    features = np.concatenate((stored["real"][keep], stored["first"]))
    labels = np.array([1] * keep.sum() + [0] * len(stored["first"]))
    model = make_pipeline(StandardScaler(), LogisticRegression(C=0.01, max_iter=2000, class_weight="balanced"))
    model.fit(features, labels)
    return {"batch": round(float(model.predict_proba(whole_features(cards, encode))[:, 1].mean()), 3),
            "held_out_real": round(float(model.predict_proba(stored["real"][~keep])[:, 1].mean()), 3)}


def matched_classifier(name):
    """Each real card against its own redraw. A pair stays in one fold, so only style is left to learn."""
    root = ROOT / "runs" / name
    briefs = load_json(root / "briefs.json")
    encode = load_hf(MODELS["dinov3"], torch.float32)
    originals = [{"id": b["real"], "file": f"materials/card_examples/{b['real']}.png"} for b in briefs]
    groups = np.tile(np.arange(len(briefs)), 2)
    labels = np.array([1] * len(briefs) + [0] * len(briefs))
    result = {}
    for label in sorted(p.name for p in root.iterdir() if p.is_dir()):
        folder = root / label
        drawn = [{"id": f"{b['id']}_1", "file": str((folder / "tries" / f"{b['id']}_1.png").relative_to(ROOT))} for b in briefs]
        write_masks(drawn, "cuda", folder / "derived" / "masks")
        scores = {}
        for view in ("whole", "subject", "background"):
            images = [dict(views(r, DERIVED))[view] for r in originals]
            images += [dict(views(r, folder / "derived"))[view] for r in drawn]
            with torch.inference_mode():
                chunks = [encode(images[i:i + 16]).float().cpu().numpy() for i in range(0, len(images), 16)]
            features = np.concatenate(chunks)
            aucs = []
            for seed in range(20):
                model = make_pipeline(StandardScaler(), LogisticRegression(C=0.01, max_iter=2000))
                folds = StratifiedGroupKFold(5, shuffle=True, random_state=seed)
                predicted = cross_val_predict(model, features, labels, groups=groups, cv=folds, method="predict_proba")[:, 1]
                aucs.append(roc_auc_score(labels, predicted))
            scores[view] = round(float(np.mean(aucs)), 3)
        result[label] = scores
        print(label, scores, flush=True)
    save_json(ROOT / "runs" / "drift" / f"{name}.json", result)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", nargs="*")
    parser.add_argument("--no-classifier", action="store_true")
    parser.add_argument("--matched", help="a folder of twins drawn in several styles, such as twins40")
    args = parser.parse_args()
    if args.matched:
        matched_classifier(args.matched)
        return

    real = real_cards()
    cards, derived = [], {}
    for run in args.runs:
        folder, records = picked(run)
        write_masks(records, "cuda", folder / "derived" / "masks")
        write_marigold(records, "cuda", folder / "derived")
        for record in records:
            record["measured"] = measure_card(record, folder / "derived")
            derived[record["id"]] = folder / "derived"
        save_json(folder / "measured.json", {r["id"]: r["measured"] for r in records})
        cards += records

    fields = field_drift(cards, real)
    for row in fields[:20]:
        print(f"{row['field']:48} percentile {row['percentile']:.2f}  z {row['z']:+.1f}")
    result = {"runs": args.runs, "cards": len(cards), "fields": fields}
    if not args.no_classifier:
        result["auc"] = classifier(cards, real, lambda card: derived.get(card["id"], DERIVED))
        print(result["auc"])
    result["real_likeness"] = real_likeness(cards, real)
    result["mean_drift"] = round(float(np.mean([abs(row["percentile"] - 0.5) for row in fields])), 3)
    print(result["real_likeness"], "mean drift", result["mean_drift"])
    save_json(ROOT / "runs" / "drift" / f"{'+'.join(args.runs).replace('/', '_')}.json", result)


if __name__ == "__main__":
    main()
