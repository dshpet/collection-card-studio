# Cowboy hat: an oval brim, flat by the crown, curls up hard at both sides and dips a little at the front and
# back; a cream binding runs around its edge. The tall crown rises from the brim's center, tapers slightly and
# carries a center crease along its top with the front pinched in. A red band wraps the crown's base, sitting on
# the brim. It floats, tilted a little forward so the crease and the inside of the side curls show.
import math

SCENE = {"category": "1", "backdrop": "#3fb4ef", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}

OVAL = 1.12      # the brim and crown run longer front to back
R_BRIM = 0.5
R_FLAT = 0.24    # brim stays flat out to this radius


def brim_shape(p):
    x, y, z = p
    y *= OVAL
    s = max(0.0, (abs(x) - R_FLAT) / (R_BRIM - R_FLAT))
    lift = 0.17 * s * s
    dip = -0.04 * (y / (R_BRIM * OVAL)) ** 2 * (1 - s)
    return (x, y, z + lift + dip)


def crown_shape(p):
    x, y, z = p
    y *= OVAL
    t = min(1.0, max(0.0, (z - 0.2) / 0.13))
    if y < 0:  # front pinch
        x *= 1 - 0.3 * t * min(1.0, -y / 0.22)
    z -= 0.075 * t * math.exp(-(x / 0.075) ** 2)  # center crease along the top
    z -= 0.025 * t * max(0.0, -y / 0.22)  # front of the crown sits a little lower
    return (x, y, z)


def build(k):
    felt = k.mat("#b8804a", "matte")
    cream = k.mat("#f1e2c0", "matte")
    red = k.mat("#d23a2c", "matte")

    # brim: a thin disk with many rings so it curls smoothly
    top, bottom = [], []
    n = 24
    for i in range(n + 1):
        r = (R_BRIM - 0.01) * i / n
        bottom.append((r, -0.012))
        top.append((r, 0.012))
    profile = bottom + [(R_BRIM, 0.0)] + top[::-1]
    brim = k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=felt, verts=96)
    k.warp(brim, brim_shape)

    # cream binding around the brim edge
    edge = []
    for i in range(73):
        a = 2 * math.pi * i / 72
        edge.append(brim_shape((R_BRIM * math.cos(a), R_BRIM * math.sin(a), 0.0)))
    k.tube(edge, 0.014, cream, curved=True)

    # crown: tall, slightly tapered, closed and domed on top with dense rings for the crease
    crown_profile = [(0.0, 0.0), (0.2, 0.0), (0.199, 0.06), (0.196, 0.14), (0.192, 0.22), (0.188, 0.27),
                     (0.18, 0.3), (0.165, 0.318), (0.14, 0.328), (0.11, 0.333), (0.08, 0.336),
                     (0.05, 0.338), (0.025, 0.339), (0.0, 0.34)]
    crown = k.lathe(crown_profile, at=(0, 0, 0), rot=(0, 0, 0), m=felt, verts=96)
    k.warp(crown, crown_shape)

    # red hatband at the crown's base
    band_profile = [(0.19, 0.012), (0.209, 0.012), (0.21, 0.04), (0.208, 0.068), (0.19, 0.068)]
    band = k.lathe(band_profile, at=(0, 0, 0), rot=(0, 0, 0), m=red, verts=96)
    k.warp(band, lambda p: (p[0], p[1] * OVAL, p[2]))

    k.turn(10, -6, 0)
