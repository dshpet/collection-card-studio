# Stage spotlight: clamp on the truss's bottom chord, a U yoke, a barrel pivoting on the yoke's side bolts,
# three lamps behind the lens and beams that start at the lens.
import math

SCENE = {"category": "1", "backdrop": "#1fb5b0", "azimuth": 0, "elevation": 6, "light": "right"}


def build(k):
    steel, dark = k.mat("#b9c0c8", "metal"), k.mat("#26304a", "satin")
    navy = k.mat("#1d2850", "satin")
    for y in (-0.06, 0.06):
        for z in (0.36, 0.48):
            k.tube([(-0.3, y, z), (0.3, y, z)], 0.012, steel)
    for i in range(6):
        x0, x1 = -0.3 + i * 0.1, -0.2 + i * 0.1
        a, b = (0.36, 0.48) if i % 2 else (0.48, 0.36)
        for y in (-0.06, 0.06):
            k.tube([(x0, y, a), (x1, y, b)], 0.007, steel)
        c, d = (-0.06, 0.06) if i % 2 else (0.06, -0.06)
        for z in (0.36, 0.48):
            k.tube([(x0, c, z), (x1, d, z)], 0.007, steel)
    k.box((0.05, 0.05, 0.05), at=(0, -0.06, 0.36), m=dark, bevel=0.008)
    k.cyl(0.012, 0.05, at=(0, -0.06, 0.315), m=dark)
    k.box((0.29, 0.03, 0.02), at=(0, -0.06, 0.29), m=dark, bevel=0.005)
    for side in (-1, 1):
        k.box((0.02, 0.03, 0.2), at=(side * 0.135, -0.06, 0.19), m=dark, bevel=0.005)
        k.cyl(0.022, 0.05, at=(side * 0.12, -0.06, 0.11), rot=(0, 90, 0), m=steel)

    center = (0, -0.06, 0.11)
    axis = (0, -math.sin(math.radians(60)), -0.5)
    tilt = (120, 0, 0)
    along = lambda d: tuple(c + a * d for c, a in zip(center, axis))
    k.cyl(0.1, 0.3, at=center, rot=tilt, m=navy, bevel=0.01)
    k.torus(0.1, 0.014, at=along(0.15), rot=tilt, m=dark)
    k.cyl(0.09, 0.01, at=along(0.148), rot=tilt, m=k.mat("#1a1f30", "gloss"), bevel=0)
    k.cyl(0.085, 0.02, at=along(-0.155), rot=tilt, m=dark)
    up = (0, -0.5, math.sin(math.radians(60)))
    for angle, color in ((90, "#ffd43a"), (210, "#3fe6ff"), (330, "#ff3b3b")):
        a = math.radians(angle)
        spot = tuple(f + 0.045 * (math.cos(a) * u + math.sin(a) * w) for f, u, w in zip(along(0.156), (1, 0, 0), up))
        k.cyl(0.028, 0.006, at=spot, rot=tilt, m=k.mat(color, "glow"), bevel=0)
        k.cone(0.03, 0.12, 0.36, at=tuple(s + a_ * 0.183 for s, a_ in zip(spot, axis)), rot=tilt, m=k.mat(color, "beam"),
               bevel=0)
    k.turn(z=-40)
