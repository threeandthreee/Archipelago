from collections.abc import Iterable
from dataclasses import replace
from random import Random
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification
from .data import data as crystal_data, LogicalAccess, PokemonData, EncounterType
from .items import get_random_filler_item
from .moves import get_tmhm_compatibility, randomize_learnset, moves_convert_friendly_to_ids
from .options import RandomizeTypes, RandomizePalettes, RandomizeBaseStats, RandomizeStarters, RandomizeTrades, \
    DexsanityStarters, EncounterGrouping, BreedingMethodsRequired, RandomizePokemonRequests
from .utils import evolution_in_logic

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_pokemon_data(world: "PokemonCrystalWorld"):
    # follow_evolutions can change types after the pokemon has already been randomized,
    # so we randomize types before all else
    if world.options.randomize_types.value:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            evolution_line_list = [pkmn_name]
            if world.options.randomize_types.value == RandomizeTypes.option_follow_evolutions:
                # skip evolved pokemon if follow_evolutions
                if (not pkmn_data.is_base
                        and pkmn_name not in ("FLAREON", "JOLTEON", "VAPOREON", "ESPEON", "UMBREON")):
                    continue
                for evo in pkmn_data.evolutions:
                    evolution_line_list.append(evo.pokemon)
                    evo_poke = world.generated_pokemon[evo.pokemon]
                    for second_evo in evo_poke.evolutions:
                        evolution_line_list.append(second_evo.pokemon)

            new_types = get_random_types(world.random)
            for pokemon in evolution_line_list:
                world.generated_pokemon[pokemon] = replace(
                    world.generated_pokemon[pokemon],
                    types=new_types
                )

    move_blocklist = moves_convert_friendly_to_ids(world, world.options.move_blocklist)

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        new_base_stats = pkmn_data.base_stats
        new_learnset = pkmn_data.learnset
        new_tm_hms = pkmn_data.tm_hm

        if world.options.randomize_palettes.value:
            if world.options.randomize_palettes.value == RandomizePalettes.option_match_types:
                world.generated_palettes[pkmn_name] = get_type_colors(pkmn_data.types, world.random)
            else:
                world.generated_palettes[pkmn_name] = get_random_colors(world.random)

        if world.options.randomize_base_stats.value:
            if world.options.randomize_base_stats.value == RandomizeBaseStats.option_keep_bst:
                new_base_stats = get_random_base_stats(world.random, pkmn_data.bst)
            else:
                new_base_stats = get_random_base_stats(world.random)

        if world.options.randomize_learnsets or world.options.metronome_only:
            new_learnset = randomize_learnset(world, pkmn_name, move_blocklist)

        if world.options.tm_compatibility >= 0 or world.options.hm_compatibility >= 0:
            new_tm_hms = get_tmhm_compatibility(world, pkmn_name)

        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            tm_hm=new_tm_hms,
            learnset=new_learnset,
            base_stats=new_base_stats,
            bst=sum(new_base_stats)
        )


def randomize_starters(world: "PokemonCrystalWorld"):
    if not world.options.randomize_starters: return

    blocklist = pokemon_convert_friendly_to_ids(world, world.options.starter_blocklist.value)

    def get_starter_rival_fights(starter_name):
        return [(rival_name, rival) for rival_name, rival in world.generated_trainers.items() if
                rival_name.startswith("RIVAL_" + starter_name)]

    def set_rival_fight_starter(rival_name, rival, new_pokemon):
        # starter is always the last pokemon
        rival_pkmn = replace(rival.pokemon[-1], pokemon=new_pokemon)
        new_party = rival.pokemon[:-1] + [rival_pkmn]
        world.generated_trainers[rival_name] = replace(
            world.generated_trainers[rival_name],
            pokemon=new_party
        )

    base_only = world.options.randomize_starters.value == RandomizeStarters.option_unevolved_only
    for evo_line in world.generated_starters:
        # get all rival fights where the starter is unevolved
        rival_fights = get_starter_rival_fights(evo_line[0])
        # randomize starter
        starter_pokemon = get_random_pokemon(world, base_only=base_only, starter=True, exclude_unown=True,
                                             blocklist=blocklist)
        blocklist.add(starter_pokemon)
        starter_data = world.generated_pokemon[starter_pokemon]
        evo_line[0] = starter_pokemon
        # replace unevolved starter rival fights with new starter
        for trainer_name, trainer in rival_fights:
            set_rival_fight_starter(trainer_name, trainer, starter_pokemon)

        # get all rival fights where the starter is middle evolution
        rival_fights = get_starter_rival_fights(evo_line[1])
        # get random evolution of randomized starter
        middle_evo_pokemon = get_random_pokemon_evolution(world.random, starter_pokemon, starter_data)
        middle_data = world.generated_pokemon[middle_evo_pokemon]
        evo_line[1] = middle_evo_pokemon
        # replace middle evolution rival fights with new middle evolution
        for trainer_name, trainer in rival_fights:
            set_rival_fight_starter(trainer_name, trainer, middle_evo_pokemon)

        # get all rival fights where the starter is final evolution
        rival_fights = get_starter_rival_fights(evo_line[2])
        # get random evolution of randomized starter
        final_evo_pokemon = get_random_pokemon_evolution(world.random, middle_evo_pokemon, middle_data)
        evo_line[2] = final_evo_pokemon
        # replace final evolution rival fights with new final evolution
        for trainer_name, trainer in rival_fights:
            set_rival_fight_starter(trainer_name, trainer, final_evo_pokemon)

    new_helditems = (get_random_filler_item(world.random),
                     get_random_filler_item(world.random),
                     get_random_filler_item(world.random))

    world.generated_starter_helditems = new_helditems


