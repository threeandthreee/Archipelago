"""
Functions related to AP regions for Pokémon FireRed and LeafGreen (see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Dict, List, Tuple, Optional, Callable
from BaseClasses import Region, CollectionState, ItemClassification
from .data import data
from .items import PokemonFRLGItem
from .locations import PokemonFRLGLocation
from .options import GameVersion, LevelScaling

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

INDIRECT_CONDITIONS: Dict[str, List[str]] = {
    "Seafoam Islands 1F": ["Seafoam Islands B3F Southwest Surfing Spot", "Seafoam Islands B3F Southwest Landing",
                           "Seafoam Islands B3F East Landing (South)", "Seafoam Islands B3F East Surfing Spot (South)",
                           "Seafoam Islands B3F South Water (Water Battle)"],
    "Seafoam Islands B3F Southwest": ["Seafoam Islands B4F Surfing Spot (West)",
                                      "Seafoam Islands B4F Near Articuno Landing"],
    "Victory Road 3F Southwest": ["Victory Road 2F Center Rock Barrier"],
    "Vermilion City": ["Navel Rock Arrival", "Birth Island Arrival"]
}

SEVII_REQUIRED_EVENTS = [
    "Champion's Room - Champion Rematch Reward"
]

STATIC_POKEMON_SPOILER_NAMES = {
    "STATIC_POKEMON_ELECTRODE_1": "Power Plant (Static)",
    "STATIC_POKEMON_ELECTRODE_2": "Power Plant (Static)",
    "LEGENDARY_POKEMON_ZAPDOS": "Power Plant (Static)",
    "CELADON_PRIZE_POKEMON_1": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_2": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_3": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_4": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_5": "Celadon Game Corner Prize Room",
    "GIFT_POKEMON_EEVEE": "Celadon Condominiums Roof Room",
    "STATIC_POKEMON_ROUTE12_SNORLAX": "Route 12 (Static)",
    "STATIC_POKEMON_ROUTE16_SNORLAX": "Route 16 (Static)",
    "GIFT_POKEMON_HITMONCHAN": "Saffron Dojo",
    "GIFT_POKEMON_HITMONLEE": "Saffron Dojo",
    "GIFT_POKEMON_LAPRAS": "Silph Co. 7F",
    "LEGENDARY_POKEMON_ARTICUNO": "Seafoam Islands B4F (Static)",
    "GIFT_POKEMON_OMANYTE": "Pokemon Lab Experiment Room (Helix)",
    "GIFT_POKEMON_KABUTO": "Pokemon Lab Experiment Room (Dome)",
    "GIFT_POKEMON_AERODACTYL": "Pokemon Lab Experiment Room (Amber)",
    "LEGENDARY_POKEMON_MOLTRES": "Mt. Ember Summit",
    "STATIC_POKEMON_HYPNO": "Berry Forest (Static)",
    "EGG_POKEMON_TOGEPI": "Water Labyrinth (Egg)",
    "LEGENDARY_POKEMON_MEWTWO": "Cerulean Cave B1F (Static)",
    "LEGENDARY_POKEMON_HO_OH": "Navel Rock Summit",
    "LEGENDARY_POKEMON_LUGIA": "Navel Rock Base",
    "LEGENDARY_POKEMON_DEOXYS": "Birth Island Exterior"
}

STARTING_TOWNS = {
    "SPAWN_PALLET_TOWN": "Pallet Town",
    "SPAWN_VIRIDIAN_CITY": "Viridian City South",
    "SPAWN_PEWTER_CITY": "Pewter City",
    "SPAWN_CERULEAN_CITY": "Cerulean City",
    "SPAWN_LAVENDER_TOWN": "Lavender Town",
    "SPAWN_VERMILION_CITY": "Vermilion City",
    "SPAWN_CELADON_CITY": "Celadon City",
    "SPAWN_FUCHSIA_CITY": "Fuchsia City",
    "SPAWN_CINNABAR_ISLAND": "Cinnabar Island",
    "SPAWN_INDIGO_PLATEAU": "Indigo Plateau",
    "SPAWN_SAFFRON_CITY": "Saffron City",
    "SPAWN_ROUTE4": "Route 4 West",
    "SPAWN_ROUTE10": "Route 10 North",
    "SPAWN_ONE_ISLAND": "One Island Town",
    "SPAWN_TWO_ISLAND": "Two Island Town",
    "SPAWN_THREE_ISLAND": "Three Island Town",
    "SPAWN_FOUR_ISLAND": "Four Island Town",
    "SPAWN_FIVE_ISLAND": "Five Island Town",
    "SPAWN_SEVEN_ISLAND": "Seven Island Town",
    "SPAWN_SIX_ISLAND": "Six Island Town"
}


class PokemonFRLGRegion(Region):
    distance: Optional[int]

    def __init__(self, name, player, multiworld):
        super().__init__(name, player, multiworld)
        self.distance = None


def create_regions(world: "PokemonFRLGWorld") -> Dict[str, Region]:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """

    # Used in connect_to_map_encounters. Splits encounter categories into "subcategories" and gives them names
    # and rules so the rods can only access their specific slots.
    encounter_categories: Dict[str, List[Tuple[Optional[str], range, Optional[Callable[[CollectionState], bool]]]]] = {
        "Land": [(None, range(0, 12), None)],
        "Water": [(None, range(0, 5), None)],
        "Fishing": [
            ("Old Rod", range(0, 2), lambda state: state.has("Old Rod", world.player)),
            ("Good Rod", range(2, 5), lambda state: state.has("Good Rod", world.player)),
            ("Super Rod", range(5, 10), lambda state: state.has("Super Rod", world.player)),
        ],
    }

    game_version = world.options.game_version.current_key
    kanto_only = world.options.kanto_only

    def connect_to_map_encounters(regions: Dict[str, Region], region: Region, map_name: str, encounter_region_name: str,
                                  include_slots: Tuple[bool, bool, bool]):
        """
        Connects the provided region to the corresponding wild encounters for the given parent map.

        Each in-game map may have a non-physical Region for encountering wild Pokémon in each of the three categories
        land, water, and fishing. Region data defines whether a given region includes places where those encounters can
        be accessed (i.e. whether the region has tall grass, a river bank, is on water, etc.).

        These regions are created lazily and dynamically so as not to bother with unused maps.
        """

        if True in include_slots and encounter_region_name is None:
            raise AssertionError(f"{region.name} has encounters but does not have an encounter region name")

        for i, encounter_category in enumerate(encounter_categories.items()):
            if include_slots[i]:
                region_name = f"{encounter_region_name} {encounter_category[0]} Encounters"

                # If the region hasn't been created yet, create it now
                try:
                    encounter_region = regions[region_name]
                except KeyError:
                    encounter_region = PokemonFRLGRegion(region_name, world.player, world.multiworld)
                    encounter_slots = getattr(world.modified_maps[map_name],
                                              f"{encounter_category[0].lower()}_encounters").slots[game_version]

                    # Subcategory is for splitting fishing rods; land and water only have one subcategory
                    for subcategory in encounter_category[1]:
                        # Want to create locations per species, not per slot
                        # encounter_categories includes info on which slots belong to which subcategory
                        unique_species = []
                        for j, species_data in enumerate(encounter_slots):
                            species_id = species_data.species_id
                            if j in subcategory[1] and species_id not in unique_species:
                                unique_species.append(species_id)

                        # Create a location for the species
                        for j, species_id in enumerate(unique_species):
                            subcategory_name = subcategory[0] if subcategory[0] is not None else encounter_category[0]

                            encounter_location = PokemonFRLGLocation(
                                world.player,
                                f"{encounter_region_name} - {subcategory_name} Encounter {j + 1}",
                                None,
                                encounter_region,
                                None,
                                None,
                                frozenset(["Pokemon", "Wild"]),
                                spoiler_name=f"{encounter_region_name} ({subcategory_name})",
                            )
                            encounter_location.show_in_spoiler = False

                            # Add access rules
                            if subcategory[2] is not None:
                                encounter_location.access_rule = subcategory[2]

                            # Fill the location with an event for catching that species
                            encounter_location.place_locked_item(PokemonFRLGItem(
                                data.species[species_id].name,
                                ItemClassification.progression_skip_balancing,
                                None,
                                world.player
                            ))
                            world.repeatable_pokemon.add(data.species[species_id].name)
                            encounter_region.locations.append(encounter_location)

                    # Add the new encounter region to the multiworld
                    regions[region_name] = encounter_region

                # Encounter region exists, just connect to it
                region.connect(encounter_region, f"{region.name} ({encounter_category[0]} Battle)")

    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    for region_data in data.regions.values():
        if kanto_only and not region_data.kanto:
            continue

        region_name = region_data.name
        new_region = PokemonFRLGRegion(region_name, world.player, world.multiworld)

        for event_id in region_data.events:
            event_data = world.modified_events[event_id]

            if world.options.kanto_only and event_data.name in SEVII_REQUIRED_EVENTS:
                continue

            if type(event_data.name) is list:
                if world.options.game_version == GameVersion.option_firered:
                    name = event_data.name[0]
                else:
                    name = event_data.name[1]
            else:
                name = event_data.name

            if type(event_data.item) is list:
                if world.options.game_version == GameVersion.option_firered:
                    item = event_data.item[0]
                else:
                    item = event_data.item[1]
            else:
                item = event_data.item

            event = PokemonFRLGLocation(world.player,
                                        name,
                                        None,
                                        new_region,
                                        None,
                                        None,
                                        event_data.tags,
                                        spoiler_name=STATIC_POKEMON_SPOILER_NAMES[event_id]
                                        if event_id in STATIC_POKEMON_SPOILER_NAMES else None)
            event.place_locked_item(PokemonFRLGItem(item,
                                                    ItemClassification.progression,
                                                    None,
                                                    world.player))
            event.show_in_spoiler = False
            new_region.locations.append(event)

            if "Trade" in name:
                world.trade_pokemon.append([region_name, name])

        for region_id, exit_name in region_data.exits.items():
            if kanto_only and not data.regions[region_id].kanto:
                continue
            region_exit = data.regions[region_id].name
            connections.append((exit_name, region_name, region_exit))

        for warp in region_data.warps:
            source_warp = data.warps[warp]
            if source_warp.name == "":
                continue
            dest_warp = data.warps[data.warp_map[warp]]
            if dest_warp.parent_region_id is None:
                continue
            if kanto_only and not data.regions[dest_warp.parent_region_id].kanto:
                continue
            dest_region_name = data.regions[dest_warp.parent_region_id].name
            connections.append((source_warp.name, region_name, dest_region_name))

        regions[region_name] = new_region

        parent_map_name = region_data.parent_map.name if region_data.parent_map is not None else None
        connect_to_map_encounters(regions, new_region, parent_map_name, region_data.encounter_region,
                                  (region_data.has_land, region_data.has_water, region_data.has_fishing))

    for name, source, dest in connections:
        name = modify_entrance_name(world, name)
        regions[source].connect(regions[dest], name)

    if world.options.level_scaling != LevelScaling.option_off:
        trainer_name_level_list: List[Tuple[str, int]] = []
        encounter_name_level_list: List[Tuple[str, int]] = []

        game_version = world.options.game_version.current_key

        for scaling_data in world.scaling_data:
            if scaling_data.region not in regions:
                region = PokemonFRLGRegion(scaling_data.region, world.player, world.multiworld)
                regions[scaling_data.region] = region

                for connection in scaling_data.connections:
                    name = f"{regions[connection].name} -> {region.name}"
                    regions[connection].connect(region, name)
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
                region.locations.append(scaling_event)
            elif "Wild" in scaling_data.tags:
                index = 1
                events: Dict[str, Tuple[str, List[str], Optional[Callable[[CollectionState], bool]]]] = {}
                encounter_category_data = encounter_categories[scaling_data.type]
                for data_id in scaling_data.data_ids:
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

    if world.options.random_starting_town:
        forbidden_starting_towns = ["SPAWN_INDIGO_PLATEAU", "SPAWN_ROUTE10"]
        if world.options.kanto_only:
            forbidden_starting_towns.extend(["SPAWN_ONE_ISLAND", "SPAWN_TWO_ISLAND", "SPAWN_THREE_ISLAND",
                                             "SPAWN_FOUR_ISLAND", "SPAWN_FIVE_ISLAND", "SPAWN_SIX_ISLAND",
                                             "SPAWN_SEVEN_ISLAND"])
        allowed_starting_towns = [town for town in STARTING_TOWNS.keys() if town not in forbidden_starting_towns]
        world.starting_town = world.random.choice(allowed_starting_towns)

    regions["Menu"] = PokemonFRLGRegion("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions[STARTING_TOWNS[world.starting_town]], "Start Game")
    regions["Menu"].connect(regions["Player's PC"], "Use PC")
    regions["Menu"].connect(regions["Pokedex"], "Pokedex")
    regions["Menu"].connect(regions["Evolutions"], "Evolve")
    regions["Menu"].connect(regions["Sky"], "Flying")

    return regions


def create_indirect_conditions(world: "PokemonFRLGWorld"):
    for region, entrances in INDIRECT_CONDITIONS.items():
        for entrance in entrances:
            world.multiworld.register_indirect_condition(world.get_region(region), world.get_entrance(entrance))


def modify_entrance_name(world: "PokemonFRLGWorld", name: str) -> str:
    route_2_modification = {
        "Route 2 Northwest Cuttable Tree": "Route 2 Northwest Smashable Rock",
        "Route 2 Northeast Cuttable Tree (North)": "Route 2 Northeast Smashable Rock",
        "Route 2 Northeast Cuttable Tree (South)": "Route 2 Northeast Cuttable Tree"
    }
    block_tunnels = {
        "Route 5 Unobstructed Path": "Route 5 Smashable Rocks",
        "Route 5 Near Tunnel Unobstructed Path": "Route 5 Near Tunnel Smashable Rocks",
        "Route 6 Unobstructed Path": "Route 6 Smashable Rocks",
        "Route 6 Near Tunnel Unobstructed Path": "Route 6 Near Tunnel Smashable Rocks",
        "Route 7 Unobstructed Path": "Route 7 Smashable Rocks",
        "Route 7 Near Tunnel Unobstructed Path": "Route 7 Near Tunnel Smashable Rocks",
        "Route 8 Unobstructed Path": "Route 8 Smashable Rocks",
        "Route 8 Near Tunnel Unobstructed Path": "Route 8 Near Tunnel Smashable Rocks"
    }
    block_pokemon_tower = {
        "Pokemon Tower 1F Unobstructed Path": "Pokemon Tower 1F Reveal Ghost",
        "Pokemon Tower 1F Near Stairs Unobstructed Path": "Pokemon Tower 1F Near Stairs Pass Ghost"
    }
    rotue_23_trees = {
        "Route 23 Near Water Unobstructed Path": "Route 23 Near Water Cuttable Trees",
        "Route 23 Center Unobstructed Path": "Route 23 Center Cuttable Trees"
    }
    route_23_modification = {
        "Route 23 South Water Unobstructed Path": "Route 23 Waterfall Ascend",
        "Route 23 North Water Unobstructed Path": "Route 23 Waterfall Drop"
    }

    if "Modify Route 2" in world.options.modify_world_state.value and name in route_2_modification.keys():
        return route_2_modification[name]
    if "Block Tunnels" in world.options.modify_world_state.value and name in block_tunnels.keys():
        return block_tunnels[name]
    if "Block Tower" in world.options.modify_world_state.value and name in block_pokemon_tower.keys():
        return block_pokemon_tower[name]
    if "Route 23 Trees" in world.options.modify_world_state.value and name in rotue_23_trees.keys():
        return rotue_23_trees[name]
    if "Modify Route 23" in world.options.modify_world_state.value and name in route_23_modification.keys():
        return route_23_modification[name]
    return name
