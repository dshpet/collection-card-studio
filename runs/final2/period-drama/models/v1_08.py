# Steamer trunk: a wooden body box with a flat lid on top, split by a raised rim band. Two tan leather straps
# run up the front, over the lid and down the back, each with a brass buckle on the front. Brass caps guard all
# eight corners, a brass latch closes the lid at the front centre, and a green leather handle hangs from two
# brass plates on each end. It stands on a floor of grey stone flags of the station platform.
SCENE = {"category": "3", "backdrop": "#5cc4f2", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#7a301a", "matte")
    trim = k.mat("#4e1d0f", "matte")
    leather = k.mat("#c99a5b", "matte")
    brass = k.mat("#d4a537", "metal")
    green = k.mat("#2f5e34", "matte")

    W, D, H = 1.0, 0.56, 0.62
    seam = 0.44
    # body and lid
    k.box((W, D, seam), at=(0, 0, seam / 2), m=wood, bevel=0.012)
    k.box((W, D, H - seam - 0.01), at=(0, 0, seam + 0.01 + (H - seam - 0.01) / 2), m=wood, bevel=0.012)
    # rim bands at the lid seam and around the base
    k.box((W + 0.016, D + 0.016, 0.05), at=(0, 0, seam), m=trim, bevel=0.008)
    k.box((W + 0.016, D + 0.016, 0.04), at=(0, 0, 0.02), m=trim, bevel=0.008)
    # vertical wooden battens on front and back
    for x in (-0.42, 0.42):
        for y in (-1, 1):
            k.box((0.05, 0.016, H - 0.02), at=(x, y * (D / 2 + 0.008), H / 2), m=trim, bevel=0.005)

    # brass corner guards on all eight corners
    g = 0.09
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (g / 2 - 0.004, H - g / 2 + 0.004):
                k.box((g, g, g), at=(x * (W / 2 - g / 2 + 0.008), y * (D / 2 - g / 2 + 0.008), z),
                      m=brass, bevel=0.012)

    # two straps wrapping front, top and back
    t = 0.014
    for x in (-0.25, 0.25):
        for y in (-1, 1):
            k.box((0.085, t, H), at=(x, y * (D / 2 + 0.017), H / 2), m=leather, bevel=0.004)
        k.box((0.085, D + 0.048, t), at=(x, 0, H + t / 2), m=leather, bevel=0.004)
        # buckle on the front of each strap
        fy = -(D / 2 + 0.03)
        k.tube([(x - 0.06, fy, 0.26), (x + 0.06, fy, 0.26), (x + 0.06, fy, 0.36),
                (x - 0.06, fy, 0.36), (x - 0.06, fy, 0.26)], 0.012, brass)
        k.cyl(0.007, 0.1, at=(x, fy, 0.31), rot=(0, 0, 0), m=brass)

    # front latch over the lid seam
    k.box((0.12, 0.02, 0.1), at=(0, -(D / 2 + 0.018), seam - 0.05), m=brass, bevel=0.006)
    k.box((0.07, 0.022, 0.12), at=(0, -(D / 2 + 0.026), seam + 0.04), m=brass, bevel=0.008)
    k.cyl(0.018, 0.012, at=(0, -(D / 2 + 0.034), seam - 0.04), rot=(90, 0, 0), m=brass)

    # end handles: brass plates and a hanging green leather loop on each end
    for s in (-1, 1):
        x0 = s * (W / 2 + 0.01)
        for y in (-0.12, 0.12):
            k.box((0.02, 0.07, 0.07), at=(x0, y, 0.42), m=brass, bevel=0.006)
        k.tube([(x0 + s * 0.012, -0.12, 0.42), (x0 + s * 0.04, -0.09, 0.37), (x0 + s * 0.05, 0, 0.345),
                (x0 + s * 0.04, 0.09, 0.37), (x0 + s * 0.012, 0.12, 0.42)], 0.02, green, curved=True)

    # stone platform: grout bed with grey flagstones
    k.box((8, 8, 0.1), at=(0, 0, -0.06), m=k.mat("#4f4c48", "matte"), bevel=0, setting=True)
    stones = ("#8e8a82", "#7f7b74", "#999489")
    s = 0.6
    for i in range(-6, 7):
        for j in range(-4, 9):
            k.box((s - 0.025, s - 0.025, 0.06), at=(i * s + (j % 2) * s / 2, j * s, -0.03),
                  m=k.mat(stones[(i + j) % 3], "matte"), bevel=0.01, setting=True)