def randomize_traded_pokemon(world: "PokemonCrystalWorld"):
    if not world.options.randomize_trades: return

    randomize_received = world.options.randomize_trades.value in (RandomizeTrades.option_received,
                                                                  RandomizeTrades.option_both)
    randomize_requested = world.options.randomize_trades.value in (RandomizeTrades.option_requested,
                                                                   RandomizeTrades.option_both)
    new_trades = []
    for trade in world.generated_trades:
        received_pokemon = get_random_pokemon(world) if randomize_received else trade.received_pokemon

        new_trades.append(
            replace(
                trade,
                requested_gender=0,  # no gender
                held_item=get_random_filler_item(world.random) if received_pokemon != "ABRA" else "TM_9",
                requested_pokemon=get_random_pokemon(world) if randomize_requested else trade.requested_pokemon,
                received_pokemon=received_pokemon
            )
        )

    world.generated_trades = new_trades


def randomize_requested_pokemon(world: "PokemonCrystalWorld"):
    if world.options.randomize_pokemon_requests in (RandomizePokemonRequests.option_items_and_pokemon,
                                                    RandomizePokemonRequests.option_pokemon):

        logically_available_pokemon = [pokemon for pokemon in world.logic.available_pokemon if pokemon != "UNOWN"]

        assert logically_available_pokemon
        while len(logically_available_pokemon) < len(world.generated_request_pokemon):
            logically_available_pokemon.append(world.random.choice(logically_available_pokemon))

        world.random.shuffle(logically_available_pokemon)
        world.generated_request_pokemon = [logically_available_pokemon.pop() for _ in world.generated_request_pokemon]
    elif world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
        # ideally we should never need this, but best to be safe
        logically_available_pokemon = [pokemon for pokemon in world.logic.available_pokemon if pokemon != "UNOWN"]

        world.generated_request_pokemon = [
            world.random.choice(logically_available_pokemon) if mon not in world.logic.available_pokemon else mon for
            mon in world.generated_request_pokemon]


