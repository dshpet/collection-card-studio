---
name: make-card-set
description: Produce a collection card set for a theme and free-form producer wishes. Use when someone asks for new cards, a new set or a new collection topic.
---

# Make a card set

The theme is required. Wishes are optional. Do not ask about anything else. If the wishes ask for characters, add `--cast 1` (or 2): character cards show the game's own cast.

1. Run this from the project root, in the background, because it takes about 40 minutes per variant. If it stops, the same command continues where it left off:

   ```sh
   .venv/bin/python -B scripts/make_set.py "<Theme>" --wishes "<wishes>" --variants 3
   ```

2. Show each variant's sheet, `runs/<slug>/variant_N.png` (`variant_N_cast.png` when it has character cards), and name the cards that `runs/<slug>/report.md` marks as `review`, `unsure pick` or `missing`.

3. For a variant the producer likes, show it in the game's window:

   ```sh
   .venv/bin/python -B scripts/screen.py <slug> --variant N --color blue
   ```

   Colors are blue, orange, magenta and purple. The result is `runs/<slug>/screen_N.png`.

4. If the producer names a problem that will recur, such as an object type to avoid, add it as a line under Planning in `analysis/lessons.md`.

The run needs the Codex and Claude CLIs logged in and Blender on the PATH. A theme that was run before continues in its old folder, so to start a topic fresh, give a new folder name with `--run <name>` and never delete an earlier run.
