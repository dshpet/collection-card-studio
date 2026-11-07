# Vintage flash camera: a black box body with the lens barrel on its front face (-y): a black barrel, a silver
# lens ring and a glass front lens. A silver post rises from the top plate on the left and holds the round flash
# dish, which faces forward with its bulb in a socket at the centre. The red shutter button sits on a silver
# collar on the top right, beside a winding knob. Floating, tilted a little.
SCENE = {"category": "1", "backdrop": "#45b6f0", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#1d1e22", "satin")
    silver = k.mat("#c9ced6", "metal")
    glass = k.mat("#2a3f5c", "glass")
    red = k.mat("#e8262b", "gloss")
    bulb = k.mat("#f4f6fa", "glass")

    # Body
    k.box((0.70, 0.32, 0.46), at=(0, 0, 0.25), m=black, bevel=0.04)
    k.box((0.72, 0.34, 0.03), at=(0, 0, 0.47), m=silver, bevel=0.01)   # top plate trim

    # Lens: black barrel from the front face, silver ring, glass front lens
    k.cyl(0.15, 0.10, at=(0.02, -0.20, 0.24), rot=(90, 0, 0), m=black, bevel=0.01)
    k.cyl(0.165, 0.06, at=(0.02, -0.27, 0.24), rot=(90, 0, 0), m=silver, bevel=0.012)
    k.torus(0.125, 0.018, at=(0.02, -0.30, 0.24), rot=(90, 0, 0), m=silver)
    k.sphere(0.115, at=(0.02, -0.295, 0.24), scale=(1, 0.28, 1), m=glass)

    # Flash: post from the top plate, socket arm, dish facing forward, bulb in the middle
    px, py = -0.20, 0.08
    k.cyl(0.022, 0.24, at=(px, py, 0.60), m=silver)
    k.cyl(0.03, 0.02, at=(px, py, 0.495), m=silver)
    k.cyl(0.03, 0.06, at=(px, py - 0.01, 0.72), rot=(90, 0, 0), m=silver)
    dish = [(0.0, 0.0), (0.03, 0.002), (0.06, 0.010), (0.09, 0.025), (0.12, 0.048), (0.145, 0.078),
            (0.16, 0.10), (0.152, 0.104), (0.138, 0.084), (0.113, 0.056), (0.085, 0.034), (0.055, 0.020),
            (0.028, 0.014), (0.0, 0.012)]
    k.lathe(dish, at=(px, 0.04, 0.72), rot=(90, 0, 0), m=silver)
    k.cyl(0.018, 0.04, at=(px, 0.015, 0.72), rot=(90, 0, 0), m=silver)
    k.sphere(0.042, at=(px, -0.025, 0.72), m=bulb)

    # Shutter button and winding knob on the top plate
    k.cyl(0.045, 0.02, at=(0.20, -0.06, 0.495), m=silver, bevel=0.004)
    k.cyl(0.032, 0.035, at=(0.20, -0.06, 0.52), m=red, bevel=0.008)
    k.cyl(0.05, 0.035, at=(0.22, 0.08, 0.50), m=silver, bevel=0.008)

    k.turn(-4, 6, 0)
