# Police badge wallet: an open black leather wallet lies flat on a honey wooden desk, its two flaps joined by a
# rounded spine fold. The left flap carries a gold shield badge (raised rim, eagle with spread wings on top, blue
# enamel disc holding a gold five-pointed star, a blank gold banner across the lower part). The right flap holds
# an ID card with a blue top band and a grey photo square. Seen from high above, like the map and book cards.
import math

SCENE = {"category": "3", "backdrop": "#3fd0e8", "azimuth": 18, "elevation": 64, "lens": 60, "light": "left"}


def shield(r):
    # Turn a flat round disc into a shield outline: flat-ish top, pointed bottom.
    def fn(p):
        x, y, z = p
        if math.hypot(x, y) < 1e-6:
            return p
        if y < 0:
            t = min(1.0, -y / r)
            return (x * (1 - 0.75 * t ** 1.6), y * 1.3, z)
        return (x, y * 0.8, z)
    return fn


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
    leather = k.mat("#1c1c1f", "matte")
    leather_in = k.mat("#2a2a2e", "matte")
    gold = k.mat("#e8b631", "metal")
    gold_dark = k.mat("#c99320", "metal")
    enamel = k.mat("#1f5fd6", "gloss")
    white = k.mat("#f7f7f2", "satin")
    band = k.mat("#2a6fe0", "satin")
    grey = k.mat("#6f757e", "matte")

    # Wallet: two flaps and the spine fold between them.
    fw, fd, ft = 0.5, 0.68, 0.03
    for side in (-1, 1):
        k.box((fw, fd, ft), at=(side * (fw / 2 + 0.012), 0, ft / 2), rot=(0, 0, 0), m=leather, bevel=0.018)
        k.box((fw - 0.05, fd - 0.05, 0.006), at=(side * (fw / 2 + 0.012), 0, ft + 0.001), rot=(0, 0, 0),
              m=leather_in, bevel=0.004)
    k.cyl(0.022, fd - 0.004, at=(0, 0, 0.022), rot=(90, 0, 0), m=leather, bevel=0.006)

    # Badge on the left flap.
    bx, by, zb = -(fw / 2 + 0.012), -0.04, ft + 0.004
    r = 0.15
    base = k.lathe([(0, 0), (r, 0), (r, 0.018), (0, 0.018)], at=(bx, by, zb), rot=(0, 0, 0), m=gold_dark, verts=96)
    k.warp(base, shield(r))
    ri = r - 0.018
    face = k.lathe([(0, 0), (ri, 0), (ri, 0.012), (0, 0.012)], at=(bx, by + 0.002, zb + 0.016), rot=(0, 0, 0),
                   m=gold, verts=96)
    k.warp(face, shield(ri))
    zt = zb + 0.028
    k.cyl(0.072, 0.01, at=(bx, by + 0.02, zt), rot=(0, 0, 0), m=gold_dark, bevel=0.003)
    k.cyl(0.06, 0.012, at=(bx, by + 0.02, zt + 0.003), rot=(0, 0, 0), m=enamel, bevel=0.003)

    # Gold five-pointed star on the enamel: a pentagon core and five triangular points, all convex.
    ro, rin = 0.048, 0.02
    sx, sy, sz = bx, by + 0.02, zt + 0.011
    core = k.cyl(1.0, 0.01, at=(sx, sy, sz), rot=(0, 0, 0), m=gold, bevel=0, verts=5)
    k.warp(core, polygon([(rin * math.cos(math.radians(126 + 72 * j)), rin * math.sin(math.radians(126 + 72 * j)))
                          for j in range(5)]))
    for i in range(5):
        a = math.radians(90 + 72 * i)
        tip = (ro * math.cos(a), ro * math.sin(a))
        b1 = (rin * math.cos(a - math.radians(36)), rin * math.sin(a - math.radians(36)))
        b2 = (rin * math.cos(a + math.radians(36)), rin * math.sin(a + math.radians(36)))
        pt = k.cyl(1.0, 0.01, at=(sx, sy, sz), rot=(0, 0, 0), m=gold, bevel=0, verts=3)
        k.warp(pt, polygon([tip, b2, b1]) if False else polygon([b1, tip, b2]))

    # Blank banner across the lower part, with folded tails.
    k.box((0.2, 0.042, 0.012), at=(bx, by - 0.085, zt + 0.002), rot=(0, 0, 0), m=gold, bevel=0.004)
    for side in (-1, 1):
        k.box((0.04, 0.034, 0.01), at=(bx + side * 0.115, by - 0.092, zt - 0.002), rot=(0, 0, side * 12),
              m=gold_dark, bevel=0.003)
    # Eagle spreading its wings on top of the shield.
    ey, ez = by + 0.135, zb + 0.02
    balls = [(bx, ey, ez, 0.03, (1, 1.1, 0.5)),                  # body
             (bx, ey + 0.045, ez + 0.004, 0.018, (1, 1, 0.6)),   # head
             (bx, ey + 0.068, ez + 0.002, 0.008, (1, 1.2, 0.6))]  # beak
    for side in (-1, 1):
        for dx, dy, rr in [(0.04, 0.01, 0.024), (0.07, 0.03, 0.022), (0.1, 0.048, 0.019), (0.126, 0.062, 0.015)]:
            balls.append((bx + side * dx, ey + dy, ez, rr, (1.1, 1, 0.45)))
    k.blob(balls, gold)

    # ID card on the right flap.
    cx, cz = fw / 2 + 0.012, ft + 0.006
    k.box((0.38, 0.5, 0.008), at=(cx, 0, cz), rot=(0, 0, 0), m=white, bevel=0.003)
    k.box((0.38, 0.1, 0.01), at=(cx, 0.2, cz + 0.001), rot=(0, 0, 0), m=band, bevel=0.003)
    k.box((0.11, 0.135, 0.01), at=(cx - 0.1, 0.05, cz + 0.001), rot=(0, 0, 0), m=grey, bevel=0.003)

    # Light honey wooden desk: planks with thin seams, top at z = 0.
    shades = ["#e3ac62", "#d99f55", "#e8b56d", "#dca45a"]
    for i in range(-8, 9):
        k.box((8, 0.34, 0.1), at=(0, i * 0.35, -0.05), rot=(0, 0, 0), m=k.mat(shades[i % 4], "matte"),
              bevel=0.012, setting=True)
    k.box((10, 10, 0.1), at=(0, 0, -0.08), rot=(0, 0, 0), m=k.mat("#b77f3c", "matte"), bevel=0, setting=True)
    k.turn(0, 0, -12)
