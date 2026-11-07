# Parasol: a straight wooden shaft runs from the hooked handle up through the canopy to a top knob. Eight ribs
# run from the top over the domed canopy to tips at the rim, and the canopy rises into scallops between
# them. Under the canopy, eight braces run from a collar on the shaft out to the ribs. A white lace frill of
# thin flat scallops hangs from a band at the rim. The parasol floats, tilted to show the top and a bit of the underside.
import math

SCENE = {"category": "1", "backdrop": "#2fc4ee", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}

R, RIM, TOP = 0.42, 0.60, 0.82
N = 8


def lift(r, a):
    # canopy lifts between ribs near the rim, giving scalloped panels
    return 0.035 * (r / R) ** 3 * (1 - abs(math.cos(N / 2 * a)))


def build(k):
    canopy = k.mat("#f0584a", "satin")
    lace = k.mat("#fbfaf4", "matte")
    wood = k.mat("#8a5530", "satin")
    rib_m = k.mat("#d84638", "satin")
    tip_m = k.mat("#7a4a2a", "satin")

    # domed canopy with a hollowed underside
    under = [(0.40 * i / 10, 0.72 - 0.12 * (i / 10) ** 2) for i in range(11)]
    outer = [(R * math.cos(math.radians(p)), RIM + (TOP - RIM) * math.sin(math.radians(p)))
             for p in range(0, 91, 6)]
    dome = k.lathe(under + outer, at=(0, 0, 0), rot=(0, 0, 0), m=canopy, verts=128)

    def warp(v):
        x, y, z = v
        r = math.hypot(x, y)
        return (x, y, z + lift(r, math.atan2(y, x)))
    k.warp(dome, warp)

    for i in range(N):
        a = i * 2 * math.pi / N
        c, s = math.cos(a), math.sin(a)
        # rib over the top of the canopy, with a tip past the rim
        pts = []
        for p in range(0, 91, 10):
            ph = math.radians(p)
            r = (R + 0.008) * math.cos(ph)
            pts.append((r * c, r * s, RIM + (TOP - RIM + 0.008) * math.sin(ph)))
        pts.append((0.445 * c, 0.445 * s, RIM - 0.012))
        k.tube(pts, 0.012, rib_m, curved=True)
        k.sphere(0.02, at=(0.45 * c, 0.45 * s, RIM - 0.02), m=tip_m)
        # brace from the shaft collar out to the rib under the canopy
        k.tube([(0.02 * c, 0.02 * s, 0.56), (0.24 * c, 0.24 * s, 0.70)], 0.009, wood)

    # white lace frill: thin flat scallops hanging from a band at the rim
    M = 48
    for j in range(M):
        a = j * 2 * math.pi / M
        z = RIM + lift(R, a) - 0.035
        k.sphere(0.036, at=(0.428 * math.cos(a), 0.428 * math.sin(a), z), scale=(0.28, 1, 1.15),
                 rot=(0, 0, math.degrees(a)), m=lace)
    k.torus(0.424, 0.012, at=(0, 0, RIM + 0.004), rot=(0, 0, 0), m=lace)

    # shaft, top knob, collar on the shaft
    k.cyl(0.018, 0.80, at=(0, 0, 0.44), rot=(0, 0, 0), m=wood)
    k.sphere(0.032, at=(0, 0, TOP + 0.03), m=wood)
    k.cyl(0.03, 0.05, at=(0, 0, 0.56), rot=(0, 0, 0), m=wood, bevel=0.008)

    # curved hooked handle
    hook = [(0, 0, 0.10), (0, 0, 0.03), (0.015, 0, -0.03), (0.055, 0, -0.06),
            (0.10, 0, -0.05), (0.125, 0, -0.01), (0.12, 0, 0.03)]
    k.tube(hook, 0.026, wood, curved=True)
    k.sphere(0.028, at=(0.12, 0, 0.03), m=wood)

    k.turn(14, -22, 0)
