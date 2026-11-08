# Project guide

- Keep the project lean: short docs, small scripts, and no test suites without a real need.
- Board images and the game's characters are Playrix art and stay out of git: cast cutouts, pre-drawn figures and cards showing the cast.
- `.env` holds `HUGGING_FACE_API_KEY`. Never print or commit it, and keep it away from external code.
- External code is pinned to reviewed revisions. Review again before changing one.
- Sets are topics with 1–3 word names. Rarity does not change the art.
- Codex is the working generator, behind `draw()` in `scripts/draw.py`.
- `scripts/` is the pipeline and the reference analysis. One-off studies go in `experiments/`, and the pipeline never imports them.
- The user's ratings in `runs/ratings.json` are the measure. Judge a pipeline change on twins against their real cards, pairwise or by CSD against the same object, and by looking at the cards. Scores of a lone card do not track the user.
- Model raters are biased on this style. Never trust a rating without labelled lessons: see `analysis/STYLE_GAPS.md`.
- Style wording is high-gain. Change one thing per round and measure it.
- Rules learned from the producer go in `analysis/lessons.md`, not into code.
- In analysis, keep measured, model-estimated and rated fields distinct.
- Reference cards are 430×480, which limits conclusions about fine detail.
- Specialist agents, one per art vector, plus an art director are a core idea of this project: see `analysis/agents/`.
- Findings live in `analysis/SYNTHESIS.md` and `analysis/STYLE_GAPS.md`. The form lives in `scripts/form.py`.
- Scripts run with `.venv/bin/python -B` from the project root.
