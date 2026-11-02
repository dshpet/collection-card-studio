"""Model estimates per card: subject mask, depth, attention, normals and shading, in analysis/derived.

BiRefNet, Depth Anything 3 and DeepGaze run external code, pinned here to the reviewed revisions.
None of these models needs the Hugging Face key. See README.md for the two source checkouts.
"""

import argparse
import sys
from unittest.mock import MagicMock
from urllib.request import urlretrieve

from common import DERIVED, MODELS, ROOT, cards  # first: sets the model cache

import numpy as np
import torch
from PIL import Image

BIREFNET_REVISION = "e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4"
DEPTH_REVISION = "f465978e618db8cc79c83b8bbf24964857db1875"
CENTER_BIAS = "https://github.com/matthias-k/DeepGaze/releases/download/v1.0.0/centerbias_mit1003.npy"


def run_deform_conv_on_cpu():
    """The CPU torchvision wheel has no GPU kernel for this op, which BiRefNet needs."""
    import torchvision.ops as ops

    original = ops.deform_conv2d

    def wrapped(input, offset, weight, bias=None, mask=None, **options):
        move = lambda tensor: None if tensor is None else tensor.cpu()
        result = original(move(input), move(offset), move(weight), move(bias), mask=move(mask), **options)
        return result.to(input.device)

    ops.deform_conv2d = wrapped


def write_masks(records, device, folder=DERIVED / "masks"):
    from torchvision import transforms
    from transformers import AutoModelForImageSegmentation

    run_deform_conv_on_cpu()
    model = AutoModelForImageSegmentation.from_pretrained(
        "ZhengPeng7/BiRefNet", revision=BIREFNET_REVISION, code_revision=BIREFNET_REVISION,
        trust_remote_code=True).float().to(device).eval()
    prepare = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(),
                                  transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
    folder.mkdir(parents=True, exist_ok=True)
    for record in records:
        out = folder / f"{record['id']}.png"
        if out.exists():
            continue
        image = Image.open(ROOT / record["file"]).convert("RGB")
        with torch.inference_mode():
            mask = model(prepare(image)[None].to(device))[-1].sigmoid()[0, 0].cpu().numpy()
        Image.fromarray((mask * 255).astype(np.uint8)).resize(image.size).save(out)
    del model
    torch.cuda.empty_cache()


def write_depth(records, device):
    """Depth Anything 3. Its export and pose modules need a 3D stack that depth does not use."""
    sys.path.insert(0, str(MODELS / "src/da3/src"))
    sys.modules["depth_anything_3.utils.export"] = MagicMock()
    sys.modules["depth_anything_3.utils.pose_align"] = MagicMock()
    from depth_anything_3.api import DepthAnything3

    model = DepthAnything3.from_pretrained("depth-anything/DA3MONO-LARGE", revision=DEPTH_REVISION)
    model = model.to(device).eval()
    folder = DERIVED / "depth"
    folder.mkdir(parents=True, exist_ok=True)
    for record in records:
        out = folder / f"{record['id']}.png"
        if out.exists():
            continue
        image = Image.open(ROOT / record["file"]).convert("RGB")
        depth = model.inference([image]).depth[0]
        near = 1 / np.maximum(depth, 1e-6)  # near is bright
        low, high = np.percentile(near, [0.5, 99.5])
        near = np.clip((near - low) / (high - low + 1e-9), 0, 1)
        Image.fromarray((near * 65535).astype(np.uint16)).resize(image.size, Image.BICUBIC).save(out)


def write_attention(records, device):
    """DeepGaze IIE: where people are predicted to look."""
    from scipy.ndimage import zoom
    from scipy.special import logsumexp

    sys.path.insert(0, str(MODELS / "src/deepgaze"))
    sys.modules.setdefault("clip", MagicMock())  # only other DeepGaze models need it
    import deepgaze_pytorch

    bias_path = MODELS / "centerbias_mit1003.npy"
    if not bias_path.exists():
        urlretrieve(CENTER_BIAS, bias_path)
    template = np.load(bias_path)
    model = deepgaze_pytorch.DeepGazeIIE(pretrained=True).to(device).eval()
    folder = DERIVED / "attention"
    folder.mkdir(parents=True, exist_ok=True)
    for record in records:
        out = folder / f"{record['id']}.npy"
        if out.exists():
            continue
        image = np.asarray(Image.open(ROOT / record["file"]).convert("RGB"), dtype=np.float32)
        height, width = image.shape[:2]
        bias = zoom(template, (height / template.shape[0], width / template.shape[1]), order=0, mode="nearest")
        bias = bias - logsumexp(bias)
        with torch.inference_mode():
            density = model(torch.tensor(image.transpose(2, 0, 1)[None]).to(device),
                            torch.tensor(bias[None], dtype=torch.float32).to(device))
        density = torch.exp(density)[0, 0].cpu().numpy()
        np.save(out, density.astype(np.float32))
        Image.fromarray((density / density.max() * 255).astype(np.uint8)).save(out.with_suffix(".png"))


def write_marigold(records, device):
    from diffusers import MarigoldIntrinsicsPipeline, MarigoldNormalsPipeline

    def pipeline(kind, repo):
        return kind.from_pretrained(repo, variant="fp16", torch_dtype=torch.float16).to(device)

    normals = pipeline(MarigoldNormalsPipeline, "prs-eth/marigold-normals-v1-1")
    for name in ("normals", "shading"):
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
        Image.fromarray((np.clip(result[1], 0, 1) * 255).astype(np.uint8)).save(shading_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("steps", nargs="+", choices=("masks", "depth", "attention", "marigold"))
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    records = cards()[:args.limit]
    steps = {"masks": write_masks, "depth": write_depth, "attention": write_attention,
             "marigold": write_marigold}
    for step in args.steps:
        steps[step](records, args.device)
        print("done", step, flush=True)


if __name__ == "__main__":
    main()
