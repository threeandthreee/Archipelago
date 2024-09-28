"""
Option definitions for Pokémon FireRed/LeafGreen
"""
from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, NamedRange, OptionSet, PerGameCommonOptions, Range, Toggle
from .data import data


class GameVersion(Choice):
    """
    Select FireRed or LeafGreen version.
    """
    display_name = "Game Version"
    option_firered = 0
    option_leafgreen = 1
    default = "random"


class Goal(Choice):
    """
    Sets what your goal is to consider the game beaten.

    - Elite Four: Defeat the Elite Four
    - Elite Four Rematch: Defeat the Elite Four Rematch
    """
    display_name = "Goal"
    default = 0
    option_elite_four = 0
    option_elite_four_rematch = 1


class KantoOnly(Toggle):
    """
    Excludes all the Sevii Island locations. Navel Rock and Birth Island are still included.
    The Rock Smash and Waterfall HMs will still be in the item pool and their vanilla locations will have a random
    filler item.
    """
    display_name = "Kanto Only"


class ShuffleBadges(DefaultOnToggle):
    """
    Shuffle Gym Badges into the general item pool. If turned off, Badges will be shuffled among themselves.
    """
    display_name = "Shuffle Badges"


class ShuffleHiddenItems(Choice):
    """
    Shuffle Hidden Items into the general item pool.

    - Off: Hidden Items are not shuffled.
    - Nonrecurring: Nonrecurring Hidden Items are shuffled.
    - All: All Hidden Items are shuffled. Recurring Hidden Items will always appear and will not regenerate.
    """
    display_name = "Shuffle Hidden Items"
    default = 0
    option_off = 0
    option_nonrecurring = 1
    option_all = 2


class ExtraKeyItems(Toggle):
    """
    Adds key items that are required to access the Rocket Hideout, Safari Zone, Pokémon Mansion, and Power Plant.

    Adds four new locations:
    - Item in the Celadon Rocket House
    - Item given by a Worker in the Fuchsia Safari Office
    - Item given by the Scientist in the Cinnabar Pokémon Lab Research Room
    - Hidden Item in the Cerulean Gym (requires Surf & Itemfinder)
    """
    display_name = "Extra Key Items"


class Trainersanity(Toggle):
    """
    Defeating a trainer gives you an item.

    Trainers are no longer missable. Each trainer will add a random filler item into the pool.
    """
    display_name = "Trainersanity"


class Famesanity(Toggle):
    """
    Unlocking entries in the Fame Checker gives you an item.

    Each entry will add a random filler item into the pool.
    """
    display_name = "Famesanity"


class ShuffleFlyDestinationUnlocks(Toggle):
    """
    Shuffles the ability to fly to Pokémon Centers into the pool. Entering the map that normally would unlock the
    fly destination gives a random item.
    """
    display_name = "Shuffle Fly Destination Unlocks"


class PokemonRequestLocations(Toggle):
    """
    Shuffle the locations that require you to show a specific Pokémon to an NPC. If turned on, the Pokémon that are
    required will be found somewhere in the wild. Talking to the NPC that wants to see the Pokémon will provide you with
    the Pokédex info for where to find it as well as tell you the item they'll give.
    """
    display_name = "Pokémon Request Locations"


class SilphCoCardKey(Choice):
    """
    Sets how the card key that unlocks the doors in Silph Co. is handled.

    - Vanilla: There is one Card Key in the pool that unlocks every door in Silph Co.
    - Split: The Card Key is split into ten items, one for each floor of Silph Co. that has doors.
    - Progressive: The Card Key is split into ten items, and you will always obtain them in order from 2F to 11F.
    """
    display_name = "Silph Co. Card Key"
    default = 0
    option_vanilla = 0
    option_split = 1
    option_progressive = 2


class SeviiIslandPasses(Choice):
    """
    Sets how the passes that allow you to travel to the Sevii Islands are handled.

    - Vanilla: The Tri Pass and Rainbow Pass are two separate items in the pool and can be found in any order.
    - Progressive: There are two Progressive Passes in the pool. You will always obtain the Tri Pass before the Rainbow
                   Pass.
    - Split: The Tri Pass and Rainbow Pass are split into seven items, one for each island.
    - Progressive Split: The Tri Pass and Rainbow Pass are split into seven items, and you will always obtain the Passes
                         in order from the First Pass to the Seventh Pass.
    """
    display_name = "Sevii Island Passes"
    default = 0
    option_vanilla = 0
    option_progressive = 1
    option_split = 2
    option_progressive_split = 3


