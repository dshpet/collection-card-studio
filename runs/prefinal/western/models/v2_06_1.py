# Acoustic guitar lying on its back on porch planks. The body is one guitar outline (a cylinder warped into lower
# bout, waist and upper bout) with a lighter top plate of the same outline. The round sound hole with its rosette sits
# in the upper bout; the fretboard stops just short of it, and the red pick guard lies beside it on the treble side.
# The neck joins the upper bout and the headstock carries three tuning pegs per side. Six strings run from the
# bridge saddle over the sound hole and the nut to the peg posts. Seen from high above, laid diagonally.
import math

SCENE = {"category": "3", "backdrop": "#45c8e8", "azimuth": 25, "elevation": 62, "lens": 60, "light": "left"}


def outline(scale):
    # Unit-circle cylinder -> guitar body outline: wide lower bout (-x), pinched waist, smaller upper bout (+x).
    def fn(p):
        u = max(-1.0, min(1.0, p[0]))
        g = (1.04 - 0.25 * u) - 0.45 * math.exp(-((u - 0.1) / 0.2) ** 2)
        return (p[0] * 0.3225 * scale, p[1] * 0.215 * g * scale, p[2])
    return fn


def build(k):
    side = k.mat("#8a4a20", "satin")
    top = k.mat("#c98a48", "satin")
    neckw = k.mat("#7a4019", "satin")
    board = k.mat("#3a2418", "satin")
    black = k.mat("#151515", "matte")
    red = k.mat("#d3262b", "gloss")
    bone = k.mat("#f2ead8", "satin")
    metal = k.mat("#c9ced6", "metal")
    string = k.mat("#1a1a1a", "satin")

    # Body: one shaped shell (sides and back) and a top plate of the same outline.
    cx = -0.12
    body = k.cyl(1.0, 0.1, at=(cx, 0, 0.05), m=side, bevel=0.04, verts=160)
    k.warp(body, outline(1.0))
    plate = k.cyl(1.0, 0.006, at=(cx, 0, 0.101), m=top, bevel=0.005, verts=160)
    k.warp(plate, outline(0.965))

    # Sound hole with rosette in the upper bout; pick guard beside it on the treble side.
    hx = 0.07
    k.cyl(0.05, 0.006, at=(hx, 0, 0.103), m=black, bevel=0.001)
    k.torus(0.06, 0.007, at=(hx, 0, 0.105), m=bone)
    guard = k.cyl(0.045, 0.004, at=(0.0, -0.1, 0.104), m=red, bevel=0.001)
    k.warp(guard, lambda p: (p[0] * 1.2, p[1], p[2]))

    # Bridge with saddle on the lower bout.
    k.box((0.055, 0.19, 0.018), at=(-0.27, 0, 0.113), m=board, bevel=0.006)
    k.box((0.008, 0.09, 0.012), at=(-0.262, 0, 0.126), m=bone, bevel=0.002)

    # Neck joined to the upper bout, fretboard from just above the sound hole to the nut, frets, nut.
    k.box((0.47, 0.062, 0.05), at=(0.415, 0, 0.073), m=neckw, bevel=0.015)
    k.box((0.508, 0.072, 0.012), at=(0.394, 0, 0.11), m=board, bevel=0.003)
    for i in range(12):
        x = 0.635 - 0.04 * i * (1 - 0.025 * i)
        k.box((0.005, 0.072, 0.004), at=(x, 0, 0.117), m=metal, bevel=0.001)
    k.box((0.01, 0.074, 0.012), at=(0.648, 0, 0.122), m=bone, bevel=0.002)

    # Headstock with tuning pegs: post on top, shaft and key sticking out each side.
    k.box((0.17, 0.1, 0.026), at=(0.738, 0, 0.098), m=neckw, bevel=0.008)
    for x in (0.69, 0.74, 0.79):
        for s in (-1, 1):
            k.cyl(0.008, 0.03, at=(x, s * 0.03, 0.12), m=metal)
            k.cyl(0.006, 0.03, at=(x, s * 0.062, 0.098), rot=(90, 0, 0), m=metal)
            k.box((0.03, 0.02, 0.012), at=(x, s * 0.085, 0.098), m=bone, bevel=0.004)

    # Strings: bridge pin -> saddle -> nut -> peg post. Strings 0-2 go to the -y pegs, 3-5 to +y.
    order = [(0.79, -1), (0.74, -1), (0.69, -1), (0.69, 1), (0.74, 1), (0.79, 1)]
    for i in range(6):
        f = (i - 2.5) / 2.5
        px, ps = order[i]
        k.tube([(-0.262, f * 0.036, 0.132), (0.648, f * 0.028, 0.129), (px, ps * 0.03, 0.128)], 0.0045, string)
        k.sphere(0.006, at=(-0.285, f * 0.036, 0.123), m=bone)

    k.turn(0, 0, 38)

    # Porch planks running across the card, with dark gaps between them.
    k.floor("#5a3a22", z=-0.03)
    planks = (k.mat("#e0b06e", "matte"), k.mat("#d6a462", "matte"))
    for i in range(-12, 13):
        k.box((0.27, 8, 0.05), at=(i * 0.28, 0, -0.025), m=planks[i % 2], bevel=0.006, setting=True)
