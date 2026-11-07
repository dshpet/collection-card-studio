# Haunted house: a tall narrow two-storey mansion with a steep front gable. Two roof slabs meet on a ridge over
# a gable wall; a round turret with a cone roof stands at the front-left corner; a crooked chimney rises out of
# the right roof slope. The front door sits on a stone step under an arched head, and the windows glow yellow.
# The house stands on a short-grass lawn.
import math

SCENE = {"category": "4", "backdrop": "#1f3aa0", "azimuth": 28, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    wall = k.mat("#8c9096", "matte")
    trim = k.mat("#4d5258", "matte")
    slate = k.mat("#353a48", "matte")
    glow = k.mat("#ffd23a", "glow")
    door_m = k.mat("#4a3426", "matte")
    brick = k.mat("#5c5f66", "matte")

    W, D, H = 0.5, 0.4, 0.75          # main body width (x), depth (y), wall height
    front = -D / 2

    # Main body and stone plinth
    k.box((W, D, H), at=(0, 0, H / 2), m=wall, bevel=0.006)
    k.box((W + 0.04, D + 0.04, 0.06), at=(0, 0, 0.03), m=trim, bevel=0.008)
    k.box((W + 0.03, D + 0.03, 0.03), at=(0, 0, H - 0.015), m=trim, bevel=0.005)

    # Gable wall: a box whose top corners pull in to the ridge line
    gable_h = 0.3
    g = k.box((W, D, gable_h), at=(0, 0, H + gable_h / 2), m=wall, bevel=0)
    k.warp(g, lambda p: (0.0 if p[2] > 0 else p[0], p[1], p[2]))

    # Roof slabs on the two slopes, meeting at the ridge
    ang = math.degrees(math.atan2(gable_h, W / 2))
    run = math.hypot(W / 2, gable_h) + 0.08
    t = 0.04
    for s in (-1, 1):
        a = math.radians(ang)
        cx = s * (W / 4 + 0.03 * math.cos(a)) + s * math.sin(a) * t / 2
        cz = H + gable_h / 2 - 0.03 * math.sin(a) + math.cos(a) * t / 2
        k.box((run, D + 0.1, t), at=(cx, 0, cz), rot=(0, s * ang, 0), m=slate, bevel=0.006)
    k.cyl(0.018, D + 0.1, at=(0, 0, H + gable_h + 0.02), rot=(90, 0, 0), m=slate)

    # Crooked chimney out of the right slope, leaning, with a cap
    k.box((0.08, 0.08, 0.34), at=(0.15, 0.08, 1.04), rot=(0, 9, 4), m=brick, bevel=0.005)
    k.box((0.11, 0.11, 0.035), at=(0.177, 0.082, 1.215), rot=(0, 9, 4), m=trim, bevel=0.005)

    # Round turret at the front-left corner with a cone roof
    tx, ty, tr, th = -0.25, -0.2, 0.12, 0.98
    k.cyl(tr, th, at=(tx, ty, th / 2), m=wall, bevel=0.006)
    k.cyl(tr + 0.015, 0.06, at=(tx, ty, 0.03), m=trim)
    k.cyl(tr + 0.02, 0.03, at=(tx, ty, th + 0.015), m=trim)
    k.cone(tr + 0.045, 0.0, 0.44, at=(tx, ty, th + 0.03 + 0.22), m=slate)
    k.cyl(0.008, 0.08, at=(tx, ty, th + 0.03 + 0.44 + 0.03), m=trim)

    # Turret windows facing front
    for z in (0.36, 0.7):
        k.box((0.075, 0.03, 0.15), at=(tx, ty - tr + 0.005, z), m=trim, bevel=0.004)
        k.box((0.055, 0.03, 0.12), at=(tx, ty - tr - 0.002, z), m=glow, bevel=0.003)

    # Front door on a stone step, arched head: each arch disc shares its box's front plane so they read as one
    dx = 0.03
    k.box((0.22, 0.1, 0.06), at=(dx, front - 0.05, 0.03), m=trim, bevel=0.008)
    k.box((0.15, 0.03, 0.25), at=(dx, front - 0.005, 0.185), m=trim, bevel=0.001)
    k.cyl(0.075, 0.03, at=(dx, front - 0.006, 0.31), rot=(90, 0, 0), m=trim, bevel=0.001)
    k.box((0.12, 0.03, 0.23), at=(dx, front - 0.016, 0.175), m=door_m, bevel=0.001)
    k.cyl(0.06, 0.03, at=(dx, front - 0.017, 0.29), rot=(90, 0, 0), m=door_m, bevel=0.001)
    k.sphere(0.012, at=(dx + 0.04, front - 0.036, 0.18), m=k.mat("#b08a3a", "metal"))

    # Front windows: one beside the door, two upstairs, a round one in the gable
    def front_window(x, z, w=0.09, h=0.14):
        k.box((w + 0.025, 0.03, h + 0.025), at=(x, front - 0.004, z), m=trim, bevel=0.004)
        k.box((w, 0.03, h), at=(x, front - 0.01, z), m=glow, bevel=0.003)
        k.box((w + 0.04, 0.045, 0.02), at=(x, front - 0.018, z - h / 2 - 0.02), m=trim, bevel=0.004)

    front_window(0.18, 0.22)
    front_window(-0.05, 0.53)
    front_window(0.16, 0.53)
    k.cyl(0.058, 0.03, at=(0, front - 0.004, 0.88), rot=(90, 0, 0), m=trim)
    k.cyl(0.045, 0.03, at=(0, front - 0.01, 0.88), rot=(90, 0, 0), m=glow)

    # Side windows on the right wall
    for y in (-0.07, 0.11):
        for z in (0.22, 0.53):
            k.box((0.03, 0.115, 0.165), at=(W / 2 + 0.004, y, z), m=trim, bevel=0.004)
            k.box((0.03, 0.09, 0.14), at=(W / 2 + 0.01, y, z), m=glow, bevel=0.003)

    # Lawn of short grass
    k.floor("#3e7a34", "matte")
