# Oil lantern (hurricane style): a round iron fuel tank carries the burner collar; the glass globe sits on the
# collar and the vented top cap sits on the globe. Four iron guard rods run from the tank rim, bow out around the
# globe through a mid ring and end under the cap. The bail handle swings on two pins on the cap's sides, and its
# ends sit on the pins. A wick rises from the burner inside the globe and holds the flame: a yellow-white core
# with an orange tip.
import math

SCENE = {"category": "1", "backdrop": "#2fd3e6", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    iron = k.mat("#1f1f22", "satin")
    glass = k.mat("#eef8ff", "glass")
    wick = k.mat("#3a2c22", "matte")

    # fuel tank
    k.lathe([(0, 0.0), (0.2, 0.0), (0.23, 0.025), (0.245, 0.07), (0.24, 0.11), (0.22, 0.15),
             (0.18, 0.18), (0.15, 0.19), (0, 0.19)], at=(0, 0, 0), rot=(0, 0, 0), m=iron)
    # burner collar, which is also the globe seat
    k.lathe([(0, 0.185), (0.15, 0.185), (0.155, 0.21), (0.15, 0.24), (0.13, 0.245), (0, 0.245)],
            at=(0, 0, 0), rot=(0, 0, 0), m=iron)
    # wick standing on the burner
    k.cyl(0.026, 0.035, at=(0, 0, 0.26), rot=(0, 0, 0), m=wick)

    # glass globe, open at both ends, resting on the collar and holding up the cap
    k.lathe([(0.12, 0.24), (0.14, 0.27), (0.165, 0.33), (0.175, 0.42), (0.165, 0.51), (0.14, 0.57),
             (0.125, 0.6), (0.125, 0.63)], at=(0, 0, 0), rot=(0, 0, 0), m=glass)

    # vented top cap and chimney
    k.lathe([(0, 0.615), (0.135, 0.615), (0.155, 0.635), (0.15, 0.665), (0.11, 0.705), (0.07, 0.735),
             (0.06, 0.75), (0.06, 0.79), (0.075, 0.8), (0.075, 0.815), (0, 0.82)],
            at=(0, 0, 0), rot=(0, 0, 0), m=iron)

    # four guard rods from the tank rim to under the cap, through a mid ring
    for x, y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        pts = [(x * r, y * r, z) for r, z in
               ((0.205, 0.17), (0.215, 0.3), (0.222, 0.42), (0.2, 0.54), (0.145, 0.63))]
        k.tube(pts, 0.014, iron, curved=True)
    k.torus(0.222, 0.013, at=(0, 0, 0.42), rot=(0, 0, 0), m=iron)

    # bail handle: pins on the cap's sides, and an arch whose ends sit on the pins
    for s in (-1, 1):
        k.cyl(0.02, 0.05, at=(s * 0.125, 0, 0.7), rot=(0, 90, 0), m=iron)
    arch = [(0.15 * math.cos(math.pi * i / 24), 0, 0.7 + 0.27 * math.sin(math.pi * i / 24)) for i in range(25)]
    k.tube(arch, 0.015, iron, curved=True)

    # flame on the wick: bright yellow-white core, orange tip
    k.blob([(0, 0, 0.315, 0.034, (1, 1, 1.5)), (0, 0, 0.35, 0.026)], k.mat("#fff4b8", "glow"))
    k.blob([(0, 0, 0.385, 0.02, (1, 1, 1.6)), (0, 0, 0.415, 0.011)], k.mat("#ff8a1e", "glow"))

    k.turn(0, 6, 0)
