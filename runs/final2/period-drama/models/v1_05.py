# Pocket watch: a round gold case (lathe, face toward -y) with a raised bezel ring holding the white dial; navy hour
# ticks and two hands with a centre cap sit on the dial. A stem rises from the top of the case into a ridged crown,
# the ring bow passes through the crown's top, and a short chain of interlocking links hangs from the bow's top,
# arcing out to the right and ending free in a small T-bar. Floating, tilted to show the dial and some of the rim.
import math

SCENE = {"category": "1", "backdrop": "#5fd068", "azimuth": 22, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#f2b632", "metal")
    dial = k.mat("#fbfaf4", "gloss")
    navy = k.mat("#1f2f6b", "satin")
    z0 = 0.45

    # Case: lathe about local z, rotated so local +z points to the front (-y).
    case = [(0.0, -0.075), (0.22, -0.073), (0.31, -0.065), (0.36, -0.048), (0.383, -0.022), (0.388, 0.0),
            (0.384, 0.022), (0.372, 0.04), (0.35, 0.05), (0.0, 0.05)]
    k.lathe(case, at=(0, 0, z0), rot=(90, 0, 0), m=gold)
    k.torus(0.345, 0.03, at=(0, -0.055, z0), rot=(90, 0, 0), m=gold)
    k.cyl(0.33, 0.012, at=(0, -0.056, z0), rot=(90, 0, 0), m=dial, bevel=0.002)

    # Hour ticks (raised), hands and centre cap.
    fy = -0.064
    for i in range(12):
        a = math.radians(i * 30)
        big = i % 3 == 0
        r = 0.275
        k.box((0.022 if big else 0.014, 0.008, 0.05 if big else 0.032),
              at=(r * math.sin(a), fy, z0 + r * math.cos(a)), rot=(0, i * 30, 0), m=navy, bevel=0.002)
    for ang, length, width in ((-60, 0.16, 0.026), (60, 0.235, 0.018)):  # hour hand at 10, minute hand at 2
        a = math.radians(ang)
        c = length / 2 - 0.02
        k.box((width, 0.008, length), at=(c * math.sin(a), fy - 0.004, z0 + c * math.cos(a)),
              rot=(0, ang, 0), m=navy, bevel=0.003)
    k.cyl(0.028, 0.016, at=(0, fy - 0.008, z0), rot=(90, 0, 0), m=gold)

    # Stem, crown, bow.
    k.cyl(0.035, 0.07, at=(0, 0, z0 + 0.405), m=gold)
    k.cyl(0.062, 0.07, at=(0, 0, z0 + 0.465), m=gold, verts=20, bevel=0.008)
    k.cyl(0.04, 0.02, at=(0, 0, z0 + 0.505), m=gold)
    bow_c, bow_r, bow_t = z0 + 0.585, 0.085, 0.02
    k.torus(bow_r, bow_t, at=(0, 0, bow_c), rot=(90, 0, 0), m=gold)

    # Chain: links along a quadratic curve from the bow top, alternating planes, ending free.
    p0, p1, p2 = (0.0, bow_c + bow_r), (0.36, bow_c + 0.3), (0.62, z0 + 0.42)

    def curve(t):
        u = 1 - t
        return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])

    samples = [curve(i / 400) for i in range(401)]
    dist = [0.0]
    for a, b in zip(samples, samples[1:]):
        dist.append(dist[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    step, s, n = 0.085, 0.035, 0
    last = None
    while s < dist[-1]:
        j = next(i for i, d in enumerate(dist) if d >= s)
        j = max(1, min(j, 399))
        (x, z), (xa, za), (xb, zb) = samples[j], samples[j - 1], samples[j + 1]
        ang = math.degrees(math.atan2(zb - za, xb - xa))
        rot = (90, -ang, 0) if n % 2 == 0 else (0, -ang, 0)
        link = k.torus(0.034, 0.012, at=(x, 0, z), rot=rot, m=gold)
        k.warp(link, lambda v: (v[0] * 1.45, v[1], v[2]))
        last = (x, z, ang)
        s += step
        n += 1
    x, z, ang = last
    a = math.radians(ang)
    ex, ez = x + 0.065 * math.cos(a), z + 0.065 * math.sin(a)
    k.cyl(0.016, 0.13, at=(ex, 0, ez), rot=(0, -ang, 0), m=gold, bevel=0.004)

    k.turn(8, -8, -14)
