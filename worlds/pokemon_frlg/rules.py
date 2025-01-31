"""
Logic rule definitions for Pokémon FireRed and LeafGreen
"""
import re
from typing import TYPE_CHECKING, Dict, List
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .data import data, EvolutionMethodEnum, NATIONAL_ID_TO_SPECIES_ID, NUM_REAL_SPECIES
from .items import offset_item_value
from .locations import PokemonFRLGLocation
from .options import (CeruleanCaveRequirement, Dexsanity, EliteFourRequirement, FlashRequired, GameVersion, Goal,
                      ItemfinderRequired, LevelScaling, PewterCityRoadblock, Route22GateRequirement,
                      Route23GuardRequirement, SeviiIslandPasses, ShuffleHiddenItems, ShuffleRunningShoes,
                      Trainersanity, ViridianCityRoadblock, ViridianGymRequirement)

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


def set_rules(world: "PokemonFRLGWorld") -> None:
    player = world.player
    options = world.options
    multiworld = world.multiworld

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

    def has_badge_requirement(hm: str, state: CollectionState):
        return hm in options.remove_badge_requirement.value or state.has(badge_requirements[hm], player)

    def can_cut(state: CollectionState):
        return (state.has("HM01 Cut", player)
                and has_badge_requirement("Cut", state)
                and can_use_hm(state, "Cut"))

    def can_fly(state: CollectionState):
        return (state.has("HM02 Fly", player)
                and has_badge_requirement("Fly", state)
                and can_use_hm(state, "Fly"))

    def can_surf(state: CollectionState):
        return (state.has("HM03 Surf", player)
                and has_badge_requirement("Surf", state)
                and can_use_hm(state, "Surf"))

    def can_strength(state: CollectionState):
        return (state.has("HM04 Strength", player)
                and has_badge_requirement("Strength", state)
                and can_use_hm(state, "Strength"))

    def can_flash(state: CollectionState):
        return (state.has("HM05 Flash", player)
                and has_badge_requirement("Flash", state)
                and can_use_hm(state, "Flash"))

    def can_rock_smash(state: CollectionState):
        return (state.has("HM06 Rock Smash", player)
                and has_badge_requirement("Rock Smash", state)
                and can_use_hm(state, "Rock Smash"))

    def can_waterfall(state: CollectionState):
        return (state.has("HM07 Waterfall", player)
                and has_badge_requirement("Waterfall", state)
                and can_use_hm(state, "Waterfall"))

    def can_use_hm(state: CollectionState, hm: str):
        species_can_use_hm: List[str] = world.hm_compatibility[hm]
        return state.has_any(species_can_use_hm, player)

    def has_n_badges(state: CollectionState, n: int):
        return sum([state.has(badge, player) for badge in [
            "Boulder Badge",
            "Cascade Badge",
            "Thunder Badge",
            "Rainbow Badge",
            "Soul Badge",
            "Marsh Badge",
            "Volcano Badge",
            "Earth Badge"
        ]]) >= n

    def has_n_gyms(state: CollectionState, n: int):
        return sum([state.has(gym, player) for gym in [
            "Defeat Brock",
            "Defeat Misty",
            "Defeat Lt. Surge",
            "Defeat Erika",
            "Defeat Koga",
            "Defeat Sabrina",
            "Defeat Blaine",
            "Defeat Giovanni"
        ]]) >= n

    def has_n_pokemon(state: CollectionState, n: int):
        count = 0
        for species in data.species.values():
            if state.has(species.name, player):
                count += 1
            elif state.has(f"Static {species.name}", player):
                count += 1
            if count >= n:
                return True
        return False

    def has_pokemon(state: CollectionState, pokemon: str):
        return state.has_any([pokemon, f"Static {pokemon}"], player)

    def can_pass_viridian_city_roadblock(state: CollectionState):
        if options.viridian_city_roadblock != ViridianCityRoadblock.option_open:
            return state.has("Deliver Oak's Parcel", player)
        return True

    def can_enter_viridian_gym(state: CollectionState):
        requirement = options.viridian_gym_requirement
        count = options.viridian_gym_count.value
        if requirement == ViridianGymRequirement.option_badges:
            return has_n_badges(state, count)
        elif requirement == ViridianGymRequirement.option_gyms:
            return has_n_gyms(state, count)

    def can_pass_route_22_gate(state: CollectionState):
        requirement = options.route22_gate_requirement
        count = options.route22_gate_count.value
        if requirement == Route22GateRequirement.option_badges:
            return has_n_badges(state, count)
        elif requirement == Route22GateRequirement.option_gyms:
            return has_n_gyms(state, count)

    def can_pass_pewter_city_roadblock(state: CollectionState):
        requirement = options.pewter_city_roadblock
        if requirement == PewterCityRoadblock.option_brock:
            return state.has("Defeat Brock", player)
        elif requirement == PewterCityRoadblock.option_any_gym:
            return has_n_gyms(state, 1)
        elif requirement == PewterCityRoadblock.option_boulder_badge:
            return state.has("Boulder Badge", player)
        elif requirement == PewterCityRoadblock.option_any_badge:
            return has_n_badges(state, 1)
        return True

    def can_pass_cerulean_city_roadblocks(state: CollectionState):
        if "Remove Cerulean Roadblocks" in options.modify_world_state.value:
            return True
        return state.has("Help Bill", player)

    def can_enter_cerulean_cave(state: CollectionState):
        requirement = options.cerulean_cave_requirement
        count = options.cerulean_cave_count.value
        if requirement == CeruleanCaveRequirement.option_vanilla:
            return state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], player)
        elif requirement == CeruleanCaveRequirement.option_champion:
            return state.has("Defeat Champion", player)
        elif requirement == CeruleanCaveRequirement.option_restore_network:
            return state.has("Restore Pokemon Network Machine", player)
        elif requirement == CeruleanCaveRequirement.option_badges:
            return has_n_badges(state, count)
        elif requirement == CeruleanCaveRequirement.option_gyms:
            return has_n_gyms(state, count)

    def dark_cave(state: CollectionState):
        if options.flash_required != FlashRequired.option_off:
            return can_flash(state)
        return True

    def silph_open(state: CollectionState):
        if "Open Silph" in options.modify_world_state.value:
            return True
        return state.has("Rescue Mr. Fuji", player)

    def saffron_rockets_gone(state: CollectionState):
        if "Remove Saffron Rockets" in options.modify_world_state.value:
            return True
        return state.has("Liberate Silph Co.", player)

    def can_pass_route_23_guard(state: CollectionState):
        requirement = options.route23_guard_requirement
        count = options.route23_guard_count.value
        if requirement == Route23GuardRequirement.option_badges:
            return has_n_badges(state, count)
        elif requirement == Route23GuardRequirement.option_gyms:
            return has_n_gyms(state, count)

    def can_challenge_elite_four(state: CollectionState):
        requirement = options.elite_four_requirement
        count = options.elite_four_count.value
        if requirement == EliteFourRequirement.option_badges:
            return has_n_badges(state, count)
        elif requirement == EliteFourRequirement.option_gyms:
            return has_n_gyms(state, count)

    def can_challenge_elite_four_rematch(state: CollectionState):
        requirement = options.elite_four_requirement
        count = options.elite_four_rematch_count.value
        if state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], player):
            if requirement == EliteFourRequirement.option_badges:
                return has_n_badges(state, count)
            elif requirement == EliteFourRequirement.option_gyms:
                return has_n_gyms(state, count)
        return False

    def can_evolve(state: CollectionState, pokemon: str):
        evolution_data = data.evolutions[pokemon]
        pokemon = re.sub(r'\d+', '', pokemon)
        if state.has(pokemon, player):
            if evolution_data.method == EvolutionMethodEnum.ITEM:
                return state.has(world.item_id_to_name[offset_item_value(evolution_data.param)], player)
            elif evolution_data.method == EvolutionMethodEnum.FRIENDSHIP:
                return has_n_gyms(state, 4)
            else:
                return has_n_gyms(state, evolution_data.param / 7)
        return False

    def can_open_silph_door(floor: int, state: CollectionState):
        return (state.has_any(["Card Key", f"Card Key {floor}F"], player) or
                state.has("Progressive Card Key", player, floor - 1))

    def can_sail_island(island: int, state: CollectionState):
        progressives_needed = {
            1: (1, 1),
            2: (1, 2),
            3: (1, 3),
            4: (2, 4),
            5: (2, 5),
            6: (2, 6),
            7: (2, 7)
        }
        if options.island_passes.value in [SeviiIslandPasses.option_vanilla, SeviiIslandPasses.option_progressive]:
            progressives_count = progressives_needed[island][0]
        else:
            progressives_count = progressives_needed[island][1]
        return state.has_any(island_passes[island], player) or state.has("Progressive Pass", player, progressives_count)

    def post_game_gossipers(state: CollectionState):
        if "Early Gossipers" in options.modify_world_state.value:
            return True
        return state.has("Defeat Champion", player)

    def sail_vermilion(state: CollectionState):
        if "Block Vermilion Sailing" not in options.modify_world_state.value:
            return True
        return state.has("S.S. Ticket", player)

    def get_entrance(entrance: str):
        return multiworld.get_entrance(entrance, player)

    def get_location(location: str):
        return multiworld.get_location(location, player)

    def set_kanto_rules():
        if options.goal == Goal.option_elite_four:
            multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion", player)
        elif options.goal == Goal.option_elite_four_rematch:
            multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion (Rematch)", player)

        # Sky
        set_rule(get_entrance("Flying"), lambda state: can_fly(state))
        set_rule(get_entrance("Pallet Town Fly Destination"), lambda state: state.has("Fly Pallet Town", player))
        set_rule(get_entrance("Viridian City Fly Destination"), lambda state: state.has("Fly Viridian City", player))
        set_rule(get_entrance("Pewter City Fly Destination"), lambda state: state.has("Fly Pewter City", player))
        set_rule(get_entrance("Route 4 Fly Destination"), lambda state: state.has("Fly Route 4", player))
        set_rule(get_entrance("Cerulean City Fly Destination"), lambda state: state.has("Fly Cerulean City", player))
        set_rule(get_entrance("Vermilion City Fly Destination"), lambda state: state.has("Fly Vermilion City", player))
        set_rule(get_entrance("Route 10 Fly Destination"), lambda state: state.has("Fly Route 10", player))
        set_rule(get_entrance("Lavender Town Fly Destination"), lambda state: state.has("Fly Lavender Town", player))
        set_rule(get_entrance("Celadon City Fly Destination"), lambda state: state.has("Fly Celadon City", player))
        set_rule(get_entrance("Fuchsia City Fly Destination"), lambda state: state.has("Fly Fuchsia City", player))
        set_rule(get_entrance("Saffron City Fly Destination"), lambda state: state.has("Fly Saffron City", player))
        set_rule(get_entrance("Cinnabar Island Fly Destination"),
                 lambda state: state.has("Fly Cinnabar Island", player))
        set_rule(get_entrance("Indigo Plateau Fly Destination"), lambda state: state.has("Fly Indigo Plateau", player))

        # Seagallop
        set_rule(get_entrance("Vermilion City Arrival"), lambda state: sail_vermilion(state))
        set_rule(get_entrance("Navel Rock Arrival"),
                 lambda state: state.has("Mystic Ticket", player) and state.can_reach_region("Vermilion City", player))
        set_rule(get_entrance("Birth Island Arrival"),
                 lambda state: state.has("Aurora Ticket", player) and state.can_reach_region("Vermilion City", player))

        # Pallet Town
        set_rule(get_location("Rival's House - Daisy Gift"), lambda state: state.has("Deliver Oak's Parcel", player))
        set_rule(get_location("Professor Oak's Lab - Oak Gift (Deliver Parcel)"),
                 lambda state: state.has("Oak's Parcel", player))
        set_rule(get_location("Professor Oak's Lab - Oak Gift (Post Route 22 Rival)"),
                 lambda state: state.has("Defeat Route 22 Rival", player))
        set_rule(get_location("Professor Oak's Lab - Oak's Delivery"), lambda state: state.has("Oak's Parcel", player))
        set_rule(get_entrance("Pallet Town Surfing Spot"), lambda state: can_surf(state))

        # Viridian City
        set_rule(get_location("Viridian City - Old Man Gift"), lambda state: can_pass_viridian_city_roadblock(state))
        set_rule(get_entrance("Viridian City South Roadblock"),
                 lambda state: can_pass_viridian_city_roadblock(state) or can_cut(state))
        set_rule(get_entrance("Viridian City South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Viridian Gym"), lambda state: can_enter_viridian_gym(state))

        # Route 22
        set_rule(get_location("Route 22 - Early Rival Battle"), lambda state: state.has("Deliver Oak's Parcel", player))
        set_rule(get_entrance("Route 22 Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 22 Gate Exit (North)"), lambda state: can_pass_route_22_gate(state))

        # Route 2
        set_rule(get_location("Route 2 Gate - Oak's Aide Gift (Pokedex Progress)"),
                 lambda state: has_n_pokemon(state, options.oaks_aide_route_2.value))
        set_rule(get_location("Route 2 Trade House - Trade Abra"), lambda state: state.has("Abra", player))
        set_rule(get_entrance("Route 2 Southwest Cuttable Trees"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 2 East Cuttable Tree"), lambda state: can_cut(state))

        if "Modify Route 2" in options.modify_world_state.value:
            set_rule(get_entrance("Route 2 Northwest Smashable Rock"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 2 Northeast Smashable Rock"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 2 Northeast Cuttable Tree"), lambda state: can_cut(state))
        else:
            set_rule(get_entrance("Route 2 Northwest Cuttable Tree"), lambda state: can_cut(state))
            set_rule(get_entrance("Route 2 Northeast Cuttable Tree (North)"), lambda state: can_cut(state))
            set_rule(get_entrance("Route 2 Northeast Cuttable Tree (South)"), lambda state: can_cut(state))

        # Pewter City
        if options.shuffle_running_shoes != ShuffleRunningShoes.option_vanilla:
            set_rule(get_location("Pewter City - Gift from Mom"),
                     lambda state: state.has("Defeat Brock", player) and state.can_reach_region("Route 3", player))
        set_rule(get_entrance("Pewter City Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Pewter City Exit (East)"), lambda state: can_pass_pewter_city_roadblock(state))

        # Mt. Moon
        if "Mt. Moon" in options.additional_dark_caves.value:
            set_rule(get_entrance("Mt. Moon 1F Leave South Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon 1F Leave Center-Right Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon 1F Leave Center-Left Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon 1F Leave Northwest Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave First Tunnel Northeast Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave First Tunnel Southeast Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave Second Tunnel East Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave Second Tunnel West Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave Third Tunnel Northwest Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave Third Tunnel Southeast Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave Fourth Tunnel West Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B1F Leave Fourth Tunnel East Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B2F Leave South Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B2F Leave Northeast Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B2F Leave Center Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Mt. Moon B2F Leave Northwest Entry"), lambda state: dark_cave(state))

            for i in range(1, 5):
                set_rule(get_location(f"Mt. Moon 1F - Land Encounter {i}"), lambda state: dark_cave(state))
                set_rule(get_location(f"Mt. Moon B2F - Land Encounter {i}"), lambda state: dark_cave(state))
                if (options.flash_required == FlashRequired.option_required and
                        options.level_scaling != LevelScaling.option_off):
                    set_rule(get_location(f"Mt. Moon 1F Land Scaling {i}"), lambda state: dark_cave(state))
                    set_rule(get_location(f"Mt. Moon B2F Land Scaling {i}"), lambda state: dark_cave(state))

            set_rule(get_location("Mt. Moon B1F - Land Encounter 1"), lambda state: dark_cave(state))
            if (options.flash_required == FlashRequired.option_required and
                    options.level_scaling != LevelScaling.option_off):
                set_rule(get_location("Mt. Moon B1F Land Scaling 1"), lambda state: dark_cave(state))

        # Cerulean City
        set_rule(get_location("Bike Shop - Bicycle Purchase"), lambda state: state.has("Bike Voucher", player))
        set_rule(get_location("Cerulean Trade House - Trade Poliwhirl"), lambda state: state.has("Poliwhirl", player))
        set_rule(get_entrance("Cerulean City Cuttable Tree"),
                 lambda state: can_pass_cerulean_city_roadblocks(state) and can_cut(state))
        set_rule(get_entrance("Robbed House (Front)"), lambda state: can_pass_cerulean_city_roadblocks(state))
        set_rule(get_entrance("Cerulean City Outskirts Exit (East)"), lambda state: can_cut(state))
        set_rule(get_entrance("Cerulean City Near Cave Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Cerulean Cave"), lambda state: can_enter_cerulean_cave(state))

        if "Modify Route 9" in options.modify_world_state.value:
            set_rule(get_entrance("Cerulean City Outskirts Exit (East)"), lambda state: can_rock_smash(state))
        else:
            set_rule(get_entrance("Cerulean City Outskirts Exit (East)"), lambda state: can_cut(state))

        # Route 24
        set_rule(get_entrance("Route 24 Surfing Spot"), lambda state: can_surf(state))

        # Route 25
        set_rule(get_location("Route 25 - Item Near Bush"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 25 Surfing Spot"), lambda state: can_surf(state))

        # Route 5
        set_rule(get_entrance("Route 5 Gate North Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Blue Tea"], player))
        set_rule(get_entrance("Route 5 Gate South Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Blue Tea"], player))

        if "Block Tunnels" in options.modify_world_state.value:
            set_rule(get_entrance("Route 5 Smashable Rocks"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 5 Near Tunnel Smashable Rocks"), lambda state: can_rock_smash(state))

        # Underground Path North-South Tunnel
        if options.game_version == GameVersion.option_firered:
            set_rule(get_location("Underground Path North Entrance - Trade Nidoran M"),
                     lambda state: state.has("Nidoran M", player))
        elif options.game_version == GameVersion.option_leafgreen:
            set_rule(get_location("Underground Path North Entrance - Trade Nidoran F"),
                     lambda state: state.has("Nidoran F", player))

        # Route 6
        set_rule(get_entrance("Route 6 Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 6 Gate South Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Red Tea"], player))
        set_rule(get_entrance("Route 6 Gate North Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Red Tea"], player))

        if "Block Tunnels" in options.modify_world_state.value:
            set_rule(get_entrance("Route 6 Smashable Rocks"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 6 Near Tunnel Smashable Rocks"), lambda state: can_rock_smash(state))

        # Vermilion City
        set_rule(get_location("Vermilion Trade House - Trade Spearow"), lambda state: state.has("Spearow", player))
        set_rule(get_entrance("Vermilion City Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Vermilion City Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Vermilion City Near Gym Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Vermilion City Near Gym Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Vermilion Harbor"), lambda state: state.has("S.S. Ticket", player))

        # S.S. Anne
        set_rule(get_entrance("S.S. Anne Exterior Surfing Spot"), lambda state: can_surf(state))

        # Route 11
        set_rule(get_location("Route 11 Gate 2F - Oak's Aide Gift (Pokedex Progress)"),
                 lambda state: has_n_pokemon(state, options.oaks_aide_route_11.value))
        set_rule(get_entrance("Route 11 West Surfing Spot"), lambda state: can_surf(state))

        if "Route 12 Boulders" in options.modify_world_state.value:
            set_rule(get_entrance("Route 11 East Exit"), lambda state: can_strength(state))

        if options.game_version == GameVersion.option_firered:
            set_rule(get_location("Route 11 Gate 2F - Trade Nidorino"), lambda state: state.has("Nidorino", player))
        elif options.game_version == GameVersion.option_leafgreen:
            set_rule(get_location("Route 11 Gate 2F - Trade Nidorina"), lambda state: state.has("Nidorina", player))

        # Diglett's Cave
        if "Diglett's Cave" in options.additional_dark_caves.value:
            set_rule(get_entrance("Diglett's Cave B1F Leave Northwest Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Diglett's Cave B1F Leave Southeast Entry"), lambda state: dark_cave(state))

            for i in range(1, 3):
                set_rule(get_location(f"Diglett's Cave B1F - Land Encounter {i}"), lambda state: dark_cave(state))
                if (options.flash_required == FlashRequired.option_required and
                        options.level_scaling != LevelScaling.option_off):
                    set_rule(get_location(f"Diglett's Cave B1F Land Scaling {i}"), lambda state: dark_cave(state))

        # Route 9
        if "Modify Route 9" in options.modify_world_state.value:
            set_rule(get_entrance("Route 9 Exit (West)"), lambda state: can_rock_smash(state))
        else:
            set_rule(get_entrance("Route 9 Exit (West)"), lambda state: can_cut(state))

        # Route 10
        set_rule(get_location("Route 10 Pokemon Center 1F - Oak's Aide Gift (Pokedex Progress)"),
                 lambda state: has_n_pokemon(state, options.oaks_aide_route_10.value))
        set_rule(get_entrance("Route 10 North Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 10 Near Power Plant Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Power Plant (Front)"),
                 lambda state: state.has("Machine Part", player) or not options.extra_key_items)
        set_rule(get_entrance("Route 10 Waterfall Drop"), lambda state: can_waterfall(state))
        set_rule(get_entrance("Route 10 Waterfall Ascend"), lambda state: can_waterfall(state))

        if "Modify Route 10" in options.modify_world_state.value:
            set_rule(get_entrance("Route 10 South Surfing Spot"), lambda state: can_surf(state))
        else:
            set_rule(get_entrance("Route 10 South Surfing Spot"), lambda state: False)
            set_rule(get_entrance("Route 10 South Landing"), lambda state: False)
            set_rule(get_entrance("Route 10 South (Fishing Battle)"), lambda state: False)

        # Rock Tunnel
        set_rule(get_entrance("Rock Tunnel 1F Leave Northeast Entry (Northeast)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel 1F Leave Northeast Entry (Northwest)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel 1F Leave Northwest Entry (Northwest)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel 1F Leave Northwest Entry (East)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel 1F Leave South Entry (Northeast)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel 1F Leave South Entry (South)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel B1F Leave Southeast Entry (Southeast)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel B1F Leave Southeast Entry (Northeast)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel B1F Leave Northwest Entry (East)"), lambda state: dark_cave(state))
        set_rule(get_entrance("Rock Tunnel B1F Leave Northwest Entry (Northwest)"), lambda state: dark_cave(state))

        for i in range(1, 6):
            set_rule(get_location(f"Rock Tunnel 1F - Land Encounter {i}"), lambda state: dark_cave(state))
            set_rule(get_location(f"Rock Tunnel B1F - Land Encounter {i}"), lambda state: dark_cave(state))
            if (options.flash_required == FlashRequired.option_required and
                    options.level_scaling != LevelScaling.option_off):
                set_rule(get_location(f"Rock Tunnel 1F Land Scaling {i}"), lambda state: dark_cave(state))
                set_rule(get_location(f"Rock Tunnel B1F Land Scaling {i}"), lambda state: dark_cave(state))

        # Lavender Town
        set_rule(get_location("Volunteer Pokemon House - Mr. Fuji Gift"),
                 lambda state: state.has("Rescue Mr. Fuji", player))

        if "Route 12 Boulders" in options.modify_world_state.value:
            set_rule(get_entrance("Lavender Town Exit (South)"), lambda state: can_strength(state))

        # Route 8
        set_rule(get_entrance("Route 8 Cuttable Trees"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 8 Gate East Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Purple Tea"], player))
        set_rule(get_entrance("Route 8 Gate West Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Purple Tea"], player))

        if "Block Tunnels" in options.modify_world_state.value:
            set_rule(get_entrance("Route 8 Smashable Rocks"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 8 Near Tunnel Smashable Rocks"), lambda state: can_rock_smash(state))

        # Route 7
        set_rule(get_entrance("Route 7 Gate West Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Green Tea"], player))
        set_rule(get_entrance("Route 7 Gate East Guard Checkpoint"),
                 lambda state: state.has_any(["Tea", "Green Tea"], player))

        if "Block Tunnels" in options.modify_world_state.value:
            set_rule(get_entrance("Route 7 Smashable Rocks"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 7 Near Tunnel Smashable Rocks"), lambda state: can_rock_smash(state))

        # Celadon City
        set_rule(get_location("Celadon Game Corner - Fisherman Gift"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - Scientist Gift"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - Gentleman Gift"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner Prize Room - Prize Pokemon 1"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner Prize Room - Prize Pokemon 2"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner Prize Room - Prize Pokemon 3"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner Prize Room - Prize Pokemon 4"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner Prize Room - Prize Pokemon 5"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_entrance("Celadon City Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Celadon City Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Celadon City Near Gym Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Rocket Hideout"),
                 lambda state: state.has("Hideout Key", player) or not options.extra_key_items)
        set_rule(get_entrance("Celadon Gym Cuttable Trees"), lambda state: can_cut(state))

        # Rocket Hideout
        set_rule(get_entrance("Rocket Hideout Elevator B1F Stop"), lambda state: state.has("Lift Key", player))
        set_rule(get_entrance("Rocket Hideout Elevator B2F Stop"), lambda state: state.has("Lift Key", player))
        set_rule(get_entrance("Rocket Hideout Elevator B4F Stop"), lambda state: state.has("Lift Key", player))

        # Pokemon Tower
        set_rule(get_entrance("Pokemon Tower 6F (Ghost Battle)"), lambda state: state.has("Silph Scope", player))
        set_rule(get_entrance("Pokemon Tower 6F Near Stairs (Ghost Battle)"),
                 lambda state: state.has("Silph Scope", player))
        set_rule(get_entrance("Pokemon Tower 6F Reveal Ghost"), lambda state: state.has("Silph Scope", player))

        if "Block Tower" in options.modify_world_state.value:
            set_rule(get_entrance("Pokemon Tower 1F (Ghost Battle)"), lambda state: state.has("Silph Scope", player))
            set_rule(get_entrance("Pokemon Tower 1F Near Stairs (Ghost Battle)"),
                     lambda state: state.has("Silph Scope", player))
            set_rule(get_entrance("Pokemon Tower 1F Reveal Ghost"), lambda state: state.has("Silph Scope", player))
        else:
            set_rule(get_entrance("Pokemon Tower 1F (Ghost Battle)"), lambda state: False)
            set_rule(get_entrance("Pokemon Tower 1F Near Stairs (Ghost Battle)"), lambda state: False)

        for i in range(3, 8):
            for j in range(1, 4):
                set_rule(get_location(f"Pokemon Tower {i}F - Land Encounter {j}"),
                         lambda state: state.has("Silph Scope", player))

        # Route 12
        set_rule(get_entrance("Route 12 West Play Poke Flute"), lambda state: state.has("Poke Flute", player))
        set_rule(get_entrance("Route 12 North Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 12 Center Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 12 Center Play Poke Flute"), lambda state: state.has("Poke Flute", player))
        set_rule(get_entrance("Route 12 South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 12 South Cuttable Tree (North)"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 12 South Cuttable Tree (South)"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 12 South Play Poke Flute"), lambda state: state.has("Poke Flute", player))

        if "Route 12 Boulders" in options.modify_world_state.value:
            set_rule(get_entrance("Route 12 West Exit"), lambda state: can_strength(state))
            set_rule(get_entrance("Route 12 North Exit"), lambda state: can_strength(state))
            set_rule(get_entrance("Route 12 South Exit"), lambda state: can_strength(state))

        if "Modify Route 12" in options.modify_world_state.value:
            set_rule(get_entrance("Route 12 Center Water Unobstructed Path"), lambda state: False)
            set_rule(get_entrance("Route 12 South Water Unobstructed Path"), lambda state: False)

        # Route 13
        set_rule(get_entrance("Route 13 Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 13 Cuttable Tree"), lambda state: can_cut(state))

        if "Route 12 Boulders" in options.modify_world_state.value:
            set_rule(get_entrance("Route 13 Exit (East)"), lambda state: can_strength(state))

        # Route 14
        set_rule(get_entrance("Route 14 Cuttable Tree (North)"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 14 Cuttable Tree (South)"), lambda state: can_cut(state))

        # Route 15
        set_rule(get_location("Route 15 Gate 2F - Oak's Aide Gift (Pokedex Progress)"),
                 lambda state: has_n_pokemon(state, options.oaks_aide_route_15.value))

        # Route 16
        set_rule(get_location("Route 16 Gate 2F - Oak's Aide Gift (Pokedex Progress)"),
                 lambda state: has_n_pokemon(state, options.oaks_aide_route_16.value))
        set_rule(get_entrance("Route 16 Southeast Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 16 Southeast Play Poke Flute"), lambda state: state.has("Poke Flute", player))
        set_rule(get_entrance("Route 16 Northeast Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Route 16 Center Play Poke Flute"), lambda state: state.has("Poke Flute", player))
        set_rule(get_entrance("Route 16 Gate 1F Southeast Bike Checkpoint"), lambda state: state.has("Bicycle", player))

        if "Modify Route 16" in options.modify_world_state.value:
            set_rule(get_entrance("Route 16 Northeast Smashable Rock"), lambda state: can_rock_smash(state))
            set_rule(get_entrance("Route 16 Center Smashable Rock"), lambda state: can_rock_smash(state))
        else:
            set_rule(get_entrance("Route 16 Northeast Smashable Rock"), lambda state: False)
            set_rule(get_entrance("Route 16 Center Smashable Rock"), lambda state: False)

        # Route 18
        set_rule(get_entrance("Route 18 Gate 1F East Bike Checkpoint"), lambda state: state.has("Bicycle", player))

        if options.game_version == GameVersion.option_firered:
            set_rule(get_location("Route 18 Gate 2F - Trade Golduck"), lambda state: state.has("Golduck", player))
        elif options.game_version == GameVersion.option_leafgreen:
            set_rule(get_location("Route 18 Gate 2F - Trade Slowbro"), lambda state: state.has("Slowbro", player))

        # Fuchsia City
        set_rule(get_location("Safari Zone Warden's House - Warden Gift (Return Teeth)"),
                 lambda state: state.has("Gold Teeth", player))
        set_rule(get_location("Safari Zone Warden's House - Item"), lambda state: can_strength(state))
        set_rule(get_entrance("Fuchsia City Backyard Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone"),
                 lambda state: state.has("Safari Pass", player) or not options.extra_key_items)

        # Safari Zone
        set_rule(get_entrance("Safari Zone Center Area South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone Center Area Northwest Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone Center Area Northeast Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone East Area Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone North Area Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone West Area North Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Safari Zone West Area South Surfing Spot"), lambda state: can_surf(state))

        # Saffron City
        set_rule(get_entrance("Silph Co."), lambda state: silph_open(state) or saffron_rockets_gone(state))
        set_rule(get_entrance("Copycat's House"), lambda state: saffron_rockets_gone(state))
        set_rule(get_entrance("Saffron Gym"), lambda state: saffron_rockets_gone(state))
        set_rule(get_entrance("Saffron Pidgey House"), lambda state: saffron_rockets_gone(state))

        # Silph Co.
        set_rule(get_entrance("Silph Co. 2F Barrier (Northwest)"), lambda state: can_open_silph_door(2, state))
        set_rule(get_entrance("Silph Co. 2F Barrier (Southwest)"), lambda state: can_open_silph_door(2, state))
        set_rule(get_entrance("Silph Co. 2F Northwest Room Barrier"), lambda state: can_open_silph_door(2, state))
        set_rule(get_entrance("Silph Co. 2F Southwest Room Barrier"), lambda state: can_open_silph_door(2, state))
        set_rule(get_entrance("Silph Co. 3F Barrier"), lambda state: can_open_silph_door(3, state))
        set_rule(get_entrance("Silph Co. 3F Center Room Barrier (East)"),
                 lambda state: can_open_silph_door(3, state))
        set_rule(get_entrance("Silph Co. 3F Center Room Barrier (West)"),
                 lambda state: can_open_silph_door(3, state))
        set_rule(get_entrance("Silph Co. 3F West Room Barrier"), lambda state: can_open_silph_door(3, state))
        set_rule(get_entrance("Silph Co. 4F Barrier (West)"), lambda state: can_open_silph_door(4, state))
        set_rule(get_entrance("Silph Co. 4F Barrier (Center)"), lambda state: can_open_silph_door(4, state))
        set_rule(get_entrance("Silph Co. 4F North Room Barrier"), lambda state: can_open_silph_door(4, state))
        set_rule(get_entrance("Silph Co. 5F Barrier (Northwest)"), lambda state: can_open_silph_door(5, state))
        set_rule(get_entrance("Silph Co. 5F Barrier (Center)"), lambda state: can_open_silph_door(5, state))
        set_rule(get_entrance("Silph Co. 5F Barrier (Southwest)"), lambda state: can_open_silph_door(5, state))
        set_rule(get_entrance("Silph Co. 5F Southwest Room Barrier"), lambda state: can_open_silph_door(5, state))
        set_rule(get_entrance("Silph Co. 6F Barrier"), lambda state: can_open_silph_door(6, state))
        set_rule(get_entrance("Silph Co. 7F Barrier (Center)"), lambda state: can_open_silph_door(7, state))
        set_rule(get_entrance("Silph Co. 7F Barrier (East)"), lambda state: can_open_silph_door(7, state))
        set_rule(get_entrance("Silph Co. 7F East Room Barrier (North)"),
                 lambda state: can_open_silph_door(7, state))
        set_rule(get_entrance("Silph Co. 7F East Room Barrier (South)"),
                 lambda state: can_open_silph_door(7, state))
        set_rule(get_entrance("Silph Co. 7F Southeast Room Barrier"), lambda state: can_open_silph_door(7, state))
        set_rule(get_entrance("Silph Co. 8F Barrier"), lambda state: can_open_silph_door(8, state))
        set_rule(get_entrance("Silph Co. 8F West Room Barrier"), lambda state: can_open_silph_door(8, state))
        set_rule(get_entrance("Silph Co. 9F Barrier"), lambda state: can_open_silph_door(9, state))
        set_rule(get_entrance("Silph Co. 9F Northwest Room Barrier"), lambda state: can_open_silph_door(9, state))
        set_rule(get_entrance("Silph Co. 9F Southwest Room Barrier (East)"),
                 lambda state: can_open_silph_door(9, state))
        set_rule(get_entrance("Silph Co. 9F Southwest Room Barrier (West)"),
                 lambda state: can_open_silph_door(9, state))
        set_rule(get_entrance("Silph Co. 10F Barrier"), lambda state: can_open_silph_door(10, state))
        set_rule(get_entrance("Silph Co. 10F Southeast Room Barrier"),
                 lambda state: can_open_silph_door(10, state))
        set_rule(get_entrance("Silph Co. 11F West Barrier"), lambda state: can_open_silph_door(11, state))

        # Route 19
        set_rule(get_entrance("Route 19 Surfing Spot"), lambda state: can_surf(state))

        # Route 20
        set_rule(get_entrance("Route 20 Near North Cave Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 20 Near South Cave Surfing Spot"), lambda state: can_surf(state))

        # Seafoam Islands
        set_rule(get_entrance("Seafoam Islands B3F West Surfing Spot"),
                 lambda state: can_surf(state) and can_strength(state) and
                               state.can_reach_region("Seafoam Islands 1F", player))
        set_rule(get_entrance("Seafoam Islands B3F Southeast Surfing Spot"),
                 lambda state: can_surf(state) and can_strength(state) and
                               state.can_reach_region("Seafoam Islands 1F", player))
        set_rule(get_entrance("Seafoam Islands B3F West Landing"),
                 lambda state: can_strength(state) and state.can_reach_region("Seafoam Islands 1F", player))
        set_rule(get_entrance("Seafoam Islands B3F Southeast Landing"),
                 lambda state: can_strength(state) and state.can_reach_region("Seafoam Islands 1F", player))
        set_rule(get_entrance("Seafoam Islands B4F Surfing Spot (West)"),
                 lambda state: can_surf(state) and can_strength(state) and
                               state.can_reach_region("Seafoam Islands B3F West", player))
        set_rule(get_entrance("Seafoam Islands B4F Near Articuno Landing"),
                 lambda state: can_strength(state) and state.can_reach_region("Seafoam Islands B3F West", player))

        for i in range(1, 6):
            set_rule(get_location(f"Seafoam Islands B3F - Water Encounter {i}"),
                     lambda state: can_strength(state) and state.can_reach_region("Seafoam Islands 1F", player))

        # Cinnabar Island
        set_rule(get_location("Pokemon Lab Lounge - Trade Raichu"), lambda state: state.has("Raichu", player))
        set_rule(get_location("Pokemon Lab Lounge - Trade Venonat"), lambda state: state.has("Venonat", player))
        set_rule(get_location("Pokemon Lab Experiment Room - Revive Helix Fossil"),
                 lambda state: state.has("Helix Fossil", player))
        set_rule(get_location("Pokemon Lab Experiment Room - Revive Dome Fossil"),
                 lambda state: state.has("Dome Fossil", player))
        set_rule(get_location("Pokemon Lab Experiment Room - Revive Old Amber"),
                 lambda state: state.has("Old Amber", player))
        set_rule(get_location("Pokemon Lab Experiment Room - Trade Ponyta"),
                 lambda state: state.has("Ponyta", player))
        set_rule(get_entrance("Cinnabar Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Cinnabar Gym"), lambda state: state.has("Secret Key", player))
        set_rule(get_entrance("Pokemon Mansion"),
                 lambda state: state.has("Letter", player) or not options.extra_key_items)

        # Route 23
        set_rule(get_entrance("Route 23 South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 23 Near Water Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Route 23 Center Guard Checkpoint"), lambda state: can_pass_route_23_guard(state))

        if "Route 23 Trees" in options.modify_world_state.value:
            set_rule(get_entrance("Route 23 Near Water Cuttable Trees"), lambda state: can_cut(state))
            set_rule(get_entrance("Route 23 Center Cuttable Trees"), lambda state: can_cut(state))

        if "Modify Route 23" in options.modify_world_state.value:
            set_rule(get_entrance("Route 23 Waterfall Ascend"), lambda state: can_waterfall(state))
            set_rule(get_entrance("Route 23 Waterfall Drop"), lambda state: can_waterfall(state))

        # Victory Road
        set_rule(get_location("Victory Road 1F - North Item (Left)"), lambda state: can_strength(state))
        set_rule(get_location("Victory Road 1F - North Item (Right)"), lambda state: can_strength(state))
        set_rule(get_entrance("Victory Road 1F North Strength Boulder"), lambda state: can_strength(state))
        set_rule(get_entrance("Victory Road 2F Center Rock Barrier"),
                 lambda state: can_strength(state) and state.can_reach_region("Victory Road 3F Southwest", player))
        set_rule(get_entrance("Victory Road 2F Northwest Strength Boulder"), lambda state: can_strength(state))
        set_rule(get_entrance("Victory Road 3F Southwest Strength Boulder"), lambda state: can_strength(state))
        set_rule(get_entrance("Victory Road 3F Southeast Strength Boulder"), lambda state: can_strength(state))

        if "Victory Road Rocks" in options.modify_world_state.value:
            set_rule(get_entrance("Victory Road 1F South Rock Barrier"),
                     lambda state: can_strength(state) and can_rock_smash(state))
            set_rule(get_entrance("Victory Road 2F Southwest Rock Barrier"),
                     lambda state: can_strength(state) and can_rock_smash(state))
            set_rule(get_entrance("Victory Road 3F North Rock Barrier"),
                     lambda state: can_strength(state) and can_rock_smash(state))
        else:
            set_rule(get_entrance("Victory Road 1F South Rock Barrier"), lambda state: can_strength(state))
            set_rule(get_entrance("Victory Road 2F Southwest Rock Barrier"), lambda state: can_strength(state))
            set_rule(get_entrance("Victory Road 3F North Rock Barrier"), lambda state: can_strength(state))

        if "Victory Road" in options.additional_dark_caves.value:
            set_rule(get_entrance("Victory Road 1F Leave South Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 1F Leave North Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 2F Leave Southwest Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 2F Leave Center Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 2F Leave Northwest Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 2F Leave Southeast Entry"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 2F Leave East Entry (West)"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 2F Leave East Entry (East)"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 3F Leave North Entry (West)"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 3F Leave North Entry (East)"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 3F Leave Southeast Entry (North)"), lambda state: dark_cave(state))
            set_rule(get_entrance("Victory Road 3F Leave Southeast Entry (South)"), lambda state: dark_cave(state))

            for i in range(1, 9):
                set_rule(get_location(f"Victory Road 1F - Land Encounter {i}"), lambda state: dark_cave(state))
                set_rule(get_location(f"Victory Road 2F - Land Encounter {i}"), lambda state: dark_cave(state))
                set_rule(get_location(f"Victory Road 3F - Land Encounter {i}"), lambda state: dark_cave(state))
                if (options.flash_required == FlashRequired.option_required and
                        options.level_scaling != LevelScaling.option_off):
                    set_rule(get_location(f"Victory Road 1F Land Scaling {i}"), lambda state: dark_cave(state))
                    set_rule(get_location(f"Victory Road 2F Land Scaling {i}"), lambda state: dark_cave(state))
                    set_rule(get_location(f"Victory Road 3F Land Scaling {i}"), lambda state: dark_cave(state))

            set_rule(get_location("Victory Road 2F - Land Encounter 9"), lambda state: dark_cave(state))
            if (options.flash_required == FlashRequired.option_required and
                    options.level_scaling != LevelScaling.option_off):
                set_rule(get_location("Victory Road 2F Land Scaling 9"), lambda state: dark_cave(state))

        # Indigo Plateau
        set_rule(get_entrance("Pokemon League"), lambda state: can_challenge_elite_four(state))

        # Cerulean Cave
        set_rule(get_location("Cerulean Cave 2F - East Item"), lambda state: can_rock_smash(state))
        set_rule(get_location("Cerulean Cave 2F - West Item"), lambda state: can_rock_smash(state))
        set_rule(get_location("Cerulean Cave 2F - Center Item"), lambda state: can_rock_smash(state))
        set_rule(get_entrance("Cerulean Cave 1F Southeast Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Cerulean Cave 1F Northeast Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Cerulean Cave 1F Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Cerulean Cave B1F Surfing Spot"), lambda state: can_surf(state))

        # Navel Rock
        set_rule(get_entrance("Navel Rock Seagallop"), lambda state: sail_vermilion(state))

        # Birth Island
        set_rule(get_entrance("Birth Island Seagallop"), lambda state: sail_vermilion(state))

        # Evolutions
        for location in multiworld.get_locations(player):
            assert isinstance(location, PokemonFRLGLocation)
            if location.tags is not None and "Evolution" in location.tags:
                pokemon_name = location.name.split("-")[1].strip()
                set_rule(get_location(location.name), lambda state, pokemon=pokemon_name: can_evolve(state, pokemon))

    def set_hidden_item_rules():
        # Viridian Gym
        set_rule(get_location("Viridian Gym - Hidden Item Under Giovanni"),
                 lambda state: state.has("Itemfinder", player))

        # Route 10
        set_rule(get_location("Route 10 - Hidden Item Behind Cuttable Tree"), lambda state: can_cut(state))

        # Celadon City
        set_rule(get_location("Celadon Game Corner - Northwest Hidden Item"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - North Hidden Item (Left)"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - North Hidden Item (Right)"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - Northeast Hidden Item"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - West Hidden Item"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - Center Hidden Item"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - East Hidden Item (Left)"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - East Hidden Item (Right)"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - Southwest Hidden Item"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - South Hidden Item (Left)"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - South Hidden Item (Right)"),
                 lambda state: state.has("Coin Case", player))
        set_rule(get_location("Celadon Game Corner - Southeast Hidden Item"),
                 lambda state: state.has("Coin Case", player))

        # Pokemon Tower
        set_rule(get_location("Pokemon Tower 7F - Hidden Item Under Mr. Fuji"),
                 lambda state: state.has("Itemfinder", player))

        # Route 12
        set_rule(get_location("Route 12 - Hidden Item Under Snorlax"), lambda state: state.has("Itemfinder", player))

        # Route 16
        set_rule(get_location("Route 16 - Hidden Item Under Snorlax"), lambda state: state.has("Itemfinder", player))

        # Navel Rock
        set_rule(get_location("Navel Rock - Hidden Item Near Ho-Oh"), lambda state: state.has("Itemfinder", player))

        # Add rules for hidden items
        if world.options.itemfinder_required != ItemfinderRequired.option_off:
            for location in multiworld.get_locations(player):
                assert isinstance(location, PokemonFRLGLocation)
                if location.tags is not None and "Hidden" in location.tags:
                    add_rule(location, lambda state: state.has("Itemfinder", player))

    def set_extra_key_item_rules():
        # Cerulean City
        set_rule(get_location("Cerulean Gym - Hidden Item in Water"),
                 lambda state: can_surf(state) and state.has("Itemfinder", player))

    def set_trainersanity_rules():
        # Route 22
        set_rule(get_location("Route 22 - Early Rival Reward"), lambda state: state.has("Deliver Oak's Parcel", player))
        set_rule(get_location("Route 22 - Late Rival Reward"),
                 lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player))

    def set_dexsanity_rules():
        for i in range(NUM_REAL_SPECIES):
            species = data.species[NATIONAL_ID_TO_SPECIES_ID[i + 1]]
            set_rule(get_location(f"Pokedex - {species.name}"),
                     lambda state, pokemon=species.name: has_pokemon(state, pokemon))

    def set_famesanity_rules():
        # Pallet Town
        set_rule(get_location("Professor Oak's Lab - Oak's Aide M Info (Right)"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Professor Oak's Lab - Oak Info"),
                 lambda state: state.has("Oak's Parcel", player))
        set_rule(get_location("Professor Oak's Lab - Oak's Aide M Info (Left)"),
                 lambda state: post_game_gossipers(state))

        # Viridian City
        set_rule(get_location("Viridian Gym - Gym Guy Info"),
                 lambda state: state.has("Defeat Giovanni", player))

        # Cerulean City
        set_rule(get_location("Cerulean Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state))

        # Vermilion City
        set_rule(get_location("Pokemon Fan Club - Worker Info"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Vermilion Pokemon Center 1F - Bookshelf Info"),
                 lambda state: state.has("Defeat Lt. Surge", player))

        # Lavender Town
        set_rule(get_location("Lavender Pokemon Center 1F - Balding Man Info"),
                 lambda state: post_game_gossipers(state))

        # Celadon City
        set_rule(get_location("Celadon Condominiums 1F - Tea Woman Info"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Celadon Condominiums 2F - Bookshelf Info"),
                 lambda state: state.has("Defeat Erika", player))
        set_rule(get_location("Celadon Department Store 2F - Woman Info"),
                 lambda state: post_game_gossipers(state))

        # Fuchsia City
        set_rule(get_location("Fuchsia City - Koga's Daughter Info"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("FuchSafari Zone Warden's House - Bookshelf Info"),
                 lambda state: state.has("Defeat Koga", player))

        # Saffron City
        set_rule(get_location("Pokemon Trainer Fan Club - Bookshelf Info"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Saffron City - Battle Girl Info"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Saffron Pokemon Center 1F - Bookshelf Info"),
                 lambda state: state.has("Defeat Sabrina", player))

        # Cinnabar Island
        set_rule(get_location("Cinnabar Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state))

        # Indigo Plateau
        set_rule(get_location("Indigo Plateau Pokemon Center 1F - Black Belt Info 1"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Indigo Plateau Pokemon Center 1F - Black Belt Info 2"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Indigo Plateau Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state))
        set_rule(get_location("Indigo Plateau Pokemon Center 1F - Cooltrainer Info"),
                 lambda state: post_game_gossipers(state))

        # Add rules for fame checker locations
        if world.options.fame_checker_required:
            for location in multiworld.get_locations(player):
                assert isinstance(location, PokemonFRLGLocation)
                if location.tags is not None and ("FameChecker" in location.tags):
                    add_rule(location, lambda state: state.has("Fame Checker", player))

    def set_pokemon_request_rules():
        # Route 12
        set_rule(get_location("Route 12 Fishing House - Fishing Guru Gift (Show Magikarp)"),
                 lambda state: state.has("Magikarp", player))

    def set_split_tea_rules():
        # Celadon City
        set_rule(get_location("Celadon Condominiums 1F - Brock"),
                 lambda state: state.has("Defeat Brock", player))
        set_rule(get_location("Celadon Condominiums 1F - Misty"),
                 lambda state: state.has("Defeat Misty", player))
        set_rule(get_location("Celadon Condominiums 1F - Erika"),
                 lambda state: state.has("Defeat Erika", player))

    def set_scaling_rules():
        # Route 22
        set_rule(get_location("Route 22 Early Rival"), lambda state: state.has("Deliver Oak's Parcel", player))
        set_rule(get_location("Route 22 Late Rival"),
                 lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player))

        # Celadon City
        set_rule(get_location("Prize Pokemon 1"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Prize Pokemon 2"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Prize Pokemon 3"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Prize Pokemon 4"), lambda state: state.has("Coin Case", player))
        set_rule(get_location("Prize Pokemon 5"), lambda state: state.has("Coin Case", player))

        # Cinnabar Island
        set_rule(get_location("Gift Omanyte"), lambda state: state.has("Helix Fossil", player))
        set_rule(get_location("Gift Kabuto"), lambda state: state.has("Dome Fossil", player))
        set_rule(get_location("Gift Aerodactyl"), lambda state: state.has("Old Amber", player))

    def set_sevii_rules():
        # Sky
        set_rule(get_entrance("One Island Fly Destination"), lambda state: state.has("Fly One Island", player))
        set_rule(get_entrance("Two Island Fly Destination"), lambda state: state.has("Fly Two Island", player))
        set_rule(get_entrance("Three Island Fly Destination"), lambda state: state.has("Fly Three Island", player))
        set_rule(get_entrance("Four Island Fly Destination"), lambda state: state.has("Fly Four Island", player))
        set_rule(get_entrance("Five Island Fly Destination"), lambda state: state.has("Fly Five Island", player))
        set_rule(get_entrance("Six Island Fly Destination"), lambda state: state.has("Fly Six Island", player))
        set_rule(get_entrance("Seven Island Fly Destination"), lambda state: state.has("Fly Seven Island", player))

        # Seagallop
        set_rule(get_entrance("One Island Arrival"), lambda state: can_sail_island(1, state))
        set_rule(get_entrance("Two Island Arrival"), lambda state: can_sail_island(2, state))
        set_rule(get_entrance("Three Island Arrival"), lambda state: can_sail_island(3, state))
        set_rule(get_entrance("Four Island Arrival"), lambda state: can_sail_island(4, state))
        set_rule(get_entrance("Five Island Arrival"), lambda state: can_sail_island(5, state))
        set_rule(get_entrance("Six Island Arrival"), lambda state: can_sail_island(6, state))
        set_rule(get_entrance("Seven Island Arrival"), lambda state: can_sail_island(7, state))

        # Cinnabar Island
        set_rule(get_entrance("Follow Bill"), lambda state: state.has("Defeat Blaine", player))

        # One Island Town
        set_rule(get_location("One Island Pokemon Center 1F - Celio Gift (Deliver Ruby)"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby"], player))
        set_rule(get_location("One Island Pokemon Center 1F - Help Celio"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"],
                                             player))
        set_rule(get_entrance("One Island Town Surfing Spot"), lambda state: can_surf(state))

        # Kindle Road
        set_rule(get_location("Kindle Road - Plateau Item"), lambda state: can_rock_smash(state))
        set_rule(get_location("Kindle Road - Item Behind Smashable Rock"), lambda state: can_rock_smash(state))
        set_rule(get_entrance("Kindle Road South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Kindle Road Center Surfing Spot (South)"), lambda state: can_surf(state))
        set_rule(get_entrance("Kindle Road Center Surfing Spot (North)"), lambda state: can_surf(state))
        set_rule(get_entrance("Kindle Road North Surfing Spot"), lambda state: can_surf(state))

        # Mt. Ember
        set_rule(get_location("Mt. Ember Exterior - Item Near Summit"),
                 lambda state: can_strength(state) and can_rock_smash(state))
        set_rule(get_location("Mt. Ember Exterior - Eavesdrop on Team Rocket Grunts"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(get_location("Mt. Ember Summit - Legendary Pokemon"), lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Exterior South Strength Boulders"), lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path"), lambda state: state.has("Deliver Meteorite", player))
        set_rule(get_entrance("Mt. Ember Ruby Path B2F West Strength Boulders"), lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B2F East Strength Boulders"), lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southwest)"),
                 lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southeast)"),
                 lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B3F Southwest Strength Boulder (Northwest)"),
                 lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B3F Southwest Strength Boulder (Southeast)"),
                 lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B3F Southeast Strength Boulder (Northwest)"),
                 lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path B3F Southeast Strength Boulder (Southwest)"),
                 lambda state: can_strength(state))

        # Two Island Town
        set_rule(get_location("Two Island Town - Item Behind Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_location("Two Island Game Corner - Lostelle's Dad Gift (Deliver Meteorite)"),
                 lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player))
        set_rule(get_location("Two Island Town - Market Stall"),
                 lambda state: state.has_all(["Rescue Lostelle", "Defeat Champion"], player))
        set_rule(get_location("Two Island Game Corner - Lostelle's Dad's Delivery"),
                 lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player))

        # Cape Brink
        set_rule(get_entrance("Cape Brink Surfing Spot"), lambda state: can_surf(state))

        # Three Island Town
        set_rule(get_entrance("Three Island Town Cuttable Tree"), lambda state: can_cut(state))

        # Bond Bridge
        set_rule(get_entrance("Bond Bridge Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Bond Bridge Cuttable Tree"), lambda state: can_cut(state))

        # Berry Forest
        set_rule(get_location("Berry Forest - Item Past Southwest Pond"), lambda state: can_cut(state))
        set_rule(get_entrance("Berry Forest Surfing Spot"), lambda state: can_surf(state))

        # Four Island Town
        set_rule(get_location("Four Island Town - Beach Item"), lambda state: can_rock_smash(state))
        set_rule(get_entrance("Four Island Town Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Four Island Town Near Cave Surfing Spot"), lambda state: can_surf(state))

        # Icefall Cave
        set_rule(get_entrance("Icefall Cave Front South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Icefall Cave Front Waterfall Ascend"), lambda state: can_waterfall(state))
        set_rule(get_entrance("Icefall Cave Front Waterfall Drop"), lambda state: can_waterfall(state))
        set_rule(get_entrance("Icefall Cave Front Center Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Icefall Cave Front North Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Icefall Cave Back Surfing Spot"), lambda state: can_surf(state))

        # Five Island Town
        set_rule(get_entrance("Five Island Town Surfing Spot"), lambda state: can_surf(state))

        # Five Isle Meadow
        set_rule(get_location("Five Isle Meadow - Item Behind Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Five Isle Meadow Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Rocket Warehouse"),
                 lambda state: state.has_all(["Learn Goldeen Need Log", "Learn Yes Nah Chansey"], player))

        # Memorial Pillar
        set_rule(get_location("Memorial Pillar - Memorial Man Gift"), lambda state: state.has("Buy Lemonade", player))

        # Resort Gorgeous
        set_rule(get_entrance("Resort Gorgeous Near Resort Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Resort Gorgeous Near Cave Surfing Spot"), lambda state: can_surf(state))

        # Water Path
        set_rule(get_entrance("Water Path South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Water Path North Surfing Spot (South)"), lambda state: can_surf(state))
        set_rule(get_entrance("Water Path North Surfing Spot (North)"), lambda state: can_surf(state))

        # Ruin Valley
        set_rule(get_location("Ruin Valley - Plateau Item"), lambda state: can_strength(state))
        set_rule(get_location("Ruin Valley - Southwest Item"), lambda state: can_strength(state))
        set_rule(get_location("Ruin Valley - Southeast Item"), lambda state: can_strength(state))
        set_rule(get_entrance("Ruin Valley Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Dotted Hole"), lambda state: state.has("Help Lorelei", player) and can_cut(state))

        # Green Path
        set_rule(get_entrance("Green Path West Surfing Spot"), lambda state: can_surf(state))

        # Outcast Island
        set_rule(get_entrance("Outcast Island Surfing Spot"), lambda state: can_surf(state))

        # Seven Island Town
        set_rule(get_location("Seven Island Town - Scientist Gift 1 (Trade Scanner)"),
                 lambda state: state.has("Scanner", player))
        set_rule(get_location("Seven Island Town - Scientist Gift 2 (Trade Scanner)"),
                 lambda state: state.has("Scanner", player))

        # Sevault Canyon
        set_rule(get_location("Sevault Canyon - Item Behind Smashable Rocks"),
                 lambda state: can_strength(state) and can_rock_smash(state))

        # Tanoby Key
        set_rule(get_location("Tanoby Key - Solve Puzzle"), lambda state: can_strength(state))

        # Tanoby Ruins
        set_rule(get_location("Tanoby Ruins - Island Item"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Monean Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Liptoo Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Weepth Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Dilford Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Scufib Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Rixy Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Viapos Chamber - Land Encounter 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_entrance("Tanoby Ruins Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Viapois Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Rixy Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Scufib Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Dilford Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Weepth Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Liptoo Island Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Tanoby Ruins Monean Island Surfing Spot"), lambda state: can_surf(state))

        # Trainer Tower
        set_rule(get_entrance("Trainer Tower Exterior South Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Trainer Tower Exterior North Surfing Spot"), lambda state: can_surf(state))

        # Indigo Plateau
        set_rule(get_location("Champion's Room - Champion Rematch Battle"),
                 lambda state: can_challenge_elite_four_rematch(state))

    def set_sevii_hidden_item_rules():
        # Cape Brink
        set_rule(get_location("Cape Brink - Hidden Item Across Pond"),
                 lambda state: state.has("Itemfinder", player))

    def set_sevii_trainersanity_rules():
        # Mt. Ember
        set_rule(get_location("Mt. Ember Exterior - Team Rocket Grunt Reward (Left)"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(get_location("Mt. Ember Exterior - Team Rocket Grunt Reward (Right)"),
                 lambda state: state.has("Deliver Meteorite", player))

        # Indigo Plateau
        set_rule(get_location("Lorelei's Room - Elite Four Lorelei Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state))
        set_rule(get_location("Bruno's Room - Elite Four Bruno Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state))
        set_rule(get_location("Agatha's Room - Elite Four Agatha Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state))
        set_rule(get_location("Lance's Room - Elite Four Lance Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state))
        set_rule(get_location("Champion's Room - Champion Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state))

    def set_sevii_famesanity_rules():
        # One Island Town
        set_rule(get_location("One Island Pokemon Center 1F - Celio Info 1"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))
        set_rule(get_location("One Island Pokemon Center 1F - Celio Info 2"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))
        set_rule(get_location("One Island Pokemon Center 1F - Celio Info 3"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))

        # Ember Spa
        set_rule(get_location("Ember Spa - Black Belt Info"), lambda state: post_game_gossipers(state))

        # Two Island Town
        set_rule(get_location("Two Island Town - Beauty Info"),
                 lambda state: state.has_all(["Rescue Lostelle", "Defeat Champion"], player))

        # Four Island Town
        set_rule(get_location("Four Island Town - Old Woman Info"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))

        # Five Island Town
        set_rule(get_location("Five Island Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state))

        # Rocket Warehouse
        set_rule(get_location("Rocket Warehouse - Scientist Gideon Info"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))

        # Water Labyrinth
        if options.pokemon_request_locations:
            set_rule(get_location("Water Labyrinth - Gentleman Info"),
                     lambda state: state.has_any(["Togepi", "Togetic"], player))

        # Seven Island
        set_rule(get_location("Seven Island Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state))

    def set_sevii_pokemon_request_rules():
        # Resort Gorgeous
        set_rule(get_location("Resort Gorgeous House - Selphy Gift (Show Pokemon)"),
                 lambda state: state.has_all(["Rescue Selphy", world.resort_gorgeous_mon[1]], player))

        # Water Path
        set_rule(get_location("Water Path Heracross Woman's House - Woman Gift (Show Heracross)"),
                 lambda state: state.has("Heracross", player))

    def set_split_pass_rules():
        # Cinnabar Island
        set_rule(get_location("One Cinnabar Pokemon Center 1F - Bill"),
                 lambda state: state.has("Defeat Blaine", player))

        # One Island Town
        set_rule(get_location("One Island Pokemon Center 1F - Celio (Deliver Sapphire)"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"],
                                             player))

        # Three Island Town
        set_rule(get_location("Lostelle's House - Lostelle"),
                 lambda state: state.has("Deliver Meteorite", player))

        # Dotted Hole
        set_rule(get_location("Dotted Hole 1F - Dropped Item"),
                 lambda state: state.has("Learn Yes Nah Chansey", player))

    def set_sevii_scaling_rules():
        # Mt. Ember
        set_rule(get_location("Team Rocket Grunt 43"), lambda state: state.has("Deliver Meteorite", player))
        set_rule(get_location("Team Rocket Grunt 44"), lambda state: state.has("Deliver Meteorite", player))
        set_rule(get_location("Legendary Moltres"), lambda state: can_strength(state))

        # Indigo Plateau
        set_rule(get_location("Elite Four Rematch"),
                 lambda state: state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], player))

        # Tanoby Ruins
        set_rule(get_location("Monean Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Liptoo Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Weepth Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Dilford Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Scufib Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Rixy Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))
        set_rule(get_location("Viapos Chamber Land Scaling 1"), lambda state: state.has("Unlock Ruins", player))

    set_kanto_rules()
    if options.shuffle_hidden != ShuffleHiddenItems.option_off:
        set_hidden_item_rules()
    if options.extra_key_items:
        set_extra_key_item_rules()
    if options.trainersanity != Trainersanity.special_range_names["none"]:
        set_trainersanity_rules()
    if options.dexsanity != Dexsanity.special_range_names["none"]:
        set_dexsanity_rules()
    if options.famesanity:
        set_famesanity_rules()
    if options.pokemon_request_locations:
        set_pokemon_request_rules()
    if options.split_teas:
        set_split_tea_rules()
    if options.level_scaling != LevelScaling.option_off:
        set_scaling_rules()
    if not options.kanto_only:
        set_sevii_rules()
        if options.shuffle_hidden != ShuffleHiddenItems.option_off:
            set_sevii_hidden_item_rules()
        if options.trainersanity != Trainersanity.special_range_names["none"]:
            set_sevii_trainersanity_rules()
        if options.famesanity:
            set_sevii_famesanity_rules()
        if options.pokemon_request_locations:
            set_sevii_pokemon_request_rules()
        if options.island_passes.value in [SeviiIslandPasses.option_split, SeviiIslandPasses.option_progressive_split]:
            set_split_pass_rules()
        if options.level_scaling != LevelScaling.option_off:
            set_sevii_scaling_rules()
