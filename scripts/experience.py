"""What the pipeline learns from its own edits and from the producer's ratings.

    experience.py collect    every edit tried in every run, and whether it beat its draft -> analysis/experience.json
    experience.py propose    a model drafts lessons from lost edits and rating comments, under Proposed in
                             analysis/lessons.md. A person moves the ones they agree with up.

make_set.py records each run's edits in runs/<run>/edits.json and collects them after a run. The art director sees past
edits when it writes new notes, and the planner reads the Planning lessons.
"""

import argparse
import re

from common import ANALYSIS, JUDGE, ROOT, load_json, save_json, strict, text

LESSONS = ANALYSIS / "lessons.md"
EXPERIENCE = ANALYSIS / "experience.json"


def lessons(section):
    """The rules of one section of lessons.md, without their sources."""
    content = LESSONS.read_text("utf-8")
    if f"## {section}\n" not in content:
        print(f"warning: no ## {section} section in {LESSONS.name}, so no lessons are used", flush=True)
        return []
    part = content.split(f"## {section}\n", 1)[1].split("\n## ", 1)[0]
    return [re.sub(r"\s*\*\(.*\)\*$", "", line) for line in part.splitlines() if line.startswith("- ")]


def collect():
    rows = [row for path in sorted((ROOT / "runs").rglob("edits.json")) for row in load_json(path)]
    rows.sort(key=lambda row: row.get("date", ""))  # oldest first, so the director's examples are the latest edits
    save_json(EXPERIENCE, rows)
    print(f"{len(rows)} edits, {sum(r['kept'] for r in rows)} kept")
    return rows


def edit_examples(count=12):
    """Recent edit notes that won and lost against their drafts, for the director's prompt."""
    rows = load_json(EXPERIENCE) if EXPERIENCE.exists() else []
    if not rows:
        return ""
    kept = [r for r in rows if r["kept"]][-(count // 2):]
    lost = [r for r in rows if not r["kept"]][-(count // 2):]
    lines = [f"- {'kept' if r['kept'] else 'lost'}: {r['name']}: {r['note']}" for r in kept + lost]
    return (f"Edit notes tried on earlier cards. An edit was kept only if a judge preferred it to its draft; overall "
            f"{sum(r['kept'] for r in rows)} of {len(rows)} were kept. Write notes like the kept ones:\n"
            + "\n".join(lines))


PROPOSE_SCHEMA = strict({"lessons": {"type": "array", "items": strict({"rule": text(), "evidence": text()})}})


def propose(rater):
    from rate import ask_claude

    rows = collect()
    ratings = load_json(ROOT / "runs" / "ratings.json")
    comments = [f"- {r['id']}: grade {r.get('grade', '?')}, works {r.get('works', '?')}: {r['comment']}"
                for r in ratings.values() if r.get("comment")]
    edits = [f"- {'kept' if r['kept'] else 'lost'}: {r['name']}: {r['note']}" for r in rows]
    answer = ask_claude(
        "A pipeline plans ten-card collection sets for a mobile game, writes one sentence per card for an image model, "
        "and edits drawn cards with notes. Below are its current planning lessons, the producer's rating comments "
        "and edit notes that a judge kept or rejected against their drafts. Propose at most five new planning lessons: "
        "general rules for the planner that would have avoided a problem the producer named more than once. Do not "
        "repeat a current lesson or a rule about rendering style. For each, give the evidence, citing the comments.\n\n"
        "Current lessons:\n" + "\n".join(lessons("Planning")) + "\n\nComments:\n" + "\n".join(comments)
        + "\n\nEdits:\n" + "\n".join(edits), None, PROPOSE_SCHEMA, rater)
    current = LESSONS.read_text("utf-8").rstrip("\n") + "\n"
    if "## Proposed\n" not in current:
        current = current.rstrip("\n") + "\n\n## Proposed\n"
    head, tail = current.split("## Proposed\n", 1)
    section, rest = (tail.split("\n## ", 1) + [""])[:2]
    added = "".join(f"- {lesson['rule']} *({lesson['evidence']})*\n" for lesson in answer["lessons"])
    section = section.rstrip("\n") + "\n" + added
    LESSONS.write_text(head + "## Proposed\n" + section + (f"\n## {rest}" if rest else ""), "utf-8")
    print(f"proposed {len(answer['lessons'])} lessons in {LESSONS.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("collect", "propose"))
    parser.add_argument("--rater", default=JUDGE)
    args = parser.parse_args()
    if args.mode == "collect":
        collect()
    else:
        propose(args.rater)


if __name__ == "__main__":
    main()
