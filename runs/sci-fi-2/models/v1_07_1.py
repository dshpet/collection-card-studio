# Space station: a round hub sits on the middle of a long tube body, with docking collars on both tube ends.
# Near each end a mast crosses the tube vertically, and each mast carries two large blue solar panels, one above
# and one below the tube, so four panels in all; each panel has a raised gray frame and ribs. The hub carries an
# even ring of small portholes all around between two gray bands. A short antenna on top of the hub ends in a
# small red light. Setting: open space, with a large blue planet low behind on the right.
import math

SCENE = {"category": "4", "backdrop": "#3fa9ec", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    gray = k.mat("#9aa1ab", "metal")
    dark = k.mat("#5c636e", "satin")
    blue = k.mat("#2f6fe0", "gloss")
    window = k.mat("#2a3f66", "glass")
    red = k.mat("#ff2a2a", "glow")

    # Tube body along x, with gray bands and docking collars at both ends.
    k.cyl(0.08, 1.12, at=(0, 0, 0), rot=(0, 90, 0), m=white, bevel=0.01)
    for x in (-0.27, 0.27):
        k.cyl(0.092, 0.04, at=(x, 0, 0), rot=(0, 90, 0), m=gray, bevel=0.006)
    for side in (-1, 1):
        k.cyl(0.095, 0.05, at=(side * 0.585, 0, 0), rot=(0, 90, 0), m=gray, bevel=0.008)
        k.cyl(0.055, 0.04, at=(side * 0.63, 0, 0), rot=(0, 90, 0), m=dark, bevel=0.006)

    # Round central hub: two gray bands, with an even ring of small portholes all around between them.
    k.sphere(0.19, at=(0, 0, 0), m=white)
    k.torus(0.19, 0.016, at=(0, 0, 0), rot=(0, 0, 0), m=gray)
    k.torus(0.168, 0.014, at=(0, 0, 0.09), rot=(0, 0, 0), m=gray)
    for i in range(12):
        a = i * 30 + 15
        t = math.radians(a)
        x, y = 0.176 * math.sin(t), -0.176 * math.cos(t)
        k.cyl(0.018, 0.02, at=(x, y, 0.046), rot=(90, 0, a), m=window, bevel=0.003)

    # Antenna on top of the hub with the small red light.
    k.cyl(0.035, 0.03, at=(0, 0, 0.19), m=gray, bevel=0.005)
    k.tube([(0, 0, 0.18), (0, 0, 0.33)], 0.012, gray)
    k.sphere(0.028, at=(0, 0, 0.345), m=red)

    # Two masts cross the tube; each carries an upper and a lower solar panel (four panels).
    for x in (-0.43, 0.43):
        k.cyl(0.026, 1.24, at=(x, 0, 0), m=gray, bevel=0.005)
        k.cyl(0.04, 0.2, at=(x, 0, 0), m=dark, bevel=0.006)
        for zs in (-1, 1):
            zc = zs * 0.37
            k.box((0.34, 0.016, 0.46), at=(x, -0.03, zc), m=blue, bevel=0.004)
            # Raised frame and ribs on the panel's front face.
            k.box((0.36, 0.026, 0.022), at=(x, -0.032, zc + 0.235), m=gray, bevel=0.004)
            k.box((0.36, 0.026, 0.022), at=(x, -0.032, zc - 0.235), m=gray, bevel=0.004)
            for sx in (-0.175, 0.175):
                k.box((0.022, 0.026, 0.49), at=(x + sx, -0.032, zc), m=gray, bevel=0.004)
            for dz in (-0.077, 0.077):
                k.box((0.34, 0.022, 0.012), at=(x, -0.034, zc + dz), m=gray, bevel=0.003)
            k.box((0.012, 0.022, 0.46), at=(x, -0.034, zc), m=gray, bevel=0.003)
            # Bracket joining the panel to the mast where it leaves the tube.
            k.box((0.05, 0.03, 0.06), at=(x, -0.012, zs * 0.13), m=dark, bevel=0.005)

    k.turn(6, 0, -4)

    # Setting: one large blue planet low behind the station on the right, a clear arc of it in view.
    k.sphere(3.0, at=(1.9, 5.5, -2.4), m=k.mat("#2b7fd8", "matte"), setting=True)
