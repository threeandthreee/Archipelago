from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Choice, PerGameCommonOptions


class JobPalettes(Toggle):
    """
    When enabled, randomizes palettes for each characters' jobs
    """
    display_name = "Randomize Job Palettes"
class FourJob(Toggle):
    """
    When enabled, enables four job mode. No crystals are placed in the world, and the player starts with 4 crystals.
    Players are disallowed from leaving the menu if every character doesnt have a unique job
    """
    display_name = "Enable Four Job Mode"

class RemoveFlashes(DefaultOnToggle):
    """
    When enabled, optional patches for removing flashes (notably Neo ExDeath) are applied
    """
    display_name = "Apply flash removal"

class WorldLock(Choice):
    """Determines how many worlds are available from the start.
    1: The first world is available. Adamantite unlocks World 2. Defeating Exdeath in World 2 unlocks World 3 via Anti Barrier and Bracelet.
    2: Worlds 1 and 2 are available. Defeating Exdeath in World 2 unlocks World 3 via Anti Barrier and Bracelet.
    3: All worlds are available immediately.    
    """
    display_name = "World Lock"
    option_world_1 = 0
    option_world_2 = 1
    option_world_3 = 2


class ProgressionChecks(Choice):
    """Determines where progression checks are in the game for the multiworld.
    1: All boss locations (before the Rift only) are valid checks for progression
    2: All bosses (before the Rift only), all events & all chests are valid checks for progression
    """
    display_name = "Progression Checks"
    option_bosses = 0
    option_all = 1



class TrappedChests(Toggle):
    """
    When enabled, 30 trapped chests will be spread across the world.
    These chests will only give high value items local to the player's world
    """
    display_name = "Enable Trapped Chests"



@dataclass
class ffvcd_options(PerGameCommonOptions):
    job_palettes: JobPalettes
    four_job: FourJob
    remove_flashes : RemoveFlashes
    world_lock : WorldLock
    progression_checks : ProgressionChecks
    trapped_chests: TrappedChests