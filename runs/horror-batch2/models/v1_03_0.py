# Cauldron on a fireplace hearth: a round iron pot (lathe) with a thick rolled rim, two ring handles that hang
# through lugs cast on the sides, and three short splayed legs whose feet stand on the hearth stones. The pot is
# filled to just under the rim with a flat green potion surface; big bubbles sit half-sunk in it. Under the pot,
# three logs lie on the hearth between the legs, meeting at the middle, with glowing cut ends and a low glowing
# core and a few short flame tongues that reach up toward the pot's bottom. Setting: flagstone hearth floor and
# the sooty stone back wall of the fireplace, close behind.
import math

SCENE = {"category": "4", "backdrop": "#6a3fb0", "azimuth": 28, "elevation": 11, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#26262b", "satin")
    potion = k.mat("#5fe03a", "gloss")
    bubble = k.mat("#8ff25e", "gloss")
    wood = k.mat("#6b3f22", "matte")
    ember = k.mat("#ff7a1a", "glow")
    core = k.mat("#fff2a8", "glow")
    flame = k.mat("#ff9a2a", "glow")

    # Pot body: round belly, slight neck, closed at the potion level.
    profile = [(0.0, 0.16), (0.10, 0.165), (0.18, 0.18), (0.25, 0.205), (0.31, 0.24), (0.36, 0.29),
               (0.395, 0.35), (0.415, 0.42), (0.418, 0.48), (0.41, 0.54), (0.39, 0.60), (0.37, 0.65),
               (0.36, 0.69), (0.36, 0.71), (0.0, 0.71)]
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=iron)
    k.torus(0.37, 0.04, at=(0, 0, 0.72), rot=(0, 0, 0), m=iron)

    # Potion surface and half-sunk bubbles.
    k.cyl(0.345, 0.02, at=(0, 0, 0.72), rot=(0, 0, 0), m=potion, bevel=0.004)
    for x, y, r in ((-0.12, -0.08, 0.075), (0.10, 0.06, 0.06), (0.05, -0.17, 0.045), (-0.05, 0.18, 0.05),
                    (0.2, -0.05, 0.035), (-0.22, 0.06, 0.04)):
        k.sphere(r, at=(x, y, 0.725), scale=(1, 1, 0.85), m=bubble)

    # Side handles: a lug on each side, a ring hanging through it.
    for s in (-1, 1):
        k.box((0.07, 0.07, 0.05), at=(s * 0.405, 0, 0.635), m=iron, bevel=0.012)
        k.torus(0.075, 0.018, at=(s * 0.455, 0, 0.575), rot=(90, 0, 0), m=iron)

    # Three short legs, splayed, feet on the hearth.
    for a in (90, 210, 330):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        k.tube([(0.24 * c, 0.24 * s, 0.24), (0.31 * c, 0.31 * s, 0.03)], 0.034, iron)
        k.sphere(0.042, at=(0.315 * c, 0.315 * s, 0.03), scale=(1, 1, 0.7), m=iron)

    # Fire: three logs between the legs meeting under the pot, glowing ends, core and short flames.
    for a in (30, 150, 270):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        k.cyl(0.045, 0.46, at=(0.25 * c, 0.25 * s, 0.045), rot=(0, 90, a), m=wood, bevel=0.01)
        k.cyl(0.04, 0.012, at=(0.482 * c, 0.482 * s, 0.045), rot=(0, 90, a), m=ember, bevel=0.003)
    k.blob([(0, 0, 0.07, 0.09, (1.3, 1.3, 0.7)), (0.06, -0.05, 0.06, 0.06)], core)
    for x, y, h, r in ((0.13, -0.12, 0.12, 0.04), (-0.12, -0.13, 0.10, 0.035), (0.0, -0.20, 0.09, 0.03),
                      (0.2, 0.05, 0.1, 0.035), (-0.18, 0.08, 0.09, 0.03)):
        k.cone(r, 0.004, h, at=(x, y, 0.07 + h / 2), rot=(0, 0, 0), m=flame)

    # Hearth: flagstones and the fireplace back wall.
    stones = ("#7d7488", "#8d8597", "#6f6779")
    for i in range(-3, 4):
        for j in range(-3, 3):
            w = 0.58
            k.box((w, w, 0.06), at=(i * 0.62 + (0.31 if j % 2 else 0), j * 0.62 + 0.1, -0.03),
                  m=k.mat(stones[(i + j) % 3], "matte"), bevel=0.02, setting=True)
    k.box((8, 8, 0.02), at=(0, 0, -0.07), m=k.mat("#3b3346", "matte"), bevel=0, setting=True)
    for i in range(-4, 5):
        for row in range(4):
            k.box((0.5, 0.2, 0.3), at=(i * 0.54 + (0.27 if row % 2 else 0), 1.35, 0.16 + row * 0.33),
                  m=k.mat("#4a3f5c" if (i + row) % 2 else "#55496a", "matte"), bevel=0.03, setting=True)
