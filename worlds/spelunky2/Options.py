from Options import Toggle, DefaultOnToggle, Range, Choice, PerGameCommonOptions, DeathLink
from dataclasses import dataclass


class Goal(Choice):
    """When is your world considered finished.
    Tiamat: Requires completing the "normal" ending by reaching 6-4 and defeating Tiamat
    Hundun: Requires completing the "hard" ending by reaching 7-4 and defeating Hundun
    Cosmic Ocean: Requires reaching a specified level in Cosmic Ocean"""
    display_name = "Goal"
    option_tiamat = 0
    option_hundun = 1
    option_cosmic_ocean = 2
    default = 0


class GoalLevel(Range):
    """Which level in Cosmic Ocean are you required to clear to consider your game as beaten.
    This option can be ignored if your goal is not set to \"Cosmic Ocean\""""
    display_name = "Cosmic Ocean Goal Level"
    range_start = 10
    range_end = 99
    default = 30


class ProgressiveWorlds(DefaultOnToggle):
    """Whether new worlds should be unlocked individually or progressively."""
    display_name = "Progressive Worlds"


"""
# Not implemented yet
class ProgressiveShortcuts(DefaultOnToggle):
    \"""Whether new shortcuts should be unlocked individually or progressively.\"""
    display_name = "Progressive Shortcuts"
"""

class StartingHealth(Range):
    """How much Health should you initially start with."""
    display_name = "Starting Health"
    range_start = 1
    range_end = 8
    default = 4


class StartingBombs(Range):
    """How many Bombs should you initially start with."""
    display_name = "Starting Bombs"
    range_start = 0
    range_end = 10
    default = 4


class StartingRopes(Range):
    """How many Ropes should you initially start with."""
    display_name = "Starting Ropes"
    range_start = 0
    range_end = 10
    default = 4


class EnableTraps(Toggle):
    """Whether traps should be included in the item pool."""
    display_name = "Enable Traps"


class TrapWeight(Range):
    """Determines the percentage of filler items that will be replaced by traps."""
    display_name = "Trap Percentage"
    range_start = 5
    range_end = 30
    default = 15


class PoisonTrapChance(Range):
    """Sets the likelihood of a trap being a Poison Trap relative to other traps.
    Poison Traps will instantly poison the player."""
    display_name = "Poison Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class CurseTrapChance(Range):
    """Sets the likelihood of a trap being a Curse Trap relative to other traps.
    Curse Traps will instantly curse the player."""
    display_name = "Curse Trap Weight"
    range_start = 0
    range_end = 100
    default = 5


class GhostTrapChance(Range):
    """Sets the likelihood of a trap being a Ghost Trap relative to other traps.
    Ghost Traps will immediately spawn the ghost (or Jelly if in Cosmic Ocean)."""
    display_name = "Ghost Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class StunTrapChance(Range):
    """Sets the likelihood of a trap being a Stun Trap relative to other traps.
    Stun Traps wll stun the player for 1 second."""
    display_name = "Stun Trap Weight"
    range_start = 0
    range_end = 100
    default = 25


class LooseBombsTrapChance(Range):
    """Sets the likelihood of a trap being a Loose Bombs Trap relative to other traps.
    Loose Bombs Traps will spawn 1 lit bomb at the player's feet every second for 5 seconds."""
    display_name = "Loose Bombs Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class BlindnessTrapChance(Range):
    """Sets the likelihood of a trap being a Blindness Trap relative to other traps.
    Blindness traps will trigger a darkness effect similar to the \"I can't see a thing!\" level
    feeling for the current level."""
    display_name = "Blindness Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class PunishBallTrapChance(Range):
    """Sets the likelihood of a trap being a Punish Ball Trap relative to other traps.
    Punish Ball Traps will attach a ball and chain to the player for 3 levels."""
    display_name = "Punish Ball Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class DeathLinkBypassesAnkh(Toggle):
    """Sets whether deaths sent through Death Link will trigger the Ankh, or ignore it."""
    display_name = "Death Link Ankh Handling"

@dataclass
class Spelunky2Options(PerGameCommonOptions):
    goal: Goal
    goal_level: GoalLevel
    progressive_worlds: ProgressiveWorlds
    # progressive_shortcuts: ProgressiveShortcuts - Not implemented yet
    starting_health: StartingHealth
    starting_bombs: StartingBombs
    starting_ropes: StartingRopes
    traps_enabled: EnableTraps
    trap_weight: TrapWeight
    poison_weight: PoisonTrapChance
    curse_weight: CurseTrapChance
    ghost_weight: GhostTrapChance
    stun_weight: StunTrapChance
    bomb_weight: LooseBombsTrapChance
    blind_weight: BlindnessTrapChance
    punish_weight: PunishBallTrapChance
    death_link: DeathLink
    bypass_ankh: DeathLinkBypassesAnkh
