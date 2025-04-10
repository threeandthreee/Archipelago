"""
Logic rule definitions for Pokémon FireRed and LeafGreen
"""
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule
from .data import data, LocationCategory, NATIONAL_ID_TO_SPECIES_ID, NUM_REAL_SPECIES
from .locations import PokemonFRLGLocation
from .logic import (can_challenge_elite_four, can_challenge_elite_four_rematch, can_cut, can_enter_cerulean_cave,
                    can_enter_silph, can_enter_viridian_gym, can_evolve, can_fly, can_leave_cerulean, can_leave_pewter,
                    can_leave_viridian, can_navigate_dark_caves, can_open_silph_door, can_pass_route_22_gate,
                    can_pass_route_23_guard, can_rock_smash, can_sail_island, can_sail_vermilion, can_strength,
                    can_surf, can_waterfall, has_n_pokemon, has_pokemon, post_game_gossipers, saffron_rockets_gone)
from .options import (Dexsanity, GameVersion, Goal, ItemfinderRequired, LevelScaling, SeviiIslandPasses,
                      ShuffleHiddenItems, ShuffleRunningShoes, Trainersanity)

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


def set_default_rules(world: "PokemonFRLGWorld"):
    player = world.player
    options = world.options

    if options.goal == Goal.option_elite_four:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion", player)
    elif options.goal == Goal.option_elite_four_rematch:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion (Rematch)", player)

    # Sky
    set_rule(world.get_entrance("Flying"),
             lambda state: can_fly(state, player, world))
    set_rule(world.get_entrance("Pallet Town Fly Destination"),
             lambda state: state.has("Fly Pallet Town", player))
    set_rule(world.get_entrance("Viridian City Fly Destination"),
             lambda state: state.has("Fly Viridian City", player))
    set_rule(world.get_entrance("Pewter City Fly Destination"),
             lambda state: state.has("Fly Pewter City", player))
    set_rule(world.get_entrance("Route 4 Fly Destination"),
             lambda state: state.has("Fly Route 4", player))
    set_rule(world.get_entrance("Cerulean City Fly Destination"),
             lambda state: state.has("Fly Cerulean City", player))
    set_rule(world.get_entrance("Vermilion City Fly Destination"),
             lambda state: state.has("Fly Vermilion City", player))
    set_rule(world.get_entrance("Route 10 Fly Destination"),
             lambda state: state.has("Fly Route 10", player))
    set_rule(world.get_entrance("Lavender Town Fly Destination"),
             lambda state: state.has("Fly Lavender Town", player))
    set_rule(world.get_entrance("Celadon City Fly Destination"),
             lambda state: state.has("Fly Celadon City", player))
    set_rule(world.get_entrance("Fuchsia City Fly Destination"),
             lambda state: state.has("Fly Fuchsia City", player))
    set_rule(world.get_entrance("Saffron City Fly Destination"),
             lambda state: state.has("Fly Saffron City", player))
    set_rule(world.get_entrance("Cinnabar Island Fly Destination"),
             lambda state: state.has("Fly Cinnabar Island", player))
    set_rule(world.get_entrance("Indigo Plateau Fly Destination"),
             lambda state: state.has("Fly Indigo Plateau", player))

    # Seagallop
    set_rule(world.get_entrance("Vermilion City Arrival"),
             lambda state: can_sail_vermilion(state, player, options))
    set_rule(world.get_entrance("Navel Rock Arrival"),
             lambda state: state.has("Mystic Ticket", player) and
                           state.can_reach_region("Vermilion City", player))
    set_rule(world.get_entrance("Birth Island Arrival"),
             lambda state: state.has("Aurora Ticket", player) and
                           state.can_reach_region("Vermilion City", player))

    # Pallet Town
    set_rule(world.get_location("Rival's House - Daisy Gift"),
             lambda state: state.has("Deliver Oak's Parcel", player))
    set_rule(world.get_location("Professor Oak's Lab - Oak Gift (Deliver Parcel)"),
             lambda state: state.has("Oak's Parcel", player))
    set_rule(world.get_location("Professor Oak's Lab - Oak Gift (Post Route 22 Rival)"),
             lambda state: state.has("Defeat Route 22 Rival", player))
    set_rule(world.get_location("Professor Oak's Lab - Oak's Delivery"),
             lambda state: state.has("Oak's Parcel", player))
    set_rule(world.get_entrance("Pallet Town Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Viridian City
    set_rule(world.get_location("Viridian City - Old Man Gift"),
             lambda state: can_leave_viridian(state, player, options))
    set_rule(world.get_entrance("Viridian City South Roadblock"),
             lambda state: can_leave_viridian(state, player, options) or
                           can_cut(state, player, world))
    set_rule(world.get_entrance("Viridian City South Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Viridian Gym"),
             lambda state: can_enter_viridian_gym(state, player, options))

    # Route 22
    set_rule(world.get_location("Route 22 - Early Rival Battle"),
             lambda state: state.has("Deliver Oak's Parcel", player))
    set_rule(world.get_entrance("Route 22 Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 22 Gate Exit (North)"),
             lambda state: can_pass_route_22_gate(state, player, options))

    # Route 2
    set_rule(world.get_location("Route 2 Gate - Oak's Aide Gift (Pokedex Progress)"),
             lambda state: has_n_pokemon(state, player, options.oaks_aide_route_2.value))
    set_rule(world.get_location("Route 2 Trade House - Trade Abra"),
             lambda state: state.has("Abra", player))
    set_rule(world.get_entrance("Route 2 Southwest Cuttable Trees"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 2 East Cuttable Tree"),
             lambda state: can_cut(state, player, world))

    if "Modify Route 2" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 2 Northwest Smashable Rock"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 2 Northeast Smashable Rock"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 2 Northeast Cuttable Tree"),
                 lambda state: can_cut(state, player, world))
    else:
        set_rule(world.get_entrance("Route 2 Northwest Cuttable Tree"),
                 lambda state: can_cut(state, player, world))
        set_rule(world.get_entrance("Route 2 Northeast Cuttable Tree (North)"),
                 lambda state: can_cut(state, player, world))
        set_rule(world.get_entrance("Route 2 Northeast Cuttable Tree (South)"),
                 lambda state: can_cut(state, player, world))

    # Pewter City
    if options.shuffle_running_shoes != ShuffleRunningShoes.option_vanilla:
        set_rule(world.get_location("Pewter City - Gift from Mom"),
                 lambda state: state.has("Defeat Brock", player) and
                               state.can_reach_region("Route 3", player))
    set_rule(world.get_entrance("Pewter City Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Pewter City Exit (East)"),
             lambda state: can_leave_pewter(state, player, options))

    # Mt. Moon
    if "Mt. Moon" in options.additional_dark_caves.value:
        mt_moon_regions = ["Mt. Moon 1F", "Mt. Moon B1F First Tunnel", "Mt. Moon B1F Second Tunnel",
                           "Mt. Moon B1F Third Tunnel", "Mt. Moon B1F Fourth Tunnel", "Mt. Moon B2F South",
                           "Mt. Moon B2F Northeast", "Mt. Moon B2F", "Mt. Moon 1F Land Encounters",
                           "Mt. Moon B1F Land Encounters", "Mt. Moon B2F Land Encounters"]
        for region in mt_moon_regions:
            for entrance in world.get_region(region).entrances:
                add_rule(entrance, lambda state: can_navigate_dark_caves(state, player, world))
            for location in world.get_region(region).locations:
                add_rule(location, lambda state: can_navigate_dark_caves(state, player, world))

    # Cerulean City
    set_rule(world.get_location("Bike Shop - Bicycle Purchase"),
             lambda state: state.has("Bike Voucher", player))
    set_rule(world.get_location("Cerulean Trade House - Trade Poliwhirl"),
             lambda state: state.has("Poliwhirl", player))
    set_rule(world.get_entrance("Cerulean City Cuttable Tree"),
             lambda state: can_leave_cerulean(state, player, options) and
                           can_cut(state, player, world))
    set_rule(world.get_entrance("Robbed House (Front)"),
             lambda state: can_leave_cerulean(state, player, options))
    set_rule(world.get_entrance("Cerulean City Outskirts Exit (East)"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Cerulean City Near Cave Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Cerulean Cave"),
             lambda state: can_enter_cerulean_cave(state, player, options))

    if "Modify Route 9" in options.modify_world_state.value:
        set_rule(world.get_entrance("Cerulean City Outskirts Exit (East)"),
                 lambda state: can_rock_smash(state, player, world))
    else:
        set_rule(world.get_entrance("Cerulean City Outskirts Exit (East)"),
                 lambda state: can_cut(state, player, world))

    # Route 24
    set_rule(world.get_entrance("Route 24 Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Route 25
    set_rule(world.get_location("Route 25 - Item Near Bush"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 25 Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Route 5
    set_rule(world.get_entrance("Route 5 Gate North Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Blue Tea"], player))
    set_rule(world.get_entrance("Route 5 Gate South Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Blue Tea"], player))

    if "Block Tunnels" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 5 Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 5 Near Tunnel Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))

    # Underground Path North-South Tunnel
    if options.game_version == GameVersion.option_firered:
        set_rule(world.get_location("Underground Path North Entrance - Trade Nidoran M"),
                 lambda state: state.has("Nidoran M", player))
    elif options.game_version == GameVersion.option_leafgreen:
        set_rule(world.get_location("Underground Path North Entrance - Trade Nidoran F"),
                 lambda state: state.has("Nidoran F", player))

    # Route 6
    set_rule(world.get_entrance("Route 6 Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 6 Gate South Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Red Tea"], player))
    set_rule(world.get_entrance("Route 6 Gate North Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Red Tea"], player))

    if "Block Tunnels" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 6 Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 6 Near Tunnel Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))

    # Vermilion City
    set_rule(world.get_location("Vermilion Trade House - Trade Spearow"),
             lambda state: state.has("Spearow", player))
    set_rule(world.get_entrance("Vermilion City Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Vermilion City Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Vermilion City Near Gym Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Vermilion City Near Gym Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Vermilion City Checkpoint"),
             lambda state: state.has("S.S. Ticket", player))

    # S.S. Anne
    set_rule(world.get_entrance("S.S. Anne Exterior Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Route 11
    set_rule(world.get_location("Route 11 Gate 2F - Oak's Aide Gift (Pokedex Progress)"),
             lambda state: has_n_pokemon(state, player, options.oaks_aide_route_11.value))
    set_rule(world.get_entrance("Route 11 West Surfing Spot"),
             lambda state: can_surf(state, player, world))

    if "Route 12 Boulders" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 11 East Exit"),
                 lambda state: can_strength(state, player, world))

    if options.game_version == GameVersion.option_firered:
        set_rule(world.get_location("Route 11 Gate 2F - Trade Nidorino"),
                 lambda state: state.has("Nidorino", player))
    elif options.game_version == GameVersion.option_leafgreen:
        set_rule(world.get_location("Route 11 Gate 2F - Trade Nidorina"),
                 lambda state: state.has("Nidorina", player))

    # Diglett's Cave
    if "Diglett's Cave" in options.additional_dark_caves.value:
        digletts_cave_regions = ["Diglett's Cave B1F", "Diglett's Cave B1F Land Encounters"]
        for region in digletts_cave_regions:
            for entrance in world.get_region(region).entrances:
                add_rule(entrance, lambda state: can_navigate_dark_caves(state, player, world))
            for location in world.get_region(region).locations:
                add_rule(location, lambda state: can_navigate_dark_caves(state, player, world))

    # Route 9
    if "Modify Route 9" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 9 Exit (West)"),
                 lambda state: can_rock_smash(state, player, world))
    else:
        set_rule(world.get_entrance("Route 9 Exit (West)"),
                 lambda state: can_cut(state, player, world))

    # Route 10
    set_rule(world.get_location("Route 10 Pokemon Center 1F - Oak's Aide Gift (Pokedex Progress)"),
             lambda state: has_n_pokemon(state, player, options.oaks_aide_route_10.value))
    set_rule(world.get_entrance("Route 10 North Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 10 Near Power Plant Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Power Plant (Front)"),
             lambda state: state.has("Machine Part", player) or
                           not options.extra_key_items)
    set_rule(world.get_entrance("Route 10 Waterfall Drop"),
             lambda state: can_waterfall(state, player, world))
    set_rule(world.get_entrance("Route 10 Waterfall Ascend"),
             lambda state: can_waterfall(state, player, world))

    if "Modify Route 10" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 10 South Surfing Spot"),
                 lambda state: can_surf(state, player, world))
    else:
        set_rule(world.get_entrance("Route 10 South Surfing Spot"),
                 lambda state: False)
        set_rule(world.get_entrance("Route 10 South Landing"),
                 lambda state: False)
        set_rule(world.get_entrance("Route 10 South (Fishing Battle)"),
                 lambda state: False)

    # Rock Tunnel
    rock_tunnel_regions = ["Rock Tunnel 1F Northeast", "Rock Tunnel 1F Northwest", "Rock Tunnel 1F South",
                           "Rock Tunnel B1F Southeast", "Rock Tunnel B1F Northwest", "Rock Tunnel 1F Land Encounters",
                           "Rock Tunnel B1F Land Encounters"]
    for region in rock_tunnel_regions:
        for entrance in world.get_region(region).entrances:
            add_rule(entrance, lambda state: can_navigate_dark_caves(state, player, world))
        for location in world.get_region(region).locations:
            add_rule(location, lambda state: can_navigate_dark_caves(state, player, world))

    # Lavender Town
    set_rule(world.get_location("Volunteer Pokemon House - Mr. Fuji Gift"),
             lambda state: state.has("Rescue Mr. Fuji", player))

    if "Route 12 Boulders" in options.modify_world_state.value:
        set_rule(world.get_entrance("Lavender Town Exit (South)"),
                 lambda state: can_strength(state, player, world))

    # Route 8
    set_rule(world.get_entrance("Route 8 Cuttable Trees"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 8 Gate East Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Purple Tea"], player))
    set_rule(world.get_entrance("Route 8 Gate West Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Purple Tea"], player))

    if "Block Tunnels" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 8 Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 8 Near Tunnel Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))

    # Route 7
    set_rule(world.get_entrance("Route 7 Gate West Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Green Tea"], player))
    set_rule(world.get_entrance("Route 7 Gate East Guard Checkpoint"),
             lambda state: state.has_any(["Tea", "Green Tea"], player))

    if "Block Tunnels" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 7 Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 7 Near Tunnel Smashable Rocks"),
                 lambda state: can_rock_smash(state, player, world))

    # Celadon City
    set_rule(world.get_location("Celadon Game Corner - Fisherman Gift"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - Scientist Gift"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - Gentleman Gift"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner Prize Room - Prize Pokemon 1"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner Prize Room - Prize Pokemon 2"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner Prize Room - Prize Pokemon 3"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner Prize Room - Prize Pokemon 4"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner Prize Room - Prize Pokemon 5"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_entrance("Celadon City Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Celadon City Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Celadon City Near Gym Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Rocket Hideout"),
             lambda state: state.has("Hideout Key", player) or
                           not options.extra_key_items)
    set_rule(world.get_entrance("Celadon Gym Cuttable Trees"),
             lambda state: can_cut(state, player, world))

    # Rocket Hideout
    set_rule(world.get_entrance("Rocket Hideout Elevator B1F Stop"),
             lambda state: state.has("Lift Key", player))
    set_rule(world.get_entrance("Rocket Hideout Elevator B2F Stop"),
             lambda state: state.has("Lift Key", player))
    set_rule(world.get_entrance("Rocket Hideout Elevator B4F Stop"),
             lambda state: state.has("Lift Key", player))

    # Pokemon Tower
    set_rule(world.get_entrance("Pokemon Tower 6F (Ghost Battle)"),
             lambda state: state.has("Silph Scope", player))
    set_rule(world.get_entrance("Pokemon Tower 6F Near Stairs (Ghost Battle)"),
             lambda state: state.has("Silph Scope", player))
    set_rule(world.get_entrance("Pokemon Tower 6F Reveal Ghost"),
             lambda state: state.has("Silph Scope", player))

    if "Block Tower" in options.modify_world_state.value:
        set_rule(world.get_entrance("Pokemon Tower 1F (Ghost Battle)"),
                 lambda state: state.has("Silph Scope", player))
        set_rule(world.get_entrance("Pokemon Tower 1F Near Stairs (Ghost Battle)"),
                 lambda state: state.has("Silph Scope", player))
        set_rule(world.get_entrance("Pokemon Tower 1F Reveal Ghost"),
                 lambda state: state.has("Silph Scope", player))
    else:
        set_rule(world.get_entrance("Pokemon Tower 1F (Ghost Battle)"),
                 lambda state: False)
        set_rule(world.get_entrance("Pokemon Tower 1F Near Stairs (Ghost Battle)"),
                 lambda state: False)

    for i in range(3, 8):
        for j in range(1, 4):
            set_rule(world.get_location(f"Pokemon Tower {i}F - Land Encounter {j}"),
                     lambda state: state.has("Silph Scope", player))

    # Route 12
    set_rule(world.get_entrance("Route 12 West Play Poke Flute"),
             lambda state: state.has("Poke Flute", player))
    set_rule(world.get_entrance("Route 12 North Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 12 Center Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 12 Center Play Poke Flute"),
             lambda state: state.has("Poke Flute", player))
    set_rule(world.get_entrance("Route 12 South Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 12 South Cuttable Tree (North)"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 12 South Cuttable Tree (South)"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 12 South Play Poke Flute"),
             lambda state: state.has("Poke Flute", player))

    if "Route 12 Boulders" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 12 West Exit"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Route 12 North Exit"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Route 12 South Exit"),
                 lambda state: can_strength(state, player, world))

    if "Modify Route 12" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 12 Center Water Unobstructed Path"),
                 lambda state: False)
        set_rule(world.get_entrance("Route 12 South Water Unobstructed Path"),
                 lambda state: False)

    # Route 13
    set_rule(world.get_entrance("Route 13 Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 13 Cuttable Tree"),
             lambda state: can_cut(state, player, world))

    if "Route 12 Boulders" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 13 Exit (East)"),
                 lambda state: can_strength(state, player, world))

    # Route 14
    set_rule(world.get_entrance("Route 14 Cuttable Tree (North)"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 14 Cuttable Tree (South)"),
             lambda state: can_cut(state, player, world))

    # Route 15
    set_rule(world.get_location("Route 15 Gate 2F - Oak's Aide Gift (Pokedex Progress)"),
             lambda state: has_n_pokemon(state, player, options.oaks_aide_route_15.value))

    # Route 16
    set_rule(world.get_location("Route 16 Gate 2F - Oak's Aide Gift (Pokedex Progress)"),
             lambda state: has_n_pokemon(state, player, options.oaks_aide_route_16.value))
    set_rule(world.get_entrance("Route 16 Southeast Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 16 Southeast Play Poke Flute"),
             lambda state: state.has("Poke Flute", player))
    set_rule(world.get_entrance("Route 16 Northeast Cuttable Tree"),
             lambda state: can_cut(state, player, world))
    set_rule(world.get_entrance("Route 16 Center Play Poke Flute"),
             lambda state: state.has("Poke Flute", player))
    set_rule(world.get_entrance("Route 16 Gate 1F Southeast Bike Checkpoint"),
             lambda state: state.has("Bicycle", player))

    if "Modify Route 16" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 16 Northeast Smashable Rock"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Route 16 Center Smashable Rock"),
                 lambda state: can_rock_smash(state, player, world))
    else:
        set_rule(world.get_entrance("Route 16 Northeast Smashable Rock"),
                 lambda state: False)
        set_rule(world.get_entrance("Route 16 Center Smashable Rock"),
                 lambda state: False)

    # Route 18
    set_rule(world.get_entrance("Route 18 Gate 1F East Bike Checkpoint"),
             lambda state: state.has("Bicycle", player))

    if options.game_version == GameVersion.option_firered:
        set_rule(world.get_location("Route 18 Gate 2F - Trade Golduck"),
                 lambda state: state.has("Golduck", player))
    elif options.game_version == GameVersion.option_leafgreen:
        set_rule(world.get_location("Route 18 Gate 2F - Trade Slowbro"),
                 lambda state: state.has("Slowbro", player))

    # Fuchsia City
    set_rule(world.get_location("Safari Zone Warden's House - Warden Gift (Return Teeth)"),
             lambda state: state.has("Gold Teeth", player))
    set_rule(world.get_location("Safari Zone Warden's House - Item"),
             lambda state: can_strength(state, player, world))
    set_rule(world.get_entrance("Fuchsia City Backyard Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone"),
             lambda state: state.has("Safari Pass", player) or
                           not options.extra_key_items)

    # Safari Zone
    set_rule(world.get_entrance("Safari Zone Center Area South Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone Center Area Northwest Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone Center Area Northeast Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone East Area Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone North Area Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone West Area North Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Safari Zone West Area South Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Saffron City
    set_rule(world.get_entrance("Silph Co."),
             lambda state: can_enter_silph(state, player, options) or
                           saffron_rockets_gone(state, player, options))
    set_rule(world.get_entrance("Copycat's House"),
             lambda state: saffron_rockets_gone(state, player, options))
    set_rule(world.get_entrance("Saffron Gym"),
             lambda state: saffron_rockets_gone(state, player, options))
    set_rule(world.get_entrance("Saffron Pidgey House"),
             lambda state: saffron_rockets_gone(state, player, options))

    # Silph Co.
    set_rule(world.get_entrance("Silph Co. 2F Barrier (Northwest)"),
             lambda state: can_open_silph_door(state, player, 2))
    set_rule(world.get_entrance("Silph Co. 2F Barrier (Southwest)"),
             lambda state: can_open_silph_door(state, player, 2))
    set_rule(world.get_entrance("Silph Co. 2F Northwest Room Barrier"),
             lambda state: can_open_silph_door(state, player, 2))
    set_rule(world.get_entrance("Silph Co. 2F Southwest Room Barrier"),
             lambda state: can_open_silph_door(state, player, 2))
    set_rule(world.get_entrance("Silph Co. 3F Barrier"),
             lambda state: can_open_silph_door(state, player, 3))
    set_rule(world.get_entrance("Silph Co. 3F Center Room Barrier (East)"),
             lambda state: can_open_silph_door(state, player, 3))
    set_rule(world.get_entrance("Silph Co. 3F Center Room Barrier (West)"),
             lambda state: can_open_silph_door(state, player, 3))
    set_rule(world.get_entrance("Silph Co. 3F West Room Barrier"),
             lambda state: can_open_silph_door(state, player, 3))
    set_rule(world.get_entrance("Silph Co. 4F Barrier (West)"),
             lambda state: can_open_silph_door(state, player, 4))
    set_rule(world.get_entrance("Silph Co. 4F Barrier (Center)"),
             lambda state: can_open_silph_door(state, player, 4))
    set_rule(world.get_entrance("Silph Co. 4F North Room Barrier"),
             lambda state: can_open_silph_door(state, player, 4))
    set_rule(world.get_entrance("Silph Co. 5F Barrier (Northwest)"),
             lambda state: can_open_silph_door(state, player, 5))
    set_rule(world.get_entrance("Silph Co. 5F Barrier (Center)"),
             lambda state: can_open_silph_door(state, player, 5))
    set_rule(world.get_entrance("Silph Co. 5F Barrier (Southwest)"),
             lambda state: can_open_silph_door(state, player, 5))
    set_rule(world.get_entrance("Silph Co. 5F Southwest Room Barrier"),
             lambda state: can_open_silph_door(state, player, 5))
    set_rule(world.get_entrance("Silph Co. 6F Barrier"),
             lambda state: can_open_silph_door(state, player, 6))
    set_rule(world.get_entrance("Silph Co. 7F Barrier (Center)"),
             lambda state: can_open_silph_door(state, player, 7))
    set_rule(world.get_entrance("Silph Co. 7F Barrier (East)"),
             lambda state: can_open_silph_door(state, player, 7))
    set_rule(world.get_entrance("Silph Co. 7F East Room Barrier (North)"),
             lambda state: can_open_silph_door(state, player, 7))
    set_rule(world.get_entrance("Silph Co. 7F East Room Barrier (South)"),
             lambda state: can_open_silph_door(state, player, 7))
    set_rule(world.get_entrance("Silph Co. 7F Southeast Room Barrier"),
             lambda state: can_open_silph_door(state, player, 7))
    set_rule(world.get_entrance("Silph Co. 8F Barrier"),
             lambda state: can_open_silph_door(state, player, 8))
    set_rule(world.get_entrance("Silph Co. 8F West Room Barrier"),
             lambda state: can_open_silph_door(state, player, 8))
    set_rule(world.get_entrance("Silph Co. 9F Barrier"),
             lambda state: can_open_silph_door(state, player, 9))
    set_rule(world.get_entrance("Silph Co. 9F Northwest Room Barrier"),
             lambda state: can_open_silph_door(state, player, 9))
    set_rule(world.get_entrance("Silph Co. 9F Southwest Room Barrier (East)"),
             lambda state: can_open_silph_door(state, player, 9))
    set_rule(world.get_entrance("Silph Co. 9F Southwest Room Barrier (West)"),
             lambda state: can_open_silph_door(state, player, 9))
    set_rule(world.get_entrance("Silph Co. 10F Barrier"),
             lambda state: can_open_silph_door(state, player, 10))
    set_rule(world.get_entrance("Silph Co. 10F Southeast Room Barrier"),
             lambda state: can_open_silph_door(state, player, 10))
    set_rule(world.get_entrance("Silph Co. 11F West Barrier"),
             lambda state: can_open_silph_door(state, player, 11))

    # Route 19
    set_rule(world.get_entrance("Route 19 Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Route 20
    set_rule(world.get_entrance("Route 20 Near North Cave Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 20 Near South Cave Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Seafoam Islands
    set_rule(world.get_entrance("Seafoam Islands B3F Southwest Surfing Spot"),
             lambda state: can_surf(state, player, world) and
                           can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands 1F", player))
    set_rule(world.get_entrance("Seafoam Islands B3F Southwest Landing"),
             lambda state: can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands 1F", player))
    set_rule(world.get_entrance("Seafoam Islands B3F East Landing (South)"),
             lambda state: can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands 1F", player))
    set_rule(world.get_entrance("Seafoam Islands B3F East Surfing Spot (South)"),
             lambda state: can_surf(state, player, world) and
                           can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands 1F", player))
    set_rule(world.get_entrance("Seafoam Islands B3F East Surfing Spot (North)"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Seafoam Islands B3F Waterfall Ascend (Northeast)"),
             lambda state: can_waterfall(state, player, world))
    set_rule(world.get_entrance("Seafoam Islands B3F Waterfall Drop (Northeast)"),
             lambda state: can_waterfall(state, player, world))
    set_rule(world.get_entrance("Seafoam Islands B3F Waterfall Drop (Northwest)"),
             lambda state: can_waterfall(state, player, world))
    set_rule(world.get_entrance("Seafoam Islands B3F Waterfall Ascend (Northwest)"),
             lambda state: can_waterfall(state, player, world))
    set_rule(world.get_entrance("Seafoam Islands B3F Northwest Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Seafoam Islands B4F Surfing Spot (West)"),
             lambda state: can_surf(state, player, world) and
                           can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands B3F Southwest", player))
    set_rule(world.get_entrance("Seafoam Islands B4F Near Articuno Landing"),
             lambda state: can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands B3F Southwest", player))

    set_rule(world.get_entrance("Seafoam Islands B3F South Water (Water Battle)"),
             lambda state: can_strength(state, player, world) and
                           state.can_reach_region("Seafoam Islands 1F", player))

    # Cinnabar Island
    set_rule(world.get_location("Pokemon Lab Lounge - Trade Raichu"),
             lambda state: state.has("Raichu", player))
    set_rule(world.get_location("Pokemon Lab Lounge - Trade Venonat"),
             lambda state: state.has("Venonat", player))
    set_rule(world.get_location("Pokemon Lab Experiment Room - Revive Helix Fossil"),
             lambda state: state.has("Helix Fossil", player))
    set_rule(world.get_location("Pokemon Lab Experiment Room - Revive Dome Fossil"),
             lambda state: state.has("Dome Fossil", player))
    set_rule(world.get_location("Pokemon Lab Experiment Room - Revive Old Amber"),
             lambda state: state.has("Old Amber", player))
    set_rule(world.get_location("Pokemon Lab Experiment Room - Trade Ponyta"),
             lambda state: state.has("Ponyta", player))
    set_rule(world.get_entrance("Cinnabar Island Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Cinnabar Gym"),
             lambda state: state.has("Secret Key", player))
    set_rule(world.get_entrance("Pokemon Mansion"),
             lambda state: state.has("Letter", player) or
                           not options.extra_key_items)
    set_rule(world.get_entrance("Follow Bill"),
             lambda state: state.has("Defeat Blaine", player))

    # Route 23
    set_rule(world.get_entrance("Route 23 South Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 23 Near Water Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Route 23 Center Guard Checkpoint"),
             lambda state: can_pass_route_23_guard(state, player, options))

    if "Route 23 Trees" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 23 Near Water Cuttable Trees"),
                 lambda state: can_cut(state, player, world))
        set_rule(world.get_entrance("Route 23 Center Cuttable Trees"),
                 lambda state: can_cut(state, player, world))

    if "Modify Route 23" in options.modify_world_state.value:
        set_rule(world.get_entrance("Route 23 Waterfall Ascend"),
                 lambda state: can_waterfall(state, player, world))
        set_rule(world.get_entrance("Route 23 Waterfall Drop"),
                 lambda state: can_waterfall(state, player, world))

    # Victory Road
    set_rule(world.get_location("Victory Road 1F - North Item (Left)"),
             lambda state: can_strength(state, player, world))
    set_rule(world.get_location("Victory Road 1F - North Item (Right)"),
             lambda state: can_strength(state, player, world))
    set_rule(world.get_entrance("Victory Road 1F North Strength Boulder"),
             lambda state: can_strength(state, player, world))
    set_rule(world.get_entrance("Victory Road 2F Center Rock Barrier"),
             lambda state: can_strength(state, player, world) and
                           state.can_reach_region("Victory Road 3F Southwest", player))
    set_rule(world.get_entrance("Victory Road 2F Northwest Strength Boulder"),
             lambda state: can_strength(state, player, world))
    set_rule(world.get_entrance("Victory Road 3F Southwest Strength Boulder"),
             lambda state: can_strength(state, player, world))
    set_rule(world.get_entrance("Victory Road 3F Southeast Strength Boulder"),
             lambda state: can_strength(state, player, world))

    if "Victory Road Rocks" in options.modify_world_state.value:
        set_rule(world.get_entrance("Victory Road 1F South Rock Barrier"),
                 lambda state: can_strength(state, player, world) and
                               can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Victory Road 2F Southwest Rock Barrier"),
                 lambda state: can_strength(state, player, world) and
                               can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Victory Road 3F North Rock Barrier"),
                 lambda state: can_strength(state, player, world) and
                               can_rock_smash(state, player, world))
    else:
        set_rule(world.get_entrance("Victory Road 1F South Rock Barrier"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Victory Road 2F Southwest Rock Barrier"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Victory Road 3F North Rock Barrier"),
                 lambda state: can_strength(state, player, world))

    if "Victory Road" in options.additional_dark_caves.value:
        victory_road_regions = ["Victory Road 1F South", "Victory Road 1F North", "Victory Road 2F Southwest",
                                "Victory Road 2F Center", "Victory Road 2F Northwest", "Victory Road 2F Southeast",
                                "Victory Road 2F East", "Victory Road 3F North", "Victory Road 3F Southwest",
                                "Victory Road 3F Southeast", "Victory Road 1F Land Encounters",
                                "Victory Road 2F Land Encounters", "Victory Road 3F Land Encounters"]
        for region in victory_road_regions:
            for entrance in world.get_region(region).entrances:
                add_rule(entrance, lambda state: can_navigate_dark_caves(state, player, world))
            for location in world.get_region(region).locations:
                add_rule(location, lambda state: can_navigate_dark_caves(state, player, world))

    # Indigo Plateau
    set_rule(world.get_entrance("Pokemon League"),
             lambda state: can_challenge_elite_four(state, player, options))

    # Cerulean Cave
    set_rule(world.get_location("Cerulean Cave 2F - East Item"),
             lambda state: can_rock_smash(state, player, world))
    set_rule(world.get_location("Cerulean Cave 2F - West Item"),
             lambda state: can_rock_smash(state, player, world))
    set_rule(world.get_location("Cerulean Cave 2F - Center Item"),
             lambda state: can_rock_smash(state, player, world))
    set_rule(world.get_entrance("Cerulean Cave 1F Southeast Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Cerulean Cave 1F Northeast Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Cerulean Cave 1F Surfing Spot"),
             lambda state: can_surf(state, player, world))
    set_rule(world.get_entrance("Cerulean Cave B1F Surfing Spot"),
             lambda state: can_surf(state, player, world))

    # Navel Rock
    set_rule(world.get_entrance("Navel Rock Seagallop"),
             lambda state: can_sail_vermilion(state, player, options))

    # Birth Island
    set_rule(world.get_entrance("Birth Island Seagallop"),
             lambda state: can_sail_vermilion(state, player, options))

    # Evolutions
    for location in world.multiworld.get_locations(player):
        assert isinstance(location, PokemonFRLGLocation)
        if location.category == LocationCategory.EVENT_EVOLUTION_POKEMON:
            pokemon_name = location.name.split("-")[1].strip()
            set_rule(world.get_location(location.name),
                     lambda state, pokemon=pokemon_name: can_evolve(state, player, world, pokemon))

    if not options.kanto_only:
        # Sky
        set_rule(world.get_entrance("One Island Fly Destination"),
                 lambda state: state.has("Fly One Island", player))
        set_rule(world.get_entrance("Two Island Fly Destination"),
                 lambda state: state.has("Fly Two Island", player))
        set_rule(world.get_entrance("Three Island Fly Destination"),
                 lambda state: state.has("Fly Three Island", player))
        set_rule(world.get_entrance("Four Island Fly Destination"),
                 lambda state: state.has("Fly Four Island", player))
        set_rule(world.get_entrance("Five Island Fly Destination"),
                 lambda state: state.has("Fly Five Island", player))
        set_rule(world.get_entrance("Six Island Fly Destination"),
                 lambda state: state.has("Fly Six Island", player))
        set_rule(world.get_entrance("Seven Island Fly Destination"),
                 lambda state: state.has("Fly Seven Island", player))

        # Seagallop
        set_rule(world.get_entrance("One Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 1))
        set_rule(world.get_entrance("Two Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 2))
        set_rule(world.get_entrance("Three Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 3))
        set_rule(world.get_entrance("Four Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 4))
        set_rule(world.get_entrance("Five Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 5))
        set_rule(world.get_entrance("Six Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 6))
        set_rule(world.get_entrance("Seven Island Arrival"),
                 lambda state: can_sail_island(state, player, options, 7))

        # One Island Town
        set_rule(world.get_location("One Island Pokemon Center 1F - Celio Gift (Deliver Ruby)"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby"], player))
        set_rule(world.get_location("One Island Pokemon Center 1F - Help Celio"),
                 lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"],
                                             player))
        set_rule(world.get_entrance("One Island Town Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Kindle Road
        set_rule(world.get_location("Kindle Road - Plateau Item"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_location("Kindle Road - Item Behind Smashable Rock"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Kindle Road South Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Kindle Road Center Surfing Spot (South)"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Kindle Road Center Surfing Spot (North)"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Kindle Road North Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Mt. Ember
        set_rule(world.get_location("Mt. Ember Exterior - Item Near Summit"),
                 lambda state: can_strength(state, player, world) and
                               can_rock_smash(state, player, world))
        set_rule(world.get_location("Mt. Ember Exterior - Eavesdrop on Team Rocket Grunts"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(world.get_location("Mt. Ember Summit - Legendary Pokemon"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Exterior South Strength Boulders"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B2F West Strength Boulders"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B2F East Strength Boulders"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southwest)"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southeast)"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B3F Southwest Strength Boulder (Northwest)"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B3F Southwest Strength Boulder (Southeast)"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B3F Southeast Strength Boulder (Northwest)"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Mt. Ember Ruby Path B3F Southeast Strength Boulder (Southwest)"),
                 lambda state: can_strength(state, player, world))

        # Two Island Town
        set_rule(world.get_location("Two Island Town - Item Behind Cuttable Tree"),
                 lambda state: can_cut(state, player, world))
        set_rule(world.get_location("Two Island Game Corner - Lostelle's Dad Gift (Deliver Meteorite)"),
                 lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player))
        set_rule(world.get_location("Two Island Town - Market Stall Item 4"),
                 lambda state: state.has_all(["Rescue Lostelle", "Defeat Champion"], player))
        set_rule(world.get_location("Two Island Game Corner - Lostelle's Dad's Delivery"),
                 lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player))

        # Cape Brink
        set_rule(world.get_entrance("Cape Brink Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Three Island Town
        set_rule(world.get_location("Three Island Town - Item Behind East Fence"),
                 lambda state: can_cut(state, player, world))

        # Bond Bridge
        set_rule(world.get_entrance("Bond Bridge Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Berry Forest
        set_rule(world.get_location("Berry Forest - Item Past Southwest Pond"),
                 lambda state: can_cut(state, player, world))
        set_rule(world.get_entrance("Berry Forest Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Four Island Town
        set_rule(world.get_location("Four Island Town - Beach Item"),
                 lambda state: can_rock_smash(state, player, world))
        set_rule(world.get_entrance("Four Island Town Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Four Island Town Near Cave Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Icefall Cave
        set_rule(world.get_entrance("Icefall Cave Front South Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Icefall Cave Front Waterfall Ascend"),
                 lambda state: can_waterfall(state, player, world))
        set_rule(world.get_entrance("Icefall Cave Front Waterfall Drop"),
                 lambda state: can_waterfall(state, player, world))
        set_rule(world.get_entrance("Icefall Cave Front Center Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Icefall Cave Front North Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Icefall Cave Back Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Five Island Town
        set_rule(world.get_entrance("Five Island Town Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Five Isle Meadow
        set_rule(world.get_location("Five Isle Meadow - Item Behind Cuttable Tree"),
                 lambda state: can_cut(state, player, world))
        set_rule(world.get_entrance("Five Isle Meadow Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Rocket Warehouse"),
                 lambda state: state.has_all(["Learn Goldeen Need Log", "Learn Yes Nah Chansey"], player))

        # Memorial Pillar
        set_rule(world.get_location("Memorial Pillar - Memorial Man Gift"),
                 lambda state: state.has("Lemonade", player))

        # Resort Gorgeous
        set_rule(world.get_entrance("Resort Gorgeous Near Resort Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Resort Gorgeous Near Cave Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Water Path
        set_rule(world.get_entrance("Water Path South Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Water Path North Surfing Spot (South)"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Water Path North Surfing Spot (North)"),
                 lambda state: can_surf(state, player, world))

        # Ruin Valley
        set_rule(world.get_location("Ruin Valley - Plateau Item"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_location("Ruin Valley - Southwest Item"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_location("Ruin Valley - Southeast Item"),
                 lambda state: can_strength(state, player, world))
        set_rule(world.get_entrance("Ruin Valley Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Dotted Hole"),
                 lambda state: state.has("Help Lorelei", player) and
                               can_cut(state, player, world))

        # Green Path
        set_rule(world.get_entrance("Green Path West Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Outcast Island
        set_rule(world.get_entrance("Outcast Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Seven Island Town
        set_rule(world.get_location("Seven Island Town - Scientist Gift 1 (Trade Scanner)"),
                 lambda state: state.has("Scanner", player))
        set_rule(world.get_location("Seven Island Town - Scientist Gift 2 (Trade Scanner)"),
                 lambda state: state.has("Scanner", player))

        # Sevault Canyon
        set_rule(world.get_location("Sevault Canyon - Item Behind Smashable Rocks"),
                 lambda state: can_strength(state, player, world) and
                               can_rock_smash(state, player, world))

        # Tanoby Key
        set_rule(world.get_location("Tanoby Key - Solve Puzzle"),
                 lambda state: can_strength(state, player, world))

        # Tanoby Ruins
        set_rule(world.get_location("Tanoby Ruins - Island Item"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Monean Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Liptoo Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Weepth Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Dilford Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Scufib Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Rixy Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Viapos Chamber - Land Encounter 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_entrance("Tanoby Ruins Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Viapois Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Rixy Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Scufib Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Dilford Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Weepth Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Liptoo Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Tanoby Ruins Monean Island Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Trainer Tower
        set_rule(world.get_entrance("Trainer Tower Exterior South Surfing Spot"),
                 lambda state: can_surf(state, player, world))
        set_rule(world.get_entrance("Trainer Tower Exterior North Surfing Spot"),
                 lambda state: can_surf(state, player, world))

        # Indigo Plateau
        set_rule(world.get_location("Champion's Room - Champion Rematch Battle"),
                 lambda state: can_challenge_elite_four_rematch(state, player, options))


def set_hidden_item_rules(world: "PokemonFRLGWorld"):
    player = world.player

    # Viridian Gym
    set_rule(world.get_location("Viridian Gym - Hidden Item Under Giovanni"),
             lambda state: state.has("Itemfinder", player))

    # Route 10
    set_rule(world.get_location("Route 10 - Hidden Item Behind Cuttable Tree"),
             lambda state: can_cut(state, player, world))

    # Celadon City
    set_rule(world.get_location("Celadon Game Corner - Northwest Hidden Item"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - North Hidden Item (Left)"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - North Hidden Item (Right)"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - Northeast Hidden Item"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - West Hidden Item"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - Center Hidden Item"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - East Hidden Item (Left)"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - East Hidden Item (Right)"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - Southwest Hidden Item"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - South Hidden Item (Left)"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - South Hidden Item (Right)"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Celadon Game Corner - Southeast Hidden Item"),
             lambda state: state.has("Coin Case", player))

    # Pokemon Tower
    set_rule(world.get_location("Pokemon Tower 7F - Hidden Item Under Mr. Fuji"),
             lambda state: state.has("Itemfinder", player))

    # Route 12
    set_rule(world.get_location("Route 12 - Hidden Item Under Snorlax"),
             lambda state: state.has("Itemfinder", player))

    # Route 16
    set_rule(world.get_location("Route 16 - Hidden Item Under Snorlax"),
             lambda state: state.has("Itemfinder", player))

    # Navel Rock
    set_rule(world.get_location("Navel Rock - Hidden Item Near Ho-Oh"),
             lambda state: state.has("Itemfinder", player))

    if not world.options.kanto_only:
        # Cape Brink
        set_rule(world.get_location("Cape Brink - Hidden Item Across Pond"),
                 lambda state: state.has("Itemfinder", player))

        # Three Island Town
        set_rule(world.get_location("Three Island Town - Hidden Item Behind West Fence"),
                 lambda state: can_cut(state, player, world))

    # Add rules for hidden items
    if world.options.itemfinder_required != ItemfinderRequired.option_off:
        for location in world.multiworld.get_locations(player):
            assert isinstance(location, PokemonFRLGLocation)
            if location.category in [LocationCategory.HIDDEN_ITEM, LocationCategory.HIDDEN_ITEM_RECURRING]:
                add_rule(location, lambda state: state.has("Itemfinder", player))


def set_extra_key_item_rules(world: "PokemonFRLGWorld"):
    player = world.player

    # Cerulean City
    set_rule(world.get_location("Cerulean Gym - Hidden Item in Water"),
             lambda state: can_surf(state, player, world) and
                           state.has("Itemfinder", player))


def set_trainersanity_rules(world: "PokemonFRLGWorld"):
    player = world.player
    options = world.options

    # Route 22
    set_rule(world.get_location("Route 22 - Early Rival Reward"),
             lambda state: state.has("Deliver Oak's Parcel", player))
    set_rule(world.get_location("Route 22 - Late Rival Reward"),
             lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player))

    # Route 8
    set_rule(world.get_location("Route 8 - Twins Eli & Anne Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Route 12
    set_rule(world.get_location("Route 12 - Young Couple Gia & Jes Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Route 14
    set_rule(world.get_location("Route 14 - Twins Kiri & Jan Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Route 15
    set_rule(world.get_location("Route 15 - Crush Kin Ron & Mya Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Route 16
    set_rule(world.get_location("Route 16 - Young Couple Lea & Jed Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Route 19
    set_rule(world.get_location("Route 19 - Sis and Bro Lia & Luc Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Route 21
    set_rule(world.get_location("Route 21 - Sis and Bro Lil & Ian Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    # Victory Road
    set_rule(world.get_location("Victory Road 3F - Cool Couple Ray & Tyra Reward"),
             lambda state: state.has_any(world.repeatable_pokemon, player))

    if not options.kanto_only:
        # Indigo Plateau
        set_rule(world.get_location("Lorelei's Room - Elite Four Lorelei Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state, player, options))
        set_rule(world.get_location("Bruno's Room - Elite Four Bruno Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state, player, options))
        set_rule(world.get_location("Agatha's Room - Elite Four Agatha Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state, player, options))
        set_rule(world.get_location("Lance's Room - Elite Four Lance Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state, player, options))
        set_rule(world.get_location("Champion's Room - Champion Rematch Reward"),
                 lambda state: can_challenge_elite_four_rematch(state, player, options))

        # Kindle Road
        set_rule(world.get_location("Kindle Road - Crush Kin Mik & Kia Reward"),
                 lambda state: state.has_any(world.repeatable_pokemon, player))

        # Mt. Ember
        set_rule(world.get_location("Mt. Ember Exterior - Team Rocket Grunt Reward (Left)"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(world.get_location("Mt. Ember Exterior - Team Rocket Grunt Reward (Right)"),
                 lambda state: state.has("Deliver Meteorite", player))

        # Bond Bridge
        set_rule(world.get_location("Bond Bridge - Twins Joy & Meg Reward"),
                 lambda state: state.has_any(world.repeatable_pokemon, player))

        # Water Path
        set_rule(world.get_location("Water Path - Twins Miu & Mia Reward"),
                 lambda state: state.has_any(world.repeatable_pokemon, player))

        # Outcast Island
        set_rule(world.get_location("Outcast Island - Sis and Bro Ava & Geb Reward"),
                 lambda state: state.has_any(world.repeatable_pokemon, player))

        # Canyon Entrance
        set_rule(world.get_location("Canyon Entrance - Young Couple Eve & Jon Reward"),
                 lambda state: state.has_any(world.repeatable_pokemon, player))

        # Sevault Canyon
        set_rule(world.get_location("Sevault Canyon - Cool Couple Lex & Nya Reward"),
                 lambda state: state.has_any(world.repeatable_pokemon, player))


def set_dexsanity_rules(world: "PokemonFRLGWorld"):
    for i in range(NUM_REAL_SPECIES):
        species = data.species[NATIONAL_ID_TO_SPECIES_ID[i + 1]]
        set_rule(world.get_location(f"Pokedex - {species.name}"),
                 lambda state, pokemon=species.name: has_pokemon(state, world.player, pokemon))


def set_famesanity_rules(world: "PokemonFRLGWorld"):
    player = world.player
    options = world.options

    # Pallet Town
    set_rule(world.get_location("Professor Oak's Lab - Oak's Aide M Info (Right)"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Professor Oak's Lab - Oak Info"),
             lambda state: state.has("Oak's Parcel", player))
    set_rule(world.get_location("Professor Oak's Lab - Oak's Aide M Info (Left)"),
             lambda state: post_game_gossipers(state, player, options))

    # Viridian City
    set_rule(world.get_location("Viridian Gym - Gym Guy Info"),
             lambda state: state.has("Defeat Giovanni", player))

    # Cerulean City
    set_rule(world.get_location("Cerulean Pokemon Center 1F - Bookshelf Info"),
             lambda state: post_game_gossipers(state, player, options))

    # Vermilion City
    set_rule(world.get_location("Pokemon Fan Club - Worker Info"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Vermilion Pokemon Center 1F - Bookshelf Info"),
             lambda state: state.has("Defeat Lt. Surge", player))

    # Lavender Town
    set_rule(world.get_location("Lavender Pokemon Center 1F - Balding Man Info"),
             lambda state: post_game_gossipers(state, player, options))

    # Celadon City
    set_rule(world.get_location("Celadon Condominiums 1F - Tea Woman Info"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Celadon Condominiums 2F - Bookshelf Info"),
             lambda state: state.has("Defeat Erika", player))
    set_rule(world.get_location("Celadon Department Store 2F - Woman Info"),
             lambda state: post_game_gossipers(state, player, options))

    # Fuchsia City
    set_rule(world.get_location("Fuchsia City - Koga's Daughter Info"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Safari Zone Warden's House - Bookshelf Info"),
             lambda state: state.has("Defeat Koga", player))

    # Saffron City
    set_rule(world.get_location("Pokemon Trainer Fan Club - Bookshelf Info"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Saffron City - Battle Girl Info"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Saffron Pokemon Center 1F - Bookshelf Info"),
             lambda state: state.has("Defeat Sabrina", player))

    # Cinnabar Island
    set_rule(world.get_location("Cinnabar Pokemon Center 1F - Bookshelf Info"),
             lambda state: post_game_gossipers(state, player, options))

    # Indigo Plateau
    set_rule(world.get_location("Indigo Plateau Pokemon Center 1F - Black Belt Info 1"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Indigo Plateau Pokemon Center 1F - Black Belt Info 2"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Indigo Plateau Pokemon Center 1F - Bookshelf Info"),
             lambda state: post_game_gossipers(state, player, options))
    set_rule(world.get_location("Indigo Plateau Pokemon Center 1F - Cooltrainer Info"),
             lambda state: post_game_gossipers(state, player, options))

    if not options.kanto_only:
        # One Island Town
        set_rule(world.get_location("One Island Pokemon Center 1F - Celio Info 1"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))
        set_rule(world.get_location("One Island Pokemon Center 1F - Celio Info 2"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))
        set_rule(world.get_location("One Island Pokemon Center 1F - Celio Info 3"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))

        # Ember Spa
        set_rule(world.get_location("Ember Spa - Black Belt Info"),
                 lambda state: post_game_gossipers(state, player, options))

        # Two Island Town
        set_rule(world.get_location("Two Island Town - Beauty Info"),
                 lambda state: state.has_all(["Rescue Lostelle", "Defeat Champion"], player))

        # Four Island Town
        set_rule(world.get_location("Four Island Town - Old Woman Info"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))

        # Five Island Town
        set_rule(world.get_location("Five Island Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state, player, options))

        # Rocket Warehouse
        set_rule(world.get_location("Rocket Warehouse - Scientist Gideon Info"),
                 lambda state: state.has("Restore Pokemon Network Machine", player))

        # Water Labyrinth
        if options.pokemon_request_locations:
            set_rule(world.get_location("Water Labyrinth - Gentleman Info"),
                     lambda state: state.has_any(["Togepi", "Togetic"], player))

        # Seven Island
        set_rule(world.get_location("Seven Island Pokemon Center 1F - Bookshelf Info"),
                 lambda state: post_game_gossipers(state, player, options))

    # Add rules for fame checker locations
    if world.options.fame_checker_required:
        for location in world.multiworld.get_locations(player):
            assert isinstance(location, PokemonFRLGLocation)
            if location.category == LocationCategory.FAMESANITY:
                add_rule(location, lambda state: state.has("Fame Checker", player))


def set_pokemon_request_rules(world: "PokemonFRLGWorld"):
    player = world.player

    # Route 12
    set_rule(world.get_location("Route 12 Fishing House - Fishing Guru Gift (Show Magikarp)"),
             lambda state: state.has("Magikarp", player))

    if not world.options.kanto_only:
        # Resort Gorgeous
        set_rule(world.get_location("Resort Gorgeous House - Selphy Gift (Show Pokemon)"),
                 lambda state: state.has_all(["Rescue Selphy", data.species[world.resort_gorgeous_mon].name], player))

        # Water Path
        set_rule(world.get_location("Water Path Heracross Woman's House - Woman Gift (Show Heracross)"),
                 lambda state: state.has("Heracross", player))


def set_split_tea_rules(world: "PokemonFRLGWorld"):
    player = world.player

    # Celadon City
    set_rule(world.get_location("Celadon Condominiums 1F - Brock Gift"),
             lambda state: state.has("Defeat Brock", player))
    set_rule(world.get_location("Celadon Condominiums 1F - Misty Gift"),
             lambda state: state.has("Defeat Misty", player))
    set_rule(world.get_location("Celadon Condominiums 1F - Erika Gift"),
             lambda state: state.has("Defeat Erika", player))


def set_split_pass_rules(world: "PokemonFRLGWorld"):
    player = world.player

    # Cinnabar Island
    set_rule(world.get_location("Cinnabar Pokemon Center 1F - Bill Gift"),
             lambda state: state.has("Defeat Blaine", player))

    # One Island Town
    set_rule(world.get_location("One Island Pokemon Center 1F - Celio Gift (Deliver Sapphire)"),
             lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"],
                                         player))

    # Three Island Town
    set_rule(world.get_location("Lostelle's House - Lostelle Gift"),
             lambda state: state.has("Deliver Meteorite", player))

    # Dotted Hole
    set_rule(world.get_location("Dotted Hole 1F - Dropped Item"),
             lambda state: state.has("Learn Yes Nah Chansey", player))


def set_scaling_rules(world: "PokemonFRLGWorld"):
    player = world.player

    # Route 22
    set_rule(world.get_location("Route 22 Early Rival"),
             lambda state: state.has("Deliver Oak's Parcel", player))
    set_rule(world.get_location("Route 22 Late Rival"),
             lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player))

    # Celadon City
    set_rule(world.get_location("Prize Pokemon 1"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Prize Pokemon 2"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Prize Pokemon 3"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Prize Pokemon 4"),
             lambda state: state.has("Coin Case", player))
    set_rule(world.get_location("Prize Pokemon 5"),
             lambda state: state.has("Coin Case", player))

    # Cinnabar Island
    set_rule(world.get_location("Gift Omanyte"),
             lambda state: state.has("Helix Fossil", player))
    set_rule(world.get_location("Gift Kabuto"),
             lambda state: state.has("Dome Fossil", player))
    set_rule(world.get_location("Gift Aerodactyl"),
             lambda state: state.has("Old Amber", player))

    if not world.options.kanto_only:
        # Mt. Ember
        set_rule(world.get_location("Team Rocket Grunt 43"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(world.get_location("Team Rocket Grunt 44"),
                 lambda state: state.has("Deliver Meteorite", player))
        set_rule(world.get_location("Legendary Moltres"),
                 lambda state: can_strength(state, player, world))

        # Indigo Plateau
        set_rule(world.get_location("Elite Four Rematch"),
                 lambda state: state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], player))

        # Tanoby Ruins
        set_rule(world.get_location("Monean Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Liptoo Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Weepth Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Dilford Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Scufib Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Rixy Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))
        set_rule(world.get_location("Viapos Chamber Land Scaling 1"),
                 lambda state: state.has("Unlock Ruins", player))


def set_rules(world: "PokemonFRLGWorld") -> None:
    options = world.options

    set_default_rules(world)
    if options.shuffle_hidden != ShuffleHiddenItems.option_off:
        set_hidden_item_rules(world)
    if options.extra_key_items:
        set_extra_key_item_rules(world)
    if options.trainersanity != Trainersanity.special_range_names["none"]:
        set_trainersanity_rules(world)
    if options.dexsanity != Dexsanity.special_range_names["none"]:
        set_dexsanity_rules(world)
    if options.famesanity:
        set_famesanity_rules(world)
    if options.pokemon_request_locations:
        set_pokemon_request_rules(world)
    if options.split_teas:
        set_split_tea_rules(world)
    if ((options.island_passes == SeviiIslandPasses.option_split or
         options.island_passes == SeviiIslandPasses.option_progressive_split) and
            not options.kanto_only):
        set_split_pass_rules(world)
    if options.level_scaling != LevelScaling.option_off:
        set_scaling_rules(world)
