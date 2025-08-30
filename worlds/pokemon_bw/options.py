from dataclasses import dataclass

from Options import (Choice, PerGameCommonOptions, OptionSet, Range, Toggle, OptionCounter,
                     PlandoTexts, OptionError)


class Goal(Choice):
    """
    Determines what your goal is to consider the game beaten.
    - **Ghetsis** - Clear the main story by defeating Ghetsis
    - **Champion** - Become the champion by defeating Alder
    - **Cynthia** - Defeat Cynthia in Undella Town
    - **Cobalion** - Reach and defeat/catch Cobalion in Mistralton Cave
    - **Regional pokedex** - Complete the Unova pokedex (requires wild Pokemon being randomized)
    - **National pokedex** - Complete the national pokedex (requires wild Pokemon being randomized)
    - **Custom pokedex** - Complete all dexsanity locations (requires wild Pokemon being randomized
                           and dexsanity being set to at least 100)
    - **TM/HM hunt** - Get all TMs and HMs
    - **Seven Sages hunt** - Find the Seven Sages
    - **Legendary hunt** - Find and defeat/catch all (stationary available) legendary encounters, including Volcarona
    - **Pokemon master** - Complete the requirements of all other goals combined
    """
    display_name = "Goal"
    option_ghetsis = 0
    option_champion = 1
    option_cynthia = 2
    option_cobalion = 3
    # option_regional_pokedex = 4
    # option_national_pokedex = 5
    # option_custom_pokedex = 6
    option_tmhm_hunt = 7
    option_seven_sages_hunt = 8
    option_legendary_hunt = 9
    option_pokemon_master = 10
    default = 0


class GameVersion(Choice):
    """
    Select your game version.
    """
    display_name = "Game Version"
    option_black = 0
    option_white = 1
    # option_dynamic = 2
    default = "random"


class RandomizeWildPokemon(OptionSet):
    """
    Randomizes wild pokemon encounters.
    - **Randomize** - Toggles wild pokemon being randomized. Required for any modifier below.
    - **Ensure all obtainable** - Ensures that every pokemon species is obtainable by either catching
                                  or evolving. This is automatically checked if **National pokedex** is chosen as the goal.
    - **Similar base stats** - Tries to keep every randomized pokemon at a similar base stat total as the replaced encounter.
    - **Type themed** - Makes every pokemon in an area have a certain same type.
    - **Area 1-to-1** - Keeps the amount of different encounters and their encounter rate in every area.
    - **Merge phenomenons** - Makes rustling grass, rippling water spots, dust clouds, and flying shadows
                              in the same area have only one encounter.
    - **Prevent rare encounters** - Randomizes the encounter slots with the lowest chance in each area to the same pokemon.
    """
    display_name = "Randomize Wild Pokemon"
    valid_keys = [
        "Randomize",
        "Ensure all obtainable",
        "Similar base stats",
        "Type themed",
        "Area 1-to-1",
        "Merge phenomenons",
        "Prevent rare encounters",
    ]
    default = ["Merge phenomenons", "Prevent rare encounters"]


class RandomizeTrainerPokemon(OptionSet):
    """
    Randomizes trainer pokemon.
    - **Randomize** - Toggles trainer pokemon being randomized. Required for any modifier below.
    - **Similar base stats** - Tries to keep the randomized pokemon at a similar base stat total as the replaced one.
    - **Type themed** - All pokemon of a trainer have to share at least one randomly chosen type.
                        Gym leaders will always have themed teams, regardless of this modifier.
    - **Themed gym trainers** - All pokemon of gym trainers will share the type assigned to the gym leader.
    """
    display_name = "Randomize Trainer Pokemon"
    valid_keys = [
        "Randomize",
        "Similar base stats",
        "Type themed",
        "Themed gym trainers",
    ]
    default = ["Themed gym trainers"]


