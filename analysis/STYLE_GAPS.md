# Style gaps and what closed them

Why the first cards looked off, how that was measured, and what fixed it. Human grades are the producer's (see the README glossary); model results are named as such. Numbers trace to `runs/` and the scripts in `experiments/`.

## What holds now

- **The producer is the measure.** Blind, they find our drawing in 24 of 32 final-style twins (31 of 32 in the old style). Model reviewers are at chance on the same pairs.
- **Style rounds stopped.** The producer rates the final style, r3 and r9 about equal, and no tone change beat the final style.
- **Construction is the main complaint, and geometry fixes it.** A Blender blockout took broken cards from 5 of 12 to none. No model judges construction above chance, so the planner models built objects and a human checks the rest.
- **Compare, never score.** No score of a lone card follows the producer's grades. The art director picks the producer's side of a pair 61% of the time, 76% when confident; CSD against the same object's real card agrees above chance.
- **The plan decides most of the card.** Batch grades rose from 3.63 to 3.97 through object choice; the same objects redrawn moved by +0.11. Words do not hold a shape or a camera; a Blender model does.
- **Edits by note are a gamble.** First-round edits beat their drafts 35 of 82 times and second-round ones 0 of 11, so an edit stays only if it wins and the pipeline reviews once.
- **The game's cast stays itself on new cards** when drawn in one go with its real cutouts attached.
- **Another generator was tried.** See the generator bake-off below.

## How the gap is measured

- **Twins.** A real card redrawn from a text brief with that card hidden from the generator. Content is equal, so what differs is style. Twelve twins steered the style rounds; forty more (`runs/twins40`) test it on objects it was never tuned on.
- **Calibrated reviewers.** Without lessons, model specialists called the real card the fake 12 of 12 times on color and surface: they expect game art glossier and more saturated than it is. Four labelled twins flipped this to 7 of 8 on held-out pairs, so every review now carries labelled lessons and hidden real controls.
- **The producer's blind ratings** in `scripts/rate_ui.py`: twins, closest pick, grades 1-5 and "does it work as built". One rater; 22 cards graded twice agree at Spearman 0.68, the ceiling for any judge.
- **Pairwise judges.** Of two drawings of one object beside its real card, which is closer, asked in both orders.
- **CSD against the same object's real card**, the one embedding measure that tracks the producer. It needs a real card of the same object, so it scores twins, not new cards.

## Style text rounds, 2026-11-02 to 11-03

| Round | Style text change | Reviewers caught | Field drift | Real-likeness |
|---|---|---:|---:|---:|
| baseline | "Chunky, toy-like, very saturated, no small details" | 89% | 0.086 | 0.50 |
| r1 | True proportions, fine real detail | 61% | 0.075 | 0.65 |
| r2 | Few main parts, calm surfaces | 50% | 0.065 | 0.61 |
| r3 | Long lens, low camera | 36% | 0.077 | 0.69 |
| r4 | Close framing, side light | 47% | 0.115 | 0.58 |
| r5 | r4 without close framing | 44% | 0.066 | 0.59 |
| r6 | Distant camera, natural color | 58% | 0.092 | 0.68 |
| r7 | Hero spans four fifths of the card | 60% | 0.067 | 0.65 |
| r8 | Low camera, one soft side light | 54% | 0.063 | 0.67 |

Reviewers caught = calibrated model specialists naming the generated card; 50% is chance, and lessons sharpened between rounds. Field drift is the mean distance from the real median (0-0.5). Real-likeness is a DINOv3 classifier's score (held-out real cards: 0.72). The final style text is in `scripts/style.py`.

What the rounds fixed:

| Vector | Mismatch | Cause | Fix |
|---|---|---|---|
| Pipeline | Prompts reached the image tool rewritten, with "smooth rounded shapes" added | Codex's LLM rewrites prompts | `draw()` forces verbatim text and fails if it changed |
| Shape | Objects inflated, thin parts became sausages, rigid objects swelled like pillows | "Chunky, toy-like" in the style text | True proportions, slim named parts, small soft bevels |
| Viewpoint | Wide angle, near parts balloon, openings gape | No camera in the text | Low camera, mild perspective, rims as thin ovals |
| Composition | Hero too big, then too small | "Close" and "distant" are high-gain | A measured value: about four fifths of the card |
| Surface | One candy lacquer on every material, then too much detail | "Clean surfaces", then "fine real detail" | Each material looks like itself, a little quiet detail |
| Lighting | Each part its own sheen | No light in the text | One soft light from one side |
| Color | Every hue pushed pure, shadows hot orange | "Very saturated, bright colors" | Natural local color |
| Staging | Invented props, dioramas, busy scenes | "A few supporting objects" | "Draw only what the subject names", a close view of its spot |

