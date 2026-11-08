# Steel safe: a square steel body stands on four short feet at its corners. The closed door is a raised panel
# on the front, hung on two thick silver hinge barrels on its left edge. A round gold dial with a raised rim and
# a centre knob sits in the middle of the door, and a gold U-shaped grab handle stands off the door on the right.
SCENE = {"category": "2", "backdrop": "#d6337a", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    steel = k.mat("#1f2b55", "satin")
    door_steel = k.mat("#26346a", "satin")
    gold = k.mat("#f2c23a", "metal")
    silver = k.mat("#c9ced6", "metal")
    foot = k.mat("#151c38", "satin")

    # Feet and body
    for x in (-0.33, 0.33):
        for y in (-0.30, 0.30):
            k.cyl(0.05, 0.07, at=(x, y, 0.035), m=foot, bevel=0.01)
    k.box((0.8, 0.75, 0.85), at=(0, 0, 0.495), m=steel, bevel=0.04)

    # Door panel, raised from the front face (front at y = -0.375)
    k.box((0.64, 0.03, 0.68), at=(0, -0.39, 0.495), m=door_steel, bevel=0.015)

    # Hinges on the left edge: thick barrels with pins, mounted half on body, half on door
    for z in (0.30, 0.69):
        k.box((0.07, 0.03, 0.12), at=(-0.335, -0.39, z), m=silver, bevel=0.006)
        k.cyl(0.035, 0.14, at=(-0.36, -0.41, z), m=silver, bevel=0.008)
        k.cyl(0.015, 0.17, at=(-0.36, -0.41, z), m=silver, bevel=0.004)

    # Dial in the centre
    k.cyl(0.10, 0.04, at=(0, -0.425, 0.53), rot=(90, 0, 0), m=gold, bevel=0.008)
    k.torus(0.10, 0.012, at=(0, -0.445, 0.53), rot=(90, 0, 0), m=gold)
    k.cyl(0.04, 0.04, at=(0, -0.465, 0.53), rot=(90, 0, 0), m=gold, bevel=0.008)

    # Grab handle on the right
    k.tube([(0.24, -0.405, 0.60), (0.24, -0.47, 0.60), (0.24, -0.47, 0.38), (0.24, -0.405, 0.38)], 0.02, gold)
    for z in (0.60, 0.38):
        k.cyl(0.035, 0.012, at=(0.24, -0.41, z), rot=(90, 0, 0), m=gold, bevel=0.003)

    # Plain floor, a shade lighter than the backdrop
    k.box((6, 4, 0.1), at=(0, 0.8, -0.05), m=k.mat("#e8609a", "matte"), bevel=0.01, setting=True)
