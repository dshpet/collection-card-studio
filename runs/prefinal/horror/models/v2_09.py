# Cobweb window: a tall arched wooden window set into a thick grey stone house wall, near the house corner. The
# frame (two side posts and an arch made of short pieces) lines the opening and stands slightly out from the wall; a
# stone sill sits under it. One upright bar and two crossbars divide the glass. Behind the panes is a dark room with
# an inner shelf, on which a candle in a dish has a small glowing flame. A white cobweb spans the top-right corner of
# the upper-right pane, its threads anchored on the side post and the upper crossbar. The wall ends in a capping a
# little above the arch and at a corner a little right of the window, so the night sky shows above and beside it.
import math

SCENE = {"category": "4", "backdrop": "#1f3a9e", "azimuth": 20, "elevation": 8, "lens": 70, "light": "left"}

HALF = 0.28      # half width of the wall opening
SPRING = 0.72    # z where the arch starts
TOP = SPRING + HALF
WALL_TOP = 1.07
CORNER = 0.75    # x of the house corner, right of the window


def build(k):
    wood = k.mat("#5a3620", "matte")
    glass = k.mat("#a9bfdc", "glass")
    stone = k.mat("#8b9099", "matte")
    stone_light = k.mat("#a3a8b0", "matte")
    room = k.mat("#2b2230", "matte")
    web = k.mat("#f6f6f2", "matte")

    # --- Stone wall around the opening (face at y = 0, 0.3 thick), ending at a corner on the right ---
    k.box((3.0, 0.3, 3.2), at=(-(HALF + 1.5), 0.15, WALL_TOP - 1.6), m=stone, bevel=0, setting=True)
    rw = CORNER - HALF
    k.box((rw, 0.3, 3.2), at=(HALF + rw / 2, 0.15, WALL_TOP - 1.6), m=stone, bevel=0, setting=True)
    # the side wall of the house, running back from the corner
    k.box((0.3, 3.0, 3.2), at=(CORNER - 0.15, 1.5, WALL_TOP - 1.6), m=stone, bevel=0, setting=True)
    k.box((2 * HALF, 0.3, 2.0), at=(0, 0.15, -1.0), m=stone, bevel=0, setting=True)
    # the stone above the arch: a ring around the arch, its outer edge squared to the opening, lower half removed
    S = WALL_TOP - SPRING
    spandrel = k.lathe([(HALF, 0.0), (0.5, 0.0), (0.5, 0.301), (HALF, 0.301), (HALF, 0.0)],
                       at=(0, 0.3, SPRING), rot=(90, 0, 0), m=stone, setting=True, verts=64)

    def square_up(p):
        x, y, z = p
        r = math.hypot(x, y)
        if r > HALF + 0.01:
            if y <= 0.0:
                return (math.copysign(HALF, x), 0.0, z)
            fx = HALF / abs(x) if abs(x) > 1e-6 else 1e9
            f = min(fx, S / y)
            return (x * f, y * f, z)
        return (x, max(y, 0.0), z)

    k.warp(spandrel, square_up)
    # capping along the wall top and back along the side wall
    k.box((CORNER + 3.6, 0.42, 0.08), at=((CORNER + 0.04 - 3.5) / 2 + 0.02, 0.15, WALL_TOP + 0.04),
          m=stone_light, bevel=0.015, setting=True)
    k.box((0.42, 3.0, 0.08), at=(CORNER - 0.15, 1.5, WALL_TOP + 0.04), m=stone_light, bevel=0.015, setting=True)

    # --- Dark room behind the window, with an inner shelf and the candle ---
    k.box((1.0, 0.05, 1.8), at=(0, 0.62, 0.4), m=room, setting=True)
    k.box((1.0, 0.35, 0.05), at=(0, 0.45, -0.025), m=room, setting=True)
    k.box((2 * HALF, 0.3, 0.04), at=(0, 0.2, -0.02), m=k.mat("#4a2e1c", "matte"))
    k.lathe([(0, 0), (0.07, 0), (0.075, 0.014), (0.058, 0.018), (0.028, 0.018), (0.028, 0.034), (0, 0.034)],
            at=(0.1, 0.22, 0.0), m=k.mat("#b07a3a", "metal"))
    k.cyl(0.032, 0.18, at=(0.1, 0.22, 0.12), m=k.mat("#f2e6c8", "satin"))
    k.cyl(0.005, 0.018, at=(0.1, 0.22, 0.218), m=k.mat("#2a2018", "matte"))
    k.sphere(0.024, at=(0.1, 0.22, 0.25), scale=(1, 1, 1.7), m=k.mat("#ffd23a", "glow"))

    # --- Window frame: side posts, arch pieces, outside stone sill ---
    cw, cd, cy = 0.07, 0.1, 0.01
    for side in (-1, 1):
        k.box((cw, cd, SPRING + 0.01), at=(side * (HALF - cw / 2), cy, SPRING / 2), m=wood)
    rc = HALF - cw / 2
    segs = 18
    for i in range(segs):
        th = (i + 0.5) * 180 / segs
        t = math.radians(th)
        k.box((cw, cd, rc * math.pi / segs * 1.12), at=(rc * math.cos(t), cy, SPRING + rc * math.sin(t)),
              rot=(0, -th, 0), m=wood, bevel=0.004)
    k.box((2 * HALF + 0.14, 0.2, 0.06), at=(0, -0.04, -0.03), m=stone_light, bevel=0.01)

    # --- Glass, upright bar, crossbars and two arch spokes ---
    gi = HALF - cw
    k.box((2 * gi, 0.01, SPRING), at=(0, 0.02, SPRING / 2), m=glass, bevel=0)
    arch_glass = k.cyl(gi, 0.01, at=(0, 0.02, SPRING), rot=(90, 0, 0), m=glass, bevel=0)
    k.warp(arch_glass, lambda p: (p[0], max(p[1], 0.0), p[2]))  # flatten the lower half: a half disc
    bar = 0.04
    k.box((bar, 0.05, TOP - cw), at=(0, 0.0, (TOP - cw) / 2), m=wood)
    for z in (0.36, SPRING):
        k.box((2 * gi, 0.044, bar), at=(0, 0.003, z), m=wood)
    for a in (45, 135):
        t = math.radians(a)
        k.box((gi, 0.044, bar), at=(gi / 2 * math.cos(t), 0.003, SPRING + gi / 2 * math.sin(t)),
              rot=(0, -a, 0), m=wood)

    # --- Cobweb in the top-right corner of the upper-right pane ---
    cx, cz, wy = gi, SPRING - bar / 2, -0.028  # corner of the side post and the upper crossbar, just in front
    radials = [180, 196, 213, 230, 247, 263, 270]  # first and last lie along the crossbar and the post
    for a in radials:
        t = math.radians(a)
        k.tube([(cx, wy, cz), (cx + 0.2 * math.cos(t), wy, cz + 0.2 * math.sin(t))], 0.006, web)
    for r in (0.045, 0.085, 0.125, 0.165):
        pts = [(cx + r * math.cos(math.radians(a)), wy, cz + r * math.sin(math.radians(a))) for a in radials]
        line = []
        for p, q in zip(pts, pts[1:]):
            mid = ((p[0] + q[0]) / 2, wy, (p[2] + q[2]) / 2)
            line += [p, (mid[0] + (cx - mid[0]) * 0.06, wy, mid[2] + (cz - mid[2]) * 0.06)]  # slight sag
        line.append(pts[-1])
        k.tube(line, 0.005, web)
