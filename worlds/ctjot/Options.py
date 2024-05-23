from Options import FreeText, OptionDict, OptionList, Range, Toggle


class Locations(OptionList):
    """List of locations chosen by the randomizer to hold key items"""
    display_name = "locations"


class Items(OptionList):
    """List of key items to be randomized"""
    display_name = "items"


class Rules(OptionDict):
    """Access rules for the chosen locations"""
    display_name = "rules"


class Victory(OptionList):
    """Victory conditions for the chosen game mode"""
    display_name = "victory"


class GameMode(FreeText):
    """Game mode chosen by the user."""
    display_name = "Game Mode"


class ItemDifficulty(FreeText):
    """Game mode chosen by the user."""
    display_name = "Item Difficulty"


class TabTreasures(Toggle):
    """Don't place dungeon-native items on the dungeon's boss."""
    display_name = "All treasures are tabs"


class BucketFragments(Toggle):
    """Don't place dungeon-native items on the dungeon's boss."""
    display_name = "Enable Bucket Fragments"


class FragmentCount(Range):
    """Total number of bucket fragments to place"""
    range_start = 0
    range_end = 100
    default = 15
    display_name = "Fragment Count"
