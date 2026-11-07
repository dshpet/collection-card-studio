# Open parasol: a domed lavender canopy stretched over eight ribs that run from the top notch on the shaft out to
# the rim, where the cloth sags a little between them. A white ruffled lace band hangs from the rim all round.
# Under the canopy a runner on the shaft holds eight stretchers that push up on the ribs. The wooden shaft runs
# from the finial above the canopy well down below the lace to a curved J handle. It floats, leaning sideways so
# the top of the dome shows and the shaft and handle swing out clear of the lace.
import math

SCENE = {"category": "1", "backdrop": "#ffc21a", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}

R, RIM, TOP = 0.5, 0.6, 0.85


def dome(r):
    return RIM + (TOP - RIM) * max(0.0, 1 - (r / R) ** 2) ** 0.7


def sag(x, y):
    a = math.atan2(y, x)
    return math.sin(4 * a) ** 2


def build(k):
    canvas = k.mat("#a084e6", "matte")
    seam = k.mat("#8466cc", "matte")
    lace = k.mat("#fdfaff", "matte")
    wood = k.mat("#9a5c2e", "matte")

    # Canopy shell: inner surface out to the rim, then the outer surface back up to the apex.
    n = 24
    inner = [(R * i / n, dome(R * i / n) - 0.018) for i in range(n + 1)]
    outer = [(R * i / n, dome(R * i / n)) for i in range(n, -1, -1)]
    canopy = k.lathe(inner + [(R + 0.004, RIM - 0.008)] + outer, at=(0, 0, 0), rot=(0, 0, 0), m=canvas, verts=256)

    def droop(p):
        x, y, z = p
        rr = math.hypot(x, y)
        s = sag(x, y) * min(1.0, rr / R) ** 2
        f = 1 - 0.03 * s
        return (x * f, y * f, z - 0.04 * s)

    k.warp(canopy, droop)

    # Ribs on the top of the canopy, from the apex to the rim, with a small tip at each end.
    for i in range(8):
        a = math.radians(i * 45)
        pts = [(r * math.cos(a), r * math.sin(a), dome(r) + 0.006) for r in [R * j / 10 for j in range(1, 11)]]
        k.tube(pts, 0.014, seam, curved=True)
        k.sphere(0.02, at=(R * math.cos(a), R * math.sin(a), RIM + 0.004), m=wood)

    # Ruffled lace band hanging from the rim, following the sag between ribs.
    band = k.lathe([(0.536, RIM - 0.085), (0.552, RIM - 0.077), (0.51, RIM + 0.006), (0.494, RIM - 0.004),
                    (0.536, RIM - 0.085)], at=(0, 0, 0), rot=(0, 0, 0), m=lace, verts=320)

    def ruffle(p):
        x, y, z = p
        a = math.atan2(y, x)
        rr = math.hypot(x, y)
        flare = max(0.0, min(1.0, (RIM + 0.006 - z) / 0.09))
        s = sag(x, y)
        nr = rr * (1 - 0.03 * s) + 0.016 * flare * math.sin(40 * a)
        return (nr * math.cos(a), nr * math.sin(a), z - 0.04 * s)

    k.warp(band, ruffle)

    # Shaft, top notch, finial and the runner with its stretchers.
    k.cyl(0.022, 1.06, at=(0, 0, 0.41), rot=(0, 0, 0), m=wood)
    k.cyl(0.04, 0.04, at=(0, 0, TOP - 0.01), rot=(0, 0, 0), m=lace)
    k.lathe([(0.0, TOP + 0.02), (0.022, TOP + 0.02), (0.026, TOP + 0.05), (0.012, TOP + 0.09), (0.0, TOP + 0.1)],
            at=(0, 0, 0), rot=(0, 0, 0), m=wood)
    run_z = 0.52
    k.cyl(0.036, 0.07, at=(0, 0, run_z), rot=(0, 0, 0), m=wood)
    for i in range(8):
        a = math.radians(i * 45)
        rr = 0.27
        k.tube([(0.034 * math.cos(a), 0.034 * math.sin(a), run_z + 0.02),
                (rr * math.cos(a), rr * math.sin(a), dome(rr) - 0.02)], 0.012, wood)

    # Curved J handle at the bottom of the shaft.
    k.tube([(0, 0, -0.06), (0, 0, -0.16), (0.015, 0, -0.24), (0.065, 0, -0.285), (0.12, 0, -0.27),
            (0.145, 0, -0.22), (0.14, 0, -0.18)], 0.028, wood, curved=True)
    k.sphere(0.03, at=(0.14, 0, -0.175), m=wood)

    # Lean sideways so the shaft and handle swing out clear of the lace, with a little forward tip to show the dome.
    k.turn(10, -24, 10)
