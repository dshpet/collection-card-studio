# Radar dish: a thick post stands on a bolted flange fixed to a flat concrete pad. A turntable on the post carries a
# yoke of two arms; a horizontal axle between them runs through the hub on the dish's back. The parabolic dish is
# tilted up to the sky, its concave face lined light grey so the bowl reads, and a short feed arm rises from its
# center along its axis to the focus, ending in a feed horn with a small red tip.
import math

SCENE = {"category": "4", "backdrop": "#7fd0f5", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}

TILT = 45  # dish axis elevation from horizontal, facing -y


def build(k):
    white = k.mat("#f4f5f7", "satin")
    lining = k.mat("#d9dde3", "satin")
    grey = k.mat("#c3c8cf", "satin")
    steel = k.mat("#9aa1aa", "metal")
    red = k.mat("#e3262b", "gloss")

    a = math.radians(90 - TILT)  # rotation about x that tips local z toward -y
    axle = (0.0, 0.0, 0.66)

    def frame(x, y, z, origin):
        # dish-local point -> world, local z along the dish axis
        return (origin[0] + x,
                origin[1] + y * math.cos(a) - z * math.sin(a),
                origin[2] + y * math.sin(a) + z * math.cos(a))

    rot = (90 - TILT, 0, 0)

    # flange, post, turntable
    k.cyl(0.17, 0.04, at=(0, 0, 0.02), rot=(0, 0, 0), m=grey, bevel=0.008)
    for i in range(6):
        t = math.radians(i * 60 + 30)
        k.cyl(0.018, 0.03, at=(0.135 * math.cos(t), 0.135 * math.sin(t), 0.05), rot=(0, 0, 0), m=steel, verts=6)
    k.cyl(0.095, 0.40, at=(0, 0, 0.24), rot=(0, 0, 0), m=white, bevel=0.01)
    k.cyl(0.19, 0.05, at=(0, 0, 0.465), rot=(0, 0, 0), m=grey, bevel=0.01)

    # yoke arms and axle
    for s in (-1, 1):
        k.box((0.05, 0.11, 0.21), at=(s * 0.13, 0, 0.585), rot=(0, 0, 0), m=white, bevel=0.012)
        k.cyl(0.04, 0.02, at=(s * 0.165, 0, axle[2]), rot=(0, 90, 0), m=steel)
    k.cyl(0.03, 0.34, at=axle, rot=(0, 90, 0), m=steel)

    # hub on the dish back
    k.cyl(0.08, 0.14, at=frame(0, 0, 0.03, axle), rot=rot, m=grey, bevel=0.01)

    # dish shell: deep paraboloid, outer surface out to the rim lip, inner surface back to the center
    R, d, t = 0.42, 0.17, 0.022
    n = 32
    outer = [(R * i / n, d * (i / n) ** 2) for i in range(n + 1)]
    lip = [(R + 0.014, d + 0.004), (R + 0.008, d + 0.018)]
    inner = [(R * i / n, t + (d + 0.014 - t) * (i / n) ** 2) for i in range(n, -1, -1)]
    vertex = frame(0, 0, 0.10, axle)
    k.lathe(outer + lip + inner, at=vertex, rot=rot, m=white, verts=96)

    # light grey lining on the concave face, stopping short of the white rim
    Ri = R - 0.03
    m_in = 32
    top = [(Ri * i / m_in, t + 0.003 + (d + 0.014 - t) * (Ri * i / m_in / R) ** 2) for i in range(m_in + 1)]
    under = [(Ri * i / m_in, t - 0.004 + (d + 0.014 - t) * (Ri * i / m_in / R) ** 2) for i in range(m_in, -1, -1)]
    k.lathe(top + under, at=vertex, rot=rot, m=lining, verts=96)

    # feed arm from the dish center along the axis to the focus (R^2 / 4d ~ 0.26)
    focus = R * R / (4 * d)
    base = frame(0, 0, t, vertex)
    tip = frame(0, 0, focus - 0.03, vertex)
    k.tube([base, tip], 0.022, grey)
    k.cyl(0.045, 0.014, at=frame(0, 0, t + 0.007, vertex), rot=rot, m=grey)
    k.cyl(0.042, 0.06, at=frame(0, 0, focus - 0.01, vertex), rot=rot, m=grey, bevel=0.006)
    k.sphere(0.03, at=frame(0, 0, focus + 0.025, vertex), scale=(1, 1, 0.8), rot=rot, m=red)

    # flat concrete pad
    k.box((6, 6, 0.2), at=(0, 0, -0.1), rot=(0, 0, 0), m=k.mat("#b9b4ab", "matte"), bevel=0.01, setting=True)
