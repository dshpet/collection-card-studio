# Space capsule: a white conical crew module stands on a wide, slightly domed dark heat shield that overhangs its
# base. A short docking neck caps the cone. One round yellow window sits on the sloping front face, set into a
# raised rim. It floats in open sky, tilted as if climbing, so the window shows along with a glimpse of the shield.
import math

SCENE = {"category": "1", "backdrop": "#4fb4ef", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    shield = k.mat("#4a2f22", "matte")
    trim = k.mat("#9aa0a8", "metal")
    glass = k.mat("#ffd23a", "glow")

    # Heat shield: shallow dish under the base, wider than the cone.
    dish = [(0.0, 0.0)] + [(0.5 * math.sin(math.radians(a)), 0.07 * (1 - math.cos(math.radians(a))))
                            for a in range(6, 91, 6)] + [(0.5, 0.11), (0.0, 0.11)]
    k.lathe(dish, at=(0, 0, 0), rot=(0, 0, 0), m=shield)

    # Crew module: a cone from the shield up to a rounded shoulder.
    body = [(0.0, 0.10), (0.46, 0.10), (0.47, 0.13), (0.15, 0.76), (0.13, 0.78), (0.0, 0.78)]
    k.lathe(body, at=(0, 0, 0), rot=(0, 0, 0), m=white)

    # Docking neck and its ring.
    k.cyl(0.11, 0.1, at=(0, 0, 0.82), rot=(0, 0, 0), m=white, bevel=0.015)
    k.torus(0.11, 0.022, at=(0, 0, 0.87), rot=(0, 0, 0), m=trim)

    # Window on the sloping front face, its axis along the cone's surface normal.
    half = math.atan2(0.47 - 0.15, 0.76 - 0.13)
    tilt = 90 - math.degrees(half)
    z = 0.42
    r = 0.47 - (0.47 - 0.15) * (z - 0.13) / (0.76 - 0.13)
    nx, nz = math.cos(half), math.sin(half)
    k.torus(0.085, 0.022, at=(0, -(r + 0.005 * nx), z + 0.005 * nz), rot=(tilt, 0, 0), m=trim)
    k.cyl(0.085, 0.03, at=(0, -(r - 0.005), z), rot=(tilt, 0, 0), m=glass, bevel=0.004)

    k.turn(-10, -18, 25)
