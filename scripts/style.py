"""What the reference analysis says about the art, written for the generator."""

# The smooth-surface line, from experiments/night.py (2026-11-08): twins came out less grainy by pixels and by eye,
# with no gloss or CSD cost. BLOCKOUT keeps the old line: over a blockout the same line read glossier.
STYLE ="""The attached images are real cards from the game. Draw one new card that could sit beside them unnoticed: the same rendering, lighting, finish, color and level of detail.
Draw the object turned about 20-30 degrees into a three-quarter view, even when it is symmetric; only a face meant to be read, such as a clock or a sign, faces the camera. Keep its true proportions and mild perspective, from a low camera, so openings and rims are thin ovals. It spans about four fifths of the card. Forms are smooth, with small soft bevels. Rims, handles, cords, bands and posts stay slim, and small parts stay small.
One soft light from one side turns the form smoothly into shade.
Each material looks like itself by its color, in natural local color. Large surfaces stay smooth, with no grain, weave, nap or pores: detail lives in the parts. Shiny materials carry one soft highlight. Cloth, cord and wood stay matte.
Draw only what the subject names. No text, letters, numbers, frame, border or watermark."""

CATEGORY_RULES = {
    "1": "The object floats in the air, usually slightly tilted, large on the card; a big object may run past the card's edge. The background is flat and graphic, or the sky or water the object flies or swims in.",
    "2": "The object stands on a plain floor in the backdrop's color, a shade lighter, running out of the bottom of the card, and casts a soft shadow, large on the card. No shelf edge, wood or stone. Behind it is a simple graphic backdrop, with a soft pool of light behind the object, darker toward the corners.",
    "3": "The object stands on a real material surface and casts a soft shadow, large on the card. The backdrop behind it stays simple and graphic, not a full scene, with a soft pool of light behind the object, darker toward the corners.",
    "4": "A close view of the object in the exact spot where it is used, central and large: only a few metres of that place show, and the card's edge may cut the object. A building or landmark shows by its recognizable part, close.",
    # A flat object lying down (pattern surface_from_above), as on the real Map, Travel Book, Fruit Plate and Tennis.
    "flat": "The object lies on a real material surface that fills the whole card, seen from high above: no wall, no horizon and no backdrop. It casts a soft shadow and is large on the card.",
    "5": "The characters are central and large. The setting is a real place, simple and calm: a few large soft shapes.",
}

# Character cards. Tested in experiments/cast_trial.py: the cast stays itself when its cutouts are attached first.
# The outfit line, from experiments/outfit_check.py: without it, cutouts lent their costumes to new cards.
CAST_STYLE = """The first images show {who} from the game, cut out of real cards. The cutouts show who each character is, not what it wears: dress it only as the subject says. The last images are real cards from the game. Draw one new card that could sit beside the real cards unnoticed: the same rendering, lighting, finish, color and level of detail. {same} stays exactly the same: face, body, proportions and colors.
Draw only what the subject names. No text, letters, numbers, frame, border or watermark."""

BLOCKOUT = """The attached images are real cards from the game, except the last one, which is a 3D blockout of a new card. The blockout is right about the object's shape, its parts, where each part attaches and what it rests on, and about the camera and the framing.
Redraw the blockout as a finished card that could sit beside the real cards unnoticed: the same rendering, lighting, finish, color and level of detail. Keep every part, every connection, the pose, the camera and the framing exactly. Change only the surfaces: materials, bevels, shading and small details, and draw the backdrop and setting.
Each material looks like itself, with a little quiet detail and natural local color. Shiny materials carry one soft highlight. Cloth, cord and wood stay matte.
Draw only what the subject names. No text, letters, numbers, frame, border or watermark."""

EDIT = """The last attached image is a draft of a new card. The other images are real cards from the game.
Redraw the draft with these changes and keep everything else: the object, its pose, the backdrop and the colors.
{notes}"""

PATTERNS = {
    "plain_gradient": "a smooth gradient", "concentric_rings": "tone-on-tone concentric rings",
    "rays": "tone-on-tone radial rays", "stripes": "tone-on-tone wide stripes", "waves": "tone-on-tone soft waves",
    "diamonds": "tone-on-tone diamonds", "repeated_motif": "a faint tone-on-tone repeated motif of small {topic} icons",
    "plain_wall": "a plain wall", "full_scene": "a simple scene", "surface_from_above": "none: the surface fills the card",
}

# Measured fields checked against the real range of each category.
BANDS = ("composition_hierarchy.subject_area", "composition_hierarchy.box_width", "composition_hierarchy.box_height",
         "composition_hierarchy.center_x", "composition_hierarchy.center_y", "composition_hierarchy.margin_min",
         "color_palette.chroma_subject", "color_palette.chroma_background", "color_palette.hue_gap",
         "color_palette.shadow_chroma_kept", "value_contrast.lightness_mean", "value_contrast.lightness_p1",
         "value_contrast.rms_contrast", "value_contrast.boundary_contrast", "surface_finish.detail_subject",
         "edges_linework.edge_density_subject", "edges_linework.edge_density_background")
