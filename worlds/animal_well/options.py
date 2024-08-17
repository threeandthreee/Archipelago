from dataclasses import dataclass
from typing import Dict, Any
from Options import DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, PerGameCommonOptions, OptionGroup


class Goal(Choice):
    """
    What you need to do to beat the game.
    Fireworks requires you to get the 4 flames and defeat the Manticore. The House Key is placed in its vanilla location.
    Bunny Land requires you to find the 65th Egg, bring it to the incubator, and leave the Well.
    Egg Hunt requires you to collect the amount of eggs you need to open the 4th Egg Door, then open the chest inside.
    """
    internal_name = "goal"
    display_name = "Goal"
    option_fireworks = 1
    # option_bunny_land = 2 TODO(Frank-Pasqualini)
    option_egg_hunt = 3
    default = 1


class FinalEggLocation(Toggle):
    """
    Choose whether the 65th Egg is shuffled into the multiworld item pool or placed in its vanilla location, requiring opening the 4th Egg Door to access it.
    This option is forced on if you have the egg hunt goal selected.
    """
    internal_name = "random_final_egg_location"
    display_name = "Randomize Final Egg"


# todo: client needs work to get this to work with other values - TODO(Frank-Pasqualini)
class EggsNeeded(Range):
    """
    How many Eggs you need to open the 4th Egg Door.
    The amount of Eggs you need for the other 3 doors will scale accordingly.
    """
    internal_name = "eggs_needed"
    display_name = "Eggs Required"
    range_start = 64
    range_end = 64
    default = 64


class BunniesAsChecks(Choice):
    """
    Include the secret bunnies as checks.
    Exclude Tedious removes the Mural, Dream, UV, and Floor is Lava bunnies.
    """
    internal_name = "bunnies_as_checks"
    display_name = "Bunnies as Checks"
    option_off = 0
    option_exclude_tedious = 1
    option_all_bunnies = 2
    default = 0


class BunnyWarpsInLogic(Toggle):
    """
    Include the songs that warp you to Bunny spots in logic.
    If you have Bunnies as Checks enabled, this option is automatically enabled.
    """
    internal_name = "bunny_warps_in_logic"
    display_name = "Bunny Warps in Logic"


class CandleChecks(Choice):  # choice so we can comment out non-working ones then readd them later
    """
    Lighting each of the candles sends a check.
    """
    internal_name = "candle_checks"
    display_name = "Candle Checks"
    option_off = 0
    option_on = 1
    default = 0


class KeyRing(DefaultOnToggle):
    """
    Have one keyring which unlocks all normal key doors instead of individual key items.
    Note: Due to how consumable key logic works, if this option is not enabled, you logically require all 6 keys to open any of the key doors.
    """
    internal_name = "key_ring"
    display_name = "Key Ring"


class Matchbox(DefaultOnToggle):
    """
    Have one matchbox which can light all candles instead of individual match items.
    Note: Due to how consumable item logic works, if this option is not enabled, you logically require all 9 matches to light any of the candles.
    """
    internal_name = "matchbox"
    display_name = "Matchbox"


class BubbleJumping(Choice):
    """
    Include using the standard Bubble Wand and chaining bubble jumps together in logic.
    Exclude Long Chains makes it so you may be required to chain a few bubble jumps before landing.
    """
    internal_name = "bubble_jumping"
    display_name = "Bubble Jumping"
    option_off = 0
    option_exclude_long_chains = 1
    option_on = 2
    default = 1


class DiscHopping(Choice):
    """
    Include jumping onto the disc without letting it bounce off of a wall first in logic.
    Single means doing it once from the ground.
    Multiple means having to chain them in midair.
    Exception: The bunny that requires you to use this tech.
    """
    internal_name = "disc_hopping"
    display_name = "Midair Disc Jumping"
    option_off = 0
    option_single = 1
    option_multiple = 2
    default = 0


class WheelHopping(Choice):
    """
    Include some tricks that involve using the wheel in unconventional ways.
    Simple means toggling wheel midair to "double jump", or mashing against walls to climb them.
    Advanced also adds more complicated tech, such as braking on walls or climbing walls out of jumps.
    Note: Tricks using wheel desyncs or wrong warps are not ever considered logical.
    """
    internal_name = "wheel_tricks"
    display_name = "Wheel Tricks"
    option_off = 0
    option_simple = 1
    option_advanced = 2
    default = 0


class WeirdTricks(Toggle):
    """
    Include performing "weird" tricks in the logic.
    Some of these tricks are difficult, tedious, or inconsistent.
    Use at your own risk.
    """
    internal_name = "weird_tricks"
    display_name = "Weird Tricks"


class ExcludeSongChests(DefaultOnToggle):
    """
    Exclude the Wheel chest and Office Key chests, so that you don't have to play their songs.
    They will contain either filler or traps.
    """
    internal_name = "exclude_song_chests"
    display_name = "Exclude Song Chests"


@dataclass
class AnimalWellOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    eggs_needed: EggsNeeded
    key_ring: KeyRing
    matchbox: Matchbox
    random_final_egg_location: FinalEggLocation
    bunnies_as_checks: BunniesAsChecks
    bunny_warps_in_logic: BunnyWarpsInLogic
    candle_checks: CandleChecks
    bubble_jumping: BubbleJumping
    disc_hopping: DiscHopping
    wheel_hopping: WheelHopping
    weird_tricks: WeirdTricks
    exclude_song_chests: ExcludeSongChests


aw_option_groups = [
    OptionGroup("Logic Options", [
        BubbleJumping,
        DiscHopping,
        WheelHopping,
        WeirdTricks,
    ])
]

aw_option_presets: Dict[str, Dict[str, Any]] = {
    "Animal Hell": {
        "eggs_needed": 64,
        "bubble_jumping": BubbleJumping.option_on,
        "disc_hopping": DiscHopping.option_multiple,
        "wheel_tricks": WheelHopping.option_advanced,
        "weird_tricks": True,
        "bunnies_as_checks": BunniesAsChecks.option_all_bunnies
    },
}
