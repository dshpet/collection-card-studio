# Folding fan, open: thirteen gold ribs fan out over 160 degrees from one plum pivot pin at the bottom. Red silk
# is pleated between neighbouring ribs (a valley on each rib, a ridge between) over the outer part of the ribs;
# the bare rib roots show below it. The two outer guard sticks are thicker and lie on the front of the silk.
# The pin passes through every rib and has a cap on each side. Floating, tilted a little.
import math

SCENE = {"category": "1", "backdrop": "#5ec4f2", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    silk = k.mat("#c8102e", "satin")
    gold = k.mat("#d9a62e", "metal")
    plum = k.mat("#7a2a5c", "satin")

    R_OUT, R_IN = 0.62, 0.27   # silk band
    SPREAD, N = 160.0, 13      # degrees, rib count
    angles = [math.radians(-SPREAD / 2 + i * SPREAD / (N - 1)) for i in range(N)]
    FOLD = 0.07                # ridge depth per unit radius, toward -y
    T = 0.008                  # silk thickness

    def facet(a0, a1, d0, d1):
        def fn(p):
            x, y, z = p
            u = min(max(x + 0.5, 0.0), 1.0)
            v = min(max(y + 0.5, 0.0), 1.0)
            r = R_IN + u * (R_OUT - R_IN)
            a = a0 + v * (a1 - a0)
            depth = -(d0 + v * (d1 - d0)) * r + z
            return (r * math.sin(a), depth, r * math.cos(a))
        k.warp(k.box((1, 1, T), at=(0, 0, 0), m=silk, bevel=0.002), fn)

    # pleated silk: each panel is two flat facets, valley on the ribs, ridge at mid-angle
    for a0, a1 in zip(angles, angles[1:]):
        am = (a0 + a1) / 2
        facet(a0, am, 0.0, FOLD)
        facet(am, a1, FOLD, 0.0)

    # ribs behind the silk, from just below the pivot out to near the rim
    w, th = 0.022, 0.012
    tail, tip = -0.06, R_OUT - 0.03
    for a in angles[1:-1]:
        L = tip - tail
        c = tail + L / 2
        k.box((w, th, L), at=(c * math.sin(a), 0.011, c * math.cos(a)), rot=(0, math.degrees(a), 0), m=gold, bevel=0.004)
    # guard sticks: thicker, full length, on the front at the two ends
    for a in (angles[0], angles[-1]):
        L = R_OUT + 0.01 - tail
        c = tail + L / 2
        k.box((0.032, 0.016, L), at=(c * math.sin(a), -0.012, c * math.cos(a)), rot=(0, math.degrees(a), 0), m=gold, bevel=0.005)
        # back rib under the guard so the silk end is held on both sides
        Lb = tip - tail
        cb = tail + Lb / 2
        k.box((w, th, Lb), at=(cb * math.sin(a), 0.011, cb * math.cos(a)), rot=(0, math.degrees(a), 0), m=gold, bevel=0.004)

    # pivot pin through the stack, capped on both faces
    k.cyl(0.016, 0.07, at=(0, 0, 0), rot=(90, 0, 0), m=plum)
    k.cyl(0.036, 0.014, at=(0, -0.026, 0), rot=(90, 0, 0), m=plum, bevel=0.005)
    k.cyl(0.032, 0.012, at=(0, 0.024, 0), rot=(90, 0, 0), m=plum, bevel=0.005)
    k.sphere(0.02, at=(0, -0.034, 0), scale=(1, 0.5, 1), m=plum)

    k.turn(-8, -14, 0)
