# Stage spotlight: clamp on the truss's bottom chord, a U yoke, a barrel pivoting on the yoke's side bolts and
# three lamps behind the lens. The truss runs off the card; the image model draws the beams.
import math

SCENE = {"category": "1", "backdrop": "#1fb5b0", "azimuth": 0, "elevation": 6, "light": "right"}


def build(k):
    steel, dark = k.mat("#b9c0c8", "metal"), k.mat("#26304a", "satin")
    navy = k.mat("#1d2850", "satin")
    truss = []
    for y in (-0.06, 0.06):
        for z in (0.36, 0.48):
            truss.append(k.tube([(-0.8, y, z), (0.8, y, z)], 0.016, steel))
    for i in range(16):
        x0, x1 = -0.8 + i * 0.1, -0.7 + i * 0.1
        a, b = (0.36, 0.48) if i % 2 else (0.48, 0.36)
        for y in (-0.06, 0.06):
            truss.append(k.tube([(x0, y, a), (x1, y, b)], 0.009, steel))
        c, d = (-0.06, 0.06) if i % 2 else (0.06, -0.06)
        for z in (0.36, 0.48):
            truss.append(k.tube([(x0, c, z), (x1, d, z)], 0.009, steel))
    k.unframed(*truss)
    k.box((0.06, 0.06, 0.06), at=(0, -0.06, 0.36), m=dark, bevel=0.01)
    k.cyl(0.016, 0.05, at=(0, -0.06, 0.31), m=dark)
    k.box((0.3, 0.04, 0.028), at=(0, -0.06, 0.286), m=dark, bevel=0.008)
    for side in (-1, 1):
        k.box((0.028, 0.04, 0.2), at=(side * 0.136, -0.06, 0.19), m=dark, bevel=0.008)
        k.cyl(0.026, 0.05, at=(side * 0.12, -0.06, 0.11), rot=(0, 90, 0), m=steel)

    center = (0, -0.06, 0.11)
    axis = (0, -math.sin(math.radians(60)), -0.5)
    tilt = (120, 0, 0)
    along = lambda d: tuple(c + a * d for c, a in zip(center, axis))
    k.cyl(0.1, 0.3, at=center, rot=tilt, m=navy, bevel=0.012)
    k.torus(0.1, 0.016, at=along(0.15), rot=tilt, m=dark)
    k.cyl(0.09, 0.01, at=along(0.148), rot=tilt, m=k.mat("#1a1f30", "gloss"), bevel=0)
    k.cyl(0.085, 0.02, at=along(-0.155), rot=tilt, m=dark)
    up = (0, -0.5, math.sin(math.radians(60)))
    for angle, color in ((90, "#ffd43a"), (210, "#3fe6ff"), (330, "#ff3b3b")):
        a = math.radians(angle)
        spot = tuple(f + 0.042 * (math.cos(a) * u + math.sin(a) * w) for f, u, w in zip(along(0.156), (1, 0, 0), up))
        k.cyl(0.03, 0.006, at=spot, rot=tilt, m=k.mat(color, "glow"), bevel=0)
    k.turn(z=-40)
