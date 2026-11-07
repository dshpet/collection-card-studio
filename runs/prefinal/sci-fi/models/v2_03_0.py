# Rocket: a cream round body with an orange ogive nose cone on top and an orange band near the base. Three swept
# orange fins sit at 120 degrees on the lower body, their roots set into the hull. A round yellow window with a
# thick orange rim faces the front. A dark metal nozzle hangs under the base, and a short glowing flame (white-yellow
# core inside an orange sheath) comes out of it; the flame is left out of the framing so it can run off the card
# and the image model can grow the fire. The rocket floats, tilted to fly up and to the right.
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

    # Nose cone: ogive from the body radius to a rounded tip.
    nose = [(0.172, 0.715)]
    for i in range(1, 17):
        t = i / 16
        nose.append((0.172 * math.cos(t * math.pi / 2) ** 0.8, 0.715 + 0.34 * math.sin(t * math.pi / 2)))
    nose[-1] = (0.0, nose[-1][1])
    k.lathe(nose, at=(0, 0, 0), m=orange)

    # Orange band near the base.
    k.torus(0.172, 0.018, at=(0, 0, 0.25), m=orange)

    # Three swept fins, roots inside the hull, bottoms reaching below the base.
    for ang in (-30, -150, 90):
        a = math.radians(ang)
        cx, cy = 0.235 * math.cos(a), 0.235 * math.sin(a)
        k.box((0.17, 0.04, 0.28), at=(cx, cy, 0.18), rot=(0, -16, ang), m=orange, bevel=0.018)

    # Round window facing the front (-y).
    k.torus(0.072, 0.02, at=(0, -0.172, 0.5), rot=(90, 0, 0), m=orange)
    k.cyl(0.066, 0.03, at=(0, -0.165, 0.5), rot=(90, 0, 0), m=glass)

    # Engine nozzle under the base.
    k.lathe([(0.0, 0.17), (0.075, 0.17), (0.07, 0.13), (0.085, 0.09), (0.11, 0.055), (0.095, 0.05),
             (0.0, 0.05)], at=(0, 0, 0), m=steel)

    # Short flame from the nozzle: orange sheath with a white-yellow core.
    outer = [(0.0, -0.3), (0.03, -0.24), (0.06, -0.15), (0.085, -0.05), (0.095, 0.02), (0.08, 0.06), (0.0, 0.06)]
    core = [(0.0, -0.18), (0.025, -0.13), (0.05, -0.05), (0.06, 0.02), (0.05, 0.065), (0.0, 0.065)]
    flame = k.lathe(outer, at=(0, 0, 0), m=k.mat("#ff8a1f", "glow"))
    flame_core = k.lathe(core, at=(0, -0.012, 0), m=k.mat("#fff4b0", "glow"))
    k.unframed(flame, flame_core)

    # Fly up and to the right, leaning a little toward the camera to show the window.
    k.turn(-6, 20, 0)
