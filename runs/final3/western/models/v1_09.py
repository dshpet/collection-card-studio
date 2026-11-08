# Farm windmill: a tall four-sided tower with solid walls tapers from a wide base on the prairie to a narrow
# top. On top, a turntable carries the gear head; a horizontal axle runs forward from the head to the hub of the
# wheel. Many pitched blades run between an inner and an outer ring around the hub. Behind the head, a long boom
# with a brace carries the flat tail vane, which shows clear of the wheel from the three-quarter view. The framing
# holds the wheel and the upper half of the tower, so the lower tower runs off the bottom of the card toward the grass.
import math

SCENE = {"category": "4", "backdrop": "#4fb4f2", "azimuth": 40, "elevation": 8, "lens": 60, "light": "left"}

H = 1.6                     # tower height
W0, W1 = 0.25, 0.11         # half-width at base and top


def half_width(z):
    return W0 - (W0 - W1) * z / H


def build(k):
    tower = k.mat("#8e3b24", "satin")
    trim = k.mat("#6b2a18", "satin")
    blade = k.mat("#f6f4ee", "satin")
    vane = k.mat("#f2c12e", "satin")
    steel = k.mat("#5d6168", "metal")

    # Tapering tower: unit boxes warped so each side follows the taper line.
    def section(z0, z1, m, grow=0.0):
        cz = (z0 + z1) / 2
        part = k.box((1, 1, z1 - z0), at=(0, 0, cz), m=m, bevel=0.004)
        k.warp(part, lambda p: (p[0] * 2 * (half_width(cz + p[2]) + grow),
                                p[1] * 2 * (half_width(cz + p[2]) + grow), p[2]))
        return part

    k.unframed(section(0.0, 0.75, tower))
    section(0.75, 1.15, tower)
    section(1.15, H, tower)
    k.unframed(section(0.43, 0.47, trim, grow=0.012))
    section(0.83, 0.87, trim, grow=0.012)
    section(1.13, 1.17, trim, grow=0.012)
    k.box((2 * W1 + 0.05, 2 * W1 + 0.05, 0.04), at=(0, 0, H + 0.02), m=trim, bevel=0.008)

    # Turntable and gear head.
    k.cyl(0.075, 0.05, at=(0, 0, H + 0.065), m=steel)
    k.box((0.13, 0.22, 0.11), at=(0, 0.0, H + 0.145), m=k.mat("#b8432a", "satin"), bevel=0.02)

    # Axle and hub; the wheel stands in front of the tower, facing -y.
    wc = (0.0, -0.24, H + 0.145)
    k.cyl(0.022, 0.16, at=(0, -0.17, wc[2]), rot=(90, 0, 0), m=steel)
    k.cyl(0.06, 0.07, at=wc, rot=(90, 0, 0), m=steel)
    k.sphere(0.045, at=(wc[0], wc[1] - 0.04, wc[2]), scale=(1, 0.7, 1), m=steel)

    # Wheel: inner and outer rings, many pitched blades between them.
    R_in, R_out = 0.12, 0.42
    k.torus(R_in, 0.012, at=wc, rot=(90, 0, 0), m=blade)
    k.torus(R_out, 0.014, at=wc, rot=(90, 0, 0), m=blade)
    k.torus((R_in + R_out) / 2, 0.009, at=(wc[0], wc[1] + 0.01, wc[2]), rot=(90, 0, 0), m=blade)
    n = 18
    r_mid, length = (R_in + R_out) / 2, R_out - R_in + 0.02
    for i in range(n):
        a = 360 * i / n
        t = math.radians(a)
        at = (wc[0] + r_mid * math.cos(t), wc[1], wc[2] - r_mid * math.sin(t))
        k.box((length, 0.008, 0.085), at=at, rot=(28, a, 0), m=blade, bevel=0.003)
    # Spokes from the hub to the inner ring.
    for i in range(6):
        t = math.radians(60 * i + 15)
        k.tube([(wc[0] + 0.05 * math.cos(t), wc[1], wc[2] + 0.05 * math.sin(t)),
                (wc[0] + R_in * math.cos(t), wc[1], wc[2] + R_in * math.sin(t))], 0.01, steel)

    # Tail: long boom and brace from the head back to the vane, which sits well behind the wheel.
    k.tube([(0, 0.10, H + 0.16), (0, 0.92, H + 0.21)], 0.016, steel)
    k.tube([(0, 0.08, H + 0.10), (0, 0.90, H + 0.07)], 0.012, steel)
    k.box((0.014, 0.50, 0.30), at=(0, 1.14, H + 0.15), m=vane, bevel=0.006)

    # Dry prairie with golden grass, running to the horizon.
    k.floor("#e8c45a", "matte")
