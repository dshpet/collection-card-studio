# Collection Card Studio

A tool that turns a theme and a producer's free-form wishes into 3–5 variants of a ten-card collection set, drawn to sit beside a mobile game's own cards. Built for Playrix's AI-producer test task: [brief](materials/01_task_description.md), [collections](materials/02_collection_explanation.md), [art guide](materials/03_art_guide.md), [Miro board](https://miro.com/app/board/uXjVEUZR5u0=/).

![The final sets: Western, Period Drama and Detective, object cards only](runs/final6/final_sets.png)

*The three film sets: [Western](runs/final5/western-2/variant_1.png), [Period Drama](runs/final5/period-drama/variant_1.png) and [Detective](runs/final6/detective/variant_1.png), each with a `spec.md` beside it. Six bonus cards with the game's cast are on the Miro board; they show Playrix characters and stay out of git.*

| The brief asks for | Here |
|---|---|
| An analysis of how the reference sets are built and drawn | [analysis/SYNTHESIS.md](analysis/SYNTHESIS.md); a dashboard, `analysis/report.html`, opens locally with the board images |
| A tool: theme and wishes in, 3–5 variants of a set out | The [make-card-set skill](.claude/skills/make-card-set/SKILL.md) over `scripts/make_set.py` (linked at `.agents/skills/` for Codex) |
| Three film-genre sets, no gold cards | Western, Period Drama and Detective above; [runs/final6/README.md](runs/final6/README.md) lists their folders and plans |
| Our sets against the references | [analysis/COMPARISON.md](analysis/COMPARISON.md) |
| What was tried and why | [PROCESS.md](PROCESS.md), with the evidence in [STYLE_GAPS](analysis/STYLE_GAPS.md), [experiments/](experiments/README.md) and [runs/](runs/README.md) |

## Approach

- **Hold the object equal to measure style.** A twin is a real card redrawn from a text brief with that card hidden, so the object is the same and what differs is mostly style. Every change to the style text was judged on twins.
- **Compare, don't score.** No score of a lone card followed a human's grades, but pairwise choices did. The pipeline picks between candidates two at a time, in both orders.
- **Calibrate model judges before trusting them.** Without labelled examples, model reviewers called the real card the fake 12 of 12 times: they expect game art to be glossier than it is.
- **Geometry for construction, words for style.** Built objects get a Blender model that the image model restyles. Simple forms are drawn from words.
- **The producer teaches in plain words.** Comments become rules in [lessons.md](analysis/lessons.md), which the planner reads. Nobody edits code to change what gets planned.

## Results

The producer here is the author, playing the brief's producer. Every human grade is theirs unless noted; an outside artist graded the pre-final sets.

- **Final sets.** Drawn once, then three fix rounds redrew 17, 8 and 2 cards, almost all of them cards the producer had commented on. Set grades went from 4, 4, 4 to 5, 5, 5 after the second round; the third answered the one remaining comment, on the Magnifier, and was not graded again. Card means, latest grade per card, are 4.5 Western, 3.8 Period Drama and 4.0 Detective, and the six cast cards are at 5.0. The outside artist gave the pre-final cards 3.1 of 5.
- **Autonomy.** One command makes a set with no human step, such as the [pre-final Detective](runs/prefinal/detective/variant_1.png), one of three variants. The final sets added the producer's pass: plans composed from graded variants, then fix rounds through the same tool with `--keep`. In those rounds a few Blender models and three picks were adjusted by hand; a producer's note now reaches the modeller directly.
- **Style.** Blind, the producer still finds our drawing in 24 of 32 twins of the final style, down from 31 of 32 for the first. Calibrated model reviewers are at chance on 16 of the same twins, so the producer stays the measure.
- **Construction.** In a six-object trial, Blender models cut broken cards from 5 of 12 to 1, and to none once the models were fixed (grade 3.7 against 2.2). Only built, multi-part objects get a model.
- **Plans matter most.** Between two graded batches the mean rose from 3.63 to 3.97: half of that came from three character cards, most of the rest from better objects. Low grades traced back to the plan and became lessons.
- **Robustness.** 19 odd or hostile requests (emoji and non-English themes, brands, franchises, weapons, gore, prompt injection) all produced plans, with forbidden wishes declined and named in the report. War and Gangsters kept three cards flagged for a person.
- **Generator.** On the same twins and prompts the art director preferred Codex to Nano Banana Pro 11 to 0 and to Qwen-Image-2.1 39 to 1. CSD agrees for Qwen and is split for Nano Banana Pro (5 of 11). The prompts were tuned on Codex.

