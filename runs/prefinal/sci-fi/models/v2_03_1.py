# Rocket: a cream round body with an orange ogive nose cone on top and an orange band near the base. Three swept
# orange fins sit at 120 degrees on the lower body: each is a trapezoid whose long root is set into the hull, whose
# leading edge rakes back and whose tip reaches below the base. A round yellow window with a thick orange rim faces
# the front. A dark metal nozzle hangs under the base, and a glowing flame (white-yellow core inside a wider orange
# sheath) comes out of it; the flame is left out of the framing so the image model can grow the fire. The rocket
# floats, tilted to fly up and to the right.
import math

SCENE = {"category": "1", "backdrop": "#3a9ff0", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    cream = k.mat("#f4ead2", "satin")
    orange = k.mat("#f27a1a", "satin")
    steel = k.mat("#5a5f68", "metal")
    glass = k.mat("#ffd23a", "glass")

    # Body: rounded shoulder at the base, slight bulge, meets the nose at z = 0.72.
    body = [(0.0, 0.16), (0.10, 0.16), (0.14, 0.175), (0.16, 0.2), (0.172, 0.26), (0.178, 0.4),
            (0.177, 0.55), (0.172, 0.68), (0.168, 0.72), (0.0, 0.72)]
    k.lathe(body, at=(0, 0, 0), m=cream)

    # Nose cone: ogive tapering from the body radius to a near point.
    nose = [(0.172, 0.715)]
    for i in range(1, 21):
        t = i / 20
        nose.append((0.172 * (1 - t ** 1.8) ** 0.7, 0.715 + 0.4 * t))
    nose[-1] = (0.0, nose[-1][1])
    k.lathe(nose, at=(0, 0, 0), m=orange)

    # Orange band near the base.
    k.torus(0.172, 0.018, at=(0, 0, 0.25), m=orange)

    # Three swept fins: a box sheared into a trapezoid, the root (inner edge) buried in the hull.
    def sweep(p):
        x, y, z = p
        if x > 0 and z > 0:
            x -= 0.09
        if x > 0 and z < 0:
            z -= 0.07
        return (x, y, z)

    for ang in (-30, -150, 90):
        a = math.radians(ang)
        cx, cy = 0.225 * math.cos(a), 0.225 * math.sin(a)
        fin = k.box((0.17, 0.04, 0.30), at=(cx, cy, 0.24), rot=(0, 0, ang), m=orange, bevel=0.015)
        k.warp(fin, sweep)

    # Round window facing the front (-y).
    k.torus(0.072, 0.02, at=(0, -0.172, 0.5), rot=(90, 0, 0), m=orange)
    k.cyl(0.066, 0.03, at=(0, -0.165, 0.5), rot=(90, 0, 0), m=glass)

    # Engine nozzle under the base.
    k.lathe([(0.0, 0.17), (0.075, 0.17), (0.07, 0.13), (0.085, 0.09), (0.11, 0.055), (0.095, 0.05),
             (0.0, 0.05)], at=(0, 0, 0), m=steel)

    # Flame from the nozzle: a wide orange sheath with a shorter white-yellow core inside it.
    outer = [(0.0, -0.36), (0.035, -0.28), (0.075, -0.17), (0.105, -0.06), (0.115, 0.02), (0.09, 0.06),
             (0.0, 0.06)]
    core = [(0.0, -0.17), (0.025, -0.12), (0.045, -0.05), (0.055, 0.02), (0.045, 0.065), (0.0, 0.065)]
    flame = k.lathe(outer, at=(0, 0, 0), m=k.mat("#ff6a10", "glow"))
    flame_core = k.lathe(core, at=(0, -0.02, 0), m=k.mat("#fff4b0", "glow"))
    k.unframed(flame, flame_core)

    # Fly up and to the right, leaning a little toward the camera to show the window.
    k.turn(-6, 20, 0)
