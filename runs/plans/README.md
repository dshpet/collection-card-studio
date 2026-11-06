# Draft plans

Plans for the final film sets, made by the current planner on 2026-11-05 and not yet drawn. Pick or edit one, then draw it with `make_set.py "<Theme>" --plan runs/plans/<file>.json --run <genre>-final`.

Category in brackets; M marks a card that gets a Blender model first.

## western.json: Western

Default rule: variants share at most 5 objects.

- **Variant 1:** Cowboy Hat [1], Cowboy Boot [1], Sheriff Star [1], Saddle [2 M], Horseshoe [3], Lasso [3], Coffee Pot [3], Red Barn [4 M], Log Cabin [4 M], Cactus [4]
- **Variant 2:** Tumbleweed [1], Spurs [1 M], Cowboy Hat [1], Barrel [2], Cowboy Boot [2], Hay Bale [3], Water Well [3 M], Windmill [4 M], Steam Train [4 M], Red Mesa [4]
- **Variant 3:** Gold Nugget [1], Gold Pan [1], Oil Lantern [1 M], Tin Cup [2], Harmonica [2], Mine Cart [3 M], Cooking Pot [3], Campfire [4], Gold Mine [4 M], Horse [4]

## western-cast.json: Western

One character card per variant (`--cast 1`).

- **Variant 1:** Cowboy Hat [1], Cowboy Boot [1], Sheriff Star [1], Cactus [2], Saloon Doors [3 M], Horse [3], Barrel [3], Covered Wagon [4 M], Windmill [4 M], Lasso Mix-up [5]
  - *Lasso Mix-up:* The man in a cowboy hat swings a rope lasso and has accidentally caught the cow around her horns, who looks surprised.
- **Variant 2:** Lasso [1], Horseshoe [1], Bandana [1], Coffee Pot [2], Saddle [3 M], Hay Bale [3], Wagon Wheel [3 M], Red Barn [4 M], Campfire [4], Rooster Rodeo [5]
  - *Rooster Rodeo:* The rooster in a tiny cowboy hat crows on a hay bale while the sheep sits nearby wearing a red bandana.
- **Variant 3:** Prickly Pear [1], Tumbleweed [1], Spurs [1], Lantern [2 M], Gold Pan [3], Mine Cart [3 M], Roadrunner [3], Mine Entrance [4 M], Steam Train [4 M], Gold Find [5]
  - *Gold Find:* The pig in a prospector hat holds up a giant gold nugget and grins while a pickaxe-free pan sits at its feet.

## sci-fi.json: Sci-Fi

Default rule.

- **Variant 1:** Rocket [4 M], Flying Saucer [1 M], Space Helmet [1], Ringed Planet [1], Satellite [1 M], Control Panel [2 M], Telescope [3 M], Jetpack [3 M], Moon Rover [4 M], Space Station [4 M]
- **Variant 2:** Time Machine [4 M], Teleport Pod [3 M], Hologram Globe [1 M], Hoverboard [1], Atom Model [1 M], Microscope [3 M], Energy Cell [2], Hover Car [4 M], Radar Dish [3 M], Bubbling Flask [3]
- **Variant 3:** Space Shuttle [4 M], Comet [1], Moon [1], Spiral Galaxy [1], Meteorite [3], Space Boots [3], Space Capsule [3 M], Space Helmet [2], Flying Saucer [4 M], Lunar Base [4 M]

## sci-fi-shared.json: Sci-Fi

Variants keep the most iconic objects (experiments/shared_plans.py).

- **Variant 1:** Rocket [1 M], Flying Saucer [1 M], Ringed Planet [1], Space Helmet [2], Satellite [3 M], Telescope [3 M], Moon Rover [3 M], Space Station [4 M], Observatory [4 M], Moon Base [4 M]
- **Variant 2:** Rocket Launch [4 M], Flying Saucer [4 M], Ringed Planet [1], Space Helmet [1], Jetpack [1 M], Atom Model [2 M], Control Console [3 M], Glowing Flask [3], Time Machine [3 M], Teleporter [4 M]
- **Variant 3:** Ringed Planet [1], Comet [1], Space Capsule [1 M], Rocket [2 M], Flying Saucer [3 M], Space Helmet [3], Moon Rover [3 M], Radar Dish [4 M], Space Station [4 M], Observatory [4 M]

