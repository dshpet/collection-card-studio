# Police badge wallet: an open black leather wallet lies flat on a honey wooden desk, its two flaps joined by a
# rounded spine fold. The left flap carries a large gold police shield (peaked top, straight sides, pointed bottom)
# with a raised rim, an eagle with spread wings sitting on its top edge, a blue enamel disc holding a gold
# five-pointed star, and a blank gold banner across the lower face. The right flap holds an ID card with a blue
# top band and a grey photo square. Seen from high above.
import math

SCENE = {"category": "3", "backdrop": "#3fd0e8", "azimuth": 18, "elevation": 64, "lens": 62, "light": "left"}

# Convex shield outline, counterclockwise from angle ~0 (matches cylinder vertex order).
SHIELD = [(0.17, -0.02), (0.17, 0.12), (0.08, 0.15), (-0.08, 0.15), (-0.17, 0.12),
          (-0.17, -0.02), (-0.1, -0.14), (0.0, -0.21), (0.1, -0.14)]


def polygon(targets):
    # Snap the n rim vertices of an n-sided cylinder onto the given convex (x, y) corner points.
    n = len(targets)

    def fn(p):
        x, y, z = p
        if math.hypot(x, y) < 1e-6:
            return p
        i = int(round(math.atan2(y, x) / (2 * math.pi / n))) % n
        return (targets[i][0], targets[i][1], z)
    return fn


def build(k):
    leather = k.mat("#0d0d0f", "matte")
    leather_in = k.mat("#17171a", "matte")
    gold = k.mat("#e8b631", "metal")
    gold_dark = k.mat("#c99320", "metal")
    enamel = k.mat("#1f5fd6", "gloss")
    white = k.mat("#f7f7f2", "satin")
    band = k.mat("#2a6fe0", "satin")
    grey = k.mat("#6f757e", "matte")

    # Wallet: two flaps and the spine fold between them.
    fw, fd, ft = 0.5, 0.68, 0.03
    for side in (-1, 1):
        k.box((fw, fd, ft), at=(side * (fw / 2 + 0.012), 0, ft / 2), m=leather, bevel=0.018)
        k.box((fw - 0.05, fd - 0.05, 0.006), at=(side * (fw / 2 + 0.012), 0, ft + 0.001), m=leather_in,
              bevel=0.004)
    k.cyl(0.022, fd - 0.004, at=(0, 0, 0.022), rot=(90, 0, 0), m=leather, bevel=0.006)

    # Shield badge on the left flap: dark gold rim plate, bright gold face on it.
    bx, by, zb = -(fw / 2 + 0.012), -0.03, ft + 0.004
    rim = k.cyl(1.0, 0.018, at=(bx, by, zb + 0.009), m=gold_dark, bevel=0, verts=len(SHIELD))
    k.warp(rim, polygon(SHIELD))
    face = k.cyl(1.0, 0.012, at=(bx, by + 0.004, zb + 0.022), m=gold, bevel=0, verts=len(SHIELD))
    k.warp(face, polygon([(x * 0.86, y * 0.86) for x, y in SHIELD]))
    zt = zb + 0.028

    # Blue enamel disc in a gold ring.
    ex, ey = bx, by + 0.025
    k.cyl(0.085, 0.01, at=(ex, ey, zt + 0.002), m=gold_dark, bevel=0.003)
    k.cyl(0.072, 0.012, at=(ex, ey, zt + 0.005), m=enamel, bevel=0.003)

    # Gold five-pointed star: a pentagon core and five triangular points, all convex.
    ro, rin = 0.058, 0.024
    sz = zt + 0.013
    core = k.cyl(1.0, 0.01, at=(ex, ey, sz), m=gold, bevel=0, verts=5)
    k.warp(core, polygon([(rin * math.cos(math.radians(126 + 72 * j)), rin * math.sin(math.radians(126 + 72 * j)))
                          for j in range(5)]))
    for i in range(5):
        a = math.radians(90 + 72 * i)
        tip = (ro * math.cos(a), ro * math.sin(a))
        b1 = (rin * math.cos(a - math.radians(36)), rin * math.sin(a - math.radians(36)))
        b2 = (rin * math.cos(a + math.radians(36)), rin * math.sin(a + math.radians(36)))
        pt = k.cyl(1.0, 0.01, at=(ex, ey, sz), m=gold, bevel=0, verts=3)
        k.warp(pt, polygon([b1, tip, b2]))

    # Blank banner lying on the lower face, inside the outline.
    k.box((0.2, 0.045, 0.012), at=(bx, by - 0.095, zt + 0.003), m=gold, bevel=0.005)
    k.box((0.21, 0.012, 0.008), at=(bx, by - 0.12, zt + 0.001), m=gold_dark, bevel=0.003)

    # Eagle with spread wings sitting on the shield's top edge, overlapping it.
    ey0, ez = by + 0.16, zt + 0.004
    balls = [(bx, ey0, ez, 0.032, (1, 1.15, 0.55)),                 # body
             (bx, ey0 + 0.045, ez + 0.006, 0.02, (1, 1, 0.65)),     # head
             (bx, ey0 + 0.068, ez + 0.004, 0.009, (1, 1.2, 0.6)),   # beak
             (bx, ey0 - 0.04, ez, 0.018, (1.4, 1, 0.5))]            # tail on the shield
    for side in (-1, 1):
        for j in range(9):
            t = j / 8
            balls.append((bx + side * (0.03 + 0.13 * t), ey0 + 0.01 + 0.06 * t ** 1.3, ez + 0.002,
                          0.03 - 0.012 * t, (1, 1.25, 0.45)))
    k.blob(balls, gold)

    # ID card on the right flap.
    cx, cz = fw / 2 + 0.012, ft + 0.006
    k.box((0.38, 0.5, 0.008), at=(cx, 0, cz), m=white, bevel=0.003)
    k.box((0.38, 0.1, 0.01), at=(cx, 0.2, cz + 0.001), m=band, bevel=0.003)
    k.box((0.11, 0.135, 0.01), at=(cx - 0.1, 0.05, cz + 0.001), m=grey, bevel=0.003)

    # Light honey wooden desk: planks with thin seams, top at z = 0.
    shades = ["#e3ac62", "#d99f55", "#e8b56d", "#dca45a"]
    for i in range(-8, 9):
        k.box((8, 0.34, 0.1), at=(0, i * 0.35, -0.05), m=k.mat(shades[i % 4], "matte"), bevel=0.012, setting=True)
    k.box((10, 10, 0.1), at=(0, 0, -0.08), m=k.mat("#b77f3c", "matte"), bevel=0, setting=True)
    k.turn(0, 0, -12)
