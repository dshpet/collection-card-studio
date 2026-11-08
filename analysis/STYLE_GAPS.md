# Style gaps

Why the first cards looked off, how the gap was measured, and what narrowed it. Human grades are the producer's unless noted; model results are named as such. Numbers trace to `runs/` and the scripts in `experiments/`. The short version is in [PROCESS.md](../PROCESS.md).

## How the gap is measured

- **Twins.** A real card redrawn from a text brief with that card hidden from the generator. The object is the same, so what differs is mostly style, though pose and framing differ too. Twelve twins steered the style rounds; forty more (`runs/twins40`) first tested the result on objects it was not tuned on. Later rounds (`r9`, `p1`-`p3`, the overnight arms) were chosen on those forty too, so no untouched hold-out remains.
- **Calibrated reviewers.** Without lessons, model specialists called the real card the fake 12 of 12 times on color and surface: they expect game art glossier and more saturated than it is. Four labelled twins flipped this to 7 of 8 on held-out pairs, so every review now carries labelled lessons and hidden real controls.
- **The producer's blind ratings** in `scripts/rate_ui.py`: twins, closest pick, grades 1-5 and "does it work as built". One rater; 22 cards graded twice agree at Spearman 0.68, a measure of how repeatable those grades are.
- **Pairwise judges.** Of two drawings of one object beside its real card, which is closer, asked in both orders.
- **CSD against the same object's real card**, the one embedding measure that tracks the producer. It needs a real card of the same object, so it scores twins, not new cards.

## Style text rounds

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

**The producer, blind.** Of 80 twins, 16 answered "neither"; of the rest they found the generated card 31 of 32 times in the old style and 24 of 32 in the final style. They named: toy-like roundness and gloss short of the real cards' "grounded realism" (real cards look like rendered 3D models, ours like illustrations of 3D), objects that could not work, and parts seen from different cameras.

**Closest style (36 twins).** Picked closest among old, final, r3 and r9: r3 15, final 10, r9 10, old 1. Old is out (p 0.02 for r3 against chance); r3's lead over final and r9 is weak. So the three count as one band and style rounds stopped. The model reviewers had called r3 "too realistic"; the producer preferred it.

**What did not help.** More wording (each sentence is high-gain); softening the export (spectra already match); specialists studying real cards alone (they wrote "clay-like toy"); geometry overlays for reviewers (construction 9 of 16 caught instead of 11, more false alarms: models read the marks as proof); outline roundness measures (no separation at 430×480).

## Construction

**Trial** (`experiments/trial.py`). Six twins, two draws each, four arms, graded blind:

| Arm | Works / slightly off / broken | Mean grade |
|---|---|---:|
| The brief as drawn | 4 / 3 / 5 | 2.2 |
| Plus one line on how it works | 2 / 7 / 3 | 2.2 |
| Blender blockout, restyled | 6 / 5 / 1 | 3.1 |
| Blockout, models fixed | 10 / 2 / 0 | 3.7 |

A blockout fixes construction (0 broken against 5, Fisher p 0.04), mostly on multi-part structures: chair, clock and pier rose 3 to 3.5 grades. The fixed models had seen the real cards, but the first blockout arm had not and still won. A line on how the object works did nothing. The restyle copies the model, flaws included, and drops what the model lacks, such as printed calculator keys.

**Redraw from blockouts.** The 30 earlier final cards redrawn from blockouts lost 7 to 15 (8 ties): they won on built things (saddle, badge, telescope) and lost on simple forms (boot, witch hat, cat), which came out "too glossy, looks like a statue". A matte render lost the designed shape instead (`experiments/trial2.py`), and photos taught engineering truth that reads as wrong, such as smaller front wagon wheels. So the planner models built, multi-part objects only; on the 30 cards that rule matched the producer's preference 16 of 22 times.

**Checkers removed.** On 93 pairs the producer labelled works or broken, every model judge was at chance (construction checker 42 of 86, director 39 of 83), confident or not (`experiments/prefer.py`). They prefer the drawing with more hardware; the producer judges whether the whole object could work.

**Geometric check.** `scripts/blockout.py` reports hero parts that touch nothing holding them. Over 200 model files it found early-round gaps the modeller had fixed and three parts that float by design; no final model had a loose part. A guard, not a measured gain.

## What scores cannot do

