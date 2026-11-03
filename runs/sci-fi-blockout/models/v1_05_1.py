# Space helmet: a round white shell sits down into a wide collar ring that rests on the ledge. The big gold visor
# is a curved glass dome set into the front of the shell, framed by a rim tube that follows the line where visor
# and shell meet. A thin red stripe runs around the collar.
import math

SCENE = {"category": "2", "backdrop": "#f27fb2", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    trim = k.mat("#c9ced6", "metal")
    visor = k.mat("#e3a92f", "glass")
    red = k.mat("#e0332e", "satin")

    # Shell: a sphere sunk into the collar, so it meets the ring near the ring's own width.
    shell_c, shell_r = (0.0, 0.0, 0.47), 0.42
    k.sphere(shell_r, at=shell_c, m=white)

    # Wide, low collar ring under the shell, standing on the ledge.
    k.lathe([(0.0, 0.0), (0.33, 0.0), (0.35, 0.02), (0.35, 0.13), (0.335, 0.155), (0.29, 0.175), (0.0, 0.175)],
            at=(0, 0, 0), m=white)
    k.cyl(0.353, 0.03, at=(0, 0, 0.07), m=red, bevel=0.004)
    k.torus(0.315, 0.022, at=(0, 0, 0.165), m=trim)

    # Visor: an ellipsoid dome pushed out through the front of the shell.
    cy, cz, ax, ay, az = -0.17, 0.51, 0.32, 0.29, 0.26
    k.sphere(1.0, at=(0, cy, cz), scale=(ax, ay, az), m=visor)

    # Rim along the visor/shell seam, found by bisecting the visor surface against the shell sphere.
    def on_visor(theta, phi):
        s = math.sin(phi)
        return (ax * s * math.cos(theta), cy - ay * math.cos(phi), cz + az * s * math.sin(theta))

    def outside(p):
        return math.dist(p, shell_c) > shell_r

    rim = []
    for i in range(-2, 40):
        theta = 2 * math.pi * i / 36
        lo, hi = 0.0, math.pi / 2
        for _ in range(30):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if outside(on_visor(theta, mid)) else (lo, mid)
        rim.append(on_visor(theta, lo))
    k.tube(rim, 0.026, trim, curved=True)

    # White metal ledge.
    k.box((4, 1.6, 0.12), at=(0, 0.3, -0.06), m=k.mat("#eef0f4", "metal"), bevel=0.01, setting=True)
