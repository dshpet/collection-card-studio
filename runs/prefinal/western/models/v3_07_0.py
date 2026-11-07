# Coiled leather belt with an oval silver buckle, lying on wooden planks, seen from high above.
# The strap stands on its edge in a flat spiral; at the outer end it leaves the coil, twists down to lie flat
# on the planks and runs under the buckle, which rests face-up on the strap end and on a hook at its far end.
# The buckle plate has a raised rim and a raised house pictogram: walls, a pitched roof, a chimney and a cut door.
import math

SCENE = {"category": "3", "backdrop": "#5cbf3a", "azimuth": 25, "elevation": 62, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4a22", "matte")
    silver = k.mat("#cfd4db", "metal")
    dark = k.mat("#7d838c", "metal")
    w, th = 0.09, 0.02  # strap width (vertical in the coil) and thickness

    def seg(p0, p1, roll, z):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        length = math.hypot(dx, dy) + 0.006
        yaw = math.degrees(math.atan2(dy, dx))
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, z)
        k.box((length, w, th), at=mid, rot=(roll, 0, yaw), m=leather, bevel=0.004)

    # Spiral coil, strap on edge, ending at the front (-y) heading +x.
    cx, cy = -0.2, 0.04
    r0, pitch, turns = 0.07, 0.027, 5.5
    t_end = -math.pi / 2 + 2 * math.pi * 6
    t_start = t_end - 2 * math.pi * turns
    steps = int(turns * 30)
    pts = []
    for i in range(steps + 1):
        t = t_start + (t_end - t_start) * i / steps
        r = r0 + pitch * (t - t_start) / (2 * math.pi)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    for a, b in zip(pts, pts[1:]):
        seg(a, b, 90, w / 2)

    # Tail twists from on-edge to flat, its lowest edge always on the planks.
    ex, ey = pts[-1]
    n, run = 10, 0.16
    for i in range(n):
        roll = 90 * (1 - (i + 0.5) / n)
        z = w / 2 * math.sin(math.radians(roll)) + th / 2 * math.cos(math.radians(roll))
        seg((ex + run * i / n, ey), (ex + run * (i + 1) / n, ey), roll, z)
    bx, by = ex + run + 0.21, ey
    seg((ex + run, ey), (bx - 0.06, ey), 0, th / 2)  # flat end runs under the buckle's left half

    # Buckle: oval plate on the strap end, hook under its right end down to the planks.
    oval = lambda p: (p[0] * 1.36, p[1], p[2])
    pz = th + 0.0125
    k.warp(k.cyl(0.125, 0.025, at=(bx, by, pz), m=silver, bevel=0.006), oval)
    k.warp(k.torus(0.114, 0.011, at=(bx, by, pz + 0.0125), m=silver), oval)
    k.cyl(0.012, th, at=(bx + 0.13, by, th / 2), m=dark)

    # Embossed house, upright toward +y so it reads from the camera.
    top = pz + 0.0125
    hy = by - 0.03
    k.box((0.11, 0.075, 0.012), at=(bx, hy, top + 0.006), m=silver, bevel=0.003)
    ridge_y = hy + 0.0375 + 0.05
    for side in (-1, 1):
        k.box((0.105, 0.024, 0.014), at=(bx + side * 0.04, ridge_y - 0.028, top + 0.007),
              rot=(0, 0, -side * 35), m=silver, bevel=0.003)
    k.box((0.02, 0.04, 0.014), at=(bx + 0.035, ridge_y - 0.005, top + 0.007), m=silver, bevel=0.003)
    k.box((0.026, 0.045, 0.004), at=(bx, hy - 0.015, top + 0.0105), m=dark, bevel=0.002)  # cut door

    # Wooden planks running away from the camera, filling the card.
    for i in range(-8, 9):
        tone = ("#c98a4b", "#d39552", "#bd7f42")[i % 3]
        k.box((0.29, 8, 0.06), at=(i * 0.3, 0, -0.03), m=k.mat(tone, "matte"), bevel=0.012, setting=True)
