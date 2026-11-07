# Upright piano against a wallpapered wall on a polished wooden floor. The closed lower case stands on four
# short bun feet; the key bed juts forward between two cheek blocks and carries a row of white keys with black
# keys in 2-3 groups. The key lid (fallboard) is swung up on its hinge rod and leans back against the upper case.
# Two brass pedals come out of a block at the foot of the kick board. The back of the case touches the wall.

SCENE = {"category": "4", "backdrop": "#5fd3ea", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#5a3220", "satin")
    dark = k.mat("#43241a", "satin")
    ivory = k.mat("#f4ecd6", "gloss")
    ebony = k.mat("#1d1715", "gloss")
    brass = k.mat("#d9a63a", "metal")

    W, back = 1.0, 0.20

    # short bun feet under the four corners
    for x in (-0.44, 0.44):
        for y in (-0.12, 0.16):
            k.cyl(0.035, 0.04, at=(x, y, 0.02), m=dark, bevel=0.008)

    # lower case: closed front with a recessed kick board
    k.box((W, 0.36, 0.38), at=(0, 0.02, 0.23), m=wood, bevel=0.01)
    k.box((0.82, 0.02, 0.28), at=(0, -0.165, 0.24), m=dark, bevel=0.006)

    # pedal block and two brass pedals
    k.box((0.16, 0.04, 0.035), at=(0, -0.17, 0.08), m=dark, bevel=0.006)
    for x in (-0.04, 0.04):
        k.box((0.03, 0.09, 0.016), at=(x, -0.225, 0.075), m=brass, bevel=0.006)

    # key bed, key slip and cheek blocks
    k.box((W, 0.20, 0.06), at=(0, -0.22, 0.43), m=wood, bevel=0.008)
    k.box((W, 0.02, 0.05), at=(0, -0.325, 0.425), m=dark, bevel=0.006)
    for x in (-0.475, 0.475):
        k.box((0.05, 0.22, 0.12), at=(x, -0.21, 0.52), m=wood, bevel=0.01)

    # keys: 28 white keys across the bed, black keys in groups of two and three
    n, span = 28, 0.88
    step = span / n
    x0 = -span / 2 + step / 2
    for i in range(n):
        k.box((step - 0.003, 0.15, 0.024), at=(x0 + i * step, -0.235, 0.472), m=ivory, bevel=0.003)
    for i in range(n - 1):
        if i % 7 in (0, 1, 3, 4, 5):
            k.box((step * 0.55, 0.09, 0.024), at=(x0 + (i + 0.5) * step, -0.205, 0.494), m=ebony, bevel=0.003)

    # upper case with raised front panels and an overhanging top lid
    k.box((W, 0.26, 0.42), at=(0, 0.07, 0.67), m=wood, bevel=0.01)
    for x in (-0.24, 0.24):
        k.box((0.38, 0.015, 0.16), at=(x, -0.065, 0.76), m=dark, bevel=0.01)
    k.box((W + 0.04, 0.30, 0.03), at=(0, 0.065, 0.895), m=dark, bevel=0.01)

    # raised key lid: hinge rod at the back of the keys, the board swung up leaning on the upper case
    k.cyl(0.01, 0.9, at=(0, -0.155, 0.49), rot=(0, 90, 0), m=brass)
    k.box((0.9, 0.02, 0.17), at=(0, -0.085, 0.575), rot=(-15, 0, 0), m=wood, bevel=0.006)

    # setting: polished wooden floor, cream wallpapered wall with a skirting board
    k.box((6, 6, 0.04), at=(0, 0, -0.02), m=k.mat("#b0703a", "gloss"), bevel=0, setting=True)
    k.box((6, 0.05, 4), at=(0, back + 0.025, 2), m=k.mat("#f1e3bf", "matte"), bevel=0, setting=True)
    k.box((6, 0.02, 0.08), at=(0, back - 0.01, 0.04), m=k.mat("#e8d3a8", "satin"), bevel=0.004, setting=True)
