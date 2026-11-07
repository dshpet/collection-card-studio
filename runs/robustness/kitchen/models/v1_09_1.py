# Soup pot on a gas burner: the round teal pot stands on a four-arm cast-iron grate whose arms end in feet on the
# black stove top. The burner sits under the grate's centre with a ring of glowing flame tongues, yellow-white cores
# with orange tips leaning outward, reaching up around the pot's base. The lid sits on the rim with a silver knob;
# two silver loop handles are bolted to the sides through plates. A yellow tiled wall stands behind the stove top.
# Steam and cast light are left to the image model.
import math

SCENE = {"category": "4", "backdrop": "#ffd23a", "azimuth": 25, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    teal = k.mat("#1fa3a0", "gloss")
    teal_dark = k.mat("#17807e", "gloss")
    silver = k.mat("#cfd4db", "metal")
    iron = k.mat("#2b2b2e", "satin")
    burner = k.mat("#55585e", "metal")
    core = k.mat("#fff3b0", "glow")
    tips = k.mat("#ff8a1f", "glow")

    # Burner: base ring and cap sitting on the stove top.
    k.cyl(0.17, 0.04, at=(0, 0, 0.02), rot=(0, 0, 0), m=burner, bevel=0.008)
    k.cyl(0.13, 0.03, at=(0, 0, 0.055), rot=(0, 0, 0), m=iron, bevel=0.006)

    # Flame: a ring of tongues around the burner cap, leaning outward, yellow-white core and orange tips.
    for i in range(12):
        a = i * 30
        ar = math.radians(a)
        c, s = math.cos(ar), math.sin(ar)
        k.cone(0.028, 0.0, 0.10, at=(0.155 * c, 0.155 * s, 0.115), rot=(0, 25, a), m=core)
        k.cone(0.022, 0.0, 0.10, at=(0.20 * c, 0.20 * s, 0.17), rot=(0, 35, a), m=tips)

    # Grate: an inner ring and four arms out to feet standing on the stove top.
    gz = 0.24
    k.torus(0.24, 0.016, at=(0, 0, gz), rot=(0, 0, 0), m=iron)
    for i in range(4):
        a = i * 90 + 45
        ar = math.radians(a)
        k.box((0.30, 0.04, 0.035), at=(0.37 * math.cos(ar), 0.37 * math.sin(ar), gz), rot=(0, 0, a), m=iron,
              bevel=0.006)
        fx, fy = 0.50 * math.cos(ar), 0.50 * math.sin(ar)
        k.box((0.045, 0.045, gz + 0.0175), at=(fx, fy, (gz + 0.0175) / 2), rot=(0, 0, a), m=iron, bevel=0.006)

    # Pot body, resting on the grate.
    base = gz + 0.0175
    body = [(0.0, base), (0.33, base), (0.37, base + 0.006), (0.395, base + 0.025), (0.40, base + 0.06),
            (0.40, base + 0.40), (0.41, base + 0.41), (0.418, base + 0.425), (0.412, base + 0.435),
            (0.39, base + 0.435), (0.0, base + 0.435)]
    k.lathe(body, at=(0, 0, 0), rot=(0, 0, 0), m=teal, verts=128)
    top = base + 0.435

    # Lid: a low dome resting on the rim, with a silver knob.
    lid = [(0.0, top), (0.405, top), (0.41, top + 0.012), (0.39, top + 0.03)]
    for j in range(1, 9):
        t = j / 8
        lid.append((0.39 * math.cos(t * math.pi / 2), top + 0.03 + 0.09 * math.sin(t * math.pi / 2)))
    k.lathe(lid, at=(0, 0, 0), rot=(0, 0, 0), m=teal_dark, verts=128)
    lid_top = top + 0.12
    k.cyl(0.025, 0.04, at=(0, 0, lid_top + 0.015), rot=(0, 0, 0), m=silver)
    k.sphere(0.05, at=(0, 0, lid_top + 0.05), scale=(1, 1, 0.6), m=silver)

    # Handles: a bolt plate on each side of the body, two bolts, and a silver loop.
    hz = base + 0.33
    for side in (-1, 1):
        k.box((0.02, 0.22, 0.06), at=(side * 0.402, 0, hz), rot=(0, 0, 0), m=silver, bevel=0.008)
        for y in (-0.08, 0.08):
            k.sphere(0.016, at=(side * 0.414, y, hz), m=silver)
        loop = [(side * 0.405, -0.08, hz), (side * 0.47, -0.075, hz + 0.01), (side * 0.51, 0.0, hz + 0.015),
                (side * 0.47, 0.075, hz + 0.01), (side * 0.405, 0.08, hz)]
        k.tube(loop, 0.022, silver, curved=True)

    # Setting: black stove top, and a yellow tiled wall behind it (raised tiles on grout).
    k.box((3.4, 2.2, 0.1), at=(0, 0.0, -0.05), m=k.mat("#141416", "satin"), bevel=0.01, setting=True)
    wy = 1.15
    k.box((6, 0.1, 4), at=(0, wy + 0.05, 1.9), m=k.mat("#e8c96a", "matte"), bevel=0, setting=True)
    tile = k.mat("#ffd23a", "gloss")
    s = 0.3
    for ix in range(-8, 9):
        for iz in range(9):
            k.box((s - 0.02, 0.03, s - 0.02), at=(ix * s, wy - 0.01, 0.16 + iz * s), m=tile, bevel=0.01,
                  setting=True)
