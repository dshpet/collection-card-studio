# Badge wallet: an open bifold of brown leather lying flat on a dark wooden table. Two leather flaps meet at a
# rounded spine fold. The left flap carries a raised gold shield badge (flat top, straight sides, pointed bottom)
# with a raised round boss, fixed flat on a leather backing patch. On the right flap a cream card sits in a
# leather pocket, its top part showing, with a green stripe across it. The table fills the card from high above.
import math

SCENE = {"category": "3", "backdrop": "#3fc8e0", "azimuth": 15, "elevation": 70, "lens": 70, "light": "left"}

SHIELD = [(-1.0, 0.8), (-0.5, 0.7), (0.0, 0.8), (0.5, 0.7), (1.0, 0.8), (1.0, 0.05), (0.85, -0.45),
          (0.5, -0.85), (0.0, -1.15), (-0.5, -0.85), (-0.85, -0.45), (-1.0, 0.05)]


def shield_radius(dx, dy):
    best = 10.0
    n = len(SHIELD)
    for i in range(n):
        ax, ay = SHIELD[i]
        bx, by = SHIELD[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = (ax * ey - ay * ex) / den
        s = (ax * dy - ay * dx) / den
        if t > 0 and -1e-6 <= s <= 1 + 1e-6:
            best = min(best, t)
    return best


def make_shield(r):
    def fn(p):
        x, y, z = p
        d = math.hypot(x, y)
        if d < 1e-6:
            return p
        dx, dy = x / d, y / d
        k = shield_radius(dx, dy) * (d / r)
        return (dx * k * r, dy * k * r, z)
    return fn


def build(k):
    leather = k.mat("#4f240c", "matte")
    leather_dk = k.mat("#331607", "matte")
    leather_lt = k.mat("#5c2c10", "matte")
    gold = k.mat("#e8a820", "metal")
    cream = k.mat("#e6cf98", "satin")
    green = k.mat("#1d8a38", "satin")

    # Flaps and spine fold
    t = 0.035
    for side in (-1, 1):
        k.box((0.47, 0.5, t), at=(side * 0.25, 0, t / 2), m=leather, bevel=0.02)
    k.cyl(t * 0.75, 0.5, at=(0, 0, t * 0.75), rot=(90, 0, 0), m=leather_dk, bevel=0.01)

    # Left flap: leather backing patch with the gold shield badge
    k.box((0.36, 0.40, 0.012), at=(-0.25, 0, t + 0.006), m=leather_lt, bevel=0.008)
    bz = t + 0.012
    r = 0.13
    badge = k.cyl(r, 0.025, at=(-0.25, 0.02, bz + 0.0125), m=gold, bevel=0.005, verts=128)
    k.warp(badge, make_shield(r))
    k.cyl(0.045, 0.014, at=(-0.25, 0.01, bz + 0.032), m=gold, bevel=0.005)

    # Right flap: cream card standing out of a leather pocket, green stripe across it
    k.box((0.36, 0.24, 0.008), at=(0.25, 0.04, t + 0.004), m=cream, bevel=0.004)
    k.box((0.36, 0.05, 0.004), at=(0.25, 0.09, t + 0.009), m=green, bevel=0.002)
    k.box((0.40, 0.22, 0.016), at=(0.25, -0.12, t + 0.012), m=leather_lt, bevel=0.008)

    # Dark wooden table of planks, filling the card
    for i, hexc in enumerate(("#1c0e06", "#22120a", "#190c05", "#201109", "#170b04", "#211109", "#1c0e06")):
        y = -1.5 + i * 0.5
        k.box((6, 0.48, 0.1), at=(0, y, -0.05), m=k.mat(hexc, "matte"), bevel=0.012, setting=True)
    k.box((6, 4, 0.05), at=(0, 0, -0.11), m=k.mat("#0d0602", "matte"), bevel=0, setting=True)