class RandomizeStarterPokemon(OptionSet):
    """
    Randomizes the starter pokemon you receive at the start of the game.
    - **Randomize** - Toggles starter pokemon being randomized. Required for any other modifier.
    - **Any base** - Only use unevolved/baby pokemon.
    - **Base with 2 evolutions** - Only use unevolved/baby pokemon that can evolve twice. Overrides **Any base**.
    - **Only official starters** - Only use pokemon that have been a starter in any mainline game. Overrides
                                   **Any base** and **Base with 2 evolutions**.
    - **Type variety** - Every starter will have a single type that is different from the other two.
    """
    display_name = "Randomize Starter Pokemon"
    valid_keys = [
        "Randomize",
        "Any base",
        "Base with 2 evolutions",
        "Only official starters"
        "Type variety",
    ]
    default = []


class RandomizeStaticPokemon(OptionSet):
    """
    Randomizes static encounters you can battle and catch throughout the game, e.g. Volcarona in Relic Castle.
    - **Randomize** - Toggles static pokemon being randomized. Required for any other modifier.
    - **Similar base stats** - Tries to keep the randomized pokemon at a similar base stat total as the replaced one.
    - **Only base** - Only use unevolved Pokemon.
    - **No legendaries** - Exclude legendaries from being placed into static encounters.
    """
    display_name = "Randomize Static Pokemon"
    valid_keys = [
        "Randomize",
        "Similar base stats",
        "Only base",
        "No legendaries",
    ]
    default = []


class RandomizeGiftPokemon(OptionSet):
    """
    Randomizes gift pokemon that you receive for free, e.g. the Larvesta egg on route 18.
    - **Randomize** - Toggles gift pokemon being randomized. Required for any other modifier.
    - **Similar base stats** - Tries to keep the randomized pokemon at a similar base stat total as the replaced one.
    - **No legendaries** - Exclude legendaries from being placed into gift encounters.
    """
    display_name = "Randomize Gift Pokemon"
    valid_keys = [
        "Randomize",
        "Similar base stats",
        "No legendaries",
    ]
    default = []


class RandomizeTradePokemon(OptionSet):
    """
    Randomizes trade offers from NPCs. Any **Randomize ...** is required for the other modifiers.
    - **Randomize offer** - Toggles offered pokemon being randomized.
    - **Randomize request** - Toggles requested pokemon being randomized.
    - **Similar base stats** - Tries to keep the randomized pokemon at a similar base stat total as the replaced one.
    - **No legendaries** - Exclude legendaries from being placed into trades.
    """
    display_name = "Randomize Trade Pokemon"
    valid_keys = [
        "Randomize offer",
        "Randomize request",
        "Similar base stats",
        "No legendaries",
    ]
    default = []


class RandomizeLegendaryPokemon(OptionSet):
    """
    Randomizes legendary and mythical encounters.
    - **Randomize** - Toggles legendary pokemon being randomized. Required for any other modifier.
    - **Keep legendary** - Randomized pokemon will all still be legendaries or mythicals.
    - **Same type** - Tries to keep at least one type of every encounter.
    """
    display_name = "Randomize Legendary Pokemon"
    valid_keys = [
        "Randomize",
        "Keep legendary",
        "Same type",
    ]
    default = []


class RandomizeBaseStats(OptionSet):
    """
    Randomizes the base stats of every pokemon species.
    - **Randomize** - Toggles base stats being randomized. Required for any other modifier.
    - **Keep total** - Every species will keep the sum of its base stats.
    - **Follow evolutions** - Evolved species will use their pre-evolution's base stats and add on top of that.
    """
    display_name = "Randomize Base Stats"
    valid_keys = [
        "Randomize",
        "Keep total",
        "Follow evolutions",
    ]
    default = []


class BaseStatTotalLimits(OptionCounter):
    """
    Determines the maximum and minimum base stat total if base stats are randomized.

    Maximum cannot be lower than minimum.
    """
    display_name = "Base Stat Total Limits"
    min = 6
    max = 1530
    valid_keys = [
        "minimum",
        "maximum",
    ]
    default = {"minimum": 6, "maximum": 1530}


