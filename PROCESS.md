# Process

> **DRAFT. This narrative must be reviewed and rewritten before submission.**

How the tool got here, decision by decision. Numbers are in [STYLE_GAPS](analysis/STYLE_GAPS.md); the studies behind each decision are in [experiments/](experiments/README.md).

## 1. Analysis before generation, 2026-10-31 to 11-02

- Exported the Miro board: task documents, 160 cards, 16 sets, result templates. The first thumbnails turned out to be different drawings, so every card was replaced by its board original.
- A first pilot ran nine specialist agents on four cards ([pilot](analysis/runs/2026-11-01-reference-pilot-01/README.md)). Four cards were too few, and a planner built on it confirmed its own 90 briefs while an audit found contradictions. It was cut.
- An audit against the brief found no generated card yet, no analysis of the 16 sets, invented story premises where real sets use plain topics, and 500 words of pasted documentation in every prompt. Decisions: sets are topics with 1–3 word names, and every reference is analysed in one form before anything is drawn.
- All 160 cards and 16 sets were rated in one form by four vision models, measured from pixels, masks, depth, shading and attention, and embedded three ways ([SYNTHESIS](analysis/SYNTHESIS.md)). External tools ran on a few test cards, were stopped until their code was reviewed, then pinned to the reviewed revisions; BiRefNet and Depth Anything 3 replaced weaker first choices.
- Three fresh reviewers then checked the findings against the cards. Two were wrong and were corrected, and the backdrop fields they surfaced became some of the most reliable.

## 2. The first pipeline passed every check and failed the eye, 11-02

- One command planned, drew, checked and delivered three genres, three variants each. The check rejected six off-style controls, and one generated card hidden among nine real ones was found at chance.
- The producer still saw it at once: not quite the game's style. The cause was the measures, not the eye. Codex had been rewriting prompts and adding its own style words; a classifier told our cards from real ones at AUC 0.92-0.95; uncalibrated model reviewers called the real card the fake 12 of 12 times, because they expect game art to be glossier than it is.

## 3. Making the measurement honest, 11-02 to 11-05

- **Twins:** real cards redrawn with the card hidden, so content is equal and only style differs. Eight style rounds brought calibrated reviewers from 89% to chance.
- **The producer's blind ratings** became the measure: 31 of 32 old-style twins found, 24 of 32 final-style. Models were at chance on 16 of the same twins.
- **Compare, never score.** No score of a lone card followed the producer's grades. Pairwise judging did: the director agrees 61% of the time, 76% when confident, so the pipeline picks candidates pairwise in both orders and flags close calls. Tuning the director automatically overfitted and was dropped.

## 4. Construction from geometry, 11-03 to 11-05

- The producer's main complaint became construction: cables ending in air, a chair that could not fold. A line describing how an object works did nothing; in a six-object trial, a Blender blockout restyled by the image model cut broken cards from 5 of 12 to 1, and to none once the models were fixed.
- Blockouts took the charm out of simple forms, so the planner models only built, multi-part objects. Construction and perspective checkers were at chance on the producer's labelled pairs and were removed. A geometric check of loose parts guards the models instead.

## 5. The producer's loop, 11-05 to 11-06

- **Lessons.** Rules learned from the producer's comments live in plain words in [lessons.md](analysis/lessons.md), which the planner reads; a producer edits that file, not code. A model proposes new lessons from comments and lost edits, and a person accepts them.
- **Cast.** SAM 3 cut the game's characters out of the reference cards. Drawn in one go with the real cutouts attached, they stayed themselves and graded 3.8 against 1.5-2.4 for pre-drawn figures pasted in.
- **Batches.** Two batches of one version per genre: 3.63, then 3.97 after the planner learned the real backdrop color logic (temperature, not complements) and a second reference pass (places shown by their signature object, partner objects, three-quarter views, flat objects from above). Half the gain came from the three character cards and most of the rest from swapped objects; the same objects redrawn moved by only +0.11. Each low grade traced to the plan and became a lesson.
- **Edits.** Review edits lost to their drafts more often than they won, so an edit stays only if it wins, and the pipeline reviews once.

