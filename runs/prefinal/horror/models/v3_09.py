# Haunted door: a tall arched plank door of dark wood stands on a stone porch step, set into a grey stone house wall
# with a stone arch surround. The surround is the door's frame and counts for framing, so the whole doorway fits the
# card with the wall's coping and a strip of night sky above it. Two iron strap hinges run in from the left edge and
# turn on barrels at the jamb; a brass ring knocker hangs from a boss on the right; a small round window with a brass
# frame and cross bars glows yellow near the top of the arch.
import math

SCENE = {"category": "4", "backdrop": "#1f3a9e", "azimuth": 20, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#4a2c17", "matte")
    groove = k.mat("#2a170b", "matte")
    iron = k.mat("#34353a", "metal")
    brass = k.mat("#c99a3a", "metal")
    glow = k.mat("#ffd84a", "glow")

    w, base, spring = 0.3, 0.12, 0.90
    # door leaf: straight lower part and a half-round top, both with the same front face
    k.box((2 * w, 0.06, spring - base), at=(0, -0.01, (spring + base) / 2), m=wood, bevel=0.003)
    k.cyl(w, 0.06, at=(0, -0.01, spring), rot=(90, 0, 0), m=wood, bevel=0.003)
    # plank joints
    for x in (-0.2, -0.1, 0.0, 0.1, 0.2):
        top = spring + math.sqrt(w * w - x * x) - 0.025
        k.box((0.012, 0.006, top - base - 0.02), at=(x, -0.041, (top + base + 0.02) / 2), m=groove, bevel=0.002)

    # strap hinges on the left, turning on barrels at the jamb
    for z in (0.32, 0.80):
        k.box((0.36, 0.012, 0.045), at=(-0.12, -0.047, z), m=iron, bevel=0.004)
        k.cyl(0.03, 0.012, at=(0.06, -0.047, z), rot=(90, 0, 0), m=iron)
        k.cyl(0.022, 0.1, at=(-0.31, -0.035, z), m=iron)

    # brass ring knocker on the right
    k.sphere(0.035, at=(0.17, -0.05, 0.64), scale=(1, 0.55, 1), m=brass)
    k.torus(0.07, 0.014, at=(0.17, -0.062, 0.575), rot=(90, 0, 0), m=brass)
    k.cyl(0.022, 0.012, at=(0.17, -0.046, 0.505), rot=(90, 0, 0), m=brass)

    # small round glowing window near the top
    wc = (0, 1.0)
    k.cyl(0.085, 0.012, at=(wc[0], -0.042, wc[1]), rot=(90, 0, 0), m=glow)
    k.torus(0.09, 0.018, at=(wc[0], -0.046, wc[1]), rot=(90, 0, 0), m=brass)
    k.box((0.17, 0.012, 0.016), at=(wc[0], -0.05, wc[1]), m=brass, bevel=0.003)
    k.box((0.016, 0.012, 0.17), at=(wc[0], -0.05, wc[1]), m=brass, bevel=0.003)

    # stone door surround (the doorway frame, part of the hero for framing)
    stone = k.mat("#8d939c", "matte")
    stone2 = k.mat("#7a8089", "matte")
    stone3 = k.mat("#9da3ab", "matte")
    for side in (-1, 1):
        z = base
        i = 0
        while z < spring - 0.01:
            h = min(0.13, spring - z)
            k.box((0.13 if i % 2 else 0.17, 0.07, h - 0.012), at=(side * (0.375 + (0 if i % 2 else 0.02)), -0.035,
                  z + h / 2), m=stone if i % 2 else stone3, bevel=0.012)
            z += h
            i += 1
    n = 9
    for i in range(n):
        a = math.pi * (i + 0.5) / n
        rad = 0.38 if i != n // 2 else 0.4
        k.box((0.14 if i != n // 2 else 0.18, 0.07, 0.118), at=(rad * math.cos(a), -0.035, spring + rad * math.sin(a)),
              rot=(0, -math.degrees(a), 0), m=stone3 if i % 2 else stone, bevel=0.012)

    # --- setting: wall with coping, step, ground; sky shows above the coping ---
    top = 1.40
    k.box((3.4, 0.3, top), at=(0, 0.15, top / 2), m=stone2, bevel=0.01, setting=True)
    k.box((3.5, 0.38, 0.06), at=(0, 0.13, top + 0.03), m=stone, bevel=0.012, setting=True)
    row, z = 0, 0.0
    while z < top - 0.05:
        x = -1.7 + (0.15 if row % 2 else 0.0)
        j = 0
        while x < 1.7:
            cx, cz = x + 0.15, z + 0.07
            in_door = (abs(cx) < 0.6 and cz < spring) or math.hypot(cx, cz - spring) < 0.6
            if not in_door and not (abs(cx) < 0.6 and cz < base):
                k.box((0.28, 0.02, 0.12), at=(cx, -0.008, cz), m=(stone, stone3, stone2)[(row + j) % 3],
                      bevel=0.01, setting=True)
            x += 0.3
            j += 1
        z += 0.14
        row += 1

    k.box((1.2, 0.42, base), at=(0, -0.21, base / 2), m=stone3, bevel=0.015, setting=True)
    k.floor("#5a606b", "matte")
