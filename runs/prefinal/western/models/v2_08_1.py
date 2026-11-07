# Cast iron hand pump: a flanged round body is bolted with four bolts to a flat stone slab in a dirt yard. A spout
# leaves the body's left side and turns down. On the cap, a forked bracket holds the bolt the long red handle turns
# on; the handle's short inner end links to the plunger rod rising from the cap's centre, and the long arm curves
# out and down to the right with a rounded grip.
import math

SCENE = {"category": "4", "backdrop": "#ffd66b", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#2f6b45", "satin")
    dark = k.mat("#24543a", "satin")
    red = k.mat("#d8322a", "satin")
    bolt = k.mat("#4a4f57", "metal")
    top = 0.08  # top of the stone slab

    # Base flange and bolts.
    k.cyl(0.19, 0.04, at=(0, 0, top + 0.02), m=dark, bevel=0.01)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        x, y = 0.15 * math.cos(a), 0.15 * math.sin(a)
        k.cyl(0.024, 0.025, at=(x, y, top + 0.052), m=bolt, bevel=0.004, verts=6)

    # Round body with a waist, a belly and a lipped cap.
    profile = [(0.15, top + 0.04), (0.14, top + 0.08), (0.115, top + 0.14), (0.105, top + 0.24),
               (0.11, top + 0.32), (0.13, top + 0.40), (0.14, top + 0.48), (0.14, top + 0.60),
               (0.13, top + 0.66), (0.15, top + 0.67), (0.15, top + 0.70), (0.12, top + 0.72),
               (0.07, top + 0.75), (0, top + 0.755)]
    k.lathe(profile, at=(0, 0, 0), m=iron)
    k.torus(0.135, 0.014, at=(0, 0, top + 0.40), m=dark)

    # Spout: leaves the body on the left and bends down.
    spout = [(-0.08, 0, top + 0.50), (-0.22, 0, top + 0.50), (-0.30, 0, top + 0.47), (-0.33, 0, top + 0.38)]
    k.tube(spout, 0.04, iron, curved=True)
    k.cyl(0.048, 0.03, at=(-0.33, 0, top + 0.37), m=dark, bevel=0.006)

    # Forked bracket on the cap with the pivot bolt.
    piv = (0.12, top + 0.86)
    for y in (-0.04, 0.04):
        k.box((0.05, 0.022, 0.18), at=(0.11, y, top + 0.79), m=iron, bevel=0.006)
    k.cyl(0.016, 0.12, at=(piv[0], 0, piv[1]), rot=(90, 0, 0), m=bolt)

    # Plunger rod from the cap up to the handle's inner end, with its link pin.
    k.cyl(0.018, 0.17, at=(-0.03, 0, top + 0.80), m=bolt)
    k.cyl(0.012, 0.09, at=(-0.03, 0, top + 0.885), rot=(90, 0, 0), m=bolt)

    # Long curved red handle through the pivot.
    handle = [(-0.06, 0, top + 0.89), (piv[0], 0, piv[1]), (0.32, 0, top + 0.86),
              (0.50, 0, top + 0.78), (0.62, 0, top + 0.66)]
    k.tube(handle, 0.026, red, curved=True)
    k.sphere(0.04, at=(0.635, 0, top + 0.645), scale=(1, 1, 1.2), m=red)

    # Setting: the stone slab on a dirt yard.
    k.box((0.75, 0.65, top), at=(0, 0, top / 2), rot=(0, 0, 4), m=k.mat("#857e72", "matte"), bevel=0.015,
          setting=True)
    k.floor("#b5814c")
