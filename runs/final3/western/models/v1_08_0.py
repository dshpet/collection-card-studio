# Covered wagon: a wooden box bed rests on two bolsters, one on each axle. The four wheels turn on the axle
# ends (bigger at the rear, smaller at the front), each with a hub, eight spokes and a red rim. An arched white
# canvas cover with slightly flared ends sits in the bed, held by wooden hoops. The tongue starts at the front
# bolster and runs forward and down until its tip rests on the packed-dirt ground.
import math

SCENE = {"category": "3", "backdrop": "#5cbf3a", "azimuth": 32, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#8a5a2e", "matte")
    dark = k.mat("#6b4322", "matte")
    canvas = k.mat("#f4f1e8", "matte")
    red = k.mat("#d23a2a", "satin")
    iron = k.mat("#4a4f57", "metal")

    # Running gear: axles at wheel-centre height, bolsters up to the bed bottom.
    bed_z = 0.36
    axles = ((-0.33, 0.30), (0.33, 0.24))  # (x, wheel radius)
    for x, r in axles:
        k.cyl(0.03, 0.74, at=(x, 0, r), rot=(90, 0, 0), m=iron)
        k.box((0.09, 0.46, bed_z - r + 0.02), at=(x, 0, (bed_z + r) / 2), m=dark, bevel=0.008)
        for side in (-1, 1):
            y = side * 0.32
            k.torus(r - 0.028, 0.028, at=(x, y, r), rot=(90, 0, 0), m=red)
            k.cyl(0.055, 0.09, at=(x, y, r), rot=(90, 0, 0), m=wood, bevel=0.01)
            k.cyl(0.03, 0.1, at=(x, y + side * 0.01, r), rot=(90, 0, 0), m=iron)
            for i in range(8):
                a = i * 45
                d = (r - 0.02) / 2 + 0.02
                k.box((0.024, 0.022, r - 0.05),
                      at=(x + math.sin(math.radians(a)) * d, y, r + math.cos(math.radians(a)) * d),
                      rot=(0, a, 0), m=wood, bevel=0.004)

    # Bed: a solid box with darker rails along its sides.
    k.box((1.0, 0.5, 0.18), at=(0, 0, bed_z + 0.09), m=wood, bevel=0.012)
    for y in (-0.255, 0.255):
        k.box((1.02, 0.03, 0.035), at=(0, y, bed_z + 0.165), m=dark, bevel=0.006)
        k.box((1.02, 0.03, 0.035), at=(0, y, bed_z + 0.02), m=dark, bevel=0.006)

    # Canvas cover: a lathe along x with flared ends, stretched taller into an arch.
    n = 24
    prof = [(0.0, -0.45)]
    for i in range(n + 1):
        z = -0.45 + 0.9 * i / n
        t = abs(z) / 0.45
        prof.append((0.25 + 0.025 * t ** 4, z))
    prof.append((0.0, 0.45))
    cover = k.lathe(prof, at=(0, 0, 0.67), rot=(0, 90, 0), m=canvas)
    k.warp(cover, lambda p: (p[0] * 1.15, p[1], p[2]))
    for x in (-0.22, 0.0, 0.22):
        hoop = k.torus(0.258, 0.014, at=(x, 0, 0.67), rot=(0, 90, 0), m=dark)
        k.warp(hoop, lambda p: (p[0] * 1.15, p[1], p[2]))

    # Tongue: from the front bolster forward, its tip resting on the ground.
    k.tube([(0.33, 0, 0.30), (0.55, 0, 0.22), (0.98, 0, 0.035)], 0.03, wood)
    k.cyl(0.035, 0.24, at=(0.97, 0, 0.035), rot=(90, 0, 0), m=wood, bevel=0.008)

    # Packed dirt ground.
    k.box((6, 6, 0.1), at=(0, 0.8, -0.05), m=k.mat("#b48555", "matte"), bevel=0.01, setting=True)
