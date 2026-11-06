# Teleport pod: a round stepped metal base sits on the metal floor; a cyan glow ring is set into the base's top
# step around the foot of the glass. A tall hollow glass tube with thin walls stands on the base, around a dark
# floor pad, and a round metal cap with a shallow dome sits on the tube's top rim, its lip overhanging the glass.
# The shiny metal floor runs off the card.
SCENE = {"category": "3", "backdrop": "#9be03a", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    dark = k.mat("#7d848e", "metal")
    glass = k.mat("#dff6ff", "glass")
    glow = k.mat("#3ff0ff", "glow")

    # Base: wide bottom plinth stepping in to a top deck that carries the glass.
    k.lathe([(0.0, 0.0), (0.34, 0.0), (0.35, 0.01), (0.35, 0.07), (0.34, 0.08),
             (0.305, 0.085), (0.30, 0.095), (0.30, 0.14), (0.29, 0.15), (0.0, 0.15)],
            at=(0, 0, 0), rot=(0, 0, 0), m=silver)
    # Glow ring on the top deck, around the foot of the glass.
    k.torus(0.265, 0.02, at=(0, 0, 0.152), rot=(0, 0, 0), m=glow)
    # Inner floor pad inside the glass tube.
    k.cyl(0.2, 0.012, at=(0, 0, 0.156), rot=(0, 0, 0), m=dark, bevel=0.004)

    # Hollow glass tube: thin wall, standing on the base deck and carrying the cap.
    k.lathe([(0.215, 0.15), (0.235, 0.15), (0.235, 1.15), (0.215, 1.15), (0.215, 0.15)],
            at=(0, 0, 0), rot=(0, 0, 0), m=glass, verts=96)

    # Cap: a lip that overhangs the glass rim, a band, then a shallow dome.
    k.lathe([(0.0, 1.15), (0.285, 1.15), (0.295, 1.16), (0.295, 1.20), (0.285, 1.21),
             (0.27, 1.215), (0.24, 1.232), (0.20, 1.248), (0.14, 1.26), (0.07, 1.266), (0.0, 1.268)],
            at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # Shiny metal floor, top at z = 0, running off the card.
    k.box((8, 8, 0.04), at=(0, 1.5, -0.02), m=k.mat("#aab3bd", "metal"), bevel=0, setting=True)
