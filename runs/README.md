# Runs

Every generated card and every measurement, oldest first. Full-size drawings, review sheets and model renders are kept on disk but not in git. Findings are in [analysis/STYLE_GAPS.md](../analysis/STYLE_GAPS.md).

| Folder | What | Made by |
|---|---|---|
| `pilot/` | First small batches, before the reference analysis | early `make_set.py` |
| `first/` | First full run: three genres, three variants, plus the off-style controls and the hidden-card test | `make_set.py`, `validate.py` |
| `twins/` | Twelve real cards redrawn with the card hidden, once per style round (`baseline`, `r1`-`r8`), and `r2e`, six r2 twins edited by the director's notes | `validate.py twins` |
| `review/` | Specialist and director reports: style rounds, calibration, checkers, set reviews | `review.py` |
| `drift/` | Field drift and classifier results per batch | `drift.py` |
| `western/`, `sci-fi/`, `horror/` | Three variants of each film genre in the final style | `make_set.py` |
| `final/`, `final.json`, `compare.json` | The ten cards chosen from those variants per genre, and their set numbers against the real sets | by hand, `compare.py` |
| `twins40/` | Forty more twins: old and final style, then `r3`, `r9`, and the parameter rounds `p1`-`p3` | `validate.py`, `experiments/param.py` |
| `ratings.json` | Every human rating: twins, closest style, set cards, trials | `rate_ui.py` |
| `trial/` | Construction trial: brief, brief plus how it works, Blender blockout, fixed blockout | `experiments/trial.py` |
| `*-blockout/` | The 30 final cards redrawn from Blender models | `make_set.py` |
| `trial2/` | Soft render and real photos for the modeller | `experiments/trial2.py` |
| `score/` | Every rated card scored by embeddings, classifier and reviewers | `experiments/score.py` |
| `prefer/`, `prefer_works/` | Which of two drawings is closer, or built right, on pairs the producer decided | `experiments/prefer.py` |
| `tune/` | Automatic tuning of the director's notes | `experiments/tune.py` |
| `param/` | Parameter loop: measured style parameters on the forty twins | `experiments/param.py` |
| `western-2/`, `sci-fi-2/` | Test run of the current pipeline, one variant each. Not final | `make_set.py` |
| `cast_trial/` | The game's characters on new cards: drawn directly, or pre-drawn, pasted and blended | `experiments/cast_trial.py` |
| `search_trial/` | The forty twins with label-picked, search-picked and five references | `experiments/search_trial.py` |
| `smoke/`, `smoke-2/` | Three cards through the changed pipeline, before and after the second review's fixes, one with the cast. Not sets | `make_set.py --plan` |
| `plain_check/` | The sheriff star's invented jewel: subject wording against the colors line | `experiments/plain_check.py` |
| `shape_check/` | The clock twin with and without "a perfect circle", with measured roundness | `experiments/shape_check.py` |
| `fire_check/` | Cauldron and campfire fires: as planned, worded as the real fire, and with the real fire cards as references | `experiments/fire_check.py` |
| `western-batch/`, `sci-fi-batch/`, `horror-batch/` | Variant 1 of each `*-shared-cast` plan: the producer's lessons, iconic objects and one character card. Not final | `make_set.py` |
| `wording_check/` | Hat, boot, witch hat and console from their batch briefs, with the batch's and the earlier finals' wording | `experiments/wording_check.py` |
| `colors/` | Measured backdrop, surface and hero colors of the real cards, the earlier finals and the batch, with a swatch sheet | `experiments/colors.py` |
| `western-batch2/`, `sci-fi-batch2/`, `horror-batch2/` | Variant 1 of each `*-shared-cast-2` plan: the reference color logic and the second reference pass. Not final | `make_set.py` |
| `cast-check/`, `cast-check-2/`, `outfit_check/` | The Western cast plan's character cards, before and after the outfit fix | `make_set.py --plan`, `experiments/outfit_check.py` |
| `plans/` | Draft plans for the film sets, for the producer to approve before drawing | `make_set.make_plan`, `experiments/shared_plans.py` |
| `batch2.png` | The object cards of the three `*-batch2` runs, one row per genre | by hand |
| `robustness/` | 19 odd, risky and hostile requests planned (`plans/`, then `plans2/` after the repair loop), and Kitchen, Pirates and Star Wars drawn end to end | `experiments/robustness.py`, `make_set.py` |
| `grade/` | The forty final-style twins with a measured backdrop grade | `experiments/grade.py` |
| `generators/` | Twins drawn by Nano Banana Pro (11) and Qwen-Image-2.1, against the Codex draws | `experiments/generators.py` |
| `prefinal/` | Pre-final film sets for five candidate genres (`western`, `sci-fi`, `horror`, `period-drama`, `detective`, three variants each, five candidates per card) and six bonus character cards (`cast`); `outside/` holds an outside rater's sample and answers | `make_set.py`, `experiments/outside_rating.py` |
| `night/` | Overnight arms on the twins and on pre-final blockout cards (`palette/`, `blockout/`, `perspective/`), their readings (`read.json`, `read_blockout.json`) and the plan review (`plan_review.json`) | `experiments/night.py`, `plan_review.py` |
| `smooth_check/`, `perspective_check/`, `blockout_drift/` | The research check: flat share of surfaces, a one-camera fit, blockout drift | `experiments/smooth_check.py`, `perspective_check.py`, `blockout_drift.py` |
| `final2/` | The final plans drawn before the smooth-surface line, stopped early and resumable; `cast/` holds the six final cast cards, whose prompt has no material line | `make_set.py --plan runs/plans/final-*.json` |
| `final3/` | The final sets, 2026-11-08: `western/`, `period-drama-2/` and `detective/`, eight candidates per card, with the smooth-surface line, rich colors and the wider blockout frame; each with its `spec.md`. `period-drama/` is Period Drama's first draw, before two cards were replaced. `README.md` says what changed; `sets.json` and `compare.json` are the set numbers (`compare.py --sets`), `set_numbers.json` adds the pre-final variants; `review.json` feeds the morning review page | `make_set.py --plan runs/plans/final-*.json`, `experiments/final_review.py` |

A set run folder holds `plan.json` (with the request that made it), `spec.md` (the set as designed, card by card, with the plan's notes on why; runs before 2026-11-08 have none) and `briefs.json`, the drawings in `tries/`, prompts in `prompts/`, Blender models in `models/`, pairwise judgements in `choose/`, `check.json` with every try's checks, `rounds.json` and `edits.json` with every edit and whether it was kept, and `report.md`.