class RandomizeEvolutions(OptionSet):
    """
    Randomizes the evolutions of every pokemon species.
    - **Randomize** - Toggles evolutions being randomized. Required for any other modifier.
    - **Keep method** - Keeps the method (e.g. levelup, evolution stone, ...) of every evolution.
    - **Follow type** - Pre-evolution and evolved pokemon always share at least one type.
    - **Allow multiple pre-evolutions** - Multiple pokemon species can evolve into the same species.
    - **Allow more or less branches** - Allows all species to be able to evolve into more or less species than before.
    """
    display_name = "Randomize Evolutions"
    valid_keys = [
        "Randomize",
        "Keep method",
        "Follow type",
        "Allow multiple pre-evolutions",
        "Allow more or less branches",
    ]
    default = []


class RandomizeCatchRates(OptionSet):
    """
    Randomizes the catch rate of every pokemon species.
    - **Shuffle** - Gives every species a commonly used catch rate (e.g. 255, 45, 3, ...).
    - **Randomize** - Gives every species a completely random catch rate. Overrides **Shuffle**.
    - **Follow evolutions** - Evolved species will have a catch rate equal to or lower than their pre-evolution(s).
    """
    display_name = "Randomize Catch Rates"
    valid_keys = [
        "Shuffle",
        "Randomize",
        "Follow evolutions",
    ]
    default = []


class CatchRateLimits(OptionCounter):
    """
    Determines the maximum and minimum catch rate if those are randomized.

    Maximum cannot be lower than minimum.
    """
    display_name = "Catch Rate Limits"
    min = 3
    max = 255
    valid_keys = [
        "minimum",
        "maximum",
    ]
    default = {"minimum": 3, "maximum": 255}


class RandomizeLevelUpMovesets(OptionSet):
    """
    Randomizes the moves a pokemon species learns by leveling up.
    - **Randomize** - Toggles level up movesets being randomized. Required for any other modifier.
    - **Keep types** - Randomized moves have either a matching or normal type.
    - **Progressive power** - If a move is learned after another one, it will have an equal or higher base power.
    - **Keep amount** - Keeps the amount of moves a species learns normally.
    - **Keep levels** - If the species learned a move at a certain level, it will still learn something at that level.
    - **Follow evolutions** - Evolved species will have at least 50% of the level up moveset(s)
                              of their pre-evolution(s). Overrides all **Keep ...** modifiers.
    """
    display_name = "Randomize Level Up Movesets"
    valid_keys = [
        "Randomize",
        "Keep types",
        "Progressive power",
        "Keep amount",
        "Keep levels",
        "Follow evolutions",
    ]
    default = []


class RandomizeTypes(OptionSet):
    """
    Randomizes the type(s) of every pokemon species.
    - **Randomize** - Toggles types being randomized. Required for any other modifier.
    - **Only secondary type** - Only randomizes the secondary type of every species and thereby keeps the primary type.
                                Includes removing it. Not compatible with **Only primary type**.
    - **Only primary type** - Only randomizes the primary type of every species and thereby keeps the secondary type
                              (which might be none). Not compatible with **Only secondary type**.
    - **Follow evolutions** - Evolved species will share at least one type with (one of) their pre-evolutions.
    """
    display_name = "Randomize Types"
    valid_keys = [
        "Randomize",
        "Only secondary type",
        "Only primary type",
        "Follow evolutions",
    ]
    default = []


class RandomizeAbilities(OptionSet):
    """
    Randomizes the abilities of every pokemon species.
    - **Randomize** - Toggles abilities being randomized. Required for any other modifier.
    - **One per pokemon** - Gives every species only one ability.
    - **Follow evolutions** - Evolved pokemon will have the abilities of (one of) their pre-evolution(s)..
    - **Include hidden abilities** - Includes hidden abilities being randomized. Note that only a few select pokemon
                                     that originate from these games can have their hidden ability.
    """
    display_name = "Randomize Abilities"
    valid_keys = [
        "Randomize",
        "One per pokemon",
        "Follow evolutions",
        "Include hidden abilities",
    ]
    default = []