## 6. Hardening and outside views, 11-07

- Independent code, docs and hiring-manager reviews. The code review found that the skill's own command stopped in an old run folder, an empty theme wrote into `runs/`, and a failed Blender model stopped a run. All were fixed, and run folders now record their request.
- 19 odd and hostile requests (emoji, Ukrainian, brands, franchises, weapons, gore, an injected "ignore all previous rules") all produced plans, with forbidden wishes declined and named in the report; after two repairs, War and Gangsters kept three cards still flagged for the producer, and Elections stayed a voting set. Three new topics ran end to end in one consistent style.
- A generator bake-off on the twins: Codex against Nano Banana Pro through Antigravity (11 twins, until its quota ran out) and Qwen-Image-2.1, open weights on this GPU ([STYLE_GAPS](analysis/STYLE_GAPS.md#generator-bake-off-2026-11-07)).

## 7. The final sets, 11-08

- Before the final drawing, the chosen variants were reviewed card by card against the other variants: grades, broken flags, the planner's checks and the lessons (`experiments/plan_review.py`).
- Every set now has a short spec, `spec.md` in its run folder, written from the plan before drawing: each card's staging, subject and colors, and the notes on why the cards were chosen.
- Overnight, one change per arm on the twins (`experiments/night.py`, STYLE_GAPS): smooth large surfaces in the text prompt, richer planner colors and a wider blockout frame were adopted; one camera and the perspective fixes wait on the producer's blind look.
- The final started late, at 11:15 instead of 04:00: a background wait loop matched its own command line and waited on itself all night. Steps are now chained directly.
- After the draw, two Period Drama cards were weak in every candidate, a plan problem: the Pearl Necklace became the Quill Pen (the outside rater's 4) and the Hat Box got stripes. The set was redrawn in a new folder seeded with the other eight cards' candidates, so only the two new cards were drawn and the picks and review ran again (`runs/final3/README.md`).
- The same way, Detective's Badge Wallet left its dark table, darker than any real card, for a light desk, and the Flash Camera moved to royal blue so the set kept six or more backdrop hues, as every real set has.
- The producer graded every set 4 of 5, "Yes, with small issues"; cards 4.4 Western, 3.8 Period Drama, 3.1 Detective. Blind, they found the control closer to the real card than one camera, and the current pipeline better built than either perspective arm: both were dropped. The smooth line held.
- Their comments were mostly about recognition and composition, not style: a badge without its emblem, a hat box that read American, a windmill on a solid tower that read as a monument, objects off center, a dog that read as a character. A fix round redrew only the commented cards: `make_set.py --keep` reuses an earlier run's cards whose plan is unchanged, a plan card's `note` carries the fix into its brief, and `k.focus` frames a blockout on its main body. The comments became planner rules in `analysis/lessons.md`, accepted by the producer (`runs/final4/README.md`).
- Round 2 got 5, 4 and 4, cast 5: "I like it overall". Eight small fixes followed: matte metal and porcelain, an even brim, a shorter handle, a candelabra seen from mid-height. The first review undid three of them, asking for chrome cuffs and glossy porcelain: the art director had never seen the producer's notes. Now it gets them, and each edit prompt repeats the note to keep (`runs/final5/README.md`).
- Round 3 got 5 of 5 for every set. The last comment, a magnifier whose glass was too large, was fixed after looking at the one real card with a magnifier; a Blender top hat fixed the uneven brim but read stiffer, so the round-3 hat stayed. The producer was tired of viewing cards, so this last round was judged here (`runs/final6/README.md`).

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

- One human rater. The final style is still spotted in 24 of 32 twins.
- No model judges construction; it comes from geometry and a human look.
- Each variant takes about 40 minutes and needs a GPU, Blender and two logged-in CLIs.
- Next: the producer's review of the fix round (`experiments/final_review.py`), then a style LoRA trained on the reference cards with an open model.
