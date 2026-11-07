# Magnifying glass: a round silver rim holds a clear glass lens. A short silver collar at the rim's lower edge
# joins it to the glossy red handle, which runs straight down and ends in a rounded knob. A small white glint
# arc sits on the front of the lens. It floats, tilted so the handle points to the lower right and the rim's
# thickness shows.
import math

SCENE = {"category": "1", "backdrop": "#5cc45a", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#d3d8de", "metal")
    glass = k.mat("#dff4ff", "glass")
    red = k.mat("#e3262e", "gloss")
    white = k.mat("#ffffff", "glow")

    cz, R = 0.62, 0.30
    # rim and lens, in the xz plane facing -y
    k.torus(R, 0.038, at=(0, 0, cz), rot=(90, 0, 0), m=silver)
    k.cyl(R + 0.004, 0.06, at=(0, 0, cz), rot=(90, 0, 0), m=silver, bevel=0.01)  # rim band
    k.cyl(R - 0.01, 0.035, at=(0, 0, cz), rot=(90, 0, 0), m=glass, bevel=0.012)

    # glint: a short white arc on the upper left of the lens front
    arc = [math.radians(a) for a in range(125, 166, 8)]
    pts = [(0.2 * math.cos(a), -0.022, cz + 0.2 * math.sin(a)) for a in arc]
    k.tube(pts, 0.014, white, curved=True)

    # collar joining the rim's lower edge (z = 0.282) to the handle
    k.lathe([(0.0, 0.19), (0.05, 0.19), (0.055, 0.21), (0.045, 0.25), (0.036, 0.29), (0.0, 0.29)],
            at=(0, 0, 0), m=silver)
    # red handle with a rounded end
    k.lathe([(0.0, -0.33), (0.03, -0.325), (0.05, -0.31), (0.06, -0.28), (0.062, -0.2),
             (0.058, -0.05), (0.052, 0.08), (0.05, 0.16), (0.053, 0.185), (0.05, 0.2), (0.0, 0.2)],
            at=(0, 0, 0), m=red)

    k.turn(8, -35, 22)
