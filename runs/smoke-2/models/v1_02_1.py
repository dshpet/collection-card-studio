# Western saddle hung over the top rail of a wooden plank fence: the rail runs along x through the saddle the way
# a horse's back would, the seat sits on it, and the skirts hang down both sides over a red blanket that shows only
# a thin edge past them. Each stirrup leather runs down the outside of its skirt and holds a silver stirrup
# hanging free below. The girth strap goes from one skirt, under the rail, to the other. The horn rises from the
# front fork. The rail and its posts run off the card both ways.
SCENE = {"category": "3", "backdrop": "#3cc8f0", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4a22", "matte")
    dark = k.mat("#5e3015", "matte")
    blanket = k.mat("#d4282c", "matte")
    silver = k.mat("#c9ced6", "metal")
    wood = k.mat("#b0703a", "matte")

    # Seat: low curved middle, rising cantle at the back (-x), fork at the front (+x), resting on the rail.
    k.blob([
        (-0.22, 0, 0.06, 0.12, (1.6, 1.55, 0.55)),
        (0.0, 0, 0.055, 0.12, (1.6, 1.5, 0.5)),
        (0.2, 0, 0.07, 0.12, (1.4, 1.45, 0.6)),
        (-0.36, 0, 0.16, 0.1, (0.55, 1.6, 1.05)),
        (0.3, 0, 0.13, 0.09, (0.8, 1.4, 1.0)),
    ], leather)

    # Horn on the fork: neck and a flat cap.
    k.cyl(0.032, 0.16, at=(0.33, 0, 0.27), rot=(0, 12, 0), m=dark, bevel=0.006)
    k.cyl(0.07, 0.035, at=(0.345, 0, 0.355), rot=(0, 12, 0), m=dark, bevel=0.012)

    # Red blanket under the saddle: top across the rail and a panel down each side, just larger than the skirts.
    k.box((0.79, 0.23, 0.016), at=(0, 0, 0.008), m=blanket, bevel=0.005)
    for s in (-1, 1):
        k.box((0.79, 0.016, 0.33), at=(0, s * 0.108, -0.14), rot=(s * 10, 0, 0), m=blanket, bevel=0.006)

    for s in (-1, 1):
        # Skirt hanging over the blanket.
        k.box((0.74, 0.026, 0.32), at=(0, s * 0.128, -0.12), rot=(s * 10, 0, 0), m=leather, bevel=0.02)
        # Stirrup leather: down the skirt, then hanging straight below it.
        k.box((0.1, 0.02, 0.36), at=(-0.03, s * 0.152, -0.12), rot=(s * 10, 0, 0), m=dark, bevel=0.006)
        k.box((0.075, 0.02, 0.25), at=(-0.03, s * 0.175, -0.4), m=dark, bevel=0.006)
        # Silver stirrup on the end of the leather.
        y = s * 0.175
        loop = [(-0.1, y, -0.72), (-0.095, y, -0.62), (-0.07, y, -0.545), (-0.03, y, -0.525),
                (0.01, y, -0.545), (0.035, y, -0.62), (0.04, y, -0.72)]
        k.tube(loop, 0.016, silver, curved=True)
        k.box((0.16, 0.08, 0.028), at=(-0.03, y, -0.725), m=silver, bevel=0.008)
        k.cyl(0.012, 0.05, at=(-0.03, y, -0.528), rot=(90, 0, 0), m=silver)
        # Girth strap down the outside of the skirt.
        k.box((0.06, 0.016, 0.3), at=(0.2, s * 0.155, -0.15), rot=(s * 10, 0, 0), m=dark, bevel=0.004)
        k.box((0.06, 0.016, 0.08), at=(0.2, s * 0.183, -0.33), m=dark, bevel=0.004)
        k.box((0.075, 0.02, 0.05), at=(0.2, s * 0.188, -0.29), m=silver, bevel=0.005)
    # Girth strap passing under the rail.
    k.box((0.06, 0.39, 0.016), at=(0.2, 0, -0.372), m=dark, bevel=0.004)

    # Fence: top plank rail with posts far off to each side.
    k.box((7, 0.15, 0.2), at=(0, 0, -0.1), m=wood, bevel=0.015, setting=True)
    k.box((7, 0.15, 0.2), at=(0, 0, -1.1), m=wood, bevel=0.015, setting=True)
    for x in (-1.5, 1.5):
        k.box((0.18, 0.18, 2.4), at=(x, 0.165, -0.95), m=k.mat("#9a5f30", "matte"), bevel=0.015, setting=True)
