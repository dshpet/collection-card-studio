# Frosted office door: a dark wood frame-and-panel door (two stiles, three rails) hangs in a wood casing set in a
# brick wall. The frosted glass sits in the upper opening between the stiles, with a warm glowing room panel just
# behind it. Two raised panels fill the lower part. Hinge barrels with leaves join the left stile to the casing; a
# brass knob on a rosette and stem sits on the right stile. The door stands on a stone doorstep resting on the
# pavement. The wall and step run off the card; the framing holds the door and its casing.
SCENE = {"category": "4", "backdrop": "#5fc4f2", "azimuth": 20, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#4a2a17", "satin")
    trim = k.mat("#3b2011", "satin")
    glass = k.mat("#f4f1ea", "glass")
    glow = k.mat("#ffd58a", "glow")
    brass = k.mat("#d4a23c", "metal")
    iron = k.mat("#b48a3a", "metal")

    z0, z1 = 0.06, 1.11            # door bottom (on step) and top
    yd = 0.0                       # door slab center depth (front faces -y)
    t = 0.05

    # door: stiles and rails
    for x in (-0.215, 0.215):
        k.box((0.07, t, z1 - z0), at=(x, yd, (z0 + z1) / 2), m=wood, bevel=0.006)
    for zc, h in ((0.10, 0.08), (0.57, 0.10), (1.07, 0.08)):
        k.box((0.36, t, h), at=(0, yd, zc), m=wood, bevel=0.006)
    k.box((0.05, t, 0.38), at=(0, yd, 0.33), m=wood, bevel=0.006)          # lower mullion
    # lower raised panels
    for x in (-0.105, 0.105):
        k.box((0.155, 0.03, 0.38), at=(x, yd + 0.005, 0.33), m=wood, bevel=0.004)
        k.box((0.11, 0.02, 0.32), at=(x, yd - 0.012, 0.33), m=wood, bevel=0.008)
    # frosted glass with warm room light behind
    k.box((0.36, 0.012, 0.41), at=(0, yd, 0.825), m=glass, bevel=0.002)
    k.box((0.36, 0.005, 0.41), at=(0, yd + 0.02, 0.825), m=glow, bevel=0.0)
    # glazing beads
    for x in (-0.172, 0.172):
        k.box((0.016, 0.016, 0.41), at=(x, yd - 0.012, 0.825), m=wood, bevel=0.003)
    for zc in (0.628, 1.022):
        k.box((0.36, 0.016, 0.016), at=(0, yd - 0.012, zc), m=wood, bevel=0.003)

    # casing around the opening
    for x in (-0.28, 0.28):
        k.box((0.06, 0.12, 1.17 - z0), at=(x, -0.02, (z0 + 1.17) / 2), m=trim, bevel=0.008)
    k.box((0.62, 0.12, 0.07), at=(0, -0.02, 1.14), m=trim, bevel=0.008)

    # hinges on the left: barrel on the joint, leaves on stile and casing
    for zc in (0.24, 0.92):
        k.cyl(0.013, 0.09, at=(-0.25, -0.03, zc), m=iron, bevel=0.003)
        k.box((0.035, 0.006, 0.08), at=(-0.232, -0.027, zc), m=iron, bevel=0.002)
        k.box((0.03, 0.006, 0.08), at=(-0.266, -0.08, zc), m=iron, bevel=0.002)
        k.sphere(0.014, at=(-0.25, -0.03, zc + 0.052), m=iron)

    # brass knob on the right stile
    kx, kz = 0.205, 0.55
    k.cyl(0.03, 0.008, at=(kx, -0.029, kz), rot=(90, 0, 0), m=brass, bevel=0.003)
    k.cyl(0.011, 0.04, at=(kx, -0.05, kz), rot=(90, 0, 0), m=brass, bevel=0.002)
    k.sphere(0.034, at=(kx, -0.085, kz), scale=(1, 0.85, 1), m=brass)

    # setting: brick wall with the opening, stone doorstep, pavement
    brick = k.mat("#b5523a", "matte")
    k.box((2.0, 0.3, 3.0), at=(-1.31, 0.1, 1.5), m=brick, bevel=0.01, setting=True)
    k.box((2.0, 0.3, 3.0), at=(1.31, 0.1, 1.5), m=brick, bevel=0.01, setting=True)
    k.box((0.62, 0.3, 1.83), at=(0, 0.1, 2.09), m=brick, bevel=0.01, setting=True)
    k.box((0.8, 0.36, 0.06), at=(0, -0.13, 0.03), m=k.mat("#bdb5a6", "matte"), bevel=0.012, setting=True)
    k.box((6, 4, 0.1), at=(0, -1.8, -0.05), m=k.mat("#9a948a", "matte"), bevel=0.01, setting=True)
