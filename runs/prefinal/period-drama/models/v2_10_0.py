# Front door: a burgundy six-panel door hangs on three brass hinges on its left edge, in a cream stone surround
# set against the wall. A transom bar caps it and a half-round fanlight with radial glazing bars sits in the arch
# above. The brass knocker ring hangs from a pivot on a backplate on the center stile; the brass knob is on the
# right lock rail. Two stone steps lead up to the threshold from the pavement.
import math

SCENE = {"category": "4", "backdrop": "#5fd3f0", "azimuth": 20, "elevation": 8, "lens": 60, "light": "left"}


def build(k):
    paint = k.mat("#7d1426", "satin")
    brass = k.mat("#d4a537", "metal")
    stone = k.mat("#efe3c6", "matte")
    step_stone = k.mat("#d8cdb4", "matte")
    glass = k.mat("#9fdcef", "glass")

    z0, w, h = 0.16, 0.42, 0.90
    # door slab and raised panels
    k.box((w, 0.04, h), at=(0, -0.035, z0 + h / 2), m=paint, bevel=0.006)
    for zb, zt in ((0.07, 0.29), (0.37, 0.65), (0.71, 0.83)):
        for x in (-0.09, 0.09):
            k.box((0.12, 0.015, zt - zb - 0.01), at=(x, -0.06, z0 + (zb + zt) / 2), m=paint, bevel=0.006)
    # hinges on the left edge
    for rz in (0.12, 0.45, 0.78):
        k.cyl(0.014, 0.08, at=(-w / 2 + 0.004, -0.058, z0 + rz), m=brass)
    # knocker: backplate, pivot, ring
    kz = z0 + 0.68
    k.cyl(0.028, 0.012, at=(0, -0.061, kz + 0.02), rot=(90, 0, 0), m=brass)
    k.cyl(0.011, 0.05, at=(0, -0.074, kz + 0.02), rot=(0, 90, 0), m=brass)
    k.torus(0.045, 0.011, at=(0, -0.076, kz - 0.025), rot=(90, 0, 0), m=brass)
    # knob on the lock side
    hz = z0 + 0.33
    k.cyl(0.024, 0.01, at=(0.165, -0.06, hz), rot=(90, 0, 0), m=brass)
    k.cyl(0.009, 0.04, at=(0.165, -0.08, hz), rot=(90, 0, 0), m=brass)
    k.sphere(0.026, at=(0.165, -0.105, hz), scale=(1, 0.8, 1), m=brass)

    # transom bar and fanlight
    top = z0 + h
    cz = top + 0.03
    k.box((w + 0.04, 0.05, 0.035), at=(0, -0.03, top + 0.0175), m=paint, bevel=0.005)
    k.cyl(0.215, 0.01, at=(0, -0.007, cz), rot=(90, 0, 0), m=glass, bevel=0.002)
    arc = [(0.21 * math.cos(math.radians(a)), -0.02, cz + 0.21 * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    k.tube(arc, 0.018, paint, curved=True)
    hub = [(0.06 * math.cos(math.radians(a)), -0.02, cz + 0.06 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    k.tube(hub, 0.013, paint, curved=True)
    for a in (36, 72, 108, 144):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        k.tube([(0.06 * c, -0.02, cz + 0.06 * s), (0.205 * c, -0.02, cz + 0.205 * s)], 0.012, paint)

    # stone surround: pilasters, arch, keystone
    for x in (-0.25, 0.25):
        k.box((0.07, 0.06, cz - z0), at=(x, -0.025, (z0 + cz) / 2), m=stone, bevel=0.008)
        k.box((0.09, 0.07, 0.03), at=(x, -0.03, cz - 0.015), m=stone, bevel=0.006)
    ring = [(0.25 * math.cos(math.radians(a)), -0.025, cz + 0.25 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
    k.tube(ring, 0.035, stone, curved=True)
    k.box((0.07, 0.07, 0.09), at=(0, -0.03, cz + 0.255), m=stone, bevel=0.008)

    # two stone steps
    k.box((0.86, 0.40, 0.08), at=(0, -0.20, 0.04), m=step_stone, bevel=0.012)
    k.box((0.68, 0.22, 0.08), at=(0, -0.11, 0.12), m=step_stone, bevel=0.012)

    # setting: cream wall and pavement
    k.box((6, 0.4, 4), at=(0, 0.2, 2), m=k.mat("#f2e6c8", "matte"), bevel=0, setting=True)
    k.box((6, 0.06, 0.12), at=(0, -0.03, 0.06), m=k.mat("#cfc3a8", "matte"), bevel=0.01, setting=True)
    k.floor("#c9c2b4", "matte")