## horror.json: Horror

Default rule.

- **Variant 1:** Jack-o-Lantern [1], Witch Hat [1], Crystal Ball [1 M], Old Key [1], Candelabra [2 M], Cauldron [3 M], Broomstick [3], Potion Bottle [3], Haunted House [4 M], Spooky Tree [4]
- **Variant 2:** Chandelier [1 M], Black Cat [1], Lantern [1 M], Candy Pail [1], Standing Mirror [2 M], Music Box [3 M], Old Phone [3 M], Gramophone [3 M], Iron Gate [4 M], Spooky Cabin [4 M]
- **Variant 3:** Bat [1], Cobweb [1], Jack-o-Lantern [1], Old Trunk [2 M], Candlestick [2], Lab Flask [3], Flashlight [3 M], Wardrobe [3 M], Carousel [4 M], Ferris Wheel [4 M]

## horror-shared.json: Horror

Variants keep the most iconic objects.

- **Variant 1:** Jack-o-Lantern [1], Witch Hat [1], Potion Bottle [1], Candelabra [2 M], Black Cat [2], Cauldron [3 M], Broomstick [3], Candy Pail [3], Haunted House [4 M], Creepy Gate [4 M]
- **Variant 2:** Pumpkin [1], Witch Hat [1], Ghost Sheet [1], Bat [1], Candelabra [2 M], Cauldron [3 M], Standing Mirror [3 M], Haunted Mansion [4 M], Bare Tree [4], Rowboat [4 M]
- **Variant 3:** Pumpkin [3], Witch Hat [1], Iron Lantern [1 M], Spider [1], Cauldron [2 M], Candy Pail [2], Candelabra [3 M], Haunted House [4 M], Stone Bridge [4 M], Creepy Gate [4 M]

## *-shared-cast.json: all three genres, 2026-11-06

Planned with the producer's accepted lessons, variants keeping the most iconic objects, and one character card per variant (`experiments/shared_plans.py <Theme> --cast 1`). Variant 1 of each was drawn as `runs/<genre>-batch`; M is known only for those.

**Western** (by hand 2026-11-06: Chuck Wagon Chef renamed Pancake Flip (name rule))

- **Variant 1:** Cowboy Hat [1], Lasso [1 M], Bandana [1], Cowboy Boot [2], Cactus [3], Horseshoe [3], Covered Wagon [4 M], Windmill [4 M], Mesa [4], Campfire Pals [5]
- **Variant 2:** Cowboy Boot [1], Lasso [1], Lantern [1], Gold Pan [2], Cowboy Hat [3], Tumbleweed [3], Cactus [4], Stagecoach [4], Horse [4], Dawn Crow [5]
- **Variant 3:** Cowboy Hat [1], Lasso [1], Horseshoe [1], Cowboy Boot [2], Cactus [3], Hay Bale [3], Campfire [3], Covered Wagon [4], Rock Arch [4], Pancake Flip [5]

**Sci-Fi**

- **Variant 1:** Rocket [3 M], Flying Saucer [1 M], Ringed Planet [1 M], Space Helmet [1], Comet [1], Control Panel [2 M], Teleport Pod [3 M], Moon Rover [4 M], Moon Base [4 M], Zero Gravity [5]
- **Variant 2:** Flying Saucer [4], Retro Rocket [1], Ringed Planet [1], Space Helmet [3], Lab Flask [2], Satellite [1], Radio Dish [3], Space Capsule [3], Observatory [4], Barn Visitors [5]
- **Variant 3:** Toy Rocket [2], Flying Saucer [3], Ringed Planet [1], Space Helmet [1], Jetpack [1], Control Console [2], Teleport Pod [3], Space Shuttle [4], Mars Rover [4], Button Pusher [5]

