from dataclasses import dataclass
from Options import OptionList, OptionSet, PerGameCommonOptions, Toggle, Range


class Victims(OptionList):
    """List of players to be locked out of the game."""


class AutoHintGameStart(Toggle):
    """If the Game Start items should be prehinted."""


class RandomStartStart(Range):
    """adds that many random start games to start inventory, for randomizing everything"""
    range_start = 0
    range_end = 4
    default = 0


@dataclass
class ShahrazadOptions(PerGameCommonOptions):
    victims: Victims
    hint_game_start: AutoHintGameStart
    random_start: RandomStartStart
