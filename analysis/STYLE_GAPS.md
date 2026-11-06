# Style mismatches and fixes

The first run looked off to a human, yet every automatic check passed it. This file records what was wrong, why the checks missed it and what fixed it, in date order. Ratings are the user's unless a model is named.

## What holds now

- **The user is the measure.** They still spot 24 of 32 final-style twins, where model reviewers are at chance. No score of a lone card follows their grades.
- **Style is settled as a band.** The final style, r3 and r9 are near ties for the user, and no tone round beat the final style.
- **Construction is the main complaint.** Blender blockouts fix built, multi-part objects and take the charm out of simple forms, so the planner models only built objects. No model judges construction above chance.
- **Comparison works where scores fail.** The art director picks the user's side of a pair 61% of the time, about 77% when confident. CSD against the same object's real card agrees with the user's closest pick above chance.
- **Edits by note mostly hurt.** 16 of 22 lost to their drafts, and a second round kept none, so an edit stays only if it wins and the pipeline reviews once.
- **The brief decides the drawing.** Search-picked references, and five instead of three, drew no clearly closer to hidden cards. Within the brief, the colors line outweighs the subject: an accent named as a gem draws a gem even when the subject says no gem. Words do not hold a shape or a camera; a Blender model does.
- **The game's cast can be drawn on new cards and stay itself,** best in one go with its cutouts attached.

## How the gap was measured, 2026-11-02

**Twins.** Twelve real cards were redrawn from a text brief, with the card itself hidden from the generator. Content is equal, so what remains is style.

**Blind pairs.** Specialists see a real card and its twin in random order and name the generated one. 50% is chance.

**Reviewers were calibrated first.** Without lessons, they picked the real card as the fake 12 of 12 times on color and surface. They could see the difference, but they expected game art to be glossier and more saturated than it is. Four labelled twins flipped this to 7 of 8 on held-out pairs.

Lessons changed between rounds, so reviewers got sharper as cards improved. Catch rates are not strictly comparable across rounds. Drift and likeness are.

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

Field drift is the mean distance from the real median, 0 to 0.5. Real-likeness comes from a DINOv3 classifier of real cards against the first run. Held-out real cards score 0.72.

Below 50% means reviewers mistook the real card for the fake: r3 went past the target, into realism. That bracket located the target between r2 and r3. The real look is simplified but not inflated.

**Held-out objects.** The twelve twins steered every style decision, so forty more real cards were redrawn in the old and the final style. On sixteen of them, reviewers caught the old style 97 of 144 times and the final style 64 of 144. When they chose a side, that is 71% against 47%. So the final style holds on objects it was never tuned on, and the reviewers can still see the difference when there is one. Slight tells remain on color and shape, at 11 and 10 of 16.

**Content-matched classifier.** On all forty, with each real card and its redraw kept in one fold, DINOv3 separates the old style at AUC 0.86 whole, 0.82 subject and 0.83 background, and the final style at 0.84, 0.80 and 0.76. Style moved less here than for reviewers and by eye, and a classifier can still tell. Without twins this test misleads: summer against genre content gave 0.95 for both the first run and the final sets.

**Second vendor.** With the same lessons, GPT-6.1 specialists caught baseline 46 times and missed 6, abstaining 20 times. On r8 they caught 11 and missed 39, abstaining 22. So an unrelated model also fails to separate r8, and leans slightly toward calling the real card the fake.

## Mismatches found, 2026-11-02

| Vector | Mismatch | Cause | Fix |
|---|---|---|---|
| Pipeline | Prompts reached the image tool rewritten, with added "smooth rounded shapes" | Codex's LLM rewrites prompts. `--ephemeral` hid it | `draw()` forces verbatim text and fails if it changed |
| Shape | Objects inflated, thin parts became sausages | Style text said chunky, toy-like, no thin parts | True proportions, named slim parts, small soft bevels |
| Shape | Rigid objects swollen like pillows | Same | Same |
| Viewpoint | Wide-angle view, near parts balloon, openings gape | No camera in the text. "Close" made it worse | Low camera, mild perspective, rims as thin ovals |
| Composition | Hero too big, then too small | Words like "close" and "distant" are high-gain | A measured value: spans about four fifths of the card |
| Surface | One candy lacquer on every material | "Clean surfaces with soft highlights" | Each material looks like itself. Cloth, cord and wood are matte |
| Surface | Then too much detail: rivets, tread, grain | "Fine real detail" overshot (r1) | "A little quiet detail" |
| Lighting | Each part got its own sheen, even frontal light | No light in the text | One soft light from one side |
| Color | Every hue pushed pure, shadows hot orange | "Very saturated, bright colors" | Natural local color. Saturation words removed |
| Color | Dull backdrops on new sets | Planner chose dusty, muted colors. Twins inherited real ones, so only new sets showed it | Planner rule, from the hues real backdrops use |
| Staging | Invented props, dioramas, little islands | Environment rule invited "a few supporting objects" | "Draw only what the subject names", close view of the object in its place |
| Staging | Environment cards too detailed | Same, plus no limit on scene size | Hero large and central, setting of a few large soft shapes |
| Identity | A poster needing the word WANTED came out blank | Style forbids text | Planner skips objects that need readable words |

## What did not help, 2026-11-02 to 11-03

