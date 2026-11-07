# Flying saucer: one revolved silver hull, a shallow belly under a wider upper deck, meeting at a vertical rim band.
# A ring of twelve small round lights sits half-sunk in the rim band. The red glass dome rests on a silver collar on
# top of the deck; a small round plate closes the underside. It floats in a plain green sky, tilted to show its top.
import math

SCENE = {"category": "1", "backdrop": "#5fcf6a", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    trim = k.mat("#9aa1ab", "metal")
    dome = k.mat("#e8262b", "glass")
    light = k.mat("#fbfbf7", "glow")

    hull = [(0.0, -0.13), (0.10, -0.13), (0.16, -0.12), (0.24, -0.10), (0.32, -0.075), (0.40, -0.05),
            (0.46, -0.035), (0.50, -0.028), (0.50, 0.028), (0.47, 0.04), (0.42, 0.06), (0.36, 0.08),
            (0.29, 0.10), (0.22, 0.115), (0.18, 0.12), (0.0, 0.12)]
    k.lathe(hull, at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # collar the dome sits in, and the dome itself
    k.torus(0.175, 0.022, at=(0, 0, 0.125), rot=(0, 0, 0), m=trim)
    cap = [(0.17, 0.0)] + [(0.17 * math.cos(math.radians(a)), 0.16 * math.sin(math.radians(a)))
                           for a in range(6, 91, 6)]
    cap[-1] = (0.0, cap[-1][1])
    k.lathe(cap, at=(0, 0, 0.12), rot=(0, 0, 0), m=dome)

    # underside plate
    k.cyl(0.09, 0.03, at=(0, 0, -0.135), rot=(0, 0, 0), m=trim, bevel=0.008)

    # ring of lights half-sunk in the rim band
    for i in range(12):
        a = math.radians(i * 30 + 15)
        k.sphere(0.03, at=(0.505 * math.cos(a), 0.505 * math.sin(a), 0.0), m=light)

    k.turn(12, -8, 0)
