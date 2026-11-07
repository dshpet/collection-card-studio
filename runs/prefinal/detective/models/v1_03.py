# Vintage press camera: a black box body with a black bellows stepping forward to a lens board, which carries the
# lens barrel, a silver lens ring and a round glass front lens. A silver post rises from the top plate and holds
# the round flash dish facing forward, with a bulb at its centre. The red shutter button sits on a silver collar on
# the top plate. Category 1: it floats, turned a little to show the front with the lens and the right side, and
# tipped forward so the top with the button and flash shows.
SCENE = {"category": "1", "backdrop": "#2fd6e6", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#1b1c20", "satin")
    leather = k.mat("#26272c", "matte")
    silver = k.mat("#c9ced6", "metal")
    glass = k.mat("#9fd3ea", "glass")
    red = k.mat("#e0262b", "gloss")

    # Body: black box, front face at y = -0.175, top at z = 0.55.
    k.box((0.70, 0.35, 0.50), at=(0, 0, 0.30), m=leather, bevel=0.03)
    k.box((0.72, 0.37, 0.03), at=(0, 0, 0.545), m=black, bevel=0.01)  # top plate
    k.box((0.72, 0.37, 0.03), at=(0, 0, 0.055), m=black, bevel=0.01)  # bottom plate

    # Bellows: stepped folds from the body front to the lens board.
    for i, (s, y) in enumerate([(0.40, -0.195), (0.37, -0.23), (0.34, -0.265), (0.31, -0.30), (0.28, -0.33)]):
        k.box((s, 0.04, s), at=(0, y, 0.30), m=leather if i % 2 else black, bevel=0.012)

    # Lens board and lens.
    k.box((0.32, 0.03, 0.32), at=(0, -0.36, 0.30), m=black, bevel=0.012)
    k.cyl(0.115, 0.10, at=(0, -0.42, 0.30), rot=(90, 0, 0), m=black, bevel=0.01)
    k.cyl(0.125, 0.03, at=(0, -0.385, 0.30), rot=(90, 0, 0), m=silver, bevel=0.006)
    k.torus(0.115, 0.024, at=(0, -0.47, 0.30), rot=(90, 0, 0), m=silver)
    k.sphere(0.096, at=(0, -0.468, 0.30), scale=(1, 0.35, 1), m=glass)

    # Flash dish on top: a post from the top plate holds the dish, which opens toward the front (-y).
    k.cyl(0.022, 0.25, at=(-0.18, 0.06, 0.675), m=silver)
    k.cyl(0.035, 0.03, at=(-0.18, 0.06, 0.56), m=silver)
    dish = [(0.0, 0.0), (0.035, 0.0), (0.06, 0.015), (0.09, 0.035), (0.12, 0.06), (0.145, 0.09),
            (0.165, 0.12), (0.155, 0.125), (0.135, 0.098), (0.11, 0.07), (0.08, 0.047), (0.05, 0.03),
            (0.02, 0.022), (0.0, 0.022)]
    k.lathe(dish, at=(-0.18, 0.04, 0.80), rot=(90, 0, 0), m=silver)
    k.cyl(0.012, 0.04, at=(-0.18, 0.0, 0.80), rot=(90, 0, 0), m=silver)
    k.sphere(0.03, at=(-0.18, -0.03, 0.80), m=k.mat("#f4f7fb", "glass"))

    # Red shutter button on a silver collar.
    k.cyl(0.04, 0.025, at=(0.22, -0.06, 0.572), m=silver, bevel=0.005)
    k.cyl(0.03, 0.035, at=(0.22, -0.06, 0.60), m=red, bevel=0.008)

    k.turn(10, 0, -8)
