# Doorknob print: a round brass knob on a neck stands out from a tall brass back plate that is screwed to a dark
# green painted door. A grey dusted fingerprint swirl lies on the front of the knob ball. The door runs off the
# card, with its raised panels above and below and the white casing and cream hallway wall at the latch edge.
import math

SCENE = {"category": "4", "backdrop": "#f6c94a", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    brass = k.mat("#d4a23c", "metal")
    powder = k.mat("#9a9da3", "matte")
    door = k.mat("#1f5a3c", "satin")
    casing = k.mat("#f4efe4", "satin")
    wall = k.mat("#f1d9a8", "matte")

    zc = 1.0
    # back plate on the door face (door face is y = 0)
    k.box((0.34, 0.03, 1.0), at=(0, -0.015, zc), m=brass, bevel=0.012)
    for z in (zc + 0.4, zc - 0.4):
        k.sphere(0.03, at=(0, -0.03, z), scale=(1, 0.5, 1), m=brass)

    # knob: rose, neck and ball, revolved along -y from the plate
    R, c = 0.2, 0.32
    profile = [(0.0, 0.0), (0.17, 0.0), (0.17, 0.02), (0.14, 0.05), (0.09, 0.08), (0.065, 0.11)]
    for i in range(25):
        t = math.radians(-69 + i * (159 / 24))
        profile.append((R * math.cos(t), c + R * math.sin(t)))
    profile.append((0.0, c + R))
    k.lathe(profile, at=(0, -0.03, zc), rot=(90, 0, 0), m=brass)

    # dusted fingerprint swirl on the ball's front, lying on its surface
    C = (0.0, -0.03 - c, zc)
    pts = []
    n = 120
    for i in range(n + 1):
        t = i / n * 3 * 2 * math.pi
        a = 0.04 + 0.022 * t
        ax = 0.15 + a * math.cos(t)
        az = 0.12 + 1.25 * a * math.sin(t)
        x, z = math.sin(ax), math.sin(az)
        y = -math.sqrt(max(0.0, 1 - x * x - z * z))
        rr = R + 0.004
        pts.append((C[0] + rr * x, C[1] + rr * y, C[2] + rr * z))
    k.tube(pts, 0.007, powder, curved=True)

    # setting: the door with raised panels, its casing and the hallway wall
    k.box((3.0, 0.08, 4.0), at=(-1.05, 0.04, 1.0), m=door, bevel=0.01, setting=True)
    k.box((1.6, 0.03, 1.2), at=(-1.1, -0.012, 2.2), m=door, bevel=0.015, setting=True)
    k.box((1.6, 0.03, 1.0), at=(-1.1, -0.012, -0.1), m=door, bevel=0.015, setting=True)
    k.box((0.2, 0.12, 4.0), at=(0.57, 0.02, 1.0), m=casing, bevel=0.015, setting=True)
    k.box((2.4, 0.2, 4.0), at=(1.87, 0.1, 1.0), m=wall, bevel=0.0, setting=True)
