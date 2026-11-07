# Flying saucer: one lens-shaped silver hull, turned on a lathe, thickest at the rim. A light-grey collar sits on
# the top deck and holds the smooth glass dome; a light-grey belly pod sits under the hull. A raised metal band
# runs round the rim edge and carries twelve round yellow lights, evenly spaced, each half sunk into the band.
# The saucer floats in clear sky, tilted toward the camera so the dome, the top deck and the lit rim all show.
import math

SCENE = {"category": "1", "backdrop": "#45b0ef", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    grey = k.mat("#dfe3e8", "satin")
    band = k.mat("#9aa1ab", "metal")
    glass = k.mat("#bfe6f7", "glass")
    lamp = k.mat("#ffd23a", "glow")

    z0 = 0.4  # bottom of the hull
    hull = [(0.0, 0.0), (0.12, 0.004), (0.22, 0.018), (0.31, 0.04), (0.39, 0.066), (0.45, 0.09),
            (0.49, 0.11), (0.505, 0.125), (0.508, 0.135), (0.503, 0.147), (0.48, 0.16), (0.43, 0.178),
            (0.36, 0.196), (0.28, 0.211), (0.2, 0.22), (0.1, 0.225), (0.0, 0.226)]
    k.lathe(hull, at=(0, 0, z0), m=silver, verts=96)

    # rim band and its ring of lights
    k.torus(0.505, 0.022, at=(0, 0, z0 + 0.133), m=band)
    for i in range(12):
        a = 2 * math.pi * i / 12
        k.sphere(0.034, at=(0.522 * math.cos(a), 0.522 * math.sin(a), z0 + 0.133), m=lamp)

    # collar and glass dome on the top deck
    collar = [(0.0, 0.0), (0.25, 0.0), (0.255, 0.012), (0.25, 0.03), (0.215, 0.04), (0.0, 0.04)]
    k.lathe(collar, at=(0, 0, z0 + 0.212), m=grey)
    dome = [(0.205 * math.cos(math.radians(t)), 0.2 * math.sin(math.radians(t))) for t in range(0, 91, 6)]
    dome[-1] = (0.0, 0.2)
    k.lathe(dome, at=(0, 0, z0 + 0.248), m=glass)

    # belly pod under the hull
    pod = [(0.0, -0.045), (0.06, -0.042), (0.11, -0.03), (0.14, -0.014), (0.15, 0.0), (0.15, 0.01), (0.0, 0.01)]
    k.lathe(pod, at=(0, 0, z0 + 0.004), m=grey)

    k.turn(14, -6, 0)
