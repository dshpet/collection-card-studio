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
    k.lathe([(0.0, 0.0), (0.036, 0.0), (0.042, 0.03), (0.056, 0.065), (0.066, 0.085),
             (0.066, 0.1), (0.0, 0.1)], at=p(R + 0.03), rot=rot, m=silver)
    # Red handle: short and chunky, slight swell, rounded end. Fix round 2 ("It's kinda elongated"): 0.30 long
    # and 0.08 thick instead of 0.48 and 0.066, so the glass reads as one compact round object
    prof = [(0.0, 0.0), (0.064, 0.0), (0.072, 0.02), (0.08, 0.09), (0.082, 0.16),
            (0.078, 0.22), (0.07, 0.25)]
    for i in range(1, 9):
        t = i / 8 * math.pi / 2
        prof.append((0.07 * math.cos(t), 0.25 + 0.05 * math.sin(t)))
    k.lathe(prof, at=p(R + 0.12), rot=rot, m=red)

    # White glint: a bold curved streak on the upper-left of the lens front, plus a round highlight
    pts = []
    for j in range(9):
        t = math.radians(100 + j * 8)
        rr = R * 0.72
        pts.append((c[0] + rr * math.cos(t), c[1] - 0.03, c[2] + rr * math.sin(t)))
    k.tube(pts, 0.022, white, curved=True)
    k.sphere(0.028, at=(c[0] - 0.10, c[1] - 0.032, c[2] + 0.07), m=white)

    # Fix round, 2026-11-08 ("Perspective looks a bit off"): the lens faces the camera, 12 degrees off, not 46
    k.turn(4, -8, 16)
