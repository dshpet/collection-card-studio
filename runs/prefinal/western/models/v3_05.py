# Western saddle on a fence rail: the saddle's spine runs along the rail (x), horn at -x, high cantle at +x.
# The seat rests on the rail's top (z = 1.0). The skirts hang from the seat edge and flare out over both sides.
# A leather fender starts under the seat on each side, lies flat on the skirt and runs below it. The fender's
# lower end holds the silver crossbar of a stirrup: a leather arch with a wide silver tread, hanging in the
# fender's plane. The rail runs off the card both ways onto two posts that stand on the ground below the frame.
import math

SCENE = {"category": "3", "backdrop": "#2fc4e8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4f24", "matte")
    dark = k.mat("#5e3416", "matte")
    seat = k.mat("#a8653a", "matte")
    silver = k.mat("#d3d7de", "metal")
    wood = k.mat("#a8743f", "matte")

    # Fence: a long square rail, top at z = 1.0, on two posts off the card.
    k.unframed(k.box((6.0, 0.14, 0.14), at=(0, 0, 0.93), m=wood, bevel=0.012, setting=True))
    for x in (-1.5, 1.5):
        k.unframed(k.box((0.18, 0.18, 1.12), at=(x, 0.0, 0.5), m=wood, bevel=0.015, setting=True))

    # Saddle tree: seat, rising pommel at the front, high cantle at the back, as one leather form.
    k.blob([
        (0.0, 0.0, 1.075, 0.26, (1.65, 1.0, 0.3)),
        (-0.34, 0.0, 1.11, 0.16, (0.8, 0.95, 0.65)),
        (0.36, 0.0, 1.16, 0.2, (0.38, 1.05, 0.75)),
    ], leather)
    # Stitched seat panel lying on the seat's top (stitching left to the restyle).
    k.blob([(0.03, 0.0, 1.152, 0.2, (1.35, 0.9, 0.12))], seat)
    # Horn: neck rising from the pommel, flat round cap.
    k.cyl(0.04, 0.16, at=(-0.40, 0, 1.22), rot=(0, -12, 0), m=leather, bevel=0.01)
    k.cyl(0.075, 0.035, at=(-0.418, 0, 1.30), rot=(0, -12, 0), m=dark, bevel=0.012)

    tilt = 10.0
    s, c = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    for side in (-1, 1):
        # Skirt: top edge tucked under the seat edge, flaring outward as it hangs.
        k.box((0.80, 0.035, 0.30), at=(0.02, side * (0.24 + 0.15 * s), 1.07 - 0.15 * c),
              rot=(side * tilt, 0, 0), m=dark, bevel=0.025)
        # Fender: starts under the seat, lies on the skirt, runs below it.
        top_y, top_z, length = 0.27, 1.06, 0.45
        k.box((0.17, 0.035, length), at=(0.0, side * (top_y + length / 2 * s), top_z - length / 2 * c),
              rot=(side * tilt, 0, 0), m=leather, bevel=0.012)
        by, bz = side * (top_y + length * s), top_z - length * c
        # Stirrup in the fender's plane: silver crossbar through the fender's end, leather arch, silver tread.
        k.cyl(0.02, 0.13, at=(0.0, by, bz - 0.005), rot=(0, 90, 0), m=silver, bevel=0.005)
        for sx in (-1, 1):
            k.tube([(sx * 0.055, by, bz - 0.005), (sx * 0.08, by, bz - 0.07),
                    (sx * 0.088, by, bz - 0.14), (sx * 0.08, by, bz - 0.18)], 0.02, leather, curved=True)
        k.box((0.19, 0.10, 0.03), at=(0.0, by, bz - 0.19), m=silver, bevel=0.008)
