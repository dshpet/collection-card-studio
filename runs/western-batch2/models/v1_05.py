# Saloon doors: two half-height louvred doors hang on barrel hinges from the inner faces of the posts of a
# wooden door frame (red trim strips on the posts and header) set into a horizontal-board front wall with a
# solid backing. Each door is a frame of stiles and rails holding tilted slats; both swing a little inward.
# Gaps above and below the doors show the dim interior. A plank boardwalk runs in front of the wall.
import math

SCENE = {"category": "4", "backdrop": "#5cc2f2", "azimuth": 18, "elevation": 9, "lens": 55, "light": "left"}


def build(k):
    wood = k.mat("#8a5129", "matte")
    door_wood = k.mat("#a8652f", "matte")
    slat_wood = k.mat("#b8743a", "matte")
    red = k.mat("#c8352b", "satin")
    iron = k.mat("#3d3a38", "metal")

    # Door frame: two posts and a header, with red trim on the front faces.
    post_x, post_w, frame_h = 0.5, 0.1, 1.72
    for s in (-1, 1):
        x = s * post_x
        k.box((post_w, 0.14, frame_h), at=(x, 0, frame_h / 2), m=wood, bevel=0.01)
        k.box((0.035, 0.02, frame_h - 0.02), at=(x + s * 0.02, -0.075, frame_h / 2), m=red, bevel=0.004)
    k.box((2 * post_x + post_w + 0.08, 0.16, 0.12), at=(0, 0, frame_h + 0.06), m=wood, bevel=0.012)
    k.box((2 * post_x + post_w + 0.04, 0.02, 0.04), at=(0, -0.085, frame_h + 0.06), m=red, bevel=0.004)

    # Doors: hinged on the inner faces of the posts, swung 12 degrees inward (toward +y).
    inner = post_x - post_w / 2
    width, z0, z1 = 0.435, 0.42, 1.12
    height, zc = z1 - z0, (z0 + z1) / 2
    a = math.radians(12)
    for s in (-1, 1):
        hx = s * (inner - 0.02)
        rz = -s * 12

        def put(size, u, z, m, tilt=0.0, bevel=0.006):
            k.box(size, at=(hx - s * u * math.cos(a), u * math.sin(a), z), rot=(tilt, 0, rz), m=m, bevel=bevel)

        stile = 0.055
        put((stile, 0.045, height), stile / 2, zc, door_wood)
        put((stile, 0.045, height), width - stile / 2, zc, door_wood)
        span = width - 2 * stile
        put((span + 0.01, 0.045, 0.07), width / 2, z1 - 0.035, door_wood)
        put((span + 0.01, 0.045, 0.09), width / 2, z0 + 0.045, door_wood)
        put((span + 0.01, 0.045, 0.05), width / 2, zc - 0.02, door_wood)
        for lo, hi in ((z0 + 0.09, zc - 0.045), (zc + 0.005, z1 - 0.07)):
            n = int((hi - lo) / 0.042)
            step = (hi - lo) / n
            for i in range(n):
                put((span, 0.04, 0.014), width / 2, lo + step * (i + 0.5), slat_wood, tilt=35, bevel=0.003)

        # Barrel hinges: the barrel sits on the door's hinge edge, the leaf is screwed to the post's inner face.
        for z in (z0 + 0.1, z1 - 0.1):
            k.cyl(0.022, 0.1, at=(s * (inner - 0.012), -0.03, z), m=iron, bevel=0.003)
            k.box((0.012, 0.06, 0.08), at=(s * (inner + 0.004), -0.01, z), m=iron, bevel=0.003)

    # Front wall: solid backing around the doorway, with horizontal boards over it.
    back = k.mat("#5a341b", "matte")
    for s in (-1, 1):
        k.box((3.0, 0.04, 3.0), at=(s * (post_x + 1.5), 0.09, 1.5), m=back, bevel=0, setting=True)
    k.box((1.2, 0.04, 1.4), at=(0, 0.09, frame_h + 0.7), m=back, bevel=0, setting=True)
    board = k.mat("#7a4a26", "matte")
    board2 = k.mat("#6d4021", "matte")
    for i in range(18):
        z = 0.08 + i * 0.16
        m = board if i % 2 else board2
        if z > frame_h + 0.1:
            k.box((6.4, 0.08, 0.15), at=(0, 0.03, z), m=m, bevel=0.01, setting=True)
        else:
            for s in (-1, 1):
                k.box((2.7, 0.08, 0.15), at=(s * (post_x + 1.35), 0.03, z), m=m, bevel=0.01, setting=True)

    # Dim interior seen through the gaps above and below the doors.
    k.box((3, 0.1, 2.6), at=(0, 1.6, 1.3), m=k.mat("#3b2416", "matte"), bevel=0, setting=True)
    k.box((3, 1.6, 0.04), at=(0, 0.8, -0.02), m=k.mat("#4a2d1a", "matte"), bevel=0, setting=True)

    # Boardwalk in front of the wall.
    plank = k.mat("#a56a38", "matte")
    for i in range(14):
        k.box((6, 0.12, 0.05), at=(0, -0.08 - i * 0.13, -0.025), m=plank, bevel=0.008, setting=True)
