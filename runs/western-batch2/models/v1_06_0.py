# Lasso: one continuous rope. A free end hangs from the bottom of a hand coil of about four and a half turns;
# the top of the coil runs up as the standing part to the honda (the sliding knot's eye), and from there the rope
# opens into a wide loop that comes back round into the honda. A red cloth is wrapped and tied around the honda,
# its knot at the front and two pointed tails hanging down. Floating, front-on with a slight tilt, like the
# neckerchief, fan and anchor cards.
import math

SCENE = {"category": "1", "backdrop": "#3fcff2", "azimuth": 10, "elevation": 10, "lens": 70, "light": "left"}


def build(k):
    rope = k.mat("#d4a86a", "matte")
    cloth = k.mat("#e2262c", "matte")
    r = 0.024
    hx, hy, hz = 0.09, 0.0, 0.5  # honda / knot

    # Coil: stacked turns in the card plane, centered lower left, each turn a little different.
    cx, cz, rx, rz = -0.28, 0.38, 0.2, 0.27
    t_end = 8 * math.pi + 1.5 * math.pi
    n = 120
    coil = []
    for i in range(n + 1):
        t = t_end * i / n
        s = 1.0 - 0.035 * (t / (2 * math.pi)) + 0.02 * math.sin(3 * t)
        coil.append((cx + rx * s * math.cos(t), -0.07 + 0.14 * t / t_end, cz + rz * s * math.sin(t)))
    standing = [(hx, hy, hz), (0.03, -0.03, 0.45), (-0.04, -0.06, 0.40)]
    tail = [(-0.24, 0.08, 0.06), (-0.2, 0.06, -0.02), (-0.13, 0.04, -0.07), (-0.07, 0.03, -0.08)]
    k.tube(standing + coil[1:] + tail, r, rope, curved=True)

    # Wide open loop: an ellipse from the honda round and back into it, its top leaning back.
    lx, lz, lrx, lrz = 0.3, 0.68, 0.3, 0.26
    a0 = math.radians(225)
    loop = []
    for i in range(73):
        a = a0 + 2 * math.pi * i / 72
        z = lz + lrz * math.sin(a)
        loop.append((lx + lrx * math.cos(a), 0.4 * (z - hz), z))
    loop[0] = (hx, hy, hz)
    loop[-1] = (hx - 0.01, hy + 0.01, hz + 0.01)
    k.tube(loop, r, rope, curved=True)
    k.blob([(hx, hy, hz, 0.045), (hx - 0.03, hy, hz - 0.02, 0.04)], rope)  # the honda knot

    # Red cloth wrapped around the knot, tied at the front with two tails hanging down.
    k.cyl(0.062, 0.1, at=(hx - 0.01, hy, hz - 0.01), rot=(0, 55, 0), m=cloth, bevel=0.015)
    k.sphere(0.045, at=(hx - 0.01, hy - 0.065, hz - 0.01), scale=(1.1, 0.7, 0.9), m=cloth)
    for side in (-1, 1):
        balls = []
        for j in range(6):
            f = j / 5
            balls.append((hx - 0.01 + side * (0.02 + 0.06 * f), hy - 0.08 - 0.02 * f, hz - 0.05 - 0.2 * f,
                          0.042 * (1 - 0.75 * f), (1.0, 0.35, 1.3)))
        k.blob(balls, cloth)

    k.turn(6, 0, -12)
