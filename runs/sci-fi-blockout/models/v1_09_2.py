# Radio dish: a concrete pad carries a tall tapered gray pedestal; a turntable on top holds a two-arm yoke, and
# the dish turns on a horizontal axle through the yoke arms, tilted up to the sky. A hub joins the axle to the back
# of the dish shell. Three struts rise from the rim to the feed at the focus, with the small red light on top.
# The hero is turned so the dish faces up and to the side, showing the bowl's depth and rim rather than a flat disc.
# The setting is a flat sunny desert with a few low dunes and a mesa far back.
import math

SCENE = {"category": "4", "backdrop": "#5cc4f2", "azimuth": 25, "elevation": 10, "lens": 55, "light": "left"}


def build(k):
    white = k.mat("#f4f6f8", "satin")
    gray = k.mat("#7f868f", "satin")
    dark = k.mat("#565c64", "satin")
    strut = k.mat("#8a9099", "metal")
    red = k.mat("#ff3b30", "glow")

    # Pad, tall pedestal, turntable
    k.box((0.6, 0.6, 0.04), at=(0, 0, 0.02), m=k.mat("#a9a398", "matte"), bevel=0.008)
    k.lathe([(0.0, 0.04), (0.19, 0.04), (0.18, 0.14), (0.13, 0.50), (0.115, 0.70), (0.0, 0.70)],
            at=(0, 0, 0), rot=(0, 0, 0), m=gray)
    k.cyl(0.15, 0.05, at=(0, 0, 0.725), rot=(0, 0, 0), m=dark, bevel=0.008)

    # Yoke rising from the turntable, and the elevation axle through both arms
    pivot = (0.0, 0.0, 0.98)
    for side in (-1, 1):
        k.box((0.05, 0.14, 0.28), at=(side * 0.17, 0, 0.89), rot=(0, 0, 0), m=gray, bevel=0.01)
    k.box((0.39, 0.14, 0.04), at=(0, 0, 0.77), rot=(0, 0, 0), m=gray, bevel=0.008)
    k.cyl(0.035, 0.42, at=pivot, rot=(0, 90, 0), m=dark)

    # Dish frame: local +z is the dish axis, tilted 35 degrees from vertical toward -y, i.e. 55 degrees up
    tilt_deg = 35
    tilt = math.radians(tilt_deg)
    axis = (0.0, -math.sin(tilt), math.cos(tilt))

    def world(p, origin):
        x, y, z = p
        return (origin[0] + x,
                origin[1] + y * math.cos(tilt) - z * math.sin(tilt),
                origin[2] + y * math.sin(tilt) + z * math.cos(tilt))

    # Hub from the axle to the dish back
    hub_at = tuple(pivot[i] + axis[i] * 0.05 for i in range(3))
    k.cyl(0.07, 0.1, at=hub_at, rot=(tilt_deg, 0, 0), m=gray, bevel=0.008)

    # Parabolic shell: back surface outward, rim lip, front surface back to the center
    d = 0.11
    dish_at = tuple(pivot[i] + axis[i] * d for i in range(3))
    R, c, t = 0.4, 1.333, 0.03
    back = [(R * i / 16, (R * i / 16) ** 2 / c - t) for i in range(17)]
    front = [(R * i / 16, (R * i / 16) ** 2 / c) for i in range(16, -1, -1)]
    k.lathe(back + [(R + 0.012, R * R / c - 0.01), (R + 0.012, R * R / c + 0.004)] + front,
            at=dish_at, rot=(tilt_deg, 0, 0), m=white)

    # Feed struts standing off the shell to the feed horn at the focus
    focus = (0.0, 0.0, 0.36)
    for deg in (90, 210, 330):
        a = math.radians(deg)
        rim = (0.37 * math.cos(a), 0.37 * math.sin(a), 0.37 ** 2 / c + 0.01)
        k.sphere(0.022, at=world(rim, dish_at), m=strut)
        k.tube([world(rim, dish_at), world(focus, dish_at)], 0.016, strut)
    k.cone(0.035, 0.05, 0.08, at=world((0, 0, 0.37), dish_at), rot=(tilt_deg, 0, 0), m=gray)
    k.cyl(0.05, 0.02, at=world((0, 0, 0.42), dish_at), rot=(tilt_deg, 0, 0), m=dark)
    k.sphere(0.022, at=world((0, 0, 0.44), dish_at), m=red)

    # Face the dish up and to the left so its bowl reads in depth from the camera
    k.turn(0, 0, -55)

    # Desert plain, low dunes and a far mesa
    k.floor("#efc07a", "matte", size=60)
    k.blob([(-4.5, 9, 0, 1.6, (2.6, 1.0, 0.35)), (-2.0, 9.5, 0, 1.4, (2.2, 1.0, 0.3))],
           k.mat("#e7b06a", "matte"), setting=True)
    k.blob([(3.5, 8, 0, 1.5, (2.4, 1.0, 0.3))], k.mat("#e7b06a", "matte"), setting=True)
    k.box((3.0, 1.6, 0.9), at=(6.5, 14, 0.45), rot=(0, 0, 8), m=k.mat("#d48a55", "matte"),
          bevel=0.15, setting=True)
