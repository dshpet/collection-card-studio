# Moon rover: a flat white box body sits on six short legs, three per side; each leg drops to an axle that
# carries a black wheel resting on the sand. A short mast is fixed to the top of the body and carries a small
# yellow dish, tilted up toward the front, with a feed rod at its centre. A pale sand slab runs off the card;
# its front edge shows near the bottom, like the table edges on the reference cards.
SCENE = {"category": "3", "backdrop": "#4fb3ef", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    grey = k.mat("#b9bec6", "metal")
    tire = k.mat("#1e1f22", "matte")
    yellow = k.mat("#ffc21f", "satin")

    # Body: flat box, underside at z = 0.27.
    k.box((1.0, 0.56, 0.2), at=(0, 0, 0.37), m=white, bevel=0.03)

    wheel_r, wheel_w = 0.13, 0.09
    for x in (-0.36, 0.0, 0.36):
        for side in (-1, 1):
            # Leg from body underside down to the axle.
            k.box((0.06, 0.06, 0.16), at=(x, side * 0.24, 0.2), m=grey, bevel=0.01)
            # Axle from the leg out to the wheel hub.
            k.cyl(0.025, 0.16, at=(x, side * 0.31, wheel_r), rot=(90, 0, 0), m=grey)
            # Wheel resting on the ground, with a white hub cap.
            k.cyl(wheel_r, wheel_w, at=(x, side * 0.37, wheel_r), rot=(90, 0, 0), m=tire, bevel=0.02)
            k.cyl(0.055, 0.02, at=(x, side * (0.37 + wheel_w / 2 + 0.005), wheel_r), rot=(90, 0, 0),
                  m=white, bevel=0.005)

    # Mast fixed to the top of the body.
    mx, my, top = -0.28, 0.08, 0.47
    k.cyl(0.05, 0.03, at=(mx, my, top + 0.015), m=grey, bevel=0.005)
    k.cyl(0.025, 0.2, at=(mx, my, top + 0.1), m=grey)

    # Dish on the mast top, tilted up toward the front (-y).
    dish_at = (mx, my, top + 0.2)
    profile = [(0.0, 0.0), (0.03, 0.002), (0.06, 0.008), (0.09, 0.019), (0.12, 0.034), (0.15, 0.053),
               (0.15, 0.065), (0.12, 0.046), (0.09, 0.031), (0.06, 0.020), (0.03, 0.014), (0.0, 0.012)]
    k.lathe(profile, at=dish_at, rot=(35, 0, 0), m=yellow)
    k.sphere(0.03, at=dish_at, m=grey)
    # Feed rod from the dish centre along its axis, with a small tip.
    k.tube([(mx, my, top + 0.21), (mx, my - 0.057, top + 0.292)], 0.01, grey)
    k.sphere(0.02, at=(mx, my - 0.06, top + 0.296), m=yellow)

    # Pale sand slab, top at z = 0, front edge visible near the bottom of the card.
    k.box((6, 3, 0.3), at=(0, 0.7, -0.15), m=k.mat("#ecd9a6", "matte"), bevel=0.03, setting=True)
