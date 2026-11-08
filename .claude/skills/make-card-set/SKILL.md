---
name: make-card-set
description: Produce a collection card set for a theme and free-form producer wishes. Use when someone asks for new cards, a new set or a new collection topic.
---

# Make a card set

The theme is required. Wishes are optional. Do not ask about anything else. If the wishes ask for characters, add `--cast 1` (or 2): character cards show the game's own cast.

1. Run this from the project root, in the background, because it takes about 40 minutes per variant:

   ```sh
   .venv/bin/python -B scripts/make_set.py "<Theme>" --wishes "<wishes>" --variants 3
   ```

   When the set joins others in one collection, add `--alongside <folder> ...` with their run folders, so its objects do not repeat theirs.

   The first line names the run folder, `run: <folder>`. If the run stops at once with `Cannot start`, do what it lists first. If it stops later, or its report lists a card as `missing`, run the same command again: it continues in that folder. Another theme or other wishes get a folder of their own.

2. Show each variant's sheet, `runs/<folder>/variant_N.png` (`variant_N-cast.png` when it has character cards). `runs/<folder>/spec.md` lists every card as planned; point the producer to it. From the top of `runs/<folder>/report.md`, tell the producer which wishes were not followed and why, and which cards are still flagged as possibly upsetting. Name the cards the report marks `review`, `unsure pick` or `missing`.

3. For a variant the producer likes, show it in the game's window:

   ```sh
   .venv/bin/python -B scripts/screen.py <folder> --variant N --color blue
   ```

   Colors are blue, orange, magenta and purple. The result is `runs/<folder>/screen_N.png`.

4. If the producer names a problem that will recur, such as an object type to avoid, add it to `analysis/lessons.md` under Planning, as one line that starts with `- `.

The run needs the Codex and Claude CLIs logged in, Blender on the PATH, a GPU and the board images in `materials/`. Character cards also need the cast cutouts in `library/cast/`, made once by `scripts/cast.py find` and `label`. Never delete an earlier run.
