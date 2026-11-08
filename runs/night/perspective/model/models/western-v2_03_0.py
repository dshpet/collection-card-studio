# Harmonica: a comb sits between a top and a bottom silver cover plate. The front of the comb shows a row of ten
# square holes, cut between the comb's teeth into a dark channel behind them. Two red curved end covers clamp
# the left and right ends of the plates and comb. Floating, tilted a little so the hole row and the top both show.
SCENE = {"category": "1", "backdrop": "#3fd6e8", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#cfd4dc", "metal")
    comb = k.mat("#aeb4bd", "metal")
    dark = k.mat("#2a2d33", "satin")
    red = k.mat("#e0262f", "gloss")

    L, D = 0.86, 0.26          # plate length (x) and depth (y)
    # Comb: a dark channel block set back from the front; the teeth and two rails form the hole row.
    k.box((L - 0.02, D - 0.06, 0.07), at=(0, 0.01, 0), m=dark, bevel=0.003)
    k.box((L - 0.02, 0.03, 0.014), at=(0, -0.105, 0.028), m=comb, bevel=0.003)
    k.box((L - 0.02, 0.03, 0.014), at=(0, -0.105, -0.028), m=comb, bevel=0.003)
    n, hole = 10, 0.05
    pitch = (L - 0.02) / n
    for i in range(n + 1):
        x = -(L - 0.02) / 2 + i * pitch
        k.box((pitch - hole, 0.03, 0.07), at=(x, -0.105, 0), m=comb, bevel=0.003)

    # Top and bottom cover plates, rounded and slightly domed.
    for s in (1, -1):
        plate = k.box((L, D, 0.05), at=(0, 0, s * 0.06), m=silver, bevel=0.02)
        k.warp(plate, lambda p, s=s: (p[0], p[1], p[2] + s * 0.012 * (1 - (p[1] / 0.13) ** 2)
                                      if s * p[2] > 0 else p[2]))
        k.box((L - 0.04, D + 0.004, 0.012), at=(0, 0, s * 0.036), m=silver, bevel=0.004)

    # Red curved end covers clamping each end.
    for side in (-1, 1):
        cap = k.cyl(0.12, D + 0.03, at=(side * 0.45, 0, 0), rot=(90, 0, 0), m=red, bevel=0.015)
        k.warp(cap, lambda p: (p[0] * 0.6, p[1], p[2]))
        k.box((0.06, D + 0.03, 0.2), at=(side * 0.42, 0, 0), m=red, bevel=0.015)

    k.turn(12, 10, 0)
