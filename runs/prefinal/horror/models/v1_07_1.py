# Magic mirror: a tall oval silver-white mirror face sits in a thick gold oval frame, backed by a gold panel. The
# frame's bottom rests on a turned gold neck rising from a wide, flat, oval gold base, and two S-scroll legs brace
# the frame's lower sides down to the base. Gold C-scrolls curl out from the frame's top on either side of a finial
# and from the middle of each side. Stands on a plain green floor, low three-quarter view.
import math

SCENE = {"category": "2", "backdrop": "#2f9e4f", "azimuth": 24, "elevation": 11, "lens": 60, "light": "left"}

CZ, A, B = 0.6, 0.29, 0.42  # oval center height, half-width, half-height


def oval_point(t, a, b, y):
    return (a * math.sin(t), y, CZ + b * math.cos(t))


def curl(cx, cz, R, start, turns, side, y=0.0, n=28, shrink=0.72):
    # A shrinking spiral in the xz plane, built for the right side and mirrored for side = -1.
    pts = []
    for i in range(n):
        t = i / (n - 1)
        ang = start - turns * 2 * math.pi * t
        r = R * (1 - shrink * t)
        pts.append((side * (cx + r * math.cos(ang)), y, cz + r * math.sin(ang)))
    return pts


def build(k):
    gold = k.mat("#e8b53a", "metal")
    dark_gold = k.mat("#c99227", "metal")
    mirror = k.mat("#eef3f8", "gloss")

    # Oval frame: thick outer ring and a thinner inner bead, both closed loops.
    ring = [oval_point(2 * math.pi * i / 48, A, B, 0.0) for i in range(49)]
    k.tube(ring, 0.036, gold, curved=True)
    bead = [oval_point(2 * math.pi * i / 48, A - 0.035, B - 0.035, -0.022) for i in range(49)]
    k.tube(bead, 0.013, dark_gold, curved=True)

    # Opaque silver-white mirror face and the gold back panel behind it: discs stretched into ovals.
    g = k.cyl(A - 0.01, 0.012, at=(0, -0.006, CZ), rot=(90, 0, 0), m=mirror, bevel=0.002)
    k.warp(g, lambda p: (p[0], p[1] * B / A, p[2]))
    back = k.cyl(A + 0.01, 0.02, at=(0, 0.024, CZ), rot=(90, 0, 0), m=dark_gold, bevel=0.004)
    k.warp(back, lambda p: (p[0], p[1] * B / A, p[2]))

    # Wide flat oval base.
    base = k.lathe([(0, 0), (0.33, 0), (0.345, 0.018), (0.33, 0.04), (0.28, 0.055), (0.2, 0.062), (0, 0.064)],
                   at=(0, 0, 0), rot=(0, 0, 0), m=gold)
    k.warp(base, lambda p: (p[0], p[1] * 0.62, p[2]))

    # Turned neck from the base up into the frame's bottom.
    bottom = CZ - B
    k.lathe([(0, 0.06), (0.09, 0.06), (0.085, 0.08), (0.05, 0.1), (0.04, 0.13), (0.055, 0.15),
             (0.06, bottom + 0.01), (0, bottom + 0.02)], at=(0, 0, 0), rot=(0, 0, 0), m=gold)

    for s in (-1, 1):
        # S-scroll legs: from the frame's lower side down to the base, ending in a small curl on it.
        fx, _, fz = oval_point(math.radians(140), A, B, 0)
        leg = [(s * (fx + 0.02), 0, fz), (s * 0.26, 0, fz - 0.07), (s * 0.235, 0, 0.13), (s * 0.26, 0, 0.085)]
        leg += curl(0.29, 0.095, 0.03, math.pi, 0.9, s, n=12)[1:]
        k.tube(leg, 0.019, gold, curved=True)

        # Top crest C-scrolls curling outward from the frame's top.
        k.tube(curl(0.12, CZ + B + 0.025, 0.065, math.radians(-150), 1.25, s), 0.02, gold, curved=True)

        # Side scrolls at the middle of the frame, starting against the ring.
        k.tube(curl(A + 0.065, CZ + 0.03, 0.05, math.radians(-125), 1.2, s), 0.019, gold, curved=True)

    # Finial on top of the frame.
    top = CZ + B
    k.lathe([(0, top + 0.01), (0.04, top + 0.02), (0.03, top + 0.05), (0.045, top + 0.09), (0.02, top + 0.13),
             (0, top + 0.15)], at=(0, 0, 0), rot=(0, 0, 0), m=gold)

    # Plain floor, a shade lighter than the backdrop, running off the card.
    k.box((4, 3, 0.12), at=(0, 0.6, -0.06), m=k.mat("#4cbb68", "satin"), bevel=0.01, setting=True)
