# Process log

> **DRAFT. This narrative must be reviewed and rewritten before submission.**

## 2026-10-31: Sources and research

- Exported the Miro board: task documents, 160 cards, 16 sets, result templates.
- Wrote two research reports on measuring visual style and on image generation.

## 2026-11-01: First analysis

- Ran nine separate art-analysis agents on four cards and merged them into a style brief.
- Built a text search over 102 cards with SigLIP 2 and DINOv2 on ROCm.
- Labelled those cards automatically with local Gemma and Qwen models.

## 2026-11-02: Planner prototype

- Built a planner that proposed objects, assembled sets and wrote 90 text briefs for three genres.
- Its automatic review confirmed all 90, yet a content audit still found contradictions. Control tests failed, so that work stopped.
- Replaced low-resolution images with all 180 board originals. The old thumbnails turned out to be different drawings.
- Reindexed and relabelled all 160 cards: 148 reviewed, 12 with uncertain staging.

## 2026-11-02: Audit and reset

An audit against the task found four problems:

- No card image had been generated.
- No document analysed the 16 reference sets.
- Planned sets used invented story premises, while real sets are plain topics.
- Every prompt carried about 500 words of pasted documentation.

Decisions:

- Removed the planner, its test suite and most generated documents.
- Sets are now topics with 1–3 word names.
- Analyse every reference in one form before generating anything.

## 2026-11-02: Reference analysis

- Rebuilt the analysis around one form with fixed fields, covering nine art vectors plus staging, identity and idea.
- Matched every card to its set and slot from the screenshots.
- Rated all 160 cards and 16 sets with Codex, Claude, Qwen and Gemma, and measured how far they agree.
- Claude Code first blocked external code, so masks started on SAM 2.1 and depth on Depth Anything V2. About 9 of 160 masks stayed wrong despite several fixes.
- With approval, tested RMBG-2.0, BiRefNet, Depth Anything 3 and DeepGaze. They ran on test cards before the review; the jobs were then stopped until the code was audited.
- BiRefNet replaced SAM and all the mask-rescue logic. DA3 replaced V2. RMBG-2.0 was dropped: it was weaker on the test cards and its licence is non-commercial.
- Added Marigold normals and shading, DeepGaze attention, and embedded each card as whole, subject and background with DINOv2, SigLIP 2 and CSD.
- Dropped star counts because the readings were unreliable.
- Main results: the look is a soft 3D render, sets hold together by idea rather than look, and five sets without characters are the closest models for the movie sets.

## 2026-11-02: Independent review

- Three fresh agents audited the data, checked the findings against the cards and reviewed the fit with the task.
- Two findings were wrong and were corrected: sets do share a look, and their variety is no better than chance. "No-gold" sets were also misnamed.
- The review surfaced traits the form had missed, so a backdrop section was added: pattern, tone, glow and surface kind. These are among the most reliable fields.

## 2026-11-02: First end-to-end pipeline

- Built one command: plan, brief, draw, check, correct, deliver. Generated cards go through the same analysis as the references.
- First try, one Western set: 8 of 10 passed. The same set without references: 6 of 10.
- Negative control: the check rejected all six wrong-style images (photo, vector, pixel, watercolor, line art, clay).
- Full run: three genres, three variants each, 90 cards. 66 passed first time, redraws rescued 8 more, and 16 were left for review.
- Acceptance test: one generated card hidden among nine real ones. Codex and Claude found it 5 times in 48, which matches the 10% chance rate.
- Known weak spots: horror drifted to Halloween and antiques, environment cards came out too detailed, several objects read poorly, and correction rounds rarely help.

## 2026-11-02 night: Closing the style gap

The first run looked off to a human, while every check passed it. Details are in [STYLE_GAPS](analysis/STYLE_GAPS.md).

- Found Codex's LLM rewriting prompts and adding its own style words. `draw()` now forces them verbatim.
- DINOv3 told first-run cards from real ones at AUC 0.95, on whole card, subject and background alike, so the "hidden among nine" test had simply been too weak.
- Built twins: real cards redrawn with the card hidden, to compare style with content held equal.
- Blind specialists called the real card fake 12 of 12 times on color and surface. Models expect game art to be glossier than it is, which is also how "chunky, toy-like" got into the style text. Four labelled lessons fixed this.
- Eight rounds of twins brought reviewers from 89% to chance, and showed where the style overshoots in each direction.
- Rebuilt the specialists around current tools, with a lens per vector, and replaced correction rounds with candidates, selection and targeted edits.
