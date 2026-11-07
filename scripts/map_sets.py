"""Match every slot in the 16 set screenshots to one of the 160 cards."""

import argparse

import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment

from common import ANALYSIS, ROOT, cards, manifest, save_json

# Card art position in the screenshot, as fractions of width and height.
COLUMNS = (0.2570, 0.3590, 0.4615, 0.5635, 0.6660)
ROWS = (0.3050, 0.6150)
SLOT_W, SLOT_H = 0.0775, 0.1880
PATCH = (48, 54)


def patch(image):
    data = np.asarray(image.convert("RGB").resize(PATCH, Image.LANCZOS), dtype=np.float32)
    data = data[6:-6, 6:-6].ravel()  # skip corners and star overlays
    data -= data.mean()
    return data / (np.linalg.norm(data) + 1e-9)


def slots(path):
    image = Image.open(path)
    width, height = image.size
    for row in ROWS:
        for column in COLUMNS:
            box = (column * width, row * height, (column + SLOT_W) * width, (row + SLOT_H) * height)
            yield image.crop(tuple(int(v) for v in box))


def main():
    all_cards = cards()
    references = np.stack([patch(Image.open(ROOT / c["file"])) for c in all_cards])
    sets = sorted(manifest("collection_examples"), key=lambda r: r["id"])

    crops, labels = [], []
    for set_index, record in enumerate(sets):
        for slot, crop in enumerate(slots(ROOT / record["file"])):
            crops.append(patch(crop))
            labels.append((set_index, slot, record["id"]))

    scores = np.stack(crops) @ references.T
    rows, columns = linear_sum_assignment(-scores)
    result = {}
    for row, column in zip(rows, columns):
        set_index, slot, set_id = labels[row]
        runner_up = np.partition(scores[row], -2)[-2]
        result[all_cards[column]["id"]] = {
            "set_index": set_index, "set_id": set_id, "slot": slot,
            "score": round(float(scores[row, column]), 4),
            "margin": round(float(scores[row, column] - runner_up), 4),
        }
    save_json(ANALYSIS / "set_map.json", result)

    values = np.array([v["score"] for v in result.values()])
    print(f"matched {len(result)} slots; score min={values.min():.3f} median={np.median(values):.3f}")
    print("weakest:", sorted(result.values(), key=lambda v: v["score"])[:5])


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()  # --help only; the script takes no options
    main()
