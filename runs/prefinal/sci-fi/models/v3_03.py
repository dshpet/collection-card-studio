# Rocket: a slim silver body turned as one piece, a red ogive nose cone sitting on its top rim, four red swept
# fins set into the base at 90 degrees apart, a round yellow window with a silver rim on the front, and a dark
# engine bell under the base with a small glowing disc in its mouth (the fire itself is left to the image model).
# It floats in the sky, leaning to the right as it climbs.
import math

SCENE = {"category": "1", "backdrop": "#4fb4ef", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#cfd5dd", "metal")
    red = k.mat("#e0262b", "satin")
    dark = k.mat("#5a6068", "metal")
    window = k.mat("#ffd23a", "gloss")
    fire = k.mat("#ffe9a0", "glow")

    # Body: closed base, slight swell, straight to the nose joint.
    k.lathe([(0, 0.12), (0.085, 0.12), (0.1, 0.135), (0.108, 0.18), (0.112, 0.4), (0.11, 0.68), (0, 0.68)],
            at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # Nose cone: ogive from the body rim to a sharp tip.
    nose = []
    for i in range(17):
        t = i / 16
        nose.append((0.11 * (1 - t * t) ** 0.65, 0.68 + 0.34 * t))
    nose[-1] = (0, 1.02)
    k.lathe([(0, 0.678)] + nose, at=(0, 0, 0), rot=(0, 0, 0), m=red)

    # Round window with a silver rim on the front.
    k.cyl(0.05, 0.02, at=(0, -0.106, 0.56), rot=(90, 0, 0), m=window)
    k.torus(0.055, 0.012, at=(0, -0.112, 0.56), rot=(90, 0, 0), m=silver)

    # Four swept fins, roots buried in the base.
    for a in (45, 135, 225, 315):
        ra = math.radians(a)
        fin = k.box((0.18, 0.024, 0.26), at=(0.17 * math.cos(ra), 0.17 * math.sin(ra), 0.23),
                    rot=(0, 0, a), m=red, bevel=0.008)

        def sweep(p):
            x, y, z = p
            if x > 0:  # outer edge: drop and shorten
                z = -0.2 if z < 0 else -0.02
            return (x, y, z)

        k.warp(fin, sweep)

    # Engine bell under the base and the glowing core in its mouth.
    k.lathe([(0, 0.03), (0.078, 0.03), (0.072, 0.05), (0.056, 0.09), (0.06, 0.125), (0, 0.125)],
            at=(0, 0, 0), rot=(0, 0, 0), m=dark)
    k.cyl(0.062, 0.012, at=(0, 0, 0.026), rot=(0, 0, 0), m=fire)

    k.turn(0, 20, 0)