- **More wording.** Each sentence is high-gain: "nearly touching the edges" took hero area from percentile 0.56 to 0.91. The art director's rewrites swung between too toy and too realistic, so the final text was settled by hand from the evidence.
- **Softening the export.** Real and generated spectra already match in every band, so a blur would add a mismatch.
- **Reference-only study.** Specialists working from real cards alone wrote "clay-like toy" and "never stitching", though the real Baseball Mitt has stitching.
- **The old correction rounds.** They rescued 8 of 24 cards. Edit mode replaced them.
- **Geometry for the reviewers.** A panel of measured geometry beside each card made both checkers worse. It showed straight edges grouped by direction, curves fitted to true ellipses and the skeleton of thin parts. On the same labelled cards, construction caught 9 of 16 instead of 11, and perspective 2 of 6 instead of 6, with 8 false alarms on real cards instead of 5. Models read the marks as proof that the drawing is right. "Ratio 0.95, a near-circle at a slight angle" passed the clock the user called not round, and "parallel edges drawn parallel" passed both chess tables. New lenses for four specialists did no better than the old ones on the sixteen held-out twins, 26 caught and 31 wrong against 31 and 28. Those lenses were normals with the outline's bends, edges and ellipses, lines of equal shading, and a vectorscope. The panel code is in commit 3efa3bf.
- **Outline measures of roundness.** Straight share, corner rate, corner radius and planar share do not separate real cards from their twins. In both styles the twin scores higher 16 to 24 times in 40, and 8 times in the 16 with normals. The roundness a person sees is not in the outline at 430×480.

## Human rating, 2026-11-03

The user rated all 80 blind twins with `scripts/rate_ui.py`. They found the generated card 31 of 32 times in the old style and 24 of 32 in the final style, choosing a side each time. Model reviewers were at chance on the same final style. **So the final style is closer, but a person still sees through most of it, and the models do not.** Every model result below should be read with that in mind.

What the user named:
- **Style:** too round, glossy and toy-like, short of the real cards' grounded realism. The real cards look like rendered 3D models, while ours look like illustrations of 3D.
- **Construction:** objects that could not exist, such as headphone cables ending in three strands, a folding chair that could not fold, a pier that leads nowhere, ropes ending in the air.
- **Perspective:** parts seen from different cameras, such as calculator keys drawn front-on on a tilted body.

None of the nine style specialists judged construction or perspective, so two checkers were added, taught with the user's marked cards. On a full-size crop they caught 11 of 16 held-out construction errors and 6 of 6 perspective errors, and also flagged 3 and 5 of 20 real cards. They were removed on 2026-11-05, when pairs the user had labelled showed them at chance (below).

## Closest style, 2026-11-03

For 36 of the forty twins, the user picked the redraw closest to the real card among old, final, r3 and r9. One draw per style, so draw luck is part of every pick. The test forced one choice, though the user found several close to a tie, and the real cards themselves vary in style. So final, r3 and r9 count as one band, and style rounds stop here.

| Style | Picked | Matched classifier AUC, whole / subject / background |
|---|---:|---|
| r3 | 15 | 0.89 / 0.83 / 0.79 |
| final | 10 | 0.84 / 0.80 / 0.76 |
| r9 | 10 | 0.82 / 0.82 / 0.70 |
| old | 1 | 0.86 / 0.82 / 0.83 |

- **Old is out.** r3 is the only style picked above chance (p 0.02), but its lead over final and r9 is weak: odds 1.5 and 1.2 to 1 after screen position, and r3 beats final in 79% of bootstrap resamples.
- **Position bias.** Redraw 4 sat alone on a second row and was picked 17 times where 9 were expected. It was spread across styles, so the order holds. A repeat should fit one row.
- **Reviewers had the direction wrong.** They said r3 went past the target into realism. The user prefers it, so the target is at r3 or beyond, not between r2 and r3.
- **No measure follows the user.** The classifier ranks r3 farthest, and its subject scores are flat, so it reacts to backgrounds and framing. Silhouette area and fill pick the user's choice 10 of 36 times, about chance.
- **Construction is not a style problem.** Seven of ten comments name objects that could not work or sit wrong, in every style: the duck ride's handle and seat, the waterslide, the phone in the booth, the earbud cable, the map folds, spotlights hanging in space, the topiary on the path. r9's "every cable, rope, leg and hinge attaches where it should" did not prevent them. Several come from briefs that name parts but not how they connect: "a red saddle seat and red handle" became a bag handle on the saddle three times, and a setting with "a curving paved path" put the planter on the path three times.

## Construction trial, 2026-11-03

Six twins (spotlights, calculator, chair, clock, chess table, pier), two draws each, four arms, made by `experiments/trial.py`. The user rated all 48 blind, arm hidden: does it work as built, and a grade 1-5 against the real card.

| Arm | Works / slightly off / broken | Mean grade |
|---|---|---:|
| control, the brief as drawn | 4 / 3 / 5 | 2.2 |
| how, one line on how it works | 2 / 7 / 3 | 2.2 |
| blockout, Blender model restyled | 6 / 5 / 1 | 3.1 |
| blockout2, the models fixed | 10 / 2 / 0 | 3.7 |

- **A blockout fixes construction.** blockout2 had no broken card against 5 of 12 for control (Fisher p 0.04). The gain is on multi-part structures: chair, clock and pier rose by 3 to 3.5 grades. Spotlights rose 0.5, and calculator and chess table fell 0.5, as control drew them fairly well already.
- **blockout2 is not a clean test.** Its models were fixed after seeing the six real cards. The first blockout arm was built before that look and still beat control, 1 broken against 5 (p 0.15) and 3.1 against 2.2.
- **A line on how the object works did nothing.** Words do not hold construction. Geometry does.
- **The restyle copies the model, flaws included.** It drops what the model lacks: the calculator keys came out blank ("no numbers there"). Printed marks need to be in the model or named in the prompt.
- **The checkers have no signal here.** A major flag fell on 10 of 22 working drawings and 5 of 9 broken ones. Any flag fell on 17 of 22 and 8 of 9. As a gate on any error, they would pass over most good cards.

