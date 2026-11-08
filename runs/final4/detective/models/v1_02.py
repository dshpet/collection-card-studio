# Vintage press camera: a box body with a short bellows out of the front, carrying the lens barrel with a silver
# ring and front glass. A round flash dish faces forward from a post that stands on the body's top, with a small
# bulb at its centre. A yellow shutter button and a viewfinder sit on top, and a winding knob on the side.
SCENE = {"category": "1", "backdrop": "#3a62d8", "azimuth": 30, "elevation": 12, "lens": 60, "light": "left"}


def build(k):
    body = k.mat("#8e3b26", "satin")
    trim = k.mat("#5a2418", "matte")
    dark = k.mat("#2b2b30", "satin")
    silver = k.mat("#cfd4db", "metal")
    glass = k.mat("#9fc6e0", "glass")
    yellow = k.mat("#ffcc2e", "satin")

    # Body: the card centers on it (fix round, 2026-11-08: "should be more centered at the point of visual attention")
    k.focus(k.box((0.70, 0.32, 0.50), at=(0, 0, 0.25), m=body, bevel=0.05))
    k.box((0.72, 0.30, 0.06), at=(0, 0, 0.25), m=trim, bevel=0.02)

    # Front standard, bellows and lens
    k.box((0.36, 0.04, 0.36), at=(0.04, -0.175, 0.25), m=dark, bevel=0.02)
    k.cone(0.16, 0.125, 0.10, at=(0.04, -0.245, 0.25), rot=(90, 0, 0), m=dark, bevel=0.01)
    k.cyl(0.125, 0.08, at=(0.04, -0.33, 0.25), rot=(90, 0, 0), m=dark, bevel=0.01)
    k.cyl(0.13, 0.03, at=(0.04, -0.375, 0.25), rot=(90, 0, 0), m=silver, bevel=0.008)
    k.torus(0.11, 0.025, at=(0.04, -0.39, 0.25), rot=(90, 0, 0), m=silver)
    k.sphere(0.09, at=(0.04, -0.388, 0.25), scale=(1, 0.3, 1), m=glass)

    # Flash: post on the top, dish facing front, bulb in the middle; compact, so the centered body stays large
    fx, fz, sc = -0.20, 0.72, 0.68
    k.cyl(0.05, 0.03, at=(fx, 0.04, 0.515), m=silver, bevel=0.006)
    k.cyl(0.025, fz - 0.53, at=(fx, 0.04, (fz + 0.53) / 2), m=silver)
    profile = [(0.0, 0.0), (0.05, 0.003), (0.10, 0.014), (0.15, 0.034), (0.19, 0.062), (0.21, 0.08),
               (0.205, 0.088), (0.185, 0.074), (0.145, 0.047), (0.095, 0.027), (0.045, 0.017), (0.0, 0.014)]
    k.lathe([(r * sc, z * sc) for r, z in profile], at=(fx, 0.0, fz), rot=(90, 0, 0), m=silver)
    k.cyl(0.03, 0.05, at=(fx, 0.02, fz), rot=(90, 0, 0), m=dark)
    k.sphere(0.03, at=(fx, -0.03, fz), m=k.mat("#fff6d8", "glow"))

    # Top: viewfinder and shutter button
    k.box((0.16, 0.12, 0.07), at=(0.06, 0.03, 0.535), m=dark, bevel=0.015)
    k.cyl(0.03, 0.012, at=(0.06, -0.035, 0.535), rot=(90, 0, 0), m=glass)
    k.cyl(0.045, 0.03, at=(0.25, -0.04, 0.51), m=silver, bevel=0.006)
    k.cyl(0.035, 0.04, at=(0.25, -0.04, 0.54), m=yellow, bevel=0.01)

    # Side winding knob
    k.cyl(0.06, 0.05, at=(0.375, 0.02, 0.36), rot=(0, 90, 0), m=silver, bevel=0.01)

    k.turn(0, -5, 0)
