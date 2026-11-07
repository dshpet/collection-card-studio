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
| Pairwise director (`choose()`) | Which of two drawings is closer to the real cards | Rated | Agrees with the producer 61% of the time, 76% when confident |
| CSD against the same object's real card | Style closeness with content held equal | Measured | Needs a real card of the same object, so only twins |
| SigLIP 2 (`scripts/search.py`) | Which real cards show a phrase, with a confidence | Model estimate | Confidence is near 0 for objects no real card shows |
| SAM 3 (`scripts/cast.py`) | Cutouts of the cast, by name | Model estimate | Misses a character hidden under a costume or a blanket |

Model raters are not neutral. Without labelled lessons they chose the real card as the fake on color and surface in every pair, because they expect game art to be glossier and more saturated than it is. Never read a rating of this style without a calibration on twins.

Reference cards are 430×480, so nothing finer than about 2 px is evidence.
