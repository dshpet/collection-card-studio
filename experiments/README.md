# Experiments

One-off studies behind the pipeline's decisions. Each ran once, its results are in `runs/` and its findings in [analysis/STYLE_GAPS.md](../analysis/STYLE_GAPS.md). They import the pipeline's modules from `scripts/` and run the same way: `.venv/bin/python -B experiments/<name>.py`.

| Script | Question | Answer |
|---|---|---|
| `trial.py` | Does a Blender blockout fix construction? | Yes: no broken card against 5 of 12 from the brief. One first-arm model, m04, used a light-beam finish since removed, so it no longer renders |
| `trial2.py`, `photos.py` | Does a soft render or a real photo help the blockout? | No: soft lost designed shape, photos taught engineering truth that reads as wrong |
| `score.py` | Can any score of a lone card follow the producer's grades? | No. Only CSD against the same object's real card tracks the producer |
| `prefer.py` | Can a judge pick the closer of two drawings? | Yes, 61% for the director, 76-78% when confident. Construction: no judge beats chance |
| `tune.py` | Can the director's notes be tuned automatically? | No: gains on the tuning half did not hold on held-out pairs |
| `param.py` | Which measured style parameters are off, and does one line fix them? | Tone is off, but no tone round beat the final style for the producer |
| `cast_trial.py` | Can the game's characters appear on new cards and stay themselves? | Yes, best drawn in one go with real cutouts attached. Pre-drawn and pasted figures look pasted |
| `search_trial.py` | Do search-picked references, or five instead of three, bring drawings closer to the real card? | No clear change, so search only breaks ties and cards keep three |
| `plain_check.py` | Where does the invented jewel on the sheriff star come from? | From the colors line: an accent hue named as a gem. Saying "no gem" does not help |
| `shape_check.py` | Does naming the canonical shape keep a front-on clock round? | No: roundness 0.95 either way, against 0.995 on the real card |
| `fire_check.py` | Can the model draw a convincing fire? | Yes by eye, when the subject describes the real card's fire. References add nothing. In batch 2 the campfire got 5, the cauldron 1 |
| `wording_check.py` | Does the batch's plainness come from the subject wording? | Yes, in 4 of 4 objects: the earlier wording brings back the badge, spur, bent tip and lever |
| `colors.py` | Which backdrop colors do the real cards use, and do ours follow them? | Mostly cool, loosely opposite the hero, surface often in the backdrop's hue. Ours are more saturated and more contrasting |
| `color_logic.py` | What logic picks the real backdrop color? | Opposite temperature to the hero (84% for warm heroes) and never the hero's own hue; not strict complements. Real backdrops carry more light-dark pattern than ours on ledges and surfaces |
| `batch2_check.py` | Did the second batch move toward the real cards? | Yes on turn, backdrop colors and saturation; the light pool and edge crops did not take |
| `shared_plans.py` | Do variants drift less if they share the most iconic objects? | The producer asked for it; the rule is now a lesson. Its plans are in `runs/plans/` |
| `outfit_check.py` | Do character cards borrow the outfits of their cutouts? | Yes; a prompt line and outfit-free cutouts first fix it for the animals |
| `robustness.py` | Does the planner hold its rules on odd, risky and hostile requests? | Mostly: all 19 gave plans with brands, weapons, vices, text and injected instructions declined. After two repairs War and Gangsters kept three cards still flagged, and Elections stayed a voting set. The sensitivity check is a model call and varies between runs |
| `csd_plus.py` | Does hubness-corrected CSD follow the producer's pairs better? | A lean: 128 to 132 of 218, within noise |
| `grade.py` | Does a measured backdrop grade bring twins closer to their real cards? | No: CSD 0.910 to 0.909, 21 of 40 closer |
| `generators.py` | Does another image model draw closer than Codex? | No: the director preferred Codex to Nano Banana Pro 11 to 0 (11 twins) and to Qwen-Image-2.1 39 to 1 (40 twins); CSD agrees for Qwen |
| `outside_rating.py` | Does an outside artist find our pre-final cards among real ones, and how do they grade them? | Not by a lay eye: 23 of 72 right, inverted (p 0.003), because she took bright, large, clean subjects for AI. Cards 3.1 of 5, 9 of 75 broken on perspective; ours read grainier. A page in Ukrainian: a blind real-or-AI test first, then the brief, the sets and the cards beside their references |
| `perspective_check.py` | Does a one-camera fit (GeoCalib) find the cards called off in perspective? | No: near-zero confidence on cards; at 10% false alarms on real cards it finds 3 of 18 of the producer's and 0 of 10 of the outside rater's |
| `blockout_drift.py` | Do blockout cards break where the drawing leaves the blockout? | No: drawings keep the render's outline (IoU 0.90) whether broken or not. The breaks sit in the setting, in the render or added by the drawing |
| `smooth_check.py` | Does edge-preserving smoothing take out the grain, and can pixels see it? | Pixels see it on twins: fewer flat surface pixels than their real cards (32 of 40), twice the gap when the brief names a material. Smoothing restores them but not CSD (13-18 of 40 closer). Not a judge: 104 of 218 producer pairs. `--flat` scores any twin round |
| `night.py` | Overnight arms before the final, one change each against a shared control: smooth surfaces, one camera, planner colors, blockout frame size | Adopted: smooth surfaces for cards drawn from text (flat share nearer the real cards on 27 of 40, no gloss or CSD cost), rich planner colors (CSD 29 of 40), blockouts framed at half the real gap (categories 2-4). One camera and the perspective arms wait on the producer; see STYLE_GAPS. Also writes the final's plan files |
| `plan_review.py` | Before the final, are the chosen variants the best plans on the evidence? | Not quite: five Western cards were swapped for ones the producer graded 5 or that the pre-final lacked, two Detective cards and one Period Drama card swapped, two reworded |
| `final_review.py` | The morning review page: final sets with a grade each, cards with references and candidates, and the blind arms | Pending the producer |
| `final_numbers.py` | How do the final sets compare with the real sets and their pre-final variants? | Subject chroma near the real cards (0.125 against 0.128), margins halfway; sets less alike card to card than real ones, mostly by color (grey copies: Period Drama 0.635, in the real range). See COMPARISON |
