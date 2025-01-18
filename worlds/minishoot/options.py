from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, Choice, PerGameCommonOptions

class NpcSanity(Toggle):
    """
    Randomizes the freeable NPCs in the world, making them obtainable from any source.
    """
    internal_name = "npc_sanity"
    display_name = "NPC Sanity"

class ScarabSanity(Toggle):
    """
    Randomizes the scarabs in the world.
    """
    internal_name = "scarab_sanity"
    display_name = "Scarab Sanity"

class ShardSanity(Toggle):
    """
    Randomizes the XP shards "groups" (not individual crystals) in the world.
    """
    internal_name = "shard_sanity"
    display_name = "Shard Sanity"

class KeySanity(Toggle):
    """
    Randomizes the small keys of dungeons in the world.
    """
    internal_name = "key_sanity"
    display_name = "Key Sanity"

class BossKeySanity(Toggle):
    """
    Randomizes the boss keys of dungeons in the world.
    """
    internal_name = "boss_key_sanity"
    display_name = "Boss Key Sanity"

class SimpleTempleExit(DefaultOnToggle):
    """
    Change the exits of the 3 temples, so that they don't require the vanilla power to leave without requiring a save and quit.
    """
    internal_name = "simple_temple_exit"
    display_name = "Simple Temple Exit"

class BlockedForest(DefaultOnToggle):
    """
    Replace the bushes of the secret pond in the forest with rocks. This make the south forest area blocked until you have the supershot.
    With this option enabled, the forest area no longer contains sphere 0 locations locked behind a particular difficult fight without any additional offensive capabilities.
    """
    internal_name = "blocked_forest"
    display_name = "Blocked Forest"

class CannonLevelLogicalRequirements(DefaultOnToggle):
    """
    Ensure that progressive cannon levels are accessible before fights in late game areas.
    So for example, you will be able to enter Dungeon 3 in logic, but you will need the cannon level 4 to beat the boss, or items behind fights in the dungeon.
    """
    internal_name = "cannon_level_logical_requirements"
    display_name = "Cannon Level Logical Requirements"

class CompletionGoals(Choice):
    """
    Set the goals required to finish the game.
    * Dungeon 5 : Beat the boss of Dungeon 5 and get to the normal ending.
    * Snow : Beat the Unchosen inside the tree and get to the true ending.
    * Both : Beat both the normal and true ending.
    """
    internal_name = "completion_goals"
    display_name = "Completion Goals"
    option_dungeon_5 = 0
    option_snow = 1
    option_both = 2

@dataclass
class MinishootOptions(PerGameCommonOptions):
    npc_sanity: NpcSanity
    scarab_sanity: ScarabSanity
    shard_sanity: ShardSanity
    key_sanity: KeySanity
    boss_key_sanity: BossKeySanity
    simple_temple_exit: SimpleTempleExit
    blocked_forest: BlockedForest
    cannon_level_logical_requirements: CannonLevelLogicalRequirements
    completion_goals: CompletionGoals
