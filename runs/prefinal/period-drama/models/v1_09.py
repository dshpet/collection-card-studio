# Velvet wingback armchair: an upholstered base box stands on four short turned wooden legs at its corners.
# The padded seat cushion rests on the base between the two arm panels. Each arm panel rises from the base and is
# topped by a rolled arm that runs front to back and ends in a round scroll face. The tall back leans back slightly
# and rises from the rear of the base; the two wings join its sides above the arms and flare out toward the front.
# Gold buttons are set into the back's front face in a tufted diamond pattern. The chair stands on a polished
# plank floor that ends in an edge behind it, as on the real cards.
import math

SCENE = {"category": "3", "backdrop": "#3cc8e8", "azimuth": 30, "elevation": 13, "lens": 60, "light": "left"}


def build(k):
    velvet = k.mat("#8e1424", "matte")
    velvet_dark = k.mat("#741020", "matte")
    wood = k.mat("#6b3a1c", "satin")
    gold = k.mat("#e3b23c", "metal")

    # Four short carved legs: turned profile, foot on the floor, top tucked into the base.
    leg = [(0.0, 0.0), (0.03, 0.0), (0.034, 0.012), (0.026, 0.03), (0.022, 0.055), (0.03, 0.075),
           (0.038, 0.09), (0.032, 0.105), (0.04, 0.12), (0.045, 0.15), (0.0, 0.15)]
    for x in (-0.32, 0.32):
        for y in (-0.28, 0.27):
            k.lathe(leg, at=(x, y, 0.0), rot=(0, 0, 0), m=wood)

    # Upholstered base (seat box) on the legs: z 0.14 to 0.31.
    k.box((0.80, 0.72, 0.17), at=(0, -0.01, 0.225), m=velvet, bevel=0.03)
    # Thin wooden skirt rail at the bottom of the base front.
    k.box((0.80, 0.03, 0.03), at=(0, -0.37, 0.15), m=wood, bevel=0.008)

    # Padded seat cushion on the base, between the arms.
    k.box((0.58, 0.60, 0.11), at=(0, -0.05, 0.355), m=velvet, bevel=0.045)

    # Tall back, leaning back 6 degrees, rising from the rear of the base.
    tilt = -6.0
    back_c = (0.0, 0.29, 0.69)
    back_h = 0.80
    k.box((0.64, 0.14, back_h), at=back_c, rot=(tilt, 0, 0), m=velvet, bevel=0.06)
    # Rounded top roll of the back.
    a = math.radians(tilt)
    top_local = back_h / 2 - 0.03
    top_y = back_c[1] - top_local * math.sin(a)
    top_z = back_c[2] + top_local * math.cos(a)
    k.cyl(0.075, 0.64, at=(0, top_y, top_z), rot=(0, 90, 0), m=velvet, bevel=0.03)

    # Gold tufting buttons on the back's front face, diamond pattern.
    def on_back(dx, dz):
        ly = -0.07
        y = back_c[1] + ly * math.cos(a) - dz * math.sin(a)
        z = back_c[2] + ly * math.sin(a) + dz * math.cos(a)
        return (dx, y, z)

    for dz, xs in ((0.22, (-0.15, 0.0, 0.15)), (0.08, (-0.075, 0.075)), (-0.06, (-0.15, 0.0, 0.15))):
        for dx in xs:
            k.sphere(0.02, at=on_back(dx, dz), scale=(1, 0.6, 1), m=gold)

    for side in (-1, 1):
        # Arm panel rising from the base.
        k.box((0.12, 0.64, 0.22), at=(side * 0.35, -0.03, 0.40), m=velvet, bevel=0.03)
        # Rolled arm on top, running front to back.
        k.cyl(0.08, 0.66, at=(side * 0.37, -0.04, 0.51), rot=(90, 0, 0), m=velvet, bevel=0.03)
        # Round scroll face at the front of the roll.
        k.cyl(0.07, 0.03, at=(side * 0.37, -0.375, 0.505), rot=(90, 0, 0), m=velvet_dark, bevel=0.012)
        # Wing: joins the back's side above the arm and flares out toward the front.
        k.box((0.09, 0.30, 0.50), at=(side * 0.355, 0.15, 0.80), rot=(-4, 0, side * 10), m=velvet, bevel=0.04)

    # Polished plank floor: boards running toward the camera, ending in an edge behind the chair.
    floor_cols = ("#c4824a", "#b8763f", "#cc8b52")
    w = 0.36
    for i in range(-7, 8):
        k.box((w - 0.008, 3.0, 0.06), at=(i * w, -0.6, -0.03), m=k.mat(floor_cols[i % 3], "gloss"),
              bevel=0.004, setting=True)