class RandomizeGenderRatio(OptionSet):
    """
    Randomizes the gender ratio of every pokemon species.
    - **Shuffle** - Gives every species a commonly used gender ratio (e.g. 50/50, 1 in 8, ...).
    - **Randomize** - Gives every species a completely random gender ratio. Overrides **Shuffle**.
    - **Follow evolutions** - Evolved species will have the same gender ratio as (one of) their pre-evolution(s).
    """
    display_name = "Randomize Gender Ratio"
    valid_keys = [
        "Shuffle",
        "Randomize",
        "Follow evolutions",
    ]
    default = []


class GenderRatioLimits(OptionCounter):
    """
    Determines the maximum and minimum gender ratio if those are randomized.

    Maximum cannot be lower than minimum.

    0 is always female, 255 is always male.
    """
    display_name = "Gender Ratio Limits"
    min = 0
    max = 255
    valid_keys = [
        "minimum",
        "maximum",
    ]
    default = {"minimum": 0, "maximum": 255}


class RandomizeTMHMCompatibility(OptionSet):
    """
    Randomizes the TM and HM compatibility of every pokemon species.
    - **Force all TMs** - Forces all TMs to be compatible with every pokemon species.
    - **Force all HMs** - Forces all HMs (and TM70 Flash) to be compatible with every pokemon species.
    - **Randomize** - Toggles TM and HM compatibility being randomized. Required for any other modifier.
    - **Keep types** - Randomized moves have either a matching or normal type.
    - **Keep amount** - Keeps the amount of moves a species learns normally.
    - **Follow evolutions** - Evolved species will have at least 50% of the learnable TMs and HMs
                              of their pre-evolution(s). Overrides all **Keep ...** modifiers.
    """
    display_name = "Randomize TM/HM Compatibility"
    valid_keys = [
        "Force all TMs",
        "Force all HMs",
        "Randomize",
        "Keep types",
        "Keep amount",
        "Follow evolutions",
    ]
    default = []


class ShuffleBadgeRewards(Choice):
    """
    Determines how gym badges are randomized and what items gym badge locations can have.
    - **Vanilla** - Gym badges will stay at their vanilla locations.
    - **Shuffle** - Gym badges are shuffled between the gym leaders.
    - **Any badge** - Puts the badges into the item pool, while only allowing items that have the word "badge"
                      in their name (which also applies to gym badges of other games/slots) being placed at gym leaders.
    - **Anything** - Gym badges can be anywhere and gym leaders can give any item.
    """
    display_name = "Shuffle Badge Rewards"
    option_vanilla = 0
    option_shuffle = 1
    option_any_badge = 2
    option_anything = 3
    default = 1


class ShuffleTMRewards(Choice):
    """
    Determines what items NPCs, who would normally give TMs or HMs, can have.
    - **Shuffle** - These NPCs will always give a TM or HM from the same slot.
    - **HM with Badge** - Like "Shuffle", but puts each HM (and TM70 Flash) at a gym leader's badge reward
                          (including the TM from Clay on route 6).
    - **Any TM/HM** - These NPCs will give any item that starts with "TM" or "HM" followed by any digit
                      (which also applies to TMs and HMs of other games/slots).
    - **Anything** - No restrictions.
    """
    display_name = "Shuffle TM Rewards"
    option_shuffle = 0
    option_hm_with_badge = 1
    option_any_tm_hm = 2
    option_anything = 3
    default = 0


class ShuffleRoadblockReqs(Toggle):
    """
    Roadblocks always require a specific item to disappear in this randomizer.
    If set to true, roadblocks will require a random key item.
    """
    display_name = "Shuffle Roadblock Requirements"
    default = False


