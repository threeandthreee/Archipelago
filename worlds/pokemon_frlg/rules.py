"""
Logic rule definitions for Pokémon FireRed and LeafGreen
"""
import math
from typing import TYPE_CHECKING, Dict, List
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .data import data
from .options import (ViridianCityRoadblock, ViridianGymRequirement, Route22GateRequirement, ItemfinderRequired,
                      PewterCityRoadblock, CeruleanCaveRequirement, Route23GuardRequirement, EliteFourRequirement,
                      ShuffleHiddenItems, GameVersion)

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

    def gyms_beaten(state: CollectionState):
        return sum([state.has(gym, player) for gym in [
            "Defeat Brock",
            "Defeat Misty",
            "Defeat Lt. Surge",
            "Defeat Erika",
            "Defeat Koga",
            "Defeat Sabrina",
            "Defeat Blaine",
            "Defeat Giovanni"
        ]])

    def has_n_pokemon(state: CollectionState, n: int):
        count = 0
        for species in data.species.values():
            if state.has(species.name, player):
                count += 1
            elif state.has(f'Static {species.name}', player):
                count += 1
            if count >= n:
                return True
        return False

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
        if options.cerulean_city_roadblocks:
            return state.has("Save Bill", player)
        return True

    def can_enter_cerulean_cave(state: CollectionState):
        requirement = options.cerulean_cave_requirement
        count = options.cerulean_cave_count.value
        if requirement == CeruleanCaveRequirement.option_vanilla:
            return (state.has("Defeat Champion", player) and
                    state.has("Restore Pokemon Network Machine", player))
        elif requirement == CeruleanCaveRequirement.option_champion:
            return state.has("Defeat Champion", player)
        elif requirement == CeruleanCaveRequirement.option_restore_network:
            return state.has("Restore Pokemon Network Machine", player)
        elif requirement == CeruleanCaveRequirement.option_badges:
            return has_n_badges(state, count)
        elif requirement == CeruleanCaveRequirement.option_gyms:
            return has_n_gyms(state, count)

    def rock_tunnel(state: CollectionState):
        if options.flash_required:
            return can_flash(state)
        return True

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

    def evolve_level(state: CollectionState, level: int):
        return gyms_beaten(state) >= level / 7

    def get_entrance(entrance: str):
        return multiworld.get_entrance(entrance, player)

    def get_location(location: str):
        return multiworld.get_location(location, player)

    multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion", player)

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
    set_rule(get_entrance("Cinnabar Island Fly Destination"), lambda state: state.has("Fly Cinnabar Island", player))
    set_rule(get_entrance("Indigo Plateau Fly Destination"), lambda state: state.has("Fly Indigo Plateau", player))

    # Seagallop
    set_rule(get_entrance("Navel Rock Arrival"), lambda state: state.has("Mystic Ticket", player))
    set_rule(get_entrance("Birth Island Arrival"), lambda state: state.has("Aurora Ticket", player))

    # Pallet Town
    set_rule(get_location("Pallet Town - Oak (First Gift)"), lambda state: state.has("Defeat Champion", player))
    set_rule(get_location("Pallet Town - Oak (Second Gift)"), lambda state: state.has("Defeat Champion", player))
    set_rule(get_location("Rival's House - Daisy"), lambda state: state.has("Deliver Oak's Parcel", player))
    set_rule(get_location("Professor Oak's Lab - Oak (Deliver Parcel)"),
             lambda state: state.has("Oak's Parcel", player))
    set_rule(get_location("Professor Oak's Lab - Oak (After Route 22 Rival)"),
             lambda state: state.has("Defeat Route 22 Rival", player))
    set_rule(get_location("Professor Oak's Lab - Oak's Delivery"), lambda state: state.has("Oak's Parcel", player))
    set_rule(get_entrance("Pallet Town Surfing Spot"), lambda state: can_surf(state))

    # Viridian City
    set_rule(get_location("Viridian City - Old Man"), lambda state: can_pass_viridian_city_roadblock(state))
    set_rule(get_entrance("Viridian City South Roadblock"),
             lambda state: can_pass_viridian_city_roadblock(state) or can_cut(state))
    set_rule(get_entrance("Viridian City South Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Viridian Gym"), lambda state: can_enter_viridian_gym(state))

    # Route 22
    set_rule(get_location("Route 22 - Early Rival Battle"), lambda state: state.has("Deliver Oak's Parcel", player))
    set_rule(get_entrance("Route 22 Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 22 Gate Exit (North)"), lambda state: can_pass_route_22_gate(state))

    # Route 2
    set_rule(get_location("Route 2 Gate - Oak's Aide"),
             lambda state: has_n_pokemon(state, math.ceil(options.oaks_aide_route_2.value * 1.2)))
    set_rule(get_entrance("Route 2 Southwest Cuttable Trees"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 2 Northwest Cuttable Tree"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 2 Northeast Cuttable Tree (North)"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 2 Northeast Cuttable Tree (South)"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 2 East Cuttable Tree"), lambda state: can_cut(state))

    # Pewter City
    set_rule(get_entrance("Pewter City Cuttable Tree"), lambda state: can_cut(state))
    set_rule(get_entrance("Pewter City Exit (East)"), lambda state: can_pass_pewter_city_roadblock(state))

    # Cerulean City
    set_rule(get_location("Bike Shop - Bicycle Purchase"), lambda state: state.has("Bike Voucher", player))
    set_rule(get_entrance("Cerulean City Cuttable Tree"),
             lambda state: can_pass_cerulean_city_roadblocks(state) and can_cut(state))
    set_rule(get_entrance("Robbed House (Front)"), lambda state: can_pass_cerulean_city_roadblocks(state))
    set_rule(get_entrance("Cerulean City Outskirts Exit (East)"), lambda state: can_cut(state))
    set_rule(get_entrance("Cerulean City Near Cave Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Cerulean Cave"), lambda state: can_enter_cerulean_cave(state))

    # Route 24
    set_rule(get_entrance("Route 24 Surfing Spot"), lambda state: can_surf(state))

    # Route 25
    set_rule(get_location("Route 25 - Item Near Bush"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 25 Surfing Spot"), lambda state: can_surf(state))

    # Route 5
    set_rule(get_entrance("Route 5 Gate North Guard Checkpoint"), lambda state: state.has("Tea", player))
    set_rule(get_entrance("Route 5 Gate South Guard Checkpoint"), lambda state: state.has("Tea", player))

    # Route 6
    set_rule(get_entrance("Route 6 Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 6 Gate South Guard Checkpoint"), lambda state: state.has("Tea", player))
    set_rule(get_entrance("Route 6 Gate North Guard Checkpoint"), lambda state: state.has("Tea", player))

    # Vermilion City
    set_rule(get_entrance("Vermilion City Cuttable Tree"), lambda state: can_cut(state))
    set_rule(get_entrance("Vermilion City Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Vermilion City Near Gym Cuttable Tree"), lambda state: can_cut(state))
    set_rule(get_entrance("Vermilion City Near Gym Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Vermilion Harbor"), lambda state: state.has("S.S. Ticket", player))

    # S.S. Anne
    set_rule(get_entrance("S.S. Anne Exterior Surfing Spot"), lambda state: can_surf(state))

    # Route 11
    set_rule(get_location("Route 11 Gate 2F - Oak's Aide"),
             lambda state: has_n_pokemon(state, math.ceil(options.oaks_aide_route_11.value * 1.2)))
    set_rule(get_entrance("Route 11 West Surfing Spot"), lambda state: can_surf(state))

    # Route 9
    set_rule(get_entrance("Route 9 Exit (West)"), lambda state: can_cut(state))

    # Route 10
    set_rule(get_location("Route 10 Pokemon Center 1F - Oak's Aide"),
             lambda state: has_n_pokemon(state, math.ceil(options.oaks_aide_route_10.value * 1.2)))
    set_rule(get_entrance("Route 10 North Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 10 Near Power Plant Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Rock Tunnel (North)"), lambda state: rock_tunnel(state))
    set_rule(get_entrance("Rock Tunnel (South)"), lambda state: rock_tunnel(state))
    set_rule(get_entrance("Power Plant (Front)"),
             lambda state: state.has("Machine Part", player) or not options.extra_key_items)

    # Lavender Town
    set_rule(get_location("Volunteer Pokemon House - Mr. Fuji"), lambda state: state.has("Rescue Mr. Fuji", player))

    # Route 8
    set_rule(get_entrance("Route 8 Cuttable Trees"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 8 Gate East Guard Checkpoint"), lambda state: state.has("Tea", player))
    set_rule(get_entrance("Route 8 Gate West Guard Checkpoint"), lambda state: state.has("Tea", player))

    # Route 7
    set_rule(get_entrance("Route 7 Gate West Guard Checkpoint"), lambda state: state.has("Tea", player))
    set_rule(get_entrance("Route 7 Gate East Guard Checkpoint"), lambda state: state.has("Tea", player))

    # Celadon City
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
    set_rule(get_location("Pokemon Tower 6F - Ghost Pokemon"), lambda state: state.has("Silph Scope", player))
    set_rule(get_entrance("Pokemon Tower 6F Stairs (South)"), lambda state: state.has("Silph Scope", player))

    # Route 12
    set_rule(get_entrance("Route 12 West Play Poke Flute"), lambda state: state.has("Poke Flute", player))
    set_rule(get_entrance("Route 12 North Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 12 Center Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 12 Center Play Poke Flute"), lambda state: state.has("Poke Flute", player))
    set_rule(get_entrance("Route 12 South Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 12 South Cuttable Tree (North)"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 12 South Cuttable Tree (South)"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 12 South Play Poke Flute"), lambda state: state.has("Poke Flute", player))

    # Route 13
    set_rule(get_entrance("Route 13 Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 13 Cuttable Tree"), lambda state: can_cut(state))

    # Route 14
    set_rule(get_entrance("Route 14 Cuttable Tree (North)"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 14 Cuttable Tree (South)"), lambda state: can_cut(state))

    # Route 15
    set_rule(get_location("Route 15 Gate 2F - Oak's Aide"),
             lambda state: has_n_pokemon(state, math.ceil(options.oaks_aide_route_15.value * 1.2)))

    # Route 16
    set_rule(get_location("Route 16 Gate 2F - Oak's Aide"),
             lambda state: has_n_pokemon(state, math.ceil(options.oaks_aide_route_16.value * 1.2)))
    set_rule(get_entrance("Route 16 Southeast Cuttable Tree"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 16 Southeast Play Poke Flute"), lambda state: state.has("Poke Flute", player))
    set_rule(get_entrance("Route 16 Northeast Cuttable Tree"), lambda state: can_cut(state))
    set_rule(get_entrance("Route 16 Center Play Poke Flute"), lambda state: state.has("Poke Flute", player))
    set_rule(get_entrance("Route 16 Gate 1F Southeast Bike Checkpoint"), lambda state: state.has("Bicycle", player))

    # Route 18
    set_rule(get_entrance("Route 18 Gate 1F East Bike Checkpoint"), lambda state: state.has("Bicycle", player))

    # Fuchsia City
    set_rule(get_location("Safari Zone Warden's House - Safari Zone Warden"),
             lambda state: state.has("Gold Teeth", player))
    set_rule(get_location("Safari Zone Warden's House - Item"), lambda state: can_strength(state))
    set_rule(get_entrance("Fuchsia City Backyard Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone"), lambda state: state.has("Safari Pass", player) or not options.extra_key_items)

    # Safari Zone
    set_rule(get_entrance("Safari Zone Center Area South Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone Center Area Northwest Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone Center Area Northeast Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone East Area Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone North Area Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone West Area North Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Safari Zone West Area South Surfing Spot"), lambda state: can_surf(state))

    # Saffron City
    set_rule(get_entrance("Silph Co."), lambda state: state.has("Rescue Mr. Fuji", player))
    set_rule(get_entrance("Copycat's House"), lambda state: state.has("Liberate Silph Co.", player))
    set_rule(get_entrance("Saffron Gym"), lambda state: state.has("Liberate Silph Co.", player))
    set_rule(get_entrance("Saffron Pidgey House"), lambda state: state.has("Liberate Silph Co.", player))

    # Silph Co.
    set_rule(get_entrance("Silph Co. 2F Barrier (Northwest)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 2F Barrier (Southwest)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 2F Northwest Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 2F Southwest Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 3F Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 3F Center Room Barrier (East)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 3F Center Room Barrier (West)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 3F West Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 4F Barrier (West)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 4F Barrier (Center)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 4F North Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 5F Barrier (Northwest)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 5F Barrier (Center)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 5F Barrier (Southwest)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 5F Southwest Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 6F Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 7F Barrier (Center)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 7F Barrier (East)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 7F East Room Barrier (North)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 7F East Room Barrier (South)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 7F Southeast Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 8F Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 8F West Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 9F Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 9F Northwest Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 9F Southwest Room Barrier (East)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 9F Southwest Room Barrier (West)"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 10F Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 10F Southeast Room Barrier"), lambda state: state.has("Card Key", player))
    set_rule(get_entrance("Silph Co. 11F West Barrier"), lambda state: state.has("Card Key", player))

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

    # Cinnabar Island
    set_rule(get_entrance("Cinnabar Island Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Cinnabar Gym"), lambda state: state.has("Secret Key", player))
    set_rule(get_entrance("Pokemon Mansion"), lambda state: state.has("Letter", player) or not options.extra_key_items)

    # Route 23
    set_rule(get_entrance("Route 23 South Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 23 Center Surfing Spot"), lambda state: can_surf(state))
    set_rule(get_entrance("Route 23 Center Guard Checkpoint"), lambda state: can_pass_route_23_guard(state))

    # Victory Road
    set_rule(get_location("Victory Road 1F - North Item (Left)"), lambda state: can_strength(state))
    set_rule(get_location("Victory Road 1F - North Item (Right)"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 1F South Rock Barrier"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 1F North Strength Boulder"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 2F Southwest Rock Barrier"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 2F Center Rock Barrier"),
             lambda state: can_strength(state) and state.can_reach_region("Victory Road 3F Southwest", player))
    set_rule(get_entrance("Victory Road 2F Northwest Strength Boulder"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 3F North Rock Barrier"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 3F Southwest Strength Boulder"), lambda state: can_strength(state))
    set_rule(get_entrance("Victory Road 3F Southeast Strength Boulder"), lambda state: can_strength(state))

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

    # Hidden Items
    if options.shuffle_hidden != ShuffleHiddenItems.option_off:
        # Viridian Gym
        set_rule(get_location("Viridian Gym - Hidden Item Under Giovanni"),
                 lambda state: state.has("Itemfinder", player))

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
                if location.tags is not None and ("Hidden" in location.tags):
                    add_rule(location, lambda state: state.has("Itemfinder", player))

    # Extra Key Items
    if options.extra_key_items:
        # Cerulean City
        set_rule(get_location("Cerulean Gym - Hidden Item in Water"),
                 lambda state: can_surf(state) and state.has("Itemfinder", player))

    # Trainersanity
    if options.trainersanity:
        # Route 22
        set_rule(get_location("Route 22 - Early Rival Reward"), lambda state: state.has("Deliver Oak's Parcel", player))
        set_rule(get_location("Route 22 - Late Rival Reward"),
                 lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player))

    # Static Pokémon
    set_rule(get_location("Route 2 Trade House - Trade Abra"), lambda state: state.has("Abra", player))
    set_rule(get_location("Cerulean Trade House - Trade Poliwhirl"), lambda state: state.has("Poliwhirl", player))
    set_rule(get_location("Vermilion Trade House - Trade Spearow"), lambda state: state.has("Spearow", player))
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

    if options.game_version == GameVersion.option_firered:
        set_rule(get_location("Underground Path North Entrance - Trade Nidoran M"),
                 lambda state: state.has("Nidoran M", player))
        set_rule(get_location("Route 11 Gate 2F - Trade Nidorino"), lambda state: state.has("Nidorino", player))
        set_rule(get_location("Route 18 Gate 2F - Trade Golduck"), lambda state: state.has("Golduck", player))
    elif options.game_version == GameVersion.option_leafgreen:
        set_rule(get_location("Underground Path North Entrance - Trade Nidoran F"),
                 lambda state: state.has("Nidoran F", player))
        set_rule(get_location("Route 11 Gate 2F - Trade Nidorina"), lambda state: state.has("Nidorina", player))
        set_rule(get_location("Route 18 Gate 2F - Trade Slowbro"), lambda state: state.has("Slowbro", player))

    # Pokémon Tower encounters
    for i in range(3, 8):
        for j in range(1, 4):
            set_rule(get_location(f"Pokemon Tower {i}F - Land Encounter {j}"),
                     lambda state: state.has("Silph Scope", player))

    # Seafoam Islands B3F water encounters
    for i in range(1, 6):
        set_rule(get_location(f"Seafoam Islands B3F - Water Encounter {i}"),
                 lambda state: can_strength(state) and state.can_reach_region("Seafoam Islands 1F", player))

    # Sevii Islands
    if not options.kanto_only:
        # Sky
        set_rule(get_entrance("One Island Fly Destination"), lambda state: state.has("Fly One Island", player))
        set_rule(get_entrance("Two Island Fly Destination"), lambda state: state.has("Fly Two Island", player))
        set_rule(get_entrance("Three Island Fly Destination"), lambda state: state.has("Fly Three Island", player))
        set_rule(get_entrance("Four Island Fly Destination"), lambda state: state.has("Fly Four Island", player))
        set_rule(get_entrance("Five Island Fly Destination"), lambda state: state.has("Fly Five Island", player))
        set_rule(get_entrance("Six Island Fly Destination"), lambda state: state.has("Fly Six Island", player))
        set_rule(get_entrance("Seven Island Fly Destination"), lambda state: state.has("Fly Seven Island", player))

        # Seagallop
        set_rule(get_entrance("One Island Arrival"), lambda state: state.has("Tri Pass", player))
        set_rule(get_entrance("Two Island Arrival"), lambda state: state.has("Tri Pass", player))
        set_rule(get_entrance("Three Island Arrival"), lambda state: state.has("Tri Pass", player))
        set_rule(get_entrance("Four Island Arrival"), lambda state: state.has("Rainbow Pass", player))
        set_rule(get_entrance("Five Island Arrival"), lambda state: state.has("Rainbow Pass", player))
        set_rule(get_entrance("Six Island Arrival"), lambda state: state.has("Rainbow Pass", player))
        set_rule(get_entrance("Seven Island Arrival"), lambda state: state.has("Rainbow Pass", player))

        # Cinnabar Island
        set_rule(get_entrance("Follow Bill"), lambda state: state.has("Defeat Blaine", player))

        # One Island Town
        set_rule(get_location("One Island Pokemon Center 1F - Celio (Deliver Ruby)"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby"], player))
        set_rule(get_location("One Island Pokemon Center 1F - Help Celio"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Sapphire"], player))
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
        set_rule(get_entrance("Mt. Ember Exterior South Strength Boulders"), lambda state: can_strength(state))
        set_rule(get_entrance("Mt. Ember Ruby Path"), lambda state: state.has("Deliver Meteorite", player))
        set_rule(get_entrance("Mt. Ember Summit Strength Boulders"), lambda state: can_strength(state))
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
        set_rule(get_location("Two Island Game Corner - Lostelle's Dad"),
                 lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player))
        set_rule(get_location("Two Island Town - Market Stall"), lambda state: state.has("Defeat Champion", player))
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
        set_rule(get_entrance("Icefall Cave Front Center Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Icefall Cave Front North Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Icefall Cave Back Surfing Spot"), lambda state: can_surf(state))

        # Five Island Town
        set_rule(get_entrance("Five Island Town Surfing Spot"), lambda state: can_surf(state))

        # Five Isle Meadow
        set_rule(get_location("Five Isle Meadow - Item Behind Cuttable Tree"), lambda state: can_cut(state))
        set_rule(get_entrance("Five Isle Meadow Surfing Spot"), lambda state: can_surf(state))
        set_rule(get_entrance("Rocket Warehouse"), lambda state: state.has("Learn Rocket Warehouse Password", player))

        # Memorial Pillar
        set_rule(get_location("Memorial Pillar - Memorial Man"),
                 lambda state: state.has("Buy Lemonade", player))

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

        # Sevault Canyon
        set_rule(get_location("Sevault Canyon - Item Behind Smashable Rocks"),
                 lambda state: can_strength(state) and can_rock_smash(state))

        # Tanoby Key
        set_rule(get_location("Tanoby Key - Solve Puzzle"), lambda state: can_strength(state))

        # Tanoby Ruins
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

        # Hidden Items
        if options.shuffle_hidden != ShuffleHiddenItems.option_off:
            # Cape Brink
            set_rule(get_location("Cape Brink - Hidden Item Across Pond"),
                     lambda state: state.has("Itemfinder", player))

        # Trainersanity
        if options.trainersanity:
            # Mt. Ember
            set_rule(get_location("Mt. Ember Exterior - Team Rocket Grunt Reward (Left)"),
                     lambda state: state.has("Deliver Meteorite", player))
            set_rule(get_location("Mt. Ember Exterior - Team Rocket Grunt Reward (Right)"),
                     lambda state: state.has("Deliver Meteorite", player))

        # Tanoby Ruins encounters
        set_rule(get_location("Monean Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))
        set_rule(get_location("Liptoo Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))
        set_rule(get_location("Weepth Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))
        set_rule(get_location("Dilford Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))
        set_rule(get_location("Scufib Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))
        set_rule(get_location("Rixy Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))
        set_rule(get_location("Viapos Chamber - Land Encounter 1"), lambda state: state.has("Spawn Unown", player))

    # Evolutions
    set_rule(get_location("Evolution - Bulbasaur"),
             lambda state: state.has("Bulbasaur", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Ivysaur"),
             lambda state: state.has("Ivysaur", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Charmander"),
             lambda state: state.has("Charmander", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Charmeleon"),
             lambda state: state.has("Charmeleon", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Squirtle"),
             lambda state: state.has("Squirtle", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Wartortle"),
             lambda state: state.has("Wartortle", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Caterpie"),
             lambda state: state.has("Caterpie", player) and evolve_level(state, 7))
    set_rule(get_location("Evolution - Metapod"),
             lambda state: state.has("Metapod", player) and evolve_level(state, 10))
    set_rule(get_location("Evolution - Weedle"),
             lambda state: state.has("Weedle", player) and evolve_level(state, 7))
    set_rule(get_location("Evolution - Kakuna"),
             lambda state: state.has("Kakuna", player) and evolve_level(state, 10))
    set_rule(get_location("Evolution - Pidgey"),
             lambda state: state.has("Pidgey", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Pidgeotto"),
             lambda state: state.has("Pidgeotto", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Rattata"),
             lambda state: state.has("Rattata", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Spearow"),
             lambda state: state.has("Spearow", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Ekans"),
             lambda state: state.has("Ekans", player) and evolve_level(state, 22))
    set_rule(get_location("Evolution - Pikachu"),
             lambda state: state.has("Pikachu", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Sandshrew"),
             lambda state: state.has("Sandshrew", player) and evolve_level(state, 22))
    set_rule(get_location("Evolution - Nidoran F"),
             lambda state: state.has("Nidoran F", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Nidoran M"),
             lambda state: state.has("Nidoran M", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Vulpix"),
             lambda state: state.has("Vulpix", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Zubat"),
             lambda state: state.has("Zubat", player) and evolve_level(state, 22))
    set_rule(get_location("Evolution - Golbat"),
             lambda state: state.has("Golbat", player))
    set_rule(get_location("Evolution - Oddish"),
             lambda state: state.has("Oddish", player) and evolve_level(state, 21))
    set_rule(get_location("Evolution - Gloom"),
             lambda state: state.has("Gloom", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Paras"),
             lambda state: state.has("Paras", player) and evolve_level(state, 24))
    set_rule(get_location("Evolution - Venonat"),
             lambda state: state.has("Venonat", player) and evolve_level(state, 31))
    set_rule(get_location("Evolution - Diglett"),
             lambda state: state.has("Diglett", player) and evolve_level(state, 26))
    set_rule(get_location("Evolution - Meowth"),
             lambda state: state.has("Meowth", player) and evolve_level(state, 28))
    set_rule(get_location("Evolution - Psyduck"),
             lambda state: state.has("Psyduck", player) and evolve_level(state, 33))
    set_rule(get_location("Evolution - Mankey"),
             lambda state: state.has("Mankey", player) and evolve_level(state, 28))
    set_rule(get_location("Evolution - Growlithe"),
             lambda state: state.has("Growlithe", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Poliwag"),
             lambda state: state.has("Poliwag", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Poliwhirl"),
             lambda state: state.has("Poliwhirl", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Abra"),
             lambda state: state.has("Abra", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Kadabra"),
             lambda state: state.has("Kadabra", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Machop"),
             lambda state: state.has("Machop", player) and evolve_level(state, 28))
    set_rule(get_location("Evolution - Machoke"),
             lambda state: state.has("Machoke", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Bellsprout"),
             lambda state: state.has("Bellsprout", player) and evolve_level(state, 21))
    set_rule(get_location("Evolution - Weepinbell"),
             lambda state: state.has("Weepinbell", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Tentacool"),
             lambda state: state.has("Tentacool", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Geodude"),
             lambda state: state.has("Geodude", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Graveler"),
             lambda state: state.has("Graveler", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Ponyta"),
             lambda state: state.has("Ponyta", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Slowpoke"),
             lambda state: state.has("Slowpoke", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Magnemite"),
             lambda state: state.has("Magnemite", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Doduo"),
             lambda state: state.has("Doduo", player) and evolve_level(state, 31))
    set_rule(get_location("Evolution - Seel"),
             lambda state: state.has("Seel", player) and evolve_level(state, 34))
    set_rule(get_location("Evolution - Grimer"),
             lambda state: state.has("Grimer", player) and evolve_level(state, 38))
    set_rule(get_location("Evolution - Shellder"),
             lambda state: state.has("Shellder", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Gastly"),
             lambda state: state.has("Gastly", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Haunter"),
             lambda state: state.has("Haunter", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Drowzee"),
             lambda state: state.has("Drowzee", player) and evolve_level(state, 26))
    set_rule(get_location("Evolution - Krabby"),
             lambda state: state.has("Krabby", player) and evolve_level(state, 28))
    set_rule(get_location("Evolution - Voltorb"),
             lambda state: state.has("Voltorb", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Exeggcute"),
             lambda state: state.has("Exeggcute", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Cubone"),
             lambda state: state.has("Cubone", player) and evolve_level(state, 28))
    set_rule(get_location("Evolution - Koffing"),
             lambda state: state.has("Koffing", player) and evolve_level(state, 35))
    set_rule(get_location("Evolution - Rhyhorn"),
             lambda state: state.has("Rhyhorn", player) and evolve_level(state, 42))
    set_rule(get_location("Evolution - Chansey"),
             lambda state: state.has("Chansey", player))
    set_rule(get_location("Evolution - Horsea"),
             lambda state: state.has("Horsea", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Goldeen"),
             lambda state: state.has("Goldeen", player) and evolve_level(state, 33))
    set_rule(get_location("Evolution - Staryu"),
             lambda state: state.has("Staryu", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Magikarp"),
             lambda state: state.has("Magikarp", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Eevee (Thunder Stone)"),
             lambda state: state.has("Eevee", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Eevee (Water Stone)"),
             lambda state: state.has("Eevee", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Eevee (Fire Stone)"),
             lambda state: state.has("Eevee", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Omanyte"),
             lambda state: state.has("Omanyte", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Kabuto"),
             lambda state: state.has("Kabuto", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Dratini"),
             lambda state: state.has("Dratini", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Dragonair"),
             lambda state: state.has("Dragonair", player) and evolve_level(state, 55))
    set_rule(get_location("Evolution - Chikorita"),
             lambda state: state.has("Chikorita", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Bayleef"),
             lambda state: state.has("Bayleef", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Cyndaquil"),
             lambda state: state.has("Cyndaquil", player) and evolve_level(state, 14))
    set_rule(get_location("Evolution - Quilava"),
             lambda state: state.has("Quilava", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Totodile"),
             lambda state: state.has("Totodile", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Croconaw"),
             lambda state: state.has("Croconaw", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Sentret"),
             lambda state: state.has("Sentret", player) and evolve_level(state, 15))
    set_rule(get_location("Evolution - Hoothoot"),
             lambda state: state.has("Hoothoot", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Ledyba"),
             lambda state: state.has("Ledyba", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Spinarak"),
             lambda state: state.has("Spinarak", player) and evolve_level(state, 22))
    set_rule(get_location("Evolution - Chinchou"),
             lambda state: state.has("Chinchou", player) and evolve_level(state, 27))
    set_rule(get_location("Evolution - Pichu"),
             lambda state: state.has("Pichu", player))
    set_rule(get_location("Evolution - Cleffa"),
             lambda state: state.has("Cleffa", player))
    set_rule(get_location("Evolution - Igglybuff"),
             lambda state: state.has("Igglybuff", player))
    set_rule(get_location("Evolution - Togepi"),
             lambda state: state.has("Togepi", player))
    set_rule(get_location("Evolution - Natu"),
             lambda state: state.has("Natu", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Mareep"),
             lambda state: state.has("Mareep", player) and evolve_level(state, 15))
    set_rule(get_location("Evolution - Flaaffy"),
             lambda state: state.has("Flaaffy", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Marill"),
             lambda state: state.has("Marill", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Hoppip"),
             lambda state: state.has("Hoppip", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Skiploom"),
             lambda state: state.has("Skiploom", player) and evolve_level(state, 27))
    set_rule(get_location("Evolution - Wooper"),
             lambda state: state.has("Wooper", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Pineco"),
             lambda state: state.has("Pineco", player) and evolve_level(state, 31))
    set_rule(get_location("Evolution - Snubbull"),
             lambda state: state.has("Snubbull", player) and evolve_level(state, 23))
    set_rule(get_location("Evolution - Teddiursa"),
             lambda state: state.has("Teddiursa", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Slugma"),
             lambda state: state.has("Slugma", player) and evolve_level(state, 38))
    set_rule(get_location("Evolution - Swinub"),
             lambda state: state.has("Swinub", player) and evolve_level(state, 33))
    set_rule(get_location("Evolution - Remoraid"),
             lambda state: state.has("Remoraid", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Houndour"),
             lambda state: state.has("Houndour", player) and evolve_level(state, 24))
    set_rule(get_location("Evolution - Phanpy"),
             lambda state: state.has("Phanpy", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Tyrogue (Atk < Def)"),
             lambda state: state.has("Tyrogue", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Tyrogue (Atk > Def)"),
             lambda state: state.has("Tyrogue", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Tyrogue (Atk = Def)"),
             lambda state: state.has("Tyrogue", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Smoochum"),
             lambda state: state.has("Smoochum", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Elekid"),
             lambda state: state.has("Elekid", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Magby"),
             lambda state: state.has("Magby", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Larvitar"),
             lambda state: state.has("Larvitar", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Pupitar"),
             lambda state: state.has("Pupitar", player) and evolve_level(state, 55))
    set_rule(get_location("Evolution - Treecko"),
             lambda state: state.has("Treecko", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Grovyle"),
             lambda state: state.has("Grovyle", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Torchic"),
             lambda state: state.has("Torchic", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Combusken"),
             lambda state: state.has("Combusken", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Mudkip"),
             lambda state: state.has("Mudkip", player) and evolve_level(state, 16))
    set_rule(get_location("Evolution - Marshtomp"),
             lambda state: state.has("Marshtomp", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Poochyena"),
             lambda state: state.has("Poochyena", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Zigzagoon"),
             lambda state: state.has("Zigzagoon", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Wurmple (Low Personality)"),
             lambda state: state.has("Wurmple", player) and evolve_level(state, 7))
    set_rule(get_location("Evolution - Wurmple (High Personality)"),
             lambda state: state.has("Wurmple", player) and evolve_level(state, 7))
    set_rule(get_location("Evolution - Silcoon"),
             lambda state: state.has("Silcoon", player) and evolve_level(state, 10))
    set_rule(get_location("Evolution - Cascoon"),
             lambda state: state.has("Cascoon", player) and evolve_level(state, 10))
    set_rule(get_location("Evolution - Lotad"),
             lambda state: state.has("Lotad", player) and evolve_level(state, 14))
    set_rule(get_location("Evolution - Lombre"),
             lambda state: state.has("Lombre", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Seedot"),
             lambda state: state.has("Seedot", player) and evolve_level(state, 14))
    set_rule(get_location("Evolution - Nuzleaf"),
             lambda state: state.has("Nuzleaf", player) and state.has("Buy Evo Stones", player))
    set_rule(get_location("Evolution - Nincada"),
             lambda state: state.has("Nincada", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Nincada (Extra)"),
             lambda state: state.has("Nincada", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Taillow"),
             lambda state: state.has("Taillow", player) and evolve_level(state, 22))
    set_rule(get_location("Evolution - Shroomish"),
             lambda state: state.has("Shroomish", player) and evolve_level(state, 23))
    set_rule(get_location("Evolution - Wingull"),
             lambda state: state.has("Wingull", player) and evolve_level(state, 25))
    set_rule(get_location("Evolution - Surskit"),
             lambda state: state.has("Surskit", player) and evolve_level(state, 22))
    set_rule(get_location("Evolution - Wailmer"),
             lambda state: state.has("Wailmer", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Baltoy"),
             lambda state: state.has("Baltoy", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Barboach"),
             lambda state: state.has("Barboach", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Corphish"),
             lambda state: state.has("Corphish", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Feebas"),
             lambda state: state.has("Feebas", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Carvanha"),
             lambda state: state.has("Carvanha", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Trapinch"),
             lambda state: state.has("Trapinch", player) and evolve_level(state, 35))
    set_rule(get_location("Evolution - Vibrava"),
             lambda state: state.has("Vibrava", player) and evolve_level(state, 45))
    set_rule(get_location("Evolution - Makuhita"),
             lambda state: state.has("Makuhita", player) and evolve_level(state, 24))
    set_rule(get_location("Evolution - Electrike"),
             lambda state: state.has("Electrike", player) and evolve_level(state, 26))
    set_rule(get_location("Evolution - Numel"),
             lambda state: state.has("Numel", player) and evolve_level(state, 33))
    set_rule(get_location("Evolution - Spheal"),
             lambda state: state.has("Spheal", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Sealeo"),
             lambda state: state.has("Sealeo", player) and evolve_level(state, 44))
    set_rule(get_location("Evolution - Cacnea"),
             lambda state: state.has("Cacnea", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Snorunt"),
             lambda state: state.has("Snorunt", player) and evolve_level(state, 42))
    set_rule(get_location("Evolution - Azurill"),
             lambda state: state.has("Azurill", player))
    set_rule(get_location("Evolution - Spoink"),
             lambda state: state.has("Spoink", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Meditite"),
             lambda state: state.has("Meditite", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Swablu"),
             lambda state: state.has("Swablu", player) and evolve_level(state, 35))
    set_rule(get_location("Evolution - Wynaut"),
             lambda state: state.has("Wynaut", player) and evolve_level(state, 15))
    set_rule(get_location("Evolution - Duskull"),
             lambda state: state.has("Duskull", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Slakoth"),
             lambda state: state.has("Slakoth", player) and evolve_level(state, 18))
    set_rule(get_location("Evolution - Vigoroth"),
             lambda state: state.has("Vigoroth", player) and evolve_level(state, 36))
    set_rule(get_location("Evolution - Gulpin"),
             lambda state: state.has("Gulpin", player) and evolve_level(state, 26))
    set_rule(get_location("Evolution - Whismur"),
             lambda state: state.has("Whismur", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Loudred"),
             lambda state: state.has("Loudred", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Shuppet"),
             lambda state: state.has("Shuppet", player) and evolve_level(state, 37))
    set_rule(get_location("Evolution - Aron"),
             lambda state: state.has("Aron", player) and evolve_level(state, 32))
    set_rule(get_location("Evolution - Lairon"),
             lambda state: state.has("Lairon", player) and evolve_level(state, 42))
    set_rule(get_location("Evolution - Lileep"),
             lambda state: state.has("Lileep", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Anorith"),
             lambda state: state.has("Anorith", player) and evolve_level(state, 40))
    set_rule(get_location("Evolution - Ralts"),
             lambda state: state.has("Ralts", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Kirlia"),
             lambda state: state.has("Kirlia", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Bagon"),
             lambda state: state.has("Bagon", player) and evolve_level(state, 30))
    set_rule(get_location("Evolution - Shelgon"),
             lambda state: state.has("Shelgon", player) and evolve_level(state, 50))
    set_rule(get_location("Evolution - Beldum"),
             lambda state: state.has("Beldum", player) and evolve_level(state, 20))
    set_rule(get_location("Evolution - Metang"),
             lambda state: state.has("Metang", player) and evolve_level(state, 45))
