# Handheld calculator, tilted: display, solar strip and keys all lie on one face, in one perspective.
SCENE = {"category": "1", "backdrop": "#f6b12a", "azimuth": 0, "elevation": 8, "light": "left"}


def build(k):
    body, keys, ops = k.mat("#1d2b6b", "gloss"), k.mat("#33478f", "satin"), k.mat("#7fe3f5", "satin")
    k.box((0.17, 0.026, 0.26), at=(0, 0, 0), m=body, bevel=0.014)
    face = -0.013
    k.box((0.132, 0.006, 0.05), at=(0, face, 0.078), m=k.mat("#c9cfc9", "satin"), bevel=0.004)
    k.box((0.05, 0.006, 0.014), at=(0.035, face, 0.114), m=k.mat("#c8282b", "gloss"), bevel=0.002)
    for row in range(4):
        z = 0.022 - row * 0.038
        for col in range(3):
            k.box((0.03, 0.012, 0.028), at=(-0.059 + col * 0.037, face - 0.004, z), m=keys, bevel=0.005)
        k.box((0.036, 0.012, 0.03), at=(0.056, face - 0.004, z), m=ops, bevel=0.006)
    k.turn(x=-18, y=-14, z=24)
