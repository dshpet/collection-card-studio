# Flashlight: one red lathed body, tail cap at the bottom, a straight barrel with raised grip rings, then a
# flared head. A silver bezel ring holds the glass lens over a glowing reflector disc. The yellow slide
# switch sits on the barrel above the grip. Built upright along z, then tilted so the lens points up-left
# toward the viewer, like the bugle card. The light shafts are left to the image model.
import math

SCENE = {"category": "1", "backdrop": "#2fd3e6", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    red = k.mat("#c4161c", "satin")
    silver = k.mat("#d3d7de", "metal")
    yellow = k.mat("#ffd21f", "satin")
    glass = k.mat("#e8f6ff", "glass")
    glow = k.mat("#fff2a0", "glow")

    # Body: tail cap, barrel, flared head (radius, z), bottom to top.
    profile = [(0.0, 0.0), (0.07, 0.0), (0.09, 0.01), (0.1, 0.03), (0.1, 0.09), (0.092, 0.1),
               (0.088, 0.11), (0.088, 0.56)]
    for i in range(1, 13):
        t = i / 12
        s = 0.5 - 0.5 * math.cos(math.pi * t)
        profile.append((0.088 + 0.06 * s, 0.56 + 0.2 * t))
    profile += [(0.148, 0.86), (0.13, 0.86), (0.0, 0.86)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=red, verts=96)

    # Ridged grip: raised red rings around the barrel.
    for i in range(9):
        k.torus(0.09, 0.011, at=(0, 0, 0.15 + i * 0.038), rot=(0, 0, 0), m=red)

    # Silver bezel ring around the head, holding the lens.
    k.lathe([(0.13, 0.845), (0.158, 0.845), (0.162, 0.86), (0.162, 0.9), (0.155, 0.915),
             (0.13, 0.915)], at=(0, 0, 0), rot=(0, 0, 0), m=silver, verts=96)
    k.cyl(0.128, 0.006, at=(0, 0, 0.87), rot=(0, 0, 0), m=glow, bevel=0.001)
    k.cyl(0.132, 0.02, at=(0, 0, 0.9), rot=(0, 0, 0), m=glass, bevel=0.004)

    # Yellow slide switch on the barrel, facing up and toward the viewer after the tilt.
    a = math.radians(-35)
    d = (math.cos(a), math.sin(a))
    k.box((0.03, 0.06, 0.1), at=(0.088 * d[0], 0.088 * d[1], 0.5), rot=(0, 0, -35), m=red, bevel=0.012)
    k.box((0.03, 0.045, 0.06), at=(0.108 * d[0], 0.108 * d[1], 0.5), rot=(0, 0, -35), m=yellow, bevel=0.01)

    k.turn(18, -55, 0)
