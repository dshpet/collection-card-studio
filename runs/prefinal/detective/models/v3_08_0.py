# Neon sign: a round grey metal drum hangs on two short rods from a steel arm. The arm and a diagonal brace
# come off a wall plate bolted to the brick wall. Each round face has a dark panel with a glowing orange
# neon rim and magnifier (ring lens and handle). The wall runs off the card to the left. The framing holds the sign.
SCENE = {"category": "4", "backdrop": "#1f3fa8", "azimuth": 32, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    metal = k.mat("#8e959e", "metal")
    dark = k.mat("#3a3f48", "satin")
    neon = k.mat("#ff8a1f", "glow")
    bolt = k.mat("#5d636c", "metal")

    wx = -0.45  # brick wall face
    cx, cz, R = 0.12, 1.5, 0.38

    # Sign drum: axis along y, faces toward -y and +y
    k.cyl(R, 0.14, at=(cx, 0, cz), rot=(90, 0, 0), m=metal, bevel=0.02)
    for s in (-1, 1):
        y = s * 0.072
        k.cyl(R - 0.04, 0.008, at=(cx, y, cz), rot=(90, 0, 0), m=dark, bevel=0.002)
        yn = s * 0.09
        k.torus(R - 0.065, 0.016, at=(cx, yn, cz), rot=(90, 0, 0), m=neon)
        lx, lz = cx - 0.05 * s, cz + 0.05
        k.torus(0.13, 0.02, at=(lx, yn, lz), rot=(90, 0, 0), m=neon)
        d = 0.7071
        k.tube([(lx + s * 0.15 * d, yn, lz - 0.15 * d), (lx + s * 0.33 * d, yn, lz - 0.33 * d)], 0.026, neon)
        # standoffs holding the neon off the panel
        for px, pz in ((lx, lz + 0.13), (lx + s * 0.24 * d, lz - 0.24 * d), (cx, cz - R + 0.065)):
            k.cyl(0.008, 0.02, at=(px, s * 0.081, pz), rot=(90, 0, 0), m=bolt)

    # Bracket: wall plate, arm, diagonal brace, hanger rods
    k.box((0.03, 0.12, 0.42), at=(wx + 0.015, 0, 1.86), m=metal, bevel=0.006)
    for z in (1.7, 2.02):
        for y in (-0.035, 0.035):
            k.cyl(0.014, 0.02, at=(wx + 0.04, y, z), rot=(0, 90, 0), m=bolt, verts=6)
    arm_z = 2.0
    k.tube([(wx + 0.03, 0, arm_z), (cx + 0.3, 0, arm_z)], 0.022, metal)
    k.sphere(0.03, at=(cx + 0.3, 0, arm_z), m=metal)
    k.tube([(wx + 0.03, 0, 1.68), (cx - 0.12, 0, arm_z)], 0.018, metal)
    for hx in (cx - 0.2, cx + 0.2):
        top_sign = cz + (R * R - (hx - cx) ** 2) ** 0.5
        k.tube([(hx, 0, arm_z), (hx, 0, top_sign - 0.01)], 0.012, metal)
        k.torus(0.025, 0.008, at=(hx, 0, arm_z), rot=(90, 0, 0), m=metal)

    # Brick wall (setting): mortar slab with raised bricks on its face
    k.box((0.2, 6, 4), at=(wx - 0.1, 1.2, 1.6), m=k.mat("#b9a48e", "matte"), bevel=0, setting=True)
    bricks = (k.mat("#a8452e", "matte"), k.mat("#8f3a26", "matte"))
    bh, bl, gap = 0.1, 0.26, 0.022
    for row in range(32):
        z = -0.3 + row * (bh + gap)
        off = (bl + gap) / 2 if row % 2 else 0
        for col in range(22):
            y = -1.6 + col * (bl + gap) + off
            k.box((0.03, bl, bh), at=(wx - 0.005, y, z), m=bricks[(row * 3 + col) % 5 == 0],
                  bevel=0.008, setting=True)
