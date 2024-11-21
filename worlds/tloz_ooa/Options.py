from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool


class OracleOfAgesGoal(Choice):
    """
    <NOT IMPLEMENTED, ONLY VERAN IS HANDLED RIGHT NOW>
    The goal to accomplish in order to complete the seed.
    - Beat Veran: beat the usual final boss (same as vanilla)
    - Beat Ganon: teleport to the Room of Rites after beating Veran, then beat Ganon (same as linked game)
    """
    display_name = "Goal"

    option_beat_veran = 0
    option_beat_ganon = 1

    default = 0


class OracleOfAgesLogicDifficulty(Choice):
    """
    The difficulty of the logic used to generate the seed.
    - Casual: expects you to know what you would know when playing the game for the first time
    - Medium: expects you to know well the alternatives on how to do basic things, but won't expect any trick
    - Hard: expects you to know difficult tricks such as bomb jumps
    """
    display_name = "Logic Difficulty"

    option_casual = 0
    option_medium = 1
    option_hard = 2

    default = 0


class OracleOfAgesRequiredEssences(Range):
    """
    The amount of essences that need to be obtained in order to get the Maku Seed from the Maku Tree and be able
    to fight Veran in the Black Tower
    """
    display_name = "Required Essences"
    range_start = 0
    range_end = 8
    default = 8

class OracleOfAgesRequiredSlates(Range):
    """
    The amount of slate that need to be obtained in order to get to the boss of the eigth dungeons.
    """
    display_name = "Required Slates"
    range_start = 0
    range_end = 4
    default = 4

class OracleOfAgesAnimalCompanion(Choice):
    """
    Determines which animal companion you can summon using the Flute, as well as the layout of the Nuun region.
    - Ricky: the kangaroo with boxing skills
    - Dimitri: the swimming dinosaur who can eat anything
    - Moosh: the flying blue bear with a passion for Spring Bananas
    """
    display_name = "Animal Companion"

    option_ricky = 0
    option_dimitri = 1
    option_moosh = 2

    default = "random"


class OracleOfAgesDefaultSeedType(Choice):
    """
    Determines which of the 5 seed types will be the "default seed type", which is given:
    - when obtaining Seed Satchel
    - when obtaining Slingshot
    - by Lynna Seed Tree
    """
    display_name = "Default Seed Type"

    option_ember = 0
    option_scent = 1
    option_pegasus = 2
    option_gale = 3
    option_mystery = 4

    default = 0


class OracleOfAgesDungeonShuffle(Choice):
    """
    - Vanilla: each dungeon entrance leads to its intended dungeon
    - Shuffle: each dungeon entrance leads to a random dungeon picked at generation time
    """
    display_name = "Shuffle Dungeons"

    option_vanilla = 0
    option_shuffle = 1

    default = 0


class OracleOfAgesMasterKeys(Choice):
    """
    <NOT IMPLEMENTED RIGHT NOW>
    - Disabled: All dungeon keys must be obtained individually, just like in vanilla
    - All Small Keys: Small Keys are replaced by a single Master Key for each dungeon which is capable of opening
      every small keydoor for that dungeon
    - All Dungeon Keys: the Master Key for each dungeon is also capable of opening the boss keydoor,
      removing Boss Keys from the item pool
    Master Keys placement is determined following the "Keysanity (Small Keys)" option.
    """
    display_name = "Master Keys"

    option_disabled = 0
    option_all_small_keys = 1
    option_all_dungeon_keys = 2

    default = 0

class OracleOfAgesSmallKeyShuffle(Toggle):
    """
    If enabled, dungeon Small Keys can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Keysanity (Small Keys)"


class OracleOfAgesBossKeyShuffle(Toggle):
    """
    If enabled, dungeon Boss Keys can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Keysanity (Boss Keys)"


