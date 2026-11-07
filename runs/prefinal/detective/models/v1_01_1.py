# Magnifier: a round gold rim holds a clear lens disc; a gold ferrule sits on the rim's lower edge and takes the
# dark wooden handle, about as long as the lens is wide, which carries a red grip band and ends in a rounded knob.
# A small white glint lies on the lens front. Floating, tilted so the handle runs down to the left and the lens
# shows a little of its edge.
SCENE = {"category": "1", "backdrop": "#45c4f0", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#f0b429", "metal")
    glass = k.mat("#e6f6ff", "glass")
    wood = k.mat("#5a3218", "satin")
    red = k.mat("#d8262b", "satin")
    white = k.mat("#ffffff", "glow")

    cz, R = 0.86, 0.30
    # Rim and lens, ring in the xz plane facing -y. Rim's lower edge at cz - R - 0.036 = 0.524.
    k.torus(R, 0.036, at=(0, 0, cz), rot=(90, 0, 0), m=gold)
    k.cyl(R - 0.004, 0.022, at=(0, 0, cz), rot=(90, 0, 0), m=glass, bevel=0.008)
    # White glint on the lens front, upper left.
    k.sphere(0.05, at=(-0.12, -0.013, cz + 0.13), scale=(1.0, 0.12, 0.35), rot=(0, 40, 0), m=white)

    # Gold ferrule joining the rim's lower edge to the handle.
    k.lathe([(0, 0.425), (0.05, 0.425), (0.056, 0.44), (0.05, 0.46), (0.042, 0.48),
             (0.036, 0.50), (0.032, 0.535), (0, 0.535)], at=(0, 0, 0), rot=(0, 0, 0), m=gold)

    # Dark wooden handle with a rounded knob at the end.
    k.lathe([(0, -0.04), (0.025, -0.038), (0.045, -0.025), (0.056, -0.005), (0.056, 0.015),
             (0.05, 0.035), (0.046, 0.08), (0.046, 0.2), (0.044, 0.32), (0.042, 0.43), (0, 0.43)],
            at=(0, 0, 0), rot=(0, 0, 0), m=wood)
    # Red grip band around the handle.
    k.cyl(0.052, 0.05, at=(0, 0, 0.2), rot=(0, 0, 0), m=red, bevel=0.008)

    k.turn(8, 28, -12)
