# Sheriff star: one thick five-pointed gold plate facing the camera, a ball fixed on each of its five tips,
# and a raised rim running along all ten edges of its front face. It floats, tilted, on a flat purple backdrop.
import math

SCENE = {"category": "1", "backdrop": "#6a2c9e", "azimuth": 22, "elevation": 10, "lens": 70, "light": "left"}

R, RI, T, CZ = 0.5, 0.22, 0.08, 0.6  # tip radius, inner radius, plate thickness, center height


def corner(i, scale_tip=1.0, scale_in=1.0):
    a = math.pi / 2 + i * math.pi / 5
    rad = R * scale_tip if i % 2 == 0 else RI * scale_in
    return rad * math.cos(a), rad * math.sin(a)


def star_edge(a):
    """Point on the star outline along the ray at angle a (star plane, tip at +y)."""
    step = math.pi / 5
    n = math.floor(((a - math.pi / 2) % (2 * math.pi)) / step)
    p, q = corner(n), corner(n + 1)
    ex, ey = q[0] - p[0], q[1] - p[1]
    dx, dy = math.cos(a), math.sin(a)
    t = (p[0] * ey - p[1] * ex) / (dx * ey - dy * ex)
    return t * dx, t * dy


def build(k):
    gold = k.mat("#f2b632", "metal")
    rim_gold = k.mat("#f7c94a", "metal")

    # Star plate: a 40-sided disc warped onto the star outline, then stood up to face -y.
    plate = k.cyl(1.0, T, at=(0, 0, CZ), rot=(90, 0, 0), m=gold, bevel=0, verts=40)

    def to_star(v):
        x, y, z = v
        rho = math.hypot(x, y)
        if rho < 1e-6:
            return v
        ex, ey = star_edge(math.atan2(y, x))
        return ex * rho, ey * rho, z

    k.warp(plate, to_star)

    # Raised rim along the front face's edges (star plane is world xz, front face at y = -T/2).
    pts = []
    for i in range(11):
        x, z = corner(i % 10, 0.9, 0.86)
        pts.append((x, -T / 2 - 0.01, CZ + z))
    k.tube(pts, 0.026, rim_gold)

    # A ball on each of the five tips, sunk a little into the point so it is fixed to it.
    for i in range(0, 10, 2):
        x, z = corner(i, 1.06, 1.0)
        k.sphere(0.075, at=(x, 0, CZ + z), m=gold)

    k.turn(8, -10, 22)
