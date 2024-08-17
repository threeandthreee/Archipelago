from typing import Dict, List, Tuple, Union

from BaseClasses import CollectionState

from .data import EncounterSpeciesData, MiscPokemonData, TrainerPokemonData


_RIVAL_IDS: Dict[str, List[str]] = {
    "TRAINER_RIVAL_OAKS_LAB_BULBASAUR": ["TRAINER_RIVAL_OAKS_LAB_CHARMANDER",
                                         "TRAINER_RIVAL_OAKS_LAB_SQUIRTLE"],
    "TRAINER_RIVAL_ROUTE22_EARLY_BULBASAUR": ["TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER",
                                              "TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE"],
    "TRAINER_RIVAL_CERULEAN_BULBASAUR": ["TRAINER_RIVAL_CERULEAN_CHARMANDER",
                                         "TRAINER_RIVAL_CERULEAN_SQUIRTLE"],
    "TRAINER_RIVAL_SS_ANNE_BULBASAUR": ["TRAINER_RIVAL_SS_ANNE_CHARMANDER",
                                        "TRAINER_RIVAL_SS_ANNE_SQUIRTLE"],
    "TRAINER_RIVAL_POKEMON_TOWER_BULBASAUR": ["TRAINER_RIVAL_POKEMON_TOWER_CHARMANDER",
                                              "TRAINER_RIVAL_POKEMON_TOWER_SQUIRTLE"],
    "TRAINER_RIVAL_SILPH_BULBASAUR": ["TRAINER_RIVAL_SILPH_CHARMANDER",
                                      "TRAINER_RIVAL_SILPH_SQUIRTLE"],
    "TRAINER_RIVAL_ROUTE22_LATE_BULBASAUR": ["TRAINER_RIVAL_ROUTE22_LATE_CHARMANDER",
                                             "TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE"],
    "TRAINER_CHAMPION_FIRST_BULBASAUR": ["TRAINER_CHAMPION_FIRST_CHARMANDER",
                                         "TRAINER_CHAMPION_FIRST_SQUIRTLE"]
}


def level_scaling(multiworld):
    state = CollectionState(multiworld)
    locations = set(multiworld.get_filled_locations())
    spheres = []

    while len(locations) > 0:
        sphere = set()

        for location in locations:
            def can_reach():
                if location.can_reach(state):
                    return True
                if ("Rock Tunnel 1F - Land Encounter" in location.name and
                    any([multiworld.get_entrance(e, location.player).connected_region.can_reach(state)
                        for e in ["Rock Tunnel 1F - Northeast to Route 10 - North",
                                  "Rock Tunnel 1F - South to Route 10 - South"]])):
                    return True
                return False

            if can_reach():
                sphere.add(location)

        if sphere:
            spheres.append(sphere)
            locations -= sphere
        else:
            spheres.append(locations)
            break

        for location in sphere:
            if not location.item:
                continue
            state.collect(location.item, True, location)

    for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
        if not world.options.level_scaling:
            continue

        game_version = world.options.game_version.current_key

        for sphere in spheres:
            locations = [loc for loc in sphere if loc.player == world.player]
            trainer_sphere_objects: List[Tuple[str, Union[MiscPokemonData, TrainerPokemonData]]] = []
            land_water_sphere_objects: List[Tuple[str, EncounterSpeciesData]] = []
            fishing_sphere_objects: List[Tuple[str, EncounterSpeciesData]] = []

            trainer_objects = [loc for loc in locations if "Trainer" in loc.tags]
            misc_pokemon_objects = [loc for loc in locations if "Pokemon" in loc.tags and "Misc" in loc.tags]
            legendary_pokemon_objects = [loc for loc in locations if "Pokemon" in loc.tags and "Legendary" in loc.tags]
            wild_pokemon_objects = [loc for loc in locations if "Pokemon" in loc.tags and "Wild" in loc.tags]

            for trainer in trainer_objects:
                trainer_party_data = world.modified_trainers[trainer.data_id].party
                for i, pokemon in enumerate(trainer_party_data.pokemon):
                    trainer_sphere_objects.append((f"{trainer.data_id} {i}", pokemon))

            for misc_pokemon in misc_pokemon_objects:
                misc_pokemon_data = world.modified_misc_pokemon[misc_pokemon.data_id]
                if misc_pokemon_data.level[game_version] != 0:
                    trainer_sphere_objects.append((misc_pokemon.data_id, misc_pokemon_data))

            for legendary_pokemon in legendary_pokemon_objects:
                legendary_pokemon_data = world.modified_legendary_pokemon[legendary_pokemon.data_id]
                trainer_sphere_objects.append((legendary_pokemon.data_id, legendary_pokemon_data))

            for wild_pokemon in wild_pokemon_objects:
                data_ids: List[str] = wild_pokemon.data_id.split()
                map_data = world.modified_maps[data_ids[0]]
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
                                land_water_sphere_objects.append((name, encounter))
                            elif data_ids[1] == "FISHING":
                                fishing_sphere_objects.append((name, encounter))

            trainer_sphere_objects.sort(key=lambda obj: world.trainer_id_list.index(obj[0]))
            land_water_sphere_objects.sort(key=lambda obj: world.land_water_id_list.index(obj[0]))
            fishing_sphere_objects.sort(key=lambda obj: world.fishing_id_list.index(obj[0]))

            for trainer_object in trainer_sphere_objects:
                if type(trainer_object[1]) is TrainerPokemonData:
                    trainer_id = trainer_object[0].split()[0]
                    if trainer_id in _RIVAL_IDS:
                        level = world.trainer_level_list.pop(0)
                        trainer_object[1].level = level
                        slot_id = int(trainer_object[0].split()[1])
                        for rival_id in _RIVAL_IDS[trainer_id]:
                            trainer_pokemon = world.modified_trainers[rival_id].party.pokemon[slot_id]
                            trainer_pokemon.level = level
                    else:
                        trainer_object[1].level = world.trainer_level_list.pop(0)
                elif type(trainer_object[1]) is MiscPokemonData:
                    trainer_object[1].level[game_version] = world.trainer_level_list.pop(0)

            for land_water_object in land_water_sphere_objects:
                level = world.land_water_level_list.pop(0)
                land_water_object[1].min_level = level
                land_water_object[1].max_level = level

            for fishing_object in fishing_sphere_objects:
                level = world.fishing_level_list.pop(0)
                fishing_object[1].min_level = level
                fishing_object[1].max_level = level

    for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
        world.finished_level_scaling.set()