class ItemfinderRequired(Choice):
    """
    Sets whether the Itemfinder if required for Hidden Items. Some items cannot be picked up without using the
    Itemfinder regardless of this setting (e.g. the Leftovers under Snorlax on Route 12 & 16).

    - Off: The Itemfinder is not required to pickup Hidden Items.
    - Logic: The Itemfinder is logically required to pickup Hidden Items.
    - Required: The Itemfinder is required to pickup Hidden Items.
    """
    display_name = "Itemfinder Required"
    default = 1
    option_off = 0
    option_logic = 1
    option_required = 2


class FlashRequired(Choice):
    """
    Sets whether HM05 Flash is logically required to navigate dark caves.

    - Off: Flash is not required to navigate dark caves.
    - Logic: Flash is logically required to navigate dark caves.
    - Required: Flash is required to navigate dark caves.
    """
    display_name = "Flash Required"
    default = 1
    option_off = 0
    option_logic = 1
    option_required = 2


class FameCheckerRequired(DefaultOnToggle):
    """
    Sets whether it is required to have the Fame Checker in order to unlock entries.

    All Fame Checker entries that are one time occurences have been changed so that you can trigger them repeatedly.
    """
    display_name = "Fame Checker Required"


class ViridianCityRoadblock(Choice):
    """
    Sets the requirement for passing the Viridian City Roadblock.

    - Vanilla: The Old Man moves out of the way after delivering Oak's Parcel.
    - Early Parcel: Same as Vanilla but Oak's Parcel will be available at the beginning of your game. This option will
                    have no effect and be treated as Vanilla if Random Starting Town is on.
    - Open: The Old Man is moved out of the way at the start of the game.
    """
    display_name = "Viridian City Roadblock"
    default = 1
    option_vanilla = 0
    option_early_parcel = 1
    option_open = 2


class PewterCityRoadblock(Choice):
    """
    Sets the requirement for passing the Pewter City Roadblock.

    - Open: The boy will not stop you from entering Route 3.
    - Brock: The boy will stop you from entering Route 3 until you defeat Brock.
    - Any Gym Leader: The boy will stop you from entering Route 3 until you defeat any Gym Leader.
    - Boulder Badge: The boy will stop you from entering Route 3 until you have the Boulder Badge.
    - Any Badge: The boy will stop you from entering Route 3 until you have a Badge.
    """
    display_name = "Pewter City Roadblock"
    default = 1
    option_open = 0
    option_brock = 1
    option_any_gym = 2
    option_boulder_badge = 3
    option_any_badge = 4


class ModifyWorldState(OptionSet):
    """
    Set various changes to the world's state that changes how you can access various regions and locations.
    The valid options and their effects are the following:

    - Modify Route 2: Replaces the northmost cuttable tree with a smashable rock.
    - Remove Cerulean Roadblocks: Removes the policeman and slowpoke that block the exits of the city.
    - Block Tunnels: Blocks the entrances to the underground tunnels with smashable rocks.
    - Modify Route 9: Replaces the cuttable tree with a smashable rock.
    - Modify Route 10: Adds a waterfall to Route 10 that connects the north and south sides.
    - Block Tower: Blocks the 1F stairs of Pokémon Tower with a ghost battle.
    - Route 12 Boulders: Adds boulders to Route 12 that block the exits to Route 11 & 13.
    - Modify Route 12: Adds impassable rocks to Route 12 that prevent surfing around Snorlax.
    - Modify Route 16: Adds a smashable rock to Route 16 that allows you to bypass the Snorlax.
    - Route 23 Trees: Adds cuttable trees to Route 23 under the sixth checkpoint.
    - Modify Route 23: Adds a waterfall to Route 23 at the end of the water section.
    - Victory Road Rocks: Adds smashable rocks to Victory Road that block the floor switches.
    - Early Gossipers: Removes the requirement to have entered the Hall of Fame from various Famesanity locations.
    - Total Darkness: Changes dark caves to be completely black and provide no vision without Flash.
    """
    display_name = "Modify World State"
    valid_keys = ["Modify Route 2", "Remove Cerulean Roadblocks", "Block Tunnels", "Modify Route 9",
                  "Modify Route 10", "Block Tower", "Route 12 Boulders", "Modify Route 12", "Modify Route 16",
                  "Route 23 Trees", "Modify Route 23", "Victory Road Rocks", "Early Gossipers", "Total Darkness"]


