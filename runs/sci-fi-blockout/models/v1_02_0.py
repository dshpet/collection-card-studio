# Flying saucer: one round silver hull, a shallow lens with a thin rim edge, a domed top deck and a shallow
# belly with a round under-pod. A metal collar seats the green glass dome on the top deck. Twelve small orange
# lights sit half-sunk in the rim edge, evenly spaced. It floats with no setting, tilted toward the camera so
# the dome and the top deck show along with the rim and a bit of the belly.
import math

SCENE = {"category": "1", "backdrop": "#ffd23a", "azimuth": 0, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    hull = k.mat("#c3c8cf", "metal")
    trim = k.mat("#8d939c", "metal")
    glass = k.mat("#5fd17a", "glass")
    light = k.mat("#ff9a2e", "glow")
    zc = 0.5

    profile = [(0.0, -0.085), (0.1, -0.082), (0.2, -0.072), (0.3, -0.055), (0.38, -0.038), (0.44, -0.022),
               (0.48, -0.01), (0.5, 0.0), (0.5, 0.016), (0.48, 0.028), (0.44, 0.042), (0.38, 0.062),
               (0.32, 0.082), (0.27, 0.098), (0.23, 0.108), (0.0, 0.112)]
    k.lathe(profile, at=(0, 0, zc), m=hull)
    k.cyl(0.13, 0.04, at=(0, 0, zc - 0.095), m=trim, bevel=0.012)

    k.torus(0.2, 0.018, at=(0, 0, zc + 0.112), m=trim)
    dome = [(0.2 * math.cos(math.radians(a)), 0.2 * math.sin(math.radians(a)) * 0.9) for a in range(0, 91, 6)]
    k.lathe([(r, zc + 0.108 + z) for r, z in dome[:-1]] + [(0.0, zc + 0.108 + 0.18)], at=(0, 0, 0), m=glass)

    for i in range(12):
        a = math.radians(i * 30 + 15)
        k.sphere(0.028, at=(0.497 * math.cos(a), 0.497 * math.sin(a), zc + 0.008), m=light)

    k.turn(16, -9, 0)
