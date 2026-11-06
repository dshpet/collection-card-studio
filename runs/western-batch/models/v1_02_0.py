# Lasso: one tan rope. Its free inner end hangs inside a hank of four coils; the coils gather at the top, where a
# red cord wraps the bundle several times and ties off in a small knot. The rope leaves the coil down its right
# side to the honda (the sliding knot), runs through it and opens into a wide loop tilted toward the camera,
# whose end comes back into the knot with a short free tail.
import math

SCENE = {"category": "1", "backdrop": "#6a4fe6", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    rope = k.mat("#d4a86a", "matte")
    cord = k.mat("#d8322e", "matte")
    r = 0.022

    # Coil: four drooping loops that share a top point, stacked front to back.
    cx, cz, b, turns = -0.15, 0.65, 0.28, 4
    pts = [(cx - 0.07, -0.07, 0.48), (cx - 0.05, -0.065, 0.62), (cx - 0.02, -0.06, 0.8)]  # free inner end
    n = turns * 16
    for i in range(n + 5):  # four turns, then a quarter more down the right side
        t = 2 * math.pi * i / 16
        a = 0.22 + 0.015 * math.sin(1.7 * t)
        th = math.pi / 2 - t
        y = -0.05 + 0.1 * min(t, 2 * math.pi * turns) / (2 * math.pi * turns)
        pts.append((cx + a * math.cos(th), y, cz + b * math.sin(th) - 0.02 * math.sin(t / 2) ** 2))

    # Big loop through the honda.
    R, al = 0.33, math.radians(55)
    u, v = (1.0, 0.0, 0.0), (0.0, math.cos(al), math.sin(al))
    H = (0.18, -0.1, 0.25)
    p0 = 150.0
    L = tuple(H[j] - R * (math.cos(math.radians(p0)) * u[j] + math.sin(math.radians(p0)) * v[j]) for j in range(3))

    def on_loop(deg, rad=R):
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return tuple(L[j] + rad * (c * u[j] + s * v[j]) for j in range(3))

    pts += [(0.12, -0.02, 0.5), (0.16, -0.07, 0.36), H]  # standing part down to the knot
    for d in range(10, 360, 15):
        pts.append(on_loop(p0 + d))
    pts.append(H)
    tang = tuple(-math.sin(math.radians(p0)) * u[j] + math.cos(math.radians(p0)) * v[j] for j in range(3))
    pts.append(tuple(H[j] + 0.1 * tang[j] + (0, 0, -0.02)[j] for j in range(3)))  # short free tail
    k.tube(pts, r, rope, curved=True)

    # Honda: the sliding knot, a lump of turns around the rope.
    knot = [(H[0] + s * tang[0] * 0.035, H[1] + s * tang[1] * 0.035, H[2] + s * tang[2] * 0.035, 0.042)
            for s in (-1, 0, 1)]
    k.blob(knot, rope)

    # Red cord wrapped around the gathered top of the coil, tied off on top.
    top = cz + b - 0.01
    helix = []
    wraps, x0, x1, rr = 4, cx - 0.08, cx + 0.08, 0.078
    for i in range(wraps * 16 + 1):
        f = i / (wraps * 16)
        ph = 2 * math.pi * wraps * f
        helix.append((x0 + (x1 - x0) * f, rr * math.cos(ph), top + rr * math.sin(ph)))
    k.tube(helix, 0.014, cord, curved=True)
    k.sphere(0.03, at=(x1 + 0.005, 0.0, top + rr), scale=(1, 1, 0.8), m=cord)
    k.tube([(x1 + 0.01, 0.0, top + rr + 0.01), (x1 + 0.05, -0.02, top + rr + 0.04), (x1 + 0.09, -0.03, top + rr + 0.03)],
           0.013, cord, curved=True)

    k.turn(8, 0, -12)
