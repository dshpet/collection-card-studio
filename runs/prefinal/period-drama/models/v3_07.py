# Two-tier porcelain cake stand: a round flared foot rests on the linen tablecloth; one center post rises from it
# through collars under a wide lower plate and a smaller upper plate to a ball finial. Small iced cakes (sponge base,
# pink icing dome, white cream dot) sit on both plates: six around the lower tier, three on the upper.
import math

SCENE = {"category": "3", "backdrop": "#6b2a96", "azimuth": 28, "elevation": 17, "lens": 60, "light": "left"}


def build(k):
    china = k.mat("#f7f5f2", "gloss")
    sponge = k.mat("#f1d29a", "matte")
    icing = k.mat("#f58cb4", "gloss")
    cream = k.mat("#fffaf4", "satin")

    # Foot: a flared round base that rests on the cloth.
    k.lathe([(0, 0), (0.22, 0), (0.232, 0.012), (0.225, 0.03), (0.18, 0.05), (0.11, 0.075),
             (0.065, 0.1), (0.048, 0.13), (0.045, 0.15), (0, 0.15)], at=(0, 0, 0), rot=(0, 0, 0), m=china)
    # Center post from the foot to the finial.
    k.cyl(0.032, 0.84, at=(0, 0, 0.56), rot=(0, 0, 0), m=china)
    k.sphere(0.05, at=(0, 0, 1.0), m=china)
    k.lathe([(0.032, 0), (0.05, 0.01), (0.04, 0.03), (0, 0.03)], at=(0, 0, 0.94), rot=(0, 0, 0), m=china)

    def plate(z, rad):
        # Collar under the plate, joining it to the post.
        k.lathe([(0, 0), (0.032, 0), (0.07, 0.03), (0.075, 0.045), (0, 0.045)],
                at=(0, 0, z - 0.045), rot=(0, 0, 0), m=china)
        # Shallow dish with a clearly raised, thick rolled rim so its edge reads against the cloth.
        prof = [(0, 0), (rad * 0.6, 0.004), (rad * 0.88, 0.024), (rad * 0.98, 0.06), (rad + 0.022, 0.085),
                (rad + 0.004, 0.1), (rad * 0.95, 0.075), (rad * 0.82, 0.034), (rad * 0.4, 0.022), (0, 0.022)]
        k.lathe(prof, at=(0, 0, z), rot=(0, 0, 0), m=china)
        return z + 0.022

    def cake(x, y, base):
        k.cyl(0.058, 0.055, at=(x, y, base + 0.0275), rot=(0, 0, 0), m=sponge, bevel=0.006)
        k.lathe([(0, 0), (0.066, 0), (0.068, 0.012), (0.06, 0.03), (0.04, 0.045), (0.015, 0.052), (0, 0.053)],
                at=(x, y, base + 0.05), rot=(0, 0, 0), m=icing)
        k.sphere(0.02, at=(x, y, base + 0.112), scale=(1, 1, 0.8), m=cream)

    low = plate(0.3, 0.44)
    for i in range(6):
        a = math.radians(i * 60 + 15)
        cake(0.29 * math.cos(a), 0.29 * math.sin(a), low)

    high = plate(0.68, 0.28)
    for i in range(3):
        a = math.radians(i * 120 - 90)
        cake(0.155 * math.cos(a), 0.155 * math.sin(a), high)

    # White linen tablecloth in a deeper warm oatmeal-white so the porcelain rims stand out; top at z = 0,
    # wide enough to run off both sides of the card.
    k.box((14, 5, 0.1), at=(0, 1.5, -0.05), m=k.mat("#cbbfae", "matte"), bevel=0.01, setting=True)
