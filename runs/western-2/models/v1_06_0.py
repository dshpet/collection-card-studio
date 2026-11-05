# Leather saddle straddling a wooden fence rail. The red blanket drapes over the rail; the leather skirt lies on
# the blanket and hangs down both sides; the seat block sits on the skirt, dished, with the cantle rising at the
# back and the pommel swelling at the front under the horn (neck + cap). A fender hangs on each side, a short
# stirrup leather runs from its foot to a bolt that carries the silver stirrup. A loose cinch strap hangs from a
# rigging ring on the near side and ends free in a buckle. The rail is nailed to posts far off the card, so it
# runs off both sides.
SCENE = {"category": "3", "backdrop": "#3cc8f0", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    seat_m = k.mat("#7a4524", "matte")
    skirt_m = k.mat("#9a5a2e", "matte")
    fender_m = k.mat("#8a4f28", "matte")
    horn_m = k.mat("#6a3a1e", "matte")
    blanket = k.mat("#d8322f", "matte")
    silver = k.mat("#cfd4da", "metal")
    wood = k.mat("#b9773e", "matte")

    # Fence: rail top at z = 0, nailed to posts far off the card.
    k.box((6, 0.2, 0.16), at=(0, 0, -0.08), m=wood, bevel=0.015, setting=True)
    for x in (-1.5, 1.5):
        k.box((0.18, 0.18, 3), at=(x, 0.19, -1.48), m=wood, bevel=0.015, setting=True)

    # Blanket draped over the rail, a little larger than the skirt so its edge shows.
    k.box((1.0, 0.28, 0.03), at=(0, 0, 0.015), m=blanket, bevel=0.01)
    for s in (-1, 1):
        k.box((1.0, 0.03, 0.33), at=(0, s * 0.125, -0.135), m=blanket, bevel=0.012)

    # Leather skirt over the blanket.
    k.box((0.86, 0.36, 0.04), at=(0, 0, 0.05), m=skirt_m, bevel=0.015)
    for s in (-1, 1):
        k.box((0.86, 0.035, 0.32), at=(0, s * 0.165, -0.09), m=skirt_m, bevel=0.03)

    # Seat: a dense disk warped into a solid block, dished, cantle rising at the back (-x).
    n = 20
    profile = [(i / n, 0.0) for i in range(n + 1)] + [(1 - i / n, 0.06) for i in range(n + 1)]

    def seat_shape(p):
        x, y, z = p
        h = 0.04 + 0.04 * x * x + 0.2 * max(0.0, -x) ** 4 - 0.04 * y * y
        return (0.36 * x, 0.18 * y, z + (h if z > 0.03 else 0.0))

    k.warp(k.lathe(profile, at=(-0.03, 0, 0.07), rot=(0, 0, 0), m=seat_m), seat_shape)

    # Pommel swell and horn at the front (+x).
    k.blob([(0.30, 0, 0.12, 0.1, (0.9, 1.7, 1.0))], skirt_m)
    k.cyl(0.035, 0.16, at=(0.32, 0, 0.26), rot=(0, 0, 0), m=horn_m, bevel=0.008)
    k.cyl(0.075, 0.035, at=(0.32, 0, 0.355), rot=(0, 0, 0), m=horn_m, bevel=0.012)

    # Fenders, stirrup leathers and stirrups on both sides.
    fx = -0.02
    for s in (-1, 1):
        y = s * 0.2
        k.box((0.22, 0.03, 0.40), at=(fx, y, -0.13), m=fender_m, bevel=0.03)
        k.box((0.06, 0.02, 0.10), at=(fx, y, -0.375), m=fender_m, bevel=0.005)
        k.cyl(0.014, 0.05, at=(fx, y, -0.425), rot=(90, 0, 0), m=silver)
        arch = [(-0.075, -0.57), (-0.07, -0.50), (-0.04, -0.445), (0, -0.425),
                (0.04, -0.445), (0.07, -0.50), (0.075, -0.57)]
        k.tube([(fx + ax, y, az) for ax, az in arch], 0.015, silver, curved=True)
        k.box((0.17, 0.08, 0.025), at=(fx, y, -0.575), m=silver, bevel=0.008)

    # Loose cinch strap on the near side: rigging ring on the skirt, strap hanging, buckle at the free end.
    sx, sy = 0.27, -0.195
    k.torus(0.035, 0.009, at=(sx, sy, -0.02), rot=(90, 0, 0), m=silver)
    k.box((0.055, 0.014, 0.40), at=(sx, sy, -0.24), m=fender_m, bevel=0.004)
    k.torus(0.033, 0.009, at=(sx, sy - 0.01, -0.44), rot=(90, 0, 0), m=silver)
