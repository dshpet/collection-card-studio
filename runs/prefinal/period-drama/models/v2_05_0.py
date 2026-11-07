# Opera glasses: two short round barrels, each widening from a small eyepiece (+y) to a large objective (-y),
# lie side by side. Two gold bridge plates join them, front and back, around a black center housing. The gold
# focus wheel sits on that housing in the gap between the barrels. A short handle drops from the underside of
# the housing and ends in a gold knob. The objectives face the camera; the glasses float, tilted a little.
SCENE = {"category": "1", "backdrop": "#e8457f", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#1c1a1f", "gloss")
    gold = k.mat("#e2b24a", "metal")
    glass = k.mat("#9fc4d8", "glass")

    body = [(0, 0), (0.095, 0), (0.11, 0.012), (0.11, 0.07), (0.115, 0.09), (0.125, 0.15),
            (0.135, 0.21), (0.145, 0.27), (0.155, 0.33), (0.165, 0.37), (0.172, 0.385),
            (0.172, 0.42), (0.162, 0.43), (0, 0.43)]
    for x in (-0.2, 0.2):
        # barrel: local z runs from the eyepiece (y = +0.215) to the objective (y = -0.215)
        k.lathe(body, at=(x, 0.215, 0), rot=(90, 0, 0), m=black)
        k.torus(0.172, 0.016, at=(x, -0.2, 0), rot=(90, 0, 0), m=gold)    # objective rim
        k.torus(0.135, 0.01, at=(x, -0.02, 0), rot=(90, 0, 0), m=gold)    # middle band
        k.torus(0.11, 0.013, at=(x, 0.195, 0), rot=(90, 0, 0), m=gold)    # eyepiece rim
        k.cyl(0.152, 0.012, at=(x, -0.217, 0), rot=(90, 0, 0), m=glass)   # objective lens
        k.cyl(0.09, 0.012, at=(x, 0.217, 0), rot=(90, 0, 0), m=glass)     # eyepiece lens

    # center housing along y between the barrels, with gold bridge plates fore and aft
    k.cyl(0.05, 0.34, at=(0, 0.01, 0), rot=(90, 0, 0), m=black)
    for y in (0.16, -0.13):
        k.box((0.3, 0.035, 0.07), at=(0, y, 0.01), m=gold, bevel=0.01)

    # focus wheel on top of the housing, turning on the housing's axis
    k.cyl(0.035, 0.12, at=(0, 0.06, 0.05), rot=(90, 0, 0), m=gold)
    k.cyl(0.068, 0.06, at=(0, 0.06, 0.07), rot=(90, 0, 0), m=gold, bevel=0.008, verts=24)

    # short handle fixed below the center
    k.cyl(0.042, 0.04, at=(0, 0.02, -0.065), m=gold)                       # collar
    k.cyl(0.03, 0.36, at=(0, 0.02, -0.26), m=black, bevel=0.008)           # shaft
    k.cyl(0.036, 0.02, at=(0, 0.02, -0.33), m=gold)                        # trim band
    k.sphere(0.045, at=(0, 0.02, -0.455), m=gold)                          # end knob

    k.turn(0, 10, 0)
