# Haunted house: a tall two-storey mansion that leans a little to the right, with a steep gable roof on an attic
# wedge, a round tower on the left with a pointed cone roof, a front door on a stone step, four lit windows
# (two upstairs, one beside the door, one in the tower) and a brick chimney rising through the back roof slope.
# It stands on the crown of a grassy hill, with a second softer hill far behind.
import math

SCENE = {"category": "4", "backdrop": "#3fa4ec", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}

H = 0.6          # wall height, from z = -0.05 to 0.55
LEAN = 0.06      # how far the top of the walls leans right


def lean(z):
    return LEAN * (z + 0.05) / H


def build(k):
    wall = k.mat("#8a7f9e", "matte")
    stone = k.mat("#5b5466", "matte")
    roof = k.mat("#2e2838", "satin")
    trim = k.mat("#3b2f45", "satin")
    door_m = k.mat("#4a3328", "matte")
    glow = k.mat("#ffd84a", "glow")
    brick = k.mat("#6b4a52", "matte")

    # Main body, sheared so it leans to the right.
    body = k.box((0.6, 0.4, H), at=(0.15, 0, 0.25), m=wall, bevel=0)
    k.warp(body, lambda p: (p[0] + LEAN * (p[2] + H / 2) / H, p[1], p[2]))
    k.box((0.64, 0.44, 0.07), at=(0.15, 0, -0.015), m=stone, bevel=0.01)

    # Attic wedge (gable ends) and the two steep roof slabs, ridge along x.
    rise, half = 0.35, 0.2
    attic = k.box((0.6, 0.4, rise), at=(0.15 + LEAN, 0, 0.55 + rise / 2), m=wall, bevel=0)
    k.warp(attic, lambda p: (p[0], p[1] * (0.5 - p[2] / rise), p[2]))
    th = math.degrees(math.atan2(rise, half))
    for s in (-1, 1):
        k.box((0.72, 0.46, 0.03), at=(0.15 + LEAN, s * 0.128, 0.706), rot=(-s * th, 0, 0), m=roof, bevel=0.006)
    k.cyl(0.022, 0.74, at=(0.15 + LEAN, 0, 0.91), rot=(0, 90, 0), m=trim)

    # Chimney through the back slope, poking above the ridge.
    cx = 0.36 + LEAN
    k.box((0.09, 0.09, 0.32), at=(cx, 0.09, 0.86), m=brick, bevel=0.006)
    k.box((0.12, 0.12, 0.03), at=(cx, 0.09, 1.03), m=stone, bevel=0.005)

    # Round tower on the left, slightly taller, with a pointed roof and a finial.
    tx, ty, tr = -0.24, -0.04, 0.15
    k.cyl(tr, 0.95, at=(tx, ty, 0.425), m=wall, bevel=0.008)
    k.cyl(tr + 0.02, 0.07, at=(tx, ty, -0.015), m=stone, bevel=0.01)
    k.cyl(tr + 0.025, 0.04, at=(tx, ty, 0.91), m=trim, bevel=0.008)
    k.cone(tr + 0.05, 0.0, 0.48, at=(tx, ty, 1.17), m=roof)
    k.sphere(0.025, at=(tx, ty, 1.42), m=trim)

    # Front door with an arched top in an arched frame, on a stone step. Each arch disc sits a little behind
    # its box's front face so the box covers the disc's lower half without z-fighting.
    dx = 0.13 + lean(0.1)
    k.box((0.24, 0.12, 0.05), at=(dx, -0.25, -0.025), m=stone, bevel=0.008)
    k.box((0.17, 0.02, 0.19), at=(dx, -0.205, 0.095), m=trim, bevel=0.004)
    k.cyl(0.085, 0.016, at=(dx, -0.204, 0.19), rot=(90, 0, 0), m=trim, bevel=0.003)
    k.box((0.13, 0.02, 0.18), at=(dx, -0.212, 0.09), m=door_m, bevel=0.004)
    k.cyl(0.065, 0.016, at=(dx, -0.211, 0.18), rot=(90, 0, 0), m=door_m, bevel=0.003)
    k.sphere(0.014, at=(dx + 0.04, -0.226, 0.1), m=k.mat("#b89a4a", "metal"))

    # Lit windows on the front face: two upstairs, one beside the door.
    def window(x, z, y=-0.205, w=0.1, h=0.14):
        k.box((w + 0.04, 0.02, h + 0.04), at=(x, y, z), m=trim, bevel=0.004)
        k.box((w, 0.02, h), at=(x, y - 0.007, z), m=glow, bevel=0.003)
        k.box((w + 0.06, 0.04, 0.025), at=(x, y - 0.012, z - h / 2 - 0.025), m=trim, bevel=0.004)

    for x, z in ((0.02, 0.41), (0.32, 0.41), (0.34, 0.15)):
        window(x + lean(z), z)
    # Tower window, on the tower's front.
    window(tx, 0.66, y=ty - tr - 0.002, w=0.08, h=0.13)

    # Grassy hill under the house, a softer hill far behind.
    k.sphere(1, at=(0, 0.4, -0.5), scale=(3.5, 2.5, 0.5), m=k.mat("#5fae3e", "matte"), setting=True)
    k.sphere(1, at=(1.5, 6, -1.2), scale=(5, 3, 1.6), m=k.mat("#7cc35a", "matte"), setting=True)
