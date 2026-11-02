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
- Tried BiRefNet for masks first, but it needs external code, so masks use SAM 2.1 instead. Several rounds of fixes were needed: depth-based prompts, inverted-mask candidates and rater boxes.
- Added Depth Anything V2 and Marigold, and embedded each card as whole, subject and background with DINOv2, SigLIP 2 and CSD.
- Dropped star counts because the readings were unreliable.
- Main results: the look is a soft 3D render, sets hold together by idea rather than look, and five sets without characters are the closest models for the movie sets.
