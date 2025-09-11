from enum import IntEnum
from typing import TYPE_CHECKING, List, Set
from BaseClasses import Entrance, EntranceType
from entrance_rando import (ERPlacementState, EntranceRandomizationError, disconnect_entrance_for_randomization,
                            randomize_entrances)
from .options import DungeonEntranceShuffle

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

MAX_GER_ATTEMPTS = 20

SINGLE_DUNGEON_ENTRANCES = ["Vermilion Harbor", "Pokemon Tower", "Rocket Hideout", "Safari Zone Entrance", "Silph Co.",
                            "Pokemon Mansion", "Cerulean Cave", "Navel Rock", "Mt. Ember", "Berry Forest",
                            "Icefall Cave", "Rocket Warehouse", "Lost Cave", "Dotted Hole", "Altering Cave",
                            "Viapois Chamber", "Rixy Chamber", "Scufib Chamber", "Dilford Chamber", "Weepth Chamber",
                            "Liptoo Chamber", "Monean Chamber"]

SINGLE_DUNGEON_EXITS = ["S.S. Anne Exterior Exit", "Pokemon Tower 1F Exit", "Rocket Hideout B1F Northwest Stairs",
                        "Safari Zone Entrance Exit", "Silph Co. 1F Exit", "Pokemon Mansion 1F Exit (West)",
                        "Cerulean Cave 1F Exit", "Navel Rock 1F Exit", "Mt. Ember Exterior Exit", "Berry Forest Exit",
                        "Icefall Cave Front Exit (South)", "Rocket Warehouse Exit", "Lost Cave 1F Exit",
                        "Dotted Hole 1F Exit", "Altering Cave Exit", "Viapois Chamber Exit", "Rixy Chamber Exit",
                        "Scufib Chamber Exit", "Dilford Chamber Exit", "Weepth Chamber Exit", "Liptoo Chamber Exit",
                        "Monean Chamber Exit"]

MULTI_DUNGEON_ENTRANCES = ["Viridian Forest South Gate Exit (North)", "Viridian Forest North Gate Exit (South)",
                           "Mt. Moon (West)", "Mt. Moon (East)", "Diglett's Cave North Entrance",
                           "Diglett's Cave South Entrance", "Rock Tunnel (North)", "Rock Tunnel (South)",
                           "Power Plant (Front)", "Power Plant (Back)", "Seafoam Islands (North)",
                           "Seafoam Islands (South)", "Victory Road (West)", "Victory Road (East)",
                           "Pattern Bush (West)", "Pattern Bush (East)"]

MULTI_DUNGEON_EXITS = ["Viridian Forest Exit (South)", "Viridian Forest Exit (North)", "Mt. Moon 1F Exit",
                       "Mt. Moon B1F (Fourth Tunnel) East Ladder", "Diglett's Cave North Entrance Exit",
                       "Diglett's Cave South Entrance Exit", "Rock Tunnel 1F North Ladder", "Rock Tunnel 1F Exit",
                       "Power Plant Exit (Front)", "Power Plant Exit (Back)", "Seafoam Islands 1F Exit (West)",
                       "Seafoam Islands 1F Exit (East)", "Victory Road 1F Exit", "Victory Road 2F Exit",
                       "Pattern Bush Exit (West)", "Pattern Bush Exit (East)"]

MULTI_DUNGEON_PAIRS = {
    "Viridian Forest South Gate Exit (North)": "Viridian Forest North Gate Exit (South)",
    "Mt. Moon (West)": "Mt. Moon (East)",
    "Diglett's Cave North Entrance": "Diglett's Cave South Entrance",
    "Rock Tunnel (North)": "Rock Tunnel (South)",
    "Power Plant (Front)": "Power Plant (Back)",
    "Seafoam Islands (North)": "Seafoam Islands (South)",
    "Victory Road (West)": "Victory Road (East)",
    "Pattern Bush (West)": "Pattern Bush (East)",
    "Viridian Forest Exit (South)": "Viridian Forest Exit (North)",
    "Mt. Moon 1F Exit": "Mt. Moon B1F (Fourth Tunnel) East Ladder",
    "Diglett's Cave North Entrance Exit": "Diglett's Cave South Entrance Exit",
    "Rock Tunnel 1F North Ladder": "Rock Tunnel 1F Exit",
    "Power Plant Exit (Front)": "Power Plant Exit (Back)",
    "Seafoam Islands 1F Exit (West)": "Seafoam Islands 1F Exit (East)",
    "Victory Road 1F Exit": "Victory Road 2F Exit",
    "Pattern Bush Exit (West)": "Pattern Bush Exit (East)"
}
MULTI_DUNGEON_PAIRS_REVERSE = {k: v for v, k in MULTI_DUNGEON_PAIRS.items()}
DUNGEON_PAIRS = MULTI_DUNGEON_PAIRS | MULTI_DUNGEON_PAIRS_REVERSE


class EntranceGroups(IntEnum):
    UNSHUFFLED = 0
    DUNGEON_ENTRANCE = 1
    SINGLE_DUNGEON_ENTRANCE = 2
    MULTI_DUNGEON_ENTRANCE = 3
    DUNGEON_EXIT = 4
    SINGLE_DUNGEON_EXIT = 5
    MULTI_DUNGEON_EXIT = 6


