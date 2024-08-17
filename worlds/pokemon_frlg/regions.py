"""
Functions related to AP regions for Pokémon FireRed and LeafGreen (see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Dict, List, Tuple, Optional, Callable
from BaseClasses import Region, CollectionState, ItemClassification
from .data import data
from .items import PokemonFRLGItem
from .locations import PokemonFRLGLocation
from .options import GameVersion
if TYPE_CHECKING:
    from . import PokemonFRLGWorld

exclusive_gift_pokemon: List[str] = {
    "TRADE_POKEMON_NIDORAN",
    "TRADE_POKEMON_NIDORINOA",
    "CELADON_PRIZE_POKEMON_3",
    "CELADON_PRIZE_POKEMON_4",
    "TRADE_POKEMON_LICKITUNG"
}


indirect_conditions: Dict[str, List[Tuple[str, str]]] = {
    "Seafoam Islands 1F": [("Seafoam Islands B3F - West", "Seafoam Islands B3F - Water"),
                           ("Seafoam Islands B3F - Southeast", "Seafoam Islands B3F - Water"),
                           ("Seafoam Islands B3F - Water", "Seafoam Islands B3F - West"),
                           ("Seafoam Islands B3F - Water", "Seafoam Islands B3F - Southeast")],
    "Seafoam Islands B3F - West": [("Seafoam Islands B4F", "Seafoam Islands B4F - Water W"),
                                   ("Seafoam Islands B4F - Water W", "Seafoam Islands B4F - Articuno")],
    "Victory Road 3F - Southwest": [("Victory Road 2F - Center", "Victory Road 2F - Southeast")]
}


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

    def connect_to_map_encounters(regions: Dict[str, Region], region: Region, map_name: str, encounter_region_name: str,
                                  include_slots: Tuple[bool, bool, bool]):
        """
        Connects the provided region to the corresponding wild encounters for the given parent map.

        Each in-game map may have a non-physical Region for encountering wild Pokémon in each of the three categories
        land, water, and fishing. Region data defines whether a given region includes places where those encounters can
        be accessed (i.e. whether the region has tall grass, a river bank, is on water, etc.).

        These regions are created lazily and dynamically so as not to bother with unused maps.
        """
        game_version = world.options.game_version.current_key

        if encounter_region_name is None:
            AssertionError(f"Region {region} has encounters but doesn't have an encounter region name")

        for i, encounter_category in enumerate(encounter_categories.items()):
            if include_slots[i]:
                region_name = f"{encounter_region_name} - {encounter_category[0]} Encounters"

                # If the region hasn't been created yet, create it now
                try:
                    encounter_region = regions[region_name]
                except KeyError:
                    encounter_region = Region(region_name, world.player, world.multiworld)
                    encounter_slots = getattr(world.modified_maps[map_name],
                                              f"{encounter_category[0].lower()}_encounters").slots[game_version]

                    # Subcategory is for splitting fishing rods; land and water only have one subcategory
                    for subcategory in encounter_category[1]:
                        # Want to create locations per species, not per slot
                        # encounter_categories includes info on which slots belong to which subcategory
                        unique_species = []
                        slot_ids: List[List[int]] = []
                        for j, species_data in enumerate(encounter_slots):
                            species_id = species_data.species_id
                            if j in subcategory[1] and species_id not in unique_species:
                                unique_species.append(species_id)
                                slot_ids.append([j])
                            elif j in subcategory[1] and species_id in unique_species:
                                slot_ids[unique_species.index(species_id)].append(j)

                        # Create a location for the species
                        for j, species_id in enumerate(unique_species):
                            subcategory_name = subcategory[0] if subcategory[0] is not None else encounter_category[0]
                            slots_str = ""

                            for slot_id in slot_ids[j]:
                                slots_str += f" {slot_id}"

                            encounter_location = PokemonFRLGLocation(
                                world.player,
                                f"{encounter_region_name} - {subcategory_name} Encounter {j + 1}",
                                None,
                                encounter_region,
                                None,
                                None,
                                frozenset(["Pokemon", "Wild"]),
                                f"{map_name} {encounter_category[0].upper()}{slots_str}"
                            )
                            encounter_location.show_in_spoiler = False

                            # Add access rules
                            if subcategory[2] is not None:
                                encounter_location.access_rule = subcategory[2]

                            # Fill the location with an event for catching that species
                            encounter_location.place_locked_item(PokemonFRLGItem(
                                data.species[species_id].name,
                                ItemClassification.progression,
                                None,
                                world.player
                            ))
                            encounter_region.locations.append(encounter_location)

                    # Add the new encounter region to the multiworld
                    regions[region_name] = encounter_region

                # Encounter region exists, just connect to it
                region.connect(encounter_region, f"{region.name} to {region_name}")

    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    for region_data in data.regions.values():
        region_name = region_data.name
        new_region = Region(region_name, world.player, world.multiworld)

        for event_id in region_data.events:
            event_data = world.modified_events[event_id]

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
                                        event_id)
            event.place_locked_item(PokemonFRLGItem(item,
                                                    ItemClassification.progression,
                                                    None,
                                                    world.player))
            event.show_in_spoiler = False
            new_region.locations.append(event)

            if "Trade" in name:
                world.trade_pokemon.append([region_name, name])

        for region_exit in region_data.exits:
            exit_name = data.regions[region_exit].name
            connections.append((f"{region_name} to {exit_name}", region_name, exit_name))

        for warp in region_data.warps:
            dest_warp = data.warps[data.warp_map[warp]]
            if dest_warp.parent_region_id is None:
                continue
            dest_warp_name = dest_warp.name
            dest_region_name = data.regions[dest_warp.parent_region_id].name
            if dest_warp_name is None:
                dest_warp_name = dest_region_name
            connections.append((f"{region_name} to {dest_warp_name}", region_name, dest_region_name))

        regions[region_name] = new_region

        connect_to_map_encounters(regions, new_region, region_data.parent_map.name, region_data.encounter_region,
                                  (region_data.has_land, region_data.has_water, region_data.has_fishing))

    for name, source, dest in connections:
        regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["Player's House 2F"], "Start Game")

    return regions


def create_indirect_conditions(world: "PokemonFRLGWorld"):
    for region, entrances in indirect_conditions.items():
        for entrance in entrances:
            world.multiworld.register_indirect_condition(world.get_region(region),
                                                         world.get_entrance(f"{entrance[0]} to {entrance[1]}"))
