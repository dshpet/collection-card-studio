# Moon rover: a flat white box body rides on two side rocker beams, one per side, each pinned to the body
# by a pivot. Three struts drop from each beam to an axle stub, and each stub carries a black wheel, so all
# six wheels stand on the dust. A short mast rises from the top deck to a tilted round dish, and the camera
# box is bolted to the front face (+x) with a blue lens. The rover stands on a slab of grey moon dust whose
# front edge shows under it, like the desk and table edges on the real cards.
SCENE = {"category": "3", "backdrop": "#f28a1e", "azimuth": 32, "elevation": 13, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f4f2", "satin")
    grey = k.mat("#9ea3aa", "satin")
    steel = k.mat("#b8bcc2", "metal")
    tyre = k.mat("#222326", "matte")
    lens = k.mat("#2f8fff", "glass")

    # Body: flat white box with a grey deck plate on top.
    k.box((0.9, 0.5, 0.2), at=(0, 0, 0.32), m=white, bevel=0.03)
    k.box((0.7, 0.38, 0.025), at=(-0.04, 0, 0.432), m=grey, bevel=0.008)

    # Suspension and wheels, three per side.
    wr, ww = 0.11, 0.09
    xs = (-0.34, 0.0, 0.34)
    for side in (-1, 1):
        ys = side * 0.3
        k.cyl(0.035, 0.07, at=(0, side * 0.27, 0.27), rot=(90, 0, 0), m=steel)       # pivot into body
        k.box((0.74, 0.035, 0.035), at=(0, ys, 0.27), m=grey, bevel=0.008)          # rocker beam
        for x in xs:
            k.box((0.035, 0.035, 0.17), at=(x, ys, 0.19), m=grey, bevel=0.008)      # strut down to hub
            k.cyl(0.022, 0.09, at=(x, side * 0.335, wr), rot=(90, 0, 0), m=steel)    # axle stub
            k.cyl(wr, ww, at=(x, side * 0.375, wr), rot=(90, 0, 0), m=tyre, bevel=0.02)
            k.cyl(0.05, ww + 0.012, at=(x, side * 0.375, wr), rot=(90, 0, 0), m=grey, bevel=0.008)

    # Front camera box (+x face) with a blue lens.
    k.box((0.1, 0.18, 0.11), at=(0.495, 0, 0.35), m=white, bevel=0.015)
    k.cyl(0.042, 0.03, at=(0.555, 0, 0.35), rot=(0, 90, 0), m=grey, bevel=0.004)
    k.cyl(0.032, 0.012, at=(0.572, 0, 0.35), rot=(0, 90, 0), m=lens, bevel=0.003)

    # Short mast with a round dish.
    mx, my = -0.2, 0.06
    k.cyl(0.05, 0.03, at=(mx, my, 0.459), m=grey, bevel=0.006)
    k.cyl(0.022, 0.16, at=(mx, my, 0.55), m=steel)
    k.sphere(0.035, at=(mx, my, 0.63), m=grey)
    profile = [(0.0, 0.0), (0.04, 0.002), (0.08, 0.009), (0.12, 0.022), (0.15, 0.036), (0.155, 0.046),
               (0.12, 0.032), (0.08, 0.019), (0.04, 0.012), (0.0, 0.01)]
    k.lathe(profile, at=(mx, my, 0.65), rot=(25, -25, 0), m=white)
    k.cyl(0.008, 0.08, at=(mx + 0.015, my - 0.015, 0.69), rot=(25, -25, 0), m=steel)
    k.sphere(0.016, at=(mx + 0.03, my - 0.03, 0.725), m=grey)

    # Grey moon dust slab, front edge visible under the rover.
    k.box((6, 3, 0.3), at=(0, 0.75, -0.15), m=k.mat("#8e8f94", "matte"), bevel=0.03, setting=True)
