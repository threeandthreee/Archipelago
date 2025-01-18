from dataclasses import dataclass
from math import ceil

from Options import PerGameCommonOptions, Choice, DefaultOnToggle, Toggle, Range, OptionSet, OptionDict
#from . import Levels


class GoalChaosEmeralds(DefaultOnToggle):
    """
        Determines if chaos emeralds are required for completion.
    """
    display_name = "Goal: Chaos Emeralds"

class GoalMissions(Range):
    """
        Determines what percentage of general missions are required for completion, rounded up.
    """
    display_name = "Goal: Missions"
    range_start = 0
    range_end = 100
    default = 75

class GoalDarkMissions(Range):
    """
        Determines what percentage of dark missions are required for completion, rounded up.
    """
    display_name = "Goal: Dark Missions"
    range_start = 0
    range_end = 100
    default = 0

class GoalHeroMissions(Range):
    """
        Determines what percentage of hero missions are required for completion, rounded up.
    """
    display_name = "Goal: Hero Missions"
    range_start = 0
    range_end = 100
    default = 0

class GoalObjectiveMissions(Range):
    """
        Determines what percentage of objective missions are required for completion, rounded up.
    """
    display_name = "Goal: Objective Missions"
    range_start = 0
    range_end = 100
    default = 0

class GoalFinalMissions(Range):
    """
        Determines what percentage of final missions are required for completion, rounded up.
    """
    display_name = "Goal: Final Missions"
    range_start = 0
    range_end = 100
    default = 0

class ObjectiveSanity(DefaultOnToggle):
    """Determines if objective based checks are enabled."""
    display_name = "Objective Sanity"

class ObjectivePercentage(Range):
    """Sets the objective percentage for each objective.
    When playing objectsanity, this removes the locations for anything after the percentage objective.
    The remaining items however will still be in the pool.
    When playing without objectsanity, the requirement to finish is reduced also."""
    display_name = "Objective Percentage"
    range_start = 1
    range_end = 100
    default = 100

class EnemyObjectivePercentage(Range):
    """When playing Objective Sanity, determine the percentage of items required to finish stages for enemy objectives."""
    display_name = "Enemy Objective Percentage"
    range_start = 1
    range_end = 100
    default = 90

class ObjectiveCompletionPercentage(Range):
    """When playing Objective Sanity, determine the percentage of items required to finish stages."""
    display_name = "Objective Completion Percentage"
    range_start = 1
    range_end = 100
    default = 100

class ObjectiveCompletionEnemyPercentage(Range):
    """When playing Enemy Objective Sanity, determine the percentage of items required to finish stages."""
    display_name = "Objective Completion Enemy Percentage"
    range_start = 1
    range_end = 100
    default = 90


class ObjectiveItemPercentageAvailable(Range):
    """When playing Objective Sanity, determine the percentage of items required to finish stages left in the pool."""
    display_name = "Objective Item Percentage"
    range_start = 1
    range_end = 1000
    default = 100

class ObjectiveItemEnemyPercentageAvailable(Range):
    """When playing Objective Sanity, determine the percentage of items for enemy objectives required to finish stages left in the pool."""
    display_name = "Objective Item Enemy Percentage"
    range_start = 1
    range_end = 1000
    default = 100

class EnemyObjectiveSanity(DefaultOnToggle):
    """Determines if enemy-based objective checks are enabled."""
    display_name = "Enemy Objective Sanity"

class Enemysanity(Toggle):
    """Determines whether standard enemy sanity is enabled."""
    display_name = "Enemy Sanity"

class Keysanity(Toggle):
    """Determines whether key sanity is enabled."""
    display_name = "Key Sanity"

class Doorsanity(Toggle):
    """Determines whether key door sanity is enabled."""
    display_name = "Door Sanity"

class Checkpointsanity(Toggle):
    """Determines whether checkpoint sanity is enabled."""
    display_name = "Checkpoint Sanity"

class CharacterSanity(Toggle):
    """Determines if character checks are enabled"""
    display_name = "Character Sanity"

class WeaponsanityUnlock(Toggle):
    """Determines whether weapons are required to be obtained from the pool of items."""
    display_name = "Weapon Sanity Unlock"

class WeaponsanityHold(Choice):
    """Determines whether game contains checks for legally holding each weapon.
    If unlocked is chosen, you must unlock the weapon with unlock first.
    If on is chosen, you will still lose the item in this mode, but will get the check.
    """
    display_name = "Weapon Sanity Hold"
    option_off = 0  # No checks for holding weapons
    option_unlocked = 1  # Requires the item to be unlocked to get the check.
    option_on = 2  # Does not require the item to be unlocked to get the check.
    default = 0

class VehicleLogic(Toggle):
    """Determines if vehicle logic is active. Does not currently affect gameplay."""
    display_name = "Vehicle Logic"

class GaugeFiller(DefaultOnToggle):
    """Determines if gauge filler is included."""
    display_name = "Gauge Filler"


class EnemySanityPercentage(Range):
    """Determines the percentage of enemysanity checks in a stage to be included."""
    display_name = "Enemy Sanity Percentage"
    range_start = 25
    range_end = 100
    default = 50

