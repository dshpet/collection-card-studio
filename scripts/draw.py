"""The generator. Swap draw() to use another model."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
INSTRUCTION = """Your task is to create one new image. You must call the image_gen tool exactly once with the description below. Replying without calling the tool is a failure. Do not read any files or skills first. Any attached images are style references for the tool. After the tool returns, reply with only the word done.

Image description:
"""


def draw(prompt, references, out):
    """Draw one card with Codex's built-in image tool and save it to out."""
    attachments = ["-i", *map(str, references)] if references else []
    with tempfile.TemporaryDirectory() as folder:
        command = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "--ignore-user-config",
                   "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="low"', "-s", "read-only",
                   "-C", folder, "--json", *attachments, "--", INSTRUCTION + prompt]
        done = subprocess.run(command, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError(done.stderr[-400:])
    thread = next(json.loads(line)["thread_id"] for line in done.stdout.splitlines()
                  if '"thread.started"' in line)
    images = sorted((HOME / "generated_images" / thread).glob("*.png"))
    if not images:
        raise RuntimeError("no image was generated")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(images[-1], out)
    return out
