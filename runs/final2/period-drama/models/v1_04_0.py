# Open parasol: a domed violet canopy of eight panels sags a little between eight ribs that run from the top
# hub to the rim; a white ruffled lace skirt hangs from the canopy rim. A wooden shaft passes through the canopy
# with a ball finial on top and a small runner hub under it, and ends below in a curved crook handle.
# It floats, tilted to the right and toward the camera so the dome's top shows, like the beach umbrella card.
import math

SCENE = {"category": "1", "backdrop": "#ffc928", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}

R, Z0, H = 0.45, 0.75, 0.2              # canopy rim radius, rim height, dome height
S = (R * R + H * H) / (2 * H)           # sphere radius of the dome
ZC = Z0 + H - S                         # sphere center height
RIBS = 8


def dome_z(rho):
    return ZC + math.sqrt(max(S * S - rho * rho, 0.0))


def sag(theta):
    # 0 on a rib, 1 in the middle of a panel
    return math.sin(RIBS / 2 * theta) ** 2


def build(k):
    canopy = k.mat("#7a2cc4", "matte")
    rib_m = k.mat("#5a1d99", "matte")
    lace = k.mat("#fbf8f2", "matte")
    wood = k.mat("#9a5f2e", "matte")
    tip_m = k.mat("#f2ead8", "satin")

    def panel_warp(p):
        x, y, z = p
        rho = math.hypot(x, y)
        if rho < 1e-6:
            return p
        th = math.atan2(y, x)
        t = (rho / R) ** 2 * sag(th)
        s = 1 - 0.04 * t
        return (x * s, y * s, z - 0.035 * t)

    # canopy shell: underside from the center out to the rim, then the top surface back to the apex
    prof = []
    for i in range(13):
        rho = 0.02 + (R - 0.02) * i / 12
        prof.append((rho, dome_z(rho) - 0.05 - 0.01 * (1 - rho / R)))
    prof.append((R + 0.005, Z0 - 0.005))
    for i in range(16, -1, -1):
        rho = R * i / 16
        prof.append((rho, dome_z(rho)))
    k.warp(k.lathe(prof, at=(0, 0, 0), rot=(0, 0, 0), m=canopy, verts=128), panel_warp)

    # ribs on the top of the dome, from the hub to the rim tips, each with a small cap
    for i in range(RIBS):
        th = i * 2 * math.pi / RIBS
        pts = []
        for j in range(10):
            rho = 0.03 + (R - 0.025) * j / 9
            pts.append((rho * math.cos(th), rho * math.sin(th), dome_z(rho) + 0.006))
        k.tube(pts, 0.014, rib_m, curved=True)
        k.sphere(0.02, at=(R * math.cos(th), R * math.sin(th), Z0 + 0.002), m=tip_m)

    # lace: a ruffled skirt hanging from the rim, plus a beaded trim along the seam
    skirt = [(R - 0.005, Z0 + 0.004), (R + 0.02, Z0 - 0.03), (R + 0.045, Z0 - 0.065), (R + 0.06, Z0 - 0.085),
             (R + 0.055, Z0 - 0.09)]

    def ruffle(p):
        x, y, z = p
        rho = math.hypot(x, y)
        th = math.atan2(y, x)
        depth = (Z0 + 0.004 - z) / 0.094
        rho2 = rho + 0.014 * depth * math.sin(48 * th)
        dz = -0.035 * sag(th) + 0.01 * depth * math.cos(48 * th)
        s = (1 - 0.04 * sag(th)) * rho2 / rho
        return (x * s, y * s, z + dz)

    k.warp(k.lathe(skirt, at=(0, 0, 0), rot=(0, 0, 0), m=lace, verts=192), ruffle)
    trim = []
    for i in range(97):
        th = i * 2 * math.pi / 96
        rr = (R + 0.004) * (1 - 0.04 * sag(th))
        trim.append((rr * math.cos(th), rr * math.sin(th), Z0 - 0.002 - 0.035 * sag(th)))
    k.tube(trim, 0.014, lace, curved=True)

    # shaft through the canopy, finial on top, runner hub under the dome
    k.cyl(0.02, 1.0, at=(0, 0, 0.5), rot=(0, 0, 0), m=wood)
    k.sphere(0.04, at=(0, 0, dome_z(0) + 0.06), m=wood)
    k.cyl(0.025, 0.05, at=(0, 0, dome_z(0) + 0.02), rot=(0, 0, 0), m=wood)
    k.cone(0.02, 0.06, 0.07, at=(0, 0, dome_z(0) - 0.09), rot=(0, 0, 0), m=wood)

    # curved crook handle at the bottom
    c, rc = (0.075, 0.0, 0.0), 0.075
    crook = [(0, 0, 0.06), (0, 0, 0.02)]
    for j in range(13):
        a = math.pi - math.pi * j / 12
        crook.append((c[0] + rc * math.cos(a), 0, c[2] - rc * math.sin(a)))
    crook.append((0.15, 0, 0.03))
    k.tube(crook, 0.026, wood, curved=True)
    k.sphere(0.03, at=(0.15, 0, 0.035), m=wood)

    k.turn(22, 22, 0)
