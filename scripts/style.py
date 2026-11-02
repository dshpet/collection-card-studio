"""What the reference analysis says about the art, written for the generator."""

STYLE = """Polished mobile-game collection card art, a soft 3D render with smooth gradients.
Chunky, rounded, toy-like shapes with slightly exaggerated proportions and no thin fragile parts.
No outlines, no visible grain or brush texture. Clean surfaces with soft highlights.
Very saturated, bright colors. Shadows stay colorful: never black or grey. Dark colors are rich indigo or crimson.
One large hero, centered, seen in three-quarter view from slightly above, lit softly from above.
The hero's main color opposes the background color, so it pops instantly at thumbnail size.
No text, letters, numbers, card frame, border or watermark."""

CATEGORY_RULES = {
    "1": "The hero floats in the air with no ground and no shadow beneath it, usually slightly tilted. "
         "No small details. The background is a flat graphic field, tone-on-tone, with a soft glow behind the hero.",
    "2": "The hero stands upright on a simple plain colored ledge and casts a soft shadow. No small details. "
         "Behind it is a simple graphic backdrop, tone-on-tone, with a soft glow.",
    "3": "The hero stands on a real material surface such as wood, stone, sand or grass and casts a soft shadow. "
         "The backdrop behind it stays simple and graphic, not a full scene.",
    "4": "The hero sits inside a simple real environment that fills the card, with a few supporting objects, "
         "but it stays large, central and clearly the focus.",
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
