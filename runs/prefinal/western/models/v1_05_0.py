# Western saddle on a hay bale: the saddle runs along x (horn toward +x) and straddles the bale's top. A pad lies on
# the top and the skirts bend down both long sides. The seat dips between a high cantle at the back and the fork,
# and the horn rises from the fork. A fender hangs on each side under the seat, and a strap runs from it through
# the top bar of a stirrup that hangs free beside the bale. The bale is the real surface and runs off the card on
# both sides. It stands on plain ground.
SCENE = {"category": "3", "backdrop": "#38c6ec", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4f24", "matte")
    dark = k.mat("#5e3417", "matte")
    seat_m = k.mat("#6f3d1b", "satin")
    silver = k.mat("#d3d7dd", "metal")

    # Pad and skirts: they lie on the bale top and bend over both long edges.
    k.box((0.74, 0.54, 0.03), at=(0, 0, 0.015), m=leather, bevel=0.012)
    for s in (-1, 1):
        k.box((0.70, 0.03, 0.19), at=(0, s * 0.27, -0.075), m=leather, bevel=0.012)

    # Tree and seat as one leather form: low seat, high cantle at -x, fork at +x.
    k.blob([
        (0.0, 0.0, 0.065, 0.1, (2.3, 2.0, 0.45)),
        (-0.15, 0.0, 0.08, 0.1, (1.0, 1.9, 0.55)),
        (-0.29, 0.0, 0.16, 0.1, (0.38, 1.9, 1.05)),
        (0.15, 0.0, 0.08, 0.1, (1.0, 1.6, 0.6)),
        (0.27, 0.0, 0.13, 0.09, (0.7, 1.35, 0.95)),
    ], leather)
    # Stitched seat panel: a darker raised layer on the dip of the seat.
    k.blob([(-0.04, 0.0, 0.098, 0.1, (1.6, 1.5, 0.22))], seat_m)

    # Horn: neck on the fork and a flat cap.
    k.cyl(0.03, 0.11, at=(0.30, 0, 0.255), rot=(0, 14, 0), m=dark, bevel=0.008)
    k.cyl(0.062, 0.028, at=(0.314, 0, 0.312), rot=(0, 14, 0), m=dark, bevel=0.01)

    # Silver conchos on the skirt corners.
    for s in (-1, 1):
        for x in (-0.28, 0.28):
            k.cyl(0.026, 0.012, at=(x, s * 0.29, -0.02), rot=(90, 0, 0), m=silver, bevel=0.004)

    # Fenders, straps and stirrups on both sides.
    for s in (-1, 1):
        y = s * 0.30
        k.box((0.17, 0.025, 0.27), at=(-0.02, y, -0.12), m=dark, bevel=0.015)
        k.box((0.05, 0.018, 0.08), at=(-0.02, y + s * 0.004, -0.285), m=dark, bevel=0.005)
        # Stirrup: wooden arch with silver binding, top bar holding the strap, silver tread.
        arch = [(-0.095, y, -0.43), (-0.085, y, -0.37), (-0.05, y, -0.33),
                (-0.02, y, -0.318), (0.01, y, -0.33), (0.045, y, -0.37), (0.055, y, -0.43)]
        k.tube(arch, 0.02, leather, curved=True)
        k.cyl(0.012, 0.07, at=(-0.02, y, -0.318), rot=(0, 90, 0), m=silver)
        k.box((0.18, 0.07, 0.025), at=(-0.02, y, -0.437), m=silver, bevel=0.006)

    # Setting: the hay bale, its two twine bands, and the ground under it.
    hay = k.mat("#e6be58", "matte")
    k.box((1.5, 0.52, 0.48), at=(0, 0, -0.24), m=hay, bevel=0.03, setting=True)
    twine = k.mat("#b98a3e", "matte")
    for x in (-0.48, 0.48):
        k.box((0.025, 0.535, 0.495), at=(x, 0, -0.24), m=twine, bevel=0.006, setting=True)
    k.floor("#c9a24c", "matte", z=-0.48)
