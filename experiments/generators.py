"""Does another image model draw closer to the real cards than Codex? A bake-off on the forty twins.

Each twin is a real card redrawn from a text brief with that card hidden (runs/twins40). The codex arm is the final-style
draw made then; every other arm gets the same prompt and the same three reference cards. Closeness is CSD against the
twin's own real card and the art director's pairwise pick with that card shown, the two measures that tracked the
producer (analysis/STYLE_GAPS.md), as in experiments/search_trial.py.

    generators.py draw --arm qwen          Qwen-Image-2.1 on this GPU, open weights -> runs/generators/tries/
    generators.py draw --arm nano --limit 12   Nano Banana Pro through the Antigravity CLI (agy)
    generators.py measure --arm qwen       against the codex arm -> runs/generators/result_qwen.json

The nano arm is a system, not a model: agy's image subagent rewrites the prompt and may draw several times before it
answers. The prompts it sent are kept in runs/generators/prompts_nano.json.
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import gc
import json
import os
import shutil
import subprocess
import tempfile
import time

from common import ROOT, SIZE, load_json, save_json

import numpy as np
from PIL import Image

RUN = ROOT / "runs" / "generators"
TWINS = ROOT / "runs" / "twins40"
QWEN = ("Qwen/Qwen-Image-2.1", "d26bb61231c349cf6b7896fa83353113880e1ba3")  # Qwen Research License: evaluation only
# Side of the working resolution. At 1024 the attention runs over about 16k tokens with three references and turns the
# latents to NaN on this ROCm card, whatever the attention backend; at 640 both backends are clean. Cards are 430x480.
RESOLUTION = 640


def twins():
    return load_json(TWINS / "briefs.json")


def prompt(twin):
    return (TWINS / "final" / "prompts" / f"{twin['id']}_1.txt").read_text("utf-8")


def references(twin):
    return [Image.open(ROOT / f"materials/card_examples/{i}.png").convert("RGB") for i in twin["references"]]


def draw_qwen(limit):
    """In three passes, so the 33 GB of weights never sit in memory at once: the text encoder reads every prompt with
    its references, the transformer draws latents from those encodings, and the VAE decodes them."""
    import torch
    from diffusers import QwenImage21Pipeline
    from diffusers.pipelines.qwenimage21.pipeline_qwenimage21 import calculate_dimensions

    os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
    todo = [t for t in twins()[:limit] if not (RUN / "tries" / f"{t['id']}-qwen_1.png").exists()]
    if not todo:
        return
    reader = QwenImage21Pipeline.from_pretrained(QWEN[0], revision=QWEN[1], transformer=None, vae=None,
                                                 dtype=torch.bfloat16)
    reader.text_encoder.to("cuda")
    encoded = {}
    with torch.inference_mode():
        for twin in todo:
            images = []
            for image in references(twin):  # as the pipeline resizes its condition images
                width, height, _ = calculate_dimensions(RESOLUTION ** 2, image.size[0] / image.size[1])
                images.append(reader.image_processor.resize(image.convert("RGBA"), width=width, height=height))
            encoded[twin["id"]] = [t.cpu() if t is not None else None
                                   for t in reader.encode_prompt(prompt(twin), image=images, device="cuda")]
    del reader
    gc.collect()
    torch.cuda.empty_cache()

    pipe = QwenImage21Pipeline.from_pretrained(QWEN[0], revision=QWEN[1], text_encoder=None, dtype=torch.bfloat16)
    pipe.to("cuda")
    torch.backends.cuda.enable_flash_sdp(False)  # the memory-efficient kernel was checked clean at this resolution
    timing = load_json(RUN / "timing_qwen.json") if (RUN / "timing_qwen.json").exists() else {}
    saved = RUN / "latents"  # a rerun after a failed decode skips the drawing
    saved.mkdir(parents=True, exist_ok=True)
    for twin in todo:
        if (saved / f"{twin['id']}.pt").exists():
            continue
        pipe.encode_prompt = lambda **_: [t.to("cuda") if t is not None else None for t in encoded[twin["id"]]]
        start = time.time()
        drawn = pipe(prompt=prompt(twin), image=references(twin), num_inference_steps=40, output_type="latent",
                     output_resolution=RESOLUTION, generator=torch.Generator("cpu").manual_seed(1)).images.cpu()
        if torch.isnan(drawn).any():
            raise RuntimeError(f"{twin['id']}: the latents are NaN")
        torch.save(drawn, saved / f"{twin['id']}.pt")
        timing[twin["id"]] = round(time.time() - start, 1)
        save_json(RUN / "timing_qwen.json", timing)
        print(twin["id"], timing[twin["id"]], "s", flush=True)
    del pipe
    gc.collect()
    torch.cuda.empty_cache()

    # The VAE decodes alone: beside the transformer, a 1-megapixel decode runs out of the card's 24 GB
    decoder = QwenImage21Pipeline.from_pretrained(QWEN[0], revision=QWEN[1], text_encoder=None, transformer=None,
                                                  dtype=torch.bfloat16)
    decoder.vae.to("cuda")
    width, height, _ = calculate_dimensions(RESOLUTION ** 2, SIZE[0] / SIZE[1])  # from the last reference, as the pipeline
    width, height = width // 32 * 32, height // 32 * 32
    config = decoder.vae.config
    mean = torch.tensor(config.latents_mean).view(1, config.z_dim, 1, 1, 1).to("cuda", torch.bfloat16)
    std = torch.tensor(config.latents_std).view(1, config.z_dim, 1, 1, 1).to("cuda", torch.bfloat16)
    with torch.inference_mode():
        for twin in todo:
            drawn = torch.load(saved / f"{twin['id']}.pt", weights_only=True).to("cuda")
            packed = decoder._unpack_latents(drawn, height, width, decoder.vae_scale_factor)
            decoded = decoder.vae.decode(packed.to(torch.bfloat16) * std + mean, return_dict=False)[0][:, :, 0]
            image = decoder.image_processor.postprocess(decoded, output_type="pil")[0]
            (RUN / "full").mkdir(parents=True, exist_ok=True)
            image.save(RUN / "full" / f"{twin['id']}-qwen_1.png")
            out = RUN / "tries" / f"{twin['id']}-qwen_1.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            image.convert("RGB").resize(SIZE, Image.LANCZOS).save(out)


def sent_prompts(conversation):
    """The generate_image calls agy's image subagent made, from its transcript."""
    brain = Path.home() / ".gemini" / "antigravity-cli" / "brain"
    calls = []
    for spec in (brain / conversation / ".system_generated" / "subagents").glob("*.json"):
        log = brain / load_json(spec)["conversationId"] / ".system_generated" / "logs" / "transcript_full.jsonl"
        for line in log.read_text("utf-8").splitlines():
            calls += [c["args"] for c in json.loads(line).get("tool_calls") or [] if c["name"] == "generate_image"]
    return calls


