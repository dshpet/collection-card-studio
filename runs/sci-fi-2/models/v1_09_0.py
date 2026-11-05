# Moon rover: a flat white deck rides on six gray wheels, three per side, each on an axle stub hung from a
# strut under the deck edge, with a fender over each wheel. The open cabin is two seats under a roll bar,
# with a console in front of them and a cargo box behind. A mast rises from the front corner of the deck
# and carries a small yellow dish with a feed horn. The rover stands on gray moon ground with a few
# crater rims and low hills far back.
SCENE = {"category": "4", "backdrop": "#6cc24a", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    frame = k.mat("#b9bec6", "metal")
    tire = k.mat("#8d939b", "matte")
    hub = k.mat("#5d636b", "satin")
    seat = k.mat("#d9dce1", "matte")
    dark = k.mat("#4a4f57", "satin")
    yellow = k.mat("#ffcc22", "satin")

    # Deck (flat body)
    k.box((1.05, 0.5, 0.06), at=(0, 0, 0.31), m=white, bevel=0.012)

    # Six wheels on struts and axle stubs, fenders above
    r, w = 0.13, 0.09
    for x in (-0.38, 0.0, 0.38):
        for s in (-1, 1):
            k.cyl(r, w, at=(x, s * 0.325, r), rot=(90, 0, 0), m=tire, bevel=0.02)
            k.cyl(0.05, w + 0.02, at=(x, s * 0.325, r), rot=(90, 0, 0), m=hub, bevel=0.008)
            k.cyl(0.02, 0.09, at=(x, s * 0.245, r), rot=(90, 0, 0), m=frame)
            k.box((0.04, 0.04, 0.17), at=(x, s * 0.22, 0.2), m=frame, bevel=0.006)
            k.box((0.32, 0.135, 0.016), at=(x, s * 0.3175, 0.288), m=white, bevel=0.005)

    # Open cabin: two seats, roll bar, console
    for s in (-1, 1):
        k.box((0.17, 0.17, 0.05), at=(-0.05, s * 0.11, 0.365), m=seat, bevel=0.012)
        k.box((0.04, 0.17, 0.18), at=(-0.14, s * 0.11, 0.45), rot=(0, -8, 0), m=seat, bevel=0.012)
    k.tube([(-0.2, -0.235, 0.34), (-0.2, -0.235, 0.6), (-0.2, 0.235, 0.6), (-0.2, 0.235, 0.34)], 0.014, frame)
    k.box((0.08, 0.3, 0.14), at=(0.2, 0, 0.41), rot=(0, -10, 0), m=white, bevel=0.01)
    k.box((0.04, 0.2, 0.012), at=(0.17, 0, 0.482), rot=(0, -25, 0), m=dark, bevel=0.003)

    # Cargo box at the back
    k.box((0.2, 0.42, 0.12), at=(-0.39, 0, 0.4), m=white, bevel=0.012)

    # Antenna mast and small yellow dish at the front corner
    mx, my = 0.38, 0.17
    k.cyl(0.035, 0.03, at=(mx, my, 0.355), m=frame)
    k.cyl(0.013, 0.3, at=(mx, my, 0.49), m=frame)
    dish = [(0.0, 0.0), (0.03, 0.004), (0.06, 0.014), (0.09, 0.032), (0.105, 0.046),
            (0.1, 0.05), (0.08, 0.038), (0.05, 0.024), (0.02, 0.016), (0.0, 0.015)]
    k.lathe(dish, at=(mx, my, 0.635), rot=(0, 35, 0), m=yellow)
    k.cyl(0.006, 0.07, at=(mx + 0.02, my, 0.68), rot=(0, 35, 0), m=frame)

    # Moon ground, crater rims, far hills
    ground = k.mat("#9a9da3", "matte")
    k.floor("#9a9da3")
    for cx, cy, big in ((1.1, 0.9, 0.35), (-1.2, 1.6, 0.5), (0.6, -1.1, 0.25), (-0.2, 3.2, 0.8)):
        k.torus(big, 0.06, at=(cx, cy, 0.0), rot=(0, 0, 0), m=ground, setting=True)
        k.cyl(big - 0.03, 0.01, at=(cx, cy, 0.002), rot=(0, 0, 0), m=k.mat("#83878e", "matte"), setting=True)
    k.blob([(-3.0, 8.0, -0.6, 1.6, (2.0, 1.0, 0.6)), (2.5, 9.0, -0.8, 1.8, (2.2, 1.0, 0.6))], ground, setting=True)
