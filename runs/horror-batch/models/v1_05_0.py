# Cauldron: a round iron pot on three short legs that splay out from the grass into its belly. A thick
# rolled rim circles the wide open top. The potion is a flat glowing surface just below the rim with a few
# bubbles in it, one purple. Two small lugs on the sides each hold a ring handle that hangs against the
# wall. It stands on a grass floor with the horizon behind it, as on the real category-3 cards.
import math

SCENE = {"category": "3", "backdrop": "#f27bb5", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26272b", "metal")
    potion = k.mat("#5cf03a", "glow")
    bubble = k.mat("#8dff5e", "gloss")
    purple = k.mat("#a24de0", "gloss")

    # Body: one solid revolved shell, closed just under the potion surface.
    profile = [(0.0, 0.13), (0.12, 0.135), (0.22, 0.155), (0.3, 0.19), (0.36, 0.24), (0.40, 0.30),
               (0.425, 0.37), (0.432, 0.44), (0.425, 0.51), (0.405, 0.57), (0.38, 0.62), (0.365, 0.65),
               (0.37, 0.675), (0.385, 0.695), (0.385, 0.71), (0.35, 0.71), (0.34, 0.68), (0.0, 0.68)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=iron)
    k.torus(0.375, 0.035, at=(0, 0, 0.705), rot=(0, 0, 0), m=iron)

    # Potion surface and bubbles resting in it.
    k.cyl(0.345, 0.02, at=(0, 0, 0.685), rot=(0, 0, 0), m=potion, bevel=0.004)
    for x, y, r in ((-0.12, -0.05, 0.06), (0.1, 0.1, 0.045), (0.16, -0.12, 0.035), (-0.05, 0.17, 0.03)):
        k.sphere(r, at=(x, y, 0.69 + r * 0.3), m=bubble)
    k.sphere(0.04, at=(0.04, -0.16, 0.705), m=purple)

    # Three short legs, splayed slightly outward, from the ground into the underside of the belly.
    for a in (90, 210, 330):
        t = math.radians(a)
        cx, cy = 0.25 * math.cos(t), 0.25 * math.sin(t)
        k.cone(0.05, 0.065, 0.22, at=(cx * 1.08, cy * 1.08, 0.11), rot=(-8 * math.sin(t), 8 * math.cos(t), 0),
               m=iron)
        k.cyl(0.06, 0.025, at=(cx * 1.14, cy * 1.14, 0.0125), rot=(0, 0, 0), m=iron)

    # Side lugs, each holding a ring handle that hangs against the wall.
    for s in (-1, 1):
        k.box((0.1, 0.06, 0.05), at=(s * 0.42, 0, 0.595), rot=(0, 0, 0), m=iron, bevel=0.012)
        k.torus(0.07, 0.018, at=(s * 0.455, 0, 0.53), rot=(0, 90, 0), m=iron)

    k.floor("#5cc43a", "matte")
