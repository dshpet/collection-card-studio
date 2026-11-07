# Jetpack: two tall domed tanks stand side by side on the front of a flat back plate, each held to it by two
# clamp bands. A valve cap sits on top of each tank and a nozzle bell hangs from each tank's bottom, ending in an
# orange tip. Two shoulder straps start at the top of the plate's back face, arc over and down behind it, and
# end at its bottom corners. Floating, tilted a little so the front and the right side with the straps show.
SCENE = {"category": "1", "backdrop": "#3fb34a", "azimuth": 32, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    grey = k.mat("#7d838c", "satin")
    dark = k.mat("#4a4f57", "satin")
    strap = k.mat("#3d4148", "matte")
    orange = k.mat("#ff8a1f", "satin")

    # back plate, its front face at y = 0.095
    k.box((0.58, 0.05, 0.78), at=(0, 0.12, 0.52), m=grey, bevel=0.025)

    tank = [(0, 0.13), (0.05, 0.133), (0.09, 0.145), (0.115, 0.165), (0.128, 0.19), (0.13, 0.22),
            (0.13, 0.82), (0.128, 0.85), (0.12, 0.88), (0.105, 0.91), (0.08, 0.935), (0.045, 0.948), (0, 0.952)]
    bell = [(0, 0.15), (0.045, 0.15), (0.042, 0.12), (0.048, 0.09), (0.062, 0.06), (0.075, 0.04), (0, 0.04)]
    for x in (-0.145, 0.145):
        k.lathe(tank, at=(x, -0.025, 0), m=silver)
        for z in (0.34, 0.72):
            k.torus(0.132, 0.016, at=(x, -0.025, z), rot=(0, 0, 0), m=dark)
        k.cyl(0.035, 0.05, at=(x, -0.025, 0.965), rot=(0, 0, 0), m=dark, bevel=0.008)
        k.cyl(0.05, 0.02, at=(x, -0.025, 0.995), rot=(0, 0, 0), m=dark, bevel=0.006)
        k.lathe(bell, at=(x, -0.025, 0), m=grey)
        k.cone(0.075, 0.082, 0.05, at=(x, -0.025, 0.017), rot=(0, 0, 0), m=orange)

    # clamp blocks joining the bands to the plate between the tanks
    for z in (0.34, 0.72):
        k.box((0.08, 0.1, 0.05), at=(0, 0.05, z), m=dark, bevel=0.01)

    # shoulder straps on the back side of the plate
    for x in (-0.16, 0.16):
        k.tube([(x, 0.14, 0.86), (x, 0.19, 0.96), (x, 0.29, 0.97), (x, 0.36, 0.86), (x, 0.37, 0.62),
                (x, 0.33, 0.38), (x, 0.24, 0.22), (x, 0.15, 0.18)], 0.026, strap, curved=True)
        k.box((0.08, 0.02, 0.06), at=(x, 0.15, 0.86), m=dark, bevel=0.006)
        k.box((0.08, 0.02, 0.06), at=(x, 0.15, 0.19), m=dark, bevel=0.006)

    k.turn(-4, 6, 0)
