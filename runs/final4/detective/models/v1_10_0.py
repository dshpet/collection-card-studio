# Handcuffs lying flat on a plain floor: two round cuffs side by side. Each cuff is a ring lying on the floor
# with a thinner swing arm just inside it, a hinge pin on its outer side (the pivot the arm turns on) and a lock
# block on its inner side. A swivel tab with an eye runs from each lock block toward the middle, and a short
# chain of three oval links joins the two eyes: the middle link stands on edge through the two flat outer links.
# The camera looks down fairly steeply so the flat rings read as rings.
SCENE = {"category": "2", "backdrop": "#e8584a", "azimuth": 25, "elevation": 55, "lens": 60, "light": "left"}


def build(k):
    steel = k.mat("#d3d8de", "metal")
    dark = k.mat("#3a3e45", "satin")
    R, r = 0.17, 0.03

    def oval(at, rot):
        link = k.torus(0.026, 0.009, at=at, rot=rot, m=steel)
        k.warp(link, lambda p: (p[0] * 1.55, p[1], p[2]))  # stretch along the link's own x
        return link

    for side in (-1, 1):
        cx = side * 0.33
        # the cuff ring lying on the floor, and the thinner swing arm just inside it
        k.torus(R, r, at=(cx, 0, r), rot=(0, 0, 0), m=steel)
        k.torus(R - 0.045, 0.016, at=(cx, 0, 0.022), rot=(0, 0, 0), m=steel)
        # hinge pin on the outer side, through ring and arm
        hx = cx + side * R
        k.cyl(0.035, 0.085, at=(hx, 0, 0.0425), rot=(0, 0, 0), m=steel, bevel=0.008)
        k.cyl(0.02, 0.012, at=(hx, 0, 0.088), rot=(0, 0, 0), m=steel, bevel=0.003)
        # lock block on the inner side, toward the chain
        bx = cx - side * R
        k.box((0.1, 0.15, 0.075), at=(bx, 0, 0.0375), rot=(0, 0, 0), m=steel, bevel=0.015)
        # keyhole cut into the top of the block
        k.cyl(0.012, 0.01, at=(bx, -0.03, 0.073), rot=(0, 0, 0), m=dark, bevel=0.002)
        k.box((0.008, 0.022, 0.01), at=(bx, -0.043, 0.073), rot=(0, 0, 0), m=dark, bevel=0.001)
        # swivel tab and eye that the chain hangs from
        k.cyl(0.018, 0.04, at=(bx - side * 0.06, 0, 0.035), rot=(0, 90, 0), m=steel, bevel=0.004)
        k.torus(0.025, 0.009, at=(side * 0.098, 0, 0.035), rot=(90, 0, 0), m=steel)

    # three oval chain links: flat, on edge, flat
    oval((-0.055, 0, 0.012), (0, 0, 0))
    oval((0.0, 0, 0.032), (90, 0, 0))
    oval((0.055, 0, 0.012), (0, 0, 0))

    k.turn(0, 0, -8)
    k.box((6, 6, 0.1), at=(0, 0.8, -0.05), rot=(0, 0, 0), m=k.mat("#f27a6c", "matte"), bevel=0.01, setting=True)
