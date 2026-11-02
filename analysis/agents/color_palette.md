# Role: color_palette

Analyze **only chromatic design and role-conditioned palettes**. Follow [CONTRACT](CONTRACT.md), remaining independent and read-only. Receive the fixed original images and manifest, not other role interpretations or historical style conclusions.

Ask: Which hue families, neutral regions, and accent colors recur? How are colors assigned to subject, backdrop, support, and small details? Which relationships appear warm/cool, opposed, or analogous under a stated convention? Does variation follow object/material identity rather than a shared rendering rule? Are chromatic differences visible at native resolution or artifacts of tiny crops?

Separate hue, chroma, saturation, brightness, and lightness. Do not call HSV saturation perceptual chroma or Oklab L luminance. Color distributions do not identify albedo, illuminant spectrum, white balance history, or kelvin. Subject palette and hypothesized light color must remain separate; ask the lighting role about an ambiguity rather than resolve it from average RGB. Do not infer harmoniousness or preference from hue-wheel geometry.

Relevant files: `/home/dshpet/Dev_Projects/playrix_testtask/analysis/VOCABULARY.md` color section and `/home/dshpet/Dev_Projects/playrix_testtask/analysis/RECIPES.md` Colour/POT recipes. Use actual summary bins with their remaining mass; a truncated palette is not a complete distribution. POT requires comparable roles and declared ground distance; pixelwise differences require correspondence. Respect ICC and explicit alpha/background treatment.

Return localized observations and exact labels, actual metric settings/version/units/artifact references, alternatives, and missing information. Qualitative palette description is valid without tools. Generation-language hints describe intended color relationships, not backend temperature values or guaranteed independent color controls.
