# Magnifier: a slim round silver rim holds a slightly domed, pale blue clear lens; a short silver collar at the
# rim's lower-right edge joins it to a glossy red handle that runs down and away at 45 degrees and ends in a
# rounded cap. A bold curved white glint sits on the lens front. Floating, tilted so the lens face shows with a
# little of the rim's depth.
import math

SCENE = {"category": "1", "backdrop": "#5cc24a", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#e2e6ec", "metal")
    glass = k.mat("#bfe6ff", "glass")
    red = k.mat("#e3262e", "gloss")
    white = k.mat("#ffffff", "glow")

    c = (0.0, 0.0, 0.62)          # lens center; lens faces -y
    R = 0.30                      # lens radius

    # Lens: a domed clear disc seated in the rim (bulges a little front and back)
    k.sphere(R + 0.01, at=c, scale=(1, 0.12, 1), m=glass)
    # Rim: one slim round ring around the lens edge
    k.torus(R + 0.02, 0.034, at=c, rot=(90, 0, 0), m=silver)

    # Handle axis: down and to the right from the rim at 45 degrees
    a = math.radians(45)
    d = (math.sin(a), 0.0, -math.cos(a))
    rot = (0, 135, 0)             # maps local +z onto d

    def p(t):
        return (c[0] + d[0] * t, c[1], c[2] + d[2] * t)

    # Collar joining rim and handle (starts inside the rim tube)
    k.lathe([(0.0, 0.0), (0.034, 0.0), (0.038, 0.03), (0.046, 0.07), (0.055, 0.10),
             (0.055, 0.115), (0.0, 0.115)], at=p(R + 0.03), rot=rot, m=silver)
    # Red handle: slight swell, rounded end
    prof = [(0.0, 0.0), (0.05, 0.0), (0.056, 0.02), (0.062, 0.12), (0.066, 0.26),
            (0.064, 0.38), (0.058, 0.44)]
    for i in range(1, 9):
        t = i / 8 * math.pi / 2
        prof.append((0.058 * math.cos(t), 0.44 + 0.04 * math.sin(t)))
    k.lathe(prof, at=p(R + 0.14), rot=rot, m=red)

    # White glint: a bold curved streak on the upper-left of the lens front, plus a round highlight
    pts = []
    for j in range(9):
        t = math.radians(100 + j * 8)
        rr = R * 0.72
        pts.append((c[0] + rr * math.cos(t), c[1] - 0.03, c[2] + rr * math.sin(t)))
    k.tube(pts, 0.022, white, curved=True)
    k.sphere(0.028, at=(c[0] - 0.10, c[1] - 0.032, c[2] + 0.07), m=white)

    k.turn(0, -8, -18)
