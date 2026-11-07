# Box gramophone on a polished wooden desk: a wooden cabinet on a plinth, a turntable platter with a black
# record on the lid, a brass neck rising from the back of the lid into a large flared horn that opens forward
# over the record, a short tone arm from the neck base to a soundbox resting on the record, and a crank on the
# right side of the cabinet.
import math

SCENE = {"category": "3", "backdrop": "#5b2a86", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#7a4220", "satin")
    trim = k.mat("#5e3118", "satin")
    brass = k.mat("#d9a335", "metal")
    disc = k.mat("#151515", "gloss")
    felt = k.mat("#2a2a2a", "matte")

    # Cabinet: plinth, body, lid, raised front panel
    k.box((0.56, 0.50, 0.04), at=(0, 0, 0.02), m=trim, bevel=0.01)
    k.box((0.50, 0.44, 0.24), at=(0, 0, 0.16), m=wood, bevel=0.012)
    k.box((0.54, 0.48, 0.03), at=(0, 0, 0.295), m=trim, bevel=0.01)
    k.box((0.38, 0.012, 0.14), at=(0, -0.224, 0.16), m=trim, bevel=0.006)

    # Turntable platter, record and spindle
    k.cyl(0.19, 0.02, at=(-0.02, -0.03, 0.32), rot=(0, 0, 0), m=felt)
    k.cyl(0.18, 0.008, at=(-0.02, -0.03, 0.334), rot=(0, 0, 0), m=disc)
    k.cyl(0.055, 0.01, at=(-0.02, -0.03, 0.336), rot=(0, 0, 0), m=k.mat("#c9a24a", "satin"))
    k.cyl(0.008, 0.03, at=(-0.02, -0.03, 0.35), rot=(0, 0, 0), m=brass)

    # Horn neck: base flange on the lid at the back right, rising and bending forward into the horn
    nx, ny = 0.16, 0.17
    k.cyl(0.05, 0.02, at=(nx, ny, 0.32), rot=(0, 0, 0), m=brass)
    d = (-0.145, -0.822, 0.55)
    p = (0.15, 0.12, 0.62)
    k.tube([(nx, ny, 0.31), (nx, ny, 0.48), (0.158, 0.168, 0.55),
            (p[0] - 0.06 * d[0], p[1] - 0.06 * d[1], p[2] - 0.06 * d[2]), p], 0.032, brass, curved=True)

    # Flared horn, opening forward and up over the record (axis along d)
    L, n = 0.5, 24
    prof = [(0.034 + 0.226 * (i / n) ** 3, L * i / n) for i in range(n + 1)]
    prof += [(0.245, L - 0.01), (0.18, L - 0.05), (0.09, L - 0.12), (0.0, L - 0.16)]
    k.lathe(prof, at=p, rot=(56.6, 0, -10), m=brass)

    # Tone arm from the neck base to the soundbox resting on the record
    k.tube([(nx, ny, 0.40), (0.11, 0.02, 0.405), (0.05, -0.09, 0.39)], 0.022, brass, curved=True)
    k.cyl(0.048, 0.03, at=(0.04, -0.10, 0.39), rot=(90, 0, 30), m=brass)
    k.cyl(0.006, 0.05, at=(0.04, -0.10, 0.355), rot=(0, 0, 0), m=k.mat("#8b8f96", "metal"))

    # Crank on the right side: shaft through the cabinet wall, arm, wooden knob
    k.cyl(0.022, 0.07, at=(0.285, 0.0, 0.17), rot=(0, 90, 0), m=brass)
    k.tube([(0.31, 0.0, 0.17), (0.31, -0.05, 0.10), (0.31, -0.06, 0.08)], 0.02, brass)
    k.cyl(0.024, 0.07, at=(0.345, -0.06, 0.08), rot=(0, 90, 0), m=wood)

    # Polished wooden desk
    k.box((6, 4, 0.1), at=(0, 0.8, -0.05), m=k.mat("#c47a3c", "gloss"), bevel=0.01, setting=True)
