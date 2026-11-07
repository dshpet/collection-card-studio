# Map magnifier: a magnifying glass lies flat on a paper street map, which lies on a dark wooden table.
# The gold rim rests on the paper and holds the clear lens; a gold neck and ferrule join the rim to the dark
# brown handle, which lies on the paper and ends in a gold cap. Seen from high above; the map fills most of the
# card and the dark table shows along its edges. Road lines and the park patch are printed on the paper, so the
# image model draws them.
import math

SCENE = {"category": "3", "backdrop": "#1f4fb8", "azimuth": 25, "elevation": 65, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e2b23c", "metal")
    glass = k.mat("#cfe8f5", "glass")
    wood = k.mat("#5a2f17", "satin")
    paper = k.mat("#e6cf98", "matte")
    table = k.mat("#3e2414", "matte")

    R, ring = 0.28, 0.035
    yaw = -35.0  # handle points right and toward the camera
    dx, dy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))

    def along(dist):
        return (dx * dist, dy * dist)

    # Rim resting on the paper, lens held inside it.
    k.torus(R, ring, at=(0, 0, ring), m=gold)
    k.cyl(R - 0.01, 0.022, at=(0, 0, ring), m=glass, bevel=0.008)

    # Neck from the rim, ferrule, handle lying on the paper, end cap.
    x, y = along(R + 0.06)
    k.cyl(0.03, 0.09, at=(x, y, ring), rot=(0, 90, yaw), m=gold)
    x, y = along(R + 0.13)
    k.cyl(0.045, 0.06, at=(x, y, 0.045), rot=(0, 90, yaw), m=gold, bevel=0.01)
    x, y = along(R + 0.355)
    k.cyl(0.045, 0.39, at=(x, y, 0.045), rot=(0, 90, yaw), m=wood, bevel=0.015)
    x, y = along(R + 0.565)
    k.cyl(0.042, 0.03, at=(x, y, 0.045), rot=(0, 90, yaw), m=gold, bevel=0.01)

    # One flat paper map sheet lying on the dark wooden table, turned a little so the table shows at its edges.
    k.box((1.75, 1.55, 0.006), at=(0.12, 0.0, -0.003), rot=(0, 0, 6), m=paper, bevel=0.002, setting=True)
    k.box((8, 8, 0.1), at=(0, 0, -0.056), m=table, bevel=0, setting=True)
