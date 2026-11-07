# Structured art analysis — reference pilot 01

## Scope and evidence

This is a qualified pilot, not a claim about the complete product style. The four primary images R1–R4 are existing 430×480 files whose saved hashes match the fixed input manifest; their live-source nativeness was not independently verified. They are not asserted to be one complete product set. S1 is a 2796×1290 collection-screen context image, not a clean individual-art reference. G1 and G2 are reduced-resolution category guides; category 5’s gold-card character designs are excluded from general non-gold requirements. Analysis used the original-size supplied images, without upscaling or mixing in old thumbnails. Manifest key: `33828dbea43c519e69dd44396149f055a5c8fe52a9391c708be4a38991bd930e`.

## Nine aspects

| Aspect | Visual evidence and useful direction |
|---|---|
| **Lighting and shading** | Across R1–R4, broad color/value planes, darker lower or side regions, and bright edge accents make forms read as rounded or layered. These are reliable descriptions of the rendered appearance, not recovered lighting. R2 has brighter book tops and sides/page blocks; the nearby window plausibly relates to the cool bright appearance, but does not establish a light source. R3’s curtain folds use broad alternating red bands; its lectern combines bright warm trim with darker inset planes. R4’s blue body and raised keys have bright upper accents and dark lower edges against a broadly varying yellow-orange field. **Confidence: high** for the appearance; low for physical causes. `lighting_shading:O1–O9`; profile evidence below. |
| **Value and contrast** | Each image uses a different large-group relationship: dark indigo cap against cyan/blue rings (R1); saturated covers and pale page blocks against a mauve room (R2); warm lectern against a dark burgundy curtain (R3); blue-violet calculator against a bright yellow-orange ground (R4). Local separation—not uniformly high contrast everywhere—keeps the object legible. R1’s blue-on-cyan boundaries and some R2 mauve/cover boundaries have less value separation. Whole-frame linear-Y median is lowest for R3 (0.04427) and highest for R4 (0.55769); these are frame statistics, not object-only values. **Confidence: high** for pixel quantiles, moderate for perceptual hierarchy. `value_contrast:O1–O4`; `raw_evidence/R1_whole_frame_summary.json` through `R4_whole_frame_summary.json`. |
| **Color palette** | There is no single required palette. The cap uses navy/indigo, golden-orange accents, and a saturated cool field; books vary blue, magenta, and green with warm cream pages; the lectern is honey/orange wood against burgundy; the calculator is blue-violet with cyan keys against yellow-orange. In every case, the subject/background relationship is more reusable than the exact colors. The top-six fixed-bin whole-frame shares are backdrop-sensitive: for R1 the two largest blue/cyan bins account for 64.5%; for R4 the two yellow bins account for 66.0%. R2’s top six cover only 36.65% of pixels. These values must not be mistaken for subject palettes. **Confidence: high** for visible colors, limited for whole-frame palette summaries. `color_palette:O1–O7`; corresponding whole-frame summary files. |
| **Composition and hierarchy** | The examples deliberately differ: R1’s large diagonal cap floats with circular graphic space around it; R2’s stepped book stack sits on a tabletop in a room; R3’s narrow upright lectern and microphone are staged against curtain and floor; R4’s tilted calculator sits amid a repeating π pattern. The main subject is often prominent, but neither universal centering nor one scale/crop is supported. S1’s card grid describes interface layout, not art composition. **Confidence: high** for these four visible arrangements; no product-wide rule inferred. `composition_hierarchy:O1–O7`. |
| **Shape and proportions** | Preserve each object’s identity-bearing parts and their relationships: cap plate over short crown, button/cord/bead/tassel; three overlapping books with exposed pale page blocks and colored covers; lectern rim, framed inset, tapered body, base, and separate microphone; calculator recess/display and raised keypad with distinct operator keys. Rounded corners, beveled edges, and simplified transitions recur, but proportions remain object-specific. **Confidence: moderate** for the shared simplification tendency, high for listed visible parts. `shape_proportions:O1–O7`. |
| **Viewpoint and depth** | R1, R2, and R4 expose top surfaces; R3 is closer to a frontal presentation with restrained upper surfaces. Overlap and support cues establish local depth: cap over crown, books in a stack on a table, lectern on floor, calculator above a neighboring dark region. There is no dependable shared vanishing point or calibrated camera model. **Confidence: high** for overlap/support, moderate for qualitative viewpoint. `viewpoint_depth:O1–O9`. |
| **Edges and linework** | Silhouettes and important part boundaries are crisp, with rounded or stepped contours and selective dark separations, bright bevel accents, or narrow colored lips. The examples do not show a uniform heavy ink outline around every form. R3’s wood-grain strokes and floor seams are content-specific; R4’s keypad glyphs are functional detail; R1’s bevel transitions are shading boundaries, not necessarily drawn strokes. **Confidence: moderate** for the recurring selective-boundary convention. `edges_linework:O1–O5`. |
| **Surface finish** | Smooth color fields and broad gradients dominate; small crisp details and bright rim accents are selective. R3 has simplified wood-grain lines; R2 has page lines and clustered foliage. These are localized illustrative marks, not evidence of natural texture or a common brush technique. R1/R2/R4 suggest polished or glossy surfaces in places, but appearance does not establish physical material. **Confidence: high** for smooth, selectively detailed appearance; moderate for material-implying cues. `surface_finish:O1–O7`. |
| **Rhythm and staging** | Repetition is local and purposeful: stacked, differently sized books (R2); curtain folds and floor seams (R3); ordered number keys and a loose repeated π backdrop (R4). The cap’s tassel is an arrangement of parts, not a repeat motif. These patterns are not universal style requirements. **Confidence: moderate**; no instance masks or landmark measurements were made. `rhythm_staging:O1–O7`. |

