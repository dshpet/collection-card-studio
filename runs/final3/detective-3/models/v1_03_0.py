# Magnifier: a round silver rim holds a slightly convex clear lens; a short silver collar at the rim's lower-right
# edge joins it to a glossy red handle that runs down and away at 45 degrees, ending in a rounded cap. A curved
# white glint sits on the lens front. Floating, tilted so the lens face shows with a bit of the rim's depth.
import math

SCENE = {"category": "1", "backdrop": "#5cc24a", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#d3d8df", "metal")
    glass = k.mat("#dff3ff", "glass")
    red = k.mat("#e3262e", "gloss")
    white = k.mat("#ffffff", "glow")

    c = (0.0, 0.0, 0.62)          # lens center; lens faces -y
    R = 0.30                      # lens radius

    # Lens: a thin convex disc inside the rim
    k.sphere(R + 0.005, at=c, scale=(1, 0.1, 1), m=glass)
    # Rim: a thick ring plus a short band giving it depth
    k.torus(R + 0.012, 0.035, at=c, rot=(90, 0, 0), m=silver)
    k.lathe([(R - 0.005, -0.04), (R + 0.035, -0.04), (R + 0.035, 0.04), (R - 0.005, 0.04)],
            at=c, rot=(90, 0, 0), m=silver)

    # Handle axis: down and to the right from the rim at 45 degrees
    a = math.radians(45)
    d = (math.sin(a), 0.0, -math.cos(a))
    rot = (0, 135, 0)             # maps local +z onto d

    def p(t):
        return (c[0] + d[0] * t, c[1], c[2] + d[2] * t)

    # Collar joining rim and handle
    k.lathe([(0.0, 0.0), (0.038, 0.0), (0.042, 0.03), (0.048, 0.07), (0.055, 0.10),
             (0.055, 0.115), (0.0, 0.115)], at=p(R + 0.02), rot=rot, m=silver)
    # Red handle: slight swell, rounded end
    prof = [(0.0, 0.0), (0.05, 0.0), (0.056, 0.02), (0.062, 0.12), (0.066, 0.26),
            (0.064, 0.38), (0.058, 0.44)]
    for i in range(1, 9):
        t = i / 8 * math.pi / 2
        prof.append((0.058 * math.cos(t), 0.44 + 0.04 * math.sin(t)))
    k.lathe(prof, at=p(R + 0.13), rot=rot, m=red)

    # White glint: a curved streak on the upper-left of the lens front
    pts = []
    for j in range(7):
        t = math.radians(115 + j * 8)
        rr = R * 0.72
        pts.append((c[0] + rr * math.cos(t), c[1] - 0.034, c[2] + rr * math.sin(t)))
    k.tube(pts, 0.016, white, curved=True)
    k.sphere(0.018, at=(c[0] - 0.09, c[1] - 0.032, c[2] + 0.06), m=white)

    k.turn(0, -8, -18)
