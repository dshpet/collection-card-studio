# Joystick on a metal desk: a round, domed black base sits flat on the desk top; a dark grey rubber boot rises
# from the dome's center and the thick black stick comes up through it to a round red knob. A yellow push button
# sits in a dark collar on the front-right of the dome. The desk is a metal slab whose front edge runs
# across the lower card, as the desk edge does on the computer card.
SCENE = {"category": "3", "backdrop": "#4fbf5a", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#1c1d21", "satin")
    grey = k.mat("#3c3f46", "matte")
    red = k.mat("#e1262b", "gloss")
    yellow = k.mat("#ffd21f", "gloss")
    steel = k.mat("#aab2bc", "metal")

    # Round domed base, resting on the desk top at z = 0.
    k.lathe([(0, 0), (0.37, 0), (0.385, 0.015), (0.385, 0.06), (0.37, 0.09), (0.33, 0.115),
             (0.26, 0.135), (0.17, 0.148), (0.08, 0.154), (0, 0.155)], at=(0, 0, 0), rot=(0, 0, 0), m=black)
    # Dark grey trim ring around the base's lower edge.
    k.torus(0.385, 0.018, at=(0, 0, 0.035), rot=(0, 0, 0), m=grey)

    # Rubber boot around the stick's root, seated on the dome.
    k.lathe([(0, 0.14), (0.13, 0.14), (0.125, 0.17), (0.105, 0.2), (0.085, 0.235), (0.07, 0.27),
             (0.065, 0.29), (0, 0.29)], at=(0, 0, 0), rot=(0, 0, 0), m=grey)
    # Thick upright stick, from inside the boot up into the knob.
    k.cyl(0.05, 0.46, at=(0, 0, 0.4), rot=(0, 0, 0), m=black)
    # Round red knob on top of the stick.
    k.sphere(0.13, at=(0, 0, 0.73), m=red)

    # Yellow button in a dark collar on the front-right of the dome.
    bx, by = 0.17, -0.16
    k.cyl(0.075, 0.03, at=(bx, by, 0.142), rot=(0, 0, 0), m=grey)
    k.cyl(0.055, 0.04, at=(bx, by, 0.165), rot=(0, 0, 0), m=yellow, bevel=0.012)

    # Metal desk: top at z = 0, front edge crossing below the base.
    k.box((5, 3, 0.08), at=(0, 0.9, -0.04), m=steel, bevel=0.012, setting=True)
    # Desk front panel under the edge.
    k.box((5, 0.04, 0.6), at=(0, -0.58, -0.38), m=k.mat("#8d96a1", "metal"), bevel=0.01, setting=True)
