# Lasso: one continuous rope. A free tail hangs from the lower left of a hand coil of five bundled turns that sag
# like a held coil; a red tie binds the turns together on the coil's left side. The rope leaves the coil at its lower
# right, runs in one smooth curve down to the honda (the small cream eye), and runs once around as the big open loop,
# whose end is seized beside the honda. The coil sits above-left of a tall loop so the whole reads square on the card.
import math

SCENE = {"category": "1", "backdrop": "#8a5cd8", "azimuth": 20, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d9a85a", "matte")
    cream = k.mat("#f2e2b8", "matte")
    red = k.mat("#d8262c", "matte")
    r = 0.024

    # Big loop in the xz plane behind the coil, taller than wide; the honda sits on its lower left.
    lc, lrx, lrz, ly = (0.16, 0.06, 0.40), 0.36, 0.42, 0.06
    t0 = math.radians(200)
    honda = (lc[0] + lrx * math.cos(t0), ly, lc[2] + lrz * math.sin(t0))
    tan = (-math.sin(t0), 0.0, math.cos(t0))

    # Hand coil, upper left, in front of the loop's upper-left rim: five turns spread in depth and in size so each
    # turn shows, sagging into a teardrop below as when held at the top.
    cc, crx, crz = (-0.24, -0.12, 0.84), 0.21, 0.21
    y0, y1 = -0.22, -0.04
    turns = 5
    a_start = -math.pi / 2 - 0.5                       # lower left: the tail leaves here
    a_end = -math.pi / 2 + 0.5 + turns * 2 * math.pi   # lower right, five turns on: the lead leaves here
    n = 160
    coil = []
    for i in range(n + 1):
        f = i / n
        a = a_start + (a_end - a_start) * f
        size = 0.9 + 0.2 * (0.5 + 0.5 * math.sin(f * turns * 2 * math.pi * 0.43 + 0.6))
        sz = crz * size * (1.3 if math.sin(a) < 0 else 1.0)
        coil.append((cc[0] + crx * size * math.cos(a), y0 + (y1 - y0) * f, cc[2] + sz * math.sin(a)))

    # Free tail hanging down and out to the left from the start of the coil.
    s = coil[0]
    tail = [(s[0] - 0.03, s[1] - 0.01, s[2] - 0.07), (s[0] - 0.07, s[1] - 0.015, s[2] - 0.15),
            (s[0] - 0.08, s[1] - 0.02, s[2] - 0.24)]
    tail.reverse()

    # Lead: one smooth curve from the coil's lower right down into the honda, arriving along the loop's direction.
    e = coil[-1]
    lead = [(e[0] + 0.005, e[1] + 0.03, e[2] - 0.09),
            ((e[0] + honda[0]) / 2 - 0.01, (e[1] + ly) / 2 + 0.02, (e[2] + honda[2]) / 2 + 0.03),
            (honda[0] - 0.10 * tan[0], ly, honda[2] - 0.10 * tan[2]),
            honda]

    # The loop: from the honda once around, ending just short of it.
    loop = []
    m = 70
    for i in range(1, m + 1):
        t = t0 + math.radians(345) * i / m
        loop.append((lc[0] + lrx * math.cos(t), ly + 0.035 * math.sin(t - t0), lc[2] + lrz * math.sin(t)))

    k.tube(tail + coil + lead + loop, r, rope, curved=True)
    k.sphere(r * 1.15, at=tail[0], m=cream)  # whipped end of the free tail

    # Honda: a rope eye around the running rope, its axis along the loop.
    theta = math.degrees(math.atan2(tan[0], tan[2]))
    k.torus(0.042, 0.016, at=honda, rot=(0, theta, 0), m=cream)
    back = (honda[0] - 0.05 * tan[0], ly, honda[2] - 0.05 * tan[2])
    k.cyl(0.03, 0.045, at=back, rot=(0, theta, 0), m=cream, bevel=0.008)  # seizing where the loop end ties in

    # Red tie binding the coil turns on its left side.
    tx, tz, ty = cc[0] - crx * 1.05, cc[2], (y0 + y1) / 2
    k.box((0.075, (y1 - y0) + 0.08, 0.065), at=(tx, ty, tz), m=red, bevel=0.02)
    k.sphere(0.034, at=(tx - 0.05, y0 - 0.02, tz), m=red)
    k.box((0.018, 0.035, 0.11), at=(tx - 0.065, y0 - 0.03, tz - 0.07), rot=(0, -20, 0), m=red, bevel=0.008)
    k.box((0.018, 0.035, 0.09), at=(tx - 0.05, y0 - 0.01, tz - 0.065), rot=(0, 15, 0), m=red, bevel=0.008)

    k.turn(6, -8, -10)
