# Rocket: a slim white hull rises into a pointed nose cone with a small red tip and a red band at the joint.
# One round porthole with a metal rim sits on the front. Three red swept fins stand 120 degrees apart, their roots
# on the hull and their outer tips reaching below the tail. A dark metal engine bell sits under the tail.
# A small glowing plume hangs from the bell: a yellow-white teardrop core with five short orange tongues around
# its top that curl upward. The image model grows the fire. The whole rocket tilts to fly up and to the right.
import math

SCENE = {"category": "1", "backdrop": "#4fb4f2", "azimuth": 28, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f6f7fa", "satin")
    red = k.mat("#e3262e", "satin")
    steel = k.mat("#5b6270", "metal")
    rim = k.mat("#c9ced6", "metal")
    glass = k.mat("#5fd0ff", "glass")
    core = k.mat("#fff4b0", "glow")
    fire = k.mat("#ff8a1f", "glow")

    # Hull and nose: base at z 0.20, full radius 0.14, nose narrowing to z 1.13, red tip to 1.22.
    k.lathe([(0.0, 0.20), (0.115, 0.20), (0.128, 0.24), (0.137, 0.32), (0.14, 0.42), (0.14, 0.78),
             (0.138, 0.84), (0.132, 0.90), (0.121, 0.96), (0.106, 1.02), (0.087, 1.07), (0.065, 1.11),
             (0.052, 1.13), (0.0, 1.13)], at=(0, 0, 0), m=white)
    k.lathe([(0.0, 1.125), (0.054, 1.125), (0.045, 1.15), (0.033, 1.175), (0.018, 1.20), (0.0, 1.22)],
            at=(0, 0, 0), m=red)
    k.torus(0.141, 0.012, at=(0, 0, 0.80), m=red)

    # Porthole on the front (-y): metal rim ring around a glass disc set into the hull.
    k.torus(0.058, 0.015, at=(0, -0.136, 0.62), rot=(90, 0, 0), m=rim)
    k.cyl(0.05, 0.02, at=(0, -0.132, 0.62), rot=(90, 0, 0), m=glass)

    # Three swept fins. Each is built at the origin and warped into place: local x runs radially outward
    # from the hull (root at radius 0.12), the outer edge drops to sweep the fin down past the tail.
    for angle in (-30, 90, 210):
        a = math.radians(angle)
        c, s = math.cos(a), math.sin(a)
        fin = k.box((0.17, 0.03, 0.30), at=(0, 0, 0), m=red, bevel=0.01)

        def place(p, c=c, s=s):
            x, y, z = p
            if x > 0:
                z -= 0.15 if z > 0 else 0.08
            x += 0.205
            z += 0.38
            return (x * c - y * s, x * s + y * c, z)

        k.warp(fin, place)

    # Engine bell under the tail, flaring downward.
    k.lathe([(0.0, 0.07), (0.105, 0.07), (0.095, 0.09), (0.08, 0.13), (0.072, 0.17), (0.075, 0.205),
             (0.0, 0.205)], at=(0, 0, 0), m=steel)

    # Plume: a yellow-white teardrop core under the bell, short orange tongues curling up around its top.
    k.lathe([(0.0, -0.24), (0.025, -0.20), (0.05, -0.15), (0.075, -0.09), (0.092, -0.03), (0.098, 0.03),
             (0.09, 0.075), (0.0, 0.075)], at=(0, 0, 0), m=core)
    for i in range(5):
        a = math.radians(i * 72 + 15)
        c, s = math.cos(a), math.sin(a)
        k.blob([(0.09 * c, 0.09 * s, 0.0, 0.045),
                (0.125 * c, 0.125 * s, 0.04, 0.03),
                (0.14 * c, 0.14 * s, 0.085, 0.018)], fire)

    k.turn(0, 22, 0)