## Reconciliation and limits

**Resolved from visible evidence:** R4 clearly shows a thick-looking rounded casing and raised rim; its main face, screen recess, and keys are visible. But the viewpoint observation that no *distinct side wall* establishes thickness is compatible with that appearance: the image suggests thickness through rim, bevel, and shading without exposing a clear side face. Do not turn this into a definite camera or geometry claim. `shape_proportions:O4`; `viewpoint_depth:O4`.

**Keep coupled, not artificially independent:** bright rims and broad gradients can simultaneously describe shading and finish; contrast at edges may come from color blocks, bevels, or selective contour accents. The dark regions near R2’s books and R4’s calculator are visible tonal regions, but not thereby proven cast shadows. Similarly, observed top/front faces constrain how shape reads, while not determining a unique camera.

**Subject-specific constraints, not style rules:** the four object descriptions above are individual identity requirements only when generating those subjects. The general style guidance is the clean, rounded, smoothly shaded, selectively detailed presentation—not a requirement to reuse graduation caps, book stacks, lecterns, calculator keys, π symbols, or their colors.

The category guides add staging options rather than a single composition rule: categories 1–2 describe simpler backgrounds and object/support arrangements; category 3 adds a realistic support surface and volumetric context; category 4 places a central object in realistic surroundings. Those are guide instructions, not measurements or proof that every card follows them. S1 supports collection/UI context only.

## What the tools added

Whole-frame evidence provided rendered-pixel summaries, including Y and Oklab-L quantiles, fixed-bin RGB palette shares, Oklab chroma quantiles, and Haar SWT band energy. These quantify the whole canvas; they do not segment subjects or recover material, edge quality, or artistic intent. The native-resolution evidence makes it possible to reject misleading frame-wide palette or contrast claims where background pixels dominate. It does not establish that any metric improved generation.

Two agent-chosen lighting profile probes tested candidate transitions, using linear relative luminance Y along three-pixel-wide paths:

- **LP1, R2:** from `(340,380)` to `(340,425)`, 46 samples. Y rises sharply from 0.0955 to about 0.60 by roughly y=397, then remains near 0.60 before declining slightly. The proposed shadow/lit windows have a negative median difference (−0.0102); multiple 10% and 90% crossings make a penumbra-width interpretation invalid.
- **LP2, R4:** from `(220,395)` to `(220,432)`, 38 samples. Y rises from roughly 0.02 to about 0.66, but includes intervening decreases and renewed rises. The computable 10–90% span of 16.32 px is therefore not an accepted shadow width: the sampled window mixes transitions and does not isolate a boundary.

