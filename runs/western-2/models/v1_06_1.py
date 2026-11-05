# Leather saddle straddling a wooden plank fence rail. The red blanket drapes over the rail with a rounded
# shoulder; the leather skirt drapes over the blanket the same way, a little shorter so the red edge shows. The
# seat block sits on the skirt, dished, with a low cantle at the back and the pommel swelling at the front under
# the horn (neck + cap). A fender hangs on each side under the seat edge; a short stirrup leather runs from its
# foot to a bolt that carries the silver stirrup. A loose cinch strap hangs from a rigging ring on the near side
# and ends free in a buckle. The rail is nailed to posts far off the card, so it runs off both sides.
import math

SCENE = {"category": "3", "backdrop": "#3cc8f0", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def drape(w, r, base, a, L, n):
    # Unit disk -> rounded rectangle (superellipse n), then wrapped over the rail: flat top of half-width w,
    # a rounded shoulder of radius r, then a straight hang. The local z is the thickness along the normal.
    def fn(p):
        x, y, z = p
        rho = math.hypot(x, y)
        if rho > 1e-9:
            c, s = abs(x) / rho, abs(y) / rho
            f = 1.0 / (c ** n + s ** n) ** (1.0 / n)
            x, y = x * f, y * f
        sarc = y * L
        d = abs(sarc) - w
        sg = 1 if sarc >= 0 else -1
        if d <= 0:
            py, pz, ny, nz = sarc, 0.0, 0.0, 1.0
        elif d < r * math.pi / 2:
            phi = d / r
            py, pz = sg * (w + r * math.sin(phi)), -(r - r * math.cos(phi))
            ny, nz = sg * math.sin(phi), math.cos(phi)
        else:
            py, pz = sg * (w + r), -r - (d - r * math.pi / 2)
            ny, nz = float(sg), 0.0
        return (a * x, py + z * ny, base + pz + z * nz)
    return fn


def disk(t, steps=24):
    return [(i / steps, 0.0) for i in range(steps + 1)] + [(1 - i / steps, t) for i in range(steps + 1)]


def build(k):
    seat_m = k.mat("#7a4524", "matte")
    skirt_m = k.mat("#9a5a2e", "matte")
    fender_m = k.mat("#8a4f28", "matte")
    horn_m = k.mat("#6a3a1e", "matte")
    blanket = k.mat("#d8322f", "matte")
    silver = k.mat("#cfd4da", "metal")
    wood = k.mat("#b9773e", "matte")

    # Fence: a plank rail with its top at z = 0, nailed to posts far off the card.
    k.box((6, 0.24, 0.12), at=(0, 0, -0.06), m=wood, bevel=0.012, setting=True)
    for x in (-1.5, 1.5):
        k.box((0.18, 0.18, 3), at=(x, 0.21, -1.5), m=wood, bevel=0.015, setting=True)

    # Blanket draped over the rail; the skirt drapes over it, shorter, so the red edge shows.
    k.warp(k.lathe(disk(0.03), at=(0, 0, 0), rot=(0, 0, 0), m=blanket, verts=96),
           drape(0.08, 0.04, 0.0, 0.5, 0.44, 8))
    k.warp(k.lathe(disk(0.035), at=(0, 0, 0), rot=(0, 0, 0), m=skirt_m, verts=96),
           drape(0.08, 0.07, 0.03, 0.44, 0.40, 3))

    # Seat: a dense disk warped into a solid block, dished, with a low cantle rising at the back (-x).
    n = 20
    profile = [(i / n, 0.0) for i in range(n + 1)] + [(1 - i / n, 0.06) for i in range(n + 1)]

    def seat_shape(p):
        x, y, z = p
        h = 0.04 + 0.04 * x * x + 0.12 * max(0.0, -x) ** 4 - 0.04 * y * y
        return (0.36 * x, 0.16 * y, z + (h if z > 0.03 else 0.0))

    k.warp(k.lathe(profile, at=(-0.03, 0, 0.065), rot=(0, 0, 0), m=seat_m), seat_shape)

    # Pommel swell and horn at the front (+x).
    k.blob([(0.30, 0, 0.12, 0.1, (0.9, 1.5, 1.0))], skirt_m)
    k.cyl(0.035, 0.16, at=(0.32, 0, 0.26), rot=(0, 0, 0), m=horn_m, bevel=0.008)
    k.cyl(0.075, 0.035, at=(0.32, 0, 0.355), rot=(0, 0, 0), m=horn_m, bevel=0.012)

    # Fenders under the seat edge, stirrup leathers and stirrups on both sides.
    fx = -0.02
    for s in (-1, 1):
        y = s * 0.205
        k.box((0.22, 0.03, 0.37), at=(fx, y, -0.165), m=fender_m, bevel=0.03)
        k.box((0.06, 0.02, 0.09), at=(fx, y, -0.385), m=fender_m, bevel=0.005)
        k.cyl(0.014, 0.05, at=(fx, y, -0.425), rot=(90, 0, 0), m=silver)
        arch = [(-0.075, -0.57), (-0.07, -0.50), (-0.04, -0.445), (0, -0.425),
                (0.04, -0.445), (0.07, -0.50), (0.075, -0.57)]
        k.tube([(fx + ax, y, az) for ax, az in arch], 0.015, silver, curved=True)
        k.box((0.17, 0.08, 0.025), at=(fx, y, -0.575), m=silver, bevel=0.008)

    # Loose cinch strap on the near side: rigging ring on the skirt, strap hanging, buckle at the free end.
    sx, sy = 0.27, -0.2
    k.torus(0.035, 0.009, at=(sx, sy, -0.03), rot=(90, 0, 0), m=silver)
    k.box((0.055, 0.014, 0.38), at=(sx, sy, -0.24), m=fender_m, bevel=0.004)
    k.torus(0.033, 0.009, at=(sx, sy - 0.01, -0.44), rot=(90, 0, 0), m=silver)
