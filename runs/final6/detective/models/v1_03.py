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
    # Red handle, sturdy, slight swell, rounded end. Fix round 2 ("elongated", 0.48 long and 0.066 thick) made it
    # 0.30; round 3 ("Too large the glass is, and the handle is too small"): 0.40 long and 0.076 thick, about 0.85
    # of the lens's width from the rim, as on the real Map card, and framed at 0.9 so the glass is smaller
    prof = [(0.0, 0.0), (0.062, 0.0), (0.068, 0.02), (0.074, 0.12), (0.076, 0.24),
            (0.073, 0.33), (0.066, 0.37)]
    for i in range(1, 9):
        t = i / 8 * math.pi / 2
        prof.append((0.066 * math.cos(t), 0.37 + 0.045 * math.sin(t)))
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
