# Saloon: a two-story wooden building whose flat false front rises past the roof with a stepped crown. A sloped
# porch roof leans from the facade onto a header beam and four posts that stand on the plank porch deck. The
# swinging half doors hang on hinges inside a red door frame. A dusty street runs under it, and tall red mesas
# stand far back in the open sky on either side of the building.
import math

SCENE = {"category": "4", "backdrop": "#4fb8f2", "azimuth": 25, "elevation": 10, "lens": 55, "light": "left"}


def build(k):
    wall = k.mat("#a8683a", "matte")
    trim = k.mat("#7a4524", "matte")
    plank = k.mat("#c08048", "matte")
    roof = k.mat("#6b3c22", "matte")
    red = k.mat("#c4302b", "satin")
    dark = k.mat("#3a2416", "matte")
    glass = k.mat("#2c4a63", "gloss")
    iron = k.mat("#4a4f57", "metal")

    # Main body and its flat roof
    k.box((0.9, 0.7, 1.0), at=(0, 0.05, 0.5), m=wall, bevel=0.01)
    k.box((0.94, 0.74, 0.04), at=(0, 0.05, 1.02), m=roof, bevel=0.008)

    # False front with corner boards, cornice and stepped crown
    k.box((1.0, 0.05, 1.3), at=(0, -0.325, 0.65), m=wall, bevel=0.008)
    for x in (-0.5, 0.5):
        k.box((0.05, 0.07, 1.3), at=(x, -0.325, 0.65), m=trim, bevel=0.006)
    k.box((1.08, 0.09, 0.06), at=(0, -0.325, 1.3), m=trim, bevel=0.008)
    k.box((0.5, 0.05, 0.12), at=(0, -0.325, 1.39), m=wall, bevel=0.006)
    k.box((0.56, 0.09, 0.04), at=(0, -0.325, 1.47), m=trim, bevel=0.006)
    k.box((1.04, 0.07, 0.04), at=(0, -0.36, 0.7), m=trim, bevel=0.006)

    # Door opening, red frame and swinging half doors on hinges
    k.box((0.26, 0.02, 0.46), at=(0, -0.355, 0.30), m=dark, bevel=0.002)
    for x in (-0.15, 0.15):
        k.box((0.04, 0.04, 0.5), at=(x, -0.36, 0.32), m=red, bevel=0.005)
    k.box((0.34, 0.04, 0.04), at=(0, -0.36, 0.555), m=red, bevel=0.005)
    a = math.radians(20)
    for side in (-1, 1):
        hx, hy = side * 0.13, -0.37
        cx, cy = hx - side * 0.0625 * math.cos(a), hy - 0.0625 * math.sin(a)
        k.box((0.125, 0.025, 0.24), at=(cx, cy, 0.30), rot=(0, 0, side * 20), m=plank, bevel=0.005)
        for z in (0.22, 0.38):
            k.cyl(0.015, 0.05, at=(hx, hy, z), m=iron)

    # Windows: two below, three above, two on the right side
    def window(x, z, w, h):
        k.box((w, 0.02, h), at=(x, -0.36, z), m=glass, bevel=0.002)
        k.box((w + 0.06, 0.04, 0.035), at=(x, -0.365, z + h / 2 + 0.0175), m=trim, bevel=0.004)
        k.box((w + 0.08, 0.06, 0.035), at=(x, -0.37, z - h / 2 - 0.0175), m=trim, bevel=0.004)
        for s in (-1, 1):
            k.box((0.035, 0.04, h), at=(x + s * (w / 2 + 0.0175), -0.365, z), m=trim, bevel=0.004)

    for x in (-0.33, 0.33):
        window(x, 0.32, 0.17, 0.26)
    for x in (-0.3, 0.0, 0.3):
        window(x, 0.93, 0.15, 0.24)
    for z in (0.32, 0.85):
        k.box((0.02, 0.16, 0.24), at=(0.455, 0.1, z), m=glass, bevel=0.002)
        k.box((0.03, 0.2, 0.035), at=(0.46, 0.1, z - 0.137), m=trim, bevel=0.004)

    # Porch deck, front step, posts, header beam and sloped porch roof
    k.box((1.1, 0.34, 0.07), at=(0, -0.52, 0.035), m=plank, bevel=0.006)
    k.box((0.42, 0.12, 0.035), at=(0, -0.75, 0.0175), m=plank, bevel=0.005)
    for x in (-0.52, -0.2, 0.2, 0.52):
        k.box((0.05, 0.05, 0.48), at=(x, -0.68, 0.31), m=trim, bevel=0.006)
    k.box((1.1, 0.05, 0.05), at=(0, -0.68, 0.575), m=trim, bevel=0.006)
    k.box((1.14, 0.42, 0.03), at=(0, -0.54, 0.63), rot=(9, 0, 0), m=roof, bevel=0.006)

    # Setting: dusty street and distant red mesas, placed beside the camera's line of sight so they show
    # in the sky left and right of the building, and taller than the camera so they rise above the horizon.
    k.floor("#e3b47a", "matte", size=60)
    az = math.radians(SCENE["azimuth"])
    fwd = (-math.sin(az), math.cos(az))
    right = (math.cos(az), math.sin(az))

    def mesa(depth, lateral, r1, r2, h, hex_):
        x = fwd[0] * depth + right[0] * lateral
        y = fwd[1] * depth + right[1] * lateral
        k.cone(r1, r2, h, at=(x, y, h / 2), rot=(0, 0, 0), m=k.mat(hex_, "matte"), setting=True)

    mesa(14, -4.0, 1.7, 1.25, 2.4, "#c4583a")
    mesa(14, 4.3, 1.5, 1.1, 2.1, "#c4583a")
    mesa(18, -5.6, 1.4, 1.0, 1.7, "#d9724c")