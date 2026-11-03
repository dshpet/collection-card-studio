# Meteor: one lumpy rock made of merged balls, with stretched lobes that break its outline and four craters of
# clearly different sizes scattered off-center over its front and side (a dished hollow with a low raised rim).
# It flies toward the lower left, so a short flame tail grows from the rock's upper-right back and tapers away
# in three separate tongues, each a dense run of overlapping balls shrinking smoothly to a point. No floor; the
# whole thing floats, tilted a little.
import math

SCENE = {"category": "1", "backdrop": "#2cc6f0", "azimuth": 15, "elevation": 10, "lens": 70, "light": "left"}


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


CRATERS = [  # direction from the rock's center, angular radius (radians), depth
    (_norm((-0.5, -1.0, 0.5)), 0.38, 0.065),
    (_norm((0.4, -1.0, -0.05)), 0.15, 0.035),
    (_norm((0.25, -0.8, -0.75)), 0.24, 0.045),
    (_norm((0.95, -0.35, 0.3)), 0.2, 0.04),
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


def _tongue(tail, side, off, length, width, bend):
    # A dense run of overlapping balls from the rock's back, shrinking smoothly to a point, curving a little.
    balls = []
    n = 12
    for i in range(n):
        t = i / (n - 1)
        d = 0.26 + 0.5 * length * t
        spread = off * (0.4 + d) + bend * t * t
        rad = width * (0.17 * (1 - t) ** 1.2 + 0.012)
        balls.append((tail[0] * d + side[0] * spread, tail[1] * d + side[1] * spread,
                      tail[2] * d + side[2] * spread, rad))
    return balls


def build(k):
    rock = k.mat("#5f564f", "matte")
    body = k.blob([
        (0.0, 0.0, 0.0, 0.32, (1.08, 1.0, 0.92)),
        (0.2, -0.04, 0.16, 0.2, (1.2, 1.0, 0.8)),
        (-0.24, 0.02, -0.08, 0.2, (1.0, 1.0, 1.25)),
        (0.08, 0.1, -0.24, 0.19, (1.3, 1.0, 0.75)),
        (-0.14, -0.06, 0.22, 0.17, (1.25, 1.0, 0.85)),
        (0.27, 0.04, -0.1, 0.16),
        (-0.06, -0.14, -0.2, 0.14),
    ], rock)
    k.warp(body, _crater)

    # Short flame tail behind the rock, up and to the right, opposite the direction of flight.
    flame = k.mat("#ff4d00", "glow")
    core = k.mat("#ff7a00", "glow")
    tail = _norm((0.75, 0.35, 0.6))
    side = _norm((tail[2], 0.0, -tail[0]))
    for off, length, width, bend in ((0.0, 1.0, 1.0, 0.04), (0.2, 0.75, 0.78, -0.05), (-0.2, 0.65, 0.72, 0.05)):
        k.blob(_tongue(tail, side, off, length, width, bend), flame)
    k.blob([(tail[0] * d, tail[1] * d - 0.02, tail[2] * d, rad) for d, rad in
            ((0.28, 0.1), (0.34, 0.085), (0.4, 0.065), (0.46, 0.045))], core)

    k.turn(8, 0, -10)
