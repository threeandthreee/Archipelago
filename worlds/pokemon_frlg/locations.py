import copy
from typing import TYPE_CHECKING, Callable, Dict, FrozenSet, Iterable, List, Optional, Tuple, Union
from BaseClasses import CollectionState, Location, Region, ItemClassification
from .data import data, BASE_OFFSET
from .items import get_random_item, offset_item_value, reverse_offset_item_value, PokemonFRLGItem
from .options import FreeFlyLocation, PewterCityRoadblock, TownMapFlyLocation, ViridianCityRoadblock

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

LOCATION_GROUPS = {
    "Badges": {
        "Pewter Gym - Prize",
        "Cerulean Gym - Prize",
        "Vermilion Gym - Prize",
        "Celadon Gym - Prize",
        "Fuchsia Gym - Prize",
        "Saffron Gym - Prize",
        "Cinnabar Gym - Prize",
        "Viridian Gym - Prize"
    },
    "Gym TMs": {
        "Pewter Gym - Brock TM",
        "Cerulean Gym - Misty TM",
        "Vermilion Gym - Lt. Surge TM",
        "Celadon Gym - Erika TM",
        "Fuchsia Gym - Koga TM",
        "Saffron Gym - Sabrina TM",
        "Cinnabar Gym - Blaine TM",
        "Viridian Gym - Giovanni TM"
    },
    "Oak's Aides": {
        "Route 2 Gate - Oak's Aide",
        "Route 10 Pokemon Center 1F - Oak's Aide",
        "Route 11 Gate 2F - Oak's Aide",
        "Route 16 Gate 2F - Oak's Aide",
        "Route 15 Gate 2F - Oak's Aide"
    }
}

FLY_ITEM_ID_MAP = {
    "ITEM_FLY_NONE": 0,
    "ITEM_FLY_PALLET": 1,
    "ITEM_FLY_VIRIDIAN": 2,
    "ITEM_FLY_PEWTER": 3,
    "ITEM_FLY_CERULEAN": 4,
    "ITEM_FLY_LAVENDER": 5,
    "ITEM_FLY_VERMILION": 6,
    "ITEM_FLY_CELADON": 7,
    "ITEM_FLY_FUCHSIA": 8,
    "ITEM_FLY_CINNABAR": 9,
    "ITEM_FLY_INDIGO": 10,
    "ITEM_FLY_SAFFRON": 11,
    "ITEM_FLY_ONE_ISLAND": 12,
    "ITEM_FLY_TWO_ISLAND": 13,
    "ITEM_FLY_THREE_ISLAND": 14,
    "ITEM_FLY_FOUR_ISLAND": 15,
    "ITEM_FLY_FIVE_ISLAND": 16,
    "ITEM_FLY_SEVEN_ISLAND": 17,
    "ITEM_FLY_SIX_ISLAND": 18,
    "ITEM_FLY_ROUTE4": 19,
    "ITEM_FLY_ROUTE10": 20
}


class PokemonFRLGLocation(Location):
    game: str = "Pokemon FireRed and LeafGreen"
    item_address = Optional[Dict[str, int]]
    default_item_id: Optional[int]
    tags: FrozenSet[str]
    data_ids: Optional[List[str]]

    def __init__(
            self,
            player: int,
            name: str,
            address: Optional[int],
            parent: Optional[Region] = None,
            item_address: Optional[Dict[str, Union[int, List[int]]]] = None,
            default_item_id: Optional[int] = None,
            tags: FrozenSet[str] = frozenset(),
            data_ids: Optional[List[str]] = None) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_id = None if default_item_id is None else offset_item_value(default_item_id)
        self.item_address = item_address
        self.tags = tags
        self.data_ids = data_ids


def offset_flag(flag: int) -> int:
    if flag is None:
        return None
    return flag + BASE_OFFSET


def reverse_offset_flag(location_id: int) -> int:
    if location_id is None:
        return None
    return location_id - BASE_OFFSET


