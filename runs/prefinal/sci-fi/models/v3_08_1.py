# Power cell: a tall glass tube is held between two grey metal caps. The glowing cyan core runs up the axis
# inside, seated in a socket in each cap. The top cap carries a small yellow ring around a short terminal nub.
# It stands upright on a plain pink floor.
SCENE = {"category": "2", "backdrop": "#f06aa8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    metal = k.mat("#9aa1ab", "metal")
    dark = k.mat("#5d636c", "metal")
    glass = k.mat("#cfefff", "glass")
    core = k.mat("#38e8ff", "glow")
    ring = k.mat("#ffd23a", "satin")

    # bottom cap: a stepped metal base standing on the floor
    k.lathe([(0, 0.0), (0.23, 0.0), (0.24, 0.015), (0.24, 0.07), (0.225, 0.085), (0.215, 0.09),
             (0.215, 0.15), (0.205, 0.16), (0, 0.16)], at=(0, 0, 0), m=metal)
    # glass tube, seated into both caps
    k.cyl(0.19, 0.70, at=(0, 0, 0.50), m=glass, bevel=0.004)
    # core and the two sockets that hold it
    k.cyl(0.05, 0.08, at=(0, 0, 0.19), m=dark)
    k.cyl(0.05, 0.08, at=(0, 0, 0.81), m=dark)
    k.cyl(0.07, 0.56, at=(0, 0, 0.50), m=core, bevel=0.02)
    # top cap
    k.lathe([(0, 0.84), (0.205, 0.84), (0.215, 0.85), (0.215, 0.91), (0.225, 0.915), (0.24, 0.93),
             (0.24, 0.99), (0.23, 1.005), (0, 1.005)], at=(0, 0, 0), m=metal)
    # small yellow ring on the top cap, around the terminal nub
    k.torus(0.10, 0.018, at=(0, 0, 1.012), m=ring)
    k.cyl(0.05, 0.06, at=(0, 0, 1.03), m=dark, bevel=0.01)

    # plain floor, a shade lighter than the pink backdrop, top at z = 0, wide enough that no side edge shows
    k.box((14, 10, 0.2), at=(0, 2.5, -0.1), m=k.mat("#f58cbc", "matte"), bevel=0.01, setting=True)
