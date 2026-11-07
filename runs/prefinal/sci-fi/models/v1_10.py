# Moon rover: a flat open chassis tub rides on four wheels, each held on a stub axle out of the chassis side,
# with a continuous fender arc over each wheel, held by a bracket from the chassis floor. Two seats sit side by
# side on pedestals on the floor, with a small console in front of them. A mast rises from the front panel and
# carries a small dish antenna on a joint at its top; an orange tool box with a handle sits on the rear deck. It
# stands on pale grey moon dust, with a low crater rim behind it. Front faces -y.
import math

SCENE = {"category": "4", "backdrop": "#6a4fc9", "azimuth": 35, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    grey = k.mat("#8a8f98", "satin")
    dark = k.mat("#4b5058", "matte")
    steel = k.mat("#c3c8d0", "metal")
    orange = k.mat("#ff8a1f", "satin")
    seat = k.mat("#5d636c", "matte")

    wr, ww, wz = 0.14, 0.1, 0.14
    # Wheels, stub axles, suspension blocks, fenders and fender brackets.
    for sx in (-1, 1):
        for y in (-0.33, 0.33):
            x = sx * 0.39
            k.cyl(wr, ww, at=(x, y, wz), rot=(0, 90, 0), m=dark, bevel=0.02)
            k.cyl(0.075, ww + 0.012, at=(x, y, wz), rot=(0, 90, 0), m=grey, bevel=0.008)
            k.cyl(0.03, 0.03, at=(x + sx * 0.06, y, wz), rot=(0, 90, 0), m=steel)
            k.cyl(0.022, 0.1, at=(sx * 0.3, y, wz), rot=(0, 90, 0), m=steel)
            k.box((0.06, 0.06, 0.08), at=(sx * 0.28, y, 0.19), m=grey, bevel=0.008)
            rr = wr + 0.035
            n = 7
            for i in range(n):
                a = math.radians(-75 + (i + 0.5) * 150 / n)
                k.box((ww + 0.04, 0.072, 0.016),
                      at=(x, y + rr * math.sin(a), wz + rr * math.cos(a)),
                      rot=(-math.degrees(a), 0, 0), m=white, bevel=0.005)
            k.box((0.06, 0.05, 0.11), at=(sx * 0.32, y, 0.275), m=grey, bevel=0.008)

    # Chassis tub: floor plate, front and rear panels, side rails between the wheels.
    k.box((0.6, 1.0, 0.05), at=(0, 0, 0.215), m=white, bevel=0.012)
    k.box((0.6, 0.04, 0.13), at=(0, -0.48, 0.3), m=white, bevel=0.01)
    k.box((0.6, 0.04, 0.08), at=(0, 0.48, 0.275), m=white, bevel=0.01)
    for sx in (-1, 1):
        k.box((0.035, 0.32, 0.11), at=(sx * 0.285, 0, 0.295), m=white, bevel=0.01)

    # Two seats on pedestals.
    for sx in (-1, 1):
        x = sx * 0.13
        k.box((0.14, 0.14, 0.06), at=(x, 0.06, 0.27), m=grey, bevel=0.01)
        k.box((0.2, 0.2, 0.04), at=(x, 0.05, 0.32), m=seat, bevel=0.012)
        k.box((0.2, 0.04, 0.24), at=(x, 0.16, 0.44), rot=(-10, 0, 0), m=seat, bevel=0.012)
        k.box((0.03, 0.03, 0.1), at=(x, 0.17, 0.29), m=grey, bevel=0.005)

    # Console in front of the seats.
    k.box((0.2, 0.08, 0.16), at=(0, -0.26, 0.32), m=grey, bevel=0.01)
    k.box((0.22, 0.12, 0.025), at=(0, -0.27, 0.41), rot=(18, 0, 0), m=white, bevel=0.006)

    # Mast clamped to the front panel, dish on a joint at the top, facing forward and up.
    k.cyl(0.035, 0.05, at=(0.18, -0.48, 0.38), m=grey)
    k.cyl(0.013, 0.42, at=(0.18, -0.48, 0.6), m=steel)
    k.sphere(0.025, at=(0.18, -0.48, 0.815), m=grey)
    tilt = 55
    ax = (0, -math.sin(math.radians(tilt)), math.cos(math.radians(tilt)))
    base = (0.18, -0.48 + 0.02 * ax[1], 0.815 + 0.02 * ax[2])
    k.lathe([(0, 0), (0.04, 0.005), (0.08, 0.02), (0.12, 0.048), (0.117, 0.056), (0.08, 0.03),
             (0.04, 0.015), (0, 0.01)], at=base, rot=(tilt, 0, 0), m=white)
    tip = tuple(base[i] + 0.1 * ax[i] for i in range(3))
    k.tube([base, tip], 0.007, steel)
    k.sphere(0.013, at=tip, m=grey)

    # Orange tool box with a lid and handle on the rear deck.
    k.box((0.32, 0.15, 0.14), at=(0, 0.39, 0.31), m=orange, bevel=0.012)
    k.box((0.33, 0.16, 0.02), at=(0, 0.39, 0.385), m=orange, bevel=0.006)
    k.tube([(-0.07, 0.39, 0.395), (-0.07, 0.39, 0.43), (0.07, 0.39, 0.43), (0.07, 0.39, 0.395)], 0.01, dark)

    # Moon dust ground and a low crater rim behind the rover.
    k.floor("#a9abb2", "matte")
    k.lathe([(1.6, 0), (2.0, 0.18), (2.3, 0.25), (2.7, 0.1), (3.0, 0)], at=(1.5, 4.5, 0),
            m=k.mat("#9c9ea6", "matte"), setting=True)
