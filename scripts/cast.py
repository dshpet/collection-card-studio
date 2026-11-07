"""The recurring cast of the reference cards, cut out as a library to reuse on new cards.

The collection has one cast: a man with glasses and a mustache, a pig, a sheep, a cow and a rooster. They appear on 30
of its 31 character cards, in many outfits and from many angles.

    cast.py find     SAM 3 cuts every cast member out of every reference card
    cast.py label    a vision model labels each cutout: view, pose, how much body shows, outfit, cleanness
    cast.py sheet    one sheet per character, for a look

Cutouts are Playrix art, so they live in library/cast/ out of git. Their records are in analysis/cast.json.
"""

import argparse
import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")

from common import ANALYSIS, PLANNER, ROOT, cards, hf_key, load_json, save_json

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont

LIBRARY = ROOT / "library" / "cast"
CATALOG = ANALYSIS / "cast.json"
CAST = {
    "man": "man",
    "pig": "pig",
    "sheep": "sheep",
    "cow": "cow",
    "rooster": "rooster",
}
LOOKS = {
    "man": "a stocky man with short brown hair, round glasses and a big brown mustache",
    "pig": "a round pink pig with big ears and a curly tail, standing on two legs",
    "sheep": "a sheep with a white fleece of round curls, a dark grey face and dark grey legs",
    "cow": "a white cow with black spots, a big orange muzzle and short horns",
    "rooster": "an orange rooster with a red comb, a yellow beak and big round eyes",
}
THRESHOLD = 0.4
MIN_AREA = 0.03  # of the card: drops crowds and far background figures
OVERLAP = 0.5  # share of the smaller mask; above it two finds are one figure, and the surer name wins
GREY = (128, 128, 128)


def segmenter():
    """SAM 3 with a text prompt: (image, word) -> [(score, boolean mask)]."""
    from transformers import Sam3Model, Sam3Processor

    # SAM 3 is gated. The key goes to the download alone, never into the environment, which programs this process
    # starts would inherit. Downloading needs HF_HUB_OFFLINE=0; afterwards the cached model loads offline.
    token = hf_key() if os.environ.get("HF_HUB_OFFLINE") == "0" else None
    model = Sam3Model.from_pretrained("facebook/sam3", dtype=torch.float32, token=token).cuda().eval()
    processor = Sam3Processor.from_pretrained("facebook/sam3", token=token)

    def find(image, word, threshold=THRESHOLD):
        inputs = processor(images=image, text=word, return_tensors="pt").to("cuda")
        with torch.inference_mode():
            outputs = model(**inputs)
        result = processor.post_process_instance_segmentation(
            outputs, threshold=threshold, mask_threshold=0.5, target_sizes=[image.size[::-1]])[0]
        return [(float(s), m.cpu().numpy().astype(bool)) for s, m in zip(result["scores"], result["masks"])]

    return find


def figures(image, find):
    """Every cast member on a card: one entry per figure, named by the surest prompt."""
    found = [(name, score, mask) for name, word in CAST.items() for score, mask in find(image, word)
             if mask.mean() >= MIN_AREA]
    found.sort(key=lambda f: -f[1])
    kept = []
    for name, score, mask in found:
        if all((mask & other).sum() / min(mask.sum(), other.sum()) < OVERLAP for _, _, other in kept):
            kept.append((name, score, mask))
    return kept


def cutout(image, mask, margin=4):
    """The figure alone on a transparent ground, cropped to its box."""
    rgba = image.convert("RGBA")
    rgba.putalpha(Image.fromarray((mask * 255).astype(np.uint8)))
    ys, xs = np.nonzero(mask)
    box = (max(xs.min() - margin, 0), max(ys.min() - margin, 0),
           min(xs.max() + margin + 1, image.width), min(ys.max() + margin + 1, image.height))
    return rgba.crop(box), box


