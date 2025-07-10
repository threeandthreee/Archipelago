from copy import copy
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .data.locations import Requirement, Level2KeycardRequirement
from .Items import item_names

if TYPE_CHECKING:
    from worlds.metroidfusion import MetroidFusionOptions

class LogicObject():
    requirements: list[list[str]] = []
    energy_tanks: int = 0
    player: int

    def __init__(self, player: int):
        self.player = player

    def logic_rule(self, state: CollectionState) -> bool:
        if len(self.requirements) == 0:
            return True
        expression = None
        for requirement_list in self.requirements:
            if expression is None:
                expression = state.has_all(requirement_list, self.player)
            else:
                expression = expression or state.has_all(requirement_list, self.player)
        if self.energy_tanks > 0:
            expression = bool(expression) and state.has("Energy Tank", self.player, self.energy_tanks)
        return expression



def create_logic_rule_for_list(requirements: list[Requirement], options: "MetroidFusionOptions", debug: bool = False) -> tuple[list, int]:
    energy_tanks = 0
    requirements_list = []
    for requirement in requirements:
        new_rule = create_logic_rule(requirement, options, debug)
        energy_tanks += new_rule[1]
        for requirement2 in new_rule[0]:
            requirements_list.append(requirement2)
        continue
    return requirements_list, energy_tanks

def create_logic_rule(requirement: Requirement, options: "MetroidFusionOptions", debug: bool = False) -> tuple[list, int]:
    if requirement.check_option_enabled(options):
        requirements_list = []
        energy_tanks_needed = unpack_requirement(requirement, requirements_list, [])
        if debug:
            print(requirement)
            print(requirements_list)
        return requirements_list, energy_tanks_needed
    else:
        if debug:
            print(f"Requirement {requirement} disabled due to options.")
        return [], 0

def unpack_requirement(requirement: Requirement, possibilities: list[list[str]], parent_items: list[str]) -> int:
    energy_tanks = 0
    if len(requirement.other_requirements) > 0:
        for nested_requirement in requirement.other_requirements:
            current_parent_items = copy(parent_items)
            for item_needed in requirement.items_needed:
                assert item_needed in item_names, (item_needed, requirement)
            parent_items.extend(requirement.items_needed)
            energy_tanks += unpack_requirement(nested_requirement, possibilities, parent_items)
            parent_items = copy(current_parent_items)
    elif len(requirement.items_needed) > 0:
        items_needed = copy(requirement.items_needed)
        for item_needed in items_needed:
            assert item_needed in item_names, (item_needed, requirement)
        items_needed.extend(parent_items)
        possibilities.append(items_needed)
    energy_tanks += requirement.energy_tanks_needed
    return energy_tanks