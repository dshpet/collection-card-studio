# Coach-built pram: a deep oval navy tub sits on mounting blocks on two side rails; each rail curves down at both
# ends onto an axle, and each axle carries two large spoked silver wheels (bigger at the handle end). The cream
# folding hood is a half dome over the head end of the tub, its bows pivoting on a bolt each side at the rim.
# The long push handle rises from the rear of the rails behind the hood to a crossbar grip. It stands empty on
# a cobblestone street; the camera sees the long side and the open foot end.
import math

SCENE = {"category": "3", "backdrop": "#f39a3a", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    navy = k.mat("#1f2f6b", "satin")
    cream = k.mat("#f3e6c4", "matte")
    bow_m = k.mat("#e3d3ad", "matte")
    silver = k.mat("#c9ced6", "metal")
    tyre = k.mat("#34373d", "satin")
    grip = k.mat("#2a2420", "satin")

    # Body: an open oval tub with a rounded bottom, and a rolled rim.
    zb, ztop = 0.40, 0.68
    profile = [(0.0, 0.0), (0.07, 0.001), (0.12, 0.005), (0.15, 0.014), (0.17, 0.03), (0.183, 0.05),
               (0.192, 0.08), (0.198, 0.12), (0.201, 0.17), (0.203, 0.22), (0.205, 0.28)]
    tub = k.lathe(profile, at=(0, 0, zb), m=navy)
    k.warp(tub, lambda p: (p[0] * 2.0, p[1], p[2]))
    rim = [(0.41 * math.cos(2 * math.pi * i / 48), 0.205 * math.sin(2 * math.pi * i / 48), ztop) for i in range(49)]
    k.tube(rim, 0.02, navy, curved=True)

    # Folding hood over the head end (-x): half dome resting on the rim, with bows and side pivots.
    cx, R = -0.20, 0.23
    dome = [(R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for a in range(0, 91, 5)]
    dome[-1] = (0.0, R)
    hood = k.lathe(dome, at=(cx, 0, ztop), rot=(0, -90, 0), m=cream)
    k.warp(hood, lambda p: (max(p[0], 0.0), p[1], p[2]))
    for th, r in ((0, 0.02), (30, 0.014), (60, 0.014)):
        t = math.radians(th)
        pts = []
        for j in range(19):
            f = math.pi * j / 18
            rr = R + 0.008
            pts.append((cx - rr * math.sin(t) * math.sin(f), rr * math.cos(f), ztop + rr * math.cos(t) * math.sin(f)))
        k.tube(pts, r, bow_m, curved=True)
    for s in (-1, 1):
        k.cyl(0.032, 0.03, at=(cx, s * 0.245, ztop), rot=(90, 0, 0), m=silver)

    # Chassis: two side rails under the tub, curving down onto the axles.
    xr, xf, Rr, Rf, ty = -0.30, 0.30, 0.21, 0.17, 0.28
    for s in (-1, 1):
        y = s * 0.15
        k.tube([(xr, y, Rr), (-0.40, y, 0.30), (-0.33, y, 0.385), (0.0, y, 0.385), (0.33, y, 0.385),
                (0.38, y, 0.28), (xf, y, Rf)], 0.016, silver, curved=True)
        for x in (-0.15, 0.15):
            k.box((0.06, 0.05, 0.07), at=(x, y, 0.41), m=silver, bevel=0.008)

    # Axles and wheels.
    for x, R0 in ((xr, Rr), (xf, Rf)):
        k.cyl(0.016, 2 * ty + 0.04, at=(x, 0, R0), rot=(90, 0, 0), m=silver)
        for s in (-1, 1):
            c = (x, s * ty, R0)
            k.torus(R0 - 0.02, 0.022, at=c, rot=(90, 0, 0), m=tyre)
            k.torus(R0 - 0.045, 0.011, at=c, rot=(90, 0, 0), m=silver)
            k.cyl(0.04, 0.06, at=c, rot=(90, 0, 0), m=silver)
            for i in range(10):
                a = 2 * math.pi * i / 10
                k.tube([(x + 0.035 * math.cos(a), c[1], R0 + 0.035 * math.sin(a)),
                        (x + (R0 - 0.045) * math.cos(a), c[1], R0 + (R0 - 0.045) * math.sin(a))], 0.01, silver)

    # Long push handle fixed at the back, rising from the rails behind the hood.
    hx, hz = -0.74, 1.0
    for s in (-1, 1):
        k.tube([(-0.30, s * 0.15, 0.385), (-0.42, s * 0.16, 0.56), (hx, s * 0.17, hz)], 0.016, silver)
    k.tube([(-0.52, -0.163, 0.68), (-0.52, 0.163, 0.68)], 0.013, silver)
    k.cyl(0.028, 0.30, at=(hx, 0, hz), rot=(90, 0, 0), m=grip)
    k.cyl(0.016, 0.38, at=(hx, 0, hz), rot=(90, 0, 0), m=silver)

    # Cobblestone street: staggered rounded stones on dark mortar.
    k.box((5.2, 4.0, 0.06), at=(0, 0.4, -0.04), m=k.mat("#5c534b", "matte"), bevel=0, setting=True)
    stones = (k.mat("#9a8f84", "matte"), k.mat("#857a6f", "matte"), k.mat("#a89c8e", "matte"))
    p = 0.22
    for j in range(17):
        y = -1.45 + j * p
        for i in range(23):
            x = -2.5 + i * p + (p / 2 if j % 2 else 0)
            k.box((0.2, 0.2, 0.06), at=(x, y, -0.03), m=stones[(i * 7 + j * 3) % 3], bevel=0.035, setting=True)
