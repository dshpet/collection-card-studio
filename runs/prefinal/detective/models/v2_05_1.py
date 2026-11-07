# Badge wallet: an open bifold of brown leather lying flat on a dark wooden table. Two leather flaps meet at a
# rounded spine fold. The left flap carries a raised gold shield badge, one solid shield shape with a raised boss,
# fixed flat on a leather backing patch. On the right flap a cream card sits in a leather pocket, its top part
# showing, with a green stripe across it. The table fills the card and is seen from high above.
import math

SCENE = {"category": "3", "backdrop": "#3fc8e0", "azimuth": 15, "elevation": 70, "lens": 60, "light": "left"}


def shield(p):
    x, y, z = p
    r = 0.11
    u, v = x / r, y / r
    if v > 0:
        v = min(v, 0.55)
        u = math.copysign(min(abs(u) * 1.15, 1.0), u) if abs(u) > 0.01 else u
    else:
        u = u * (1 + v) ** 0.7 if v > -1 else 0.0
        v = v * 1.3
    return (u * r, v * r, z)


def build(k):
    leather = k.mat("#6a3517", "matte")
    leather_dk = k.mat("#4a230d", "matte")
    leather_lt = k.mat("#7a4020", "matte")
    gold = k.mat("#f2b632", "metal")
    cream = k.mat("#efe2c0", "satin")
    green = k.mat("#2fa84a", "satin")

    # Flaps and spine fold
    t = 0.035
    for side in (-1, 1):
        k.box((0.47, 0.5, t), at=(side * 0.25, 0, t / 2), m=leather, bevel=0.02)
    k.cyl(t * 0.75, 0.5, at=(0, 0, t * 0.75), rot=(90, 0, 0), m=leather_dk, bevel=0.01)

    # Left flap: leather backing patch with the gold shield badge
    k.box((0.36, 0.40, 0.012), at=(-0.25, 0, t + 0.006), m=leather_lt, bevel=0.008)
    bz = t + 0.012
    badge = k.cyl(0.11, 0.025, at=(-0.25, 0.01, bz + 0.0125), m=gold, bevel=0.006, verts=96)
    k.warp(badge, shield)
    k.cyl(0.045, 0.014, at=(-0.25, 0.0, bz + 0.032), m=gold, bevel=0.005)

    # Right flap: cream card standing out of a leather pocket, green stripe across it
    k.box((0.36, 0.24, 0.008), at=(0.25, 0.04, t + 0.004), m=cream, bevel=0.004)
    k.box((0.36, 0.05, 0.004), at=(0.25, 0.09, t + 0.009), m=green, bevel=0.002)
    k.box((0.40, 0.22, 0.016), at=(0.25, -0.12, t + 0.012), m=leather_lt, bevel=0.008)

    # Dark wooden table of planks, filling the card
    for i, hexc in enumerate(("#2e1a0d", "#36200f", "#2a170b", "#331d0e", "#28150a", "#341e0f", "#2e1a0d")):
        y = -1.5 + i * 0.5
        k.box((6, 0.48, 0.1), at=(0, y, -0.05), m=k.mat(hexc, "matte"), bevel=0.012, setting=True)
    k.box((6, 4, 0.05), at=(0, 0, -0.11), m=k.mat("#170c05", "matte"), bevel=0, setting=True)
