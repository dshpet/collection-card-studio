"""Does a one-camera fit find the cards drawn from two cameras?

GeoCalib (Veicht et al., ECCV 2024) predicts a perspective field, the up direction and latitude at every pixel, and
fits one pinhole camera to it. On a card drawn from one camera the field should agree with that fit; parts drawn from
another camera should not. Scores per card, inside the subject mask: the up and latitude residuals to the whole fit,
and the pitch and roll gaps between cameras fitted to the top and bottom, and left and right, halves of the subject.

Labels: the producer's comments naming perspective, angle or camera (runs/ratings.json), their cards graded 4-5 that
work, their other broken cards, the outside rater's broken cards and her others graded 3 or more, all forty twins
(paired with their real cards), and the 160 real cards. GeoCalib code from .models/src/geocalib at 1dedb29 (Apache-2.0),
weights geocalib-pinhole.tar v1.0 (CC BY 4.0, sha256 86d6aeac...), loaded with torch's restricted loader.

    perspective_check.py    -> runs/perspective_check/scores.json, summary.json
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import re

from common import ANALYSIS, MODELS, ROOT, cards, load_json, save_json

import numpy as np
import torch
from PIL import Image
from scipy.stats import mannwhitneyu, wilcoxon

sys.path.insert(0, str(MODELS / "src/geocalib"))
from geocalib.geocalib import GeoCalib  # noqa: E402
from geocalib.perspective_fields import get_perspective_field  # noqa: E402
from geocalib.utils import ImagePreprocessor  # noqa: E402

OUT = ROOT / "runs" / "perspective_check"
WEIGHTS = MODELS / "geocalib" / "pinhole.tar"
PERSPECTIVE = re.compile(r"perspective|angle|camera|seen from", re.I)
CARD_RUNS = ("western", "sci-fi", "horror", "western-batch", "sci-fi-batch", "horror-batch",
             "western-batch2", "sci-fi-batch2", "horror-batch2")


def mask_of(path):
    path = ROOT / path
    if path.parts[-3:-1] == ("materials", "card_examples"):
        mask = ANALYSIS / "derived" / "masks" / path.name
    else:
        mask = path.parent.parent / "derived" / "masks" / path.name
    return mask if mask.exists() else None


def labelled():
    """Every labelled image once, with the strongest label it has."""
    import rate_ui
    ratings = load_json(ROOT / "runs" / "ratings.json")
    items = {item["id"]: item for item in rate_ui.items(sets=CARD_RUNS)}
    rows = {}

    def add(path, group, source):
        if path not in rows or group in ("flagged", "outside_broken"):
            rows[path] = {"file": path, "group": group, "source": source}

    for key, rating in ratings.items():
        if not key.endswith("|me") or rating["id"] not in items:
            continue
        item, comment = items[rating["id"]], rating.get("comment", "")
        if rating["kind"] == "twin":
            drawn = [item["images"][0 if item["generated"] == "A" else 1]]
        elif rating["kind"] in ("closest", "param"):
            drawn = item["images"][1:]
        elif rating["kind"] == "trial":  # the real card first
            drawn = item["images"][1:]
        else:
            drawn = item["images"][:1]
        if PERSPECTIVE.search(comment):
            for path in drawn:
                add(path, "flagged", rating["id"])
        elif rating["kind"] in ("card", "redraw", "trial", "soft", "cast"):
            if rating.get("grade", 0) >= 4 and rating.get("works") in ("yes", None):
                add(drawn[0], "producer_good", rating["id"])
            elif rating.get("works") == "no":
                add(drawn[0], "producer_broken_other", rating["id"])
    outside = load_json(ROOT / "runs" / "prefinal" / "outside" / "ratings.json")
    for card in load_json(ROOT / "runs" / "prefinal" / "outside" / "items.json")["cards"]:
        rating = outside.get(f"{card['id']}|reviewer 2", {})
        if rating.get("broken"):
            add(card["image"], "outside_broken", card["id"])
        elif rating.get("grade", 0) >= 3:
            add(card["image"], "outside_ok", card["id"])
    for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json"):
        for style in ("final", "old"):
            add(f"runs/twins40/{style}/tries/{brief['id']}_1.png", "twin", f"{style}/{brief['id']}")
    for record in cards():
        add(record["file"], "real", record["id"])
    return list(rows.values())


def degrees(value):
    return float(np.degrees(float(value)))


def score(model, path):
    process = ImagePreprocessor({"resize": 320, "edge_divisible_by": 32})
    image = torch.from_numpy(np.asarray(Image.open(ROOT / path).convert("RGB"), dtype=np.float32) / 255)
    data = process(image.permute(2, 0, 1)[None].cuda())
    mask_path = mask_of(path)
    if mask_path:
        mask = np.asarray(Image.open(mask_path).convert("L").resize(Image.open(ROOT / path).size), dtype=np.float32) / 255
        mask = process(torch.from_numpy(mask)[None, None].expand(1, 3, -1, -1).cuda())["image"][0, 0] > 0.5
    else:
        mask = torch.ones(data["image"].shape[-2:], dtype=torch.bool, device="cuda")
    with torch.no_grad():
        out = model(data)
        fields = {k: out[k] for k in ("up_field", "latitude_field", "up_confidence", "latitude_confidence")}

        def fit(region):
            region = region.float()[None]
            result = model.optimizer(fields | {"up_confidence": fields["up_confidence"] * region,
                                               "latitude_confidence": fields["latitude_confidence"] * region})
            return result["gravity"].rp[0], result["camera"].vfov[0]

        up_fit, lat_fit = get_perspective_field(out["camera"], out["gravity"])
        up_error = torch.rad2deg(torch.acos((fields["up_field"] * up_fit).sum(1).clamp(-1, 1)))[0]
        lat_error = torch.rad2deg((fields["latitude_field"] - lat_fit).abs())[0, 0]
        ys, xs = torch.nonzero(mask, as_tuple=True)
        rows, cols = torch.meshgrid(torch.arange(mask.shape[0], device="cuda"),
                                    torch.arange(mask.shape[1], device="cuda"), indexing="ij")
        gaps = {}
        for name, split in (("vertical", rows < ys.float().median()), ("horizontal", cols < xs.float().median())):
            (roll_a, pitch_a), _ = fit(mask & split)
            (roll_b, pitch_b), _ = fit(mask & ~split)
            gaps[f"pitch_gap_{name}"] = abs(degrees(pitch_a - pitch_b))
            gaps[f"roll_gap_{name}"] = abs(degrees(roll_a - roll_b))
        (roll_m, pitch_m), vfov_m = fit(mask)
    roll, pitch = out["gravity"].rp[0]
    weight = fields["up_confidence"][0][mask]
    return {
        "masked": mask_path is not None,
        "roll": round(degrees(roll), 2), "pitch": round(degrees(pitch), 2), "vfov": round(degrees(out["camera"].vfov[0]), 2),
        "pitch_subject": round(degrees(pitch_m), 2), "vfov_subject": round(degrees(vfov_m), 2),
        "pitch_uncertainty": round(degrees(out["pitch_uncertainty"][0]), 3),
        "roll_uncertainty": round(degrees(out["roll_uncertainty"][0]), 3),
        "up_residual": round(float((up_error[mask] * weight).sum() / weight.sum()), 3),
        "latitude_residual": round(float(lat_error[mask].mean()), 3),
        "up_residual_p90": round(float(torch.quantile(up_error[mask], 0.9)), 3),
        "confidence": round(float(weight.mean()), 3),
        **{k: round(v, 3) for k, v in gaps.items()},
        "split_gap": round(max(gaps["pitch_gap_vertical"], gaps["pitch_gap_horizontal"]), 3),
    }


def auc(positive, negative):
    if not positive or not negative:
        return None
    statistic, p = mannwhitneyu(positive, negative, alternative="two-sided")
    return {"auc": round(statistic / (len(positive) * len(negative)), 3), "p": round(float(p), 4),
            "n": [len(positive), len(negative)]}


def summarize(rows):
    fields = ["up_residual", "latitude_residual", "up_residual_p90", "split_gap", "pitch_gap_vertical",
              "roll_gap_vertical", "pitch_uncertainty", "roll_uncertainty", "confidence"]
    groups = {}
    for row in rows:
        groups.setdefault(row["group"], []).append(row)
    summary = {"counts": {g: len(r) for g, r in groups.items()}, "median": {}, "auc": {}, "at_real_p90": {}}
    for field in fields:
        values = {g: [r[field] for r in rs] for g, rs in groups.items()}
        summary["median"][field] = {g: round(float(np.median(v)), 3) for g, v in values.items()}
        summary["auc"][field] = {
            "flagged_vs_producer_good": auc(values["flagged"], values["producer_good"]),
            "outside_broken_vs_outside_ok": auc(values["outside_broken"], values["outside_ok"]),
            "flagged_vs_real": auc(values["flagged"], values["real"]),
            "all_flagged_vs_all_ok": auc(values["flagged"] + values["outside_broken"],
                                         values["producer_good"] + values["outside_ok"]),
            "producer_broken_other_vs_producer_good": auc(values["producer_broken_other"], values["producer_good"]),
        }
        threshold = float(np.percentile(values["real"], 90))
        summary["at_real_p90"][field] = {g: f"{sum(v > threshold for v in vs)}/{len(vs)}" for g, vs in values.items()}
    # Twins hold content equal: does the drawn twin score above its own real card, more so when flagged?
    real = {r["source"]: r for r in rows if r["group"] == "real"}
    briefs = {b["id"]: b["real"] for b in load_json(ROOT / "runs" / "twins40" / "briefs.json")}
    paired = {}
    for row in rows:
        match = re.search(r"twins40/(\w+)/tries/(m\d+)_1", row["file"])
        if match and briefs.get(match.group(2)) in real:
            other = real[briefs[match.group(2)]]
            paired.setdefault("flagged" if row["group"] == "flagged" else "unflagged", []).append(
                {f: row[f] - other[f] for f in fields})
    summary["twin_minus_real"] = {}
    for field in fields:
        entry = {}
        for name, diffs in paired.items():
            d = [x[field] for x in diffs]
            entry[name] = {"median": round(float(np.median(d)), 3), "above": f"{sum(x > 0 for x in d)}/{len(d)}",
                           "p": round(float(wilcoxon(d).pvalue), 4) if len(d) > 5 else None}
        summary["twin_minus_real"][field] = entry
    return summary


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    model = GeoCalib()
    model.flexible_load(torch.load(WEIGHTS, map_location="cpu", weights_only=True)["model"])
    model = model.eval().cuda()
    done = {r["file"]: r for r in load_json(OUT / "scores.json")} if (OUT / "scores.json").exists() else {}
    rows = []
    for index, row in enumerate(labelled()):
        if row["file"] not in done:
            done[row["file"]] = row | score(model, row["file"])
            if index % 50 == 0:
                print(index, row["file"], flush=True)
        rows.append(done[row["file"]])
    save_json(OUT / "scores.json", rows)
    summary = summarize(rows)
    save_json(OUT / "summary.json", summary)
    print(summary["counts"])
    for field, entry in summary["auc"].items():
        print(field, {k: (v["auc"], v["p"]) if v else None for k, v in entry.items()})


if __name__ == "__main__":
    main()