class AdditionalRoadblocks(Choice):
    """
    Adds a number of additional roadblocks like cut trees or npcs blocking your way across the region.
    """
    display_name = "Additional Roadblocks"
    option_none = 0
    option_some = 1
    option_many = 2
    default = 0


class Dexsanity(Range):
    """
    Adds a number of locations that can be checked by catching a certain Pokemon species
    and registering it in the pokedex. The actual maximum number of added checks depends on what pokemon species are
    actually obtainable in the wild.

    The following will only apply once wild randomization is implemented:
    If you want to have all 649 possible checks, then you need to randomize wild
    encounters and add the **Ensure all obtainable** modifier.
    """
    display_name = "Dexsanity"
    default = 0
    range_start = 0
    range_end = 649


class Trainersanity(Range):
    """
    Adds a number of locations that can be checked by defeating a regular trainer.
    """
    display_name = "Trainersanity"
    default = 0
    range_start = 0
    range_end = 1  # TODO need to count trainers in the game


class Seensanity(Range):
    """
    Adds a number of locations that can be checked by seeing a certain Pokemon species, which is marked in the pokedex.
    The actual maximum number of added checks depends on what pokemon species are
    actually observable in the wild or in trainer battles.

    If you want to have all 649 possible checks, then you need to randomize wild
    encounters and add the **Ensure all obtainable** modifier.
    """
    display_name = "Seensanity"
    default = 0
    range_start = 0
    range_end = 649


class DoorShuffle(OptionSet):
    """
    Shuffles or randomizes door warps.
    - **Gates** - Shuffles city gate entrances, leading to the region having a different layout than normally.
    - **Buildings per map** - Shuffles the building entrances (not gates) within every city or route.
    - **Buildings anywhere** - Shuffles building entrances (not gates) all over Unova.
    - **Dungeons** - Shuffles the location of all dungeons with two entrances and all dungeons with only one entrance.
    - **Full** - Fully shuffle all door warps. Overrides all modifiers above.
    - **Decoupled** - Removes the requirement for all shuffled door warps leading to each other.
    """
    display_name = "Door Shuffle"
    valid_keys = [
        "Gates",
        "Buildings per map",
        "Buildings anywhere",
        "Dungeons",
        "Full",
        "Decoupled",
    ]
    default = []


class SeasonControl(Choice):
    """
    Determines how seasons are handled by the game.
    - **Vanilla** - Seasons are not randomized and change based on real time. Locations that depend on the season
                    will only contain filler items.
    - **Changeable** - The current season can be changed by an NPC next to the Pokemon Center in Nimbasa City.
    - **Randomized** - All seasons are unlockable by items that get shuffled into the item pool. They can as well be
                       changed by an NPC in Nimbasa City, with one season being unlocked from the beginning.
    """
    display_name = "Season Control"
    option_vanilla = 0
    option_changeable = 1
    option_randomized = 2
    default = 0


class AdjustLevels(OptionSet):
    """
    Adjusts the levels of wild and trainer pokemon in postgame areas and surfing/fishing encounters
    to similar levels in surrounding areas (regardless of randomization).

    - **Wild** - Normalizes wild pokemon levels, including surfing and fishing encounters.
    - **Trainer** - Normalizes trainer pokemon levels, excluding Cynthia.
    """
    display_name = "Adjust levels"
    valid_keys = [
        "Wild",
        "Trainer",
    ]
    default = ["Wild", "Trainer"]


class ExpModifier(Range):
    """
    Multiplies the experience received from defeating wild and trainer pokemon.

    The value is in percent, meaning 100 is normal, 200 is double, 50 is half, etc.
    """
    display_name = "Experience Modifier"
    default = 100
    range_start = 10
    range_end = 160


class AllPokemonSeen(Toggle):
    """
    Marks all pokemon in the pokedex (that do not have a Seensanity check) as seen
    (including all forms, except shinies). This could possibly have no effect under certain circumstances.
    """
    display_name = "All Pokemon Seen"
    default = False


