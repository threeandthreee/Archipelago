import abc
from dataclasses import dataclass

from BaseClasses import CollectionState

class Condition(abc.ABC):
    @abc.abstractmethod
    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        pass

@dataclass
class ItemCondition(Condition):
    item_name: str
    amount: int = 1

    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        target = self.amount
        if self.item_name in kwargs["keyrings"]:
            target = 1

        replacements = kwargs["item_progressive_replacements"]

        if self.item_name in replacements:
            for prog_item_name, quantity in replacements[self.item_name]:
                if state.has(prog_item_name, player, quantity):
                    return True

        return state.has(self.item_name, player, target)

@dataclass
class QuestCondition(Condition):
    quest_name: str

    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        return state.has(f"{self.quest_name} (Event)", player)

@dataclass
class LocationCondition(Condition):
    location_name: str

    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        return state.has(f"{self.location_name} (Event)", player)

@dataclass
class RegionCondition(Condition):
    target_mode: str
    region_name: str

    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        mode: str = kwargs["mode"]

        return mode != self.target_mode or state.has(f"{self.region_name} (Event)", player)

@dataclass
class AnyElementCondition(Condition):
    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        return any([
            state.has("Heat", player),
            state.has("Cold", player),
            state.has("Shock", player),
            state.has("Wave", player),
        ])

@dataclass
class OrCondition(Condition):
    subconditions: list[Condition]

    def satisfied(self, state: CollectionState, player: int, **kwargs) -> bool:
        return any(map(lambda x: x.satisfied(state, player, **kwargs), self.subconditions))

@dataclass
class VariableCondition(Condition):
    name: str

    def satisfied(self, state: CollectionState, player: int,  **kwargs) -> bool:
        variables: dict[str, list[str]] = kwargs["variables"]
        variable_definitions: dict[str, dict[str, list[Condition]]] = kwargs["variable_definitions"]

        if self.name not in variables:
            return True

        for value in variables[self.name]:
            if not all(map(lambda c: c.satisfied(state, player, **kwargs), variable_definitions[self.name][value])):
                return False

        return True
