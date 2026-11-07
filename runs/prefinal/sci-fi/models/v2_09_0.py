# Observatory dome: a short round wall stands on the lawn, a light grey ring caps it, and the white dome sits on
# the ring. The slit runs as one dark band over the dome from its base past the top, edged by two shutter rails.
# A small red door sits in a light grey frame at the wall's base, turned toward the camera beside the slit.
import math

SCENE = {"category": "4", "backdrop": "#5ab8f0", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f4f5f2", "satin")
    grey = k.mat("#c3c8cf", "satin")
    dark = k.mat("#2a3240", "matte")
    red = k.mat("#d8322b", "satin")

    # Wall, plinth and cap ring
    k.cyl(0.46, 0.04, at=(0, 0, 0.02), m=grey, bevel=0.01)
    k.cyl(0.44, 0.38, at=(0, 0, 0.21), m=white, bevel=0.01)
    k.cyl(0.475, 0.05, at=(0, 0, 0.405), m=grey, bevel=0.012)

    # Dome
    R, base = 0.45, 0.43
    prof = [(R * math.cos(math.radians(t)), base + R * math.sin(math.radians(t))) for t in range(0, 90, 5)]
    k.lathe(prof + [(0, base + R)], at=(0, 0, 0), m=white)

    # Slit band and shutter rails along a meridian facing the camera side
    a = 15
    ar = math.radians(a)
    d = (math.sin(ar), -math.cos(ar))
    t = (math.cos(ar), math.sin(ar))
    step = 7.5

    def point(theta, rad, off=0.0):
        th = math.radians(theta)
        return (rad * math.cos(th) * d[0] + off * t[0], rad * math.cos(th) * d[1] + off * t[1],
                base + rad * math.sin(th))

    theta = step / 2
    while theta < 110:
        k.box((0.12, 0.012, R * math.radians(step) * 1.15), at=point(theta, R + 0.002),
              rot=(-theta, 0, a), m=dark, bevel=0.002)
        theta += step
    for off in (-0.072, 0.072):
        pts = [point(th, R + 0.008, off) for th in range(0, 112, 8)]
        k.tube(pts, 0.018, grey, curved=True)

    # Door at the wall base
    b = math.radians(-28)
    dd = (math.sin(b), -math.cos(b))
    k.box((0.2, 0.03, 0.29), at=(0.432 * dd[0], 0.432 * dd[1], 0.165), rot=(0, 0, -28), m=grey, bevel=0.01)
    k.box((0.15, 0.03, 0.24), at=(0.448 * dd[0], 0.448 * dd[1], 0.16), rot=(0, 0, -28), m=red, bevel=0.008)
    kx, ky = 0.468 * dd[0] + 0.05 * math.cos(b), 0.468 * dd[1] + 0.05 * math.sin(b)
    k.sphere(0.014, at=(kx, ky, 0.16), m=k.mat("#e8c45a", "metal"))

    # Lawn
    k.floor("#5cbf3a", "matte")
