# Hover car: one smooth rounded yellow hull, nose toward -y, made by lathing a long profile and flattening it.
# A glass bubble canopy sits on a trim ring on top, with a dark cockpit floor and seat inside. A low tail fin
# stands on the rear deck. No wheels: two small round pink lights are set almost flush into the belly, front and
# rear, in thin grey rims. It floats in clear sky, banked toward the camera so its nose, right side, top and the
# belly lights all show.
import math

SCENE = {"category": "1", "backdrop": "#4ab3ee", "azimuth": 35, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    yellow = k.mat("#ffc61a", "satin")
    trim = k.mat("#e09a12", "satin")
    glass = k.mat("#d8f3ff", "glass")
    grey = k.mat("#4a505b", "satin")
    pink = k.mat("#ff4fb8", "glow")

    # Hull: a lathed profile along y (nose at y = -0.45), slightly tapered at the nose, fuller at the back,
    # then flattened to a low, wide car body.
    n = 40
    profile = []
    for i in range(n + 1):
        t = i / n
        u = abs(2 * t - 1)
        e = 2.2 if t < 0.5 else 3.0  # rounder, narrower nose; fuller tail
        r = 0.3 * max(0.0, 1 - u ** e) ** (1 / e)
        profile.append((r, 0.9 * t))
    hull = k.lathe(profile, at=(0, -0.45, 0.3), rot=(-90, 0, 0), m=yellow)
    k.warp(hull, lambda p: (p[0], p[1] * 0.55, p[2]))

    # Canopy: glass bubble on a trim ring, with a dark floor and seat inside.
    k.sphere(0.2, at=(0, -0.04, 0.45), scale=(0.85, 1.2, 0.85), m=glass)
    ring = [(0.17 * math.cos(math.radians(a)), -0.04 + 0.24 * math.sin(math.radians(a)), 0.45)
            for a in range(0, 361, 15)]
    k.tube(ring, 0.022, trim, curved=True)
    k.cyl(0.16, 0.02, at=(0, -0.04, 0.445), m=grey, bevel=0.005)
    k.box((0.16, 0.06, 0.13), at=(0, 0.06, 0.51), m=grey, bevel=0.025)

    # Low tail fin on the rear deck.
    k.box((0.035, 0.16, 0.09), at=(0, 0.34, 0.44), rot=(-30, 0, 0), m=yellow, bevel=0.015)

    # Underlights: thin grey rims set into the belly, each with a shallow glowing pink lens.
    for y in (-0.24, 0.24):
        k.cyl(0.075, 0.03, at=(0, y, 0.155), m=grey, bevel=0.008)
        k.sphere(0.062, at=(0, y, 0.14), scale=(1, 1, 0.35), m=pink)

    # Bank toward the camera so the belly lights show.
    k.turn(-8, -18, 0)