class AdditionalDarkCaves(OptionSet):
    """
    Set additional caves to be dark caves, potentially requiring Flash to navigate them.

    The caves that can be turned into dark caves are:
    - Mt. Moon
    - Diglett's Cave
    - Victory Road
    """
    display_name = "Additional Dark Caves"
    valid_keys = ["Mt. Moon", "Diglett's Cave", "Victory Road"]


class RemoveBadgeRequirement(OptionSet):
    """
    Removes the badge requirement to use any of the HMs listed.

    HMs need to be listed by the move name. (e.g. Cut, Fly, Surf, etc.)
    """
    display_name = "Remove Badge Requirement"
    valid_keys = ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]


class OaksAideRoute2(Range):
    """
    Sets the number of Pokémon that need to be registered in the Pokédex to receive the item from Professor Oak's Aide
    on Route 2. Vanilla is 10.
    """
    display_name = "Oak's Aide Route 2"
    default = 5
    range_start = 0
    range_end = 50


class OaksAideRoute10(Range):
    """
    Sets the number of Pokémon that need to be registered in the Pokédex to receive the item from Professor Oak's Aide
    on Route 10. Vanilla is 20.
    """
    display_name = "Oak's Aide Route 10"
    default = 10
    range_start = 0
    range_end = 50


class OaksAideRoute11(Range):
    """
    Sets the number of Pokémon that need to be registered in the Pokédex to receive the item from Professor Oak's Aide
    on Route 11. Vanilla is 30.
    """
    display_name = "Oak's Aide Route 11"
    default = 15
    range_start = 0
    range_end = 50


class OaksAideRoute16(Range):
    """
    Sets the number of Pokémon that need to be registered in the Pokédex to receive the item from Professor Oak's Aide
    on Route 16. Vanilla is 40.
    """
    display_name = "Oak's Aide Route 16"
    default = 20
    range_start = 0
    range_end = 50


class OaksAideRoute15(Range):
    """
    Sets the number of Pokémon that need to be registered in the Pokédex to receive the item from Professor Oak's Aide
    on Route 15. Vanilla is 50.
    """
    display_name = "Oak's Aide Route 15"
    default = 25
    range_start = 0
    range_end = 50


class ViridianGymRequirement(Choice):
    """
    Sets the requirement for opening the Viridian Gym.

    - Badges: Obtain some number of Badges.
    - Gyms: Beat some number of Gyms.
    """
    display_name = "Viridian Gym Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class ViridianGymCount(Range):
    """
    Sets the number of Badges/Gyms required to open the Viridian Gym.
    """
    display_name = "Viridian Gym Count"
    default = 7
    range_start = 0
    range_end = 7


class Route22GateRequirement(Choice):
    """
    Sets the requirement for passing through the Route 22 Gate.

    - Badges: Obtain some number of Badges.
    - Gyms: Beat some number of Gyms.
    """
    display_name = "Route 22 Gate Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route22GateCount(Range):
    """
    Sets the number of Badges/Gyms required to pass through the Route 22 Gate.
    """
    display_name = "Route 22 Gate Count"
    default = 7
    range_start = 0
    range_end = 8


class Route23GuardRequirement(Choice):
    """
    Sets the requirement for passing the Route 23 Guard.

    - Badges: Obtain some number of Badges.
    - Gyms: Beat some number of Gyms.
    """
    display_name = "Route 23 Guard Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route23GuardCount(Range):
    """
    Sets the number of Badges/Gyms required to pass the Route 23 Guard.
    """
    display_name = "Route 23 Guard Count"
    default = 7
    range_start = 0
    range_end = 8


class EliteFourRequirement(Choice):
    """
    Sets the requirement for challenging the Elite Four.

    - Badges: Obtain some number of Badges.
    - Gyms: Beat some number of Gyms.
    """
    display_name = "Elite Four Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class EliteFourCount(Range):
    """
    Sets the number of Badges/Gyms required to challenge the Elite Four.
    """
    display_name = "Elite Four Count"
    default = 8
    range_start = 0
    range_end = 8


