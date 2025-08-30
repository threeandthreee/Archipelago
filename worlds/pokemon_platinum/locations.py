# locations.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from BaseClasses import Location, Region
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

from .data import items as itemdata, locations as locationdata, regions as regiondata
from .options import PokemonPlatinumOptions, RandomizeKeyItems

if TYPE_CHECKING:
    from . import PokemonPlatinumWorld

raw_id_to_const_name = { loc.get_raw_id():name for name, loc in locationdata.locations.items() }

@dataclass(frozen=True)
class LocationType:
    is_enabled: Callable[[PokemonPlatinumOptions], bool]

location_types: Mapping[str, LocationType] = {
    "overworld": LocationType(is_enabled = lambda opts : opts.overworlds.value == 1),
    "hidden": LocationType(is_enabled = lambda opts : opts.hiddens.value == 1),
    "hm": LocationType(is_enabled = lambda opts : opts.hms.value == 1),
    "badge": LocationType(is_enabled = lambda opts : opts.badges.value == 1),
    "key_item": LocationType(is_enabled = lambda opts : opts.key_items.are_most_randomized()),
    "all_key_item": LocationType(is_enabled = lambda opts : opts.key_items.value == RandomizeKeyItems.option_all),
    "npc_gift": LocationType(is_enabled = lambda opts : opts.npc_gifts.value == 1),
    "rod": LocationType(is_enabled = lambda opts : opts.rods.value == 1),
    "poketchapp": LocationType(is_enabled = lambda opts : opts.poketch_apps.value == 1),
    "running_shoes": LocationType(is_enabled = lambda opts : opts.running_shoes.value == 1),
    "bicycle": LocationType(is_enabled = lambda opts : opts.bicycle.value == 1),
    "pokedex": LocationType(is_enabled = lambda opts : opts.pokedex.value == 1),
}

def get_parent_region(label: str, world: "PokemonPlatinumWorld") -> str | None:
    const_name = raw_id_to_const_name[world.location_name_to_id[label]]
    return locationdata.locations[const_name].parent_region

def is_location_enabled(label: str, world: "PokemonPlatinumWorld"):
    const_name = raw_id_to_const_name[world.location_name_to_id[label]]
    return location_types[locationdata.locations[const_name].type].is_enabled(world.options) or const_name in locationdata.required_locations

def create_location_label_to_code_map() -> Dict[str, int]:
    return {v.label:v.get_raw_id() for v in locationdata.locations.values()}

class PokemonPlatinumLocation(Location):
    game: str = "Pokemon Platinum"
    default_item_id: int | None
    is_enabled: bool

    def __init__(
        self,
        player: int,
        name: str,
        address: int | None = None,
        parent: Region | None = None,
        default_item_id: int | None = None,
        is_enabled: bool = True,
    ) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_id = default_item_id
        self.is_enabled = is_enabled

def create_locations(world: "PokemonPlatinumWorld", regions: Mapping[str, Region]) -> None:
    for region_name, region_data in regiondata.regions.items():
        if region_name not in regions:
            continue
        region = regions[region_name]
        for name in region_data.locs:
            loc = locationdata.locations[name]
            is_enabled = location_types[loc.type].is_enabled(world.options)
            if not (is_enabled or name in locationdata.required_locations):
                continue
            item = itemdata.items[loc.original_item]
            plat_loc = PokemonPlatinumLocation(
                world.player,
                loc.label,
                address=loc.get_raw_id(),
                parent=region,
                default_item_id=item.get_raw_id(),
                is_enabled=is_enabled)
            if not is_enabled:
                plat_loc.place_locked_item(world.create_item(item.label))
                plat_loc.show_in_spoiler = False
            region.locations.append(plat_loc)
