# Satellite: a gold-foil box body capped by white plates top and bottom. On each side a short round arm runs out
# from the body's center into the inner edge of a flat solar panel: a white frame holding six blue cells, raised
# on both faces. A short mast on the top plate holds a small white dish, tilted toward the viewer, with a feed rod
# and tip at its center. It floats, tilted a little, like the bugle and ring box on the reference cards.

SCENE = {"category": "1", "backdrop": "#4cc95a", "azimuth": 25, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e9b437", "metal")
    white = k.mat("#f4f5f2", "satin")
    blue = k.mat("#2f6fe0", "gloss")
    steel = k.mat("#b9bec6", "metal")

    # Body, z 0.30..0.70, with white end plates
    k.box((0.34, 0.34, 0.40), at=(0, 0, 0.5), m=gold, bevel=0.02)
    k.box((0.37, 0.37, 0.03), at=(0, 0, 0.715), m=white, bevel=0.008)
    k.box((0.37, 0.37, 0.03), at=(0, 0, 0.285), m=white, bevel=0.008)

    # Arms and solar panels on both sides
    pw, ph, pt = 0.48, 0.30, 0.024
    for s in (-1, 1):
        k.cyl(0.026, 0.15, at=(s * 0.245, 0, 0.5), rot=(0, 90, 0), m=steel)
        k.cyl(0.04, 0.03, at=(s * 0.185, 0, 0.5), rot=(0, 90, 0), m=steel)  # collar on the body
        cx = s * (0.30 + pw / 2)
        k.box((pw, pt, ph), at=(cx, 0, 0.5), m=white, bevel=0.006)
        cw, ch = 0.136, 0.12
        for i in (-1, 0, 1):
            for j in (-1, 1):
                k.box((cw, pt + 0.012, ch), at=(cx + i * (cw + 0.012), 0, 0.5 + j * (ch / 2 + 0.006)),
                      m=blue, bevel=0.004)

    # Dish on a short mast on the top plate
    k.cyl(0.022, 0.08, at=(0, 0, 0.77), m=steel)
    profile = [(0.0, 0.0), (0.03, 0.002), (0.06, 0.009), (0.09, 0.02), (0.12, 0.036), (0.135, 0.046),
               (0.13, 0.052), (0.11, 0.04), (0.08, 0.027), (0.05, 0.018), (0.02, 0.014), (0.0, 0.013)]
    k.lathe(profile, at=(0, 0, 0.805), rot=(28, 0, 0), m=white)
    k.tube([(0, -0.005, 0.815), (0, -0.04, 0.885)], 0.009, steel)
    k.sphere(0.02, at=(0, -0.042, 0.89), m=white)

    k.turn(6, -10, 0)
