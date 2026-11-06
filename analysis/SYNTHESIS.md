# What the references show

All 160 cards and 16 sets of one summer collection, rated by four vision models (Codex, Claude, Qwen, Gemma) and measured from pixels, subject masks, depth, shading and predicted attention. Numbers are counts out of 160 cards unless stated. The generator reads this through `knowledge.json` and `scripts/style.py`.

Rater counts below are what models said, not what the cards are. Blind tests later showed the raters expect game art to be rounder, glossier and more saturated than it is: see [STYLE_GAPS.md](STYLE_GAPS.md). Where a rated claim and a twin comparison disagree, the comparison wins.

## The style that never changes

- **Render:** soft or glossy 3D in 154 cards, with soft gradients on all 160. A polished hero often sits on a flatter backdrop (87 cards).
- **No outlines:** 154 cards. Form comes from shading.
- **Shapes:** raters said round and soft in 133 and chunky in 136, but that is rater bias. Beside redraws of the same objects, real cards keep true proportions, slim parts and small soft bevels. They are simplified, not inflated.
- **Surfaces:** smooth and calm. Raters said little texture in 132, yet materials stay readable: stitching, grain and seams exist, small and quiet.
- **Colour:** saturation 4–5 of 5 in 156. Backgrounds are as saturated as subjects.
- **Hero against background:** opposite temperature, not strict complements. A warm hero sits on a cool backdrop on 84% of cards, and a backdrop near the hero's own hue is rare (4% within 30°, against 14% shuffled). Details in [STYLE_GAPS.md](STYLE_GAPS.md), Backdrop colors.
- **Shadows stay colourful:** the darkest quarter of a subject keeps 95% of its chroma. Dark means rich indigo or crimson, not black or grey.
- **Camera:** eye level or slightly above in 145, three-quarter view in 127.
- **Framing:** centred in 135. The subject's box spans about 83% × 76% of the card, though its silhouette covers only 33% of the area. 42 cards touch an edge.
- **Attention:** 86% of predicted gaze lands on the subject. A content-free average map already scores 75%, so most of this reflects central framing.
- **Light:** from above in 155 cards. Normal maps split evenly between left and right, so the raters' "upper left" is a habit, not a rule.

## What changes by category

- **Category 1 (35):** always floating, with no ground. Most are tilted. Backdrops are tone-on-tone rays, rings or stripes.
- **Category 2 (20):** upright on a plain floor in the wall's colour, with no front edge or material (17 of 20 by eye), and a cast shadow. Backdrops are the most saturated. Raters never fully agree on this category, so the surface field below is the reliable test.
- **Category 3 (32):** on a real material such as wood, sand or grass (23 of 32). The backdrop stays graphic.
- **Category 4 (42):** a real environment, usually outdoors, with a few supporting objects.
- **Category 5 (31):** characters in dynamic poses with comic timing. Ten of these are the all-gold grand set, Summer Party. The rest sit late in their sets, mostly in gold frames, though Music Fest shows two without. 30 of the 31 show one cast: a stocky man with glasses and a mustache (14 cutouts), a pig (9), a sheep (5), a cow (4) and a rooster (5), in a new outfit on almost every card. A one-character card's figure spans about 70% × 68% of the card, centred, and the bottom edge cuts it on 10 of 23 (`analysis/cast.json`).

## How a set is built

- **Names:** 13 titles are one word and 3 are two words. Card names are one or two words.
- **Topics:** six activities, five places, three events, one group and one mood.
- **Picks:** every set rates 4–5 of 5 for obviousness: the first things anyone would name.
- **Sets share a look as well as an idea.** Regular sets average 0.62 style similarity against 0.57 for random cards, partly through shared ground materials such as sand, lawn or deck.
- **Variety is not engineered.** Background hues per set (6.7) barely beat random draws (6.5), so a set's colours are about what chance gives. Object classes range from 4 to 9.
- **Category mix is uneven:** Category 2 appears only 1–3 times per set, when it appears at all.
- **Models for the movie sets:** Sports, Finals, Coolness, Countrystead and Gardens have no characters and no gold frames. Amusement has no characters, but three objects carry gold frames.

## What the embeddings group by

