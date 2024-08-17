from typing import TYPE_CHECKING, Dict, FrozenSet, Iterable, List, Optional, Tuple, Union
from BaseClasses import Location, Region, ItemClassification
from .data import data, BASE_OFFSET
from .items import get_filler_item, offset_item_value, reverse_offset_item_value, PokemonFRLGItem
from .options import FreeFlyLocation, PewterCityRoadblock, ViridianCityRoadblock
if TYPE_CHECKING:
    from . import PokemonFRLGWorld


LOCATION_GROUPS = {
    "Badges": {
        "Pewter Gym - Leader Brock Prize",
        "Cerulean Gym - Leader Misty Prize",
        "Vermilion Gym - Leader Lt. Surge Prize",
        "Celadon Gym - Leader Erika Prize",
        "Fuchsia Gym - Leader Koga Prize",
        "Saffron Gym - Leader Sabrina Prize",
        "Cinnabar Gym - Leader Blaine Prize",
        "Viridian Gym - Leader Giovanni Prize"
    },
    "Gym TMs": {
        "Pewter Gym - Leader Brock Reward",
        "Cerulean Gym - Leader Misty Reward",
        "Vermilion Gym - Leader Lt. Surge Reward",
        "Celadon Gym - Leader Erika Reward",
        "Fuchsia Gym - Leader Koga Reward",
        "Saffron Gym - Leader Sabrina Reward",
        "Cinnabar Gym - Leader Blaine Reward",
        "Viridian Gym - Leader Giovanni Reward"
    },
    "Oak's Aides": {
        "Route 2 East Building - Professor Oak's Aide",
        "Route 10 Pokemon Center 1F - Professor Oak's Aide",
        "Route 11 East Entrance 2F - Professor Oak's Aide",
        "Route 16 North Entrance 2F - Professor Oak's Aide",
        "Route 15 West Entrance 2F - Professor Oak's Aide"
    }
}


FLY_EVENT_NAME_TO_ID = {
    "EVENT_FLY_PALLET_TOWN": 0,
    "EVENT_FLY_VIRIDIAN_CITY": 1,
    "EVENT_FLY_PEWTER_CITY": 2,
    "EVENT_FLY_ROUTE4": 3,
    "EVENT_FLY_CERULEAN_CITY": 4,
    "EVENT_FLY_VERMILION_CITY": 5,
    "EVENT_FLY_ROUTE10": 6,
    "EVENT_FLY_LAVENDER_TOWN": 7,
    "EVENT_FLY_CELADON_CITY": 8,
    "EVENT_FLY_FUCHSIA_CITY": 9,
    "EVENT_FLY_SAFFRON_CITY": 10,
    "EVENT_FLY_CINNABAR_ISLAND": 11,
    "EVENT_FLY_INDIGO_PLATEAU": 12,
    "EVENT_FLY_ONE_ISLAND": 13,
    "EVENT_FLY_TWO_ISLAND": 14,
    "EVENT_FLY_THREE_ISLAND": 15,
    "EVENT_FLY_FOUR_ISLAND": 16,
    "EVENT_FLY_FIVE_ISLAND": 17,
    "EVENT_FLY_SIX_ISLAND": 18,
    "EVENT_FLY_SEVEN_ISLAND": 19
}


