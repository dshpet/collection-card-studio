# Two-slot toaster: a rounded silver body stands on four small feet. Two slots run along its top, and a golden
# toast slice stands in each, popped halfway out. Each slice is one bread outline (square lower body, domed crown)
# with a crust rim around the crumb. The lever rides in a vertical track on the right end face, with the red dial
# below it on the same face. It stands on a plain pink floor.
import math

SCENE = {"category": "2", "backdrop": "#f06aa8", "azimuth": 32, "elevation": 12, "lens": 60, "light": "left"}


def bread_outline(r0, half_w, dome, drop):
    # maps a cylinder rim (local xy circle of radius r0) onto a bread outline; local y becomes world up
    def fn(p):
        x, y, z = p
        rr = math.hypot(x, y) / r0
        a = math.atan2(y, x)
        c, s = math.cos(a), math.sin(a)
        if s >= 0:
            nx, ny = half_w * c, dome * s
        else:
            nx = half_w * math.copysign(abs(c) ** 0.3, c)
            ny = -drop * abs(s) ** 0.3
        return (nx * rr, ny * rr, z)
    return fn


def build(k):
    steel = k.mat("#d4d8de", "metal")
    dark = k.mat("#2b2d33", "satin")
    black = k.mat("#3a3c42", "satin")
    red = k.mat("#e3262f", "gloss")
    bread = k.mat("#f2c867", "matte")
    crust = k.mat("#c9862e", "matte")

    # body on feet
    w, d, h, base = 0.62, 0.34, 0.40, 0.03
    top = base + h
    k.box((w, d, h), at=(0, 0, base + h / 2), m=steel, bevel=0.08)
    for x in (-0.24, 0.24):
        for y in (-0.12, 0.12):
            k.cyl(0.03, base + 0.01, at=(x, y, (base + 0.01) / 2), m=black, bevel=0.006)

    # two slots along the top, each holding a popped-up toast slice
    cz = 0.53
    for y in (-0.075, 0.075):
        k.box((0.46, 0.06, 0.012), at=(0, y, top - 0.002), m=dark, bevel=0.004)
        outer = k.cyl(0.2, 0.036, at=(0, y, cz), rot=(90, 0, 0), m=crust, bevel=0.01, verts=96)
        k.warp(outer, bread_outline(0.2, 0.18, 0.115, 0.23))
        inner = k.cyl(0.2, 0.04, at=(0, y, cz), rot=(90, 0, 0), m=bread, bevel=0.008, verts=96)
        k.warp(inner, bread_outline(0.2, 0.158, 0.095, 0.21))

    # right end face: lever track and lever on a stem, dial with a grip ridge below
    face = w / 2
    k.box((0.012, 0.035, 0.24), at=(face + 0.002, 0, 0.29), m=dark, bevel=0.004)
    k.box((0.04, 0.02, 0.025), at=(face + 0.02, 0, 0.34), m=steel, bevel=0.005)
    k.box((0.06, 0.13, 0.045), at=(face + 0.065, 0, 0.34), m=black, bevel=0.015)
    k.cyl(0.06, 0.03, at=(face + 0.015, -0.08, 0.13), rot=(0, 90, 0), m=red, bevel=0.008)
    k.box((0.025, 0.018, 0.08), at=(face + 0.035, -0.08, 0.13), m=red, bevel=0.006)

    k.turn(0, 0, -8)
    k.box((6, 4, 0.12), at=(0, 0.8, -0.06), m=k.mat("#f78fc2", "matte"), bevel=0.01, setting=True)
