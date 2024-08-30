from dataclasses import dataclass

from schema import Schema, And

from Options import Choice, DefaultOnToggle, OptionDict, PerGameCommonOptions, Range, StartInventoryPool, Toggle


class Goal(Choice):
    """The victory condition for your Archipelago run.
    Song of Five: Reach the Eye
    Song of Six: Reach the Eye after meeting Solanum"""
    display_name = "Goal"
    option_song_of_five = 0
    option_song_of_six = 1


class RandomizeCoordinates(DefaultOnToggle):
    """Randomize the Eye of the Universe coordinates needed to reach the end of the game."""
    display_name = "Randomize Coordinates"


class TrapChance(Range):
    """The probability for each filler item (including unique filler) to be replaced with a trap item.
    The exact number of trap items will still be somewhat random, so you can't know
    if you've seen the 'last trap' in your world without checking the spoiler log.
    If you don't want any traps, set this to 0."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 15


class TrapTypeWeights(OptionDict):
    """When a filler item is replaced with a trap, these weights determine the
    odds for each trap type to be selected.
    If you don't want a specific trap type, set its weight to 0.
    Setting all weights to 0 is the same as setting trap_chance to 0."""
    schema = Schema({
        "Ship Damage Trap": And(int, lambda n: n >= 0),
        "Nap Trap": And(int, lambda n: n >= 0),
        "Audio Trap": And(int, lambda n: n >= 0),
    })
    display_name = "Trap Type Weights"
    default = {
        "Ship Damage Trap": 2,
        "Nap Trap": 2,
        "Audio Trap": 1,
    }


class DeathLink(Choice):
    """When you die, everyone dies. Of course the reverse is true too.
    The "default" option will not include deaths to meditation, the supernova or the time loop ending.
    Be aware that the game mod provides a 'Death Link Override' setting, in case you change your mind later."""
    display_name = "Death Link"
    option_off = 0
    option_default = 1
    option_all_deaths = 2


# DLC + logsanity is another 71 checks. "rumor sanity" would be another 103 (+22 with DLC).
class Logsanity(Toggle):
    """Adds 176 locations for all the (non-DLC, non-rumor, non-missable) ship log facts in the game."""
    display_name = "Logsanity"


class ShuffleSpacesuit(Toggle):
    """
    Puts the spacesuit into the Archipelago item pool, forcing you to play suitless until it's found.

    This option is incompatible with non-vanilla spawns (i.e. generation will fail), since those imply playing "shipless" at first, and almost nothing can be done both shipless and suitless.
    """
    display_name = "Shuffle Spacesuit"


class RandomizeDarkBrambleLayout(Choice):
    """Randomizes which Dark Bramble 'rooms' link to which other rooms, so you can't rely on your memory of the vanilla layout.
    Be aware that randomized layouts are often significantly harder to navigate than vanilla Dark Bramble, since they allow several paths to the same room and more complex loops / recursion.
    'hub_start' forces the first room to be Hub (same as the vanilla game), which tends to generate shorter and simpler paths than full randomization."""
    display_name = "Randomize Dark Bramble Layout"
    option_false = 0
    option_true = 1
    option_hub_start = 2
    default = 0


class RandomizeOrbits(DefaultOnToggle):
    """Randomizes:
    - The order of the five planets (the Hourglass Twins as a whole, Timber Hearth, Brittle Hollow, Giant's Deep, Dark Bramble), i.e. which ones are closer or farther from the sun
    - The orbit angles of the five planets, as well as four satellites (Sun Station, Attlerock, Hollow's Lantern, and the Orbital Probe Cannon)
    - The axes of rotation for Ember Twin, Ash Twin, Timber Hearth and Brittle Hollow. This often causes the Hourglass Twins' sand pillar to pass through different areas."""
    display_name = "Randomize Orbits"


class Spawn(Choice):
    """
    Where you wake up at the start of each loop.

    'vanilla' is the same as the base game: you wake up in TH Village, talk to Hornfels to get the Launch Codes, then walk by the Nomai statue to start the time loop.
    All other options (including timber_hearth) will spawn you in your spacesuit, with the time loop already started, and the Launch Codes item placed randomly like any other AP item.

    The idea is that non-vanilla spawns will require you to play "shipless" for a while, possibly using Nomai Warp Codes to visit other planets. The ship will still spawn nearby, so you can use the ship log/tracker right away.
    When playing with non-vanilla spawns, we recommend:
    - Consider enabling randomize_warp_platforms for greater variety if you get warp codes early
    - Consider enabling early_key_item in non-solo games, or else your first session may end after only 4-10 checks
    - Install a fast-forward mod such as Alter Time or Cheat And Debug Mod, since you may need to do a lot of waiting for e.g. Ash Twin sand or Giant's Deep islands
    """
    display_name = "Spawn"
    option_vanilla = 0
    option_hourglass_twins = 1
    option_timber_hearth = 2
    option_brittle_hollow = 3
    option_giants_deep = 4
    default = 0


class EarlyKeyItem(Choice):
    """
    Ensure that either Translator, Nomai Warp Codes, or Launch Codes will be somewhere in sphere 1 and
    in your own world, guaranteeing you can find it without waiting on other players.
    `any` randomly selects one of these items to place early.

    Recommended for games with non-vanilla spawns, especially async games.
    In addition, without this AP seems to almost always put Launch Codes in sphere 1, so `any` also helps increase variety.
    """
    display_name = "Early Key Item"
    option_off = 0
    option_any = 1
    option_translator = 2
    option_nomai_warp_codes = 3
    option_launch_codes = 4


class RandomizeWarpPlatforms(Toggle):
    """
    Randomize which Nomai warp platforms are connected to each other.
    Warp connections are still 'coupled', i.e. if platform A warps to platform B, then B will take you back to A.
    Highly recommended when playing with non-vanilla spawns.
    """
    display_name = "Randomize Warp Platforms"


@dataclass
class OuterWildsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    spawn: Spawn
    early_key_item: EarlyKeyItem
    randomize_coordinates: RandomizeCoordinates
    randomize_orbits: RandomizeOrbits
    randomize_warp_platforms: RandomizeWarpPlatforms
    randomize_dark_bramble_layout: RandomizeDarkBrambleLayout
    trap_chance: TrapChance
    trap_type_weights: TrapTypeWeights
    death_link: DeathLink
    logsanity: Logsanity
    shuffle_spacesuit: ShuffleSpacesuit
