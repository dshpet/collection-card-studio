"""Shared paths, models, the card list and small helpers."""

import json
import os
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
DERIVED = ANALYSIS / "derived"
MODELS = ROOT / ".models"
SIZE = (430, 480)  # a reference card

# The models behind the CLIs. draw.py holds the generator itself.
DRAWER = "gpt-6.1-sol"  # Codex: draws, edits and rates blind
PLANNER = "claude-sonnet-5-5"  # plans sets, flags sensitive cards
JUDGE = "claude-opus-5-5"  # models in Blender, reviews, judges pairs

os.environ.setdefault("HF_HOME", str(MODELS / "hf"))
os.environ.setdefault("TORCH_HOME", str(MODELS / "torch"))


def hf_key():
    """The Hugging Face key from .env, or None. It is never printed, and only gated downloads get it."""
    env = ROOT / ".env"
    match = env.exists() and re.search(r"^\s*HUGGING_FACE_API_KEY\s*=\s*(.+?)\s*$", env.read_text(), re.M)
    return match.group(1).strip("\"'") if match else None


def load_token():
    """Expose the key to the hub client through the environment. Only for scripts that start no other program."""
    key = hf_key()
    if key:
        os.environ.setdefault("HF_TOKEN", key)


def manifest(group):
    records = json.loads((ROOT / "sources/image_manifest.json").read_text("utf-8"))
    return [r for r in records if r["group"] == group]


def cards():
    return manifest("card_examples")


def save_json(path, value):
    """Write through a temporary file, so a crash mid-write never leaves a run's state half written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=1) + "\n", "utf-8")
    os.replace(temporary, path)


def load_json(path):
    return json.loads(path.read_text("utf-8"))


def text():
    return {"type": "string"}


def strict(properties):
    """A JSON schema object that requires every property and allows no other."""
    return {"type": "object", "additionalProperties": False, "properties": properties, "required": list(properties)}


def best_try(tries):
    return min(tries, key=lambda t: (not t.get("chosen"), not t["passed"], len(t["issues"]), len(t["misses"])))


def run_name(run):
    """A run's folder under runs/, nested ones included."""
    return str(run.relative_to(ROOT / "runs")) if run.is_relative_to(ROOT / "runs") else run.name


def contact_sheet(paths, out, columns=5):
    tile = (258, 288)
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile[0], rows * tile[1]), "white")
    for index, path in enumerate(paths):
        sheet.paste(Image.open(path).convert("RGB").resize(tile), (index % columns * tile[0], index // columns * tile[1]))
    sheet.save(out)


# Flat objects lying on a surface that fills the card, seen from above. Raters labelled most of them stripes (the
# planks), so they were attached as references to upright stripes cards, such as a rocket.
SURFACE_FROM_ABOVE = {"Fruit Plate", "Tennis", "Binoculars", "Travel Book", "Map"}


def pattern(card):
    """A real card's backdrop pattern: the raters' label, corrected for the cards seen from above."""
    return "surface_from_above" if card["name"] in SURFACE_FROM_ABOVE else card["form"]["backdrop"]["pattern"]
