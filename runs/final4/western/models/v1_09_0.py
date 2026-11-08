# Farm wind pump: four straight wooden legs lean in from the wheat to a small top deck, tied by girts and crossed
# braces on every face. A turntable on the deck carries the gearbox; the axle runs forward to a hub, two rings and
# spokes hold eighteen pitched blades, and a boom runs back from the gearbox to the tail vane. The wheat stands as
# a golden bed of ears that hides the tower's feet; the whole tower is framed, the field runs off the card.
import math

SCENE = {"category": "4", "backdrop": "#5cc4f5", "azimuth": 30, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#8e3b22", "matte")
    brace = k.mat("#7a3220", "matte")
    white = k.mat("#f7f7f2", "satin")
    steel = k.mat("#5d6168", "metal")
    gold = k.mat("#f2b62a", "satin")

    # Tower: legs from the ground (buried a little) up to the deck, leaning in.
    z0, z1, w0, w1 = -0.05, 1.15, 0.30, 0.08

    def w(z):
        return w0 + (w1 - w0) * (z - z0) / (z1 - z0)

    corners = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    for sx, sy in corners:
        k.tube([(sx * w0, sy * w0, z0), (sx * w1, sy * w1, z1)], 0.032, wood)

    levels = (0.3, 0.68, 1.0)
    for z in levels:
        h = w(z)
        for i in range(4):
            ax, ay = corners[i]
            bx, by = corners[(i + 1) % 4]
            k.tube([(ax * h, ay * h, z), (bx * h, by * h, z)], 0.022, wood)
    # Crossed braces between the girt levels on each face.
    spans = ((0.02, levels[0]), (levels[0], levels[1]), (levels[1], levels[2]))
    for za, zb in spans:
        ha, hb = w(za), w(zb)
        for i in range(4):
            ax, ay = corners[i]
            bx, by = corners[(i + 1) % 4]
            k.tube([(ax * ha, ay * ha, za), (bx * hb, by * hb, zb)], 0.018, brace)
            k.tube([(bx * ha, by * ha, za), (ax * hb, ay * hb, zb)], 0.018, brace)

    # Deck, turntable and gearbox.
    k.box((0.24, 0.24, 0.04), at=(0, 0, z1 + 0.02), m=wood, bevel=0.008)
    k.cyl(0.08, 0.04, at=(0, 0, z1 + 0.06), rot=(0, 0, 0), m=steel)
    hub_z = 1.30
    k.box((0.13, 0.22, 0.12), at=(0, 0.0, hub_z - 0.01), m=steel, bevel=0.02)
    k.cyl(0.025, 0.24, at=(0, -0.2, hub_z), rot=(90, 0, 0), m=steel)

    # Wheel in front of the tower, facing -y.
    wy = -0.3
    k.cyl(0.075, 0.09, at=(0, wy, hub_z), rot=(90, 0, 0), m=white, bevel=0.015)
    k.sphere(0.05, at=(0, wy - 0.05, hub_z), scale=(1, 0.8, 1), m=white)
    k.torus(0.2, 0.02, at=(0, wy, hub_z), rot=(90, 0, 0), m=white)
    k.torus(0.45, 0.022, at=(0, wy, hub_z), rot=(90, 0, 0), m=white)
    for i in range(6):
        a = math.radians(i * 60 + 15)
        k.tube([(0.07 * math.sin(a), wy, hub_z + 0.07 * math.cos(a)),
                (0.45 * math.sin(a), wy, hub_z + 0.45 * math.cos(a))], 0.016, white)

    n, pitch = 18, math.radians(28)
    for i in range(n):
        a = 2 * math.pi * i / n
        blade = k.box((0.085, 0.014, 0.29), at=(0, 0, 0), rot=(0, 0, 0), m=white, bevel=0.004)

        def place(p, a=a):
            x, y, z = p
            # Pitch about the blade's radial axis, push out to radius, spin about the axle.
            x, y = x * math.cos(pitch) - y * math.sin(pitch), x * math.sin(pitch) + y * math.cos(pitch)
            z += 0.33
            return (x * math.cos(a) + z * math.sin(a), y + wy, -x * math.sin(a) + z * math.cos(a) + hub_z)

        k.warp(blade, place)

    # Tail: boom back from the gearbox with a strut, vane at its end.
    k.tube([(0, 0.08, hub_z + 0.01), (0, 0.62, hub_z + 0.05)], 0.022, steel)
    k.tube([(0, 0.04, hub_z + 0.06), (0, 0.4, hub_z + 0.04)], 0.016, steel)
    vane = k.box((0.016, 0.34, 0.26), at=(0, 0, 0), m=gold, bevel=0.006)

    def taper(p):
        x, y, z = p
        s = 0.65 if y < 0 else 1.0  # narrower toward the boom
        return (x, y + 0.72, z * s + hub_z + 0.05)

    k.warp(vane, taper)

    # Wheat field: a golden bed with rows of ripe ears standing above it.
    k.floor("#c98f22")
    k.box((6, 6, 0.18), at=(0, 0, 0.09), m=k.mat("#d9a32e", "matte"), bevel=0.02, setting=True)
    ear = k.mat("#eec04a", "matte")
    step = 0.11
    for ix in range(-16, 17):
        for iy in range(-10, 16):
            jx = math.sin(ix * 12.9898 + iy * 78.233) * 0.035
            jy = math.sin(ix * 39.346 + iy * 11.135) * 0.035
            x, y = ix * step + jx, iy * step + jy
            hz = 0.22 + 0.04 * math.sin(ix * 4.1 + iy * 2.7)
            tilt = 12 * math.sin(ix * 1.7 + iy * 3.3)
            k.sphere(0.032, at=(x, y, hz), scale=(1, 1, 2.3), rot=(tilt, tilt * 0.6, 0), m=ear, setting=True)