class StartingStages(Range):
    """Determines the number of stages that start unlocked."""
    display_name = "Starting Stages"
    range_start = 0
    range_end = 22
    default = 1

class ForceObjectiveSanityChance(Range):
    """Determines the probability of a objective-sanity stage being force-added to Priority Locations"""
    display_name = "Force Objective Sanity Mission Chance"
    range_start = 0
    range_end = 100
    default = 25

class ForceObjectiveSanityMax(Range):
    """Determines the upper limit of total objectsanity items in priority locations."""
    display_name = "Force Objective Sanity Max"
    range_start = 0
    range_end = 60
    default = 10

class ForceObjectiveSanityMaxCounter(Range):
    """Determines the upper limit of stages to be forced into priority locations."""
    display_name = "Force Objective Sanity Max"
    range_start = 0
    range_end = 1000
    default = 1000

class ExcludedStages(OptionSet):
    """Stage names to exclude checks from."""
    display_name = "Excluded Stages"
    default = {}
    #valid_keys = [i for i in Levels.LEVEL_ID_TO_LEVEL.values() ]

class ExceedingItemsFiller(Choice):
    """Determines whether game marks non-required items as progression or not."""
    display_name = "Exceeding Items Filler"
    option_off = 0  # Never convert exceeding items into filler
    option_minimise = 1  # Minimise exceeding items into filler
    option_always = 2  # Always mark exceeding items as filler
    default = option_minimise

class RingLink(Toggle):
    """
    Whether your in-level ring gain/loss is linked to other players.
    """
    display_name = "Ring Link"

class AutoClearMissions(DefaultOnToggle):
    """
        Set automatic clears for missions once objective criteria is achieved.
    """
    display_name = "Auto Clear Missions"

class LevelProgression(Choice):
    """Which type of logic to use for progression through the game."""
    display_name = "Level Progression"
    option_select = 0  # All stages will be unlocked through unlocks to Select Mode
    option_story = 1  # All stages will only be unlocked through story mode progression
    option_both = 2  # Stages can be unlocked through story mode progression or unlocked for Select Mode
    default = option_select

class PercentOverrides(OptionDict):
    """List of provided keys to dictate percentage based overrides."""
    display_name = "Percent Overrides"

class LogicLevel(Choice):
    """Determines the logic level for playthrough."""
    display_name = "Logic Level"
    option_easy = 0  # Logic adds in easier elements for completion
    option_normal = 1  # Standard logic
    option_hard = 2  # Requires skips to traverse regions.
    default = option_normal

class AllowDangerousPercentage(Toggle):
    """Allows setting dangerous logic for percentages for objectives"""
    display_name = "Dangerous Percentage"
    option_off = 0
    option_on = 1
    default = option_off

class BossChecks(Toggle):
    """
        Determines if bosses provide checks. On vanilla story mode, bosses will still have to be fought to progress.
    """
    display_name = "Boss Checks"

@dataclass
class ShadowTheHedgehogOptions(PerGameCommonOptions):
    #goal: Goal
    #goal_percentage: GoalMissionPercentage
    goal_chaos_emeralds: GoalChaosEmeralds
    goal_missions: GoalMissions
    goal_final_missions: GoalFinalMissions
    goal_hero_missions: GoalHeroMissions
    goal_dark_missions: GoalDarkMissions
    goal_objective_missions: GoalObjectiveMissions
    objective_sanity: ObjectiveSanity
    objective_percentage: ObjectivePercentage
    objective_enemy_percentage: EnemyObjectivePercentage
    objective_completion_percentage: ObjectiveCompletionPercentage
    objective_completion_enemy_percentage: ObjectiveCompletionEnemyPercentage
    objective_item_percentage_available: ObjectiveItemPercentageAvailable
    objective_item_enemy_percentage_available: ObjectiveItemEnemyPercentageAvailable
    enemy_objective_sanity: EnemyObjectiveSanity
    character_sanity: CharacterSanity
    enemy_sanity: Enemysanity
    key_sanity: Keysanity
    #door_sanity: Doorsanity
    checkpoint_sanity: Checkpointsanity
    enemy_sanity_percentage: EnemySanityPercentage
    starting_stages: StartingStages
    force_objective_sanity_chance: ForceObjectiveSanityChance
    force_objective_sanity_max: ForceObjectiveSanityMax
    force_objective_sanity_max_counter: ForceObjectiveSanityMaxCounter
    excluded_stages: ExcludedStages
    weapon_sanity_unlock: WeaponsanityUnlock
    weapon_sanity_hold: WeaponsanityHold
    vehicle_logic: VehicleLogic
    exceeding_items_filler: ExceedingItemsFiller
    enable_gauge_items: GaugeFiller
    ring_link: RingLink
    auto_clear_missions: AutoClearMissions
    level_progression: LevelProgression
    percent_overrides: PercentOverrides
    logic_level: LogicLevel
    allow_dangerous_settings: AllowDangerousPercentage

    #boss_checks: BossChecks



