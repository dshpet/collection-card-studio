# Rocket: a silver lathed body with a white band under a pointed red nose cone. Three red swept fins sit
# 120 degrees apart around the base, their roots sunk into the hull. A round porthole with a red rim faces front.
# A dark nozzle closes the tail and holds a small glowing yellow flame. It floats, tilted on a diagonal, nose up-right.
import math

SCENE = {"category": "1", "backdrop": "#4cc3f2", "azimuth": 28, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#d3d8df", "metal")
    white = k.mat("#f6f6f2", "satin")
    red = k.mat("#e0302b", "satin")
    dark = k.mat("#5a5f68", "metal")
    glass = k.mat("#7fe3ff", "glass")
    flame = k.mat("#ffd23a", "glow")

    # Hull: rounded tail, full belly, slight taper toward the nose.
    hull = [(0.0, 0.12), (0.10, 0.12), (0.135, 0.14), (0.155, 0.18), (0.166, 0.24), (0.170, 0.32),
            (0.170, 0.42), (0.167, 0.52), (0.161, 0.60), (0.153, 0.67), (0.148, 0.71), (0.0, 0.71)]
    k.lathe(hull, at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # White band where hull meets nose.
    k.cyl(0.156, 0.04, at=(0, 0, 0.725), rot=(0, 0, 0), m=white, bevel=0.008)

    # Pointed red nose cone (ogive).
    nose = []
    for i in range(25):
        t = i / 24
        nose.append((0.15 * (1 - t ** 1.7) ** 0.75, 0.745 + 0.33 * t))
    nose[-1] = (0.0, 1.075)
    k.lathe(nose, at=(0, 0, 0), rot=(0, 0, 0), m=red)

    # Three swept fins, roots inside the hull; two flank the front, one at the back.
    for ang in (90, 210, 330):
        a = math.radians(ang)
        fin = k.box((0.17, 0.032, 0.30), at=(0, 0, 0), rot=(0, 0, 0), m=red, bevel=0.01)

        def shape(p, a=a, r=0.225):
            x, y, z = p
            if x > 0 and z > 0:
                x, z = 0.0, z - 0.02       # leading edge sweeps back to the hull
            elif x > 0 and z < 0:
                z -= 0.07                  # tip reaches down past the tail
            return (r * math.cos(a) + x * math.cos(a) - y * math.sin(a),
                    r * math.sin(a) + x * math.sin(a) + y * math.cos(a),
                    0.28 + z)

        k.warp(fin, shape)

    # Porthole on the front face.
    k.torus(0.068, 0.018, at=(0, -0.168, 0.47), rot=(90, 0, 0), m=red)
    k.cyl(0.062, 0.03, at=(0, -0.158, 0.47), rot=(90, 0, 0), m=glass, bevel=0.006)

    # Nozzle under the tail and a small flame held in it.
    k.lathe([(0.0, 0.135), (0.075, 0.135), (0.08, 0.10), (0.10, 0.04), (0.085, 0.04), (0.0, 0.07)],
            at=(0, 0, 0), rot=(0, 0, 0), m=dark)
    k.sphere(0.055, at=(0, 0, 0.0), scale=(1, 1, 1.7), m=flame)

    k.turn(8, 28, 18)
