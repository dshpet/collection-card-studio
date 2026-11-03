# Star badge: a thick gold five-pointed star slab with a low faceted pyramid on its front, so each arm has a
# raised ridge; a gold ball sits on every tip, and a small red gem in a gold bezel crowns the center. The star
# floats front-on, turned and tipped a little to show its edge thickness.
import math

SCENE = {"category": "1", "backdrop": "#7a3fd1", "azimuth": 0, "elevation": 10, "lens": 70, "light": "left"}

OUTER, INNER = 0.5, 0.22


def star_point(k):
    # k counts 18-degree steps from the top tip; even steps are the tips and inner corners in turn,
    # odd steps lie halfway along the straight edge between them.
    def corner(j):
        a = math.radians(90 + j * 36)
        r = OUTER if j % 2 == 0 else INNER
        return r * math.cos(a), r * math.sin(a)
    if k % 2 == 0:
        return corner(k // 2)
    (x1, y1), (x2, y2) = corner(k // 2), corner(k // 2 + 1)
    return (x1 + x2) / 2, (y1 + y2) / 2


def starify(base_r):
    # Snaps each rim vertex of a 20-sided cylinder or cone onto the star outline, keeping its relative radius.
    def fn(p):
        x, y, z = p
        rho = math.hypot(x, y)
        if rho < 1e-6:
            return p
        k = int(round(math.degrees(math.atan2(y, x) - math.pi / 2) / 18)) % 20
        sx, sy = star_point(k)
        s = rho / base_r
        return sx * s, sy * s, z
    return fn


def build(k):
    gold = k.mat("#f5b81c", "metal")
    yellow = k.mat("#ffd84a", "metal")
    gem = k.mat("#e0182d", "gloss")
    cz = 0.6

    slab = k.cyl(1.0, 0.08, at=(0, 0, cz), rot=(90, 0, 0), m=gold, bevel=0.012, verts=20)
    k.warp(slab, starify(1.0))
    ridge = k.cone(0.94, 0.06, 0.07, at=(0, -0.075, cz), rot=(90, 0, 0), m=yellow, bevel=0.004, verts=20)
    k.warp(ridge, starify(1.0))

    for j in range(5):
        a = math.radians(90 + j * 72)
        k.sphere(0.065, at=(0.535 * math.cos(a), -0.01, cz + 0.535 * math.sin(a)), m=gold)

    k.torus(0.062, 0.018, at=(0, -0.108, cz), rot=(90, 0, 0), m=gold)
    k.sphere(0.055, at=(0, -0.115, cz), scale=(1, 0.55, 1), m=gem)

    k.turn(8, 10, -18)
