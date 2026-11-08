# Our sets against the references

The final sets, drawn 2026-11-08, are in `runs/final3/` (`western/`, `period-drama-2/`, `detective-3/`), with six bonus cast cards in `runs/final2/cast/`; [what changed](../runs/final3/README.md). The earlier sets of 2026-11-03 (Western, Sci-Fi, Horror) stay in `runs/final/`. Evidence for the style is in [STYLE_GAPS.md](STYLE_GAPS.md). Set numbers come from `scripts/compare.py --sets runs/final3/sets.json`, on the definitions used for the real sets.

After the producer's grades, a fix round redrew 17 cards (`runs/final4/`, [what changed](../runs/final4/README.md)); the numbers below are for round 1. Round 2 (`compare.py --sets runs/final4/sets.json`): Western 7 object classes, 5 scales, 6 backdrop hues, style similarity 0.554; Period Drama 7, 2, 6, 0.551; Detective 6, 4, 8, 0.471. Detective's replaced cards brought new colors, and its similarity fell from 0.543; it now has one or two backdrop hues more than any real set.

## Idea

| Principle in the references | Western | Period Drama | Detective |
|---|---|---|---|
| A plain topic for a title, 1-2 words | Western | Period Drama | Detective |
| Cards are the first things anyone would name | Cowboy hat, sheriff star, boots, saddle, covered wagon, campfire | Top hat, tea cup, parasol, pocket watch, quill pen, piano | Magnifier, fedora, flashlight, badge wallet, fingerprint, squad car, bloodhound |
| Every object belongs to this topic, not the wider collection | No reels or popcorn | No reels or popcorn | No reels or popcorn |
| Mixes small things with big ones | Harmonica to windmill | Pocket watch to piano | Evidence bag to squad car |
| All four art categories, with few of category 2 | 4/1/3/2 | 4/2/3/1 | 3/2/3/2 |

The film genre sets carry the idea through objects alone, as the brief asks: no gold cards and no characters. The cast cards are a bonus beside them, two per genre, with the game's characters drawn from their real cutouts. The genres were chosen with the producer; each set starts from the outside artist's best-graded pre-final variant of it, with cards swapped on the grades ([plan review](../experiments/plan_review.py), notes in each set's `spec.md`).

## Set numbers

| Set | Title words | Name words | Object classes | Scales | Backdrop hues | Categories 1/2/3/4 | Style similarity |
|---|---:|---:|---:|---:|---:|---|---:|
| Sports | 1 | 2 | 4 | 2 | 6 | 3/1/3/3 | 0.613 |
| Finals | 1 | 2 | 6 | 2 | 6 | 4/1/4/1 | 0.603 |
| Coolness | 1 | 2 | 6 | 2 | 7 | 2/2/2/4 | 0.610 |
| Countrystead | 1 | 2 | 7 | 5 | 6 | 1/2/2/5 | 0.641 |
| **Western** | 1 | 2 | 7 | 5 | 6 | 4/1/3/2 | 0.552 |
| **Period Drama** | 2 | 2 | 6 | 2 | 7 | 4/2/3/1 | 0.556 |
| **Detective** | 1 | 2 | 8 | 4 | 7 | 3/2/3/2 | 0.543 |

Names, scales and backdrop hues sit inside the real ranges. Period Drama is the one two-word title, and Detective has one object class more than the widest real set.

Style similarity, the mean CSD between a set's own cards, is lower than in the real sets (0.54-0.56 against 0.60-0.64; the 2026-11-03 sets had 0.57-0.66, the pre-final variants 0.48-0.56). Most of it is color. On grey copies of the cards, Period Drama rises to 0.635, inside the real range, and Western to 0.590, while the real sets move by less than 0.03: a real set's cards share one color treatment, and each of ours takes its own saturated hue. Detective stays low in grey (0.570) because its objects differ in form and material: a safe, a car, a dog, a bag. This measure has not been checked against the producer; CSD against the same object, which has, improved overnight.

## Art

Medians on the 30 final cards against the 126 real object cards, beside the same genres' pre-final variants (`experiments/final_numbers.py`, `runs/final3/set_numbers.json`):

| Measure | Real | Pre-final | Final |
|---|---:|---:|---:|
| Subject chroma | 0.128 | 0.102 | 0.125 |
| Hue families | 3.8 | 2.4 | 2.5 |
| Shadow chroma kept | 97% | 82% | 87% |
| Smallest margin to the card edge | 0.060 | 0.098 | 0.082 |
| Subject area | 0.324 | 0.279 | 0.277 |

| Principle in the references | Where we stand |
|---|---|
| Real proportions, simplified but not inflated | Followed; objects still slightly plumper |
| Thin parts stay thin | Followed on straps, spurs, chains and handles |
| Materials read as themselves; large surfaces smooth, detail in the parts | Closer: the smooth-surface line brought flat surfaces nearer the real cards on 27 of 40 twins. The outside artist had found ours grainy |
| Rich, clean local colors, three or four hues on the object | Partly: subject chroma is now near the real cards; ours still use fewer hue families |
| One clear soft light, form turns smoothly | Followed |
| Backdrop against the hero's color temperature, never its hue | Followed in the plan |
| Three-quarter view, even for symmetric objects | Followed since batch 2 (2 of 16 near-mirror) |
| The object large on the card | Closer: margins shrank on the blockout cards; subject area still below the real cards |
| A pool of light behind the object, darker corners | Rare: the image model ignores the words |
| Tone-on-tone patterns: rays, rings, stripes, waves, diamonds | Followed |
| No text, frame or outline | Followed, except numerals on the pocket watch face |

## Where we still differ

- **Construction and perspective:** the outside artist marked 9 of 75 pre-final cards broken, all on perspective or construction. No model or pixel judge reads it, so the camera line and Blender models for those cards wait on the producer's blind look (`experiments/final_review.py`).
- **Color across a set:** each card gets its own saturated backdrop, so our sets vary more in color than the real ones (above).
- **Blind:** the producer still spots 24 of 32 final-style twins; the outside artist's quick blind pass came out inverted (23 of 72), calling the brighter, larger real cards AI ([STYLE_GAPS](STYLE_GAPS.md)).
- **Rating:** the final sets are not graded yet. The pre-final cards had 3.1 of 5 from the outside artist; the producer graded batch 2's object cards at 3.85. The other numbers above come from models or measurement.
