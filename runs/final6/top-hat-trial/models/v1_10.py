# Upright piano: a closed case stands against the wall on two toe-block legs at the front and low feet at the back.
# The key bed rests on the legs between two cheek blocks; white and black keys lie on it, and the key lid is folded
# up, leaning against the upper front. Two brass pedals stick out of the lower front panel. Polished plank floor,
# cream wall with a baseboard behind.
SCENE = {"category": "4", "backdrop": "#4fd3e8", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#7a2e1c", "gloss")
    dark = k.mat("#5c2014", "gloss")
    ivory = k.mat("#f6efdc", "satin")
    ebony = k.mat("#1a1414", "gloss")
    brass = k.mat("#d9a93a", "metal")

    # Case: back body, top lid, front panels raised from the body.
    k.box((1.0, 0.24, 0.9), at=(0, 0.12, 0.49), m=wood, bevel=0.01)
    k.box((1.04, 0.28, 0.035), at=(0, 0.115, 0.955), m=dark, bevel=0.01)
    k.box((0.86, 0.02, 0.26), at=(0, -0.005, 0.76), m=dark, bevel=0.008)   # upper panel
    k.box((0.84, 0.02, 0.3), at=(0, -0.005, 0.22), m=dark, bevel=0.008)    # lower panel
    k.box((0.96, 0.03, 0.03), at=(0, -0.01, 0.055), m=dark, bevel=0.006)   # bottom rail

    # Back feet under the case.
    for x in (-0.46, 0.46):
        k.box((0.06, 0.06, 0.04), at=(x, 0.19, 0.02), m=dark, bevel=0.006)

    # Front legs: toe block on the floor, column up to the cheek block.
    for x in (-0.47, 0.47):
        k.box((0.06, 0.26, 0.05), at=(x, -0.09, 0.025), m=dark, bevel=0.01)
        k.lathe([(0.03, 0), (0.032, 0.02), (0.024, 0.08), (0.026, 0.2), (0.022, 0.33), (0.03, 0.37), (0.03, 0.39)],
                at=(x, -0.16, 0.05), m=wood)
        k.box((0.06, 0.22, 0.13), at=(x, -0.09, 0.505), m=wood, bevel=0.01)   # cheek block

    # Key bed and key slip.
    k.box((0.88, 0.22, 0.04), at=(0, -0.09, 0.46), m=wood, bevel=0.005)
    k.box((0.88, 0.02, 0.05), at=(0, -0.2, 0.46), m=dark, bevel=0.005)

    # Keys: 36 white, black keys in groups of two and three.
    n, w = 36, 0.88 / 36
    x0 = -0.44 + w / 2
    for i in range(n):
        k.box((w * 0.9, 0.15, 0.022), at=(x0 + i * w, -0.115, 0.491), m=ivory, bevel=0.002)
    for i in range(n - 1):
        if i % 7 in (0, 1, 3, 4, 5):
            k.box((w * 0.55, 0.09, 0.024), at=(x0 + (i + 0.5) * w, -0.075, 0.512), m=ebony, bevel=0.002)
    k.box((0.88, 0.05, 0.05), at=(0, -0.015, 0.505), m=dark, bevel=0.005)   # key rail behind the keys

    # Key lid folded up, leaning back on the upper front.
    k.box((0.88, 0.02, 0.12), at=(0, -0.03, 0.6), rot=(-12, 0, 0), m=wood, bevel=0.006)

    # Pedals out of the lower front.
    for x in (-0.06, 0.06):
        k.box((0.03, 0.11, 0.014), at=(x, -0.06, 0.09), rot=(6, 0, 0), m=brass, bevel=0.005)
        k.box((0.05, 0.012, 0.04), at=(x, -0.012, 0.09), m=brass, bevel=0.004)

    # Setting: polished plank floor, cream wall with baseboard.
    for i in range(-12, 13):
        k.box((0.24, 6, 0.04), at=(i * 0.25, 0, -0.02), m=k.mat("#b8743c" if i % 2 else "#a9672f", "gloss"),
              bevel=0.006, setting=True)
    k.box((6, 0.05, 4), at=(0, 0.275, 2), m=k.mat("#f3e6c4", "matte"), bevel=0, setting=True)
    k.box((6, 0.03, 0.1), at=(0, 0.24, 0.05), m=k.mat("#fbf4e2", "satin"), bevel=0.005, setting=True)
