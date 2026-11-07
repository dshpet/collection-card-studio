# Vintage press camera on a dark wooden desk: a boxy black body stands on four small feet; its front bed folds
# down level and is held by two side braces. The lens standard stands on the bed, joined to the body by tapered
# bellows, and carries the lens barrel with a silver ring and glass. A post rises from the body top and holds the
# round flash dish facing forward, with its bulb in the middle. The red shutter button sits on top. The desk
# top runs off the card, its front edge and apron showing low in front, as on the computer card.

SCENE = {"category": "3", "backdrop": "#f6a623", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    body = k.mat("#1c1c1f", "satin")
    bellows = k.mat("#141416", "matte")
    silver = k.mat("#cfd3d9", "metal")
    glass = k.mat("#3b4a5a", "glass")
    red = k.mat("#e0262a", "gloss")

    # Body on four feet
    k.box((0.50, 0.32, 0.46), at=(0, 0.10, 0.25), m=body, bevel=0.03)
    for x in (-0.21, 0.21):
        for y in (-0.03, 0.23):
            k.cyl(0.02, 0.02, at=(x, y, 0.01), m=silver)
    # Silver front frame where the bellows meet the body
    k.box((0.44, 0.02, 0.40), at=(0, -0.065, 0.26), m=silver, bevel=0.008)

    # Folded-down front bed with hinge and side braces
    k.box((0.42, 0.36, 0.03), at=(0, -0.245, 0.045), m=body, bevel=0.008)
    k.cyl(0.018, 0.42, at=(0, -0.065, 0.045), rot=(0, 90, 0), m=silver)
    for x in (-0.205, 0.205):
        k.cyl(0.02, 0.03, at=(x, -0.39, 0.01), m=silver)
        k.tube([(x * 1.08, -0.38, 0.05), (x * 1.08, -0.08, 0.26)], 0.012, silver)

    # Bellows: tapered pleats from the body front to the lens standard
    n = 6
    y0, y1 = -0.075, -0.305
    for i in range(n):
        t = (i + 0.5) / n
        y = y0 + (y1 - y0) * t
        w = 0.40 + (0.26 - 0.40) * t + (0.02 if i % 2 else 0.0)
        h = 0.34 + (0.24 - 0.34) * t + (0.02 if i % 2 else 0.0)
        k.box((w, (y0 - y1) / n + 0.004, h), at=(0, y, 0.25), m=bellows, bevel=0.012)

    # Lens standard on the bed, with lens barrel, silver ring and glass
    k.box((0.30, 0.03, 0.34), at=(0, -0.32, 0.23), m=body, bevel=0.01)
    k.box((0.32, 0.06, 0.03), at=(0, -0.32, 0.075), m=silver, bevel=0.006)
    k.cyl(0.085, 0.09, at=(0, -0.38, 0.25), rot=(90, 0, 0), m=body)
    k.torus(0.085, 0.022, at=(0, -0.425, 0.25), rot=(90, 0, 0), m=silver)
    k.cyl(0.07, 0.012, at=(0, -0.428, 0.25), rot=(90, 0, 0), m=glass)

    # Flash: post on the body top holding a round dish that faces forward
    k.cyl(0.03, 0.02, at=(0.13, 0.17, 0.49), m=silver)
    k.tube([(0.13, 0.17, 0.48), (0.13, 0.17, 0.72), (0.13, 0.12, 0.72)], 0.016, silver)
    dish = [(0.0, 0.0), (0.035, 0.0), (0.07, 0.012), (0.11, 0.035), (0.14, 0.062), (0.16, 0.09), (0.165, 0.1),
            (0.152, 0.1), (0.135, 0.075), (0.105, 0.048), (0.065, 0.025), (0.03, 0.015), (0.0, 0.014)]
    k.lathe(dish, at=(0.13, 0.12, 0.72), rot=(90, 0, 0), m=silver)
    k.sphere(0.03, at=(0.13, 0.085, 0.72), m=k.mat("#fff4d6", "glow"))

    # Red shutter button on top
    k.cyl(0.03, 0.015, at=(-0.15, 0.0, 0.487), m=silver)
    k.cyl(0.022, 0.025, at=(-0.15, 0.0, 0.505), m=red, bevel=0.006)

    # Dark wooden desk: top running off the card, front edge and apron below
    k.box((6, 4, 0.08), at=(0, 1.2, -0.04), m=k.mat("#5a3420", "matte"), bevel=0.02, setting=True)
    k.box((6, 0.06, 1.2), at=(0, -0.72, -0.68), m=k.mat("#4a2a19", "matte"), bevel=0.01, setting=True)
