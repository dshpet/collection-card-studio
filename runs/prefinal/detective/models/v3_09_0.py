# Yellow taxi: a rounded lower body on four wheels, a glass cabin with a sloped windshield and rear window under
# a yellow roof, a B-pillar on each side, and the roof lamp on a small base on the roof. A black band runs along
# each side, silver bumpers at both ends, warm glowing headlights and red tail lights. The car stands on the asphalt
# with its near side to the camera; the curb and pavement run behind it along the far side.
SCENE = {"category": "4", "backdrop": "#8a5cc8", "azimuth": 35, "elevation": 10, "lens": 55, "light": "left"}


def build(k):
    yellow = k.mat("#ffc61a", "satin")
    black = k.mat("#1c1c1f", "satin")
    silver = k.mat("#c9ced6", "metal")
    glass = k.mat("#2b3a4f", "glass")
    tire = k.mat("#222226", "matte")

    # Lower body, front at +x
    k.box((1.0, 0.44, 0.17), at=(0, 0, 0.155), m=yellow, bevel=0.04)
    # Cabin: top corners pulled in for the sloped windshield and rear window
    cabin = k.box((0.56, 0.40, 0.17), at=(-0.04, 0, 0.325), m=glass, bevel=0.015)

    def slope(p):
        x, y, z = p
        if z > 0:
            x = x - 0.10 if x > 0 else x + 0.07
            y *= 0.88
        return (x, y, z)

    k.warp(cabin, slope)
    k.box((0.40, 0.37, 0.025), at=(-0.055, 0, 0.42), m=yellow, bevel=0.01)
    k.box((0.04, 0.385, 0.165), at=(-0.04, 0, 0.325), m=yellow, bevel=0.005)

    # Roof lamp on its base
    k.box((0.13, 0.05, 0.012), at=(-0.055, 0, 0.438), m=black, bevel=0.003)
    k.box((0.15, 0.06, 0.05), at=(-0.055, 0, 0.469), m=k.mat("#fff2b8", "glow"), bevel=0.012)

    # Black checker band along both sides
    k.box((0.9, 0.452, 0.045), at=(0, 0, 0.2), m=black, bevel=0.004)

    # Bumpers, grille, lights
    for x in (0.51, -0.51):
        k.box((0.05, 0.46, 0.05), at=(x, 0, 0.095), m=silver, bevel=0.015)
    k.box((0.012, 0.18, 0.05), at=(0.502, 0, 0.155), m=black, bevel=0.003)
    for y in (-0.15, 0.15):
        k.cyl(0.032, 0.02, at=(0.498, y, 0.17), rot=(0, 90, 0), m=k.mat("#ffd27a", "glow"))
    for y in (-0.17, 0.17):
        k.box((0.012, 0.06, 0.04), at=(-0.502, y, 0.18), m=k.mat("#d8262b", "gloss"), bevel=0.004)

    # Side mirrors on the doors at the windshield base
    for s in (-1, 1):
        k.box((0.025, 0.04, 0.012), at=(0.16, s * 0.235, 0.255), m=black, bevel=0.003)
        k.box((0.035, 0.035, 0.03), at=(0.16, s * 0.265, 0.27), m=yellow, bevel=0.008)

    # Four wheels with silver hubs
    for x in (0.32, -0.32):
        for y in (-0.19, 0.19):
            k.cyl(0.085, 0.07, at=(x, y, 0.085), rot=(90, 0, 0), m=tire, bevel=0.015)
            k.cyl(0.045, 0.076, at=(x, y, 0.085), rot=(90, 0, 0), m=silver, bevel=0.006)

    # Setting: asphalt street, curb and pavement behind the car
    k.box((8, 8, 0.1), at=(0, 0, -0.05), m=k.mat("#4b4a56", "matte"), bevel=0, setting=True)
    k.box((8, 0.08, 0.1), at=(0, 0.42, 0.05), m=k.mat("#b8b4bc", "matte"), bevel=0.01, setting=True)
    k.box((8, 3, 0.09), at=(0, 1.96, 0.045), m=k.mat("#d9c8d4", "matte"), bevel=0.005, setting=True)
