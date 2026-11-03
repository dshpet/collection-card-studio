# Stone chess table in a park: the top sits centered on the pedestal, the stools stand on the lawn at opposite
# sides and lower than the top, and the 8 by 8 board lies flat on the top. Stone parts are chunky.
SCENE = {"category": "4", "backdrop": "#86d3fb", "azimuth": 28, "elevation": 20, "light": "left"}


def build(k):
    stone = k.mat("#c9c2d8", "matte")
    k.box((0.76, 0.76, 0.09), at=(0, 0, 0.705), m=stone, bevel=0.025)
    k.box((0.32, 0.32, 0.6), at=(0, 0, 0.36), m=stone, bevel=0.025)
    k.box((0.48, 0.48, 0.1), at=(0, 0, 0.05), m=stone, bevel=0.025)
    for row in range(8):
        for col in range(8):
            color = "#1f2b5e" if (row + col) % 2 else "#f4ead0"
            k.box((0.075, 0.075, 0.006), at=(-0.2625 + col * 0.075, -0.2625 + row * 0.075, 0.752),
                  m=k.mat(color, "satin"), bevel=0.001)
    for side in (-1, 1):
        k.cyl(0.14, 0.38, at=(side * 0.72, 0, 0.19), m=stone, bevel=0.02)
        k.cyl(0.2, 0.08, at=(side * 0.72, 0, 0.42), m=stone, bevel=0.025)

    k.floor("#5cc23a")
    for i in range(14):
        x = -2.2 + i * 0.35
        k.cyl(0.32, 0.01, at=(x, 1.3 + 0.35 * (x / 2.2) ** 2, 0.006 + 0.003 * (i % 2)), m=k.mat("#f0d79c", "matte"),
              bevel=0, setting=True)
    leaf, trunk = k.mat("#2f9a35", "matte"), k.mat("#7a5233", "matte")
    for x, y, size in ((-1.9, 2.6, 1.0), (1.8, 3.2, 1.2), (0.2, 4.5, 1.1)):
        k.cyl(0.08 * size, 1.4 * size, at=(x, y, 0.7 * size), m=trunk, setting=True)
        for dx, dz, r in ((0, 1.6, 0.6), (-0.4, 1.3, 0.45), (0.4, 1.35, 0.45)):
            k.sphere(r * size, at=(x + dx * size, y, dz * size), m=leaf, setting=True)
    for x, y in ((-1.2, 3.4), (-0.6, 3.6), (0.9, 2.4), (2.6, 2.2)):
        k.sphere(0.35, at=(x, y, 0.15), scale=(1.3, 1, 0.8), m=k.mat("#47b33c", "matte"), setting=True)
