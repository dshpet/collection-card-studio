# Short wooden pier: it starts on the beach and runs out over the water on pairs of posts; planks lie across two
# beams; the rope coils around the top of the end post and the life ring hangs from a hook on another post.
import math

SCENE = {"category": "4", "backdrop": "#8fdcff", "azimuth": 22, "elevation": 18, "light": "left"}


def build(k):
    post, beam, plank = k.mat("#9a5a2b", "matte"), k.mat("#86502a", "matte"), k.mat("#c77d3d", "matte")
    for x in (-0.6, -0.05, 0.5, 0.95):
        for y in (-0.26, 0.26):
            top = 0.6 if x == 0.95 or (x == 0.5 and y < 0) else 0.42
            k.cyl(0.04, top + 0.3, at=(x, y, (top - 0.3) / 2), m=post, bevel=0.008)
    for y in (-0.22, 0.22):
        k.box((1.65, 0.06, 0.06), at=(0.17, y, 0.31), m=beam, bevel=0.006)
    for i in range(13):
        k.box((0.11, 0.6, 0.03), at=(-0.66 + i * 0.125, 0, 0.355), m=plank, bevel=0.006)
    rope = k.mat("#d9b57c", "matte")
    for z in (0.47, 0.505, 0.54):
        k.torus(0.058, 0.018, at=(0.95, -0.26, z), m=rope)
    k.cyl(0.008, 0.09, at=(0.5, -0.345, 0.55), rot=(90, 0, 0), m=k.mat("#8b8f96", "metal"))
    center = (0.5, -0.36, 0.482)
    for i in range(8):
        arc = [math.radians(i * 45 + j * 9) for j in range(6)]
        points = [(center[0] + 0.11 * math.sin(a), center[1], center[2] + 0.11 * math.cos(a)) for a in arc]
        k.tube(points, 0.034, k.mat("#e8262b" if i % 2 else "#fbfbf7", "satin"), curved=True)

    k.box((8, 8, 0.02), at=(0, 0, -0.01), m=k.mat("#25bfd3", "gloss"), bevel=0, setting=True)
    k.box((4, 8, 0.3), at=(-2.55, 0, -0.1), rot=(0, -4, 0), m=k.mat("#f3cf8a", "matte"), bevel=0.02, setting=True)