## Make a set

```sh
.venv/bin/python -B scripts/make_set.py "Western" --wishes "A set for a Movie collection" --variants 3
```

```mermaid
flowchart LR
    T[Theme and wishes] --> P[Plan] --> R[References] --> M[Blender model] --> D[Draw candidates]
    D --> C[Check] --> CH[Choose pairwise] --> RV[Review and edit] --> V[Variants]
    A[(Reference analysis)] --> P & R & C
    L[(Lessons)] --> P
    RV -- edit outcomes --> X[(Experience)] --> RV
    U[Producer ratings] -- proposed lessons --> L
```

| Stage | What happens |
|---|---|
| Plan | Claude Sonnet plans the variants by rules taken from the real sets and the producer's [lessons](analysis/lessons.md). A second call flags cards that could upset players, and the plan is repaired at most twice. Declined wishes and cards still flagged head the report. `spec.md` describes the set card by card before drawing |
| References | Each card gets three real cards of the same art category, backdrop pattern and object class; text search over the card images breaks ties |
| Model | For built objects of several parts, Claude Opus writes a Blender model, looks at its render and fixes it, up to two rounds |
| Draw | Codex's image model draws three candidates per card, restyling the model's render where there is one |
| Check | Each candidate is measured like the references: per-category ranges, CSD distance to the real cards, and a blind look at what it shows |
| Choose | The art director compares candidates two at a time, in both orders. Close wins are marked for a human look |
| Review | Nine specialists, one each for shape, viewpoint, light, value, color, surface, edges, composition and staging, review each variant beside hidden real cards; the director turns their reports into edit notes |
| Edit | Codex applies the notes. An edit stays only if it beats its draft, and the outcome is saved for later runs |
| Deliver | `runs/<theme>/variant_N/`, a sheet per variant and `report.md`, which marks cards for a look as `review` (failed a check), `unsure pick` (a close choice) or `missing` |

A run first checks that its tools and data are in place. Rerunning the same request continues where it stopped; another request for the same theme gets `runs/<theme>-2`. Options:

- `--alongside <folder> ...`: other sets of the same collection, whose objects the plan must not repeat.
- `--plan <file>`: draw a plan a producer has checked, such as those in `runs/plans/`.
- `--cast N`: add N character cards per variant, drawn with the game's cast.
- `--keep <folder>` with `--plan` and `--run`: a fix round. Cards whose plan is unchanged keep their drawings and picks; only the others are drawn again. A card's `note`, such as the producer's fix, closes its brief, and the review may not undo it.
- `--candidates 1 --review-rounds 0`: a quick draft.
- `scripts/screen.py <folder> --variant 1 --color blue` places a variant in the game's window.

A variant takes about 40 minutes. One run peaks at about 5 GB of GPU memory; Blender renders on the CPU, about 10 s a render. The Blender models are Python written by Claude and run locally with the user's rights, so run the tool only on your own machine.

## Teach it

- **Lessons:** [analysis/lessons.md](analysis/lessons.md) holds rules learned from the producer, in plain words the planner reads. Edit it to teach the tool. `scripts/experience.py propose` drafts new lessons from rating comments and lost edits, for a person to accept.
- **Experience:** every edit and whether it beat its draft goes to `analysis/experience.json`; the director sees past notes that won and lost.
- **Ratings:** `scripts/rate_ui.py` serves a blind rating page at http://127.0.0.1:8765. Answers go to `runs/ratings.json`.

## The cast

