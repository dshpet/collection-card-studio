# Vintage table radio: one wooden cabinet whose arched top runs straight down into vertical sides, set on a
# slightly wider plinth. The front carries a round cream speaker grille behind a wooden bezel and slats, a lit dial
# window in a gold frame below it, and two gold knobs either side of the dial. It stands on a dark wooden desk made
# of planks whose back edge shows behind the radio, against a plain purple backdrop.
SCENE = {"category": "3", "backdrop": "#6b3fb8", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#b5672e", "matte")
    dark = k.mat("#7a3e1a", "matte")
    cream = k.mat("#f1e3c2", "matte")
    gold = k.mat("#e0b043", "metal")
    glow = k.mat("#ffd27a", "glow")

    w, d = 1.0, 0.4
    front = -d / 2

    # Plinth, then a single cabinet solid: a cylinder lying along y whose lower half-rim is pulled straight
    # down to the plinth top (straight sides, flat bottom), and whose upper half is flattened into the arch.
    k.box((w + 0.06, d + 0.04, 0.06), at=(0, 0, 0.03), m=dark, bevel=0.015)
    cz = 0.45
    body = k.cyl(w / 2, d, at=(0, 0, cz), rot=(90, 0, 0), m=wood, bevel=0.02)
    k.warp(body, lambda p: (p[0], p[1] * 0.5 if p[1] > 0 else -(cz - 0.06), p[2]))

    # Round speaker grille: cream cloth disc, wooden bezel ring, raised wooden slats.
    gz, gr = 0.43, 0.18
    k.cyl(gr, 0.02, at=(0, front - 0.002, gz), rot=(90, 0, 0), m=cream)
    k.torus(gr, 0.022, at=(0, front - 0.01, gz), rot=(90, 0, 0), m=dark)
    for x in (-0.105, -0.035, 0.035, 0.105):
        h = 2 * (gr * gr - x * x) ** 0.5
        k.box((0.026, 0.02, h), at=(x, front - 0.012, gz), m=dark, bevel=0.006)

    # Lit dial window in a gold frame, with a needle.
    dz = 0.165
    k.box((0.34, 0.02, 0.11), at=(0, front - 0.004, dz), m=gold, bevel=0.012)
    k.box((0.29, 0.02, 0.07), at=(0, front - 0.012, dz), m=glow, bevel=0.008)
    k.box((0.008, 0.012, 0.066), at=(0.03, front - 0.022, dz), m=dark, bevel=0.002)

    # Two gold knobs on short shafts.
    for x in (-0.33, 0.33):
        k.cyl(0.02, 0.03, at=(x, front - 0.015, dz), rot=(90, 0, 0), m=gold)
        k.cyl(0.058, 0.045, at=(x, front - 0.05, dz), rot=(90, 0, 0), m=gold, bevel=0.01)
        k.cyl(0.035, 0.012, at=(x, front - 0.078, dz), rot=(90, 0, 0), m=gold, bevel=0.004)

    # Dark wooden desk of planks running left-right; its back edge shows behind the radio.
    desk = ["#4a2a17", "#53301b", "#472815"]
    for i in range(6):
        y = 0.55 - i * 0.5
        k.box((7, 0.49, 0.1), at=(0, y - 0.25, -0.05), m=k.mat(desk[i % 3], "matte"), bevel=0.01, setting=True)
