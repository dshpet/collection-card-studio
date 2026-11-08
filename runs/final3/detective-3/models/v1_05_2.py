# Badge wallet, open and lying flat on a desk: two leather flaps joined by a rounded fold at the spine, each
# with a lighter inner lining. The gold shield badge sits on the left lining: a straight-sided top that tapers
# to a point toward the front, with a raised rim and a round boss. The cream card lies on the right lining with
# its lower part tucked into a leather pocket stitched onto the lining; the green stripe is a thin inlay across
# its top. A honey wooden desk of wide planks fills the card, seen from high above.
SCENE = {"category": "3", "backdrop": "#45c8e8", "azimuth": 25, "elevation": 65, "lens": 60, "light": "left"}


def build(k):
    shell = k.mat("#4e2812", "matte")
    lining = k.mat("#6e3a1c", "matte")
    pocket = k.mat("#3f200e", "matte")
    gold = k.mat("#f2b632", "metal")
    gold_dark = k.mat("#c98a1c", "metal")
    cream = k.mat("#e2c98e", "satin")
    green = k.mat("#1f8a3c", "satin")

    # Two flaps and the fold between them. Lining top is at z = 0.032.
    for side in (-1, 1):
        cx = side * 0.255
        k.box((0.48, 0.44, 0.024), at=(cx, 0, 0.012), m=shell, bevel=0.01)
        k.box((0.44, 0.40, 0.008), at=(cx, 0, 0.028), m=lining, bevel=0.004)
    k.cyl(0.026, 0.44, at=(0, 0, 0.018), rot=(90, 0, 0), m=shell, bevel=0.006)

    # Gold shield badge on the left flap, its back plate set into the lining.
    bx, by = -0.255, 0.0

    def shield(w, top, mid, bottom, z, t, m):
        k.box((w, top - mid + 0.004, t), at=(bx, by + (top + mid) / 2, z), m=m, bevel=0.003)
        h = mid - bottom
        tip = k.box((w, h, t), at=(bx, by + mid - h / 2, z), m=m, bevel=0.003)
        k.warp(tip, lambda p: (p[0] * max(0.06, (p[1] + h / 2) / h), p[1], p[2]))

    shield(0.22, 0.15, 0.02, -0.15, 0.038, 0.016, gold_dark)   # z 0.030 - 0.046
    shield(0.19, 0.135, 0.02, -0.125, 0.048, 0.008, gold)      # z 0.044 - 0.052
    k.cyl(0.05, 0.012, at=(bx, by + 0.02, 0.056), m=gold_dark, bevel=0.004)   # z 0.050 - 0.062
    k.cyl(0.032, 0.01, at=(bx, by + 0.02, 0.065), m=gold, bevel=0.004)        # z 0.060 - 0.070

    # Cream card on the right lining, its lower part in a leather pocket stitched to the lining.
    rx = 0.255
    k.box((0.36, 0.24, 0.006), at=(rx, 0.04, 0.0345), m=cream, bevel=0.002)
    k.box((0.36, 0.05, 0.003), at=(rx, 0.12, 0.0385), m=green, bevel=0.001)
    k.box((0.42, 0.15, 0.016), at=(rx, -0.115, 0.039), m=pocket, bevel=0.004)

    # Light honey wooden desk of wide planks, top at z = 0.
    tones = ("#e3b56e", "#dcaa62", "#e8bd78")
    for i in range(12):
        y = -2.75 + i * 0.5
        k.box((6, 0.49, 0.1), at=(0, y, -0.05), m=k.mat(tones[i % 3], "matte"), bevel=0.01, setting=True)
