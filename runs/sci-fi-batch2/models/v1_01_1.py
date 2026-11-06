# Flying saucer: one round hull turned on a lathe, a shallow lens with its upper and lower shells meeting at a flat
# disc rim. Eight yellow lights sit evenly around the rim's outer edge. A clear pale-green dome sits on a collar
# ring at the top of the hull. Three legs splay out from a mount plate on the underside, each ending in a small
# round foot that shows below the rim. It floats in an empty sky, tilted a little so the top and the dome show.
import math

SCENE = {"category": "1", "backdrop": "#3fa9ec", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c8cdd4", "metal")
    grey = k.mat("#7d848e", "metal")
    dome = k.mat("#d4ffe0", "glass")
    light = k.mat("#ffd23a", "glow")

    # Hull: lower and upper shells in one profile, bottom to top.
    hull = [(0.0, -0.10), (0.12, -0.10), (0.20, -0.093), (0.28, -0.078), (0.35, -0.060), (0.41, -0.042),
            (0.45, -0.028), (0.47, -0.018), (0.47, 0.018), (0.45, 0.030), (0.41, 0.046), (0.35, 0.066),
            (0.29, 0.084), (0.23, 0.098), (0.20, 0.104), (0.0, 0.104)]
    k.lathe(hull, at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # Flat disc rim around the widest point.
    k.cyl(0.52, 0.036, at=(0, 0, 0), rot=(0, 0, 0), m=grey, bevel=0.01)

    # Eight lights set into the rim's outer edge.
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        k.sphere(0.028, at=(0.52 * math.cos(a), 0.52 * math.sin(a), 0.0), m=light)

    # Dome on a collar ring.
    k.torus(0.2, 0.018, at=(0, 0, 0.106), rot=(0, 0, 0), m=grey)
    cap = [(0.2 * math.cos(math.radians(t)), 0.104 + 0.17 * math.sin(math.radians(t))) for t in range(0, 91, 6)]
    cap[-1] = (0.0, cap[-1][1])
    k.lathe(cap, at=(0, 0, 0), rot=(0, 0, 0), m=dome)

    # Small plate at the center of the underside.
    k.cyl(0.09, 0.02, at=(0, 0, -0.105), rot=(0, 0, 0), m=grey, bevel=0.006)

    # Three legs splaying out from the underside, two toward the camera, each with a round foot.
    for i in range(3):
        a = math.radians(i * 120 + 90)
        c, s = math.cos(a), math.sin(a)
        k.tube([(0.2 * c, 0.2 * s, -0.085), (0.31 * c, 0.31 * s, -0.25)], 0.02, grey)
        k.sphere(0.042, at=(0.315 * c, 0.315 * s, -0.265), scale=(1, 1, 0.8), m=silver)

    k.turn(5, -7, 0)
