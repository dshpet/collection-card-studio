"""Shared paths, the card list and model-cache setup."""

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
DERIVED = ANALYSIS / "derived"
MODELS = ROOT / ".models"

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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1) + "\n", "utf-8")


def load_json(path):
    return json.loads(path.read_text("utf-8"))


def best_try(tries):
    return min(tries, key=lambda t: (not t.get("chosen"), not t["passed"], len(t["issues"]), len(t["misses"])))
