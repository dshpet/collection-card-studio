# Open parasol: a round domed canopy of eight gently scalloped panels sits on a long wooden shaft with a round
# finial on top. Eight thin ribs run under the canopy to its rim, and eight stretchers hold them up from a runner
# collar on the shaft. A soft pink ruffle hangs all round the rim. The shaft ends in a curved wooden crook handle.
# It floats, tipped sideways and a little back so the dome, the underside ribs and the whole shaft and handle show.
import math

SCENE = {"category": "1", "backdrop": "#2fc4ef", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}

RIM_R, RIM_Z, TOP_Z, PANELS = 0.46, 0.70, 0.92, 8


def dip(x, y, r):
    # Scallop: each panel sags slightly between ribs toward the rim.
    a = math.atan2(y, x)
    return 0.02 * (min(r, RIM_R) / RIM_R) ** 2 * (1 - math.cos(PANELS * a)) / 2


def build(k):
    canvas = k.mat("#fbefa0", "matte")
    lace = k.mat("#f59ac0", "matte")
    wood = k.mat("#8a5530", "satin")
    rib = k.mat("#d9d4c8", "metal")

    # Canopy: shallow concave underside, smooth domed top.
    prof = [(0.0, 0.79), (0.10, 0.786), (0.20, 0.772), (0.30, 0.752), (0.38, 0.732), (0.43, 0.716), (RIM_R, RIM_Z)]
    for i in range(1, 41):
        t = i / 40
        prof.append((RIM_R * math.cos(t * math.pi / 2) ** 0.9, RIM_Z + (TOP_Z - RIM_Z) * math.sin(t * math.pi / 2)))
    prof[-1] = (0.0, TOP_Z)
    canopy = k.lathe(prof, at=(0, 0, 0), rot=(0, 0, 0), m=canvas, verts=192)
    k.warp(canopy, lambda p: (p[0], p[1], p[2] - dip(p[0], p[1], math.hypot(p[0], p[1]))))

    # Ruffle: a thin band hanging out and down from the rim, in soft rounded folds.
    band = [(RIM_R - 0.012, RIM_Z + 0.012), (RIM_R + 0.02, RIM_Z - 0.03), (RIM_R + 0.045, RIM_Z - 0.07),
            (RIM_R + 0.055, RIM_Z - 0.065), (RIM_R + 0.03, RIM_Z - 0.025), (RIM_R + 0.004, RIM_Z + 0.016)]
    ruffle = k.lathe(band, at=(0, 0, 0), rot=(0, 0, 0), m=lace, verts=576)

    def wave(p):
        x, y, z = p
        r = math.hypot(x, y)
        a = math.atan2(y, x)
        depth = max(0.0, (r - RIM_R + 0.012) / 0.065)
        s = 1 + (0.016 * math.sin(24 * a) * depth) / max(r, 1e-6)
        return (x * s, y * s, z - dip(x, y, RIM_R))
    k.warp(ruffle, wave)

    # Shaft, finial, runner collar.
    k.cyl(0.024, 0.93, at=(0, 0, 0.505), rot=(0, 0, 0), m=wood)
    k.sphere(0.04, at=(0, 0, TOP_Z + 0.03), m=wood)
    k.cyl(0.04, 0.06, at=(0, 0, 0.52), rot=(0, 0, 0), m=wood, bevel=0.01)

    # Ribs under the canopy and stretchers from the runner.
    for i in range(PANELS):
        a = 2 * math.pi * i / PANELS
        c, s = math.cos(a), math.sin(a)
        pts = [(RIM_R * f * c, RIM_R * f * s, z) for f, z in ((0.05, 0.786), (0.33, 0.766), (0.66, 0.736), (0.98, 0.70))]
        k.tube(pts, 0.012, rib, curved=True)
        k.sphere(0.018, at=(RIM_R * c, RIM_R * s, RIM_Z - 0.005), m=rib)
        k.tube([(0.035 * c, 0.035 * s, 0.53), (0.25 * c, 0.25 * s, 0.758)], 0.011, rib)

    # Curved crook handle at the bottom of the shaft.
    cx, cz, rr = 0.075, 0.06, 0.075
    crook = [(0, 0, 0.13)]
    for j in range(13):
        t = math.pi + j * math.pi / 12
        crook.append((cx + rr * math.cos(t), 0, cz + rr * math.sin(t)))
    crook.append((cx + rr, 0, cz + 0.035))
    k.tube(crook, 0.03, wood, curved=True)
    k.sphere(0.031, at=(cx + rr, 0, cz + 0.035), m=wood)

    # Tip sideways and slightly back: the dome, the ribs underneath and the full shaft and handle all show.
    k.turn(-8, -18, 0)
