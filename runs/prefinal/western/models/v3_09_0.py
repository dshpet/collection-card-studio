# Farm windmill: a two-tier stone plinth carries four wooden legs that taper up into a lattice tower, tied by
# horizontal girts and X braces. A platform caps the tower; a turntable on it carries the gearbox head. The
# axle runs forward from the head to the hub of the bladed wheel; the blades span an inner and an outer rim.
# The tail boom runs back from the head to the red vane. The tower stands on a dirt patch in dry grass.
import math

SCENE = {"category": "4", "backdrop": "#4fb3f2", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def leg_at(sx, sy, z):
    # Leg position at height z: from half-width 0.2 at z=0.16 to 0.07 at z=1.0.
    h = 0.2 - 0.13 * (z - 0.16) / 0.84
    return (sx * h, sy * h, z)


def build(k):
    wood = k.mat("#8a5a32", "matte")
    brace = k.mat("#7a4e2a", "matte")
    stone = k.mat("#9a968e", "matte")
    stone2 = k.mat("#b2ada3", "matte")
    steel = k.mat("#a7adb5", "metal")
    dark = k.mat("#5d636b", "metal")
    red = k.mat("#d8322b", "satin")

    # Stone plinth
    k.box((0.62, 0.62, 0.08), at=(0, 0, 0.04), m=stone, bevel=0.02)
    k.box((0.52, 0.52, 0.08), at=(0, 0, 0.12), m=stone2, bevel=0.02)

    # Four legs
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    for sx, sy in corners:
        k.tube([leg_at(sx, sy, 0.16), leg_at(sx, sy, 1.0)], 0.024, wood)

    # Girts and X braces on each face
    levels = [0.16, 0.42, 0.68, 0.9]
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        for z in levels[1:]:
            k.tube([leg_at(*a, z), leg_at(*b, z)], 0.015, brace)
        for z0, z1 in zip(levels[:-1], levels[1:]):
            k.tube([leg_at(*a, z0), leg_at(*b, z1)], 0.013, brace)
            k.tube([leg_at(*b, z0), leg_at(*a, z1)], 0.013, brace)

    # Platform, turntable, gearbox head
    k.box((0.2, 0.2, 0.03), at=(0, 0, 1.015), m=wood, bevel=0.006)
    k.cyl(0.055, 0.04, at=(0, 0, 1.05), m=dark)
    k.box((0.1, 0.2, 0.09), at=(0, -0.02, 1.115), m=dark, bevel=0.015)

    # Axle and hub
    wc = (0.0, -0.19, 1.13)
    k.cyl(0.018, 0.08, at=(0, -0.15, wc[2]), rot=(90, 0, 0), m=steel)
    k.cyl(0.055, 0.06, at=wc, rot=(90, 0, 0), m=dark, bevel=0.01)
    k.sphere(0.035, at=(0, wc[1] - 0.03, wc[2]), m=dark)

    # Rims
    k.torus(0.34, 0.013, at=wc, rot=(90, 0, 0), m=steel)
    k.torus(0.13, 0.011, at=wc, rot=(90, 0, 0), m=steel)
    # Spokes from hub to outer rim
    for i in range(6):
        a = math.radians(i * 60 + 15)
        k.tube([(0.05 * math.sin(a), wc[1], wc[2] + 0.05 * math.cos(a)),
                (0.34 * math.sin(a), wc[1], wc[2] + 0.34 * math.cos(a))], 0.008, steel)

    # Blades, twisted, between the rims
    tw = math.radians(28)

    def twist(p):
        x, y, z = p
        return (x * math.cos(tw) - y * math.sin(tw), x * math.sin(tw) + y * math.cos(tw), z)

    n = 18
    for i in range(n):
        a = i * 360.0 / n
        r = 0.235
        ar = math.radians(a)
        blade = k.box((0.085, 0.01, 0.22), at=(r * math.sin(ar), wc[1], wc[2] + r * math.cos(ar)),
                      rot=(0, a, 0), m=steel, bevel=0.003)
        k.warp(blade, twist)

    # Tail boom and vane
    k.tube([(0, 0.07, 1.12), (0, 0.5, 1.15)], 0.014, dark)
    k.tube([(0, 0.07, 1.09), (0, 0.46, 1.07)], 0.01, dark)
    k.box((0.014, 0.3, 0.2), at=(0, 0.6, 1.14), m=red, bevel=0.006)

    # Setting: dirt patch in dry grass
    k.floor("#c2b45c", "matte")
    k.cyl(0.7, 0.01, at=(0, 0, 0.0), m=k.mat("#a8794a", "matte"), bevel=0.004, setting=True)
