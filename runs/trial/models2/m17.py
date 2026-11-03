# Round wall clock seen straight on: true circles, every hand on one center cap, evenly spaced marks.
import math

SCENE = {"category": "2", "backdrop": "#7cc943", "azimuth": 0, "elevation": 0, "light": "left"}


def build(k):
    navy, orange = k.mat("#1f2a5c", "satin"), k.mat("#ff8a1e", "gloss")
    k.cyl(0.33, 0.07, at=(0, 0.035, 0), rot=(90, 0, 0), m=orange, bevel=0.02)
    k.torus(0.31, 0.035, at=(0, -0.005, 0), rot=(90, 0, 0), m=orange)
    k.cyl(0.29, 0.01, at=(0, -0.003, 0), rot=(90, 0, 0), m=k.mat("#fbfbf7", "satin"), bevel=0)
    for i in range(60):
        a = math.radians(i * 6)
        if i % 5 == 0:
            k.box((0.016, 0.006, 0.05), at=(0.235 * math.sin(a), -0.01, 0.235 * math.cos(a)), rot=(0, i * 6, 0),
                  m=navy, bevel=0.003)
        else:
            k.sphere(0.0055, at=(0.262 * math.sin(a), -0.009, 0.262 * math.cos(a)), m=navy)

    def hand(angle, length, width, depth, m, tail=0.0):
        a = math.radians(angle)
        middle = (length - tail) / 2
        k.box((width, 0.005, length + tail), at=(middle * math.sin(a), depth, middle * math.cos(a)), rot=(0, angle, 0),
              m=m, bevel=0.002)

    hand(305, 0.13, 0.024, -0.012, navy)
    hand(60, 0.2, 0.017, -0.018, navy)
    hand(150, 0.23, 0.006, -0.024, k.mat("#e3262b", "satin"), tail=0.05)
    k.cyl(0.02, 0.012, at=(0, -0.026, 0), rot=(90, 0, 0), m=navy)
    k.cyl(0.008, 0.006, at=(0, -0.034, 0), rot=(90, 0, 0), m=k.mat("#e3262b", "satin"))
    for i in range(-8, 9):
        shade = "#6cbf3a" if i % 2 else "#8fd655"
        k.box((0.25, 0.02, 4), at=(i * 0.25, 0.08, 0), m=k.mat(shade, "matte"), bevel=0, setting=True)
