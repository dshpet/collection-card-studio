"""Build the single-file dashboard, analysis/report.html. Open it from disk."""

import argparse
import html
import json
import re
from pathlib import Path

from common import ANALYSIS, FINAL_SETS, ROOT, best_try, load_json

from form import CARD_FORM


def markdown(text):
    """Enough Markdown for the synthesis: headings, bullets, paragraphs, bold, code and links."""
    output, in_list = [], False
    for line in text.splitlines():
        line = html.escape(line.strip(), quote=False)
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
        line = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', line)
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


def generated_runs():
    """The final sets, then every earlier pipeline run at the top of runs/ with an object-card sheet, for the Generated
    tab. A run of character cards has only its cast sheet, which stays out of git."""
    finals = list(load_json(FINAL_SETS)) if FINAL_SETS.exists() else []
    runs = []
    for slug in finals + sorted(report.parent.name for report in (ROOT / "runs").glob("*/report.md")):
        folder = ROOT / "runs" / slug
        if not (folder / "variant_1.png").exists():
            continue
        plan = load_json(folder / "plan.json")
        history = load_json(folder / "check.json")
        best = [best_try(tries) for tries in history.values() if tries]
        runs.append({"slug": slug, "title": plan["title"], "story": plan.get("story"),
                     "variants": len(plan["variants"]), "cards": len(best),
                     "passed": sum(b["passed"] for b in best),
                     "review": [b["card"]["name"] for b in best if not b["passed"]]})
        if slug in finals:
            runs[-1]["note"] = f"The final set, {slug}: drawn once, then fixed card by card on the producer's comments."
    return runs


def main():
    synthesis = ANALYSIS / "SYNTHESIS.md"
    maps = load_json(ANALYSIS / "embedding_map.json")
    cards = load_json(ANALYSIS / "cards.json")
    data = {"cards": cards, "sets": load_json(ANALYSIS / "sets.json"),
            "stats": load_json(ANALYSIS / "stats.json"), "maps": maps, "form": CARD_FORM, "runs": generated_runs(),
            "synthesis": markdown(synthesis.read_text("utf-8")) if synthesis.exists() else "<p>No synthesis yet.</p>"}
    template = (Path(__file__).parent / "report_template.html").read_text("utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (ANALYSIS / "report.html").write_text(template.replace("/*DATA*/", payload), "utf-8")
    print(f"report: {len(payload) / 1e6:.1f} MB of data")


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()  # --help only; the script takes no options
    main()
