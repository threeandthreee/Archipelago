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

class ShuffleTrialsMaze(DefaultOnToggle):
    """
    Shuffle the Pillars Maze on floor 2F of the Citadel of Trials.
    """
    internal_name = "shuffle_trials_maze"
    display_name = "Shuffle Trials' Maze"

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
    dungeon_encounter_rate: DungeonEncounterRate
    overworld_encounter_rate: OverworldEncounterRate
    shuffle_trials_maze: ShuffleTrialsMaze
    xp_boost: ExperienceBoost
    gil_boost: GilBoost
    boost_menu: BoostMenu

grouped_options = [
    OptionGroup("Shop Options", [
        ShuffleGearShops,
        ShuffleSpells,
    ]),
    OptionGroup("Map Options", [
        ShuffleTrialsMaze,
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
        "shuffle_trials_maze": True,
        "dungeon_encounter_rate": 2,
        "overworld_encounter_rate": 2,
        "xp_boost": 3,
        "gil_boost": 3,
        "boost_menu": True,
    }}