- **Lone scores** (`experiments/score.py`, 129 graded cards): specialists, the director, CSD to the nearest real cards and a DINOv3 classifier all have Spearman about 0 with the producer's grades. Reviewers score hidden real cards lowest. Whole-card embeddings measure content.
- **Pairs work** (`experiments/prefer.py`, 218 pairs of 59 objects the producer decided): director 61%, shape specialist 63%, CSD 59%. Resampled by object, the 95% intervals are 54-69%, 55-71% and 49-69%, so the director and the shape specialist beat chance and CSD only leans. The director at confidence 4 is right 37 of 49 times. `choose()` therefore picks pairwise, both orders, and flags close wins for a human.
- **Hubness-corrected CSD** (CSD+, `experiments/csd_plus.py`): subtracting each drawing's similarity to its nearest real cards moved agreement from 128 to 132 of 218 pairs, all on closest picks. A lean within noise, with k chosen from three; not adopted.
- **Edits by note.** The director judged first-round edits better than their drafts 135 of 263 times and second-round ones 0 of 11, so an edit stays only if it wins and the pipeline reviews once.
- **Tuning the director overfits** (`experiments/tune.py`): 65 to 84 of 115 on the tuning half, no gain held out, within run noise of about 5 pairs.
- **Tone parameters** (`experiments/param.py`, 69 measured parameters on 40 twins): the final style is lighter (29 of 40), with shallower darks and lower contrast. One line on deeper shade moved the darks onto the real cards on average but greyed the shadows; a second line restored their color but read glossier. The producer, blind: same 16, final 11, p2 9, p1 4. Their comments were about construction. A line that simplifies hardware into broad smooth parts (p3) fixed the treasure chest's rivets but lightened the cards further, so it was not adopted.
- **A measured backdrop grade** (`experiments/grade.py`): adding the real-twin lightness gap by distance from the object to the twins' backgrounds, fitted on one half and applied to the other, moved CSD from 0.910 to 0.909 (21 of 40 closer, p 0.82). Not adopted.

## The brief decides the drawing

- **References move drawings little.** Search-picked references were nearer the hidden card, yet the drawings came out no closer (CSD 19 of 40, director 16 to 24 against), and five references instead of three were a lean, not a gain (26 of 40, p 0.24). So search only breaks ties in the label rule, and cards keep three (`experiments/search_trial.py`).
- **The colors line outweighs the subject.** Every sheriff star got a red jewel from "with a small red gem" in its colors. "No gem" in the subject left it in 3 of 3 draws; moving the red onto the ring removed it in 3 of 3 (`experiments/plain_check.py`). The planner's accent lesson now puts the accent on a part the object has.
- **Words do not hold a shape.** "A perfect circle" left the clock twin's roundness at 0.95 against 0.995 on the real card (`experiments/shape_check.py`). A Blender model at azimuth 0 fixes the camera instead.
- **Fire takes the real card's words.** "A small orange flame" drew a tiny flame 3 of 3 times; the real Campfire Cook card's description, with "big", drew a bright fire 3 of 3, judged by eye and one pixel measure (`experiments/fire_check.py`). The lesson drops "big"; with it, batch 2's campfire got 5 and its cauldron 1 ("Fire is off"). The real fire cards as references added nothing.
- **Geometric subjects make plain objects.** The shape lesson's wording dropped the hat's badge, the boot's spur and the witch hat's bent tip in 12 of 12 draws, read by eye; the earlier wording brought them back in 12 of 12 (`experiments/wording_check.py`). The producer graded the plain versions about the same (4.25 against 4.5) and accepted the signature-details lesson.
- **Cutouts lend their outfits.** Character cards copied the cutouts' costumes. One prompt line and outfit-free cutouts first fixed it for the animals; the man has no outfit-free cutout (`experiments/outfit_check.py`).

## Backdrop color

The producer asked whether the real backdrops follow a color logic (`experiments/colors.py`, `color_logic.py`, tested against the same cards with backdrops shuffled):

- **Temperature, not complements.** A warm hero sits on a cool backdrop on 84% of cards (n 94); a cool hero gets a warm one half the time. A backdrop within 30° of the hero's hue is rare: 4%, against 14% shuffled.
- **By category.** Floating objects take cyan, blue or green; plain floors the richest purple, green or pink; scenes clear cyan or blue skies. A surface often shares the backdrop's hue.
- **Ours were more saturated and more opposed** (chroma 0.180 against 0.143, median hue gap 125° against 110°), because the planner asked for "bright" and "contrasting" colors.

The planner's color rules now state the temperature rule, the colors by category and "rich and clean, never neon". On the next batch, floating objects took cool backdrops 8 of 9 times (real 25 of 35) and backdrop chroma fell to 0.160 (real 0.153 on the same categories).

## Batches graded by the producer

Variant 1 of each film genre, drawn with the producer's lessons, graded in the Cards tab (not blind):

| | Western | Sci-Fi | Horror | Mean |
|---|---:|---:|---:|---:|
| Batch 1 | 4.1 | 3.6 | 3.2 | 3.63 |
| Batch 2: color logic and the second reference pass | 4.0 | 4.1 | 3.8 | 3.97 |