Six objects and one rater make this a small sample.

## Redraw from blockouts, 2026-11-04

The 30 final cards, as chosen before and as redrawn from a modeller's blockout (commit 8a46e06), 60 blind and mixed.

| Arm | Works / slightly off / broken | Mean grade |
|---|---|---:|
| old | 23 / 6 / 1 | 3.4 |
| blockout | 23 / 5 / 2 | 3.0 |

- **The blockout lost on these cards.** Old won 15, blockout 7, 8 tied. It won on built things (saddle, lasso, badge, telescope) and lost on simple forms (boot, witch hat, candelabra, crystal ball, cat, barrel). These briefs had already been chosen as the best of several old draws, so the old arm had a head start.
- **The blockout carries a rendered finish.** Comments: "too glossy, looks like a statue", "too texture-y", "too 3D modelled", "a little too realistic". Real cards are smoother and more stylized, satin rather than gloss. The Blender render's clearcoat, metal reflections and raking light pass through the restyle.
- **Measures miss it.** Gloss share, highlight share and micro texture sit at the real median in both arms (percentiles 0.47 to 0.51, micro texture 0.40). The gloss the user sees is in the kind of highlight, not its area.
- **Topic.** A coffin and a tombstone with a cross may upset players. The planner should avoid death and religious symbols.

## Soft render and photos, 2026-11-04

`experiments/trial2.py`, rated blind against the old card. Finish cards, models rendered matte: soft beat old 2 times and lost 4. The cards lost designed shape with the gloss: the cat's face, the boot's tooling, the hat's curl. Matte primitives give primitive charm ("texture and color is better, but form is somewhat lacking"). Built objects: remodel 2/1/4 wins/losses/ties, photo 2/2/3, photo_style 3/2/2. The saddle rose from 2 to 5 and the cauldron stayed at 1 in every arm. Photos taught real construction that reads as wrong, such as smaller front wagon wheels and a raised dome entry with a ladder. The target is iconic logic, not engineering truth.

## Uniform scores against the user, 2026-11-04

`experiments/score.py` puts every graded card on one list (129 graded, 80 twins, 24 hidden real cards). It scores each card by embeddings, the classifier, the nine specialists (1-10 on their vector) and the art director (1-10 overall). All reviewers saw the same real cards and six graded lessons. Results are in `runs/score/summary.json`.

| Measure | Spearman with grade | Real vs drawn AUC | Predicts twins that fooled the user |
|---|---:|---:|---:|
| Specialists, mean | 0.00 | 0.40 | 0.40 |
| Art director | 0.00 | 0.38 | 0.42 |
| Best specialist (composition) | 0.16, p 0.08 | 0.45 | 0.47 |
| CSD, nearest real cards | 0.06 | 0.59 | 0.38 |
| DINOv3 classifier | 0.00 | 0.61 | 0.59 |
| CSD, own real twin | | | **0.65** |

- **The user is the ceiling.** 22 images graded twice matched 13 times, mean gap 0.55, Spearman 0.68.
- **Model reviewers rank real cards lowest,** even with graded lessons. They call them painterly, flat, pillowy or "a different style". Their idea of the game is narrower than the real set. Paired on the same object, only the director leans the right way, final above old 19 to 13 (p 0.06).
- **Distance to the real cluster measures content.** Whole-card embeddings put old twins as close as final ones or closer, and new-topic cards far from all real cards whatever their style.
- **With content held equal there is signal.** CSD puts the final twin nearer its real card than the old one in 29 of 40 (Wilcoxon p 0.0001), agrees with the user's closest pick 15 of 36 against 9 by chance (p 0.02), and predicts which twins fooled the user at AUC 0.65. It needs a real card of the same object, so it cannot score new set cards.

## Pairwise against the user, 2026-11-05

A lone 1-10 score failed, so `experiments/prefer.py` asks a different question: of two drawings of one object, beside its real card or cards, which is closer? Truth is 218 pairs the user already decided. 108 come from closest picks, 60 from the trial and 50 from set cards. The bar set before the run was about 70% agreement.

| Judge | Agrees with the user | Closest / trial / set |
|---|---:|---|
| Art director (Opus) | 132/216, 61%, p 0.001 | 72/108, 32/59, 28/49 |
| when its confidence is 4 of 5 | 37/49, 76% | |
| Shape specialist | 128/204, 63%, p <0.001 | 68/105, 35/57, 25/42 |
| Director and shape agree | 98/144, 68% | |
| Specialist majority | 121/208, 58% | |
| CSD similarity, no training | 128/218, 59%, p 0.006 | 73/108, 29/60, 26/50 |
| Probe trained on the user's pairs | 129/218, 59% | 71/108, 27/60, 31/50 |

- **Comparison works where a lone score did not.** Every reviewer is above chance on pairs, and below chance when scoring a lone card. `choose()` in `make_set.py` already compares, so it picks the user's side about 6 times in 10.
- **Confidence carries information.** The director is right 76% of the time when it says 4 of 5, on a quarter of the pairs. This cut was chosen after seeing the results, so it needs fresh pairs to confirm.
- **Viewpoint and composition are at chance.** Shape, finish, staging and value carry the signal.
- **Clear preferences are still hard.** On graded pairs two or more grades apart, often construction, CSD agrees 20 of 49 times, the director 29 of 49 and shape 30 of 46.
- **No judge reaches the bar.** Agreement is at most 63% over all pairs, against the user's own retest of 0.68 on grades.

