# First draw of the final sets

| Set | Folder | Plan |
|---|---|---|
| Western | `western/` | `runs/plans/final-western.json` |
| Period Drama | `period-drama-2/` | `runs/plans/final-period-drama-2.json` |
| Detective | `detective-3/` | `runs/plans/final-detective-3.json` |
| Cast bonus, two cards per genre | `runs/final2/cast/` | `runs/plans/final-cast.json` |

Each folder has `spec.md` (staging, subject, colors and why, per card), `report.md` (checks), `variant_1.png` (the cast sheet is kept out of git) and every candidate in `tries/` (on disk, not in git). `period-drama/`, `detective/` and `detective-2/` are earlier draws of those sets.

The producer graded this draw on `experiments/final_review.py` (round 1): every set 4 of 5, "Yes, with small issues"; cards 4.4 Western, 3.8 Period Drama, 3.1 Detective, 3.83 cast. The fix rounds follow in [final4](../final4/README.md).

## What changed since the pre-final

- **Plans** composed card by card: the outside rater's best variant per genre, cards the producer graded 5 before, and swaps for cards graded low or broken (`experiments/plan_review.py`, notes in each `spec.md`).
- **Rich colors** in the planner: twins closer to their real cards by CSD on 29 of 40.
- **Smooth surfaces** in the prompt for cards drawn from text: flat share nearer the real cards on 27 of 40 twins, no gloss or CSD cost. The blockout prompt is unchanged: there the line read glossier.
- **Blockouts framed larger**, half the gap to the real cards' median, categories 2-4.
- **Eight candidates per card** instead of five.
- **Period Drama, after its first draw:** the Pearl Necklace failed the style check in all nine drawings (a navy cushion filling the card), so it became the Quill Pen, the outside rater's 4; the Hat Box drew as a plain red drum and got crimson and cream stripes.
- **Detective, in two redraws:** the Badge Wallet lay on a dark wooden table, darker than any real card, so it moved to a light honey-colored desk; then the Flash Camera moved from sky blue to royal blue, so the set no longer had four cyan backdrops. Both redraws were seeded with the other cards' candidates.

The arms tried and dropped before this draw (one camera, perspective fixes) are in [STYLE_GAPS](../../analysis/STYLE_GAPS.md#overnight-arms-before-the-final).

## Set numbers

Against the four real sets without character cards (`set_numbers.json` from `experiments/final_numbers.py`; `compare.json` from `scripts/compare.py --sets runs/final3/sets.json`). Style similarity is the mean CSD between a set's own cards; [COMPARISON](../../analysis/COMPARISON.md) explains why it is low.

| Set | Object classes | Scale classes | Backdrop hues | Style similarity |
|---|---:|---:|---:|---:|
| Real sets, range | 4-7 | 2-5 | 6-7 | 0.603-0.641 |
| Western, final / pre-final v1 | 7 / 8 | 5 / 5 | 6 / 6 | 0.552 / 0.563 |
| Period Drama, final / pre-final v3 | 6 / 5 | 2 / 2 | 7 / 8 | 0.556 / 0.482 |
| Detective, final / pre-final v2 | 8 / 9 | 4 / 3 | 7 / 5 | 0.543 / 0.543 |

The review page: `.venv/bin/python -B experiments/final_review.py serve`, then http://127.0.0.1:8767; `final_review.py summary` reads the grades.
