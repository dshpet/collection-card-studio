# Haunted house: a two-storey mansion on a stone footing set into the hill; the upper storey sits a little skewed on
# the lower one, and a steep gable roof sits on the upper storey with a round attic window in its front gable. A
# leaning round tower stands on its own footing against the left corner under a tilted spire, and a kinked chimney
# rises out of the right roof plane. Windows glow yellow. The house stands on the crown of a grassy hill, with two
# trees far back at the sides and a big moon in the sky behind.
import math

SCENE = {"category": "4", "backdrop": "#3ea8f0", "azimuth": 28, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    wall = k.mat("#8a7a6a", "matte")
    stone = k.mat("#6e655c", "matte")
    trim = k.mat("#4b3a33", "satin")
    roof = k.mat("#4a2a5e", "satin")
    glow = k.mat("#ffd640", "glow")

    # Footing sunk into the hill, two storeys and the band between them. The upper storey leans a little,
    # and the gable leans with it so it sits flush.
    k.box((0.58, 0.46, 0.16), at=(0, 0, -0.02), m=stone, bevel=0.01)
    k.box((0.52, 0.40, 0.40), at=(0, 0, 0.26), m=wall, bevel=0.008)
    k.box((0.56, 0.44, 0.03), at=(0, 0, 0.465), m=trim, bevel=0.006)
    k.box((0.50, 0.38, 0.30), at=(0.015, 0, 0.63), rot=(0, 0, -2), m=wall, bevel=0.008)

    # Gable mass: a box tapered to a ridge along y, then two roof planes and a ridge cap.
    gable = k.box((0.50, 0.38, 0.36), at=(0.015, 0, 0.955), rot=(0, 0, -2), m=wall, bevel=0.004)
    k.warp(gable, lambda p: (p[0] * (0.18 - p[2]) / 0.36, p[1], p[2]))
    slope = math.degrees(math.atan2(0.36, 0.25))
    for side in (-1, 1):
        k.box((0.50, 0.46, 0.03), at=(0.015 + side * 0.156, 0, 0.939), rot=(0, side * slope, -2), m=roof,
              bevel=0.006)
    k.cyl(0.025, 0.48, at=(0.015, 0, 1.145), rot=(90, 0, -2), m=roof)

    # Round attic window in the front gable.
    k.cyl(0.068, 0.02, at=(0.02, -0.19, 0.985), rot=(90, 0, 0), m=glow)
    k.torus(0.075, 0.015, at=(0.02, -0.2, 0.985), rot=(90, 0, 0), m=trim)
    k.box((0.13, 0.012, 0.012), at=(0.02, -0.2, 0.985), m=trim, bevel=0.003)
    k.box((0.012, 0.012, 0.13), at=(0.02, -0.2, 0.985), m=trim, bevel=0.003)

    # Front: door with a step sunk into the ground, ground-floor and upper windows, each in a dark frame.
    k.box((0.12, 0.02, 0.2), at=(-0.03, -0.205, 0.16), m=trim, bevel=0.005)
    k.box((0.09, 0.015, 0.17), at=(-0.03, -0.212, 0.155), m=k.mat("#3a2433", "satin"), bevel=0.004)
    k.box((0.18, 0.1, 0.12), at=(-0.03, -0.27, -0.01), m=stone, bevel=0.008)

    def window(x, y, z, face="front", tilt=0.0):
        if face == "front":
            k.box((0.11, 0.016, 0.14), at=(x, y, z), rot=(0, tilt, 0), m=trim, bevel=0.004)
            k.box((0.08, 0.016, 0.11), at=(x, y - 0.006, z), rot=(0, tilt, 0), m=glow, bevel=0.003)
        else:
            k.box((0.016, 0.11, 0.14), at=(x, y, z), rot=(tilt, 0, 0), m=trim, bevel=0.004)
            k.box((0.016, 0.08, 0.11), at=(x + 0.006, y, z), rot=(tilt, 0, 0), m=glow, bevel=0.003)

    window(0.15, -0.203, 0.28)
    window(-0.13, -0.198, 0.63, tilt=4)
    window(0.15, -0.203, 0.62, tilt=-3)
    window(0.263, 0.0, 0.28, face="side")
    window(0.263, 0.02, 0.63, face="side", tilt=3)

    # Leaning round tower on its own footing at the left front corner, its spire tilted further.
    k.cyl(0.13, 0.14, at=(-0.33, -0.1, -0.02), m=stone, bevel=0.008)
    k.cyl(0.11, 0.94, at=(-0.33, -0.1, 0.47), rot=(0, -3, 0), m=wall, bevel=0.008)
    top = (-0.355, -0.1, 0.939)
    k.cyl(0.13, 0.035, at=top, rot=(0, -3, 0), m=trim, bevel=0.006)
    t = math.radians(-8)
    k.cone(0.15, 0.0, 0.42, at=(top[0] + 0.21 * math.sin(t), -0.1, top[2] + 0.21 * math.cos(t)), rot=(0, -8, 0),
           m=roof, bevel=0.004)
    k.sphere(0.022, at=(top[0] + 0.42 * math.sin(t), -0.1, top[2] + 0.42 * math.cos(t)), m=trim)
    for z, x, tilt in ((0.33, -0.33, -3), (0.68, -0.348, -5)):
        k.box((0.075, 0.03, 0.13), at=(x, -0.2, z), rot=(0, tilt, 0), m=trim, bevel=0.004)
        k.box((0.05, 0.03, 0.1), at=(x, -0.207, z), rot=(0, tilt, 0), m=glow, bevel=0.003)

    # Kinked chimney rising out of the right roof plane.
    k.box((0.08, 0.08, 0.32), at=(0.2, 0.08, 0.96), rot=(0, 8, 0), m=stone, bevel=0.006)
    k.box((0.086, 0.086, 0.05), at=(0.222, 0.08, 1.118), rot=(0, -1, 0), m=stone, bevel=0.006)
    k.box((0.08, 0.08, 0.12), at=(0.212, 0.08, 1.177), rot=(0, -10, 0), m=stone, bevel=0.006)
    k.box((0.11, 0.11, 0.03), at=(0.2, 0.08, 1.245), rot=(0, -10, 0), m=trim, bevel=0.006)

    # Grassy hilltop, the land below it, two trees far back toward the card edges and the moon in the sky.
    k.blob([(0, 0.3, -1.37, 1.4, (2.2, 1.6, 1.0))], k.mat("#5fae3c", "matte"), setting=True)
    k.floor("#3f8a34", z=-0.8)
    tree = k.mat("#2f6b2e", "matte")
    for x, y, r in ((-3.0, 2.9, 0.45), (-1.1, 5.1, 0.5)):
        k.cyl(0.06, 0.6, at=(x, y, -0.5), m=k.mat("#5a3b26", "matte"), setting=True)
        k.sphere(r, at=(x, y, -0.2 + r), m=tree, setting=True)
    k.sphere(0.4, at=(-2.97, 7.47, 1.1), m=k.mat("#ffe36a", "glow"), setting=True)
