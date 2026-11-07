# Airlock door: a round steel hatch sits in a thick collar ring that is sunk into the curved white corridor wall.
# Bolts ring the collar's face, the door carries a raised rim, and the orange wheel turns on a hub and shaft
# fixed to the door's center. Two hinge arms on the right join the door to blocks on the collar around one pin.
# The wall is part of the corridor's round cross-section (axis along x), so it bows toward the viewer up top and
# meets a flat corridor floor at the bottom.
import math

SCENE = {"category": "4", "backdrop": "#3f8fe0", "azimuth": 22, "elevation": 9, "lens": 60, "light": "left"}


def build(k):
    wall = k.mat("#f4f5f7", "satin")
    collar = k.mat("#c3c8cf", "metal")
    door = k.mat("#d6dae0", "satin")
    rim = k.mat("#b3b9c2", "metal")
    bolt = k.mat("#8d939c", "metal")
    wheel = k.mat("#ff8a1f", "satin")

    cz = 0.66  # hatch center height

    # Collar ring set into the wall: front face at y = -0.06, back buried behind the wall surface.
    prof = [(0.43, 0.0), (0.6, 0.0), (0.6, 0.07), (0.58, 0.11), (0.45, 0.11), (0.43, 0.09), (0.43, 0.0)]
    k.lathe(prof, at=(0, 0.05, cz), rot=(90, 0, 0), m=collar)
    for i in range(12):
        a = math.radians(i * 30 + 15)
        k.cyl(0.024, 0.03, at=(0.515 * math.cos(a), -0.065, cz + 0.515 * math.sin(a)), rot=(90, 0, 0),
              m=bolt, bevel=0.006, verts=6)

    # Door slab with a thick raised rim.
    k.cyl(0.43, 0.09, at=(0, -0.025, cz), rot=(90, 0, 0), m=door, bevel=0.012)
    k.torus(0.395, 0.038, at=(0, -0.07, cz), rot=(90, 0, 0), m=rim)

    # Wheel handle: shaft from the door, hub, rim and three crossing bars (six spokes).
    k.cyl(0.032, 0.09, at=(0, -0.115, cz), rot=(90, 0, 0), m=bolt)
    k.cyl(0.055, 0.05, at=(0, -0.165, cz), rot=(90, 0, 0), m=wheel, bevel=0.01)
    k.torus(0.23, 0.028, at=(0, -0.165, cz), rot=(90, 0, 0), m=wheel)
    for i in range(3):
        a = math.radians(90 + i * 60)
        dx, dz = 0.23 * math.cos(a), 0.23 * math.sin(a)
        k.tube([(-dx, -0.165, cz - dz), (dx, -0.165, cz + dz)], 0.02, wheel)

    # Hinges on the right: arm on the door, block on the collar, vertical pin through both.
    for dz in (-0.22, 0.22):
        z = cz + dz
        k.box((0.26, 0.04, 0.07), at=(0.5, -0.09, z), m=rim, bevel=0.008)
        k.box((0.07, 0.07, 0.11), at=(0.6, -0.06, z), m=collar, bevel=0.01)
        k.cyl(0.03, 0.15, at=(0.63, -0.1, z), m=bolt)

    # Curved corridor wall: strips along an arc about a horizontal axis on the corridor side.
    R = 1.7
    cy = 0.03 - R
    steps = 24
    a0, a1 = math.radians(-24), math.radians(75)
    for i in range(steps):
        a = a0 + (a1 - a0) * (i + 0.5) / steps
        seg = R * (a1 - a0) / steps * 1.04
        y = cy + (R + 0.04) * math.cos(a)
        z = cz + (R + 0.04) * math.sin(a)
        k.box((6, 0.08, seg), at=(0, y, z), rot=(math.degrees(a), 0, 0), m=wall, bevel=0, setting=True)
    # Two raised panel ribs running around the arc on either side of the hatch.
    for x in (-1.05, 1.05):
        pts = []
        for j in range(13):
            a = a0 + (a1 - a0) * j / 12
            pts.append((x, cy + (R - 0.01) * math.cos(a), cz + (R - 0.01) * math.sin(a)))
        k.tube(pts, 0.035, k.mat("#e3e6ea", "satin"), curved=True, setting=True)

    # Corridor floor.
    k.box((6, 3, 0.1), at=(0, -1.0, -0.05), m=k.mat("#b9c0c9", "satin"), bevel=0.01, setting=True)
