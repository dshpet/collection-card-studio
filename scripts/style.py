"""What the reference analysis says about the art, written for the generator."""

STYLE = """The attached images are real cards from the game. Draw one new card that could sit beside them unnoticed: the same rendering, lighting, finish, color and level of detail.
Draw the object with its true proportions and mild perspective. It spans about four fifths of the card. Forms are smooth, with small soft bevels. Rims, handles, cords, bands and posts stay slim, and small parts stay small.
Each material looks like itself, with a little quiet detail and natural local color. Shiny materials carry one soft highlight. Cloth, cord and wood stay matte.
Draw only what the subject names. No text, letters, numbers, frame, border or watermark."""

CATEGORY_RULES = {
    "1": "The object floats in the air, usually slightly tilted, large on the card. The background is flat and graphic.",
    "2": "The object stands on a plain colored ledge and casts a soft shadow, large on the card. Behind it is a simple graphic backdrop.",
    "3": "The object stands on a real material surface and casts a soft shadow, large on the card. The backdrop behind it stays simple and graphic, not a full scene.",
    "4": "A close view of the object in its real place, central and large. The setting is open and calm: a few large soft shapes, with nothing added around the object.",
}

EDIT = """The last attached image is a draft of a new card. The other images are real cards from the game.
Redraw the draft with these changes and keep everything else: the object, its pose, the backdrop and the colors.
{notes}
No text, letters, numbers, frame, border or watermark."""

PATTERNS = {
    "plain_gradient": "a smooth gradient", "concentric_rings": "tone-on-tone concentric rings",
    "rays": "tone-on-tone radial rays", "stripes": "tone-on-tone wide stripes", "waves": "tone-on-tone soft waves",
    "diamonds": "tone-on-tone diamonds", "repeated_motif": "a faint tone-on-tone repeated motif",
    "plain_wall": "a plain wall", "full_scene": "a simple scene",
}

# Measured fields checked against the real range of each category.
BANDS = ("composition_hierarchy.subject_area", "composition_hierarchy.box_width", "composition_hierarchy.box_height",
         "composition_hierarchy.center_x", "composition_hierarchy.center_y", "composition_hierarchy.margin_min",
         "color_palette.chroma_subject", "color_palette.chroma_background", "color_palette.hue_gap",
         "color_palette.shadow_chroma_kept", "value_contrast.lightness_mean", "value_contrast.lightness_p1",
         "value_contrast.rms_contrast", "value_contrast.boundary_contrast", "surface_finish.detail_subject",
         "edges_linework.edge_density_subject", "edges_linework.edge_density_background")
