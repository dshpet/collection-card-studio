# Wooden barrel standing on packed dirt: a bulging stave body with a flat lid set inside the top chime, three
# dark iron hoops (two near the ends, one at the lower quarter) and a raised house pictogram (walls, filled
# gable under a pitched roof, chimney, door) on the front between the lower-quarter hoop and the top hoop. The
# dirt is a wide slab whose back edge sits behind the barrel, with the sky-blue backdrop above it.
import math

SCENE = {"category": "3", "backdrop": "#5ab8ef", "azimuth": 30, "elevation": 15, "lens": 60, "light": "left"}

H = 1.0


def rad(z):
    return 0.30 + 0.06 * math.sin(math.pi * z / H)


def build(k):
    wood = k.mat("#9a5f30", "matte")
    lid_wood = k.mat("#a86c3a", "matte")
    iron = k.mat("#4a4d52", "metal")

    # Body: staves bulge out, the top chime rises a little above the inset flat lid.
    prof = [(0.0, 0.0)]
    for i in range(41):
        z = H * i / 40
        prof.append((rad(z), z))
    prof += [(0.272, H), (0.272, H - 0.03), (0.0, H - 0.03)]
    body = k.lathe(prof, at=(0, 0, 0), rot=(0, 0, 0), m=wood, verts=128)

    staves = 16

    def grooves(p):
        x, y, z = p
        r = math.hypot(x, y)
        if r < 0.285 or z < 0.005 or z > H - 0.005:
            return p
        a = math.atan2(y, x)
        g = abs(math.cos(staves * a / 2)) ** 30
        s = 1 - 0.022 * g
        return (x * s, y * s, z)

    k.warp(body, grooves)

    # Flat lid boards sitting in the chime.
    k.cyl(0.272, 0.02, at=(0, 0, H - 0.02), rot=(0, 0, 0), m=lid_wood, bevel=0.004)

    # Three iron hoops.
    for zc in (0.09, 0.32, 0.91):
        r = max(rad(zc - 0.03), rad(zc + 0.03)) + 0.013
        k.cyl(r, 0.06, at=(0, 0, zc), rot=(0, 0, 0), m=iron, bevel=0.006)

    # Raised house pictogram on the front (-y), between the 0.32 and 0.91 hoops.
    zc = 0.53
    yf = -rad(zc)
    wall_top = zc + 0.065
    # Walls.
    k.box((0.17, 0.04, 0.13), at=(0, yf + 0.004, zc), rot=(0, 0, 0), m=wood, bevel=0.006)
    # Gable: a square turned 45 degrees, its lower half sunk in the wall, its upper half the filled triangle.
    k.box((0.12, 0.04, 0.12), at=(0, yf + 0.004, wall_top), rot=(0, 45, 0), m=wood, bevel=0.005)
    # Pitched roof: two boards, eaves overhanging the wall corners, meeting at the ridge above the gable peak.
    slope = 45
    half = 0.075
    for side in (-1, 1):
        cx = side * half * math.cos(math.radians(slope)) / 1.0 * 0.95
        cz = wall_top + 0.085 - half * math.sin(math.radians(slope)) * 0.95
        k.box((0.15, 0.042, 0.026), at=(cx, yf - 0.002, cz), rot=(0, side * slope, 0), m=lid_wood, bevel=0.006)
    # Chimney standing on the right roof slope.
    k.box((0.03, 0.04, 0.07), at=(0.06, yf + 0.002, wall_top + 0.07), rot=(0, 0, 0), m=wood, bevel=0.005)
    # Door at the bottom of the wall.
    k.box((0.045, 0.02, 0.075), at=(0, yf - 0.022, zc - 0.025), rot=(0, 0, 0), m=lid_wood, bevel=0.005)

    k.turn(0, 0, 15)

    # Packed dirt slab; front runs off the card, back edge behind the barrel.
    k.box((7, 2.6, 0.2), at=(0, -0.3, -0.1), rot=(0, 0, 0), m=k.mat("#8a6440", "matte"), bevel=0.02,
          setting=True)
