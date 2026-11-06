# Farm windmill: a solid four-sided tower tapers from a wide footing on the prairie to a small cap platform, with
# a band where the lower tower meets the upper. On the cap sits a head housing; an axle runs forward out of it to
# the hub of the wheel, whose spokes carry an inner and an outer rim, and eighteen white blades span between the
# two rims. A boom runs back from the housing to the red tail vane. The framing holds the wheel, the tail and the
# upper tower, so the lower tower runs off the bottom of the card down to the ground.
import math

SCENE = {"category": "4", "backdrop": "#3fb4f2", "azimuth": 38, "elevation": 10, "lens": 60, "light": "left"}

TOWER_H = 1.5
JOINT = 0.85


def width(z):
    return 0.42 - 0.30 * z / TOWER_H


def build(k):
    grey = k.mat("#9aa1a8", "satin")
    dark = k.mat("#5d646c", "satin")
    white = k.mat("#f7f7f2", "satin")
    red = k.mat("#e0302a", "satin")
    steel = k.mat("#8b9097", "metal")

    def tower_section(z0, z1):
        wb = width(z0)
        zc = (z0 + z1) / 2
        part = k.box((wb, wb, z1 - z0), at=(0, 0, zc), m=grey, bevel=0.01)

        def taper(p):
            f = width(zc + p[2]) / wb
            return (p[0] * f, p[1] * f, p[2])

        k.warp(part, taper)
        return part

    # One tapering tower; the lower part reaches the ground but is left out of the framing.
    k.unframed(tower_section(0.0, JOINT))
    tower_section(JOINT, TOWER_H)
    wj = width(JOINT) + 0.03
    k.box((wj, wj, 0.04), at=(0, 0, JOINT), m=dark, bevel=0.008)

    # Cap platform and the head housing on it.
    k.box((0.2, 0.2, 0.035), at=(0, 0, TOWER_H + 0.0175), m=dark, bevel=0.008)
    k.cyl(0.04, 0.05, at=(0, 0, TOWER_H + 0.06), m=dark)
    hz = TOWER_H + 0.12
    k.box((0.09, 0.2, 0.08), at=(0, 0.0, hz), m=dark, bevel=0.012)

    # Axle forward to the hub; the wheel faces -y.
    wy = -0.17
    k.cyl(0.02, 0.09, at=(0, -0.13, hz), rot=(90, 0, 0), m=steel)
    k.cyl(0.05, 0.05, at=(0, wy, hz), rot=(90, 0, 0), m=dark)
    k.sphere(0.032, at=(0, wy - 0.025, hz), scale=(1, 0.7, 1), m=dark)

    r_in, r_out = 0.11, 0.34
    for rr in (r_in, r_out):
        k.torus(rr, 0.013, at=(0, wy, hz), rot=(90, 0, 0), m=steel)
    for i in range(6):
        a = math.radians(i * 60 + 15)
        k.tube([(0.04 * math.sin(a), wy, hz + 0.04 * math.cos(a)),
                (r_out * math.sin(a), wy, hz + r_out * math.cos(a))], 0.01, steel)
    n = 18
    L = r_out - r_in + 0.02
    mid = (r_in + r_out) / 2
    for i in range(n):
        ra = math.radians(i * 360 / n)
        blade = k.box((0.058, 0.011, L), at=(0, 0, 0), m=white, bevel=0.003)

        # Widen the blade toward the rim, give it a pitch, then place it radially in the wheel plane.
        def place(p, ra=ra):
            x, y, z = p
            x *= 0.7 + 0.6 * (z + L / 2) / L
            pitch = math.radians(22)
            x, y = x * math.cos(pitch), y + x * math.sin(pitch)
            r = mid + z
            return (r * math.sin(ra) + x * math.cos(ra), wy + y, hz + r * math.cos(ra) - x * math.sin(ra))

        k.warp(blade, place)

    # Tail boom and vane behind the wheel.
    k.tube([(0, 0.09, hz), (0, 0.5, hz + 0.02)], 0.014, steel)
    k.tube([(0, 0.07, hz + 0.04), (0, 0.42, hz + 0.08)], 0.01, steel)
    vane = k.box((0.014, 0.28, 0.2), at=(0, 0.6, hz + 0.03), m=red, bevel=0.005)
    k.warp(vane, lambda p: (p[0], p[1], p[2] * (0.6 + 0.4 * (p[1] + 0.14) / 0.28)))

    # Dry prairie with golden grass, soft hills far back.
    k.floor("#e2b64c", "matte")
    k.sphere(1.0, at=(-2.5, 7.0, -1.2), scale=(5, 1.6, 1.7), m=k.mat("#cfa040", "matte"), setting=True)
    k.sphere(1.0, at=(3.5, 8.5, -1.3), scale=(5, 1.6, 1.8), m=k.mat("#c39a3e", "matte"), setting=True)
