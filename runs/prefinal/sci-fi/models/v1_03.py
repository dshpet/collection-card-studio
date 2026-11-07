# Rocket: a white body revolved as one smooth hull, a pointed red nose cone seated on its top, three red swept fins
# at 120 degrees set into the lower hull, one round yellow window with a red rim facing the viewer, and a grey
# engine nozzle under the base. The fire is left to the image model; only a small glowing core sits in the
# nozzle mouth. Floating, tilted to the right as it climbs.
import math

SCENE = {"category": "1", "backdrop": "#2ec4ef", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f6f6f2", "satin")
    red = k.mat("#e3262b", "satin")
    grey = k.mat("#8d939b", "metal")
    window = k.mat("#ffd23a", "glass")
    core = k.mat("#fff4b0", "glow")

    # Hull: closed at the base, slight bulge, open seam at the top where the nose sits.
    hull = []
    for i in range(17):
        t = i / 16
        z = 0.12 + 0.62 * t
        r = 0.125 + 0.045 * math.sin(math.pi * (0.25 + 0.6 * t))
        hull.append((r, z))
    k.lathe([(0.0, 0.12)] + hull + [(0.0, 0.74)], at=(0, 0, 0), m=white)
    top_r = hull[-1][0]

    # Nose cone: ogive from the hull's top radius to a point.
    nose = [(top_r * math.cos(0.5 * math.pi * (i / 16)) ** 0.8, 0.735 + 0.33 * (i / 16)) for i in range(17)]
    nose[-1] = (0.0, nose[-1][1])
    k.lathe([(0.0, 0.735)] + nose, at=(0, 0, 0), m=red)

    # Window facing the front (-y).
    wz = 0.56
    wr = 0.125 + 0.045 * math.sin(math.pi * (0.25 + 0.6 * (wz - 0.12) / 0.62))
    k.cyl(0.062, 0.03, at=(0, -wr + 0.005, wz), rot=(90, 0, 0), m=window)
    k.torus(0.068, 0.016, at=(0, -wr - 0.005, wz), rot=(90, 0, 0), m=red)

    # Three swept fins; inner edge sunk into the hull, outer edge shorter and lower.
    def sweep(p):
        x, y, z = p
        if y > 0:
            return (x, y, z * 0.55 - 0.11)
        return (x, y, z)

    for a in (90, 210, 330):
        rad = math.radians(a)
        R = 0.205
        fin = k.box((0.03, 0.18, 0.30), at=(R * math.cos(rad), R * math.sin(rad), 0.27), rot=(0, 0, a - 90),
                    m=red, bevel=0.012)
        k.warp(fin, sweep)

    # Engine nozzle under the base, and the glowing core in its mouth.
    k.lathe([(0.0, 0.135), (0.075, 0.135), (0.07, 0.11), (0.08, 0.07), (0.1, 0.03), (0.105, 0.02),
             (0.0, 0.02)], at=(0, 0, 0), m=grey)
    k.lathe([(0.0, -0.06), (0.04, -0.02), (0.07, 0.01), (0.075, 0.025), (0.0, 0.025)], at=(0, 0, 0), m=core)

    k.turn(0, 22, 12)
