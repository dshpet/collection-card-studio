# Wooden hourglass: a round turned base and an identical top are joined by three turned posts. Between them
# stands one glass body of two round bulbs meeting at a narrow neck, its ends seated in wooden collars on the
# base and under the top. Tan sand fills the bottom of the lower bulb with a small mound in the middle.
import math

SCENE = {"category": "2", "backdrop": "#239b4a", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}

BASE_TOP = 0.08   # top face of the base disc
TOP_LOW = 0.92    # underside of the top disc
NECK_Z = 0.5


def glass_radius(z):
    # lower half; the upper half mirrors it about the neck
    if z > NECK_Z:
        z = 2 * NECK_Z - z
    u = (z - BASE_TOP) / (NECK_Z - BASE_TOP)
    return 0.085 * (1 - u) + 0.028 * u + 0.115 * math.sin(math.pi * min(u * 1.08, 1.0)) ** 1.3


def build(k):
    wood = k.mat("#8a4f24", "satin")
    dark = k.mat("#6e3c1a", "satin")
    glass = k.mat("#e6f6ff", "glass")
    sand = k.mat("#d9b26a", "matte")

    # base and top: thick discs with rounded rims
    disc = [(0, 0), (0.29, 0), (0.305, 0.012), (0.31, 0.03), (0.305, 0.048), (0.29, 0.06),
            (0.27, 0.065), (0.26, 0.08), (0, 0.08)]
    k.lathe(disc, at=(0, 0, 0), m=wood)
    k.lathe(disc, at=(0, 0, 1.0), rot=(180, 0, 0), m=wood)

    # collars that hold the glass ends
    k.cyl(0.11, 0.03, at=(0, 0, BASE_TOP + 0.015), m=dark)
    k.cyl(0.11, 0.03, at=(0, 0, TOP_LOW - 0.015), m=dark)

    # three turned posts
    h = TOP_LOW - BASE_TOP
    post = [(0, 0), (0.034, 0), (0.034, 0.04), (0.024, 0.06), (0.022, 0.2), (0.03, 0.25), (0.022, 0.3),
            (0.02, h / 2), (0.022, h - 0.3), (0.03, h - 0.25), (0.022, h - 0.2), (0.024, h - 0.06),
            (0.034, h - 0.04), (0.034, h), (0, h)]
    for i in range(3):
        a = math.radians(90 + i * 120)
        k.lathe(post, at=(0.235 * math.cos(a), 0.235 * math.sin(a), BASE_TOP), m=wood, verts=32)

    # glass body: two bulbs joined at the neck, ends closed against the collars
    n = 60
    zs = [BASE_TOP + 0.03 + (TOP_LOW - 0.03 - BASE_TOP - 0.03) * i / n for i in range(n + 1)]
    profile = [(0, zs[0])] + [(glass_radius(z), z) for z in zs] + [(0, zs[-1])]
    k.lathe(profile, at=(0, 0, 0), m=glass)

    # sand in the lower bulb, a little inside the glass, with a soft mound on top
    level = 0.27
    sz = [BASE_TOP + 0.032 + (level - BASE_TOP - 0.032) * i / 20 for i in range(21)]
    rim = glass_radius(level) - 0.012
    sand_profile = [(0, sz[0])] + [(glass_radius(z) - 0.012, z) for z in sz]
    for j in range(1, 9):
        r = rim * (1 - j / 8)
        sand_profile.append((r, level + 0.05 * (1 - (r / rim) ** 2) ** 1.5))
    k.lathe(sand_profile, at=(0, 0, 0), m=sand)

    # plain floor, a shade lighter than the backdrop
    k.box((6, 6, 0.1), at=(0, 1.5, -0.05), m=k.mat("#43b866", "matte"), bevel=0, setting=True)
