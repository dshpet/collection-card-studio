"""Model estimates per card: subject mask, depth, normals and shading, saved to analysis/derived."""

import argparse

from common import ANALYSIS, DERIVED, ROOT, cards, load_json, load_token  # first: sets the model cache

import numpy as np
import torch
from PIL import Image
from skimage import filters, measure, morphology

PAD = 0.015


def rated_boxes(record, size):
    """Every rater's box in pixels. Some raters answer on a 0-1000 scale."""
    boxes = []
    for rater in ("codex", "claude", "gemma4", "qwen3.8"):
        path = ANALYSIS / "ratings" / rater / f"{record['id']}.json"
        if path.exists():
            box = load_json(path)["subject_box"]
            values = [box[side] for side in ("x0", "y0", "x1", "y1")]
            if max(values) > 1:
                values = [v / 1000 for v in values]
            width, height = size
            boxes.append([max(0, (values[0] - PAD) * width), max(0, (values[1] - PAD) * height),
                          min(width, (values[2] + PAD) * width), min(height, (values[3] + PAD) * height)])
    return boxes


def depth_box(depth):
    """The box around the largest region standing out from the background in depth."""
    regions = measure.label(depth > filters.threshold_otsu(depth))
    largest = max(measure.regionprops(regions), key=lambda region: region.area)
    y0, x0, y1, x1 = largest.bbox
    return [float(x0), float(y0), float(x1), float(y1)]


def union(first, second):
    return [min(first[0], second[0]), min(first[1], second[1]),
            max(first[2], second[2]), max(first[3], second[3])]


def separation(mask, depth):
    """How far the mask stands out in depth from the ring around it. Rejects bad masks."""
    share = mask.mean()
    if not 0.03 < share < 0.85:
        return -1.0
    ring = morphology.dilation(mask, morphology.disk(10)) & ~mask
    if not ring.any():
        return -1.0
    frame_contact = np.concatenate((mask[0], mask[-1], mask[:, 0], mask[:, -1])).mean()
    return float(depth[mask].mean() - depth[ring].mean()) - 0.6 * float(frame_contact)


def clean(mask):
    """Drop specks and fill small holes."""
    labels = measure.label(mask)
    keep = [r.label for r in measure.regionprops(labels) if r.area >= 0.03 * mask.sum()]
    return morphology.remove_small_holes(np.isin(labels, keep), max_size=int(0.08 * mask.size))


def write_masks(records, device):
    from transformers import Sam2Model, Sam2Processor

    repo = "facebook/sam2.1-hiera-large"
    processor = Sam2Processor.from_pretrained(repo)
    model = Sam2Model.from_pretrained(repo).to(device).eval()
    folder = DERIVED / "masks"
    folder.mkdir(parents=True, exist_ok=True)
    for record in records:
        out = folder / f"{record['id']}.png"
        image = Image.open(ROOT / record["file"]).convert("RGB")
        rated = rated_boxes(record, image.size)
        if out.exists() or not rated:
            continue
        depth = np.asarray(Image.open(DERIVED / "depth" / f"{record['id']}.png"), dtype=np.float32) / 65535
        from_depth = depth_box(depth)
        boxes = rated + [from_depth] + [union(box, from_depth) for box in rated]
        boxes = [box for box in boxes if box[2] > box[0] and box[3] > box[1]]
        inputs = processor(images=image, input_boxes=[boxes], return_tensors="pt").to(device)
        with torch.inference_mode():
            output = model(**inputs, multimask_output=True)
        masks = processor.post_process_masks(output.pred_masks.cpu(), inputs["original_sizes"])[0].numpy() > 0
        confidence = output.iou_scores.squeeze(0).cpu().numpy()
        options = [(masks[b, m], 0.25 * confidence[b, m])
                   for b in range(masks.shape[0]) for m in range(masks.shape[1])]
        options += [(~mask, 0.0) for mask, _ in options]  # SAM sometimes outlines the background
        options.append((depth > filters.threshold_otsu(depth), 0.0))
        best = max(options, key=lambda option: separation(option[0], depth) + option[1])[0]
        Image.fromarray((clean(best) * 255).astype(np.uint8)).save(out)


def write_depth(records, device):
    from transformers import AutoImageProcessor, AutoModelForDepthEstimation

    repo = "depth-anything/Depth-Anything-V2-Small-hf"
    processor = AutoImageProcessor.from_pretrained(repo)
    model = AutoModelForDepthEstimation.from_pretrained(repo).to(device).eval()
    folder = DERIVED / "depth"
    folder.mkdir(parents=True, exist_ok=True)
    for record in records:
        out = folder / f"{record['id']}.png"
        if out.exists():
            continue
        image = Image.open(ROOT / record["file"]).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.inference_mode():
            depth = model(**inputs).predicted_depth
        depth = torch.nn.functional.interpolate(depth[None], image.size[::-1], mode="bicubic")[0, 0]
        depth = depth.cpu().numpy()
        depth = (depth - depth.min()) / (np.ptp(depth) + 1e-9)
        Image.fromarray((depth * 65535).astype(np.uint16)).save(out)


def write_marigold(records, device):
    from diffusers import MarigoldIntrinsicsPipeline, MarigoldNormalsPipeline

    def pipeline(kind, repo):
        return kind.from_pretrained(repo, variant="fp16", torch_dtype=torch.float16).to(device)

    normals = pipeline(MarigoldNormalsPipeline, "prs-eth/marigold-normals-v1-1")
    for name in ("normals", "shading", "albedo"):
        (DERIVED / name).mkdir(parents=True, exist_ok=True)
    for record in records:
        out = DERIVED / "normals" / f"{record['id']}.npy"
        if not out.exists():
            image = Image.open(ROOT / record["file"]).convert("RGB")
            result = normals(image, num_inference_steps=4, ensemble_size=1, output_type="np").prediction
            np.save(out, result[0].astype(np.float16))
            Image.fromarray(((result[0] + 1) * 127.5).astype(np.uint8)).save(out.with_suffix(".png"))
    del normals
    torch.cuda.empty_cache()

    intrinsics = pipeline(MarigoldIntrinsicsPipeline, "prs-eth/marigold-iid-lighting-v1-1")
    for record in records:
        shading_path = DERIVED / "shading" / f"{record['id']}.png"
        if shading_path.exists():
            continue
        image = Image.open(ROOT / record["file"]).convert("RGB")
        result = intrinsics(image, num_inference_steps=4, ensemble_size=1, output_type="np").prediction
        albedo, shading = result[0], result[1]
        Image.fromarray((np.clip(shading, 0, 1) * 255).astype(np.uint8)).save(shading_path)
        Image.fromarray((np.clip(albedo, 0, 1) * 255).astype(np.uint8)).save(
            DERIVED / "albedo" / f"{record['id']}.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("steps", nargs="+", choices=("masks", "depth", "marigold"))
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    load_token()
    records = cards()[:args.limit]
    steps = {"masks": write_masks, "depth": write_depth, "marigold": write_marigold}
    for step in args.steps:
        steps[step](records, args.device)
        print("done", step, flush=True)


if __name__ == "__main__":
    main()
