# Silver candelabra on a dark oak table: a round stepped base, a central stem with knops, and three S-curved arms
# that leave the stem 120 degrees apart (one toward the back, two flanking the front). Each arm ends in a socket
# with a drip pan holding a cream candle; a wick carries a small glowing flame. A finial caps the stem between
# the arms. The table is a dark oak slab running off the card.
import math

SCENE = {"category": "3", "backdrop": "#5b2a8e", "azimuth": 25, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#d3d7de", "metal")
    cream = k.mat("#f3e6c4", "satin")
    wick = k.mat("#2b2522", "matte")
    core = k.mat("#fff4c2", "glow")
    tip = k.mat("#ff8a1f", "glow")

    # Base and stem, one turned piece.
    k.lathe([(0.0, 0.0), (0.2, 0.0), (0.205, 0.012), (0.2, 0.03), (0.17, 0.045), (0.12, 0.06), (0.08, 0.085),
             (0.05, 0.11), (0.035, 0.14), (0.03, 0.18), (0.045, 0.2), (0.05, 0.215), (0.045, 0.23), (0.03, 0.25),
             (0.026, 0.33), (0.026, 0.4), (0.045, 0.415), (0.05, 0.44), (0.045, 0.465), (0.028, 0.48),
             (0.028, 0.52), (0.04, 0.535), (0.0, 0.55)], at=(0, 0, 0), rot=(0, 0, 0), m=silver)
    # Finial on top of the stem.
    k.sphere(0.03, at=(0, 0, 0.575), m=silver)
    k.cone(0.012, 0.0, 0.05, at=(0, 0, 0.625), rot=(0, 0, 0), m=silver)

    for deg in (90, 210, 330):
        a = math.radians(deg)
        c, s = math.cos(a), math.sin(a)
        prof = [(0.03, 0.44), (0.1, 0.4), (0.18, 0.4), (0.24, 0.45), (0.26, 0.52), (0.26, 0.57)]
        k.tube([(r * c, r * s, z) for r, z in prof], 0.024, silver, curved=True)
        x, y = 0.26 * c, 0.26 * s
        # Drip pan and socket.
        k.lathe([(0.0, 0.0), (0.03, 0.0), (0.075, 0.02), (0.08, 0.03), (0.07, 0.03), (0.045, 0.025),
                 (0.045, 0.07), (0.05, 0.08), (0.0, 0.08)], at=(x, y, 0.56), rot=(0, 0, 0), m=silver)
        # Candle with softly rounded edges.
        k.cyl(0.036, 0.27, at=(x, y, 0.64 + 0.135), rot=(0, 0, 0), m=cream, bevel=0.012)
        k.cyl(0.004, 0.025, at=(x, y, 0.92), rot=(0, 0, 0), m=wick)
        # Flame: yellow-white core with an orange tip pointing upward.
        k.sphere(0.022, at=(x, y, 0.945), scale=(1, 1, 1.6), m=core)
        k.cone(0.016, 0.0, 0.05, at=(x, y, 0.985), rot=(0, 0, 0), m=tip)

    k.box((5, 3, 0.12), at=(0, 0.6, -0.06), m=k.mat("#4a2c18", "matte"), bevel=0.01, setting=True)
