# Street lamp: a round stepped iron base stands on the cobblestone path, the slim post rises out of it to a
# flared collar that carries the lantern floor plate. The four-sided glass lantern widens upward between four
# corner bars, under a top plate and a pyramid roof with a ball finial. Small cobbles, at street-lamp scale,
# are set in staggered rows on a mortar bed. The bed beyond them is stone-colored, so the path runs on to the horizon.
import math

SCENE = {"category": "4", "backdrop": "#7a5cc4", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#1d1e22", "satin")
    glow = k.mat("#ffd23a", "glow")

    # Round stepped base
    k.lathe([(0, 0), (0.16, 0), (0.16, 0.035), (0.14, 0.05), (0.125, 0.09), (0.1, 0.13),
             (0.075, 0.16), (0.06, 0.2), (0.05, 0.225), (0.04, 0.24), (0, 0.24)], at=(0, 0, 0), m=iron)
    # Slim post with a decorative ring
    k.cyl(0.032, 0.54, at=(0, 0, 0.49), m=iron)
    k.torus(0.034, 0.012, at=(0, 0, 0.42), m=iron)
    # Collar flaring to the lantern floor
    k.lathe([(0.032, 0.74), (0.04, 0.75), (0.05, 0.77), (0.075, 0.79), (0.09, 0.8), (0, 0.8)],
            at=(0, 0, 0), m=iron)
    k.box((0.19, 0.19, 0.025), at=(0, 0, 0.81), m=iron, bevel=0.006)

    # Glowing glass lantern, widening upward
    z0, z1, rb, rt = 0.822, 1.02, 0.095, 0.125
    k.cone(rb, rt, z1 - z0, at=(0, 0, (z0 + z1) / 2), rot=(0, 0, 45), m=glow, verts=4)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        k.tube([(rb * math.cos(a), rb * math.sin(a), z0), (rt * math.cos(a), rt * math.sin(a), z1)], 0.012, iron)
    # Top plate, pyramid roof, finial
    k.box((0.25, 0.25, 0.025), at=(0, 0, 1.03), m=iron, bevel=0.006)
    k.cone(0.2, 0.025, 0.11, at=(0, 0, 1.097), rot=(0, 0, 45), m=iron, verts=4)
    k.cyl(0.02, 0.03, at=(0, 0, 1.165), m=iron)
    k.sphere(0.03, at=(0, 0, 1.2), m=iron)

    # Cobblestone path: small staggered stones on a mortar bed; the bed beyond is stone-colored to the horizon
    stone_a, stone_b = k.mat("#8d8794", "matte"), k.mat("#a39a8f", "matte")
    k.floor("#938c97", "matte", size=60)
    s = 0.12
    for row in range(-6, 41):
        y = row * s
        off = s / 2 if row % 2 else 0
        for col in range(-25, 26):
            x = col * s + off
            if math.hypot(x, y) < 0.18:
                continue  # the lamp base stands here
            k.box((0.105, 0.1, 0.035), at=(x, y, -0.005), rot=(0, 0, (row * 7 + col * 3) % 9 - 4),
                  m=stone_a if (row + col) % 3 else stone_b, bevel=0.018, setting=True)
