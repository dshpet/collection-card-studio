# Brass candelabra: a round weighted base turns up into a turned stem with two knops; two arms leave the upper
# knop to either side, sweep out and curve up into cups. The stem ends in a third, higher cup. Each cup holds a
# tall white candle with a wick and a small glowing flame. It stands on a plain teal floor.
# Fix round 2 ("Perspective seems a little off?"): seen from the front at the height of its middle with a longer
# lens, so the base and the cups show the same thin ellipses; was 28 degrees round, 12 up, 60 mm.
SCENE = {"category": "2", "backdrop": "#0f6f73", "azimuth": 8, "elevation": 6, "lens": 85, "light": "left"}


def build(k):
    brass = k.mat("#d9a63a", "metal")
    wax = k.mat("#f7f3ea", "satin")
    wick = k.mat("#2b2420", "matte")
    core = k.mat("#fff4b8", "glow")
    tip = k.mat("#ff9a2e", "glow")

    # Base and turned stem, one lathe from the floor to the central cup.
    k.lathe([(0, 0), (0.22, 0), (0.226, 0.015), (0.222, 0.03), (0.2, 0.045), (0.16, 0.065), (0.11, 0.09),
             (0.07, 0.11), (0.05, 0.125), (0.048, 0.14), (0.068, 0.155), (0.072, 0.17), (0.062, 0.185),
             (0.04, 0.2), (0.032, 0.24), (0.03, 0.28), (0.036, 0.3), (0.058, 0.315), (0.068, 0.33),
             (0.062, 0.345), (0.04, 0.36), (0.03, 0.4), (0.027, 0.46), (0.03, 0.52), (0.042, 0.55),
             (0.03, 0.57), (0.028, 0.6), (0, 0.6)], at=(0, 0, 0), rot=(0, 0, 0), m=brass)

    cup = [(0, 0), (0.022, 0), (0.03, 0.012), (0.072, 0.028), (0.078, 0.036), (0.07, 0.042),
           (0.046, 0.046), (0.044, 0.07), (0.05, 0.085), (0.052, 0.095), (0, 0.095)]

    def holder(x, z, height):
        k.lathe(cup, at=(x, 0, z), rot=(0, 0, 0), m=brass)
        base = z + 0.08
        k.cyl(0.036, height, at=(x, 0, base + height / 2), rot=(0, 0, 0), m=wax, bevel=0.006)
        top = base + height
        k.cyl(0.005, 0.03, at=(x, 0, top + 0.012), rot=(0, 0, 0), m=wick, bevel=0.001)
        k.sphere(0.022, at=(x, 0, top + 0.045), scale=(1, 1, 1.7), m=core)
        k.cone(0.012, 0.0, 0.035, at=(x, 0, top + 0.095), rot=(0, 0, 0), m=tip, bevel=0.002)

    # Center cup and candle on top of the stem.
    holder(0.0, 0.585, 0.28)

    # Two arms from the upper knop, out and up into their cups.
    for s in (-1, 1):
        k.tube([(s * 0.03, 0, 0.33), (s * 0.1, 0, 0.31), (s * 0.19, 0, 0.32), (s * 0.255, 0, 0.37),
                (s * 0.28, 0, 0.44), (s * 0.28, 0, 0.5)], 0.024, brass, curved=True)
        k.sphere(0.034, at=(s * 0.28, 0, 0.495), m=brass)
        holder(s * 0.28, 0.51, 0.26)

    # Plain floor a shade lighter than the backdrop.
    k.box((6, 4, 0.1), at=(0, 1.2, -0.05), m=k.mat("#2a9894", "matte"), bevel=0.0, setting=True)
