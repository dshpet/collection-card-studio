# What the references show

All 160 cards and 16 sets, rated by four vision models (Codex, Claude, Qwen, Gemma) and measured from pixels, subject masks, depth, shading and predicted attention. Numbers below are counts out of 160 cards unless stated.

## The style that never changes

- **Render:** soft or glossy 3D in 154 cards, with soft gradients in all 160. It is not a flat painted style, which corrects the earlier four-card brief.
- **No outlines:** 154 cards. Form comes from shading.
- **Shapes:** round and soft in 133, chunky in 148.
- **Surfaces:** clean, with little texture in 142.
- **Colour:** saturation 4–5 of 5 in 158. Warm and cool colours are mixed in 140. Backgrounds are as saturated as subjects.
- **Value:** bright overall, and deep shadow is rare. About 1% of a typical subject is dark.
- **Camera:** eye level or slightly above in 145, three-quarter view in 127.
- **Framing:** centred in 135. The subject covers about 33% of the card (23–47%) and comes within 5% of an edge.
- **Attention:** 85% of predicted gaze lands on the subject, in 33% of the area. The peak sits at the card centre, and higher on character cards, where it finds faces.
- **Light:** from above. Normal maps put it in the upper half in 155 cards. Raters say upper left, but they agree poorly on this.

## What changes by category

- **Category 1 (35):** always floating, with no ground shadow. Most are tilted. Backgrounds are rays, motifs or stripes, with the strongest colour separation.
- **Category 2 (20):** upright on a surface with a cast shadow. This is the rarest category and has the most saturated backgrounds.
- **Category 3 (32):** on a real surface, but the background stays graphic: rays, gradient or stripes.
- **Category 4 (42):** a real environment, usually outdoors, with a few supporting objects.
- **Category 5 (31):** characters in dynamic poses with comic timing, and about twice the hue variety.

## How a set is built

- **Names:** 13 titles are one word and 3 are two words. Card names are one or two words.
- **Topics:** six activities, five places, three events, one group and one mood. All 16 are plain topics.
- **Picks:** every set rates 4–5 of 5 for obviousness: the first things anyone would name.
- **Variety is deliberate:** each set uses 5–8 background hues and usually 6 object classes, mixing small objects with vehicles and buildings.
- **Sets hold together by idea, not look.** Style similarity within a set is 0.57–0.74, against 0.57 for any two cards.
- **Category mix is uneven:** Category 2 appears only 1–3 times per set, when it appears at all.
- **No-gold models:** Sports, Finals, Amusement, Coolness and Countrystead have no character cards. They are the closest templates for the movie sets.

## What the embeddings group by

- **DINOv2:** object family, such as music gear, sports balls, drinks and paper items.
- **SigLIP 2:** closest to the sets, but still weak (0.29).
- **CSD:** staging, not style differences (0.43 with category).
- **Subject only:** SigLIP 2 and CSD density clusters simply split characters from objects.
- **No natural families:** the best silhouette is 0.24. The cards form a continuum, not distinct groups.

## How far to trust this

- Raters agree on 70–79% of choice fields, and within one point on 97–99% of scales. Mean κ is 0.41–0.52.
- Most reliable: support, object class, category, background type and humour (κ above 0.75).
- Weak: subject-versus-background contrast, light direction, rim light, margin and value key (κ below 0.2).
- Two fields carry no information. Recognizability is 5 and shading model is soft gradient on every card.
- The 48 hardest and lowest-scoring masks were checked by eye and look right. The rest were sampled, not all inspected.
- DeepGaze learned from photos, so its attention maps on stylised art are unvalidated, and they include a built-in pull toward the centre.
- No art director has checked these ratings, and 430×480 limits conclusions about fine texture.

## What this means for generation

- Show the look with category-matched reference cards, and keep prompts short: subject, category, background type and colour.
- Plan sets as plain topics with obvious, varied objects, modelled on the five no-gold sets.
- Rate generated cards with the same form and compare them with these ranges.
