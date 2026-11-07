# Treasure chest on sand: a wooden box with gold corner posts, top and base rims, and a gold lock plate on the
# front; red lining covers the inner walls. The rounded (D-section) lid turns on two gold hinges on the back top
# edge and stands open about 105 degrees, its underside lined red, gold bands round both ends and along the front
# edge, with the hasp that meets the lock. A domed heap of gold coins fills the box above the rim. The sand is a
# slab under it.
import math

SCENE = {"category": "3", "backdrop": "#3ea6ec", "azimuth": 24, "elevation": 14, "lens": 60, "light": "left"}

W, D, H = 0.9, 0.55, 0.45      # body width (x), depth (y), height (z)
R = 0.28                        # lid radius (half depth plus a little overhang)
LW = 0.92                       # lid width
OPEN = math.radians(105)        # how far the lid is swung back


def lid_pose(p):
    """Closed-lid world point -> open-lid world point, turning on the back hinge line (y=R, z=H)."""
    x, y, z = p
    dy, dz = y - R, z - H
    c, s = math.cos(OPEN), math.sin(OPEN)
    return (x, R + dy * c + dz * s, H - dy * s + dz * c)


def build(k):
    wood = k.mat("#8a4f2a", "matte")
    wood_dark = k.mat("#6e3d20", "matte")
    gold = k.mat("#f2b824", "metal")
    red = k.mat("#c4222c", "matte")
    coin = k.mat("#ffc933", "metal")
    hole = k.mat("#3a2210", "matte")

    # ---- body: floor and four walls, wood
    t = 0.05
    k.box((W, D, t), at=(0, 0, t / 2), m=wood)
    k.box((W, t, H), at=(0, -D / 2 + t / 2, H / 2), m=wood)
    k.box((W, t, H), at=(0, D / 2 - t / 2, H / 2), m=wood)
    for sx in (-1, 1):
        k.box((t, D, H), at=(sx * (W / 2 - t / 2), 0, H / 2), m=wood)

    # red lining on the inner wall faces
    lt, lh = 0.014, H - t
    k.box((W - 2 * t, lt, lh), at=(0, -D / 2 + t + lt / 2, t + lh / 2), m=red, bevel=0.004)
    k.box((W - 2 * t, lt, lh), at=(0, D / 2 - t - lt / 2, t + lh / 2), m=red, bevel=0.004)
    for sx in (-1, 1):
        k.box((lt, D - 2 * t, lh), at=(sx * (W / 2 - t - lt / 2), 0, t + lh / 2), m=red, bevel=0.004)

    # gold metalwork on the body: corner posts, top rim, base rim
    g, gt = 0.07, 0.022
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.box((g, g, H + 0.01), at=(sx * (W / 2 - g / 2 + 0.008), sy * (D / 2 - g / 2 + 0.008), H / 2),
                  m=gold, bevel=0.01)
    for z, hgt in ((H - 0.03, 0.06), (0.03, 0.06)):
        for sy in (-1, 1):
            k.box((W - 0.06, gt, hgt), at=(0, sy * (D / 2 + gt / 2 - 0.004), z), m=gold, bevel=0.006)
        for sx in (-1, 1):
            k.box((gt, D - 0.06, hgt), at=(sx * (W / 2 + gt / 2 - 0.004), 0, z), m=gold, bevel=0.006)

    # lock plate on the front, with a cut keyhole
    k.box((0.15, 0.03, 0.17), at=(0, -D / 2 - 0.02, H - 0.13), m=gold, bevel=0.015)
    k.cyl(0.018, 0.012, at=(0, -D / 2 - 0.033, H - 0.11), rot=(90, 0, 0), m=hole)
    k.box((0.016, 0.012, 0.05), at=(0, -D / 2 - 0.033, H - 0.14), m=hole, bevel=0.003)

    # back hinges: knuckles on the hinge line, leaves on the back wall
    for sx in (-1, 1):
        k.cyl(0.026, 0.11, at=(sx * 0.27, R + 0.005, H), rot=(0, 90, 0), m=gold)
        k.box((0.1, 0.016, 0.09), at=(sx * 0.27, D / 2 + 0.012, H - 0.05), m=gold, bevel=0.004)

    # ---- lid: a solid D-section, built closed in world coordinates and swung open on the hinge line
    def lid_lathe(radius, x0, width, m):
        part = k.lathe([(0, 0), (radius, 0), (radius, width), (0, width)], at=(0, 0, 0), rot=(0, 0, 0), m=m,
                       verts=96)

        def fn(p):
            lx, ly, lz = p
            return lid_pose((x0 + lz, lx, H + max(ly, 0.0)))
        k.warp(part, fn)
        return part

    def lid_box(size, center, m, bevel=0.006):
        part = k.box(size, at=(0, 0, 0), m=m, bevel=bevel)
        k.warp(part, lambda p: lid_pose((center[0] + p[0], center[1] + p[1], center[2] + p[2])))
        return part

    lid_lathe(R, -LW / 2, LW, wood_dark)
    # gold bands round the two ends of the lid
    for x0 in (-LW / 2 - 0.004, LW / 2 - 0.066):
        lid_lathe(R + 0.016, x0, 0.07, gold)
    # gold band along the lid's front edge, and the hasp that drops onto the lock plate
    lid_box((LW + 0.008, 0.026, 0.06), (0, -R - 0.006, H + 0.03), gold)
    lid_box((0.1, 0.024, 0.11), (0, -R - 0.016, H + 0.04), gold, bevel=0.012)
    # red lining on the flat underside
    lid_box((LW - 0.1, 2 * R - 0.08, 0.012), (0, 0, H - 0.004), red, bevel=0.003)

    # ---- heap of gold coins filling the box
    z0, a, b, c = 0.33, 0.40, 0.23, 0.2
    k.blob([(0, 0, z0, 0.1, (a / 0.1, b / 0.1, c / 0.1))], coin)

    def heap(x, y):
        gg = max(1 - (x / a) ** 2 - (y / b) ** 2, 0.02)
        s = math.sqrt(gg)
        return z0 + c * s, -c * x / (a * a * s), -c * y / (b * b * s)

    n = 0
    for i in range(7):
        for j in range(5):
            x = -0.3 + i * 0.1 + 0.03 * math.sin(i * 3.1 + j * 1.7)
            y = -0.16 + j * 0.08 + 0.025 * math.cos(i * 2.3 + j * 2.9)
            if (x / 0.36) ** 2 + (y / 0.2) ** 2 > 1:
                continue
            z, fx, fy = heap(x, y)
            jx = 14 * math.sin(n * 2.7)
            jy = 14 * math.cos(n * 1.9)
            k.cyl(0.045, 0.014, at=(x, y, z + 0.004),
                  rot=(math.degrees(math.atan(fy)) + jx, -math.degrees(math.atan(fx)) + jy, 0), m=coin,
                  bevel=0.004)
            n += 1

    # ---- sand slab under the chest
    k.box((6, 3.2, 0.3), at=(0, 0.7, -0.15), m=k.mat("#ecc98a", "matte"), bevel=0.04, setting=True)
