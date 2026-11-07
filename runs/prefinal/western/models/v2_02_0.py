# Pair of cowboy spurs. Each U-shaped heel band opens toward the toe (+x). A short neck runs back from the
# heel of the band and splits into a fork. An axle through the fork carries the spiky rowel, a star wheel
# standing upright in the band's plane so it faces the camera. A leather strap is riveted to button studs at
# both band ends and arches over the instep, with a small buckle on top. The two spurs float side by side,
# one higher and further forward than the other.
import math

SCENE = {"category": "1", "backdrop": "#2fb8ee", "azimuth": 22, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    dark = k.mat("#8b9099", "metal")
    leather = k.mat("#8a4f24", "matte")

    def spur(ox, oy, oz):
        def p(x, y, z):
            return (ox + x, oy + y, oz + z)

        R, arm = 0.16, 0.12
        # Heel band: semicircle at the back with straight arms forward.
        band = [p(arm, R, 0), p(0.04, R, 0)]
        for i in range(1, 12):
            a = math.pi / 2 + i * math.pi / 12
            band.append(p(R * math.cos(a), R * math.sin(a), 0))
        band += [p(0.04, -R, 0), p(arm, -R, 0)]
        k.tube(band, 0.024, silver, curved=True)
        # Button studs at the band ends, where the strap is riveted.
        for s in (-1, 1):
            k.cyl(0.032, 0.03, at=p(0.10, s * (R + 0.018), 0), rot=(90, 0, 0), m=dark)
        # Neck rising slightly back from the heel of the band.
        k.tube([p(-R + 0.01, 0, 0), p(-0.26, 0, 0.02), p(-0.33, 0, 0.045)], 0.024, silver, curved=True)
        # Fork tines on either side of the rowel, and the axle through them.
        hub = (-0.42, 0, 0.06)
        for s in (-1, 1):
            k.tube([p(-0.33, 0, 0.045), p(-0.36, s * 0.03, 0.05), p(hub[0], s * 0.03, hub[2])], 0.014, silver)
        k.cyl(0.016, 0.085, at=p(*hub), rot=(90, 0, 0), m=dark)
        # Rowel: a hub disc with twelve spikes in the xz plane.
        k.cyl(0.05, 0.022, at=p(*hub), rot=(90, 0, 0), m=silver, bevel=0.004)
        for i in range(12):
            t = math.radians(i * 30 + 15)
            h = 0.09
            d = 0.04 + h / 2
            k.cone(0.018, 0.003, h, at=p(hub[0] + d * math.sin(t), 0, hub[2] + d * math.cos(t)),
                   rot=(0, i * 30 + 15, 0), m=silver)
        # Leather strap arching over the instep between the band ends.
        n = 14
        sr = R + 0.018
        for i in range(n):
            a = math.pi * (i + 0.5) / n
            L = 2 * sr * math.sin(math.pi / (2 * n)) + 0.006
            k.box((0.07, L, 0.014), at=p(0.10, sr * math.cos(a), sr * math.sin(a)),
                  rot=(math.degrees(a) + 90, 0, 0), m=leather, bevel=0.004)
        # Buckle frame on top of the strap.
        top = p(0.10, 0, sr + 0.012)
        k.tube([(top[0] - 0.05, top[1] - 0.035, top[2]), (top[0] + 0.05, top[1] - 0.035, top[2]),
                (top[0] + 0.05, top[1] + 0.035, top[2]), (top[0] - 0.05, top[1] + 0.035, top[2]),
                (top[0] - 0.05, top[1] - 0.035, top[2])], 0.009, silver)

    spur(-0.06, -0.14, 0.14)
    spur(0.08, 0.16, -0.14)
    k.turn(8, -10, -12)
