# Crystal ball: a clear glass ball sits in the cup of a gold stand; three gold prongs rise from the cup rim and
# hug the ball's lower half. The stand is one turned piece: a round foot, a waist, and the cup. A red band wraps
# the straight side of the foot. Violet mist swirls inside the glass as one soft spiral form. It stands on a
# plain lighter-green ledge that runs off the card.
import math

SCENE = {"category": "2", "backdrop": "#3fae4a", "azimuth": 20, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e8b53a", "metal")
    red = k.mat("#d8262e", "satin")
    glass = k.mat("#eaf6ff", "glass")
    mist = k.mat("#9a4ee0", "satin")

    # Turned gold stand: foot, waist, cup (rim radius 0.22 at z = 0.36).
    profile = [(0.0, 0.0), (0.29, 0.0), (0.305, 0.012), (0.305, 0.115), (0.29, 0.13), (0.24, 0.145),
               (0.17, 0.165), (0.12, 0.19), (0.095, 0.215), (0.09, 0.24), (0.1, 0.265), (0.13, 0.29),
               (0.17, 0.315), (0.2, 0.338), (0.22, 0.355), (0.226, 0.365), (0.2, 0.36), (0.0, 0.29)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=gold)
    # Red band around the foot's side.
    k.cyl(0.316, 0.06, at=(0, 0, 0.064), rot=(0, 0, 0), m=red, bevel=0.008)

    # Glass ball resting in the cup.
    R = 0.33
    c = 0.36 + math.sqrt(R * R - 0.22 * 0.22)
    k.sphere(R, at=(0, 0, c), m=glass)

    # Three prongs from the cup rim, curving up along the ball surface.
    rp = R + 0.018
    for i in range(3):
        a = math.radians(90 + i * 120)
        pts = []
        for j in range(6):
            lat = math.radians(-48 + j * 6)  # latitude on the ball, from the rim upward
            rr = rp * math.cos(lat)
            pts.append((rr * math.cos(a), rr * math.sin(a), c + rp * math.sin(lat)))
        k.tube(pts, 0.022, gold, curved=True)
        k.sphere(0.03, at=pts[-1], m=gold)

    # Swirling violet mist inside the glass: one soft spiral.
    balls = []
    for i in range(22):
        t = i / 21
        ang = t * 2.6 * math.pi
        rad = 0.05 + 0.15 * math.sin(t * math.pi)
        z = c - 0.2 + 0.4 * t
        balls.append((rad * math.cos(ang), rad * math.sin(ang), z, 0.06 + 0.03 * math.sin(t * math.pi)))
    balls.append((0, 0, c, 0.11))
    k.blob(balls, mist)

    # Plain ledge, lighter than the backdrop, top at z = 0.
    k.box((5, 3, 0.4), at=(0, 0.6, -0.2), m=k.mat("#6fd27a", "matte"), bevel=0.01, setting=True)
