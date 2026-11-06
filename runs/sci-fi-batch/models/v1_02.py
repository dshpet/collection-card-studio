# Flying saucer: one round lens-shaped silver hull, thicker at the centre and thinning to a rounded rim. A
# raised metal collar sits on the top centre, and the light-blue glass dome sits in the collar. A satin bumper
# ring runs around the rim edge, and eight round orange lights sit evenly around it, half set into the ring.
# A small metal dome under the hull closes the bottom. The saucer floats with no setting and is tilted toward
# the camera so the top and the dome show, with a slight roll for life.
import math

SCENE = {"category": "1", "backdrop": "#8a3fd6", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    rim = k.mat("#9aa1ab", "satin")
    glass = k.mat("#9fdcff", "glass")
    lamp = k.mat("#ff5a00", "glow")

    # Hull: a smooth lens of revolution.
    hull = [(0.0, -0.085)]
    for i in range(1, 17):
        t = i / 16
        hull.append((0.5 * math.sin(t * math.pi / 2), -0.085 * math.cos(t * math.pi / 2)))
    for i in range(1, 17):
        t = i / 16
        hull.append((0.5 * math.cos(t * math.pi / 2), 0.075 * math.sin(t * math.pi / 2)))
    hull[-1] = (0.0, 0.075)
    k.lathe(hull, at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # Bumper ring around the rim and the eight lights set into it.
    k.torus(0.49, 0.024, at=(0, 0, 0), rot=(0, 0, 0), m=rim)
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        k.sphere(0.038, at=(0.505 * math.cos(a), 0.505 * math.sin(a), 0.0), m=lamp)

    # Collar on top and the glass dome seated in it.
    k.cyl(0.235, 0.04, at=(0, 0, 0.075), rot=(0, 0, 0), m=rim, bevel=0.01)
    dome = [(0.21 * math.cos(i / 20 * math.pi / 2), 0.09 + 0.2 * math.sin(i / 20 * math.pi / 2)) for i in range(21)]
    dome[-1] = (0.0, 0.29)
    k.lathe([(0.0, 0.09)] + dome, at=(0, 0, 0), rot=(0, 0, 0), m=glass)

    # Small dome under the hull.
    under = [(0.0, -0.14)] + [(0.13 * math.sin(i / 12 * math.pi / 2), -0.075 - 0.065 * math.cos(i / 12 * math.pi / 2))
                              for i in range(1, 13)]
    k.lathe(under, at=(0, 0, 0), rot=(0, 0, 0), m=rim)

    k.turn(14, -6, 0)
