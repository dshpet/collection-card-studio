# Iron gate: two wrought iron leaves, each a frame of stiles and rails with spear-top bars, close between two
# stone gateposts. The top rail of the leaves rises in an arch to the center, with scroll curls under it. Each
# leaf turns on two hinge pins set in its post. A chain loops around the two center stiles and a gold padlock
# hangs from it. The gravel path runs through the gate; a dark lawn and hedges sit behind.
import math

SCENE = {"category": "4", "backdrop": "#1f3a8f", "azimuth": 20, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#1e1f23", "metal")
    stone = k.mat("#77777a", "matte")
    stone_lt = k.mat("#8a8a8c", "matte")
    gold = k.mat("#e2b23a", "metal")
    r = 0.014
    half = 0.505
    mid = 0.018

    def arch(x):
        return 0.80 + 0.16 * math.cos(math.pi * x / (2 * half))

    for side in (-1, 1):
        outer, inner = side * half, side * mid
        # stiles
        k.tube([(outer, 0, 0.05), (outer, 0, arch(outer))], r * 1.4, iron)
        k.tube([(inner, 0, 0.05), (inner, 0, arch(inner))], r * 1.4, iron)
        # straight rails
        for z in (0.06, 0.20, 0.62):
            k.tube([(outer, 0, z), (inner, 0, z)], r * 1.2, iron)
        # arched top rail
        xs = [outer + (inner - outer) * i / 12 for i in range(13)]
        k.tube([(x, 0, arch(x)) for x in xs], r * 1.2, iron, curved=True)
        # spear-top bars
        for i in range(1, 7):
            x = outer + (inner - outer) * i / 7
            top = arch(x) + 0.09
            k.tube([(x, 0, 0.06), (x, 0, top)], r, iron)
            k.cone(0.03, 0.0, 0.07, at=(x, 0, top + 0.03), rot=(0, 0, 0), m=iron)
        # spear tips on the stiles too
        for x in (outer, inner):
            k.cone(0.032, 0.0, 0.07, at=(x, 0, arch(x) + 0.035), rot=(0, 0, 0), m=iron)
        # scroll curls between the upper rail and the arch
        for cx_frac, turn in ((0.3, 1), (0.7, -1)):
            cx = outer + (inner - outer) * cx_frac
            cz = 0.62 + (arch(cx) - 0.62) * 0.5
            rad = (arch(cx) - 0.62) * 0.5 - 0.012
            pts = []
            for j in range(40):
                t = j / 39
                a = turn * side * (math.pi / 2 + t * 3.2 * math.pi)
                rr = rad * (1 - 0.75 * t)
                pts.append((cx + rr * math.cos(a), 0, cz + rr * math.sin(a)))
            k.tube(pts, r * 0.9, iron, curved=True)
        # lower scroll pair between bottom rails
        for cx_frac in (0.35, 0.65):
            cx = outer + (inner - outer) * cx_frac
            pts = []
            for j in range(30):
                t = j / 29
                a = math.pi * 1.5 + t * 2.6 * math.pi
                rr = 0.058 * (1 - 0.7 * t)
                pts.append((cx + rr * math.cos(a), 0, 0.13 + rr * math.sin(a)))
            k.tube(pts, r * 0.9, iron, curved=True)

        # stone gatepost
        px = side * 0.635
        k.box((0.30, 0.30, 0.14), at=(px, 0, 0.07), m=stone_lt, bevel=0.015)
        k.box((0.24, 0.24, 1.0), at=(px, 0, 0.64), m=stone, bevel=0.012)
        k.box((0.30, 0.30, 0.07), at=(px, 0, 1.175), m=stone_lt, bevel=0.015)
        k.cyl(0.055, 0.05, at=(px, 0, 1.235), m=stone_lt)
        k.sphere(0.1, at=(px, 0, 1.345), m=stone_lt)
        # hinges: pin in the post, strap to the stile
        for z in (0.16, 0.70):
            k.cyl(0.02, 0.09, at=(side * 0.525, 0, z), m=iron)
            k.box((0.04, 0.03, 0.025), at=(side * 0.53, 0, z - 0.05), m=iron, bevel=0.004)
            k.box((0.10, 0.018, 0.03), at=(side * 0.47, -0.02, z), m=iron, bevel=0.004)

    # chain looped around the two center stiles: fewer, bigger links
    links = 10
    for i in range(links):
        a = 2 * math.pi * i / links - math.pi / 2
        x, y = 0.075 * math.cos(a), 0.05 * math.sin(a)
        z = 0.46 - 0.01 * math.sin(a)
        heading = math.degrees(a) + 90
        tilt = 90 if i % 2 else 0
        k.torus(0.026, 0.009, at=(x, y, z), rot=(tilt, 0, heading), m=iron)
    # padlock hanging from the front link of the chain
    k.torus(0.03, 0.009, at=(0, -0.05, 0.42), rot=(90, 0, 0), m=k.mat("#c9ced6", "metal"))
    k.box((0.10, 0.04, 0.09), at=(0, -0.05, 0.36), m=gold, bevel=0.012)
    k.cyl(0.008, 0.01, at=(0, -0.072, 0.35), rot=(90, 0, 0), m=k.mat("#5a4413", "satin"))

    # gravel path through the gate, dark lawn on both sides and behind, hedges at the back
    k.box((1.1, 8, 0.04), at=(0, 0.5, 0.0), m=k.mat("#8f8470", "matte"), bevel=0.01, setting=True)
    k.floor("#1f4a2a", "matte", size=40, z=-0.01)
    for x, y, s in ((-1.6, 2.2, 0.55), (-0.9, 2.8, 0.6), (0.2, 3.2, 0.7), (1.2, 2.6, 0.6), (1.9, 2.0, 0.5)):
        k.blob([(x, y, s * 0.6, s), (x + s * 0.7, y + 0.2, s * 0.5, s * 0.8), (x - s * 0.6, y + 0.1, s * 0.45, s * 0.75)],
               k.mat("#173b22", "matte"), setting=True)
