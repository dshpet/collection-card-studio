# Cowboy hat: an oval brim, flat by the crown, curls up at both sides and dips a little at the front and back;
# a cream binding runs around its edge. The tall crown rises from the brim's center, tapers slightly and carries a
# center crease along its top with the front pinched in. A red band wraps the crown's base, sitting on the brim.
# It floats, tilted a little forward so the crease and the inside of both side curls show.
import math

SCENE = {"category": "1", "backdrop": "#3fb4ef", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}

OVAL = 1.12      # the brim and crown run longer front to back
R_BRIM = 0.43
R_FLAT = 0.22    # brim stays flat out to this radius


def brim_shape(p):
    x, y, z = p
    y *= OVAL
    s = max(0.0, (abs(x) - R_FLAT) / (R_BRIM - R_FLAT))
    lift = 0.12 * s ** 1.6
    dip = -0.05 * (y / (R_BRIM * OVAL)) ** 2 * (1 - s)
    return (x, y, z + lift + dip)


def crown_shape(p):
    x, y, z = p
    y *= OVAL
    t = min(1.0, max(0.0, (z - 0.26) / 0.16))
    if y < 0:  # front pinch
        x *= 1 - 0.35 * t * min(1.0, -y / 0.2)
    z -= 0.09 * t * math.exp(-(x / 0.07) ** 2)  # center crease along the top
    z -= 0.03 * t * max(0.0, -y / 0.2)  # front of the crown sits a little lower
    return (x, y, z)


def build(k):
    felt = k.mat("#b8804a", "matte")
    brim_felt = k.mat("#9c6638", "matte")  # darker so the lit top of the brim still reads tan brown
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
    brim = k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=brim_felt, verts=96)
    k.warp(brim, brim_shape)

    # cream binding around the brim edge
    edge = []
    for i in range(73):
        a = 2 * math.pi * i / 72
        edge.append(brim_shape((R_BRIM * math.cos(a), R_BRIM * math.sin(a), 0.0)))
    k.tube(edge, 0.013, cream, curved=True)

    # crown: tall, slightly tapered, closed and domed on top with dense rings for the crease
    crown_profile = [(0.0, 0.0), (0.19, 0.0), (0.189, 0.08), (0.185, 0.18), (0.18, 0.27), (0.176, 0.33),
                     (0.168, 0.37), (0.152, 0.392), (0.13, 0.404), (0.1, 0.41), (0.07, 0.414),
                     (0.045, 0.416), (0.022, 0.417), (0.0, 0.418)]
    crown = k.lathe(crown_profile, at=(0, 0, 0), rot=(0, 0, 0), m=felt, verts=96)
    k.warp(crown, crown_shape)

    # red hatband at the crown's base
    band_profile = [(0.18, 0.012), (0.199, 0.012), (0.2, 0.042), (0.198, 0.072), (0.18, 0.072)]
    band = k.lathe(band_profile, at=(0, 0, 0), rot=(0, 0, 0), m=red, verts=96)
    k.warp(band, lambda p: (p[0], p[1] * OVAL, p[2]))

    k.turn(12, -4, 0)
