from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle

class LogicMode(Choice):
    """
    Logic mode; in other words, how is the player allowed to access items.
    [Linear] Progression follows the game's linear path, though sequence breaks are allowed and inevitably will still occur. Makes for a longer, more BK-heavy playthrough with fewer options at each point.
    [Open] (Default) Progression is based only on whether it is possible to reach area given the current list of received items.
    """
    display_name = "Logic Mode"
    option_linear = 0
    option_open = 1
    
    default = 1

class VTShadeLock(Choice):
    """
    If set to a non-None value, creates an in-game barrier at the entrance of Vermillion Tower to prevent extremely quick playthroughs.
    [Bosses] Vermillion Tower only opens when the bosses at the end of the first four dungeons have been beaten.
    [Shades] Vermillion Tower only opens when the four shades acquired at the end of the first four dungeons have been acquired.
    [Bosses and Shades] Vermillion Tower opens when both of the other conditions have been satisfied.
    """
    display_name = "Vermillion Tower Shade Lock"

    option_none = 0
    option_bosses_and_shades = 1
    option_shades = 2
    option_bosses = 3
    default = 1

class VWMeteorPassage(DefaultOnToggle):
    """
    If enabled, places a gate between Sapphire Ridge and Vermillion Wasteland unlockable with the meteor shade
    """
    display_name = "Vermillion Wasteland Meteor Passage"

class VTSkip(DefaultOnToggle):
    """
    If enabled, Vermillion Tower will not need to be completed; instead, the player will skip through it to the final boss.
    """
    display_name = "Skip Vermillion Tower"

class QuestRando(Toggle):
    """
    If enabled, all quests will be randomized along with chests and cutscene locations.
    """
    display_name = "Quest Randomization"

class HiddenQuestRewardMode(Choice):
    """
    Some quests hide their rewards until they are completed.
    [Vanilla] Behavior is unchanged from the base game.
    [Show All] Show all rewards regardless of whether they're hidden in the base game.
    [Hide All] Hide all rewards regardless of whether they're hidden in the base game.
    """
    display_name = "Show Hidden Quest Rewards"

    option_vanilla = 0
    option_show_all = 1
    option_hide_all = 2

    default = 0

class HiddenQuestObfuscationLevel(Choice):
    """
    For quests with hidden rewards, this option controls the level to which rewards are obscured.
    [Hide Item] Only hides the item name. The icon and receiving player are still accurate.
    [Hide Text] Obscures item name and receiving player. The icon will still be accurate.
    [Hide All] The item name and receiving player will all be hidden and the icon will be replaced with a generic archipelago logo.
    """
    display_name = "Hidden Quest Obfuscation Level"

    option_hide_item = 0
    option_hide_text = 1
    option_hide_all = 2

    default = 0

class QuestDialogHints(DefaultOnToggle):
    """
    If enabled, upon viewing the quest dialog for a quest with rewards that are not hidden, corresponding hints are sent to the archipelago server.
    """
    display_name = "Quest Dialog Hints"

class StartWithGreenLeafShade(DefaultOnToggle):
    """
    If enabled, the player will start with the green leaf shade, unlocking Autumn's Fall. This makes the early game far more open.
    """
    display_name = "Start with Green Leaf Shade"

class StartWithChestDetector(DefaultOnToggle):
    """
    If enabled, the player will start with the chest detector item, which will notify them of the chests in the room.
    """
    display_name = "Start with Chest Detector"

class Keyrings(Toggle):
    """
    If enabled, all keys for each dungeon will be replaced with a singular item that unlocks every door in that dungeon.
    """
    display_name = "Keyrings"

class Reachability(Choice):
    option_own_world = 0
    option_different_world = 1
    option_any_world = 2

    default = 2

    items: dict[str, set[str]]

    def register_locality(self, local_items: set[str], non_local_items: set[str]):
        if self.value == Reachability.option_own_world:
            for _, lst in self.items.items():
                local_items |= lst
        elif self.value == Reachability.option_different_world:
            for _, lst in self.items.items():
                non_local_items |= lst

class DungeonReachability(Reachability):
    option_own_dungeons = 10
    option_original_dungeons = 11

    def register_pre_fill_lists(
        self,
        specific_dungeons: dict[str, set[str]],
        all_dungeons: set[str]
    ):
        if self.value == DungeonReachability.option_own_dungeons:
            for _, lst in self.items.items():
                all_dungeons |= lst
        if self.value == DungeonReachability.option_original_dungeons:
            for key, lst in self.items.items():
                specific_dungeons[key] |= lst

class ShadeShuffle(Reachability):
    """
    Where shades will appear.
    """
    display_name = "Shade Shuffle"

    items = {
        "any": {
            "Green Leaf Shade", "Yellow Sand Shade", "Blue Ice Shade",
            "Red Flame Shade", "Purple Bolt Shade", "Azure Drop Shade",
            "Green Seed Shade", "Star Shade", "Meteor Shade",
        }
    }

class ElementShuffle(DungeonReachability):
    """
    Where elements will appear.
    """
    display_name = "Element Shuffle"

    items = {
        "cold-dng": { "Heat" },
        "heat-dng": { "Cold" },
        "wave-dng": { "Shock" },
        "shock-dng": { "Wave" },
    }

class SmallKeyShuffle(DungeonReachability):
    """
    Where small keys will appear.
    """
    display_name = "Small Key Shuffle"

    items = {
        "cold-dng": { "Mine Key" },
        "heat-dng": { "Faj'ro Key" },
        "wave-dng": { "So'najiz Key" },
        "shock-dng": { "Zir'vitar Key" },
        "tree-dng": { "Krys'kajo Key" },
    }

class MasterKeyShuffle(DungeonReachability):
    """
    Where master keys will appear.
    """
    display_name = "Master Key Shuffle"

    items = {
        "cold-dng": { "Mine Master Key" },
        "heat-dng": { "Faj'ro Master Key" },
        "tree-dng": { "Kajo Master Key" },
    }

class ChestKeyShuffle(DungeonReachability):
    """
    Where the Thief's Key, White Key, and Radiant Key (the keys that open bronze, silver, and gold chests, respectively) may appear.
    """

    display_name = "Chest Key Shuffle"

    items = {
        "cold-dng": { "Thief's Key" },
        "heat-dng": { "White Key" },
        "wave-dng": { "Radiant Key" },
    }

@dataclass
class CrossCodeOptions(PerGameCommonOptions):
    logic_mode: LogicMode
    vt_shade_lock: VTShadeLock
    vw_meteor_passage: VWMeteorPassage
    vt_skip: VTSkip
    quest_rando: QuestRando
    hidden_quest_reward_mode: HiddenQuestRewardMode
    hidden_quest_obfuscation_level: HiddenQuestObfuscationLevel
    quest_dialog_hints: QuestDialogHints
    start_with_green_leaf_shade: StartWithGreenLeafShade
    start_with_chest_detector: StartWithChestDetector
    keyrings: Keyrings
    shade_shuffle: ShadeShuffle
    element_shuffle: ElementShuffle
    small_key_shuffle: SmallKeyShuffle
    master_key_shuffle: MasterKeyShuffle
    chest_key_shuffle: ChestKeyShuffle

addon_options = ["quest_rando"]
