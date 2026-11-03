# Style mismatches and fixes

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

## Limits

Eight blind pairs per role is a small sample, and rounds are noisy. Reviewers are models, and on pairs of different objects they also raise false alarms on hidden real controls, so they guide edits and are not a gate. No human has rated these cards yet.
