# Crystal ball: a clear glass sphere rests in the hollow cup of a gold lathe-turned stand (wide foot, narrow
# waist, flared cup that follows the sphere's underside). Three curved gold claws rise from the cup rim and hug
# the sphere's lower half. The mist inside is left to the image model; one small pink sparkle glows in the ball.
# The stand sits on a wooden ledge whose top is z = 0 and runs off the card at both sides and at the bottom.
import math

SCENE = {"category": "2", "backdrop": "#5cc24a", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    gold = k.mat("#e8b53a", "metal")
    glass = k.mat("#a9dcff", "glass")
    sparkle = k.mat("#ff7fc8", "glow")

    R, cz = 0.36, 0.568
    under = lambda r: cz - math.sqrt(R * R - r * r)

    # Stand: foot, waist, cup; the inner profile follows the sphere so the ball sits in it.
    outer = [(0.0, 0.0), (0.30, 0.0), (0.315, 0.015), (0.31, 0.035), (0.28, 0.06), (0.21, 0.08),
             (0.14, 0.105), (0.105, 0.14), (0.10, 0.165), (0.115, 0.19), (0.16, 0.22), (0.21, 0.255),
             (0.245, 0.29), (0.255, 0.305)]
    inner = [(r, under(r) - 0.002) for r in (0.235, 0.2, 0.16, 0.12, 0.08, 0.04, 0.0)]
    k.lathe(outer + inner, at=(0, 0, 0), m=gold)

    # Three claws from the cup rim curving up along the sphere.
    for i in range(3):
        a = math.radians(90 + i * 120)
        pts = []
        for phi in (-48, -38, -28, -18, -10):
            p = math.radians(phi)
            rr = (R + 0.018) * math.cos(p)
            pts.append((rr * math.cos(a), rr * math.sin(a), cz + (R + 0.018) * math.sin(p)))
        k.tube(pts, 0.022, gold, curved=True)
        k.sphere(0.03, at=pts[-1], m=gold)

    k.sphere(R, at=(0, 0, cz), m=glass)
    k.sphere(0.03, at=(0.08, -0.12, cz + 0.1), m=sparkle)

    # Wooden ledge, deep enough at the front to run off the bottom of the card.
    k.box((4, 2.4, 0.12), at=(0, -0.1, -0.06), m=k.mat("#9a5a2b", "matte"), bevel=0.01, setting=True)