These probes help reject unsupported measurement claims, not identify physical key/fill lighting. No accepted penumbra width, light count, physical direction, Kelvin value, roughness, or recovered camera is available. No reviewed semantic masks, subject-only color regions, or learned depth/normal/light maps were supplied. Tool use varied by role; not all nine roles ran new measurement tools. PyWavelets is recorded as module version 1.8.0 in the artifacts, while runtime distribution metadata says 1.10.0; the discrepancy remains unresolved.

## Generation brief

**Untested specification derived from this pilot; no generation or prompt-performance improvement has been demonstrated.**

Create one polished, readable illustrated card image of **[SUBJECT]** in **[CATEGORY / STAGING MODE]**. Use clean, rounded, clearly separated forms; smooth broad gradients and graphic light/dark planes to suggest volume; crisp silhouettes with selective edge accents rather than a uniform heavy outline. Keep the subject’s identity-bearing parts and their overlaps legible, with small crisp detail reserved for features that identify the object. Use a subject palette distinct from its background, but choose colors for this subject and scene rather than copying a reference palette. Preserve a composition suited to the subject—floating against a simple graphic field, supported on a surface, upright staged, or integrated into an environment—rather than forcing all subjects to the same center, angle, or scale. Keep important subject boundaries broadly sharp; do not add shallow-focus blur unless requested.

- **Subject slot:** name the object and specify its essential visible parts/part relationships.
- **Category slot:** choose simple graphic backdrop, supported object with simple backdrop, grounded object with contextual surface, or central object in realistic surroundings, as appropriate.
- **Reference roles:** use primary art references for rendering and local form cues; use category guides for staging expectations; use S1 only for collection-screen context, never as an art-only measurement source.
- **Protect:** silhouette readability, contact/overlap, required small identity details, and clear subject/background separation.
- **Vary:** palette, backdrop motif, environment, object orientation, and local surface marks to suit the new subject; do not copy the cap, book, calculator, lectern, π pattern, or their exact colors.
- **Avoid:** ubiquitous grain or hatch, uniform black outlines, forced identical centering, and unrequested lens/camera or physical-light specifications.

## Information that would unblock refinement

The coverage gap in this pilot is that it analyzed four of the 102 already available larger cards, plus S1/G1/G2; the remaining 98 available cards were not analyzed. These four examples cannot establish the full style range. Broader coverage can first use the existing local pack; 58 additional cards remain unretrieved behind the public Miro signup gate, and native-source provenance remains qualified. Do not mix in low-resolution thumbnails as substitutes. If object-only palette/contrast or shadow claims are important, obtain reviewed art/subject and relevant background-region masks, then compare like regions. For more exact technical reproduction, resolve the PyWavelets module/distribution version discrepancy; it does not alter the visual observations above.
## Evidence source key

References such as `role:O#` identify observations in the following normalized source reports. Normalization repaired input metadata only; raw responses remain preserved.

| Role | Observation IDs | Source |
|---|---|---|
| lighting_shading | O1–O11 | normalized JSON |
| value_contrast | O1–O4 | normalized JSON |
| color_palette | O1–O7 | normalized JSON |
| composition_hierarchy | O1–O7 | normalized JSON |
| shape_proportions | O1–O7 | normalized JSON |
| viewpoint_depth | O1–O9 | normalized JSON |
| edges_linework | O1–O5 | normalized JSON |
| surface_finish | O1–O7 | normalized JSON |
| rhythm_staging | O1–O7 | normalized JSON |

Tool evidence: LP1_profile · LP2_profile · R1_whole_frame_summary · R2_whole_frame_summary · R3_whole_frame_summary · R4_whole_frame_summary · lighting_probe_statistics.

Frozen manifest · runtime qualification · report validation · capture provenance.
