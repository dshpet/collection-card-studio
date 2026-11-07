# Two-slot toaster: a rounded silver body on four short feet. Two slots run along its length on top; a golden
# toast slice stands in each, dropping down into the body and popping up above it at slightly different heights.
# The push-down lever rides in a vertical slot on the right end, and the red browning dial sits on the front
# face near the right end, with a raised pointer ridge.
SCENE = {"category": "2", "backdrop": "#ef6aa6", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    steel = k.mat("#d6dae0", "metal")
    dark = k.mat("#2c2c33", "satin")
    red = k.mat("#e2303c", "gloss")
    crust = k.mat("#c17a2c", "matte")
    crumb = k.mat("#f1c76c", "matte")

    W, D, H, base = 0.64, 0.40, 0.42, 0.025
    top = base + H

    # Feet and body
    for x in (-0.26, 0.26):
        for y in (-0.14, 0.14):
            k.cyl(0.03, base + 0.01, at=(x, y, (base + 0.01) / 2), m=dark, bevel=0.006)
    k.box((W, D, H), at=(0, 0, base + H / 2), m=steel, bevel=0.08)

    # Slot openings (dark insets flush with the top) and the toast standing in them
    for y, t in ((-0.085, 0.70), (0.085, 0.66)):
        k.box((0.48, 0.075, 0.012), at=(0, y, top - 0.004), m=dark, bevel=0.004)
        lobe_z = t - 0.09
        bottom = top - 0.12
        box_top = lobe_z + 0.03
        k.box((0.40, 0.05, box_top - bottom), at=(0, y, (box_top + bottom) / 2), m=crust, bevel=0.01)
        for x in (-0.11, 0.11):
            k.cyl(0.09, 0.05, at=(x, y, lobe_z), rot=(90, 0, 0), m=crust, bevel=0.01)
        # soft crumb faces inset from the crust on both sides
        k.box((0.36, 0.056, box_top - bottom - 0.02), at=(0, y, (box_top + bottom) / 2 - 0.01), m=crumb,
              bevel=0.008)
        for x in (-0.11, 0.11):
            k.cyl(0.072, 0.056, at=(x, y, lobe_z), rot=(90, 0, 0), m=crumb, bevel=0.008)

    # Lever on the right end: vertical slot and a handle that sticks out of it
    k.box((0.012, 0.035, 0.26), at=(W / 2 + 0.002, -0.04, base + 0.22), m=dark, bevel=0.004)
    k.box((0.022, 0.024, 0.04), at=(W / 2 + 0.012, -0.04, base + 0.30), m=steel, bevel=0.004)
    k.box((0.08, 0.075, 0.04), at=(W / 2 + 0.055, -0.04, base + 0.30), m=dark, bevel=0.015)

    # Browning dial on the front face near the right end
    k.cyl(0.062, 0.035, at=(0.19, -D / 2 - 0.012, base + 0.15), rot=(90, 0, 0), m=red, bevel=0.01)
    k.box((0.016, 0.02, 0.08), at=(0.19, -D / 2 - 0.035, base + 0.15), m=red, bevel=0.006)

    # Plain floor, a lighter pink than the backdrop
    k.box((6, 6, 0.1), at=(0, 1.0, -0.05), m=k.mat("#f6a3c8", "matte"), bevel=0, setting=True)
