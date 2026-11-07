# Map magnifier: a magnifying glass lies flat on a folded paper street map, which lies on a dark wooden table.
# The gold rim rests on the paper and holds the clear lens; a gold ferrule joins the rim to the dark brown
# handle, which lies on the paper and ends in a gold cap. Seen from high above, like the map and racket cards;
# the map runs off the card and the table shows only at its edges. Road lines and the park patch are printed
# on the paper, so the image model draws them.
import math

SCENE = {"category": "3", "backdrop": "#1f4fb8", "azimuth": 25, "elevation": 65, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e2b23c", "metal")
    glass = k.mat("#cfe8f5", "glass")
    wood = k.mat("#5a2f17", "satin")
    paper = k.mat("#f3e6c4", "matte")
    table = k.mat("#5b3620", "matte")

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
    k.cyl(0.03, 0.09, at=(x, y, 0.04), rot=(0, 90, yaw), m=gold)
    x, y = along(R + 0.13)
    k.cyl(0.045, 0.06, at=(x, y, 0.045), rot=(0, 90, yaw), m=gold, bevel=0.01)
    x, y = along(R + 0.355)
    k.cyl(0.045, 0.39, at=(x, y, 0.045), rot=(0, 90, yaw), m=wood, bevel=0.015)
    x, y = along(R + 0.565)
    k.cyl(0.042, 0.03, at=(x, y, 0.045), rot=(0, 90, yaw), m=gold, bevel=0.01)

    # Folded paper map: three panels meeting at shallow creases, on the dark wooden table.
    for i, (px, tilt) in enumerate(((-0.55, 1.2), (0.0, -1.2), (0.55, 1.2))):
        k.box((0.56, 1.9, 0.006), at=(px + 0.1, 0.05, -0.004 + (0.006 if i == 1 else 0.0)),
              rot=(0, tilt, 8), m=paper, bevel=0.002, setting=True)
    k.box((8, 8, 0.1), at=(0, 0, -0.06), m=table, bevel=0, setting=True)
