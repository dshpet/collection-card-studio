# Spell book: a thick closed book lying flat on a dark oak table, seen from high above. Two purple boards
# sandwich the cream page block; a rounded spine closes the left side. A gold clasp band wraps the fore-edge
# from the bottom board up onto the top cover and ends in a plate with a round stud. A raised gold star sits
# in the middle of the cover. The table's planks run off the card on every side.
import math

SCENE = {"category": "3", "backdrop": "#f2a2c8", "azimuth": 20, "elevation": 62, "lens": 60, "light": "left"}


def build(k):
    purple = k.mat("#6a2fa0", "satin")
    pages = k.mat("#f3e6c4", "matte")
    gold = k.mat("#f2b630", "metal")

    w, d, t, ph = 0.74, 0.96, 0.03, 0.18
    k.box((w, d, t), at=(0, 0, t / 2), m=purple, bevel=0.012)
    k.box((w - 0.05, d - 0.04, ph), at=(0.005, 0, t + ph / 2), m=pages, bevel=0.006)
    top_z = t + ph + t / 2
    k.box((w, d, t), at=(0, 0, top_z), m=purple, bevel=0.012)
    spine = k.cyl(0.13, d, at=(-w / 2 + 0.01, 0, (t + ph + 2 * t) / 2), rot=(90, 0, 0), m=purple, bevel=0.01)
    k.warp(spine, lambda p: (p[0] * 0.35, p[1], p[2]))

    # Raised five-point star on the cover.
    cover_z = top_z + t / 2
    star = k.cyl(0.17, 0.022, at=(-0.02, 0.02, cover_z + 0.011), rot=(0, 0, 18), m=gold, bevel=0.003, verts=10)

    def starify(p):
        x, y, z = p
        r = math.hypot(x, y)
        if r < 1e-6:
            return p
        i = round(math.atan2(y, x) / math.radians(36))
        s = 1.0 if i % 2 == 0 else 0.42
        return (x * s, y * s, z)

    k.warp(star, starify)

    # Front clasp: a gold band wraps the fore-edge from the bottom board onto the top cover.
    band_w, ex = 0.15, w / 2
    k.box((0.08, band_w, 0.014), at=(ex - 0.03, 0, 0.0), m=gold, bevel=0.004)
    k.box((0.016, band_w, top_z + t / 2 + 0.01), at=(ex + 0.008, 0, (top_z + t / 2) / 2 + 0.003), m=gold, bevel=0.005)
    k.box((0.13, band_w, 0.016), at=(ex - 0.055, 0, cover_z + 0.008), m=gold, bevel=0.005)
    k.box((0.07, band_w + 0.04, 0.02), at=(ex - 0.13, 0, cover_z + 0.01), m=gold, bevel=0.007)
    k.sphere(0.03, at=(ex - 0.13, 0, cover_z + 0.025), scale=(1, 1, 0.6), m=gold)

    # Dark oak table: planks running along x, slight gaps between them.
    oak = (k.mat("#5b3a22", "matte"), k.mat("#4e321d", "matte"))
    for i in range(-8, 9):
        k.box((8, 0.39, 0.1), at=(0, i * 0.4, -0.05), m=oak[i % 2], bevel=0.01, setting=True)
