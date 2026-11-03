# Lasso: one rope. A free end hangs from the bottom of a four-turn hand coil standing face-on; the coil is
# bound at the top by a red tie. The rope leaves the coil's bottom, runs right to the honda (eye knot), and the
# big open loop starts at the honda, goes all the way round and passes back through the eye.
import math

SCENE = {"category": "1", "backdrop": "#8a4fd8", "azimuth": 22, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d4a04c", "matte")
    cream = k.mat("#f3e3b8", "matte")
    red = k.mat("#e0302b", "matte")
    r = 0.03

    # Hand coil: four turns in the xz plane, stepping back in y, starting and ending at the bottom.
    cx, cz, R = -0.25, 0.52, 0.27
    coil = []
    for i in range(65):
        t = -math.pi / 2 + i * math.pi / 8
        rr = R + 0.012 * math.sin(1.7 * t)
        coil.append((cx + rr * math.cos(t), -0.06 + 0.12 * i / 64, cz + rr * math.sin(t)))
    tail = [(cx - 0.11, -0.075, cz - R - 0.2), (cx - 0.06, -0.07, cz - R - 0.09)]
    honda = (0.2, 0.0, 0.36)
    lead = [(cx + 0.12, 0.05, cz - R + 0.005), (0.06, 0.03, 0.29), honda]
    k.tube(tail + coil + lead, r, rope, curved=True)
    k.sphere(r * 1.05, at=tail[0], m=cream)  # whipped free end

    # Big open loop: from the honda all the way round and back through the eye.
    c, a, b = (0.53, 0.56), 0.37, 0.34
    loop = [(honda[0], -0.02, honda[2])]
    for j in range(18):
        ang = math.radians(235 + j * 20)
        loop.append((c[0] + a * math.cos(ang), -0.02 + 0.04 * j / 17, c[1] + b * math.sin(ang)))
    loop.append((honda[0] - 0.06, 0.02, honda[2] - 0.03))
    k.tube(loop, r, rope, curved=True)
    k.torus(0.05, 0.024, at=honda, rot=(0, 90, -35), m=cream)

    # Red tie binding the coil bundle at its top, with two short ends.
    top = (cx, 0.0, cz + R)
    for dx in (-0.025, 0.025):
        k.torus(0.085, 0.018, at=(top[0] + dx, 0, top[2]), rot=(0, 90, 0), m=red)
    k.tube([(cx, -0.08, top[2] + 0.06), (cx - 0.05, -0.1, top[2] + 0.12)], 0.016, red)
    k.tube([(cx, -0.08, top[2] + 0.06), (cx + 0.05, -0.1, top[2] + 0.12)], 0.016, red)

    k.turn(8, -10, 12)
