# Soup pot on a gas burner: a round teal pot stands on the four arms of a cast-iron grate ring, which rests on the
# black stove top around the burner cap. A ring of flames rises from the cap's ports into the open gap under the
# pot's base, with yellow-white cores and orange tips curling outward. The lid sits in the rim and has a silver knob;
# two silver loop handles are bolted to the body on mounting plates. Behind the stove top stands a yellow tiled
# wall. Steam and the cast light are left to the image model.
import math

SCENE = {"category": "4", "backdrop": "#ffd23f", "azimuth": 25, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    teal = k.mat("#1fa3a0", "gloss")
    teal_dark = k.mat("#17807e", "gloss")
    silver = k.mat("#cfd4da", "metal")
    iron = k.mat("#2a2a2e", "satin")
    cap = k.mat("#3b3b40", "metal")
    core = k.mat("#fff4b8", "glow")
    tip = k.mat("#ff8a1f", "glow")

    # Burner cap on the stove top, and the grate ring with four arms rising and reaching in under the pot.
    k.cyl(0.15, 0.03, at=(0, 0, 0.015), m=cap, bevel=0.006)
    k.cyl(0.11, 0.025, at=(0, 0, 0.042), m=cap, bevel=0.006)
    arm_z = 0.175
    k.torus(0.36, 0.022, at=(0, 0, 0.022), m=iron)
    for i in range(4):
        a = math.radians(45 + i * 90)
        c, s = math.cos(a), math.sin(a)
        k.tube([(0.36 * c, 0.36 * s, 0.022), (0.36 * c, 0.36 * s, arm_z), (0.18 * c, 0.18 * s, arm_z)], 0.02, iron)
        k.cyl(0.024, 0.022, at=(0.36 * c, 0.36 * s, 0.011), m=iron)

    # Flames from the burner ports: a bright core and an orange tip curling up and outward under the pot.
    for i in range(14):
        a = math.radians(i * 360 / 14)
        c, s = math.cos(a), math.sin(a)
        k.cone(0.026, 0.0, 0.08, at=(0.13 * c, 0.13 * s, 0.09), rot=(-25 * s, 25 * c, 0), m=core, verts=16)
        k.cone(0.018, 0.0, 0.06, at=(0.175 * c, 0.175 * s, 0.13), rot=(-50 * s, 50 * c, 0), m=tip, verts=16)

    # Pot body, sitting on the grate arms.
    z0 = arm_z + 0.02
    body = [(0.0, 0.0), (0.36, 0.0), (0.395, 0.012), (0.41, 0.04), (0.41, 0.44), (0.425, 0.452),
            (0.43, 0.47), (0.415, 0.48), (0.0, 0.48)]
    k.lathe([(r, z + z0) for r, z in body], at=(0, 0, 0), m=teal)

    # Lid resting in the rim, with a silver knob.
    lid = [(0.0, 0.47), (0.425, 0.47), (0.43, 0.485), (0.41, 0.5), (0.36, 0.525), (0.28, 0.552),
           (0.18, 0.571), (0.08, 0.58), (0.0, 0.582)]
    k.lathe([(r, z + z0) for r, z in lid], at=(0, 0, 0), m=teal_dark)
    k.cyl(0.03, 0.04, at=(0, 0, z0 + 0.598), m=silver)
    k.lathe([(0.0, 0.0), (0.05, 0.005), (0.065, 0.025), (0.06, 0.04), (0.035, 0.05), (0.0, 0.052)],
            at=(0, 0, z0 + 0.612), m=silver)

    # Two side handles: a mounting plate bolted to the wall of the pot, a loop handle between its ends.
    hz = z0 + 0.36
    for side in (-1, 1):
        k.box((0.025, 0.24, 0.07), at=(side * 0.415, 0, hz), m=silver, bevel=0.008)
        for y in (-0.085, 0.085):
            k.cyl(0.016, 0.02, at=(side * 0.43, y, hz), rot=(0, 90, 0), m=silver)
        loop = [(side * 0.425, -0.085, hz), (side * 0.49, -0.09, hz + 0.02), (side * 0.53, -0.04, hz + 0.035),
                (side * 0.535, 0.0, hz + 0.038), (side * 0.53, 0.04, hz + 0.035), (side * 0.49, 0.09, hz + 0.02),
                (side * 0.425, 0.085, hz)]
        k.tube(loop, 0.022, silver, curved=True)

    # Black stove top under the burner, and a yellow tiled wall behind it.
    k.box((5, 2.2, 0.08), at=(0, 0.1, -0.04), m=k.mat("#141416", "satin"), bevel=0.01, setting=True)
    k.box((5, 0.1, 3), at=(0, 1.25, 1.5), m=k.mat("#e8b52a", "matte"), bevel=0, setting=True)
    tile = k.mat("#ffd23f", "gloss")
    for col in range(-8, 9):
        for row in range(10):
            k.box((0.28, 0.03, 0.28), at=(col * 0.3, 1.19, 0.15 + row * 0.3), m=tile, bevel=0.02, setting=True)