**Held-out twins.** On sixteen of the forty, reviewers caught the old style 97 of 144 times and the final style 64 of 144: 71% against 47% when they chose a side. A content-matched DINOv3 classifier still separates both (AUC 0.86 old, 0.84 final, whole card), so it sees something viewers may not. GPT-6.1 specialists with the same lessons also failed to separate r8 (11 caught, 39 missed).

**The producer, blind (2026-11-03).** Of 80 twins, 16 answered "neither"; of the rest they found the generated card 31 of 32 times in the old style and 24 of 32 in the final style. They named: toy-like roundness and gloss short of the real cards' "grounded realism" (real cards look like rendered 3D models, ours like illustrations of 3D), objects that could not work, and parts seen from different cameras.

**Closest style (36 twins).** Picked closest among old, final, r3 and r9: r3 15, final 10, r9 10, old 1. Old is out (p 0.02 for r3 against chance); r3's lead over final and r9 is weak. So the three count as one band and style rounds stopped. The model reviewers had called r3 "too realistic"; the producer preferred it.

**What did not help.** More wording (each sentence is high-gain); softening the export (spectra already match); specialists studying real cards alone (they wrote "clay-like toy"); geometry overlays for reviewers (construction 9 of 16 caught instead of 11, more false alarms: models read the marks as proof); outline roundness measures (no separation at 430×480).

## Construction

**Trial, 2026-11-03** (`experiments/trial.py`). Six twins, two draws each, four arms, graded blind:

| Arm | Works / slightly off / broken | Mean grade |
|---|---|---:|
| The brief as drawn | 4 / 3 / 5 | 2.2 |
| Plus one line on how it works | 2 / 7 / 3 | 2.2 |
| Blender blockout, restyled | 6 / 5 / 1 | 3.1 |
| Blockout, models fixed | 10 / 2 / 0 | 3.7 |

A blockout fixes construction (0 broken against 5, Fisher p 0.04), mostly on multi-part structures: chair, clock and pier rose 3 to 3.5 grades. The fixed models had seen the real cards, but the first blockout arm had not and still won. A line on how the object works did nothing. The restyle copies the model, flaws included, and drops what the model lacks, such as printed calculator keys.

**Redraw from blockouts, 2026-11-04.** The 30 earlier final cards redrawn from blockouts lost 7 to 15 (8 ties): they won on built things (saddle, badge, telescope) and lost on simple forms (boot, witch hat, cat), which came out "too glossy, looks like a statue". A matte render lost the designed shape instead (`experiments/trial2.py`), and photos taught engineering truth that reads as wrong, such as smaller front wagon wheels. So the planner models built, multi-part objects only; on the 30 cards that rule matched the producer's preference 16 of 22 times.

**Checkers removed, 2026-11-05.** On 93 pairs the producer labelled works or broken, every model judge was at chance (construction checker 42 of 86, director 39 of 83), confident or not (`experiments/prefer.py`). They prefer the drawing with more hardware; the producer judges whether the whole object could work.

**Geometric check.** `scripts/blockout.py` reports hero parts that touch nothing holding them. Over 200 model files it found early-round gaps the modeller had fixed and three parts that float by design; no final model had a loose part. A guard, not a measured gain.

## What scores cannot do

- **Lone scores** (`experiments/score.py`, 129 graded cards): specialists, the director, CSD to the nearest real cards and a DINOv3 classifier all have Spearman about 0 with the producer's grades. Reviewers score hidden real cards lowest. Whole-card embeddings measure content.
- **Pairs work** (`experiments/prefer.py`, 218 pairs the producer decided): director 61%, shape specialist 63%, CSD 59%, all above chance; the director at confidence 4 is right 37 of 49 times. `choose()` therefore picks pairwise, both orders, and flags close wins for a human.
- **Tuning the director overfits** (`experiments/tune.py`): 65 to 84 of 115 on the tuning half, no gain held out, within run noise of about 5 pairs.
- **Tone parameters** (`experiments/param.py`, 69 measured parameters on 40 twins): the final style is lighter (29 of 40), with shallower darks and lower contrast. One line on deeper shade moved the darks onto the real cards on average but greyed the shadows; a second line restored their color but read glossier. The producer, blind: same 16, final 11, p2 9, p1 4. Their comments were about construction. A line that simplifies hardware into broad smooth parts (p3) fixed the treasure chest's rivets but lightened the cards further, so it was not adopted.
- **A measured backdrop grade** (`experiments/grade.py`, 2026-11-07): adding the real-twin lightness gap by distance from the object to the twins' backgrounds, fitted on one half and applied to the other, moved CSD from 0.910 to 0.909 (21 of 40 closer, p 0.82). Not adopted.

## The brief decides the drawing