- **Batch 2 measured closer** (`experiments/batch2_check.py`): objects turn into three-quarter view (near-mirror silhouettes 2 of 16 against 9 of 17; real 13 of 67) and floating objects take the real cards' cool backdrops. The light pool behind objects and the card edge cropping scenes did not take: the image model ignored those words.
- **Where the gain came from.** Of the 10 points gained over 30 cards, the three character cards brought 5 (5, 2, 3 to 5, 5, 5), swapped objects 3 (Teleport Pod 2 to Glow Flask 5, Candy Corn 2 to Crystal Ball 4) and the 18 objects drawn in both batches 2, +0.11 each. Object cards alone went from 3.67 to 3.85.
- **Low grades** traced to the plan: an invented planet icon on a star map, landing legs on a flying saucer, a door handle in the middle of a door, saloon doors seen from inside, and four objects that failed twice (lasso, horseshoe, grounded rocket, cauldron over a fire). Each became a lesson in `analysis/lessons.md`.

## The cast on new cards

Six character cards, four ways, two draws each (`experiments/cast_trial.py`), graded blind by the producer:

| Arm | How | Works | Mean grade |
|---|---|---:|---:|
| direct | the card in one go, real cutouts attached first | 8 of 12 | 3.8 |
| figure | the character pre-drawn alone, then attached | 2 of 11 | 2.4 |
| paste2 | the figure pasted on a drawn setting, then redrawn | 4 of 11 | 1.8 |
| paste | the same, scaled by outline | 0 of 11 | 1.5 |

Identity held in every arm (each figure nearest its own cast member in DINOv2). Pasted figures stayed small and stood in front of their settings: a figure drawn alone does not fit the setting it should lean on. So `make_set.py --cast N` draws character cards directly.

## Generator bake-off

Every style result above came from one generator, so two others drew the twins from the same prompts and the same three references (`experiments/generators.py`). Codex's arm is its final-style draws. Judged by CSD against each twin's own real card and by the art director, pairwise in both orders with the real card shown.

| Arm | Twins | CSD to own real card, Codex / arm | Arm closer by CSD | Director: Codex / arm |
|---|---:|---|---:|---|
| Nano Banana Pro, through the Antigravity CLI | 11 | 0.914 / 0.897 | 5 (p 0.46) | 11 / 0 (p 0.001) |
| Qwen-Image-2.1, open weights on this GPU, 640 px | 40 | 0.910 / 0.815 | 2 (p < 0.001) | 39 / 1 (p < 0.001) |

- **Nano Banana Pro loses.** Its cards are darker, less saturated and more photographic: a realistic folded map, a flat calculator, a dim jellyfish. Antigravity's image agent rewrites the prompt, so this tests the system, not only the model; its daily image quota stopped the arm at 11 twins.
- **Qwen-Image-2.1 loses more clearly.** The palette and patterns are right, but objects sit small in the frame, and it breaks hard rules Codex keeps: a drawn card frame on the drink, printed text on the phone booth. It ran at 640 px: at 1024 px with three references its latents turned NaN on this ROCm card under every attention backend. The prompts were written for Codex, so a prompt tuned for Qwen, or a style LoRA, could narrow the gap.
- **Codex stays.** Both other models drew further from the real cards, so another generator would not remove the look the producer still spots.

## An outside artist on the pre-final sets

A UI designer with an art background, new to the project (`experiments/outside_rating.py`, answers in `runs/prefinal/outside/`). Blind first: 72 single cards, 36 ours from five genres and the cast, each against a real card of its art category. Then the brief, the five sets and 75 genre cards plus the 6 cast cards beside their references.

- **The blind test came out inverted:** 23 of 72 right (p 0.003), AUC 0.33. The rater called 24 of 36 real cards AI and 11 of 36 of ours, at about 2 s a card, using only the middle answers. Brighter, larger and cleaner subjects were called AI (AUC 0.72 on subject chroma, 0.62 on subject area, about 0.3 on every surface-detail field), and real cards are the brighter and larger ones. Like the uncalibrated model raters, the rater accused the real cards, though for a different reason. The inversion means the two groups do look different (AUC 0.67 read the other way), but at a glance the brighter, larger real cards read as AI; the producer, who knows the game's art, attributes them correctly in 24 of 32 twins.
- **Measured gaps against the 129 real object cards** (150 of ours, AUC ours over real): fewer hue families, 2.6 against 3.9 (0.25); objects smaller in the frame, minimum margin 0.10 against 0.06 (0.72); duller subjects, chroma 0.101 against 0.130 (0.35); plainer backdrops (0.32); greyer shadows, 84% of chroma kept against 97% (0.41); simpler silhouettes (0.40). Fine texture measures the same on both.
- **Feedback after the session:** ours look grainier and more textured; the style is close but not theirs. Real cards keep large surfaces smooth and put their detail into parts, colors and silhouette; ours render the material (felt nap, leather grain, fabric weave) on simple shapes. Pixel measures at 430×480 do not separate the two, so this is judged by eye.
- **Cards:** mean grade 3.1 of 5 on the 75 genre cards (41 of them a 3, "close"). 9 were flagged broken, all on perspective or construction: brims that do not match their crowns, tables and floors at a different angle from the object. Cast cards scored best, 3.5.
- **Sets:** every variant 3 or 4 of 5, "could stand in the game with small issues". The rater kept Detective, Horror and Period Drama.

