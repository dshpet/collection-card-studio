"""The universal forms. One definition drives the raters, the schema and the report."""


def choice(*options):
    return {"kind": "choice", "options": list(options)}


def scale(low, high):
    return {"kind": "scale", "low": low, "high": high}


def text(hint):
    return {"kind": "text", "hint": hint}


NOTE = text("one observation about this card, at most 12 words")

CARD_FORM = {
    "identity": {
        "subject": text("the main object or scene in 1-4 plain words"),
        "object_class": choice(
            "tool", "accessory", "clothing", "food_drink", "furniture", "vehicle", "building_place",
            "plant_nature", "animal", "character", "toy_game", "electronics", "sports_gear",
            "container", "paper_document", "music_instrument", "other"),
        "real_world_scale": choice(
            "handheld", "body_sized", "furniture_sized", "vehicle_sized", "building_or_larger"),
        "subject_count": choice("one", "pair", "few", "many"),
    },
    "staging": {
        "art_category": choice("1", "2", "3", "4", "5"),
        "support": choice("floating", "on_surface", "in_environment"),
        "background_type": choice(
            "flat_gradient", "rays", "stripes", "motif_pattern", "simple_wall",
            "interior_scene", "exterior_scene"),
        "background_detail": scale("plain field", "busy full scene"),
        "secondary_objects": choice("none", "one", "few", "many"),
    },
    "backdrop": {
        "pattern": choice(
            "plain_gradient", "concentric_rings", "rays", "stripes", "waves", "diamonds",
            "repeated_motif", "plain_wall", "full_scene"),
        "tone": choice("tone_on_tone", "two_tone", "multicolor", "natural_scene"),
        "glow_behind_subject": choice("none", "soft", "strong"),
        "surface_kind": choice("none", "plain_colored_surface", "real_material_surface", "environment_ground"),
        "rendering_vs_subject": choice("same_finish", "flatter_than_subject", "more_painterly_than_subject"),
        "game_motif": choice("none", "house_logo", "animal_logo", "other_logo"),
    },
    "lighting_shading": {
        "light_direction": choice(
            "upper_left", "top", "upper_right", "left", "front", "right", "no_clear_direction"),
        "shading_model": choice("flat_cel", "stepped", "soft_gradient", "mixed"),
        "shadow_softness": scale("hard-edged shadows", "very soft shadows"),
        "ground_shadow": choice("none", "contact", "cast", "not_applicable"),
        "highlight_style": choice("none", "soft_bloom", "crisp_specular", "both"),
        "rim_light": choice("none", "subtle", "strong"),
        "note": NOTE,
    },
    "value_contrast": {
        "value_key": choice("high", "mid", "low"),
        "contrast": scale("narrow tonal range", "full black-to-white range"),
        "subject_separation": scale("subject merges with background", "subject pops clearly"),
        "darkest_accent": choice("none", "outline", "shadows", "object_parts"),
        "note": NOTE,
    },
    "color_palette": {
        "harmony": choice("monochrome", "analogous", "complementary", "triadic", "multicolor"),
        "saturation": scale("muted", "maximally saturated"),
        "temperature": choice("warm", "cool", "neutral", "warm_cool_mix"),
        "subject_vs_background": choice("hue_contrast", "value_contrast", "both", "similar"),
        "accent_color": choice("none", "one", "several"),
        "note": NOTE,
    },
    "composition_hierarchy": {
        "placement": choice("center", "center_low", "center_high", "off_center"),
        "scale_in_frame": scale("small with much space", "fills the frame"),
        "margin": choice("generous", "medium", "tight", "cropped"),
        "main_axis": choice("vertical", "horizontal", "diagonal", "round"),
        "focal_clarity": scale("several things compete", "one clear focus"),
        "note": NOTE,
    },
    "shape_proportions": {
        "form_language": choice("round_soft", "geometric", "organic", "angular", "mixed"),
        "exaggeration": scale("realistic proportions", "caricature"),
        "chunkiness": scale("thin and delicate", "thick and toy-like"),
        "silhouette_clarity": scale("hard to read in silhouette", "instantly readable"),
        "simplification": scale("many small details", "strongly reduced"),
        "note": NOTE,
    },
    "viewpoint_depth": {
        "camera_height": choice("eye_level", "slightly_above", "high_above", "below"),
        "object_angle": choice("front", "three_quarter", "side", "top", "mixed"),
        "perspective": scale("flat, orthographic", "strong convergence"),
        "depth_layers": choice("1", "2", "3", "4_or_more"),
        "background_blur": choice("none", "slight", "strong"),
        "note": NOTE,
    },
    "edges_linework": {
        "outline": choice("none", "selective", "full_colored", "full_dark"),
        "edge_softness": scale("crisp", "soft"),
        "interior_lines": scale("none", "many drawn lines"),
        "note": NOTE,
    },
    "surface_finish": {
        "render_look": choice("flat_2d", "painted_2d", "soft_3d", "glossy_3d", "clay_toy"),
        "gloss": scale("matte", "very glossy"),
        "texture_amount": scale("clean surfaces", "rich surface texture"),
        "material_realism": scale("symbolic materials", "convincing materials"),
        "note": NOTE,
    },
    "pose_rhythm": {
        "pose": choice("upright_static", "slight_tilt", "strong_tilt", "dynamic"),
        "symmetry": scale("asymmetric", "symmetric"),
        "repetition": scale("no repeated motifs", "strong repeated motifs"),
        "energy": scale("calm", "lively"),
        "note": NOTE,
    },
    "idea": {
        "recognizability": scale("ambiguous", "instant at thumbnail size"),
        "recognition_cue": text("the visual feature that identifies it, at most 8 words"),
        "theme_role": choice(
            "core_symbol", "equipment", "place", "food_drink", "vehicle", "activity",
            "keepsake", "character_moment"),
        "humor": scale("none", "openly comic"),
    },
}

