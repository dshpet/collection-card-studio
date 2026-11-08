# Vintage squad car: a rounded sedan body on four wheels, black hood, trunk and fenders, white doors and roof.
# The tapered glass cabin sits on the body with pillars running from the belt line to the roof; the red light
# stands on a short base in the middle of the roof. Chrome bumpers span the nose and tail, each held on two
# brackets bolted into the body. It is parked on asphalt beside a curb, with the pavement behind it. The door's
# house pictogram is a printed mark, so it is left to the image model.
SCENE = {"category": "4", "backdrop": "#5cc8f2", "azimuth": 32, "elevation": 9, "lens": 55, "light": "left"}


def build(k):
    black = k.mat("#1d1f24", "gloss")
    white = k.mat("#f4f4f0", "gloss")
    glass = k.mat("#7fb6d6", "glass")
    chrome = k.mat("#cfd4da", "metal")
    tyre = k.mat("#2a2a2c", "matte")

    # Four wheels on axles along x, chrome hubcaps through them.
    for x in (-0.19, 0.19):
        for y in (-0.32, 0.32):
            k.cyl(0.08, 0.06, at=(x, y, 0.08), rot=(0, 90, 0), m=tyre, bevel=0.015)
            k.cyl(0.045, 0.066, at=(x, y, 0.08), rot=(0, 90, 0), m=chrome, bevel=0.01)

    # Lower body: black nose and tail, white door section between them.
    k.box((0.38, 1.0, 0.13), at=(0, 0, 0.175), m=black, bevel=0.045)
    k.box((0.388, 0.40, 0.128), at=(0, 0.03, 0.176), m=white, bevel=0.03)
    # Smooth hood in front of the cabin and trunk behind it, resting on the body.
    k.box((0.34, 0.27, 0.04), at=(0, -0.355, 0.255), m=black, bevel=0.018)
    k.box((0.34, 0.21, 0.04), at=(0, 0.385, 0.255), m=black, bevel=0.018)

    # Rounded fenders over the top of each wheel, set close into the body sides.
    for x in (-0.17, 0.17):
        for y in (-0.32, 0.32):
            k.blob([(x, y, 0.2, 0.1, (0.45, 1.4, 0.5))], black)

    # Cabin: a glass greenhouse on the belt line, tapering toward the roof.
    cabin = k.box((0.36, 0.48, 0.13), at=(0, 0.04, 0.305), m=glass, bevel=0.02)

    def taper(p):
        x, y, z = p
        f = (z + 0.065) / 0.13
        return (x * (1 - 0.17 * f), y * (1 - 0.29 * f) - 0.01 * f, z)

    k.warp(cabin, taper)
    k.box((0.31, 0.37, 0.03), at=(0, 0.03, 0.375), m=white, bevel=0.012)
    for sx in (-1, 1):
        k.tube([(sx * 0.18, -0.2, 0.24), (sx * 0.15, -0.14, 0.37)], 0.012, white)
        k.tube([(sx * 0.18, 0.28, 0.24), (sx * 0.15, 0.20, 0.37)], 0.012, white)
        k.tube([(sx * 0.18, 0.03, 0.24), (sx * 0.15, 0.03, 0.37)], 0.012, white)
        # Door handles on the white doors.
        k.box((0.012, 0.04, 0.012), at=(sx * 0.196, -0.07, 0.215), m=chrome, bevel=0.004)
        k.box((0.012, 0.04, 0.012), at=(sx * 0.196, 0.18, 0.215), m=chrome, bevel=0.004)

    # Roof light: short black base on the roof, red dome on the base.
    k.cyl(0.04, 0.02, at=(0, 0.04, 0.4), m=black, bevel=0.005)
    k.lathe([(0.032, 0), (0.032, 0.03), (0.028, 0.045), (0.018, 0.058), (0, 0.062)],
            at=(0, 0.04, 0.41), m=k.mat("#e8262b", "glow"))

    # Chrome bumpers on two brackets each, set into the nose and tail of the body.
    for sy in (-1, 1):
        k.cyl(0.022, 0.44, at=(0, sy * 0.51, 0.13), rot=(0, 90, 0), m=chrome, bevel=0.008)
        for x in (-0.12, 0.12):
            k.box((0.03, 0.06, 0.03), at=(x, sy * 0.48, 0.14), m=chrome, bevel=0.005)
    # Grille, headlights in the front of the body, tail lights.
    k.box((0.14, 0.02, 0.06), at=(0, -0.502, 0.18), m=chrome, bevel=0.008)
    for x in (-0.14, 0.14):
        k.cyl(0.035, 0.03, at=(x, -0.49, 0.2), rot=(90, 0, 0), m=chrome, bevel=0.006)
        k.cyl(0.026, 0.01, at=(x, -0.507, 0.2), rot=(90, 0, 0), m=k.mat("#fff4c8", "glow"))
        k.cyl(0.018, 0.01, at=(x, 0.505, 0.2), rot=(90, 0, 0), m=k.mat("#c81e22", "gloss"))

    # Setting: asphalt street, the curb on the car's left, and the pavement beyond it.
    k.box((10, 10, 0.04), at=(0, 0, -0.02), m=k.mat("#4a4d55", "matte"), bevel=0, setting=True)
    k.box((0.1, 10, 0.1), at=(-0.37, 0, 0.05), m=k.mat("#a9a69d", "matte"), bevel=0.01, setting=True)
    k.box((4, 10, 0.1), at=(-2.42, 0, 0.05), m=k.mat("#8e8a82", "matte"), bevel=0.01, setting=True)
