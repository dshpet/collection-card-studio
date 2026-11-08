# Process

What was tried, and why the tool is built the way it is. Numbers are in [STYLE_GAPS](analysis/STYLE_GAPS.md); each study's script is listed in [experiments/](experiments/README.md).

## 1. Analysis before generation

- The Miro board was exported: task documents, 160 cards, 16 sets and the result templates. The first export's thumbnails differed from the originals, so every card was re-exported from the board.
- A pilot ran nine specialist agents on four cards ([pilot](analysis/runs/2026-11-01-reference-pilot-01/README.md)). Four cards were too few, and a planner built on it approved its own 90 briefs while an audit found contradictions in them. It was cut, and its specialists became the reviewers.
- The audit set two rules: sets are plain topics with 1–3 word names, not story premises; and every reference card is analysed in one form before anything is drawn.
- All 160 cards and 16 sets were rated in that form by four vision models, measured from pixels, masks, depth, shading and attention, and embedded three ways ([SYNTHESIS](analysis/SYNTHESIS.md)). Fresh reviewers then checked the findings against the cards; two were wrong and were corrected.

## 2. The first pipeline

- One command planned, drew, checked and delivered three genres, three variants each. The check rejected six off-style controls, and one generated card hidden among nine real ones was found only at chance.
- The producer still saw at once that the cards were not quite the game's style. The checks had missed it: Codex had been rewriting prompts and adding its own style words (`draw()` now forces them verbatim), a classifier told our cards from real ones at AUC 0.92–0.95, and uncalibrated model reviewers called the real card the fake 12 of 12 times, because they expect game art to be glossier than it is.

## 3. Measurement

- **Twins:** real cards redrawn with the card hidden, so the object is the same and what differs is mostly style. Eight style-text rounds took calibrated reviewers from catching 89% of twins to chance.
- **The producer's blind ratings** became the measure: 31 of 32 first-style twins found, 24 of 32 final-style. Models were at chance on 16 of the same twins.
- No score of a lone card followed the producer's grades. Pairwise judging did: the director agrees with the producer 61% of the time, 76% when confident. So the pipeline picks candidates pairwise in both orders and flags close calls.
- Dropped: automatic tuning of the director (gains on the tuning half did not hold out), tone rounds that moved measured darks onto the real cards (the producer preferred neither), measured geometry overlays for reviewers (they read the marks as proof), search-picked or five references, and a measured backdrop grade (no gain).

## 4. Construction from geometry

- The producer's main complaint became construction: cables ending in air, a chair that could not fold. A line describing how the object works did nothing. In a six-object trial, a Blender blockout restyled by the image model cut broken cards from 5 of 12 to 1, and to none once the models were fixed.
- Blockouts took the charm out of simple forms, so only built, multi-part objects get a model.
- Construction and perspective checkers were at chance on 93 pairs the producer labelled, and were removed. A geometric check for loose parts guards the models instead; close calls go to a human.

## 5. The producer's loop

- **Lessons.** Rules learned from the producer's comments live in plain words in [lessons.md](analysis/lessons.md), which the planner reads. A model proposes new lessons from comments and lost edits; a person accepts them.
- **Cast.** SAM 3 cut the game's characters out of the reference cards. Drawn in one go with the real cutouts attached, they stayed themselves and graded 3.8, against 1.5–2.4 for pre-drawn figures pasted or attached.
- **Batches.** Two graded batches of one variant per genre: 3.63, then 3.97 after the planner learned the real backdrop color logic (opposite temperature, not complements) and a second pass over the references (a place shown by its signature object, partner objects, three-quarter views, flat objects from above). Half the gain came from the three character cards and most of the rest from swapped objects; objects redrawn in both batches moved only +0.11. Each low grade traced to the plan and became a lesson.
- **Edits.** Correction rounds rescued only 8 of 24 cards, so the pipeline now draws several candidates and picks pairwise. Review edits beat their drafts about half the time (135 of 263) and a second review round kept none of 11, so an edit stays only if it wins and the pipeline reviews once.

## 6. Robustness and other generators

