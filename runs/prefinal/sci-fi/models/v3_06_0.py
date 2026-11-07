# Quadcopter drone: a round white shell; four arms run out on the diagonals from its rim, each ending in a
# motor pod that carries a black round rotor disc on a hub. A short mount under the shell holds a ball
# gimbal with the camera, its blue lens facing forward. Floating in the sky, tipped forward as in flight.
import math

SCENE = {"category": "1", "backdrop": "#ffc83a", "azimuth": 30, "elevation": 18, "lens": 60, "light": "left"}


def build(k):
    white = k.mat("#f6f7f9", "satin")
    black = k.mat("#1d1f24", "satin")
    grey = k.mat("#5b616b", "satin")
    lens = k.mat("#2f8cff", "glass")

    # Round body shell.
    k.lathe([(0.0, -0.06), (0.17, -0.06), (0.21, -0.045), (0.232, -0.015), (0.235, 0.01),
             (0.222, 0.04), (0.19, 0.07), (0.14, 0.092), (0.08, 0.104), (0.0, 0.108)],
            at=(0, 0, 0), rot=(0, 0, 0), m=white)

    # Four arms, motor pods and rotors.
    for i in range(4):
        a = math.radians(45 + 90 * i)
        dx, dy = math.cos(a), math.sin(a)
        ex, ey = 0.42 * dx, 0.42 * dy
        k.tube([(0.16 * dx, 0.16 * dy, 0.0), (ex, ey, 0.0)], 0.032, white)
        k.cyl(0.05, 0.08, at=(ex, ey, 0.01), rot=(0, 0, 0), m=white, bevel=0.01)
        k.cyl(0.014, 0.03, at=(ex, ey, 0.062), rot=(0, 0, 0), m=grey)
        k.cyl(0.165, 0.014, at=(ex, ey, 0.082), rot=(0, 0, 0), m=black, bevel=0.005)
        k.sphere(0.03, at=(ex, ey, 0.092), scale=(1, 1, 0.6), m=black)

    # Camera on a gimbal under the body.
    k.cyl(0.035, 0.05, at=(0, -0.03, -0.075), rot=(0, 0, 0), m=grey)
    k.sphere(0.06, at=(0, -0.03, -0.13), m=white)
    k.cyl(0.036, 0.03, at=(0, -0.08, -0.13), rot=(90, 0, 0), m=black, bevel=0.006)
    k.cyl(0.026, 0.012, at=(0, -0.098, -0.13), rot=(90, 0, 0), m=lens, bevel=0.004)

    k.turn(8, -5, 0)
