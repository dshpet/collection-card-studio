# Boxy friendly robot standing on a metal floor: two legs with flat feet carry a box torso with a red chest
# button; a short neck holds a square head with two round eyes and two antennae with ball tips. Each arm hangs
# from a shoulder ball on the torso side, bends at an elbow ball and ends in a round hand. The floor is a grid of
# steel plates with thin gaps between them, running off the card.
SCENE = {"category": "3", "backdrop": "#ffc21a", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    gray = k.mat("#c3c8cf", "satin")
    white = k.mat("#f4f5f7", "satin")
    dark = k.mat("#5d646e", "satin")
    eye = k.mat("#1f2530", "gloss")
    red = k.mat("#e8262b", "gloss")

    # Legs and feet
    for s in (-1, 1):
        x = s * 0.11
        k.box((0.2, 0.26, 0.07), at=(x, -0.02, 0.035), m=gray, bevel=0.025)
        k.box((0.13, 0.14, 0.26), at=(x, 0, 0.19), m=gray, bevel=0.02)
        k.cyl(0.05, 0.15, at=(x, 0, 0.32), rot=(0, 90, 0), m=dark, bevel=0.01)

    # Torso with chest panel and button
    k.box((0.44, 0.3, 0.36), at=(0, 0, 0.52), m=white, bevel=0.04)
    k.box((0.24, 0.02, 0.16), at=(0, -0.152, 0.52), m=gray, bevel=0.01)
    k.cyl(0.035, 0.03, at=(0, -0.165, 0.54), rot=(90, 0, 0), m=red, bevel=0.008)

    # Neck and head
    k.cyl(0.06, 0.08, at=(0, 0, 0.72), m=dark, bevel=0.01)
    k.box((0.38, 0.32, 0.27), at=(0, 0, 0.885), m=white, bevel=0.045)
    for s in (-1, 1):
        k.cyl(0.055, 0.02, at=(s * 0.085, -0.16, 0.9), rot=(90, 0, 0), m=gray, bevel=0.006)
        k.cyl(0.038, 0.02, at=(s * 0.085, -0.172, 0.9), rot=(90, 0, 0), m=eye, bevel=0.006)
        # ear bolts on the head sides
        k.cyl(0.045, 0.04, at=(s * 0.2, 0, 0.9), rot=(0, 90, 0), m=gray, bevel=0.008)
        # antennae rise from the head top, tipped with balls
        k.cyl(0.016, 0.13, at=(s * 0.1, 0, 1.075), rot=(0, s * 12, 0), m=dark, bevel=0.004)
        k.sphere(0.035, at=(s * 0.114, 0, 1.14), m=red if s > 0 else gray)

    # Arms: shoulder ball, upper arm, elbow, forearm, hand
    for s in (-1, 1):
        sh = (s * 0.25, 0, 0.64)
        el = (s * 0.29, -0.02, 0.48)
        wr = (s * 0.29, -0.07, 0.34)
        k.sphere(0.055, at=sh, m=gray)
        k.tube([sh, el], 0.032, gray)
        k.sphere(0.042, at=el, m=dark)
        k.tube([el, wr], 0.032, gray)
        k.sphere(0.055, at=(wr[0], wr[1] - 0.005, wr[2] - 0.03), scale=(0.9, 1, 1.1), m=white)

    # Metal floor: steel plates with thin seams over a dark base, top at z = 0
    steel = k.mat("#9ea6b0", "metal")
    for i in range(-3, 4):
        for j in range(-3, 5):
            k.box((0.585, 0.585, 0.04), at=(i * 0.6 + 0.3, j * 0.6, -0.02), m=steel, bevel=0.01, setting=True)
    k.box((5, 6, 0.02), at=(0, 0.3, -0.05), m=k.mat("#4d545d", "matte"), bevel=0, setting=True)
