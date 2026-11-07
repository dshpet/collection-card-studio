# Vintage squad car: a rounded 1950s sedan parked on an asphalt street beside a pavement curb. Black body with
# white doors and roof; four wheels on two axles sit in rounded fenders; a glass cabin tapers up to the roof, which
# carries one red light on a short base; chrome bumpers wrap the front and rear. The front faces -y. The door's house
# pictogram is a printed mark and is left to the image model.
SCENE = {"category": "4", "backdrop": "#5ec8f2", "azimuth": 32, "elevation": 10, "lens": 55, "light": "left"}


def build(k):
    black = k.mat("#16171b", "gloss")
    white = k.mat("#f4f4f0", "gloss")
    chrome = k.mat("#c9ced6", "metal")
    tyre = k.mat("#2a2a2e", "matte")
    glass = k.mat("#9fd6ee", "glass")
    red = k.mat("#e8262b", "glow")

    # Wheels on two axles, hubcaps outside.
    for y in (-0.31, 0.31):
        k.cyl(0.018, 0.36, at=(0, y, 0.085), rot=(0, 90, 0), m=chrome)
        for side in (-1, 1):
            k.cyl(0.085, 0.06, at=(side * 0.18, y, 0.085), rot=(0, 90, 0), m=tyre, bevel=0.015)
            k.cyl(0.05, 0.012, at=(side * 0.212, y, 0.085), rot=(0, 90, 0), m=chrome, bevel=0.004)

    # Lower body and rounded fenders over each wheel.
    k.box((0.38, 0.98, 0.15), at=(0, 0, 0.175), m=black, bevel=0.05)
    for y in (-0.31, 0.31):
        for side in (-1, 1):
            k.blob([(side * 0.17, y, 0.19, 0.1, (0.55, 1.35, 0.75))], black)

    # White doors on both sides between the fenders.
    for side in (-1, 1):
        k.box((0.012, 0.36, 0.13), at=(side * 0.192, 0.02, 0.18), m=white, bevel=0.01)
        k.box((0.016, 0.05, 0.012), at=(side * 0.2, -0.08, 0.215), m=chrome, bevel=0.003)  # door handle

    # Cabin: tapered glass greenhouse, white roof, pillars.
    cabin = k.box((0.34, 0.48, 0.14), at=(0, 0.05, 0.315), m=glass, bevel=0.02)
    k.warp(cabin, lambda p: (p[0] * (0.88 if p[2] > 0 else 1.0), p[1] * (0.78 if p[2] > 0 else 1.0), p[2]))
    k.box((0.31, 0.39, 0.03), at=(0, 0.05, 0.395), m=white, bevel=0.012)
    for side in (-1, 1):
        k.tube([(side * 0.165, -0.19, 0.25), (side * 0.148, -0.137, 0.385)], 0.012, white)
        k.tube([(side * 0.165, 0.29, 0.25), (side * 0.148, 0.237, 0.385)], 0.012, white)
        k.tube([(side * 0.168, 0.05, 0.25), (side * 0.15, 0.05, 0.385)], 0.01, white)

    # Roof light: short chrome base and a single red dome.
    k.cyl(0.035, 0.015, at=(0, 0.03, 0.418), m=chrome)
    k.lathe([(0.0, 0.0), (0.03, 0.0), (0.03, 0.03), (0.025, 0.05), (0.014, 0.06), (0.0, 0.063)],
            at=(0, 0.03, 0.425), m=red)

    # Front: grille, round headlights. Rear: tail lights.
    k.box((0.2, 0.02, 0.06), at=(0, -0.49, 0.16), m=chrome, bevel=0.01)
    for side in (-1, 1):
        k.cyl(0.032, 0.02, at=(side * 0.13, -0.487, 0.2), rot=(90, 0, 0), m=chrome, bevel=0.005)
        k.cyl(0.024, 0.01, at=(side * 0.13, -0.499, 0.2), rot=(90, 0, 0), m=k.mat("#fff4c8", "glow"))
        k.cyl(0.022, 0.02, at=(side * 0.14, 0.488, 0.2), rot=(90, 0, 0), m=k.mat("#c81e22", "gloss"))

    # Chrome bumpers front and rear.
    for y in (-0.5, 0.5):
        k.cyl(0.024, 0.42, at=(0, y, 0.11), rot=(0, 90, 0), m=chrome, bevel=0.01)

    # Setting: asphalt street with a curb and pavement along the car's left side.
    k.box((10, 10, 0.02), at=(0, 0, -0.01), m=k.mat("#4b4e55", "matte"), bevel=0, setting=True)
    k.box((0.14, 10, 0.08), at=(-0.42, 0, 0.04), m=k.mat("#c8c6c0", "matte"), bevel=0.01, setting=True)
    k.box((4, 10, 0.07), at=(-2.49, 0, 0.035), m=k.mat("#b9b3a8", "matte"), bevel=0.0, setting=True)
