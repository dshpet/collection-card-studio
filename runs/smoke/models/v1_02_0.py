# Leather saddle on a wooden fence rail: the rail runs through the saddle's gullet front to back, and the saddle
# straddles it. The red blanket lies on the rail top and drops down both sides. The leather skirts hang over it.
# The seat is one curved form, from the raised fork and horn at the front to the cantle at the back. A fender
# hangs on each side with a silver stirrup at its end. A cinch strap hangs from a metal ring on each skirt and
# ends free. The rail runs off the card both ways on posts that reach down past the card's bottom edge.
SCENE = {"category": "3", "backdrop": "#2fb8f0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8b4a22", "satin")
    seat_leather = k.mat("#9c5629", "satin")
    dark = k.mat("#6e3818", "satin")
    silver = k.mat("#cfd4da", "metal")
    red = k.mat("#d8322b", "matte")
    wood = k.mat("#c98a4b", "matte")
    post = k.mat("#a8703a", "matte")

    # blanket: top layer on the rail plus a panel down each side
    k.box((0.92, 0.27, 0.02), at=(0, 0, 0.01), m=red, bevel=0.006)
    for side in (-1, 1):
        k.box((0.92, 0.02, 0.36), at=(0, side * 0.125, -0.16), rot=(side * 6, 0, 0), m=red, bevel=0.01)
        # leather skirt over the blanket
        k.box((0.8, 0.03, 0.34), at=(0, side * 0.145, -0.15), rot=(side * 6, 0, 0), m=leather, bevel=0.03)
        # fender and stirrup
        k.box((0.16, 0.025, 0.5), at=(0.02, side * 0.172, -0.21), rot=(side * 6, 0, 0), m=dark, bevel=0.012)
        y = side * 0.2
        k.tube([(-0.065, y, -0.61), (-0.07, y, -0.52), (-0.04, y, -0.465), (0.02, y, -0.445),
                (0.08, y, -0.465), (0.11, y, -0.52), (0.105, y, -0.61)], 0.018, silver, curved=True)
        k.box((0.2, 0.08, 0.03), at=(0.02, y, -0.615), m=silver, bevel=0.008)
        k.cyl(0.02, 0.06, at=(0.02, y, -0.45), rot=(0, 90, 0), m=silver)
        # rigging ring with a cinch strap hanging free
        k.torus(0.04, 0.013, at=(-0.22, side * 0.178, -0.3), rot=(90, 0, 0), m=silver)
        k.box((0.07, 0.022, 0.32), at=(-0.22, side * 0.182, -0.49), m=dark, bevel=0.01)

    # seat: one curved form from the fork to the cantle
    balls = [(x, 0, 0.06, 0.09, (1.2, 1.7, 0.55)) for x in (-0.28, -0.14, 0.0, 0.14, 0.28)]
    balls.append((-0.3, 0, 0.13, 0.09, (0.9, 1.4, 1.2)))
    balls.append((0.32, 0, 0.15, 0.09, (0.55, 1.7, 1.3)))
    k.blob(balls, seat_leather)

    # horn on the fork
    k.lathe([(0.04, 0.0), (0.032, 0.04), (0.03, 0.08), (0.04, 0.1), (0.07, 0.115), (0.072, 0.13),
             (0.06, 0.145), (0.03, 0.152), (0.0, 0.154)], at=(-0.31, 0, 0.2), rot=(0, -12, 0), m=leather)

    # wooden fence rail on posts
    k.box((6, 0.22, 0.18), at=(0, 0, -0.09), m=wood, bevel=0.015, setting=True)
    for x in (-1.5, 1.5):
        k.box((0.24, 0.26, 3.0), at=(x, 0.0, -1.45), m=post, bevel=0.02, setting=True)
