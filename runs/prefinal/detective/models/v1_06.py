# Rotary phone on a dark wooden desk: a low base plate carries the body, whose front slopes back; the gold dial
# plate sits flat on that sloped face with the black finger wheel and its ten holes on top and a finger stop at
# the lower right. On top, two pairs of cradle prongs hold the curved handset lying left to right, its earpiece
# and mouthpiece cups hanging past the body's top edge. The coiled cord leaves the earpiece end, drops beside the
# body, lies on the desk and enters the body's left side near the back.
import math

SCENE = {"category": "3", "backdrop": "#f5a623", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#111114", "gloss")
    gold = k.mat("#d9a93a", "metal")
    steel = k.mat("#c9ced6", "metal")
    cream = k.mat("#f3ead2", "satin")

    # Base plate and body; the warp narrows the top and slopes the front face back by about 24 degrees.
    k.box((0.82, 0.74, 0.04), at=(0, 0, 0.02), m=black, bevel=0.012)
    body = k.box((0.8, 0.72, 0.36), at=(0, 0, 0.22), m=black, bevel=0.06)

    def shape(p):
        x, y, z = p
        t = (z + 0.18) / 0.36
        x *= 1 - 0.2 * t
        y *= (1 - 0.45 * t) if y < 0 else (1 - 0.15 * t)
        return (x, y, z)

    k.warp(body, shape)

    # Front face frame: u across, v up the slope, w out along the face normal.
    slope = math.atan(0.162 / 0.36)
    s, c = math.sin(slope), math.cos(slope)
    cy, cz = -0.279, 0.22

    def fp(u, v, w):
        return (u, cy + v * s - w * c, cz + v * c + w * s)

    tilt = (90 - math.degrees(slope), 0, 0)
    k.cyl(0.145, 0.02, at=fp(0, 0, 0.0), rot=tilt, m=gold, bevel=0.006)
    k.cyl(0.13, 0.012, at=fp(0, 0, 0.016), rot=tilt, m=black, bevel=0.004)
    for i in range(10):
        a = math.radians(-60 + i * 29)
        k.cyl(0.021, 0.004, at=fp(0.093 * math.cos(a), 0.093 * math.sin(a), 0.023), rot=tilt, m=gold, bevel=0.002)
    k.cyl(0.045, 0.006, at=fp(0, 0, 0.024), rot=tilt, m=cream, bevel=0.003)
    a = math.radians(-95)
    k.tube([fp(0.12 * math.cos(a - 0.25), 0.12 * math.sin(a - 0.25), 0.035),
            fp(0.155 * math.cos(a), 0.155 * math.sin(a), 0.035)], 0.012, steel)

    # Cradle: a raised saddle block and two pairs of prongs.
    k.box((0.5, 0.26, 0.05), at=(0, 0.05, 0.415), m=black, bevel=0.02)
    for x in (-0.25, 0.25):
        for y in (-0.015, 0.115):
            k.cyl(0.022, 0.13, at=(x, y, 0.47), m=black, bevel=0.008)
            k.sphere(0.024, at=(x, y, 0.535), m=black)
        k.box((0.06, 0.15, 0.03), at=(x, 0.05, 0.47), m=black, bevel=0.01)

    # Handset: curved bar, with earpiece (left) and mouthpiece (right) cups opening downward.
    hy = 0.05
    k.tube([(-0.40, hy, 0.505), (-0.3, hy, 0.54), (0, hy, 0.555), (0.3, hy, 0.54), (0.40, hy, 0.505)],
           0.045, black, curved=True)
    cup = [(0, 0), (0.08, 0), (0.088, 0.02), (0.08, 0.05), (0.06, 0.08), (0.035, 0.1), (0, 0.105)]
    for side in (-1, 1):
        k.lathe(cup, at=(side * 0.41, hy, 0.415), rot=(0, side * 12, 0), m=black)

    # Coiled cord: a helix around a curve from the earpiece end down to the desk and into the body's side.
    A, B, C = (-0.47, 0.06, 0.44), (-0.58, 0.14, 0.0), (-0.40, 0.30, 0.045)

    def path(t):
        return tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t * t * cc for a, b, cc in zip(A, B, C))

    def norm(v):
        L = math.sqrt(sum(q * q for q in v))
        return tuple(q / L for q in v)

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    ref = norm((1, -1, 0))
    pts, n, turns = [], 320, 20
    for i in range(n + 1):
        t = i / n
        p0, p1 = path(max(t - 0.002, 0)), path(min(t + 0.002, 1))
        tan = norm(tuple(b - a for a, b in zip(p0, p1)))
        e1 = norm(cross(tan, ref))
        e2 = cross(tan, e1)
        ang = 2 * math.pi * turns * t
        p = path(t)
        pts.append(tuple(p[j] + 0.03 * (math.cos(ang) * e1[j] + math.sin(ang) * e2[j]) for j in range(3)))
    k.tube([(-0.42, 0.055, 0.45)] + pts + [(-0.37, 0.30, 0.05)], 0.011, black, curved=True)
    k.cyl(0.02, 0.05, at=(-0.39, 0.30, 0.05), rot=(0, 90, 0), m=black)

    # Dark wooden desk top.
    k.box((6, 2.2, 0.1), at=(0, 0.1, -0.05), m=k.mat("#5a3420", "matte"), bevel=0.01, setting=True)
