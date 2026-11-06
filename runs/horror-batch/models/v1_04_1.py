# Brass candlestick: a wide flat round base, a straight stem rising from its domed center, and a cup (drip pan)
# on top that holds one tall white candle with a short wick and a small flame. A finger ring stands upright on the
# base's right edge, held by a sturdy tab into the rim. It stands on a plain grey stone ledge.
SCENE = {"category": "2", "backdrop": "#3cc8e8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    brass = k.mat("#d9a536", "metal")
    wax = k.mat("#f7f3e8", "satin")

    # Wide flat base with a rounded rim and a low dome where the stem sits.
    k.lathe([(0, 0), (0.27, 0), (0.285, 0.012), (0.285, 0.028), (0.27, 0.04), (0.2, 0.05),
             (0.12, 0.06), (0.075, 0.08), (0.05, 0.1), (0.045, 0.11), (0, 0.11)], at=(0, 0, 0), m=brass)

    # Straight stem with a collar at each end.
    k.cyl(0.032, 0.42, at=(0, 0, 0.31), m=brass)
    k.torus(0.034, 0.012, at=(0, 0, 0.115), m=brass)
    k.torus(0.034, 0.012, at=(0, 0, 0.5), m=brass)

    # Cup on top of the stem, flaring out to a rolled lip; the candle sits in it.
    k.lathe([(0, 0.49), (0.04, 0.49), (0.06, 0.505), (0.1, 0.53), (0.12, 0.555), (0.122, 0.57),
             (0.11, 0.578), (0.07, 0.57), (0, 0.57)], at=(0, 0, 0), m=brass)

    # Tall white candle, wick and small flame.
    k.cyl(0.052, 0.4, at=(0, 0, 0.765), m=wax, bevel=0.008)
    k.cyl(0.007, 0.03, at=(0, 0, 0.978), m=k.mat("#3a2a20", "matte"))
    k.sphere(0.022, at=(0, 0, 1.012), scale=(1, 1, 1.8), m=k.mat("#ff9a2a", "glow"))

    # Finger ring standing upright on the base's right edge, joined by a sturdy tab that runs into the rim.
    k.box((0.1, 0.05, 0.05), at=(0.29, 0, 0.03), m=brass, bevel=0.01)
    k.torus(0.07, 0.018, at=(0.38, 0, 0.09), rot=(90, 0, 0), m=brass)

    # Plain grey stone ledge.
    k.box((4, 1.6, 0.12), at=(0, 0.3, -0.06), m=k.mat("#6f7279", "matte"), bevel=0.01, setting=True)
