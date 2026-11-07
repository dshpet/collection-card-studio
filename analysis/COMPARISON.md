# Our sets against the references

The three sets chosen on 2026-11-03 are in `runs/final/`, one folder per set with a sheet beside it. They will be redrawn with the current pipeline, and this comparison redone. Evidence for the style is in [STYLE_GAPS.md](STYLE_GAPS.md). Set numbers come from `scripts/compare.py`, on the definitions used for the real sets.

## Idea

| Principle in the references | Western | Sci-Fi | Horror |
|---|---|---|---|
| A plain topic for a title, 1-2 words | Western | Sci-Fi | Horror |
| Cards are the first things anyone would name | Hat, boot, lasso, star, saloon doors, wagon | Rocket, saucer, planet, helmet, telescope | Pumpkin, witch hat, cauldron, coffin, black cat |
| Every object belongs to this topic, not the wider collection | No reels or popcorn | No reels or popcorn | No reels or popcorn |
| Mixes small things with big ones | Hat to steam train | Meteor to moon base | Candelabra to haunted house |
| All four art categories, with few of category 2 | 4/1/3/2 | 4/1/3/2 | 3/2/3/2 |

The film genre sets carry the idea through objects alone, as the brief asks: no gold cards and no characters. Horror leans Halloween, the user's choice, and differs from Playrix's own Horror set, which uses dolls, masks and mirrors ([research](../research/card-sets-in-real-games.md)).

## Set numbers

| Set | Title words | Name words | Object classes | Scales | Backdrop hues | Categories 1/2/3/4 | Style similarity |
|---|---:|---:|---:|---:|---:|---|---:|
| Sports | 1 | 2 | 4 | 2 | 6 | 3/1/3/3 | 0.613 |
| Finals | 1 | 2 | 6 | 2 | 6 | 4/1/4/1 | 0.603 |
| Coolness | 1 | 2 | 6 | 2 | 7 | 2/2/2/4 | 0.610 |
| Countrystead | 1 | 2 | 7 | 5 | 6 | 1/2/2/5 | 0.641 |
| **Western** | 1 | 2 | 7 | 4 | 5 | 4/1/3/2 | 0.602 |
| **Sci-Fi** | 1 | 2 | 7 | 5 | 6 | 4/1/3/2 | 0.658 |
| **Horror** | 1 | 2 | 7 | 4 | 7 | 3/2/3/2 | 0.572 |

Our sets sit inside or at the edge of the real ranges. Horror is the least unified by style similarity, close to the 0.57 of random real cards, because its objects vary most in material. Western has fewer backdrop hue bins, although yellow and orange share a bin, and it reads as six colors on screen.

## Art

Measured rows count our earlier cards: these sets and the first batch, as in [SYNTHESIS](SYNTHESIS.md#second-pass-2026-11-06) and `experiments/batch2_check.py`.

| Principle in the references | In our earlier cards | Since |
|---|---|---|
| Real proportions, simplified but not inflated | Followed; objects still slightly plumper | |
| Thin parts stay thin | Followed on straps, spurs, candle arms and rails | |
| Materials read as themselves, with quiet detail | Followed: leather, brass, enamel, wood, canvas | |
| One clear soft light, form turns smoothly | Followed | |
| Backdrop against the hero's color temperature, never its hue | Partly: ours were more saturated and more opposed, backdrop chroma 0.180 against 0.143 | The planner states the real rule; batch 2 measured 0.160 against 0.153 |
| Three-quarter view, even for symmetric objects | Not followed: a near-mirror silhouette on 9 of 17 first-batch cards against 13 of 67 real | Batch 2: 2 of 16 |
| A pool of light behind the object, darker corners | Not followed: 11 of 23 against 39 of 52 real | Still not: the image model ignores the words |
| Category 4 is the object's exact spot, close, often cut by the card edge | Partly: our scenes are wider, cut on 2 of 13 against 17 of 42 real | Close spots in the plan; edge cuts still rare |
| Tone-on-tone patterns: rays, rings, stripes, waves, diamonds | Followed | |
| No text, frame or outline | Followed | |

## Where we still differ

- **Objects:** Coffin and Tombstone are in the Horror set; the producer has since ruled out death and religious symbols. The third variants of Horror and Sci-Fi were weaker in idea (Armchair, Rocking Horse and Space Food fit only beside the others), which became a planning lesson.
- **By eye:** real cards look a little softer and quieter than ours; ours are slightly tidier.
- **Classifier:** a DINOv3 classifier still separates real cards from their redraws (AUC 0.84 whole card; old style 0.86). Whether a viewer sees what it sees is untested.
- **Blind review:** on unseen same-object pairs, specialists are at chance: right 47% of the time when they choose a side, against 71% for the old style.
- **Rating:** the producer graded these 30 cards 3.4 of 5 beside their references and still spots 24 of 32 final-style twins ([STYLE_GAPS](STYLE_GAPS.md)). The other numbers above come from models or measurement.