- **References move drawings little.** Search-picked references were nearer the hidden card, yet the drawings came out no closer (CSD 19 of 40, director 16 to 24 against), and five references instead of three were a lean, not a gain (26 of 40, p 0.24). So search only breaks ties in the label rule, and cards keep three (`experiments/search_trial.py`).
- **The colors line outweighs the subject.** Every sheriff star got a red jewel from "with a small red gem" in its colors. "No gem" in the subject left it in 3 of 3 draws; moving the red onto the ring removed it in 3 of 3 (`experiments/plain_check.py`). The planner's accent lesson now puts the accent on a part the object has.
- **Words do not hold a shape.** "A perfect circle" left the clock twin's roundness at 0.95 against 0.995 on the real card (`experiments/shape_check.py`). A Blender model at azimuth 0 fixes the camera instead.
- **Fire takes the real card's words.** "A small orange flame" drew a tiny flame 3 of 3 times; the real Campfire Cook card's description drew a bright fire 3 of 3 (`experiments/fire_check.py`). The real fire cards as references added nothing.
- **Geometric subjects make plain objects.** The shape lesson's wording dropped the hat's badge, the boot's spur and the witch hat's bent tip in 12 of 12 draws; the earlier wording brought them back in 12 of 12 (`experiments/wording_check.py`). The producer graded the plain versions about the same (4.25 against 4.5), so a signature-details lesson waits under Proposed.
- **Cutouts lend their outfits.** Character cards copied the cutouts' costumes. One prompt line and outfit-free cutouts first fixed it for the animals; the man has no outfit-free cutout (`experiments/outfit_check.py`).

## Backdrop color, 2026-11-06

The producer asked whether the real backdrops follow a color logic (`experiments/colors.py`, `color_logic.py`, tested against the same cards with backdrops shuffled):

- **Temperature, not complements.** A warm hero sits on a cool backdrop on 84% of cards (n 94); a cool hero gets a warm one half the time. A backdrop within 30° of the hero's hue is rare: 4%, against 14% shuffled.
- **By category.** Floating objects take cyan, blue or green; plain floors the richest purple, green or pink; scenes clear cyan or blue skies. A surface often shares the backdrop's hue.
- **Ours were more saturated and more opposed** (chroma 0.180 against 0.143, median hue gap 125° against 110°), because the planner asked for "bright" and "contrasting" colors.

The planner's color rules now state the temperature rule, the colors by category and "rich and clean, never neon". On the next batch, floating objects took cool backdrops 8 of 9 times (real 25 of 35) and backdrop chroma fell to 0.160 (real 0.153 on the same categories).

## Batches graded by the producer, 2026-11-06

Variant 1 of each film genre, drawn with the producer's lessons, graded in the Cards tab (not blind):

| | Western | Sci-Fi | Horror | Mean |
|---|---:|---:|---:|---:|
| Batch 1 | 4.1 | 3.6 | 3.2 | 3.63 |
| Batch 2: color logic and the second reference pass | 4.0 | 4.1 | 3.8 | 3.97 |

- **Batch 2 measured closer** (`experiments/batch2_check.py`): objects turn into three-quarter view (near-mirror silhouettes 2 of 16 against 9 of 17; real 13 of 67) and floating objects take the real cards' cool backdrops. The light pool behind objects and the card edge cropping scenes did not take: the image model ignored those words.
- **The gain came from object choice.** The 18 objects drawn in both batches moved by +0.11; swaps did the rest (Teleport Pod 2 to Glow Flask 5, Candy Corn 2 to Crystal Ball 4).
- **Low grades name the plan.** An invented planet icon on a star map, landing legs on a flying saucer, a door handle in the middle of a door, saloon doors seen from inside, and four objects that failed twice (lasso, horseshoe, grounded rocket, cauldron over a fire). Each became a lesson in `analysis/lessons.md`.

## The cast on new cards, 2026-11-05

Six character cards, four ways, two draws each (`experiments/cast_trial.py`), graded blind by the producer:

| Arm | How | Works | Mean grade |
|---|---|---:|---:|
| direct | the card in one go, real cutouts attached first | 8 of 12 | 3.8 |
| figure | the character pre-drawn alone, then attached | 2 of 11 | 2.4 |
| paste2 | the figure pasted on a drawn setting, then redrawn | 4 of 11 | 1.8 |
| paste | the same, scaled by outline | 0 of 11 | 1.5 |

Identity held in every arm (each figure nearest its own cast member in DINOv2). Pasted figures stayed small and stood in front of their settings; drawn alone, a figure cannot know the counter it should lean on. So `make_set.py --cast N` draws character cards directly.

## Generator bake-off, 2026-11-07

Results pending; see `experiments/generators.py`.

## Limits

One human rater. Model reviewers are not a gate: on pairs of different objects they also accuse hidden real cards. Reference cards are 430×480, so fine texture is out of reach. Draw-to-draw variation is as large as most single-line style changes.