The reference collection has one cast: a man with glasses and a mustache, a pig, a sheep, a cow and a rooster. `scripts/cast.py find` cuts them out of the reference cards with SAM 3, and `label` records view, pose and outfit. A character card attaches the clearest cutouts, so the cast stays itself. Cutouts and cards showing the cast are Playrix art and stay out of git.

## Setup

Needs a ROCm or CUDA GPU with PyTorch, the Codex and Claude CLIs logged in, Blender on the PATH, and the board images in `materials/` at the paths in `sources/image_manifest.json`. Board images, model weights and derived data are not in git.

```sh
python -m venv --system-site-packages .venv    # PyTorch for your GPU comes from the system
.venv/bin/pip install -r requirements.txt
.venv/bin/python -B -m unittest discover -s tests    # the board images are complete and unchanged
.venv/bin/python -B scripts/embed.py
.venv/bin/python -B scripts/estimate.py masks marigold
```

DINOv3 and SAM 3 are gated on Hugging Face: put `HUGGING_FACE_API_KEY` in `.env`, then run `scripts/embed.py --models dinov3` and `HF_HUB_OFFLINE=0 .venv/bin/python -B scripts/cast.py find`, then `cast.py label`. Only these gated downloads get the key.

BiRefNet, Depth Anything 3 and DeepGaze run upstream code, so each is pinned to a reviewed revision: weights in `scripts/estimate.py`, sources `depth-anything-3` at `3d835ec` and `DeepGaze` at `c7db17e` in `.models/src/`.

## Change the generator or the style

`scripts/draw.py` holds the generator, so another model replaces one function; `experiments/generators.py` shows two. Style wording is high-gain: change one thing, redraw the twins and compare them with their real cards.

```sh
.venv/bin/python -B scripts/validate.py twins --label r9
.venv/bin/python -B scripts/review.py twins r9
```

## Layout

| Path | Contents |
|---|---|
| `scripts/` | The pipeline and the reference analysis |
| `experiments/` | One-off studies behind the pipeline's decisions |
| `analysis/` | Findings and analysis outputs. The pipeline reads `knowledge.json`, `cards.json`, `cast.json`, `lessons.md`, `experience.json` and `judge_lessons.json`; `VOCABULARY.md` and `TOOLS.md` are the specialists' language and evidence |
| `analysis/agents/` | The specialists, the art director and the modeller |
| `runs/` | Every generated card and measurement, indexed in `runs/README.md` |
| `research/` | Literature, market research and a check of current models and tools ([index](research/README.md)) |
| `materials/`, `sources/` | The brief, the board export and image manifests |
| `library/` | Cast cutouts. Not in git |

## Reference analysis

Run from the project root; each step skips finished work. The form every rater fills is in `scripts/form.py`.

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

To refresh the materials from the board, update `sources/board.svg` and `sources/original_images.json`, then run `scripts/export_materials.py`.

## Glossary

- **Producer:** the author, playing the brief's producer. Every human grade in `runs/ratings.json` is theirs unless noted.
- **Twin:** a real card redrawn from a text brief with that card hidden from the generator. The object is the same, so what differs is mostly style, with some pose and framing.
- **Style rounds:** versions of the style text: `baseline` and `r1`–`r8` on 12 twins (`runs/twins`); `old` (the first style), `final`, `r3`, `r9` and `p1`–`p3` on 40 (`runs/twins40`). The current text is in `scripts/style.py`. `runs/final/` holds early picks drawn in the `final` style, not the final sets.
- **Blockout:** a Blender model of the object, rendered and restyled by the image model.
- **Category 1–5:** the art guide's staging: floating, plain floor, real surface, in its place, characters.
- **CSD:** Contrastive Style Descriptors, a style embedding. Its similarity to the same object's real card is the one embedding measure that tracked the producer.
- **Calibrated reviewer:** a model reviewer shown labelled twins, with the answers, before it judges.
- **Specialists and director:** nine model reviewers, one per aspect of the art, and an art director, in [analysis/agents/](analysis/agents/README.md).

## License

[PolyForm Noncommercial 1.0.0](LICENSE.md): free for personal, research and other noncommercial use. Commercial use needs the author's written permission.
