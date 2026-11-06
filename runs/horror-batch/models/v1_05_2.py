# Cauldron: a round iron pot on three short straight legs set under the belly, their tops sunk into it and
# their round feet resting on the grass. A thick rolled rim circles the wide open top. The potion is a flat
# glowing surface just below the rim with a few bubbles in it, one purple. Two small lugs sunk into the sides
# each hold a ring handle that hangs just off the wall. It stands on a grass slab, with the plain pink
# backdrop behind it.
import math

SCENE = {"category": "3", "backdrop": "#f27bb5", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26272b", "metal")
    potion = k.mat("#5cf03a", "glow")
    bubble = k.mat("#8dff5e", "gloss")
    purple = k.mat("#a24de0", "gloss")

    # Body: one solid revolved shell, a smooth elliptical belly that flares into the lip under the rim.
    profile = [(0.0, 0.13), (0.08, 0.132), (0.14, 0.138)]
    for i in range(61):
        phi = math.radians(-64 + 104 * i / 60)
        profile.append((0.432 * math.cos(phi), 0.42 + 0.30 * math.sin(phi)))
    profile += [(0.338, 0.628), (0.346, 0.645), (0.356, 0.662), (0.368, 0.678), (0.379, 0.694),
                (0.385, 0.71), (0.35, 0.71), (0.34, 0.68), (0.0, 0.68)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=iron, verts=160)
    k.torus(0.375, 0.035, at=(0, 0, 0.705), rot=(0, 0, 0), m=iron)

    # Potion surface and bubbles resting in it.
    k.cyl(0.345, 0.02, at=(0, 0, 0.685), rot=(0, 0, 0), m=potion, bevel=0.004, verts=128)
    for x, y, r in ((-0.12, -0.05, 0.06), (0.1, 0.1, 0.045), (0.16, -0.12, 0.035), (-0.05, 0.17, 0.03)):
        k.sphere(r, at=(x, y, 0.69 + r * 0.3), m=bubble)
    k.sphere(0.04, at=(0.04, -0.16, 0.705), m=purple)

    # Three short straight legs under the belly: tops sunk well inside it, round feet on the grass.
    for a in (90, 210, 330):
        t = math.radians(a)
        cx, cy = 0.22 * math.cos(t), 0.22 * math.sin(t)
        k.cone(0.05, 0.065, 0.25, at=(cx, cy, 0.125), rot=(0, 0, 0), m=iron)
        k.cyl(0.062, 0.025, at=(cx * 1.04, cy * 1.04, 0.0125), rot=(0, 0, 0), m=iron)

    # Side lugs sunk into the wall, each holding a ring handle that hangs just clear of it.
    for s in (-1, 1):
        k.box((0.12, 0.06, 0.05), at=(s * 0.40, 0, 0.595), rot=(0, 0, 0), m=iron, bevel=0.012)
        k.torus(0.07, 0.018, at=(s * 0.44, 0, 0.53), rot=(0, 90, 0), m=iron)

    # Grass slab, running off the card at the sides and the bottom, with the pink backdrop behind.
    k.box((4, 3.5, 0.12), at=(0, -0.6, -0.06), m=k.mat("#5cc43a", "matte"), bevel=0.01, setting=True)
