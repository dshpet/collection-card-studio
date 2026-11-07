# Moon rover: a flat open chassis on four wheels, each hung from the chassis on a strut, with a curved fender
# over it. Two seats sit side by side mid-deck behind a small control console. A mast rises from the front corner
# of the deck and carries a small dish antenna; the orange tool box sits on the rear deck. The rover stands on
# pale grey moon dust with a low crater rim beside it.
import math

SCENE = {"category": "4", "backdrop": "#7a4fc9", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f2f2ee", "satin")
    grey = k.mat("#8d9199", "metal")
    dark = k.mat("#4a4e57", "matte")
    seat = k.mat("#b9bcc3", "matte")
    orange = k.mat("#f08a1c", "satin")

    wr, wx, wy, wz = 0.13, 0.37, 0.34, 0.125
    deck_z = 0.30

    # Chassis deck and low open body walls.
    k.box((0.6, 0.98, 0.05), at=(0, 0, deck_z), m=white, bevel=0.012)
    for side in (-1, 1):
        k.box((0.025, 0.42, 0.09), at=(side * 0.287, 0, deck_z + 0.07), m=white, bevel=0.008)
    k.box((0.6, 0.03, 0.08), at=(0, -0.475, deck_z + 0.065), m=white, bevel=0.008)

    # Wheels, hubs, struts and fenders.
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * wx, sy * wy
            k.cyl(wr, 0.09, at=(x, y, wz), rot=(0, 90, 0), m=dark, bevel=0.02)
            k.torus(wr - 0.005, 0.012, at=(x + sx * 0.045, y, wz), rot=(0, 90, 0), m=grey)
            k.cyl(0.045, 0.11, at=(x, y, wz), rot=(0, 90, 0), m=grey, bevel=0.008)
            k.tube([(sx * 0.25, y, deck_z - 0.02), (x - sx * 0.02, y, wz)], 0.018, grey)
            R = 0.175
            for i in range(7):
                a = math.radians(-75 + i * 25)
                k.box((0.12, 0.08, 0.012), at=(x, y + R * math.sin(a), wz + R * math.cos(a)),
                      rot=(-math.degrees(a), 0, 0), m=white, bevel=0.004)
            k.box((0.08, 0.02, 0.05), at=(sx * 0.33, y, deck_z), m=white, bevel=0.004)

    # Two seats side by side.
    for sx in (-1, 1):
        x = sx * 0.13
        k.box((0.2, 0.2, 0.05), at=(x, 0.03, deck_z + 0.07), m=seat, bevel=0.012)
        k.box((0.2, 0.04, 0.22), at=(x, 0.14, deck_z + 0.16), rot=(-10, 0, 0), m=seat, bevel=0.012)
        for dx in (-0.07, 0.07):
            k.cyl(0.012, 0.045, at=(x + dx, 0.03, deck_z + 0.045), m=grey)

    # Control console ahead of the seats, with a hand stick.
    k.box((0.1, 0.08, 0.12), at=(0, -0.13, deck_z + 0.085), m=white, bevel=0.01)
    k.cyl(0.012, 0.08, at=(0, -0.13, deck_z + 0.18), m=dark)
    k.sphere(0.022, at=(0, -0.13, deck_z + 0.225), m=dark)

    # Mast fixed at the front corner of the deck, carrying the dish antenna.
    mx, my, top = 0.2, -0.42, 0.82
    k.cyl(0.035, 0.03, at=(mx, my, deck_z + 0.04), m=grey)
    k.cyl(0.016, top - deck_z - 0.025, at=(mx, my, (top + deck_z + 0.025) / 2), m=grey)
    prof = [(0.0, 0.0)] + [(0.11 * i / 8, 0.05 * (i / 8) ** 2) for i in range(1, 9)]
    prof += [(0.105, 0.056)] + [(0.105 * i / 8, 0.006 + 0.05 * (i / 8) ** 2) for i in range(7, -1, -1)]
    k.lathe(prof, at=(mx, my - 0.02, top), rot=(60, 0, 0), m=white)
    k.cyl(0.006, 0.07, at=(mx, my - 0.05, top + 0.02), rot=(60, 0, 0), m=grey)
    k.sphere(0.012, at=(mx, my - 0.08, top + 0.04), m=grey)

    # Orange tool box on the rear deck.
    k.box((0.4, 0.16, 0.14), at=(0, 0.39, deck_z + 0.095), m=orange, bevel=0.012)
    k.box((0.41, 0.17, 0.012), at=(0, 0.39, deck_z + 0.14), m=orange, bevel=0.004)
    k.box((0.12, 0.02, 0.02), at=(0, 0.39, deck_z + 0.175), m=dark, bevel=0.004)

    # Pale grey moon dust and a low crater rim beside the rover.
    k.floor("#b2b2ba", "matte")
    k.torus(0.7, 0.07, at=(-1.4, 0.9, 0.0), rot=(0, 0, 0), m=k.mat("#a2a2ac", "matte"), setting=True)
