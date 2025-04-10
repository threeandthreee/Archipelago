from dataclasses import dataclass
from Options import PerGameCommonOptions, Choice, DefaultOnToggle, Toggle, Range, OptionSet, OptionDict, OptionGroup
from worlds.shadow_the_hedgehog import Names


class GoalChaosEmeralds(DefaultOnToggle):
    """
        Determines if chaos emeralds are required for completion.
        If enabled, you require the 7 chaos emeralds to unlock your goal.
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


class GoalBosses(Range):
    """
        Determines what percentage of bosses are required for completion, rounded up.
    """
    display_name = "Goal: Bosses"
    range_start = 0
    range_end = 100
    default = 0

class GoalFinalBosses(Range):
    """
        Determines what percentage of final boss missions are required for completion, rounded up.
    """
    display_name = "Goal: Bosses"
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
    """
        Determines if objective based checks are enabled.
        Objectivesanity checks are all stage objectives for dark/hero missions.
        Please read the readme for more information.
    """
    display_name = "Objective Sanity"

class ObjectivePercentage(Range):
    """Sets the objective percentage for each objective.
    When playing objectsanity, this removes the locations for anything after the percentage objective.
    Only affects locations, use available/completion for goal-related effects."""
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
    """When playing Objective Sanity, determine the percentage of items required to finish stages.
    When playing non-objective, this is the amount required to complete the stage."""
    display_name = "Objective Completion Percentage"
    range_start = 1
    range_end = 100
    default = 100

class ObjectiveCompletionEnemyPercentage(Range):
    """
        When playing Enemy Objective Sanity, determine the percentage of items required to finish stages.
        This is specifically the enemy-based objectivesanity missions.
        For all enemies, refer to enemy sanity. These can be used in tandem.
    """
    display_name = "Objective Completion Enemy Percentage"
    range_start = 1
    range_end = 100
    default = 90


class ObjectiveItemPercentageAvailable(Range):
    """
        When playing Objective Sanity, determine the percentage of items required to finish stages left in the pool.
        This number MUST be higher than the required amount to clear.
        This number can exceed 100% if you want more items than there are to add,
        so long as you have location space.
    """
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
    """
        Determines whether standard enemy sanity is enabled.
        This can be used in tandem with enemy objectve sanity.
    """
    display_name = "Enemy Sanity"

class Keysanity(Toggle):
    """
        Determines whether key sanity is enabled.
        This enables checks as keys and does not add any items to the pool.
    """
    display_name = "Key Sanity"

class Doorsanity(Toggle):
    """Determines whether key door sanity is enabled."""
    display_name = "Door Sanity"

class Checkpointsanity(DefaultOnToggle):
    """
        Determines whether checkpoint sanity is enabled.
        This only adds checks and does not add anything to the pool.
    """
    display_name = "Checkpoint Sanity"

class CharacterSanity(DefaultOnToggle):
    """
        Determines if character checks are enabled.
        The first time you meet a character, the cutscene will play and provide a check.
        Disabling is handling by overwriting the value and cutscene will never play.
    """
    display_name = "Character Sanity"

class WeaponsanityUnlock(Toggle):
    """
        Determines whether weapons are required to be obtained from the pool of items.
        This will change the logic of same stages.
        Can be used alongside Weapon Groups for more flexibility.
    """
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

class RingFiller(DefaultOnToggle):
    """Determines if ring filler is included."""
    display_name = "Ring Filler"


class EnemySanityPercentage(Range):
    """Determines the percentage of enemysanity checks in a stage to be included."""
    display_name = "Enemy Sanity Percentage"
    range_start = 0
    range_end = 100
    default = 50

class StartingStages(Range):
    """
        Determines the number of stages that start unlocked in Select mode.
    """
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
    #default = {}
    valid_keys = [i for i in Names.getLevelNames() ]

class ExceedingItemsFiller(Choice):
    """Determines whether game marks non-required items as progression or not."""
    display_name = "Exceeding Items Filler"
    option_off = 0  # Never convert exceeding items into filler
    option_minimise = 1  # Minimise exceeding items into filler
    option_always = 2  # Always mark exceeding items as filler
    default = option_minimise

class RingLink(Choice):
    """
    Whether your in-level ring gain/loss is linked to other players.
    Off disabled the feature.
    On enables the feature excluding special cases.
    Unsafe disables ring link during Circus Park missions and during the final boss.

    """
    option_off = 0
    option_on = 1
    option_unsafe = 2

    display_name = "Ring Link"
    default = option_off

class AutoClearMissions(DefaultOnToggle):
    """
        Set automatic clears for missions once objective criteria is achieved. When playing story mode, ensure
        that the player has access to a new stage before auto-clearing to improve tracking behaviour.
        Auto clear is automatically disabled when playing on objective-less sanity.
    """
    display_name = "Auto Clear Missions"

class LevelProgression(Choice):
    """
        Which type of logic to use for progression through the game.
        Select will provide stage unlock items to unlock stages via the Select screen.
        Story will require the user to play through story mode.
        Select mode can still be used, but recommended to complete missions in story mode where possible.
    """
    display_name = "Level Progression"
    option_select = 0  # All stages will be unlocked through unlocks to Select Mode
    option_story = 1  # All stages will only be unlocked through story mode progression
    option_both = 2  # Stages can be unlocked through story mode progression or unlocked for Select Mode
    default = option_select

class SelectBosses(DefaultOnToggle):
    """
        Whether bosses can be unlocked via select mode.
        Note that mid-bosses require the ability to access the main stage in order to enter them.
    """
    display_name = "Select Bosses"

class PercentOverrides(OptionDict):
    """
        Advanced YAML setting to provide keys to dictate percentage based overrides.
        Read the setup_en.yaml for more information.
    """
    display_name = "Percent Overrides"
    valid_keys = Names.getValidPercentOverrides()
    default = {}

class WeaponGroups(OptionSet):
    """
    Group together confirmed sets of weapon items to unlock them in given batches.

    - Stage Melee Weapons: Non-required Stage Melee Weapons
    - Environment Weapons: All Stage Melee Environment Weapons
    - Egg Pawn Weapons: Used by Egg Pawns
    - GUN Launcher Weapons: Launching GUN Weapons
    - Black Warrior Weapons: Held by standard Black Arms
    - Black Oak Weapons: Held by big Black Arm enemies
    - Worm Weapons:  Held by Black Arm Worm enemies
    - Gun Solider Weapons: Held by GUN Soliders
    - Gun Mech Weapons: Held by GUN Mechs
    - Laser Weapons: Laser-style weapons
    """
    display_name = "Weapon Groups"
    valid_keys = []
    default = ["Stage Melee Weapons"]


class LogicLevel(Choice):
    """
        Determines the logic level for play-through.
        Easy: Some requirements are dialled back to make for a smoother early experience.
        Normal: Standard logic.
        Hard: Skips expected of the player in order to make progress.
    """
    display_name = "Logic Level"
    option_easy = 0  # Logic adds in easier elements for completion
    option_normal = 1  # Standard logic
    option_hard = 2  # Requires skips to traverse regions.
    default = option_normal

class BossLogicLevel(Choice):
    """
        Determines the boss logic level for playthrough.
        Easy boss logic ensures the player has access to one of the weapons within the stage in order to beat it.
    """
    display_name = "Boss Logic Level"
    option_easy = 0  # Logic adds in easier elements for completion
    option_normal = 1  # Standard logic
    option_hard = 2  # Requires skips to traverse regions.
    default = option_normal

class CraftLogicLevel(Choice):
    """
        Determines the craft logic level for playthrough - distinguishing a difference
        in logic for crafts in Iron Jungle, Lethal Highway and Air Fleet
    """
    display_name = "Logic Level"
    option_easy = 0  # Logic adds in easier elements for completion
    option_normal = 1  # Standard logic
    option_hard = 2  # Requires skips to traverse regions.
    default = option_normal

class AllowDangerousPercentage(Toggle):
    """
        Allows setting dangerous logic for percentages for objectives.
        Do not enable this unless you are very sure about what you are setting!
    """
    display_name = "Dangerous Percentage"
    option_off = 0
    option_on = 1
    default = option_off

class BossChecks(Toggle):
    """
        Determines if bosses provide checks. On vanilla story mode, bosses will still have to be fought to progress.
    """
    display_name = "Boss Checks"

class StoryShuffle(Choice):
    """
    Determines method for shuffling story stages.
    Off will disable the story shuffle and will instead require vanilla order.
    Chaos mode will shuffle the story. For more information on chaos shuffle, please read the documentation.
    """
    display_name = "Story Shuffle"
    option_off = 0  # Story stages will be in vanilla order
    #option_basic = 1
    #option_shuffle = 2
    option_chaos = 3
    default = option_off

class IncludeLastStoryShuffle(Toggle):
    """
        Determines whether to include Last Way / Devil Doom in the story shuffle.
        By enabling this, Devil Doom (the final fight) will be hidden in story mode and must be found
        in order to clear the game.
        Last Way goes to a random stage at the end, hence why Devil Doom MUST be shuffled in this way.
        Note, if you are in the Devil Doom stage without the goal unlocked, you will be unable to complete it,
        and must come back when unlocked.
    """
    display_name = "Include Last Story"


class SecretStoryProgression(Toggle):
    """
        When using trackers, hide the progress of stages until the player has found them in the story mode.
    """
    display_name = "Secret Story Progression"

class StoryBossCount(Range):
    """
        How many copies of each standard boss to feature through the story chain.
    """
    display_name = "Story Boss Count"
    range_start = 0
    range_end = 3
    default = 1

class GuaranteedLevelClear(DefaultOnToggle):
    """
        Ensures the first available stage in shuffled story mode is a completable mission out the gate.
        This option is ignored should you disable all stages meeting this criteria.
    """
    display_name = "Guaranteed Level Clear"

class SingleEggDealer(Toggle):
    """
        When shuffling story mode, only include a single Egg Dealer of the available 3.
    """
    display_name = "Single Egg Dealer"

class SingleBlackDoom(Toggle):
    """
        When shuffling story mode, only include a single Black Doom of the available 3.
    """
    display_name = "Single Black Doom"

class SingleDiablon(Toggle):
    """
        When shuffling story mode, only include a single Sonic & Diablon of the available 3.
    """
    display_name = "Single Diablon"

class RifleComponents(Toggle):
    """
        Whether parts are required for the Shadow Rifle to be complete and available.
    """
    display_name = "Shadow Rfile Components"

class ObjectiveFrequency(Range):
    """
        Frequency of checks for objective checks, i.e. if set to 4, each 4 progress is 1 check.
        This will always include the final check as well as every 4.
    """
    display_name = "Objective Frequency"
    range_start = 1
    range_end = 100
    default = 100

class EnemyObjectiveFrequency(Range):
    """
        Frequency of checks for enemy objective checks as percentage.
    """
    display_name = "Enemy Objective Frequency"
    range_start = 1
    range_end = 100
    default = 100

class EnemyFrequency(Range):
    """
        Frequency of checks for enemy checks, i.e. if set to 4, each 4 progress is 1 check.
    """
    display_name = "Enemy Frequency"
    range_start = 1
    range_end = 100
    default = 100

class MinimumRank(Choice):
    """Minimum rank required to get the location clear check."""
    display_name = "Minimum Rank"
    option_a = "A"
    option_b = "B"
    option_c = "C"
    option_d = "D"
    option_e = "E"
    default = option_e

class StoryProgressionBalancing(Range):
    """
        Story progression balancing to determine sphering for story stages.
        Refer to the documentation for more information.
    """
    range_start = 0
    range_end = 100
    default = 0

class ShadowMod(Choice):
    """
        Shadow Mod intended to be used. In order to use a mod you accept that the game may not yet
        be fully supported and that bugs will occur.
        Only vanilla is officially supported.
        Only mods in the list have any testing or handling at all.
        Minor mods will not affect memory and are likely to be fine.
    """
    display_name = "Shadow Mod"
    option_vanilla = "Vanilla"
    option_reloaded = "Reloaded"
    option_sx = "SX"
    default = option_vanilla

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
    goal_bosses: GoalBosses
    goal_final_bosses: GoalFinalBosses
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
    enable_ring_items: RingFiller
    ring_link: RingLink
    auto_clear_missions: AutoClearMissions
    level_progression: LevelProgression
    percent_overrides: PercentOverrides
    logic_level: LogicLevel
    boss_logic_level: BossLogicLevel
    craft_logic_level: CraftLogicLevel
    allow_dangerous_settings: AllowDangerousPercentage
    story_shuffle: StoryShuffle
    include_last_way_shuffle: IncludeLastStoryShuffle
    secret_story_progression: SecretStoryProgression
    story_boss_count: StoryBossCount
    guaranteed_level_clear: GuaranteedLevelClear
    single_egg_dealer: SingleEggDealer
    single_black_doom: SingleBlackDoom
    single_diablon: SingleDiablon
    rifle_components: RifleComponents
    objective_frequency: ObjectiveFrequency
    enemy_objective_frequency: EnemyObjectiveFrequency
    enemy_frequency: EnemyFrequency
    select_bosses: SelectBosses
    minimum_rank: MinimumRank
    weapon_groups: WeaponGroups
    story_progression_balancing: StoryProgressionBalancing
    shadow_mod: ShadowMod

shadow_option_groups = [
    OptionGroup("Goal",
        [GoalChaosEmeralds, GoalMissions, GoalFinalMissions,
         GoalHeroMissions, GoalDarkMissions, GoalObjectiveMissions,
         GoalBosses]),
    OptionGroup("Sanities", [ObjectiveSanity, EnemyObjectiveSanity,
                             CharacterSanity, Enemysanity, Keysanity,
                             Checkpointsanity, WeaponsanityUnlock, WeaponsanityHold,
                             WeaponGroups, SelectBosses,
                             VehicleLogic]),
    OptionGroup("Sanity Config", [LogicLevel, ObjectivePercentage, EnemyObjectivePercentage,
                                  ObjectiveCompletionPercentage, ObjectiveCompletionEnemyPercentage,
                                  ObjectiveItemPercentageAvailable, ObjectiveItemEnemyPercentageAvailable,
                                  EnemySanityPercentage, PercentOverrides,
                                  MinimumRank, EnemyFrequency, EnemyObjectiveFrequency,
                                  ObjectiveFrequency, BossLogicLevel, CraftLogicLevel], True),
    OptionGroup("Story", [LevelProgression, IncludeLastStoryShuffle, SecretStoryProgression,
                          StoryBossCount, GuaranteedLevelClear,
                          SingleDiablon, SingleBlackDoom, SingleEggDealer,
                          StoryProgressionBalancing ]),
    OptionGroup("Junk", [ExceedingItemsFiller, GaugeFiller], True),
    OptionGroup("Other", [StartingStages, ForceObjectiveSanityChance, ForceObjectiveSanityMax,
                          ForceObjectiveSanityMaxCounter, ExcludedStages,
                          AutoClearMissions, AllowDangerousPercentage,
                          RifleComponents], True)
]