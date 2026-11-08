# Flashlight: one red lathed body, tail cap at the bottom, a straight barrel with raised grip rings, then a
# flared head. A silver bezel ring with an inner lip holds a lit lens set just below the lip, over a shallow
# silver reflector bowl. The yellow slide switch sits on smooth barrel above the grip. Built upright along z,
# then tilted so the head points up-left and the lens face turns toward the viewer. Light shafts are left to
# the image model.
import math

SCENE = {"category": "1", "backdrop": "#2fd3e6", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    red = k.mat("#c4161c", "satin")
    silver = k.mat("#d3d7de", "metal")
    yellow = k.mat("#ffd21f", "satin")
    glow = k.mat("#fff3a6", "glow")

    # Body: tail cap, barrel, flared head (radius, z), bottom to top.
    profile = [(0.0, 0.0), (0.07, 0.0), (0.09, 0.01), (0.1, 0.03), (0.1, 0.09), (0.092, 0.1),
               (0.088, 0.11), (0.088, 0.56)]
    for i in range(1, 13):
        t = i / 12
        s = 0.5 - 0.5 * math.cos(math.pi * t)
        profile.append((0.088 + 0.06 * s, 0.56 + 0.2 * t))
    profile += [(0.148, 0.86), (0.13, 0.86), (0.0, 0.86)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=red, verts=96)

    # Ridged grip: raised red rings around the barrel, ending below the switch.
    for i in range(8):
        k.torus(0.09, 0.011, at=(0, 0, 0.15 + i * 0.038), rot=(0, 0, 0), m=red)

    # Silver bezel ring around the head, with an inner lip that holds the lens.
    k.lathe([(0.12, 0.845), (0.158, 0.845), (0.162, 0.86), (0.162, 0.9), (0.155, 0.92),
             (0.112, 0.92), (0.112, 0.908), (0.12, 0.905)], at=(0, 0, 0), rot=(0, 0, 0), m=silver, verts=96)
    # Shallow silver reflector bowl resting on the head top, inside the bezel.
    k.lathe([(0.03, 0.862), (0.07, 0.868), (0.105, 0.88), (0.122, 0.892), (0.122, 0.896),
             (0.0, 0.896)], at=(0, 0, 0), rot=(0, 0, 0), m=silver, verts=96)
    # Lit lens: a pale glowing disc seated on the reflector, just under the bezel lip.
    k.cyl(0.118, 0.008, at=(0, 0, 0.901), rot=(0, 0, 0), m=glow, bevel=0.002)

    # Yellow slide switch on smooth barrel above the grip, facing the viewer after the tilt.
    a = math.radians(-35)
    d = (math.cos(a), math.sin(a))
    k.box((0.03, 0.06, 0.09), at=(0.088 * d[0], 0.088 * d[1], 0.5), rot=(0, 0, -35), m=red, bevel=0.012)
    k.box((0.03, 0.045, 0.055), at=(0.108 * d[0], 0.108 * d[1], 0.5), rot=(0, 0, -35), m=yellow, bevel=0.01)

    k.turn(50, -35, 0)
