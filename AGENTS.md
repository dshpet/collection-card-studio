# Project guide

- Keep the project lean: short docs, small scripts, and no test suites without a real need.
- `PROCESS.md` is a draft. It must be reviewed and rewritten before submission.
- Board images are Playrix art and stay out of git.
- `.env` holds `HUGGING_FACE_API_KEY`. Never print or commit it, and keep it away from external code.
- External code is pinned to reviewed revisions. Review again before changing one.
- Sets are topics with 1–3 word names. Rarity does not change the art.
- Codex is the working generator, behind `draw()` in `scripts/draw.py`.
- A pipeline change should be judged with `scripts/validate.py` and by looking at the cards.
- In analysis, keep measured, model-estimated and rated fields distinct.
- Reference cards are 430×480, which limits conclusions about fine detail.
- Specialist agents, one per art vector, plus an art director are a core idea of this project: see `analysis/agents/`. They review references and generated cards.
- Findings live in `analysis/SYNTHESIS.md`. The form lives in `scripts/form.py`.
- `scripts/*.py` run with `.venv/bin/python`. Use `-B` to keep the tree clean.
