# Vintage typewriter on a dark wooden desk. A low green body stands on four rubber feet: a sloped front deck
# carries four curved rows of round black keys with silver rims, each on a silver stem rising from the deck,
# and a black space bar on two arms. The taller rear body carries the carriage: a base plate with two end
# plates holding the black roller on its axle, knobs at both ends. A blank sheet rises from the roller and
# leans back. The silver return lever pivots on the left end plate and reaches forward and out.
import math

SCENE = {"category": "3", "backdrop": "#ffc24a", "azimuth": 28, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    green = k.mat("#1f5e3a", "satin")
    black = k.mat("#151515", "gloss")
    rubber = k.mat("#1c1c1c", "matte")
    silver = k.mat("#c9ced6", "metal")
    paper = k.mat("#fbfbf7", "matte")

    # Feet and body
    for x in (-0.44, 0.44):
        for y in (-0.36, 0.36):
            k.cyl(0.04, 0.02, at=(x, y, 0.01), m=rubber)
    deck = k.box((1.0, 0.42, 0.2), at=(0, -0.2, 0.12), m=green, bevel=0.015)
    # slope the top: front edge z 0.10, back edge z 0.26
    k.warp(deck, lambda p: (p[0], p[1], p[2] + (-0.04 + 0.38 * p[1]) * (1 if p[2] > 0 else 0)))
    k.box((1.0, 0.40, 0.30), at=(0, 0.2, 0.17), m=green, bevel=0.02)

    def deck_z(y):
        return 0.256 + 0.38 * y

    # Keys: four curved rows rising toward the back
    for i, n in enumerate((10, 11, 11, 10)):
        y0 = -0.34 + i * 0.08
        for j in range(n):
            x = (j - (n - 1) / 2) * 0.078
            y = y0 + 0.05 * (x / 0.42) ** 2
            top = deck_z(y) + 0.05 + i * 0.012
            base = deck_z(y) - 0.01
            k.cyl(0.01, top - base, at=(x, y, (top + base) / 2), m=silver)
            k.cyl(0.028, 0.018, at=(x, y, top), m=black, bevel=0.004)
            k.torus(0.028, 0.006, at=(x, y, top), m=silver)

    # Space bar on two arms reaching into the deck
    k.box((0.55, 0.035, 0.025), at=(0, -0.445, 0.115), m=black, bevel=0.008)
    for x in (-0.22, 0.22):
        k.tube([(x, -0.445, 0.115), (x, -0.40, 0.11), (x, -0.36, 0.12)], 0.01, silver)

    # Carriage
    k.box((1.06, 0.22, 0.04), at=(0, 0.2, 0.34), m=green, bevel=0.01)
    k.tube([(-0.6, 0.31, 0.345), (0.6, 0.31, 0.345)], 0.012, silver)
    for x in (-0.515, 0.515):
        k.box((0.03, 0.18, 0.16), at=(x, 0.19, 0.43), m=green, bevel=0.008)
    k.cyl(0.07, 1.0, at=(0, 0.18, 0.44), rot=(0, 90, 0), m=black, bevel=0.01)
    k.cyl(0.015, 1.2, at=(0, 0.18, 0.44), rot=(0, 90, 0), m=silver)
    for x in (-0.565, 0.565):
        k.cyl(0.055, 0.05, at=(x, 0.18, 0.44), rot=(0, 90, 0), m=black, bevel=0.01)

    # Paper rising from the front-top of the roller, leaning back
    tilt = 12
    h = 0.42
    by, bz = 0.142, 0.48
    k.box((0.6, 0.006, h), at=(0, by + h / 2 * math.sin(math.radians(tilt)), bz + h / 2 * math.cos(math.radians(tilt))),
          rot=(-tilt, 0, 0), m=paper, bevel=0.002)

    # Return lever on the left end plate
    k.cyl(0.022, 0.03, at=(-0.545, 0.115, 0.46), rot=(0, 90, 0), m=silver)
    k.tube([(-0.55, 0.115, 0.46), (-0.6, 0.04, 0.49), (-0.66, -0.06, 0.51), (-0.69, -0.13, 0.515)],
           0.013, silver, curved=True)
    k.sphere(0.022, at=(-0.69, -0.13, 0.515), m=silver)

    # Dark wooden desk
    k.box((4.0, 2.6, 0.1), at=(0, 0.6, -0.05), m=k.mat("#4a2c18", "matte"), bevel=0.01, setting=True)
