# Example evidence fixtures

These ready examples passed the recorded [local verification](../verification.json). They demonstrate arithmetic and output scope, not recovered lighting.

| File | Demonstration | What it does not establish |
|---|---|---|
| [shadow_ramp.png](shadow_ramp.png) | Synthetic 256×96 RGB8 numeric ramp, constant along rows; not a scene rendering. | Real illumination, physical penumbra, or lamp parameters. |
| [shadow_profile.json](shadow_profile.json) | 256 profile samples, x=0…255 at y=48, linewidth 5. | Automatic softness inference; it supplies samples only. |
| [shadow_measurement.json](shadow_measurement.json) | Reviewed endpoint levels and interpolated 10–90% crossings. | Source size, distance, light count, or physical shadow reconstruction. |
| [card_summary.json](card_summary.json) | Actual 59×67 whole-frame card summary, without a subject mask. | Automatic segmentation, fine lighting/material evidence, or a style score. |

## Reproduce the outputs on stdout

Run from the project root; these commands do not overwrite the saved records:

```sh
.venv/bin/python -B scripts/image_evidence.py profile analysis/examples/shadow_ramp.png --start 0 48 --end 255 48 --width 5
.venv/bin/python -B scripts/image_evidence.py summary materials/card_examples/3458764679576006333.png --background 255 255 255
```

## Interpret the width correctly

The specified linear-Y transition runs from x=60 to 180, with plateau levels 0.15 and 0.65. Its **unquantized** 10–90% width is 96 px. For the stored RGB8 image, plateau estimates use the first 32 samples `[0,32)` and last 32 `[224,256)`. Linear interpolation of the normalized profile's threshold crossings gives **96.82192026779823 px** (about 96.822 px), as recorded in `shadow_measurement.json`.

The difference reflects 8-bit encoding/quantization and the resulting plateau/crossing values. It is not a measured physical penumbra or a failed recovery of a real light source. The measurement record is a separate calculation using reviewed windows; `profile` itself does not return a shadow width.

See [lighting interpretation](../LIGHTING.md), [runnable commands/API recipes](../RECIPES.md), and [tool output contracts](../TOOLS.md). Source images, masks, backgrounds, and preprocessing belong in each result's provenance. Small project cards remain unsuitable for fine-finish conclusions even when a synthetic ramp behaves correctly.