**Automatic tuning did not generalize.** `experiments/tune.py` split the pairs by object into tuning and held-out halves. In six rounds an editor proposed one note at a time from the director's mistakes and the user's comments. Two notes were kept: prefer matte and calm over glossy, and judge overall color masses over small details. Tuning agreement rose from 65 to 84 of 115. On the held-out half the tuned director agreed 65 of 101 times, the untouched one 68 of 103 and the first run 65 of 102. The gain was fitting and run noise: one prompt varies by about 5 pairs between runs. So the notes were not installed. The second note also contradicts the user, whose comments are mostly about construction. Closest picks, half the pairs, reward overall look.

**Confidence held up.** On held-out pairs the untouched director at confidence 4 was right 10 of 13 times in a fresh run and 19 of 24 in the first, about 78%. `choose()` now asks for confidence and lists picks below 4 for a human look. The cut was set on data that includes these pairs, so it was not chosen blind.

**Construction cannot be judged by these models, even pairwise.** `prefer.py --target works` gives 93 pairs of one object whose works / slightly off / broken labels differ. Construction checker: 42 of 86. Perspective checker: 45 of 87. Director: 39 of 83. The old one-card checkers: 26 of 53. All are at chance, and confidence does not help: 3 of 8 and 11 of 23 at confidence 4. On works-against-broken pairs the construction checker gets 11 of 23. Its reasons look at local hardware ("the lifebuoy hangs from a peg", "X-legs join at clear pivots") and prefer the drawing with more of it. The user judges whether the whole object could work, and mostly preferred the plainer blockout drawings of the chair and pier. So construction has to come from geometry, the Blender blockout, and from a human look. A checker cannot guard it.

**Changes, 2026-11-05.** The construction and perspective checkers are removed from the pipeline: no candidate is passed over and no edit note is written on their word. A Blender model is now optional per card, and the planner decides with one rule: built objects of several rigid parts get a model, simple and organic forms do not. On the 30 final cards it chose a model for 18. Against the user's ratings it matched 16 of the 22 cards where one side won. It modelled candelabra, crystal ball, coffin and wagon, where the old draw won, and skipped badge and lasso, where the model won. The rule was not tuned on these cards.

## Parameter loop, 2026-11-05

The production pattern: split the style into parameters, measure each on the output, give concrete feedback, then measure again. `experiments/param.py` reads 69 parameters on the forty twins, each against its own real card. 55 come from pixels and 14 from Opus readings asked twice with sides swapped. Opus says only which card has more of a parameter, never which is right, so its taste cannot invert the result.

- **What the final style gets wrong.** It is lighter: 29 of 40 twins, p 0.0002, mostly the background (31 of 40). It has shallower darks on the object (27 of 40) and lower contrast (28 of 40). Backgrounds are more saturated (30 of 40) and less detailed (29 of 40). By eye the objects have more small details (24 to 11) and are more inflated (22 to 10).
- **What it does not get wrong.** Gloss, highlight size and tint, bevels and surface texture, by pixels and by eye. The user's "glossy" is not in any of these readings.
- **No parameter separates the twins the user caught from those that fooled them** (24 against 16). Caught twins leaned lighter, with shallower darks.
- **One change.** "turns the form smoothly into shade" became "into deep, colorful shade, so the shaded side is clearly darker than the lit side", drawn as `twins40/p1`. The object's 5th-percentile lightness went from +0.024 above its real card to 0.000, and the shallow darks dropped out of the deviation list. The deepest 1% now overshoots (-0.015). Per twin the redraw came closer only 17 to 23 times in 40, because draw-to-draw variation is as large as the shift. One side effect: shadows went greyer. Shadow chroma kept fell from -0.025 to -0.067 below real, now lower in 28 of 40, though the line said "colorful". The background stayed light, as it was not targeted.
- **Second round, p2.** p1's line plus "The shade keeps the object's own color, richer and deeper, never grey." Shadow chroma went back to the final style's level (-0.028). The object's 5th percentile stayed on the real cards (-0.005), and its shadows overshoot a little, darker in 27 of 40. A new side effect appeared: by eye p2 is more saturated (22 to 3, p 0.0002) and glossier (24 to 6, p 0.001), probably from "richer". Gloss is the user's main complaint. Pixel gloss share did not move, so again the gloss a viewer sees is not in the pixel measures.
- **The user's blind pick (40 twins, positions balanced):** same 16, final 11, p2 9, p1 4. Neither round beats the final style, so neither is adopted. p2 beat p1, which fits the real cards keeping color in their shadows. Moving tone onto the real cards' average did not make cards look closer.
- **The comments are about construction, not tone.** On 12 of 40 the user wrote that all three are bad, every time on how the object is built. Pier, chair, map folds, spotlight rail, calculator, clock, flippers' foot pockets, headphones, the phone outside its booth, the drum kit ("neuroslop"), the waterslide and the postcard's lines. These twins were drawn from text. The construction trial fixed chair, clock and pier with Blender models, which the pipeline now builds for such objects.
- **Treasure chest, named the clearest style example.** The real chest is built from a few broad, smooth gold bands, with no rivets or corner brackets. Its planks are wide and few, and its coins are fewer and larger. Shadows on the sand are tinted blue by the water, and the backdrop is a deeper, darker blue. All three redraws add rivets, brackets and plank lines, light the sand warm and even, and use a lighter cyan. This matches the eye readings ("more small details", 24 to 11) and the lighter backgrounds. The parameter is simplified hardware: fewer, larger, smoother parts.
- **Hardware round, p3, judged by readers only.** Added to the final style: "Hardware is simplified into a few broad, smooth parts: wide bands and plain caps instead of rivets, bolts, brackets and seams." Detail moved to the real cards. By eye "more small details" went from 20-10 to 13-17, and subject detail from +0.0034 to -0.0016 (closer in 24 of 40, p 0.04). The treasure chest lost its rivets and brackets. Inflation and bevels did not move. But cards got lighter (gap +0.022 to +0.033, p 0.006), with fewer darks (lower in 29 of 40) and less contrast, since rivets and seams were dark marks. The rule set before the run was to keep a change only if nothing else got worse, so p3 is not adopted. Small tone shifts were invisible to the user in the p1/p2 check, so p3 is the first candidate if another round is wanted.
- **Rater fatigue.** The user reports growing blind to differences, and 16 of 40 answers were "same". The one measure that tracks the user is wearing out.

