# Wicker picnic basket on grass: a slightly tapered wicker body with raised woven bands at the foot, middle and
# rim; a closed lid that turns on two hinge barrels at the back; an arched wicker handle fixed to the lid top by
# two leather brackets. One green leather strap runs from the back of the lid, across the top and down the front,
# through a metal buckle, and its lower end passes through a leather loop on the middle band of the body.
SCENE = {"category": "3", "backdrop": "#5ec3f2", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    wicker = k.mat("#d6a560", "matte")
    band = k.mat("#c08a45", "matte")
    leather = k.mat("#1f5b35", "satin")
    metal = k.mat("#c9c3b5", "metal")

    # Body, tapered toward the bottom.
    body = k.box((0.72, 0.46, 0.38), at=(0, 0, 0.19), m=wicker, bevel=0.03)
    k.warp(body, lambda p: (p[0] * (0.92 + 0.08 * (p[2] + 0.19) / 0.38),
                            p[1] * (0.92 + 0.08 * (p[2] + 0.19) / 0.38), p[2]))
    k.box((0.68, 0.44, 0.04), at=(0, 0, 0.02), m=band, bevel=0.015)
    k.box((0.705, 0.455, 0.03), at=(0, 0, 0.2), m=band, bevel=0.012)
    k.box((0.74, 0.48, 0.04), at=(0, 0, 0.36), m=band, bevel=0.015)

    # Lid, closed, with a low raised top panel.
    k.box((0.75, 0.49, 0.07), at=(0, 0, 0.415), m=wicker, bevel=0.025)
    k.box((0.68, 0.42, 0.03), at=(0, 0, 0.46), m=wicker, bevel=0.012)

    # Hinges at the back, between rim and lid.
    for x in (-0.2, 0.2):
        k.cyl(0.018, 0.09, at=(x, 0.248, 0.385), rot=(0, 90, 0), m=metal)
        k.box((0.06, 0.006, 0.06), at=(x, 0.246, 0.385), m=metal, bevel=0.002)

    # Arched handle on two leather brackets.
    for x in (-0.24, 0.24):
        k.box((0.07, 0.07, 0.03), at=(x, 0, 0.488), m=leather, bevel=0.008)
    k.tube([(-0.24, 0, 0.49), (-0.225, 0, 0.6), (-0.15, 0, 0.69), (0, 0, 0.725),
            (0.15, 0, 0.69), (0.225, 0, 0.6), (0.24, 0, 0.49)], 0.024, wicker, curved=True)

    # Strap: from the back of the lid, across the top, down the front, through the buckle, into a keeper loop.
    k.box((0.07, 0.012, 0.1), at=(0, 0.252, 0.437), m=leather, bevel=0.004)
    k.box((0.07, 0.51, 0.012), at=(0, 0, 0.481), m=leather, bevel=0.004)
    k.box((0.07, 0.012, 0.19), at=(0, -0.252, 0.385), m=leather, bevel=0.004)
    k.box((0.07, 0.012, 0.2), at=(0, -0.24, 0.25), rot=(-4, 0, 0), m=leather, bevel=0.004)
    # Buckle frame and prong.
    for x in (-0.05, 0.05):
        k.box((0.016, 0.016, 0.09), at=(x, -0.262, 0.31), m=metal, bevel=0.004)
    for z in (0.272, 0.348):
        k.box((0.116, 0.016, 0.016), at=(0, -0.262, z), m=metal, bevel=0.004)
    k.cyl(0.006, 0.04, at=(0, -0.264, 0.31), rot=(0, 0, 0), m=metal)
    # Leather keeper loop on the middle band, holding the strap's lower end.
    k.box((0.1, 0.022, 0.045), at=(0, -0.244, 0.2), m=leather, bevel=0.006)

    # Grass ground.
    k.box((6, 5, 0.1), at=(0, 1.2, -0.05), m=k.mat("#5cb83a", "matte"), bevel=0, setting=True)
