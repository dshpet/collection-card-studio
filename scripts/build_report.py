"""Build the single-file dashboard, analysis/report.html. Open it from disk."""

import html
import json
import re
from pathlib import Path

from common import ANALYSIS, load_json

from form import CARD_FORM


def markdown(text):
    """Enough Markdown for the synthesis: headings, bullets, paragraphs and bold."""
    output, in_list = [], False
    for line in text.splitlines():
        line = html.escape(line.strip(), quote=False)
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        is_item = line.startswith("- ")
        if in_list and not is_item:
            output.append("</ul>")
            in_list = False
        if is_item and not in_list:
            output.append("<ul>")
            in_list = True
        if is_item:
            output.append(f"<li>{line[2:]}</li>")
        elif line.startswith("## "):
            output.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            output.append(f"<h2>{line[2:]}</h2>")
        elif line:
            output.append(f"<p>{line}</p>")
    if in_list:
        output.append("</ul>")
    return "\n".join(output)


def main():
    synthesis = ANALYSIS / "SYNTHESIS.md"
    maps = load_json(ANALYSIS / "embedding_map.json")
    cards = load_json(ANALYSIS / "cards.json")
    data = {"cards": cards, "sets": load_json(ANALYSIS / "sets.json"),
            "stats": load_json(ANALYSIS / "stats.json"), "maps": maps, "form": CARD_FORM,
            "synthesis": markdown(synthesis.read_text("utf-8")) if synthesis.exists() else "<p>No synthesis yet.</p>"}
    template = (Path(__file__).parent / "report_template.html").read_text("utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (ANALYSIS / "report.html").write_text(template.replace("/*DATA*/", payload), "utf-8")
    print(f"report: {len(payload) / 1e6:.1f} MB of data")


if __name__ == "__main__":
    main()
