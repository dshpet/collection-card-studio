# Soup pot on a gas burner: a round teal pot stands on the four arms of a cast-iron grate ring, which rests on the
# black stove top around the burner cap. A ring of flames rises from the cap's ports into the open gap under the
# pot's base: yellow-white cores, and orange tips that flare outward and curl up toward the pot's rim. The lid sits
# in the rim and has a silver knob; two silver loop handles are bolted to the body on mounting plates. Behind the
# stove top stands a yellow tiled wall. Steam and the cast light are left to the image model.
import math

SCENE = {"category": "4", "backdrop": "#ffd23f", "azimuth": 25, "elevation": 11, "lens": 60, "light": "left"}


def flame(k, angle, r0, z0, h, rad, tilt, m):
    # A cone whose base sits at radius r0, height z0, leaning outward by tilt degrees toward the given angle.
    a = math.radians(angle)
    t = math.radians(tilt)
    rc = r0 + 0.5 * h * math.sin(t)
    zc = z0 + 0.5 * h * math.cos(t)
    k.cone(rad, 0.0, h, at=(rc * math.cos(a), rc * math.sin(a), zc), rot=(0, tilt, angle), m=m, verts=16)


def build(k):
    teal = k.mat("#1fa3a0", "gloss")
    teal_dark = k.mat("#17807e", "gloss")
    silver = k.mat("#cfd4da", "metal")
    iron = k.mat("#2a2a2e", "satin")
    cap = k.mat("#3b3b40", "metal")
    core = k.mat("#ffe56a", "glow")
    tip = k.mat("#ff7a1a", "glow")

    # Burner cap on the stove top, and the grate ring with four arms rising and reaching in under the pot.
    k.cyl(0.15, 0.03, at=(0, 0, 0.015), m=cap, bevel=0.006)
    k.cyl(0.11, 0.025, at=(0, 0, 0.042), m=cap, bevel=0.006)
    arm_z = 0.24
    k.torus(0.36, 0.022, at=(0, 0, 0.022), m=iron)
    for i in range(4):
        a = math.radians(45 + i * 90)
        c, s = math.cos(a), math.sin(a)
        k.tube([(0.36 * c, 0.36 * s, 0.022), (0.36 * c, 0.36 * s, arm_z), (0.2 * c, 0.2 * s, arm_z)], 0.02, iron)
        k.cyl(0.024, 0.022, at=(0.36 * c, 0.36 * s, 0.011), m=iron)

    # Flames from the burner ports: a bright core rising, an orange tip flaring outward, and a smaller orange
    # tip curling upward at its end.
    for i in range(16):
        ang = i * 360 / 16
        flame(k, ang, 0.115, 0.05, 0.12, 0.03, 22, core)
        flame(k, ang, 0.15, 0.1, 0.15, 0.03, 58, tip)
        flame(k, ang + 6, 0.26, 0.16, 0.09, 0.022, 28, tip)

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
