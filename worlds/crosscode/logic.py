"""
This module contains various logic functions
"""

import typing
from BaseClasses import CollectionState
from .types.condition import Condition

# this is uncharacteristic of me, but i'm hardcoding something here. weird.
clearance_items = {
    "Bronze": "Thief's Key",
    "Silver": "White Key",
    "Gold": "Radiant Key",
}

def condition_satisfied(
    player: int,
    conditions: list[Condition],
    **kwargs: dict[str, typing.Any]
) -> typing.Callable[[CollectionState], bool]:
    """
    Factory function. Return value is a rule that checks whether all the conditions are satisfied.
    """
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        return all(c.satisfied(state, player, **kwargs) for c in conditions)

    return conditions_satisfied_internal

def has_clearance(player: int, clearance: str) -> typing.Callable[[CollectionState], bool]:
    """
    Function to check whether a player has the correct key (bronze, silver, or gold) to access a location.
    """
    return lambda state: state.has(clearance_items[clearance], player)
