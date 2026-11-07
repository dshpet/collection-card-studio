# Badge wallet: an open bifold of brown leather lying flat on a dark wooden table. Two leather flaps meet at a
# rounded spine fold. The left flap carries a raised gold shield badge, fixed flat on a leather backing patch.
# On the right flap a cream card sits in a leather pocket, its top part showing, with a green stripe across it.
# The table fills the card and is seen from high above.
SCENE = {"category": "3", "backdrop": "#3fc8e0", "azimuth": 25, "elevation": 65, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4f28", "matte")
    leather_dk = k.mat("#6b3a1c", "matte")
    leather_lt = k.mat("#a3633a", "matte")
    gold = k.mat("#f2b632", "metal")
    cream = k.mat("#f4ead0", "satin")
    green = k.mat("#2fa84a", "satin")

    # Flaps and spine fold
    t = 0.035
    for side in (-1, 1):
        k.box((0.47, 0.5, t), at=(side * 0.25, 0, t / 2), m=leather, bevel=0.02)
    k.cyl(t * 0.75, 0.5, at=(0, 0, t * 0.75), rot=(90, 0, 0), m=leather_dk, bevel=0.01)

    # Left flap: leather backing patch with the gold shield badge
    k.box((0.36, 0.40, 0.012), at=(-0.25, 0, t + 0.006), m=leather_lt, bevel=0.008)
    bz = t + 0.012
    k.box((0.22, 0.15, 0.03), at=(-0.25, 0.06, bz + 0.015), m=gold, bevel=0.012)
    k.box((0.155, 0.155, 0.03), at=(-0.25, -0.025, bz + 0.015), rot=(0, 0, 45), m=gold, bevel=0.012)
    k.box((0.24, 0.03, 0.034), at=(-0.25, 0.135, bz + 0.017), m=gold, bevel=0.012)
    k.cyl(0.05, 0.016, at=(-0.25, 0.03, bz + 0.038), m=gold, bevel=0.006)

    # Right flap: cream card standing out of a leather pocket, green stripe across it
    k.box((0.36, 0.24, 0.008), at=(0.25, 0.04, t + 0.004), m=cream, bevel=0.004)
    k.box((0.36, 0.05, 0.004), at=(0.25, 0.09, t + 0.009), m=green, bevel=0.002)
    k.box((0.40, 0.22, 0.016), at=(0.25, -0.12, t + 0.012), m=leather_lt, bevel=0.008)

    # Dark wooden table of planks, filling the card
    for i, hexc in enumerate(("#4a2c18", "#53321c", "#472915", "#4f2f1a", "#442714", "#51311b", "#4a2c18")):
        y = -1.5 + i * 0.5
        k.box((6, 0.48, 0.1), at=(0, y, -0.05), m=k.mat(hexc, "matte"), bevel=0.012, setting=True)
    k.box((6, 4, 0.05), at=(0, 0, -0.11), m=k.mat("#2a170b", "matte"), bevel=0, setting=True)