## Pipeline test run, 2026-11-05

Western and Sci-Fi went through the current pipeline into `runs/western-2` and `runs/sci-fi-2`, one variant each, as a test. They are not the final sets. Horror was stopped at planning.

- **Literal counts.** "A covered wagon with two large spoked wheels" became a two-wheeled cart. The planner and the modeller now count parts as the whole real object has them.
- **The three-up pick followed screen position.** The director picked the second slot for ten of ten cards, always as "the largest", while subject areas differed by under 2 points. Shuffling only changed which candidate sat there. Picks are now pairwise, both orders, the framing that agreed with the user. The result is honest: candidates of one card are nearly identical, and most picks are close (8 of 10 and 6 of 10 unsure).
- **Edits mostly made cards worse.** Judged pairwise against the drawing they replaced, Western's edits lost 7 of 10, each 2-0 in both orders. Sci-Fi kept 3 of 5 in round 1 and 0 of 5 in round 2. An edit now stays only if it beats its draft.
- **Invented extras survive "draw only what the subject names".** Every sheriff star had a red jewel, which the user rejected before. It was removed by hand, which counts against autonomy. The cause was the colors line, fixed by a lesson the same night (below).
- **Characters slip in.** Sci-Fi planned a "friendly robot" and an "Alien Pet" with a face and a smile. The rule allows one animal as an object, and an alien counted as one. The movie-style reference sets have no characters.

## Reference search, 2026-11-05 night

`scripts/search.py` links text to the 160 card images with SigLIP 2, and gives a confidence for each match. Asked for "a wooden barrel" it finds Cargo Barrel at 0.75, and for a new topic's object, such as a cowboy hat, its closest real cards with a confidence near 0.

- **Hidden cards.** Each of 129 real cards was hidden and its references picked from its own description. Ranking by likeness within the backdrop pattern brought the references nearer the hidden card than matching labels did: DINOv2 subject similarity 0.124 against 0.106, CSD 0.650 against 0.627, with random picks at 0.100 and 0.598. The backdrop pattern matched as often, 0.80.
- **Drawings did not change.** The forty twins were drawn with each rule's references (`experiments/search_trial.py`). CSD put the search arm nearer the real card on 19 of 40 (p 0.35), and the director preferred the label arm 24 to 16. The mean difference, 0.003, is a sixth of the draw-to-draw spread. The brief decides the drawing, and references this similar move it little.
- **So search breaks ties only.** References keep the label rule, category then backdrop pattern then object class, and search orders the equals, which were random before. On hidden cards that keeps class and pattern as before and brings the references nearer (DINOv2 0.117).
- **No outliers to drop.** Within each category no reference card is an outlier in CSD, DINOv2 or SigLIP 2 (local outlier factor 1.44 at most), and the spaces disagree on which cards are odd. The most flagged are on-style cards with unusual staging, such as Aircon and Rock Guitar.

## The cast on new cards, 2026-11-05 night

The reference collection has one cast, cut out by `scripts/cast.py`: the man, the pig, the sheep, the cow and the rooster, 38 figures from 30 cards. Six character cards for the film genres, such as the pig lassoing its own tail or the cow in a ghost sheet, were drawn four ways, two draws each (`experiments/cast_trial.py`, 45 of 48 drawn):

| Arm | How | Director's wins against the others |
|---|---|---|
| direct | The card in one go, real cutouts of the character attached first | 31 of 32 decided duels |
| figure | The character pre-drawn alone, then the card drawn with that figure attached | 18 of 32 |
| paste2 | The pre-drawn figure pasted on a drawn setting at the real cards' size, then redrawn with small corrections | 8 of 28 |
| paste | The same, scaled by the figure's outline | 3 of 28 |

- **Identity holds in every arm.** Cut out of each result by SAM 3, every figure found was nearer its own cast member than any other in DINOv2, by a margin of 0.21 to 0.22, as the real cutouts are to each other (0.22).
- **Pasting looks pasted.** The redraw keeps the pasted size and pose, so characters stay small and stand in front of the setting rather than in it. A figure drawn without its setting cannot know the counter it should lean on: the man came out lying on the saloon bar in every arm that used his figure. One figure could not be drawn at all, twice.
- **Direct is best for the director, and by eye on par with figure.** The figure arm keeps an asked outfit better (the green hoodie), and direct composes more freely. Direct takes one step instead of three.
- **So character cards are drawn directly.** `make_set.py --cast N` plans N character cards per variant with the cast's cutouts attached. The default is 0, since the movie brief asks for no gold cards, though Music Fest shows that character cards without gold frames exist. Cards showing the cast stay out of git.
- **The producer agrees, blind (2026-11-06).** Graded in the Cast tab with the arms hidden: direct works in 8 of 12 with a mean grade of 3.8, figure 2 of 11 and 2.4, paste2 4 of 11 and 1.8, paste 0 of 11 and 1.5. The comments on figure and paste name wrong limb counts ("3 legs", "3 fingers") and arms out of place. Direct got one such comment ("Limbs placement may be off"). By eye, figure had looked on par with direct; the producer puts it well below. Two direct draws got a 1, so drawing several and choosing still matters.

