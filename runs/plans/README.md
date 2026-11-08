# Plans

Plans for the film sets, oldest first; the card lists are in each JSON. Draw one with `make_set.py "<Theme>" --plan runs/plans/<file>.json`. The final sets draw `final-western-3.json`, `final-period-drama-5.json`, `final-detective-6.json` and `final-cast-2.json`.

| Files | Made | What changed |
|---|---|---|
| `western.json`, `sci-fi.json`, `horror.json`, `western-cast.json` | 2026-11-05 | The planner as it was: variants shared at most five objects |
| `*-shared.json` | 2026-11-05 | Variants keep the topic's most iconic objects (`experiments/shared_plans.py`) |
| `*-shared-cast.json` | 2026-11-06 | The producer's first accepted lessons and one character card per variant; variant 1 drawn as `runs/<genre>-batch` |
| `*-shared-cast-2.json` | 2026-11-06 | Backdrop color logic and the second reference pass; variant 1 drawn as `runs/<genre>-batch2` |
| `*-shared-3.json` | 2026-11-06 | No character cards, as the brief asks; no landforms or sky bodies, night skies for dark topics, the game's emblem on one object |
| `cast-bonus.json` | 2026-11-07 | Bonus character cards: the planner's two per genre (`--cast 2`), the object cards dropped; drawn as `runs/prefinal/cast` |
| `final-*.json` | 2026-11-08 | First draw of the final sets, composed card by card from the pre-final variants and the producer's earlier batches after `experiments/plan_review.py`, recolored under the rich-color rule; each plan's `notes` say why, and its run's `spec.md` shows them. `final-cast.json`: six cast cards, two per genre. Made by `experiments/night.py plans` and `recolor`. `final-period-drama-2.json`, `final-detective-2.json` and `final-detective-3.json` change cards after a draw (their last notes) |
| `final-western-2.json`, `final-period-drama-3.json` and `-4` (the Candelabra), `final-detective-4.json`, `final-cast-2.json` | 2026-11-08 | Fix round 1: each changes only the cards the producer commented on, and its last notes quote the comment and say what changed; drawn as `runs/final4` with `--keep` |
| `final-western-3.json`, `final-period-drama-5.json`, `final-detective-5.json` | 2026-11-08 | Fix round 2: notes and colors on the eight commented cards, with the comments in the last notes; drawn as `runs/final5` with `--keep` |
| `final-period-drama-6.json`, `final-detective-6.json` | 2026-11-08 | Fix round 3: the Top Hat built in Blender (not used) and the Magnifier's handle; drawn as `runs/final6` |
