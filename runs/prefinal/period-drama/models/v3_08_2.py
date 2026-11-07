# Steamer trunk: a tall wooden box with two darker wooden bands, closed by a lid with a gently rounded (barrel)
# top that sits on a flat lid rim. Brass guards cap the eight body corners and the four lid-rim corners, and brass
# strips curve over the lid near each end. A brass hasp hangs from the lid onto a lock plate on the front, clear
# of the bands. Each end has a leather strap handle held by two brass brackets. The trunk stands on a wooden
# station platform of warm brown planks that runs off the card.
import math

SCENE = {"category": "3", "backdrop": "#5cc4f2", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    wood = k.mat("#7a4220", "matte")
    band = k.mat("#4e2a14", "matte")
    brass = k.mat("#e0a93a", "metal")
    leather = k.mat("#3e2212", "matte")

    W, D, H = 1.0, 0.55, 0.6
    RIM = 0.07
    FLAT = 0.3  # dome height as a fraction of its half-depth: a low, gentle curve
    # Body and wooden bands (kept below the latch plate)
    k.box((W, D, H), at=(0, 0, H / 2), m=wood, bevel=0.015)
    for z in (0.15, 0.38):
        k.box((W + 0.012, D + 0.012, 0.05), at=(0, 0, z), m=band, bevel=0.008)

    # Lid: flat rim on the body, then the rounded top (cylinder along x, flattened vertically), its centre at the
    # rim top so only the upper half shows; a little shorter than the rim so its ends never sit flush.
    k.box((W + 0.02, D + 0.02, RIM), at=(0, 0, H + RIM / 2), m=band, bevel=0.012)
    zc = H + RIM
    dome = k.cyl(D / 2, W - 0.01, at=(0, 0, zc), rot=(0, 90, 0), m=wood, bevel=0.012)
    k.warp(dome, lambda p: (p[0] * FLAT, p[1], p[2]))  # local x maps to world z under rot (0, 90, 0)

    # Brass strips over the lid near each end, following the dome
    for x in (-0.44, 0.44):
        pts = []
        for i in range(13):
            a = math.radians(180 * i / 12)
            r = D / 2 + 0.008
            pts.append((x, -r * math.cos(a), zc + (D / 2 * FLAT + 0.008) * math.sin(a)))
        k.tube(pts, 0.016, brass, curved=True)

    # Brass corner guards on the body and on the lid rim
    g = 0.11
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z in (g / 2 - 0.005, H - g / 2 + 0.005):
                k.box((g, g, g), at=(sx * (W / 2 - g / 2 + 0.008), sy * (D / 2 - g / 2 + 0.008), z),
                      m=brass, bevel=0.015)
            k.box((g, g, 0.08), at=(sx * (W / 2 - g / 2 + 0.012), sy * (D / 2 - g / 2 + 0.012), H + RIM / 2),
                  m=brass, bevel=0.015)

    # Front latch: lock plate on the body, hasp hanging from the lid over it, keyhole knob
    k.box((0.14, 0.02, 0.12), at=(0, -D / 2 - 0.01, H - 0.07), m=brass, bevel=0.01)
    k.box((0.07, 0.03, 0.13), at=(0, -D / 2 - 0.03, H - 0.01), m=brass, bevel=0.012)
    k.cyl(0.018, 0.02, at=(0, -D / 2 - 0.05, H - 0.05), rot=(90, 0, 0), m=k.mat("#2a180a", "satin"))

    # End handles: leather strap sagging between two brass brackets on each end
    hz = 0.47
    for sx in (-1, 1):
        x0 = sx * (W / 2 + 0.008)
        for y in (-0.1, 0.1):
            k.box((0.03, 0.06, 0.07), at=(x0 + sx * 0.012, y, hz), m=brass, bevel=0.008)
        k.tube([(x0 + sx * 0.03, -0.1, hz), (x0 + sx * 0.05, -0.06, hz - 0.035), (x0 + sx * 0.055, 0, hz - 0.045),
                (x0 + sx * 0.05, 0.06, hz - 0.035), (x0 + sx * 0.03, 0.1, hz)], 0.02, leather, curved=True)

    # Wooden station platform: warm brown planks running across the view, top at z = 0
    plank_cols = ("#a8743f", "#9a6836", "#b47f48")
    for i in range(24):
        y = -3.0 + i * 0.26
        k.box((8, 0.245, 0.08), at=(0, y, -0.04), m=k.mat(plank_cols[i % 3], "matte"),
              bevel=0.01, setting=True)
