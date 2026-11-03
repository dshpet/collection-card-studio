# Steam train: a black locomotive stands on a desert track. Three pairs of large red driving wheels and a small
# front pair sit on the rails and turn on axles in the frame; coupling rods join the crank pins, and a main rod runs
# from each cylinder to the middle wheel. The boiler lies on the running board with the smokebox in front, carrying
# the tall funnel chimney and the round lamp; the steam dome and the gold bell sit on top, and the cab closes the
# rear. The cowcatcher hangs from the front beam. The tender behind runs off the card, as does the track.
SCENE = {"category": "4", "backdrop": "#7fc8f0", "azimuth": 32, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    black, gray = k.mat("#1c1d21", "satin"), k.mat("#3d4047", "satin")
    red, gold = k.mat("#d8262b", "satin"), k.mat("#e8b83a", "metal")
    steel = k.mat("#8b8f96", "metal")
    rail = 0.12  # rail top
    gauge = 0.27

    # Wheels: red discs on the rails with dark hubs, an axle through the frame.
    def wheel(y, r, framed=True):
        parts = []
        z = rail + r
        for s in (-1, 1):
            parts.append(k.cyl(r, 0.05, at=(s * gauge, y, z), rot=(0, 90, 0), m=red, bevel=0.008))
            parts.append(k.cyl(r * 0.3, 0.07, at=(s * gauge, y, z), rot=(0, 90, 0), m=gray))
        parts.append(k.cyl(0.03, 2 * gauge, at=(0, y, z), rot=(0, 90, 0), m=steel))
        if not framed:
            k.unframed(*parts)
        return z

    rd = 0.19
    drivers = (-0.08, 0.32, 0.72)
    for y in drivers:
        zc = wheel(y, rd)
    wheel(-0.5, 0.11)

    # Crank pins, coupling rods and main rods.
    pin_z = zc - 0.09
    for s in (-1, 1):
        for y in drivers:
            k.cyl(0.022, 0.04, at=(s * 0.31, y, pin_z), rot=(0, 90, 0), m=steel)
        k.box((0.025, 0.86, 0.045), at=(s * 0.325, 0.32, pin_z), m=steel, bevel=0.008)
        k.cyl(0.09, 0.26, at=(s * 0.36, -0.42, 0.42), rot=(90, 0, 0), m=black, bevel=0.01)
        k.tube([(s * 0.35, -0.29, 0.42), (s * 0.35, 0.32, pin_z)], 0.018, steel)

    # Frame and running board.
    k.box((0.36, 1.5, 0.14), at=(0, 0.08, 0.36), m=gray, bevel=0.01)
    k.box((0.78, 1.56, 0.03), at=(0, 0.08, 0.475), m=black, bevel=0.006)

    # Boiler and smokebox.
    bz = 0.49 + 0.235
    k.cyl(0.235, 0.87, at=(0, 0.035, bz), rot=(90, 0, 0), m=black, bevel=0.01)
    k.cyl(0.25, 0.26, at=(0, -0.53, bz), rot=(90, 0, 0), m=gray, bevel=0.012)
    k.cyl(0.2, 0.02, at=(0, -0.665, bz), rot=(90, 0, 0), m=gray, bevel=0.006)
    k.cyl(0.025, 0.03, at=(0, -0.68, bz), rot=(90, 0, 0), m=steel)
    top = bz + 0.25

    # Tall funnel chimney, flaring at the top.
    k.lathe([(0.075, 0), (0.07, 0.1), (0.075, 0.18), (0.1, 0.25), (0.13, 0.3), (0.145, 0.33), (0.145, 0.36),
             (0.12, 0.36), (0.0, 0.36)], at=(0, -0.45, top - 0.04), m=black)

    # Round lamp on its bracket at the front of the smokebox.
    k.box((0.09, 0.08, 0.06), at=(0, -0.6, top), m=gray, bevel=0.008)
    k.cyl(0.065, 0.1, at=(0, -0.6, top + 0.085), rot=(90, 0, 0), m=black, bevel=0.008)
    k.cyl(0.052, 0.01, at=(0, -0.653, top + 0.085), rot=(90, 0, 0), m=k.mat("#ffe38a", "glow"))

    # Steam dome and gold bell on the boiler.
    btop = bz + 0.235
    k.lathe([(0.12, 0), (0.11, 0.06), (0.1, 0.1), (0.08, 0.13), (0.04, 0.15), (0, 0.155)],
            at=(0, -0.08, btop - 0.03), m=black)
    k.cyl(0.03, 0.05, at=(0, 0.2, btop + 0.01), m=gray)
    k.lathe([(0.055, 0), (0.05, 0.012), (0.04, 0.03), (0.032, 0.06), (0.03, 0.08), (0.015, 0.09), (0, 0.092)],
            at=(0, 0.2, btop + 0.035), m=gold)

    # Front beam and cowcatcher.
    k.box((0.78, 0.06, 0.1), at=(0, -0.7, 0.42), m=red, bevel=0.01)
    for x in (-0.3, -0.18, -0.06, 0.06, 0.18, 0.3):
        k.tube([(x, -0.72, 0.38), (x * 0.6, -0.88, rail + 0.02)], 0.016, gray)
    k.tube([(-0.18, -0.88, rail + 0.02), (0.18, -0.88, rail + 0.02)], 0.016, gray)

    # Cab: lower walls, front wall with round windows, corner posts and a roof.
    k.box((0.78, 0.39, 0.3), at=(0, 0.665, 0.64), m=black, bevel=0.01)
    k.box((0.78, 0.04, 0.58), at=(0, 0.49, 0.78), m=black, bevel=0.01)
    for x in (-0.24, 0.24):
        k.cyl(0.065, 0.012, at=(x, 0.468, 0.95), rot=(90, 0, 0), m=k.mat("#2b3440", "glass"))
    for x in (-0.36, 0.36):
        for y in (0.49, 0.665, 0.84):
            k.box((0.05, 0.05, 0.28), at=(x, y, 0.93), m=black, bevel=0.006)
    k.box((0.88, 0.5, 0.04), at=(0, 0.665, 1.09), m=gray, bevel=0.015)

    # Tender behind, coupled by a drawbar; it runs off the card.
    tender = [k.box((0.08, 0.1, 0.05), at=(0, 0.9, 0.36), m=gray)]
    tender.append(k.box((0.36, 0.66, 0.14), at=(0, 1.26, 0.36), m=gray, bevel=0.01))
    tender.append(k.box((0.76, 0.7, 0.44), at=(0, 1.27, 0.66), m=black, bevel=0.012))
    tender.append(k.blob([(0, 1.2, 0.88, 0.16, (2.0, 1.6, 0.5)), (0.1, 1.38, 0.88, 0.14, (1.8, 1.4, 0.5))], gray))
    k.unframed(*tender)
    for y in (1.06, 1.46):
        wheel(y, 0.11, framed=False)

    # Desert track and ground, mesas far back.
    k.floor("#e8b97a")
    k.box((1.1, 14, 0.04), at=(0, 0, 0.02), m=k.mat("#b89272", "matte"), bevel=0.01, setting=True)
    for i in range(56):
        k.box((0.8, 0.1, 0.035), at=(0, -7 + i * 0.25, 0.0575), m=k.mat("#7a5232", "matte"), bevel=0.006,
              setting=True)
    for s in (-1, 1):
        k.box((0.04, 14, 0.045), at=(s * gauge, 0, rail - 0.0225), m=steel, bevel=0.004, setting=True)
    sand = k.mat("#d98a4e", "matte")
    k.cone(1.6, 1.1, 0.9, at=(-4.5, 7, 0.45), rot=(0, 0, 0), m=sand, setting=True)
    k.cone(1.2, 0.8, 0.6, at=(-1.2, 9, 0.3), rot=(0, 0, 0), m=sand, setting=True)
    k.cone(2.2, 1.6, 1.1, at=(-7.5, 4, 0.55), rot=(0, 0, 0), m=sand, setting=True)
