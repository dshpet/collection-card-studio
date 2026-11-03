# Moon base: a glass dome sits on a white round base wall whose top is a ledge; white ribs run over the glass
# from the base ring to a top cap. A round tunnel runs out of the base wall toward the front-left on two feet
# and ends in a collar with a small yellow door. A small ladder leans from the ground up onto the ledge. A
# shallow crater with a raised rim lies beside the base, behind and to the right, with low hills far back.
import math

SCENE = {"category": "4", "backdrop": "#7b4fe0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f6fa", "satin")
    glass = k.mat("#a9e2ff", "glass")
    trim = k.mat("#c9ced6", "metal")
    door = k.mat("#ffcf2e", "satin")
    cx, cy = 0.05, 0.12

    # Base wall with a ledge on top, and the glass dome set inside it.
    k.cyl(0.44, 0.2, at=(cx, cy, 0.1), m=white, bevel=0.01)
    k.cyl(0.47, 0.03, at=(cx, cy, 0.215), m=white, bevel=0.008)
    R, z0 = 0.37, 0.23
    profile = [(R * math.cos(math.radians(a)), z0 + R * math.sin(math.radians(a))) for a in range(0, 91, 5)]
    profile[-1] = (0, z0 + R)
    k.lathe(profile, at=(cx, cy, 0), m=glass)
    k.torus(R, 0.02, at=(cx, cy, z0 + 0.005), m=white)
    for i in range(6):
        yaw = math.radians(i * 30)
        arc = []
        for a in range(-90, 91, 10):
            t = math.radians(a)
            r = R * math.cos(t)
            arc.append((cx + r * math.cos(yaw) * (1 if a >= 0 else -1),
                        cy + r * math.sin(yaw) * (1 if a >= 0 else -1),
                        z0 + R * abs(math.sin(t)) + 0.004))
        k.tube(arc, 0.016, white, curved=True)
    k.cyl(0.07, 0.04, at=(cx, cy, z0 + R + 0.005), m=white, bevel=0.01)

    # Tunnel out of the base wall toward the front-left, on two feet, with a yellow door at its end.
    yaw = -20
    dx, dy = -math.sin(math.radians(20)), -math.cos(math.radians(20))
    tr, tz = 0.12, 0.14

    def along(d, z=tz):
        return (cx + dx * d, cy + dy * d, z)

    k.cyl(tr, 0.52, at=along(0.62), rot=(90, 0, yaw), m=white, bevel=0.01)
    for d in (0.55, 0.7):
        k.torus(tr, 0.016, at=along(d), rot=(90, 0, yaw), m=white)
    k.cyl(tr + 0.025, 0.05, at=along(0.87), rot=(90, 0, yaw), m=white, bevel=0.01)
    k.box((0.1, 0.03, 0.15), at=along(0.9, tz - 0.015), rot=(0, 0, yaw), m=door, bevel=0.012)
    k.sphere(0.012, at=along(0.917, tz - 0.015), m=trim)
    for d in (0.55, 0.8):
        k.box((0.16, 0.06, tz - 0.06), at=along(d, (tz - 0.06) / 2), rot=(0, 0, yaw), m=trim, bevel=0.008)

    # Small ladder leaning from the ground onto the ledge top, on the front-right of the base.
    a = math.radians(-50)
    ux, uy = math.cos(a), math.sin(a)
    tx, ty = -uy, ux
    foot, top, ztop = 0.62, 0.45, 0.245
    for s in (-0.055, 0.055):
        k.tube([(cx + ux * foot + tx * s, cy + uy * foot + ty * s, 0.0),
                (cx + ux * top + tx * s, cy + uy * top + ty * s, ztop)], 0.014, trim)
    for i in range(1, 5):
        f = i / 5
        rr, z = foot + (top - foot) * f, ztop * f
        k.tube([(cx + ux * rr - tx * 0.055, cy + uy * rr - ty * 0.055, z),
                (cx + ux * rr + tx * 0.055, cy + uy * rr + ty * 0.055, z)], 0.011, trim)

    # Gray moon ground, a shallow crater with a raised rim beside the base, and low hills far back.
    k.floor("#858796", "matte")
    rim = [(0, 0.004), (0.1, 0.005), (0.14, 0.012), (0.17, 0.028), (0.2, 0.045), (0.23, 0.05), (0.26, 0.032),
           (0.3, 0.01), (0.33, 0.0)]
    k.lathe(rim, at=(0.75, 0.78, 0), m=k.mat("#6f7183", "matte"), setting=True)
    k.cyl(0.13, 0.004, at=(0.75, 0.78, 0.006), m=k.mat("#5c5e70", "matte"), setting=True)
    hill = k.mat("#77798b", "matte")
    k.blob([(-3.5, 8, -1.1, 1.4, (2.2, 1, 1)), (2.5, 9, -1.2, 1.6, (2.4, 1, 1))], hill, setting=True)
