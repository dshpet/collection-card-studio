# Wooden coffin standing upright on the graveyard grass: a six-sided body (narrow foot, wide shoulders, narrow
# head) with the lid hinged along its lower-left long edge on two hinges and swung slightly open, showing the purple
# lining panel inside. A tan cross is raised on the lid's front. A grassy hill, a few tombstones and two trees stand
# far back.
import math

SCENE = {"category": "4", "backdrop": "#5fd3f0", "azimuth": 25, "elevation": 11, "lens": 60, "light": "left"}

# Coffin outline in the front (x, z) plane: foot, shoulders, head.
OUTLINE = [(-0.13, 0.0), (0.13, 0.0), (0.23, 0.68), (0.16, 1.0), (-0.16, 1.0), (-0.23, 0.68)]
CENTER = (0.0, 0.6)
# Lid hinge axis: the lower-left long edge on the body's front face.
HINGE_A, HINGE_B = (-0.13, 0.03, 0.0), (-0.23, 0.03, 0.68)
OPEN = -16


def hit(d):
    # Distance from CENTER along direction d to the outline.
    best = None
    for i in range(len(OUTLINE)):
        p, q = OUTLINE[i], OUTLINE[(i + 1) % len(OUTLINE)]
        ex, ez = q[0] - p[0], q[1] - p[1]
        den = d[0] * ez - d[1] * ex
        if abs(den) < 1e-9:
            continue
        wx, wz = p[0] - CENTER[0], p[1] - CENTER[1]
        t = (wx * ez - wz * ex) / den
        s = (wx * d[1] - wz * d[0]) / den
        if t > 0 and -1e-6 <= s <= 1 + 1e-6 and (best is None or t < best):
            best = t
    return best


def swing(p):
    ax = [HINGE_B[i] - HINGE_A[i] for i in range(3)]
    n = math.sqrt(sum(a * a for a in ax))
    kx, ky, kz = (a / n for a in ax)
    vx, vy, vz = (p[i] - HINGE_A[i] for i in range(3))
    c, s = math.cos(math.radians(OPEN)), math.sin(math.radians(OPEN))
    dot = kx * vx + ky * vy + kz * vz
    cx, cy, cz = ky * vz - kz * vy, kz * vx - kx * vz, kx * vy - ky * vx
    return tuple(v * c + cr * s + kk * dot * (1 - c) + HINGE_A[i]
                 for i, (v, cr, kk) in enumerate(((vx, cx, kx), (vy, cy, ky), (vz, cz, kz))))


def slab(k, y0, y1, m, scale=1.0, swung=False):
    # A six-sided prism with the coffin outline, from y0 to y1, made by warping a round cylinder.
    r, h = 0.5, y1 - y0

    def fn(p):
        x, y, z = p
        rho = math.sqrt(x * x + y * y) / r
        if rho < 1e-6:
            X, Z = CENTER
        else:
            d = (x / (rho * r), y / (rho * r))
            t = hit(d) * rho * scale
            X, Z = CENTER[0] + d[0] * t, CENTER[1] + d[1] * t
        world = (X, y0 + (z / h + 0.5) * h, Z)
        if swung:
            world = swing(world)
        return (world[0], world[2], -world[1])

    return k.warp(k.cyl(r, h, at=(0, 0, 0), rot=(90, 0, 0), m=m, verts=64), fn)


def build(k):
    wood = k.mat("#7a4524", "matte")
    lid_wood = k.mat("#8a5029", "matte")
    tan = k.mat("#e2bf86", "matte")
    lining = k.mat("#7b3fa8", "matte")
    iron = k.mat("#5b5f66", "metal")

    slab(k, 0.03, 0.25, wood)
    slab(k, 0.02, 0.03, lining, scale=0.88)
    slab(k, -0.025, 0.03, lid_wood, swung=True)

    # Raised cross on the lid's front, swung with the lid.
    for size, at in (((0.055, 0.022, 0.56), (0.0, -0.035, 0.56)), ((0.27, 0.022, 0.055), (0.0, -0.035, 0.68))):
        k.warp(k.box(size, at=(0, 0, 0), m=tan, bevel=0.006),
               lambda p, at=at: swing((p[0] + at[0], p[1] + at[1], p[2] + at[2])))

    # Two hinge barrels on the hinge edge.
    tilt = -math.degrees(math.atan2(0.10, 0.68))
    for z in (0.17, 0.52):
        x = HINGE_A[0] + (HINGE_B[0] - HINGE_A[0]) * z / 0.68
        k.cyl(0.02, 0.09, at=(x - 0.008, 0.03, z), rot=(0, tilt, 0), m=iron)

    # Graveyard: grass, a soft hill behind, a few tombstones and two trees far back.
    k.floor("#5fbf3a")
    k.sphere(3.0, at=(1.0, 8.0, -2.2), scale=(1.6, 1.0, 1.0), m=k.mat("#4fae35", "matte"), setting=True)
    stone = k.mat("#a9a7b3", "matte")
    for x, y, w, h in ((-1.9, 3.2, 0.34, 0.42), (1.4, 3.8, 0.3, 0.38), (2.6, 2.8, 0.36, 0.46)):
        body = h - w / 2
        k.box((w, 0.1, body), at=(x, y, body / 2), m=stone, bevel=0.02, setting=True)
        k.cyl(w / 2, 0.096, at=(x, y, body), rot=(90, 0, 0), m=stone, setting=True)
    trunk, leaves = k.mat("#6b4428", "matte"), k.mat("#3f9a3a", "matte")
    for x, y in ((-4.5, 10.0), (5.0, 11.0)):
        k.cyl(0.1, 1.2, at=(x, y, 0.6), m=trunk, setting=True)
        k.blob([(x, y, 1.5, 0.6), (x - 0.4, y, 1.3, 0.45), (x + 0.4, y, 1.35, 0.45), (x, y, 1.95, 0.4)],
               leaves, setting=True)
