# Candelabra: a round domed foot carries a tall turned stem; at the top of the stem three arms branch out, the
# two outer ones swinging down and out and curving back up, the middle one rising straight on. Each arm ends in
# a cup with a drip pan, a cream candle stands in each cup, and a small flame sits on each wick. It floats, tilted
# a little so the arms show some depth.
SCENE = {"category": "1", "backdrop": "#6a1fd1", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e0a52a", "metal")
    wax = k.mat("#f6ecd2", "satin")
    wick = k.mat("#3a2a1e", "matte")
    flame = k.mat("#ff9a2a", "glow")

    k.lathe([(0.0, 0.0), (0.2, 0.0), (0.205, 0.015), (0.2, 0.03), (0.17, 0.05), (0.12, 0.075), (0.07, 0.095),
             (0.05, 0.11), (0.0, 0.11)], at=(0, 0, 0), rot=(0, 0, 0), m=gold)
    k.lathe([(0.0, 0.1), (0.04, 0.1), (0.035, 0.14), (0.03, 0.2), (0.055, 0.23), (0.06, 0.25), (0.055, 0.27),
             (0.028, 0.3), (0.026, 0.42), (0.045, 0.45), (0.05, 0.47), (0.045, 0.49), (0.032, 0.51),
             (0.04, 0.54), (0.04, 0.56), (0.0, 0.56)], at=(0, 0, 0), rot=(0, 0, 0), m=gold)

    r = 0.03
    cups = []
    for side in (-1, 1):
        k.tube([(side * 0.02, 0, 0.53), (side * 0.12, 0, 0.46), (side * 0.25, 0, 0.47), (side * 0.32, 0, 0.56),
                (side * 0.33, 0, 0.66)], r, gold, curved=True)
        cups.append((side * 0.33, 0.66))
    k.tube([(0, 0, 0.55), (0, 0, 0.66), (0, 0, 0.76)], r, gold)
    cups.append((0, 0.76))

    for x, z in cups:
        k.lathe([(0.0, 0.0), (0.03, 0.0), (0.045, 0.02), (0.075, 0.03), (0.08, 0.04), (0.05, 0.04),
                 (0.05, 0.07), (0.055, 0.08), (0.0, 0.08)], at=(x, 0, z - 0.01), rot=(0, 0, 0), m=gold)
        k.cyl(0.04, 0.28, at=(x, 0, z + 0.21), rot=(0, 0, 0), m=wax, bevel=0.008)
        k.cyl(0.004, 0.03, at=(x, 0, z + 0.36), rot=(0, 0, 0), m=wick)
        k.sphere(0.022, at=(x, 0, z + 0.4), scale=(1, 1, 1.8), m=flame)

    k.turn(4, -5, 0)
