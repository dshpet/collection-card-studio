# Carved pumpkin on a wooden table: a squat ribbed body (a lathe with eight lobes pressed in by a warp) rests on
# the plank top, with a short tapered stem leaning out of the dimple on top. The carved face sits on the front
# lobe: two up-pointing triangle eyes and a zigzag grin, built from small glowing plates whose corners lie on the
# skin, so the openings follow the curve of the body.
import math

SCENE = {"category": "3", "backdrop": "#7a3fc8", "azimuth": 14, "elevation": 15, "lens": 60, "light": "left"}

A, C = 0.5, 0.34  # body half-width and half-height
LOBES, GROOVE = 8, 0.07


def lobe(theta):
    g = (1 - math.cos(LOBES * (theta + math.pi / 2))) / 2  # 0 on a crest (the front is one), 1 in a groove
    return 1 - GROOVE * g ** 3


def profile():
    points = []
    for i in range(41):
        t = math.radians(-90 + i * 4.5)
        r, z = A * math.cos(t), C + C * math.sin(t)
        if z > C:
            z -= 0.07 * math.exp(-(r / 0.13) ** 2)  # dimple under the stem
        else:
            z += 0.035 * math.exp(-(r / 0.16) ** 2)  # flattened underside
        points.append((max(r, 0.0), z))
    low = min(z for _, z in points)
    return [(r, z - low) for r, z in points], C - low  # resting on z = 0; returns the body center height


def skin(u, v, zc, depth):
    """Point on the front of the body at arc offset u (to the right) and height v above the center."""
    re = A * math.sqrt(max(0.05, 1 - (v / C) ** 2))
    phi = u / re
    r = re * lobe(phi - math.pi / 2)
    nx, ny, nz = math.sin(phi) * re / A ** 2, -math.cos(phi) * re / A ** 2, v / C ** 2
    n = math.sqrt(nx * nx + ny * ny + nz * nz)
    return (r * math.sin(phi) + depth * nx / n, -r * math.cos(phi) + depth * ny / n, zc + v + depth * nz / n)


def build(k):
    orange = k.mat("#f2801c", "satin")
    green = k.mat("#4f9a2c", "matte")
    glow = k.mat("#ffd23a", "glow")

    prof, zc = profile()
    body = k.lathe(prof, at=(0, 0, 0), rot=(0, 0, 0), m=orange, verts=128)
    k.warp(body, lambda p: (p[0] * lobe(math.atan2(p[1], p[0])), p[1] * lobe(math.atan2(p[1], p[0])), p[2]))

    def patch(quad):
        """A glowing plate over four (u, v) corners: front face just proud of the skin, back sunk into the body."""
        part = k.box((1, 1, 1), at=(0, 0, 0), rot=(0, 0, 0), m=glow, bevel=0)
        corners = {(-1, -1): quad[0], (1, -1): quad[1], (1, 1): quad[2], (-1, 1): quad[3]}

        def place(p):
            sx, sy, sz = (1 if c > 0 else -1 for c in p)
            u, v = corners[(sx, sy)]
            return skin(u, v, zc, 0.006 if sz > 0 else -0.03)
        k.warp(part, place)

    # Eyes: up-pointing triangles, cut in strips (and halves) so each plate hugs the curve.
    for side in (-1, 1):
        cu, base, top, half, steps = side * 0.155, 0.055, 0.2, 0.085, 4
        for i in range(steps):
            v0, v1 = base + (top - base) * i / steps, base + (top - base) * (i + 1) / steps
            w0, w1 = half * (1 - i / steps), max(half * (1 - (i + 1) / steps), 0.004)
            patch([(cu - w0, v0), (cu, v0), (cu, v1), (cu - w1, v1)])
            patch([(cu, v0), (cu + w0, v0), (cu + w1, v1), (cu, v1)])

    # Grin: a smiling band with teeth on both edges, offset so the edges zigzag; the corners close to points.
    n, tooth = 10, 0.035
    us = [-0.27 + 0.54 * i / n for i in range(n + 1)]
    top = [-0.045 + 1.15 * u * u - (tooth if i % 2 else 0) for i, u in enumerate(us)]
    bot = [-0.175 + 1.75 * u * u + (0 if i % 2 else tooth) for i, u in enumerate(us)]
    for j in (0, -1):
        top[j] = bot[j] = (top[j] + bot[j]) / 2
    for i in range(n):
        patch([(us[i], bot[i]), (us[i + 1], bot[i + 1]), (us[i + 1], top[i + 1]), (us[i], top[i])])

    # Stem: short, tapered and leaning, rooted in the top dimple.
    stem = [(0.075, 0.0), (0.068, 0.03), (0.055, 0.06), (0.05, 0.1), (0.047, 0.14), (0.05, 0.155), (0.0, 0.16)]
    st = k.lathe(stem, at=(0, 0, prof[-1][1] - 0.03), rot=(0, 0, 0), m=green, verts=12)
    k.warp(st, lambda p: (p[0] + 2.2 * p[2] ** 2, p[1], p[2]))

    # Wooden table top: planks running across, top at z = 0, dark wood showing in the gaps.
    wood = [k.mat("#b8743a", "matte"), k.mat("#c98544", "matte")]
    for j in range(-6, 9):
        k.box((6, 0.27, 0.08), at=(0, j * 0.28, -0.04), m=wood[j % 2], bevel=0.012, setting=True)
    k.box((6, 4.4, 0.06), at=(0, 0.28, -0.07), m=k.mat("#5a3218", "matte"), bevel=0, setting=True)
