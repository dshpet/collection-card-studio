# Control panel: a boxy grey metal console on a dark plinth. Its top slopes up from front to back. On the slope,
# from front to back: a row of six red push buttons, two round dial knobs with raised pointers, and one wide flat
# screen set in a bezel. It stands on a plain ledge.
import math

SCENE = {"category": "2", "backdrop": "#5cc2f2", "azimuth": 30, "elevation": 14, "lens": 60, "light": "left"}

SLOPE = math.degrees(math.atan2(0.3, 0.6))  # top rises 0.3 over the 0.6 depth
CA, SA = math.cos(math.radians(SLOPE)), math.sin(math.radians(SLOPE))


def on_slope(x, s, h):
    """Point at width x, distance s up the slope from its front edge, h out along the slope's normal."""
    return (x, -0.3 + CA * s - SA * h, 0.56 + SA * s + CA * h)


def build(k):
    body = k.mat("#9aa3ad", "metal")
    trim = k.mat("#4a5059", "satin")
    screen = k.mat("#16222e", "gloss")
    red = k.mat("#e3342f", "gloss")
    knob = k.mat("#d4d9df", "metal")
    tilt = (SLOPE, 0, 0)

    # Plinth and body. The body box's top face is warped down toward the front into the slope.
    k.box((1.04, 0.64, 0.06), at=(0, 0, 0.03), m=trim, bevel=0.012)
    shell = k.box((1.0, 0.6, 0.8), at=(0, 0, 0.46), m=body, bevel=0.03)

    def slope_top(p):
        x, y, z = p
        if z > 0:
            z -= 0.3 * (0.3 - y) / 0.6 * (z / 0.4)
        return (x, y, z)

    k.warp(shell, slope_top)

    # Six red buttons in a row near the front of the slope, each in a dark collar.
    for i in range(6):
        x = -0.375 + i * 0.15
        k.cyl(0.045, 0.016, at=on_slope(x, 0.1, 0.006), rot=tilt, m=trim, bevel=0.004)
        k.cyl(0.033, 0.04, at=on_slope(x, 0.1, 0.02), rot=tilt, m=red, bevel=0.01)

    # Two round dials with a raised pointer ridge.
    for x, turn in ((-0.22, 35), (0.22, -50)):
        k.cyl(0.075, 0.014, at=on_slope(x, 0.27, 0.005), rot=tilt, m=trim, bevel=0.004)
        k.cyl(0.06, 0.045, at=on_slope(x, 0.27, 0.03), rot=tilt, m=knob, bevel=0.01)
        a = math.radians(turn)
        dx, ds = 0.03 * math.sin(a), 0.03 * math.cos(a)
        k.box((0.016, 0.06, 0.016), at=on_slope(x + dx, 0.27 + ds, 0.058), rot=(SLOPE, 0, -turn), m=trim,
              bevel=0.005)

    # One wide flat screen in a bezel on the upper slope.
    k.box((0.76, 0.24, 0.03), at=on_slope(0, 0.51, 0.005), rot=tilt, m=trim, bevel=0.01)
    k.box((0.68, 0.18, 0.02), at=on_slope(0, 0.51, 0.018), rot=tilt, m=screen, bevel=0.004)

    # Plain ledge.
    k.box((4, 2, 0.12), at=(0, 0.4, -0.06), m=k.mat("#d8eef8", "satin"), bevel=0.01, setting=True)
