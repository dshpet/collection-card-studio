# Front door: a tall deep-green paneled door stands in a painted frame set into a cream brick wall. Two jambs and a
# transom bar hold the door; above the transom a half-round fanlight sits under an arched frame with a keystone,
# its glass split by radial glazing bars. Brass knocker (backplate + hanging ring) on the center stile, brass knob
# on the right (hinges with brass knuckles on the left). Two stone steps run from the threshold to the pavement.
# The wall is raised brick courses in running bond over a mortar backing; bricks are cut to meet the frame closely.
import math

SCENE = {"category": "4", "backdrop": "#e8508f", "azimuth": 20, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    green = k.mat("#1d5a3a", "satin")
    brass = k.mat("#d6a63a", "metal")
    frame = k.mat("#f6efe0", "satin")
    stone = k.mat("#cfc4b2", "matte")
    glass = k.mat("#bfe2ef", "glass")

    z0, z1 = 0.16, 1.11          # door bottom (top step) and top
    w = 0.5                      # door width
    cz, rad = 1.15, 0.25         # fanlight center and glass radius

    # Door slab and raised panels (2 columns x 2 rows, middle rail between)
    k.box((w, 0.05, z1 - z0), at=(0, 0.0, (z0 + z1) / 2), m=green, bevel=0.006)
    for x in (-0.115, 0.115):
        for lo, hi in ((0.24, 0.57), (0.70, 1.04)):
            k.box((0.15, 0.02, hi - lo), at=(x, -0.028, (lo + hi) / 2), m=green, bevel=0.01)

    # Frame: jambs up to the transom, transom bar flush with the arch feet, arched head with keystone
    for s in (-1, 1):
        k.box((0.064, 0.08, 1.11 - z0), at=(s * 0.28, -0.01, (z0 + 1.11) / 2), m=frame, bevel=0.008)
    k.box((0.624, 0.08, 0.05), at=(0, -0.01, 1.13), m=frame, bevel=0.008)
    arch = [(0.28 * math.cos(math.radians(a)), -0.02, cz + 0.28 * math.sin(math.radians(a)))
            for a in range(0, 181, 10)]
    k.tube(arch, 0.032, frame, curved=True)
    k.box((0.09, 0.1, 0.12), at=(0, -0.025, cz + 0.30), m=frame, bevel=0.012)

    # Fanlight glass (lower half hidden behind transom and door) and radial glazing bars
    k.cyl(rad, 0.01, at=(0, 0.01, cz), rot=(90, 0, 0), m=glass, bevel=0.002)
    k.cyl(0.06, 0.02, at=(0, -0.005, cz), rot=(90, 0, 0), m=frame, bevel=0.003)
    for a in (30, 60, 90, 120, 150):
        t = math.radians(a)
        k.tube([(0.06 * math.cos(t), -0.005, cz + 0.06 * math.sin(t)),
                (0.265 * math.cos(t), -0.005, cz + 0.265 * math.sin(t))], 0.011, frame)

    # Brass knocker on the center stile: backplate, pivot pin, hanging ring
    k.cyl(0.035, 0.015, at=(0, -0.032, 0.86), rot=(90, 0, 0), m=brass, bevel=0.004)
    k.cyl(0.01, 0.04, at=(0, -0.045, 0.85), rot=(0, 90, 0), m=brass)
    k.torus(0.055, 0.012, at=(0, -0.05, 0.795), rot=(90, 0, 0), m=brass)

    # Brass knob on the right (opposite the hinges): rose, stem, knob
    k.cyl(0.03, 0.012, at=(0.19, -0.03, 0.62), rot=(90, 0, 0), m=brass, bevel=0.003)
    k.cyl(0.01, 0.04, at=(0.19, -0.05, 0.62), rot=(90, 0, 0), m=brass)
    k.sphere(0.03, at=(0.19, -0.075, 0.62), scale=(1, 0.8, 1), m=brass)

    # Hinge knuckles on the left edge
    for z in (0.3, 0.95):
        k.cyl(0.014, 0.08, at=(-0.252, -0.03, z), m=brass)

    # Two stone steps from the threshold to the pavement
    k.box((0.78, 0.22, 0.08), at=(0, -0.09, 0.12), m=stone, bevel=0.012)
    k.box((0.9, 0.4, 0.08), at=(0, -0.18, 0.04), m=stone, bevel=0.012)

    # Setting: mortar backing wall, raised cream bricks in running bond cut around the frame, stone plinth, pavement
    k.box((4, 0.2, 3), at=(0, 0.12, 1.5), m=k.mat("#cdb48a", "matte"), bevel=0.0, setting=True)
    brick = k.mat("#ecd3a2", "matte")
    bw, bh, gap = 0.13, 0.042, 0.011
    ro = 0.325                   # opening half-width around the frame (frame outer edge ~0.312)

    def half_open(z):
        hw = 0.0
        if z <= cz:
            hw = ro
        elif z - cz < ro:
            hw = math.sqrt(ro * ro - (z - cz) ** 2)
        if z < cz + 0.375:
            hw = max(hw, 0.058)  # keystone
        return hw

    row = 0
    z = 0.12 + gap
    while z + bh < 2.0:
        hw = max(half_open(z + bh * f) for f in (0.0, 0.25, 0.5, 0.75, 1.0))
        off = 0 if row % 2 == 0 else (bw + gap) / 2
        x = -1.4 + off
        while x < 1.4:
            a, b = x - bw / 2, x + bw / 2
            pieces = [(a, b)]
            if hw > 0 and b > -hw and a < hw:
                pieces = [(a, -hw), (hw, b)]
            for pa, pb in pieces:
                if pb - pa > 0.025:
                    k.box((pb - pa, 0.02, bh), at=((pa + pb) / 2, 0.02, z + bh / 2), m=brick, bevel=0.005,
                          setting=True)
            x += bw + gap
        z += bh + gap
        row += 1
    k.box((4, 0.26, 0.12), at=(0, 0.1, 0.06), m=stone, bevel=0.01, setting=True)
    k.floor("#b9b2a8", "matte")
