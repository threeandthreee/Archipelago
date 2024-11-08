from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range

class ScoreForLastCheck(Range):
    """
    Score you need to reach to get the final check.
    THIS DETERMINES THE DIFFICULTY! 1000 is probably way to hard, 300 too easy. We will need to figure this out :)
    """

    display_name = "Score for last check"
    range_start = 160
    range_end = 1000
    default = 200


class ScoreForGoal(Range):
    """
    This option determines what score you need to reach to finish the game.
    It cannot be higher than the score for the last check (if it is, this option is changed automatically).
    """

    display_name = "Score for goal"
    range_start = 160
    range_end = 1000
    default = 300
    

@dataclass
class YachtDiceOptions(PerGameCommonOptions):
    score_for_last_check: ScoreForLastCheck
    score_for_goal: ScoreForGoal