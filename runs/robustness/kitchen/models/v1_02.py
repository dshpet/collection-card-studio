# Stovetop kettle: a rounded, flat-bottomed red body stands on the floor. A domed lid sits in the top opening,
# with a silver rim and a round silver knob on a short stem. The curved spout grows out of the lower body on the
# -x side and rises outward to a flared tip. The black handle arches over the lid in the same plane and is held at
# both ends by silver mounts on the body's shoulder, one above the spout and one on the opposite side.
SCENE = {"category": "2", "backdrop": "#8a3fd1", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    red = k.mat("#e0222b", "gloss")
    silver = k.mat("#cfd4dc", "metal")
    black = k.mat("#1c1c20", "satin")

    # Body: wide rounded belly, flat base, shoulder curving in to the lid opening.
    body = [(0.0, 0.0), (0.30, 0.0), (0.35, 0.012), (0.385, 0.04), (0.41, 0.09), (0.422, 0.15),
            (0.418, 0.21), (0.40, 0.27), (0.37, 0.32), (0.33, 0.36), (0.28, 0.395), (0.23, 0.418),
            (0.20, 0.428), (0.0, 0.428)]
    k.lathe(body, at=(0, 0, 0), rot=(0, 0, 0), m=red)

    # Lid: silver rim ring, red dome, silver knob on a stem.
    k.torus(0.2, 0.014, at=(0, 0, 0.432), rot=(0, 0, 0), m=silver)
    lid = [(0.0, 0.425), (0.195, 0.425), (0.195, 0.44), (0.18, 0.465), (0.15, 0.49), (0.11, 0.508),
           (0.06, 0.518), (0.0, 0.521)]
    k.lathe(lid, at=(0, 0, 0), rot=(0, 0, 0), m=red)
    k.cyl(0.022, 0.04, at=(0, 0, 0.535), rot=(0, 0, 0), m=silver)
    k.sphere(0.045, at=(0, 0, 0.575), m=silver)

    # Spout: rooted in the lower belly, curving up and out, with a flared tip.
    k.tube([(-0.33, 0.0, 0.13), (-0.44, 0.0, 0.17), (-0.53, 0.0, 0.25), (-0.59, 0.0, 0.35),
            (-0.62, 0.0, 0.41)], 0.048, red, curved=True)
    k.sphere(0.07, at=(-0.36, 0.0, 0.14), scale=(0.6, 1, 1), m=red)
    k.cone(0.044, 0.058, 0.06, at=(-0.632, 0.0, 0.44), rot=(0, -25, 0), m=red)

    # Handle: black arch over the lid, held by silver mounts on the shoulder.
    for side in (-1, 1):
        k.cyl(0.04, 0.05, at=(side * 0.3, 0.0, 0.355), rot=(0, side * 45, 0), m=silver)
        k.sphere(0.035, at=(side * 0.27, 0.0, 0.39), m=silver)
    k.tube([(-0.27, 0.0, 0.39), (-0.27, 0.0, 0.52), (-0.19, 0.0, 0.68), (0.0, 0.0, 0.75),
            (0.19, 0.0, 0.68), (0.27, 0.0, 0.52), (0.27, 0.0, 0.39)], 0.032, black, curved=True)

    # Plain floor, a shade lighter than the backdrop.
    k.box((8, 8, 0.1), at=(0, 1.5, -0.05), m=k.mat("#a466e2", "matte"), bevel=0, setting=True)