class AddFairyType(Choice):
    """
    Adds the fairy type from the sixth generation games.
    - **No** - Don't add the fairy type.
    - **Only randomized** - If types are randomized, this adds the fairy type to the pool of possible types.
    - **Modify vanilla** - Updates the type combination of all pokemon that received the fairy type in X and Y.
    """
    display_name = "Add Fairy Type"
    option_no = 0
    option_only_randomized = 1
    option_modify_vanilla = 2
    default = 0


class ReplaceEvoMethods(OptionSet):
    """
    Replaces certain vanilla evolution methods with other methods that are easier to achieve.
    This also excludes them from randomized evolutions.
    Trade and time based evolutions are always replaced/excluded.

    - **Locations** - Replaces evolutions requiring a magnetic place, the ice rock, or the mossy rock
                      with using a thunder stone, using a leaf stone, and leveling up with a held casteliacone.
    - **Friendship** - Replaces friendship based evolutions with level up evolutions.
    - **PID** - Replaces personality value based evolutions. Gender dependant evolutions lose their gender dependency,
                Wurmple's random evolutions will require a Butterfree/Venomoth in your party, and Burmy will also evolve
                into Mothim while having a Venomoth in your party. Be aware that this can lead to affected pokemon
                changing their gender when evolved.
    - **Stats** - Replaces Tyrogue's stat based evolutions with level up while holding a protein, iron, or carbos.
    """
    display_name = "Replace Evolution Methods"
    valid_keys = [
        "Locations",
        "Friendship",
        "PID",
        "Stats",
    ]
    default = []


class WonderTrade(Toggle):
    """
    Enables pokemon being sent to and received from the datastorage wonder trade protocol.
    """
    display_name = "Wonder Trade"
    default = False


class MultiworldGiftPokemon(Toggle):
    """
    Adds pokemon to the item pool that can be obtained from an npc in [TBD] after receiving
    the corresponding item from another player. Pokemon will only be placed in other worlds and
    have a species that matches the theme of that world (if defined).
    """
    display_name = "Multiworld Gift Pokemon"
    default = False


class TrapsProbability(Range):
    """
    Determines the probability of every randomly generated filler item being replaced by a random trap item.
    """
    display_name = "Traps Probability"
    default = 0
    range_start = 0
    range_end = 100


class ModifyItemPool(OptionSet):
    """
    Modifies what items your world puts into the item pool.

    - **Useless key items** - Adds one of each unused key item with filler classification.
    - **Useful filler** - Main bag items that would normally occur only once can be generated multiple times.
    - **Ban bad filler** - Bans niche berries and mail from being generated as filler items.
    """
    display_name = "Modify Item Pool"
    valid_keys = [
        "Useless key items",
        "Useful filler",
        "Ban bad filler",
    ]
    default = []


class ModifyLogic(OptionSet):
    """
    Modifies parts of what's logically required for various locations.

    - **Require Dowsing Machine** - Makes the Dowsing Machine a logical requirement to find hidden items.
    - **Prioritize key item locations** - Marks locations, that normally contain key items (which also includes
                                          badge rewards in gyms), as priority locations, making them mostly contain
                                          progressive items.
    """
    display_name = "Modify Item Pool"
    valid_keys = [
        "Require Dowsing Machine",
        "Prioritize key item locations",
    ]
    default = ["Require Dowsing Machine", "Prioritize key item locations"]


class FunnyDialogue(Toggle):
    """
    Adds humorous dialogue submitted by the folks in the Pokemon Black and White thread of the
    Archipelago Discord server. This option requires Text Plando being enabled in the host settings.
    """
    display_name = "Funny Dialogue"
    default = 0


