# Wall control panel in a spaceship cabin: a grey box panel bolted flat to the cabin wall, front facing -y.
# Upper left: a dark bezel framing a blue screen with a small glowing planet icon (disk with a flat elliptical
# ring tilted across it) raised on the glass. Upper right: three rows of four round yellow push buttons, each on
# a short collar. Lower part: two horizontal slots, each holding a lever whose stem rises out of a sliding
# carriage to a round knob. Four bolts at the corners hold the panel to the wall. The setting is only the few
# metres of wall around it: plated wall with raised seams and ribs, a floor far below. The camera is low and
# fairly frontal, so the panel fills the card.
SCENE = {"category": "4", "backdrop": "#7b4fc8", "azimuth": 22, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    grey = k.mat("#a3aab4", "satin")
    dark = k.mat("#4d535d", "satin")
    slot_m = k.mat("#2a2e35", "matte")
    screen = k.mat("#2f86e8", "gloss")
    planet = k.mat("#bff0ff", "glow")
    yellow = k.mat("#ffcf2e", "gloss")
    steel = k.mat("#c9ced6", "metal")
    knob_m = k.mat("#3b4049", "gloss")

    # Panel body: wall face at y = 0, panel front at y = -0.09.
    zc, w, h, d = 1.25, 1.0, 0.8, 0.09
    front = -d
    k.box((w, d, h), at=(0, -d / 2, zc), m=grey, bevel=0.025)
    # Mounting plate against the wall, a little larger than the panel.
    k.box((w + 0.06, 0.02, h + 0.06), at=(0, -0.01, zc), m=dark, bevel=0.008)
    for x in (-w / 2 + 0.045, w / 2 - 0.045):
        for z in (zc - h / 2 + 0.045, zc + h / 2 - 0.045):
            k.cyl(0.022, 0.02, at=(x, front - 0.005, z), rot=(90, 0, 0), m=steel, verts=6)

    # Screen in its bezel.
    sx, sz = -0.2, zc + 0.12
    k.box((0.5, 0.025, 0.4), at=(sx, front - 0.012, sz), m=dark, bevel=0.012)
    k.box((0.42, 0.012, 0.32), at=(sx, front - 0.028, sz), m=screen, bevel=0.006)
    # Planet icon on the screen: a flat glowing disk and a flat elliptical ring tilted across it, both just
    # in front of the glass (glass front at front - 0.034).
    k.cyl(0.07, 0.004, at=(sx, front - 0.037, sz), rot=(90, 0, 0), m=planet)
    ring = k.torus(0.125, 0.011, at=(sx, front - 0.045, sz), rot=(90, -18, 0), m=planet)
    k.warp(ring, lambda p: (p[0], p[1] * 0.32, p[2] * 0.3))

    # Three rows of four round yellow buttons on dark collars.
    for row in range(3):
        z = zc + 0.25 - row * 0.13
        for col in range(4):
            x = 0.15 + col * 0.095
            k.cyl(0.038, 0.012, at=(x, front - 0.006, z), rot=(90, 0, 0), m=dark)
            k.lathe([(0.0, 0.0), (0.03, 0.0), (0.03, 0.018), (0.026, 0.026), (0.015, 0.031), (0.0, 0.032)],
                    at=(x, front - 0.01, z), rot=(90, 0, 0), m=yellow, verts=48)

    # Two sliding levers, each riding a carriage in its own horizontal slot.
    for lx, frac in ((-0.2, 0.3), (0.25, 0.7)):
        z = zc - 0.27
        slot_w = 0.36
        k.box((slot_w + 0.04, 0.012, 0.075), at=(lx, front - 0.004, z), m=dark, bevel=0.01)
        k.box((slot_w, 0.016, 0.026), at=(lx, front - 0.008, z), m=slot_m, bevel=0.004)
        kx = lx - slot_w / 2 + 0.04 + frac * (slot_w - 0.08)
        k.box((0.05, 0.02, 0.045), at=(kx, front - 0.02, z), m=steel, bevel=0.008)
        k.tube([(kx, front - 0.025, z), (kx, front - 0.07, z + 0.05)], 0.012, steel)
        k.sphere(0.03, at=(kx, front - 0.075, z + 0.06), m=knob_m)

    # Setting: cabin wall with raised ribs and seams, and a floor far below.
    wall = k.mat("#8a7fb8", "satin")
    rib = k.mat("#6a5c9c", "satin")
    k.box((7, 0.2, 4), at=(0, 0.1, 2), m=wall, bevel=0.0, setting=True)
    for x in (-1.0, 1.0):
        k.box((0.14, 0.06, 4), at=(x, -0.03, 2), m=rib, bevel=0.015, setting=True)
    for z in (0.62, 1.92):
        k.box((7, 0.02, 0.04), at=(0, -0.01, z), m=rib, bevel=0.006, setting=True)
    k.floor("#4a3f78", "satin")
