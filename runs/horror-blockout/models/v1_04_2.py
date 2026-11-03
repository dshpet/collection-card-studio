# Cauldron: a round iron pot stands on three short legs that grow out of its rounded underside, one at the front
# and two at the back sides so all three read; a thick rolled rim closes the top, where a flat pool of green potion
# sits just below the lip with a few bubbles breaking it. Two lugs stick out from the shoulders and each holds a
# hanging ring handle. A small teardrop flame burns on two crossed sticks on the stone under the pot, between the
# legs. The floor is mid-grey stone flags set in dark mortar, running back and off the card, with the pink
# backdrop behind.
import math

SCENE = {"category": "3", "backdrop": "#f27fb0", "azimuth": 28, "elevation": 16, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26262b", "satin")
    potion = k.mat("#5cf03a", "gloss")
    fire = k.mat("#ff8a1f", "glow")
    wood = k.mat("#5a3620", "matte")

    # Smooth belly: an ellipse in profile, taller above its widest point, then a short flared neck and lip.
    profile = [(0.0, 0.12)]
    for i in range(41):
        z = 0.125 + i * (0.6 - 0.125) / 40
        d = (z - 0.38) / (0.26 if z < 0.38 else 0.34)
        profile.append((0.45 * math.sqrt(max(0.0, 1 - d * d)), z))
    profile += [(0.35, 0.615), (0.355, 0.63), (0.362, 0.645), (0.33, 0.665), (0.33, 0.62), (0.0, 0.62)]
    k.lathe(profile, at=(0, 0, 0), m=iron, verts=128)
    k.torus(0.362, 0.035, at=(0, 0, 0.655), m=iron)

    # Potion surface just below the lip, with bubbles half sunk into it.
    k.cyl(0.33, 0.02, at=(0, 0, 0.625), m=potion, bevel=0.004)
    for x, y, r in ((-0.12, -0.08, 0.06), (0.1, 0.05, 0.05), (0.02, -0.18, 0.04), (-0.05, 0.16, 0.045),
                    (0.2, -0.12, 0.035), (-0.2, 0.06, 0.03)):
        k.sphere(r, at=(x, y, 0.635), scale=(1, 1, 0.8), m=potion)

    # Three short legs, one at the front and two at the back sides, their tops sunk into the rounded underside.
    for a in (270, 30, 150):
        t = math.radians(a)
        cx, cy = 0.27 * math.cos(t), 0.27 * math.sin(t)
        k.cone(0.05, 0.065, 0.2, at=(cx, cy, 0.1), m=iron, bevel=0.008)
        k.cyl(0.07, 0.03, at=(cx, cy, 0.015), m=iron, bevel=0.01)

    # Side handles: a lug on each shoulder and a ring hanging through it.
    for s in (-1, 1):
        k.box((0.11, 0.07, 0.06), at=(s * 0.45, 0, 0.53), m=iron, bevel=0.015)
        k.torus(0.075, 0.02, at=(s * 0.5, 0, 0.465), rot=(90, 0, 0), m=iron)

    # Small fire under the pot: two crossed sticks on the stone and a teardrop flame rising from them.
    for a in (35, -35):
        k.cyl(0.014, 0.16, at=(0, 0.03, 0.016), rot=(0, 90, a), m=wood, bevel=0.004)
    k.blob([(0.0, 0.03, 0.05, 0.03), (0.0, 0.03, 0.078, 0.02), (0.0, 0.03, 0.1, 0.01)], fire)

    # Stone floor: mid-grey flags set in a dark mortar bed, running far back.
    k.box((16, 16, 0.1), at=(0, 4, -0.07), m=k.mat("#38353c", "matte"), bevel=0, setting=True)
    shades = ("#6e6a72", "#625e68", "#78747d")
    for i in range(-5, 6):
        for j in range(-2, 9):
            off = 0.45 if j % 2 else 0.0
            k.box((0.88, 0.88, 0.12), at=(i * 0.9 + off, j * 0.9 + 0.1, -0.06),
                  m=k.mat(shades[(i + j) % 3], "matte"), bevel=0.02, setting=True)