def fill_wild_encounter_locations(world: "PokemonCrystalWorld"):
    if world.options.dexsanity_starters.value == DexsanityStarters.option_available_early:

        locations = world.multiworld.get_reachable_locations(world.multiworld.state, world.player)
        early_wild_regions = [loc.parent_region for loc in locations if "wild encounter" in loc.tags]
        early_wild_regions = [region for region in early_wild_regions if
                              world.logic.wild_regions[region.key] is LogicalAccess.InLogic
                              and region.key.encounter_type is not EncounterType.Static]
        early_wild_regions.sort(key=lambda region: region.name)
        world.random.shuffle(early_wild_regions)

        other_wild_regions = [loc.parent_region for loc in world.multiworld.get_locations(world.player) if
                              "wild encounter" in loc.tags
                              and loc.parent_region not in early_wild_regions
                              and world.logic.wild_regions[loc.parent_region.key] is LogicalAccess.InLogic
                              and loc.parent_region.key.encounter_type is not EncounterType.Static]
        other_wild_regions.sort(key=lambda region: region.name)
        world.random.shuffle(other_wild_regions)

        if early_wild_regions and other_wild_regions:

            for evo_line in world.generated_starters:

                if not early_wild_regions: continue
                starter = evo_line[0]
                source_region = None
                source_encounters = None

                if any(encounter
                       for region in early_wild_regions
                       for encounter in world.generated_wild[region.key]
                       if encounter.pokemon == starter):
                    continue

                for region in other_wild_regions:
                    source_encounters = world.generated_wild[region.key]
                    if starter in [encounter.pokemon for encounter in source_encounters]:
                        source_region = region
                        break

                if not source_region:  continue
                target_region = None
                target_encounters = None
                while not target_encounters:
                    if not early_wild_regions: break
                    target_region = early_wild_regions.pop()
                    target_encounters = world.generated_wild[target_region.key]

                if not target_encounters: continue

                if (world.options.encounter_grouping == EncounterGrouping.option_one_to_one
                        or not world.options.randomize_wilds):
                    pokemon_to_swap = target_encounters[0].pokemon
                    target_indexes = [i for i, enc in enumerate(target_encounters) if enc.pokemon == pokemon_to_swap]
                    source_indexes = [i for i, enc in enumerate(source_encounters) if enc.pokemon == starter]
                    for i in target_indexes:
                        target_encounters[i] = replace(target_encounters[i], pokemon=starter)
                    for i in source_indexes:
                        source_encounters[i] = replace(source_encounters[i], pokemon=pokemon_to_swap)
                elif world.options.encounter_grouping.value == EncounterGrouping.option_all_split:
                    starter_index = next(
                        i for i, encounter in enumerate(source_encounters) if encounter.pokemon == starter)
                    source_encounters[starter_index] = replace(source_encounters[starter_index],
                                                               pokemon=target_encounters[0].pokemon)
                    target_encounters[0] = replace(target_encounters[0], pokemon=starter)
                else:
                    pokemon_to_swap = target_encounters[0].pokemon
                    target_encounters = [replace(mon, pokemon=starter) for mon in target_encounters]
                    source_encounters = [replace(mon, pokemon=pokemon_to_swap) for mon in source_encounters]
                world.generated_wild[source_region.key] = source_encounters
                world.generated_wild[target_region.key] = target_encounters

    for region_key, encounters in world.generated_wild.items():
        if world.logic.wild_regions[region_key] is LogicalAccess.InLogic:
            seen_pokemon = set()
            for i, encounter in enumerate(encounters):
                location = world.get_location(f"{region_key.region_name()}_{i + 1}")
                location.place_locked_item(world.create_event(encounter.pokemon))
                if encounter.pokemon in seen_pokemon:
                    location.item.classification = ItemClassification.useful
                seen_pokemon.add(encounter.pokemon)

    for region_key, static in world.generated_static.items():
        if world.logic.wild_regions[region_key] is LogicalAccess.InLogic:
            location = world.get_location(f"{region_key.region_name()}_1")
            location.place_locked_item((world.create_event(static.pokemon)))


def generate_breeding_data(random_evolutions_dict: dict[str, str], world: "PokemonCrystalWorld"):
    if not world.options.breeding_methods_required: return

    def recursive_process_evolution(base: str, evo_pkmn: str):
        if evo_pkmn in world.logic.available_pokemon:
            evo_pkmn_data = world.generated_pokemon[evo_pkmn]
            if "EGG_NONE" in evo_pkmn_data.egg_groups or evo_pkmn_data.gender_ratio == "GENDER_UNKNOWN": return
            if (world.options.breeding_methods_required.value == BreedingMethodsRequired.option_any
                    and evo_pkmn_data.gender_ratio in ("GENDER_F100", "GENDER_F0")): return
            world.generated_breeding[base].add(evo_pkmn)

        for evos_evo in world.generated_pokemon[evo_pkmn].evolutions:
            recursive_process_evolution(base, evos_evo.pokemon)

    if random_evolutions_dict:
        potentially_reachable_bases = {v for v in random_evolutions_dict.values() if world.generated_pokemon[v].is_base}
    else:
        potentially_reachable_bases = {k for k, v in world.generated_pokemon.items() if v.is_base}

    for pokemon_id in potentially_reachable_bases:
        for evolution in world.generated_pokemon[pokemon_id].evolutions:
            recursive_process_evolution(pokemon_id, evolution.pokemon)

    world.logic.available_pokemon.update(world.generated_breeding.keys())


def generate_evolution_data(world: "PokemonCrystalWorld"):
    evolution_pokemon = set()

    def recursive_evolution_add(evolving_pokemon):
        for evo in world.generated_pokemon[evolving_pokemon].evolutions:
            if evolution_in_logic(world, evo) and evo.pokemon not in evolution_pokemon:
                evolution_pokemon.add(evo.pokemon)
                recursive_evolution_add(evo.pokemon)
        return

    for pokemon in world.logic.available_pokemon:
        recursive_evolution_add(pokemon)

    world.logic.available_pokemon.update(evolution_pokemon)


