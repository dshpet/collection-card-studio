# Rural mailbox on a wooden post at the edge of a dirt road. The arched sheet-metal box (flat walls under a
# half-round roof) lies front-to-back on a mounting board screwed to the top of a square post. Two angled
# braces run from the post up to the underside of the board. The front door, a slightly larger arched plate,
# faces the road (-y) and has a pull knob. The red flag's arm pivots on a bolt through the right side wall and
# stands raised. The post goes into the grass verge; the road runs past in front. The framing holds the box,
# so the post runs off the bottom of the card.
SCENE = {"category": "4", "backdrop": "#f7a54a", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    blue = k.mat("#2f7fd6", "metal")
    blue_dark = k.mat("#2466b3", "metal")
    red = k.mat("#e3312b", "satin")
    wood = k.mat("#8a5a32", "matte")
    board_wood = k.mat("#a26a3a", "matte")
    bolt = k.mat("#4a4f57", "metal")

    base = 1.0              # bottom of the mailbox
    w, length, wall = 0.46, 0.95, 0.26
    r = w / 2

    # Mailbox body: flat walls with a half-round roof along y
    k.box((w, length, wall), at=(0, 0, base + wall / 2), m=blue, bevel=0.012)
    k.cyl(r, length, at=(0, 0, base + wall), rot=(90, 0, 0), m=blue, bevel=0.012)

    # Front door, a bit bigger than the body, facing the road (-y)
    fy = -length / 2 - 0.012
    k.box((w + 0.03, 0.03, wall + 0.015), at=(0, fy, base + wall / 2 - 0.0075), m=blue_dark, bevel=0.008)
    k.cyl(r + 0.015, 0.03, at=(0, fy, base + wall), rot=(90, 0, 0), m=blue_dark, bevel=0.008)
    k.cyl(0.018, 0.04, at=(0, fy - 0.03, base + wall + 0.12), rot=(90, 0, 0), m=bolt)
    k.sphere(0.03, at=(0, fy - 0.055, base + wall + 0.12), scale=(1, 0.6, 1), m=bolt)
    # Back end plate
    by = length / 2 + 0.008
    k.box((w + 0.016, 0.02, wall + 0.008), at=(0, by, base + wall / 2 - 0.004), m=blue_dark, bevel=0.006)
    k.cyl(r + 0.008, 0.02, at=(0, by, base + wall), rot=(90, 0, 0), m=blue_dark, bevel=0.006)

    # Red flag on the right side (+x): bolt through the wall, arm raised, flag plate at the top
    sx = w / 2
    pivot = (sx + 0.03, 0.18, base + 0.2)
    k.cyl(0.028, 0.05, at=(sx + 0.02, pivot[1], pivot[2]), rot=(0, 90, 0), m=bolt)
    k.box((0.02, 0.045, 0.42), at=(sx + 0.05, pivot[1], pivot[2] + 0.17), m=red, bevel=0.006)
    k.box((0.022, 0.2, 0.13), at=(sx + 0.05, pivot[1] + 0.09, pivot[2] + 0.33), m=red, bevel=0.008)

    # Mounting board under the box, on top of the post
    k.box((0.36, 0.8, 0.045), at=(0, 0, base - 0.0225), m=board_wood, bevel=0.008)

    # Square wooden post going down into the verge; two braces under the board
    post_parts = [k.box((0.15, 0.15, 1.2), at=(0, 0, base - 0.045 - 0.6 + 0.2), m=wood, bevel=0.012)]
    for s in (-1, 1):
        post_parts.append(k.box((0.07, 0.36, 0.06), at=(0, s * 0.19, base - 0.16),
                                rot=(s * -35, 0, 0), m=wood, bevel=0.008))
    k.unframed(*post_parts)

    # Setting: grass verge around the post, dirt road in front, lying a little lower
    k.box((8, 3.2, 0.2), at=(0, 1.1, -0.1), m=k.mat("#5fb83a", "matte"), bevel=0.03, setting=True)
    k.box((8, 4, 0.2), at=(0, -2.5, -0.14), m=k.mat("#c08a52", "matte"), bevel=0.03, setting=True)
