# Western saddle astride the top rail of a wooden fence. The rail runs along the saddle's length; the bridge under
# the seat rests on the rail top, and the skirts hang down both sides from the bridge edges. A fender lies on the
# outer face of each skirt, hangs past its hem and wraps around the top bar of a stirrup, whose tread is silver. The
# horn rises from the pommel at the front, the cantle curls up high at the back, and gold piping runs along the
# stitched seat edges. The rails run into two posts that reach the ground, both off the card; the framing holds the
# saddle.
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

    # Gold stitched piping along both seat edges.
    for s in (-1, 1):
        pts = [(-0.28 + i * 0.04, s * 0.17, seat_z(-0.28 + i * 0.04) + 0.035) for i in range(15)]
        k.tube(pts, 0.012, gold, curved=True)

    t15 = math.tan(math.radians(15))
    for s in (-1, 1):
        # Skirt hanging down the side of the rail from the bridge edge.
        k.box((0.82, 0.02, 0.34), at=(0, s * 0.235, 0.86), rot=(s * 15, 0, 0), m=leather, bevel=0.01)
        # Fender lying on the skirt's outer face, from under the bridge edge down past the hem to the stirrup.
        x0 = -0.03
        face_y = 0.235 + 0.021 / math.cos(math.radians(15))
        z_top, z_bot = 1.0, 0.55
        zc = (z_top + z_bot) / 2
        yc = face_y + (0.86 - zc) * t15
        length = (z_top - z_bot) / math.cos(math.radians(15))
        k.box((0.17, 0.022, length), at=(x0, s * yc, zc), rot=(s * 15, 0, 0), m=dark, bevel=0.008)
        # Stirrup: top bar wrapped by the fender end, a leather loop, and a silver tread.
        y = s * (face_y + (0.86 - z_bot) * t15)
        k.cyl(0.024, 0.19, at=(x0, y, 0.548), rot=(0, 90, 0), m=dark, bevel=0.006)
        loop = [(x0 - 0.06, y, 0.55), (x0 - 0.095, y, 0.47), (x0 - 0.095, y, 0.395),
                (x0 + 0.095, y, 0.395), (x0 + 0.095, y, 0.47), (x0 + 0.06, y, 0.55), (x0 - 0.06, y, 0.55)]
        k.tube(loop, 0.02, leather)
        k.box((0.21, 0.09, 0.03), at=(x0, y, 0.385), m=silver, bevel=0.008)
        for dx in (-0.095, 0.095):
            k.sphere(0.026, at=(x0 + dx, y, 0.47), m=silver)
