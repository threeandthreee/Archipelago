import re
from typing import TYPE_CHECKING, Dict, List
from BaseClasses import CollectionState
from .data import data, EvolutionMethodEnum
from .options import (PokemonFRLGOptions, CeruleanCaveRequirement, EliteFourRequirement, FlashRequired,
                      PewterCityRoadblock, Route22GateRequirement, Route23GuardRequirement, SeviiIslandPasses,
                      ViridianCityRoadblock, ViridianGymRequirement)

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


badge_requirements: Dict[str, str] = {
    "Cut": "Cascade Badge",
    "Fly": "Thunder Badge",
    "Surf": "Soul Badge",
    "Strength": "Rainbow Badge",
    "Flash": "Boulder Badge",
    "Rock Smash": "Marsh Badge",
    "Waterfall": "Volcano Badge"
}

island_passes: Dict[int, List[str]] = {
    1: ["Tri Pass", "One Pass"],
    2: ["Tri Pass", "Two Pass"],
    3: ["Tri Pass", "Three Pass"],
    4: ["Rainbow Pass", "Four Pass"],
    5: ["Rainbow Pass", "Five Pass"],
    6: ["Rainbow Pass", "Six Pass"],
    7: ["Rainbow Pass", "Seven Pass"]
}


def has_badge_requirement(state: CollectionState, player: int, options: PokemonFRLGOptions, hm: str):
    return hm in options.remove_badge_requirement.value or state.has(badge_requirements[hm], player)


def can_use_hm(state: CollectionState, player: int, world: "PokemonFRLGWorld", hm: str):
    return state.has_any(world.hm_compatibility[hm], player)


def can_cut(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM01 Cut", player) and
            has_badge_requirement(state, player, world.options, "Cut")
            and can_use_hm(state, player, world, "Cut"))


def can_fly(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM02 Fly", player) and
            has_badge_requirement(state, player, world.options, "Fly")
            and can_use_hm(state, player, world, "Fly"))


def can_surf(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM03 Surf", player) and
            has_badge_requirement(state, player, world.options, "Surf")
            and can_use_hm(state, player, world, "Surf"))


def can_strength(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM04 Strength", player) and
            has_badge_requirement(state, player, world.options, "Strength")
            and can_use_hm(state, player, world, "Strength"))


def can_flash(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM05 Flash", player) and
            has_badge_requirement(state, player, world.options, "Flash")
            and can_use_hm(state, player, world, "Flash"))


def can_rock_smash(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM06 Rock Smash", player) and
            has_badge_requirement(state, player, world.options, "Rock Smash")
            and can_use_hm(state, player, world, "Rock Smash"))


def can_waterfall(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    return (state.has("HM07 Waterfall", player) and
            has_badge_requirement(state, player, world.options, "Waterfall")
            and can_use_hm(state, player, world, "Waterfall"))


def has_n_badges(state: CollectionState, player: int, n: int):
    badges = ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge",
              "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"]
    return sum([state.has(badge, player) for badge in badges]) >= n


def has_n_gyms(state: CollectionState, player: int, n: int):
    gyms = ["Defeat Brock", "Defeat Misty", "Defeat Lt. Surge", "Defeat Erika",
            "Defeat Koga", "Defeat Sabrina", "Defeat Blaine", "Defeat Giovanni"]
    return sum([state.has(gym, player) for gym in gyms]) >= n


def has_n_pokemon(state: CollectionState, player: int, n: int):
    count = 0
    for species in data.species.values():
        if state.has(species.name, player) or state.has(f"Static {species.name}", player):
            count += 1
        if count >= n:
            return True
    return False


def has_pokemon(state: CollectionState, player: int, pokemon: str):
    return state.has_any([pokemon, f"Static {pokemon}"], player)


def can_leave_viridian(state: CollectionState, player: int, options: PokemonFRLGOptions):
    if options.viridian_city_roadblock != ViridianCityRoadblock.option_open:
        return state.has("Deliver Oak's Parcel", player)
    return True


