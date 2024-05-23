import typing
from BaseClasses import CollectionState
from .types.locations import Condition, LocationData
from .types.regions import RegionConnection

# this is uncharacteristic of me, but i'm hardcoding something here. weird.
clearance_items = {
    "Bronze": "Thief's Key",
    "Silver": "White Key",
    "Gold": "Radiant Key",
}

def condition_satisfied(player: int, conditions: list[Condition], **kwargs) -> typing.Callable[[CollectionState], bool]:
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        return all([c.satisfied(state, player, **kwargs) for c in conditions])

    return conditions_satisfied_internal

def has_clearance(player: int, clearance: str) -> typing.Callable[[CollectionState], bool]:
    return lambda state: state.has(clearance_items[clearance], player)