def get_random_pokemon(world: "PokemonCrystalWorld", priority_pokemon: set[str] | None = None, types=None,
                       base_only=False, force_fully_evolved_at=None, current_level=None, starter=False,
                       exclude_unown=False, blocklist: set[str] | None = None):
    bst_range = world.options.starters_bst_average * .10

    def filter_out_pokemon(pkmn_name, pkmn_data):

        if blocklist and pkmn_name in blocklist:
            return True

        if exclude_unown and pkmn_name == "UNOWN":
            return True

        # If types are passed in, filter out Pokemon that do not match it
        if types is not None:
            if types[0] not in pkmn_data.types and types[-1] not in pkmn_data.types:
                return True

        # Exclude evolved Pokemon when we only want base ones
        if base_only and not pkmn_data.is_base:
            return True

        # If we have a level to force fully evolved at and the current level of the pokemon is passed in,
        # exlude Pokemon with evolutions from the list if the level is greater or equal than forced_fully_evolved
        if force_fully_evolved_at and current_level is not None:
            if current_level >= force_fully_evolved_at and pkmn_data.evolutions:
                return True

        # if this is a starter and the starter option is first stage can evolve, filter Pokemon that are not base
        if starter and world.options.randomize_starters == RandomizeStarters.option_first_stage_can_evolve and not pkmn_data.is_base:
            return True

        # if this is a starter and the starter option is first stage can evolve, filter Pokemon that cannot evolve
        if starter and world.options.randomize_starters == RandomizeStarters.option_first_stage_can_evolve and pkmn_data.evolutions == []:
            return True

        # if this is a starter and the starter option is base stat mode, filter Pokemon that are
        if starter and world.options.randomize_starters == RandomizeStarters.option_base_stat_mode:
            if abs(pkmn_data.bst - world.options.starters_bst_average) >= bst_range:
                return True

        return False

    if priority_pokemon:
        pokemon_pool = [pkmn_name for pkmn_name in priority_pokemon if
                        not filter_out_pokemon(pkmn_name, world.generated_pokemon[pkmn_name])]
    else:
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in world.generated_pokemon.items()
                        if not filter_out_pokemon(pkmn_name, pkmn_data)]

    # If there are no Pokemon left and this is bst mode, increase the range and try again
    if not pokemon_pool and starter and world.options.randomize_starters == RandomizeStarters.option_base_stat_mode:
        bst_range += world.options.starters_bst_average * .10
        pokemon_pool = [pkmn_name for pkmn_name, pkmn_data in world.generated_pokemon.items()
                        if not filter_out_pokemon(pkmn_name, pkmn_data)]

    # If there's no Pokemon left, give up and shove everything back in, it can happen in some very rare edge cases
    if not pokemon_pool:
        pokemon_pool = [pkmn_name for pkmn_name, _ in world.generated_pokemon.items() if
                        (not exclude_unown or pkmn_name != "UNOWN")]

    return world.random.choice(pokemon_pool)


def get_random_nezumi(random):
    # 🐁
    pokemon_pool = ["RATTATA", "RATICATE", "NIDORAN_F", "NIDORAN_M", "NIDORINA", "NIDORINO", "PIKACHU", "RAICHU",
                    "SANDSHREW", "SANDSLASH", "CYNDAQUIL", "QUILAVA", "SENTRET", "FURRET", "MARILL"]
    return random.choice(pokemon_pool)


def get_random_pokemon_evolution(random: Random, pkmn_name: str, pkmn_data: PokemonData):
    # if the Pokemon has no evolutions
    if not pkmn_data.evolutions:
        # return the same Pokemon
        return pkmn_name
    return random.choice(pkmn_data.evolutions).pokemon


def pokemon_convert_friendly_to_ids(world: "PokemonCrystalWorld", pokemon: Iterable[str]) -> set[str]:
    if not pokemon: return set()

    pokemon = set(pokemon)
    if "_Legendaries" in pokemon:
        pokemon.discard("_Legendaries")
        pokemon.update({"Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Entei", "Raikou", "Suicune", "Celebi",
                        "Lugia", "Ho-Oh"})

    pokemon_ids = {pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                   pokemon_data.friendly_name in pokemon}

    return pokemon_ids


