# Our sets against the references

The final sets ([list](../runs/final6/README.md)) are Western (`runs/final5/western-2/`), Period Drama (`runs/final5/period-drama/`) and Detective (`runs/final6/detective/`), with six bonus cast cards in `runs/final4/cast/`. They were drawn on 2026-11-08 (`runs/final3/`, [what changed](../runs/final3/README.md)), then three fix rounds redrew 17, 8 and 1 cards on the producer's comments. The numbers below are for the final sets, from `scripts/compare.py --sets runs/final6/sets.json` and `experiments/final_numbers.py` (`runs/final6/set_numbers.json`), on the definitions used for the real sets; the sets as first drawn are in `runs/final3/compare.json` and `runs/final3/set_numbers.json`. The earlier sets of 2026-11-03 stay in `runs/final/`. Evidence for the style is in [STYLE_GAPS.md](STYLE_GAPS.md).

## Idea

| Principle in the references | Western | Period Drama | Detective |
|---|---|---|---|
| A plain topic for a title, 1-2 words | Western | Period Drama | Detective |
| Cards are the first things anyone would name | Cowboy hat, sheriff star, boots, saddle, covered wagon, campfire | Top hat, tea cup, parasol, pocket watch, quill pen, piano | Magnifier, fedora, trench coat, police badge, handcuffs, squad car |
| Every object belongs to this topic, not the wider collection | No reels or popcorn | No reels or popcorn | No reels or popcorn |
| Mixes small things with big ones | Harmonica to windmill | Pocket watch to piano | Evidence bag to squad car |
| All four art categories, with few of category 2 | 4/1/2/3 | 4/2/3/1 | 4/2/2/2 |

