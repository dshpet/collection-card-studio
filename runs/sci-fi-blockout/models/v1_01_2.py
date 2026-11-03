# Classic rocket: a silver lathed body with a red pointed nose cone on top and a dark nozzle under the tail; three
# red swept fins sit at 120 degrees, two spread to the sides of the camera's view and one behind, their root edges
# sunk into the body; two round portholes with metal rims face the camera above the fins. A small glowing flame
# hangs from the nozzle. It floats, leaning up and to the right.
import math

SCENE = {"category": "1", "backdrop": "#45b6f0", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#d3d8de", "metal")
    red = k.mat("#e2312b", "satin")
    rim = k.mat("#8b9097", "metal")
    glass = k.mat("#5fd3f5", "glass")
    dark = k.mat("#4a4f57", "metal")

    k.lathe([(0, 0.12), (0.11, 0.12), (0.135, 0.15), (0.155, 0.22), (0.165, 0.35), (0.165, 0.55),
             (0.16, 0.65), (0.152, 0.72), (0, 0.72)], at=(0, 0, 0), rot=(0, 0, 0), m=silver)
    nose = [(0, 0.71)]
    for i in range(13):
        t = i / 12
        nose.append((0.153 * math.cos(t * math.pi / 2) ** 0.8, 0.71 + 0.3 * t))
    nose[-1] = (0, 1.01)
    k.lathe(nose, at=(0, 0, 0), rot=(0, 0, 0), m=red)
    k.torus(0.156, 0.014, at=(0, 0, 0.715), rot=(0, 0, 0), m=red)

    k.lathe([(0.075, 0.13), (0.085, 0.10), (0.105, 0.065), (0.09, 0.06), (0, 0.06)], at=(0, 0, 0),
            rot=(0, 0, 0), m=dark)
    k.lathe([(0, 0.075), (0.07, 0.07), (0.068, 0.02), (0.05, -0.04), (0.025, -0.1), (0, -0.13)], at=(0, 0, 0),
            rot=(0, 0, 0), m=k.mat("#ffc93a", "glow"))

    for deg in (0, 120, 240):
        a = math.radians(deg)
        fin = k.box((0.18, 0.03, 0.26), at=(0.2 * math.cos(a), 0.2 * math.sin(a), 0.24), rot=(0, 0, deg),
                    m=red, bevel=0.012)
        k.warp(fin, lambda p: (p[0], p[1], p[2] - (0.12 if p[2] > 0 else 0.05) if p[0] > 0 else p[2]))

    face = math.radians(-60)
    for z, r in ((0.58, 0.058), (0.43, 0.048)):
        dx, dy = math.cos(face), math.sin(face)
        k.torus(r, 0.016, at=(0.168 * dx, 0.168 * dy, z), rot=(90, 0, 30), m=rim)
        k.cyl(r, 0.02, at=(0.16 * dx, 0.16 * dy, z), rot=(90, 0, 30), m=glass)

    k.turn(6, 22, 0)
