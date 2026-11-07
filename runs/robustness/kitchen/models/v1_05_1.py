# Sink tap: a chrome kitchen mixer stands on a round flange bolted to the flat back deck of a steel sink. A
# tall round body carries one lever on a side pivot with a small blue tip; the spout rises from the body top
# and bends over in a gooseneck so its outlet points down over the basin, with a few drops falling below it.
# Behind it, a white tiled wall rises from the back of the deck. The framing holds the tap; the sink and wall
# run off the card.
import math

SCENE = {"category": "4", "backdrop": "#ffd84a", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    chrome = k.mat("#d7dce2", "metal")
    blue = k.mat("#2f7fe0", "gloss")
    water = k.mat("#bfe6ff", "glass")

    # Tap, mounted at the back edge of the sink deck.
    bx, by = 0.0, 0.14
    k.cyl(0.075, 0.025, at=(bx, by, 0.0125), m=chrome, bevel=0.008)
    for a in (0, 180):
        t = math.radians(a)
        k.cyl(0.012, 0.012, at=(bx + 0.055 * math.cos(t), by + 0.055 * math.sin(t), 0.031), m=chrome, bevel=0.003)
    k.lathe([(0.0, 0.025), (0.055, 0.025), (0.052, 0.06), (0.046, 0.1), (0.046, 0.30), (0.05, 0.32),
             (0.05, 0.34), (0.034, 0.36), (0.0, 0.36)], at=(bx, by, 0), rot=(0, 0, 0), m=chrome)
    # Lever on a pivot on the right side of the body.
    k.cyl(0.03, 0.03, at=(bx + 0.055, by, 0.27), rot=(0, 90, 0), m=chrome, bevel=0.005)
    k.tube([(bx + 0.07, by, 0.27), (bx + 0.13, by + 0.01, 0.31), (bx + 0.2, by + 0.02, 0.36)], 0.016, chrome,
           curved=True)
    k.sphere(0.024, at=(bx + 0.215, by + 0.022, 0.37), scale=(1.4, 1, 1), m=blue)

    # Gooseneck spout from the body top, over the arc, down to an outlet above the basin.
    cy, cz, rr = by - 0.17, 0.78, 0.17
    pts = [(bx, by, 0.34), (bx, by, 0.5), (bx, by, 0.66)]
    for i in range(13):
        t = math.pi * i / 12
        pts.append((bx, cy + rr * math.cos(t), cz + rr * math.sin(t)))
    pts.append((bx, cy - rr, 0.71))
    k.tube(pts, 0.03, chrome, curved=True)
    k.cyl(0.036, 0.06, at=(bx, cy - rr, 0.69), m=chrome, bevel=0.006)
    # Drops falling from the outlet (free by design).
    ox, oy = bx, cy - rr
    for z, s in ((0.635, 0.011), (0.565, 0.012), (0.48, 0.013)):
        k.sphere(s, at=(ox, oy, z), scale=(1, 1, 1.4), m=water)

    # Steel sink: back deck (running under the wall), side decks, basin walls and floor.
    steel = k.mat("#aeb5bd", "metal")
    basin = k.mat("#9aa2ab", "metal")
    k.box((3.4, 0.40, 0.04), at=(0, 0.22, -0.02), m=steel, bevel=0.012, setting=True)
    for sx in (-1, 1):
        k.box((1.1, 2.0, 0.04), at=(sx * 1.15, -0.98, -0.02), m=steel, bevel=0.012, setting=True)
        k.box((0.03, 2.0, 0.36), at=(sx * 0.585, -0.98, -0.2), m=basin, bevel=0.01, setting=True)
    k.box((1.2, 0.03, 0.36), at=(0, 0.035, -0.2), m=basin, bevel=0.01, setting=True)
    k.box((1.2, 2.0, 0.03), at=(0, -0.98, -0.375), m=basin, bevel=0.01, setting=True)
    k.cyl(0.06, 0.012, at=(0, -0.5, -0.356), m=steel, bevel=0.003, setting=True)

    # White tiled wall behind the sink, its base set down below the deck so no gap shows.
    k.box((4.0, 0.08, 3.2), at=(0, 0.36, 1.5), m=k.mat("#cfd3d6", "matte"), bevel=0, setting=True)
    tile = k.mat("#f6f7f8", "gloss")
    size, gap = 0.2, 0.016
    for i in range(14):
        for j in range(9):
            x = -1.4 + i * (size + gap)
            z = 0.008 + size / 2 + j * (size + gap)
            k.box((size, 0.02, size), at=(x, 0.312, z), m=tile, bevel=0.012, setting=True)