def on_grey(path, size=None):
    """A cutout on mid grey, for a model or a sheet."""
    figure = Image.open(path).convert("RGBA")
    if size:
        figure.thumbnail(size, Image.LANCZOS)
    canvas = Image.new("RGB", size or figure.size, GREY)
    canvas.paste(figure, ((canvas.width - figure.width) // 2, (canvas.height - figure.height) // 2), figure)
    return canvas


def find_all():
    """Cut out every figure. A figure found again with the same name and box keeps its labels."""
    find = segmenter()
    known = {(r["id"], r["character"], tuple(r["box"])): r.get("labels") for r in load_json(CATALOG)} if CATALOG.exists() else {}
    records = []
    for card in cards():
        image = Image.open(ROOT / card["file"]).convert("RGB")
        for index, (name, score, mask) in enumerate(figures(image, find)):
            figure, box = cutout(image, mask)
            entry = f"{card['id']}_{index}"
            path = LIBRARY / "real" / name / f"{entry}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            figure.save(path)
            edges = box[0] == 0, box[1] == 0, box[2] == image.width, box[3] == image.height
            records.append({"id": entry, "character": name, "card": card["id"], "score": round(score, 3),
                            "area": round(float(mask.mean()), 3), "box": [int(v) for v in box],
                            "cut_by_edge": [side for side, cut in zip(("left", "top", "right", "bottom"), edges) if cut],
                            "file": str(path.relative_to(ROOT))})
            labels = known.get((entry, name, tuple(records[-1]["box"])))
            if labels:
                records[-1]["labels"] = labels
        print(card["id"], [r["character"] for r in records if r["card"] == card["id"]], flush=True)
    save_json(CATALOG, records)


LABEL_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["figures"], "properties": {
    "figures": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                "required": ["id", "is_character", "view", "body", "pose", "outfit", "clean"], "properties": {
        "id": {"type": "string"},
        "is_character": {"type": "boolean"},
        "view": {"type": "string", "enum": ["front", "three_quarter_left", "three_quarter_right", "side_left",
                                            "side_right", "back"]},
        "body": {"type": "string", "enum": ["full", "most", "upper", "head"]},
        "pose": {"type": "string"},
        "outfit": {"type": "string"},
        "clean": {"type": "boolean"}}}}}}


def label(rater):
    from rate import ask_claude

    records = load_json(CATALOG)
    folder = LIBRARY / "grey"
    folder.mkdir(parents=True, exist_ok=True)
    for name in CAST:
        todo = [r for r in records if r["character"] == name and "labels" not in r]
        for start in range(0, len(todo), 10):
            batch = todo[start:start + 10]
            paths = []
            for record in batch:
                path = folder / f"{record['id']}.png"
                on_grey(ROOT / record["file"]).save(path)
                paths.append(path)
            listing = ", ".join(f"image {i + 1} is {r['id']}" for i, r in enumerate(batch))
            answer = ask_claude(
                f"Each image is a figure cut out of a mobile-game card and shown on grey ({listing}). It should be "
                f"{LOOKS[name]}. For each: is_character is false if it is not that character. view is the way the body "
                "faces, from the viewer: three_quarter_left means turned toward the viewer's left. body is how much of "
                "the body shows. pose in a few words (standing, sitting, waving, holding a guitar). outfit in a few "
                "words, or 'none'. clean is false if the cutout has a missing part, a piece of another figure or a "
                "large prop fused to it.", paths, LABEL_SCHEMA, rater)
            by_id = {f["id"]: f for f in answer["figures"]}
            for record in batch:
                if record["id"] in by_id:
                    record["labels"] = {k: v for k, v in by_id[record["id"]].items() if k != "id"}
            save_json(CATALOG, records)
            print(name, start, len(by_id), flush=True)


def sheet():
    records = load_json(CATALOG)
    font = ImageFont.load_default(16)
    tile = (200, 224)
    for name in CAST:
        mine = [r for r in records if r["character"] == name]
        columns = 6
        canvas = Image.new("RGB", (columns * tile[0], -(-len(mine) // columns) * tile[1]), "white")
        for index, record in enumerate(mine):
            image = on_grey(ROOT / record["file"], tile)
            labels = record.get("labels", {})
            text = f"{record['id'][-6:]} {labels.get('view', '?')} {labels.get('body', '')}"
            if labels and (not labels["clean"] or not labels["is_character"]):
                text += " X"
            ImageDraw.Draw(image).text((4, tile[1] - 20), text, fill="white", font=font)
            canvas.paste(image, (index % columns * tile[0], index // columns * tile[1]))
        canvas.save(LIBRARY / f"{name}.png")
        print(name, len(mine))


def identity_references(name, count=3):
    """The clearest real cutouts of a character, on grey: clean, in no outfit where there is one, as much body as
    possible, largest first. A costume in a cutout tends to come along onto the new card."""
    order = {"full": 0, "most": 1, "upper": 2, "head": 3}
    mine = [r for r in load_json(CATALOG) if r["character"] == name and r.get("labels", {}).get("is_character")
            and r["labels"]["clean"]]
    mine.sort(key=lambda r: (r["labels"]["outfit"].lower() != "none", order[r["labels"]["body"]], -r["area"]))
    return [LIBRARY / "grey" / f"{r['id']}.png" for r in mine[:count]]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("find", "label", "sheet"))
    parser.add_argument("--rater", default=PLANNER)
    args = parser.parse_args()
    if args.mode == "find":
        find_all()
    elif args.mode == "label":
        label(args.rater)
    else:
        sheet()


if __name__ == "__main__":
    main()
