# Garden bench: four square legs; the rear legs rise into tilted backrest uprights. Seat slats rest on side
# rails and front/back aprons. Vertical back slats stand between a low back rail and an arched top rail that
# spans the two uprights. Each armrest runs from the rear upright over the front leg's top and curls down into
# a scroll. The bench stands on a gravel path, with lawn around it.
import math

SCENE = {"category": "4", "backdrop": "#7cc8f2", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}

TILT = math.degrees(math.atan2(0.08, 0.53))


def back_y(z):
    return 0.21 + 0.08 * (z - 0.44) / 0.53


def top_z(x):
    return 0.86 + 0.12 * math.cos(math.pi * x / 1.24)


def build(k):
    white = k.mat("#f6f4ee", "satin")
    wood = k.mat("#a8683a", "matte")
    W = 0.6  # half width to leg centers

    for s in (-1, 1):
        x = s * W
        # front leg rises to carry the armrest
        k.box((0.06, 0.06, 0.62), at=(x, -0.2, 0.31), m=white)
        # rear leg and tilted upright
        k.box((0.06, 0.06, 0.46), at=(x, 0.21, 0.23), m=white)
        k.box((0.06, 0.06, 0.58), at=(x, 0.252, 0.72), rot=(-TILT, 0, 0), m=white)
        k.sphere(0.04, at=(x, 0.295, 1.0), m=white)
        # side seat rail and low stretcher
        k.box((0.05, 0.47, 0.07), at=(x, 0.005, 0.38), m=white)
        k.box((0.04, 0.41, 0.04), at=(x, 0.005, 0.1), m=white)
        # scrolled armrest: from the upright, over the front leg, curling down in front
        pts = [(x, back_y(0.66), 0.66), (x, 0.05, 0.655), (x, -0.2, 0.645), (x, -0.27, 0.635),
               (x, -0.315, 0.6), (x, -0.31, 0.55), (x, -0.27, 0.535), (x, -0.245, 0.565), (x, -0.265, 0.59)]
        k.tube(pts, 0.03, white, curved=True)

    # front and back aprons
    k.box((1.2, 0.04, 0.08), at=(0, -0.22, 0.37), m=white)
    k.box((1.2, 0.04, 0.08), at=(0, 0.22, 0.37), m=white)
    # seat slats, ending inside the outer faces of the frame
    for i in range(5):
        y = -0.19 + i * 0.095
        k.box((1.22, 0.08, 0.03), at=(0, y, 0.43), m=wood, bevel=0.008)

    # backrest: low rail, arched top rail, vertical slats
    k.box((1.2, 0.045, 0.06), at=(0, back_y(0.52), 0.52), rot=(-TILT, 0, 0), m=white)
    xs = [-W + i * (2 * W) / 16 for i in range(17)]
    rail = [(x, back_y(top_z(x)), top_z(x)) for x in xs]
    k.tube(rail, 0.035, white, curved=True)
    for i in range(9):
        x = -0.48 + i * 0.12
        z0, z1 = 0.55, top_z(x) - 0.02
        zc = (z0 + z1) / 2
        k.box((0.075, 0.022, z1 - z0), at=(x, back_y(zc), zc), rot=(-TILT, 0, 0), m=white, bevel=0.006)

    # setting: gravel path on a lawn
    k.box((7, 1.5, 0.04), at=(0, -0.05, -0.02), m=k.mat("#bfa984", "matte"), bevel=0.01, setting=True)
    k.floor("#5fb83c", "matte", z=-0.03)
