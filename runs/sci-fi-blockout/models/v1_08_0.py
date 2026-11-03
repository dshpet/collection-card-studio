# Telescope: a long cream tube tilted up 30 degrees, held at its balance point by a clamp ring on an axle
# between two fork plates; the fork stands on a round head, and three wooden legs hinge under the head and
# spread to the ground. At the back the tube steps down to a brass focuser collar and the eyepiece.
# It stands on a slab of gray moon dust that runs back to the teal backdrop.
import math

SCENE = {"category": "3", "backdrop": "#1ec8c0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    cream = k.mat("#f1e6c8", "satin")
    wood = k.mat("#8a5530", "matte")
    brass = k.mat("#d2a23a", "metal")
    dark = k.mat("#3b3f46", "satin")
    lens = k.mat("#2f5f8f", "glass")

    pivot, tilt = (0.0, 0.0, 0.72), 30
    d = (math.cos(math.radians(tilt)), 0.0, math.sin(math.radians(tilt)))
    rot = (0, 90 - tilt, 0)

    def on_axis(s):
        return (pivot[0] + s * d[0], pivot[1] + s * d[1], pivot[2] + s * d[2])

    def section(r, s0, s1, m, bevel=0.006):
        return k.cyl(r, s1 - s0, at=on_axis((s0 + s1) / 2), rot=rot, m=m, bevel=bevel)

    # Tube, front dew shield and objective glass, back cap, brass focuser collar, eyepiece and eyecup.
    section(0.07, -0.40, 0.44, cream)
    section(0.082, 0.42, 0.56, cream, bevel=0.01)
    section(0.066, 0.555, 0.565, lens, bevel=0.002)
    section(0.06, -0.45, -0.39, dark)
    section(0.036, -0.51, -0.44, brass)
    section(0.024, -0.61, -0.50, dark)
    section(0.032, -0.65, -0.60, dark, bevel=0.008)

    # Clamp ring around the tube at the pivot, the axle through it, and the fork plates holding the axle.
    k.torus(0.078, 0.014, at=pivot, rot=rot, m=dark)
    k.cyl(0.016, 0.25, at=pivot, rot=(90, 0, 0), m=dark)
    for y in (-0.108, 0.108):
        k.box((0.07, 0.022, 0.17), at=(0, y, 0.66), m=dark, bevel=0.006)
        k.cyl(0.026, 0.012, at=(0, y * 1.1, 0.72), rot=(90, 0, 0), m=dark)
    k.box((0.09, 0.24, 0.03), at=(0, 0, 0.59), m=dark, bevel=0.006)

    # Round tripod head and three wooden legs hinged under it, each with a foot on the ground.
    k.cyl(0.1, 0.05, at=(0, 0, 0.55), m=wood, bevel=0.01)
    for a in (-90, 30, 150):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        top = (0.06 * c, 0.06 * s, 0.53)
        foot = (0.4 * c, 0.4 * s, 0.02)
        k.tube([top, foot], 0.024, wood)
        k.sphere(0.022, at=(0.075 * c, 0.075 * s, 0.525), m=brass)
        k.sphere(0.03, at=(foot[0], foot[1], 0.018), scale=(1, 1, 0.6), m=dark)

    # Gray moon dust ground.
    k.box((6, 3.2, 0.2), at=(0, 0.9, -0.1), m=k.mat("#a3a3a6", "matte"), bevel=0.02, setting=True)
