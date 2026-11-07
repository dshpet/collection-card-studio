# Toy spaceship: a rounded grey body lies along the x axis with its nose toward +x. Its underside is cut
# flat so it rests on the floor. A clear yellow cockpit dome sits sunk into the top, a little ahead of the
# middle, and a trim ring hugging the hull runs around its base. Two swept wings go into the sides of the
# body, low down, taper back toward the tips and lift slightly so the far one shows past the hull. Two
# engine pods attach to the flat tail end, each ending in a dark nozzle. The floor is plain green, a shade
# lighter than the backdrop.
import math

SCENE = {"category": "2", "backdrop": "#5cc23f", "azimuth": 30, "elevation": 20, "lens": 60, "light": "left"}


def build(k):
    grey = k.mat("#9ea5af", "satin")
    trim = k.mat("#7d838c", "satin")
    dark = k.mat("#4a4f57", "satin")
    dome = k.mat("#ffd23a", "glass")

    # Body: a lathe along its local z, turned so local z points to world +x and local x points down.
    axis_z = 0.12
    x0 = -0.5
    profile = [(0.0, 0.0), (0.15, 0.0), (0.17, 0.04), (0.19, 0.12), (0.2, 0.25), (0.2, 0.42), (0.19, 0.56),
               (0.17, 0.68), (0.14, 0.79), (0.1, 0.88), (0.06, 0.95), (0.025, 0.99), (0.0, 1.0)]
    body = k.lathe(profile, at=(x0, 0, axis_z), rot=(0, 90, 0), m=grey)
    # Flatten the underside (local +x is world down) so it sits on the floor at z = 0.
    k.warp(body, lambda p: (min(p[0], axis_z), p[1], p[2]))

    def radius(x):
        lz = x - x0
        for (r1, z1), (r2, z2) in zip(profile, profile[1:]):
            if z1 <= lz <= z2:
                return r1 + (r2 - r1) * (lz - z1) / max(z2 - z1, 1e-6)
        return 0.0

    def top(x, y):
        r = radius(x)
        return axis_z + math.sqrt(max(r * r - y * y, 0.0))

    # Cockpit dome: its lower half buried in the body, its upper half standing clear of the top.
    k.sphere(0.13, at=(0.1, 0, 0.22), scale=(1.45, 1.0, 1.15), m=dome)
    # Trim ring following the hull surface around the dome's base.
    pts = []
    for i in range(49):
        a = 2 * math.pi * i / 48
        x, y = 0.1 + 0.17 * math.cos(a), 0.115 * math.sin(a)
        pts.append((x, y, top(x, y) + 0.004))
    k.tube(pts, 0.013, trim, curved=True)

    # Swept wings, their roots buried in the sides of the body, with a small pod on each tip.
    span = 0.5
    for s in (-1, 1):
        wing = k.box((0.34, span, 0.04), at=(-0.12, s * 0.37, 0.12), m=grey, bevel=0.012)

        def sweep(p, s=s):
            t = (s * p[1] + span / 2) / span  # 0 at the root, 1 at the tip
            return (p[0] * (1 - 0.45 * t) - 0.22 * t, p[1], p[2] + 0.07 * t)

        k.warp(wing, sweep)
        k.cyl(0.035, 0.16, at=(-0.29, s * 0.62, 0.19), rot=(0, 90, 0), m=trim)

    # Twin engine pods joined to the tail end, with dark nozzles.
    for y in (-0.085, 0.085):
        k.cyl(0.075, 0.2, at=(-0.55, y, 0.15), rot=(0, 90, 0), m=trim)
        k.cone(0.06, 0.08, 0.06, at=(-0.68, y, 0.15), rot=(0, -90, 0), m=dark)
        k.cyl(0.05, 0.01, at=(-0.712, y, 0.15), rot=(0, 90, 0), m=k.mat("#2a2d33", "matte"))

    # Plain floor, a shade lighter than the backdrop, large enough that its edge never shows.
    k.box((40, 40, 0.1), at=(0, 0, -0.05), m=k.mat("#7fd463", "matte"), bevel=0, setting=True)
