import logging
from dataclasses import dataclass
from typing import Dict, Any, TYPE_CHECKING

from decimal import Decimal, ROUND_HALF_UP

from Options import DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, TextChoice, PlandoConnections, \
                     PerGameCommonOptions, OptionGroup, Removed, Visibility, NamedRange
if TYPE_CHECKING:
    from . import FF1pixelWorld


class ShuffleGearShops(DefaultOnToggle):
    """
    Shuffle the content of all Weapon Shops together, and do the same for Armor Shops.
    """
    internal_name = "shuffle_gear_shops"
    display_name = "Shuffle Gear Shops"

class ShuffleSpells(DefaultOnToggle):
    """
    Shuffle Spells amongst their own School.
    """
    internal_name = "shuffle_spells"
    display_name = "Shuffle Spells"

class JobPromotion(Choice):
    """
    Set how Promotion Jobs are handled.

    Bahamut: Giving the Rat's Tail to Bahamut promote all Characters.

    Promote All Item: A Promote All Item is added to the Item Pool, when found all Characters promote.
    Bahamut becomes a Location.

    Job Item: All six Promotion Jobs become an individual Item added to the Item Pool.
    When acquired, all characters of the corresponding base Job promote. Bahamut becomes a Location.
    """
    internal_name = "job_promotion"
    display_name = "Job Promotion"
    option_bahamut = 0
    option_promote_all_item = 1
    option_job_item = 2
    default = 0

class ShuffleTrialsMaze(DefaultOnToggle):
    """
    Shuffle the Pillars Maze on floor 2F of the Citadel of Trials.
    """
    internal_name = "shuffle_trials_maze"
    display_name = "Shuffle Trials' Maze"

class EarlyProgression(Choice):
    """
    Set how the world is opened at the start of the game.

    Bikke's Ship: The Bridge is built from the start and Bikke will always give the Ship.

    Marsh Cave Path: Open a path to the West of Cornelia that allows you to reach the Marsh Cave area by foot.
    The Bridge is never built. The Ship is shuffled with other items and Bikke is a Location.
    """
    internal_name = "early_progression"
    display_name = "Early Progression"
    option_bikke_ship = 0
    option_marsh_cave_path = 1
    default = 0

class NerfChaos(DefaultOnToggle):
    """
    Halve Chaos' HP and reduce his Intelligence and Attack Power by 25%.
    """
    internal_name = "nerf_chaos"
    display_name = "Nerf Chaos"

class MonsterParties(Choice):
    """
    Randomize Monster Parties.
    Standard: Original Monster Parties are maintained.
    No Variance: Monsters will be replaced by Monsters of roughly the same power.
    Low Variance: Monsters can be replaced by slightly weaker or slightly stronger Monsters.
    High Variance: Monsters can be replaced by much weaker or much stronger Monsters.
    """
    internal_name = "monster_parties"
    display_name = "Monster Parties"
    option_standard = 0
    option_random_no_variance = 1
    option_random_low_variance = 2
    option_random_high_variance = 3
    default = 1

class MonstersCap(Choice):
    """
    If Monster Parties are randomized, bound Power Variance.
    This option doesn't do anything for Standard and No Variance choices.
    None: Variance is unbounded, Randomized Monster Parties can be weaker or stronger.
    Upper Bound: Randomized Monsters cannot be more powerful than the replaced Monsters, but they can be weaker.
    Lower Bound: Randomized Monsters cannot be weaker than the replaced Monsters, but they can be more powerful.
    """
    internal_name = "monsters_cap"
    display_name = "Variance Cap"
    option_none = 0
    option_upper_bound = 1
    option_lower_bound = 2
    default = 0

class DungeonEncounterRate(Choice):
    """
    Modify the Encounter Rate in dungeons by the multiplier selected.
    NOTE: This option doesn't affect the Boost setting to disable/enable encounters.
    """
    internal_name = "dungeon_encounter_rate"
    display_name = "Dungeon Encounter Rate"
    option_0_00x = 0
    option_0_25x = 1
    option_0_50x = 2
    option_0_75x = 3
    option_1_00x = 4
    option_1_25x = 5
    option_1_50x = 6
    default = 3

class OverworldEncounterRate(Choice):
    """
    Modify the Encounter Rate on the Overworld by the multiplier selected.
    NOTE: This option doesn't affect the Boost setting to disable/enable encounters.
    """
    internal_name = "overworld_encounter_rate"
    display_name = "Overworld Encounter Rate"
    option_0_00x = 0
    option_0_25x = 1
    option_0_50x = 2
    option_0_75x = 3
    option_1_00x = 4
    option_1_25x = 5
    option_1_50x = 6
    default = 3

class ExperienceBoost(Choice):
    """
    Set the default Experience Boost multiplier. This can still be modified in the Boost menu.
    """
    internal_name = "xp_boost"
    display_name = "Experience Boost"
    option_0_5x = 0
    option_1_0x = 1
    option_2_0x = 2
    option_3_0x = 3
    option_4_0x = 4
    default = 2

class GilBoost(Choice):
    """
    Set the default Gil Boost multiplier. This can still be modified in the Boost menu.
    """
    internal_name = "gil_boost"
    display_name = "Gil Boost"
    option_0_5x = 0
    option_1_0x = 1
    option_2_0x = 2
    option_3_0x = 3
    option_4_0x = 4
    default = 2

class BoostMenu(DefaultOnToggle):
    """
    Enable/Disable the in-game Boost menu. This will lock you to your current XP, Gil and Encounter Rate options.
    """
    internal_name = "boost_menu"
    display_name = "Boost Menu"

@dataclass
class FF1pixelOptions(PerGameCommonOptions):
    # generation options
    shuffle_gear_shops: ShuffleGearShops
    shuffle_spells: ShuffleSpells
    job_promotion: JobPromotion
    nerf_chaos: NerfChaos
    monster_parties: MonsterParties
    monsters_cap: MonstersCap
    dungeon_encounter_rate: DungeonEncounterRate
    overworld_encounter_rate: OverworldEncounterRate
    shuffle_trials_maze: ShuffleTrialsMaze
    early_progression: EarlyProgression
    xp_boost: ExperienceBoost
    gil_boost: GilBoost
    boost_menu: BoostMenu


grouped_options = [
    OptionGroup("Items Options", [
        ShuffleGearShops,
        ShuffleSpells,
        JobPromotion
    ]),
    OptionGroup("Map Options", [
        ShuffleTrialsMaze,
        EarlyProgression
    ]),
    OptionGroup("Monsters Options", [
        NerfChaos,
        MonsterParties,
        MonstersCap
    ]),
    OptionGroup("Scaling Options", [
        DungeonEncounterRate,
        OverworldEncounterRate,
        ExperienceBoost,
        GilBoost,
        BoostMenu
    ])
]

presets = {
    "Starter": {
        "shuffle_gear_shops": True,
        "shuffle_spells": True,
        "job_promotion": 0,
        "shuffle_trials_maze": True,
        "early_progression": 0,
        "nerf_chaos": True,
        "monster_parties": 1,
        "monsters_cap": 0,
        "dungeon_encounter_rate": 2,
        "overworld_encounter_rate": 2,
        "xp_boost": 3,
        "gil_boost": 3,
        "boost_menu": True,
    }}