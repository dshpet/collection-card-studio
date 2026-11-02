# What the references show

All 160 cards and 16 sets of one summer collection, rated by four vision models (Codex, Claude, Qwen, Gemma) and measured from pixels, subject masks, depth, shading and predicted attention. Numbers are counts out of 160 cards unless stated. The generator reads this through `knowledge.json` and `scripts/style.py`.

Rater counts below are what models said, not what the cards are. Blind tests later showed the raters expect game art to be rounder, glossier and more saturated than it is: see [STYLE_GAPS.md](STYLE_GAPS.md). Where a rated claim and a twin comparison disagree, the comparison wins.

## The style that never changes

- **Render:** soft or glossy 3D in 154 cards, with soft gradients on all 160. A polished hero often sits on a flatter backdrop (87 cards).
- **No outlines:** 154 cards. Form comes from shading.
- **Shapes:** raters said round and soft in 133 and chunky in 136, but that is rater bias. Beside redraws of the same objects, real cards keep true proportions, slim parts and small soft bevels. They are simplified, not inflated.
- **Surfaces:** smooth and calm. Raters said little texture in 132, yet materials stay readable: stitching, grain and seams exist, small and quiet.
- **Colour:** saturation 4–5 of 5 in 156. Backgrounds are as saturated as subjects.
- **Hero against background:** opposing hues, strongest in Category 1 (142° apart, against 98° for shuffled pairs).
- **Shadows stay colourful:** the darkest quarter of a subject keeps 95% of its chroma. Dark means rich indigo or crimson, not black or grey.
- **Camera:** eye level or slightly above in 145, three-quarter view in 127.
- **Framing:** centred in 135. The subject's box spans about 83% × 76% of the card, though its silhouette covers only 33% of the area. 42 cards touch an edge.
- **Attention:** 86% of predicted gaze lands on the subject. A content-free average map already scores 75%, so most of this reflects central framing.
- **Light:** from above in 155 cards. Normal maps split evenly between left and right, so the raters' "upper left" is a habit, not a rule.

## What changes by category

- **Category 1 (35):** always floating, with no ground. Most are tilted. Backdrops are tone-on-tone rays, rings or stripes.
- **Category 2 (20):** upright on a plain coloured ledge (17 of 20) with a cast shadow. Backdrops are the most saturated. Raters never fully agree on this category, so the surface field below is the reliable test.
- **Category 3 (32):** on a real material such as wood, sand or grass (23 of 32). The backdrop stays graphic.
- **Category 4 (42):** a real environment, usually outdoors, with a few supporting objects.
- **Category 5 (31):** characters in dynamic poses with comic timing. Ten of these are the all-gold grand set, Summer Party. The rest come from one recurring cast and sit late in their sets.

## How a set is built

- **Names:** 13 titles are one word and 3 are two words. Card names are one or two words.
- **Topics:** six activities, five places, three events, one group and one mood.
- **Picks:** every set rates 4–5 of 5 for obviousness: the first things anyone would name.
- **Sets share a look as well as an idea.** Regular sets average 0.62 style similarity against 0.57 for random cards, partly through shared ground materials such as sand, lawn or deck.
- **Variety is not engineered.** Background hues per set (6.7) barely beat random draws (6.5), so a set's colours are about what chance gives. Object classes range from 4 to 9.
- **Category mix is uneven:** Category 2 appears only 1–3 times per set, when it appears at all.
- **Models for the movie sets:** Sports, Finals, Coolness and Countrystead have no characters and no gold frames. Amusement has no characters, but three objects carry gold frames.

## What the embeddings group by

- **DINOv2:** object family, such as music gear, sports balls, drinks and paper items.
- **SigLIP 2:** closest to the sets, but still weak (0.29).
- **CSD:** staging, not style differences (0.43 with category).
- **Subject only:** SigLIP 2 and CSD density clusters simply split characters from objects.
- **No natural families:** the best silhouette is 0.24. The cards form a continuum, not distinct groups.

## How far to trust this

- Raters agree on 70–79% of choice fields, and within one point on 97–99% of scales. Mean κ is 0.41–0.53.
- **Most reliable:** backdrop pattern (κ 0.88), support, object class, tone, surface kind, art category and background type (κ 0.76–0.83).
- **Weak:** subject-versus-background contrast, light direction, rim light, margin and value key (κ below 0.2).
- **Constant fields** are kept as style invariants, but they are unproven as checks, because all 160 cards are positives. Off-style controls test them.
- **Agreement is not truth.** All four raters shared the same wrong expectation, so their agreement could not reveal it.
- A fresh reviewer's spot check of 38 cards found 8 wrong, mostly rings read as rays, which the new pattern field addresses, and surfaces misjudged.
- Reviewers found 3 of 24 hard masks incomplete: Park Gate, Pool Bar and Adventure.
- Shading maps leak some colour. DeepGaze learned from photos, so it is unvalidated on this art.
- The sky, sand and lawn reflect this summer collection, not the franchise. No art director has checked these ratings, and 430×480 limits conclusions about fine texture.
