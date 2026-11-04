# Steam locomotive (4-4-0) on a desert track, length along y with the smokebox front facing -y. Two pairs of large
# red drivers and a four-wheel leading truck sit on the rail tops (z = 0.07); driver axles pass through a deep frame,
# truck axles through a truck frame bolted under it. A side rod couples the drivers' crank pins, and a main rod runs
# from the crosshead behind each steam cylinder to the rear driver's pin. The running board rests on the frame above
# the drivers; the boiler, smokebox and cab stand on it. The funnel, steam dome and bell yoke sit on the boiler top,
# the round lamp on a block atop the smokebox, the gold bell hangs on an axle between two posts. A gray pilot wedge
# hangs from the red buffer beam. The tender couples behind the cab and is left out of the framing; rails and ties run off.
import math

SCENE = {"category": "4", "backdrop": "#5bb8ee", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#1d1f23", "satin")
    gray = k.mat("#3c4047", "satin")
    steel = k.mat("#6d727a", "metal")
    red = k.mat("#d52a22", "satin")
    gold = k.mat("#f0b833", "metal")
    glass = k.mat("#2b3d52", "glass")
    lamp = k.mat("#fff1b0", "glow")

    rail_top = 0.07

    # Wheels standing on the rails at x = +-0.2.
    def wheel(y, r, side):
        x = side * 0.2
        z = rail_top + r
        k.cyl(r, 0.045, at=(x, y, z), rot=(0, 90, 0), m=red, bevel=0.008)
        k.cyl(r * 0.3, 0.055, at=(x + side * 0.005, y, z), rot=(0, 90, 0), m=black, bevel=0.005)
        return z

    drivers = (0.0, 0.36)
    truck = (-0.52, -0.33)
    rd, rp = 0.16, 0.075
    zd = rail_top + rd
    zpin = zd + 0.07
    for side in (-1, 1):
        for y in drivers:
            wheel(y, rd, side)
            k.cyl(0.022, 0.08, at=(side * 0.25, y, zpin), rot=(0, 90, 0), m=steel)
        for y in truck:
            wheel(y, rp, side)
    for y in drivers:
        k.cyl(0.025, 0.4, at=(0, y, zd), rot=(0, 90, 0), m=steel)
    for y in truck:
        k.cyl(0.02, 0.4, at=(0, y, rail_top + rp), rot=(0, 90, 0), m=steel)
    # leading-truck frame, bolted up into the main frame
    k.box((0.3, 0.34, 0.05), at=(0, -0.425, 0.165), m=black, bevel=0.008)

    # Main frame between the wheels, and the running board on top of it, above the drivers.
    k.box((0.26, 1.3, 0.24), at=(0, 0.0, 0.29), m=black, bevel=0.01)
    k.box((0.6, 1.0, 0.025), at=(0, -0.13, 0.4125), m=black, bevel=0.006)
    # red buffer beam with two buffers, and a gray pilot wedge hanging from its underside
    k.box((0.6, 0.06, 0.12), at=(0, -0.66, 0.35), m=red, bevel=0.01)
    for side in (-1, 1):
        k.cyl(0.03, 0.06, at=(side * 0.2, -0.71, 0.37), rot=(90, 0, 0), m=steel)
    k.box((0.44, 0.035, 0.235), at=(0, -0.745, 0.2), rot=(-40, 0, 0), m=gray, bevel=0.01)

    # Steam cylinders under the running board, piston rods, crossheads, main and side rods.
    for side in (-1, 1):
        cx = side * 0.3
        k.cyl(0.07, 0.2, at=(cx, -0.42, 0.33), rot=(90, 0, 0), m=gray, bevel=0.01)
        k.cyl(0.02, 0.1, at=(cx, -0.28, 0.33), rot=(90, 0, 0), m=steel)
        k.box((0.04, 0.05, 0.05), at=(cx, -0.23, 0.33), m=steel, bevel=0.005)
        k.box((0.02, 0.42, 0.035), at=(side * 0.262, 0.18, zpin), m=steel, bevel=0.005)
        k.tube([(side * 0.29, -0.23, 0.33), (side * 0.285, 0.36, zpin)], 0.02, steel)

    # Boiler, smokebox, its saddle and door.
    bz = 0.425 + 0.17
    k.cyl(0.17, 0.82, at=(0, -0.08, bz), rot=(90, 0, 0), m=black, bevel=0.01)
    for y in (-0.3, -0.05, 0.2):
        k.cyl(0.175, 0.02, at=(0, y, bz), rot=(90, 0, 0), m=gray, bevel=0.004)
    k.cyl(0.18, 0.2, at=(0, -0.53, bz), rot=(90, 0, 0), m=gray, bevel=0.012)
    k.box((0.3, 0.2, 0.06), at=(0, -0.53, 0.45), m=gray, bevel=0.01)
    k.cyl(0.15, 0.025, at=(0, -0.64, bz), rot=(90, 0, 0), m=black, bevel=0.01)
    k.cyl(0.03, 0.04, at=(0, -0.66, bz), rot=(90, 0, 0), m=steel)
    # handrails on stanchions
    for side in (-1, 1):
        k.tube([(side * 0.19, -0.5, bz + 0.07), (side * 0.19, 0.28, bz + 0.07)], 0.018, steel)
        for y in (-0.45, -0.1, 0.25):
            k.tube([(side * 0.15, y, bz + 0.07), (side * 0.19, y, bz + 0.07)], 0.012, steel)

    # Round front lamp on a block atop the smokebox.
    top = bz + 0.18
    k.box((0.09, 0.08, 0.05), at=(0, -0.58, top + 0.005), m=black, bevel=0.008)
    k.cyl(0.06, 0.11, at=(0, -0.59, top + 0.085), rot=(90, 0, 0), m=black, bevel=0.01)
    k.cyl(0.066, 0.02, at=(0, -0.65, top + 0.085), rot=(90, 0, 0), m=steel, bevel=0.005)
    k.cyl(0.048, 0.012, at=(0, -0.662, top + 0.085), rot=(90, 0, 0), m=lamp, bevel=0.003)

    # Tall flared funnel chimney.
    k.lathe([(0.075, top - 0.04), (0.068, top + 0.05), (0.062, top + 0.14), (0.07, top + 0.2), (0.09, top + 0.25),
             (0.11, top + 0.29), (0.115, top + 0.31), (0.09, top + 0.31), (0.05, top + 0.28), (0, top + 0.27)],
            at=(0, -0.45, 0), m=black)
    k.torus(0.112, 0.012, at=(0, -0.45, top + 0.305), m=gray)

    # Steam dome and the small gold bell hung in a yoke.
    k.lathe([(0.1, top - 0.04), (0.09, top + 0.03), (0.075, top + 0.08), (0.05, top + 0.105), (0, top + 0.115)],
            at=(0, -0.12, 0), m=black)
    for side in (-1, 1):
        k.box((0.022, 0.025, 0.13), at=(side * 0.06, 0.1, top + 0.045), m=black, bevel=0.004)
    k.cyl(0.011, 0.14, at=(0, 0.1, top + 0.1), rot=(0, 90, 0), m=steel)
    k.lathe([(0.045, top + 0.0), (0.042, top + 0.01), (0.03, top + 0.04), (0.026, top + 0.07), (0.018, top + 0.09),
             (0, top + 0.095)], at=(0, 0.1, 0), m=gold)

    # Cab at the back of the boiler, with window panels and an overhanging roof.
    k.box((0.58, 0.34, 0.48), at=(0, 0.47, 0.665), m=black, bevel=0.012)
    k.box((0.66, 0.42, 0.035), at=(0, 0.47, 0.92), m=gray, bevel=0.01)
    for side in (-1, 1):
        k.box((0.012, 0.16, 0.16), at=(side * 0.291, 0.46, 0.76), m=glass, bevel=0.004)
        k.box((0.1, 0.012, 0.12), at=(side * 0.2, 0.299, 0.8), m=glass, bevel=0.004)
    k.box((0.6, 0.36, 0.03), at=(0, 0.47, 0.41), m=black, bevel=0.006)

    # Tender coupled behind, on two small wheel pairs whose axles pass through its frame; left out of the framing.
    tender = [
        k.box((0.26, 0.7, 0.2), at=(0, 1.02, 0.27), m=black, bevel=0.01),
        k.box((0.06, 0.06, 0.06), at=(0, 0.66, 0.29), m=steel, bevel=0.005),
        k.box((0.56, 0.66, 0.42), at=(0, 1.03, 0.58), m=black, bevel=0.015),
        k.blob([(0, 0.9, 0.8, 0.1, (2.2, 1.6, 0.6)), (0.05, 1.12, 0.8, 0.1, (2.0, 1.5, 0.5))], m=gray),
    ]
    for y in (0.83, 1.23):
        for side in (-1, 1):
            tender.append(k.cyl(0.1, 0.04, at=(side * 0.2, y, rail_top + 0.1), rot=(0, 90, 0), m=red))
        tender.append(k.cyl(0.02, 0.4, at=(0, y, rail_top + 0.1), rot=(0, 90, 0), m=steel))
    k.unframed(*tender)

    # Desert railroad: sand, a ballast bed, sleepers and two rails running off the card; mesas far back.
    k.floor("#e9b97a", "matte")
    k.box((0.9, 12, 0.03), at=(0, 0, 0.0), m=k.mat("#b89a78", "matte"), bevel=0.01, setting=True)
    tie = k.mat("#7a5233", "matte")
    for i in range(55):
        k.box((0.62, 0.09, 0.03), at=(0, -6 + i * 0.22, 0.025), m=tie, bevel=0.006, setting=True)
    for side in (-1, 1):
        k.box((0.04, 12, 0.03), at=(side * 0.2, 0, 0.055), m=steel, bevel=0.004, setting=True)
    rock = k.mat("#d9845a", "matte")
    k.box((3.5, 1.6, 0.9), at=(-3.2, 7.5, 0.45), rot=(0, 0, 10), m=rock, bevel=0.15, setting=True)
    k.box((2.2, 1.4, 0.6), at=(2.8, 9.0, 0.3), rot=(0, 0, -15), m=rock, bevel=0.12, setting=True)
