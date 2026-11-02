# Playrix AI Producer test task

Turn a theme and free-form producer wishes into 3–5 complete ten-card sets that could sit next to the [reference collection](materials/02_collection_explanation.md). Full brief: [task](materials/01_task_description.md), [art guide](materials/03_art_guide.md), [Miro board](https://miro.com/app/board/uXjVEUZR5u0=/).

**Status:** reference analysis done. No cards generated yet.

Start with the [findings](analysis/SYNTHESIS.md). Open `analysis/report.html` for the dashboard. It reads card images from `materials/`.

## Plan

1. ~~Analyse all 160 reference cards and 16 sets in one universal form.~~
2. Plan sets as topics with 1–3 word names. A story behind a set is optional.
3. Pick objects as a whole set: theme fit, variety, and all four non-gold categories.
4. Generate cards with style references. Codex is the working generator.
5. Check generated cards with the same form, then correct failures.
6. Deliver three movie-genre sets, the comparison with the references, and the process on Miro.

## Layout

| Path | Contents |
|---|---|
| `materials/` | Task documents and board images. Images are not in git. |
| `sources/` | Board export and image manifests with hashes. |
| `research/` | Research reports and the item-selection source pack. |
| `analysis/` | Analysis outputs. |
| `scripts/` | Pipeline scripts. |
| `PROCESS.md` | What was tried and why. Draft. |

## Reference analysis

Run from the project root. Each step skips finished work where it can. Masks use the rater boxes, so `depth` and the ratings come first.

```sh
python scripts/map_sets.py
python scripts/rate.py cards --rater codex    # also: claude, or an Ollama tag
python scripts/rate.py sets --rater codex
python scripts/estimate.py depth
python scripts/estimate.py masks marigold
python scripts/embed.py
python scripts/measure.py
python scripts/cluster.py
python scripts/summarize.py
python scripts/build_report.py
```

The forms are defined in `scripts/form.py`. `.env` needs `HUGGING_FACE_API_KEY` only for gated models.

## Materials

Board images go in `materials/` at the paths in `sources/image_manifest.json`. Check them with:

```sh
python -m unittest discover -s tests
```

To refresh from the board, update `sources/board.svg` and `sources/original_images.json`, then run `python scripts/export_materials.py`.
