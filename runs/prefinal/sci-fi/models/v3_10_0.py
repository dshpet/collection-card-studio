# Hover car: one rounded yellow body, nose toward -y, with a glass bubble canopy set into its top on a trim ring.
# Two pods under the belly, front and rear, each hold a glowing pink light. A small tail fin rises at the back.
# No wheels. It floats in clear sky, banked a little so it shows its nose, its right side and its top.
import math

SCENE = {"category": "1", "backdrop": "#4ab3ee", "azimuth": 35, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    yellow = k.mat("#ffc61a", "satin")
    trim = k.mat("#e09a12", "satin")
    glass = k.mat("#d8f3ff", "glass")
    grey = k.mat("#5a606b", "satin")
    pink = k.mat("#ff4fb8", "glow")

    # Main body: a long rounded hull, a little fuller at the back.
    k.blob([
        (0, -0.08, 0.30, 0.30, (1.0, 1.6, 0.55)),
        (0, 0.18, 0.31, 0.27, (1.05, 1.0, 0.6)),
    ], yellow)

    # Side skirts along the waist.
    for side in (-1, 1):
        k.tube([(side * 0.27, -0.36, 0.27), (side * 0.30, -0.05, 0.26),
                (side * 0.29, 0.25, 0.27), (side * 0.22, 0.42, 0.28)], 0.03, trim, curved=True)

    # Canopy: a glass bubble seated on a ring in the body top.
    k.sphere(0.2, at=(0, -0.02, 0.44), scale=(0.85, 1.2, 0.72), m=glass)
    ring = [(0.17 * math.cos(math.radians(a)), -0.02 + 0.235 * math.sin(math.radians(a)), 0.452)
            for a in range(0, 361, 15)]
    k.tube(ring, 0.02, trim, curved=True)
    k.box((0.16, 0.08, 0.1), at=(0, 0.06, 0.48), m=grey, bevel=0.02)  # seat back inside the bubble

    # Tail fin.
    k.box((0.04, 0.18, 0.14), at=(0, 0.38, 0.47), rot=(-25, 0, 0), m=yellow, bevel=0.02)

    # Underlights: pods sunk into the belly, glowing discs facing down.
    for y in (-0.25, 0.25):
        k.cyl(0.075, 0.06, at=(0, y, 0.16), m=grey, bevel=0.01)
        k.cyl(0.055, 0.012, at=(0, y, 0.126), m=pink, bevel=0.004)

    k.turn(-4, 7, 0)
