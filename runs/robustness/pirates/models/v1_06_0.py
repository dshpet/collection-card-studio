# Spyglass: a brass telescope pulled out to three round sections, each narrower than the one before. The widest
# section has a hood with a round glass lens set into its open end, a red band behind the hood and a dark leather
# grip held by brass rings. Each narrower section comes out of a brass collar on the one before it, and the last
# one ends in a small eyepiece. It floats on the diagonal like the bugle card: lens end up-left toward the viewer,
# eyepiece down-right.

SCENE = {"category": "1", "backdrop": "#3fae4a", "azimuth": 0, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    brass = k.mat("#d9a234", "metal")
    leather = k.mat("#4a2a17", "matte")
    red = k.mat("#c8282c", "satin")
    glass = k.mat("#bfe8f2", "glass")
    along = (0, 90, 0)  # local z of lathes and cylinders runs along +x

    # One brass body, lens end at -x, eyepiece at +x. A recess at the lens end holds the glass.
    profile = [
        (0.0, -0.47), (0.118, -0.47), (0.118, -0.52), (0.15, -0.52), (0.152, -0.50), (0.15, -0.44),
        (0.132, -0.425), (0.132, -0.10),                     # section 1, widest
        (0.142, -0.10), (0.145, -0.085), (0.142, -0.07),     # collar
        (0.104, -0.07), (0.104, 0.20),                       # section 2
        (0.112, 0.20), (0.115, 0.212), (0.112, 0.225),       # collar
        (0.078, 0.225), (0.078, 0.43),                       # section 3, narrowest
        (0.088, 0.43), (0.09, 0.445), (0.088, 0.46),         # end ring
        (0.052, 0.47), (0.05, 0.53), (0.04, 0.535), (0.0, 0.535),  # eyepiece
    ]
    k.lathe(profile, at=(0, 0, 0), rot=along, m=brass)

    # Glass lens set into the hood.
    k.cyl(0.118, 0.012, at=(-0.478, 0, 0), rot=along, m=glass, bevel=0.004)

    # Red band just behind the hood.
    k.cyl(0.14, 0.035, at=(-0.395, 0, 0), rot=along, m=red, bevel=0.006)

    # Leather grip wrapped around the widest section, held at each end by a brass ring.
    k.cyl(0.143, 0.19, at=(-0.255, 0, 0), rot=along, m=leather, bevel=0.01)
    for x in (-0.358, -0.152):
        k.cyl(0.15, 0.018, at=(x, 0, 0), rot=along, m=brass, bevel=0.005)

    # Lens end up and toward the viewer, eyepiece down and away.
    k.turn(0, 32, 35)
