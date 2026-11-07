# Balloon whisk, floating: a round orange handle with a rounded end, a steel ferrule at its top, and five
# steel wire loops. Each loop rises out of the ferrule on one side, swells into the balloon, crosses over the top
# through the axis and comes down the opposite side back into the ferrule, so ten wires show around the balloon
# and the five loops cross in a smooth round dome at the top. Upright and symmetrical, tilted a little to show depth.
import math

SCENE = {"category": "1", "backdrop": "#5cc94a", "azimuth": 25, "elevation": 12, "lens": 70, "light": "left"}


def build(k):
    steel = k.mat("#cfd5dc", "metal")
    orange = k.mat("#f27a1a", "satin")

    # Handle: round, slightly wider toward the bottom, with a rounded bottom end.
    k.lathe([(0.0, 0.0), (0.022, 0.003), (0.036, 0.012), (0.045, 0.03), (0.049, 0.06), (0.049, 0.12),
             (0.047, 0.2), (0.044, 0.28), (0.042, 0.335), (0.0, 0.335)], at=(0, 0, 0), rot=(0, 0, 0), m=orange)
    # Steel ferrule clamping the wire ends into the handle.
    k.lathe([(0.0, 0.33), (0.045, 0.33), (0.046, 0.345), (0.044, 0.38), (0.04, 0.41), (0.034, 0.435),
             (0.0, 0.435)], at=(0, 0, 0), rot=(0, 0, 0), m=steel)

    # Half-loop profile as (radius, z), from the ferrule up to the axis at the top; the crown is a round dome.
    half = [(0.026, 0.42), (0.05, 0.47), (0.09, 0.54), (0.135, 0.62), (0.175, 0.71), (0.2, 0.8),
            (0.206, 0.87), (0.196, 0.93), (0.172, 0.98), (0.135, 1.017), (0.09, 1.04), (0.045, 1.051),
            (0.0, 1.054)]
    wire_r = 0.013
    loops = 5
    for i in range(loops):
        a = math.pi * i / loops
        ca, sa = math.cos(a), math.sin(a)
        lift = i * 0.5 * wire_r  # a slight stagger where the loops cross, spread over the whole crown

        def pt(r, z, side):
            w = 0.5 + 0.5 * math.cos(math.pi * min(1.0, r / 0.2)) if z > 0.85 else 0.0
            return (side * r * ca, side * r * sa, z + lift * w)

        pts = [pt(r, z, 1) for r, z in half] + [pt(r, z, -1) for r, z in reversed(half[:-1])]
        k.tube(pts, wire_r, steel, curved=True)

    k.turn(5, -7, 0)