## Smaller checks, 2026-11-05 night

- **Five references instead of three.** Codex takes up to five images. The forty twins drawn with the same three references plus two more came out nearer the real card on 26 of 40 by CSD (p 0.24), and the director preferred them 21 to 17. A lean, not a clear gain, so cards keep three references.
- **Invented extras come from the colors line.** The sheriff star's jewel was in its hero colors, "golden yellow with a small red gem in the center", put there to meet the rule of one accent hue. Writing "plain ... and no gem" in the subject left the jewel in 3 of 3 draws. Moving the red onto a part the subject names, the ring, removed it in 3 of 3 (`experiments/plain_check.py`). The planner's lesson now says the accent colors a named part and never adds one.
- **No topic checker.** A text check of whether each card alone names its topic flagged 60 to 76% of the cards in draft plans for the film sets, and 77 of 123 cards in the game's own sets, such as Bottle and Sneakers in Sports and Tea Cup in Countrystead. It cannot tell a weak set from a real one, so it was not added. Real sets use plenty of everyday objects that read through the set, so the planner's lesson on this, which came from the user's ratings, is not made stricter.
- **Naming a shape does not hold it.** The clock twin's face, measured as the axis ratio of its SAM 3 mask, is 0.995 on the real card and 0.95 on every redraw, with or without "its face is a perfect circle" in the subject (`experiments/shape_check.py`). The redraws turn the clock slightly, so one side of the rim shows. A Blender model at azimuth 0, which the modeller's rules give objects read front-on, fixes the camera instead.
- **A third candidate rarely matters.** Over 146 cards in ten runs, the first draw failed its checks 46 times. A second candidate passed for 12 of those and only the third for 2 more. Candidates of one card are near-identical, so the pick between them is close too. Cards keep three candidates for the final sets; `--candidates 2` costs a third fewer drawings and loses about 1 card in 70.
- **One review round is enough.** Across every run so far, edits from a first review round were kept 6 of 11 times and from a second round 0 of 11. The second round costs nine specialist calls, the director, the edits and their judging per variant, so `make_set.py` now reviews once by default.

## Character outfits, 2026-11-05 night

The three character cards of the Western cast plan, drawn through the pipeline (`runs/cast-check`), kept the outfits of the cutouts they were drawn from: the cow wore the red life vest and sunglasses of the jet-ski card, the man the hiker's backpack, the pig the straw hat of its train card. One sentence in the cast prompt, "the cutouts show who each character is, not what it wears: dress it only as the subject says", removed the backpack and the sunglasses but not the vest (`experiments/outfit_check.py`). With cutouts in no outfit ranked first as well, the cow came out plain and the pig in the asked prospector's hat (`runs/cast-check-2`). The man has no cutout without an outfit, and still borrowed overalls. One draw per card.

## A geometric construction check, 2026-11-05 night

No model judges construction, but a Blender blockout is real geometry, so loose parts can be found without a judge. `scripts/blockout.py` now reports each group of hero parts that touches nothing holding it: with a floor, ledge or setting, every group of touching parts must reach it, and a floating object must hang together. Two parts touch when their surfaces cross or come within 1% of the hero's height.

- **Over the 200 model files so far it flagged 14.** Early rounds had real gaps the modeller fixed later, such as a steam train's tender set apart from the engine and a wagon's loose hoops. Three final models float by design: a planet's ring, a station in orbit and mist inside a crystal ball. No final model had an unintended loose part, because the modeller's look at its render already catches what the camera shows.
- **So it is a guard, not a measured gain.** The modeller now gets each loose group's position and size with each render, and keeps a group that floats by design, such as a station in orbit with a planet far behind. The user's remaining complaints on blockout cards are about function, such as a ladder that leads nowhere, which no contact test sees.

## Fire, 2026-11-06

The producer called the drawn fires weak: the cauldron's tiny flame was "laughable", and the meteor's tail did not read as fire. The proposed lesson said the reference set has no fire, but it has the Campfire Cook card, a bright fire under a cauldron, and a lantern's flame. `experiments/fire_check.py` drew the horror cauldron and the western campfire three times in each of three arms: as planned, with the subject describing the real card's fire, and with that plus the two real fire cards as references.

- **Wording fixes it.** As planned, "small orange flame" in the colors drew a tiny flame under the cauldron in 3 of 3. Described as "big and bright: a yellow-white glowing core, orange flame tips curling upward, glowing orange ends on the logs, and warm orange light" on the pot, it drew a bright campfire with lit logs in 3 of 3, for both objects. The share of bright fire-colored pixels on the cauldron went from 0.010 to 0.076, against 0.034 on the real card, so "big" overshoots. On the desert campfire the sand falls in the same color range, so there the change is judged by eye only.
- **References add nothing.** With the real fire cards attached the fires look the same as with words alone, and the lantern card's sunburst rays replaced the cauldron's stripes.
- Rated by the author's eye and one pixel measure, not yet by the producer.

## Batch with the producer's lessons and the cast, 2026-11-06

