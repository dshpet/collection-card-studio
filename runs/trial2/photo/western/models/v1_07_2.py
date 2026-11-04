# Western saddle on a wooden fence rail: the saddle's length runs along the rail (x), its bars rest on the rail's
# top and two rounded skirts hang down either side. The seat is one soft form that dips between a raised, wide
# cantle wall at the back and the swell at the front, which carries a short stout horn. A tan fender, flaring wider
# toward the bottom, hangs nearly plumb from under each seat edge, outside the skirt, and its foot wraps the top bar
# of a stirrup. The camera-side fender carries a small silver buckle on a keeper strap. The rail sits on two posts
# with a lower rail, running off the card.
SCENE = {"category": "3", "backdrop": "#3fc8e8", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4a24", "matte")
    dark = k.mat("#6e3a1c", "matte")
    tan = k.mat("#d6a466", "matte")
    silver = k.mat("#c9ced6", "metal")

    # Bars resting on the rail top (z = 0.70).
    k.box((0.8, 0.17, 0.08), at=(0, 0, 0.74), m=dark, bevel=0.03)

    # Skirts: rounded leather panels hanging close along both sides of the rail.
    for s in (-1, 1):
        k.sphere(1.0, at=(0, s * 0.125, 0.56), scale=(0.46, 0.02, 0.21), rot=(s * 8, 0, 0), m=leather)

    # Seat, a wide curved cantle wall (back, -x) and the swell (front, +x) as one soft form with a dip between.
    k.blob([
        (-0.04, 0, 0.76, 0.1, (2.6, 1.9, 0.5)),
        (-0.31, 0, 0.84, 0.1, (0.45, 1.95, 1.05)),
        (0.25, 0, 0.82, 0.1, (0.9, 1.7, 1.0)),
    ], leather)

    # Horn: short stout neck rising out of the swell, broad flat tan cap tipped back slightly.
    k.cyl(0.042, 0.08, at=(0.27, 0, 0.96), rot=(0, 8, 0), m=dark, bevel=0.008)
    k.cyl(0.07, 0.03, at=(0.275, 0, 1.005), rot=(0, -10, 0), m=tan, bevel=0.012)

    # Fenders hanging from under the seat edge, flaring wider at the foot, which wraps a stirrup's top bar.
    for s in (-1, 1):
        fender = k.box((0.18, 0.025, 0.52), at=(0.02, s * 0.18, 0.5), rot=(s * 6, 0, 0), m=tan, bevel=0.012)
        k.warp(fender, lambda p: (p[0] * (1 - p[2] * 1.0), p[1], p[2]))
        yb = s * 0.207
        k.cyl(0.022, 0.25, at=(0.02, yb, 0.235), rot=(0, 90, 0), m=dark, bevel=0.005)
        k.torus(0.08, 0.018, at=(0.02, yb, 0.155), rot=(90, 0, 0), m=tan)
        k.box((0.13, 0.1, 0.03), at=(0.02, yb, 0.085), m=tan, bevel=0.01)

    # Small silver buckle on a dark keeper strap across the camera-side fender.
    k.box((0.21, 0.008, 0.035), at=(0.02, -0.2, 0.42), rot=(-6, 0, 0), m=dark, bevel=0.003)
    k.torus(0.03, 0.007, at=(0.02, -0.206, 0.42), rot=(90, 0, 0), m=silver)

    # Fence: top rail under the saddle, a lower rail, two posts to the ground.
    rail = k.mat("#b9895a", "matte")
    k.box((5, 0.12, 0.16), at=(0, 0, 0.62), m=rail, bevel=0.015, setting=True)
    k.box((5, 0.1, 0.12), at=(0, 0.02, 0.28), m=rail, bevel=0.015, setting=True)
    for x in (-1.4, 1.4):
        k.cyl(0.08, 0.85, at=(x, 0.12, 0.425), m=k.mat("#9c6f45", "matte"), bevel=0.01, setting=True)
