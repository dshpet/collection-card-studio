# Gold detective badge: a shield-shaped gold plate (flat top with a soft crown, straight sides, curving to a point
# at the bottom), a raised silver rim tube running round its front edge, and a small raised house pictogram
# (walls, gabled roof, chimney) embossed in the centre. It floats, tilted a little to show the face and the edge.
import math

SCENE = {"category": "1", "backdrop": "#1f6fe0", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}

# Shield outline in the badge plane (x across, v up), clockwise from the top centre.
_HALF = [(0.0, 0.5), (0.2, 0.47), (0.42, 0.45), (0.43, 0.2), (0.42, 0.0), (0.38, -0.2),
         (0.27, -0.38), (0.13, -0.5), (0.0, -0.57)]
OUTLINE = _HALF + [(-x, v) for x, v in reversed(_HALF[1:-1])]


def _ray_hit(a):
    """Distance from the origin to the shield outline along angle a."""
    dx, dy = math.cos(a), math.sin(a)
    best = 1.0
    n = len(OUTLINE)
    for i in range(n):
        (x1, y1), (x2, y2) = OUTLINE[i], OUTLINE[(i + 1) % n]
        ex, ey = x2 - x1, y2 - y1
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = (x1 * ey - y1 * ex) / den
        s = (x1 * dy - y1 * dx) / den
        if t > 0 and -1e-6 <= s <= 1 + 1e-6:
            best = t
    return best


def _dense_outline(scale, step=0.02):
    pts = []
    n = len(OUTLINE)
    for i in range(n):
        (x1, y1), (x2, y2) = OUTLINE[i], OUTLINE[(i + 1) % n]
        seg = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for j in range(seg):
            f = j / seg
            pts.append(((x1 + (x2 - x1) * f) * scale, (y1 + (y2 - y1) * f) * scale))
    return pts


def build(k):
    gold = k.mat("#f2b51c", "metal")
    silver = k.mat("#d3d8df", "metal")
    r0 = 0.3

    def shield(p):
        x, y, z = p
        rho = math.hypot(x, y)
        if rho < 1e-6:
            return p
        a = math.atan2(y, x)
        d = _ray_hit(a) * 0.98 * rho / r0
        return (d * math.cos(a), d * math.sin(a), z)

    # Gold plate: a dense cylinder whose rims are pushed out onto the shield outline; its face looks toward -y.
    plate = k.cyl(r0, 0.06, at=(0, 0, 0), rot=(90, 0, 0), m=gold, bevel=0.008, verts=160)
    k.warp(plate, shield)

    # Raised silver rim following the front edge, standing proud of the gold face.
    ring = [(x, -0.03, v) for x, v in _dense_outline(0.955)]
    k.tube(ring + ring[:3], 0.034, silver, curved=True)

    # Embossed house standing on the plate face: walls, gabled roof (a box tapered to a ridge), chimney.
    depth = 0.03
    yc = -0.03 - depth / 2 + 0.002
    k.box((0.22, depth, 0.15), at=(0, yc, -0.06), m=gold, bevel=0.006)
    roof = k.box((0.32, depth, 0.13), at=(0, yc, 0.08), m=gold, bevel=0.004)
    k.warp(roof, lambda p: (p[0] * (0.065 - p[2]) / 0.13, p[1], p[2]))
    k.box((0.04, depth, 0.07), at=(0.07, yc, 0.095), m=gold, bevel=0.004)

    k.turn(6, 0, -8)