The film genre sets carry the idea through objects alone, as the brief asks: no gold cards and no characters. The cast cards are a bonus beside them, two per genre, with the game's characters drawn from their real cutouts. The genres were chosen with the producer; each set starts from the outside artist's best-graded pre-final variant of it, with cards swapped on the grades ([plan review](../experiments/plan_review.py), notes in each set's `spec.md`). The fix rounds swapped four objects that did not read: the Hat Box became the Candelabra, the Badge Wallet a Police Badge with its emblem, the Doorknob Print a Trench Coat and the Bloodhound, which read as a character, the Handcuffs.

## Set numbers

| Set | Title words | Name words | Object classes | Scales | Backdrop hues | Categories 1/2/3/4 | Style similarity |
|---|---:|---:|---:|---:|---:|---|---:|
| Sports | 1 | 2 | 4 | 2 | 6 | 3/1/3/3 | 0.613 |
| Finals | 1 | 2 | 6 | 2 | 6 | 4/1/4/1 | 0.603 |
| Coolness | 1 | 2 | 6 | 2 | 7 | 2/2/2/4 | 0.610 |
| Countrystead | 1 | 2 | 7 | 5 | 6 | 1/2/2/5 | 0.641 |
| **Western** | 1 | 2 | 7 | 5 | 6 | 4/1/2/3 | 0.560 |
| **Period Drama** | 2 | 2 | 7 | 2 | 6 | 4/2/3/1 | 0.551 |
| **Detective** | 1 | 2 | 6 | 4 | 9 | 4/2/2/2 | 0.474 |

Names, object classes and scales sit inside the real ranges. Period Drama is the one two-word title. Detective has nine backdrop hues, two more than any real set: its fix rounds brought coral red and sage green.

Style similarity, the mean CSD between a set's own cards, is lower than in the real sets (0.47-0.56 against 0.60-0.64; the sets as first drawn had 0.54-0.56, the 2026-11-03 sets 0.57-0.66). Most of it is color. On grey copies of the cards Period Drama rises to 0.623, inside the real range, Western to 0.586 and Detective to 0.588, while the real sets move by less than 0.03: a real set's cards share one color treatment, and each of ours takes its own saturated hue. This measure has not been checked against the producer, who graded all three sets 5 of 5 at these values.

## Art

Medians on the 30 final cards against the 126 real object cards, beside the sets as first drawn and the same genres' pre-final variants (`experiments/final_numbers.py`):

| Measure | Real | Pre-final | First drawn | Final |
|---|---:|---:|---:|---:|
| Subject chroma | 0.128 | 0.102 | 0.125 | 0.111 |
| Hue families | 3.8 | 2.4 | 2.5 | 2.3 |
| Shadow chroma kept | 97% | 82% | 87% | 90% |
| Smallest margin to the card edge | 0.060 | 0.098 | 0.082 | 0.079 |
| Subject area | 0.324 | 0.279 | 0.277 | 0.247 |

The fix rounds moved subject chroma and area away from the real cards while the producer's grades rose: matte metal and porcelain, soft grey handcuffs and a smaller magnifier glass were what they asked for. These medians describe; they do not judge.

| Principle in the references | Where we stand |
|---|---|
| Real proportions, simplified but not inflated | Followed; the producer still caught a magnifier too long, then too short |
| Thin parts stay thin | Followed on straps, spurs, chains and handles |
| Materials read as themselves; large surfaces smooth, detail in the parts | Followed after the fixes: the image model paints metal, porcelain and enamel glossier than the game, and the producer asked for matte four times |
| Rich, clean local colors, three or four hues on the object | Partly: subject chroma 0.111 against 0.128, and fewer hue families |
| One clear soft light, form turns smoothly | Followed |
| Backdrop against the hero's color temperature, never its hue | Followed in the plan |
| Three-quarter view, even for symmetric objects | Followed: 3 of 19 near-mirror silhouettes in categories 1 and 3, against 13 of 67 real. A top hat seen straight from the front read stiff and was not used |
| The object large on the card | Partly: margins near the real cards, subject area below them |
| A pool of light behind the object, darker corners | Partly: 7 of 12 cards in categories 2 and 3, against 39 of 52 real |
| Category 4 shows the object's exact spot, close, often cut by the card's edge | Not followed: no final card in category 4 is cut by the edge, against 17 of 42 real |
| Tone-on-tone patterns: rays, rings, stripes, waves, diamonds | Followed |
| No text, frame or outline | Followed, except numerals on the pocket watch face |

## What the producer's comments were about

The producer left 23 comments on single cards over four review rounds. None asked for a different overall style: render, palette, outline or light. Nine were about shape, proportion, viewpoint or construction (a magnifier's perspective and proportions, a top hat's brim, a candelabra and a watch in perspective, a ring that did not sit inside its bag), five about material finish (gloss, metal, texture), three about recognition (a windmill that read as a monument, a badge without its emblem, a dog as an object), three about composition (off-center objects, a busy doorway), and three about the cast cards (blush, a third leg, a misplaced hat). The rules drawn from them wait for the producer under Proposed in [lessons.md](lessons.md).

## Where we still differ

- **Construction and perspective:** the outside artist marked 9 of 75 pre-final cards broken, all on perspective or construction. No model or pixel judge reads it. Blind, the producer found the current pipeline better built than the camera line or Blender models for those cards, so both arms were dropped; their later comments were fixed card by card in the plan or the blockout. Two minor ones were left as they are: the pocket watch "may have some problems with the perspective", and the hat on the man in Sheriff Pals is "a tad misplaced".
- **Color across a set:** each card gets its own saturated backdrop, so our sets vary more in color than the real ones (above).
- **Blind:** the producer still spots 24 of 32 final-style twins; the outside artist's quick blind pass came out inverted (23 of 72), calling the brighter, larger real cards AI ([STYLE_GAPS](STYLE_GAPS.md)).
- **Rating:** the producer graded each final set 5 of 5; cards 4.5 Western, 3.8 Period Drama, 4.0 Detective (without the last Magnifier, judged by us) and 5.0 for the cast cards ([final sets](../runs/final6/README.md)). The pre-final cards had 3.1 of 5 from the outside artist; the producer graded batch 2's object cards at 3.85. The other numbers above come from models or measurement.
