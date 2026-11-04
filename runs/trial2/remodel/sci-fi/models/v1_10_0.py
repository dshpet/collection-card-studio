# Moon base: a glass dome on a low white ring wall that stands on the ground, with white ribs over the glass.
# A round tunnel runs from the dome's wall to a raised airlock on four legs; the yellow door is in the airlock's
# front above a small sill, and a short ladder leans from the ground up to that sill. A crater lies beside the base.
import math

SCENE = {"category": "4", "backdrop": "#7b4fe6", "azimuth": 30, "elevation": 12, "lens": 55, "light": "left"}


def build(k):
    white = k.mat("#f4f5f8", "satin")
    glass = k.mat("#9fdcff", "glass")
    gray = k.mat("#a9adb6", "metal")
    door = k.mat("#ffcc2a", "satin")

    # Dome: ring wall on the ground, glass hemisphere on it, ribs, a ring band and a top hatch.
    cx, cy, R, wall = 0.15, 0.15, 0.42, 0.18
    k.lathe([(0, 0), (R + 0.03, 0), (R + 0.03, wall), (R - 0.01, wall + 0.01), (0, wall + 0.01)],
            at=(cx, cy, 0), m=white)
    dome = [(R * math.cos(math.radians(a)), wall + R * math.sin(math.radians(a))) for a in range(0, 90, 5)]
    k.lathe(dome + [(0, wall + R)], at=(cx, cy, 0), m=glass)
    for i in range(6):
        h = math.radians(i * 60 + 15)
        pts = [(cx + (R + 0.008) * math.cos(math.radians(a)) * math.cos(h),
                cy + (R + 0.008) * math.cos(math.radians(a)) * math.sin(h),
                wall + (R + 0.008) * math.sin(math.radians(a))) for a in range(0, 81, 10)]
        k.tube(pts, 0.014, white, curved=True)
    k.torus(R * math.cos(math.radians(40)) + 0.006, 0.013,
            at=(cx, cy, wall + R * math.sin(math.radians(40))), m=white)
    k.cyl(0.08, 0.04, at=(cx, cy, wall + R), m=white, bevel=0.01)

    # Tunnel from the dome wall to the airlock, with rib rings and two feet on the ground.
    tz, tr = 0.2, 0.085
    k.cyl(tr, 0.42, at=(-0.42, 0, tz), rot=(0, 90, 0), m=white, bevel=0.01)
    for x in (-0.33, -0.45, -0.57):
        k.torus(tr + 0.004, 0.012, at=(x, 0, tz), rot=(0, 90, 0), m=gray)
    for x in (-0.38, -0.52):
        k.box((0.05, 0.1, tz - tr + 0.01), at=(x, 0, (tz - tr) / 2), m=gray, bevel=0.005)

    # Airlock on four legs with foot pads, and a rounded top.
    ax, ar, ab, ah = -0.72, 0.16, 0.1, 0.3
    k.cyl(ar, ah, at=(ax, 0, ab + ah / 2), m=white, bevel=0.015)
    cap = [(ar * math.cos(math.radians(a)), ab + ah + 0.6 * ar * math.sin(math.radians(a))) for a in range(0, 90, 10)]
    k.lathe(cap + [(0, ab + ah + 0.6 * ar)], at=(ax, 0, 0), m=white)
    k.cyl(ar + 0.01, 0.02, at=(ax, 0, ab + 0.01), m=gray)
    for a in (45, 135, 225, 315):
        x, y = ax + 0.11 * math.cos(math.radians(a)), 0.11 * math.sin(math.radians(a))
        k.cyl(0.016, ab, at=(x, y, ab / 2), m=gray)
        k.cyl(0.03, 0.012, at=(x, y, 0.006), m=gray)

    # Yellow door in the airlock front, a sill under it, and a short ladder from the ground to the sill.
    k.box((0.12, 0.04, 0.2), at=(ax, -ar + 0.005, ab + 0.12), m=door, bevel=0.012)
    k.box((0.16, 0.08, 0.016), at=(ax, -ar - 0.02, ab + 0.012), m=gray, bevel=0.004)
    top_y, bot_y, top_z = -ar - 0.05, -ar - 0.16, ab + 0.02
    for dx in (-0.05, 0.05):
        k.tube([(ax + dx, bot_y, 0.0), (ax + dx, top_y, top_z + 0.04)], 0.009, gray)
    for t in (0.3, 0.65):
        y, z = bot_y + (top_y - bot_y) * t, (top_z + 0.04) * t
        k.tube([(ax - 0.05, y, z), (ax + 0.05, y, z)], 0.008, gray)

    # Setting: gray moon ground, a crater with a raised rim beside the base, soft hills far back.
    k.floor("#9a9aa6", "matte")
    rim = [(0.0, 0.004), (0.2, 0.007), (0.26, 0.03), (0.3, 0.055), (0.34, 0.05), (0.42, 0.015), (0.5, 0.0)]
    k.lathe(rim, at=(0.85, -0.5, 0.0), m=k.mat("#83838f", "matte"), setting=True)
    for x, y, r in ((-2.5, 5.0, 2.2), (2.0, 6.0, 2.8)):
        k.sphere(r, at=(x, y, -r * 0.75), scale=(1.4, 1, 1), m=k.mat("#858597", "matte"), setting=True)
