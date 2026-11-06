# Ringed planet: one round orange sphere, floating. A flat pale-yellow ring circles its equator with a small gap
# from the surface. One red band runs around the southern half, well clear of the ring, so the sphere reads as a
# banded planet and not a hat. The hero has a mild tilt only, so the ring shows a thin top face and the planet's
# lower half shows below it. There is no floor or setting.
SCENE = {"category": "1", "backdrop": "#2fc4ee", "azimuth": 20, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    planet = k.mat("#f28a2e", "satin")
    stripe = k.mat("#d93a2b", "satin")
    ring = k.mat("#ecd27a", "matte")
    cz, R = 0.5, 0.4

    k.sphere(R, at=(0, 0, cz), m=planet)

    # Red band: a thin shell following the sphere between two latitudes in the southern half, clear of the ring.
    n = 12
    z0, z1, rr = -0.24, -0.15, R + 0.006
    outer = []
    for i in range(n + 1):
        z = z0 + (z1 - z0) * i / n
        outer.append(((rr * rr - z * z) ** 0.5, z))
    inner = [((R * R - z * z) ** 0.5 - 0.004, z) for _, z in reversed(outer)]
    k.lathe(outer + inner + [outer[0]], at=(0, 0, cz), rot=(0, 0, 0), m=stripe)

    # Ring: a flat annulus with soft edges, around the equator, with a gap from the surface.
    ri, ro, t = 0.50, 0.70, 0.012
    profile = [(ri, -t), (ro - 0.01, -t), (ro, -t + 0.006), (ro, t - 0.006), (ro - 0.01, t),
               (ri, t), (ri - 0.006, 0), (ri, -t)]
    k.lathe(profile, at=(0, 0, cz), rot=(0, 0, 0), m=ring)

    k.turn(8, -18, 0)