SET_FORM = {
    "reading": {
        "title": text("the set title exactly as written at the top"),
        "title_words": choice("1", "2", "3", "4_or_more"),
    },
    "idea": {
        "topic_type": choice(
            "place", "activity", "event", "group_or_profession", "object_family", "mood_or_season"),
        "breadth": scale("very narrow topic", "very broad topic"),
        "item_logic": choice("things_you_use", "things_at_a_place", "activities", "mixed"),
        "obviousness": scale("obscure picks", "the first things anyone would name"),
        "name_style": choice("plain_noun", "descriptive_phrase", "wordplay", "mixed"),
        "story": choice("none", "implied", "explicit_in_character_cards"),
    },
    "variety": {
        "scale_variety": scale("same-sized things", "from small objects to buildings"),
        "color_variety": scale("one dominant color", "every card a different color"),
        "silhouette_variety": scale("similar shapes", "all different shapes"),
        "object_type_variety": scale("one kind of thing", "many kinds of things"),
    },
    "note": {"note": text("what makes this set hold together, at most 20 words")},
}


def _schema(field):
    if field["kind"] == "choice":
        return {"type": "string", "enum": field["options"]}
    if field["kind"] == "scale":
        return {"type": "integer", "enum": [1, 2, 3, 4, 5]}
    return {"type": "string"}


def _object(properties):
    return {"type": "object", "additionalProperties": False,
            "properties": properties, "required": list(properties)}


def _sections(form):
    return {section: _object({name: _schema(field) for name, field in fields.items()})
            for section, fields in form.items()}


def card_schema(sections=None):
    form = {name: CARD_FORM[name] for name in sections or CARD_FORM}
    return _object(_sections(form))


def set_schema():
    card = _object({"slot": {"type": "integer"}, "name": {"type": "string"},
                    "gold_frame": {"type": "boolean"}})
    return _object({"cards": {"type": "array", "items": card}, **_sections(SET_FORM)})


def guide(form):
    """Render a form as rater instructions."""
    lines = []
    for section, fields in form.items():
        lines.append(f"\n{section}:")
        for name, field in fields.items():
            if field["kind"] == "scale":
                lines.append(f"- {name}: 1 = {field['low']}, 5 = {field['high']}")
            elif field["kind"] == "text":
                lines.append(f"- {name}: {field['hint']}")
            else:
                lines.append(f"- {name}: one of {', '.join(field['options'])}")
    return "\n".join(lines)
