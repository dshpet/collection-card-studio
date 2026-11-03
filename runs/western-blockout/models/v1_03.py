# Lasso: one rope. A free end hangs from the bottom of a four-turn hand coil standing face-on; the turns are
# gathered at the top, where a red tie binds the bundle, and below it they differ in size, fan apart and sag
# under their weight. The rope leaves the coil's bottom, runs right and passes through the honda (eye knot),
# goes all the way round as the big open loop and ends at the honda, whose eye is tied on that end.
import math

SCENE = {"category": "1", "backdrop": "#8a4fd8", "azimuth": 22, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d4a04c", "matte")
    cream = k.mat("#f3e3b8", "matte")
    red = k.mat("#e0302b", "matte")
    r = 0.03

    # Hand coil: four turns in the xz plane, stacked in y. They are gathered at the top (f = 0); toward the
    # bottom (f = 1) each turn has its own size and offset and sags, so the turns fan apart like real rope.
    cx, cz, R = -0.25, 0.52, 0.27
    coil = []
    for i in range(65):
        t = -math.pi / 2 + i * math.pi / 8
        d = i / 16 - 2
        f = (1 - math.sin(t)) / 2
        rr = R + 0.022 * d * f
        x = cx + 0.032 * d * f + rr * math.cos(t)
        z = cz + rr * math.sin(t) - 0.035 * f * (1 + 0.3 * d)
        coil.append((x, -0.09 + 0.18 * i / 64, z))
    tail = [(cx - 0.14, -0.11, cz - R - 0.3), (cx - 0.11, -0.1, cz - R - 0.17), (cx - 0.08, -0.095, cz - R - 0.05)]
    honda = (0.2, 0.0, 0.36)
    lead = [(cx + 0.2, 0.06, cz - R - 0.06), (0.06, 0.03, 0.29), honda]

    # Big open loop: through the eye, all the way round, and back to the honda where the rope ends.
    c, a, b = (0.53, 0.56), 0.37, 0.34
    loop = []
    for j in range(17):
        ang = math.radians(235 + j * 20)
        loop.append((c[0] + a * math.cos(ang), 0.04 * j / 16, c[1] + b * math.sin(ang)))
    end = (honda[0], 0.0, honda[2] + 0.055)
    loop.append(end)
    k.tube(tail + coil + lead + loop, r, rope, curved=True)
    k.sphere(r * 1.05, at=tail[0], m=cream)  # whipped free end
    k.torus(0.05, 0.024, at=honda, rot=(0, 90, -35), m=cream)
    k.sphere(0.034, at=end, m=cream)  # the eye knot on the rope's end

    # Red tie: two bands round the gathered bundle at the top of the coil, with two short ends.
    top = cz + R
    for dx in (-0.03, 0.03):
        band = [(cx + dx, 0.118 * math.cos(math.radians(a2)), top + 0.05 * math.sin(math.radians(a2)))
                for a2 in range(0, 361, 20)]
        k.tube(band, 0.016, red, curved=True)
    knot = (cx, -0.02, top + 0.055)
    k.sphere(0.024, at=knot, m=red)
    k.tube([knot, (cx - 0.05, -0.04, top + 0.12)], 0.016, red)
    k.tube([knot, (cx + 0.05, -0.04, top + 0.12)], 0.016, red)

    k.turn(8, -10, 12)
