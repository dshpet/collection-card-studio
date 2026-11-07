# Airlock hatch: a round grey door sits in a bolted round flange set into a paneled space-station wall. Two hinges
# on the left join the door to the flange: an arm from the door face to a vertical barrel on a block bolted to the
# flange. A spoked orange wheel turns on a hub in the door's center, and a small round window with a rim sits
# above it (the stars beyond are left to the image model). The deck floor runs under the wall.
import math

SCENE = {"category": "4", "backdrop": "#3fd0e8", "azimuth": 15, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    door = k.mat("#9aa3ad", "metal")
    flange_m = k.mat("#6f7882", "metal")
    bolt = k.mat("#cfd5dc", "metal")
    orange = k.mat("#ff8a1f", "satin")
    glass = k.mat("#1b2a5a", "glass")
    cz = 0.72

    # flange set into the wall, with a rim of bolts
    k.cyl(0.71, 0.05, at=(0, -0.025, cz), rot=(90, 0, 0), m=flange_m, bevel=0.012)
    for i in range(18):
        a = math.radians(i * 20 + 10)
        k.cyl(0.024, 0.03, at=(0.655 * math.cos(a), -0.06, cz + 0.655 * math.sin(a)), rot=(90, 0, 0), m=bolt,
              bevel=0.006, verts=6)

    # the door disc and its raised rim
    k.cyl(0.5, 0.1, at=(0, -0.1, cz), rot=(90, 0, 0), m=door, bevel=0.015)
    k.torus(0.465, 0.028, at=(0, -0.15, cz), rot=(90, 0, 0), m=door)

    # small round window above the wheel
    wz = cz + 0.31
    k.cyl(0.075, 0.02, at=(0, -0.152, wz), rot=(90, 0, 0), m=glass, bevel=0.003)
    k.torus(0.085, 0.018, at=(0, -0.155, wz), rot=(90, 0, 0), m=flange_m)

    # spoked wheel handle on a central hub
    k.cyl(0.05, 0.11, at=(0, -0.205, cz), rot=(90, 0, 0), m=flange_m, bevel=0.008)
    k.cyl(0.035, 0.03, at=(0, -0.265, cz), rot=(90, 0, 0), m=orange, bevel=0.006)
    k.torus(0.17, 0.022, at=(0, -0.24, cz), rot=(90, 0, 0), m=orange)
    for i in range(5):
        a = math.radians(90 + i * 72)
        k.tube([(0.04 * math.cos(a), -0.24, cz + 0.04 * math.sin(a)),
                (0.17 * math.cos(a), -0.24, cz + 0.17 * math.sin(a))], 0.016, orange)

    # two hinges on the left side
    for dz in (0.2, -0.2):
        z = cz + dz
        k.box((0.06, 0.1, 0.12), at=(-0.585, -0.1, z), m=flange_m, bevel=0.008)
        k.cyl(0.03, 0.15, at=(-0.585, -0.165, z), m=bolt, bevel=0.006)
        k.box((0.2, 0.03, 0.08), at=(-0.48, -0.165, z), m=door, bevel=0.006)
        for x in (-0.45, -0.4):
            k.cyl(0.012, 0.012, at=(x, -0.185, z), rot=(90, 0, 0), m=bolt, verts=6)

    # setting: paneled station wall and deck floor
    k.box((7, 0.2, 4.5), at=(0, 0.1, 2.0), m=k.mat("#7f93a3", "satin"), bevel=0.01, setting=True)
    panel = k.mat("#b4c6d3", "satin")
    for ix in range(-3, 4):
        for iz in range(0, 4):
            k.box((0.86, 0.02, 0.86), at=(ix * 0.9, -0.01, 0.47 + iz * 0.9), m=panel, bevel=0.012, setting=True)
    k.box((7, 4, 0.1), at=(0, -2.0, -0.05), m=k.mat("#5e6b78", "satin"), bevel=0.01, setting=True)
