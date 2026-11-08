# Top hat: a tall black crown, a little wider at its flat top, with a red satin band at its foot; a black brim
# with a rolled edge curls up gently and evenly at the left and right and dips a little at the front and back.
# Floating, seen almost from the front so both sides of the brim match. Fix round 3: the drawings from text curled
# one side of the brim higher in all sixteen candidates ("the rim is too curved on one side, noticeable").
import math

SCENE = {"category": "1", "backdrop": "#2fd3e6", "azimuth": 6, "elevation": 18, "lens": 60, "light": "left"}

RB = 0.37          # brim outer radius
CURL = 0.12        # side curl at the brim edge
DIP = 0.02         # dip at the front and back edge


def brim_warp(p):
    x, y, z = p
    rho = math.hypot(x, y)
    if rho < 1e-6:
        return p
    t = max(0.0, (rho - 0.23) / (RB - 0.23)) ** 2
    side = (x / rho) ** 2
    return (x, y, z + CURL * t * side - DIP * t * (1 - side))


def build(k):
    felt = k.mat("#22222b", "satin")
    band = k.mat("#d81e2c", "satin")

    # crown: slightly concave sides flaring to a flat top with a rounded edge
    k.lathe([(0, 0.0), (0.215, 0.0), (0.214, 0.12), (0.218, 0.3), (0.232, 0.5), (0.24, 0.6), (0.238, 0.615),
             (0.228, 0.625), (0, 0.625)], at=(0, 0, 0), rot=(0, 0, 0), m=felt, verts=96)
    # band at the foot of the crown
    k.lathe([(0.21, 0.025), (0.222, 0.025), (0.224, 0.03), (0.226, 0.15), (0.222, 0.155), (0.21, 0.155)],
            at=(0, 0, 0), rot=(0, 0, 0), m=band, verts=96)
    # brim: a thin disc with a rolled edge, curled up evenly at both sides
    brim = k.lathe([(0.18, 0.0), (RB - 0.02, 0.0), (RB, 0.012), (RB + 0.004, 0.03), (RB - 0.012, 0.042),
                    (RB - 0.03, 0.03), (0.18, 0.026)], at=(0, 0, 0), rot=(0, 0, 0), m=felt, verts=192)
    k.warp(brim, brim_warp)

    k.turn(6, 0, 0)