class PokemonFRLGLocation(Location):
    game: str = "Pokemon FireRed and LeafGreen"
    item_address = Optional[Dict[str, int]]
    default_item_id: Optional[int]
    tags: FrozenSet[str]
    data_id: Optional[str]

    def __init__(
            self,
            player: int,
            name: str,
            address: Optional[int],
            parent: Optional[Region] = None,
            item_address: Optional[Dict[str, Union[int, List[int]]]] = None,
            default_item_id: Optional[int] = None,
            tags: FrozenSet[str] = frozenset(),
            data_id: Optional[str] = None) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_id = None if default_item_id is None else offset_item_value(default_item_id)
        self.item_address = item_address
        self.tags = tags
        self.data_id = data_id


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
    game_version = world.options.game_version.current_key

    tags = set(tags)

    for region_data in data.regions.values():
        region = regions[region_data.name]
        included_locations = [loc for loc in region_data.locations
                              if len(tags & data.locations[loc].tags) >= len(data.locations[loc].tags)]

        for location_flag in included_locations:
            location_data = data.locations[location_flag]

            location_id = offset_flag(location_data.flag)

            if location_data.default_item == data.constants["ITEM_NONE"]:
                default_item = reverse_offset_item_value(world.item_name_to_id[get_filler_item(world)])
            else:
                default_item = location_data.default_item

            if "Trainer" in location_data.tags:
                data_id = location_flag[:-7]
            else:
                data_id = location_flag

            location = PokemonFRLGLocation(
                world.player,
                location_data.name,
                location_id,
                region,
                location_data.address,
                default_item,
                location_data.tags,
                data_id
            )
            region.locations.append(location)

        excluded_trainer_locations = [loc for loc in region_data.locations
                                      if "Trainer" in data.locations[loc].tags and
                                      "Trainer" not in tags]

        for location_flag in excluded_trainer_locations:
            location_data = data.locations[location_flag]

            location = PokemonFRLGLocation(
                world.player,
                location_data.name,
                None,
                region,
                None,
                None,
                location_data.tags,
                location_flag[:-7]
            )
            location.place_locked_item(PokemonFRLGItem("None",
                                                       ItemClassification.filler,
                                                       None,
                                                       world.player))
            location.show_in_spoiler = False
            region.locations.append(location)

    trainer_level_object_list: List[Tuple[str, int]] = []
    land_water_level_object_list: List[Tuple[str, int]] = []
    fishing_level_object_list: List[Tuple[str, int]] = []

    if world.options.level_scaling:
        for region in regions.values():
            for location in region.locations:
                if "Trainer" in location.tags:
                    trainer_party_data = data.trainers[location.data_id].party
                    for i, pokemon in enumerate(trainer_party_data.pokemon):
                        trainer_level_object_list.append((f"{location.data_id} {i}", pokemon.level))
                elif "Pokemon" in location.tags:
                    if "Misc" in location.tags:
                        misc_pokemon_data = data.misc_pokemon[location.data_id]
                        # We don't want to include Pokémon whose level cannot be scaled
                        if misc_pokemon_data.level[game_version] != 0:
                            trainer_level_object_list.append((location.data_id, misc_pokemon_data.level[game_version]))
                    elif "Legendary" in location.tags:
                        legendary_pokemon_data = data.legendary_pokemon[location.data_id]
                        trainer_level_object_list.append((location.data_id, legendary_pokemon_data.level[game_version]))
                    elif "Wild" in location.tags:
                        data_ids: List[str] = location.data_id.split()
                        map_data = data.maps[data_ids[0]]
                        slot_ids: List[int] = [int(slot_id) for slot_id in data_ids[2:]]
                        encounters = (map_data.land_encounters if data_ids[1] == "LAND" else
                                      map_data.water_encounters if data_ids[1] == "WATER" else
                                      map_data.fishing_encounters if data_ids[1] == "FISHING" else
                                      None)
                        if encounters is not None:
                            for i, encounter in enumerate(encounters.slots[game_version]):
                                if i in slot_ids:
                                    name = f"{data_ids[0]} {data_ids[1]} {i}"
                                    if data_ids[1] in ["LAND", "WATER"]:
                                        avg_level = round((encounter.min_level + encounter.max_level) / 2)
                                        land_water_level_object_list.append((name, avg_level))
                                    elif data_ids[1] == "FISHING":
                                        avg_level = round((encounter.min_level + encounter.max_level) / 2)
                                        fishing_level_object_list.append((name, avg_level))

        trainer_level_object_list.sort(key=lambda i: i[1])
        land_water_level_object_list.sort(key=lambda i: i[1])
        fishing_level_object_list.sort(key=lambda i: i[1])
        world.trainer_id_list = [i[0] for i in trainer_level_object_list]
        world.trainer_level_list = [i[1] for i in trainer_level_object_list]
        world.land_water_id_list = [i[0] for i in land_water_level_object_list]
        world.land_water_level_list = [i[1] for i in land_water_level_object_list]
        world.fishing_id_list = [i[0] for i in fishing_level_object_list]
        world.fishing_level_list = [i[1] for i in fishing_level_object_list]


def set_free_fly(world: "PokemonFRLGWorld") -> None:
    # Set our free fly location
    free_fly_location_id = "EVENT_FLY_PALLET_TOWN"
    if world.options.free_fly_location != FreeFlyLocation.option_off:
        free_fly_list: List[str] = [
            "EVENT_FLY_ROUTE10",
            "EVENT_FLY_LAVENDER_TOWN",
            "EVENT_FLY_CELADON_CITY",
            "EVENT_FLY_FUCHSIA_CITY",
            "EVENT_FLY_SAFFRON_CITY",
            "EVENT_FLY_CINNABAR_ISLAND",
            "EVENT_FLY_ONE_ISLAND",
            "EVENT_FLY_TWO_ISLAND",
            "EVENT_FLY_THREE_ISLAND",
            "EVENT_FLY_FOUR_ISLAND",
            "EVENT_FLY_FIVE_ISLAND",
            "EVENT_FLY_SIX_ISLAND",
            "EVENT_FLY_SEVEN_ISLAND"
        ]

        if world.options.viridian_city_roadblock == ViridianCityRoadblock.option_vanilla:
            free_fly_list.append("EVENT_FLY_PEWTER_CITY")
        if world.options.pewter_city_roadblock != PewterCityRoadblock.option_open:
            free_fly_list.append("EVENT_FLY_ROUTE4")
            free_fly_list.append("EVENT_FLY_CERULEAN_CITY")
            free_fly_list.append("EVENT_FLY_VERMILION_CITY")
        if world.options.free_fly_location == FreeFlyLocation.option_any:
            free_fly_list.append("EVENT_FLY_INDIGO_PLATEAU")

        free_fly_location_id = world.random.choice(free_fly_list)

    world.free_fly_location_id = FLY_EVENT_NAME_TO_ID[free_fly_location_id]

    free_fly_location = world.multiworld.get_location("Free Fly Location", world.player)
    free_fly_location.item = None
    free_fly_location.place_locked_item(PokemonFRLGItem(
        data.events[free_fly_location_id].item,
        ItemClassification.progression,
        None,
        world.player
    ))
