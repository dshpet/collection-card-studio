# Western saddle on a fence rail: the seat sits across the top of a square wooden rail, which is nailed to the
# front of a post standing on the ground. The skirts hang down both sides of the rail; under them a fender hangs on
# each side, narrow at the top and wide at the bottom, and a short strap with a silver buckle carries the stirrup.
# The horn rises from the raised pommel at the front, the cantle curls up at the back, and the seat dips between.
# The rail runs off the card both ways and is left out of the framing.
SCENE = {"category": "3", "backdrop": "#3fd0e8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    T = 1.1  # top of the rail
    leather = k.mat("#8a4a22", "satin")
    tan = k.mat("#d29a5c", "matte")
    silver = k.mat("#c9ced6", "metal")
    rail_wood = k.mat("#c08a52", "matte")
    post_wood = k.mat("#a3703e", "matte")

    # Fence: top and lower rails nailed to the front of the posts, posts on the ground.
    k.box((6, 0.14, 0.16), at=(0, 0, T - 0.08), m=rail_wood, bevel=0.015, setting=True)
    k.box((6, 0.12, 0.14), at=(0, 0, 0.3), m=rail_wood, bevel=0.015, setting=True)
    for x in (0.72, -1.9):
        k.box((0.17, 0.17, T + 0.08), at=(x, 0.155, (T + 0.08) / 2), m=post_wood, bevel=0.02, setting=True)
    k.floor("#d9b27a")

    # Seat body: dips in the middle, raised pommel at the front (-x), curled cantle at the back (+x).
    balls = []
    for i in range(9):
        x = -0.32 + i * 0.08
        balls.append((x, 0, T + 0.02 + 0.06 * (x / 0.32) ** 2, 0.06, (1.2, 2.6, 0.7)))
    balls.append((-0.34, 0, T + 0.12, 0.07, (0.8, 1.6, 1.1)))
    balls.append((0.36, 0, T + 0.15, 0.06, (0.6, 2.4, 1.3)))
    k.blob(balls, leather)
    k.sphere(0.1, at=(0.02, 0, T + 0.07), scale=(1.9, 1.3, 0.3), m=tan)

    # Horn: a neck leaning forward with a flat cap.
    k.cyl(0.028, 0.13, at=(-0.37, 0, T + 0.24), rot=(0, -12, 0), m=leather)
    k.cyl(0.06, 0.03, at=(-0.384, 0, T + 0.304), rot=(0, -12, 0), m=leather, bevel=0.01)

    for s in (-1, 1):
        # Skirt hanging against the side of the rail.
        k.box((0.78, 0.03, 0.36), at=(0, s * 0.10, T - 0.12), rot=(s * 4, 0, 0), m=leather, bevel=0.012)
        # Fender, tapering wider toward the bottom.
        fender = k.box((0.16, 0.025, 0.46), at=(-0.03, s * 0.142, T - 0.17), m=leather, bevel=0.008)
        k.warp(fender, lambda p: (p[0] * (0.75 + 0.5 * (0.5 - p[2] / 0.46)), p[1], p[2]))
        # Stirrup leather with its buckle.
        y = s * 0.142
        k.box((0.07, 0.035, 0.09), at=(-0.03, y, T - 0.385), m=leather, bevel=0.006)
        bx, by, bz = -0.03, s * 0.165, T - 0.375
        k.tube([(bx - 0.03, by, bz - 0.022), (bx + 0.03, by, bz - 0.022), (bx + 0.03, by, bz + 0.022),
                (bx - 0.03, by, bz + 0.022), (bx - 0.03, by, bz - 0.022)], 0.01, silver)
        k.cyl(0.006, 0.044, at=(bx, by, bz), m=silver)
        # Stirrup: an arch with a flat tread, hanging from the strap.
        z0 = T - 0.60
        arch = [(-0.08, 0, 0), (-0.085, 0, 0.10), (-0.05, 0, 0.165), (0, 0, 0.18), (0.05, 0, 0.165),
                (0.085, 0, 0.10), (0.08, 0, 0)]
        k.tube([(-0.03 + ax, y, z0 + az) for ax, _, az in arch], 0.018, tan, curved=True)
        k.box((0.18, 0.09, 0.035), at=(-0.03, y, z0), m=tan, bevel=0.01)
