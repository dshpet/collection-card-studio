# Admiralty anchor standing upright on dock planks: a tapered iron shank rises from the crown, which rests on the
# planks on a heavy flattened foot. Two arms curve up from the crown in one plane and end in pointed flukes that
# fully enclose the arm ends. Near the top the shank passes through a wooden stock that crosses at right angles to
# the arms, held by two iron bands. The ring runs through an eye boss at the head of the shank. Planks run back
# from the camera with dark gaps between them and run off the card.
import math

SCENE = {"category": "3", "backdrop": "#ffc83d", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#3b4047", "metal")
    wood = k.mat("#8b5a32", "matte")

    # Shank: tapered iron bar from the crown up to the head.
    k.cone(0.05, 0.038, 0.84, at=(0, 0, 0.48), rot=(0, 0, 0), m=iron, bevel=0.006)

    # Arms: one curved bar, an arc around a point on the shank, lowest at the crown.
    cz, rad, r_arm = 0.44, 0.39, 0.045
    angles = [math.radians(a) for a in range(-62, 63, 6)]
    k.tube([(rad * math.sin(a), 0, cz - rad * math.cos(a)) for a in angles], r_arm, iron, curved=True)

    # Crown: heavy flattened foot where the arms meet the shank; it sits on the planks.
    k.blob([(0, 0, 0.06, 0.07, (1.5, 1.0, 0.85)), (0, 0, 0.12, 0.055)], iron)

    # Flukes: pointed spade heads at the arm tips, thick enough at the base to swallow the arm end,
    # thinning toward the point, pointing along the arm, up and outward.
    def spade(p):
        x, y, z = p
        if z > 0:
            return (x * 0.04, y * 0.5, z + 0.03)
        return (x, y, z)

    end = math.radians(62)
    for side in (-1, 1):
        tip = (side * rad * math.sin(end), 0, cz - rad * math.cos(end))
        d = (side * math.cos(end), 0, math.sin(end))
        c = (tip[0] + d[0] * 0.03, 0, tip[2] + d[2] * 0.03)
        f = k.box((0.17, 0.1, 0.17), at=c, rot=(0, side * (90 - 62), 0), m=iron, bevel=0.01)
        k.warp(f, spade)
        k.sphere(r_arm, at=tip, m=iron)

    # Head: eye boss bored front to back, and the ring through it.
    k.cyl(0.05, 0.08, at=(0, 0, 0.9), rot=(90, 0, 0), m=iron, bevel=0.008)
    k.torus(0.085, 0.022, at=(0, 0, 0.985), rot=(90, 0, 0), m=iron)

    # Stock: wooden crossbar at right angles to the arms, tapering to its ends, with two iron bands.
    half = 0.37

    def taper(p):
        x, y, z = p
        s = 1 - 0.35 * min(abs(y) / half, 1)
        return (x * s, y, z * s)

    stock = k.box((0.09, half * 2, 0.09), at=(0, 0, 0.75), m=wood, bevel=0.012)
    k.warp(stock, taper)
    for y in (-0.075, 0.075):
        k.box((0.1, 0.03, 0.1), at=(0, y, 0.75), m=iron, bevel=0.005)

    # Dock planks, running back from the camera, with dark gaps.
    planks = [k.mat("#c98a4e", "matte"), k.mat("#b97a42", "matte")]
    w, gap = 0.2, 0.014
    for i in range(-15, 16):
        k.box((w - gap, 6, 0.05), at=(i * w + 0.05, 1.5, -0.025), m=planks[i % 2], bevel=0.006, setting=True)
    k.box((6.4, 6, 0.04), at=(0, 1.5, -0.07), m=k.mat("#4a2c16", "matte"), bevel=0, setting=True)
