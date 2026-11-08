# The final sets, 2026-11-08

| Set | Folder | Plan |
|---|---|---|
| Western | `western/` | `runs/plans/final-western.json` |
| Period Drama | `period-drama-2/` | `runs/plans/final-period-drama-2.json` |
| Detective | `detective/` | `runs/plans/final-detective.json` |
| Cast bonus, two cards per genre | `runs/final2/cast/` | `runs/plans/final-cast.json` |

Each folder has `spec.md` (the set: staging, subject, colors, why each card), `report.md` (checks), `variant_1.png` (the set) and every candidate in `tries/`. `period-drama/` is the first draw of Period Drama, kept for the record.

## Review

`.venv/bin/python -B experiments/final_review.py serve`, then http://127.0.0.1:8767. Sets: the four rows under a real set. Cards: each card with its references, all eight candidates (click one to pick it instead), its blockout and the pre-final drawing with the outside rater's grade; grade 1-5, broken, comment. Blind arms: the overnight smooth-surface and one-camera twins against the real card, and the nine broken pre-final cards redrawn by the perspective arms. Answers go to `runs/ratings.json`; `final_review.py summary` reads them.

## What changed since the pre-final

- **Plans** composed card by card from the evidence: the outside rater's best variant per genre, cards the producer graded 5 before, and swaps for cards graded low or broken (`experiments/plan_review.py`, notes in each `spec.md`).
- **Rich colors** in the planner: twins closer to their real cards by CSD on 29 of 40.
- **Smooth surfaces** in the prompt for cards drawn from text: flat share nearer the real cards on 27 of 40 twins, no gloss or CSD cost. The blockout prompt is unchanged: there the line read glossier.
- **Blockouts framed larger**, half the gap to the real cards' median, categories 2-4.
- **Eight candidates per card** instead of five.
- **Period Drama, after its first draw:** the Pearl Necklace failed the style check in all nine drawings (a navy cushion filling the card), so it became the Quill Pen, the outside rater's 4; the Hat Box drew as a plain red drum and got crimson and cream stripes. Both then passed.

Evidence and the dropped arms: `analysis/STYLE_GAPS.md`, "Overnight arms".

## Set numbers

Against the four real sets without character cards (`set_numbers.json`; `compare.json` from `scripts/compare.py --sets runs/final3/sets.json`). [COMPARISON](../../analysis/COMPARISON.md) has the full table and why style similarity is low. Style similarity is the mean CSD between a set's own cards; it is descriptive, not a judge.

| Set | Object classes | Scale classes | Backdrop hues | Style similarity |
|---|---:|---:|---:|---:|
| Real sets, range | 4-7 | 2-5 | 6-7 | 0.603-0.641 |
| Western, final / pre-final v1 | 7 / 8 | 5 / 5 | 6 / 6 | 0.552 / 0.563 |
| Period Drama, final / pre-final v3 | 6 / 5 | 2 / 2 | 7 / 8 | 0.556 / 0.482 |
| Detective, final / pre-final v2 | 8 / 9 | 4 / 3 | 7 / 5 | 0.536 / 0.543 |

## Not in the final, waiting on the producer

- One camera: no measured change on the twins; the blind page asks.
- Perspective: no model or pixel judge reads it; the blind page shows the nine broken cards redrawn with the camera line and with Blender models.
- A style LoRA on the reference cards: about half a day; needs a decision.

The final started at 11:15 instead of 04:00: a background wait loop matched its own command line and waited on itself all night.
