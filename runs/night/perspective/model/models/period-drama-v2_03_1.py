# Top hat: a tall silk crown, a little narrower at the waist and slightly flared to a flat top, sits on a
# brim that curls up at the left and right sides and dips a little at front and back. A purple ribbon band
# wraps the base of the crown with a small flat bow on the side facing the camera. It floats, tilted toward
# the camera to show the flat top and the curl of the brim.
SCENE = {"category": "1", "backdrop": "#ffc83a", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    silk = k.mat("#5f646d", "satin")
    ribbon = k.mat("#6a2fa8", "satin")

    # Crown: lathe from the closed bottom to the flat top.
    crown = [(0.0, 0.01), (0.282, 0.01), (0.279, 0.08), (0.272, 0.2), (0.268, 0.32), (0.271, 0.45),
             (0.279, 0.58), (0.29, 0.7), (0.298, 0.79), (0.3, 0.805), (0.295, 0.815), (0.28, 0.82), (0.0, 0.82)]
    k.lathe(crown, at=(0, 0, 0), m=silk, verts=96)

    # Brim: a thin ring with a rolled lip, then curled up gently at the sides (x) and dipped at front/back (y).
    brim = [(0.26, 0.0), (0.4, 0.0), (0.47, 0.004), (0.51, 0.014), (0.535, 0.032), (0.542, 0.052),
            (0.532, 0.066), (0.512, 0.064), (0.49, 0.046), (0.45, 0.032), (0.4, 0.026), (0.26, 0.026)]
    part = k.lathe(brim, at=(0, 0, 0), m=silk, verts=128)

    def curl(p):
        x, y, z = p
        sx = max(0.0, abs(x) - 0.27)
        sy = max(0.0, abs(y) - 0.27)
        return (x, y * 0.92, z + 1.3 * sx * sx - 0.4 * sy * sy)

    k.warp(part, curl)

    # Ribbon band hugging the base of the crown.
    band = [(0.27, 0.025), (0.288, 0.025), (0.292, 0.035), (0.29, 0.15), (0.284, 0.165), (0.265, 0.165)]
    k.lathe(band, at=(0, 0, 0), m=ribbon, verts=96)

    # Small flat bow on the band, on the side the camera sees.
    bx = 0.29
    k.sphere(0.03, at=(bx + 0.005, 0.0, 0.095), scale=(0.6, 1, 1.1), m=ribbon)
    for s in (-1, 1):
        k.sphere(0.045, at=(bx - 0.004, s * 0.05, 0.097), scale=(0.35, 1.2, 0.75), rot=(s * 12, 0, 0), m=ribbon)

    k.turn(14, -6, 0)
