# Porthole: a thick steel ring frames a round dark blue glass and sits on a raised flange ringed with twelve
# bolts. The flange is set into the curved white wall of a spaceship corridor. The wall bends toward the viewer
# above and below like the inside of a large cylinder. A short bore runs back through the hull to a dark starry
# disc, so the glass looks out into space. A plain floor runs along the foot of the wall.
import math

SCENE = {"category": "4", "backdrop": "#f39ac4", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    steel = k.mat("#c3c8cf", "metal")
    bolt = k.mat("#9aa0a8", "metal")
    glass = k.mat("#1d3f8f", "glass")
    space = k.mat("#0d1640", "matte")
    star = k.mat("#fff6d8", "glow")
    wall = k.mat("#f4f5f7", "satin")
    floor = k.mat("#b9bec6", "satin")

    cz = 0.6                      # porthole centre height; the front faces -y
    face = (90, 0, 0)             # local z of lathes and cylinders points at the viewer (-y)

    # raised flange where the porthole meets the wall, sunk a little into it
    k.lathe([(0.30, -0.1), (0.47, -0.1), (0.47, 0.06), (0.465, 0.075), (0.45, 0.088), (0.43, 0.09),
             (0.30, 0.09)], at=(0, 0, cz), rot=face, m=steel)
    # thick round rim
    k.torus(0.31, 0.065, at=(0, -0.11, cz), rot=face, m=steel)
    # bolts around the flange
    for i in range(12):
        a = math.radians(i * 30 + 15)
        k.cyl(0.024, 0.03, at=(0.405 * math.cos(a), -0.1, cz + 0.405 * math.sin(a)), rot=face, m=bolt,
              bevel=0.006, verts=6)
    # bore through the hull, open at both ends
    k.lathe([(0.255, 0.0), (0.255, 0.35)], at=(0, 0.3, cz), rot=face, m=steel)
    # glass pane inside the rim
    k.cyl(0.262, 0.014, at=(0, -0.085, cz), rot=face, m=glass, bevel=0.003)
    # dark starry view at the back of the bore
    k.cyl(0.26, 0.01, at=(0, 0.3, cz), rot=face, m=space, bevel=0)
    for x, z, r in ((-0.12, 0.10, 0.009), (0.08, 0.15, 0.007), (0.15, -0.05, 0.01), (-0.05, -0.14, 0.007),
                    (0.02, 0.02, 0.006), (-0.17, -0.03, 0.006), (0.11, -0.16, 0.006), (-0.06, 0.19, 0.005)):
        k.sphere(r, at=(x, 0.29, cz + z), m=star)

    # curved corridor wall: panels on a cylinder of radius R whose axis runs along x in front of the porthole
    R, ds = 2.5, 0.1
    n = 18
    for i in range(n):
        t = -0.25 + (i + 0.5) * ds / R
        y = -R + R * math.cos(t)
        z = cz + R * math.sin(t)
        k.box((4.0, 0.05, ds * 1.02), at=(0, y + 0.025 * math.cos(t), z + 0.025 * math.sin(t)),
              rot=(math.degrees(t), 0, 0), m=wall, bevel=0.006, setting=True)
    # corridor floor at the foot of the wall
    k.box((4.0, 3.0, 0.1), at=(0, -1.4, -0.05), m=floor, bevel=0.01, setting=True)
