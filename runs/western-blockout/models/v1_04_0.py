# Saloon doors: two posts on the ledge carry a header beam; each short door hangs from its post on two gold
# hinges, with a gap below and above. A door is two stiles and three rails, a solid lower panel and vertical
# slats in the top half. Both doors stand swung a little toward the viewer about their hinge lines.
import math

SCENE = {"category": "2", "backdrop": "#ff5f9e", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    frame = k.mat("#7a4424", "matte")
    wood = k.mat("#ecc285", "matte")
    panel = k.mat("#d9a466", "matte")
    gold = k.mat("#f2c23a", "metal")

    # Posts and header.
    for side in (-1, 1):
        k.box((0.08, 0.1, 1.2), at=(side * 0.48, 0, 0.6), m=frame, bevel=0.008)
        k.box((0.11, 0.13, 0.06), at=(side * 0.48, 0, 0.03), m=frame, bevel=0.008)
    k.box((1.12, 0.13, 0.1), at=(0, 0, 1.25), m=frame, bevel=0.01)

    def door(hx, theta):
        t = math.radians(theta)
        c, s = math.cos(t), math.sin(t)

        def part(u0, u1, z0, z1, thick, m, v=0.0):
            u, z = (u0 + u1) / 2, (z0 + z1) / 2
            at = (hx + u * c - v * s, u * s + v * c, z)
            return k.box((u1 - u0, thick, z1 - z0), at=at, rot=(0, 0, theta), m=m, bevel=0.005)

        part(0.015, 0.065, 0.28, 0.92, 0.036, wood)    # hinge stile
        part(0.375, 0.425, 0.30, 0.86, 0.036, wood)    # latch stile
        for z0, z1 in ((0.30, 0.37), (0.55, 0.61), (0.80, 0.86)):
            part(0.065, 0.375, z0, z1, 0.034, wood)    # rails
        part(0.065, 0.375, 0.37, 0.55, 0.018, panel)   # lower panel
        n, inner = 5, 0.31
        for i in range(n):
            u = 0.065 + inner * (i + 0.5) / n
            part(u - 0.018, u + 0.018, 0.61, 0.80, 0.014, panel)  # slats
        for z in (0.40, 0.80):
            k.cyl(0.02, 0.08, at=(hx, 0, z), rot=(0, 0, 0), m=gold)
            part(0.02, 0.07, z - 0.025, z + 0.025, 0.006, gold, v=-0.021)

    door(-0.44, -12)
    door(0.44, 180 + 18)

    # Wooden plank ledge, top at z = 0.
    for i, y in enumerate((-1.15, -0.85, -0.55, -0.25, 0.05, 0.35, 0.65, 0.95)):
        tone = "#c48a52" if i % 2 else "#b97d47"
        k.box((5, 0.29, 0.14), at=(0, y, -0.07), m=k.mat(tone, "matte"), bevel=0.01, setting=True)
