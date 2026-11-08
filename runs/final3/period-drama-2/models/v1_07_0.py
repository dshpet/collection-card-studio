# Two-tier cake stand: a round foot holds a center post that runs up through two round plates (a wide lower one
# and a small upper one) and ends in a ball finial. Small iced cakes, pink and mint, sit on both plates. It stands
# on a white linen tablecloth that runs off the card.
import math

SCENE = {"category": "3", "backdrop": "#6a2c9e", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def plate(k, radius, z, m):
    t = 0.024
    profile = [(0, z), (radius * 0.6, z), (radius * 0.9, z + 0.006), (radius, z + 0.03), (radius + 0.012, z + 0.048),
               (radius - 0.006, z + 0.05), (radius * 0.9, z + 0.028), (radius * 0.6, z + t), (0, z + t)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=m)
    return z + t


def cake(k, x, y, z, r, icing, top):
    h = r * 1.1
    k.cyl(r, h, at=(x, y, z + h / 2), rot=(0, 0, 0), m=icing, bevel=0.012)
    k.sphere(r * 0.98, at=(x, y, z + h), scale=(1, 1, 0.35), m=icing)
    k.sphere(r * 0.3, at=(x, y, z + h + r * 0.38), m=top)


def build(k):
    porcelain = k.mat("#f7f5f0", "gloss")
    pink = k.mat("#f58bb5", "satin")
    mint = k.mat("#8fe0c0", "satin")
    cream = k.mat("#fff6ea", "satin")

    # Foot
    k.lathe([(0, 0), (0.17, 0), (0.18, 0.012), (0.17, 0.028), (0.12, 0.045), (0.07, 0.07), (0.045, 0.1),
             (0.04, 0.12), (0, 0.12)], at=(0, 0, 0), rot=(0, 0, 0), m=porcelain)
    # Center post with a knob between the tiers and a ball finial on top
    k.cyl(0.028, 0.78, at=(0, 0, 0.11 + 0.39), rot=(0, 0, 0), m=porcelain)
    k.lathe([(0, 0.40), (0.035, 0.40), (0.055, 0.43), (0.06, 0.45), (0.05, 0.48), (0.032, 0.50), (0, 0.50)],
            at=(0, 0, 0), rot=(0, 0, 0), m=porcelain)
    k.sphere(0.05, at=(0, 0, 0.9), m=porcelain)
    k.torus(0.03, 0.008, at=(0, 0, 0.865), rot=(0, 0, 0), m=porcelain)

    # Lower and upper plates, threaded on the post
    lower = plate(k, 0.42, 0.25, porcelain)
    upper = plate(k, 0.26, 0.6, porcelain)

    # Lower plate: a ring of seven cakes
    for i in range(7):
        a = math.radians(i * 360 / 7 + 10)
        cake(k, 0.27 * math.cos(a), 0.27 * math.sin(a), lower, 0.062, pink if i % 2 == 0 else mint, cream)
    # Upper plate: four cakes around the post
    for i in range(4):
        a = math.radians(i * 90 + 45)
        cake(k, 0.15 * math.cos(a), 0.15 * math.sin(a), upper, 0.055, mint if i % 2 == 0 else pink, cream)

    # White linen tablecloth, top at z = 0
    k.box((5, 3, 0.1), at=(0, 0.6, -0.05), rot=(0, 0, 0), m=k.mat("#f4f1ea", "matte"), bevel=0.01, setting=True)
