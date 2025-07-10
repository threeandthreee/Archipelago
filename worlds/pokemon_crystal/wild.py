from collections import defaultdict
from dataclasses import replace
from typing import TYPE_CHECKING

from .data import EncounterMon, LogicalAccess, EncounterType, EncounterKey
from .options import RandomizeWilds, EncounterGrouping, BreedingMethodsRequired
from .pokemon import get_random_pokemon, pokemon_convert_friendly_to_ids, get_priority_dexsanity

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_wild_pokemon(world: "PokemonCrystalWorld"):
    if world.options.randomize_wilds:

        world.generated_wooper = get_random_pokemon(world, exclude_unown=True)

        required_logical_pokemon = 0
        required_accessible_pokemon = 0
        required_inaccessible_pokemon = 0

        for region_key, wilds in world.generated_wild.items():
            logical_access = world.generated_wild_region_logic[region_key]

            if world.options.encounter_grouping == EncounterGrouping.option_all_split:
                count = len(wilds)
            elif world.options.encounter_grouping == EncounterGrouping.option_one_per_method:
                count = 1
            else:
                count = len({encounter.pokemon for encounter in wilds})

            if logical_access is LogicalAccess.InLogic:
                required_logical_pokemon += count
            elif logical_access is LogicalAccess.OutOfLogic:
                required_accessible_pokemon += count
            else:
                required_inaccessible_pokemon += count

        logical_pokemon_pool = list[str]()
        accessible_pokemon_pool = list[str]()

        if world.options.randomize_wilds.value == RandomizeWilds.option_base_forms:
            logical_pokemon_pool.extend(
                pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if pokemon_data.is_base)
        elif world.options.randomize_wilds.value == RandomizeWilds.option_evolution_lines:
            base_pokemon = [pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                            pokemon_data.is_base]
            evo_lines = list[list[str]]()
            for base in base_pokemon:
                line = [base]
                for evo in world.generated_pokemon[base].evolutions:
                    line.append(evo.pokemon)
                    for evo2 in world.generated_pokemon[evo.pokemon].evolutions:
                        line.append(evo2.pokemon)
                evo_lines.append(line)

            logical_pokemon_pool.extend(world.random.choice(evo_line) for evo_line in evo_lines)
        elif world.options.randomize_wilds.option_catch_em_all:
            logical_pokemon_pool.extend(world.generated_pokemon.keys())

        logical_pokemon_pool.extend(get_priority_dexsanity(world))

        global_blocklist = pokemon_convert_friendly_to_ids(world, world.options.wild_encounter_blocklist)

        if global_blocklist:
            logical_pokemon_pool = [pokemon_id for pokemon_id in logical_pokemon_pool if
                                    pokemon_id not in global_blocklist]

        if len(logical_pokemon_pool) > required_logical_pokemon:
            world.random.shuffle(logical_pokemon_pool)
            accessible_pokemon_pool = logical_pokemon_pool[(len(accessible_pokemon_pool) - required_logical_pokemon):]
            logical_pokemon_pool = logical_pokemon_pool[:required_logical_pokemon]

        if len(logical_pokemon_pool) < required_logical_pokemon:
            logical_pokemon_pool.extend(get_random_pokemon(world, blocklist=global_blocklist) for _ in
                                        range(required_logical_pokemon - len(logical_pokemon_pool)))

        if (world.options.breeding_methods_required.value == BreedingMethodsRequired.option_with_ditto
                and "DITTO" not in logical_pokemon_pool):
            accessible_pokemon_pool.append(logical_pokemon_pool.pop())
            logical_pokemon_pool.append("DITTO")

        world.random.shuffle(logical_pokemon_pool)

        if len(accessible_pokemon_pool) > required_accessible_pokemon:
            accessible_pokemon_pool = accessible_pokemon_pool[:required_accessible_pokemon]

        if len(accessible_pokemon_pool) < required_accessible_pokemon:
            accessible_pokemon_pool.extend(get_random_pokemon(world, blocklist=global_blocklist) for _ in
                                           range(required_accessible_pokemon - len(accessible_pokemon_pool)))

        world.random.shuffle(accessible_pokemon_pool)

        inaccessible_pokemon_pool = [get_random_pokemon(world, blocklist=global_blocklist) for _ in
                                     range(required_inaccessible_pokemon)]

        world.random.shuffle(inaccessible_pokemon_pool)

        def get_pokemon_from_pool(pool: list[str], blocklist: set[str] | None = None,
                                  exclude_unown: bool = False) -> str:
            pokemon = pool.pop()
            if exclude_unown and pokemon == "UNOWN" and not pool:
                pokemon = get_random_pokemon(world, exclude_unown=True, blocklist=global_blocklist)
            elif exclude_unown and pokemon == "UNOWN":
                pokemon = get_pokemon_from_pool(pool, exclude_unown=exclude_unown, blocklist=blocklist)
                pool.append("UNOWN")
                world.random.shuffle(pool)

            if blocklist and pokemon in blocklist:
                pokemon = get_random_pokemon(world, exclude_unown=exclude_unown, blocklist=blocklist | global_blocklist)
            return pokemon

        def randomize_encounter_list(region_key: EncounterKey, encounter_list: list[EncounterMon],
                                     exclude_unown=False) -> list[EncounterMon]:

            region_type = world.generated_wild_region_logic[region_key]
            if region_type is LogicalAccess.InLogic:
                pokemon_pool = logical_pokemon_pool
            elif region_type is LogicalAccess.OutOfLogic:
                pokemon_pool = accessible_pokemon_pool
            else:
                pokemon_pool = inaccessible_pokemon_pool

            new_encounters = list[EncounterMon]()
            if world.options.encounter_grouping.value == EncounterGrouping.option_one_per_method:
                pokemon = get_pokemon_from_pool(pokemon_pool, exclude_unown=exclude_unown)
                for encounter in encounter_list:
                    new_encounters.append(replace(encounter, pokemon=pokemon))

            elif world.options.encounter_grouping.value == EncounterGrouping.option_one_to_one:
                distribution = defaultdict[str, list[int]](lambda: [])
                new_encounters = [encounter for encounter in encounter_list]
                encounter_blocklist = set()
                for i, encounter in enumerate(encounter_list):
                    distribution[encounter.pokemon].append(i)
                for pokemon, slots in distribution.items():
                    pokemon = get_pokemon_from_pool(pokemon_pool, encounter_blocklist, exclude_unown=exclude_unown)
                    encounter_blocklist.add(pokemon)
                    for slot in slots:
                        new_encounters[slot] = replace(new_encounters[slot], pokemon=pokemon)
            else:
                encounter_blocklist = set()
                for encounter in encounter_list:
                    pokemon = get_pokemon_from_pool(pokemon_pool, encounter_blocklist, exclude_unown=exclude_unown)
                    encounter_blocklist.add(pokemon)
                    new_encounters.append(replace(encounter, pokemon=pokemon))

            if region_type is LogicalAccess.InLogic:
                world.logically_available_pokemon.update(encounter.pokemon for encounter in new_encounters)
            return new_encounters

        region_keys = list(world.generated_wild)
        world.random.shuffle(region_keys)
        for region_key in region_keys:
            encounters = world.generated_wild[region_key]
            world.generated_wild[region_key] = randomize_encounter_list(
                region_key, encounters,
                exclude_unown=region_key.encounter_type not in (EncounterType.Grass, EncounterType.Water))

        if logical_pokemon_pool: raise AssertionError(
            "Logical Pokemon pool is not empty, something went horribly wrong.")
        if accessible_pokemon_pool: raise AssertionError(
            "Accessible Pokemon pool is not empty, something went horribly wrong.")
        if inaccessible_pokemon_pool: raise AssertionError(
            "Inaccessible Pokemon pool is not empty, something went horribly wrong.")
    else:
        wild_pokemon = set()
        for region_key, wilds in world.generated_wild.items():
            if world.generated_wild_region_logic[region_key] is LogicalAccess.InLogic:
                wild_pokemon.update(wild.pokemon for wild in wilds)

        world.logically_available_pokemon.update()


def randomize_static_pokemon(world: "PokemonCrystalWorld"):
    if world.options.randomize_static_pokemon:
        blocklist = pokemon_convert_friendly_to_ids(world, world.options.static_blocklist)
        for static_name, pkmn_data in world.generated_static.items():
            priority_pokemon = {poke for poke, data in world.generated_pokemon.items() if
                                data.is_base} if pkmn_data.level_type == "giveegg" else None
            world.generated_static[static_name] = replace(
                world.generated_static[static_name],
                pokemon=get_random_pokemon(world,
                                           exclude_unown=True,
                                           priority_pokemon=priority_pokemon,
                                           blocklist=blocklist),
            )
    else:  # Still randomize the Odd Egg
        pokemon = world.random.choice(["PICHU", "CLEFFA", "IGGLYBUFF", "SMOOCHUM", "MAGBY", "ELEKID", "TYROGUE"])
        encounter_key = EncounterKey.static("OddEgg")
        world.generated_static[encounter_key] = replace(world.generated_static[encounter_key], pokemon=pokemon)

    world.logically_available_pokemon.update(
        static.pokemon for region_key, static in world.generated_static.items() if world.generated_wild_region_logic[
            region_key] is LogicalAccess.InLogic)