class PokemonBWTextPlando(PlandoTexts):
    """
    Replaces specified text lines. Every entry follows the following format:
    ```
    - text: 'This is your text'
      at: text_key
      percentage: 100
    ```
    Refer to the Text Plando guide of this game for further information.
    """
    display_name = "Text Plando"
    default = [
        ("story 160 0 7", "[vMisc_0] received [vPkmn_1]![NextLine] Congratulations![Terminate]", 100),
        ("system 172 0 1", "Huh? Why did you press the[NextLine]B button?[Terminate]", 100),
    ]

    def verify_keys(self) -> None:
        invalid = []
        for word in self:
            parts = word.at.casefold().split()
            reasons = []
            if len(parts) < 4:
                reasons.append("Not enough arguments")
            if len(parts) > 4:
                reasons.append("Too many arguments")
            if parts[0] not in ("system", "story"):
                reasons.append("Unknown module")
            if not parts[1].isnumeric():
                reasons.append("File index is not a number")
            if not parts[2].isnumeric():
                reasons.append("Part index is not a number")
            if not parts[3].isnumeric():
                reasons.append("Line index is not a number")
            if reasons:
                invalid.append((" ".join(parts), reasons))
        if invalid:
            raise OptionError(
                f"Invalid \"at\" placement{'s' if len(invalid) > 1 else ''} " +
                f"in {getattr(self, 'display_name', self)}:\n" +
                "\n".join((f"{entry[0]}: {', '.join(entry[1])}" for entry in invalid)) +
                "\nRefer to the Text Plando guide of this game for further information."
            )


class ReusableTMs(Choice):
    """
    Enables reusable TMs, allowing for the reuse of TMs. 
    """
    display_name = "Reusable TMs"
    option_on = 0
    option_yes = 1
    option_of_course = 2
    option_im_not_a_masochist = 3
    default = 0


@dataclass
class PokemonBWOptions(PerGameCommonOptions):
    # General
    goal: Goal
    version: GameVersion

    # Pokemon encounters
    # randomize_wild_pokemon: RandomizeWildPokemon
    # randomize_trainer_pokemon: RandomizeTrainerPokemon
    # randomize_starter_pokemon: RandomizeStarterPokemon
    # randomize_static_pokemon: RandomizeStaticPokemon
    # randomize_gift_pokemon: RandomizeGiftPokemon
    # randomize_trade_pokemon: RandomizeTradePokemon
    # randomize_legendary_pokemon: RandomizeLegendaryPokemon

    # Pokemon stats
    # randomize_base_stats: RandomizeBaseStats
    # base_stat_total_limits: BaseStatTotalLimits
    # randomize_evolutions: RandomizeEvolutions
    # randomize_level_up_movesets: RandomizeLevelUpMovesets
    # randomize_tm_hm_compatibility: RandomizeTMHMCompatibility
    # randomize_types: RandomizeTypes
    # randomize_abilities: RandomizeAbilities
    # randomize_catch_rates: RandomizeCatchRates
    # catch_rates_limits: CatchRatesLimits
    # randomize_gender_ratio: RandomizeGenderRatio
    # gender_ratio_limits: GenderRatioLimits

    # Items, locations, and progression
    shuffle_badges: ShuffleBadgeRewards
    shuffle_tm_hm: ShuffleTMRewards
    # shuffle_roadblock_reqs: ShuffleRoadblockReqs
    # additional_roadblocks: AdditionalRoadblocks
    dexsanity: Dexsanity
    # trainersanity: Trainersanity
    # seensanity: Seensanity
    # door_shuffle: DoorShuffle
    season_control: SeasonControl

    # Miscellaneous
    # adjust_levels: AdjustLevels
    # exp_modifier: ExpModifier
    # all_pokemon_seen: AllPokemonSeen
    # add_fairy_type: AddFairyType
    # replace_evo_methods: ReplaceEvoMethods
    # deathlink: DeathLink  # Needs to be imported from base options
    # wonder_trade: WonderTrade
    # multiworld_gift_pokemon: MultiworldGiftPokemon
    # traps_percentage: TrapsPercentage
    modify_item_pool: ModifyItemPool
    modify_logic: ModifyLogic
    # funny_dialogue: FunnyDialogue
    # text_plando: TextPlando
    reusable_tms: ReusableTMs
