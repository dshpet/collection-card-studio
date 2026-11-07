# Satellite: a gold foil box body. On each side a short metal arm runs out of a collar on the body wall into
# a clamp on the inner edge of a rectangular solar panel. Each panel is a dark blue slab in a silver frame,
# split into cells by raised ribs. On top, a short mast carries a small round white dish tipped toward the
# viewer, with a feed horn on a stalk at its centre. It floats, rolled a little so the panels run diagonally.
import math

SCENE = {"category": "1", "backdrop": "#5cb82e", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#d9a521", "metal")
    silver = k.mat("#c9ced6", "metal")
    cell = k.mat("#1d3b8f", "gloss")
    white = k.mat("#f4f5f2", "satin")

    # Body: gold foil box with silver top and bottom plates.
    k.box((0.40, 0.40, 0.46), at=(0, 0, 0), m=gold, bevel=0.025)
    for z in (0.238, -0.238):
        k.box((0.36, 0.36, 0.02), at=(0, 0, z), m=silver, bevel=0.006)

    # Arms and solar panels, one on each side.
    pw, ph = 0.44, 0.36                     # panel width (x) and height (z)
    for s in (-1, 1):
        k.cyl(0.042, 0.03, at=(s * 0.215, 0, 0), rot=(0, 90, 0), m=silver)        # collar on the body
        k.cyl(0.026, 0.14, at=(s * 0.26, 0, 0), rot=(0, 90, 0), m=silver)         # arm
        k.box((0.04, 0.05, 0.08), at=(s * 0.335, 0, 0), m=silver, bevel=0.006)    # clamp on panel edge
        cx = s * (0.33 + pw / 2)
        k.box((pw, 0.03, ph), at=(cx, 0, 0), m=silver, bevel=0.006)               # frame
        k.box((pw - 0.04, 0.04, ph - 0.04), at=(cx, 0, 0), m=cell, bevel=0.004)   # cells
        for i in (1, 2):                                                           # 3 columns
            x = cx - (pw - 0.04) / 2 + i * (pw - 0.04) / 3
            k.box((0.014, 0.046, ph - 0.04), at=(x, 0, 0), m=silver, bevel=0.003)
        k.box((pw - 0.04, 0.046, 0.014), at=(cx, 0, 0), m=silver, bevel=0.003)    # 2 rows

    # Dish on top: mast, a shallow white bowl tipped toward the front (-y), and a feed horn.
    k.cyl(0.03, 0.09, at=(0, 0, 0.29), m=silver)
    tilt = 30
    base = (0, 0, 0.33)
    profile = [(0.0, 0.0), (0.03, 0.002), (0.06, 0.010), (0.09, 0.024), (0.12, 0.043), (0.145, 0.063),
               (0.155, 0.072), (0.15, 0.08), (0.12, 0.058), (0.09, 0.040), (0.06, 0.027), (0.03, 0.020),
               (0.0, 0.018)]
    k.lathe(profile, at=base, rot=(tilt, 0, 0), m=white)
    dy, dz = -math.sin(math.radians(tilt)), math.cos(math.radians(tilt))   # dish axis direction
    tip = (0, 0.14 * dy, base[2] + 0.14 * dz)
    k.tube([(0, 0.01 * dy, base[2] + 0.01 * dz), tip], 0.011, silver)
    k.sphere(0.022, at=tip, m=white)

    k.turn(6, -14, 0)
