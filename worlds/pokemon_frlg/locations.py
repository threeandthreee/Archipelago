import copy
from typing import TYPE_CHECKING, Dict, FrozenSet, Iterable, List, Optional, Union
from BaseClasses import CollectionState, Location, Region, ItemClassification
from .data import data
from .items import PokemonFRLGItem, get_random_item
from .options import FreeFlyLocation, TownMapFlyLocation, ViridianCityRoadblock

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
        "Route 2 Gate - Oak's Aide Gift (Pokedex Progress)",
        "Route 10 Pokemon Center 1F - Oak's Aide Gift (Pokedex Progress)",
        "Route 11 Gate 2F - Oak's Aide Gift (Pokedex Progress)",
        "Route 16 Gate 2F - Oak's Aide Gift (Pokedex Progress)",
        "Route 15 Gate 2F - Oak's Aide Gift (Pokedex Progress)"
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

sevii_required_locations = [
    "One Cinnabar Pokemon Center 1F - Bill",
    "Lorelei's Room - Elite Four Lorelei Rematch Reward",
    "Bruno's Room - Elite Four Bruno Rematch Reward",
    "Agatha's Room - Elite Four Agatha Rematch Reward",
    "Lance's Room - Elite Four Lance Rematch Reward",
    "Champion's Room - Champion Rematch Reward"
]

fly_item_exclusion_map = {
    "Pallet Town": "ITEM_FLY_PALLET",
    "Viridian City South": "ITEM_FLY_VIRIDIAN",
    "Pewter City": "ITEM_FLY_PEWTER",
    "Cerulean City": "ITEM_FLY_CERULEAN",
    "Lavender Town": "ITEM_FLY_LAVENDER",
    "Vermilion City": "ITEM_FLY_VERMILION",
    "Celadon City": "ITEM_FLY_CELADON",
    "Fuchsia City": "ITEM_FLY_FUCHSIA",
    "Cinnabar Island": "ITEM_FLY_CINNABAR",
    "Indigo Plateau": "ITEM_FLY_INDIGO",
    "Saffron City": "ITEM_FLY_SAFFRON",
    "One Island Town": "ITEM_FLY_ONE_ISLAND",
    "Two Island Town": "ITEM_FLY_TWO_ISLAND",
    "Three Island Town": "ITEM_FLY_THREE_ISLAND",
    "Four Island Town": "ITEM_FLY_FOUR_ISLAND",
    "Five Island Town": "ITEM_FLY_FIVE_ISLAND",
    "Six Island Town": "ITEM_FLY_SIX_ISLAND",
    "Seven Island Town": "ITEM_FLY_SEVEN_ISLAND",
    "Route 4 West": "ITEM_FLY_ROUTE4",
    "Route 10 North": "ITEM_FLY_ROUTE10"
}


class PokemonFRLGLocation(Location):
    game: str = "Pokemon FireRed and LeafGreen"
    item_address = Optional[Dict[str, int]]
    default_item_id: Optional[int]
    tags: FrozenSet[str]
    data_ids: Optional[List[str]]
    spoiler_name: str

    def __init__(
            self,
            player: int,
            name: str,
            address: Optional[int],
            parent: Optional[Region] = None,
            item_address: Optional[Dict[str, Union[int, List[int]]]] = None,
            default_item_id: Optional[int] = None,
            tags: FrozenSet[str] = frozenset(),
            data_ids: Optional[List[str]] = None,
            spoiler_name: Optional[str] = None) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_id = default_item_id
        self.item_address = item_address
        self.tags = tags
        self.data_ids = data_ids
        self.spoiler_name = spoiler_name if spoiler_name is not None else name


