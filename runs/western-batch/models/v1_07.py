# Covered wagon: a plank box rides on two axles through bolsters; four spoked wheels turn on the axle ends, the
# rear pair bigger. The canvas cover is one arched shell over the box, flared at both ends with a recessed
# opening. The tongue runs forward from the front axle and rests its tip on the trail. The wagon stands on a dirt
# trail across dry prairie, with low hills far back. The front faces +x, so the three-quarter view shows the side
# and the front opening.
import math

SCENE = {"category": "4", "backdrop": "#4fb8f2", "azimuth": 30, "elevation": 11, "lens": 55, "light": "left"}


def wheel(k, x, y, r, rim_m, hub_m):
    k.torus(r - 0.022, 0.024, at=(x, y, r), rot=(90, 0, 0), m=rim_m)
    k.cyl(0.05, 0.09, at=(x, y, r), rot=(90, 0, 0), m=hub_m, bevel=0.008)
    for i in range(12):
        a = math.radians(i * 30)
        tip = (x + (r - 0.03) * math.cos(a), y, r + (r - 0.03) * math.sin(a))
        k.tube([(x + 0.04 * math.cos(a), y, r + 0.04 * math.sin(a)), tip], 0.014, rim_m)


def build(k):
    wood = k.mat("#8a5530", "matte")
    dark = k.mat("#5e3a20", "matte")
    red = k.mat("#d23a2c", "satin")
    canvas = k.mat("#f4f1e8", "matte")
    iron = k.mat("#4a4a4f", "metal")

    # Box: plank bed with a darker top rail and bottom sill.
    k.box((1.0, 0.42, 0.22), at=(0, 0, 0.45), m=wood, bevel=0.012)
    k.box((1.02, 0.44, 0.035), at=(0, 0, 0.555), m=dark, bevel=0.008)
    k.box((1.02, 0.44, 0.03), at=(0, 0, 0.35), m=dark, bevel=0.008)

    # Axles and bolsters (rear at -x, bigger wheels).
    for x, r in ((-0.33, 0.26), (0.33, 0.2)):
        k.cyl(0.028, 0.64, at=(x, 0, r), rot=(90, 0, 0), m=iron)
        h = 0.34 - r + 0.02
        k.box((0.08, 0.44, h), at=(x, 0, r + h / 2 - 0.01), m=dark, bevel=0.006)
        for y in (-0.275, 0.275):
            wheel(k, x, y, r, red, dark)

    # Tongue from the front axle, tip resting on the trail.
    k.unframed(k.tube([(0.33, 0, 0.2), (0.6, 0, 0.13), (0.92, 0, 0.035)], 0.022, wood))
    k.unframed(k.box((0.05, 0.3, 0.04), at=(0.9, 0, 0.03), m=wood, bevel=0.006))

    # Canvas cover: lathe along x, bottom flattened onto the box, top raised into a tall arch.
    profile = [(0.0, 0.08), (0.17, 0.07), (0.22, 0.04), (0.26, 0.0), (0.255, 0.04), (0.24, 0.12),
               (0.232, 0.25), (0.228, 0.4), (0.227, 0.52), (0.228, 0.64), (0.232, 0.79), (0.24, 0.92),
               (0.255, 1.0), (0.26, 1.04), (0.22, 1.0), (0.17, 0.97), (0.0, 0.96)]
    cover = k.lathe(profile, at=(-0.52, 0, 0.565), rot=(0, 90, 0), m=canvas)
    # Local x points down after the rotation: flatten below the box top, stretch the arch upward.
    k.warp(cover, lambda p: (p[0] * 1.35 if p[0] < 0 else 0.0, p[1], p[2]))

    # Dry prairie with a dirt trail and low hills far back.
    k.floor("#d8c47a", "matte")
    k.box((12, 0.9, 0.004), at=(0, 0, 0.002), m=k.mat("#c49a62", "matte"), bevel=0, setting=True)
    hills = k.mat("#b9c46e", "matte")
    k.sphere(2.5, at=(-2.5, 9, -1.4), scale=(2.4, 1, 0.6), m=hills, setting=True)
    k.sphere(2.5, at=(4.0, 11, -1.5), scale=(2.8, 1, 0.6), m=hills, setting=True)
