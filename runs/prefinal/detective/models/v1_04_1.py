# Detective badge lying flat on a plain purple floor, seen from above: a gold shield-shaped back plate with a
# pointed bottom, a silver face set into it, a raised gold rim running round the face, and a small house
# embossed in the centre of the face. Shield parts are 64-sided cylinders warped onto the shield outline.
import math

SCENE = {"category": "2", "backdrop": "#6a2bb0", "azimuth": 20, "elevation": 65, "lens": 60, "light": "left"}

N = 64


def _outline():
    # Shield outline in xy (top toward +y), counter-clockwise from the right side, resampled by arc length.
    raw = [(0.4, 0.05), (0.4, 0.40)]
    for i in range(1, 12):  # gentle arched top, right to left
        t = i / 12
        x = 0.4 - 0.8 * t
        raw.append((x, 0.40 + 0.07 * math.sin(t * math.pi)))
    raw += [(-0.4, 0.40), (-0.4, 0.05)]
    for i in range(1, 11):  # left lower curve down to the point
        t = i / 10
        raw.append((-0.4 * (1 - t) ** 1.4, 0.05 - 0.6 * math.sin(t * math.pi / 2)))
    for i in range(1, 10):  # right lower curve back up
        t = 1 - i / 10
        raw.append((0.4 * (1 - t) ** 1.4, 0.05 - 0.6 * math.sin(t * math.pi / 2)))
    loop = raw + [raw[0]]
    seg = [math.dist(loop[i], loop[i + 1]) for i in range(len(raw))]
    total = sum(seg)
    pts, j, acc = [], 0, 0.0
    for n in range(N):
        d = total * n / N
        while j < len(seg) - 1 and acc + seg[j] < d:
            acc += seg[j]
            j += 1
        f = (d - acc) / seg[j]
        a, b = loop[j], loop[j + 1]
        pts.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return pts


SHIELD = _outline()


def _shield_warp(radius, scale):
    def fn(p):
        x, y, z = p
        ang = math.atan2(y, x) % (2 * math.pi)
        idx = int(round(ang / (2 * math.pi) * N)) % N
        ratio = math.hypot(x, y) / radius  # keeps bevel rings inset
        sx, sy = SHIELD[idx]
        return (sx * scale * ratio, sy * scale * ratio, z)
    return fn


def build(k):
    gold = k.mat("#e8b53a", "metal")
    silver = k.mat("#cfd5de", "metal")

    # Gold back plate, full shield.
    R = 0.3
    plate = k.cyl(R, 0.04, at=(0, 0, 0.02), rot=(0, 0, 0), m=gold, bevel=0.008, verts=N)
    k.warp(plate, _shield_warp(R, 1.0))

    # Silver face lying on the plate.
    face = k.cyl(R, 0.016, at=(0, 0, 0.046), rot=(0, 0, 0), m=silver, bevel=0.004, verts=N)
    k.warp(face, _shield_warp(R, 0.9))

    # Raised gold rim around the face edge, a smooth closed loop.
    rim = [(x * 0.9, y * 0.9, 0.06) for x, y in SHIELD]
    k.tube(rim + rim[:3], 0.026, gold, curved=True)

    # Embossed house in silver relief on the face: walls, gable roof, chimney, and a door.
    k.box((0.2, 0.15, 0.024), at=(0, -0.06, 0.066), m=silver, bevel=0.004)
    roof = k.box((0.28, 0.13, 0.026), at=(0, 0.08, 0.067), m=silver, bevel=0.003)
    k.warp(roof, lambda p: (p[0] * 0.03 if p[1] > 0 else p[0], p[1], p[2]))
    k.box((0.035, 0.06, 0.02), at=(0.075, 0.105, 0.064), m=silver, bevel=0.003)
    k.box((0.045, 0.075, 0.008), at=(0, -0.0975, 0.082), m=k.mat("#9aa2ad", "metal"), bevel=0.002)

    k.turn(0, 0, -10)

    # Plain floor, a shade lighter than the backdrop, top at z = 0.
    k.box((6, 6, 0.1), at=(0, 0, -0.05), m=k.mat("#7d3fc4", "matte"), bevel=0, setting=True)
