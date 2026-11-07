# Chopping board: one rectangular wooden board lying flat on a blue gingham tablecloth, seen from high above.
# The board is a single piece: a flat lathed ring around the handle hole, squared off to the board's rectangle,
# so the round hole at the +x end is a real opening onto the cloth. On top lie neat piles of slices, each row
# shingled so every slice rests on the board and on the slice before: tomato, cucumber, carrot.
import math

SCENE = {"category": "3", "backdrop": "#4f8fdc", "azimuth": 25, "elevation": 65, "lens": 70, "light": "left"}

T = 0.05  # board thickness, top at z = T


def shingle(k, n, start, step, r, t, tilt, skin, flesh, inset):
    """A row of round slices, each leaning on the one before, lower edge on the board."""
    a = math.radians(tilt)
    heading = math.degrees(math.atan2(step[1], step[0]))
    for i in range(n):
        x, y = start[0] + i * step[0], start[1] + i * step[1]
        z = T + r * math.sin(a) * 0.85 + t / 2 * math.cos(a) + i * 0.004
        k.cyl(r, t, at=(x, y, z), rot=(0, -tilt, heading), m=skin, bevel=0.004)
        if flesh is not None:
            nx = math.sin(-a) * math.cos(math.radians(heading))
            ny = math.sin(-a) * math.sin(math.radians(heading))
            nz = math.cos(a)
            d = t / 2 + 0.002
            k.cyl(r - inset, 0.004, at=(x + nx * d, y + ny * d, z + nz * d), rot=(0, -tilt, heading),
                  m=flesh, bevel=0.001)


def build(k):
    wood = k.mat("#a8683a", "matte")
    W, D = 1.0, 0.62
    hx, hole = 0.38, 0.06  # hole center x, hole radius

    # One-piece board: a flat ring from the hole out past the far corners, clamped to the rectangle.
    R = 1.1
    board = k.lathe([(hole, 0.0), (R, 0.0), (R, T), (hole, T), (hole, 0.0)], at=(hx, 0, 0), rot=(0, 0, 0),
                    m=wood, verts=160)
    x0, x1, y0 = -W / 2 - hx, W / 2 - hx, D / 2
    k.warp(board, lambda p: (max(x0, min(x1, p[0])), max(-y0, min(y0, p[1])), p[2]))

    # Tomato slices: red skin, lighter red flesh face.
    shingle(k, 5, (-0.36, 0.14), (0.075, 0.0), 0.075, 0.018, 14,
            k.mat("#e0281e", "gloss"), k.mat("#f0533e", "gloss"), 0.008)
    # Cucumber rounds: dark green rind, pale green flesh face.
    shingle(k, 6, (-0.36, -0.15), (0.06, 0.0), 0.05, 0.016, 14,
            k.mat("#2f7d2a", "satin"), k.mat("#b9e07a", "satin"), 0.007)
    # Carrot coins: a shingled row with a small stack right at its end.
    carrot = k.mat("#f27a1a", "satin")
    shingle(k, 5, (0.08, 0.15), (0.0, -0.06), 0.036, 0.014, 14, carrot, k.mat("#f8a040", "satin"), 0.012)
    for i in range(4):
        k.cyl(0.036, 0.014, at=(0.08 + 0.003 * (i % 2), -0.17, T + 0.007 + i * 0.014), rot=(0, 0, 0),
              m=carrot, bevel=0.004)

    k.turn(0, 0, -18)

    # Blue gingham tablecloth filling the card.
    k.box((8, 8, 0.02), at=(0, 0, -0.01), m=k.mat("#5b9be0", "matte"), bevel=0, setting=True)
