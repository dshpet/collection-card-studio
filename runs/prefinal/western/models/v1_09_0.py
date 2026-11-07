# Farm windmill: four wooden legs splay from a stone plinth up to a small top deck, braced by rails and
# diagonals on every face. A turntable on the deck carries the head; a shaft runs forward (-y) to the hub,
# whose spokes hold an inner and outer ring with eighteen pitched metal blades between them. A boom runs
# back from the head to the red tail vane. The whole tower stands on a patch of dirt in dry grass.
import math

SCENE = {"category": "4", "backdrop": "#5fd0f5", "azimuth": 32, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#8a5a32", "matte")
    wood_dark = k.mat("#6e4526", "matte")
    stone = k.mat("#a9a49b", "matte")
    steel = k.mat("#9aa1a8", "metal")
    dark = k.mat("#5b6168", "satin")
    red = k.mat("#d8322a", "satin")

    # Stone base: a wide plinth with a smaller cap course.
    k.box((0.52, 0.52, 0.08), at=(0, 0, 0.04), m=stone, bevel=0.02)
    k.box((0.44, 0.44, 0.05), at=(0, 0, 0.105), m=stone, bevel=0.015)

    # Tower: four splayed legs from the plinth to the deck.
    z0, z1, w0, w1 = 0.13, 0.82, 0.17, 0.065

    def w(z):
        return w0 + (w1 - w0) * (z - z0) / (z1 - z0)

    r = 0.02
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.tube([(sx * w0, sy * w0, z0 - 0.01), (sx * w1, sy * w1, z1 + 0.01)], r, wood)
            k.box((0.07, 0.07, 0.03), at=(sx * w0, sy * w0, z0 + 0.005), m=dark, bevel=0.006)

    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    for z in (0.3, 0.5, 0.68):
        for i in range(4):
            a, b = corners[i], corners[(i + 1) % 4]
            k.tube([(a[0] * w(z), a[1] * w(z), z), (b[0] * w(z), b[1] * w(z), z)], 0.015, wood_dark)
    spans = [(z0 + 0.02, 0.3), (0.3, 0.5), (0.5, 0.68)]
    for n, (za, zb) in enumerate(spans):
        for i in range(4):
            a, b = corners[i], corners[(i + 1) % 4]
            if n % 2:
                a, b = b, a
            k.tube([(a[0] * w(za), a[1] * w(za), za), (b[0] * w(zb), b[1] * w(zb), zb)], 0.013, wood_dark)

    # Deck, turntable and head.
    k.box((0.2, 0.2, 0.03), at=(0, 0, 0.835), m=wood, bevel=0.008)
    k.cyl(0.06, 0.04, at=(0, 0, 0.87), m=dark)
    k.box((0.1, 0.2, 0.1), at=(0, 0, 0.94), m=dark, bevel=0.015)
    hz, hy = 0.95, -0.2
    k.cyl(0.02, 0.1, at=(0, -0.13, hz), rot=(90, 0, 0), m=steel)
    k.cyl(0.05, 0.07, at=(0, hy, hz), rot=(90, 0, 0), m=dark)
    k.sphere(0.035, at=(0, hy - 0.035, hz), scale=(1, 0.8, 1), m=dark)

    # Wheel: spokes, two rings and pitched blades in the x-z plane.
    for i in range(6):
        a = math.radians(i * 60 + 15)
        k.tube([(0.045 * math.sin(a), hy + 0.012, hz + 0.045 * math.cos(a)),
                (0.33 * math.sin(a), hy + 0.012, hz + 0.33 * math.cos(a))], 0.013, steel)
    k.torus(0.12, 0.013, at=(0, hy, hz), rot=(90, 0, 0), m=steel)
    k.torus(0.33, 0.015, at=(0, hy, hz), rot=(90, 0, 0), m=steel)
    pitch = math.radians(25)
    c, s = math.cos(pitch), math.sin(pitch)
    for i in range(18):
        a = i * 20
        ar = math.radians(a)
        blade = k.box((0.075, 0.008, 0.22), at=(0.225 * math.sin(ar), hy, hz + 0.225 * math.cos(ar)),
                      rot=(0, a, 0), m=steel, bevel=0.003)
        k.warp(blade, lambda p: (p[0] * c - p[1] * s, p[0] * s + p[1] * c, p[2]))

    # Tail: a boom with a brace back to the red vane.
    k.tube([(0, 0.09, 0.95), (0, 0.52, 0.98)], 0.017, wood)
    k.tube([(0, 0.06, 0.99), (0, 0.3, 1.04), (0, 0.5, 0.99)], 0.011, steel)
    k.box((0.014, 0.28, 0.2), at=(0, 0.6, 0.99), m=red, bevel=0.006)

    # Setting: dry grass with a patch of dirt round the plinth.
    k.floor("#c2ad5e", "matte")
    k.cyl(0.6, 0.012, at=(0, 0, 0.0), m=k.mat("#a4774a", "matte"), bevel=0.004, setting=True)
