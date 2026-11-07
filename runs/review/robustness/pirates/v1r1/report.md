# Review: robustness/pirates/v1r1

| Specialist | Caught | Wrong | Abstained | False alarms |
|---|---:|---:|---:|---:|
| shape_proportions | 6/10 | 3 | 1 | 2/2 |
| viewpoint_depth | 4/10 | 3 | 3 | 2/2 |
| lighting_shading | 5/10 | 4 | 1 | 1/2 |
| value_contrast | 7/10 | 3 | 0 | 1/2 |
| color_palette | 4/10 | 5 | 1 | 2/2 |
| surface_finish | 4/10 | 6 | 0 | 2/2 |
| edges_linework | 5/10 | 5 | 0 | 2/2 |
| composition_hierarchy | 6/10 | 4 | 0 | 1/2 |
| staging_detail | 3/10 | 4 | 3 | 1/2 |

## Art director

Close. Three generated cards could pass as they are (gold pouch, palm tree, parrot), and the rest are near misses rather than obvious fakes. The main tells are value and colour: dark heroes on pale or same-hue backgrounds (anchor, hat, chest), flat front lighting (ship, map), and busy orange plank floors (anchor, wheel). A wide, centred whole-object framing also gives some away, but edit notes can't fix that. Several specialists overreached. The 'invented extras' and 'inflated form' claims are overruled, because real cards here show the same traits. staging_detail picked the real card in four pairs, and the shape and surface specialists often flagged controls and real cards.

1. **Dark hero on a pale or same-hue field. The anchor is near-black on a yellow glow over orange planks, the tricorn is near-black on a washed-out cyan burst, and the chest is red-orange wood with red lining on warm sand. The real cards keep the hero close in value to a mid-key background and set a warm hero against a cool ground, as the barrel, coin sack, spyglass and underwater chest show. This gives the cards away more than anything else.** Lift the dark heroes to a rich mid-dark that keeps its hue, such as blue-grey iron or navy felt. Put a cool sky, sea or mid-cyan ray backdrop behind warm objects. Remove white glows behind the hero.
2. **Flat front lighting. The galleon, the map, the anchor and the chest's front face are lit evenly, with a shallow shadow side and weak contact shadows. The real cards (barrel, rowboat, topiary, real map) light from one side and give the object a clear dark side.** Light from the upper left. Make the right side clearly darker, give each object a firm contact shadow, and shade the folds and sails with a lit face and a shadow face.
3. **Busy, saturated orange wood floors. The anchor deck and the ship's-wheel deck have long, sharp plank grooves and grain over half the card, all in the same orange as the hero, so the hero merges into the floor. The real barrel deck is paler, smoother and quieter.** Draw decks as a few wide, smooth planks with faint grain in a slightly paler, greyer brown, so the wooden hero stands out from them.
4. **A small whole object centred in a wide scene: the galleon on open sea, the wheel on a large deck, the anchor on an empty floor. The real cards crop in close. Edit notes cannot change framing, so this goes into the generation prompt only.** Handle this in fresh generations only (close 3/4 framing, cropped by the card edge). Leave it out of edit notes.
5. **Crisp fine material texture on single props: the pebbled leather on the spyglass and the velvet nap and sharp grain on the chest. The real cards keep surfaces smooth.** Per-card notes only: smooth leather and cloth with a soft sheen.
6. **Overruled: invented extras (lily pads, rope, shell, bubbles, spilled coins, magnifier) and the shape and inflation claims. The real cards here have lily pads (rowboat), a rope and post (snorkel), a shell, bubbles and loose coins (underwater chest), and a magnifier (real map). staging_detail picked the real card in p03, p05, p06 and p12. Shape findings on the controls and real cards (snorkel, topiary, viewer, buoy) show inflated forms are part of this game's look.** Do not remove props for being extras and do not thin or stiffen forms. Neither is a tell in this set.

- p01: Anchor: Change the yellow wall to a clear blue sky with soft sea haze, and remove the bright glow behind the anchor. Make the iron a slightly lighter blue-grey with a darker shadow side on the right. Make the deck a few wide, smooth planks with faint grain in a slightly paler, greyer brown.
- p02: keep
- p03: Galleon: Light from the left so each sail shades from a bright left edge to soft grey on the right, and the right side of the hull goes darker. Add a dark reflection of the hull on the water, and slightly deepen the sea toward the bottom edge. Keep the ship as is.
- p05: Treasure Map: Tone the paper slightly to a warm cream. Light from the upper left so each fold has a lit face and a slightly shaded face. Add a soft, darker shadow under the sheet and the curled edges. Keep the drawing on the map.
- p06: keep
- p07: Ship's Wheel: Make the deck a few wide, smooth planks with faint grain in a slightly paler, greyer brown. Paint the wheel a slightly deeper, richer brown with cool dark-brown shadows. Keep the brass ring and the sea.
- p09: keep
- p10: Pirate Hat: Paint the hat in deep navy felt, slightly lighter than now, with a soft blue-grey sheen on the crown and the top of the brim. Make the background rays alternate clearly between mid and light cyan instead of a pale wash. Keep the feather and the gold trim.
- p11: Spyglass: Make the leather grip smooth dark brown with a soft sheen and no visible grain. Give the brass broader, softer reflections. Keep the lens and the green burst.
- p12: Treasure: Change the lid lining to a smooth, slightly darker maroon without velvet texture. Make the wood planks smooth with faint grain, with a clearly darker right side panel and cool dark-brown shadows. Keep the coins and the sand.
