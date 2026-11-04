# Steam locomotive on a desert track. Three pairs of large red drivers and a small leading pair stand on the
# rails, each pair on its axle through the frame; a side rod joins the driver crank pins and a main rod runs from
# the crosshead behind each cylinder to a longer crank pin on the middle driver. The cylinders hang from a saddle
# under the running board. The boiler lies on the running board, with the smokebox in front and its end inside
# the cab. The tall funnel chimney, the steam dome and the gold bell in its yoke stand on the boiler top. The
# round lamp sits on a bracket on top of the smokebox, and the wedge pilot slants down and forward from under the
# red buffer beam to just above the rails. The rails and ties run off the card both ways; flat desert and a few
# far mesas make the setting.
SCENE = {"category": "4", "backdrop": "#7cc6f2", "azimuth": 30, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    black = k.mat("#1c1d21", "satin")
    dark = k.mat("#3b3e45", "satin")
    red = k.mat("#d3262b", "satin")
    steel = k.mat("#8d939c", "metal")
    gold = k.mat("#e8b43a", "metal")
    glass = k.mat("#2a3a4a", "glass")
    lamp = k.mat("#ffe7a0", "glow")

    # Frame (holds every axle, meets the running board), running board, buffer beam, wedge pilot
    k.box((0.44, 1.5, 0.34), at=(0, -0.03, 0.34), m=dark, bevel=0.01)
    k.box((0.78, 1.55, 0.03), at=(0, -0.02, 0.515), m=black, bevel=0.006)
    k.box((0.78, 0.06, 0.12), at=(0, -0.79, 0.44), m=red, bevel=0.01)
    pilot = k.box((0.6, 0.24, 0.26), at=(0, -0.87, 0.25), m=dark, bevel=0.01)

    def wedge(p):
        x, y, z = p
        t = (0.13 - z) / 0.26
        if y < 0:
            y = 0.06 - 0.18 * t
        return (x * (1 - 0.12 * t), y, z)

    k.warp(pilot, wedge)

    # Leading wheels
    k.cyl(0.03, 0.66, at=(0, -0.6, 0.2), rot=(0, 90, 0), m=steel)
    for s in (-1, 1):
        k.cyl(0.11, 0.05, at=(s * 0.3, -0.6, 0.2), rot=(0, 90, 0), m=red, bevel=0.008)
        k.cyl(0.035, 0.07, at=(s * 0.3, -0.6, 0.2), rot=(0, 90, 0), m=dark)

    # Driving wheels, rods, cylinders
    drivers = (-0.28, 0.14, 0.56)
    for y in drivers:
        k.cyl(0.035, 0.66, at=(0, y, 0.29), rot=(0, 90, 0), m=steel)
        for s in (-1, 1):
            k.cyl(0.2, 0.05, at=(s * 0.3, y, 0.29), rot=(0, 90, 0), m=red, bevel=0.01)
            k.torus(0.185, 0.02, at=(s * 0.328, y, 0.29), rot=(0, 90, 0), m=red)
            k.cyl(0.05, 0.08, at=(s * 0.31, y, 0.29), rot=(0, 90, 0), m=dark)
            if y == 0.14:
                k.cyl(0.025, 0.12, at=(s * 0.37, y, 0.19), rot=(0, 90, 0), m=steel)
            else:
                k.cyl(0.025, 0.06, at=(s * 0.35, y, 0.19), rot=(0, 90, 0), m=steel)
    k.box((0.8, 0.2, 0.12), at=(0, -0.49, 0.42), m=dark, bevel=0.01)
    for s in (-1, 1):
        k.box((0.03, 0.9, 0.05), at=(s * 0.37, 0.14, 0.19), m=steel, bevel=0.006)
        k.cyl(0.08, 0.22, at=(s * 0.38, -0.49, 0.4), rot=(90, 0, 0), m=black, bevel=0.01)
        k.tube([(s * 0.38, -0.38, 0.4), (s * 0.38, -0.26, 0.4)], 0.018, steel)
        k.box((0.05, 0.08, 0.06), at=(s * 0.39, -0.26, 0.4), m=steel, bevel=0.006)
        k.tube([(s * 0.405, -0.24, 0.4), (s * 0.405, 0.14, 0.19)], 0.02, steel)

    # Boiler, smokebox, door
    k.cyl(0.25, 0.88, at=(0, -0.12, 0.78), rot=(90, 0, 0), m=black, bevel=0.01)
    k.cyl(0.26, 0.2, at=(0, -0.64, 0.78), rot=(90, 0, 0), m=dark, bevel=0.01)
    k.cyl(0.2, 0.03, at=(0, -0.75, 0.78), rot=(90, 0, 0), m=dark, bevel=0.01)
    k.cyl(0.03, 0.03, at=(0, -0.77, 0.78), rot=(90, 0, 0), m=steel)
    for s in (-1, 1):
        k.torus(0.252, 0.012, at=(0, s * 0.15 - 0.12, 0.78), rot=(90, 0, 0), m=gold)

    # Chimney, steam dome, bell
    funnel = [(0, 0.95), (0.09, 0.95), (0.085, 1.05), (0.075, 1.2), (0.08, 1.28), (0.1, 1.35),
              (0.13, 1.41), (0.14, 1.44), (0.14, 1.47), (0.11, 1.47), (0.0, 1.43)]
    k.lathe(funnel, at=(0, -0.45, 0), m=black)
    dome = [(0, 0.95), (0.12, 0.95), (0.12, 1.06), (0.115, 1.1), (0.1, 1.13), (0.07, 1.155), (0.035, 1.168),
            (0, 1.17)]
    k.lathe(dome, at=(0, -0.1, 0), m=black)
    for s in (-1, 1):
        k.cyl(0.015, 0.22, at=(s * 0.095, 0.15, 1.1), m=dark)
    k.cyl(0.015, 0.22, at=(0, 0.15, 1.2), rot=(0, 90, 0), m=dark)
    bell = [(0.065, 1.06), (0.062, 1.075), (0.05, 1.1), (0.042, 1.14), (0.036, 1.17), (0.02, 1.188), (0, 1.192)]
    k.lathe(bell, at=(0, 0.15, 0), m=gold)
    k.cyl(0.01, 0.02, at=(0, 0.15, 1.195), m=gold)

    # Front lamp
    k.box((0.08, 0.08, 0.08), at=(0, -0.67, 1.06), m=dark, bevel=0.008)
    k.cyl(0.08, 0.14, at=(0, -0.67, 1.16), rot=(90, 0, 0), m=dark, bevel=0.01)
    k.torus(0.07, 0.012, at=(0, -0.742, 1.16), rot=(90, 0, 0), m=gold)
    k.cyl(0.062, 0.01, at=(0, -0.742, 1.16), rot=(90, 0, 0), m=lamp, bevel=0.002)

    # Cab
    k.box((0.8, 0.45, 0.67), at=(0, 0.525, 0.865), m=black, bevel=0.012)
    roof = k.box((0.9, 0.56, 0.05), at=(0, 0.53, 1.225), m=dark, bevel=0.01)
    k.warp(roof, lambda p: (p[0], p[1], p[2] - 0.12 * p[0] * p[0]))
    for s in (-1, 1):
        k.box((0.012, 0.2, 0.2), at=(s * 0.4, 0.5, 1.0), m=glass, bevel=0.004)
        k.box((0.1, 0.012, 0.14), at=(s * 0.31, 0.297, 1.06), m=glass, bevel=0.004)
        k.box((0.012, 0.36, 0.025), at=(s * 0.403, 0.525, 0.68), m=red, bevel=0.003)

    # Track, desert, far mesas
    k.floor("#e9bf86")
    k.box((1.3, 30, 0.03), at=(0, 0, 0.015), m=k.mat("#b9a58c", "matte"), bevel=0.005, setting=True)
    tie = k.mat("#6e4a2e", "matte")
    for i in range(65):
        k.box((0.9, 0.11, 0.03), at=(0, -8 + i * 0.25, 0.045), m=tie, bevel=0.004, setting=True)
    for s in (-1, 1):
        k.box((0.05, 30, 0.03), at=(s * 0.3, 0, 0.075), m=steel, bevel=0.004, setting=True)
    mesa_m = k.mat("#d98a52", "matte")
    for x, y, w, h in ((-7, 11, 2.4, 1.6), (-2, 15, 1.8, 1.2), (-12, 7, 2.0, 1.3), (4, 16, 2.2, 1.0)):
        k.lathe([(0, 0), (w, 0), (w * 0.85, h * 0.85), (w * 0.72, h), (0, h)], at=(x, y, 0), m=mesa_m,
                setting=True)
