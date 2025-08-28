from dataclasses import dataclass
from typing import Type, Any, List
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Visibility, Option, OptionGroup
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions, StartInventoryPool

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in crystal_project_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list
#"""Goal Options"""
class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Checking the first sign in the Spawning Meadows will tell you the selected goal. A goal items counter is displayed on the in-game party screen in the menu.
    
    Astley: Defeat Astley in the New World. A New World Stone will be given to the player after obtaining a certain number of jobs (starting Jobs don't count).

    True Astley: A saga awaits you! Collect 4 Deity Eyes and the STEM WARD to challenge Gabriel for the Old World Stone. Then travel to the Old World to defeat Periculum and earn the Proof of Merit. Along the way, gather enough Jobs to unlock the New World Stone. Then you can venture to the New World to defeat true Astley to win!
    
    Clamshells: Collect enough clamshells for Mañana Man in Seaside Cliffs.
    """
    display_name = "Goal"
    option_astley = 0
    option_true_astley = 1
    option_clamshells = 2
    default = 0

class NewWorldStoneJobQuantity(Range):
    """
    If your goal is Astley, select how many Jobs you need to find before being sent the New World Stone for the final fight.

    This option is validated at generation time, and if it is higher than the number of jobs you can obtain, it will be capped to what is possible. By default, the maximum you can obtain is 18.

    Picking Job Rando: Full and decreasing the Starting Job Quantity will increase the maximum by that much. It will also increase if you enable mods that give you more.

    Picking Job Rando: None and Included Regions: Beginner or Advanced will reduce the maximum number available to 4 or 11, respectively.
    """
    display_name = "Job count that locks the New World Stone"
    range_start = 1
    range_end = 99
    default = 18

class ClamshellGoalQuantity(Range):
    """
    If your goal is Clamshells, select how many you need to win.

    (If your goal is not Clamshells, this setting does nothing. 3 Clamshells will be placed in your pool and the Mañana Man will ask for 2. Don't worry, he's cool with it.)
    """
    display_name = "Clamshells needed to win"
    range_start = 2
    range_end = 99
    default = 13
    
class ExtraClamshellsInPool(Range):
    """
    If your goal is Clamshells, pick how many more Clamshells than your goal value to have in the item pool.
    This option makes it so that you don't have to find every single Clamshell in your pool to win.

    (If your goal is not Clamshells, this setting does nothing.)
    """
    display_name = "Extra Clamshells in the pool"
    range_start = 0
    range_end = 99
    default = 6

#"""Location Options"""
class IncludedRegions(Choice):
    """
    Choose which regions to play in! Only locations within your chosen regions will give you checks; the rest will be empty.
    This can be used to adjust the difficulty and length of your game.

    NOTE: Make sure to include the region that has the finish line of your chosen goal in it!
    Example: if your goal is Astley, Advanced is considered to have that finish line, so you can pick Advanced, Expert, or All.

    Beginner: Only regions up through the end of Skumparadise will have checks. Finish Line: Clamshells

    Advanced: Regions up to Salmon Bay will have checks. Finish Line: Astley (Note: Level Gating's Level Catch-Up Option is recommended for Astley on Advanced.)

    Expert: Regions up to The Deep Sea will have checks. (Note: The Depths will not be included.)

    All: Every region is included. Finish Line: True Astley
    """
    display_name = "Regions to include in game"
    option_beginner = 0
    option_advanced = 1
    option_expert = 2
    option_all = 3
    default = 3

class JobRando(Choice):
    """
    None: all Jobs are at their normal crystal locations in the vanilla game.

    Crystal: all vanilla Jobs normally received from crystals are chucked into the item pool.

    Full: your starting jobs are randomized, and the rest of the vanilla Jobs are added to the item pool. Adjust the Starting Job Quantity (see below) for how many random Jobs you start with.
    """
    display_name = "Job Rando"
    option_none = 0
    option_crystal = 1
    option_full = 2
    default = 2

class StartingJobQuantity(Range):
    """
    Select how many Jobs you start with. (This setting only does anything if JobRando is set to Full.)
    """
    display_name = "Starting Job Quantity"
    range_start = 1
    range_end = 6
    default = 6

class KillBossesMode(Toggle):
    """
    When enabled, defeating a boss will provide checks.

    WARNING: If you restrict the Included Regions to Beginner or Advanced, checks will require defeating level 50+ bosses in some of the early areas!
    You may want to set the Level Gating option to Level Catch-Up.  Without it, you are signing up to either grind or fight the bosses under-leveled.
    """
    display_name = "Kill Bosses Mode"

class Shopsanity(Choice):
    """
    When enabled, all shop inventories will be replaced with checks. Be prepared, adventurer.

    Choosing "enabled and hint" will automatically create a hint for any item available in a store after you have visited it for the first time,
    letting other players in the multiworld know you've seen their item.
    """
    display_name = "Shopsanity"
    option_disabled = 0
    option_enabled = 1
    option_enabled_and_hint = 2
    default = 0

class Regionsanity(Toggle):
    """
    Nothing I have tried has been able to drive the citizens of Sequoia to collect enough crystals!
    Adventurers have had TOO MUCH freedom!  From now on, you will adventure where I tell you to.
    Unless you have a pass from ME, you won't be able to do any adventuring!
    - Grandmaster

    When enabled, the grandmaster will not permit you to interact with anything in a region
    without receiving his "official permission" (i.e. "Item - Spawning Meadows Pass").
    However, the Overpass and Underpass are regions of lawlessness where the Grandmaster has no authority! ;)
    (You're also still allowed to use the save points, we won't tell.)

    You will start the game with a pass for one reachable region.
    """
    display_name = "Regionsanity"

#"""Progression Options"""
class ProgressiveMountMode(DefaultOnToggle):
    """
    When enabled, all mount items are combined into a Progressive Mount Instrument and will be received in the approximate order you would receive them in the vanilla game every time:
       Quintar Pass -> Quintar Flute -> Ibek Bell -> Owl Drum -> Salmon Violin -> Salmon Cello -> Quintar Ocarina

    When disabled, different mount types are separated:
       Progressive Quintar Flute (Quintar Pass -> Quintar Flute -> Quintar Ocarina),
       Progressive Salmon Violin (Salmon Violin -> Salmon Cello),
       Ibek Bell,
       and Owl Drum.
    """
    display_name = "Progressive Mount Mode"

class LevelGating(Choice):
    """
    When enabled, the party's level is considered for Archipelago logic, and Progressive Level items are added to the pool. (This won't stop you from beating the game at level 3. ^_^)

    None: Level gating is disabled. No Progressive Levels in the pool.

    Level Passes: Progressive Levels are added to the pool. They do not affect the party's actual level or level cap. Archipelago will expect you to collect them to access level-gated areas,
    and in-game tracking will light up checks that you have access to based on that level.

    Level Capped: The party's maximum level is hard capped. Progressive Levels are added to the pool. Collecting them allows your party to gain more levels, and in-game tracking will light up
    checks that you have access to based on that max level.

    Level Catch-Up: Progressive Levels are added to the pool. Collecting them will help your party catch up in levels (and LP!) based on the number you've collected. For example, if the Progressive Level
    Size Setting is 6 (see below), 1 Progressive Level will bring your party's level up to 6, 2 Progressive Levels will bring your party's level up to 12, etc. If your party
    has already reached that level, no extra levels will be granted. 2 LP are granted per 1 level granted. In-game tracking will light up checks that you have access to based on the number you have collected.

    Level Set: A combination of Level Catch-Up and Capped. The player will always be at the level set by the Progressive Level. There is no escape.
    """
    display_name = "Level Gating"
    option_none = 0
    option_level_passes = 1
    option_level_capped = 2
    option_level_catch_up = 3
    option_level_set = 4
    default = 1

class LevelComparedToEnemies(Range):
    """
    If Level Gating is on, this option changes what level you're expected to fight enemies. Set it higher if you want to be a higher level than enemies when you enter a region, or lower if you want to be lower.

    For example, if this is set to 5, and the enemy level of a region is 12, then the Level Gating options would require you to unlock level 17 (or for Level Capped, max level 17) for that region.
    If it's set to -5, and the enemy level of a region is 12, then the Level Gating options would require you to unlock level 7 (or for Level Capped, max level 7) for that region.

    Default is 0, or on-level for the enemy level of a region.

    Note: Remember to increase your Max Level (see below) if you want regions with high-level enemies to still be lower level than you.
    Note #2: Spark color changes: red at -10 levels, orange at -5, green at +3, and grey +10. (Though enemies can be 3-5 levels above the min enemy level for a region.)
    """
    display_name = "Level compared to enemies"
    range_start = -10
    range_end = 10
    default = 0


class ProgressiveLevelSize(Range):
    """
    If Level Gating is on, Progressive Levels will be added to the item pool. This sets the number of levels that an individual Progressive Level will grant, as well as the starting level expectation.

    For example, if Progressive Level Size is 6, the three Level Gating options would behave like this:
       Level Passes - At the start, areas up to level 6 are considered in logic. The first Progressive Level you collect will signal that areas up to 12 are now logic, the second up to 18, etc.
       Level Capped - Your party's level cap starts at 6. The first Progressive Level you collect will increase your party's level cap to 12, the second to 18, and so on.
       Level Catch-Up - Your party is leveled up to 6 at the start. The first Progressive Level you collect will bring your party's level up to 12 if it isn't already, the second up to 18, and so on.
       Level Set - Your party's level and level cap start at 6. The first Progressive Level you collect will increase your party's level and level cap to 12, the second to 18, and so on.

    This setting will only increase your party's starting level (3 by default) if you pick Level Catch-Up.
    """
    display_name = "Progressive Level Size"
    range_start = 3
    range_end = 10
    default = 6

class MaxLevel(Range):
    """
    This allows your party to level past the default maximum level of 60. If Level Gating is on, increasing this number will also put more Progressive Levels in your pool.

    Set it below 60 at your own risk <3
    """
    display_name = "Max Level"
    range_start = 3
    range_end = 99
    default = 60

class KeyMode(Choice):
    """
    Skeleton Key: Only the Skeleton Key, which can open any locked door, will be in your item pool.

    Key Ring: Keys for individual dungeons will be grouped into Key Rings. Each Key Ring will give all keys needed to complete one dungeon. The Skeleton Key will still be in the pool.

    Vanilla: All vanilla keys will be in the item pool.

    Skelefree: Same as the named mode, but removes the Skeleton Key.
    """
    display_name = "Key Mode"
    option_skeleton = 0
    option_key_ring = 1
    option_vanilla = 2
    option_key_ring_skelefree = 3
    option_vanilla_skelefree = 4
    default = 2

class ObscureRoutes(Toggle):
    """
    When enabled, connections between regions that are difficult to find will be expected in logic.
    """
    display_name = "Obscure Routes"

class AutoSpendLP(Toggle):
    """
    When enabled, every time a character earn LP it will automatically spend LP on abilities or passives.
    """
    display_name = "Automatically Spend LP"

class AutoEquipPassives(Toggle):
    """
    When enabled, every time a character unlocks a new passive, it will equip it immediately if enough passive points are available.
    Passives with drawbacks, that enable equipping more gear types, or that modify threat are not automatically equipped.
    If mods are enabled all passives are auto-equipped with no exclusions.
    """
    display_name = "Automatically Equip Passives"

class EasyLeveling(Toggle):
    """
    When enabled, characters will not receive reduced experience for being dead or for being a higher level than the fought enemy.
    """
    display_name = "Easy Leveling"

#"""Item Pool Options"""
class ProgressiveEquipmentMode(DefaultOnToggle):
    """
    When enabled, each category of weapon and armor will be sent to the player in progressive order from weakest to strongest.

    When disabled, weapons and armor are fully randomized.
    """
    display_name = "Progressive Equipment"

class StartWithTreasureFinder(DefaultOnToggle):
    """
    When enabled, the player will start with the Treasure Finder in their inventory. When disabled, it will be in the item pool.

    NOTE: Having the Treasure Finder is required for the in-game minimap to display nearby checks.
    """
    display_name = "Begin with Treasure Finder"

class StartWithMaps(DefaultOnToggle):
    """
    When enabled, the player will start with all maps in their inventory.

    Note: The in-game minimap hides when in an area without its map. The world map will display check location icons but will not draw an area without its map.
    """
    display_name = "Begin with Area Maps"

class IncludeSummonAbilities(DefaultOnToggle):
    """
    When enabled, Summons are added to the item pool.

    Note: It is not recommended to turn this off with Job Rando: Full and a low number of starting Jobs. You don't want to get stuck with just a Summoner who can only summon Pinga! (I'm sorry, Pinga.)
    """
    display_name = "Include Summons in the item pool"
    
class IncludeScholarAbilities(DefaultOnToggle):
    """
    When enabled, Scholar abilities are added to the item pool. They can still be learned as normal from enemies.
    """
    display_name = "Include Scholar Abilities in the item pool"

#"""Bonus Fun"""
class TrapLikelihood(Range):
    """
    This is the likelihood that a trap will replace a filler check, a value of 0 means no traps
    """
    display_name = "Trap Likelihood"
    range_start = 0
    range_end = 100
    default = 0

class ItemInfoMode(Choice):
    """
    For Full, all treasure and store icons on the map will display if they are progression, useful, or filler items.

    For Earned, all treasure and store icons on the map will display as mimics until you obtain the map-revealing item that is not yet implemented idk come back v0.9.

    For Obscured, all treasure and store icons on the map will display as mimics permanently.
    If you find skipping treasures is distasteful but part of your brain always wants to be efficient, this option is for you!
    It's also good for a race environment.
    """
    display_name = "Item Info Mode"
    option_full = 0
    option_earned = 1
    option_obscured = 2
    default = 0

class RandomizeMusic(Toggle):
    """
    When enabled, music will be randomized upon connecting to the AP World. (This toggles the base game's Randomize Music function.)
    """
    display_name = "Randomize Music"

class UseMods(Toggle):
    """
    WARNING: This setting is very in beta right now! Enabling it is not recommended for: multiworlds that do not allow releasing items or with Regionsanity enabled (some mods add items to regions but don't place them anywhere near that region).

    When enabled, items and locations added by other Crystal Project mods will be added to the item and location pools at generation. Mods newer than Editor version 30 are incompatible.

    Multiworld host instructions:
    1. In order to select the mods you'd like to include in randomization, make a folder named "crystal_project_mods" inside your root Archipelago directory.
    2. Go to your Steam installation folder for Crystal Project (<YourSteamInstallFolder>/steamapps/workshop/content/1637730) and find the individual folders for the mods you'd like to include.
    3. Inside each mod's folder is a mod json. Copy that json to the crystal_project_mods folder you made inside the Archipelago directory.
    4. If you have a specific order you want to apply the mods, rename the jsons such that they are in alphabetical order in the order you want them to be applied. E.g. name the first mod a_modname, the second b_modname, etc.

    NOTE: When this setting is on, all Crystal Project players in the multiworld with this setting enabled MUST use the same mods.

    The in-game tracking will use special icons for modded locations that will not display their accessibility (as we can only guess at how accessible they are based on coordinates, and would prefer the tracking to be as accurate as possible).

    When disabled, only base game locations and items will be randomized. You can still use other mods - at your own risk, adventurer - they just won't add checks.

    The game will warn you if you open a game with mods that don't match the mods used to generate the multiworld. It will warn you even if this setting is disabled for you, if you start playing with mods.
    """
    display_name = "Use Mods"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    newWorldStoneJobQuantity: NewWorldStoneJobQuantity
    clamshellGoalQuantity: ClamshellGoalQuantity
    extraClamshellsInPool: ExtraClamshellsInPool
    jobRando: JobRando
    startingJobQuantity: StartingJobQuantity
    killBossesMode: KillBossesMode
    shopsanity: Shopsanity
    regionsanity: Regionsanity
    includedRegions: IncludedRegions
    progressiveMountMode: ProgressiveMountMode
    levelGating: LevelGating
    levelComparedToEnemies: LevelComparedToEnemies
    progressiveLevelSize: ProgressiveLevelSize
    maxLevel: MaxLevel
    keyMode: KeyMode
    obscureRoutes: ObscureRoutes
    auto_spend_lp: AutoSpendLP
    auto_equip_passives: AutoEquipPassives
    easyLeveling: EasyLeveling
    progressiveEquipmentMode: ProgressiveEquipmentMode
    startWithTreasureFinder: StartWithTreasureFinder
    startWithMaps: StartWithMaps
    includeSummonAbilities: IncludeSummonAbilities
    includeScholarAbilities: IncludeScholarAbilities
    trapLikelihood: TrapLikelihood
    item_info_mode: ItemInfoMode
    randomizeMusic: RandomizeMusic
    useMods: UseMods

crystal_project_option_groups: Dict[str, List[Any]] = {
    "Goal Options": [Goal, ClamshellGoalQuantity, ExtraClamshellsInPool, NewWorldStoneJobQuantity],
    "Location Options": [IncludedRegions, JobRando, StartingJobQuantity, KillBossesMode, Shopsanity, Regionsanity],
    "Progression Options": [ProgressiveMountMode, LevelGating, LevelComparedToEnemies, ProgressiveLevelSize, MaxLevel, KeyMode, ObscureRoutes, AutoSpendLP, AutoEquipPassives, EasyLeveling],
    "Item Pool Options": [ProgressiveEquipmentMode, StartWithTreasureFinder, StartWithMaps, IncludeSummonAbilities, IncludeScholarAbilities],
    "Bonus Fun": [ItemInfoMode, RandomizeMusic, UseMods]
}