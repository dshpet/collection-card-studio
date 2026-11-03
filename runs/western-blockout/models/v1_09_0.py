# Covered wagon on a prairie trail: a plank bed rides on one axle between two large spoked wheels; the canvas
# cover is gathered at both ends and sits down inside the bed, its bottom tucked below the red-trimmed top rails.
# The driver's bench rests on blocks at the front of the bed, and the tongue runs from under the bed down to the
# ground, so the two-wheeled wagon stands on its wheels and the tongue's end.
import math

SCENE = {"category": "4", "backdrop": "#5cc4f5", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#9a5a2b", "matte")
    dark = k.mat("#6e3d1c", "matte")
    canvas = k.mat("#f6f1e4", "matte")
    red = k.mat("#d8322b", "satin")
    iron = k.mat("#4a4f57", "metal")

    # bed: floor, sides and ends, red trim along the top of each side
    k.box((1.0, 0.5, 0.04), at=(0, 0, 0.42), m=wood)
    for y in (-0.235, 0.235):
        k.box((1.0, 0.03, 0.2), at=(0, y, 0.52), m=wood)
        k.box((1.0, 0.04, 0.03), at=(0, y, 0.635), m=red, bevel=0.006)
    for x in (-0.485, 0.485):
        k.box((0.03, 0.44, 0.2), at=(x, 0, 0.52), m=wood)
    # bolsters under the bed, sitting on the axle
    for x in (-0.12, 0.12):
        k.box((0.06, 0.5, 0.05), at=(x, 0, 0.375), m=dark)

    # axle and two large spoked wheels
    wr, ax_z = 0.35, 0.35
    k.cyl(0.03, 0.78, at=(0, 0, ax_z), rot=(90, 0, 0), m=iron)
    for y in (-0.33, 0.33):
        k.torus(wr - 0.02, 0.03, at=(0, y, ax_z), rot=(90, 0, 0), m=dark)
        k.cyl(0.06, 0.1, at=(0, y, ax_z), rot=(90, 0, 0), m=red, bevel=0.01)
        k.cyl(0.025, 0.12, at=(0, y, ax_z), rot=(90, 0, 0), m=iron)
        for i in range(12):
            a = math.radians(i * 30)
            k.tube([(0.05 * math.cos(a), y, ax_z + 0.05 * math.sin(a)),
                    ((wr - 0.035) * math.cos(a), y, ax_z + (wr - 0.035) * math.sin(a))], 0.015, wood)

    # canvas cover: a lathe along x, gathered at the ends, flattened below so it sits down inside the bed
    prof = [(0.0, -0.44), (0.17, -0.46), (0.22, -0.43), (0.255, -0.34), (0.27, -0.2), (0.275, 0.0),
            (0.27, 0.2), (0.255, 0.34), (0.22, 0.43), (0.17, 0.46), (0.0, 0.44)]
    cover = k.lathe(prof, at=(-0.06, 0, 0.6), rot=(0, 90, 0), m=canvas)

    def shape(p):
        x, y, z = p
        x = x * 1.3 if x < 0 else min(x, 0.05)  # local -x is world up
        return (x, y * 0.92, z)

    k.warp(cover, shape)

    # driver's bench at the front, on two blocks
    for y in (-0.19, 0.19):
        k.box((0.08, 0.05, 0.1), at=(0.43, y, 0.69), m=dark)
    k.box((0.12, 0.46, 0.035), at=(0.43, 0, 0.755), m=wood)

    # tongue from under the bed to the ground, with a crossbar resting there
    k.tube([(0.3, 0, 0.375), (0.5, 0, 0.36), (1.05, 0, 0.04)], 0.025, wood)
    k.box((0.05, 0.3, 0.04), at=(1.05, 0, 0.02), m=dark)

    # prairie: green grass, a dusty trail along the wagon, soft hills far back
    k.floor("#7cc957")
    k.box((40, 1.3, 0.02), at=(0, 0.05, 0.0), m=k.mat("#d9b98a", "matte"), bevel=0, setting=True)
    k.sphere(3.0, at=(-3.5, 9, -2.2), scale=(1.6, 1, 1), m=k.mat("#8fd06a", "matte"), setting=True)
    k.sphere(3.0, at=(4.5, 11, -2.0), scale=(1.8, 1, 1), m=k.mat("#9ad672", "matte"), setting=True)
