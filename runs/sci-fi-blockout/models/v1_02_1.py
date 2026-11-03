# Flying saucer: one round silver hull, a shallow lens with a thin rim edge, a domed top deck and a shallow
# belly with a round under-pod. A metal collar seats the green glass dome on the top deck. Twelve small orange
# lights sit half-sunk in the rim edge, evenly spaced. It floats with no setting, tilted toward the camera so
# the dome and the top deck show along with the rim and a bit of the belly.
import math

SCENE = {"category": "1", "backdrop": "#ffd23a", "azimuth": 0, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    hull = k.mat("#a9afb8", "metal")
    trim = k.mat("#7d838c", "metal")
    glass = k.mat("#4fc46c", "glass")
    light = k.mat("#ff5e14", "glow")
    zc = 0.5

    belly = [(0.5 * i / 24, -0.085 * (1 - (i / 24) ** 1.8)) for i in range(25)]
    deck = [(0.5 - 0.27 * i / 24, 0.016 + 0.092 * (1 - (1 - i / 24) ** 1.6)) for i in range(25)]
    profile = belly + deck + [(0.0, 0.112)]
    k.lathe(profile, at=(0, 0, zc), m=hull, verts=128)
    k.cyl(0.13, 0.04, at=(0, 0, zc - 0.095), m=trim, bevel=0.012)

    k.torus(0.2, 0.018, at=(0, 0, zc + 0.112), m=trim)
    dome = [(0.2 * math.cos(math.radians(a)), 0.2 * math.sin(math.radians(a)) * 0.9) for a in range(0, 91, 6)]
    k.lathe([(r, zc + 0.108 + z) for r, z in dome[:-1]] + [(0.0, zc + 0.108 + 0.18)], at=(0, 0, 0), m=glass)

    for i in range(12):
        a = math.radians(i * 30 + 15)
        k.sphere(0.032, at=(0.497 * math.cos(a), 0.497 * math.sin(a), zc + 0.008), m=light)

    k.turn(16, -9, 0)
