# Covered wagon on a prairie trail: a wooden box bed rides on two axles, each axle passes under a bolster
# block beneath the bed and carries a spoked wheel at each end (small wheels front, big wheels back, four in all).
# The arched canvas bonnet sits on the bed top and flares at both ends; the front opening shows dark. The driver's
# bench stands on two blocks at the front of the bed, with a slanted footboard below it. The tongue runs from the
# front axle and rests on the ground; it goes off the card and is left out of the framing.
import math

SCENE = {"category": "4", "backdrop": "#3fc4f0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def wheel(k, x, y, r, wood, iron, red):
    k.torus(r - 0.022, 0.025, at=(x, y, r), rot=(90, 0, 0), m=iron)
    k.torus(r - 0.05, 0.012, at=(x, y, r), rot=(90, 0, 0), m=red)
    k.cyl(0.055, 0.09, at=(x, y, r), rot=(90, 0, 0), m=red, bevel=0.01)
    k.cyl(0.03, 0.12, at=(x, y, r), rot=(90, 0, 0), m=iron)
    for i in range(12):
        a = math.radians(i * 30 + 15)
        k.tube([(x + 0.05 * math.cos(a), y, r + 0.05 * math.sin(a)),
                (x + (r - 0.03) * math.cos(a), y, r + (r - 0.03) * math.sin(a))], 0.013, wood)


def build(k):
    wood = k.mat("#8a5228", "matte")
    dark = k.mat("#5e3517", "matte")
    canvas = k.mat("#f4ead2", "matte")
    iron = k.mat("#4a4440", "metal")
    red = k.mat("#d23a2a", "satin")

    # bed
    k.box((1.0, 0.5, 0.2), at=(0, 0, 0.42), m=wood, bevel=0.012)
    for y in (-0.255, 0.255):
        k.box((1.02, 0.03, 0.04), at=(0, y, 0.51), m=dark, bevel=0.008)
        k.box((1.02, 0.03, 0.04), at=(0, y, 0.34), m=dark, bevel=0.008)

    # axles, bolsters, wheels
    for x, r in ((-0.3, 0.3), (0.33, 0.24)):
        k.cyl(0.03, 0.72, at=(x, 0, r), rot=(90, 0, 0), m=iron)
        k.box((0.09, 0.46, 0.32 - r + 0.01), at=(x, 0, (0.32 + r) / 2), m=dark, bevel=0.008)
        for y in (-0.31, 0.31):
            wheel(k, x, y, r, wood, iron, red)

    # canvas bonnet: a lathe along x, lower half flattened onto the bed top, upper half stretched taller
    prof = [(0, -0.39), (0.2, -0.39), (0.3, -0.385), (0.295, -0.33), (0.28, -0.24), (0.275, -0.1),
            (0.275, 0.1), (0.28, 0.24), (0.295, 0.33), (0.3, 0.385), (0.2, 0.39), (0, 0.39)]
    bonnet = k.lathe(prof, at=(-0.04, 0, 0.52), rot=(0, 90, 0), m=canvas)
    k.warp(bonnet, lambda p: (0.0 if p[0] > 0 else p[0] * 1.3, p[1], p[2]))
    k.sphere(0.19, at=(0.353, 0, 0.66), scale=(0.08, 1.0, 1.15), m=k.mat("#3a2414", "matte"))
    k.sphere(0.19, at=(-0.433, 0, 0.66), scale=(0.08, 1.0, 1.15), m=k.mat("#3a2414", "matte"))

    # driver's bench and footboard
    for y in (-0.19, 0.19):
        k.box((0.1, 0.05, 0.1), at=(0.43, y, 0.57), m=dark, bevel=0.008)
    k.box((0.14, 0.48, 0.04), at=(0.43, 0, 0.64), m=wood, bevel=0.01)
    k.box((0.03, 0.48, 0.1), at=(0.375, 0, 0.71), m=wood, bevel=0.008)
    k.box((0.16, 0.48, 0.025), at=(0.56, 0, 0.47), rot=(0, 30, 0), m=wood, bevel=0.006)

    # tongue resting on the ground
    k.unframed(k.tube([(0.36, 0, 0.24), (0.7, 0, 0.15), (1.2, 0, 0.03)], 0.025, wood),
               k.box((0.04, 0.4, 0.04), at=(1.15, 0, 0.03), m=wood, bevel=0.008))

    # prairie: grass, dirt trail, distant hills
    k.floor("#6cc24a")
    k.box((12, 0.9, 0.01), at=(0, 0, 0.003), m=k.mat("#c9a36b", "matte"), bevel=0, setting=True)
    for x, y, r in ((-3.5, 9, 3.2), (2.5, 11, 4.0), (8, 9, 3.0)):
        k.sphere(r, at=(x, y, -r * 0.55), scale=(1.6, 1, 0.6), m=k.mat("#58b046", "matte"), setting=True)
