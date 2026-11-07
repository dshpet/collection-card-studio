# Pirate ship: a long wooden hull with a flat deck, a raised stern castle and a curved, pointed bow whose keel
# sweeps up into the stem, with a bowsprit. Three masts stand on the deck, the main one tallest, with a topmast
# above its upper yard; each mast carries two square sails hung from yards that cross it. A small red flag flies
# from the main topmast above the sails. The hull sits in calm sea water up to its waterline, which runs off the card.
import math

SCENE = {"category": "4", "backdrop": "#5cc4f5", "azimuth": 0, "elevation": 12, "lens": 60, "light": "left"}


def sheer(x):
    return 0.27 + max(0.0, x - 0.2) * 0.4


def pinch(x):
    return min(1.0, max(0.04, 1.0 - max(0.0, x - 0.12) / 0.46))


def build(k):
    hull_m = k.mat("#8a4f24", "matte")
    deck_m = k.mat("#c98a4b", "matte")
    trim_m = k.mat("#5e3418", "matte")
    mast_m = k.mat("#7a4520", "matte")
    sail_m = k.mat("#f7f3e8", "matte")
    flag_m = k.mat("#e0262b", "matte")

    # Hull: a row of merged ellipsoids along x (bow at +x), then pinched to a point and swept up at the bow.
    balls = [(-0.45 + i * 0.1, 0, 0.16, 0.16, (1.3, 1.0, 1.4)) for i in range(9)]
    hull = k.blob(balls, hull_m)

    def shape(p):
        x, y, z = p
        y *= pinch(x)
        t = min(1.0, max(0.0, (x - 0.15) / 0.42))
        if z < 0.2:
            z = z + (0.2 - z) * t * t * 0.85  # keel curving up into the stem
        z = min(z, sheer(x))
        if x > 0.3:
            z += (x - 0.3) * 0.25 * (z / 0.3)  # stem rising forward
        return (x, y, z)

    k.warp(hull, shape)

    # Deck following the hull's taper, and gunwale trim along both sides up to the stem.
    deck = k.box((0.86, 0.28, 0.02), at=(-0.08, 0, 0.265), m=deck_m, bevel=0.005)
    k.warp(deck, lambda p: (p[0], p[1] * pinch(p[0]), p[2] + max(0.0, p[0] - 0.2) * 0.4))
    for side in (-1, 1):
        pts = []
        for i in range(12):
            x = -0.6 + i * 0.105
            pts.append((x, side * 0.155 * pinch(x), sheer(x) + 0.012))
        k.tube(pts, 0.015, trim_m, curved=True)

    # Raised stern castle with a rail, sitting on the aft deck.
    k.box((0.26, 0.29, 0.12), at=(-0.5, 0, 0.33), m=hull_m, bevel=0.015)
    k.box((0.24, 0.27, 0.015), at=(-0.5, 0, 0.393), m=deck_m, bevel=0.004)
    for side in (-1, 1):
        k.box((0.26, 0.022, 0.04), at=(-0.5, side * 0.135, 0.415), m=trim_m, bevel=0.005)
    k.box((0.022, 0.29, 0.04), at=(-0.62, 0, 0.415), m=trim_m, bevel=0.005)

    # Bowsprit from the bow deck out over the stem and up.
    k.tube([(0.36, 0, 0.34), (0.82, 0, 0.5)], 0.02, mast_m)

    # Masts with two square sails each, braced a little toward the camera.
    brace = math.radians(-15)
    masts = [(-0.28, 0.88), (0.02, 1.1), (0.28, 0.94)]  # (x, top height)
    for mx, top in masts:
        base = sheer(mx) - 0.01
        k.cyl(0.024, top - base, at=(mx, 0, base + (top - base) / 2), m=mast_m)
        span = top - 0.38
        sails = [(0.38, 0.38 + span * 0.08, span * 0.48), (0.30, 0.38 + span * 0.6, span * 0.34)]
        for width, bottom, height in sails:
            off = 0.035
            sx, sy = mx + off * math.cos(brace), off * math.sin(brace)
            k.box((0.012, width, height), at=(sx, sy, bottom + height / 2), rot=(0, 0, math.degrees(brace)),
                  m=sail_m, bevel=0.004)
            k.cyl(0.013, width + 0.06, at=(mx + 0.02 * math.cos(brace), 0.02 * math.sin(brace),
                                            bottom + height + 0.005),
                  rot=(90, 0, math.degrees(brace)), m=mast_m)

    # Main topmast above the upper yard, with the small red flag flying aft from it, under a round cap.
    k.cyl(0.018, 0.16, at=(0.02, 0, 1.17), m=mast_m)
    k.box((0.13, 0.008, 0.07), at=(0.02 - 0.018 - 0.065, 0, 1.19), m=flag_m, bevel=0.002)
    k.sphere(0.024, at=(0.02, 0, 1.255), m=mast_m)

    k.turn(0, 0, -50)

    # Calm turquoise sea, its surface at the hull's waterline, running off the card.
    k.box((12, 12, 0.02), at=(0, 2, 0.09), m=k.mat("#25bfd3", "gloss"), bevel=0, setting=True)
