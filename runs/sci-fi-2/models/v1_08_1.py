# Time machine pod: a round silver shell stands on three short legs whose feet rest on a low lab platform.
# A curved teal glass door bulges from the front face inside a silver frame, hinged on its right side.
# A ring of small orange lights runs around the lower body band, below the door frame. The lab is a dark
# floor, the round platform with a glowing rim, and a purple back wall far behind.
import math

SCENE = {"category": "4", "backdrop": "#7a4fd6", "azimuth": 25, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    silver = k.mat("#c9ced6", "metal")
    dark = k.mat("#5a6070", "metal")
    glass = k.mat("#2fc4c0", "glass")
    light = k.mat("#ff8a1f", "glow")

    # Body shell: a sphere of radius 0.4 centered at z0, as a lathe.
    z0, R = 0.62, 0.4
    prof = []
    for i in range(97):
        a = math.pi * i / 96  # 0 at the bottom, pi at the top
        prof.append((R * math.sin(a), -R * math.cos(a)))
    k.lathe(prof, at=(0, 0, z0), rot=(0, 0, 0), m=silver, verts=96)
    k.cyl(0.07, 0.04, at=(0, 0, z0 + R), rot=(0, 0, 0), m=dark, bevel=0.01)

    # Curved glass door: a spherical cap facing -y, slightly proud of the shell.
    Rg, half = 0.415, math.radians(31)
    cap = []
    for i in range(49):
        a = half * (1 - i / 48)
        cap.append((Rg * math.sin(a), Rg * math.cos(a)))
    k.lathe(cap, at=(0, 0, z0), rot=(90, 0, 0), m=glass, verts=96)
    rim_r, rim_y = Rg * math.sin(half), -Rg * math.cos(half)
    k.torus(rim_r, 0.026, at=(0, rim_y, z0), rot=(90, 0, 0), m=silver)
    # Hinges on the right edge, a handle on the left edge.
    for dz in (-0.1, 0.1):
        k.cyl(0.022, 0.07, at=(rim_r + 0.01, rim_y - 0.01, z0 + dz), rot=(0, 0, 0), m=dark)
    k.sphere(0.028, at=(-rim_r + 0.02, rim_y - 0.035, z0), m=dark)

    # Ring of lights around the lower band of the frame, clear below the door frame.
    dzb = 0.3
    zb = z0 - dzb
    rb = math.sqrt(R * R - dzb * dzb)
    k.torus(rb + 0.005, 0.033, at=(0, 0, zb), rot=(0, 0, 0), m=dark)
    for i in range(14):
        a = 2 * math.pi * i / 14
        k.sphere(0.024, at=((rb + 0.033) * math.cos(a), (rb + 0.033) * math.sin(a), zb), m=light)

    # Three short legs from the underside, below the light ring, to round feet on the platform.
    for deg in (90, 210, 330):
        a = math.radians(deg)
        c, s = math.cos(a), math.sin(a)
        k.tube([(0.14 * c, 0.14 * s, 0.27), (0.26 * c, 0.26 * s, 0.15), (0.36 * c, 0.36 * s, 0.05)], 0.032, silver)
        k.cyl(0.065, 0.04, at=(0.36 * c, 0.36 * s, 0.02), rot=(0, 0, 0), m=dark, bevel=0.01)

    # Lab setting: low round platform with a glowing rim, dark floor, purple back wall.
    k.cyl(0.8, 0.1, at=(0, 0, -0.05), rot=(0, 0, 0), m=k.mat("#4b4f6b", "satin"), bevel=0.02, setting=True)
    k.torus(0.8, 0.02, at=(0, 0, -0.03), rot=(0, 0, 0), m=k.mat("#3fe0e6", "glow"), setting=True)
    k.floor("#2e2650", finish="gloss", z=-0.1)
    k.box((12, 0.3, 6), at=(0, 3.5, 2.9), rot=(0, 0, 0), m=k.mat("#6a46c4", "satin"), bevel=0.02, setting=True)
