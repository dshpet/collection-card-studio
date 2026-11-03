# Cauldron: a round iron pot stands on three short legs that grow out of its rounded underside; a thick rolled
# rim closes the top, where a flat pool of green potion sits just below the lip with a few bubbles breaking it.
# Two lugs stick out from the shoulders and each holds a hanging ring handle. A small flame sits on the stone
# under the pot, between the legs. The floor is a few large stone flags with cut joints, running back and off
# the card, with the pink backdrop behind.
import math

SCENE = {"category": "3", "backdrop": "#f27fb0", "azimuth": 28, "elevation": 16, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26262b", "satin")
    potion = k.mat("#5cf03a", "gloss")
    fire = k.mat("#ff8a1f", "glow")

    profile = [(0.0, 0.14), (0.14, 0.142), (0.24, 0.155), (0.32, 0.18), (0.38, 0.22), (0.42, 0.27),
               (0.445, 0.33), (0.45, 0.39), (0.44, 0.45), (0.415, 0.51), (0.385, 0.56), (0.365, 0.6),
               (0.36, 0.64), (0.33, 0.66), (0.33, 0.62), (0.0, 0.62)]
    k.lathe(profile, at=(0, 0, 0), m=iron)
    k.torus(0.365, 0.035, at=(0, 0, 0.655), m=iron)

    # Potion surface just below the lip, with bubbles half sunk into it.
    k.cyl(0.335, 0.02, at=(0, 0, 0.635), m=potion, bevel=0.004)
    for x, y, r in ((-0.12, -0.08, 0.06), (0.1, 0.05, 0.05), (0.02, -0.18, 0.04), (-0.05, 0.16, 0.045),
                    (0.2, -0.12, 0.035), (-0.2, 0.06, 0.03)):
        k.sphere(r, at=(x, y, 0.645), scale=(1, 1, 0.8), m=potion)

    # Three short legs, splayed slightly, feet resting on the floor.
    for a in (90, 210, 330):
        t = math.radians(a)
        cx, cy = 0.27 * math.cos(t), 0.27 * math.sin(t)
        k.cone(0.05, 0.065, 0.2, at=(cx, cy, 0.1), m=iron, bevel=0.008)
        k.cyl(0.07, 0.03, at=(cx, cy, 0.015), m=iron, bevel=0.01)

    # Side handles: a lug on each shoulder and a ring hanging through it.
    for s in (-1, 1):
        k.box((0.11, 0.07, 0.06), at=(s * 0.45, 0, 0.53), m=iron, bevel=0.015)
        k.torus(0.075, 0.02, at=(s * 0.5, 0, 0.465), rot=(90, 0, 0), m=iron)

    # Small flame on the stone under the pot.
    k.blob([(0.0, -0.04, 0.03, 0.035, (1, 1, 1.0)), (0.0, -0.04, 0.075, 0.022, (1, 1, 1.6))], fire)

    # Stone floor: large flags with cut joints.
    shades = ("#9c9aa6", "#8e8c98", "#a7a5b0")
    for i in range(-3, 4):
        for j in range(-2, 4):
            off = 0.45 if j % 2 else 0.0
            k.box((0.86, 0.86, 0.12), at=(i * 0.9 + off, j * 0.9 + 0.1, -0.06),
                  m=k.mat(shades[(i + j) % 3], "matte"), bevel=0.03, setting=True)
