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

    # Crown: a dense, smooth profile (straight slightly tapered sides, then a squarish rounded top that is
    # evenly sampled to the center) so the crease warp stays smooth.
    profile = []
    for i in range(12):
        f = i / 11
        profile.append((0.29 - 0.015 * f, 0.30 * f))
    for i in range(1, 29):
        a = (math.pi / 2) * i / 28
        c, s = math.cos(a), math.sin(a)
        profile.append((0.275 * c ** 0.6, 0.30 + 0.13 * s ** 0.6))
    profile[-1] = (0.0, 0.43)
    crown = k.lathe(profile, at=(0, 0, t - 0.005), m=felt, verts=128)

    def crease(p):
        x, y, z = p
        y *= OVAL
        high = clamp((z - 0.25) / 0.18)
        # Lengthwise groove down the middle of the top, shallower toward the back.
        depth = 0.1 * (1 - 0.3 * clamp(y / 0.33))
        z -= depth * math.exp(-(x / 0.07) ** 2) * high
        # Front pinches: narrow the front of the crown near the top.
        if y < 0:
            x *= 1 - 0.24 * high * clamp(-y / 0.33) ** 2
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
