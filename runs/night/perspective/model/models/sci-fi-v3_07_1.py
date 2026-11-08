# Tablet lying flat on a metal desk: a thin black slab with rounded edges, the glowing cyan screen set into
# its top face inside a black bezel, and a white round home button centred in the wider bottom bezel. The desk
# is a large orange-painted steel top that fills the card. The camera looks down from high above, with the
# tablet turned a little so it lies on a diagonal.
SCENE = {"category": "3", "backdrop": "#f08a2c", "azimuth": 25, "elevation": 64, "lens": 60, "light": "left"}


def build(k):
    body = k.mat("#16171b", "gloss")
    screen = k.mat("#12bfd8", "glow")
    button = k.mat("#f7f7f4", "satin")

    w, d, t = 0.72, 1.0, 0.04
    k.box((w, d, t), at=(0, 0, t / 2), m=body, bevel=0.018)
    # screen panel: spans y -0.38..0.42, slightly proud of the bezel so it reads as a separate surface
    k.box((w - 0.08, d - 0.2, 0.004), at=(0, 0.02, t + 0.001), m=screen, bevel=0.002)
    # home button centred in the bottom bezel (y -0.5..-0.38), a short white disc on the top face
    k.cyl(0.036, 0.008, at=(0, -0.44, t + 0.002), m=button, bevel=0.003)

    k.turn(0, 0, -18)

    # metal desk top, painted orange, filling the whole card
    k.box((8, 8, 0.06), at=(0, 0, -0.03), m=k.mat("#e8862f", "metal"), bevel=0, setting=True)
