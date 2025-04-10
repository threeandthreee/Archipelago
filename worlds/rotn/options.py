from Options import Toggle, Range, Choice, DeathLink, ItemSet, OptionSet, PerGameCommonOptions, OptionGroup, Removed
from dataclasses import dataclass

class StartingSongs(Range):
    """The number of songs that will be unlocked from the start"""
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"

class AdditionalSongs(Range):
    """The total number of songs that will be placed in the randomization pool.
    - This does not count any starting songs or the goal song.
    - The final song count may be lower due to other settings.
    """
    range_start = 15
    range_end = 100
    default = 30
    display_name = "Additional Song Count"

class DuplicateSongPercentage(Range):
    """
    Percentage of duplicate songs to place in remaining filler slots.
    Duplicate songs are considered Useful and thus out of logic.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Duplicate Song Percentage"

class IncludeMinigames(Toggle):
    """
    Not Yet Implemented

    Adds minigames to the song pool
    """
    display_name = "Include Minigames"

class IncludeBossBattles(Toggle):
    """
    Not Yet Implemented
    
    Add boss battles to the song pool
    """
    display_name = "Include Boss Battles"

class MinIntensity(Range):
    """
    Ensures chosen rhythm rift will have a chart with an intensity value higher than this value 
    """
    range_start = 1
    range_end = 99
    default = 1
    display_name = "Minimum Intensity"

class MaxIntensity(Range):
    """
    Ensures chosen rhythm rift will have a chart with an intensity value lower than this value
    """
    range_start = 1
    range_end = 99
    default = 30
    display_name = "Maximum Intensity"

class GradeNeeded(Choice):
    """
    Not Yet Implemented

    Required grade that needs to be achieved to send a check
    """
    display_name = "Grade Needed"
    option_Any = 0
    option_C = 1
    option_B = 2
    option_A = 3
    option_S = 4
    option_S_Plus = 5
    default = 0

class DiamondCountPercentage(Range):
    """The percentage of Diamonds in the item pool that are needed to unlock the winning song."""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Diamonds Needed to Win"

class DiamondWinPercentage(Range):
    """The percentage of Diamonds in the item pool that are needed to unlock the winning song."""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Diamonds Needed to Win"

class IncludeSongs(ItemSet):
    """
    These songs will be guaranteed to show up within the seed.
    - You must have the DLC enabled to play these songs.
    - Difficulty options will not affect these songs.
    - If there are too many included songs, this will act as a whitelist ignoring song difficulty.
    """
    verify_item_name = True
    display_name = "Include Songs"


class ExcludeSongs(ItemSet):
    """
    These songs will be guaranteed to not show up within the seed.
    
    Note: Does not affect songs within the "Include Songs" list.
    """
    verify_item_name = True
    display_name = "Exclude Songs"

@dataclass
class RotNOptions(PerGameCommonOptions):
    starting_song_count: StartingSongs
    additional_song_count: AdditionalSongs
    duplicate_song_percentage: DuplicateSongPercentage
    include_minigames: IncludeMinigames
    include_boss_battle: IncludeBossBattles
    min_intensity: MinIntensity
    max_intensity: MaxIntensity
    grade_needed: GradeNeeded
    diamond_count_percentage: DiamondCountPercentage
    diamond_win_percentage: DiamondWinPercentage
    death_link: DeathLink
    include_songs: IncludeSongs
    exclude_songs: ExcludeSongs