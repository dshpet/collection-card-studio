# Witch hat: a tall cone with a slightly concave taper whose tip flops back and to the side; it stands on a wide
# round brim that stays nearly flat and turns up only in a short lip at the outer edge, with a gentle wave. A purple
# band wraps the base of the cone, and a small yellow square buckle sits on the band at the front. Floating, tilted
# toward the camera to show the brim's top.
import math

SCENE = {"category": "1", "backdrop": "#ff8a1f", "azimuth": 25, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    felt = k.mat("#24202b", "matte")
    band = k.mat("#7b3fc4", "matte")
    gold = k.mat("#ffd23a", "satin")

    # Brim: a flat disk out and back, then a short upturned lip at the edge with a soft wave.
    rs = [i * 0.52 / 32 for i in range(33)]
    profile = [(r, 0.0) for r in rs] + [(r, 0.026) for r in reversed(rs)]
    brim = k.lathe(profile, at=(0, 0, 0), m=felt, verts=96)

    def curl(p):
        x, y, z = p
        r = math.hypot(x, y)
        a = math.atan2(y, x)
        t = max(0.0, (r - 0.38) / 0.14)
        return (x, y, z + 0.075 * t ** 2.2 + 0.015 * (r / 0.52) ** 3 * math.cos(3 * a + 0.6))

    k.warp(brim, curl)

    # Crown: concave taper to a point, bent back and to the side near the top.
    h, base = 0.88, 0.215

    def radius(z):
        return base * (1 - z / h) ** 1.25

    zs = [0.015 + i * (h - 0.015) / 40 for i in range(41)]
    crown = k.lathe([(radius(z), z) for z in zs[:-1]] + [(0.0, h)], at=(0, 0, 0), m=felt)

    def bend(p):
        x, y, z = p
        s = (z / h) ** 3
        return (x + 0.16 * s, y + 0.12 * s, z - 0.06 * s)

    k.warp(crown, bend)

    # Band hugging the crown's base.
    bz = [0.03 + i * 0.1 / 8 for i in range(9)]
    k.lathe([(radius(z) + 0.012, z) for z in bz] + [(radius(z) + 0.001, z) for z in reversed(bz)],
            at=(0, 0, 0), m=band)

    # Buckle: a square frame with a center prong on the front of the band, leaning with the crown's slope.
    zc = 0.08
    y0 = -(radius(zc) + 0.02)
    tilt = -math.degrees(math.atan(base * 1.25 / h))
    w, hh, t = 0.1, 0.085, 0.02
    lean = math.tan(math.radians(-tilt))
    for dx, dz, sx, sz in ((0, hh / 2 - t / 2, w, t), (0, -hh / 2 + t / 2, w, t),
                           (w / 2 - t / 2, 0, t, hh), (-w / 2 + t / 2, 0, t, hh)):
        k.box((sx, 0.016, sz), at=(dx, y0 + dz * lean, zc + dz), rot=(tilt, 0, 0), m=gold, bevel=0.004)
    k.box((0.012, 0.012, hh - 2 * t), at=(0, y0 - 0.004, zc), rot=(tilt, 0, 0), m=gold, bevel=0.003)

    k.turn(12, -6, 0)
