"""What the reference analysis says about the art, written for the generator."""

STYLE = """The attached images are real cards from the game. Draw one new card that could sit beside them unnoticed: the same rendering, lighting, finish, color and level of detail.
Draw the object at its true real-world proportions, seen through a long lens from a low camera, so near parts never balloon. Tubes, ropes, rims, handles and hoops stay thin, and small parts stay small.
Surfaces are smooth and calm, with a few quiet marks. Cloth, cord and wood are matte. Only metal and glaze shine.
Draw only what the subject names. No text, letters, numbers, frame, border or watermark."""

CATEGORY_RULES = {
    "1": "The object floats in the air, usually slightly tilted, large on the card. The background is flat and graphic.",
    "2": "The object stands on a plain colored ledge and casts a soft shadow, large on the card. Behind it is a simple graphic backdrop.",
    "3": "The object stands on a real material surface and casts a soft shadow, large on the card. The backdrop behind it stays simple and graphic, not a full scene.",
    "4": "A close view of the object in its real place, central and large. The setting is open and calm: a few large soft shapes, with nothing added around the object.",
}

PATTERNS = {
    "plain_gradient": "a smooth gradient", "concentric_rings": "tone-on-tone concentric rings",
    "rays": "tone-on-tone radial rays", "stripes": "tone-on-tone wide stripes", "waves": "tone-on-tone soft waves",
    "diamonds": "tone-on-tone diamonds", "repeated_motif": "a faint tone-on-tone repeated motif",
    "plain_wall": "a plain wall", "full_scene": "a simple scene",
}

FIXES = {
    "composition_hierarchy.subject_area": "Make the hero fill more of the card.",
    "composition_hierarchy.box_width": "Make the hero wider so it spans most of the card.",
    "composition_hierarchy.box_height": "Make the hero taller so it spans most of the card.",
    "composition_hierarchy.center_x": "Center the hero horizontally.",
    "composition_hierarchy.center_y": "Center the hero vertically.",
    "composition_hierarchy.margin_min": "Keep a small even margin around the hero.",
    "color_palette.chroma_subject": "Make the hero's colors more saturated.",
    "color_palette.chroma_background": "Make the background more saturated.",
    "color_palette.hue_gap": "Give the hero a color opposite to the background.",
    "color_palette.shadow_chroma_kept": "Keep shadows colorful, never grey.",
    "value_contrast.lightness_mean": "Keep the card bright overall.",
    "value_contrast.lightness_p1": "Avoid pure black areas.",
    "value_contrast.rms_contrast": "Keep tones within a soft, moderate range.",
    "value_contrast.boundary_contrast": "Separate the hero's outline clearly from the background.",
    "surface_finish.detail_subject": "Simplify the hero: fewer small details.",
    "edges_linework.edge_density_subject": "Use larger, simpler shapes on the hero.",
    "edges_linework.edge_density_background": "Simplify the background.",
    "style": "Match the reference cards' render and finish more closely.",
    "art_category": "Follow the staging instructions exactly.",
    "support": "Follow the staging instructions exactly: floating, on a surface or in an environment as asked.",
    "pattern": "Use exactly the requested backdrop.",
    "identity": "Make the object instantly recognizable, keeping its most typical features.",
}
