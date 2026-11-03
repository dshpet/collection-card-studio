# Cowboy boot, floating: the toe points +x so the camera sees the side profile and a little of the pointed toe.
# A tall oval shaft with V-scalloped top sinks into the heel counter of one smooth foot form that tapers to a
# pointed, slightly upturned toe. The foot sits on a dark sole that follows its outline, raised under the heel and
# flat under the forefoot, and the sole rests on an angled, forward-raked heel block. A gold spur band wraps the
# back of the heel counter, and a short shank carries a rowel on an axle pin.
import math

SCENE = {"category": "1", "backdrop": "#ffc22e", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8b4a1f", "matte")
    dark = k.mat("#3e2210", "matte")
    gold = k.mat("#e7b53c", "metal")

    def sole_top(X):
        if X < -0.02:
            return 0.16
        if X > 0.16:
            return 0.03
        return 0.16 - 0.13 * (X + 0.02) / 0.18

    def foot_r(X):
        t = min(1.0, max(0.0, (X + 0.1) / 0.52))
        return 0.02 + 0.105 * (1 - t) ** 1.3, t

    # Shaft: an open oval tube whose bottom sinks into the heel counter, with V dips front and back at the top.
    profile = [(0.12, 0.25), (0.121, 0.45), (0.126, 0.65), (0.134, 0.85), (0.142, 1.02),
               (0.128, 1.02), (0.12, 0.85), (0.112, 0.65), (0.106, 0.5), (0.0, 0.48)]
    shaft = k.lathe(profile, at=(-0.1, 0, 0), rot=(0, 0, 0), m=leather, verts=96)

    def scallop(p):
        x, y, z = p
        a = math.atan2(y, x)
        lift = max(0.0, (z - 0.75) / 0.27)
        return (x, y * 0.85, z - 0.1 * abs(math.cos(a)) ** 3 * lift)

    k.warp(shaft, scallop)

    # Foot: one smooth form from densely overlapping balls, heel counter to a pointed, upturned toe.
    balls = []
    n = 30
    for i in range(n + 1):
        X = -0.1 + 0.52 * i / n
        r, t = foot_r(X)
        sz = 1 - 0.3 * t
        z = sole_top(X) + r * sz + 0.018 * max(0.0, (t - 0.85) / 0.15)
        balls.append((X, 0, z, r, (1, 0.9, sz)))
    k.blob(balls, leather)

    # Sole: follows the foot outline, raised under the heel and flat under the forefoot.
    sole = k.cyl(1.0, 0.03, at=(0, 0, 0), rot=(0, 0, 0), m=dark, bevel=0.004, verts=96)

    def sole_shape(p):
        x, y, z = p
        X = -0.2 + (x + 1) / 2 * 0.65
        r, t = foot_r(X)
        w = 0.9 * r + 0.01
        return (X, y * w, z + sole_top(X) - 0.015)

    k.warp(sole, sole_shape)

    # Angled heel under the raised sole: the bottom is smaller and set forward, so the back face rakes under.
    heel = k.box((0.14, 0.19, 0.13), at=(-0.115, 0, 0.065), m=dark, bevel=0.008)

    def rake(p):
        x, y, z = p
        if z < 0:
            return (x * 0.7 + 0.025, y * 0.8, z)
        return p

    k.warp(heel, rake)

    # Spur: a band around the back of the heel counter, a shank, and a rowel on a pin.
    cx, cz, rx, ry = -0.1, 0.25, 0.124, 0.11
    arc = [math.radians(70 + i * 11) for i in range(21)]
    k.tube([(cx + rx * math.cos(a), ry * math.sin(a), cz) for a in arc], 0.013, gold, curved=True)
    k.tube([(cx - rx, 0, cz), (-0.29, 0, cz - 0.015), (-0.33, 0, cz - 0.02)], 0.012, gold)
    rc = (-0.36, cz - 0.02)
    k.cyl(0.042, 0.012, at=(rc[0], 0, rc[1]), rot=(90, 0, 0), m=gold, verts=10, bevel=0.002)
    for i in range(8):
        a = math.radians(i * 45)
        k.cone(0.008, 0.0, 0.03, at=(rc[0] + 0.052 * math.cos(a), 0, rc[1] + 0.052 * math.sin(a)),
               rot=(0, 90 - i * 45, 0), m=gold)
    k.cyl(0.012, 0.03, at=(rc[0], 0, rc[1]), rot=(90, 0, 0), m=gold)

    k.turn(0, -8, 10)
