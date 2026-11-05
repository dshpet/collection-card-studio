"""The generator. Swap draw() to use another model."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
INSTRUCTION = """Call the image_gen tool exactly once{images}. Pass the text between <prompt> and </prompt> as its prompt, verbatim: do not rewrite, shorten, translate or add a single word. Do not read any files or skills. After the tool returns, reply with only the word done.

<prompt>
{prompt}
</prompt>"""


def reached_tool(thread):
    """The prompt the image tool really received. Codex keeps it in the session log, which we then remove."""
    log = next((HOME / "sessions").rglob(f"*{thread}*.jsonl"))
    prompts = []
    with open(log, encoding="utf-8") as lines:
        for line in lines:
            item = json.loads(line).get("payload", {})
            item = item.get("item", {}) if isinstance(item, dict) else {}
            if item.get("type") == "Extension" and item.get("revisedPrompt"):
                prompts.append(item["revisedPrompt"])
    log.unlink()
    return prompts[-1] if prompts else None


def draw(prompt, references, out, transparent=False):
    """Draw one card with Codex's image tool and save it to out. The last reference is the most recent image.

    transparent: a figure alone on a transparent ground, for pasting onto a card."""
    if len(references) > 5:
        raise ValueError("Codex's image tool takes at most 5 images")
    attachments = [flag for path in references for flag in ("-i", str(path))]
    options = ([f"num_last_images_to_include set to {len(references)}"] if references else []) + (
        ["transparent_background set to true"] if transparent else [])
    images = f", with {' and '.join(options)}" if options else ""
    request = INSTRUCTION.format(images=images, prompt=prompt)
    with tempfile.TemporaryDirectory() as folder:
        command = ["codex", "exec", "--skip-git-repo-check", "--ignore-user-config",
                   "-m", "gpt-6.1-sol", "-c", 'model_reasoning_effort="low"', "-s", "read-only",
                   "-C", folder, "--json", *attachments, "--", request]
        done = subprocess.run(command, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError(done.stderr[-400:])
    thread = next(json.loads(line)["thread_id"] for line in done.stdout.splitlines()
                  if '"thread.started"' in line)
    sent = reached_tool(thread)
    images = sorted((HOME / "generated_images" / thread).glob("*.png"))
    if not images:
        raise RuntimeError("no image was generated")
    if (sent or "").strip() != prompt.strip():
        raise RuntimeError(f"the prompt was rewritten: {(sent or '')[:200]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(images[-1], out)
    return out
