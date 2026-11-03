# Specialist reviewers

Nine specialists, one per art vector, and an art director. `scripts/review.py` runs them.

| Role | Owns | Lens |
|---|---|---|
| [shape_proportions](shape_proportions.md) | Silhouette, proportions, how inflated forms are | Black silhouette |
| [viewpoint_depth](viewpoint_depth.md) | Camera height, faces shown, depth | Surface normals |
| [lighting_shading](lighting_shading.md) | Where light falls, how form turns, shadows | Estimated shading |
| [value_contrast](value_contrast.md) | Light and dark groups | Five grey levels |
| [color_palette](color_palette.md) | Hue roles, chroma, colored shadows | Eight flat colors |
| [surface_finish](surface_finish.md) | Materials, gloss, texture scale | 2× crop of the hero |
| [edges_linework](edges_linework.md) | Boundaries, internal lines | Edge map |
| [composition_hierarchy](composition_hierarchy.md) | Scale, placement, thumbnail read | Thumbnail |
| [staging_detail](staging_detail.md) | Support, props, how busy the card is | Background alone |

[art_director](art_director.md) reads every report and turns them into instructions for the generator.

Two checkers judge each card alone, for mistakes rather than style: [construction](construction.md), whether the object could exist and work, and [perspective](perspective.md), whether it is one consistent space. They see the card beside its object cut from the full-size drawing, and learn from [lessons.json](lessons.json): cards a human marked, with notes. Candidates with a major error are not chosen, and errors on a chosen card become edit notes.

## Rules for every specialist

Evidence and its limits: [TOOLS.md](../TOOLS.md). Each specialist also receives its section of [VOCABULARY.md](../VOCABULARY.md).

- Judge only your vector. Another vector's flaw is not your finding.
- Compare with the real cards, never with general taste. "Nice" and "polished" are not findings.
- Name the place on the card and what you see there. "The cap's board has flat faces and a crisp corner" is a finding. "Better shading" is not.
- A lens shows evidence, not truth. Shading and normal maps are model estimates and leak color.
- Reference cards are 430×480, so do not claim anything finer than about 2 px.
- Say "neither" when your vector gives no reason to choose. A guess presented as a finding is worse than no finding.
- A fix is wording for the image generator: what to draw, in plain visual words, not art theory.

## Modes

- **study:** real cards only. What does this vector always do, what varies, how to say it to a generator.
- **pairs:** cards A and B, blind. One may be drawn by a different process. Which one breaks the real cards' look on your vector, where, and how to fix it.

Twins are the sharpest pairs: a real card and a redraw of the same object from which that card was hidden. Content is equal, so what remains is style. A hidden real card can also sit in a batch of new cards, which measures false alarms. If specialists cannot beat chance on twins, either the style matches or they are blind, so `off-style` cards must be caught first.