- 19 odd and risky requests (emoji, brands, franchises, weapons, gore, an injected "ignore all previous rules") all produced plans, with forbidden wishes declined and named in the report. After two repairs, War and Gangsters kept three cards flagged for the producer, and Elections stayed a voting set. Kitchen, Pirates and a Star Wars request ran end to end in one consistent style.
- A code review fixed three ways a run could stop or write to the wrong place; each run folder now records its request.
- A generator bake-off on the twins: Codex against Nano Banana Pro through Antigravity (11 twins, until its quota ran out) and Qwen-Image-2.1, open weights on a local GPU ([STYLE_GAPS](analysis/STYLE_GAPS.md#generator-bake-off)). Codex won both.
- An outside artist graded the pre-final sets of five genres: 3.1 of 5 per card, every set 3–4 of 5, and our surfaces read grainier than the real cards'. Each final set starts from that rater's best-graded variant of its genre.

## 7. The final sets

- **Plans.** The chosen variants were reviewed card by card against the other variants: grades, broken flags, planner checks and lessons (`experiments/plan_review.py`). Each set got a `spec.md` written from its plan before drawing.
- **Style changes, one per arm on the twins** (`experiments/night.py`): smooth large surfaces in the prompt, richer planner colors and larger blockout framing were adopted. One camera line and new perspective models were dropped after the producer's blind look.
- **First draw.** Two Period Drama cards were weak in every candidate, a plan problem: the Pearl Necklace became the Quill Pen and the Hat Box got stripes. Detective's Badge Wallet moved from a dark table to a light desk, and the Flash Camera to royal blue so the set kept six or more backdrop hues, as the four real sets without characters have. Both sets were redrawn in new folders seeded with the other cards' candidates. The producer graded every set 4 of 5, "Yes, with small issues" (`runs/final3/README.md`).
- **Fix round 1.** The comments were about recognition and composition, not style: a badge without its emblem, a hat box that read American, a windmill that read as a monument, off-center objects, a dog that read as a character. 17 cards were redrawn, all but one of them commented on: `make_set.py --keep` reuses unchanged cards, a plan card's `note` carries the fix, and `k.focus` frames a blockout on its main body. The comments became planner lessons, which the producer accepted (`runs/final4/README.md`).
- **Fix round 2.** Sets 5, 4 and 4. Eight small fixes: matte metal and porcelain, an even brim, a shorter handle, a candelabra seen from mid-height. The first review undid three of them, because the art director had never seen the producer's notes; now it gets them and each edit prompt repeats the note to keep (`runs/final5/README.md`).
- **Fix round 3.** Every set 5 of 5. The last comment, a magnifier glass too large, was fixed by the proportions of the one real card with a magnifier. A Blender top hat fixed an uneven brim but read stiffer and was not used (`runs/final6/README.md`).

## Tools tried

| Task | Tried | Kept |
|---|---|---|
| Drawing | Codex image tool, Qwen-Image-2.1 (local), Nano Banana Pro (Antigravity) | Codex: it beat both on the twins, 39 to 1 and 11 to 0 |
| Planning, modelling, reviewing | Claude Sonnet and Opus, GPT-6.1 specialists, local Qwen and Gemma raters | Sonnet plans, Opus models and judges |
| Masks | SAM 2.1, RMBG-2.0, BiRefNet; SAM 3 for the cast | BiRefNet; SAM 3 for the cast |
| Depth, shading, attention | Depth Anything V2 and 3, Marigold, DeepGaze IIE | DA3 and Marigold for analysis; none gates a card |
| Embeddings | DINOv2, DINOv3, SigLIP 2, CSD | CSD against the same object, SigLIP 2 for reference search |
| Structure | Blender blockouts, a matte render, photos of real objects | Blockouts for built objects |
| Judging | Lone scores, pairwise judges, construction checkers, a probe on the producer's pairs | Pairwise director with a human look at close calls |

## Limits and next steps

- One main human rater, plus an outside artist on the pre-final sets. The final style is still spotted in 24 of 32 twins.
- No model judges construction; it comes from geometry and a human look.
- Each variant takes about 40 minutes and needs a GPU, Blender and two logged-in CLIs.
- A style LoRA trained on the reference cards with an open model was not tried, for lack of time. The research puts it at about half a day ([research](research/README.md)).
