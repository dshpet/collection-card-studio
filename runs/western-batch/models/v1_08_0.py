# Farm windmill: a solid four-sided tower tapers from a wide footing on the prairie to a small cap platform.
# On the cap sits a head housing; an axle runs forward out of it to the hub of the wheel, whose spokes carry an
# inner and an outer rim, and eighteen white blades span between the two rims. A boom runs back from the housing
# to the red tail vane. As on the lighthouse card, the framing holds the wheel and the upper tower, so the lower
# tower runs off the bottom of the card down to the ground.
import math

SCENE = {"category": "4", "backdrop": "#3fb4f2", "azimuth": 28, "elevation": 9, "lens": 60, "light": "left"}

TOWER_H = 1.0


def width(z):
    return 0.40 - 0.24 * z / TOWER_H


def build(k):
    grey = k.mat("#9aa1a8", "satin")
    dark = k.mat("#5d646c", "satin")
    white = k.mat("#f7f7f2", "satin")
    red = k.mat("#e0302a", "satin")
    steel = k.mat("#8b9097", "metal")

    def tower_section(z0, z1):
        wb = width(z0)
        zc = (z0 + z1) / 2
        part = k.box((wb, wb, z1 - z0), at=(0, 0, zc), m=grey, bevel=0.012)

        def taper(p):
            f = width(zc + p[2]) / wb
            return (p[0] * f, p[1] * f, p[2])

        k.warp(part, taper)
        return part

    # Tower in two stacked sections: the lower one reaches the ground but is left out of the framing.
    k.unframed(tower_section(0.0, 0.45))
    tower_section(0.45, TOWER_H)
    # Cap platform and the head housing on it.
    k.box((0.24, 0.24, 0.04), at=(0, 0, TOWER_H + 0.02), m=dark, bevel=0.008)
    k.cyl(0.05, 0.06, at=(0, 0, TOWER_H + 0.07), m=dark)
    hz = TOWER_H + 0.14
    k.box((0.11, 0.22, 0.1), at=(0, 0.0, hz), m=dark, bevel=0.015)

    # Axle forward to the hub; the wheel faces -y.
    wy = -0.19
    k.cyl(0.025, 0.1, at=(0, -0.14, hz), rot=(90, 0, 0), m=steel)
    k.cyl(0.065, 0.06, at=(0, wy, hz), rot=(90, 0, 0), m=dark)
    k.sphere(0.04, at=(0, wy - 0.03, hz), scale=(1, 0.7, 1), m=dark)

    r_in, r_out = 0.14, 0.44
    for rr in (r_in, r_out):
        k.torus(rr, 0.016, at=(0, wy, hz), rot=(90, 0, 0), m=steel)
    for i in range(6):
        a = math.radians(i * 60 + 15)
        k.tube([(0.05 * math.sin(a), wy, hz + 0.05 * math.cos(a)),
                (r_out * math.sin(a), wy, hz + r_out * math.cos(a))], 0.013, steel)
    n = 18
    for i in range(n):
        ra = math.radians(i * 360 / n)
        mid = (r_in + r_out) / 2
        blade = k.box((0.075, 0.014, r_out - r_in + 0.02), at=(0, 0, 0), m=white, bevel=0.004)

        # Widen the blade toward the rim, give it a pitch, then place it radially in the wheel plane.
        def place(p, ra=ra, mid=mid):
            x, y, z = p
            x *= 1.0 + 0.6 * (z + 0.16) / 0.32 - 0.3
            pitch = math.radians(22)
            x, y = x * math.cos(pitch), y + x * math.sin(pitch)
            r = mid + z
            return (r * math.sin(ra) + x * math.cos(ra), wy + y, hz + r * math.cos(ra) - x * math.sin(ra))

        k.warp(blade, place)

    # Tail boom and vane behind the wheel.
    k.tube([(0, 0.1, hz), (0, 0.5, hz + 0.03)], 0.018, steel)
    k.tube([(0, 0.08, hz + 0.05), (0, 0.4, hz + 0.1)], 0.012, steel)
    vane = k.box((0.016, 0.3, 0.24), at=(0, 0.58, hz + 0.04), m=red, bevel=0.006)
    k.warp(vane, lambda p: (p[0], p[1], p[2] * (0.6 + 0.4 * (p[1] + 0.15) / 0.3)))

    # Dry prairie with golden grass, a soft hill far back.
    k.floor("#e2b64c", "matte")
    k.sphere(1.0, at=(-2.5, 7.0, -1.2), scale=(5, 1.6, 1.7), m=k.mat("#cfa040", "matte"), setting=True)
    k.sphere(1.0, at=(3.5, 8.5, -1.3), scale=(5, 1.6, 1.8), m=k.mat("#c39a3e", "matte"), setting=True)
