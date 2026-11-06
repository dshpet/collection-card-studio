# Moon base: a white dome on a short drum wall sits on the moon's surface. A small round orange door with a
# grey frame is set in the dome's front, with a step below it. A short grey tunnel leaves the dome's right side
# on its side, resting on the ground, ribbed with rings and closed by a round end cap. The ground is a mid grey
# with a few shallow raised-rim craters and low hills far back under an orange sky.
import math

SCENE = {"category": "4", "backdrop": "#ff9a3c", "azimuth": 30, "elevation": 12, "lens": 55, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    grey = k.mat("#6c727b", "satin")
    dark = k.mat("#454a52", "satin")
    orange = k.mat("#f2620f", "satin")

    # Dome: drum wall 0.06 tall, then a hemisphere of radius 0.42.
    R, wall = 0.42, 0.06
    profile = [(R, 0.0), (R, wall)]
    n = 64
    for i in range(1, n + 1):
        a = math.radians(i * 90 / n)
        profile.append((R * math.cos(a), wall + R * math.sin(a)))
    profile[-1] = (0.0, wall + R)
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=white, verts=128)
    k.cyl(R + 0.02, 0.04, at=(0, 0, 0.02), rot=(0, 0, 0), m=grey, bevel=0.008)  # base ring

    # Small door on the front (-y), tilted to follow the dome surface, set proud of it.
    dz = 0.17
    tilt = math.degrees(math.asin((dz - wall) / R))
    dist = math.sqrt(R * R - (dz - wall) ** 2)
    ny, nz = -math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    rx = 90 - tilt
    out = 0.022
    k.torus(0.1, 0.02, at=(0, ny * (dist + out), dz + nz * out), rot=(rx, 0, 0), m=grey)
    k.cyl(0.09, 0.06, at=(0, ny * (dist + 0.005), dz + nz * 0.005), rot=(rx, 0, 0), m=orange, bevel=0.008)
    k.sphere(0.014, at=(0.05, ny * (dist + 0.042), dz + nz * 0.042), m=grey)  # handle
    k.box((0.18, 0.1, 0.05), at=(0, -0.47, 0.025), m=grey, bevel=0.01)  # step

    # Tunnel on the right (+x), lying on the ground, its inner end inside the dome.
    tr, x0, x1 = 0.13, 0.3, 0.8
    k.cyl(tr, x1 - x0, at=((x0 + x1) / 2, 0, tr), rot=(0, 90, 0), m=grey, bevel=0.01)
    for x in (0.42, 0.6, 0.78):
        k.torus(tr, 0.018, at=(x, 0, tr), rot=(0, 90, 0), m=dark)
    k.cyl(tr + 0.015, 0.04, at=(x1 + 0.01, 0, tr), rot=(0, 90, 0), m=dark, bevel=0.01)  # end cap
    k.box((0.42, 0.18, 0.02), at=((x0 + x1) / 2 + 0.03, 0, 0.01), m=dark, bevel=0.005)  # footing

    # Moon surface: mid-grey ground, shallow raised-rim craters, low hills far back.
    ground = "#8a8d95"
    rock = k.mat("#7a7d86", "matte")
    hill = k.mat("#6e7179", "matte")
    k.floor(ground, "matte", size=40, z=0)
    crater = [(0.0, 0.003), (0.17, 0.003), (0.21, 0.01), (0.25, 0.028), (0.28, 0.026), (0.32, 0.01),
              (0.37, 0.0)]
    for cx, cy, s in ((-0.85, -0.35, 1.0), (1.05, -0.55, 0.7), (-0.3, -1.0, 0.6), (0.6, 0.9, 1.4),
                      (-1.6, 1.2, 1.8)):
        k.lathe([(r * s, z * s) for r, z in crater], at=(cx, cy, 0), rot=(0, 0, 0), m=rock, setting=True)
    k.blob([(-3.5, 6, 0, 1.6, (1.8, 1, 0.35)), (-1.5, 6.5, 0, 1.3, (1.6, 1, 0.3))], hill, setting=True)
    k.blob([(3.2, 7, 0, 1.8, (1.7, 1, 0.3))], hill, setting=True)
