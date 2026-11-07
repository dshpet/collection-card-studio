# Grandfather clock: a flat plinth carries a narrower trunk case, and the wider hood sits on top of it, crowned by a
# cornice and an arched pediment with a gold finial. The trunk is hollow: back, sides and a front frame around a glass
# pane. Inside, the gold pendulum hangs from a bracket fixed to the back panel and swings a little to the right. The
# round cream face sits in a gold bezel on the hood front with two hands on a centre cap; numerals are left to the restyle.
import math

SCENE = {"category": "2", "backdrop": "#2f9e4a", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#7a4a26", "satin")
    trim = k.mat("#5e361b", "satin")
    inner = k.mat("#8a5a34", "matte")
    gold = k.mat("#f0bf35", "metal")
    face = k.mat("#f4e8c8", "satin")
    dark = k.mat("#2b2420", "satin")

    # Flat base and the molding that steps in to the trunk.
    k.box((0.38, 0.26, 0.14), at=(0, 0, 0.07), m=wood, bevel=0.012)
    k.box((0.32, 0.22, 0.03), at=(0, 0, 0.155), m=trim, bevel=0.008)

    # Trunk case: back, two sides and a front frame around the window, all overlapping at the corners.
    k.box((0.27, 0.025, 0.46), at=(0, 0.09, 0.39), m=inner, bevel=0.003)
    for s in (-1, 1):
        k.box((0.03, 0.21, 0.46), at=(s * 0.125, -0.0, 0.39), m=wood, bevel=0.003)
        k.box((0.04, 0.03, 0.46), at=(s * 0.12, -0.09, 0.39), m=wood, bevel=0.003)
    k.box((0.28, 0.03, 0.08), at=(0, -0.09, 0.21), m=wood, bevel=0.003)
    k.box((0.28, 0.03, 0.04), at=(0, -0.09, 0.60), m=wood, bevel=0.003)
    k.box((0.2, 0.004, 0.38), at=(0, -0.085, 0.40), m=k.mat("#eef8fb", "glass"), bevel=0.001)

    # Pendulum: an arm from the back panel to the pivot, a rod and a disc bob, swung 8 degrees.
    pivot = (0, -0.02, 0.57)
    k.box((0.04, 0.10, 0.025), at=(0, 0.03, 0.57), m=gold, bevel=0.004)
    swing, length = math.radians(8), 0.28
    bob = (pivot[0] + length * math.sin(swing), pivot[1], pivot[2] - length * math.cos(swing))
    k.tube([pivot, bob], 0.012, gold)
    k.cyl(0.065, 0.022, at=bob, rot=(90, 0, 0), m=gold, bevel=0.006)

    # Hood with corner columns.
    k.box((0.36, 0.26, 0.30), at=(0, 0, 0.77), m=wood, bevel=0.012)
    k.box((0.37, 0.27, 0.02), at=(0, 0, 0.63), m=trim, bevel=0.005)
    for s in (-1, 1):
        k.cyl(0.02, 0.27, at=(s * 0.165, -0.13, 0.775), m=trim, bevel=0.004)

    # Round face in a gold bezel, with hands at about ten past ten.
    k.cyl(0.115, 0.02, at=(0, -0.135, 0.775), rot=(90, 0, 0), m=face, bevel=0.004)
    k.torus(0.118, 0.014, at=(0, -0.142, 0.775), rot=(90, 0, 0), m=gold)
    for angle, length, width in ((-60, 0.06, 0.016), (60, 0.09, 0.012)):
        a = math.radians(angle)
        k.box((width, 0.006, length), at=(length / 2 * math.sin(a), -0.149, 0.775 + length / 2 * math.cos(a)),
              rot=(0, angle, 0), m=dark, bevel=0.002)
    k.cyl(0.014, 0.012, at=(0, -0.152, 0.775), rot=(90, 0, 0), m=gold, bevel=0.003)

    # Cornice, arched pediment and finial.
    k.box((0.40, 0.29, 0.03), at=(0, 0, 0.935), m=trim, bevel=0.008)
    k.cyl(0.12, 0.22, at=(0, 0, 0.95), rot=(90, 0, 0), m=wood, bevel=0.01)
    k.sphere(0.026, at=(0, -0.02, 1.09), m=gold)

    # Plain floor a shade lighter than the backdrop.
    k.box((6, 4, 0.1), at=(0, 1.0, -0.05), m=k.mat("#45b85e", "matte"), bevel=0.01, setting=True)
