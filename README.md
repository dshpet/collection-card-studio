# Playrix AI Producer test task

Turn a theme and free-form producer wishes into 3–5 complete ten-card sets that could sit next to the [reference collection](materials/02_collection_explanation.md). Full brief: [task](materials/01_task_description.md), [art guide](materials/03_art_guide.md), [Miro board](https://miro.com/app/board/uXjVEUZR5u0=/).

**Status:** the pipeline runs end to end. Three film-genre sets with three variants each are in `runs/`.

Findings: [analysis/SYNTHESIS.md](analysis/SYNTHESIS.md). Dashboard: open `analysis/report.html`, which reads images from `materials/` and `runs/`.

## Make a set

```sh
.venv/bin/python -B scripts/make_set.py "Western" --wishes "A set for a Movie collection" --variants 3
```

It plans the set, picks reference cards, draws every card, checks each one against the reference analysis and redraws failures. Results land in `runs/<slug>/`: the cards in `variant_N/`, a sheet per variant, and `report.md`. Rerunning continues where it stopped. A run of 30 cards takes about 25 minutes.

It needs the Codex and Claude CLIs logged in, the board images in `materials/`, and `analysis/embeddings/` from `scripts/embed.py`.

`scripts/draw.py` holds the generator, so another model replaces one function. After changing the generator or the check, run `scripts/validate.py off-style` and `scripts/validate.py acceptance`.

## How the analysis feeds generation

- **Planning:** real character-free sets are the examples, and their ranges set the rules (`knowledge.json`).
- **Prompts:** the style text and category rules come from the findings (`scripts/style.py`).
- **References:** each card gets three real cards with the same category and backdrop, and a similar object where possible (`cards.json`).
- **Checks:** every card is measured like the references and compared with per-category ranges, the style embedding and a blind rater.
- **Correction:** each failed check maps to one fix sentence for the redraw (`scripts/style.py`).

## Layout

| Path | Contents |
|---|---|
| `materials/` | Task documents and board images. Images are not in git. |
| `sources/` | Board export and image manifests with hashes. |
| `research/` | Research reports and per-vector notes. |
| `analysis/` | Analysis outputs. `knowledge.json` is what the generator reads. |
| `analysis/agents/` | Specialist art reviewers, one per vector, plus the art director. `VOCABULARY.md`, `TOOLS.md`, `LIGHTING.md` and `RECIPES.md` are their language and tools. |
| `runs/` | Generated sets and control tests. |
| `scripts/` | Pipeline scripts. |
| `PROCESS.md` | What was tried and why. Draft. |

## Reference analysis

Run from the project root. Each step skips finished work where it can.

```sh
python scripts/map_sets.py
python scripts/rate.py cards --rater codex    # also: claude, qwen3.8:27b-q4_K_M, gemma4:31b
python scripts/rate.py sets --rater codex
python scripts/estimate.py masks depth attention marigold
python scripts/embed.py
python scripts/measure.py
python scripts/summarize.py
python scripts/cluster.py
python scripts/knowledge.py
python scripts/build_report.py
```

The forms are defined in `scripts/form.py`. `.env` needs `HUGGING_FACE_API_KEY` only for gated models.

## External code

BiRefNet, Depth Anything 3 and DeepGaze run upstream code, so each is pinned to a reviewed revision. BiRefNet and the DA3 weights are pinned in `scripts/estimate.py`. The source checkouts are:

```sh
git clone https://github.com/ByteDance-Seed/depth-anything-3.git .models/src/da3
git -C .models/src/da3 checkout 3d835ec
git clone https://github.com/matthias-k/DeepGaze.git .models/src/deepgaze
git -C .models/src/deepgaze checkout c7db17e
```

The review scanned all 295 fetched Python files, read the code that actually runs, and checked every pickled checkpoint with PyTorch's restricted loader. Short test runs under a Python audit hook showed no network connections, subprocesses or writes outside the project and temp folders. It was not a line-by-line audit, and the hook cannot see inside compiled code. Review again before changing a revision.

## Materials

Board images go in `materials/` at the paths in `sources/image_manifest.json`. Check them with:

```sh
python -m unittest discover -s tests
```

To refresh from the board, update `sources/board.svg` and `sources/original_images.json`, then run `python scripts/export_materials.py`.
