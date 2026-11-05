# Leather saddle on a wooden fence rail: the rail runs through the saddle's gullet front to back, and the saddle
# straddles it. A thin red blanket lies on the rail top and drops down both sides, showing only a narrow edge
# around the rounded leather skirts. The seat is one curved form: a wide swelled fork with the horn at the front,
# a dished seat, and a low curved cantle at the back. A wide fender hangs on each side, narrowing into a stirrup
# leather that holds a silver stirrup. A cinch strap hangs from a metal ring on each skirt and ends free. The
# rail runs off the card both ways on posts that reach down past the card's bottom edge.
SCENE = {"category": "3", "backdrop": "#2fb8f0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def rounded_panel(k, w, h, t, at, rot, m, p=4.0):
    # a flat rounded-rectangle panel: a thin lathe disk warped into a superellipse
    part = k.lathe([(0.0, 0.0), (1.0, 0.0), (1.0, t), (0.0, t)], at=at, rot=rot, m=m, verts=96)

    def shape(v):
        x, y, z = v
        r = (x * x + y * y) ** 0.5
        if r < 1e-6:
            return (0.0, 0.0, z - t / 2)
        c, s = x / r, y / r
        f = 1.0 / (abs(c) ** p + abs(s) ** p) ** (1.0 / p)
        return (x * f * w / 2, y * f * h / 2, z - t / 2)

    k.warp(part, shape)
    return part


def build(k):
    leather = k.mat("#8a4720", "satin")
    seat_leather = k.mat("#9c5629", "satin")
    dark = k.mat("#6a3416", "satin")
    silver = k.mat("#cfd4da", "metal")
    red = k.mat("#d8322b", "matte")
    wood = k.mat("#c98a4b", "matte")
    post = k.mat("#a8703a", "matte")

    # blanket top lying across the rail
    k.box((0.82, 0.25, 0.016), at=(0, 0, 0.008), m=red, bevel=0.005)
    for side in (-1, 1):
        tilt = (90 + side * 6, 0, 0)
        # blanket side panel, a little larger than the skirt so a red edge shows
        rounded_panel(k, 0.82, 0.36, 0.014, at=(0, side * 0.122, -0.15), rot=tilt, m=red)
        # rounded leather skirt over the blanket
        rounded_panel(k, 0.74, 0.32, 0.026, at=(0, side * 0.142, -0.14), rot=tilt, m=leather)

        # wide fender, tapering up into the seat and widening toward the bottom
        fender = k.box((0.14, 0.024, 0.42), at=(0.02, side * 0.168, -0.15), rot=(side * 6, 0, 0), m=dark,
                       bevel=0.01)
        k.warp(fender, lambda v: (v[0] * (1.0 + 0.9 * max(0.0, -v[2]) / 0.21), v[1], v[2]))
        # stirrup leather from the fender down to the stirrup bar
        y = side * 0.196
        k.box((0.05, 0.02, 0.1), at=(0.02, y, -0.40), m=dark, bevel=0.006)
        # stirrup
        k.tube([(-0.065, y, -0.61), (-0.07, y, -0.52), (-0.04, y, -0.465), (0.02, y, -0.445),
                (0.08, y, -0.465), (0.11, y, -0.52), (0.105, y, -0.61)], 0.018, silver, curved=True)
        k.box((0.2, 0.08, 0.03), at=(0.02, y, -0.615), m=silver, bevel=0.008)
        k.cyl(0.02, 0.07, at=(0.02, y, -0.45), rot=(0, 90, 0), m=silver)

        # rigging ring on the skirt with a cinch strap hanging free
        k.torus(0.04, 0.013, at=(-0.24, side * 0.18, -0.27), rot=(90, 0, 0), m=silver)
        k.box((0.07, 0.022, 0.30), at=(-0.24, side * 0.184, -0.45), m=dark, bevel=0.01)

    # seat: swelled fork at the front, dished seat, low curved cantle at the back
    balls = [(x, 0, 0.05, 0.09, (1.2, 1.6, 0.5)) for x in (-0.16, -0.02, 0.12)]
    balls.append((-0.27, 0, 0.11, 0.09, (0.8, 1.8, 0.95)))   # fork swell
    balls.append((0.22, 0, 0.08, 0.09, (0.8, 1.6, 0.65)))    # rise to the cantle
    balls.append((0.29, 0, 0.12, 0.09, (0.45, 1.65, 0.95)))  # cantle
    k.blob(balls, seat_leather)

    # horn rising from the fork
    k.lathe([(0.05, 0.0), (0.035, 0.03), (0.03, 0.06), (0.036, 0.08), (0.06, 0.092), (0.062, 0.105),
             (0.05, 0.117), (0.025, 0.122), (0.0, 0.123)], at=(-0.29, 0, 0.18), rot=(0, -12, 0), m=leather)

    # wooden fence rail on posts
    k.box((6, 0.22, 0.18), at=(0, 0, -0.09), m=wood, bevel=0.015, setting=True)
    for x in (-1.5, 1.5):
        k.box((0.24, 0.26, 3.0), at=(x, 0.0, -1.45), m=post, bevel=0.02, setting=True)