**Horror** (by hand 2026-11-06: Ghost Sheep subject rewritten, the planner had left a self-correction in it)

- **Variant 1:** Jack-o-Lantern [1], Witch Hat [1], Bat [1], Candlestick [2 M], Cauldron [3 M], Candy Corn [3], Potion [3], Haunted House [4 M], Spooky Tree [4], Ghost Sheep [5]
- **Variant 2:** Lantern [1], Black Cat [1], Broom [1], Crystal Ball [2], Jack-o-Lantern [3], Witch Hat [3], Candle [3], Witch Cauldron [4], Haunted Mansion [4], Vampire Pig [5]
- **Variant 3:** Cauldron [1], Witch Hat [1], Owl [1], Manor [2], Potion [3], Candy Corn [3], Crystal Ball [3], Pumpkin Field [4], Spooky Tree [4], Ghost Man [5]

## *-shared-cast-2.json: all three genres, 2026-11-06 evening

As `*-shared-cast`, with the four lessons accepted on 2026-11-06 and the planner's new rules from the reference color logic and the second reference pass (`analysis/SYNTHESIS.md`): backdrop against the hero's temperature, places shown by their signature object, partner objects and pairs, the category following how the object exists, flat objects seen from above (`surface_from_above`), plain floors for category 2 and close spots for category 4 (`experiments/shared_plans.py <Theme> --cast 1 --suffix=-2`). Variant 1 of each is drawn as `runs/<genre>-batch2`. Western variant 3 came back without its character card.

**Western**

- **Variant 1:** Cowboy Hat [1], Cactus [2], Harmonica [1], Cowboy Boots [3], Saloon Doors [4], Lasso [1], Wagon [3], Horseshoe [3, from above], Campfire [4], Hat Tip [5]
- **Variant 2:** Lantern [1], Harmonica [1], Lasso [1], Root Beer [2], Cowboy Hat [3], Cowboy Boots [3], Gold Pan [3, from above], Saloon Doors [4], Hitching Post [4], Saloon Hello [5]
- **Variant 3:** Cowboy Hat [1], Spurs [1], Canteen [1], Lasso [1], Barrel [2], Cowboy Boots [3], Stagecoach [3], Saloon Doors [4], Saddle [4], Sunrise Ranch [5]

**Sci-Fi**

- **Variant 1:** Flying Saucer [1], Ringed Planet [1], Satellite [1], Space Helmet [2], Glow Flask [2], Moon Rover [3], Star Map [3, from above], Rocket [4], Control Panel [4], Space Farm [5]
- **Variant 2:** Copper Saucer [1], Retro Rocket [1], Blue Planet [1], Crystal [2], Orange Helmet [3], Blueprint [3, from above], Jetpack [3], Radio Dish [4], Airlock [4], Cockpit Crew [5]
- **Variant 3:** Saucer [1], Purple Planet [1], Space Shuttle [1], Yellow Rocket [2], Lab Flask [3], Gold Rover [3], Moon Helmet [3], Porthole [4], Sliding Door [4], Zero Gravity [5]

**Horror**

- **Variant 1:** Jack-o'-Lantern [3], Witch Hat [1], Cauldron [4], Ghost Sheet [1], Bat [1], Crystal Ball [2], Haunted Door [4], Spooky Tree [4], Potion [3], Boo Surprise [5]
- **Variant 2:** Jack-o'-Lantern [2], Cauldron [3], Witch Hat [1], Ghost Sheet [1], Broomstick [1], Black Cat [3], Spell Book [3, from above], Castle Tower [4], Candlestick [4], Pumpkin Peek [5]
- **Variant 3:** Ghost Sheet [2], Jack-o'-Lantern [4], Cauldron [3], Witch Hat [1], Owl [1], Vampire Cape [1], Full Moon [1], Old Key [3, from above], Wall Lantern [4], Spooky Cape [5]
