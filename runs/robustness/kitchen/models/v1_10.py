# Cookie jar: a round glazed ceramic jar with a hollow neck and a lip. Three cookies stand up inside it and show
# above the rim. The domed red lid sits with its back edge on the back of the lip, a short ring under it dropping
# just inside the neck, and its front is propped up on the cookies. The round knob is on a short stem on top of the
# dome. The jar stands on a white marble countertop that runs off the card. The cow pictogram is a printed mark, so
# it is left to the restyle.
import math

SCENE = {"category": "3", "backdrop": "#5cc45a", "azimuth": 15, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    glaze = k.mat("#f4ead2", "gloss")
    red = k.mat("#d8322a", "gloss")
    cookie = k.mat("#c98a45", "matte")
    chip = k.mat("#5a3320", "matte")

    # Jar body: the outer wall rises to a lip, then the inner wall drops into the jar to a hidden floor.
    k.lathe([(0.0, 0.0), (0.27, 0.0), (0.29, 0.01), (0.32, 0.06), (0.35, 0.18), (0.36, 0.30), (0.35, 0.42),
             (0.31, 0.53), (0.275, 0.585), (0.27, 0.605), (0.285, 0.612), (0.287, 0.625), (0.25, 0.627),
             (0.243, 0.60), (0.24, 0.45), (0.0, 0.45)], at=(0, 0, 0), rot=(0, 0, 0), m=glaze)

    # Cookies stand up inside the neck, faces to the front, their tops showing above the rim. The chips are
    # scattered unevenly so they read as chocolate chips, not eyes.
    chips = {
        0: ((-0.06, 0.03), (-0.01, 0.075), (0.045, 0.045), (0.02, 0.095), (-0.045, 0.085)),
        1: ((-0.055, 0.06), (0.0, 0.035), (0.03, 0.09), (0.065, 0.055), (-0.025, 0.1), (0.075, 0.03)),
        2: ((-0.05, 0.08), (-0.015, 0.04), (0.04, 0.065), (0.06, 0.03)),
    }
    for i, (x, y, zc, tilt) in enumerate(((-0.11, -0.06, 0.605, 8), (0.0, -0.11, 0.6, -3), (0.11, -0.05, 0.60, -10))):
        k.cyl(0.11, 0.026, at=(x, y, zc), rot=(90, 0, tilt), m=cookie, bevel=0.008)
        for dx, dz in chips[i]:
            if zc + dz > 0.635 and dx * dx + dz * dz < 0.095 ** 2:
                k.sphere(0.01, at=(x + dx, y - 0.014, zc + dz), scale=(1.2, 0.5, 0.9), m=chip)

    # Lid: its back edge rests on the back of the lip and its front is propped up on the cookies.
    tilt = -14.0
    a = math.radians(tilt)
    pivot = (0.0, 0.27, 0.627)

    def place(p):
        x, y, z = p[0], p[1] - 0.27, p[2]
        return (pivot[0] + x, pivot[1] + y * math.cos(a) - z * math.sin(a), pivot[2] + y * math.sin(a) + z * math.cos(a))

    dome = [(0.0, 0.0), (0.27, 0.0), (0.30, 0.008), (0.302, 0.025), (0.285, 0.035)]
    for i in range(1, 13):
        t = math.radians(i * 90 / 12)
        dome.append((0.285 * math.cos(t), 0.035 + 0.13 * math.sin(t)))
    k.lathe(dome, at=place((0, 0, 0)), rot=(tilt, 0, 0), m=red)
    # A short ring under the lid that drops just inside the neck at the back.
    k.lathe([(0.225, -0.03), (0.235, -0.03), (0.235, 0.0), (0.225, 0.0)], at=place((0, 0, 0)), rot=(tilt, 0, 0), m=red)
    k.cyl(0.03, 0.05, at=place((0, 0, 0.18)), rot=(tilt, 0, 0), m=red)
    k.sphere(0.06, at=place((0, 0, 0.235)), m=red)

    # White marble countertop, its top at z = 0, running off the card on every side.
    k.box((4.5, 3.4, 0.12), at=(0, 0.5, -0.06), m=k.mat("#f3f1ed", "gloss"), bevel=0.01, setting=True)
