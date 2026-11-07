# Coiled leather belt with an oval silver buckle, lying on wooden planks, seen from high above.
# The strap stands on its edge in a flat spiral; at the outer end it leaves the coil, twists down to lie flat
# on the planks and runs under the buckle, which rests face-up on the strap end and on a hook at its far end.
# The buckle plate has a raised rim and a raised house pictogram: walls, a solid pitched-roof gable, a chimney
# rising from the right slope and a cut door. The pictogram is turned to stand upright for the camera.
import math

SCENE = {"category": "3", "backdrop": "#5cbf3a", "azimuth": 25, "elevation": 62, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#5a2e14", "matte")
    silver = k.mat("#cfd4db", "metal")
    dark = k.mat("#7d838c", "metal")
    w, th = 0.09, 0.02  # strap width (vertical in the coil) and thickness

    def seg(p0, p1, roll, z):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        length = math.hypot(dx, dy) + 0.003
        yaw = math.degrees(math.atan2(dy, dx))
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, z)
        k.box((length, w, th), at=mid, rot=(roll, 0, yaw), m=leather, bevel=0)

    # Spiral coil, strap on edge, ending at the front (-y) heading +x.
    cx, cy = -0.2, 0.04
    r0, pitch, turns = 0.07, 0.027, 5.5
    t_end = -math.pi / 2 + 2 * math.pi * 6
    t_start = t_end - 2 * math.pi * turns
    steps = int(turns * 110)
    pts = []
    for i in range(steps + 1):
        t = t_start + (t_end - t_start) * i / steps
        r = r0 + pitch * (t - t_start) / (2 * math.pi)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    for a, b in zip(pts, pts[1:]):
        seg(a, b, 90, w / 2)

    # Tail twists from on-edge to flat, its lowest edge always on the planks.
    ex, ey = pts[-1]
    n, run = 48, 0.16
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

    # Embossed house, built in local plate coordinates (+y = house up), turned so its up points away from camera.
    top = pz + 0.0125
    turn = 25.0
    ca, sa = math.cos(math.radians(turn)), math.sin(math.radians(turn))

    def hb(size, lx, ly, z, m, bevel=0.003):
        x = bx + lx * ca - ly * sa
        y = by + lx * sa + ly * ca
        return k.box(size, at=(x, y, z), rot=(0, 0, turn), m=m, bevel=bevel)

    wall_h = 0.075
    wall_c = -0.035
    eave_y = wall_c + wall_h / 2
    ridge_rise, half = 0.055, 0.078
    hb((0.11, wall_h, 0.012), 0, wall_c, top + 0.006, silver)  # walls
    # chimney on the right slope, its foot hidden under the roof
    hb((0.02, 0.042, 0.012), 0.04, eave_y + 0.036, top + 0.006, silver)
    # roof: one solid triangular gable, the box's top corners pulled together to the ridge
    roof = hb((2 * half, ridge_rise, 0.016), 0, eave_y + ridge_rise / 2, top + 0.008, silver, bevel=0)
    k.warp(roof, lambda p: (0.0 if p[1] > 0 else p[0], p[1], p[2]))
    hb((0.026, 0.045, 0.004), 0, wall_c - 0.015, top + 0.0125, dark)  # cut door

    # Wooden planks running away from the camera, filling the card, with dark wood in the gaps.
    for i in range(-8, 9):
        tone = ("#c98a4b", "#d39552", "#bd7f42")[i % 3]
        k.box((0.29, 8, 0.06), at=(i * 0.3, 0, -0.03), m=k.mat(tone, "matte"), bevel=0.012, setting=True)
    k.floor("#5a3418", "matte", size=40, z=-0.055)