class OracleOfAgesMapCompassShuffle(Toggle):
    """
    If enabled, Dungeon Maps and Compasses can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Maps & Compasses Outside Dungeon"


class OracleOfAgesSlateShuffle(Toggle):
    """
    If enabled, Slates can be found anywhere instead of being confined in Dungeon 8.
    """
    display_name = "Slates Outside Dungeon 8"


class OracleOfAgesRingQuality(Choice):
    """
    Defines the quality of the rings that will be shuffled in your seed:
    - Any: any ring can potentially be shuffled (including literally useless ones)
    - Only Useful: only useful rings will be shuffled
    """
    display_name = "Rings Quality"

    option_any = 0
    option_only_useful = 1

    default = 1

class OracleOfAgesEnableTokkeyDanceAndKidJoke(Toggle):
    """
    Defines if you don't want to skip the small dance that tokkay does and the joke you tell the kid. (Because some people like it)
    """
    display_name = "Enable Tokkey Dance and Kid Joke"

class OracleOfAgesPricesFactor(Range):
    """
    A factor (expressed as percentage) that will be applied to all prices inside all shops in the game.
    - Setting it at 10% will make all items almost free
    - Setting it at 500% will make all items horrendously expensive, use at your own risk!
    """
    display_name = "Prices Factor (%)"

    range_start = 10
    range_end = 500
    default = 100


class OracleOfAgesAdvanceShop(Toggle):
    """
    In the vanilla game, there is secret "Advance Shop" next to the shooting gallery in past Lynna Village that can only
    be accessed if the game is being played on a Game Boy Advance console.
    If enabled, this option makes this shop always open, adding 3 shop locations to the game (and some rupees to the
    item pool to compensate for the extra purchases that might be required)
    """
    display_name = "Open Advance Shop"



class OracleOfAgesWarpToStart(DefaultOnToggle):
    """
    When enabled, you can warp to start by holding A+B while entering map or inventory screen.
    This can be used to make backtracking a bit more bearable in seeds where Gale Seeds take time to obtain and prevent
    most softlock situations from happening.
    NOTE : You can use can press A + B during the fade to white to avoid using your object.
    """
    display_name = "Warp to Start"


class OracleOfAgesCombatDifficulty(Choice):
    """
    <NOT IMPLEMENTED RIGHT NOW>
    Modifies the damage taken during combat to make this aspect of the game easier or harder depending on the
    type of experience you want to have
    """
    display_name = "Combat Difficulty"

    option_peaceful = 0
    option_easier = 1
    option_vanilla = 2
    option_harder = 3
    option_insane = 4

    default = 2


class OracleOfAgesQuickFlute(DefaultOnToggle):
    """
    When enabled, playing the flute and the harp will immobilize you during a very small amount of time compared to vanilla game.
    """
    display_name = "Quick Flute & Harp"


class OracleOfAgesHeartBeepInterval(Choice):
    """
    <NOT IMPLEMENTED RIGHT NOW>
    - Default: play the beeping sound at the usual frequency when low on health
    - Half: play the beeping sound two times less when low on health
    - Quarter: play the beeping sound four times less when low on health
    - Disabled: never play the beeping sound when low on health
    """
    display_name = "Heart Beep Frequency"

    option_default = 0
    option_half = 1
    option_quarter = 2
    option_disabled = 3

    default = 0


class OracleOfAgesCharacterSprite(Choice):
    """
    <NOT IMPLEMENTED RIGHT NOW>
    The sprite to use as a character during this seed.
    (Sprites extracted from ardnaxelarak's rando)
    """
    display_name = "Character Sprite"

    option_link = 0
    option_subrosian = 1
    option_goron = 2
    option_piratian = 3

    default = 0


class OracleOfAgesCharacterPalette(Choice):
    """
    <NOT IMPLEMENTED RIGHT NOW>
    The color tint to apply to the character sprite during this seed
    """
    display_name = "Character Tint"

    option_green = 0
    option_blue = 1
    option_red = 2
    option_orange = 3

    default = 0


@dataclass
class OracleOfAgesOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: OracleOfAgesGoal
    enable_dance_and_joke: OracleOfAgesEnableTokkeyDanceAndKidJoke
    logic_difficulty: OracleOfAgesLogicDifficulty
    required_essences: OracleOfAgesRequiredEssences
    required_slates: OracleOfAgesRequiredSlates
    animal_companion: OracleOfAgesAnimalCompanion
    default_seed: OracleOfAgesDefaultSeedType
    shuffle_dungeons: OracleOfAgesDungeonShuffle
    master_keys: OracleOfAgesMasterKeys
    keysanity_small_keys: OracleOfAgesSmallKeyShuffle
    keysanity_boss_keys: OracleOfAgesBossKeyShuffle
    keysanity_maps_compasses: OracleOfAgesMapCompassShuffle
    keysanity_slates: OracleOfAgesSlateShuffle
    ring_quality: OracleOfAgesRingQuality
    shop_prices_factor: OracleOfAgesPricesFactor
    advance_shop: OracleOfAgesAdvanceShop
    warp_to_start: OracleOfAgesWarpToStart
    combat_difficulty: OracleOfAgesCombatDifficulty
    quick_flute: OracleOfAgesQuickFlute
    heart_beep_interval: OracleOfAgesHeartBeepInterval
    character_sprite: OracleOfAgesCharacterSprite
    character_palette: OracleOfAgesCharacterPalette
    death_link: DeathLink
