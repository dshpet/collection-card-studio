# Moon base: a low white round wall carries a light blue glass dome, held by eight white ribs that meet at a top
# cap and by one ring halfway up. A round tunnel runs out of the wall below the dome toward the front left on two
# pairs of legs. Its end cap has the small yellow door, and a short ladder leans from the ground up to the door
# sill. A crater with a raised rim lies beside the base in front on the right, on the gray moon ground, with low
# hills far back.
import math

SCENE = {"category": "4", "backdrop": "#7b4fe0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f8", "satin")
    glass = k.mat("#9fdcff", "glass")
    yellow = k.mat("#ffcc2e", "satin")
    steel = k.mat("#b9bfc9", "metal")

    # Base wall, inner floor and glass dome.
    wall_h, R = 0.42, 0.48
    k.cyl(0.5, wall_h, at=(0, 0, wall_h / 2), rot=(0, 0, 0), m=white, bevel=0.02)
    k.torus(0.5, 0.022, at=(0, 0, wall_h), rot=(0, 0, 0), m=white)
    k.cyl(0.47, 0.01, at=(0, 0, wall_h + 0.005), rot=(0, 0, 0), m=k.mat("#e6e8ee", "matte"))
    dome = [(R * math.cos(math.radians(a)), wall_h + R * math.sin(math.radians(a))) for a in range(0, 90, 5)]
    k.lathe(dome + [(0.0, wall_h + R)], at=(0, 0, 0), rot=(0, 0, 0), m=glass)
    rib_r = R + 0.01
    for i in range(8):
        a = math.radians(i * 45 + 10)
        pts = [(rib_r * math.cos(math.radians(p)) * math.cos(a), rib_r * math.cos(math.radians(p)) * math.sin(a),
                wall_h + rib_r * math.sin(math.radians(p))) for p in range(0, 81, 10)]
        k.tube(pts, 0.016, white, curved=True)
    mid = math.radians(45)
    k.torus(rib_r * math.cos(mid), 0.016, at=(0, 0, wall_h + rib_r * math.sin(mid)), rot=(0, 0, 0), m=white)
    k.cyl(0.09, 0.04, at=(0, 0, wall_h + R + 0.005), rot=(0, 0, 0), m=white, bevel=0.012)

    # Tunnel out of the wall toward the front left, below the dome, raised on legs.
    dx, dy = -0.5, -0.866           # tunnel direction
    px, py = 0.866, -0.5            # sideways across the tunnel
    rot = (90, 0, -30)              # local z along the tunnel direction

    def p(d, s, z):
        return (d * dx + s * px, d * dy + s * py, z)

    tz, tr = 0.27, 0.13
    k.cyl(tr, 0.5, at=p(0.62, 0, tz), rot=rot, m=white, bevel=0.01)
    for d in (0.55, 0.75):
        k.torus(tr + 0.005, 0.016, at=p(d, 0, tz), rot=rot, m=white)
    k.cyl(tr + 0.02, 0.04, at=p(0.87, 0, tz), rot=rot, m=white, bevel=0.012)
    k.box((0.14, 0.02, 0.19), at=p(0.895, 0, tz - 0.005), rot=(0, 0, -30), m=yellow, bevel=0.008)
    for d in (0.55, 0.8):
        for s in (-0.08, 0.08):
            k.cyl(0.02, 0.17, at=p(d, s, 0.085), rot=(0, 0, 0), m=steel)
            k.cyl(0.035, 0.015, at=p(d, s, 0.0075), rot=(0, 0, 0), m=steel)

    # Short ladder from the ground up to the door sill.
    sill = tz - 0.1
    for s in (-0.05, 0.05):
        k.tube([p(1.02, s, 0.0), p(0.9, s, sill + 0.02)], 0.013, steel)
    for i in range(1, 4):
        t = i / 4
        d, z = 1.02 - 0.12 * t, (sill + 0.02) * t
        k.tube([p(d, -0.05, z), p(d, 0.05, z)], 0.011, steel)

    # Gray moon ground, a crater beside the base in front on the right, and low hills far back.
    k.floor("#8e909c", "matte")
    rim = [(0.46, 0.0), (0.41, 0.03), (0.36, 0.06), (0.33, 0.07), (0.3, 0.055), (0.26, 0.025), (0.22, 0.012),
           (0.0, 0.012)]
    cx, cy = 0.75, -0.85
    k.lathe(rim, at=(cx, cy, 0), rot=(0, 0, 0), m=k.mat("#83858f", "matte"), setting=True)
    k.cyl(0.23, 0.01, at=(cx, cy, 0.012), rot=(0, 0, 0), m=k.mat("#666874", "matte"), setting=True)
    for x, y, r, h in ((-4.5, 9.0, 3.2, 0.7), (3.5, 11.0, 4.0, 0.9)):
        hill = [(r * math.cos(math.radians(a)), h * math.sin(math.radians(a))) for a in range(0, 90, 10)]
        k.lathe(hill + [(0.0, h)], at=(x, y, 0), rot=(0, 0, 0), m=k.mat("#858793", "matte"), setting=True)
