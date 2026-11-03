# Moon rover: a white boxy body on a rocker-bogie on each side. The rocker pivots on a pin in the body side,
# runs down to the front wheel and back to the bogie pivot; the bogie carries the middle and rear wheels.
# Each of the six black wheels turns on an axle stub at the end of its arm. A small orange dish sits on a mast at
# the back of the roof, and a tiny solar panel stands on a short post at the front, tilted toward the camera.
# The rover's front faces +x, so the three-quarter view shows the long side with all three wheels near the camera.
# It stands on a slab of gray moon dust that runs off the card at the front; its back edge makes the horizon.
SCENE = {"category": "3", "backdrop": "#a6e23a", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f2", "satin")
    tire = k.mat("#1f2023", "matte")
    hub = k.mat("#9aa0a8", "metal")
    arm = k.mat("#b9bec6", "metal")
    orange = k.mat("#ff8a1f", "satin")
    cell = k.mat("#24409a", "glass")

    # Body.
    k.box((0.72, 0.42, 0.24), at=(0, 0, 0.38), m=white, bevel=0.04)
    k.box((0.6, 0.34, 0.04), at=(0, 0, 0.51), m=white, bevel=0.015)

    wr, ww, wz = 0.12, 0.085, 0.12
    for s in (-1, 1):
        ya, yw = s * 0.25, s * 0.305
        # Rocker: front wheel up to the body pivot, back down to the bogie pivot.
        k.tube([(0.3, ya, wz), (0.05, ya, 0.3), (-0.15, ya, 0.2)], 0.022, arm)
        # Bogie: middle wheel, bogie pivot, rear wheel.
        k.tube([(0.0, ya, wz), (-0.15, ya, 0.2), (-0.3, ya, wz)], 0.022, arm)
        k.cyl(0.035, 0.06, at=(0.05, s * 0.235, 0.3), rot=(90, 0, 0), m=hub)
        k.cyl(0.03, 0.04, at=(-0.15, ya, 0.2), rot=(90, 0, 0), m=hub)
        for x in (0.3, 0.0, -0.3):
            k.cyl(0.022, 0.05, at=(x, s * 0.27, wz), rot=(90, 0, 0), m=hub)
            k.cyl(wr, ww, at=(x, yw, wz), rot=(90, 0, 0), m=tire, bevel=0.02)
            k.cyl(0.05, ww + 0.01, at=(x, yw, wz), rot=(90, 0, 0), m=hub)

    # Small dish antenna on a mast at the back of the roof, turned toward the front-left.
    k.cyl(0.022, 0.16, at=(-0.18, 0.06, 0.59), m=arm)
    profile = [(0.0, 0.0), (0.025, 0.002), (0.05, 0.007), (0.075, 0.016), (0.1, 0.029), (0.112, 0.037),
               (0.108, 0.043), (0.075, 0.024), (0.05, 0.015), (0.025, 0.01), (0.0, 0.008)]
    k.lathe(profile, at=(-0.18, 0.06, 0.665), rot=(35, 0, 30), m=orange)
    n = (0.287, -0.5, 0.819)
    c = (-0.18, 0.06, 0.67)
    tip = tuple(c[i] + 0.075 * n[i] for i in range(3))
    k.tube([c, tip], 0.01, arm)
    k.sphere(0.018, at=tip, m=orange)

    # Tiny solar panel on a short post at the front of the roof, its cells tilted toward the camera.
    k.cyl(0.018, 0.08, at=(0.17, -0.02, 0.56), m=arm)
    k.box((0.24, 0.17, 0.016), at=(0.17, -0.02, 0.605), rot=(20, 0, 0), m=arm, bevel=0.004)
    k.box((0.22, 0.15, 0.008), at=(0.17, -0.023, 0.614), rot=(20, 0, 0), m=cell, bevel=0.002)

    # Gray moon dust slab running off the card at the front; its back edge is the horizon.
    k.box((10, 6, 0.1), at=(0, -0.5, -0.05), m=k.mat("#7b7b82", "matte"), bevel=0.02, setting=True)
