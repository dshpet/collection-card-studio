# Badge wallet: an open bifold leather wallet lying flat on a dark wooden table, seen from high above. The two
# leather flaps lie flat on the table and meet at a rounded spine. The left flap carries a raised gold shield badge
# riveted to a leather backing patch; the right flap has a leather pocket that holds a cream ID card with a raised
# green stripe, the card's top edge showing above the pocket lip. The table planks rest on a solid dark tabletop
# slab, so no backdrop shows through the seams, and they fill the whole card.
import math

SCENE = {"category": "3", "backdrop": "#3fd0e8", "azimuth": 24, "elevation": 64, "lens": 60, "light": "left"}


def shield(u, v, w, h):
    """Map a unit-disc point (u, v) to a shield outline w wide, h tall: flat top, round shoulders, pointed foot."""
    if v >= 0:
        x = math.copysign(min(abs(u) * 1.35, 1.0), u) * w / 2
        y = min(v * 1.35, 1.0) * h * 0.42
    else:
        t = -v
        x = u * (w / 2) * (1 - t ** 1.6)
        y = -t * h * 0.58
    return x, y


def build(k):
    leather = k.mat("#6e3b1d", "matte")
    leather_dark = k.mat("#4e2a14", "matte")
    leather_light = k.mat("#85502b", "matte")
    gold = k.mat("#e8b23a", "metal")
    gold_deep = k.mat("#c98f1f", "metal")
    cream = k.mat("#f4ead0", "satin")
    green = k.mat("#2f9e4f", "satin")

    w, d, t = 0.46, 0.42, 0.03  # each flap: width, depth, thickness
    # Two flaps lying flat on the table, spine along y at x = 0.
    for side in (-1, 1):
        k.box((w, d, t), at=(side * (w / 2 + 0.012), 0, t / 2), m=leather, bevel=0.012)
    # Rounded spine where the leather folds, resting on the table between the flaps.
    k.cyl(0.024, d - 0.004, at=(0, 0, 0.024), rot=(90, 0, 0), m=leather_dark, bevel=0.006)

    top = t  # flap top surface

    # Left flap: leather backing patch with the gold shield badge.
    bx, by = -0.245, 0.0
    patch = k.cyl(0.13, 0.012, at=(bx, by, top + 0.004), m=leather_light, bevel=0.004)
    k.warp(patch, lambda p: (*shield(p[0] / 0.13, p[1] / 0.13, 0.27, 0.32), p[2]))
    plate = k.cyl(0.13, 0.022, at=(bx, by + 0.004, top + 0.019), m=gold, bevel=0.006)
    k.warp(plate, lambda p: (*shield(p[0] / 0.13, p[1] / 0.13, 0.22, 0.27), p[2]))
    boss = k.cyl(0.13, 0.014, at=(bx, by + 0.008, top + 0.035), m=gold_deep, bevel=0.004)
    k.warp(boss, lambda p: (*shield(p[0] / 0.13, p[1] / 0.13, 0.15, 0.19), p[2]))
    k.sphere(0.03, at=(bx, by + 0.012, top + 0.045), scale=(1, 1, 0.45), m=gold)
    for rx in (-0.08, 0.08):  # rivets holding the badge's shoulders
        k.sphere(0.011, at=(bx + rx, by + 0.085, top + 0.032), scale=(1, 1, 0.6), m=gold_deep)

    # Right flap: the ID card lies on the flap inside a leather pocket; its upper part shows above the pocket lip.
    cx, cy = 0.245, 0.03
    k.box((0.34, 0.24, 0.008), at=(cx, cy, top + 0.003), m=cream, bevel=0.003)
    k.box((0.34, 0.05, 0.004), at=(cx, cy + 0.065, top + 0.007), m=green, bevel=0.0015)
    k.box((0.16, 0.022, 0.004), at=(cx - 0.06, cy - 0.005, top + 0.007), m=green, bevel=0.0015)
    k.box((0.38, 0.17, 0.016), at=(cx, -0.115, top + 0.007), m=leather_light, bevel=0.006)  # pocket front
    k.tube([(cx - 0.19, -0.03, top + 0.014), (cx + 0.19, -0.03, top + 0.014)], 0.008, leather_dark)  # lip

    # Dark wooden table: a solid tabletop slab with planks running left-right on it, filling the card.
    k.box((8, 8, 0.1), at=(0, 0, -0.11), m=k.mat("#1e1009", "matte"), bevel=0, setting=True)
    woods = ("#2f1a0d", "#3a2112", "#2a170b", "#3f2616")
    for i in range(20):
        k.box((8, 0.3, 0.06), at=(0, -3.0 + i * 0.305, -0.03), m=k.mat(woods[i % 4], "matte"), bevel=0.012,
              setting=True)
