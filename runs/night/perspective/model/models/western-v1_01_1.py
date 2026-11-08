# Cowboy hat: an oval felt crown with a lengthwise crease on top and two pinches at the front sits on a wide
# oval brim whose sides curl up and whose front and back dip a little. A red band wraps the base of the crown,
# tied in a small knot with two short tails on the left side. It floats, tipped toward the camera so the
# crease and the brim's upper face both show, with no side roll so both sides of the brim curl up evenly.
import math

SCENE = {"category": "1", "backdrop": "#45b6f0", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}

OVAL = 1.15  # crown and brim are longer front to back (y) than side to side (x)


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def build(k):
    felt = k.mat("#8a5a32", "matte")
    band = k.mat("#c8302c", "matte")

    # Brim: a thin disc with many radial rings so it can curl.
    n, R, t = 24, 0.6, 0.026
    bottom = [(R * i / n, 0.0) for i in range(n + 1)]
    top = [(R * (n - i) / n, t) for i in range(n + 1)]
    brim = k.lathe(bottom + [(R + 0.012, t / 2)] + top, at=(0, 0, 0), m=felt, verts=96)

    def curl(p):
        x, y, z = p
        y *= OVAL
        side = clamp((abs(x) - 0.3) / 0.32)
        z += 0.2 * side ** 2
        z -= 0.035 * clamp((abs(y) - 0.35) / 0.35) ** 2 * (1 - side)
        return (x, y, z)

    k.warp(brim, curl)

    # Crown: rounded oval dome, sunk slightly into the brim, with a crease along the top and front pinches.
    profile = [(0.29, 0.0), (0.29, 0.06), (0.287, 0.14), (0.282, 0.22), (0.274, 0.29), (0.262, 0.34),
               (0.245, 0.38), (0.22, 0.405), (0.185, 0.42), (0.14, 0.428), (0.09, 0.432), (0.04, 0.434),
               (0.0, 0.434)]
    crown = k.lathe(profile, at=(0, 0, t - 0.005), m=felt, verts=96)

    def crease(p):
        x, y, z = p
        y *= OVAL
        high = clamp((z - 0.24) / 0.19)
        z -= 0.085 * math.exp(-(x / 0.085) ** 2) * high * (1 - 0.35 * clamp(abs(y) / 0.33))
        if y < 0:
            x *= 1 - 0.22 * high * clamp(-y / 0.33) ** 2
        return (x, y, z)

    k.warp(crown, crease)

    # Hat band around the base of the crown.
    ring = k.lathe([(0.0, 0.0), (0.298, 0.0), (0.302, 0.01), (0.302, 0.08), (0.296, 0.09), (0.0, 0.09)],
                   at=(0, 0, t + 0.012), m=band, verts=96)
    k.warp(ring, lambda p: (p[0], p[1] * OVAL, p[2]))
    # Knot on the left side, with two short tails hanging from it against the crown, above the brim.
    k.blob([(-0.305, 0.04, t + 0.057, 0.032, (0.6, 1.0, 1.0))], band)
    k.box((0.02, 0.045, 0.07), at=(-0.31, 0.07, t + 0.045), rot=(-20, 0, 0), m=band, bevel=0.006)
    k.box((0.02, 0.045, 0.065), at=(-0.31, 0.1, t + 0.05), rot=(-35, 0, 0), m=band, bevel=0.006)

    k.turn(16, 0, 0)
