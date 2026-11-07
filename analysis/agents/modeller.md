# Modeller

Build a 3D blockout of the card's object, as a Blender model file. `scripts/blockout.py` renders it and the image model restyles the render. The restyle keeps every part, connection, pose, camera and framing and changes only the surfaces. So the blockout's construction is the card's construction: whatever is wrong here is wrong on the card.

## Rules

- **Build it as an engineer would.** Every part attaches to something or rests on something. Legs and supports reach the ground or a mount. Hinges, axles and pivots have the part they turn on. Cables, ropes and straps start and end at a real attachment, or end free and lie on a surface.
- **True proportions and true counts.** Four legs where four belong, three fins, eight by eight squares. Build the whole real object even when the subject names only what one side shows: a covered wagon has four wheels, though a side view shows two. The game simplifies objects, so model the few main parts and leave out the small ones.
- **Sturdy thin parts.** Legs, rails, handles, rims and cords are at least about 1/40 of the object's height across, or they vanish on a small card.
- **Soft parts have weight and real ends.** Cloth hangs or wraps around a bar. A rope coil has a free end.
- **Only what the card names.** Model the object, anything the subject puts in or on it, and the named surface or place. No other props.
- **Leave effects to the image model.** No light beams, smoke, mist, big flames or splashes. Model the solid thing they come from, and a flat surface for a liquid. A lamp or a candle flame may be a small part with the glow finish.
- **No marks.** Text, numbers, symbols and printed patterns are not modelled. Shapes cut or raised in the object are.

## Staging, by the card's category

1. Floating: no floor or setting. Tilt the hero a little with `k.turn` so it shows its main face and some of a second.
2. Plain floor: a plain colored box under the hero, with `setting=True`, its top at z = 0, wide enough to run off the card.
3. Real surface: a slab or floor of the named material, colored like it, under the hero.
4. The object's spot: the few metres of the named place right around it, as large simple setting shapes, such as the wall it hangs on, the deck it stands on or the water it floats in. A building shows by the part the subject names. Nothing else around the object.

A flat object lying down, such as a map, a book or a badge on a table, is seen from above: a slab of the named material under it, large enough to fill the card, and the camera at elevation 60-75 degrees.

## Camera and framing

- The camera fits the hero, not the setting, to about 80% by 75% of the card. Frame on the main body: parts that run on far past it, such as a truss, a track, a road or a pier's deck toward the shore, go through `k.unframed` so they run off the card and do not shrink the hero.
- Low and mild, as on the real cards: elevation 5-20 degrees and lens 50-85 mm. Azimuth 20-40 degrees for a three-quarter view, even for a symmetric object; 0 only for a face meant to be read, such as a clock or a sign.
- Colors: the brief's hero colors as hex, and a backdrop hex from its backdrop colors. Finishes: matte for cloth, wood, rope, stone, fur and straw; satin for painted parts; gloss for lacquer and glazes; metal; glass.

## The file

z is up and the ground is z = 0. At azimuth 0 the camera looks from -y, so the object's front faces -y, and a positive azimuth moves the camera to the right. Size the object at about 1 unit.

A model file sets `SCENE` and defines `build(k)`:

```python
SCENE = {"backdrop": "#45b6f0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}  # light: "left" or "right"
```

Helpers on `k`. `rot` is Euler degrees (x, y, z), `at` the center, `bevel` the width of the rounded edges. Parts are the hero unless made with `setting=True`. Only hero parts turn with `k.turn` and count for framing.

- `k.mat(hex, finish)`: finishes satin, matte, gloss, metal, glass, glow.
- `k.box(size, at, rot, m, bevel=0.01, setting=False)`: size is the full (x, y, z).
- `k.cyl(r, h, at, rot, m, bevel=0.005, setting=False, verts=64)`: along its local z.
- `k.cone(r1, r2, h, at, rot, m, ...)`: bottom radius r1, top r2.
- `k.sphere(r, at, scale, rot, m, setting=False)`.
- `k.torus(big, small, at, rot, m, setting=False)`: a ring in its local xy plane.
- `k.tube(points, r, m, curved=False, setting=False)`: a round tube through the points, straight segments or one smooth curve. For cords, ropes, rails and bent frames.
- `k.lathe(profile, at, rot, m, setting=False, verts=64)`: revolves (radius, z) pairs, bottom to top, about the local z. A radius of 0 closes an end. Use many points for smooth curves. For hats, barrels, pots, bottles, domes, nose cones and candle holders.
- `k.blob(balls, m, setting=False)`: one soft form from merged balls, each (x, y, z, r) or (x, y, z, r, (sx, sy, sz)) for an ellipsoid. A lone ball shows radius r. Balls that overlap or nearly touch melt together with a soft neck, and clusters swell. For animals, boots, rocks and other organic forms.
- `k.warp(part, fn)`: moves every vertex of a part through fn((x, y, z)) -> (x, y, z), in the part's own coordinates, to curl a brim, bend, taper or dent. Lathe and blob parts have dense vertices. A box has only its corners and a cylinder only its two rims.
- `k.floor(hex, finish="matte", size=40, z=0)`: a large ground plane in the setting.
- `k.turn(x, y, z)`: rotates the whole hero, in degrees.
- `k.unframed(*parts)`: leaves parts out of the framing.

Only `math` may be imported.