class CeruleanCaveRequirement(Choice):
    """
    Sets the requirement for being able to enter Cerulean Cave.

    - Vanilla: Become the Champion and restore the Network Machine on the Sevii Islands.
    - Champion: Become the Champion.
    - Network Machine: Restore the Network Machine on the Sevii Islands.
    - Badges: Obtain some number of Badges.
    - Gyms: Beat some number of Gyms.
    """
    display_name = "Cerulean Cave Requirement"
    default = 0
    option_vanilla = 0
    option_champion = 1
    option_restore_network = 2
    option_badges = 3
    option_gyms = 4


class CeruleanCaveCount(Range):
    """
    Sets the number of Badges/Gyms required to enter Cerulean Cave. This setting only matters if the Cerulean Cave
    Requirement is set to either Badges or Gyms.
    """
    display_name = "Cerulean Cave Count"
    default = 8
    range_start = 0
    range_end = 8


class LevelScaling(Choice):
    """
    Sets whether encounter levels are scaled by sphere access.

    - Off: Vanilla levels are used.
    - Spheres: Levels are scaled based on sphere access.
    - Spheres and Distance: Levels are scaled based on sphere access and the distance they are from your starting town.
    """
    display_name = "Level Scaling"
    default = 0
    option_off = 0
    option_spheres = 1
    option_spheres_and_distance = 2


class ModifyTrainerLevels(Range):
    """
    Modifies the level of all Trainer's Pokémon by the specified percentage.
    """
    display_name = "Modify Trainer Levels"
    default = 0
    range_start = -100
    range_end = 100


class RandomizeWildPokemon(Choice):
    """
    Randomizes wild Pokémon encounters (grass, caves, water, fishing)

    - Vanilla: Wild Pokémon are unchanged
    - Match Base Stats: Wild Pokémon are replaced with species with approximately the same BST
    - Match Type: Wild Pokémon are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class WildPokemonGroups(Choice):
    """
    If wild Pokémon are not vanilla, they will be randomized according to the grouping specified.

    - None: Pokémon are not randomized together based on any groupings
    - Dungeons: All Pokémon of the same species in a dungeon are randomized together
    - Species: All Pokémon of the same species are randomized together
    """
    display_name = "Wild Pokemon Groups"
    default = 0
    option_none = 0
    option_dungeons = 1
    option_species = 2


class WildPokemonBlacklist(OptionSet):
    """
    Prevents listed species from appearing in the wild when wild Pokémon are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokémon.
    """
    display_name = "Wild Pokemon Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeStarters(Choice):
    """
    Randomizes the starter Pokémon in Professor Oak's Lab.

    - Vanilla: Starters are unchanged
    - Match Base Stats: Starters are replaced with species with approximately the same BST
    - Match Type: Starters are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class StarterBlacklist(OptionSet):
    """
    Prevents listed species from appearing as a starter when starters are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokémon.
    """
    display_name = "Starter Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeTrainerParties(Choice):
    """
    Randomizes the Pokémon in all trainer's parties.

    - Vanilla: Parties are unchanged
    - Match Base Stats: Trainer Pokémon are replaced with species with approximately the same BST
    - Match Type: Trainer Pokémon are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class TrainerPartyBlacklist(OptionSet):
    """
    Prevents listed species from appearing in trainer's parties when trainer's parties are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "Legendaries" as a shortcut for all legendary Pokémon.
    """
    display_name = "Trainer Party Blacklist"
    valid_keys = ["Legendaries"] + sorted([species.name for species in data.species.values()])


class RandomizeLegendaryPokemon(Choice):
    """
    Randomizes legendary Pokémon (Mewtwo, Zapdos, Deoxys, etc.). Does not randomize the roamer.

    - Vanilla: Legendary encounters are unchanged
    - Legendaries: Legendary encounters are replaced with another legendary Pokémon
    - Match Base Stats: Legendary encounters are replaced with species with approximately the same BST
    - Match Type: Legendary encounters are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Legendary Pokemon"
    default = 0
    option_vanilla = 0
    option_legendaries = 1
    option_match_base_stats = 2
    option_match_type = 3
    option_match_base_stats_and_type = 4
    option_completely_random = 5


