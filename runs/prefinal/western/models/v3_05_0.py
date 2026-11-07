# Western saddle on a fence rail: the saddle's spine runs along the rail (x), horn at -x, high cantle at +x.
# The seat rests on the rail's top (z = 1.0); the skirts drape down both sides. A leather fender hangs from
# under the seat on each side and holds a stirrup whose loop lies across the saddle, with a silver tread.
# The rail runs off the card both ways onto two posts that stand on the ground below the frame.
SCENE = {"category": "3", "backdrop": "#2fc4e8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    leather = k.mat("#8a4f24", "matte")
    dark = k.mat("#5e3416", "matte")
    seat = k.mat("#a8653a", "matte")
    silver = k.mat("#d3d7de", "metal")
    wood = k.mat("#a8743f", "matte")

    # Fence: a long square rail, top at z = 1.0, on two posts off the card.
    k.unframed(k.box((6.0, 0.14, 0.14), at=(0, 0, 0.93), m=wood, bevel=0.012, setting=True))
    for x in (-1.5, 1.5):
        k.unframed(k.box((0.18, 0.18, 1.12), at=(x, 0.0, 0.5), m=wood, bevel=0.015, setting=True))

    # Saddle tree: seat, rising pommel at the front, high cantle at the back, as one leather form.
    k.blob([
        (0.0, 0.0, 1.075, 0.26, (1.65, 1.0, 0.3)),
        (-0.34, 0.0, 1.11, 0.16, (0.8, 0.95, 0.65)),
        (0.36, 0.0, 1.16, 0.2, (0.38, 1.05, 0.75)),
    ], leather)
    # Stitched seat panel on top (stitching left to the restyle).
    k.blob([(0.03, 0.0, 1.115, 0.2, (1.35, 0.9, 0.12))], seat)
    # Horn: neck rising from the pommel, flat round cap.
    k.cyl(0.04, 0.16, at=(-0.40, 0, 1.22), rot=(0, -12, 0), m=leather, bevel=0.01)
    k.cyl(0.075, 0.035, at=(-0.418, 0, 1.30), rot=(0, -12, 0), m=dark, bevel=0.012)

    for side in (-1, 1):
        # Skirt draping down the side of the rail.
        k.box((0.78, 0.03, 0.30), at=(0.02, side * 0.235, 0.93), rot=(side * -14, 0, 0), m=dark, bevel=0.02)
        # Fender (stirrup leather) from under the seat down to the stirrup.
        k.box((0.17, 0.03, 0.42), at=(0.0, side * 0.29, 0.83), rot=(side * -8, 0, 0), m=leather, bevel=0.012)
        # Stirrup: loop in the y-z plane so the foot passes along x; silver tread below, silver clamp above.
        sy = side * 0.315
        k.torus(0.075, 0.02, at=(0.0, sy, 0.565), rot=(0, 90, 0), m=leather)
        k.box((0.15, 0.10, 0.03), at=(0.0, sy, 0.49), m=silver, bevel=0.008)
        k.box((0.05, 0.05, 0.04), at=(0.0, sy, 0.645), m=silver, bevel=0.008)
