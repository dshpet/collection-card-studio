# Control panel: a dark gray desk console whose top slopes down toward the front. A row of five red buttons
# runs across the front of the slope; behind them a small round screen in a bezel sits on the left, and two
# levers on the right pivot in slotted bases set into the slope. The console stands on four short feet on a
# plain metal ledge.
import math

SCENE = {"category": "2", "backdrop": "#ffc62e", "azimuth": 30, "elevation": 16, "lens": 60, "light": "left"}

W, D = 0.9, 0.56            # console width (x) and depth (y)
FEET = 0.035                # height of the feet
LOW, HIGH = 0.40, 0.80      # top height at the front and back edges of the slope
SLOPE = math.degrees(math.atan((HIGH - LOW) / D))


def top(y):
    """Height of the sloped top at depth y."""
    return LOW + (y + D / 2) * (HIGH - LOW) / D


def on_slope(x, y, d):
    """Point d above the sloped top at (x, y), measured along its normal."""
    a = math.radians(SLOPE)
    return (x, y - d * math.sin(a), top(y) + d * math.cos(a))


def build(k):
    body = k.mat("#3e434b", "satin")
    trim = k.mat("#2a2d33", "satin")
    steel = k.mat("#b9bfc8", "metal")
    red = k.mat("#e2262b", "gloss")
    screen = k.mat("#4fb8ec", "gloss")
    knob = k.mat("#22252a", "gloss")
    tilt = (SLOPE, 0, 0)

    # Console body: a box whose top is warped into the slope (front low, back high).
    h = HIGH
    shell = k.box((W, D, h), at=(0, 0, FEET + h / 2), m=body, bevel=0.03)

    def slope_top(p):
        x, y, z = p
        if z > 0:
            z -= (HIGH - top(y))
        return (x, y, z)

    k.warp(shell, slope_top)
    # Darker kick strip at the base and four feet on the ledge.
    k.box((W - 0.04, 0.02, 0.07), at=(0, -D / 2 - 0.004, FEET + 0.045), m=trim, bevel=0.008)
    for x in (-W / 2 + 0.08, W / 2 - 0.08):
        for y in (-D / 2 + 0.08, D / 2 - 0.08):
            k.cyl(0.045, FEET, at=(x, y, FEET / 2), m=trim, bevel=0.006)

    # Row of five red buttons across the front of the slope, each in a steel collar.
    for i in range(5):
        x = -0.32 + i * 0.16
        k.cyl(0.058, 0.02, at=on_slope(x, -0.17, FEET + 0.01), rot=tilt, m=steel, bevel=0.005)
        k.cyl(0.045, 0.04, at=on_slope(x, -0.17, FEET + 0.03), rot=tilt, m=red, bevel=0.012)

    # Small round screen in a raised bezel, upper left of the slope.
    k.cyl(0.135, 0.03, at=on_slope(-0.2, 0.09, FEET + 0.015), rot=tilt, m=trim, bevel=0.01)
    k.cyl(0.105, 0.012, at=on_slope(-0.2, 0.09, FEET + 0.032), rot=tilt, m=screen, bevel=0.004)

    # Two levers, upper right: a slotted base on the slope, a steel stick from the pivot, a round knob.
    a = math.radians(SLOPE)
    for x, lean in ((0.13, 25), (0.32, -15)):
        base = on_slope(x, 0.09, FEET + 0.02)
        k.box((0.09, 0.2, 0.04), at=base, rot=tilt, m=trim, bevel=0.01)
        k.box((0.025, 0.15, 0.02), at=on_slope(x, 0.09, FEET + 0.035), rot=tilt, m=k.mat("#15171a", "matte"),
              bevel=0.003)
        pivot = on_slope(x, 0.09, FEET + 0.035)
        k.cyl(0.03, 0.08, at=pivot, rot=(SLOPE, 90, 0), m=steel, bevel=0.005)
        # Stick leans forward/back within the slot, measured from the slope normal.
        t = a + math.radians(lean)
        length = 0.2
        tip = (x, pivot[1] - length * math.sin(t), pivot[2] + length * math.cos(t))
        k.tube([pivot, tip], 0.016, steel)
        k.sphere(0.042, at=tip, m=knob)

    # Plain metal ledge, top at z = 0, running off the card.
    k.box((4, 1.6, 0.12), at=(0, 0.3, -0.06), m=k.mat("#a7adb6", "metal"), bevel=0.01, setting=True)
