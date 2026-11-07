# Office door: a dark wood door hangs in a wood-framed opening in a plaster corridor wall, on two hinges at its
# left edge. The top half is a frosted glass pane held in a raised wood frame, and the bottom half has two raised
# panels. A brass knob on a round plate sits at the right edge. A threshold joins the door to the tiled floor.
# The magnifier icon on the glass is a printed mark, so it is left to the image model.
SCENE = {"category": "4", "backdrop": "#3fc6d8", "azimuth": 22, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#4a2a17", "satin")
    trim = k.mat("#5a3420", "satin")
    glass = k.mat("#eef4f6", "glass")
    brass = k.mat("#d4a23c", "metal")
    wall = k.mat("#3fc6d8", "matte")

    W, H = 0.48, 1.0           # opening width and height
    hw = W / 2

    # Wall around the opening: face at y = 0, back at y = 0.12.
    k.box((1.6, 0.12, 1.6), at=(-hw - 0.8, 0.06, 0.8), m=wall, bevel=0.005, setting=True)
    k.box((1.6, 0.12, 1.6), at=(hw + 0.8, 0.06, 0.8), m=wall, bevel=0.005, setting=True)
    k.box((W + 0.02, 0.12, 0.6), at=(0, 0.06, H + 0.3), m=wall, bevel=0.005, setting=True)

    # Door frame trim on the wall face, and side and top boards lining the opening.
    c = 0.06
    for s in (-1, 1):
        k.box((c, 0.03, H + c), at=(s * (hw + c / 2), -0.015, (H + c) / 2), m=trim, bevel=0.008)
        k.box((0.02, 0.12, H), at=(s * (hw - 0.01), 0.06, H / 2), m=trim, bevel=0.003)
    k.box((W + 2 * c + 0.02, 0.035, c), at=(0, -0.0175, H + c / 2), m=trim, bevel=0.008)
    k.box((W, 0.12, 0.02), at=(0, 0.06, H - 0.01), m=trim, bevel=0.003)

    # The door itself, set back in the opening.
    L = W - 0.04
    lz = H - 0.02
    ly = 0.04
    k.box((L, 0.045, lz), at=(0, ly, lz / 2 + 0.005), m=wood, bevel=0.006)
    front = ly - 0.0225

    # Frosted glass pane in the top half with a raised wood frame around it.
    gx0, gx1, gz0, gz1 = -L / 2 + 0.07, L / 2 - 0.07, 0.56, lz - 0.07
    gw, gh = gx1 - gx0, gz1 - gz0
    k.box((gw, 0.012, gh), at=(0, front + 0.004, (gz0 + gz1) / 2), m=glass, bevel=0.002)
    f = 0.025
    for s in (-1, 1):
        k.box((f, 0.02, gh + 2 * f), at=(s * (gw / 2 + f / 2), front - 0.004, (gz0 + gz1) / 2), m=trim, bevel=0.004)
    for z in (gz0 - f / 2, gz1 + f / 2):
        k.box((gw + 2 * f, 0.02, f), at=(0, front - 0.004, z), m=trim, bevel=0.004)

    # Two raised panels in the bottom half.
    pw = (L - 0.14 - 0.05) / 2
    for s in (-1, 1):
        k.box((pw, 0.014, 0.36), at=(s * (pw / 2 + 0.025), front - 0.005, 0.25), m=trim, bevel=0.008)

    # Hinges on the left edge: a leaf plate on the door and a barrel at the gap to the frame.
    for z in (0.14, lz - 0.14):
        k.box((0.045, 0.006, 0.09), at=(-L / 2 + 0.005, front - 0.003, z), m=brass, bevel=0.002)
        k.cyl(0.013, 0.1, at=(-L / 2 - 0.005, front - 0.008, z), m=brass, bevel=0.002)

    # Brass knob on the right: round plate, neck, ball.
    kx, kz = L / 2 - 0.06, 0.48
    k.cyl(0.032, 0.01, at=(kx, front - 0.005, kz), rot=(90, 0, 0), m=brass, bevel=0.003)
    k.cyl(0.011, 0.035, at=(kx, front - 0.025, kz), rot=(90, 0, 0), m=brass, bevel=0.002)
    k.sphere(0.034, at=(kx, front - 0.055, kz), scale=(1, 0.85, 1), m=brass)

    # Threshold, baseboard on either side of the frame, and the tiled corridor floor.
    k.box((W, 0.1, 0.012), at=(0, 0.05, 0.006), m=trim, bevel=0.003)
    skirt = k.mat("#f2ead8", "satin")
    for s in (-1, 1):
        k.box((1.7, 0.03, 0.08), at=(s * 1.15, -0.015, 0.04), m=skirt, bevel=0.005, setting=True)
    k.box((4, 2.0, 0.02), at=(0, -1.0, -0.012), m=k.mat("#9a9488", "matte"), bevel=0, setting=True)  # grout
    t = 0.19
    for i in range(-10, 10):
        for j in range(8):
            col = "#e8dcc4" if (i + j) % 2 else "#cdbf9f"
            k.box((t - 0.012, t - 0.012, 0.02), at=(i * t + t / 2, -j * t - t / 2, -0.008),
                  m=k.mat(col, "gloss"), bevel=0.004, setting=True)
