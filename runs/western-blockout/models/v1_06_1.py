# Saguaro cactus: a tall ribbed trunk with a domed top stands in desert sand, its base sunk into a low mound.
# Two arms leave the trunk sideways at different heights, bend up in an elbow and rise as ribbed columns with
# domed tips; the arm ribs are cut inward so each column grows out of its smooth elbow without a collar. A small
# pink flower sits on a light green bud at the top of the trunk. The ribs are shapes in the form, not paint. As on
# the sample cards, the camera is low, the sand fills the bottom of the card, and the plain backdrop shows behind.
import math

SCENE = {"category": "3", "backdrop": "#ff9a3c", "azimuth": 25, "elevation": 9, "lens": 60, "light": "left"}


def ribs(count, depth):
    def fn(p):
        x, y, z = p
        f = 1 + depth * math.cos(count * math.atan2(y, x))
        return (x * f, y * f, z)
    return fn


def grooves(count, depth):
    # Ribs cut inward only: the rib crests keep the full radius, the grooves sink.
    def fn(p):
        x, y, z = p
        f = 1 - depth * (1 - math.cos(count * math.atan2(y, x))) / 2
        return (x * f, y * f, z)
    return fn


def column(r, bottom, top, steps=12):
    # Straight sides up to the dome, then a quarter circle closing to a point.
    profile = [(r, bottom + (top - r - bottom) * i / steps) for i in range(steps + 1)]
    for i in range(1, steps + 1):
        a = math.pi / 2 * i / steps
        profile.append((r * math.cos(a), top - r + r * math.sin(a)))
    return profile


def build(k):
    green = k.mat("#2f9a3e", "matte")
    light = k.mat("#8fd45a", "matte")
    pink = k.mat("#ff6fae", "satin")
    middle = k.mat("#ffd84a", "matte")

    trunk = k.lathe(column(0.12, -0.03, 1.08, steps=20), at=(0, 0, 0), rot=(0, 0, 0), m=green)
    k.warp(trunk, ribs(10, 0.07))

    for side, low, rise in ((-1, 0.38, 0.84), (1, 0.55, 0.95)):
        x = side * 0.30
        k.tube([(side * 0.04, 0, low), (side * 0.2, 0, low + 0.01), (side * 0.29, 0, low + 0.08),
                (x, 0, low + 0.2)], 0.07, green, curved=True)
        arm = k.lathe(column(0.069, low + 0.12, rise, steps=14), at=(x, 0, 0), rot=(0, 0, 0), m=green)
        k.warp(arm, grooves(8, 0.12))

    # Flower on the crown: a light green bud, five pink petals, a small yellow center.
    k.sphere(0.035, at=(0, 0, 1.085), scale=(1, 1, 0.7), m=light)
    for i in range(5):
        a = math.radians(i * 72 + 18)
        k.sphere(0.04, at=(0.04 * math.cos(a), 0.04 * math.sin(a), 1.115), scale=(1, 0.6, 0.35),
                 rot=(0, -20, i * 72 + 18), m=pink)
    k.sphere(0.018, at=(0, 0, 1.125), m=middle)

    sand = "#f3c37a"
    k.floor(sand, "matte")
    k.blob([(0, 0, -0.06, 0.2, (1.6, 1.3, 0.5)), (0.15, 0.08, -0.07, 0.14, (1.4, 1.2, 0.5))],
           k.mat(sand, "matte"), setting=True)
