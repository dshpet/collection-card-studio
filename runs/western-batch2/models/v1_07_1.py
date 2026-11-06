# Covered wagon: a wooden box body rests on two axles, a big pair of wheels at the back and a smaller pair at
# the front, each wheel a wooden rim with spokes around a hub on the axle. The white canvas cover is a half
# tube arched over the box, tucked onto its top edge and stretched over wooden bows at both open ends, with the
# dark inside showing through each end and a red cloth band along each side. The wooden pole is fixed to the
# front axle by two braces and runs forward and down until its tip rests on the packed dirt slab; it is left
# out of the framing so the wagon body fills the card.
import math

SCENE = {"category": "3", "backdrop": "#3cc6ea", "azimuth": 32, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#a8682f", "matte")
    dark = k.mat("#7a4520", "matte")
    canvas = k.mat("#f7f3e8", "matte")
    inside = k.mat("#5a4636", "matte")
    red = k.mat("#e0312b", "matte")
    iron = k.mat("#5c5f66", "metal")

    # Box body and its top rim boards.
    k.box((1.0, 0.5, 0.25), at=(0, 0, 0.425), m=wood, bevel=0.015)
    for y in (-0.255, 0.255):
        k.box((1.02, 0.03, 0.04), at=(0, y, 0.53), m=dark, bevel=0.008)
    for x in (-0.505, 0.505):
        k.box((0.03, 0.54, 0.04), at=(x, 0, 0.53), m=dark, bevel=0.008)

    # Axles, a bolster under the body over the front axle, and the wheels.
    for x, r in ((-0.33, 0.27), (0.33, 0.22)):
        k.cyl(0.035, 0.74, at=(x, 0, r), rot=(90, 0, 0), m=iron)
        if r < 0.27:
            k.box((0.09, 0.5, 0.06), at=(x, 0, 0.275), m=dark, bevel=0.008)
        spokes = 12 if r > 0.25 else 10
        for y in (-0.31, 0.31):
            k.torus(r - 0.035, 0.035, at=(x, y, r), rot=(90, 0, 0), m=wood)
            k.cyl(0.06, 0.11, at=(x, y, r), rot=(90, 0, 0), m=dark, bevel=0.01)
            for i in range(spokes):
                a = 2 * math.pi * i / spokes
                c, s = math.cos(a), math.sin(a)
                k.tube([(x + 0.05 * c, y, r + 0.05 * s), (x + (r - 0.055) * c, y, r + (r - 0.055) * s)],
                       0.016, wood)

    # Canvas cover: a tube along x, its lower half flattened onto the body top, raised a little taller than wide.
    length, rad = 1.06, 0.285
    profile = [(0.17, 0.0), (0.23, 0.0), (rad, 0.0), (rad, 0.02)]
    profile += [(rad, 0.02 + (length - 0.04) * i / 20) for i in range(1, 20)]
    profile += [(rad, length - 0.02), (rad, length), (0.23, length), (0.17, length)]
    cover = k.lathe(profile, at=(-length / 2, 0, 0.55), rot=(0, 90, 0), m=canvas, verts=96)

    def arch(p):
        x, y, z = p  # local x points down after the rotation
        if x > 0:
            x = 0.0
        return (x * 1.2, y, z)

    k.warp(cover, arch)

    # Open ends: a dark inside face set just within each end, and a wooden bow along each end's edge.
    for side in (-1, 1):
        lining = k.cyl(rad - 0.02, 0.01, at=(side * (length / 2 - 0.04), 0, 0.55), rot=(0, 90, 0), m=inside,
                       bevel=0.002)
        k.warp(lining, lambda p: (p[0] * 1.2, p[1], p[2]))
        bow = []
        for i in range(17):
            t = math.pi * i / 16
            bow.append((side * (length / 2 - 0.01), (rad + 0.004) * math.cos(t),
                        0.55 + 1.2 * (rad + 0.004) * math.sin(t)))
        k.tube(bow, 0.018, dark, curved=True)

    # Red band along each side of the canvas, low on its vertical part.
    for side in (-1, 1):
        k.box((length - 0.06, 0.014, 0.06), at=(0, side * 0.282, 0.6), m=red, bevel=0.004)

    # Pole on two braces from the front axle, its tip resting on the ground; kept out of the framing.
    k.unframed(k.tube([(0.30, 0, 0.24), (1.08, 0, 0.032)], 0.03, wood))
    for y in (-0.2, 0.2):
        k.tube([(0.33, y, 0.22), (0.62, 0, 0.17)], 0.02, dark)

    # Packed dry dirt slab.
    k.box((7, 7, 0.1), at=(0, 1.2, -0.05), m=k.mat("#c9995f", "matte"), bevel=0.02, setting=True)
