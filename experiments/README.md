# Experiments

One-off studies behind the pipeline's decisions. Each ran once, its results are in `runs/` and its findings in [analysis/STYLE_GAPS.md](../analysis/STYLE_GAPS.md). They import the pipeline's modules from `scripts/` and run the same way: `.venv/bin/python -B experiments/<name>.py`.

| Script | Question | Answer |
|---|---|---|
| `trial.py` | Does a Blender blockout fix construction? | Yes: no broken card against 5 of 12 from the brief |
| `trial2.py`, `photos.py` | Does a soft render or a real photo help the blockout? | No: soft lost designed shape, photos taught engineering truth that reads as wrong |
| `score.py` | Can any score of a lone card follow the user's grades? | No. Only CSD against the same object's real card tracks the user |
| `prefer.py` | Can a judge pick the closer of two drawings? | Yes, 61% for the director, 76-78% when confident. Construction: no judge beats chance |
| `tune.py` | Can the director's notes be tuned automatically? | No: gains on the tuning half did not hold on held-out pairs |
| `param.py` | Which measured style parameters are off, and does one line fix them? | Tone is off, but no tone round beat the final style for the user |
| `cast_trial.py` | Can the game's characters appear on new cards and stay themselves? | Yes, best drawn in one go with real cutouts attached. Pre-drawn and pasted figures look pasted |
| `search_trial.py` | Do search-picked references, or five instead of three, bring drawings closer to the real card? | No clear change, so search only breaks ties and cards keep three |
| `plain_check.py` | Where does the invented jewel on the sheriff star come from? | From the colors line: an accent hue named as a gem. Saying "no gem" does not help |
