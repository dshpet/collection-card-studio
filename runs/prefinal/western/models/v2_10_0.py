# Covered wagon on a dirt trail: a wooden box bed rests on two axle beams (a tall bolster under the bed over the
# smaller front axle); four spoked wooden wheels with red rims turn on the axle ends. The arched white canvas sits
# on the bed top, with a dark puckered opening at the front. The tongue runs from the front axle down to the
# ground and goes off the framing so the wagon stays large; the trail runs off the card both ways.
import math

SCENE = {"category": "4", "backdrop": "#5fd0f5", "azimuth": 35, "elevation": 10, "lens": 55, "light": "left"}


def build(k):
    wood = k.mat("#9a5a2b", "matte")
    dark = k.mat("#6e3f1e", "matte")
    canvas = k.mat("#f7f3ea", "matte")
    rim = k.mat("#d8322b", "satin")
    shade = k.mat("#4a2e18", "matte")

    # Bed
    k.box((0.5, 1.0, 0.16), at=(0, 0, 0.43), m=wood, bevel=0.012)
    for y in (-0.5, 0.5):
        k.box((0.52, 0.03, 0.04), at=(0, y, 0.49), m=dark, bevel=0.006)

    # Axles and bolsters (rear: big wheels, front: small wheels)
    wheels = ((0.33, 0.30), (-0.33, 0.24))
    for y, r in wheels:
        k.box((0.72, 0.07, 0.07), at=(0, y, r), m=dark, bevel=0.008)
        top = r + 0.035
        k.box((0.46, 0.08, 0.35 - top), at=(0, y, (top + 0.35) / 2), m=dark, bevel=0.006)
        for side in (-1, 1):
            x = side * 0.31
            k.cyl(0.06, 0.1, at=(x, y, r), rot=(0, 90, 0), m=dark, bevel=0.01)
            k.torus(r - 0.028, 0.03, at=(x, y, r), rot=(0, 90, 0), m=rim)
            for i in range(5):
                k.box((0.03, 0.03, 2 * (r - 0.04)), at=(x, y, r), rot=(i * 36, 0, 0), m=wood, bevel=0.005)

    # Canvas cover: a cylinder along y, flattened below the bed top and arched tall above
    def arch(p):
        x, y, z = p
        return (x, y * 1.5 if y > 0 else y * 0.1, z)

    cover = k.cyl(0.265, 1.06, at=(0, 0, 0.51), rot=(90, 0, 0), m=canvas, bevel=0.02)
    k.warp(cover, arch)
    opening = k.cyl(0.19, 0.02, at=(0, -0.526, 0.51), rot=(90, 0, 0), m=shade, bevel=0.004)
    k.warp(opening, arch)
    for y in (-0.36, 0.0, 0.36):
        hoop = k.cyl(0.275, 0.035, at=(0, y, 0.51), rot=(90, 0, 0), m=canvas, bevel=0.012)
        k.warp(hoop, arch)

    # Tongue: from the front axle forward, its tip resting on the ground
    tongue = k.tube([(0, -0.33, 0.24), (0, -0.7, 0.13), (0, -1.1, 0.025)], 0.028, wood)
    hounds = [k.tube([(s * 0.2, -0.33, 0.24), (0, -0.6, 0.16)], 0.022, wood) for s in (-1, 1)]
    k.unframed(tongue, *hounds)

    # Setting: grass with a dirt trail running along the wagon
    k.floor("#7cc444", "matte", size=40, z=0)
    k.box((1.7, 20, 0.02), at=(0, 0, 0.0), m=k.mat("#c99a62", "matte"), bevel=0, setting=True)
