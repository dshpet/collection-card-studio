# Runs

Every generated card and every measurement, oldest first. Full-size drawings, review sheets and model renders are kept on disk but not in git. Findings are in [analysis/STYLE_GAPS.md](../analysis/STYLE_GAPS.md).

| Folder | What | Made by |
|---|---|---|
| `pilot/` | First small batches, before the reference analysis | early `make_set.py` |
| `first/` | First full run: three genres, three variants, plus the off-style controls and the hidden-card test | `make_set.py`, `validate.py` |
| `twins/` | Twelve real cards redrawn with the card hidden, once per style round (`baseline`, `r1`-`r9`) | `validate.py twins` |
| `review/` | Specialist and director reports: style rounds, calibration, checkers, set reviews | `review.py` |
| `drift/` | Field drift and classifier results per batch | `drift.py` |
| `western/`, `sci-fi/`, `horror/` | Three variants of each film genre in the final style | `make_set.py` |
| `final/`, `final.json` | The ten cards chosen from those variants, per genre | by hand |
| `twins40/` | Forty more twins: old and final style, then `r3`, `r9`, and the parameter rounds `p1`-`p3` | `validate.py`, `experiments/param.py` |
| `ratings.json` | Every human rating: twins, closest style, set cards, trials | `rate_ui.py` |
| `trial/` | Construction trial: brief, brief plus how it works, Blender blockout, fixed blockout | `experiments/trial.py` |
| `*-blockout/` | The 30 final cards redrawn from Blender models | `make_set.py` |
| `trial2/` | Soft render and real photos for the modeller | `experiments/trial2.py` |
| `score/` | Every rated card scored by embeddings, classifier and reviewers | `experiments/score.py` |
| `prefer/`, `prefer_works/` | Which of two drawings is closer, or built right, on pairs the user decided | `experiments/prefer.py` |
| `tune/` | Automatic tuning of the director's notes | `experiments/tune.py` |
| `param/` | Parameter loop: measured style parameters on the forty twins | `experiments/param.py` |
| `western-2/`, `sci-fi-2/` | Test run of the current pipeline, one variant each. Not final | `make_set.py` |
| `cast_trial/` | The game's characters on new cards: drawn directly, or pre-drawn, pasted and blended | `experiments/cast_trial.py` |
| `search_trial/` | The forty twins with label-picked, search-picked and five references | `experiments/search_trial.py` |
| `smoke/` | Three cards through the changed pipeline, one with the cast. Not a set | `make_set.py --plan` |
| `plain_check/` | The sheriff star's invented jewel: subject wording against the colors line | `experiments/plain_check.py` |
| `shape_check/` | The clock twin with and without "a perfect circle", with measured roundness | `experiments/shape_check.py` |
| `plans/` | Draft plans for the final film sets, for the producer to approve before drawing | `make_set.make_plan` |

A set run folder holds `plan.json` and `briefs.json`, the drawings in `tries/`, prompts in `prompts/`, Blender models in `models/`, pairwise judgements in `choose/`, `check.json` with every try's checks, and `edits.json` with every edit and whether it was kept.
