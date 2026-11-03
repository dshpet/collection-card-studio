# Folding camp chair: two frames cross in an X on each side and pivot on one bolt; the seat hangs between
# the front and back top bars; the outer frame's rear legs rise into the backrest uprights.
SCENE = {"category": "2", "backdrop": "#ee5b3a", "azimuth": 35, "elevation": 12, "light": "left"}


def build(k):
    steel = k.mat("#c9ced6", "metal")
    cloth = k.mat("#3aa640", "matte")
    cap = k.mat("#4a4f57", "satin")
    r = 0.012
    for side in (-1, 1):
        outer, inner = side * 0.255, side * 0.228
        k.tube([(outer, -0.21, 0.0), (outer, 0.20, 0.45), (outer, 0.25, 0.88)], r, steel)
        k.tube([(inner, 0.21, 0.0), (inner, -0.20, 0.45)], r, steel)
        k.cyl(0.014, 0.05, at=(side * 0.242, -0.005, 0.225), rot=(0, 90, 0), m=cap)
        for y, x in ((-0.21, outer), (0.21, inner)):
            k.sphere(0.018, at=(x, y, 0.01), m=cap)
    k.tube([(-0.255, 0.20, 0.45), (0.255, 0.20, 0.45)], r, steel)
    k.tube([(-0.255, -0.20, 0.45), (0.255, -0.20, 0.45)], r, steel)
    k.tube([(-0.255, -0.21, 0.02), (0.255, -0.21, 0.02)], r, steel)
    k.tube([(-0.228, 0.21, 0.02), (0.228, 0.21, 0.02)], r, steel)
    k.tube([(-0.255, 0.25, 0.88), (0.255, 0.25, 0.88)], r, steel)
    k.box((0.49, 0.40, 0.012), at=(0, 0, 0.44), m=cloth, bevel=0.004)
    k.box((0.50, 0.012, 0.26), at=(0, 0.238, 0.73), rot=(-6.6, 0, 0), m=cloth, bevel=0.004)
    k.cyl(0.045, 0.004, at=(0, 0.229, 0.74), rot=(83.4, 0, 0), m=k.mat("#ffd23a", "matte"), verts=3)
    k.sphere(0.014, at=(0.0, 0.226, 0.69), scale=(1, 0.3, 1.4), m=k.mat("#ff8a1f", "matte"))
    k.box((4, 1.6, 0.12), at=(0, 0.3, -0.06), m=k.mat("#f3c9a2", "satin"), bevel=0.01, setting=True)
