# Fix round 3 and the final sets, 2026-11-08

The producer graded round 3 (`runs/final5`): every set 5 of 5, "close to being satisfied". The one comment was the Magnifier, 1: "Too large the glass is, and the handle is too small". The Top Hat got 3 again without a comment. The Candelabra (3) "looks fine... probably decent as it is". After four rounds the producer was tired of viewing cards, so this round's two redraws were judged here, against the comments: a redraw replaces the round-3 card only if it is clearly better.

| Card | Change | Kept? |
|---|---|---|
| Magnifier | Round 2's long thin handle was "elongated", round 3's short one "too small". The handle is now 0.40 long and sturdy, about 0.85 of the lens's width from the rim, as on the real Map card, and the blockout is framed at 0.9 so the glass is smaller | Yes, `detective/` v1_03_9: smaller glass, sturdy handle |
| Top Hat | Every one of the sixteen candidates drawn from text curled one side of the brim higher. Built in Blender with an even brim, seen almost from the front | No: the brim is even, but the hat is a stiff frontal stovepipe, less appealing than round 3's; the pipeline's pick also turned it navy. `period-drama/` is kept for the record |

## The final sets

![The three final sets](final_sets.png)

| Set | Folder | Plan |
|---|---|---|
| Western | `runs/final5/western-2/` | `runs/plans/final-western-3.json` |
| Period Drama | `runs/final5/period-drama/` | `runs/plans/final-period-drama-5.json` |
| Detective | `runs/final6/detective/` | `runs/plans/final-detective-6.json` |
| Cast bonus, two cards per genre | `runs/final4/cast/` | `runs/plans/final-cast-2.json` |

Producer's grades, latest per card: sets 5, 5, 5, cast 5; cards 4.5 Western, 3.8 Period Drama, 4.0 Detective without the new Magnifier, 4.33 cast.

| Set | Object classes | Scale classes | Backdrop hues | Style similarity |
|---|---:|---:|---:|---:|
| Real sets, range | 4-7 | 2-5 | 6-7 | 0.603-0.641 |
| Western | 7 | 5 | 6 | 0.560 |
| Period Drama | 7 | 2 | 6 | 0.551 |
| Detective | 6 | 4 | 9 | 0.474 |

`compare.json` from `scripts/compare.py --sets runs/final6/sets.json`. Style similarity is descriptive, not validated against the producer's grades. `final_sets.png` shows the object cards; the cast cards show the game's characters and stay out of git.

The review page's round 4 (`experiments/final_review.py serve`, the default) shows this assembly; only the Magnifier changed.