- **DINOv2:** object family, such as music gear, sports balls, drinks and paper items.
- **SigLIP 2:** closest to the sets, but still weak (0.29).
- **CSD:** staging, not style differences (0.43 with category).
- **Subject only:** SigLIP 2 and CSD density clusters simply split characters from objects.
- **No natural families:** the best silhouette is 0.24. The cards form a continuum, not distinct groups.
- **No outliers to drop:** within each category, local outlier factors stay at or below 1.44 in CSD, DINOv2 and SigLIP 2, and the spaces disagree on which cards are odd. The most flagged (Aircon, Rock Guitar, Podium) are on-style cards with unusual staging. Off-style work is caught one level up: a drawn card must sit near some real card in CSD, a floor that rejected all six wrong-style controls.

## Second pass, 2026-11-06

Two fresh reviewers went over all 160 cards, one for object choice and one for art logic, against the planner's rules and our 60 cards. The author checked the main claims against the card list and by eye. Tags: measured from pixels, rated by the models' labels, or read by eye.

What the sets choose:
- **Made things at object size (eye).** Wild nature appears on 4 of 129 object cards (Palm Tree, Coral Reef, Jellyfish, Seahorse), and no card shows a landform or a sky body. Our plans had about one in six.
- **A place is shown by its signature object (eye).** The motel is its neon sign, the fuel stop a pump, the house a door with a wreath. The Lighthouse is the only whole building. Our plans had 13.
- **Contents and partners (eye).** 15 of 19 containers are open and filled, and about 22 more cards pair a tool with what completes it: mitt and ball, map and magnifier. Pairs are drawn as pairs: sneakers, flip-flops, flippers, gloves.
- **Category follows how the object exists (eye, 74 of 129).** Fliers and swimmers float in their own sky or water, food and drink stand on a surface, vehicles stand on their own ground, built things sit in place. A quarter of category 4 cards show a small object where it is used, such as a ball on the pitch.
- **Words become pictograms (eye).** About 16 cards keep sign, ticket and book objects, with icons for the words.
- **Slot order is rarity (in-game screenshots).** Stars rise with the slot in 15 of 16 sets, gold cards come last, and categories are mixed.
- **The game's emblem (eye).** A house icon or a cow head sits where a label would be on 9 cards in 8 sets.

How they are drawn:
- **Category 4 is the object's exact spot, close (eye).** About 20 of 42 show no sky. 17 of 42 are cut by the card's edge, against 2 of 13 of ours (measured).
- **Three-quarter view, even when symmetric (measured).** A near-mirror silhouette occurs on 14 of 67 real cards in categories 1 and 3, against 9 of 17 in our batch.
- **A pool of light behind the object (measured).** On ledges and surfaces the backdrop beside the object is brighter than the corners by more than 5 L* on 39 of 52 real cards, against 11 of 23 of ours.
- **Flat objects seen from above (eye).** Map, Travel Book, Fruit Plate, Tennis and Binoculars lie on a surface that fills the card. Raters labelled most of them stripes, so they were attached as references to upright cards: the batch rocket got three.
- **Detail (measured).** Category 1 subjects are the plainest. The art guide says category 2 has no small details, but its subjects are the most detailed.
- **Data note (eye).** Some card names do not match their pictures: Poolside's Swim Ring shows flip-flops, its Lifeguard Tower shows sunscreen, and Beach's Sunblock shows a lifeguard chair.

The producer's calls, 2026-11-06:
- **No wild nature, as on the real sets.** A single plant or animal with a clear silhouette may stay, so the Cactus is kept. Mesa, Ringed Planet and Comet are dropped, though they were graded 5.
- **Night and dusk skies are allowed for dark topics such as horror.** Real evening scenes (13 of 73, eye) use a rich royal blue sky with small stars and a crescent moon, or violet turning pink at the horizon. They are never black, and a warm light in the scene carries them: lit windows or a glowing sign.
- **One object per set may carry the game's emblem, as on 8 of 15 real sets.** It goes where a brand or stamp would sit and is drawn from words alone: a house or cow-face pictogram. The brief neither asks for it nor rules it out.

Not adopted: close framing of character cards, which rested on only three of our cards.

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
