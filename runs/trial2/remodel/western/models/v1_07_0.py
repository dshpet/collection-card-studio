# Western saddle resting across a wooden fence rail. The seat dips between the raised front fork, which carries
# the horn (neck + flat cap), and the raised cantle at the back. Under the seat a skirt hangs down each side of the
# rail; over each skirt a tan fender hangs from under the seat, wraps the top bar of its stirrup at the bottom, and
# the stirrup dangles free. A small silver buckle sits on the near fender. The rail runs off the card both ways on
# posts that stand far outside the frame.
import math

SCENE = {"category": "3", "backdrop": "#3cc8e8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    chestnut = k.mat("#8a3f1d", "matte")
    dark = k.mat("#6e3016", "matte")
    tan = k.mat("#c98a4b", "matte")
    silver = k.mat("#d4d8de", "metal")
    wood = k.mat("#a8875f", "matte")

    # Fence rail (the named surface): top at z = 0.6, running far past the saddle onto posts off the card.
    k.box((5.0, 0.16, 0.14), at=(0, 0, 0.53), m=wood, bevel=0.015, setting=True)
    for x in (-1.6, 1.6):
        k.box((0.18, 0.18, 1.0), at=(x, 0, -0.04), m=wood, bevel=0.015, setting=True)

    # Seat: a dished leather shell, low in the middle, rising into the fork (front, -x) and the cantle (back, +x).
    balls = []
    for i in range(7):
        x = -0.24 + i * 0.08
        balls.append((x, 0, 0.632 + 0.35 * x * x, 0.1, (1.0, 1.5, 0.5)))
    balls.append((-0.29, 0, 0.70, 0.1, (0.75, 1.2, 0.9)))   # fork / pommel
    balls.append((0.31, 0, 0.715, 0.1, (0.5, 1.7, 0.85)))   # cantle
    k.blob(balls, chestnut)

    # Horn on top of the fork: a neck and a flat cap.
    k.cyl(0.026, 0.1, at=(-0.30, 0, 0.82), m=dark, bevel=0.006)
    k.cyl(0.055, 0.026, at=(-0.30, 0, 0.88), m=chestnut, bevel=0.01)

    tilt = math.degrees(math.atan(0.13))
    for side in (-1, 1):
        # Skirt: hangs from under the seat down the side of the rail, leaning slightly outward.
        k.box((0.72, 0.02, 0.28), at=(0.0, side * 0.112, 0.475), rot=(side * tilt, 0, 0), m=chestnut, bevel=0.03)

        # Fender: tapered tan leather lying on the skirt, wider at the bottom.
        fy = side * (0.095 + 0.19 * 0.13 + 0.022)
        fender = k.box((0.15, 0.02, 0.38), at=(0.03, fy, 0.42), rot=(side * tilt, 0, 0), m=tan, bevel=0.01)
        k.warp(fender, lambda p: (p[0] * (1.0 - 1.6 * p[2]), p[1], p[2]))

        # Stirrup: a loop in the y-z plane under the fender bottom; the fender wraps its top bar.
        y0 = side * (0.095 + 0.38 * 0.13 + 0.022)
        k.cyl(0.016, 0.1, at=(0.03, y0, 0.215), rot=(0, 90, 0), m=dark)
        for dx in (-0.022, 0.022):
            arch = [(0.03 + dx, y0 - 0.02, 0.212), (0.03 + dx, y0 - 0.06, 0.16), (0.03 + dx, y0 - 0.07, 0.08),
                    (0.03 + dx, y0, 0.07), (0.03 + dx, y0 + 0.07, 0.08), (0.03 + dx, y0 + 0.06, 0.16),
                    (0.03 + dx, y0 + 0.02, 0.212)]
            k.tube(arch, 0.017, tan, curved=True)
        k.box((0.08, 0.13, 0.026), at=(0.03, y0, 0.072), m=dark, bevel=0.008)

    # Small silver buckle on the near fender.
    by = -(0.095 + 0.11 * 0.13 + 0.022 + 0.012)
    k.box((0.05, 0.012, 0.038), at=(0.03, by, 0.50), rot=(-tilt, 0, 0), m=silver, bevel=0.005)