def draw_nano(limit):
    """Each twin in a fresh sandboxed workspace that holds only its prompt and references; no shell commands allowed."""
    sent_path = RUN / "prompts_nano.json"
    sent = load_json(sent_path) if sent_path.exists() else {}
    for twin in twins()[:limit]:
        out = RUN / "tries" / f"{twin['id']}-nano_1.png"
        if out.exists():
            continue
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / "prompt.txt").write_text(prompt(twin), "utf-8")
            for i, image in enumerate(references(twin), 1):
                image.save(folder / f"ref{i}.png")
            ask = ("Have the image tool draw exactly one image, once. image_paths: ref1.png, ref2.png, ref3.png in this "
                   "folder. prompt: the full text of prompt.txt in this folder, passed verbatim: do not rewrite, shorten "
                   "or add a single word, and do not draw again. Then reply with only the path of the image.")
            start = time.time()
            done = subprocess.run(["agy", "-p", ask, "--model", "gemini-3.8-flash-low", "--output-format", "json",
                                   "--sandbox", "--settings", '{"permissions":{"allow":[]},"allowNonWorkspaceAccess":false}'],
                                  cwd=folder, capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
        try:
            answer = json.loads(done.stdout)
            path = Path(answer["response"].strip().splitlines()[-1].strip())
            image = Image.open(path).convert("RGB")
        except Exception as error:
            print(twin["id"], "failed:", type(error).__name__, (done.stdout or done.stderr)[-300:], flush=True)
            continue
        (RUN / "full").mkdir(parents=True, exist_ok=True)
        image.save(RUN / "full" / f"{twin['id']}-nano_1.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        image.resize(SIZE, Image.LANCZOS).save(out)
        sent[twin["id"]] = {"seconds": round(time.time() - start), "calls": sent_prompts(answer["conversation_id"])}
        save_json(sent_path, sent)
        print(twin["id"], sent[twin["id"]]["seconds"], "s,", len(sent[twin["id"]]["calls"]), "draws", flush=True)


def codex_arm():
    """The final-style draws already made, copied in under this run's names so the judge sees both arms alike."""
    for twin in twins():
        out = RUN / "tries" / f"{twin['id']}-codex_1.png"
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(TWINS / "final" / "tries" / f"{twin['id']}_1.png", out)


def measure(arm):
    import torch
    from scipy.stats import binomtest, wilcoxon

    from common import contact_sheet
    from embed import MODELS, load_csd
    from review import judge_pairs

    codex_arm()
    done = [t for t in twins() if (RUN / "tries" / f"{t['id']}-{arm}_1.png").exists()]
    files = ([ROOT / f"materials/card_examples/{t['real']}.png" for t in done]
             + [RUN / "tries" / f"{t['id']}-{name}_1.png" for name in ("codex", arm) for t in done])
    encode = load_csd(MODELS["csd"])
    with torch.inference_mode():
        vectors = torch.cat([encode([Image.open(f).convert("RGB") for f in files[i:i + 8]]).float()
                             for i in range(0, len(files), 8)])
    vectors = torch.nn.functional.normalize(vectors, dim=-1).cpu().numpy()
    n = len(done)
    codex, other = np.sum(vectors[:n] * vectors[n:2 * n], axis=1), np.sum(vectors[:n] * vectors[2 * n:], axis=1)
    contests = [(t["id"], f"{t['id']}-codex_1", f"{t['id']}-{arm}_1", [t["real"]]) for t in done]
    wins = judge_pairs(RUN, f"codex_{arm}", contests)
    director = {name: sum(wins[f"{t['id']}-{name}_1"] > wins[f"{t['id']}-{rival}_1"] for t in done)
                for name, rival in (("codex", arm), (arm, "codex"))}
    decided = director["codex"] + director[arm]
    result = {"twins": n, "csd_codex": round(float(codex.mean()), 4), f"csd_{arm}": round(float(other.mean()), 4),
              f"{arm}_closer": int((other > codex).sum()), "wilcoxon_p": round(float(wilcoxon(other, codex).pvalue), 4),
              "director": director,
              "director_p": round(float(binomtest(director[arm], decided, 0.5).pvalue), 4) if decided else None,
              "by_twin": {t["id"]: [round(float(x), 3), round(float(y), 3)] for t, x, y in zip(done, codex, other)}}
    save_json(RUN / f"result_{arm}.json", result)
    (RUN / "sheets").mkdir(exist_ok=True)  # real cards in the top row: Playrix art, kept out of git
    shown = min(n, 12)  # one row each: real, codex, the arm
    contact_sheet(files[:shown] + files[n:n + shown] + files[2 * n:2 * n + shown], RUN / "sheets" / f"real_codex_{arm}.png",
                  shown)
    print({k: v for k, v in result.items() if k != "by_twin"})


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("draw", "measure"))
    parser.add_argument("--arm", choices=("qwen", "nano"), default="qwen")
    parser.add_argument("--limit", type=int, default=40, help="the first N twins")
    args = parser.parse_args()
    if args.mode == "measure":
        measure(args.arm)
    else:
        (draw_qwen if args.arm == "qwen" else draw_nano)(args.limit)


if __name__ == "__main__":
    main()
