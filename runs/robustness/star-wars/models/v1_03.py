# Satellite: a boxy silver body wrapped in gold foil on its lower part. A short round arm leaves the middle of each
# side, ends in a hinge hub and holds a flat solar panel: a silver frame with 4 x 2 dark blue cells set in it. A short
# mast rises from the top and carries a round dish tilted toward the viewer, with a feed rod and a knob at its focus.
# Floating, no setting; the whole hero is rolled and turned a little so the panels run on a diagonal.
SCENE = {"category": "1", "backdrop": "#ff8a2a", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    dark = k.mat("#5a606a", "satin")
    gold = k.mat("#e2aa2f", "metal")
    cell = k.mat("#1f3a8f", "gloss")

    # Body: silver box, gold foil wrap over the lower two thirds.
    k.box((0.34, 0.34, 0.40), at=(0, 0, 0), m=silver, bevel=0.025)
    k.box((0.352, 0.352, 0.24), at=(0, 0, -0.07), m=gold, bevel=0.02)

    # Arms, hinge hubs and panels on both sides.
    for s in (-1, 1):
        k.tube([(s * 0.16, 0, 0), (s * 0.30, 0, 0)], 0.026, silver)
        k.cyl(0.045, 0.05, at=(s * 0.30, 0, 0), rot=(0, 90, 0), m=dark, bevel=0.006)
        k.box((0.04, 0.04, 0.10), at=(s * 0.335, 0, 0), m=silver, bevel=0.006)
        cx = s * 0.62
        k.box((0.56, 0.022, 0.32), at=(cx, 0, 0), m=silver, bevel=0.006)
        w, h, gap = 0.115, 0.13, 0.02
        for i in range(4):
            x = cx - 0.28 + gap + w / 2 + i * (w + gap)
            for j in range(2):
                z = -0.16 + gap + h / 2 + j * (h + gap)
                k.box((w, 0.03, h), at=(x, 0, z), m=cell, bevel=0.004)

    # Mast and dish on top, tilted toward the front (-y).
    k.cyl(0.03, 0.09, at=(0, 0, 0.245), m=dark, bevel=0.005)
    k.cyl(0.045, 0.02, at=(0, 0, 0.29), m=silver, bevel=0.004)
    R, depth, t = 0.17, 0.065, 0.014
    outer = [(R * i / 16, depth * (i / 16) ** 2) for i in range(17)]
    inner = [(R * i / 16, depth * (i / 16) ** 2 + t) for i in range(16, -1, -1)]
    k.lathe(outer + inner, at=(0, 0, 0.30), rot=(25, 0, 0), m=silver)
    k.tube([(0, -0.005, 0.31), (0, -0.055, 0.42)], 0.012, dark)
    k.sphere(0.024, at=(0, -0.058, 0.425), m=gold)

    k.turn(6, -14, 0)
