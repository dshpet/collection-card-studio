# Our sets against the references

The three final sets are in `runs/final/`, one folder per set with a sheet beside it. Evidence for the style is in [STYLE_GAPS.md](STYLE_GAPS.md). Set numbers come from `scripts/compare.py`, on the definitions used for the real sets.

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

| Principle in the references | In our sets |
|---|---|
| Real proportions, simplified but not inflated | Followed. Objects are still very slightly plumper than real ones |
| Thin parts stay thin | Followed on straps, spurs, candle arms and rails |
| Materials read as themselves, with quiet detail | Followed: leather, brass, enamel, wood, canvas |
| One clear soft light, form turns smoothly | Followed |
| Bright, clean backdrops in a color that opposes the hero | Followed after a planner fix |
| Tone-on-tone patterns: rays, rings, stripes, waves, diamonds | Followed |
| Category 4 stays large and simple, a few quiet shapes | Followed. Saloon-type scenes are the busiest |
| No text, frame or outline | Followed |

## Where we still differ

- **Variants:** the third variant of Horror and of Sci-Fi is weaker in idea. Armchair, Rocking Horse and Space Food fit the topic only beside the others. The planner now asks for objects that name the topic on their own.
- **By eye:** real cards look a little softer and quieter than ours. Ours are slightly tidier.
- **Classifier:** a DINOv3 classifier still separates real cards from their redraws, at AUC 0.84 on the whole card. The old style scored 0.86. Style moved less on this measure than by eye, so part of the gap may be a generator fingerprint no viewer would see, but that is not proven.
- **Blind review:** on unseen same-object pairs, specialists are at chance: right 47% of the time when they choose a side, against 71% for the old style. On pairs of different objects they pick the generated card 75% of the time, but they also accuse a real card on 59-69% of hidden real controls, so that number is weak.
- **Rating:** no human has judged these cards. Every number above comes from models, which were wrong about this style once already.
