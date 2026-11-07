# Leather briefcase standing upright on its bottom edge on four brass studs. A front flap is one piece of leather:
# it hinges at the back of the top, runs forward over the top, rolls over the front edge and hangs down the front.
# Two brass clasps sit on the flap's lower edge and latch onto catch plates on the body. The leather top handle
# runs between two brass rings held by brass mounts on the flap's top. Cream piping traces the flap edge.
SCENE = {"category": "2", "backdrop": "#6b2a9e", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#7a4524", "matte")
    flap_m = k.mat("#6a3a1d", "matte")
    brass = k.mat("#d4a838", "metal")
    cream = k.mat("#f1e3c2", "matte")

    W, D, H, foot = 0.9, 0.24, 0.62, 0.022
    zc = foot + H / 2
    top = foot + H
    k.box((W, D, H), at=(0, 0, zc), m=leather, bevel=0.04)

    # Brass studs under the four bottom corners
    for x in (-0.36, 0.36):
        for y in (-0.07, 0.07):
            k.cyl(0.024, foot + 0.004, at=(x, y, foot / 2), m=brass, bevel=0.004)

    # Front flap, one piece: top panel from the back hinge, a rolled fold over the front edge, front panel down
    FW = W - 0.04
    fy = -D / 2 - 0.01
    k.box((FW, 0.022, 0.25), at=(0, fy, top - 0.115), m=flap_m, bevel=0.01)
    k.box((FW, 0.19, 0.022), at=(0, -0.045, top + 0.006), m=flap_m, bevel=0.008)
    k.cyl(0.02, FW, at=(0, fy + 0.006, top - 0.002), rot=(0, 90, 0), m=flap_m, bevel=0.006)
    # Cream piping along the flap's sides and lower edge
    py = fy - 0.012
    x0, x1 = -FW / 2 + 0.03, FW / 2 - 0.03
    zb, zt = top - 0.225, top - 0.03
    k.tube([(x0, py, zt), (x0, py, zb), (x1, py, zb), (x1, py, zt)], 0.009, cream)

    # Two brass clasps on the flap's lower edge, each latching to a catch plate on the body
    for x in (-0.25, 0.25):
        k.box((0.085, 0.03, 0.09), at=(x, fy - 0.012, top - 0.215), m=brass, bevel=0.008)
        k.box((0.07, 0.016, 0.05), at=(x, -D / 2 - 0.006, top - 0.29), m=brass, bevel=0.006)

    # Handle: brass mounts on the flap top, rings, and a leather grip running ring to ring
    for x in (-0.13, 0.13):
        k.box((0.06, 0.07, 0.03), at=(x, 0, top + 0.02), m=brass, bevel=0.006)
        k.torus(0.024, 0.009, at=(x, 0, top + 0.056), rot=(90, 0, 0), m=brass)
    k.tube([(-0.13, 0, top + 0.068), (-0.115, 0, top + 0.128), (-0.06, 0, top + 0.158), (0, 0, top + 0.163),
            (0.06, 0, top + 0.158), (0.115, 0, top + 0.128), (0.13, 0, top + 0.068)], 0.028, leather, curved=True)

    # Plain floor a shade lighter than the backdrop
    k.box((8, 6, 0.2), at=(0, 1.5, -0.1), m=k.mat("#8a48bd", "matte"), bevel=0.01, setting=True)
