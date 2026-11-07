# Covered wagon: a wooden box bed sits on two bolster blocks over the front and rear axles; each axle carries
# two spoked wooden wheels with red iron tyres (larger at the back, all touching the ground). The white canvas
# cover rises from the bed top as straight sides into a half-round arch, with bow ribs over it. The tongue runs
# from the front bolster down to rest on the packed-dirt ground and is left out of the framing.
import math

SCENE = {"category": "3", "backdrop": "#5cbf3a", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def wheel(k, x, y, R, wood, tyre, hub_m):
    k.torus(R - 0.022, 0.022, at=(x, y, R), rot=(90, 0, 0), m=tyre)
    k.torus(R - 0.06, 0.02, at=(x, y, R), rot=(90, 0, 0), m=wood)
    k.cyl(0.045, 0.09, at=(x, y, R), rot=(90, 0, 0), m=hub_m, bevel=0.01)
    n = 10 if R > 0.2 else 8
    L = R - 0.07
    for i in range(n):
        a = 360.0 * i / n
        ar = math.radians(a)
        cx = x + math.sin(ar) * (L / 2 + 0.02)
        cz = R + math.cos(ar) * (L / 2 + 0.02)
        k.box((0.02, 0.022, L), at=(cx, y, cz), rot=(0, a, 0), m=wood, bevel=0.004)


def build(k):
    wood = k.mat("#8a5a2e", "matte")
    dark = k.mat("#6b4222", "matte")
    tyre = k.mat("#c8302a", "satin")
    canvas = k.mat("#f6f2e6", "matte")

    rear_R, front_R = 0.24, 0.19
    rear_x, front_x = -0.32, 0.32
    wy = 0.31

    # axles
    k.cyl(0.025, 0.72, at=(rear_x, 0, rear_R), rot=(90, 0, 0), m=dark)
    k.cyl(0.025, 0.72, at=(front_x, 0, front_R), rot=(90, 0, 0), m=dark)
    # bolsters from axle up to bed bottom
    k.box((0.09, 0.5, 0.09), at=(rear_x, 0, 0.285), m=dark, bevel=0.01)
    k.box((0.09, 0.5, 0.14), at=(front_x, 0, 0.255), m=dark, bevel=0.01)

    for s in (-1, 1):
        wheel(k, rear_x, s * wy, rear_R, wood, tyre, dark)
        wheel(k, front_x, s * wy, front_R, wood, tyre, dark)

    # wooden bed
    k.box((1.0, 0.5, 0.16), at=(0, 0, 0.40), m=wood, bevel=0.015)
    k.box((1.02, 0.52, 0.025), at=(0, 0, 0.47), m=dark, bevel=0.008)
    for x in (-0.25, 0.0, 0.25):
        for s in (-1, 1):
            k.box((0.03, 0.02, 0.15), at=(x, s * 0.255, 0.40), m=dark, bevel=0.005)

    # canvas cover: straight sides then a half-round arch (box slightly shorter so end faces don't coincide)
    k.box((0.88, 0.48, 0.15), at=(0, 0, 0.555), m=canvas, bevel=0.02)
    k.cyl(0.24, 0.9, at=(0, 0, 0.63), rot=(0, 90, 0), m=canvas, bevel=0.02)
    # bow ribs pressing through the canvas
    for x in (-0.42, -0.14, 0.14, 0.42):
        pts = []
        for j in range(13):
            a = math.radians(-90 + j * 15)
            pts.append((x, 0.252 * math.sin(a), 0.63 + 0.252 * math.cos(a)))
        pts = [(x, -0.252, 0.49)] + pts + [(x, 0.252, 0.49)]
        k.tube(pts, 0.018, canvas, curved=True)

    # tongue from the front bolster down to the ground
    tongue = k.tube([(front_x + 0.04, 0, 0.22), (0.7, 0, 0.12), (1.12, 0, 0.025)], 0.026, wood)
    tip = k.cyl(0.014, 0.16, at=(1.08, 0, 0.03), rot=(90, 0, 0), m=dark)
    k.unframed(tongue, tip)

    # packed dirt ground, large enough to run off the card
    k.box((8, 8, 0.1), at=(0, 0.5, -0.05), m=k.mat("#b98a5a", "matte"), bevel=0.02, setting=True)
