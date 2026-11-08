# Draft plans

Draft plans, oldest first; the producer did not confirm every one. The card lists are in each JSON. Draw one with `make_set.py "<Theme>" --plan runs/plans/<file>.json`.

| Files | Made | What changed |
|---|---|---|
| `western.json`, `sci-fi.json`, `horror.json`, `western-cast.json` | 2026-11-05 | The planner as it was: variants shared at most five objects |
| `*-shared.json` | 2026-11-05 | Variants keep the topic's most iconic objects (`experiments/shared_plans.py`) |
| `*-shared-cast.json` | 2026-11-06 | The producer's first accepted lessons and one character card per variant; variant 1 drawn as `runs/<genre>-batch` |
| `*-shared-cast-2.json` | 2026-11-06 | Backdrop color logic and the second reference pass; variant 1 drawn as `runs/<genre>-batch2` |
| `*-shared-3.json` | 2026-11-06 | No character cards, as the brief asks; no landforms or sky bodies, night skies for dark topics, the game's emblem on one object |
| `cast-bonus.json` | 2026-11-07 | Bonus character cards: the planner's two per genre (`--cast 2`), the object cards dropped; drawn as `runs/prefinal/cast` |
| `final-*.json` | 2026-11-08 | The final sets, composed card by card from the pre-final variants and the producer's earlier batches after `experiments/plan_review.py`, recolored under the rich-color rule; each plan's `notes` say why, and its run's `spec.md` shows them. `final-cast.json`: six cast cards, two per genre. Made by `experiments/night.py plans` and `recolor`. `final-period-drama-2.json` replaces two cards after the first draw (its last notes) |

Draft plans are a record of how the plans changed; the final sets draw `final-*.json`.
