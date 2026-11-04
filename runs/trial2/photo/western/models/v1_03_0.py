# Lasso: one continuous rope. A free tail hangs from the inside of a hand coil of five stacked turns; a red tie
# binds the turns together on the coil's left side. The rope leaves the coil, passes through the honda (the small
# cream eye) and runs once around as the big open loop, whose end is tied into the honda.
import math

SCENE = {"category": "1", "backdrop": "#8a5cd8", "azimuth": 20, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d9a85a", "matte")
    cream = k.mat("#f2e2b8", "matte")
    red = k.mat("#d8262c", "matte")
    r = 0.024

    # Big loop in the xz plane behind the coil; the honda sits on its left side.
    lc, lrx, lrz, ly = (0.12, 0.05, 0.42), 0.40, 0.38, 0.05
    t0 = math.radians(200)
    honda = (lc[0] + lrx * math.cos(t0), ly, lc[2] + lrz * math.sin(t0))
    tan = (-math.sin(t0), 0.0, math.cos(t0))

    # Hand coil, upper left, in front of the loop.
    cc, crx, crz = (-0.28, -0.09, 0.72), 0.20, 0.22
    turns, y0, y1 = 5.0, -0.19, 0.01
    a_start, a_end = -math.pi / 2 + 0.6, -math.pi / 2 + 0.6 + turns * 2 * math.pi
    n = int(turns * 24)
    coil = []
    for i in range(n + 1):
        a = a_start + (a_end - a_start) * i / n
        f = i / n
        wob = 1.0 + 0.04 * math.sin(3.1 * a)
        coil.append((cc[0] + crx * wob * math.cos(a), y0 + (y1 - y0) * f, cc[2] + crz * wob * math.sin(a)))

    # Free tail hanging from the start of the coil.
    s = coil[0]
    tail = [(s[0] - 0.01, s[1] - 0.005, s[2] - 0.07), (s[0] - 0.03, s[1] - 0.01, s[2] - 0.15),
            (s[0] - 0.02, s[1] - 0.01, s[2] - 0.21)]
    tail.reverse()

    # Lead from the coil down through the honda.
    e = coil[-1]
    lead = [(e[0] - 0.04, 0.03, e[2] - 0.08),
            (honda[0] - 0.08 * tan[0], ly, honda[2] - 0.08 * tan[2]),
            honda]

    # The loop: from the honda once around, ending at the honda's rim.
    loop = []
    m = 60
    for i in range(1, m + 1):
        t = t0 + math.radians(348) * i / m
        loop.append((lc[0] + lrx * math.cos(t), ly + 0.035 * math.sin(t - t0), lc[2] + lrz * math.sin(t)))

    k.tube(tail + coil + lead + loop, r, rope, curved=True)
    k.sphere(r * 1.15, at=tail[0], m=cream)  # whipped end of the free tail

    # Honda: a rope eye around the running rope, its axis along the loop.
    theta = math.degrees(math.atan2(tan[0], tan[2]))
    k.torus(0.042, 0.016, at=honda, rot=(0, theta, 0), m=cream)
    back = (honda[0] - 0.05 * tan[0], ly, honda[2] - 0.05 * tan[2])
    k.cyl(0.03, 0.045, at=back, rot=(0, theta, 0), m=cream, bevel=0.008)  # seizing where the loop end ties in

    # Red tie binding the coil turns on its left side.
    tx, tz, ty = cc[0] - crx * 1.0, cc[2], (y0 + y1) / 2
    k.box((0.07, (y1 - y0) + 0.09, 0.065), at=(tx, ty, tz), m=red, bevel=0.02)
    k.sphere(0.034, at=(tx - 0.045, ty - 0.02, tz), m=red)
    k.box((0.018, 0.035, 0.11), at=(tx - 0.06, ty - 0.03, tz - 0.07), rot=(0, -20, 0), m=red, bevel=0.008)
    k.box((0.018, 0.035, 0.09), at=(tx - 0.05, ty - 0.0, tz - 0.065), rot=(0, 15, 0), m=red, bevel=0.008)

    k.turn(8, -12, -15)
