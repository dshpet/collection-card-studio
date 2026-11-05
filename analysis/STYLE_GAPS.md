# Style mismatches and fixes

## Human rating, 2026-11-03

The user rated all 80 blind twins with `scripts/rate_ui.py`. They found the generated card 31 of 32 times in the old style and 24 of 32 in the final style, choosing a side each time. Model reviewers were at chance on the same final style. **So the final style is closer, but a person still sees through most of it, and the models do not.** Every model result below should be read with that in mind.

What the user named:
- **Style:** too round, glossy and toy-like, short of the real cards' grounded realism. The real cards look like rendered 3D models, while ours look like illustrations of 3D.
- **Construction:** objects that could not exist, such as headphone cables ending in three strands, a folding chair that could not fold, a pier that leads nowhere, ropes ending in the air.
- **Perspective:** parts seen from different cameras, such as calculator keys drawn front-on on a tilted body.

None of the nine style specialists judged construction or perspective, so two checkers were added. Taught with the user's marked cards and shown a full-size crop, they catch 11 of 16 held-out construction errors and 6 of 6 perspective errors the user flagged. They also flag 3 and 5 of 20 real cards. That counts any error. Major errors alone catch 5 of 16 and 4 of 6, with 2 false alarms each. Together, the two checkers flag 18 of the 21 cards the user marked when any error counts, against 10 on major errors only, with 7 false alarms on 20 real cards instead of 4. So any error now passes a candidate over, while edit notes still come only from major errors, since edits are obeyed strongly. Without the full-size crop they caught 5 of 16, and GPT-6.1 caught 1 of 16, so it is not used.

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

Six twins (spotlights, calculator, chair, clock, chess table, pier), two draws each, four arms, made by `scripts/trial.py`. The user rated all 48 blind, arm hidden: does it work as built, and a grade 1-5 against the real card.

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

`scripts/trial2.py`, rated blind against the old card. Finish cards, models rendered matte: soft beat old 2 times and lost 4. The cards lost designed shape with the gloss: the cat's face, the boot's tooling, the hat's curl. Matte primitives give primitive charm ("texture and color is better, but form is somewhat lacking"). Built objects: remodel 2/1/4 wins/losses/ties, photo 2/2/3, photo_style 3/2/2. The saddle rose from 2 to 5 and the cauldron stayed at 1 in every arm. Photos taught real construction that reads as wrong, such as smaller front wagon wheels and a raised dome entry with a ladder. The target is iconic logic, not engineering truth.

## Uniform scores against the user, 2026-11-04

`scripts/score.py` puts every graded card on one list (129 graded, 80 twins, 24 hidden real cards). It scores each card by embeddings, the classifier, the nine specialists (1-10 on their vector) and the art director (1-10 overall). All reviewers saw the same real cards and six graded lessons. Results are in `runs/score/summary.json`.

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

A lone 1-10 score failed, so `scripts/prefer.py` asks a different question: of two drawings of one object, beside its real card or cards, which is closer? Truth is 218 pairs the user already decided. 108 come from closest picks, 60 from the trial and 50 from set cards. The bar set before the run was about 70% agreement.

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

**Automatic tuning did not generalize.** `scripts/tune.py` split the pairs by object into tuning and held-out halves. In six rounds an editor proposed one note at a time from the director's mistakes and the user's comments. Two notes were kept: prefer matte and calm over glossy, and judge overall color masses over small details. Tuning agreement rose from 65 to 84 of 115. On the held-out half the tuned director agreed 65 of 101 times, the untouched one 68 of 103 and the first run 65 of 102. The gain was fitting and run noise: one prompt varies by about 5 pairs between runs. So the notes were not installed. The second note also contradicts the user, whose comments are mostly about construction. Closest picks, half the pairs, reward overall look.

**Confidence held up.** On held-out pairs the untouched director at confidence 4 was right 10 of 13 times in a fresh run and 19 of 24 in the first, about 78%. `choose()` now asks for confidence and lists picks below 4 for a human look. The cut was set on data that includes these pairs, so it was not chosen blind.

The first run looked off to a human, yet every automatic check passed it. This file records what was wrong, why the checks missed it, and what fixed it.

## How the gap was measured

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

## Mismatches

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

## What did not help

- **More wording.** Each sentence is high-gain: "nearly touching the edges" took hero area from percentile 0.56 to 0.91. The art director's rewrites swung between too toy and too realistic, so the final text was settled by hand from the evidence.
- **Softening the export.** Real and generated spectra already match in every band, so a blur would add a mismatch.
- **Reference-only study.** Specialists working from real cards alone wrote "clay-like toy" and "never stitching", though the real Baseball Mitt has stitching.
- **The old correction rounds.** They rescued 8 of 24 cards. Edit mode replaced them.
- **Geometry for the reviewers.** A panel of measured geometry beside each card made both checkers worse. It showed straight edges grouped by direction, curves fitted to true ellipses and the skeleton of thin parts. On the same labelled cards, construction caught 9 of 16 instead of 11, and perspective 2 of 6 instead of 6, with 8 false alarms on real cards instead of 5. Models read the marks as proof that the drawing is right. "Ratio 0.95, a near-circle at a slight angle" passed the clock the user called not round, and "parallel edges drawn parallel" passed both chess tables. New lenses for four specialists did no better than the old ones on the sixteen held-out twins, 26 caught and 31 wrong against 31 and 28. Those lenses were normals with the outline's bends, edges and ellipses, lines of equal shading, and a vectorscope. The panel code is in commit 3efa3bf.
- **Outline measures of roundness.** Straight share, corner rate, corner radius and planar share do not separate real cards from their twins. In both styles the twin scores higher 16 to 24 times in 40, and 8 times in the 16 with normals. The roundness a person sees is not in the outline at 430×480.

## Limits

Eight blind pairs per role is a small sample, and rounds are noisy. Reviewers are models, and on pairs of different objects they also raise false alarms on hidden real controls, so they guide edits and are not a gate. The human ratings come from one rater.
