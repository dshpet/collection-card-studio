# Pirate ship: a rounded wooden hull with a flat deck, a raised stern castle and a curved bow with a bowsprit.
# Three masts stand on the deck, the main one tallest; each carries two square sails hung from yards that cross
# the mast. A small red flag flies from the top of the main mast. The hull floats in calm sea water that runs
# off the card. The ship is turned bow-toward-camera so the sails show their faces.
import math

SCENE = {"category": "4", "backdrop": "#5cc4f5", "azimuth": 0, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    hull_m = k.mat("#8a4f24", "matte")
    deck_m = k.mat("#c98a4b", "matte")
    trim_m = k.mat("#5e3418", "matte")
    mast_m = k.mat("#7a4520", "matte")
    sail_m = k.mat("#f7f3e8", "matte")
    flag_m = k.mat("#e0262b", "matte")

    # Hull: merged ellipsoids along x (bow at +x), the bow ones smaller and higher for the curved bow.
    balls = []
    for i in range(9):
        x = -0.42 + i * 0.1
        taper = 1.0 if x < 0.2 else 1.0 - (x - 0.2) * 1.6
        balls.append((x, 0, 0.15 + (0.03 if x > 0.3 else 0), 0.15 * taper, (1.25, 1.0, 1.2)))
    balls.append((0.47, 0, 0.24, 0.06, (1.3, 0.9, 1.1)))
    hull = k.blob(balls, hull_m)

    def clip(p):
        x, y, z = p
        top = 0.24 + max(0.0, x - 0.3) * 0.5  # deck line rising toward the bow
        return (x, y, min(z, top))

    k.warp(hull, clip)

    # Deck and gunwale trim.
    k.box((0.74, 0.24, 0.02), at=(-0.04, 0, 0.235), m=deck_m, bevel=0.005)
    for side in (-1, 1):
        k.tube([(-0.42, side * 0.125, 0.25), (0.15, side * 0.13, 0.25), (0.38, side * 0.09, 0.27),
                (0.5, side * 0.02, 0.3)], 0.014, trim_m, curved=True)

    # Raised stern castle with a rail.
    k.box((0.24, 0.25, 0.1), at=(-0.4, 0, 0.29), m=hull_m, bevel=0.015)
    k.box((0.22, 0.23, 0.015), at=(-0.4, 0, 0.343), m=deck_m, bevel=0.004)
    for side in (-1, 1):
        k.box((0.24, 0.022, 0.04), at=(-0.4, side * 0.115, 0.365), m=trim_m, bevel=0.005)
    k.box((0.022, 0.25, 0.04), at=(-0.51, 0, 0.365), m=trim_m, bevel=0.005)

    # Bowsprit from the bow deck out and up.
    k.tube([(0.36, 0, 0.27), (0.76, 0, 0.42)], 0.02, mast_m)

    # Masts with two square sails each, braced a little toward the camera.
    brace = math.radians(-15)
    masts = [(-0.24, 0.85), (0.04, 1.08), (0.3, 0.92)]  # (x, top height)
    for mx, top in masts:
        k.cyl(0.024, top - 0.22, at=(mx, 0, 0.22 + (top - 0.22) / 2), rot=(0, 0, 0), m=mast_m)
        span = top - 0.36
        sails = [(0.38, 0.36 + span * 0.08, span * 0.48), (0.30, 0.36 + span * 0.6, span * 0.34)]
        for width, bottom, height in sails:
            off = 0.035
            sx, sy = mx + off * math.cos(brace), off * math.sin(brace)
            k.box((0.012, width, height), at=(sx, sy, bottom + height / 2), rot=(0, 0, math.degrees(brace)),
                  m=sail_m, bevel=0.004)
            k.cyl(0.013, width + 0.06, at=(mx + 0.02 * math.cos(brace), 0.02 * math.sin(brace),
                                            bottom + height + 0.005),
                  rot=(90, 0, math.degrees(brace)), m=mast_m)
    # Small red flag on top of the main mast, flying aft, under a round mast cap.
    k.box((0.13, 0.008, 0.07), at=(0.04 - 0.065 - 0.02, 0, 1.04), m=flag_m, bevel=0.002)
    k.sphere(0.026, at=(0.04, 0, 1.085), m=mast_m)

    k.turn(0, 0, -50)

    # Calm turquoise sea running off the card.
    k.box((12, 12, 0.02), at=(0, 2, -0.01), m=k.mat("#25bfd3", "gloss"), bevel=0, setting=True)
