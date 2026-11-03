# Tombstone: an upright stone slab with a round arched top stands on a wider stone plinth. A chunk is broken out
# of the arch's upper right corner, and a crack runs down the front face from the break. A small cross is raised
# on the front near the top. Moss grows over the slab's lower left corner and on the arch's top left, and a small
# orange flower lies on the plinth. The tombstone stands on a plain stone ledge.
import math

SCENE = {"category": "2", "backdrop": "#ffc62e", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    stone = k.mat("#b9bec4", "matte")
    plinth = k.mat("#a3a9b0", "matte")
    crack = k.mat("#5d6268", "matte")
    moss = k.mat("#5fae3a", "matte")
    petal = k.mat("#ff8a1f", "matte")

    # Plinth, slab body and the arch that rounds its top.
    k.box((0.78, 0.3, 0.1), at=(0, 0, 0.05), m=plinth, bevel=0.015)
    k.box((0.6, 0.16, 0.465), at=(0, 0, 0.3325), m=stone, bevel=0.02)
    arch = k.cyl(0.3, 0.16, at=(0, 0, 0.55), rot=(90, 0, 0), m=stone, bevel=0.02, verts=96)

    # Broken corner: a jagged notch through the arch between 18 and 52 degrees from the right side.
    lo, hi = math.radians(18), math.radians(52)
    jag = [0.0, 0.05, 0.035, 0.085, 0.07, 0.095, 0.06, 0.075, 0.03, 0.0]

    def chip(p):
        x, y, z = p
        a = math.atan2(y, x)
        if lo < a < hi:
            t = (a - lo) / (hi - lo) * (len(jag) - 1)
            i = min(int(t), len(jag) - 2)
            d = jag[i] + (jag[i + 1] - jag[i]) * (t - i)
            r = math.hypot(x, y) - d
            return (r * math.cos(a), r * math.sin(a), z)
        return p

    k.warp(arch, chip)

    # Crack running down the front face from the break.
    k.tube([(0.19, -0.081, 0.66), (0.15, -0.081, 0.6), (0.17, -0.081, 0.53),
            (0.12, -0.081, 0.46), (0.13, -0.081, 0.4)], 0.008, crack)

    # Raised cross near the top of the front face.
    k.box((0.05, 0.03, 0.2), at=(0, -0.088, 0.66), m=stone, bevel=0.008)
    k.box((0.15, 0.03, 0.05), at=(0, -0.088, 0.705), m=stone, bevel=0.008)

    # Moss over the lower left corner, spilling onto the plinth, and a patch on the arch's top left.
    k.blob([(-0.26, -0.085, 0.14, 0.05, (1.2, 0.5, 1.0)), (-0.29, -0.08, 0.22, 0.035, (1.0, 0.5, 1.1)),
            (-0.2, -0.1, 0.105, 0.045, (1.4, 0.9, 0.35)), (-0.3, -0.04, 0.12, 0.04, (0.6, 1.2, 0.9))], moss)
    k.blob([(-0.18, 0.0, 0.78, 0.045, (1.3, 1.7, 0.45)), (-0.24, 0.0, 0.745, 0.035, (1.0, 1.6, 0.5))], moss)

    # Small orange flower lying on the plinth, its stem along the plinth top.
    cx, cy, cz = 0.24, -0.1, 0.11
    for i in range(5):
        a = math.radians(i * 72 + 10)
        k.sphere(0.024, at=(cx + 0.026 * math.cos(a), cy + 0.026 * math.sin(a), cz), scale=(1, 1, 0.4), m=petal)
    k.sphere(0.016, at=(cx, cy, cz + 0.006), m=k.mat("#ffd23a", "matte"))
    k.tube([(cx + 0.03, cy + 0.02, 0.106), (cx + 0.08, cy + 0.04, 0.106), (cx + 0.13, cy + 0.07, 0.106)],
           0.007, moss, curved=True)

    k.box((4, 1.8, 0.12), at=(0, 0.3, -0.06), m=k.mat("#e6d6a8", "matte"), bevel=0.01, setting=True)
