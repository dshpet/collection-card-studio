# Reference-specific feasibility: measuring and controlling visual style

## Evidence base and limits

The reference set supports a **qualitative, category-aware style brief** and a human-reviewed prompt/evaluate/edit loop. It is not a reliable basis for calibrated numerical style targets: the individual crops are only about 59 × 67 pixels, too small to separate rendering traits from image content or crop artifacts with confidence.

The collection overview, `/home/dshpet/Dev_Projects/playrix_testtask/materials/summer_collection.png`, is 733 × 807 pixels; the category sheets `/home/dshpet/Dev_Projects/playrix_testtask/materials/art_categories_1_to_3.png` and `/home/dshpet/Dev_Projects/playrix_testtask/materials/art_categories_4_and_5.png` are each 733 × 1034 pixels. The reviewed individual crops are 59 × 67 pixels, except the fruit crop, which is 58 × 67. These dimensions were checked locally with `file`. The gallery identifies its references as reduced-resolution crops; visual inspection here is constrained by their small size.

The category sheets and `/home/dshpet/Dev_Projects/playrix_testtask/materials/03_art_guide.md` explicitly define the composition progression: category 1 floats an object against a simple background; category 2 places it on a surface against a simple vertical backdrop; category 3 grounds it on a realistic surface; category 4 integrates it into a realistic setting while keeping it central. The examples support a bright, polished, dimensional illustration style with a legible focal object, but do not establish exact production-resolution rendering parameters.

## Which axes are useful now

**High-value qualitative axes for human annotation and review**

- **Focal-object prominence and silhouette legibility.** These are visible even at crop scale. The graduation cap (`/home/dshpet/Dev_Projects/playrix_testtask/materials/card_examples/3458764679576006333.png`), calculator (`…/3458764679576006337.png`), and drink (`…/3458764679576006385.png`) each read as a distinct main object.
- **Composition and environmental context.** Annotate whether the object floats, rests on a simple surface, has realistic surface contact, or is integrated into a scene. The books/window crop (`…/3458764679576006335.png`), fruit on tabletop (`…/3458764679576006387.png`), and fan in a room-like setting (`…/3458764679576006389.png`) show visibly different context levels. The category sheets are the stronger evidence for category definitions.
- **Relative background complexity and object/background separation.** This is useful as a coarse judgment, especially when conditioned on category. The striped backdrop behind the air conditioner (`…/3458764679576006383.png`) is visibly simpler than the room-like fan setting (`…/3458764679576006389.png`).
- **Broad rendering consistency.** Review whether images appear like polished, colorful, dimensional illustrations, whether the main object has a coherent light/shadow treatment, and whether the object remains more salient than its backdrop. These are appropriate qualitative checks, not measured reference values.
- **Within-set object diversity and thematic relevance.** The summer overview shows distinct named themes and varied objects. This is useful for judging whether a proposed set has both recognizable subtheme coherence and object variety, but individual thumbnail details are too small for a comprehensive inventory.

**Weak, unreliable, or currently unobservable axes**

- Do not infer exact palette targets, color-distribution statistics, saturation limits, material labels, edge softness, texture frequency, light direction, shadow strength, or object-occupancy percentages from the tiny crops. At this size, resampling, compression, crop boundaries, and the chosen object can dominate those observations.
- Exact geometry, small-detail density, fine brush/texture behavior, and subtle material distinctions are not dependable. For example, the small drink crop cannot support a robust distinction between glass, liquid, garnish, and highlights as style features independent of the depicted drink.
- The overview’s colored frames and set headers are UI/presentation elements, not evidence of the illustration’s object palette or a rarity-to-visual-style mapping.
- Rarity-linked rendering differences, numerical thresholds, and reliable automated scores are not established by these references. The user-supplied brief separately requires rarity not to alter object visuals; visual inspection of the overview cannot verify that rule.

## Shared style versus content-specific appearance

Treat **style constraints as shared** across object identities: a clear focal silhouette, polished dimensional illustration, visually coherent lighting and shading, strong subject/background separation, and compact readable composition. These are broad observed tendencies and practical targets, not exact numeric specifications.

Treat **object shape, local palette, and material as content-dependent**. A calculator, books, drink, fruit, fan, and air conditioner necessarily differ in geometry, color, and surface. Matching their individual colors or shapes across generations would confuse object identity with style. Compare rendering treatment only where the crop provides evidence, and avoid a shared palette target inferred from the heterogeneous examples.

Background and composition constraints must be **category-conditioned**, not averaged across all cards. The category sheets explicitly support simple backdrops in categories 1–2, realistic surface grounding in category 3, and an integrated but subordinate setting in category 4. Category 5 is a character-led mini-scene in the category-4 setting and should not be used as a style proxy for non-gold object cards.

## Reference → prompt → evaluate → axis-specific edit

A feasible loop at the present reference quality is qualitative:

1. **Reference:** Choose several references that match the intended category and broad object type where possible. Record which parts are observed style versus object-specific appearance.
2. **Prompt:** State the set theme and object identity, then separately specify category-conditioned composition and shared style traits. Avoid asking for an exact palette, texture, or numerical feature match unsupported by the references.
3. **Evaluate:** Compare the result with the reference on a short annotated checklist: focal-object clarity, category fit, context/background complexity, subject-background separation, and broad rendering consistency. Review at intended card size, not only enlarged.
4. **Edit one axis at a time:** If the object is unclear, request a simpler/larger focal silhouette; if category is wrong, revise support/surface/setting; if the scene competes with the object, reduce background detail. Do not use an object-specific color mismatch as evidence of a shared style failure.

This can support **axis-specific human critique**, but not validated numeric optimization from these crops. No feature extraction or numerical measurement is claimed.

## Annotation, crop, and confidence recommendations

For each reference, record:

- exact source path and, if available, set/card identity;
- category (1–4; category 5 kept separate);
- main object identity and whether any secondary objects are part of the focal grouping;
- composition/context: floating, simple support plus vertical backdrop, realistic grounding surface, or integrated setting;
- background complexity and whether it competes with the subject;
- focal-object legibility and subject/background separation;
- broad rendering observations, with content-specific palette/material notes kept separate;
- crop quality, visible frame/border intrusion, and confidence for each judgment.

For later, higher-resolution assessment, use clean card-only crops with consistent boundaries, preserving the full illustration while excluding frame, labels, stars, and UI. Keep a parallel uncropped original and record crop coordinates. Do not estimate style from crops whose borders include neighboring cards or UI, or from rescaled thumbnails without noting resampling.

Use **high confidence** only for directly visible coarse properties such as the main object and broad category composition when unambiguous; **medium confidence** for broad rendering and background-complexity judgments; **low confidence** for palette/material nuance, small details, lighting subtleties, or anything affected by tiny size or uncertain crop boundaries. The reviewed tiny crops are generally suitable for coarse object and composition judgments, not fine style annotation.

## Missing reference data for stronger measurement

Needed later: higher-resolution card artwork without surrounding UI, consistent crop bounds, the full set of cards with set/card/category labels, and examples spanning each category and varied object identities. If the intended task requires shared-style comparison, paired examples of visually different objects rendered in the same style—and preferably repeated objects across styles—would help disentangle style from content. Current materials do not provide sufficient evidence for calibrated numerical targets or confident fine-grained style axes.
