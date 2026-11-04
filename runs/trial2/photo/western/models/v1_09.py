# Covered wagon: a wooden box bed rests on two bolsters, one over each axle. Two large rear wheels and two
# smaller front wheels turn on the axle ends, each with a hub, twelve spokes and a wooden rim standing on the
# trail. A reach pole joins the axles under the bed, and the tongue runs forward from the front axle down to the
# ground. The white canvas sits on the top of the bed sides, sags a little between five bows, and is drawn in at
# the rear end around a dark opening. A thin red strip runs along the top edge of the bed. The camera looks at
# the rear three-quarter, so the big rear wheels and the opening face it, and the tongue runs off the card.
import math

SCENE = {"category": "4", "backdrop": "#5cc2f2", "azimuth": 32, "elevation": 12, "lens": 55, "light": "left"}


def wheel(k, x, y, r, wood, iron):
    k.torus(r - 0.028, 0.028, at=(x, y, r), rot=(90, 0, 0), m=wood)
    k.torus(r - 0.008, 0.012, at=(x, y, r), rot=(90, 0, 0), m=iron)
    k.cyl(0.055, 0.1, at=(x, y, r), rot=(90, 0, 0), m=wood, bevel=0.01)
    k.cyl(0.03, 0.12, at=(x, y, r), rot=(90, 0, 0), m=iron)
    length = r - 0.03
    for i in range(12):
        a = i * 30
        s, c = math.sin(math.radians(a)), math.cos(math.radians(a))
        k.cyl(0.013, length, at=(x + s * length / 2, y, r + c * length / 2), rot=(0, a, 0), m=wood, bevel=0.003)


def build(k):
    wood = k.mat("#8a5530", "matte")
    dark = k.mat("#6b3f22", "matte")
    iron = k.mat("#4a4a4f", "metal")
    canvas = k.mat("#f6f3ea", "matte")
    red = k.mat("#d6332b", "satin")

    rear_x, front_x, rear_r, front_r, wy = 0.3, -0.32, 0.3, 0.22, 0.3
    bed_bottom = 0.42

    # Running gear: axles, bolsters, reach pole, wheels.
    for x, r in ((rear_x, rear_r), (front_x, front_r)):
        k.cyl(0.03, 0.68, at=(x, 0, r), rot=(90, 0, 0), m=dark)
        h = bed_bottom - r + 0.02
        k.box((0.09, 0.5, h), at=(x, 0, r - 0.02 + h / 2), m=dark, bevel=0.008)
        for side in (-1, 1):
            wheel(k, x, side * wy, r, wood, iron)
    k.tube([(front_x, 0, front_r), (rear_x, 0, rear_r)], 0.022, dark)

    # Tongue: forked hounds from the front axle join into one pole that rests on the ground.
    tongue = [k.tube([(front_x, side * 0.15, front_r), (-0.62, 0, 0.15)], 0.02, dark) for side in (-1, 1)]
    tongue.append(k.tube([(-0.62, 0, 0.15), (-1.3, 0, 0.025)], 0.025, dark))
    k.unframed(*tongue)

    # Wagon bed with plank seams and red trim along the top edge.
    k.box((0.9, 0.42, 0.2), at=(0, 0, bed_bottom + 0.1), m=wood, bevel=0.01)
    for side in (-1, 1):
        k.box((0.9, 0.012, 0.012), at=(0, side * 0.212, bed_bottom + 0.07), m=dark, bevel=0.002)
        k.box((0.9, 0.014, 0.026), at=(0, side * 0.214, bed_bottom + 0.185), m=red, bevel=0.003)
    for x in (-0.451, 0.451):
        k.box((0.012, 0.42, 0.026), at=(x, 0, bed_bottom + 0.185), m=red, bevel=0.003)

    # Canvas cover: a lathe along x, sagging between five bows, flattened at the bed top, drawn in at the ends.
    top = bed_bottom + 0.2
    half, R = 0.47, 0.23
    bows = [-0.42, -0.21, 0.0, 0.21, 0.42]
    profile = [(0.0, -half), (0.19, -half), (0.215, -half + 0.012), (0.228, -half + 0.03)]
    steps = 60
    for i in range(steps + 1):
        z = -0.42 + 0.84 * i / steps
        d = min(abs(z - b) for b in bows)
        profile.append((R - 0.008 * math.sin(min(d / 0.105, 1) * math.pi / 2), z))
    profile += [(0.228, half - 0.03), (0.215, half - 0.012), (0.19, half), (0.0, half)]
    cover = k.lathe(profile, at=(0, 0, top), rot=(0, -90, 0), m=canvas, verts=96)

    def shape(p):
        x, y, z = p
        end = max(0.0, (abs(z) - 0.33) / 0.14)
        return (max(x, 0.0) * (1.85 + 0.15 * end), y * (1 + 0.06 * end), z)

    k.warp(cover, shape)

    # Rear opening, drawn in by the puckered canvas.
    k.sphere(1, at=(half + 0.004, 0, top + 0.15), scale=(0.008, 0.11, 0.15), m=k.mat("#2b2420", "matte"))

    # Setting: grass, a dusty trail under the wagon, soft hills far back.
    k.floor("#7cc653", z=-0.012)
    k.box((10, 1.3, 0.012), at=(0, 0, -0.006), m=k.mat("#e2bf86", "matte"), bevel=0, setting=True)
    k.blob([(-3.0, 9, -1.2, 3.0, (2.2, 1.0, 0.75))], k.mat("#5fb548", "matte"), setting=True)
    k.blob([(3.5, 11, -1.5, 3.0, (2.5, 1.0, 0.8))], k.mat("#6fbf52", "matte"), setting=True)
