# Moon base: a white dome on a short drum wall sits on the moon's surface. A small round orange door with a
# grey frame is set in the dome's front, with a step below it. A short grey tunnel leaves the dome's right side
# on its side, resting on the ground, ribbed with rings and closed by a round end cap. The ground is grey with a
# few shallow craters and low hills far back under an orange sky.
import math

SCENE = {"category": "4", "backdrop": "#ff9a3c", "azimuth": 30, "elevation": 12, "lens": 55, "light": "left"}


def build(k):
    white = k.mat("#f4f5f7", "satin")
    grey = k.mat("#9aa0a8", "satin")
    dark = k.mat("#6d737c", "satin")
    orange = k.mat("#ff7a1a", "satin")

    # Dome: drum wall 0.06 tall, then a hemisphere of radius 0.42.
    R, wall = 0.42, 0.06
    profile = [(R, 0.0), (R, wall)]
    for i in range(1, 25):
        a = math.radians(i * 90 / 24)
        profile.append((R * math.cos(a), wall + R * math.sin(a)))
    profile[-1] = (0.0, wall + R)
    k.lathe(profile, at=(0, 0, 0), rot=(0, 0, 0), m=white)
    k.cyl(R + 0.02, 0.04, at=(0, 0, 0.02), rot=(0, 0, 0), m=grey, bevel=0.008)  # base ring

    # Door on the front (-y), tilted to follow the dome surface.
    dz = 0.19
    tilt = math.degrees(math.asin((dz - wall) / R))
    dist = math.sqrt(R * R - (dz - wall) ** 2)
    ny, nz = -math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    rx = 90 - tilt
    k.torus(0.12, 0.022, at=(0, ny * (dist + 0.005), dz + nz * 0.005), rot=(rx, 0, 0), m=grey)
    k.cyl(0.11, 0.03, at=(0, ny * dist, dz), rot=(rx, 0, 0), m=orange, bevel=0.006)
    k.sphere(0.015, at=(0.06, ny * (dist + 0.02), dz + nz * 0.02), m=grey)  # handle
    k.box((0.2, 0.1, 0.05), at=(0, -0.47, 0.025), m=grey, bevel=0.01)  # step

    # Tunnel on the right (+x), lying on the ground.
    tr, x0, x1 = 0.13, 0.3, 0.8
    k.cyl(tr, x1 - x0, at=((x0 + x1) / 2, 0, tr), rot=(0, 90, 0), m=grey, bevel=0.01)
    for x in (0.42, 0.6, 0.78):
        k.torus(tr, 0.018, at=(x, 0, tr), rot=(0, 90, 0), m=dark)
    k.cyl(tr + 0.015, 0.04, at=(x1 + 0.01, 0, tr), rot=(0, 90, 0), m=dark, bevel=0.01)  # end cap
    k.box((0.42, 0.18, 0.02), at=((x0 + x1) / 2 + 0.03, 0, 0.01), m=dark, bevel=0.005)  # footing

    # Moon surface: grey ground, shallow craters, low hills far back.
    rock = k.mat("#a3a3a8", "matte")
    k.floor("#a3a3a8", "matte", size=40, z=0)
    crater = [(0.0, -0.02), (0.16, -0.02), (0.21, 0.0), (0.25, 0.025), (0.3, 0.01), (0.34, 0.0)]
    for cx, cy, s in ((-0.85, -0.35, 1.0), (1.05, -0.55, 0.7), (-0.3, -1.0, 0.6), (0.6, 0.9, 1.4),
                      (-1.6, 1.2, 1.8)):
        k.lathe([(r * s, z * s) for r, z in crater], at=(cx, cy, 0), rot=(0, 0, 0), m=rock, setting=True)
    k.blob([(-3.5, 6, 0, 1.6, (1.8, 1, 0.35)), (-1.5, 6.5, 0, 1.3, (1.6, 1, 0.3))], rock, setting=True)
    k.blob([(3.2, 7, 0, 1.8, (1.7, 1, 0.3))], rock, setting=True)