def create_location_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from location names to their AP location ID (address)
    """
    name_to_id_mapping: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_id in region_data.locations:
            location_data = data.locations[location_id]
            name_to_id_mapping[location_data.name] = location_data.flag

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

            if world.options.kanto_only and location_data.name in sevii_required_locations:
                continue

            if location_data.default_item == data.constants["ITEM_NONE"]:
                default_item = world.item_name_to_id[get_random_item(world, ItemClassification.filler)]
            else:
                default_item = location_data.default_item

            location = PokemonFRLGLocation(
                world.player,
                location_data.name,
                location_data.flag,
                region,
                location_data.address,
                default_item,
                location_data.tags
            )
            region.locations.append(location)


def set_free_fly(world: "PokemonFRLGWorld") -> None:
    # Set our free fly location
    world.free_fly_location_id = FLY_ITEM_ID_MAP["ITEM_FLY_NONE"]
    world.town_map_fly_location_id = FLY_ITEM_ID_MAP["ITEM_FLY_NONE"]

    if (world.options.free_fly_location == FreeFlyLocation.option_off and
            world.options.town_map_fly_location == TownMapFlyLocation.option_off):
        return

    state = CollectionState(world.multiworld)
    regions = world.multiworld.get_regions(world.player)
    locations = world.multiworld.get_locations(world.player)
    free_fly_list: List[str] = [
        "ITEM_FLY_PALLET",
        "ITEM_FLY_VIRIDIAN",
        "ITEM_FLY_PEWTER",
        "ITEM_FLY_CERULEAN",
        "ITEM_FLY_VERMILION",
        "ITEM_FLY_LAVENDER",
        "ITEM_FLY_CELADON",
        "ITEM_FLY_FUCHSIA",
        "ITEM_FLY_CINNABAR",
        "ITEM_FLY_SAFFRON",
        "ITEM_FLY_ROUTE4",
        "ITEM_FLY_ROUTE10",
        "ITEM_FLY_ONE_ISLAND",
        "ITEM_FLY_TWO_ISLAND",
        "ITEM_FLY_THREE_ISLAND",
        "ITEM_FLY_FOUR_ISLAND",
        "ITEM_FLY_FIVE_ISLAND",
        "ITEM_FLY_SIX_ISLAND",
        "ITEM_FLY_SEVEN_ISLAND"
    ]

    if (world.options.viridian_city_roadblock == ViridianCityRoadblock.option_early_parcel and
            not world.options.random_starting_town):
        item = PokemonFRLGItem("Oak's Parcel", ItemClassification.progression, None, world.player)
        state.collect(item, True)

    found_event = True
    collected_events = set()
    while found_event:
        found_event = False
        for location in locations:
            if state.can_reach(location) and location.is_event and location not in collected_events:
                state.collect(location.item, True, location)
                collected_events.add(location)
                found_event = True

    reachable_regions = set()
    for region in regions:
        if region.can_reach(state):
            reachable_regions.add(region.name)

    if world.options.kanto_only:
        sevii_islands = ["ITEM_FLY_ONE_ISLAND", "ITEM_FLY_TWO_ISLAND", "ITEM_FLY_THREE_ISLAND", "ITEM_FLY_FOUR_ISLAND",
                         "ITEM_FLY_FIVE_ISLAND", "ITEM_FLY_SIX_ISLAND", "ITEM_FLY_SEVEN_ISLAND"]
        free_fly_list = [fly for fly in free_fly_list if fly not in sevii_islands]

    town_map_fly_list = copy.deepcopy(free_fly_list)

    if world.options.free_fly_location == FreeFlyLocation.option_any:
        free_fly_list.append("ITEM_FLY_INDIGO")

    if world.options.town_map_fly_location == TownMapFlyLocation.option_any:
        town_map_fly_list.append("ITEM_FLY_INDIGO")

    for region in reachable_regions:
        if region in fly_item_exclusion_map.keys():
            fly_to_remove = fly_item_exclusion_map[region]
            if fly_to_remove in free_fly_list:
                free_fly_list.remove(fly_to_remove)
            if fly_to_remove in town_map_fly_list:
                town_map_fly_list.remove(fly_to_remove)

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
        town_map_fly_location_id = world.random.choice(town_map_fly_list)
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
