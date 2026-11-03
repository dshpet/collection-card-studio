# Control panel: a light gray cabinet stands on the floor on a darker plinth; its top slopes up toward the back.
# On the slope sit two rows of red and yellow round buttons at the front, a large white dial and a small green
# dial above them, and on the right a lever whose stick turns on a pivot in a slotted housing and ends in a red
# ball knob. The cabinet stands on a floor of white metal plates.
import math

SCENE = {"category": "3", "backdrop": "#f28a1e", "azimuth": 28, "elevation": 14, "lens": 60, "light": "left"}

W, D = 1.0, 0.56
FRONT, BACK = 0.5, 0.82
A = math.degrees(math.atan2(BACK - FRONT, D))
CA, SA = math.cos(math.radians(A)), math.sin(math.radians(A))


def on_slope(x, s, lift=0.0):
    # s runs up the slope from its front edge; lift moves out along the slope's normal
    return (x, -D / 2 + s * CA - lift * SA, FRONT + s * SA + lift * CA)


def build(k):
    gray = k.mat("#c9ccd1", "satin")
    dark = k.mat("#7d838c", "satin")
    trim = k.mat("#4a4f57", "satin")
    red = k.mat("#e8262b", "satin")
    yellow = k.mat("#ffd23a", "satin")
    white = k.mat("#f7f7f2", "satin")
    green = k.mat("#3fc24a", "satin")
    steel = k.mat("#b8bec6", "metal")

    # cabinet: a box whose top corners are lifted to the slope
    body = k.box((W, D, 1.0), at=(0, 0, 0.5), m=gray, bevel=0.02)
    k.warp(body, lambda p: (p[0], p[1], p[2] if p[2] < 0 else FRONT + (p[1] + D / 2) / D * (BACK - FRONT) - 0.5))
    k.box((W - 0.06, D - 0.06, 0.06), at=(0, 0, 0.03), m=dark, bevel=0.01)
    # raised front door panel with a handle bar
    k.box((W - 0.2, 0.02, 0.3), at=(0, -D / 2 - 0.008, 0.27), m=gray, bevel=0.008)
    k.box((0.2, 0.03, 0.03), at=(0, -D / 2 - 0.03, 0.36), m=trim, bevel=0.008)
    # cap rail along the high back edge
    k.box((W + 0.02, 0.08, 0.05), at=(0, D / 2 - 0.04, BACK + 0.01), m=dark, bevel=0.01)
    # control plate lying on the slope
    k.box((W - 0.08, 0.56, 0.02), at=on_slope(0, 0.33, 0.005), rot=(A, 0, 0), m=dark, bevel=0.006)

    # two rows of round buttons in collars
    for row, s in enumerate((0.1, 0.22)):
        for i in range(4):
            x = -0.36 + i * 0.13
            m = red if (i + row) % 2 == 0 else yellow
            k.cyl(0.05, 0.02, at=on_slope(x, s, 0.02), rot=(A, 0, 0), m=trim, bevel=0.004)
            k.cyl(0.038, 0.04, at=on_slope(x, s, 0.045), rot=(A, 0, 0), m=m, bevel=0.012)

    # large white dial and small green dial, each with a bezel, a needle and a hub
    for x, s, r, face in ((-0.24, 0.43, 0.11, white), (0.03, 0.43, 0.075, green)):
        k.cyl(r + 0.02, 0.04, at=on_slope(x, s, 0.03), rot=(A, 0, 0), m=trim, bevel=0.01)
        k.cyl(r, 0.012, at=on_slope(x, s, 0.052), rot=(A, 0, 0), m=face, bevel=0.003)
        k.box((0.016, r * 0.85, 0.008), at=on_slope(x + r * 0.25, s + r * 0.3, 0.06), rot=(A, 0, -35), m=red,
              bevel=0.003)
        k.cyl(0.016, 0.02, at=on_slope(x, s, 0.064), rot=(A, 0, 0), m=trim, bevel=0.004)

    # lever: a slotted housing on the slope, the stick turns on a pivot in the slot and ends in a ball knob
    lx, ls = 0.33, 0.3
    k.box((0.14, 0.3, 0.06), at=on_slope(lx, ls, 0.04), rot=(A, 0, 0), m=trim, bevel=0.012)
    k.box((0.03, 0.22, 0.02), at=on_slope(lx, ls, 0.072), rot=(A, 0, 0), m=k.mat("#2b2e33", "matte"), bevel=0.004)
    base = on_slope(lx, ls - 0.04, 0.07)
    tip = (lx, base[1] - 0.06, base[2] + 0.26)
    k.cyl(0.03, 0.05, at=base, rot=(0, 90, 0), m=steel)
    k.tube([base, tip], 0.018, steel)
    k.sphere(0.055, at=tip, m=red)

    # white metal floor plates, tops at z = 0
    plate = k.mat("#eef1f4", "metal")
    for i in range(-5, 6):
        for j in range(-5, 6):
            k.box((0.78, 0.78, 0.05), at=(i * 0.8, j * 0.8, -0.025), m=plate, bevel=0.012, setting=True)
