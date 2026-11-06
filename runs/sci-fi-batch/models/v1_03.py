# Ringed planet: one round orange sphere, floating. A flat pale-yellow ring circles its equator with a small gap
# from the surface. One red band runs around the southern half, well clear of the ring. The band is almost flush
# with the surface, so the planet stays one smooth ball and is not a capped or collared shape. The hero has a mild
# tilt only, so the ring shows a thin top face and the planet's lower half shows below it. There is no floor or
# setting.
SCENE = {"category": "1", "backdrop": "#2fc4ee", "azimuth": 20, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    planet = k.mat("#ec6f1c", "satin")
    stripe = k.mat("#d6322a", "satin")
    ring = k.mat("#ecd27a", "matte")
    cz, R = 0.5, 0.4

    k.sphere(R, at=(0, 0, cz), m=planet)

    # Red band: a very thin shell that follows the sphere between two southern latitudes. It stands only 0.002
    # proud, so no step shows at its edges.
    n = 16
    z0, z1, rr = -0.25, -0.16, R + 0.002
    outer = []
    for i in range(n + 1):
        z = z0 + (z1 - z0) * i / n
        outer.append(((rr * rr - z * z) ** 0.5, z))
    inner = [((R * R - z * z) ** 0.5 - 0.01, z) for _, z in reversed(outer)]
    k.lathe(outer + inner + [outer[0]], at=(0, 0, cz), rot=(0, 0, 0), m=stripe)

    # Ring: a flat annulus with soft edges, around the equator, with a gap from the surface.
    ri, ro, t = 0.50, 0.70, 0.012
    profile = [(ri, -t), (ro - 0.01, -t), (ro, -t + 0.006), (ro, t - 0.006), (ro - 0.01, t),
               (ri, t), (ri - 0.006, 0), (ri, -t)]
    k.lathe(profile, at=(0, 0, cz), rot=(0, 0, 0), m=ring)

    k.turn(8, -18, 0)
