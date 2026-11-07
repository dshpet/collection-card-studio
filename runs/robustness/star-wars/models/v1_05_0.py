# Toy spaceship: a rounded grey body lies along the x axis with its nose toward +x. Its underside is cut
# flat so it rests on the floor. A clear yellow cockpit dome sits sunk into the top, a little ahead of the
# middle, with a trim ring at its base. Two swept wings go into the sides of the body, low down, and taper
# back toward the tips. Two engine pods attach to the flat tail end, each ending in a dark nozzle. The floor
# is plain green, a shade lighter than the backdrop.
SCENE = {"category": "2", "backdrop": "#5cc23f", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    grey = k.mat("#cfd3d9", "satin")
    trim = k.mat("#8d939c", "satin")
    dark = k.mat("#4a4f57", "satin")
    dome = k.mat("#ffd23a", "glass")

    # Body: a lathe along its local z, turned so local z points to world +x and local x points down.
    axis_z = 0.12
    profile = [(0.0, 0.0), (0.15, 0.0), (0.17, 0.04), (0.19, 0.12), (0.2, 0.25), (0.2, 0.42), (0.19, 0.56),
               (0.17, 0.68), (0.14, 0.79), (0.1, 0.88), (0.06, 0.95), (0.025, 0.99), (0.0, 1.0)]
    body = k.lathe(profile, at=(-0.5, 0, axis_z), rot=(0, 90, 0), m=grey)
    # Flatten the underside (local +x is world down) so it sits on the floor at z = 0.
    k.warp(body, lambda p: (min(p[0], axis_z), p[1], p[2]))

    # Cockpit dome sunk into the top of the body, with an oval trim ring at its base.
    k.sphere(0.13, at=(0.1, 0, 0.27), scale=(1.45, 1.0, 0.9), m=dome)
    ring = k.torus(0.135, 0.014, at=(0.1, 0, 0.29), m=trim)
    k.warp(ring, lambda p: (p[0] * 1.45, p[1], p[2]))

    # Swept wings, their roots buried in the sides of the body, with a small pod on each tip.
    span = 0.42
    for s in (-1, 1):
        wing = k.box((0.34, span, 0.04), at=(-0.12, s * 0.33, 0.12), m=grey, bevel=0.012)

        def sweep(p, s=s):
            t = (s * p[1] + span / 2) / span  # 0 at the root, 1 at the tip
            return (p[0] * (1 - 0.45 * t) - 0.2 * t, p[1], p[2] + 0.03 * t)

        k.warp(wing, sweep)
        k.cyl(0.035, 0.16, at=(-0.27, s * 0.54, 0.15), rot=(0, 90, 0), m=trim)

    # Twin engine pods joined to the tail end, with dark nozzles.
    for y in (-0.085, 0.085):
        k.cyl(0.075, 0.2, at=(-0.55, y, 0.15), rot=(0, 90, 0), m=trim)
        k.cone(0.06, 0.08, 0.06, at=(-0.68, y, 0.15), rot=(0, -90, 0), m=dark)
        k.cyl(0.05, 0.01, at=(-0.712, y, 0.15), rot=(0, 90, 0), m=k.mat("#2a2d33", "matte"))

    # Plain floor, a shade lighter than the backdrop.
    k.box((6, 6, 0.1), at=(0, 0, -0.05), m=k.mat("#7fd463", "matte"), bevel=0, setting=True)
