# Fix round 2, 2026-11-08

The producer graded round 2 (`runs/final4`): Western 5 of 5, Period Drama 4, Detective 4, cast 5; cards 4.4 Western, 3.5 Period Drama, 3.8 Detective, 4.5 cast. "I like it overall, lets try some smaller fixes." This round redraws the eight cards with a comment, eight candidates each, with `make_set.py --keep <round-2 run> --candidates 8`.

| Set | Folder | Plan | Kept from |
|---|---|---|---|
| Western | `western-2/` | `runs/plans/final-western-3.json` | `final4/western` |
| Period Drama | `period-drama/` | `runs/plans/final-period-drama-5.json` | `final4/period-drama-2` |
| Detective | `detective/` | `runs/plans/final-detective-5.json` | `final4/detective` |
| Cast bonus | unchanged, `runs/final4/cast/` | | |

`western/` drew three candidates, the default, before the run was restarted with eight; it is kept for the record and not used.

## What changed, by the producer's comments

| Card | Round 2 | Comment | Change | Pick |
|---|---|---|---|---|
| Campfire | 3 | "Maybe the kettle is too metallic in texture?" | Matte enamel pot in the plan | Edit, v1_10_9 |
| Candelabra | 2, picked 8 | "Perspective seems a little off?"; set: "candelabra perspective?" | Every drawing showed the base from well above and the arms and cups straight on. The blockout now looks from the front at the height of its middle (8 degrees round, 6 up, 85 mm, was 28, 12, 60) | Edit, v1_02_9 |
| Top Hat | 3 | "Maybe the rim is too curved on one side, noticeable" | A note for an even brim, seen from the front | By hand, v1_03_3 |
| Parasol | 4 | "could we rotate the parasol slightly?" | The model leans 10 degrees instead of 20 | Edit, v1_04_9 |
| Folding Fan | 4 | set: "Fan maybe a little off, idk?" | The model was rolled 14 degrees, so one outer stick lay flat and the other rose. Now opened evenly, with deeper pleats, in the plan's pink and ivory | Edit, v1_06_9 |
| Cake Stand | 3 | "The white material is too glossy" | Matte porcelain in the plan and the model | Edit, v1_07_9 |
| Magnifier | 3 | "It's kinda elongated"; set: "a tad strange maybe?" | A short chunky handle, 0.30 long instead of 0.48 | Edit, v1_03_9 |
| Handcuffs | 3 | "too metallic maybe, should be softer in texture" | Soft satin grey steel in the plan and the model | Edit, v1_10_9 |

Every model change was made by hand, rendered and checked by eye before drawing (`models/`).

## The review undid the producer's notes

The first review of Period Drama and Detective asked for "bright, polished chrome" on the Handcuffs, "crisp glossy highlights" on the Cake Stand and plain scallops for the fan's lace, and its Magnifier edit grew the handle long again. The art director never saw the producer's notes. Now it does (`producer` in `scripts/review.py`): it is told never to ask for the opposite of one, and each edit prompt ends with `Keep: <note>`. The review ran again; its first notes, edits and records are in each folder's `before-notes/`.

With the notes, the director asked for soft satin cuffs and kept the short handle, but it still asked for glossy porcelain once; the edit's `Keep:` line held the porcelain matte. It still simplifies the lace on the fan and the parasol into a smooth scalloped band. The lace drafts (Parasol v1_04_7, Fan v1_06_7) are one click away on the review page.

The Top Hat's eight candidates all curl the right side of the brim higher than the left. The pick chose v1_03_1, among the least even; v1_03_3, whose two ends curl most alike, was picked by hand (`picked_by` in `period-drama/check.json`). If it still reads uneven, the next step is a Blender model.

## Results

| Set | Object classes | Scale classes | Backdrop hues | Style similarity |
|---|---:|---:|---:|---:|
| Real sets, range | 4-7 | 2-5 | 6-7 | 0.603-0.641 |
| Western, round 3 / 2 | 7 / 7 | 5 / 5 | 6 / 6 | 0.560 / 0.554 |
| Period Drama, round 3 / 2 | 7 / 7 | 2 / 2 | 6 / 6 | 0.551 / 0.551 |
| Detective, round 3 / 2 | 6 / 6 | 4 / 4 | 9 / 8 | 0.471 / 0.471 |

`compare.json` from `scripts/compare.py --sets runs/final5/sets.json`. Style similarity is descriptive, not validated against the producer's grades.

Two lessons were added under Proposed in `analysis/lessons.md`: soft matte metal, porcelain and enamel; symmetric objects shown so both sides match, tall objects from mid-height, short handles.

## Review

`.venv/bin/python -B experiments/final_review.py serve` (round 3 is the default), then http://127.0.0.1:8767. Each changed card shows its round-2 drawing with the grade and comment; a card unchanged since an earlier round carries the grade it got last. Grand Ball and Cake Clue, redrawn in round 2, have no card grade yet.
