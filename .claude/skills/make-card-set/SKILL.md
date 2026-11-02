---
name: make-card-set
description: Produce a collection card set for a theme and free-form producer wishes. Use when someone asks for new cards, a new set or a new collection topic.
---

# Make a card set

The theme is required. Wishes are optional. Do not ask about anything else.

1. Run this from the project root. It takes about an hour and continues where it stopped if interrupted:

   ```sh
   .venv/bin/python -B scripts/make_set.py "<Theme>" --wishes "<wishes>" --variants 3
   ```

2. Show each variant's sheet, `runs/<slug>/variant_N.png`, and name the cards `runs/<slug>/report.md` marks as `review`.

3. For a variant the producer likes, show it in the game's window:

   ```sh
   .venv/bin/python -B scripts/screen.py <slug> --variant N --color blue
   ```

   Colors are blue, orange, magenta and purple. The result is `runs/<slug>/screen_N.png`.

The run needs the Codex and Claude CLIs logged in. If a card is wrong, edit `runs/<slug>/plan.json` and delete that card's files in `runs/<slug>/tries/` before rerunning.