def can_breed(world: "PokemonCrystalWorld", parent: str) -> bool:
    data = world.generated_pokemon[parent]
    if "EGG_DITTO" in data.egg_groups or "EGG_NONE" in data.egg_groups: return False
    return True


def _locations_to_pokemon(world: "PokemonCrystalWorld", locations: Iterable[str]):
    pokemon = set()
    for location in locations:
        parts = location.split("- ")
        if len(parts) != 2: continue
        if "Catch" in parts[1]: continue
        pokemon.add(parts[1])
    return pokemon_convert_friendly_to_ids(world, pokemon)


def get_priority_dexsanity(world: "PokemonCrystalWorld") -> set[str]:
    return _locations_to_pokemon(world, world.options.priority_locations.value)


def get_excluded_dexsanity(world: "PokemonCrystalWorld") -> set[str]:
    return _locations_to_pokemon(world, world.options.exclude_locations.value)


def get_random_base_stats(random, bst=None):
    if bst is None:
        # sunkern to mewtwo
        bst = random.randint(180, 680)
    # add 0.5 to prevent a single stat exceeding 255
    # biggest possible variance on max bst is (1.5 * 680) / 4 = 255
    randoms = [random.random() + 0.5 for _i in range(0, 6)]
    total = sum(randoms)
    return [int((stat * bst) / total) for stat in randoms]


def get_random_types(random):
    new_types = [random.choice(crystal_data.types)]
    # approx. 110/251 Pokemon are dual type in gen 2
    if random.randint(0, 24) < 11:
        new_types.append(random.choice([t for t in crystal_data.types if t not in new_types]))
    return new_types


def add_hm_compatibility(world: "PokemonCrystalWorld", pokemon_id: str, hm: str):
    pokemon_data = world.generated_pokemon[pokemon_id]
    world.generated_pokemon[pokemon_id] = replace(pokemon_data, tm_hm=[hm] + list(pokemon_data.tm_hm))
    world.logic.add_hm_compatible_pokemon(hm, pokemon_id)


# palettes stuff
def get_random_colors(random):
    return [
        c for _ in range(4)
        for c in convert_color(random.randint(0, 31), random.randint(0, 31), random.randint(0, 31))
    ]


def get_type_colors(types, random):
    type1 = types[0]
    type2 = types[-1]

    c1 = type_palettes[type1][0]
    c2 = type_palettes[type2][1]

    r1, g1, b1 = shift_color(c1[0], c1[1], c1[2], random)
    r2, g2, b2 = shift_color(c2[0], c2[1], c2[2], random)

    # normal colors
    color1 = convert_color(r1, g1, b1)
    color2 = convert_color(r2, g2, b2)

    # invert colors for shiny palette
    color3 = convert_color(31 - r1, 31 - g1, 31 - b1)
    color4 = convert_color(31 - r2, 31 - g2, 31 - b2)
    return list(color1 + color2 + color3 + color4)


def shift_color(r: int, g: int, b: int, random):
    return r + random.randint(-1, 1), \
           g + random.randint(-1, 1), \
           b + random.randint(-1, 1)


def convert_color(r: int, g: int, b: int):
    r = max(0, min(r, 31))
    g = max(0, min(g, 31))
    b = max(0, min(b, 31))

    color = (b << 10) | (g << 5) | r
    return color.to_bytes(2, "little")


type_palettes = {
    "NORMAL": [[31, 27, 31], [31, 24, 30]],
    "FIGHTING": [[30, 17, 1], [24, 9, 0]],
    "FLYING": [[17, 21, 31], [15, 11, 28]],
    "POISON": [[27, 21, 31], [15, 10, 24]],
    "GROUND": [[28, 19, 13], [24, 14, 0]],
    "ROCK": [[21, 20, 22], [18, 15, 4]],
    "BUG": [[23, 25, 6], [16, 18, 4]],
    "GHOST": [[10, 8, 14], [5, 3, 15]],
    "STEEL": [[19, 19, 21], [12, 14, 13]],
    "FIRE": [[31, 7, 0], [31, 15, 0]],
    "WATER": [[5, 8, 31], [2, 4, 26]],
    "GRASS": [[8, 31, 5], [4, 24, 2]],
    "ELECTRIC": [[31, 23, 7], [31, 17, 0]],
    "PSYCHIC_TYPE": [[31, 14, 30], [24, 4, 14]],
    "ICE": [[17, 25, 30], [22, 27, 30]],
    "DRAGON": [[16, 20, 25], [9, 12, 23]],
    "DARK": [[4, 2, 7], [3, 2, 6]],
}