def can_enter_viridian_gym(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.viridian_gym_requirement
    count = options.viridian_gym_count.value
    if requirement == ViridianGymRequirement.option_badges:
        return has_n_badges(state, player, count)
    elif requirement == ViridianGymRequirement.option_gyms:
        return has_n_gyms(state, player, count)


def can_pass_route_22_gate(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.route22_gate_requirement
    count = options.route22_gate_count.value
    if requirement == Route22GateRequirement.option_badges:
        return has_n_badges(state, player, count)
    elif requirement == Route22GateRequirement.option_gyms:
        return has_n_gyms(state, player, count)


def can_leave_pewter(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.pewter_city_roadblock
    if requirement == PewterCityRoadblock.option_brock:
        return state.has("Defeat Brock", player)
    elif requirement == PewterCityRoadblock.option_any_gym:
        return has_n_gyms(state, player, 1)
    elif requirement == PewterCityRoadblock.option_boulder_badge:
        return state.has("Boulder Badge", player)
    elif requirement == PewterCityRoadblock.option_any_badge:
        return has_n_badges(state, player, 1)
    return True


def can_leave_cerulean(state: CollectionState, player: int, options: PokemonFRLGOptions):
    if "Remove Cerulean Roadblocks" in options.modify_world_state.value:
        return True
    return state.has("Help Bill", player)


def can_enter_cerulean_cave(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.cerulean_cave_requirement
    count = options.cerulean_cave_count.value
    if requirement == CeruleanCaveRequirement.option_vanilla:
        return state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], player)
    elif requirement == CeruleanCaveRequirement.option_champion:
        return state.has("Defeat Champion", player)
    elif requirement == CeruleanCaveRequirement.option_restore_network:
        return state.has("Restore Pokemon Network Machine", player)
    elif requirement == CeruleanCaveRequirement.option_badges:
        return has_n_badges(state, player, count)
    elif requirement == CeruleanCaveRequirement.option_gyms:
        return has_n_gyms(state, player, count)


def can_navigate_dark_caves(state: CollectionState, player: int, world: "PokemonFRLGWorld"):
    if world.options.flash_required != FlashRequired.option_off:
        return can_flash(state, player, world)
    return True


def can_enter_silph(state: CollectionState, player: int, options: PokemonFRLGOptions):
    if "Open Silph" in options.modify_world_state.value:
        return True
    return state.has("Rescue Mr. Fuji", player)


def can_open_silph_door(state: CollectionState, player: int, floor: int):
    return (state.has_any(["Card Key", f"Card Key {floor}F"], player) or
            state.has("Progressive Card Key", player, floor - 1))


def saffron_rockets_gone(state: CollectionState, player: int, options: PokemonFRLGOptions):
    if "Remove Saffron Rockets" in options.modify_world_state.value:
        return True
    return state.has("Liberate Silph Co.", player)


def can_pass_route_23_guard(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.route23_guard_requirement
    count = options.route23_guard_count.value
    if requirement == Route23GuardRequirement.option_badges:
        return has_n_badges(state, player, count)
    elif requirement == Route23GuardRequirement.option_gyms:
        return has_n_gyms(state, player, count)


def can_challenge_elite_four(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.elite_four_requirement
    count = options.elite_four_count.value
    if requirement == EliteFourRequirement.option_badges:
        return has_n_badges(state, player, count)
    elif requirement == EliteFourRequirement.option_gyms:
        return has_n_gyms(state, player, count)


def can_challenge_elite_four_rematch(state: CollectionState, player: int, options: PokemonFRLGOptions):
    requirement = options.elite_four_requirement
    count = options.elite_four_rematch_count.value
    if state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], player):
        if requirement == EliteFourRequirement.option_badges:
            return has_n_badges(state, player, count)
        elif requirement == EliteFourRequirement.option_gyms:
            return has_n_gyms(state, player, count)
    return False


def can_sail_vermilion(state: CollectionState, player: int, options: PokemonFRLGOptions):
    if "Block Vermilion Sailing" not in options.modify_world_state.value:
        return True
    return state.has("S.S. Ticket", player)


def can_sail_island(state: CollectionState, player: int, options: PokemonFRLGOptions, island: int):
    if (options.island_passes == SeviiIslandPasses.option_vanilla or
            options.island_passes == SeviiIslandPasses.option_progressive):
        progressive_passes = [1, 1, 1, 2, 2, 2, 2]
    else:
        progressive_passes = [1, 2, 3, 4, 5, 6, 7]
    return (state.has_any(island_passes[island], player) or
            state.has("Progressive Pass", player, progressive_passes[island - 1]))


def post_game_gossipers(state: CollectionState, player: int, options: PokemonFRLGOptions):
    if "Early Gossipers" in options.modify_world_state.value:
        return True
    return state.has("Defeat Champion", player)


def can_evolve(state: CollectionState, player: int, world: "PokemonFRLGWorld", pokemon: str):
    evolution_data = data.evolutions[pokemon]
    pokemon = re.sub(r'\d+', '', pokemon)
    if state.has(pokemon, player):
        if evolution_data.method == EvolutionMethodEnum.ITEM:
            return state.has(world.item_id_to_name[evolution_data.param], player)
        elif evolution_data.method == EvolutionMethodEnum.ITEM_HELD:
            return state.has_all([world.item_id_to_name[evolution_data.param],
                                  world.item_id_to_name[evolution_data.param2]],
                                 player)
        elif evolution_data.method == EvolutionMethodEnum.FRIENDSHIP:
            return has_n_gyms(state, player, 4)
        else:
            return has_n_gyms(state, player, evolution_data.param / 7)
    return False
