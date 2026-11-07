# Two-slot toaster: a rounded silver body stands on four small feet. Two slots run along its top, and a golden
# toast slice stands in each, popped halfway out. The lever rides in a vertical track on the right end face, with
# the red dial below it on the same face. It stands on a plain pink floor.
SCENE = {"category": "2", "backdrop": "#f06aa8", "azimuth": 32, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    steel = k.mat("#d4d8de", "metal")
    dark = k.mat("#2b2d33", "satin")
    black = k.mat("#3a3c42", "satin")
    red = k.mat("#e3262f", "gloss")
    bread = k.mat("#f2c867", "matte")
    crust = k.mat("#c9862e", "matte")

    # body on feet
    w, d, h, base = 0.62, 0.34, 0.40, 0.03
    top = base + h
    k.box((w, d, h), at=(0, 0, base + h / 2), m=steel, bevel=0.08)
    for x in (-0.24, 0.24):
        for y in (-0.12, 0.12):
            k.cyl(0.03, base + 0.01, at=(x, y, (base + 0.01) / 2), m=black, bevel=0.006)

    # two slots along the top, each holding a popped-up toast slice
    for y in (-0.075, 0.075):
        k.box((0.46, 0.06, 0.012), at=(0, y, top - 0.002), m=dark, bevel=0.004)
        # slice: crust rim around the crumb, square lower body and a two-lobed crown
        k.box((0.36, 0.036, 0.26), at=(0, y, 0.42), m=crust, bevel=0.012)
        for x in (-0.09, 0.09):
            k.cyl(0.095, 0.036, at=(x, y, 0.55), rot=(90, 0, 0), m=crust, bevel=0.012)
        k.box((0.32, 0.04, 0.22), at=(0, y, 0.43), m=bread, bevel=0.01)
        for x in (-0.09, 0.09):
            k.cyl(0.075, 0.04, at=(x, y, 0.55), rot=(90, 0, 0), m=bread, bevel=0.01)

    # right end face: lever track and lever on a stem, dial with a grip ridge below
    face = w / 2
    k.box((0.012, 0.035, 0.24), at=(face + 0.002, 0, 0.29), m=dark, bevel=0.004)
    k.box((0.04, 0.02, 0.025), at=(face + 0.02, 0, 0.34), m=steel, bevel=0.005)
    k.box((0.06, 0.13, 0.045), at=(face + 0.065, 0, 0.34), m=black, bevel=0.015)
    k.cyl(0.06, 0.03, at=(face + 0.015, -0.08, 0.13), rot=(0, 90, 0), m=red, bevel=0.008)
    k.box((0.025, 0.018, 0.08), at=(face + 0.035, -0.08, 0.13), m=red, bevel=0.006)

    k.turn(0, 0, -8)
    k.box((6, 4, 0.12), at=(0, 0.8, -0.06), m=k.mat("#f78fc2", "matte"), bevel=0.01, setting=True)
