# Wooden barrel: a bellied body of staves (a faceted lathe, one facet per stave) stands on its bottom end on a
# plank floor. Four dark iron hoops clasp it, two near the ends and two either side of the belly. The flat lid
# sits just inside the stave ends, which rise a little above it as the rim. The floor planks run toward the
# camera and stop behind the barrel, where the yellow backdrop begins.
import math

SCENE = {"category": "3", "backdrop": "#ffd84a", "azimuth": 25, "elevation": 15, "lens": 60, "light": "left"}

H, R_END, BULGE = 1.0, 0.30, 0.07


def radius(z):
    return R_END + BULGE * math.sin(math.pi * z / H)


def build(k):
    wood = k.mat("#9a5a2b", "matte")
    lid_wood = k.mat("#a8642f", "matte")
    iron = k.mat("#3b3d42", "metal")

    profile = [(0.0, 0.0)]
    profile += [(radius(H * i / 24), H * i / 24) for i in range(25)]
    profile += [(R_END - 0.025, H), (R_END - 0.025, H - 0.03), (0.0, H - 0.03)]
    k.lathe(profile, at=(0, 0, 0), m=wood, verts=22)

    k.cyl(R_END - 0.03, 0.02, at=(0, 0, H - 0.025), m=lid_wood, bevel=0.004)

    for z in (0.07, 0.30, 0.70, 0.93):
        k.cyl(radius(z) + 0.014, 0.065, at=(0, 0, z), m=iron, bevel=0.008)

    floor = k.mat("#d8955a", "matte")
    for i in range(-7, 8):
        k.box((0.33, 4.5, 0.12), at=(i * 0.345, -1.0, -0.06), m=floor, bevel=0.012, setting=True)
