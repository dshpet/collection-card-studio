# Flying saucer: one lathed purple hull, wide and thin, swelling to a rounded rim. A darker band runs round the
# rim and carries a ring of fourteen white lights, half sunk into it. A collar on top holds the green glass dome.
# The underside has a small glowing emitter disk set into its belly; the light beam itself is left to the image
# model. It floats, tipped toward the camera so the dome and the top of the hull show.
import math

SCENE = {"category": "1", "backdrop": "#ffd23a", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    hull = k.mat("#7b3fc4", "satin")
    band = k.mat("#5a2a9a", "satin")
    trim = k.mat("#c9ced6", "metal")
    glass = k.mat("#5fe07a", "glass")
    lamp = k.mat("#fffbea", "glow")

    z0 = 0.45
    prof = [(0.0, 0.0), (0.10, 0.0), (0.16, 0.012), (0.24, 0.035), (0.32, 0.062), (0.40, 0.092),
            (0.46, 0.115), (0.50, 0.132), (0.52, 0.148), (0.515, 0.162), (0.49, 0.175), (0.44, 0.195),
            (0.36, 0.218), (0.28, 0.236), (0.20, 0.248), (0.10, 0.255), (0.0, 0.257)]
    k.lathe([(r, z0 + z) for r, z in prof], at=(0, 0, 0), rot=(0, 0, 0), m=hull, verts=96)

    # rim band and its ring of lights
    k.torus(0.505, 0.028, at=(0, 0, z0 + 0.15), rot=(0, 0, 0), m=band)
    n = 14
    for i in range(n):
        a = 2 * math.pi * i / n
        k.sphere(0.03, at=(0.53 * math.cos(a), 0.53 * math.sin(a), z0 + 0.15), m=lamp)

    # dome on its collar
    k.cyl(0.215, 0.03, at=(0, 0, z0 + 0.262), m=trim, bevel=0.008)
    dome = [(0.2 * math.cos(math.radians(t)), z0 + 0.275 + 0.19 * math.sin(math.radians(t)))
            for t in range(0, 91, 6)]
    dome[-1] = (0.0, dome[-1][1])
    k.lathe(dome, at=(0, 0, 0), rot=(0, 0, 0), m=glass)

    # underside emitter: a metal ring with a glowing disk
    k.torus(0.1, 0.016, at=(0, 0, z0 + 0.004), rot=(0, 0, 0), m=trim)
    k.cyl(0.095, 0.02, at=(0, 0, z0 - 0.002), m=lamp, bevel=0.006)

    k.turn(14, -6, 0)
