# Western saddle astride the top rail of a wooden fence. The rail runs along the saddle's length; the bridge under
# the seat rests on the rail top, and rounded leather skirts hang down both sides from the bridge edges. A fender lies
# on the outer face of each skirt, hangs past its hem and wraps around the top bar of a stirrup; the stirrup's arched
# sides come down to a wide silver tread. The horn rises from the pommel at the front, the cantle curls up high at the
# back, and gold piping runs along the stitched seat edges. The rails run into two posts that reach the ground, both
# off the card; the framing holds the saddle.
import math

SCENE = {"category": "3", "backdrop": "#3cc8e8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4a22", "satin")
    dark = k.mat("#5e2f14", "satin")
    gold = k.mat("#e8b84a", "satin")
    silver = k.mat("#cfd4da", "metal")
    wood = k.mat("#d99a4a", "matte")

    rail_top = 1.0

    # Fence: top rail under the saddle, a lower rail, and posts down to the ground.
    k.box((4.2, 0.14, 0.18), at=(0, 0, rail_top - 0.09), m=wood, bevel=0.015, setting=True)
    k.box((4.2, 0.12, 0.16), at=(0, 0.01, 0.42), m=wood, bevel=0.015, setting=True)
    for x in (-1.45, 1.45):
        k.box((0.2, 0.2, 1.12), at=(x, 0.02, 0.56), m=wood, bevel=0.02, setting=True)

    # Bridge under the seat, resting on the rail top.
    k.box((0.78, 0.38, 0.04), at=(0, 0, rail_top + 0.02), m=dark, bevel=0.012)

    # Seat, pommel and cantle as one soft leather form.
    def seat_z(x):
        return 1.085 + 0.35 * x * x

    balls = []
    for i in range(13):
        x = -0.30 + i * 0.05
        balls.append((x, 0, seat_z(x), 0.09, (1.0, 2.3, 0.6)))
    balls += [
        (-0.34, 0, 1.15, 0.09, (0.8, 1.7, 1.0)),
        (-0.37, 0, 1.19, 0.07, (0.8, 1.3, 1.0)),
        (0.31, 0, 1.17, 0.08, (0.5, 2.2, 1.0)),
        (0.35, 0, 1.24, 0.08, (0.45, 2.1, 1.0)),
        (0.38, 0, 1.31, 0.075, (0.4, 1.9, 0.9)),
        (0.40, 0, 1.36, 0.06, (0.4, 1.8, 0.8)),
    ]
    k.blob(balls, leather)

    # Horn: neck and flat cap above the pommel, tipped slightly forward.
    k.cyl(0.035, 0.14, at=(-0.38, 0, 1.28), rot=(0, -10, 0), m=leather, bevel=0.01)
    k.cyl(0.075, 0.035, at=(-0.395, 0, 1.355), rot=(0, -10, 0), m=dark, bevel=0.012)

    # Gold stitched piping along both seat edges, sitting on the seat's outer rim.
    for s in (-1, 1):
        pts = [(-0.27 + i * 0.045, s * 0.192, seat_z(-0.27 + i * 0.045) + 0.028) for i in range(13)]
        k.tube(pts, 0.014, gold, curved=True)

    t15 = math.tan(math.radians(15))

    def skirt_shape(p):
        x, y, z = p
        return (x, min(y * 0.5, 0.14), z)

    for s in (-1, 1):
        # Skirt: a rounded leather flap hanging down the side of the rail from the bridge edge.
        skirt = k.cyl(0.42, 0.02, at=(0, s * 0.235, 0.86), rot=(90 + s * 15, 0, 0), m=leather, bevel=0.006)
        k.warp(skirt, skirt_shape)
        # Fender lying on the skirt's outer face, from under the bridge edge down past the hem to the stirrup.
        x0 = -0.03
        face_y = 0.235 + 0.021 / math.cos(math.radians(15))
        z_top, z_bot = 1.0, 0.55
        zc = (z_top + z_bot) / 2
        yc = face_y + (0.86 - zc) * t15
        length = (z_top - z_bot) / math.cos(math.radians(15))
        k.box((0.18, 0.022, length), at=(x0, s * yc, zc), rot=(s * 15, 0, 0), m=dark, bevel=0.008)
        # Stirrup: top bar wrapped by the fender end, arched sides, and a wide silver tread.
        y = s * (face_y + (0.86 - z_bot) * t15)
        k.cyl(0.026, 0.2, at=(x0, y, 0.548), rot=(0, 90, 0), m=dark, bevel=0.006)
        for d in (-1, 1):
            side = [(x0 + d * 0.09, y, 0.548), (x0 + d * 0.115, y, 0.48),
                    (x0 + d * 0.12, y, 0.41), (x0 + d * 0.108, y, 0.36)]
            k.tube(side, 0.022, leather, curved=True)
            k.cyl(0.03, 0.03, at=(x0 + d * 0.101, y, 0.548), rot=(0, 90, 0), m=silver, bevel=0.005)
        k.box((0.26, 0.11, 0.032), at=(x0, y, 0.352), m=silver, bevel=0.01)
