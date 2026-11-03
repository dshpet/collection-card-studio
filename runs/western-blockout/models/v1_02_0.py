# Cowboy boot, floating: the toe points +x so the camera sees the side profile and a little of the pointed toe.
# A tall oval shaft with a scalloped top rises from the heel of a blob foot that tapers to a pointed toe. The foot
# rests on a dark sole that steps up into an angled, forward-raked heel block. A gold spur band wraps the back of
# the heel counter, and a short shank carries a rowel on an axle pin.
import math

SCENE = {"category": "1", "backdrop": "#ffc22e", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#b0652e", "matte")
    dark = k.mat("#4a2a17", "matte")
    gold = k.mat("#e7b53c", "metal")

    # Shaft: an open oval tube with V dips at the front and back of the top edge.
    profile = [(0.115, 0.25), (0.118, 0.4), (0.124, 0.6), (0.132, 0.8), (0.14, 1.0),
               (0.124, 1.0), (0.116, 0.8), (0.108, 0.62), (0.0, 0.6)]
    shaft = k.lathe(profile, at=(-0.1, 0, 0), rot=(0, 0, 0), m=leather, verts=96)

    def scallop(p):
        x, y, z = p
        a = math.atan2(y, x)
        lift = max(0.0, (z - 0.7) / 0.3)
        return (x, y * 0.82, z - 0.07 * abs(math.cos(a)) ** 2 * lift)

    k.warp(shaft, scallop)

    # Foot: heel counter to a pointed, slightly upturned toe.
    k.blob([
        (-0.12, 0, 0.27, 0.13),
        (-0.02, 0, 0.22, 0.12, (1, 0.95, 1)),
        (0.08, 0, 0.15, 0.1, (1, 0.95, 0.8)),
        (0.18, 0, 0.1, 0.08, (1.1, 1, 0.75)),
        (0.28, 0, 0.07, 0.055, (1.2, 0.9, 0.7)),
        (0.36, 0, 0.058, 0.036),
        (0.42, 0, 0.056, 0.02),
    ], leather)

    # Sole: a thin pointed outline, raised under the heel and flat under the forefoot.
    sole = k.cyl(1.0, 0.03, at=(0, 0, 0), rot=(0, 0, 0), m=dark, bevel=0.004, verts=96)

    def sole_shape(p):
        x, y, z = p
        X = x * 0.31 + 0.13
        w = 0.12 * (1 - 0.78 * max(0.0, x))
        lift = 0.12 * min(1.0, max(0.0, (0.15 - X) / 0.3))
        return (X, y * w, z + 0.03 + lift)

    k.warp(sole, sole_shape)

    # Angled heel: the bottom is smaller and set forward, so the back face rakes under.
    heel = k.box((0.13, 0.17, 0.13), at=(-0.115, 0, 0.065), m=dark, bevel=0.008)

    def rake(p):
        x, y, z = p
        if z < 0:
            return (x * 0.7 + 0.025, y * 0.8, z)
        return p

    k.warp(heel, rake)

    # Spur: a band around the back of the heel counter, a shank, and a rowel on a pin.
    cx, cz, rb = -0.11, 0.2, 0.128
    arc = [math.radians(70 + i * 11) for i in range(21)]
    k.tube([(cx + rb * math.cos(a), rb * math.sin(a), cz) for a in arc], 0.013, gold, curved=True)
    k.tube([(cx - rb, 0, cz), (-0.3, 0, cz - 0.015), (-0.34, 0, cz - 0.02)], 0.012, gold)
    k.cyl(0.045, 0.012, at=(-0.37, 0, cz - 0.02), rot=(90, 0, 0), m=gold, verts=10, bevel=0.002)
    for i in range(8):
        a = math.radians(i * 45)
        k.cone(0.008, 0.0, 0.03, at=(-0.37 + 0.055 * math.cos(a), 0, cz - 0.02 + 0.055 * math.sin(a)),
               rot=(0, 90 - i * 45, 0), m=gold)
    k.cyl(0.012, 0.03, at=(-0.37, 0, cz - 0.02), rot=(90, 0, 0), m=gold)

    k.turn(0, -8, 10)
