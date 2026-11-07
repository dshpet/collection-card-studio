# Flashlight: one red lathe-turned barrel with a flared head; a silver bezel ring holds the glass lens, and a
# glowing reflector sits just behind it. Raised ring ridges form the grip, the yellow slide switch sits on top of
# the barrel ahead of the grip, and a silver cap closes the tail. The light shafts are left to the image model.
# Built along x with the head toward -x, then tilted so the head rises up-left and turns toward the camera.
SCENE = {"category": "1", "backdrop": "#2fd6e6", "azimuth": 25, "elevation": 10, "lens": 60, "light": "left"}


def build(k):
    red = k.mat("#d62a22", "satin")
    ridge = k.mat("#b51e18", "satin")
    silver = k.mat("#c9ced6", "metal")
    yellow = k.mat("#ffd21f", "satin")
    cz = 0.5
    # Lathe local z runs from the tail (world x = 0.5) to the head (world x = -0.5).
    axis = dict(at=(0.5, 0, cz), rot=(0, -90, 0))
    body = [(0, 0.03), (0.08, 0.03), (0.09, 0.04), (0.09, 0.62), (0.095, 0.65), (0.11, 0.69),
            (0.128, 0.73), (0.14, 0.77), (0.145, 0.81), (0.145, 0.9), (0.13, 0.9), (0, 0.9)]
    k.lathe(body, m=red, **axis)
    # Silver tail cap.
    k.lathe([(0, 0), (0.07, 0), (0.085, 0.01), (0.092, 0.03), (0.092, 0.05), (0, 0.05)], m=silver, **axis)
    # Silver head bezel ring around the lens.
    k.lathe([(0.12, 0.89), (0.155, 0.89), (0.16, 0.91), (0.16, 0.96), (0.15, 0.975), (0.13, 0.975),
             (0.13, 0.89)], m=silver, **axis)
    # Glowing reflector/bulb face behind the glass lens.
    k.cyl(0.128, 0.01, at=(0.5 - 0.935, 0, cz), rot=(0, 90, 0), m=k.mat("#fff2a0", "glow"))
    k.cyl(0.132, 0.012, at=(0.5 - 0.955, 0, cz), rot=(0, 90, 0), m=k.mat("#e8fbff", "glass"))
    # Ridged grip: raised rings around the barrel.
    for i in range(8):
        x = 0.42 - i * 0.045
        k.torus(0.09, 0.012, at=(x, 0, cz), rot=(0, 90, 0), m=ridge)
    # Yellow slide switch on top of the barrel, set in a small red housing.
    k.box((0.11, 0.07, 0.03), at=(-0.06, 0, cz + 0.085), m=red, bevel=0.012)
    k.box((0.07, 0.045, 0.03), at=(-0.06, 0, cz + 0.105), m=yellow, bevel=0.01)
    k.turn(0, 28, 40)
