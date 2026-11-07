# Folding fan, open in a half circle: fifteen gold ribs fan out from one pivot pin at the bottom; the two outer
# guard sticks are wider and run the full length in front of the silk. The red silk is pleated: each panel between
# two ribs folds once along its middle, alternating forward and back, and covers the outer part of the ribs. Below
# the pivot the stacked rib ends make a short rounded handle. It floats, tilted, showing its front and some depth.
import math

SCENE = {"category": "1", "backdrop": "#5cc2f2", "azimuth": 22, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e2ad3c", "metal")
    pin = k.mat("#b9822a", "metal")
    silk = k.mat("#d8222c", "satin")

    px, pz = 0.0, 0.0          # pivot
    r_in, r_out = 0.24, 0.58   # silk band
    n = 15
    a0, a1 = 0.0, 180.0
    angles = [math.radians(a0 + (a1 - a0) * i / (n - 1)) for i in range(n)]
    fold = 0.028

    def panel(ra, rb, ya, yb):
        part = k.box((1, 1, 1), at=(0, 0, 0), m=silk, bevel=0)

        def fn(v):
            x, y, z = v
            r = r_in if x < 0 else r_out
            a, yo = (ra, ya) if y < 0 else (rb, yb)
            return (px + r * math.cos(a), yo + z * 0.008, pz + r * math.sin(a))

        k.warp(part, fn)

    for i in range(n - 1):
        ra, rb = angles[i], angles[i + 1]
        mid = (ra + rb) / 2
        f = -fold if i % 2 == 0 else fold
        panel(ra, mid, 0.0, f)
        panel(mid, rb, f, 0.0)

    # ribs: from a short tail below the pivot up into the silk; the outer guards run the full length in front
    for i, a in enumerate(angles):
        guard = i in (0, n - 1)
        length = r_out + 0.015 if guard else r_in + 0.08
        tail = 0.07
        w = 0.034 if guard else 0.022
        y = -0.016 if guard else -0.002 + 0.0015 * (i - n / 2)
        c = (length - tail) / 2
        k.box((length + tail, 0.012, w), at=(px + c * math.cos(a), y, pz + c * math.sin(a)),
              rot=(0, -math.degrees(a), 0), m=gold, bevel=0.005)

    # rounded handle end where the rib tails stack, and the pivot pin through all ribs with a head on each side
    k.cyl(0.075, 0.036, at=(px, -0.002, pz), rot=(90, 0, 0), m=gold, bevel=0.008)
    k.cyl(0.028, 0.07, at=(px, -0.004, pz), rot=(90, 0, 0), m=pin, bevel=0.006)
    k.sphere(0.03, at=(px, -0.04, pz), scale=(1, 0.45, 1), m=pin)
    k.sphere(0.03, at=(px, 0.032, pz), scale=(1, 0.45, 1), m=pin)

    k.turn(8, -14, 12)