## Overnight arms before the final

One change per arm against a shared control, then one combining round (`experiments/night.py`, readings in `runs/night/read.json` and `runs/param/compare_n0_*.txt`). Twins arms redraw the forty final-style twins (`runs/twins40`); the blockout arms redraw 24 pre-final cards over their Blender models. Rule: adopt only if no other measured field moves away from the real cards and twin CSD does not drop; texture only where pixels and the judge agree. Flat share is the share of surface pixels with local lightness deviation under 0.004 (`experiments/smooth_check.py --flat`), the pixel measure of the grain the outside artist saw. The judge is the art director model reading pairs with the real card as the target; the producer's looks are named as such.

| Arm | What changed | Evidence | Verdict |
|---|---|---|---|
| Smooth, first wording | material line: "by its color and sheen ... large surfaces stay smooth, no grain, weave, nap or pores" | flat-share gap −0.109 to −0.032 (nearer on 22 of 40); the judge saw less texture, but more gloss (17/8 to 21/4 more/less than real), shadow depth and backdrop edges away (p 0.05 and 0.03), CSD closer on 15 of 40 | dropped |
| Smooth, no "sheen" | the same line without "and sheen" | flat-share gap −0.109 to −0.030 (nearer on 27 of 40, p 0.002); judge 9/9 to 3/14 more/less textured than real; gloss to the judge unchanged (18/6 to 19/5); CSD closer on 21 of 40 (0.908 to 0.906); no field away at p < 0.05 | **adopted** for cards drawn from text |
| The same over blockouts | the line in the blockout prompt, with the framing below | less textured to the judge, 13 to 3, and by pixels; but glossier to the judge, 14 to 0, while pixel gloss fell | blockout prompt unchanged |
| One camera | "every rim, brim, opening and tabletop opens by the same amount" | 3 of 55 fields away at p < 0.05, about chance; CSD closer on 16 of 40; no measure reads perspective. The producer, blind: the control closer to the real card on 6 of 11 twins, one camera on 2 | dropped |
| Planner colors, dark parts in rich hues | hero colors with no black or dark brown | CSD closer on 14 of 40; glossier (p 0.01) | dropped |
| Planner colors, rich | also: the main body takes a rich, saturated hue, white and grey only on small parts | CSD closer on 29 of 40 (0.836 to 0.857), lightness closer on 26 of 40, no field away | **adopted** in the planner |
| Framing | blockouts framed at the real cards' median size per category (×1.04 to ×1.12) | subject area up on 24 of 24, overshooting the real median (0.354 against 0.324); more texture to the judge, 10 to 2 | **adopted at half**, categories 2-4 only (×1.035, ×1.05, ×1.06) |
| Perspective | the camera line, and Blender models for broken cards without one, on the nine pre-final cards graded broken | no model or pixel judge reads construction. The producer, blind: the current pipeline works on 6 of 9 (1 broken), the camera line on 4 of 9 (2 broken), new models on 1 of 4; against the current pipeline on the same card, the camera line was worse on 4 and better on 1, the models worse on 3 of 4 | dropped |

Palette arms replan colors from colorless subjects, so they sit below the control by CSD (0.836 against 0.908); they are compared with each other. Combined, rich colors with the smooth line held CSD (21 of 40); three of its 15 fields moved at p < 0.05, two of them opposite to the same arm on the control: noise.

The producer's blind look at the adopted smooth line, on 12 twins beside the control and the real card: closer to the real card on 3, the control on 1, the same on 6. As built, the control was better on 4 of 8, the smooth line on 1: the line stays, and construction stays the geometry's job.

Research beside the arms (`research/README.md`): a one-camera fit (GeoCalib) does not find the cards called off in perspective; blockout drawings keep the render's outline whether broken or not, so breaks sit in the render or a surface the drawing adds; edge-preserving smoothing after drawing restores flat share but not CSD.

The final sets (`runs/final3`) are drawn with the adopted smooth line, rich colors and fill; the fix rounds (`runs/final4` to `runs/final6`) changed plans, notes and models, not the style text. `runs/final2` holds the same plans drawn without the smooth line, stopped early. The cast cards were first drawn there, and their prompt has no material line.

## Limits

One producer and one outside rater. Model reviewers are not a gate: on pairs of different objects they also accuse hidden real cards. Reference cards are 430×480, so fine texture is out of reach. Draw-to-draw variation is as large as most single-line style changes.