class RandomizeMiscPokemon(Choice):
    """
    Randomizes misc Pokémon. This includes non-legendary static encounters, gift Pokémon, and trade Pokémon

    - Vanilla: Species are unchanged
    - Match Base Stats: Species are replaced with species with approximately the same bst
    - Match Type: Species are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Misc Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class RandomizeTypes(Choice):
    """
    Randomizes the type(s) of every Pokémon. Each species will have the same number of types.

    - Vanilla: Types are unchanged
    - Shuffle: Types are shuffled globally for all species (e.g. every Water-type Pokémon becomes Fire-type)
    - Completely Random: Each species has its type(s) randomized
    - Follow Evolutions: Types are randomized per evolution line instead of per species
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2
    option_follow_evolutions = 3


class RandomizeAbilities(Choice):
    """
    Randomizes abilities of every species. Each species will have the same number of abilities.

    - Vanilla: Abilities are unchanged
    - Completely Random: Each species has its abilities randomized
    - Follow Evolutions: Abilities are randomized, but evolutions that normally retain abilities will still do so
    """
    display_name = "Randomize Abilities"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_follow_evolutions = 2


class AbilityBlacklist(OptionSet):
    """
    Prevent species from being given these abilities.

    Has no effect if abilities are not randomized.
    """
    display_name = "Ability Blacklist"
    valid_keys = sorted(data.abilities.keys())


class RandomizeMoves(Choice):
    """
    Randomizes the moves a Pokémon learns through leveling.
    Your starter is guaranteed to have a usable damaging move.

    - Vanilla: Learnset is unchanged
    - Randomized: Moves are randomized
    - Start with Four Moves: Moves are randomized and all Pokémon know 4 moves at level 1
    """
    display_name = "Randomize Moves"
    default = 0
    option_vanilla = 0
    option_randomized = 1
    option_start_with_four_moves = 2


class MoveBlacklist(OptionSet):
    """
    Prevents species from learning these moves via learnsets, TMs, and move tutors.
    """
    display_name = "Move Blacklist"
    valid_keys = sorted(data.moves.keys())


class HmCompatibility(NamedRange):
    """
    Sets the percent chance that a given HM is compatible with a species.
    """
    display_name = "HM Compatibility"
    default = -1
    range_start = 50
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "full": 100,
    }


class TmTutorCompatibility(NamedRange):
    """
    Sets the percent chance that a given TM or move tutor is compatible with a species.
    """
    display_name = "TM/Tutor Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "full": 100,
    }


class TmTutorMoves(Toggle):
    """
    Randomizes the moves taught by TMs and move tutors.

    Some opponents like gym leaders are allowed to use TMs. This option can affect the moves they know.
    """
    display_name = "Randomize TM/Tutor Moves"


class ReusableTmsTutors(Toggle):
    """
    Sets TMs to not break after use (they remain sellable). Allows Move Tutors to be used infinitely.
    """
    display_name = "Reusable TMs/Move Tutors"


class MinCatchRate(Range):
    """
    Sets the minimum catch rate a Pokémon can have. It will raise any Pokémon's catch rate to this value if its normal
    catch rate is lower than the chosen value.
    """
    display_name = "Minimum Catch Rate"
    range_start = 3
    range_end = 255
    default = 3


class GuaranteedCatch(Toggle):
    """
    Pokeballs are guaranteed to catch wild Pokémon regardless of catch rate.
    """
    display_name = "Guarenteed Catch"


class ExpModifier(Range):
    """
    Multiplies gained EXP by a percentage.

    100 is default
    50 is half
    200 is double
    etc.
    """
    display_name = "Exp Modifier"
    range_start = 1
    range_end = 1000
    default = 100


class StartingMoney(Range):
    """
    Sets the amount of money that you start with.
    """
    display_name = "Starting Money"
    range_start = 0
    range_end = 999999
    default = 3000


class BlindTrainers(Toggle):
    """
    Trainers will not start a battle with you unless you talk to them.
    """
    display_name = "Blind Trainers"


class BetterShops(Toggle):
    """
    Most Pokemarts will sell all normal Pokemart items. The exceptions are the following:

    - Celadon Department Store 2F TM Pokemart
    - Celadon Department Store 4F Evo Stone Pokemart
    - Celadon Department Store 5F Vitamin Pokemart
    - Two Island Market Stall
    """
    display_name = "Better Shops"