DUNGEON_GROUP_LOOKUP = {
    EntranceGroups.DUNGEON_ENTRANCE: [EntranceGroups.DUNGEON_EXIT],
    EntranceGroups.SINGLE_DUNGEON_ENTRANCE: [EntranceGroups.SINGLE_DUNGEON_EXIT],
    EntranceGroups.MULTI_DUNGEON_ENTRANCE: [EntranceGroups.MULTI_DUNGEON_EXIT],
    EntranceGroups.DUNGEON_EXIT: [EntranceGroups.DUNGEON_ENTRANCE],
    EntranceGroups.SINGLE_DUNGEON_EXIT: [EntranceGroups.SINGLE_DUNGEON_ENTRANCE],
    EntranceGroups.MULTI_DUNGEON_EXIT: [EntranceGroups.MULTI_DUNGEON_ENTRANCE]
}


def shuffle_entrances(world: "PokemonFRLGWorld"):
    def get_entrance_safe(entrance_name: str) -> Entrance | None:
        try:
            entrance = world.get_entrance(entrance_name)
        except KeyError:
            return None
        return entrance

    for entrance_name in SINGLE_DUNGEON_ENTRANCES:
        entrance = get_entrance_safe(entrance_name)
        if entrance is None:
            continue
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_ENTRANCE
        else:
            entrance.randomization_group = EntranceGroups.SINGLE_DUNGEON_ENTRANCE
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)
    for entrance_name in SINGLE_DUNGEON_EXITS:
        entrance = get_entrance_safe(entrance_name)
        if entrance is None:
            continue
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_EXIT
        else:
            entrance.randomization_group = EntranceGroups.SINGLE_DUNGEON_EXIT
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)
    for entrance_name in MULTI_DUNGEON_ENTRANCES:
        entrance = get_entrance_safe(entrance_name)
        if entrance is None:
            continue
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_ENTRANCE
        else:
            entrance.randomization_group = EntranceGroups.MULTI_DUNGEON_ENTRANCE
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)
    for entrance_name in MULTI_DUNGEON_EXITS:
        entrance = get_entrance_safe(entrance_name)
        if entrance is None:
            continue
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_EXIT
        else:
            entrance.randomization_group = EntranceGroups.MULTI_DUNGEON_EXIT
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)

    available_shuffle_types: Set[EntranceGroups] = set()
    if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
        available_shuffle_types.add(EntranceGroups.DUNGEON_ENTRANCE)
        available_shuffle_types.add(EntranceGroups.DUNGEON_EXIT)
    else:
        available_shuffle_types.add(EntranceGroups.SINGLE_DUNGEON_ENTRANCE)
        available_shuffle_types.add(EntranceGroups.SINGLE_DUNGEON_EXIT)
        available_shuffle_types.add(EntranceGroups.MULTI_DUNGEON_ENTRANCE)
        available_shuffle_types.add(EntranceGroups.MULTI_DUNGEON_EXIT)

    world.logic.randomizing_entrances = True
    for i in range(MAX_GER_ATTEMPTS):
        try:
            if world.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_simple:
                world.er_placement_state = randomize_entrances(world, True, DUNGEON_GROUP_LOOKUP)
            else:
                world.er_placement_state = randomize_entrances(world, True, DUNGEON_GROUP_LOOKUP,
                                                               on_connect=connect_simple_entrances)
            world.er_spoiler_names.extend(SINGLE_DUNGEON_ENTRANCES + MULTI_DUNGEON_ENTRANCES)
            world.logic.randomizing_entrances = False
            world.logic.guaranteed_hm_access = False
            # Make the Pokemon Mansion other exit match the shuffled exit
            cinnabar_region = world.get_region("Cinnabar Island")
            mansion_shuffled_entrance = world.get_entrance("Pokemon Mansion 1F Exit (West)")
            mansion_other_entrance = world.get_entrance("Pokemon Mansion 1F Exit (East)")
            cinnabar_region.entrances.remove(mansion_other_entrance)
            mansion_other_entrance.connected_region = mansion_shuffled_entrance.connected_region
            mansion_shuffled_entrance.connected_region.entrances.append(mansion_other_entrance)
            for source, dest in world.er_placement_state.pairings:
                if source == "Pokemon Mansion 1F Exit (West)":
                    world.er_placement_state.pairings.append((mansion_other_entrance.name, dest))
                    break
            break
        except EntranceRandomizationError as error:
            if i >= MAX_GER_ATTEMPTS - 1:
                raise EntranceRandomizationError(f"Pokemon FRLG: GER failed for player {world.player} "
                                                 f"({world.player_name}) after {MAX_GER_ATTEMPTS} attempts. Final "
                                                 f"error here: \n\n{error}")
            if i > 1:
                world.logic.guaranteed_hm_access = True
            for region in world.get_regions():
                for exit in region.get_exits():
                    if (exit.randomization_group in available_shuffle_types and
                            exit.parent_region and
                            exit.connected_region):
                        exit.connected_entrance_name = None
                        disconnect_entrance_for_randomization(exit, exit.randomization_group)


def connect_simple_entrances(er_state: ERPlacementState,
                             placed_exits: List[Entrance],
                             paired_entrances: List[Entrance]):
    if placed_exits[0].name not in DUNGEON_PAIRS or paired_entrances[0].name not in DUNGEON_PAIRS:
        return False

    entrance = er_state.world.get_entrance(DUNGEON_PAIRS[placed_exits[0].name])
    exit = er_state.entrance_lookup.find_target(DUNGEON_PAIRS[paired_entrances[0].name])
    er_state.connect(entrance, exit)
    return True
