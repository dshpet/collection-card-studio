# Wagon wheel: a wooden hub (the nave) bored for the axle, with iron bands at both ends. Fourteen tapered
# spokes run straight out to the wooden rim ring (the felloe), and a dark iron tire wraps around the felloe.
# The wheel stands in the xz plane facing -y and floats, turned away from the camera so its face and its
# rim thickness both show.
import math

SCENE = {"category": "1", "backdrop": "#4fb4ef", "azimuth": 22, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#9a5f2e", "matte")
    hubwood = k.mat("#7e4a22", "matte")
    iron = k.mat("#3d4046", "metal")
    cz = 0.5

    # Felloe (wooden rim) and the iron tire around it.
    k.torus(0.425, 0.05, at=(0, 0, cz), rot=(90, 0, 0), m=wood)
    k.torus(0.487, 0.03, at=(0, 0, cz), rot=(90, 0, 0), m=iron)
    # Iron bolts through the felloe, one between every other pair of spokes.
    n = 14
    for i in range(0, n, 2):
        a = 2 * math.pi * i / n + math.pi / n
        k.sphere(0.017, at=(0.425 * math.sin(a), -0.05, cz + 0.425 * math.cos(a)), scale=(1, 0.5, 1), m=iron)

    # Hub: a turned wooden nave along the axle (y), longer than the wheel is thick.
    prof = [(0.0, -0.13), (0.055, -0.13), (0.07, -0.11), (0.1, -0.06), (0.105, 0.0),
            (0.1, 0.06), (0.07, 0.11), (0.055, 0.13), (0.0, 0.13)]
    k.lathe(prof, at=(0, 0, cz), rot=(90, 0, 0), m=hubwood)
    for y in (-0.085, 0.085):
        k.torus(0.093, 0.016, at=(0, y, cz), rot=(90, 0, 0), m=iron)
    # Axle cap on the front face of the nave.
    k.cyl(0.04, 0.03, at=(0, -0.14, cz), rot=(90, 0, 0), m=iron, bevel=0.008)

    # Spokes: tapered, from inside the nave out into the felloe.
    r0, r1 = 0.08, 0.41
    for i in range(n):
        a = 2 * math.pi * i / n
        mid = (r0 + r1) / 2
        k.cone(0.032, 0.024, r1 - r0, at=(mid * math.sin(a), 0, cz + mid * math.cos(a)),
               rot=(0, math.degrees(a), 0), m=wood)

    k.turn(8, 0, -18)
