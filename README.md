# Playrix AI Producer test task

Turn a theme and free-form producer wishes into 3–5 complete ten-card sets that could sit next to the [reference collection](materials/02_collection_explanation.md). Full brief: [task](materials/01_task_description.md), [art guide](materials/03_art_guide.md), [Miro board](https://miro.com/app/board/uXjVEUZR5u0=/).

**Status:** the pipeline runs end to end. The final film-genre sets are still to be drawn with the current pipeline. Earlier sets are in `runs/final/` and every run is listed in [runs/README.md](runs/README.md).

Findings on the references: [SYNTHESIS](analysis/SYNTHESIS.md). What was wrong with our cards and what fixed it: [STYLE_GAPS](analysis/STYLE_GAPS.md). Our sets against the references: [COMPARISON](analysis/COMPARISON.md). How it got here: [PROCESS](PROCESS.md).

## Make a set

```sh
.venv/bin/python -B scripts/make_set.py "Western" --wishes "A set for a Movie collection" --variants 3
```

| Stage | What happens |
|---|---|
| Plan | Opus plans the variants by rules taken from the real sets and by the producer's [lessons](analysis/lessons.md). A second call flags cards that could upset players |
| References | Each card gets three real cards: the same art category, backdrop pattern and object class, and among equals the most likely same kind of object, by text search over the card images (`search.py`) |
| Model | For built objects of several parts, Opus writes a Blender model, looks at its render and fixes it, up to two rounds. Simple forms skip this |
| Draw | Codex draws three candidates per card, restyling the model's render where there is one |
| Check | Each candidate is measured like the references: per-category ranges, distance to the real cards in a style embedding, and a blind look at what it shows and how it is staged |
| Choose | The art director compares candidates two at a time, both orders. Close wins are marked for a human look |
| Review | Nine specialists and the art director review each variant blind, with hidden real cards as controls, and write edit notes |
| Edit | Codex applies the notes. An edit stays only if it beats its draft, and every outcome is saved for later runs |
| Deliver | `runs/<slug>/variant_N/`, a sheet per variant and `report.md` |

Rerunning continues where it stopped; `--run <name>` starts a theme fresh in a new folder. `--candidates 1 --review-rounds 0` gives a quick draft. `--cast 1` adds one character card per variant, drawn with the game's cast. To place a variant in the game's window: `scripts/screen.py western --variant 1 --color blue`.

## Teach it

- **Lessons.** [analysis/lessons.md](analysis/lessons.md) holds the rules learned from the producer's ratings, in plain words the planner reads. Edit it to teach the tool. `scripts/experience.py propose` drafts new lessons from rating comments and lost edits, under Proposed, for a person to accept.
- **Experience.** Every edit and whether it beat its draft goes to `analysis/experience.json`. The art director sees past notes that worked and failed.
- **Ratings.** `scripts/rate_ui.py` serves a rating page at http://127.0.0.1:8765: blind twins, set cards beside their references, trials. Answers go to `runs/ratings.json`, the only measure that tracks the producer.

## The cast

The reference collection has one cast: a man with glasses and a mustache, a pig, a sheep, a cow and a rooster. `scripts/cast.py find` cuts them out of the reference cards with SAM 3, `label` records view, pose and outfit, and `sheet` shows them. These real cutouts are the approved library: a character card attaches the clearest ones, and the cast stays itself. Pre-drawing a character and pasting it in looked pasted, and the art director preferred the direct drawing ([STYLE_GAPS](analysis/STYLE_GAPS.md)). Cutouts and cards showing the cast stay out of git.

## Setup

This needs a ROCm or CUDA GPU with PyTorch, the Codex and Claude CLIs logged in, Blender on the PATH, and the board images in `materials/`, which are not in git. Model weights and reference data are not in git either.

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -B scripts/embed.py
.venv/bin/python -B scripts/estimate.py masks marigold
```

DINOv3 and SAM 3 are gated on Hugging Face: put `HUGGING_FACE_API_KEY` in `.env`, then run `scripts/embed.py --models dinov3` and `scripts/cast.py find`.

## Change the generator or the style

`scripts/draw.py` holds the generator, so another model replaces one function. Style wording is high-gain: change one thing, redraw the twins and judge them against the real cards.

```sh
.venv/bin/python -B scripts/validate.py twins --label r9
.venv/bin/python -B scripts/drift.py twins/r9 --no-classifier
.venv/bin/python -B scripts/review.py twins r9 --rater claude-opus-5-5 --lessons baseline r3 r8
```

Model raters misjudge this style without labelled lessons, and no automatic score tracks the producer on a lone card. Pairwise judgements and CSD against the same object's real card do: see [STYLE_GAPS](analysis/STYLE_GAPS.md). The studies behind these choices are in [experiments/](experiments/README.md).

## Layout

| Path | Contents |
|---|---|
| `scripts/` | The pipeline and the reference analysis |
| `experiments/` | One-off studies behind the pipeline's decisions |
| `analysis/` | Analysis outputs. `knowledge.json`, `cards.json`, `lessons.md` and `cast.json` are what the pipeline reads |
| `analysis/agents/` | The specialists, the art director and the modeller. `VOCABULARY.md` and `TOOLS.md` are their language and evidence |
| `runs/` | Every generated card and measurement, indexed in `runs/README.md` |
| `library/` | Cast cutouts and pre-drawn figures. Not in git |
| `materials/`, `sources/` | Task documents, board export and image manifests. Board images are not in git |
| `research/` | Research reports on measuring style and on image generation |

## Reference analysis

Run from the project root. Each step skips finished work where it can.

```sh
.venv/bin/python -B scripts/map_sets.py
.venv/bin/python -B scripts/rate.py cards --rater codex    # also: claude, qwen3.8:27b-q4_K_M, gemma4:31b
.venv/bin/python -B scripts/rate.py sets --rater codex
.venv/bin/python -B scripts/estimate.py masks depth attention marigold
.venv/bin/python -B scripts/embed.py
.venv/bin/python -B scripts/measure.py
.venv/bin/python -B scripts/summarize.py
.venv/bin/python -B scripts/cluster.py
.venv/bin/python -B scripts/knowledge.py
.venv/bin/python -B scripts/build_report.py    # analysis/report.html, opened from disk
```

The forms are defined in `scripts/form.py`.

## External code

BiRefNet, Depth Anything 3 and DeepGaze run upstream code, so each is pinned to a reviewed revision. BiRefNet and the DA3 weights are pinned in `scripts/estimate.py`. The source checkouts are:

```sh
git clone https://github.com/ByteDance-Seed/depth-anything-3.git .models/src/da3
git -C .models/src/da3 checkout 3d835ec
git clone https://github.com/matthias-k/DeepGaze.git .models/src/deepgaze
git -C .models/src/deepgaze checkout c7db17e
```

The review scanned all 295 fetched Python files, read the code that actually runs, and checked every pickled checkpoint with PyTorch's restricted loader. Short test runs under a Python audit hook showed no network connections, subprocesses or writes outside the project and temp folders. It was not a line-by-line audit, and the hook cannot see inside compiled code. Review again before changing a revision. SAM 3, SigLIP 2, DINOv2, DINOv3 and CSD load through `transformers` and `open_clip`, with no remote code.

## Materials

Board images go in `materials/` at the paths in `sources/image_manifest.json`. Check them with:

```sh
.venv/bin/python -B -m unittest discover -s tests
```

To refresh from the board, update `sources/board.svg` and `sources/original_images.json`, then run `.venv/bin/python -B scripts/export_materials.py`.
