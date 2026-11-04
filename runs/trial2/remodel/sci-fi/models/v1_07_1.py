# Moon rover: a boxy white body rides on two rocker beams, one per side. Each beam pivots on a bolt in the body's
# side and carries three black wheels on short axles: the front and rear wheels at its ends and the middle one on a
# strut. A mast rises from the front-left of the body top and holds the orange dish, which tilts toward the front
# and the camera. The small solar panel sits on a short post at the back right of the top, clear of the dish in the
# camera's view. The rover stands on a slab of gray moon dust. Its front faces -y, and the three-quarter view shows
# the front and the long right side.
SCENE = {"category": "3", "backdrop": "#a6e22e", "azimuth": 38, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f2", "satin")
    tire = k.mat("#1d1e22", "matte")
    hub = k.mat("#9aa0a8", "metal")
    frame = k.mat("#c9ced6", "metal")
    orange = k.mat("#ff8a1f", "satin")
    panel = k.mat("#24418f", "gloss")

    # Body: bottom at z = 0.22, top at z = 0.42.
    k.box((0.5, 0.76, 0.2), at=(0, 0, 0.32), m=white, bevel=0.035)

    wheel_r, wheel_w = 0.1, 0.09
    for side in (-1, 1):
        beam_x = side * 0.27
        # Rocker beam: its front and rear ends sit at axle height and its middle runs up the body side to the pivot.
        k.tube([(beam_x, -0.28, 0.1), (beam_x, -0.12, 0.26), (beam_x, 0.12, 0.26), (beam_x, 0.28, 0.1)],
               0.02, frame)
        k.tube([(beam_x, 0.0, 0.26), (beam_x, 0.0, 0.1)], 0.02, frame)
        # Pivot bolt from the body side through the beam.
        k.cyl(0.035, 0.05, at=(side * 0.27, 0.0, 0.26), rot=(0, 90, 0), m=hub)
        for y in (-0.28, 0.0, 0.28):
            # Axle stub from the beam into the wheel, then the tire and its hub cap.
            k.cyl(0.022, 0.08, at=(side * 0.3, y, wheel_r), rot=(0, 90, 0), m=frame)
            k.cyl(wheel_r, wheel_w, at=(side * 0.345, y, wheel_r), rot=(0, 90, 0), m=tire, bevel=0.02)
            k.cyl(0.045, 0.02, at=(side * (0.345 + wheel_w / 2), y, wheel_r), rot=(0, 90, 0), m=hub, bevel=0.006)

    # Dish antenna on a mast near the front left of the top. The dish axis after rot (35, 0, 15) is about
    # (0.149, -0.554, 0.819).
    mx, my = -0.12, -0.16
    k.cyl(0.04, 0.02, at=(mx, my, 0.43), m=frame)
    k.cyl(0.022, 0.2, at=(mx, my, 0.52), m=frame)
    dish = [(0.0, 0.0), (0.03, 0.002), (0.06, 0.012), (0.09, 0.028), (0.115, 0.048), (0.125, 0.06),
            (0.118, 0.064), (0.09, 0.046), (0.06, 0.032), (0.03, 0.024), (0.0, 0.022)]
    k.lathe(dish, at=(mx, my, 0.615), rot=(35, 0, 15), m=orange)
    # Feed rod standing out of the dish's center along its axis, with a small tip.
    k.cyl(0.012, 0.08, at=(mx + 0.009, my - 0.033, 0.664), rot=(35, 0, 15), m=frame)
    k.sphere(0.018, at=(mx + 0.015, my - 0.055, 0.697), m=orange)

    # Small solar panel on a short post at the back right of the top.
    k.cyl(0.02, 0.09, at=(0.1, 0.2, 0.465), m=frame)
    k.box((0.26, 0.18, 0.016), at=(0.1, 0.2, 0.515), rot=(-15, 0, 0), m=panel, bevel=0.004)

    # Gray moon dust surface, its top at z = 0, running off the card at the sides and ending behind the rover so
    # the lime backdrop shows above it.
    k.box((6, 3.2, 0.12), at=(0, 0.6, -0.06), m=k.mat("#85858b", "matte"), bevel=0.02, setting=True)
