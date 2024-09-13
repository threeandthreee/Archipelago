from dataclasses import dataclass

from Options import Toggle, Range, NamedRange, PerGameCommonOptions

class StartingWorlds(Range):
    """
    Number of random worlds to start with.
    """
    display_name = "Starting Worlds"
    default = 0
    range_start = 0
    range_end = 11

class EXPMultiplier(NamedRange):
    """
    Determines the multiplier to apply to EXP gained
    """
    display_name = "EXP Multiplier"
    default = 16
    range_start = default // 4
    range_end = 160
    special_range_names = {
        "0.25x": default // 4,
        "0.5x":  default // 2,
        "1x":    default,
        "2x":    default * 2,
        "3x":    default * 3,
        "4x":    default * 4,
        "8x":    default * 8,
        "10x":   default * 10,
    }

class Character(NamedRange):
    """
    Determines the expected player character.
    0: Ventus
    1: Aqua
    2: Terra
    """
    display_name = "Character"
    default = 2
    range_start = 0
    range_end = 2
    special_range_names = {
        "ventus": 0,
        "aqua":   1,
        "terra":  2,
    }

class FinalTerraXehanortII(Toggle):
    """
    Determines if Aqua will need to defeat Final Terra Xehanort II to complete her seed.
    Does nothing if the player chooses a character other than Aqua
    """
    display_name = "Final Terra Xehanort II"

class MirageArena(Toggle):
    """
    Determines if Mirage Arena locations should be included.
    """
    display_name = "Mirage Arena"

class CommandBoard(Toggle):
    """
    Determines if Command Board locations should be included.
    """
    display_name = "Command Board"

class SuperBosses(Toggle):
    """
    Determines if Super Boss locations should be included.
    """
    display_name = "Super Bosses"

class MaxHPIncreases(Range):
    """
    Number of Max HP Increases are in the item pool.
    """
    display_name = "Max HP Increases"
    default = 8
    range_start = 0
    range_end = 9

class RandomizeKeybladeStats(Toggle):
    """
    Determines if Keyblade stats should be randomized
    """
    display_name = "Randomize Keyblade Stats"

class KeybladeMinStrength(Range):
    """
    Determines the minimum Strength bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum STR Bonus"
    default = 2
    range_start = 2
    range_end = 10

class KeybladeMaxStrength(Range):
    """
    Determines the maximum Strength bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum STR Bonus"
    default = 10
    range_start = 10
    range_end = 10

class KeybladeMinMagic(Range):
    """
    Determines the minimum Magic bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum MP Bonus"
    default = -2
    range_start = -2
    range_end = 10

class KeybladeMaxMagic(Range):
    """
    Determines the maximum Magic bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum MP Bonus"
    default = 7
    range_start = -2
    range_end = 10

@dataclass
class KHBBSOptions(PerGameCommonOptions):
    character:       Character
    starting_worlds: StartingWorlds
    exp_multiplier:  EXPMultiplier
    final_terra_xehanort_ii:  FinalTerraXehanortII
    mirage_arena: MirageArena
    command_board: CommandBoard
    super_bosses: SuperBosses
    max_hp_increases: MaxHPIncreases
    randomize_keyblade_stats: RandomizeKeybladeStats
    keyblade_min_str: KeybladeMinStrength
    keyblade_max_str: KeybladeMaxStrength
    keyblade_min_mgc: KeybladeMinMagic
    keyblade_max_mgc: KeybladeMaxMagic
