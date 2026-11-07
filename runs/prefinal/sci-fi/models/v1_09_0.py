# Control panel: a grey console box whose top slopes up toward the back, with a raised upper housing at the
# back. The slanted face carries an inset plate with two toggle switches and a big red push button in the front
# row and three round dials behind them. The square screen sits in the upper housing's front face. The console
# stands on its plinth on a steel lab bench whose front edge crosses the bottom of the card.
import math

SCENE = {"category": "3", "backdrop": "#3d8fe0", "azimuth": 28, "elevation": 15, "lens": 60, "light": "left"}

W, D = 1.0, 0.55            # console width (x) and depth (y)
ZF, ZB = 0.37, 0.62         # height of the slanted top at the front and at the back
A = math.degrees(math.atan2(ZB - ZF, D))
N = (0.0, -math.sin(math.radians(A)), math.cos(math.radians(A)))


def on_slope(x, t, h):
    """Point at width x, fraction t (0 front .. 1 back) along the slope, lifted h along its normal."""
    return (x, -D / 2 + D * t + N[1] * h, ZF + (ZB - ZF) * t + N[2] * h)


def build(k):
    grey = k.mat("#8e959e", "satin")
    dark = k.mat("#5c636c", "satin")
    silver = k.mat("#cfd4da", "metal")
    red = k.mat("#e3262b", "gloss")
    face = k.mat("#f2f0e8", "satin")
    needle = k.mat("#d0302a", "satin")
    screen = k.mat("#3ee08a", "glow")

    # Body with the sloped top: a box whose front top edge is pulled down.
    body = k.box((W, D, ZB - 0.04), at=(0, 0, 0.04 + (ZB - 0.04) / 2), m=grey, bevel=0.03)
    k.warp(body, lambda p: (p[0], p[1], p[2] - (ZB - ZF) * (0.5 - p[1] / D) if p[2] > 0 else p[2]))
    # Plinth it stands on.
    k.box((W - 0.06, D - 0.06, 0.05), at=(0, 0, 0.025), m=dark, bevel=0.01)

    # Upper housing at the back with the screen.
    hy0, hy1 = 0.13, D / 2
    k.box((W, hy1 - hy0, 0.46), at=(0, (hy0 + hy1) / 2, 0.76), m=grey, bevel=0.03)
    k.box((0.38, 0.03, 0.34), at=(0, hy0 - 0.01, 0.78), m=silver, bevel=0.012)
    k.box((0.30, 0.02, 0.27), at=(0, hy0 - 0.022, 0.78), m=screen, bevel=0.006)

    # Inset plate on the slope, in front of the housing.
    t_end = (hy0 + D / 2) / D
    plen = t_end * math.hypot(D, ZB - ZF)
    k.box((W - 0.08, plen - 0.04, 0.016), at=on_slope(0, t_end / 2, 0.004), rot=(A, 0, 0), m=dark, bevel=0.005)

    # Big red push button with a silver collar.
    k.cyl(0.105, 0.03, at=on_slope(0.24, 0.25, 0.025), rot=(A, 0, 0), m=silver, bevel=0.008)
    dome = [(0.085, 0), (0.085, 0.03)] + [
        (0.085 * math.cos(math.radians(a)), 0.03 + 0.045 * math.sin(math.radians(a))) for a in range(10, 91, 10)]
    dome[-1] = (0, dome[-1][1])
    k.lathe(dome, at=on_slope(0.24, 0.25, 0.038), rot=(A, 0, 0), m=red)

    # Two toggle switches: base plate, pivot boss, lever tilted forward with a ball tip.
    for x in (-0.34, -0.14):
        k.box((0.09, 0.12, 0.02), at=on_slope(x, 0.25, 0.018), rot=(A, 0, 0), m=silver, bevel=0.005)
        k.cyl(0.026, 0.03, at=on_slope(x, 0.25, 0.04), rot=(A, 0, 0), m=silver)
        base = on_slope(x, 0.25, 0.05)
        tip = on_slope(x, 0.18, 0.15)
        k.tube([base, tip], 0.014, silver)
        k.sphere(0.024, at=tip, m=dark)

    # Three round dials: silver bezel, light face, red needle.
    for x in (-0.3, 0.0, 0.3):
        k.cyl(0.085, 0.02, at=on_slope(x, 0.6, 0.018), rot=(A, 0, 0), m=silver, bevel=0.006)
        k.torus(0.078, 0.012, at=on_slope(x, 0.6, 0.03), rot=(A, 0, 0), m=silver)
        k.cyl(0.068, 0.012, at=on_slope(x, 0.6, 0.026), rot=(A, 0, 0), m=face, bevel=0.003)
        k.box((0.012, 0.06, 0.008), at=on_slope(x + 0.012, 0.64, 0.036), rot=(A, 0, -25), m=needle, bevel=0.002)
        k.cyl(0.012, 0.016, at=on_slope(x, 0.6, 0.036), rot=(A, 0, 0), m=dark)

    # Steel lab bench: top slab, front edge lip and the cabinet front below it.
    k.box((5, 1.6, 0.08), at=(0, 0.25, -0.04), m=k.mat("#b9c1ca", "metal"), bevel=0.012, setting=True)
    k.box((5, 0.04, 0.1), at=(0, -0.56, -0.03), m=k.mat("#a3acb6", "metal"), bevel=0.01, setting=True)
    k.box((5, 0.05, 0.8), at=(0, -0.5, -0.48), m=k.mat("#7f8893", "metal"), bevel=0.01, setting=True)