def create_location_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from location names to their AP location ID (address)
    """
    name_to_id_mapping: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_id in region_data.locations:
            location_data = data.locations[location_id]
            name_to_id_mapping[location_data.name] = offset_flag(location_data.flag)

    return name_to_id_mapping


def create_locations_from_tags(world: "PokemonFRLGWorld", regions: Dict[str, Region], tags: Iterable[str]) -> None:
    """
    Iterates through region data and adds locations to the multiworld if
    those locations include any of the provided tags.
    """
    tags = set(tags)

    for region_data in data.regions.values():
        if world.options.kanto_only and not region_data.kanto:
            continue

        region = regions[region_data.name]
        included_locations = [loc for loc in region_data.locations
                              if len(tags & data.locations[loc].tags) >= len(data.locations[loc].tags)]

        for location_flag in included_locations:
            location_data = data.locations[location_flag]

            location_id = offset_flag(location_data.flag)

            if location_data.default_item == data.constants["ITEM_NONE"]:
                default_item = reverse_offset_item_value(
                    world.item_name_to_id[get_random_item(world,ItemClassification.filler)]
                )
            else:
                default_item = location_data.default_item

            location = PokemonFRLGLocation(
                world.player,
                location_data.name,
                location_id,
                region,
                location_data.address,
                default_item,
                location_data.tags
            )
            region.locations.append(location)

    if world.options.level_scaling:
        # Splits encounter categories into "subcategories" and gives them names and rules so the rods can
        # only access their specific slots.
        encounter_categories: Dict[
            str, List[Tuple[Optional[str], range, Optional[Callable[[CollectionState], bool]]]]] = {
            "Land": [(None, range(0, 12), None)],
            "Water": [(None, range(0, 5), None)],
            "Fishing": [
                ("Old Rod", range(0, 2), lambda state: state.has("Old Rod", world.player)),
                ("Good Rod", range(2, 5), lambda state: state.has("Good Rod", world.player)),
                ("Super Rod", range(5, 10), lambda state: state.has("Super Rod", world.player)),
            ],
        }

        trainer_name_level_list: List[Tuple[str, int]] = []
        encounter_name_level_list: List[Tuple[str, int]] = []

        game_version = world.options.game_version.current_key
        region_names = list(regions.keys())
        included_maps = [region.parent_map.name for region in data.regions.values()
                         if region.name in region_names and region.parent_map is not None]

        for scaling_data in world.scaling_data:
            if scaling_data.region not in regions:
                if scaling_data.connections is not None and any(x in region_names for x in scaling_data.connections):
                    region = Region(scaling_data.region, world.player, world.multiworld)
                    regions[scaling_data.region] = region

                    for connection in scaling_data.connections:
                        if connection not in region_names:
                            continue
                        name = f"{regions[connection].name} Scaling Group"
                        regions[connection].connect(region, name)
                else:
                    continue
            else:
                region = regions[scaling_data.region]

            if "Trainer" in scaling_data.tags:
                scaling_event = PokemonFRLGLocation(
                    world.player,
                    scaling_data.name,
                    None,
                    region,
                    None,
                    None,
                    scaling_data.tags,
                    scaling_data.data_ids
                )
                scaling_event.place_locked_item(PokemonFRLGItem("Trainer Party",
                                                                ItemClassification.filler,
                                                                None,
                                                                world.player))
                scaling_event.show_in_spoiler = False

                if scaling_data.rule is not None:
                    scaling_event.access_rule = scaling_data.rule

                region.locations.append(scaling_event)
            elif "Static" in scaling_data.tags:
                scaling_event = PokemonFRLGLocation(
                    world.player,
                    scaling_data.name,
                    None,
                    region,
                    None,
                    None,
                    scaling_data.tags,
                    scaling_data.data_ids
                )
                scaling_event.place_locked_item(PokemonFRLGItem("Static Encounter",
                                                                ItemClassification.filler,
                                                                None,
                                                                world.player))
                scaling_event.show_in_spoiler = False

                if scaling_data.rule is not None:
                    scaling_event.access_rule = scaling_data.rule

                region.locations.append(scaling_event)
            elif "Wild" in scaling_data.tags:
                index = 1
                events: Dict[str, Tuple[str, List[str], Optional[Callable[[CollectionState], bool]]]] = {}
                encounter_category_data = encounter_categories[scaling_data.type]
                for data_id in scaling_data.data_ids:
                    if data_id not in included_maps:
                        continue
                    map_data = data.maps[data_id]
                    encounters = (map_data.land_encounters if scaling_data.type == "Land" else
                                  map_data.water_encounters if scaling_data.type == "Water" else
                                  map_data.fishing_encounters)
                    for subcategory in encounter_category_data:
                        for i in subcategory[1]:
                            subcategory_name = subcategory[0] if subcategory[0] is not None else scaling_data.type
                            species_name = f"{subcategory_name} {encounters.slots[game_version][i].species_id}"
                            if species_name not in events:
                                encounter_data = (f"{scaling_data.name} {index}", [f"{data_id} {i}"], subcategory[2])
                                events[species_name] = encounter_data
                                index = index + 1
                            else:
                                events[species_name][1].append(f"{data_id} {i}")

                for event in events.values():
                    scaling_event = PokemonFRLGLocation(
                        world.player,
                        event[0],
                        None,
                        region,
                        None,
                        None,
                        scaling_data.tags | {scaling_data.type},
                        event[1]
                    )

                    scaling_event.place_locked_item(PokemonFRLGItem("Wild Encounter",
                                                                    ItemClassification.filler,
                                                                    None,
                                                                    world.player))
                    scaling_event.show_in_spoiler = False

                    if event[2] is not None:
                        scaling_event.access_rule = event[2]
                    elif scaling_data.rule is not None:
                        scaling_event.access_rule = scaling_data.rule

                    region.locations.append(scaling_event)

        for region in regions.values():
            for location in region.locations:
                if "Scaling" in location.tags:
                    if "Trainer" in location.tags:
                        min_level = 100

                        for data_id in location.data_ids:
                            trainer_data = data.trainers[data_id]
                            for pokemon in trainer_data.party.pokemon:
                                min_level = min(min_level, pokemon.level)

                        trainer_name_level_list.append((location.name, min_level))
                        world.trainer_name_level_dict[location.name] = min_level
                    elif "Static" in location.tags:
                        for data_id in location.data_ids:
                            pokemon_data = None

                            if data_id in data.misc_pokemon:
                                pokemon_data = data.misc_pokemon[data_id]
                            elif data_id in data.legendary_pokemon:
                                pokemon_data = data.legendary_pokemon[data_id]

                            encounter_name_level_list.append((location.name, pokemon_data.level[game_version]))
                            world.encounter_name_level_dict[location.name] = pokemon_data.level[game_version]
                    elif "Wild" in location.tags:
                        max_level = 1

                        for data_id in location.data_ids:
                            data_ids = data_id.split()
                            map_data = data.maps[data_ids[0]]
                            encounters = (map_data.land_encounters if "Land" in location.tags else
                                          map_data.water_encounters if "Water" in location.tags else
                                          map_data.fishing_encounters)

                            encounter_max_level = encounters.slots[game_version][int(data_ids[1])].max_level
                            max_level = max(max_level, encounter_max_level)

                        encounter_name_level_list.append((location.name, max_level)),
                        world.encounter_name_level_dict[location.name] = max_level

        trainer_name_level_list.sort(key=lambda i: i[1])
        world.trainer_name_list = [i[0] for i in trainer_name_level_list]
        world.trainer_level_list = [i[1] for i in trainer_name_level_list]
        encounter_name_level_list.sort(key=lambda i: i[1])
        world.encounter_name_list = [i[0] for i in encounter_name_level_list]
        world.encounter_level_list = [i[1] for i in encounter_name_level_list]


def set_free_fly(world: "PokemonFRLGWorld") -> None:
    # Set our free fly location
    world.free_fly_location_id = FLY_ITEM_ID_MAP["ITEM_FLY_NONE"]
    world.town_map_fly_location_id = FLY_ITEM_ID_MAP["ITEM_FLY_NONE"]

    if (world.options.free_fly_location == FreeFlyLocation.option_off and
            world.options.town_map_fly_location == TownMapFlyLocation.option_off):
        return

    free_fly_list: List[str] = [
        "ITEM_FLY_LAVENDER",
        "ITEM_FLY_CELADON",
        "ITEM_FLY_FUCHSIA",
        "ITEM_FLY_CINNABAR",
        "ITEM_FLY_SAFFRON",
        "ITEM_FLY_ROUTE10",
    ]

    if world.options.viridian_city_roadblock == ViridianCityRoadblock.option_vanilla:
        free_fly_list.append("ITEM_FLY_PEWTER")
    if world.options.pewter_city_roadblock != PewterCityRoadblock.option_open:
        free_fly_list.extend(["ITEM_FLY_CERULEAN", "ITEM_FLY_VERMILION", "ITEM_FLY_ROUTE4"])
    if not world.options.kanto_only:
        free_fly_list.extend(["ITEM_FLY_ONE_ISLAND", "ITEM_FLY_TWO_ISLAND", "ITEM_FLY_THREE_ISLAND",
                              "ITEM_FLY_FOUR_ISLAND", "ITEM_FLY_FIVE_ISLAND", "ITEM_FLY_SEVEN_ISLAND",
                              "ITEM_FLY_SIX_ISLAND"])

    town_map_fly_list = copy.deepcopy(free_fly_list)

    if world.options.free_fly_location == FreeFlyLocation.option_any:
        free_fly_list.append("ITEM_FLY_INDIGO")

    if world.options.town_map_fly_location == TownMapFlyLocation.option_any:
        town_map_fly_list.append("ITEM_FLY_INDIGO")

    if world.options.free_fly_location != FreeFlyLocation.option_off:
        free_fly_location_id = world.random.choice(free_fly_list)
        world.free_fly_location_id = FLY_ITEM_ID_MAP[free_fly_location_id]

        if free_fly_location_id in town_map_fly_list:
            town_map_fly_list.remove(free_fly_location_id)

        menu_region = world.multiworld.get_region("Menu", world.player)
        free_fly_location = PokemonFRLGLocation(
            world.player,
            "Free Fly Location",
            None,
            menu_region,
            None,
            None,
            frozenset({"Event"})
        )
        item_id = data.constants[free_fly_location_id]
        free_fly_location.place_locked_item(PokemonFRLGItem(data.items[item_id].name,
                                                            ItemClassification.progression,
                                                            None,
                                                            world.player))
        free_fly_location.show_in_spoiler = False
        menu_region.locations.append(free_fly_location)

    if world.options.town_map_fly_location != TownMapFlyLocation.option_off:
        town_map_fly_location_id = world.random.choice(free_fly_list)
        world.town_map_fly_location_id = FLY_ITEM_ID_MAP[town_map_fly_location_id]

        menu_region = world.multiworld.get_region("Menu", world.player)
        town_map_fly_location = PokemonFRLGLocation(
            world.player,
            "Town Map Fly Location",
            None,
            menu_region,
            None,
            None,
            frozenset({"Event"})
        )
        item_id = data.constants[town_map_fly_location_id]
        town_map_fly_location.place_locked_item(PokemonFRLGItem(data.items[item_id].name,
                                                                 ItemClassification.progression,
                                                                 None,
                                                                 world.player))
        town_map_fly_location.access_rule = lambda state: state.has("Town Map", world.player)
        town_map_fly_location.show_in_spoiler = False
        menu_region.locations.append(town_map_fly_location)
