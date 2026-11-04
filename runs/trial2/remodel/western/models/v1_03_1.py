# Lasso: one rope. The free end, with a cream whipping, sticks out of the lower left of a hank of stacked
# coils. A red tie wraps the bundle at the top. From the lower right of the front coil the rope runs down
# through the honda (a small eye), sweeps around as a big open noose loop hanging in front of and below the
# hank, and ends at the honda eye. Floats, tilted a little.
import math

SCENE = {"category": "1", "backdrop": "#8a4fd8", "azimuth": 18, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d6a656", "matte")
    cream = k.mat("#f4e6c4", "matte")
    red = k.mat("#d9302b", "matte")
    r = 0.03

    # Hank of coils: a helix about the y axis, back (+y) to front (-y). Starts at the lower left (free end)
    # and ends at the lower right (to the honda).
    cx, cz = 0.0, 0.46
    t0, t1 = math.radians(200), math.radians(200 + 3 * 360 + 100)
    n = 84
    coil = []
    for i in range(n + 1):
        f = i / n
        t = t0 + (t1 - t0) * f
        a = 0.24 + 0.01 * math.sin(f * 7.0)
        b = 0.26 + 0.008 * math.cos(f * 5.0)
        coil.append((cx + a * math.cos(t), 0.1 - 0.2 * f, cz + b * math.sin(t)))

    # Free end: leaves the back coil and sticks outward, down-left, clear of the hank.
    s = coil[0]
    rad = (math.cos(t0), math.sin(t0))
    tail = []
    for d in (0.22, 0.15, 0.08):
        tail.append((s[0] + rad[0] * d - 0.03 * d, s[1] + 0.15 * d, s[2] + rad[1] * d - 0.6 * d))

    # Honda position, below the front coil's lower right end.
    e = coil[-1]
    hx, hy, hz = 0.17, -0.16, 0.11
    stem = [(e[0] + 0.04, e[1] - 0.03, e[2] - 0.07), (hx, hy, hz)]

    # Noose: a big open loop in a plane lying back, through the honda (at a = 60 deg) going around clockwise
    # and ending just short of the honda, where it is tied into the eye.
    rx, rz, tilt = 0.4, 0.34, math.radians(55)
    w = (0, math.sin(tilt), math.cos(tilt))
    s0 = math.radians(60)
    c = (hx - rx * math.cos(s0), hy - rz * math.sin(s0) * w[1], hz - rz * math.sin(s0) * w[2])
    loop = []
    steps = 44
    for j in range(1, steps + 1):
        a = s0 - math.radians(348) * j / steps
        loop.append((c[0] + rx * math.cos(a), c[1] + rz * math.sin(a) * w[1], c[2] + rz * math.sin(a) * w[2]))

    k.tube(tail + coil + stem + loop, r, rope, curved=True)

    # Whipping on the free end: a short cream sleeve over the last bit of rope.
    k.tube([tail[0], (tail[0][0] + (tail[1][0] - tail[0][0]) * 0.6, tail[0][1] + (tail[1][1] - tail[0][1]) * 0.6,
                      tail[0][2] + (tail[1][2] - tail[0][2]) * 0.6)], r * 1.18, cream)

    # Honda: the eye at the noose's end; the standing rope passes through its opening.
    k.torus(0.062, 0.022, at=(hx, hy, hz), rot=(0, 20, 0), m=rope)

    # Red tie around the bundle at the top of the coils: a band in the yz plane, a knot in front and two ends.
    ty, tz = 0.0, cz + 0.26
    band = []
    for j in range(33):
        a = 2 * math.pi * j / 32
        band.append((cx, ty + 0.145 * math.cos(a), tz + 0.055 * math.sin(a)))
    k.tube(band, 0.018, red, curved=True)
    k.sphere(0.03, at=(cx, ty - 0.15, tz + 0.01), m=red)
    k.tube([(cx, ty - 0.16, tz), (cx - 0.04, ty - 0.18, tz - 0.06), (cx - 0.05, ty - 0.19, tz - 0.11)],
           0.015, red, curved=True)
    k.tube([(cx, ty - 0.16, tz), (cx + 0.04, ty - 0.18, tz - 0.05), (cx + 0.07, ty - 0.19, tz - 0.09)],
           0.015, red, curved=True)

    k.turn(6, -6, 12)
