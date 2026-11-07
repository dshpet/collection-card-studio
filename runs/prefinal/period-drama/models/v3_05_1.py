# Violin, floating: the curved body is an arched, waisted outline with two f-holes cut in the top plate. The neck
# rises from the top of the body and carries the black fingerboard; above it the pegbox holds four pegs, two each
# side, and ends in the scroll. Four strings run from the nut over the bridge, which stands on its feet on the top
# plate, to the black tailpiece, which is tied by its tailgut to the end button. The chin rest sits on the lower
# bout beside the tailpiece. The violin stands on its long axis and is tilted so it lies diagonally across the card.
import math

SCENE = {"category": "1", "backdrop": "#5cd65a", "azimuth": 25, "elevation": 10, "lens": 70, "light": "left"}


def build(k):
    wood = k.mat("#9c4a1a", "gloss")
    neckwood = k.mat("#a8582a", "satin")
    ebony = k.mat("#1c1b1e", "satin")
    bridge_wood = k.mat("#e0b676", "matte")
    hole = k.mat("#120a05", "matte")
    steel = k.mat("#d9d8d2", "metal")

    # Body: a disk lathe warped into the violin outline. Local u (x) runs along the length, local z is the
    # thickness and becomes world y; the top plate (front) arches toward -y.
    profile = [(0, -0.060), (0.2, -0.0595), (0.4, -0.057), (0.55, -0.053), (0.7, -0.047), (0.85, -0.041),
               (0.95, -0.036), (1.0, -0.033), (1.0, 0.033), (0.95, 0.036), (0.85, 0.040), (0.7, 0.046),
               (0.4, 0.054), (0.2, 0.057), (0, 0.058)]
    body = k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=wood, verts=160)

    def outline(p):
        u, v, t = p
        g = 0.18 - 0.02 * u - 0.085 * math.exp(-((u - 0.05) / 0.22) ** 2)
        return (v * g, t, 0.3 + 0.3 * u)

    k.warp(body, outline)

    # F-holes, sunk into the top plate (mirror images).
    for s in (-1, 1):
        pts = [(s * 0.076, -0.047, 0.365), (s * 0.066, -0.048, 0.335), (s * 0.060, -0.049, 0.295),
               (s * 0.064, -0.048, 0.255), (s * 0.055, -0.047, 0.222)]
        k.tube(pts, 0.008, hole, curved=True)
        for x, z in ((s * 0.080, 0.37), (s * 0.052, 0.216)):
            k.sphere(0.011, at=(x, -0.045, z), scale=(1, 0.5, 1), m=hole)

    # Neck, fingerboard and nut.
    k.box((0.042, 0.05, 0.26), at=(0, -0.05, 0.72), m=neckwood, bevel=0.015)
    fb = k.box((0.07, 0.016, 0.44), at=(0, -0.089, 0.62), rot=(-2.3, 0, 0), m=ebony, bevel=0.004)
    k.warp(fb, lambda p: (p[0] * (1 - 0.4 * (p[2] + 0.22) / 0.44), p[1], p[2]))
    k.box((0.044, 0.02, 0.012), at=(0, -0.09, 0.846), m=ebony, bevel=0.003)

    # Pegbox, pegs and scroll.
    k.box((0.045, 0.04, 0.125), at=(0, -0.058, 0.9), rot=(-10, 0, 0), m=neckwood, bevel=0.01)
    for i, z in enumerate((0.865, 0.89, 0.915, 0.94)):
        s = -1 if i % 2 == 0 else 1
        y = -0.058 + (z - 0.9) * 0.176
        k.cyl(0.008, 0.075, at=(s * 0.037, y, z), rot=(0, 90, 0), m=ebony)
        k.sphere(0.011, at=(s * 0.062, y, z), m=ebony)
        k.box((0.012, 0.03, 0.034), at=(s * 0.078, y, z), m=ebony, bevel=0.006)
    sc = (-0.046, 0.987)
    k.cyl(0.03, 0.036, at=(0, sc[0], sc[1]), rot=(0, 90, 0), m=neckwood, bevel=0.006)
    for s in (-1, 1):
        spiral = []
        for j in range(30):
            t = j * 2.5 * math.pi / 29
            r = 0.027 - 0.019 * j / 29
            spiral.append((s * 0.019, sc[0] + r * math.sin(t), sc[1] + r * math.cos(t)))
        k.tube(spiral, 0.006, neckwood, curved=True)

    # Bridge: stands upright on the top plate (feet at y -0.057) and carries the strings at y -0.12.
    k.box((0.075, 0.064, 0.012), at=(0, -0.089, 0.29), m=bridge_wood, bevel=0.003)
    for s in (-1, 1):
        k.box((0.016, 0.008, 0.016), at=(s * 0.026, -0.059, 0.29), m=bridge_wood, bevel=0.002)

    # Tailpiece, end button and tailgut.
    tp = k.box((0.055, 0.012, 0.12), at=(0, -0.066, 0.115), rot=(12, 0, 0), m=ebony, bevel=0.005)
    k.warp(tp, lambda p: (p[0] * (0.65 + 0.35 * (p[2] + 0.06) / 0.12), p[1], p[2]))
    k.cyl(0.012, 0.022, at=(0, 0, -0.008), m=ebony)
    k.tube([(0, -0.05, 0.06), (0, -0.04, 0.006), (0, -0.012, -0.012)], 0.005, ebony, curved=True)

    # Strings: nut, over the bridge, to the tailpiece.
    for i in (-1.5, -0.5, 0.5, 1.5):
        lift = 0.003 if abs(i) < 1 else 0.0
        k.tube([(i * 0.011, -0.094, 0.845), (i * 0.021, -0.119 - lift, 0.29), (i * 0.012, -0.086, 0.165)],
               0.0055, steel)

    # Chin rest on the lower bout, beside the tailpiece, resting on the plate.
    k.blob([(-0.068, -0.058, 0.08, 0.045, (1.15, 0.35, 0.8)),
            (-0.03, -0.06, 0.06, 0.032, (1.0, 0.35, 0.7))], ebony)

    k.turn(0, 28, 0)
