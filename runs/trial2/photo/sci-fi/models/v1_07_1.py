# Moon rover: a boxy white body rides on a rocker-bogie on each side. The rocker pivots on a pin in the body side,
# runs back down to the rear wheel and forward to a bogie pivot; the bogie carries the middle and front wheels.
# Each of the six black wheels turns on a short axle stub from its leg. A mast at the front-left corner holds an
# orange dish facing forward and up; a tiny solar panel sits on a post on the rear deck, tilted toward the front so
# its cells face the camera. All six wheels rest on a slab of gray moon dust.
import math

SCENE = {"category": "3", "backdrop": "#9be03a", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f4f0", "satin")
    trim = k.mat("#c9ced6", "metal")
    tire = k.mat("#1d1f22", "matte")
    hub = k.mat("#8b8f96", "metal")
    orange = k.mat("#ff8a1f", "satin")
    cell = k.mat("#1f3f8a", "gloss")

    # Body: main box with a slightly smaller deck plate on top.
    k.box((0.50, 0.74, 0.24), at=(0, 0, 0.42), m=white, bevel=0.03)
    k.box((0.44, 0.66, 0.03), at=(0, 0, 0.555), m=trim, bevel=0.01)

    # Wheels and suspension, both sides.
    wr, ww, wz = 0.115, 0.10, 0.115
    leg_r = 0.022
    for s in (-1, 1):
        lx = s * 0.29  # plane of the suspension legs
        wx = s * 0.36  # wheel center
        for y in (-0.36, 0.0, 0.36):
            k.cyl(wr - 0.01, ww, at=(wx, y, wz), rot=(0, 90, 0), m=tire, bevel=0.02)
            for i in range(12):  # raised tread ribs around the tire
                a = math.radians(i * 30)
                k.box((ww * 0.9, 0.03, 0.02), at=(wx, y - (wr - 0.01) * math.sin(a), wz + (wr - 0.01) * math.cos(a)),
                      rot=(i * 30, 0, 0), m=tire, bevel=0.004)
            k.cyl(0.05, 0.02, at=(wx + s * 0.05, y, wz), rot=(0, 90, 0), m=hub, bevel=0.005)
            k.cyl(0.02, 0.08, at=(s * 0.30, y, wz), rot=(0, 90, 0), m=hub)  # axle stub into the wheel
        # Rocker: body pin -> rear wheel, and body pin -> bogie pivot.
        pin, bogie = (lx, 0.10, 0.37), (lx, -0.18, 0.25)
        k.cyl(0.035, 0.06, at=(s * 0.27, 0.10, 0.37), rot=(0, 90, 0), m=hub)
        k.tube([pin, (lx, 0.30, 0.28), (lx, 0.36, wz)], leg_r, trim)
        k.tube([pin, bogie], leg_r, trim)
        # Bogie: pivot -> middle and front wheels.
        k.cyl(0.03, 0.05, at=bogie, rot=(0, 90, 0), m=hub)
        k.tube([(lx, 0.0, wz), (lx, -0.06, 0.22), bogie, (lx, -0.30, 0.22), (lx, -0.36, wz)], leg_r, trim)

    # Mast and dish antenna at the front-left corner.
    k.cyl(0.035, 0.04, at=(-0.14, -0.24, 0.585), m=trim)
    k.cyl(0.022, 0.24, at=(-0.14, -0.24, 0.69), m=white)
    dish = [(0.0, 0.0), (0.04, 0.004), (0.08, 0.016), (0.11, 0.03), (0.13, 0.045),
            (0.125, 0.052), (0.10, 0.04), (0.07, 0.028), (0.035, 0.02), (0.0, 0.016)]
    k.lathe(dish, at=(-0.14, -0.25, 0.80), rot=(40, 0, 0), m=orange)
    k.tube([(-0.14, -0.25, 0.81), (-0.14, -0.31, 0.87)], 0.01, orange)  # feed arm
    k.sphere(0.02, at=(-0.14, -0.31, 0.87), m=orange)

    # Tiny solar panel on a post at the rear of the deck, tilted toward the front so the cells face the camera.
    k.cyl(0.02, 0.10, at=(0.08, 0.20, 0.62), m=trim)
    k.box((0.30, 0.22, 0.02), at=(0.08, 0.20, 0.68), rot=(20, 0, 0), m=white, bevel=0.006)
    k.box((0.27, 0.19, 0.012), at=(0.08, 0.196, 0.6913), rot=(20, 0, 0), m=cell, bevel=0.003)

    # Gray moon dust slab, top at z = 0, running off the card.
    k.box((5, 4, 0.12), at=(0, 0.6, -0.06), m=k.mat("#7e7e82", "matte"), bevel=0.02, setting=True)
