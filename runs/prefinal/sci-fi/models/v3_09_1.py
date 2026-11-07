# Antenna mast: a slim tapered white steel mast bolted by a grey flange plate onto a round concrete footing that
# sits on a flat concrete pad. A clamp collar and short arm carry the small round dish; a three-way bracket near the
# top holds three short upright rod antennas, turned so none hides the mast; a cap on the tip carries the red beacon.
import math

SCENE = {"category": "4", "backdrop": "#3fd2f2", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f6f8", "satin")
    grey = k.mat("#8d939b", "metal")
    concrete = k.mat("#96938b", "matte")
    red = k.mat("#ff2a1f", "glow")

    # Round concrete footing, flange plate and bolts.
    k.cyl(0.13, 0.1, at=(0, 0, 0.05), m=concrete, bevel=0.012)
    k.cyl(0.065, 0.016, at=(0, 0, 0.108), m=grey, bevel=0.004)
    for i in range(4):
        a = math.radians(45 + i * 90)
        k.cyl(0.011, 0.02, at=(0.048 * math.cos(a), 0.048 * math.sin(a), 0.122), m=grey, verts=6)

    # Tapered mast and the tip cap with the red light.
    k.cone(0.034, 0.022, 0.9, at=(0, 0, 0.566), m=white, bevel=0.004)
    k.cyl(0.03, 0.03, at=(0, 0, 1.026), m=grey, bevel=0.005)
    k.sphere(0.027, at=(0, 0, 1.058), m=red)

    # Dish: clamp collar, arm, dish facing the front, feed rod with its horn.
    k.cyl(0.036, 0.04, at=(0, 0, 0.7), m=grey, bevel=0.005)
    k.tube([(0.02, 0, 0.7), (0.11, 0.035, 0.7)], 0.013, grey)
    dish = [(0, 0), (0.03, 0.005), (0.055, 0.016), (0.078, 0.034), (0.074, 0.037), (0.052, 0.023),
            (0.027, 0.014), (0, 0.011)]
    k.lathe(dish, at=(0.12, 0.03, 0.7), rot=(90, 0, 15), m=white)
    tip = (0.12 - 0.085 * math.sin(math.radians(15)), 0.03 - 0.085 * math.cos(math.radians(15)), 0.7)
    k.tube([(0.12, 0.02, 0.7), tip], 0.008, grey)
    k.sphere(0.016, at=tip, m=grey)

    # Three-way bracket with three short upright rod antennas, arms turned clear of the camera line.
    k.cyl(0.034, 0.03, at=(0, 0, 0.88), m=grey, bevel=0.005)
    for i in range(3):
        a = math.radians(i * 120)
        x, y = 0.1 * math.cos(a), 0.1 * math.sin(a)
        k.tube([(0, 0, 0.88), (x, y, 0.88)], 0.012, grey)
        k.cyl(0.013, 0.17, at=(x, y, 0.925), m=white, bevel=0.004)
        k.sphere(0.016, at=(x, y, 1.012), m=grey)

    # Flat concrete pad.
    k.box((5, 5, 0.1), at=(0, 0, -0.05), m=k.mat("#bdbab2", "matte"), bevel=0.01, setting=True)
