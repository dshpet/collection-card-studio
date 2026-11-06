# Lasso: one continuous rope. A free end hangs from the bottom of a hand coil of about four and a half turns,
# the turns fanned so each strand shows; the top of the coil runs up as the standing part to the honda (the sliding
# knot's eye), and from there the rope opens into a wide oval loop that comes back round into the honda. A red cloth
# is wrapped and tied around the honda, its knot at the front and two flat pointed tails hanging down and apart.
# Floating, front-on with a slight tilt.
import math

SCENE = {"category": "1", "backdrop": "#3fcff2", "azimuth": 10, "elevation": 10, "lens": 70, "light": "left"}


def build(k):
    rope = k.mat("#d4a86a", "matte")
    cloth = k.mat("#e2262c", "matte")
    r = 0.024
    hx, hy, hz = 0.09, 0.0, 0.5  # honda / knot

    # Coil: turns fanned sideways and down, each a different size, so separate strands read.
    cx, cz, rx, rz = -0.3, 0.38, 0.24, 0.3
    t_end = 8 * math.pi + 1.5 * math.pi
    n = 160
    coil = []
    for i in range(n + 1):
        t = t_end * i / n
        turn = t / (2 * math.pi)
        s = 1.0 - 0.04 * turn + 0.025 * math.sin(3 * t)
        ox = 0.022 * turn
        oz = -0.018 * turn
        coil.append((cx + ox + rx * s * math.cos(t), -0.06 + 0.12 * t / t_end, cz + oz + rz * s * math.sin(t)))
    standing = [(hx, hy, hz), (0.03, -0.03, 0.45), (-0.04, -0.06, 0.40)]
    tail = [(-0.22, 0.07, -0.02), (-0.17, 0.06, -0.1), (-0.1, 0.05, -0.15), (-0.03, 0.04, -0.16)]
    k.tube(standing + coil[1:] + tail, r, rope, curved=True)

    # Wide open loop: an oval from the honda round and back into it, its top leaning well back.
    lx, lz, lrx, lrz = 0.33, 0.7, 0.32, 0.27
    a0 = math.radians(225)
    loop = []
    for i in range(73):
        a = a0 + 2 * math.pi * i / 72
        z = lz + lrz * math.sin(a)
        loop.append((lx + lrx * math.cos(a), 0.9 * (z - hz), z))
    loop[0] = (hx, hy, hz)
    loop[-1] = (hx - 0.01, hy + 0.01, hz + 0.01)
    k.tube(loop, r, rope, curved=True)
    k.blob([(hx, hy, hz, 0.045), (hx - 0.03, hy, hz - 0.02, 0.04)], rope)  # the honda knot

    # Red cloth bound around the knot as one soft wrap, tied at the front.
    k.blob([(hx - 0.04, hy, hz - 0.03, 0.06, (1.0, 1.0, 1.0)),
            (hx + 0.02, hy, hz + 0.01, 0.06, (1.0, 1.0, 1.0)),
            (hx - 0.01, hy - 0.06, hz - 0.01, 0.045, (1.1, 0.7, 0.9))], cloth)
    # Two flat, pointed tails hanging from the knot and spreading apart, one longer.
    for side, length in ((-1, 0.2), (1, 0.15)):
        balls = []
        for j in range(10):
            f = j / 9
            balls.append((hx - 0.01 + side * (0.025 + 0.09 * f), hy - 0.075 - 0.01 * f, hz - 0.05 - length * f,
                          0.042 * (1 - 0.7 * f), (1.5, 0.3, 1.1)))
        k.blob(balls, cloth)

    k.turn(6, 0, -8)
