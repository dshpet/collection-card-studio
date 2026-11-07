# Crystal ball: a teal glass sphere sits in a gold cup whose beaded rim holds it. Three S-curved gold legs
# spring from under the cup, are braced by a ring, and end in curled scroll claws whose ball toes rest on a
# dark oak table. The legs are turned so all three feet show: one toward the front, one in profile, one behind.
# The mist is left to the image model; the glass is teal.
import math

SCENE = {"category": "3", "backdrop": "#f06aa8", "azimuth": 30, "elevation": 18, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e0a93a", "metal")
    glass = k.mat("#2fc4b8", "glass")
    oak = k.mat("#3a2112", "matte")

    # Ball: radius 0.32, resting on the cup rim (radius 0.24 at z 0.40).
    rb, rim_r, rim_z = 0.32, 0.24, 0.40
    cz = rim_z + math.sqrt(rb * rb - rim_r * rim_r)
    k.sphere(rb, at=(0, 0, cz), m=glass)

    # Cup: a shallow bowl under the ball, with a beaded rim and a knob below.
    cup = [(0.0, 0.20), (0.07, 0.20), (0.10, 0.23), (0.15, 0.28), (0.20, 0.33), (0.23, 0.37), (0.245, 0.40)]
    k.lathe(cup, at=(0, 0, 0), rot=(0, 0, 0), m=gold)
    k.torus(rim_r, 0.022, at=(0, 0, rim_z), rot=(0, 0, 0), m=gold)
    k.sphere(0.06, at=(0, 0, 0.19), m=gold)

    # Three legs, each an S-curve from under the cup down to a curled claw foot on the table.
    # Camera sits at -60 deg in xy; legs at -30, 90, 210 put them 30, 150 and 270 deg off the view line,
    # so every foot is visible and none is hidden behind the cup.
    path = [(0.12, 0.25), (0.22, 0.30), (0.29, 0.26), (0.30, 0.18), (0.29, 0.11), (0.32, 0.06),
            (0.38, 0.05), (0.43, 0.08), (0.44, 0.13), (0.41, 0.16), (0.38, 0.13)]
    for ang in (-30, 90, 210):
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        k.tube([(r * ca, r * sa, z) for r, z in path], 0.026, gold, curved=True)
        # Claw: a ball toe resting on the table with two small talons.
        k.sphere(0.05, at=(0.35 * ca, 0.35 * sa, 0.05), m=gold)
        for d in (-1, 1):
            t = a + d * 0.12
            k.sphere(0.024, at=(0.39 * math.cos(t), 0.39 * math.sin(t), 0.024), scale=(1, 1, 0.9), m=gold)

    # Brace ring tying the three legs together.
    k.torus(0.297, 0.016, at=(0, 0, 0.17), rot=(0, 0, 0), m=gold)

    # Dark oak table top, running off the card; top at z = 0.
    k.box((7, 5.5, 0.12), at=(0, -0.2, -0.06), m=oak, bevel=0.01, setting=True)
