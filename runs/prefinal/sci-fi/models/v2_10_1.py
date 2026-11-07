# Space capsule: a white conical crew module stands on a wide, slightly domed dark heat shield that clearly
# overhangs its base. The cone ends in a blunt rounded top with a low, wide docking hatch, not a bottle neck. One
# round yellow window sits on the sloping front face, set into a raised rim. It floats in open sky, tilted as if
# climbing, so the window shows along with a glimpse of the shield.
import math

SCENE = {"category": "1", "backdrop": "#4fb4ef", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    shield = k.mat("#4a2f22", "matte")
    trim = k.mat("#9aa0a8", "metal")
    glass = k.mat("#ffd23a", "glow")

    # Heat shield: a shallow dome under the base, a thick rim, wider than the cone.
    R = 0.58
    dish = [(0.0, 0.0)] + [(R * math.sin(math.radians(a)), 0.06 * (1 - math.cos(math.radians(a))))
                            for a in range(6, 91, 6)] + [(R, 0.13), (R - 0.02, 0.15), (0.0, 0.15)]
    k.lathe(dish, at=(0, 0, 0), rot=(0, 0, 0), m=shield)

    # Crew module: a cone from the shield up to a rounded, blunt top.
    rb, zb, rt, zt = 0.46, 0.15, 0.17, 0.74
    body = [(0.0, zb - 0.01), (rb, zb - 0.01), (rb + 0.005, zb + 0.02), (rt, zt)]
    for a in range(15, 91, 15):
        t = math.radians(a)
        body.append((rt - 0.05 * (1 - math.cos(t)) - 0.0 * a, zt + 0.05 * math.sin(t)))
    body.append((0.0, zt + 0.05))
    k.lathe(body, at=(0, 0, 0), rot=(0, 0, 0), m=white)

    # Low, wide docking hatch on the blunt top.
    k.cyl(0.10, 0.04, at=(0, 0, zt + 0.06), rot=(0, 0, 0), m=trim, bevel=0.01)

    # Window on the sloping front face, its axis along the cone's surface normal.
    half = math.atan2(rb - rt, zt - zb)
    tilt = 90 - math.degrees(half)
    z = 0.43
    r = rb - (rb - rt) * (z - zb) / (zt - zb)
    nx, nz = math.cos(half), math.sin(half)
    k.torus(0.085, 0.022, at=(0, -(r + 0.005 * nx), z + 0.005 * nz), rot=(tilt, 0, 0), m=trim)
    k.cyl(0.085, 0.03, at=(0, -(r - 0.005), z), rot=(tilt, 0, 0), m=glass, bevel=0.004)

    k.turn(-10, -18, 25)
