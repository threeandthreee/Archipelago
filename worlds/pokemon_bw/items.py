from random import Random
from typing import TYPE_CHECKING, Any
from collections import ChainMap

from BaseClasses import Item

if TYPE_CHECKING:
    from . import PokemonBWWorld
    from .data import AnyItemData

all_items_view: ChainMap[str, "AnyItemData"] | None = None


class PokemonBWItem(Item):
    game = 'Pokemon Black and White'


def generate_item(name: str, world: "PokemonBWWorld") -> PokemonBWItem:
    global all_items_view

    if all_items_view is None:
        from .data.items import all_items_dict_view
        all_items_view = all_items_dict_view

    data = all_items_view[name]
    # Item id from lookup table is used instead of id from data for safety purposes
    return PokemonBWItem(name, data.classification(world), world.item_name_to_id[name], world.player)


def get_item_lookup_table() -> dict[str, int]:
    from .data.items import all_items_dict_view

    return {name: data.item_id for name, data in all_items_dict_view.items()}


def get_main_item_pool(world: "PokemonBWWorld") -> list[PokemonBWItem]:
    from .generate.items import badges, key_items, main_items, seasons, tm_hm

    return (badges.generate_default(world) +
            key_items.generate_default(world) +
            main_items.generate_default(world) +
            seasons.generate_default(world) +
            tm_hm.generate_default(world))


def generate_filler(world: "PokemonBWWorld") -> str:
    from .data.items import berries, main_items, medicine

    main_nested = [
        main_items.filler,
        main_items.filler,
        main_items.filler if "Useful filler" not in world.options.modify_item_pool else [
            main_items.filler,
            main_items.min_once,
            main_items.min_once,
        ],
        main_items.filler if "Ban bad filler" in world.options.modify_item_pool else [
            main_items.filler,
            main_items.filler,
            main_items.filler,
            main_items.mail,
        ],
    ]
    berries_nested = [
        berries.standard,
        berries.standard,
        berries.standard,
        berries.niche,
    ]

    return random_choice_nested(
        world.random, [
            main_nested,
            main_nested,
            berries_nested,
            medicine.table,
            medicine.table,
        ]
    )


def random_choice_nested(random: Random, nested: list[str | list | dict]) -> Any:
    """Helper function for getting a random element from a nested list."""
    current: str | list | dict = nested
    while isinstance(current, list | dict):
        if isinstance(current, list):
            current = random.choice(current)
        else:
            current = random.choice(tuple(current.keys()))
    return current


def populate_starting_inventory(world: "PokemonBWWorld", items: list[PokemonBWItem]) -> None:
    from .data.items import seasons

    if world.options.season_control == "randomized":
        seasons_list: list["PokemonBWItem"] = [
            item for item in items if item.name in seasons.table
        ]
        start = world.random.choice(seasons_list)
        world.push_precollected(start)
        items.remove(start)


def reserve_locked_items(world: "PokemonBWWorld", items: list[PokemonBWItem]) -> None:
    from .data.items import badges, all_tm_hm, tm_hm
    from .data.locations.ingame_items.special import tm_hm_ncps, gym_tms

    if world.options.shuffle_badges in ("vanilla", "shuffle"):
        badge_items = [item for item in items if item.name in badges.table]
        to_be_locked: dict[str, PokemonBWItem] = {}
        for item in badge_items:
            to_be_locked[item.name] = item
            items.remove(item)
        world.to_be_locked_items["badges"] = to_be_locked

    if world.options.shuffle_tm_hm == "shuffle":
        tm_hm_items = [item for item in items if item.name in all_tm_hm]
        world.random.shuffle(tm_hm_items)
        to_be_locked: list[PokemonBWItem] = tm_hm_items[:len(tm_hm_ncps)+len(gym_tms)]
        for item in to_be_locked:
            items.remove(item)
        world.to_be_locked_items["tm_hm"] = to_be_locked
    elif world.options.shuffle_tm_hm == "hm_with_badge":
        tm_items = [item for item in items if item.name in tm_hm.tm and "TM70" not in item.name]
        hm_items = [item for item in items if item.name in tm_hm.hm or "TM70" in item.name]
        hm_items.append(tm_items.pop())
        world.random.shuffle(tm_items)  # shuffled here because non-locked tms need to be in item pool
        world.random.shuffle(hm_items)
        to_be_locked_tms: list[PokemonBWItem] = tm_items[:len(tm_hm_ncps)]
        for item in to_be_locked_tms:
            items.remove(item)
        for item in hm_items:
            items.remove(item)
        world.to_be_locked_items["tms"] = to_be_locked_tms
        world.to_be_locked_items["hms"] = hm_items

