# Haunted door: an arched plank door hangs in a stone arch set in an old house's gray stone wall. Two black iron
# strap hinges run across the planks from knuckles pinned into the left jamb; a ring knocker hangs from a boss
# at the middle; a small round peephole glows above it. The door stands on a stone doorstep on stone ground.
# Front-on like the real door card: the wall fills the card, the framing holds the door.
import math

SCENE = {"category": "4", "backdrop": "#5ab8ee", "azimuth": 8, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    wood = [k.mat(c, "matte") for c in ("#7a4a2a", "#86532f", "#734426", "#8a5632", "#7d4c2b", "#6f4225")]
    groove = k.mat("#3e2414", "matte")
    iron = k.mat("#1e1e22", "metal")
    glow = k.mat("#ffd84a", "glow")
    stone = k.mat("#8e9196", "matte")
    stone_lt = k.mat("#a3a6ab", "matte")
    stone_dk = k.mat("#7b7e84", "matte")

    base, spring, half, t = 0.07, 0.72, 0.3, 0.05   # door bottom, arch spring line, half width, thickness
    yc = -0.035                                       # door center plane; front face at y = -0.06

    # Door: six vertical planks up to the spring line, the arched head as one disc, grooves between planks.
    for i in range(6):
        x = -half + 0.05 + i * 0.1
        k.box((0.1, t, spring - base), at=(x, yc, (base + spring) / 2), m=wood[i], bevel=0.006)
    k.cyl(half, t, at=(0, yc, spring), rot=(90, 0, 0), m=wood[0], bevel=0.006, verts=96)
    for i in range(1, 6):
        x = -half + i * 0.1
        top = spring + math.sqrt(half * half - x * x) - 0.012
        k.box((0.008, 0.004, top - base - 0.01), at=(x, -0.061, (base + 0.01 + top) / 2), m=groove, bevel=0)

    # Strap hinges: straps across the planks, pointed ends, knuckles on pins set into the left jamb.
    for z in (0.24, 0.62):
        k.box((0.42, 0.012, 0.05), at=(-0.09, -0.066, z), m=iron, bevel=0.003)
        k.cyl(0.04, 0.012, at=(0.12, -0.066, z), rot=(90, 0, 0), m=iron, verts=4)
        k.cyl(0.024, 0.08, at=(-0.305, -0.07, z), m=iron, bevel=0.004)
        k.cyl(0.01, 0.12, at=(-0.305, -0.07, z), m=iron)
        for x in (-0.22, -0.12, -0.02):
            k.sphere(0.011, at=(x, -0.073, z), m=iron)

    # Ring knocker: a boss on the door, a staple, and the ring hanging from it.
    k.cyl(0.04, 0.02, at=(0, -0.07, 0.5), rot=(90, 0, 0), m=iron, bevel=0.004)
    k.torus(0.018, 0.007, at=(0, -0.086, 0.49), rot=(0, 90, 0), m=iron)
    k.torus(0.075, 0.013, at=(0, -0.092, 0.415), rot=(90, 0, 0), m=iron)

    # Peephole: iron rim with the glowing lens.
    k.torus(0.036, 0.01, at=(0, -0.063, 0.86), rot=(90, 0, 0), m=iron)
    k.cyl(0.03, 0.008, at=(0, -0.061, 0.86), rot=(90, 0, 0), m=glow)

    # Stone arch: jamb blocks on the doorstep and voussoirs around the head, standing proud of the wall.
    for side in (-1, 1):
        for j in range(3):
            z0 = base + j * (spring - base) / 3
            k.box((0.13, 0.11, 0.205), at=(side * 0.375, -0.055, z0 + 0.1075),
                  m=stone_lt if (j + (side > 0)) % 2 else stone, bevel=0.012, setting=True)
    n = 9
    for i in range(n):
        a = math.pi * (i + 0.5) / n
        big = i == n // 2
        r = 0.38 if not big else 0.395
        k.box((0.14 if not big else 0.17, 0.11, 0.12), at=(r * math.cos(a), -0.055, spring + r * math.sin(a)),
              rot=(0, -math.degrees(a), 0), m=stone_lt if i % 2 else stone, bevel=0.012, setting=True)

    # Doorstep, ground and the house wall.
    k.box((1.0, 0.32, 0.07), at=(0, -0.16, 0.035), m=stone_lt, bevel=0.015, setting=True)
    k.floor("#7f8389", "matte")
    k.box((6, 0.4, 3.5), at=(0, 0.2, 1.75), m=stone, bevel=0.01, setting=True)
    blocks = [(-0.75, 0.15), (-0.62, 0.45), (-0.8, 0.8), (-0.6, 1.1), (-0.85, 1.35),
              (0.72, 0.2), (0.6, 0.55), (0.82, 0.9), (0.62, 1.2), (0.85, 1.45),
              (-0.3, 1.3), (0.05, 1.4), (0.35, 1.28), (-1.05, 0.5), (1.05, 0.7)]
    for i, (x, z) in enumerate(blocks):
        k.box((0.24, 0.02, 0.13), at=(x, -0.008, z), m=stone_dk if i % 3 == 0 else stone_lt,
              bevel=0.008, setting=True)
