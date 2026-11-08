# Tablet lying flat on a metal desk: a thin black slab with rounded edges, the glowing cyan screen set into
# its top face inside a black bezel, and a white round home button in the wider bottom bezel. The desk is a
# large orange-painted steel top that fills the card. The camera looks down from high above, as on the book,
# racket and map cards, with the tablet turned a little so it lies on a diagonal.
SCENE = {"category": "3", "backdrop": "#f08a2c", "azimuth": 25, "elevation": 64, "lens": 60, "light": "left"}


def build(k):
    body = k.mat("#16171b", "gloss")
    screen = k.mat("#3ee6f2", "glow")
    button = k.mat("#f7f7f4", "satin")

    w, d, t = 0.72, 1.0, 0.04
    k.box((w, d, t), at=(0, 0, t / 2), m=body, bevel=0.018)
    # screen panel, slightly proud of the bezel so it reads as a separate surface
    k.box((w - 0.08, d - 0.2, 0.004), at=(0, 0.02, t + 0.001), m=screen, bevel=0.002)
    # home button in the bottom bezel, a short white disc sitting just above the top face
    k.cyl(0.032, 0.008, at=(0, -d / 2 + 0.045, t + 0.001), m=button, bevel=0.003)

    k.turn(0, 0, -18)

    # metal desk top, painted orange, filling the whole card
    k.box((8, 8, 0.06), at=(0, 0, -0.03), m=k.mat("#e8862f", "metal"), bevel=0, setting=True)
