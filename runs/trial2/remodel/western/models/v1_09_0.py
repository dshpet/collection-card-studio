# Covered wagon: a wooden box bed rests on a bolster across one axle; two large spoked wheels turn on the axle
# ends outside the bed. The canvas cover is one D-section hood, flaring at both ends, sitting on the bed top, with
# its hoop ribs showing as raised bands and a dark puckered opening at the front. Red trim runs along the bed's
# top rails. The tongue runs from the front of the bed down to rest on the trail, so the cart stands on three
# points; it is left out of the framing. Setting: a dusty trail across green prairie, low hills far back.
import math

SCENE = {"category": "4", "backdrop": "#5ec2f2", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#9a5f2e", "matte")
    dark_wood = k.mat("#6b3f1f", "matte")
    canvas = k.mat("#f6f1e4", "matte")
    rib = k.mat("#ebe3cf", "matte")
    red = k.mat("#d8322b", "satin")
    iron = k.mat("#4a4a4f", "metal")
    shadow = k.mat("#3a2414", "matte")

    # Bed on a bolster on the axle.
    axle_z, wheel_r, wheel_y = 0.36, 0.36, 0.34
    k.cyl(0.03, 0.80, at=(0, 0, axle_z), rot=(90, 0, 0), m=dark_wood)
    k.box((0.10, 0.52, 0.05), at=(0, 0, 0.415), m=dark_wood)
    bed_bottom, bed_top = 0.44, 0.64
    k.box((0.98, 0.50, bed_top - bed_bottom), at=(0, 0, (bed_top + bed_bottom) / 2), m=wood, bevel=0.012)
    for y in (-0.255, 0.255):
        k.box((1.0, 0.025, 0.04), at=(0, y, bed_top - 0.02), m=red, bevel=0.006)
        k.box((1.0, 0.022, 0.03), at=(0, y, bed_bottom + 0.02), m=dark_wood, bevel=0.005)
    for x in (-0.495, 0.495):
        k.box((0.025, 0.52, 0.04), at=(x, 0, bed_top - 0.02), m=red, bevel=0.006)

    # Wheels: iron tire, wooden felloe, hub, twelve spokes.
    for side in (-1, 1):
        y = side * wheel_y
        k.torus(wheel_r - 0.025, 0.027, at=(0, y, axle_z), rot=(90, 0, 0), m=iron)
        k.torus(wheel_r - 0.065, 0.026, at=(0, y, axle_z), rot=(90, 0, 0), m=wood)
        k.cyl(0.065, 0.11, at=(0, y, axle_z), rot=(90, 0, 0), m=dark_wood, bevel=0.01)
        k.cyl(0.035, 0.13, at=(0, y, axle_z), rot=(90, 0, 0), m=red, bevel=0.006)
        for i in range(12):
            a = i * math.pi / 6
            c, s = math.cos(a), math.sin(a)
            k.tube([(0.06 * c, y, axle_z + 0.06 * s), (0.28 * c, y, axle_z + 0.28 * s)], 0.015, wood)

    # Canvas hood: a lathe along local z, warped into a D-section along x that flares at the ends.
    half_w, half_h, base = 0.262, 0.40, bed_top - 0.02

    def flare(x):
        return 1 + 0.14 * (abs(x) / 0.5) ** 3

    zs = [-0.5 + i / 40 for i in range(41)]
    profile = [(0, -0.5)] + [(flare(z), z) for z in zs] + [(0, 0.5)]
    hood = k.lathe(profile, at=(0, 0, base), m=canvas, verts=96)

    def to_hood(p):
        x, y, z = p
        r, a = math.hypot(x, y), (math.atan2(y, x) + math.pi) / 2
        return (z, r * half_w * math.cos(a), r * half_h * math.sin(a))

    k.warp(hood, to_hood)

    for x, rr, m in ((-0.25, 0.014, rib), (0.0, 0.014, rib), (0.25, 0.014, rib), (-0.5, 0.022, canvas),
                     (0.5, 0.022, canvas)):
        f = flare(x) * 1.02
        arch = [(x, f * half_w * math.cos(t), base + f * half_h * math.sin(t))
                for t in (j * math.pi / 16 for j in range(17))]
        k.tube(arch, rr, m, curved=True)

    k.sphere(0.1, at=(0.505, 0, base + 0.19), scale=(0.25, 1.6, 1.8), m=shadow)

    # Tongue from the front of the bed down to the trail.
    tongue = k.tube([(0.46, 0, 0.47), (0.75, 0, 0.30), (1.15, 0, 0.035)], 0.025, dark_wood)
    foot = k.box((0.08, 0.08, 0.03), at=(1.15, 0, 0.015), m=dark_wood, bevel=0.006)
    k.unframed(tongue, foot)

    # Setting: dusty trail across prairie grass, soft hills far back.
    k.floor("#7cc447", z=-0.012)
    k.box((12, 1.1, 0.02), at=(0, 0, -0.01), m=k.mat("#d9b77a", "matte"), bevel=0, setting=True)
    grass = k.mat("#69b83e", "matte")
    k.sphere(2.5, at=(-3.5, 9, -1.4), scale=(2.2, 1, 0.7), m=grass, setting=True)
    k.sphere(2.5, at=(4.5, 11, -1.6), scale=(2.6, 1, 0.75), m=k.mat("#5fa83a", "matte"), setting=True)
