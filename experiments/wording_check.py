"""Do the producer's lessons make objects plainer through the subject wording?

The first batch (runs/<genre>-batch) looks more correct but plainer than the earlier finals: the hat lost
its badge, the boot its spur, the witch hat its bent tip, the control panel its gauges. Its subjects are longer and
geometric, as the shape lesson asks. Four objects, each drawn from its batch brief (same staging, backdrop and
references, no blockout), three draws per arm:
    new   the batch's subject and hero colors
    old   the earlier final's subject and hero colors (runs/<genre>/briefs.json)

    wording_check.py     the sheet has one row per object and arm, new before old
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ROOT, contact_sheet, load_json

from make_set import draw_card

RUN = ROOT / "runs" / "wording_check"
OBJECTS = [("western", "Cowboy Hat"), ("western", "Cowboy Boot"), ("horror", "Witch Hat"), ("sci-fi", "Control Panel")]


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    RUN.mkdir(parents=True, exist_ok=True)
    jobs = []
    for genre, name in OBJECTS:
        new = next(b for b in load_json(ROOT / "runs" / f"{genre}-batch" / "briefs.json") if b["card"]["name"] == name)
        old = next(b for b in load_json(ROOT / "runs" / genre / "briefs.json") if b["card"]["name"] == name)
        worded = {**new, "card": {**new["card"], "subject": old["card"]["subject"], "hero_colors": old["card"]["hero_colors"]}}
        slug = name.lower().replace(" ", "-")
        jobs += [({**brief, "id": f"{slug}-{arm}"}, n) for arm, brief in (("new", new), ("old", worded)) for n in (1, 2, 3)]
    with ThreadPoolExecutor(3) as pool:
        done = list(pool.map(lambda job: draw_card(RUN, job[0], job[1], [], True), jobs))
    contact_sheet([RUN / "tries" / f"{d}.png" for d in done if d], RUN / "sheet.png", columns=3)
    print("drew", sum(bool(d) for d in done), "of", len(jobs), "->", RUN / "sheet.png")


if __name__ == "__main__":
    main()
