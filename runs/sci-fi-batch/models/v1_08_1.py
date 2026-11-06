# Moon rover: a boxy white body sits on two metal side rails; from each rail three short legs drop to the axle
# stubs of six round black wheels (three per side) standing on the dust. A short mast on the roof holds a small
# round yellow dish tilted up toward the front, with a feed spike at its center. The front faces -y. The setting
# is grey moon dust with a few clear craters (raised rims round darker floors) placed where the camera sees them,
# and low far hills under a cyan sky.
import math

SCENE = {"category": "4", "backdrop": "#38c8f2", "azimuth": 30, "elevation": 10, "lens": 55, "light": "left"}


def build(k):
    white = k.mat("#f4f5f2", "satin")
    trim = k.mat("#9aa1aa", "metal")
    tyre = k.mat("#1d1f23", "matte")
    hub = k.mat("#8d939b", "metal")
    yellow = k.mat("#ffd02a", "satin")

    # Body: a boxy shell with a slightly smaller raised deck, and a recessed panel in the nose.
    k.box((0.50, 0.70, 0.22), at=(0, 0, 0.31), m=white, bevel=0.03)
    k.box((0.42, 0.56, 0.05), at=(0, 0.03, 0.445), m=white, bevel=0.02)
    k.box((0.34, 0.02, 0.08), at=(0, -0.352, 0.34), m=k.mat("#2f3a46", "gloss"), bevel=0.01)

    # Running gear: a rail under each side of the body, a leg down to each wheel, an axle stub out to the hub.
    wr, ww = 0.12, 0.09
    for sx in (-1, 1):
        rail_x = sx * 0.24
        k.box((0.05, 0.74, 0.05), at=(rail_x, 0, 0.205), m=trim, bevel=0.01)
        for y in (-0.27, 0.0, 0.27):
            k.box((0.04, 0.04, 0.09), at=(rail_x, y, 0.16), m=trim, bevel=0.008)
            k.cyl(0.022, 0.09, at=(sx * 0.285, y, wr), rot=(0, 90, 0), m=trim)
            wx = sx * 0.33
            k.cyl(wr, ww, at=(wx, y, wr), rot=(0, 90, 0), m=tyre, bevel=0.025)
            k.cyl(0.055, ww + 0.012, at=(wx, y, wr), rot=(0, 90, 0), m=hub, bevel=0.01)

    # Mast on the roof, a ball joint, and the dish tilted 35 degrees toward the front.
    mast = (0.08, 0.14)
    k.cyl(0.022, 0.13, at=(mast[0], mast[1], 0.535), m=trim)
    k.sphere(0.035, at=(mast[0], mast[1], 0.60), m=trim)
    outer = [(0.13 * i / 10, 0.055 * (i / 10) ** 2) for i in range(11)]
    inner = [(0.12 * i / 10, 0.05 * (i / 10) ** 2 + 0.01) for i in range(10, -1, -1)]
    base = (mast[0], mast[1], 0.615)
    k.lathe(outer + [(0.13, 0.062)] + inner, at=base, rot=(35, 0, 0), m=yellow)
    a = math.radians(35)
    tip = (base[0], base[1] - 0.10 * math.sin(a), base[2] + 0.10 * math.cos(a))
    k.tube([base, tip], 0.008, trim)
    k.sphere(0.016, at=tip, m=yellow)

    # Setting: grey moon dust, craters with raised rims and darker floors in view of the camera, low far hills.
    dust = k.mat("#8f939a", "matte")
    pit = k.mat("#5f646c", "matte")
    k.floor("#8f939a", "matte", size=40)
    for cx, cy, s in ((-0.85, -0.45, 0.65), (0.75, -0.95, 0.5), (-1.0, 0.95, 1.0), (1.2, 1.1, 1.1),
                      (-2.4, 3.2, 1.6)):
        k.cyl(0.27 * s, 0.008, at=(cx, cy, 0.004), m=pit, bevel=0, setting=True)
        rim = [(0.24 * s, 0.0), (0.28 * s, 0.06 * s), (0.33 * s, 0.085 * s), (0.42 * s, 0.045 * s),
               (0.55 * s, 0.0)]
        k.lathe(rim, at=(cx, cy, 0), rot=(0, 0, 0), m=dust, setting=True)
    k.blob([(-4.0, 9.0, -0.3, 2.2, (1.8, 1.0, 0.5)), (2.5, 10.0, -0.4, 2.6, (2.0, 1.0, 0.45)),
            (7.0, 8.0, -0.3, 2.0, (1.6, 1.0, 0.5))], k.mat("#7d828a", "matte"), setting=True)
