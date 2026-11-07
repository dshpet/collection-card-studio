# Hover car: one rounded yellow body, nose toward -y, with a glass bubble canopy rising from its top on a trim ring.
# Two domed pods under the belly, front and rear, each hold a glowing pink light. A low tail fin sits at the back.
# No wheels. It floats in clear sky, banked toward the camera so it shows its nose, its right side, its top and
# enough of its belly to show the two underlights.
import math

SCENE = {"category": "1", "backdrop": "#4ab3ee", "azimuth": 35, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    yellow = k.mat("#ffc61a", "satin")
    trim = k.mat("#e09a12", "satin")
    glass = k.mat("#d8f3ff", "glass")
    grey = k.mat("#4a505b", "satin")
    pink = k.mat("#ff4fb8", "glow")

    # Main body: a long rounded hull, a little fuller at the back.
    k.blob([
        (0, -0.08, 0.30, 0.30, (1.0, 1.6, 0.55)),
        (0, 0.18, 0.31, 0.27, (1.05, 1.0, 0.6)),
    ], yellow)

    # Side skirts along the waist, both ends tucked into the hull.
    for side in (-1, 1):
        k.tube([(side * 0.19, -0.40, 0.27), (side * 0.29, -0.12, 0.26), (side * 0.30, 0.12, 0.26),
                (side * 0.24, 0.36, 0.27), (side * 0.12, 0.44, 0.28)], 0.03, trim, curved=True)

    # Canopy: a glass bubble rising clear of the body top, seated on a trim ring, with a dark seat inside.
    k.sphere(0.2, at=(0, -0.02, 0.47), scale=(0.85, 1.2, 0.85), m=glass)
    ring = [(0.17 * math.cos(math.radians(a)), -0.02 + 0.24 * math.sin(math.radians(a)), 0.47)
            for a in range(0, 361, 15)]
    k.tube(ring, 0.022, trim, curved=True)
    k.cyl(0.16, 0.02, at=(0, -0.02, 0.465), m=grey, bevel=0.005)  # cockpit floor
    k.box((0.16, 0.06, 0.13), at=(0, 0.07, 0.53), m=grey, bevel=0.025)  # seat back

    # Low tail fin on the rear deck.
    k.box((0.035, 0.16, 0.09), at=(0, 0.36, 0.47), rot=(-30, 0, 0), m=yellow, bevel=0.015)

    # Underlights: domed grey pods under the belly, each with a large glowing pink lens facing down.
    for y in (-0.25, 0.25):
        k.cyl(0.09, 0.08, at=(0, y, 0.16), m=grey, bevel=0.012)
        k.sphere(0.075, at=(0, y, 0.12), scale=(1, 1, 0.55), m=pink)

    # Bank toward the camera so the belly lights show.
    k.turn(-6, -16, 0)
