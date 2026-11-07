# Opera glasses: two short round barrels, each widening from a small eyepiece (+y) to a large objective (-y),
# lie side by side. Two gold bridge plates join them, front and back, around a black center housing. A gold axle
# runs between the plates above the housing, and the knurled focus wheel turns on it in the gap between the
# barrels, standing above the narrow eyepiece ends. A short handle drops from the underside of the housing
# through a gold collar and ends in a gold knob. The glasses float, tilted a little so the top and wheel show.
SCENE = {"category": "1", "backdrop": "#e8457f", "azimuth": 34, "elevation": 18, "lens": 60, "light": "left"}


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

    # center housing along y between the barrels, with tall gold bridge plates fore and aft
    k.cyl(0.05, 0.34, at=(0, 0.01, 0), rot=(90, 0, 0), m=black)
    for y in (0.16, -0.13):
        k.box((0.3, 0.035, 0.13), at=(0, y, 0.055), m=gold, bevel=0.01)

    # focus axle between the plates, and the knurled focus wheel turning on it
    k.cyl(0.02, 0.29, at=(0, 0.015, 0.09), rot=(90, 0, 0), m=gold)
    k.cyl(0.065, 0.06, at=(0, 0.06, 0.09), rot=(90, 0, 0), m=gold, bevel=0.008, verts=24)

    # short handle fixed below the center
    k.cyl(0.04, 0.16, at=(0, 0.02, -0.12), m=gold)                         # collar from the housing
    k.cyl(0.03, 0.34, at=(0, 0.02, -0.36), m=black, bevel=0.008)           # shaft
    k.cyl(0.036, 0.02, at=(0, 0.02, -0.45), m=gold)                        # trim band
    k.sphere(0.045, at=(0, 0.02, -0.55), m=gold)                           # end knob

    k.turn(12, 8, -6)
