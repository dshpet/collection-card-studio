# Fix round 1

After the first draw ([final3](../final3/README.md), every set 4 of 5), this round redraws only the cards the producer commented on. Each folder was started with `make_set.py --keep <first-draw run>`: unchanged cards keep their drawings and picks, and only changed cards are drawn (eight candidates), picked and reviewed.

| Set | Folder | Plan | Kept from |
|---|---|---|---|
| Western | `western/` | `runs/plans/final-western-2.json` | `final3/western` |
| Period Drama | `period-drama-2/` | `runs/plans/final-period-drama-4.json` | `period-drama/`, itself kept from `final3/period-drama-2` |
| Detective | `detective/` | `runs/plans/final-detective-4.json` | `final3/detective-3` |
| Cast bonus | `cast/` | `runs/plans/final-cast-2.json` | `final2/cast` |

## What changed, by the producer's comments

| Card | Grade | Comment | Change |
|---|---|---|---|
| Windmill | 3 | "Looks like a monument. Maybe add a recognizable field of wheat beneath? Is the structure correct?" | No: a farm wind pump stands on an open lattice tower. A new Blender model with four braced legs, in a wheat field |
| Campfire | 4 | set: "somewhat off" | The cabin and the large plum pot are gone; logs in a cone, a small blue enamel pot at the edge |
| Covered Wagon | 4 | set: "should have its own nature background" | Its own scene, a dirt trail across the prairie; same model |
| Top Hat | 5 | picked candidate 4 | Candidate 4 |
| Hat Box | 5 | set: "too american... would not be recognized easily" | Redrawn rose pink with a bow and a bonnet on the lid (`period-drama/`); still "just a strange object", so replaced by the Candelabra, the producer's choice of four proposals, modelled in Blender (`period-drama-2/`) |
| Pocket Watch | 2 | "should be more centered as the point of visual attention" | Hangs from a chain that leaves the top of the card; the blockout frames the case alone, centered, 1.2 times larger after the first three candidates came out small |
| Folding Fan | 3 | none | Red silk read Asian, as the hat box read American: a pale pink European fan with a lace edge |
| Flash Camera | 3 | "should be more centered"; set: "off-center of the circular back... Use other back" | Diamonds instead of rings; the blockout centers on the body (`k.focus`) with a smaller flash |
| Magnifier | 3 | "Perspective looks a bit off" | The lens faces the viewer, 12 degrees off instead of 46 |
| Fedora | 3 | "Is it floating? The shadow seems kinda strange" | Floats on purple waves, as the Cowboy Hat and Top Hat that got 5 |
| Badge Wallet | 2 | "Not a very recognizable badge... add more details" | Police Badge: shield, eagle, blue enamel center with a star, blank banner, ID card; new model |
| Evidence Bag | 3 | "The ring looks not inside the bag" | Highlights and creases run across the ring; a blank label; a sage green desk pad |
| Steel Safe | 3 | "A little too glossy" | Matte paint; same model |
| Doorknob Print | 3 | set: "kinda meh as an object" | Replaced by the Trench Coat on a wall hook |
| Bloodhound | 3 | "Not sure if this could be an object"; set: "looks like a character" | Replaced by the Handcuffs, modelled in Blender |
| Grand Ball | 4 | "Too much blush on the sheep" | Redrawn with a note against blush. The game's sheep has a faint blush of its own; the new drawings keep about that much, where the first draw painted it larger and brighter |
| Cake Clue | 3 | "Too texture'y" | Redrawn with a note for smooth surfaces |
| Hoofprint Clue | 2, broken | "Sheep is too blushed again. The cow has the 3rd leg behind"; set: "Detectives use magnifiers in both" | Barn Detectives: the cow dusts a milk can for prints, the sheep takes notes, both upright |

Unchanged although graded 3 without a comment: Cake Stand, Piano, Squad Car.

## Results

Every changed card drew eight candidates, picked pairwise, then one review; an edit stayed only if it beat its draft (kept: Wagon, Windmill; Magnifier, Fedora, Steel Safe; Grand Ball; Folding Fan). Two picks were set by hand:

- Top Hat: the producer's pick from the first draw.
- Windmill: the kept edit had smoothed the wheat into plain golden dunes, against the producer's ask for a recognizable wheat field, so its draft stands (`picked_by` in `western/check.json`).

Left as drawn: every Campfire candidate drew a log cabin at the edge although the plan names a pine clearing; the pick keeps it small. The Police Badge has its emblem but sits small in its wallet, as the model framed it. The Candelabra failed the automatic check on all eight candidates, on its thin silhouette and teal backdrop, not on how it looks. The sheep keeps a faint blush: the game's own sheep has one, so the lesson asks for no more than the cutout's.

| Set | Object classes | Scale classes | Backdrop hues | Style similarity |
|---|---:|---:|---:|---:|
| Real sets, range | 4-7 | 2-5 | 6-7 | 0.603-0.641 |
| Western, fix 1 / first draw | 7 / 7 | 5 / 5 | 6 / 6 | 0.554 / 0.552 |
| Period Drama, fix 1 / first draw | 7 / 6 | 2 / 2 | 6 / 7 | 0.551 / 0.556 |
| Detective, fix 1 / first draw | 6 / 8 | 4 / 4 | 8 / 7 | 0.471 / 0.543 |

`compare.json` from `scripts/compare.py --sets runs/final4/sets.json`. Detective's new colors (coral red, sage green) make its cards less alike than before and than any real set.

Pipeline changes from this round: `make_set.py --keep` and a plan card's `note`; `k.focus` in `scripts/blockout.py`, which frames a blockout on its main body; ten new planner rules in `analysis/lessons.md`, accepted by the producer.

The producer's grades of this round and the next fixes: [final5](../final5/README.md).
