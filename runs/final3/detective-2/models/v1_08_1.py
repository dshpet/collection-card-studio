# Doorknob print: a brass backplate is fixed to the front of a forest green panelled door near its latch edge;
# the round brass knob turns on a neck that rises from a collar on the plate, with a keyhole below it. A dusted
# grey fingerprint, a set of fine nested ridge loops open at the bottom, lies on the knob's front face. The
# setting is a few metres of the hallway: the door with its raised panels, the casing that frames its edge and
# the warm wall beside it. The framing holds the plate and knob.
import math

SCENE = {"category": "4", "backdrop": "#f6c94a", "azimuth": 25, "elevation": 10, "lens": 70, "light": "left"}


def build(k):
    brass = k.mat("#d9a63c", "metal")
    dark = k.mat("#3a2a14", "matte")
    powder = k.mat("#7f8389", "matte")
    door = k.mat("#2f6b3a", "satin")
    casing = k.mat("#f3ead6", "satin")
    wall = k.mat("#f2cf7a", "matte")

    x0, zk = 0.0, 0.62
    # backplate on the door face (door face at y = 0)
    k.box((0.24, 0.025, 0.62), at=(x0, -0.0125, 0.55), m=brass, bevel=0.012)
    k.box((0.2, 0.01, 0.58), at=(x0, -0.03, 0.55), m=brass, bevel=0.006)
    # keyhole cut into the plate
    k.cyl(0.022, 0.008, at=(x0, -0.034, 0.38), rot=(90, 0, 0), m=dark)
    k.box((0.022, 0.008, 0.05), at=(x0, -0.034, 0.35), m=dark, bevel=0.003)

    # knob: collar, neck and ball as one smooth turned piece along -y
    R, c = 0.12, 0.25
    prof = [(0.0, 0.0), (0.085, 0.0), (0.09, 0.012), (0.085, 0.025), (0.065, 0.04), (0.048, 0.06),
            (0.042, 0.09), (0.042, 0.12)]
    steps = 120
    for i in range(steps + 1):
        a = math.radians(-70 + i * 160 / steps)
        prof.append((max(R * math.cos(a), 0.0), c + R * math.sin(a)))
    prof[-1] = (0.0, c + R)
    k.lathe(prof, at=(x0, -0.035, zk), rot=(90, 0, 0), m=brass, verts=160)

    # grey powder fingerprint: nested ridge loops, open at the bottom, lying on the ball's front face
    cy = -0.035 - c
    cu, cw = 0.012, 0.012

    def on_ball(u, w):
        d = R * R - u * u - w * w
        return (x0 + u, cy - math.sqrt(max(d, 0.0)) - 0.0008, zk + w)

    for j in range(6):
        a = 0.008 + 0.0085 * j
        pts = []
        for i in range(31):
            ang = math.radians(-50 + i * 280 / 30)
            pts.append((cu + a * math.cos(ang), cw + 1.3 * a * math.sin(ang)))
        # legs run down and spread off the bottom of the pad
        lo = pts[0]
        hi = pts[-1]
        legs_r = [(lo[0] + 0.004, lo[1] - 0.012 - 0.002 * j), (lo[0] + 0.008, lo[1] - 0.024 - 0.003 * j)]
        legs_l = [(hi[0] - 0.004, hi[1] - 0.012 - 0.002 * j), (hi[0] - 0.008, hi[1] - 0.024 - 0.003 * j)]
        line = list(reversed(legs_r)) + pts + legs_l
        k.tube([on_ball(u, w) for u, w in line], 0.0028, powder, curved=True)

    # setting: the door with raised panels, its casing over the latch edge and the hallway wall
    k.box((1.5, 0.05, 2.4), at=(-0.55, 0.025, 0.6), m=door, bevel=0.01, setting=True)
    for zc, h in ((1.35, 0.75), (-0.15, 0.75)):
        k.box((0.75, 0.03, h), at=(-0.65, -0.01, zc), m=door, bevel=0.02, setting=True)
    k.box((0.16, 0.08, 2.4), at=(0.27, 0.0, 0.6), m=casing, bevel=0.015, setting=True)
    k.box((2.0, 0.05, 2.4), at=(1.33, 0.07, 0.6), m=wall, bevel=0.0, setting=True)
