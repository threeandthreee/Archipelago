import logging
from typing import TYPE_CHECKING, List

from BaseClasses import CollectionState

from .Data import Items, Locations, Events

if TYPE_CHECKING:
    from . import AnodyneWorld

id_offset: int = 20130204  # nice

debug_mode: bool = False

item_name_to_id = {name: n for n, name in enumerate(Items.all_items, id_offset)}
location_name_to_id = {location.name: n for n, location in enumerate(Locations.all_locations, id_offset)}

groups = {
    **Items.item_groups,
    "Bosses": [f"Defeat {c}" for c in ["Seer","The Wall","Rogue","Watcher","Servants","Manager","Sage","Briar"]],
    "Combat": ["Broom","Widen","Extend"]
}

def check_access(state: CollectionState, world: "AnodyneWorld", rule: str, map_name: str) -> bool:
    if rule in world.proxy_rules:
        return all(check_access(state, world, subrule, map_name) for subrule in world.proxy_rules[rule])
    elif rule in groups:
        return state.has_any(groups[rule],world.player)
    elif ':' in rule:
        item,count = rule.split(':')
        count = int(count)
        if item in groups:
            return state.has_from_list(groups[item],world.player,count)

        if item not in Items.all_items and item not in Events.all_events:
            logging.warning(f"Rule {rule} does not exist")
        return state.has(item,world.player,count)
    else:
        logging.debug(f"Item {rule} check in {map_name} ({world.player})")
        if rule not in Items.all_items and rule not in Events.all_events:
            logging.warning(f"Rule {rule} does not exist")
        return state.has(item=rule, player=world.player)


class AccessRule:
    def __init__(self,reqs:List[str], region_name: str, world: "AnodyneWorld"):
        self.reqs = reqs
        self.region_name = region_name
        self.world = world

    def __call__(self, state:CollectionState):
        return all(check_access(state,self.world,item,self.region_name) for item in self.reqs)

def get_access_rule(reqs: List[str], region_name: str, world: "AnodyneWorld"):
    return AccessRule(reqs,region_name,world)