Variant 1 of each `runs/plans/*-shared-cast.json` plan, drawn through the full pipeline: ten cards per genre, one with the cast (`runs/<genre>-batch`). 114 drawings: 90 candidates and 24 edits.

- **Measured.** Candidates inside the real cards' bands: Western 23 of 30, Sci-Fi 11 of 30, Horror 13 of 30. The misses are framing and color bands on thin or black objects, as before. The judge kept 12 of 24 edits; it rejected the reviewers' plum witch hat, the blue-violet cauldron and a note that removed the ghost sheep's pumpkin.
- **The lessons show in the plans.** The lasso gets a Blender model and is drawn as a coil ending in an open loop. The wagon has four wheels, the windmill a solid tower, and subjects name shapes ("perfectly round", "symmetrical from the front").
- **Author's read, not rated: more correct, but plainer.** Beside the earlier finals of the same 16 objects, the batch drops the details that gave them character: the hat's star badge, the boot's spur and flame inlay, the witch hat's bent tip, the rocket in flight, the control panel's gauges and lever, the moon base's glass dome. The new subjects are longer and geometric ("a tall black pointed cone hat with a wide round flat brim"), which the shape lesson asks for. The producer graded those earlier hat, boot and witch hat 5, 5 and 5 in the blind Redraw tab. The haunted house came out a tidy cottage: its Blender model was built straight, though the plan said crooked.
- **Cast cards.** All three read as scenes with the game's characters. The man again wears his own overalls, in a space cabin where the brief asked for a space suit.
- **The plainness comes from the wording.** `experiments/wording_check.py` drew the hat, boot, witch hat and console from their batch briefs three times each, with the batch's subject and colors, then with the earlier finals' (same staging, backdrop and references, no blockout). The batch wording drew plain objects in 12 of 12; the earlier wording brought back the badge, the spur and flame inlay, the bent tip and the lever with colored buttons in 12 of 12. The hat's badge was never in its old subject: it came from "cream" in the colors, the effect the accent lesson removes. A lesson asking for signature details, with symmetry only where the real object has it, is proposed.
- **Rated by the producer in the Cards tab, not blind: mean 3.6 from 30.** Western 4.1, Sci-Fi 3.6, Horror 3.2. On the 16 objects also graded in the blind Redraw tab: batch 3.69, earlier finals 3.44, blockout redraws 2.88, with 5 better, 8 the same and 3 worse. Better: flying saucer 2 to 5, ringed planet 3 to 5, space helmet, cactus and lasso by one. Worse: haunted house 3 to 1 ("Shape is jagged in a bad way"), cowboy hat and moon rover by one. The tabs differ (blind and mixed against labelled), so this is suggestive.
- **The plainness cost little.** Hat 4, boot 5, witch hat 5, console 3, against 5, 5, 5 and 3 before. The author's read that plain is worse did not hold.
- **Low grades name the plan more than the style.** Candy corn 2 ("unrecognizable. The art style if fine though") and teleport pod 2 ("I wouldn't know what it is without the title"). The cauldron 1 again, now for its legs ("One leg of the pot is missing"). The rocket 2 ("a toy rocket for a child"): it is small on a blank pad, while real vehicles and buildings on a surface fill the frame and stand on their own ground. The horseshoe 2 for its placement, the moon base 3 ("Too 3d render feel").
- **Cast cards:** Campfire Pals 5 ("Very good"). Ghost Sheep 3: kicking the pumpkin "may look like violence", and the sheep alone would be better. Zero Gravity 2: the man has a helmet and the pig has none, "some sort of animal cruelty".
- **Potion 4:** the cork should be cork-colored, where the plan's accent made it green, and the backdrop "reminiscent of sand". See Backdrop colors.
- Lessons proposed from these comments: no harm in cast scenes, objects named without their title, natural materials keep their color.

## Backdrop colors, 2026-11-06

The producer, on the batch potion: "The background is maybe off, reminiscent of sand. Run analysis of the colours that are being used: are there any patterns to it?" `experiments/colors.py` measures each card's backdrop (the background above the subject), its surface (the bottom of the card, for categories 2 and 3) and its main hero color, for the 160 real cards, the 30 earlier finals and the 30 batch cards. Swatches: `runs/colors/sheet.png`.

Measured patterns in the real cards:
- **Mostly cool.** Cyan 26%, blue 19%, green 14%, orange 11%, purple 9%, yellow 7%, pink 7%, red 3%, near-grey 4%.
- **By category.** Floating objects sit on cyan, blue or green. Ledges take purple, green, red or pink, the most saturated backdrops (Oklab chroma 0.187). Objects on a real surface favor orange. Scenes have cyan and blue skies, the least saturated (0.123).
- **Loosely opposite the hero.** The median hue gap from hero to backdrop is 110°, not a full complement. Red and orange heroes, the most common, sit on blue or cyan in 41 of 74 cards.
- **The surface often shares the backdrop's hue.** In 25 of 52 cards on a ledge or surface it is in the backdrop's color family, with a median hue gap of 27°.
- **Sets repeat.** A real set uses 5.8 color families over ten cards, and its most used family covers 3.7 cards.

