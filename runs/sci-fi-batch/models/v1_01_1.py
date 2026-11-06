# Rocket on a concrete launch pad: a white body tube with a red ogive nose cone on top. Three red swept fins,
# 120 degrees apart, grow from the base of the body and reach down to the pad. The rocket stands on their tips.
# A short dark nozzle hangs under the body, between the fins and clear of the pad. One blue porthole in a metal
# ring faces the camera. The pad is a plain concrete slab with its top at z = 0, wide enough to run off the card.
import math

SCENE = {"category": "3", "backdrop": "#ffc23a", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f6f4ef", "satin")
    red = k.mat("#e2302b", "satin")
    steel = k.mat("#9aa1ab", "metal")
    dark = k.mat("#3c4048", "metal")
    glass = k.mat("#3a8ee6", "glass")

    r, base, top = 0.13, 0.12, 0.72

    # Body: a slightly rounded tube from the fins to the nose cone.
    k.lathe([(0.0, base), (0.11, base), (0.125, base + 0.006), (r, base + 0.02), (r, top), (0.0, top)],
            at=(0, 0, 0), rot=(0, 0, 0), m=white)

    # Nose cone: tangent ogive, red, full radius on the body and pointed at the top.
    length = 0.32
    rho = (r * r + length * length) / (2 * r)
    nose = [(0.0, top)]
    for i in range(25):
        z = length * i / 24
        rad = math.sqrt(max(rho * rho - z * z, 0.0)) + r - rho
        nose.append((max(rad, 0.0), top + z))
    nose[-1] = (0.0, top + length)
    k.lathe(nose, at=(0, 0, 0), rot=(0, 0, 0), m=red)

    # Nozzle under the body, between the fins.
    k.cone(0.075, 0.05, 0.07, at=(0, 0, base - 0.035), rot=(0, 0, 0), m=dark)

    # Three swept fins. Local x is radial: the root lies along the body, the outer tip touches the pad.
    def sweep(p):
        x, y, z = p
        if x < 0:
            return (x, y, 0.2 if z > 0 else -0.11)
        return (x, y, -0.06 if z > 0 else -0.25)

    for a in (0, 120, 240):
        t = math.radians(a)
        fin = k.box((0.2, 0.032, 0.4), at=(0.22 * math.cos(t), 0.22 * math.sin(t), 0.25),
                    rot=(0, 0, a), m=red, bevel=0.008)
        k.warp(fin, sweep)

    # Porthole facing the camera (azimuth 30 looks from the 300-degree direction).
    d = math.radians(300)
    wx, wy, wz = math.cos(d), math.sin(d), 0.52
    k.torus(0.062, 0.015, at=(0.132 * wx, 0.132 * wy, wz), rot=(90, 0, 30), m=steel)
    k.cyl(0.055, 0.02, at=(0.128 * wx, 0.128 * wy, wz), rot=(90, 0, 30), m=glass)

    # Concrete launch pad.
    k.box((3.2, 3.2, 0.12), at=(0, 0.6, -0.06), m=k.mat("#9a9893", "matte"), bevel=0.02, setting=True)
