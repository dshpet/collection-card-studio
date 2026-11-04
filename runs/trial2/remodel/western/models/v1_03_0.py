# Lasso: one rope. A free end with a cream whipping sticks out of the back of a hank of four stacked coils;
# a red tie wraps the bundle at the top of the coils. From the front coil the rope runs down to the honda (a small
# eye), and the big open noose loop runs out of the honda and back into it. Floats, tilted a little.
import math

SCENE = {"category": "1", "backdrop": "#8a4fd8", "azimuth": 18, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d6a656", "matte")
    cream = k.mat("#f4e6c4", "matte")
    red = k.mat("#d9302b", "matte")
    r = 0.03

    # Hank of coils: a helix about the y axis, back (+y) to front (-y), each turn slightly different in size.
    cx, cz = -0.22, 0.45
    turns = 4
    steps = 24
    t0 = math.radians(-60)
    coil = []
    for i in range(turns * steps + 1):
        f = i / steps
        t = t0 + 2 * math.pi * f
        a = 0.24 + 0.012 * math.sin(f * 2.3)
        b = 0.30 + 0.01 * math.cos(f * 1.7)
        y = 0.12 - 0.24 * f / turns
        coil.append((cx + a * math.cos(t), y, cz + b * math.sin(t)))

    # Free end: leaves the back coil and sticks out down-left, behind the hank.
    s = coil[0]
    tail = [(s[0] - 0.02, s[1] + 0.07, s[2] - 0.12), (s[0] - 0.08, s[1] + 0.09, s[2] - 0.2)]
    tail.reverse()

    # Stem: from the front coil down to the honda.
    e = coil[-1]
    hx, hy, hz = 0.12, -0.15, 0.0
    stem = [(e[0] + 0.07, e[1] - 0.02, e[2] - 0.1), (0.07, -0.14, 0.06), (hx - 0.02, hy, hz + 0.02)]
    k.tube(tail + coil + stem, r, rope, curved=True)

    # Whipped free end.
    te = tail[0]
    k.cyl(r * 1.15, 0.05, at=(te[0] + 0.01, te[1] - 0.003, te[2] + 0.02), rot=(-25, 22, 0), m=cream)

    # Honda: a small eye at the end of the stem; the noose threads it.
    k.torus(0.045, 0.02, at=(hx + 0.02, hy, hz - 0.01), rot=(0, 90, 0), m=rope)
    k.cyl(r * 1.2, 0.045, at=(hx - 0.04, hy + 0.003, hz + 0.035), rot=(0, 60, 0), m=cream)

    # Noose: a big open loop in a plane tilted back, starting and ending at the honda.
    rx, rz, tilt = 0.36, 0.28, math.radians(35)
    u = (1, 0, 0)
    w = (0, math.sin(tilt), math.cos(tilt))
    s0 = math.radians(160)
    c = (hx + 0.02 - rx * math.cos(s0), hy - rz * math.sin(s0) * w[1], hz - 0.01 - rz * math.sin(s0) * w[2])
    loop = []
    for j in range(49):
        a = s0 + 2 * math.pi * j / 48
        loop.append((c[0] + rx * math.cos(a) * u[0],
                     c[1] + rz * math.sin(a) * w[1],
                     c[2] + rz * math.sin(a) * w[2]))
    k.tube(loop, r, rope, curved=True)

    # Red tie around the bundle at the top of the coils: a band wrapped in the yz plane, a knot and two short ends.
    ty, tz = 0.0, cz + 0.30
    band = []
    for j in range(33):
        a = 2 * math.pi * j / 32
        band.append((cx, ty + 0.165 * math.cos(a), tz + 0.058 * math.sin(a)))
    k.tube(band, 0.018, red, curved=True)
    k.sphere(0.03, at=(cx, ty - 0.17, tz + 0.01), m=red)
    k.tube([(cx, ty - 0.18, tz), (cx - 0.04, ty - 0.2, tz - 0.06), (cx - 0.05, ty - 0.21, tz - 0.11)],
           0.015, red, curved=True)
    k.tube([(cx, ty - 0.18, tz), (cx + 0.04, ty - 0.2, tz - 0.05), (cx + 0.07, ty - 0.21, tz - 0.09)],
           0.015, red, curved=True)

    k.turn(6, -8, 12)
