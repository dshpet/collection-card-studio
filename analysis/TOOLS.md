# Evidence

What a reviewer can rely on, and how far.

| Source | Gives | Kind | Limit |
|---|---|---|---|
| `scripts/measure.py` | Fields per card, from pixels and the subject mask | Measured | Masks are model estimates and can miss thin parts |
| BiRefNet | Subject mask | Model estimate | Spot-check: 3 of 24 hard masks were incomplete |
| Marigold | Normals, shading | Model estimate | Trained on photos. Shading leaks color |
| Depth Anything 3 | Relative depth | Model estimate | Not meters |
| DeepGaze IIE | Predicted attention | Model estimate | Trained on photos, unvalidated on this art |
| DINOv3 | Real-vs-generated classifier | Model estimate | Picks up content too, unless cards are twins |
| `scripts/drift.py` | Field percentiles of a batch against real cards | Measured | Trust it for a batch, not a single card |
| `scripts/review.py` | Specialist findings, art director | Rated | Wrong without lessons: see below |

Model raters are not neutral. Without labelled lessons they chose the real card as the fake on color and surface in every pair, because they expect game art to be glossier and more saturated than it is. Never read a rating of this style without a calibration on twins.

Reference cards are 430×480, so nothing finer than about 2 px is evidence.
