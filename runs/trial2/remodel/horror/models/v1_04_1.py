# Cauldron: a round black iron pot on three short splayed legs whose tops sink into the rounded underside.
# Two loop handles leave the wall below the rim and curve back into it. A green potion surface fills the pot
# just under the lip, with a few round bubbles half sunk in it. A small orange flame sits on the floor under
# the pot between the legs. The pot stands on a floor of mid-grey stone slabs that ends a little behind it, so
# the pink backdrop shows above.
import math

SCENE = {"category": "3", "backdrop": "#f27bb3", "azimuth": 25, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26262b", "satin")
    potion = k.mat("#4be03a", "gloss")
    bubble = k.mat("#8cf55e", "gloss")
    flame = k.mat("#ff8a1f", "glow")

    # Pot body: rounded underside, wide belly, narrower neck, thick rolled rim, then the inner wall down.
    profile = [(0.0, 0.12), (0.08, 0.122), (0.16, 0.135), (0.24, 0.165), (0.31, 0.205), (0.36, 0.255),
               (0.40, 0.32), (0.425, 0.39), (0.432, 0.45), (0.425, 0.51), (0.405, 0.57), (0.375, 0.63),
               (0.35, 0.68), (0.34, 0.72), (0.35, 0.745), (0.375, 0.76), (0.385, 0.78), (0.378, 0.80),
               (0.36, 0.81), (0.335, 0.80), (0.325, 0.78), (0.318, 0.72), (0.30, 0.66), (0.0, 0.66)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=iron, verts=96)

    # Potion surface just under the lip, inside the inner wall.
    k.cyl(0.322, 0.03, at=(0, 0, 0.745), rot=(0, 0, 0), m=potion, bevel=0.004)
    for x, y, r in ((-0.12, -0.08, 0.06), (0.10, -0.14, 0.045), (0.05, 0.10, 0.07), (-0.18, 0.12, 0.04),
                    (0.19, 0.04, 0.035), (-0.02, -0.02, 0.03)):
        k.sphere(r, at=(x, y, 0.76), scale=(1, 1, 0.75), m=bubble)

    # Three short legs, splayed a little, tops buried in the underside; two face the camera.
    for a in (90, 210, 330):
        t = math.radians(a)
        c, s = math.cos(t), math.sin(t)
        k.tube([(0.27 * c, 0.27 * s, 0.03), (0.24 * c, 0.24 * s, 0.22)], 0.045, iron)
        k.blob([(0.275 * c, 0.275 * s, 0.03, 0.05, (1, 1, 0.6))], iron)

    # Two loop handles on the sides, ends sunk into the wall.
    for side in (-1, 1):
        k.tube([(side * 0.32, 0, 0.72), (side * 0.42, 0, 0.735), (side * 0.50, 0, 0.68),
                (side * 0.51, 0, 0.60), (side * 0.40, 0, 0.55)], 0.026, iron, curved=True)

    # Small flame under the pot, standing on the floor between the legs.
    k.cone(0.055, 0.0, 0.10, at=(0, 0, 0.05), rot=(0, 0, 0), m=flame)
    k.cone(0.03, 0.0, 0.07, at=(0.045, -0.02, 0.035), rot=(0, 12, 0), m=flame)
    k.cone(0.03, 0.0, 0.065, at=(-0.045, 0.01, 0.033), rot=(0, -12, 0), m=flame)

    # Stone slab floor: dark grout bed with slightly uneven grey stone slabs on it, ending behind the pot.
    k.box((8, 4.2, 0.1), at=(0, -0.9, -0.06), rot=(0, 0, 0), m=k.mat("#3f3c43", "matte"), bevel=0, setting=True)
    tones = ("#7a7680", "#6c6971", "#858089", "#726d74")
    for i in range(-6, 7):
        for j in range(-5, 2):
            n = (i * 7 + j * 13) % 4
            dz = (n - 1.5) * 0.004
            k.box((0.56, 0.56, 0.06), at=(i * 0.6 + 0.3, j * 0.6 + 0.3, -0.03 + dz), rot=(0, 0, (n - 1.5) * 1.2),
                  m=k.mat(tones[n], "matte"), bevel=0.012, setting=True)