class FreeFlyLocation(Choice):
    """
    Enables flying to one random location (excluding cities reachable with no items).
    """
    display_name = "Free Fly Location"
    default = 0
    option_off = 0
    option_exclude_indigo = 1
    option_any = 2


class TownMapFlyLocation(Choice):
    """
    Enables flying to one random location once the town map has been obtained
    (excluding cities reachable with no items).
    """
    display_name = "Town Map Fly Location"
    default = 0
    option_off = 0
    option_exclude_indigo = 1
    option_any = 2


class TurboA(Toggle):
    """
    Holding A will advance most text automatically.
    """
    display_name = "Turbo A"


class ReceiveItemMessages(Choice):
    """
    Sets whether you receive an in-game notification when receiving an item. Items can still onlybe received in the
    overworld.

    - All: Every item shows a message.
    - Progression: Only progression items show a message
    - None: All items are added to your bag silently (badges will still show).
    """
    display_name = "Receive Item Messages"
    default = 1
    option_all = 0
    option_progression = 1
    option_none = 2


@dataclass
class PokemonFRLGOptions(PerGameCommonOptions):
    game_version: GameVersion

    goal: Goal
    kanto_only: KantoOnly

    shuffle_badges: ShuffleBadges
    shuffle_hidden: ShuffleHiddenItems
    extra_key_items: ExtraKeyItems
    trainersanity: Trainersanity
    famesanity: Famesanity
    shuffle_fly_destination_unlocks: ShuffleFlyDestinationUnlocks
    pokemon_request_locations: PokemonRequestLocations
    card_key: SilphCoCardKey
    island_passes: SeviiIslandPasses

    itemfinder_required: ItemfinderRequired
    flash_required: FlashRequired
    fame_checker_required: FameCheckerRequired
    viridian_city_roadblock: ViridianCityRoadblock
    pewter_city_roadblock: PewterCityRoadblock
    modify_world_state: ModifyWorldState
    additional_dark_caves: AdditionalDarkCaves
    remove_badge_requirement: RemoveBadgeRequirement

    oaks_aide_route_2: OaksAideRoute2
    oaks_aide_route_10: OaksAideRoute10
    oaks_aide_route_11: OaksAideRoute11
    oaks_aide_route_16: OaksAideRoute16
    oaks_aide_route_15: OaksAideRoute15

    viridian_gym_requirement: ViridianGymRequirement
    viridian_gym_count: ViridianGymCount
    route22_gate_requirement: Route22GateRequirement
    route22_gate_count: Route22GateCount
    route23_guard_requirement: Route23GuardRequirement
    route23_guard_count: Route23GuardCount
    elite_four_requirement: EliteFourRequirement
    elite_four_count: EliteFourCount
    cerulean_cave_requirement: CeruleanCaveRequirement
    cerulean_cave_count: CeruleanCaveCount

    level_scaling: LevelScaling
    modify_trainer_levels: ModifyTrainerLevels

    wild_pokemon: RandomizeWildPokemon
    wild_pokemon_groups: WildPokemonGroups
    wild_pokemon_blacklist: WildPokemonBlacklist
    starters: RandomizeStarters
    starter_blacklist: StarterBlacklist
    trainers: RandomizeTrainerParties
    trainer_blacklist: TrainerPartyBlacklist
    legendary_pokemon: RandomizeLegendaryPokemon
    misc_pokemon: RandomizeMiscPokemon
    types: RandomizeTypes
    abilities: RandomizeAbilities
    ability_blacklist: AbilityBlacklist
    moves: RandomizeMoves
    move_blacklist: MoveBlacklist
    hm_compatibility: HmCompatibility
    tm_tutor_compatibility: TmTutorCompatibility
    tm_tutor_moves: TmTutorMoves

    reusable_tm_tutors: ReusableTmsTutors
    min_catch_rate: MinCatchRate
    guaranteed_catch: GuaranteedCatch
    exp_modifier: ExpModifier
    starting_money: StartingMoney
    blind_trainers: BlindTrainers
    better_shops: BetterShops
    free_fly_location: FreeFlyLocation
    town_map_fly_location: TownMapFlyLocation

    turbo_a: TurboA
    receive_item_messages: ReceiveItemMessages
