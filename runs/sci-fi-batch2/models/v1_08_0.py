# Rocket on its launch pad: a white body (lathe) capped by a red ogive nose cone, two round yellow windows with
# red rims on the front, a short metal nozzle under the tail, and four red swept fins at 90-degree steps whose
# lower edges stand on the concrete pad, so the rocket rests on its fins. The pad is a wide concrete slab that
# runs off the card; a green ground plane lies beyond it under the sky.
import math

SCENE = {"category": "4", "backdrop": "#5cc2f2", "azimuth": 25, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f7f7f4", "satin")
    red = k.mat("#e3282b", "satin")
    yellow = k.mat("#ffd23a", "gloss")
    steel = k.mat("#8b8f96", "metal")

    R = 0.1
    # Body: slight taper into the tail, straight tube up to the nose joint.
    k.lathe([(0, 0.07), (0.07, 0.07), (0.085, 0.09), (0.096, 0.12), (R, 0.16), (R, 0.72), (0, 0.72)],
            at=(0, 0, 0), rot=(0, 0, 0), m=white)
    # Nose cone: ogive from the body radius to a point.
    nose = []
    for i in range(17):
        t = i / 16
        nose.append((R * math.cos(t * math.pi / 2) ** 1.2 if i < 16 else 0, 0.72 + 0.28 * math.sin(t * math.pi / 2)))
    k.lathe([(0, 0.72)] + nose, at=(0, 0, 0), rot=(0, 0, 0), m=red)
    # Nozzle bell under the tail, clear of the pad.
    k.lathe([(0.06, 0.025), (0.05, 0.04), (0.04, 0.06), (0.045, 0.075), (0, 0.075)],
            at=(0, 0, 0), rot=(0, 0, 0), m=steel)

    # Two round windows on the front face (-y), each a yellow pane in a red rim.
    for z in (0.58, 0.42):
        k.cyl(0.04, 0.02, at=(0, -R + 0.002, z), rot=(90, 0, 0), m=yellow)
        k.torus(0.042, 0.011, at=(0, -R - 0.004, z), rot=(90, 0, 0), m=red)

    # Four swept fins: root along the body, lower edge on the pad, outer edge swept back.
    def sweep(p):
        x, y, z = p
        if x > 0 and z > 0:  # outer top corner pulls in and down -> swept leading edge
            return (x - 0.1, y, z - 0.06)
        return p

    for i in range(4):
        a = math.radians(45 + 90 * i)
        rc = 0.075 + 0.08
        fin = k.box((0.16, 0.024, 0.3), at=(rc * math.cos(a), rc * math.sin(a), 0.15),
                    rot=(0, 0, math.degrees(a)), m=red, bevel=0.008)
        k.warp(fin, sweep)

    # Concrete launch pad and the ground beyond it.
    k.box((3.0, 3.0, 0.08), at=(0, 0.4, -0.04), m=k.mat("#b9b6b0", "matte"), bevel=0.01, setting=True)
    k.floor("#7cc65a", z=-0.08)
