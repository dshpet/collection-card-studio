# Flying saucer: one lathed silver hull, a wide disc thickest at the center that thins to a rim band; a light-blue
# glass dome sits on a metal collar on top; a ring of small orange lights is set into the rim band all the way
# round; a shallow drive bulge sits under the center. Floating, tilted toward the camera to show the dome and top.
import math

SCENE = {"category": "1", "backdrop": "#7a4fe0", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    dark = k.mat("#8b919b", "metal")
    glass = k.mat("#bfeaff", "glass")
    light = k.mat("#ff6f12", "glow")

    # Hull: lower bowl up to the rim, then the upper deck sloping in to the dome collar.
    hull = [(0.0, 0.0), (0.12, 0.005), (0.24, 0.025), (0.34, 0.055), (0.42, 0.09), (0.47, 0.12),
            (0.5, 0.145), (0.505, 0.16), (0.5, 0.175), (0.47, 0.195), (0.42, 0.22), (0.34, 0.245),
            (0.26, 0.262), (0.2, 0.27), (0.0, 0.27)]
    k.lathe(hull, at=(0, 0, 0), rot=(0, 0, 0), m=silver)

    # Rim band the lights sit in.
    k.torus(0.5, 0.03, at=(0, 0, 0.16), rot=(0, 0, 0), m=dark)
    n = 14
    for i in range(n):
        a = 2 * math.pi * i / n
        k.sphere(0.03, at=(0.528 * math.cos(a), 0.528 * math.sin(a), 0.16), m=light)

    # Underside drive bulge.
    k.lathe([(0.0, -0.05), (0.06, -0.047), (0.11, -0.035), (0.15, -0.015), (0.17, 0.01)],
            at=(0, 0, 0), rot=(0, 0, 0), m=dark)

    # Dome collar and smooth glass dome.
    k.torus(0.2, 0.022, at=(0, 0, 0.275), rot=(0, 0, 0), m=dark)
    steps = 48
    dome = [(0.195, 0.27)]
    for j in range(1, steps):
        t = j / steps * math.pi / 2
        dome.append((0.195 * math.cos(t), 0.27 + 0.2 * math.sin(t)))
    dome.append((0.0, 0.47))
    k.lathe(dome, at=(0, 0, 0), rot=(0, 0, 0), m=glass)

    # Tilt the top toward the camera and bank it a little, as if in flight.
    k.turn(14, -6, 0)