Ours against them:
- **More saturated.** Mean backdrop chroma 0.180 for the earlier finals and 0.174 for the batch, against 0.143. The gap is widest in green (0.21 against 0.15), pink (0.22 against 0.17) and purple (0.21-0.24 against 0.18). The planner is told "bright and clean... never dusty, muted, dull or dark".
- **More opposite.** A median hue gap of 125° for the earlier finals and 148° for the batch, against 110°. The planner is told to contrast the backdrop with the hero.
- **Surfaces contrast with the backdrop.** The surface shares the backdrop's family in 1 of 13 earlier finals and 3 of 10 batch cards, with median gaps of 73° and 123°, against 27° on real cards.
- Spread per set matches: 6.7 and 6.0 families against 5.8. One backdrop falls outside the real range: the earlier Candelabra's dark purple.
- **The potion's sand is not its color.** Its backdrop, #fdbf33, sits between two real wave backdrops: Fan Fold #fbc212 and Beach Ball #fbc554. Author's read: the Beach Ball's waves sit over real sand, and Fan Fold's lemon waves are crisp, with no surface. The potion's soft amber waves over a warm table look like the Beach Ball's dunes. That is one card, not a rule.

These are measured differences, not yet rated. The saturation and contrast come from the planner's color rules, which are style wording, so any change is one round, measured and shown to the producer.

### The logic behind the backdrop color

The producer asked to match the real cards' color logic, "complementary colours or whatever logic they are having". `experiments/color_logic.py` tests each idea on the real cards against the same cards with their backdrops shuffled:
- **Not complementary, but never the same hue.** A backdrop within 30° of the hero's hue is rare: 4% of cards, against 14% when shuffled. Past that, the gap is spread almost evenly, with a slight lean to the far side (48% beyond 120°, against 42%).
- **Temperature is the rule.** A warm hero sits on a cool backdrop on 84% of cards (n 94). A cool hero gets a warm backdrop half the time (n 46), against 28% warm backdrops overall: green heroes take pink or red, blue ones cyan, orange or yellow. The 20 grey or white heroes take any color.
- **No echo, no value rule.** The backdrop avoids the hero's secondary colors too (18% within 20°, against 24% shuffled). Lightness has no fixed relation (median difference 0.18, against 0.17 shuffled).
- **By category, for warm heroes.** Floating: cyan, green or blue on 18 of 21. Ledge: purple or green on 6 of 8. Real surface: spread out. Scenes: cyan or blue skies.
- **Neighbours differ.** Neighbouring slots share a backdrop family on 11% of pairs, against 16% shuffled within the set. Set-level tint stays weak, as found before, except where the topic is a color, such as Diving's sea.
- **The backdrop is a real pattern.** Light-dark spread in the backdrop (90th minus 10th percentile of Oklab lightness) is 0.12-0.13 in every category, with a hue drift of 3-8°. Ours match on floating cards (0.124) but are flat on ledges (0.083) and real surfaces (0.059).
- Planned and drawn backdrops agree: 52 of 60 of our cards came out in the planned family and 3 in a neighbouring one, so the planner's rule reaches the drawing.

**Change (2026-11-06):** the planner's color lines now state the temperature rule, no hue that is on the hero, the colors by category, and "rich and clean... never neon" in place of "bright". Checked on plans for the three genres with the new rule against the current plans, 81 cards each, colors read from the planned text: warm heroes on cool backdrops 27 of 29 against 25 of 31, floating objects on cyan, blue or green 21 of 29 against 11 of 28 (real 25 of 35), a backdrop repeating a hero hue 2 against 7. A clause asking neighbours to differ cut shared neighbours to 2 of 72, below the real 11% that the current plans already matched, so it was dropped. Saturation can only be measured on drawings. The flat backdrops on ledges and surfaces belong to the drawing prompt, a separate round.

## Second batch, after the color logic and the second reference pass, 2026-11-06

Variant 1 of each `runs/plans/*-shared-cast-2.json` plan, drawn through the full pipeline as `runs/<genre>-batch2`, after the planner learned the real backdrop color logic and the findings of the second reference pass (SYNTHESIS.md). Its Blender models were built from the modeller brief as it stood before that pass. `experiments/batch2_check.py` measures the delivered cards of both batches and the real cards the same way, categories 1-4:

| Measured | Real | Batch | Batch2 |
|---|---|---|---|
| Near-mirror silhouette, categories 1 and 3 | 13 of 67 | 9 of 17 | 2 of 16 |
| Floating on cyan, blue or green | 25 of 35 | 4 of 10 | 8 of 9 |
| Mean backdrop chroma (Oklab) | 0.153 | 0.178 | 0.160 |
| Warm hero on a cool backdrop | 60 of 72 | 13 of 15 | 11 of 12 |
| Light pool behind the object, categories 2 and 3 | 39 of 52 | 5 of 10 | 4 of 11 |
| Category 4 object cut by a card edge | 17 of 42 | 2 of 7 | 0 of 7 |
| Candidates inside the real bands | | 47 of 90 | 50 of 90 |

- **What moved.** Objects turn into three-quarter view, floating objects take the real cards' cool backdrops, and saturation fell to near the real level.
- **What did not.** The light pool and the edge crop are drawing words the image model ignored.
- **Author's read, not rated.** The staging is closer to the real cards. Category 2 objects stand on plain floors in the backdrop's color (cactus, helmet, flask). The saloon doors, haunted door and control panel are close spots on their walls. The horseshoe and star map lie flat, seen from above. The saucer and bat fly in a sky with clouds. The campfire has its coffee pot and tent. The potion has a cork-brown stopper and a star tag. Misses: the lasso became a double loop, the spooky tree gained a castle tower nobody asked for, and the rocket on its pad is still plain. On the cast card, the man again wears his overalls. Neither character card shows harm, and both characters wear the same gear.

## Limits

Eight blind pairs per role is a small sample, and rounds are noisy. Reviewers are models, and on pairs of different objects they also raise false alarms on hidden real controls, so they guide edits and are not a gate. The human ratings come from one rater.
