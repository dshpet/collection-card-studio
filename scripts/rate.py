"""Fill the universal forms with independent vision raters. Finished cards and sets are skipped."""

import argparse
import base64
import json
import subprocess
import sys
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from common import ANALYSIS, ROOT, cards, load_json, manifest, save_json
from form import CARD_FORM, SET_FORM, card_schema, guide, set_schema

CATEGORIES = """art_category uses the art guide:
1 = simple object floating in the air; plain, gradient or simple pattern background.
2 = simple object standing on a surface; plain or simple pattern vertical background.
3 = object on a realistic surface with volume; simple vertical background behind it.
4 = object set into a realistic environment, still central.
5 = a scene with one or two characters acting out a small story."""

CARD_PROMPT = """You are a senior game art director. Fill the form for this mobile-game collection card.
Judge only what is visible. Use the scales evenly: 3 is typical for stylised mobile-game art.
{categories}
surface_kind: plain_colored_surface is a simple colored ledge; real_material_surface shows wood, stone, sand or grass.
{fields}"""


def card_prompt(sections):
    fields = guide({name: CARD_FORM[name] for name in sections})
    return CARD_PROMPT.format(categories=CATEGORIES, fields=fields)


SET_PROMPT = f"""You are a senior game producer. This screenshot shows one ten-card set from a collection.
List the ten cards in reading order with slot 0-9, printed name, and whether the frame is gold. Then fill the form for the set as a whole.
{guide(SET_FORM)}"""


def image_list(image):
    return [image] if isinstance(image, (str, Path)) else list(image or [])


def ask_codex(prompt, image, schema, timeout=600, effort="low"):
    attachments = [flag for path in image_list(image) for flag in ("-i", str(path))]
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        (folder / "schema.json").write_text(json.dumps(schema))
        command = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "--ignore-user-config",
                   "-m", "gpt-6.1-sol", "-c", f'model_reasoning_effort="{effort}"', "-s", "read-only",
                   "-C", str(folder), "--output-schema", str(folder / "schema.json"),
                   "-o", str(folder / "out.json"), *attachments, "--", prompt]
        done = subprocess.run(command, capture_output=True, text=True, timeout=timeout,
                              stdin=subprocess.DEVNULL)
        if done.returncode:
            raise RuntimeError(done.stderr[-400:])
        return json.loads((folder / "out.json").read_text())


def ask_claude(prompt, image, schema, model="claude-sonnet-5-5"):
    images = image_list(image)
    folders = sorted({str(Path(path).parent) for path in images})
    tools = ["--allowedTools", "Read", "--add-dir", *folders] if images else ["--tools", ""]
    listing = ", ".join(map(str, images))
    request = f"Read every one of these images, in order, then answer: {listing}\n{prompt}" if images else prompt
    command = ["claude", "-p", "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
               "--model", model, "--output-format", "json",
               "--json-schema", json.dumps(schema), *tools, "--", request]
    with tempfile.TemporaryDirectory() as folder:
        done = subprocess.run(command, capture_output=True, text=True, timeout=1200,
                              stdin=subprocess.DEVNULL, cwd=folder)
    if done.returncode:
        raise RuntimeError((done.stdout or done.stderr)[-400:])
    return json.loads(done.stdout)["structured_output"]


def ask_ollama(model, prompt, image, schema):
    payload = {"model": model, "stream": False, "format": schema, "think": False,
               "options": {"temperature": 0, "num_ctx": 16384},
               "messages": [{"role": "user", "content": prompt,
                             "images": [base64.b64encode(Path(image).read_bytes()).decode()]}]}
    request = urllib.request.Request("http://127.0.0.1:11434/api/chat", json.dumps(payload).encode(),
                                     {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=900) as response:
        return json.loads(json.load(response)["message"]["content"])


def run_one(rater, prompt, image, schema, out):
    """Ask one rater and merge the answer into its record, so new form sections fill in later."""
    for attempt in (1, 2):
        try:
            if rater == "codex":
                result = ask_codex(prompt, image, schema)
            elif rater == "claude":
                result = ask_claude(prompt, image, schema)
            else:
                result = ask_ollama(rater, prompt, image, schema)
            save_json(out, {**(load_json(out) if out.exists() else {}), **result})
            return "ok"
        except Exception as error:
            print(f"{out.stem} attempt {attempt}: {type(error).__name__} {str(error)[:160]}",
                  file=sys.stderr, flush=True)
    return "failed"


def card_job(rater, record, folder):
    out = folder / f"{record['id']}.json"
    done = load_json(out) if out.exists() else {}
    missing = [section for section in CARD_FORM if section not in done]
    if not missing:
        return None
    return rater, card_prompt(missing), ROOT / record["file"], card_schema(missing), out


def shrunk(record, folder):
    """Set screenshots are huge; 2000 px keeps the labels readable."""
    path = Path(folder) / f"{record['id']}.png"
    image = Image.open(ROOT / record["file"]).convert("RGB")
    image.thumbnail((2000, 2000))
    image.save(path)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=("cards", "sets"))
    parser.add_argument("--rater", default="codex", help="codex, claude or an Ollama model tag")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    name = args.rater.split(":")[0]
    folder = ANALYSIS / "ratings" / name
    records = cards() if args.target == "cards" else manifest("collection_examples")
    records = records[:args.limit]

    with tempfile.TemporaryDirectory() as scratch, ThreadPoolExecutor(args.workers) as pool:
        if args.target == "cards":
            jobs = [job for job in (card_job(args.rater, r, folder) for r in records) if job]
        else:
            done = ANALYSIS / "ratings" / f"sets_{name}"
            jobs = [(args.rater, SET_PROMPT, shrunk(r, scratch), set_schema(), done / f"{r['id']}.json")
                    for r in records if not (done / f"{r['id']}.json").exists()]
        results = list(pool.map(lambda job: run_one(*job), jobs))
    print({state: results.count(state) for state in set(results)})


if __name__ == "__main__":
    main()
