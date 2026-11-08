"""Embed every card with each model, for the whole card and, with masks, subject and background."""

import argparse
import logging

from common import ANALYSIS, DERIVED, ROOT, cards, hf_key  # first: sets the model cache

import numpy as np
import torch
from PIL import Image, ImageOps
from safetensors.torch import load_file
from transformers import AutoImageProcessor, AutoModel

MODELS = {
    "dinov2": "facebook/dinov2-with-registers-giant",
    "siglip2": "google/siglip2-giant-opt-patch16-384",
    "csd": "yuxi-liu-wired/CSD",
    "dinov3": "facebook/dinov3-vitl16-pretrain-lvd1689m",  # gated: needs access on Hugging Face
}
GATED = {MODELS["dinov3"]}
NEUTRAL = (128, 128, 128)


def square(image, size):
    """Pad instead of center-cropping, so nothing at the card edge is lost."""
    return ImageOps.pad(image.convert("RGB"), (size, size), Image.BICUBIC, color=NEUTRAL)


def views(record, derived=DERIVED):
    """The whole card, and with a mask, the subject and the background alone on neutral grey."""
    image = Image.open(ROOT / record["file"]).convert("RGB")
    yield "whole", image
    mask_path = derived / "masks" / f"{record['id']}.png"
    if mask_path.exists():
        mask = Image.open(mask_path).convert("L")
        grey = Image.new("RGB", image.size, NEUTRAL)
        yield "subject", Image.composite(image, grey, mask)
        yield "background", Image.composite(grey, image, mask)


def load_hf(repo, dtype=torch.float16):
    token = hf_key() if repo in GATED else None  # passed to the download alone, never through the environment
    processor = AutoImageProcessor.from_pretrained(repo, token=token)
    model = AutoModel.from_pretrained(repo, dtype=dtype, token=token).cuda().eval()
    size = processor.size.get("height") or processor.size.get("shortest_edge")
    mean, std = torch.tensor(processor.image_mean), torch.tensor(processor.image_std)

    def encode(batch):
        tensor = torch.stack([torch.from_numpy(np.asarray(square(b, size)).copy()) for b in batch])
        tensor = (tensor.permute(0, 3, 1, 2).float() / 255 - mean[..., None, None]) / std[..., None, None]
        tensor = tensor.cuda().to(dtype)
        if hasattr(model, "get_image_features"):
            output = model.get_image_features(pixel_values=tensor)
            return getattr(output, "pooler_output", output)
        return model(pixel_values=tensor).last_hidden_state[:, 0]

    return encode


def load_csd(repo):
    """CSD is a CLIP ViT-L with a style head; its published weights load into open_clip."""
    import open_clip
    from huggingface_hub import hf_hub_download

    logging.disable(logging.WARNING)  # open_clip warns that the bare model is random; CSD's weights load next
    try:
        clip = open_clip.create_model("ViT-L-14", pretrained=None, force_quick_gelu=True)
    finally:
        logging.disable(logging.NOTSET)
    weights = load_file(hf_hub_download(repo, "model.safetensors"))
    visual = {k.removeprefix("backbone."): v for k, v in weights.items() if k.startswith("backbone.")}
    visual = {k: v for k, v in visual.items() if k != "proj"}
    clip.visual.proj = None
    clip.visual.load_state_dict(visual, strict=True)
    head = weights["last_layer_style"].float().cuda()
    visual_model = clip.visual.cuda().float().eval()
    mean = torch.tensor((0.48145466, 0.4578275, 0.40821073))
    std = torch.tensor((0.26862954, 0.26130258, 0.27577711))

    def encode(batch):
        tensor = torch.stack([torch.from_numpy(np.asarray(square(b, 224)).copy()) for b in batch])
        tensor = (tensor.permute(0, 3, 1, 2).float() / 255 - mean[..., None, None]) / std[..., None, None]
        features = visual_model(tensor.cuda())
        features = features[0] if isinstance(features, tuple) else features
        return features @ head

    return encode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["dinov2", "siglip2", "csd"])
    parser.add_argument("--batch", type=int, default=8)
    args = parser.parse_args()

    records = cards()
    output = ANALYSIS / "embeddings"
    output.mkdir(parents=True, exist_ok=True)
    by_view = {}
    for record in records:
        for view, image in views(record):
            by_view.setdefault(view, []).append(image)
    for name in args.models:
        dtype = torch.float32 if name == "dinov3" else torch.float16  # DINOv3 returns NaNs at half precision
        encode = load_csd(MODELS[name]) if name == "csd" else load_hf(MODELS[name], dtype)
        for view, images in by_view.items():
            if len(images) != len(records):
                continue
            chunks = []
            with torch.inference_mode():
                for start in range(0, len(images), args.batch):
                    vectors = encode(images[start:start + args.batch]).float()
                    chunks.append(torch.nn.functional.normalize(vectors, dim=-1).cpu().numpy())
            np.save(output / f"{name}_{view}.npy", np.concatenate(chunks).astype(np.float32))
            print(name, view, chunks[0].shape[1], flush=True)
        del encode
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
