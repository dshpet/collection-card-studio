"""Do variants drift less when they share the topic's most iconic objects?

The planner allows versions to share at most five objects, so three versions need 25 or more objects, and the later
versions drift to weak ones (an old car, a Ferris wheel in Horror). This plans the same themes with the opposite rule:
keep the three to five most iconic objects in every version and vary the rest. Plans only, for the producer to compare
with runs/plans/<genre>.json.

    shared_plans.py Horror Sci-Fi                   -> runs/plans/<theme>-shared.json
    shared_plans.py Western --cast 1                -> runs/plans/western-shared-cast.json

Adopted into make_set.py on 2026-11-06, after the producer asked that the iconic objects be tried, so this script
no longer finds the rule it replaces; it is kept as the record of the plans it made.
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
from concurrent.futures import ThreadPoolExecutor

from common import ANALYSIS, ROOT, load_json, save_json

import make_set

LIMIT = "- Versions may share at most 5 objects."
SHARED = ("- Every version keeps the topic's three to five most iconic objects, and the versions differ in the rest, "
          "in staging and in colors.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("themes", nargs="+")
    parser.add_argument("--cast", type=int, default=0, help="character cards per variant")
    parser.add_argument("--suffix", default="", help="added to the file name, so earlier plans are kept")
    args = parser.parse_args()
    themes, cast = args.themes, args.cast
    original = make_set.plan_prompt

    def shared(*args, **kwargs):
        prompt = original(*args, **kwargs)
        assert LIMIT in prompt
        return prompt.replace(LIMIT, SHARED)

    make_set.plan_prompt = shared
    make_set.plan_problems = lambda plan, cast=0: [p for p in original_problems(plan, cast) if "share too many" not in p]
    knowledge = load_json(ANALYSIS / "knowledge.json")

    def one(theme):
        plan = make_set.make_plan(theme, "A set for a Movie collection", 3, knowledge, cast)
        save_json(ROOT / "runs" / "plans" / f"{theme.lower()}-shared{'-cast' if cast else ''}{args.suffix}.json", plan)
        return theme, plan

    with ThreadPoolExecutor(3) as pool:
        for theme, plan in pool.map(one, themes):
            print(f"== {theme}: problems {plan['problems']}")
            for i, variant in enumerate(plan["variants"], 1):
                print(f"  v{i}:", "; ".join(c["name"] for c in variant["cards"]))


original_problems = make_set.plan_problems

if __name__ == "__main__":
    main()
