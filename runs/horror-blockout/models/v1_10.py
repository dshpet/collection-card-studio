# Straw broom: a long round wooden stick runs down into a straw bundle that flares in nearly straight lines from a
# narrow tied neck to a wide, flat, ragged foot of straw tips. The stick ends inside the bundle; two red cord wraps
# bind the neck, tied off in a small knot on the front. A rounded cap closes the top of the stick. It floats tilted
# on the card's diagonal.
import math

SCENE = {"category": "1", "backdrop": "#45b6f0", "azimuth": 15, "elevation": 10, "lens": 70, "light": "left"}

FLAT = 0.72  # the bundle is a little flatter front-to-back than side-to-side


def build(k):
    wood = k.mat("#8a5428", "matte")
    straw = k.mat("#e8b53a", "matte")
    cord = k.mat("#d8262b", "matte")

    # Stick: starts inside the bundle and runs up to a rounded end cap.
    k.cyl(0.032, 1.12, at=(0, 0, 0.88), m=wood, bevel=0.01)
    k.sphere(0.04, at=(0, 0, 1.44), scale=(1, 1, 0.7), m=wood)

    # Straw bundle: narrow neck around the stick, flaring in near-straight flanks to a wide, flat foot.
    profile = [(0.0, 0.0), (0.12, 0.0), (0.2, 0.002), (0.218, 0.012), (0.225, 0.03), (0.212, 0.08),
               (0.188, 0.14), (0.16, 0.2), (0.13, 0.26), (0.102, 0.31), (0.08, 0.35), (0.068, 0.38),
               (0.062, 0.42), (0.058, 0.46), (0.046, 0.48), (0.0, 0.49)]
    bundle = k.lathe(profile, at=(0, 0, 0), m=straw)

    def shape(p):
        x, y, z = p
        if z < 0.04 and math.hypot(x, y) > 0.1:  # uneven straw tips along the foot's edge
            a = math.atan2(y, x)
            z -= 0.03 * abs(math.sin(7 * a)) * abs(math.sin(3 * a + 1)) * (1 - z / 0.04)
        return (x, y * FLAT, z)

    k.warp(bundle, shape)

    # Cord: two wraps hugging the flattened neck, and a knot on the front.
    for z, big in ((0.375, 0.07), (0.425, 0.063)):
        wrap = k.torus(big, 0.014, at=(0, 0, z), rot=(0, 0, 0), m=cord)
        k.warp(wrap, lambda p: (p[0], p[1] * FLAT, p[2]))
    k.sphere(0.024, at=(0, -0.06, 0.40), scale=(1.2, 0.8, 1), m=cord)

    k.turn(8, 38, 0)
