"""Fill the universal forms with independent vision raters. Finished records are skipped."""

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

from common import ANALYSIS, ROOT, cards, manifest, save_json
from form import CARD_FORM, SET_FORM, card_schema, guide, set_schema

CATEGORIES = """art_category uses the art guide:
1 = simple object floating in the air; plain, gradient or simple pattern background.
2 = simple object standing on a surface; plain or simple pattern vertical background.
3 = object on a realistic surface with volume; simple vertical background behind it.
4 = object set into a realistic environment, still central.
5 = a scene with one or two characters acting out a small story."""

CARD_PROMPT = f"""You are a senior game art director. Fill the form for this mobile-game collection card.
Judge only what is visible. Use the scales evenly: 3 is typical for stylised mobile-game art.
subject_box is the tight box around the main subject, with values from 0 to 1 and the origin at top left.
{CATEGORIES}
{guide(CARD_FORM)}"""

SET_PROMPT = f"""You are a senior game producer. This screenshot shows one ten-card set from a collection.
List the ten cards in reading order with slot 0-9, printed name, the number of stars above the card,
and whether the frame is gold. Then fill the form for the set as a whole.
{guide(SET_FORM)}"""


def ask_codex(prompt, image, schema):
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        (folder / "schema.json").write_text(json.dumps(schema))
        command = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "--ignore-user-config",
                   "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="low"', "-s", "read-only",
                   "-C", str(folder), "--output-schema", str(folder / "schema.json"),
                   "-o", str(folder / "out.json"), "-i", str(image), "--", prompt]
        done = subprocess.run(command, capture_output=True, text=True, timeout=600)
        if done.returncode:
            raise RuntimeError(done.stderr[-400:])
        return json.loads((folder / "out.json").read_text())


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
    if out.exists():
        return "skip"
    for attempt in (1, 2):
        try:
            if rater == "codex":
                result = ask_codex(prompt, image, schema)
            else:
                result = ask_ollama(rater, prompt, image, schema)
            save_json(out, result)
            return "ok"
        except Exception as error:
            print(f"{out.stem} attempt {attempt}: {type(error).__name__} {str(error)[:160]}",
                  file=sys.stderr, flush=True)
    return "failed"


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
    parser.add_argument("--rater", default="codex", help="codex or an Ollama model tag")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    name = "codex" if args.rater == "codex" else args.rater.split(":")[0]
    folder = ANALYSIS / "ratings" / name
    records = cards() if args.target == "cards" else manifest("collection_examples")
    records = records[:args.limit]

    with tempfile.TemporaryDirectory() as scratch, ThreadPoolExecutor(args.workers) as pool:
        if args.target == "cards":
            jobs = [(args.rater, CARD_PROMPT, ROOT / r["file"], card_schema(),
                     folder / f"{r['id']}.json") for r in records]
        else:
            jobs = [(args.rater, SET_PROMPT, shrunk(r, scratch), set_schema(),
                     ANALYSIS / "ratings" / f"sets_{name}" / f"{r['id']}.json") for r in records]
        results = list(pool.map(lambda job: run_one(*job), jobs))
    print({state: results.count(state) for state in set(results)})


if __name__ == "__main__":
    main()
