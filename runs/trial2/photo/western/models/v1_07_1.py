# Western saddle on a wooden fence rail: the saddle's length runs along the rail (x), its bars rest on the rail's
# top and two rounded skirts hang down either side. The seat is one soft form that dips between a raised cantle at
# the back and the swell at the front, which carries the horn. A tan fender hangs nearly plumb from under each seat
# edge, outside the skirt, and its foot wraps the top bar of a stirrup. The camera-side fender carries a small silver
# buckle on a keeper strap. The rail sits on two posts with a lower rail, running off the card.
SCENE = {"category": "3", "backdrop": "#3fc8e8", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4a24", "matte")
    dark = k.mat("#6e3a1c", "matte")
    tan = k.mat("#d6a466", "matte")
    silver = k.mat("#c9ced6", "metal")

    # Bars resting on the rail top (z = 0.70).
    k.box((0.8, 0.17, 0.08), at=(0, 0, 0.74), m=dark, bevel=0.03)

    # Skirts: rounded panels hanging close along both sides of the rail.
    for s in (-1, 1):
        k.box((0.9, 0.03, 0.4), at=(0, s * 0.12, 0.55), rot=(s * 8, 0, 0), m=leather, bevel=0.05)

    # Seat, cantle (back, -x) and swell (front, +x) as one soft form with a dip between.
    k.blob([
        (-0.04, 0, 0.76, 0.1, (2.6, 1.9, 0.5)),
        (-0.33, 0, 0.85, 0.1, (0.5, 1.8, 1.0)),
        (0.26, 0, 0.83, 0.1, (0.8, 1.5, 1.1)),
    ], leather)

    # Horn: neck rising out of the swell, flat tan cap tipped back slightly.
    k.cyl(0.035, 0.12, at=(0.29, 0, 0.98), rot=(0, 8, 0), m=dark, bevel=0.006)
    k.cyl(0.07, 0.03, at=(0.30, 0, 1.045), rot=(0, -10, 0), m=tan, bevel=0.01)

    # Fenders hanging from under the seat edge; each foot wraps a stirrup's top bar.
    for s in (-1, 1):
        k.box((0.18, 0.025, 0.52), at=(0.02, s * 0.18, 0.5), rot=(s * 6, 0, 0), m=tan, bevel=0.012)
        yb = s * 0.207
        k.cyl(0.022, 0.13, at=(0.02, yb, 0.235), rot=(0, 90, 0), m=dark, bevel=0.005)
        k.torus(0.08, 0.018, at=(0.02, yb, 0.155), rot=(90, 0, 0), m=tan)
        k.box((0.13, 0.1, 0.03), at=(0.02, yb, 0.085), m=tan, bevel=0.01)

    # Small silver buckle on a dark keeper strap across the camera-side fender.
    k.box((0.19, 0.008, 0.035), at=(0.02, -0.2, 0.42), rot=(-6, 0, 0), m=dark, bevel=0.003)
    k.torus(0.03, 0.007, at=(0.02, -0.206, 0.42), rot=(90, 0, 0), m=silver)

    # Fence: top rail under the saddle, a lower rail, two posts to the ground.
    rail = k.mat("#b9895a", "matte")
    k.box((5, 0.12, 0.16), at=(0, 0, 0.62), m=rail, bevel=0.015, setting=True)
    k.box((5, 0.1, 0.12), at=(0, 0.02, 0.28), m=rail, bevel=0.015, setting=True)
    for x in (-1.4, 1.4):
        k.cyl(0.08, 0.85, at=(x, 0.12, 0.425), m=k.mat("#9c6f45", "matte"), bevel=0.01, setting=True)
