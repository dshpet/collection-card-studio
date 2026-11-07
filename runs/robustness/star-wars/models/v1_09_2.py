# Cockpit control panel: an upright light-grey panel is set into the ship's metal wall, its back sunk in the
# wall. A tilted ledge juts from its foot on a console base that stands on the cockpit floor. The square green
# screen (raised wave line) and the round dial sit high on the upright face. A row of red buttons and two short
# levers sit on the ledge, below the dial. Each lever turns on an axle across its slotted housing. The setting is
# the wall and floor right around the panel. The base runs off the bottom of the card.
import math

SCENE = {"category": "4", "backdrop": "#f2c14e", "azimuth": 22, "elevation": 14, "lens": 60, "light": "left"}

TILT = 15.0


def build(k):
    panel = k.mat("#b4bac3", "satin")
    trim = k.mat("#9aa1ab", "metal")
    dark = k.mat("#3c424b", "satin")
    red = k.mat("#e8322f", "gloss")
    screen = k.mat("#2f9e48", "gloss")
    wave = k.mat("#b6ff9a", "glow")
    face = k.mat("#f4f1e6", "satin")

    # Upright panel, back sunk into the wall (wall face at y = 0.1).
    k.box((1.0, 0.14, 0.56), at=(0, 0.06, 0.63), m=panel, bevel=0.02)
    k.box((1.06, 0.1, 0.04), at=(0, 0.06, 0.92), m=trim, bevel=0.01)
    for x in (-0.51, 0.51):
        k.box((0.04, 0.1, 0.62), at=(x, 0.06, 0.62), m=trim, bevel=0.01)

    # Tilted ledge (front edge lower) on a console base standing on the floor.
    th = math.radians(TILT)
    n = (0.0, -math.sin(th), math.cos(th))   # ledge top normal
    u = (0.0, math.cos(th), math.sin(th))    # ledge depth direction, toward the wall
    c = (0.0, -0.12, 0.33)
    k.box((1.0, 0.28, 0.08), at=c, rot=(TILT, 0, 0), m=panel, bevel=0.015)
    base = k.box((0.98, 0.3, 0.3), at=(0, -0.05, 0.15), m=panel, bevel=0.015)
    kick = k.box((0.94, 0.04, 0.06), at=(0, -0.205, 0.03), m=dark, bevel=0.005)
    k.unframed(base, kick)

    def on_ledge(x, v, h):
        return (x, c[1] + v * u[1] + h * n[1], c[2] + v * u[2] + h * n[2])

    # Square screen with bezel and a raised wave line.
    sx, sz = -0.24, 0.71
    k.box((0.3, 0.03, 0.3), at=(sx, -0.02, sz), m=dark, bevel=0.012)
    k.box((0.24, 0.02, 0.24), at=(sx, -0.03, sz), m=screen, bevel=0.004)
    pts = [(sx - 0.09 + 0.18 * i / 24, -0.043, sz + 0.045 * math.sin(i / 24 * 2 * math.pi * 1.5))
           for i in range(25)]
    k.tube(pts, 0.008, wave, curved=True)

    # Round dial: bezel ring, face, needle on a centre cap.
    dx, dz = 0.24, 0.71
    k.cyl(0.165, 0.04, at=(dx, -0.02, dz), rot=(90, 0, 0), m=trim, bevel=0.01)
    k.cyl(0.14, 0.02, at=(dx, -0.035, dz), rot=(90, 0, 0), m=face, bevel=0.003)
    k.torus(0.15, 0.016, at=(dx, -0.042, dz), rot=(90, 0, 0), m=trim)
    k.box((0.016, 0.008, 0.11), at=(dx + 0.025, -0.05, dz + 0.045), rot=(0, 30, 0), m=red, bevel=0.003)
    k.cyl(0.022, 0.02, at=(dx, -0.052, dz), rot=(90, 0, 0), m=dark, bevel=0.004)

    # Row of round red buttons on the ledge, each in a grey collar.
    for i in range(5):
        x = -0.4 + i * 0.105
        k.cyl(0.04, 0.016, at=on_ledge(x, -0.02, 0.048), rot=(TILT, 0, 0), m=trim, bevel=0.004)
        k.cyl(0.03, 0.03, at=on_ledge(x, -0.02, 0.065), rot=(TILT, 0, 0), m=red, bevel=0.008)

    # Two short levers: slotted housing, axle across it, rod and knob, kept below the dial.
    for x in (0.2, 0.36):
        k.box((0.08, 0.16, 0.04), at=on_ledge(x, 0.0, 0.055), rot=(TILT, 0, 0), m=dark, bevel=0.008)
        pivot = on_ledge(x, 0.0, 0.08)
        k.cyl(0.016, 0.09, at=pivot, rot=(0, 90, 0), m=trim, bevel=0.003)
        lean = -0.05 if x < 0.3 else 0.03
        tip = (x, pivot[1] + lean, pivot[2] + 0.14)
        k.tube([pivot, tip], 0.014, trim)
        k.sphere(0.033, at=tip, m=red if x < 0.3 else dark)

    # Setting: painted metal wall with seams and rivets, and the cockpit floor.
    wall = k.mat("#e0a63c", "satin")
    seam = k.mat("#a9763a", "metal")
    k.box((5, 0.3, 3.2), at=(0, 0.25, 1.4), m=wall, bevel=0.0, setting=True)
    for z in (0.08, 1.15):
        k.box((5, 0.04, 0.05), at=(0, 0.1, z), m=seam, bevel=0.008, setting=True)
    for x in (-0.95, 0.95):
        k.box((0.05, 0.04, 3.0), at=(x, 0.1, 1.4), m=seam, bevel=0.008, setting=True)
        for z in (0.3, 0.6, 0.9):
            k.sphere(0.018, at=(x, 0.075, z), m=seam, setting=True)
    k.floor("#6d737c", finish="satin")
