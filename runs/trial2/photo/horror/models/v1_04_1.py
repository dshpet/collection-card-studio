# Cauldron: a round-bellied iron pot, revolved, its belly widest a little below the middle, narrowing to a
# short neck and a flared lip. Three short tapered legs sink into the underside of the belly and stand on the
# floor, placed so one faces the camera and two stand at the back sides, all three in view. Two loop handles
# rise from the neck on the left and right. Green potion fills the pot just below the lip, with a few domed
# bubbles on its surface. A small orange flame burns on two crossed sticks under the pot, between the legs.
# The pot stands on a floor of grey stone flags, and the pink backdrop shows behind the floor.
import math

SCENE = {"category": "3", "backdrop": "#f27fb2", "azimuth": 30, "elevation": 18, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26262b", "satin")
    potion = k.mat("#5ee83a", "gloss")
    bubble = k.mat("#8cf55e", "gloss")
    wood = k.mat("#6b4022", "matte")
    flame = k.mat("#ff8a1f", "glow")

    # Pot body: outer wall up to the lip, over the lip, down the inner wall to below the potion surface.
    profile = [(0.0, 0.18), (0.14, 0.185), (0.24, 0.205), (0.32, 0.245), (0.38, 0.30), (0.415, 0.37),
               (0.43, 0.44), (0.425, 0.51), (0.405, 0.58), (0.375, 0.64), (0.345, 0.69), (0.33, 0.73),
               (0.335, 0.77), (0.355, 0.80), (0.375, 0.82), (0.38, 0.835), (0.365, 0.845), (0.335, 0.835),
               (0.315, 0.80), (0.305, 0.76), (0.0, 0.76)]
    k.lathe(profile, at=(0, 0, 0), m=iron)

    # Potion surface and bubbles.
    k.cyl(0.312, 0.03, at=(0, 0, 0.765), m=potion, bevel=0.004)
    for x, y, r in ((-0.10, -0.08, 0.055), (0.08, -0.13, 0.04), (0.13, 0.06, 0.05), (-0.05, 0.12, 0.035),
                    (0.02, 0.0, 0.03), (-0.18, 0.03, 0.03)):
        k.sphere(r, at=(x, y, 0.78), scale=(1, 1, 0.8), m=bubble)

    # Three short tapered legs, tops buried in the belly underside; one faces the camera (azimuth 30 looks
    # from the -60 degree direction), two stand at the back sides, so all three show.
    for a in (-60, 60, 180):
        t = math.radians(a)
        x, y = 0.25 * math.cos(t), 0.25 * math.sin(t)
        k.cone(0.035, 0.055, 0.28, at=(x, y, 0.14), m=iron, bevel=0.006)

    # Two loop handles on the sides of the neck.
    for s in (-1, 1):
        pts = [(s * 0.32, -0.10, 0.70), (s * 0.43, -0.10, 0.76), (s * 0.48, -0.04, 0.80),
               (s * 0.48, 0.04, 0.80), (s * 0.43, 0.10, 0.76), (s * 0.32, 0.10, 0.70)]
        k.tube(pts, 0.024, iron, curved=True)

    # Small fire under the pot: two crossed sticks on the floor and a small flame on them.
    for a in (35, -35):
        k.cyl(0.018, 0.26, at=(0, 0, 0.02), rot=(0, 90, a), m=wood, bevel=0.004)
    k.blob([(0, 0, 0.065, 0.045, (1, 1, 1.0)), (0, 0, 0.11, 0.025, (1, 1, 1.4))], flame)

    # Stone flag floor, top at about z = 0, running off the card; darker weathered greys, thin slabs with
    # narrow joints and slightly uneven heights so it reads as stone; pink backdrop behind it.
    greys = ("#6f6c70", "#5f5d63", "#7a7678", "#67646b")
    size, gap = 0.62, 0.015
    for i in range(-5, 6):
        for j in range(-3, 4):
            off = size / 2 if j % 2 else 0
            dz = ((i * 7 + j * 11) % 3 - 1) * 0.004
            k.box((size - gap, size - gap, 0.06), at=(i * size + off, j * size, -0.03 + dz),
                  m=k.mat(greys[(i * 3 + j * 5) % 4], "matte"), bevel=0.008, setting=True)
    k.box((12, 8, 0.02), at=(0, 0, -0.05), m=k.mat("#3f3d42", "matte"), bevel=0, setting=True)
