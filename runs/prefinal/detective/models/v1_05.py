# Steel safe: a square steel body stands on four short feet at its corners. The closed front door sits a little
# proud of the body's front face and turns on two thick hinge barrels on the left, each barrel bridging the body's
# edge and the door. The gold combination dial is centred on the door on a short spindle, and the gold grip handle
# stands off the door's right side on two posts. A plain pink floor runs off the card under it.
import math

SCENE = {"category": "2", "backdrop": "#d8317a", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    steel = k.mat("#565b64", "metal")
    door_steel = k.mat("#646a73", "metal")
    dark = k.mat("#2e3136", "satin")
    gold = k.mat("#f2c23a", "metal")

    # Body and feet
    w, d, h, foot = 0.80, 0.72, 0.84, 0.06
    k.box((w, d, h), at=(0, 0, foot + h / 2), m=steel, bevel=0.035)
    for x in (-0.31, 0.31):
        for y in (-0.27, 0.27):
            k.cyl(0.055, foot + 0.01, at=(x, y, (foot + 0.01) / 2), m=dark, bevel=0.01)

    # Door, slightly proud of the front face (front face at y = -0.36)
    front = -d / 2
    dz = foot + h / 2
    dw, dh, dt = 0.64, 0.68, 0.04
    k.box((dw, dt, dh), at=(0.02, front - dt / 2 + 0.01, dz), m=door_steel, bevel=0.015)
    door_face = front - dt + 0.01

    # Thick hinges on the left: barrels bridging body edge and door edge
    for z in (dz - 0.22, dz + 0.22):
        k.cyl(0.04, 0.14, at=(-0.315, front - 0.025, z), m=dark, bevel=0.008)
        k.cyl(0.046, 0.02, at=(-0.315, front - 0.025, z + 0.08), m=dark, bevel=0.005)
        k.cyl(0.046, 0.02, at=(-0.315, front - 0.025, z - 0.08), m=dark, bevel=0.005)

    # Round gold dial in the centre: spindle, dial disc, raised rim, centre knob
    cx, cz = 0.0, dz + 0.04
    k.cyl(0.03, 0.03, at=(cx, door_face - 0.012, cz), rot=(90, 0, 0), m=dark)
    k.cyl(0.115, 0.03, at=(cx, door_face - 0.035, cz), rot=(90, 0, 0), m=gold, bevel=0.008)
    k.torus(0.112, 0.014, at=(cx, door_face - 0.05, cz), rot=(90, 0, 0), m=gold)
    k.cyl(0.045, 0.04, at=(cx, door_face - 0.07, cz), rot=(90, 0, 0), m=gold, bevel=0.01)
    # Raised grip ridges around the dial face
    for i in range(12):
        a = math.radians(i * 30)
        k.box((0.012, 0.03, 0.012), at=(cx + 0.09 * math.cos(a), door_face - 0.055, cz + 0.09 * math.sin(a)),
              rot=(0, -i * 30, 0), m=gold, bevel=0.003)

    # Gold grip handle on the right, standing off the door on two posts
    hx, z0, z1 = 0.25, dz - 0.15, dz + 0.15
    for z in (z0, z1):
        k.cyl(0.03, 0.012, at=(hx, door_face - 0.006, z), rot=(90, 0, 0), m=gold, bevel=0.003)
    k.tube([(hx, door_face, z0), (hx, door_face - 0.08, z0 + 0.02), (hx, door_face - 0.08, z1 - 0.02),
            (hx, door_face, z1)], 0.022, gold)

    # Plain floor, a shade lighter than the backdrop
    k.box((6, 4, 0.12), at=(0, 0.6, -0.06), m=k.mat("#ec6aa4", "satin"), bevel=0.01, setting=True)
