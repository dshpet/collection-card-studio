# Ship's wheel: a round wooden rim joined to a brass hub by eight spokes that run on past the rim into turned
# handles. The hub turns on a brass axle that goes into the top of a sturdy square wooden post. The post stands
# on a plinth bolted to the deck planks. A low bulwark with a cap rail closes the deck behind, and the sea lies
# below it, so it shows above the rail under the clear sky.
import math

SCENE = {"category": "4", "backdrop": "#5fd8f5", "azimuth": 25, "elevation": 12, "lens": 55, "light": "left"}


def build(k):
    wood = k.mat("#8a4f24", "matte")
    dark = k.mat("#6e3d1b", "matte")
    brass = k.mat("#d9a53a", "metal")
    red = k.mat("#d8312b", "gloss")

    hz, hy = 0.78, -0.07  # hub center height and wheel plane
    # Rim: a thick wooden ring with a thin brass band on its front face.
    k.torus(0.36, 0.036, at=(0, hy, hz), rot=(90, 0, 0), m=wood)
    k.torus(0.36, 0.012, at=(0, hy - 0.03, hz), rot=(90, 0, 0), m=brass)
    # Spokes: four through-cylinders make the eight spokes, hub to rim.
    for i in range(4):
        k.cyl(0.022, 0.74, at=(0, hy, hz), rot=(0, i * 45, 0), m=wood)
    # Turned handles, one on each spoke, outside the rim.
    handle = [(0.026, 0.0), (0.03, 0.02), (0.022, 0.04), (0.034, 0.075), (0.036, 0.095),
              (0.028, 0.12), (0.03, 0.14), (0.018, 0.155), (0, 0.16)]
    for i in range(8):
        a = math.radians(i * 45)
        r0 = 0.385
        at = (r0 * math.sin(a), hy, hz + r0 * math.cos(a))
        k.lathe(handle, at=at, rot=(0, i * 45, 0), m=wood, verts=32)
    # Brass hub with a red cap on the front, on a brass axle into the post.
    k.cyl(0.075, 0.08, at=(0, hy, hz), rot=(90, 0, 0), m=brass)
    k.cyl(0.05, 0.03, at=(0, hy - 0.05, hz), rot=(90, 0, 0), m=red, bevel=0.01)
    k.cyl(0.03, 0.2, at=(0, hy + 0.12, hz), rot=(90, 0, 0), m=brass)

    # Post: the axle enters its upper front face; a cap on top, a plinth on the deck.
    py = 0.24
    k.box((0.2, 0.2, 0.9), at=(0, py, 0.45), m=wood, bevel=0.02)
    k.box((0.26, 0.26, 0.05), at=(0, py, 0.925), m=dark, bevel=0.015)
    k.cyl(0.055, 0.03, at=(0, py - 0.105, hz), rot=(90, 0, 0), m=brass)
    k.box((0.34, 0.34, 0.06), at=(0, py, 0.03), m=dark, bevel=0.015)
    for x in (-0.13, 0.13):
        for y in (py - 0.13, py + 0.13):
            k.cyl(0.015, 0.02, at=(x, y, 0.065), m=brass)

    # Deck planks running fore and aft.
    plank_a, plank_b = k.mat("#c07c3e", "matte"), k.mat("#b0703a", "matte")
    for i in range(-14, 15):
        k.box((0.2, 3.2, 0.05), at=(i * 0.21, 0.0, -0.025), m=plank_a if i % 2 else plank_b,
              bevel=0.006, setting=True)
    # Bulwark behind the helm, with a cap rail; the sea lies beyond and below it.
    k.box((6.2, 0.1, 0.5), at=(0, 1.55, 0.25), m=k.mat("#9a5a2b", "matte"), bevel=0.01, setting=True)
    k.box((6.2, 0.18, 0.06), at=(0, 1.55, 0.53), m=k.mat("#7a4420", "matte"), bevel=0.01, setting=True)
    k.floor("#1fb3cf", "gloss", size=60, z=-1.0)
