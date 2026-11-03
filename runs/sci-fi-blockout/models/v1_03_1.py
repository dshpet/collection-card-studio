# Ringed planet: a round orange planet with three raised cream belts running parallel to its equator, a small
# blue crater dish with a raised rim on the upper front, and a wide flat pale yellow ring around the middle. The
# whole planet tilts so the ring runs on a slant across the card and shows its top face, like the floating cards.
import math

SCENE = {"category": "1", "backdrop": "#9b3df0", "azimuth": 20, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    orange = k.mat("#f28a2e", "satin")
    cream = k.mat("#fbe7c2", "satin")
    ring = k.mat("#f2d35a", "satin")
    blue = k.mat("#3d9cf0", "gloss")
    R = 0.38

    k.sphere(R, at=(0, 0, 0.5), m=orange)

    # Raised belts: thin sphere zones standing just proud of the surface.
    for z1, z2 in ((0.12, 0.2), (-0.11, -0.03), (-0.27, -0.21)):
        profile = []
        for i in range(13):
            z = z1 + (z2 - z1) * i / 12
            profile.append((math.sqrt(R * R - z * z) + 0.012, z))
        profile = [(math.sqrt(R * R - z1 * z1) - 0.01, z1)] + profile + [(math.sqrt(R * R - z2 * z2) - 0.01, z2)]
        k.lathe(profile, at=(0, 0, 0.5), m=cream)

    # Crater on the upper front: a shallow blue dish with an orange rim.
    n = (-0.29, -0.668, 0.684)
    rot = (46.8, 0, -23.4)
    k.cyl(0.058, 0.02, at=(0.374 * n[0], 0.374 * n[1], 0.5 + 0.374 * n[2]), rot=rot, m=blue, bevel=0.006)
    k.torus(0.064, 0.013, at=(0.38 * n[0], 0.38 * n[1], 0.5 + 0.38 * n[2]), rot=rot, m=orange)

    # Wide flat ring: a torus squashed flat, inner edge clear of the planet.
    band = k.torus(0.6, 0.13, at=(0, 0, 0.5), rot=(0, 0, 0), m=ring)
    k.warp(band, lambda p: (p[0], p[1], p[2] * 0.14))

    k.turn(14, -22, 0)
