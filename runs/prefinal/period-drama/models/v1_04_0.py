# Pocket watch: a round gold case (domed back, rounded rim, raised front bezel) holds a white dial facing the
# camera, with hour and minute hands on a centre cap. A stem rises from the top of the case into a fluted crown,
# and the ring loop sits on the crown. A short chain of interlocking links hangs from the loop and arcs down to
# the right, ending in a T-bar threaded through the last link. It floats, tilted a little to show face and rim.
import math

SCENE = {"category": "1", "backdrop": "#5fd35a", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#f2b62e", "metal")
    dark_gold = k.mat("#d9951c", "metal")
    dial = k.mat("#fbfaf4", "gloss")
    hand = k.mat("#2b2b33", "satin")

    cz = 0.45  # centre of the case
    # Case: revolved about local z, turned so its front (top of the profile) faces -y.
    case = [(0.0, 0.0), (0.15, 0.002), (0.26, 0.008), (0.33, 0.02), (0.37, 0.035), (0.395, 0.055),
            (0.402, 0.075), (0.40, 0.095), (0.39, 0.112), (0.375, 0.124), (0.36, 0.13), (0.345, 0.128),
            (0.335, 0.118), (0.33, 0.108), (0.0, 0.108)]
    k.lathe(case, at=(0, 0, cz), rot=(90, 0, 0), m=gold)
    # White dial, set just inside the bezel.
    k.cyl(0.332, 0.01, at=(0, -0.11, cz), rot=(90, 0, 0), m=dial, bevel=0.002)

    # Hands at ten past ten, lying on the dial.
    for angle, length, width in ((60, 0.25, 0.026), (-60, 0.17, 0.034)):
        a = math.radians(angle)
        k.box((width, 0.008, length), at=(0.5 * length * math.sin(a), -0.12, cz + 0.5 * length * math.cos(a)),
              rot=(0, angle, 0), m=hand, bevel=0.003)
    k.cyl(0.03, 0.016, at=(0, -0.124, cz), rot=(90, 0, 0), m=dark_gold, bevel=0.004)

    # Stem, crown and ring loop on top of the case.
    top = cz + 0.402
    k.cyl(0.04, 0.07, at=(0, -0.055, top + 0.02), m=gold, bevel=0.006)
    k.cyl(0.072, 0.075, at=(0, -0.055, top + 0.085), m=dark_gold, bevel=0.012, verts=20)
    k.sphere(0.03, at=(0, -0.055, top + 0.125), scale=(1, 1, 0.5), m=gold)
    ring_c = (0, -0.055, top + 0.21)
    k.torus(0.085, 0.02, at=ring_c, rot=(90, 0, 0), m=gold)

    # Short chain: interlocking links from the loop, arcing out and down to the right.
    p0 = (ring_c[0] + 0.08, ring_c[1], ring_c[2] + 0.02)
    p1 = (0.42, -0.06, ring_c[2] + 0.12)
    p2 = (0.6, -0.04, cz + 0.2)
    dense = []
    for i in range(201):
        t = i / 200
        dense.append(tuple((1 - t) ** 2 * p0[j] + 2 * (1 - t) * t * p1[j] + t * t * p2[j] for j in range(3)))
    spacing, links, acc = 0.066, [dense[0]], 0.0
    for a, b in zip(dense, dense[1:]):
        acc += math.dist(a, b)
        if acc >= spacing:
            links.append(b)
            acc = 0.0
    for i, p in enumerate(links):
        prev = links[max(i - 1, 0)]
        nxt = links[min(i + 1, len(links) - 1)]
        theta = math.degrees(math.atan2(nxt[2] - prev[2], nxt[0] - prev[0]))
        # Alternate links: flat in the x-z plane, then a quarter turn so they interlock.
        rot = (90, -theta, 0) if i % 2 == 0 else (0, -theta, 0)
        k.torus(0.04, 0.014, at=p, rot=rot, m=gold)
    # T-bar threaded through the last link, hanging as the free end.
    end = links[-1]
    k.cyl(0.018, 0.16, at=(end[0], end[1], end[2] - 0.04), rot=(0, 90, 0), m=gold, bevel=0.006)

    k.turn(-8, 10, 0)
