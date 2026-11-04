# Western saddle on a wooden fence rail: the saddle's length runs along the rail (x), its bars rest on the rail's
# top and two skirt panels hang down either side. The seat dips between a raised cantle at the back and the swell at
# the front, which carries the horn. A fender hangs over each skirt with a stirrup on its lower end; the camera-side
# fender carries a small silver buckle. The rail sits on two posts and a lower rail, running off the card.
SCENE = {"category": "3", "backdrop": "#3fc8e8", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4a24", "matte")
    dark = k.mat("#6e3a1c", "matte")
    tan = k.mat("#d6a466", "matte")
    silver = k.mat("#c9ced6", "metal")

    # Bars resting on the rail top (z = 0.70).
    k.box((0.9, 0.18, 0.08), at=(0, 0, 0.74), m=leather, bevel=0.03)

    # Skirts: tops tuck in over the rail, bottoms flare out.
    for s in (-1, 1):
        k.box((1.0, 0.025, 0.42), at=(0, s * 0.135, 0.56), rot=(s * 15, 0, 0), m=leather, bevel=0.012)

    # Seat, cantle at the back (-x), swell at the front (+x).
    k.sphere(0.1, at=(-0.05, 0, 0.75), scale=(3.0, 1.7, 0.5), m=tan)
    k.sphere(0.1, at=(-0.36, 0, 0.84), scale=(0.35, 1.7, 1.0), rot=(0, -20, 0), m=leather)
    k.sphere(0.11, at=(0.28, 0, 0.82), scale=(0.9, 1.3, 1.0), m=leather)

    # Horn: neck rising out of the swell, flat cap tipped back slightly.
    k.cyl(0.035, 0.14, at=(0.32, 0, 0.96), rot=(0, 8, 0), m=dark, bevel=0.006)
    k.cyl(0.07, 0.03, at=(0.33, 0, 1.035), rot=(0, -10, 0), m=tan, bevel=0.01)

    # Fenders lying over the skirts, each with a stirrup hanging from its foot.
    for s in (-1, 1):
        k.box((0.2, 0.025, 0.6), at=(0.02, s * 0.185, 0.47), rot=(s * 15, 0, 0), m=dark, bevel=0.01)
        k.torus(0.08, 0.018, at=(0.02, s * 0.265, 0.12), rot=(90, 0, 0), m=tan)
        k.box((0.12, 0.1, 0.03), at=(0.02, s * 0.265, 0.045), m=tan, bevel=0.01)

    # Small silver buckle on the camera-side fender.
    k.box((0.07, 0.012, 0.055), at=(0.02, -0.228, 0.385), rot=(-15, 0, 0), m=silver, bevel=0.004)

    # Fence: top rail under the saddle, a lower rail, two posts to the ground.
    rail = k.mat("#b9895a", "matte")
    k.box((5, 0.12, 0.16), at=(0, 0, 0.62), m=rail, bevel=0.015, setting=True)
    k.box((5, 0.1, 0.12), at=(0, 0.02, 0.28), m=rail, bevel=0.015, setting=True)
    for x in (-1.4, 1.4):
        k.cyl(0.08, 0.85, at=(x, 0.12, 0.425), m=k.mat("#9c6f45", "matte"), bevel=0.01, setting=True)
