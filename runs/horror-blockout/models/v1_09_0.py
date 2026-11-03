# Black cat sitting on a wooden table: one soft body from haunches, chest, neck and head, with the front legs
# reaching the table on round paws. Pointed ears sink into the top of the head; big round yellow eyes sit on the
# face. A small red collar rings the neck. The tail starts at the rump and curls around the right side, lying on
# the table, with its tip lifting by the front paws. The table is a few long planks that run off the card.
SCENE = {"category": "3", "backdrop": "#ffb21e", "azimuth": 28, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    fur = k.mat("#1d1c22", "matte")
    eye = k.mat("#ffd21f", "gloss")
    pupil = k.mat("#0b0b0e", "gloss")
    nose = k.mat("#3a2e33", "satin")
    collar = k.mat("#e0262b", "satin")

    k.blob([
        (0, 0.06, 0.28, 0.2, (1.0, 1.15, 1.25)),
        (-0.14, 0.1, 0.16, 0.15, (1.0, 1.25, 0.95)),
        (0.14, 0.1, 0.16, 0.15, (1.0, 1.25, 0.95)),
        (0, -0.07, 0.42, 0.16),
        (0, -0.05, 0.56, 0.12),
        (0, -0.08, 0.72, 0.2, (1.1, 0.95, 0.92)),
        (-0.04, -0.25, 0.66, 0.05),
        (0.04, -0.25, 0.66, 0.05),
        (-0.075, -0.12, 0.3, 0.06, (1, 1, 1.6)),
        (0.075, -0.12, 0.3, 0.06, (1, 1, 1.6)),
        (-0.075, -0.14, 0.14, 0.05, (1, 1, 1.8)),
        (0.075, -0.14, 0.14, 0.05, (1, 1, 1.8)),
        (-0.075, -0.18, 0.035, 0.045, (1, 1.4, 0.8)),
        (0.075, -0.18, 0.035, 0.045, (1, 1.4, 0.8)),
    ], fur)

    for side in (-1, 1):
        k.cone(0.075, 0.006, 0.16, at=(side * 0.135, -0.07, 0.915), rot=(-8, side * 20, 0), m=fur)
        k.sphere(0.062, at=(side * 0.085, -0.235, 0.755), scale=(1, 0.55, 1.1), m=eye)
        k.sphere(0.034, at=(side * 0.085, -0.265, 0.755), scale=(0.75, 0.35, 1.15), m=pupil)
    k.sphere(0.022, at=(0, -0.295, 0.69), scale=(1.2, 0.7, 0.8), m=nose)

    k.torus(0.13, 0.022, at=(0, -0.05, 0.575), rot=(-12, 0, 0), m=collar)

    k.tube([(0.04, 0.3, 0.1), (0.17, 0.3, 0.045), (0.29, 0.16, 0.035), (0.31, -0.04, 0.035),
            (0.25, -0.2, 0.038), (0.16, -0.27, 0.06), (0.12, -0.27, 0.12)], 0.036, fur, curved=True)

    for i in range(7):
        x = -0.99 + i * 0.33
        shade = "#c9843c" if i % 2 else "#d4924a"
        k.box((0.32, 3.0, 0.1), at=(x, 0.4, -0.05), m=k.mat(shade, "matte"), bevel=0.012, setting=True)
