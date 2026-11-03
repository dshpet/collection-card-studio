# Meteor: one lumpy rock made of merged balls, with five craters pressed into its front and sides (a dished
# hollow with a low raised rim). It flies toward the lower left, so a short flame tail grows from the rock's
# upper-right back and tapers away in three tongues. No floor; the whole thing floats, tilted a little.
import math

SCENE = {"category": "1", "backdrop": "#2cc6f0", "azimuth": 15, "elevation": 10, "lens": 70, "light": "left"}


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


CRATERS = [  # direction from the rock's center, angular radius (radians), depth
    (_norm((-0.25, -1.0, 0.3)), 0.36, 0.06),
    (_norm((0.45, -1.0, -0.25)), 0.26, 0.045),
    (_norm((-0.35, -0.8, -0.65)), 0.22, 0.04),
    (_norm((0.8, -0.5, 0.35)), 0.24, 0.04),
    (_norm((-0.9, -0.3, 0.1)), 0.2, 0.035),
]


def _crater(p):
    r = math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
    if r < 1e-6:
        return p
    u = (p[0] / r, p[1] / r, p[2] / r)
    dr = 0.0
    for c, w, d in CRATERS:
        ang = math.acos(max(-1.0, min(1.0, u[0] * c[0] + u[1] * c[1] + u[2] * c[2])))
        t = ang / w
        if t < 0.75:
            dr -= d * (1 - (t / 0.75) ** 2)
        elif t < 1.0:
            dr += d * 0.35 * math.sin(math.pi * (t - 0.75) / 0.25)
    s = (r + dr) / r
    return (p[0] * s, p[1] * s, p[2] * s)


def build(k):
    rock = k.mat("#7d6e62", "matte")
    body = k.blob([
        (0.0, 0.0, 0.0, 0.36),
        (0.14, -0.08, 0.12, 0.24),
        (-0.17, 0.04, -0.09, 0.25),
        (0.05, 0.14, -0.17, 0.22),
        (-0.11, -0.12, 0.15, 0.2),
        (0.17, 0.06, -0.12, 0.2),
    ], rock)
    k.warp(body, _crater)

    # Short flame tail behind the rock, up and to the right, opposite the direction of flight.
    flame = k.mat("#ff8a1f", "glow")
    core = k.mat("#ffc83a", "glow")
    tail = _norm((0.75, 0.35, 0.6))
    side = _norm((tail[2], 0.0, -tail[0]))
    for off, length in ((0.0, 1.0), (0.14, 0.75), (-0.14, 0.7)):
        balls = []
        for d, rad in ((0.28, 0.2), (0.44, 0.15), (0.57, 0.105), (0.68, 0.07), (0.77, 0.04)):
            d *= length if d > 0.3 else 1.0
            balls.append((tail[0] * d + side[0] * off, tail[1] * d + side[1] * off,
                          tail[2] * d + side[2] * off, rad * (1.0 if off == 0 else 0.8)))
        k.blob(balls, flame)
    k.blob([(tail[0] * d, tail[1] * d - 0.04, tail[2] * d, rad)
            for d, rad in ((0.3, 0.13), (0.42, 0.09), (0.52, 0.05))], core)

    k.turn(8, 0, -10)
