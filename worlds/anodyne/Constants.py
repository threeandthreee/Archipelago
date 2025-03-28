import logging
from typing import TYPE_CHECKING, List

from BaseClasses import CollectionState

from .Data import Items, Locations, Events
from .Options import SmallKeyShuffle, BigKeyShuffle

if TYPE_CHECKING:
    from . import AnodyneWorld

id_offset: int = 20130204  # nice

debug_mode: bool = False

item_name_to_id = {name: id for id, name in enumerate(Items.all_items, id_offset)}
location_name_to_id = {location.name: id for id, location in enumerate(Locations.all_locations, id_offset)}


def count_cards(state: CollectionState, world: "AnodyneWorld") -> int:
    card_count = 0
    for card in Items.cards:
        if state.has(card, world.player):
            card_count += 1

    return card_count


def count_keys(state: CollectionState, world: "AnodyneWorld", map_name: str) -> int:
    key_name: str = f"Small Key ({map_name})"

    if key_name not in Items.all_items:
        logging.warning(f"Item {key_name} does not exist")
        return 0
    else:
        return state.count(key_name, world.player)


def check_access(state: CollectionState, world: "AnodyneWorld", rule: str, map_name: str) -> bool:
    if rule in world.proxy_rules:
        return all(check_access(state, world, subrule, map_name) for subrule in world.proxy_rules[rule])
    elif rule == "Combat":
        return state.has_any(["Broom", "Widen", "Extend"], world.player)
    elif rule.startswith("Cards:"):
        count = int(rule[6:])
        logging.debug(f"Card {count} check in {map_name} ({world.player})")
        return count_cards(state, world) >= count
    elif rule.startswith("Keys:"):
        if world.options.small_key_shuffle == SmallKeyShuffle.option_unlocked:
            logging.debug(f"Gates are unlocked ({world.player})")
            return True

        values = rule.split(":")

        count = int(values[2])
        dungeon_name = values[1]

        if world.options.small_key_shuffle == SmallKeyShuffle.option_vanilla and dungeon_name == "Hotel":
            # The vanilla key placements in Hotel are not quite strict enough for our key logic, but they do work as
            # long as you assume the player already has Combat and Jump Shoes, which must be true anyway.
            return True

        obtained_count = count_keys(state, world, dungeon_name)

        logging.debug(f"Key {count} check in {map_name} having {obtained_count} ({world.player})")
        return obtained_count >= count
    elif world.options.big_key_shuffle == BigKeyShuffle.option_unlocked and rule in Items.big_keys:
        return True
    elif rule.startswith("RedCave:"):
        side = rule[8:]

        needed_caves = 1
        if side == "Right":
            needed_caves = 2
        elif side == "Top":
            needed_caves = 3

        return state.has("Progressive Red Cave", world.player, needed_caves)
    elif rule.startswith("Swap:"):
        count = int(rule[5:])
        return state.has("Progressive Swap", world.player, count)
    else:
        logging.debug(f"Item {rule} check in {map_name} ({world.player})")
        if rule not in Items.all_items and rule not in Events.all_events:
            logging.warning(f"Rule {rule} does not exist")
        return state.has(item=rule, player=world.player)


def get_access_rule(reqs: List[str], region_name: str, world: "AnodyneWorld"):
    return lambda state: all(check_access(state, world, item, region_name) for item in reqs)
