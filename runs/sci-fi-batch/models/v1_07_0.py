# Teleport pod: a round stepped metal base sits on the metal floor; a cyan glow ring is set into the base's top
# step around the foot of the glass. The upright glass cylinder stands on the base, and a round metal cap with a
# shallow dome sits on the glass's top rim, its lip overhanging the glass. The shiny metal floor runs off the card.
SCENE = {"category": "3", "backdrop": "#9be03a", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    dark = k.mat("#7d848e", "metal")
    glass = k.mat("#dff6ff", "glass")
    glow = k.mat("#3ff0ff", "glow")

    # Base: wide bottom plinth stepping in to a top deck that carries the glass.
    k.lathe([(0.0, 0.0), (0.40, 0.0), (0.41, 0.01), (0.41, 0.07), (0.40, 0.08),
             (0.36, 0.085), (0.355, 0.095), (0.355, 0.14), (0.345, 0.15), (0.0, 0.15)],
            at=(0, 0, 0), rot=(0, 0, 0), m=silver)
    # Glow ring on the top deck, around the foot of the glass.
    k.torus(0.322, 0.022, at=(0, 0, 0.152), rot=(0, 0, 0), m=glow)
    # Inner floor pad inside the glass.
    k.cyl(0.27, 0.012, at=(0, 0, 0.156), rot=(0, 0, 0), m=dark, bevel=0.004)

    # Glass cylinder, standing on the base deck and carrying the cap.
    k.cyl(0.29, 0.70, at=(0, 0, 0.15 + 0.35), rot=(0, 0, 0), m=glass, bevel=0.006)

    # Cap: a lip that overhangs the glass rim, a band, then a shallow dome.
    k.lathe([(0.0, 0.85), (0.345, 0.85), (0.355, 0.86), (0.355, 0.90), (0.345, 0.91),
             (0.33, 0.915), (0.30, 0.935), (0.25, 0.955), (0.18, 0.968), (0.10, 0.975), (0.0, 0.977)],
            at=(0, 0, 0), rot=(0, 0, 0), m=silver)
    # Small emitter knob on top of the dome.
    k.cyl(0.06, 0.03, at=(0, 0, 0.99), rot=(0, 0, 0), m=dark, bevel=0.008)

    # Shiny metal floor, top at z = 0, running off the card.
    k.box((8, 8, 0.04), at=(0, 1.5, -0.02), m=k.mat("#aab3bd", "metal"), bevel=0, setting=True)
