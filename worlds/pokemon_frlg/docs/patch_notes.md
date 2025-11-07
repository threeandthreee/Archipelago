# 1.0.0
## Updates
- Reworked the Fossil checks
  - You can now only grab one fossil in Mt. Moon (it doesn't matter which you will get the same item)
  - The second fossil check can be gotten in the Pokémon Lab Experiment Room after you have gotten the one in Mt. Moon and revived enough fossils (set by an option)
- Updated option `randomize_fly_destinations`
  - Off: Fly destinations are not randomized
  - Area: Fly destinations will be randomized to a location in the same area as its original location (e.g. Vermilion Fly Destination would go to either Vermilion City, Route 6, or Route 11)
  - Map: Fly destinations will be randomized to a location on the same map as its original location (e.g. One Island Fly Destination would go to either One Island, Two Island, or Three Island)
  - Region: Fly destinations will be randomized to a location in the same region as its original location (e.g. Sevii fly destinations would go to another location on the Sevii Islands)
  - Completely Random: Fly destinations are completely random
- Updated option `shopsanity`
  - Local non-progression shop items can now be purchased repeatedly
- New option `shop_slots`
  - Sets the number of slots per shop that can have multiworld items when shopsanity is on. Shop slots that do not have a multiworld item will be filled with a random normal shop item
- Reworked option `shop_prices`
  - Changed so that item's prices are determined by their base price
    - Vanilla: Items cost their base price
    - Cheap: Items cost 50% of their base price
    - Affordable: Items cost between 50% - 100% of their base price
    - Standard: Items cost 50% - 150% of their base price
    - Expensive: Items cost 100% - 150% of their base price
  - Changes shop prices even if `shopsanity` isn't on
- New option `consistent_shop_prices`
  - Sets whether all instances of an item will cost the same price in every shop (e.g. if a Potion's price in a shop is
    200 then all Potions in shops will cost 200)
- Removed options `minimum_shop_price` and `maximum_shop_price`
- New option `rematchsanity`
  - Beating each of a trainer's rematches gives you an item. Only the rematches for trainers who have a trainersanity item will give an item for rematchsanity
- New option `shuffle_pokedex`
  - Vanilla: The Pokédex is obtained by delivering the parcel to Professor Oak
  - Shuffle: The Pokédex is shuffled into the item pool
  - Start With: You start with the Pokédex
- New option `shuffle_ledge_jump`
  - Shuffles the ability to jump down ledges into the item pool. If not shuffled then you will start with it
- New option `post_goal_locations`
  - Sets whether locations that are locked behind completing your goal are included
- New option `fishing_rods`
  - Vanilla: The fishing rods are all separate items in the pool and can be found in any order
  - There are three Progressive Rods in the pool, and you will always obtain them in order from Old Rod to Super Rod
- New option `bicycle_requires_ledge_jump`
  - Sets whether the ability to jump down ledges is required for the Bicycle to jump down ledges
- New option `acrobatic_bicycle`
  - Sets whether the bicycle can be used to jump up ledges. If `bicycle_requires_ledge_jump` is on then you will need to be able to jump down ledges in order to jump up them as well
- New option `fossil_count`
  - Sets the number of fossils you need to revive in order to get the fossil check in the Pokémon Lab
- New option `base_stats`
  - Vanilla: Base stats are unchanged
  - Shuffle: Base stats are shuffled amongst each other
  - Keep BST: Random base stats, but base stat total is preserved
  - Completely Random: Random base stats and base stat total
- The Title Screen locations have been removed. All items that you can start with (e.g. Berry Pouch, TM Case, etc.) will be added to your `start_inventory`
- The fences in Pallet Town and Route 21 have been modified so that you can surf left to right in Pallet Town without accidentally leaving the water
- Restored the triggers for the first Rival battle
- NPCs and events that block the player will now force the player back the direction they came from (e.g. Pewter City Roadblock, Route 23 Guard, etc.)
- Increased Trainer money rewards so that they scale based on party size and Pokémon's BST
- Updated the Two Island Market Stall so that you can view all the items in the shop immediately
- The Nurse in Silph Co. will still heal you even after Silph Co. has been liberated
- Local non-progression items are purchasable repeatedly in shops when `shopsanity` is on. This also applies if `remote_items` is on
- Lemonade is no longer sold in the Pokémon Center shop. If `shopsanity` is on then at least one Lemonade will be placed in a shop location

## Bug Fixes
- Fixed an issue with displaying move data in battle during double battles
- Fixed an issue where Route 21 fishing battles were not in logic unless you could surf

# 0.9.6
# Bug Fixes
- Fixed an issue where trying to generate a seed with `dungeon_entrance_shuffle` on using Archipelago 0.6.3 would fail

# 0.9.5
## Bug Fixes
- Fixed an error that could occur when connecting to the client if the `provide_hints` setting was set to either `progression` or `progression_and_useful`

# 0.9.4
## Updates
- Improvements made to reduce generation time (credit to [Mysteryem](https://github.com/Mysteryem))
- Support added for the Pokémon Gen III Adjuster (credit to [Rhenny](https://github.com/RhenaudTheLukark))
- If `randomize_fly_destinations` is on, the game will state what destination a fly unlock goes to regardless of if fly unlocks are shuffled
- Updated the client to send entrance data to the tracker for auto entrance tracking
- The fossil Pokémon can be obtained immediately after giving them to the scientist in the Pokémon Lab without needing to reload the map
- Updated option `provide_hints`
  - Will now also hint `shopsanity` locations
  - Can now specify whether it should hint progression, progression and useful, or all items.
- New option `legendary_pokemon_blacklist`
- New option `misc_pokemon_blacklist`
- New option `tm_tutor_moves_blacklist`
  - Allows you to blacklist the moves that can be on TMs and move tutors separately from the moves in learnsets

## Bug Fixes
- Fixed an issue where the Cinnabar Gym door would be locked again after battling a surfing trainer on Routes 20 or 21
- Fixed an issue where Pokémon with branching evolutions has their evolved forms never be expected by the logic
- Fixed a logic issue with the Water Labyrinth - Gentleman Info location assuming you need both Togepi and Togetic
- Fixed an issue with the Saffron Dojo Leader and Team Rocket Warehouse Admin where if you lost to them, the trigger that caused them to face you and battle would no longer be triggered
- Fixed an issue where the `Cerulean City - Rival Gift` location was a part of the "Overworld Items" location group instead of "NPC Gifts"
- Fixed an issue where if Pokémon Request locations weren't randomized then the NPC would say they have an AP ITEM instead of the vanilla item
- Fixed an issue where sometimes a Pokédex update was sent to the Tracker that didn't include any seen Pokémon
- Fixed an issue where the Pewter roadblock boy and Oak's Aide would pop into existence when entering from Route 3

# 0.9.3
## Updates
- New option `remote_items`
  - All randomized items are sent from the server instead of being patched into your game
- New option `death_link`

## Bug Fixes
- Fixed an issue where sometimes `dexsanity` locations were removed even if they were accessible in the seed
- Prevent blacklisted moves from showing up as a Pokémon's guaranteed damaging move (I thought I already fixed this)
- Fixed an issue where the damage type for moves shown on the Pokémon move summary screen always assumed the physical/special split was enabled

# 0.9.2
## Bug Fixes
- A logic issue involving the `Modify Route 16` setting has been fixed
- The leader of the Saffron Dojo and the second Team Rocket Admin in the Rocket Warehouse will now trigger their battles when you walk past them even if `Blind Trainers` is on

# 0.9.1
## Updates
- New icons for several AP exclusive items and new damage type icons (credit to [kattnip](https://github.com/Invader07))
- The Berry Pouch and TM Case are now given to the player at the start of the game instead of when the first berry and HM/TM are obtained
- If a gym door is locked, such as the Cinnabar or Viridian Gym, then you now need to interact with the door to unlock it
- When you receive a fly unlock it will now tell you what location it allows you to fly to
- Interacting with the Receptionist on the far right of the 2F of Pokémon Centers will allow you to purchase various consumable items that you have already obtained
- The species that is requested for in-game trades are now randomized. Dex info will be given for the requested species after talking to the trade NPC
- Added a new page to Pokémon's Dex entries that lists out the areas where they can be found and what they can evolve into
- Added a new Pokédex list when `dexsanity` is on that only shows Pokémon who have a check
- Sailing and flying to the Sevii Islands is now impossible in `kanto only` even if you have the means to do so
- New option `skip_elite_four`
  - Makes it so that entering the Pokémon League takes the player directly to the Champion battle. Any location checks that would require fighting the Elite Four will not exist
- New option `dungeon_entrance_shuffle`
  - Simple: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons will connect to the same dungeon
  - Restricted: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons do not need to lead to the same dungeon
  - Full: All dungeon entrances are shuffled together
- Updated option `fly_destination_plando`
  - Can now specify the specific warp to set a fly destination to. A list of valid warps can be found [here](https://github.com/vyneras/Archipelago/blob/frlg-stable/worlds/pokemon_frlg/docs/fly_plando.md)
- New option `shopsanity`
  - Shuffles shop items into the item pool. The Celadon Department Store 4F Held Item Shop is not shuffled
- New option `shop_prices`
  - Sets how shop prices are determined (by spheres, by item classification, by both, or completely random)
- New options `minimum_shop_price` and `maximum_shop_price`
  - Sets the minimum and maximum prices that shop items can be when `shopsanity` is on
- New options `shuffle_berry_pouch` and `shuffle_tm_case`
  - Shuffles the Berry Pouch and TM Case into the item pool. Creates a location check that is given at the start of the game for each one shuffled
- New option `gym_keys`
  - Adds keys into the item pool that are needed to unlock each gym (renames the Secret Key to the Cinnabar Key)
- New option `evolutions_required`
  - Sets which types of locations and/or access rules that evolutions may be logically required for
- New option `evolution_methods_required`
  - Sets which types of evolutions may be logically required
- New options `move_match_type_bias` and `move_normal_type_bias`
  - Sets the probability that a randomized move will match the Pokémon's type or will be a Normal move
- New option `physical_special_split`
  - Changes the damage category that moves use to match the categories since the Gen IV physical/special split instead of the damage category being determined by the move's type
- New option `move_types`
  - Randomizes the type for each move
- New option `damage_categories`
  - Randomizes the damage category for each move/type. Will randomized the damage category of the moves individually or by each type depending on if the `physical_special_split` option is on
- Changed the warps in the Lost Cave item rooms to return you to the previous room instead of back to the start
- Improved client connection error handling

## Bug Fixes
- Fixed a few typos in the game
- Fixed an issue where setting the in-game Experience option to NONE still gave 1 exp
- Fixed an issue where catching the Snorlax on Route 12 & 16 showed the text saying they returned to the mountains
- Fixed and issue where you could receive the item from Lostelle in her house repeatedly 
- Fixed an issue where a fly point randomized to take you in front of the Pewter Museum east entrance actually placed you to the left of the Pewter Pokémon Center
- Fixed dark cave logic applying to the entrances to dark caves instead of the exits from dark caves