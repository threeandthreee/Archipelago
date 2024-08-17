"""
Classes and functions related to creating a ROM patch
"""
import os
import struct
import logging
import zipfile
from typing import TYPE_CHECKING, Dict, List, Tuple, Union
from worlds.Files import APContainer, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .data import data, TrainerPokemonDataTypeEnum
from .items import reverse_offset_item_value
from .locations import reverse_offset_flag
from .options import ItemfinderRequired, ShuffleHiddenItems, TmTutorCompatibility, ViridianCityRoadblock
from .pokemon import STARTER_INDEX, randomize_tutor_moves
from .util import bool_array_to_int, encode_string
if TYPE_CHECKING:
    from . import PokemonFRLGWorld


class FRLGContainer(APContainer):
    game = "Pokemon FireRed and LeafGreen"

    def __init__(self, patch_path: str, output_path: str, player=None, player_name: str = "", server: str = ""):
        self.patch_path = patch_path
        container_path = output_path + ".zip"
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for file in os.scandir(self.patch_path):
            opened_zipfile.write(file.path, arcname=file.name)
        super().write_contents(opened_zipfile)


class PokemonFireRedProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = "e26ee0d44e809351c8ce2d73c7400cdd"
    patch_file_ending = ".apfirered"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_firered.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.firered_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


class PokemonFireRedRev1ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = "51901a6e40661b3914aa333c802e24e8"
    patch_file_ending = ".apfireredrev1"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_firered_rev1.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.firered_rev1_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


class PokemonLeafGreenProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = "612ca9473451fa42b51d1711031ed5f6"
    patch_file_ending = ".apleafgreen"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_leafgreen.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.leafgreen_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


class PokemonLeafGreenRev1ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = "9d33a02159e018d09073e700e1fd10fd"
    patch_file_ending = ".apleafgreenrev1"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_leafgreen_rev1.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.leafgreen_rev1_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def write_tokens(world: "PokemonFRLGWorld",
                 patch: Union[PokemonFireRedProcedurePatch,
                              PokemonFireRedRev1ProcedurePatch,
                              PokemonLeafGreenProcedurePatch,
                              PokemonLeafGreenRev1ProcedurePatch]) -> None:
    game_version = world.options.game_version.current_key
    if type(patch) is PokemonFireRedProcedurePatch or type(patch) is PokemonLeafGreenProcedurePatch:
        game_version_revision = game_version
    else:
        game_version_revision = f'{game_version}_rev1'

    # Set free fly location
    if world.options.free_fly_location:
        patch.write_token(
            APTokenTypes.WRITE,
            data.rom_addresses[game_version_revision]["gArchipelagoOptions"] + 0x18,
            struct.pack("<B", world.free_fly_location_id)
        )

    # Set item values
    location_info: List[Tuple[int, int, str]] = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        item_address = location.item_address[game_version_revision]

        if location.item.player == world.player:
            if type(item_address) is int:
                patch.write_token(
                    APTokenTypes.WRITE,
                    item_address,
                    struct.pack("<H", reverse_offset_item_value(location.item.code))
                )
            elif type(item_address) is list:
                for address in item_address:
                    patch.write_token(
                        APTokenTypes.WRITE,
                        address,
                        struct.pack("<H", reverse_offset_item_value(location.item.code))
                    )
        else:
            if type(item_address) is int:
                patch.write_token(
                    APTokenTypes.WRITE,
                    item_address,
                    struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])
                )
            elif type(item_address) is list:
                for address in item_address:
                    patch.write_token(
                        APTokenTypes.WRITE,
                        address,
                        struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])
                    )

        # Creates a list of item information to store in tables later. Those tables are used to display the item and
        # player name in a text box. In the case of not enough space, the game will default to "found an ARCHIPELAGO
        # ITEM"
        location_info.append((reverse_offset_flag(location.address), location.item.player, location.item.name))

    if world.options.trainersanity:
        for trainer in ["RIVAL_OAKS_LAB", "RIVAL_ROUTE22_EARLY", "RIVAL_CERULEAN", "RIVAL_SS_ANNE",
                        "RIVAL_POKEMON_TOWER", "RIVAL_SILPH", "RIVAL_ROUTE22_LATE", "CHAMPION_FIRST"]:
            location = world.multiworld.get_location(data.locations[f"TRAINER_{trainer}_BULBASAUR_REWARD"].name,
                                                     world.player)
            alternates = [
                f"TRAINER_{trainer}_CHARMANDER",
                f"TRAINER_{trainer}_SQUIRTLE"
            ]

            location_info.extend((
                data.constants["TRAINER_FLAGS_START"] + data.constants[alternate],
                location.item.player,
                location.item.name
            ) for alternate in alternates)

    player_name_ids: Dict[str, int] = {world.player_name: 0}
    item_name_offsets: Dict[str, int] = {}
    next_item_name_offset = 0
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        player_name = world.multiworld.get_player_name(item_player)

        if player_name not in player_name_ids:
            # Only space for 50 player names
            if len(player_name_ids) >= 50:
                continue

            player_name_ids[player_name] = len(player_name_ids)
            player_name_address = data.rom_addresses[game_version_revision]["gArchipelagoPlayerNames"]
            for j, b in enumerate(encode_string(player_name, 17)):
                patch.write_token(
                    APTokenTypes.WRITE,
                    player_name_address + (player_name_ids[player_name] * 17) + j,
                    struct.pack("<B", b)
                )

        if item_name not in item_name_offsets:
            if len(item_name) > 35:
                item_name = item_name[:34] + "…"

            # Only 36 * 500 bytes for item names
            if next_item_name_offset + len(item_name) + 1 > 36 * 500:
                continue

            item_name_offsets[item_name] = next_item_name_offset
            next_item_name_offset += len(item_name) + 1
            item_name_address = data.rom_addresses[game_version_revision]["gArchipelagoItemNames"]
            patch.write_token(
                APTokenTypes.WRITE,
                item_name_address + (item_name_offsets[item_name]),
                encode_string(item_name) + b"\xFF"
            )

        # There should always be enough space for one entry per location
        name_table_address = data.rom_addresses[game_version_revision]["gArchipelagoNameTable"]
        patch.write_token(
            APTokenTypes.WRITE,
            name_table_address + (i * 5) + 0,
            struct.pack("<H", flag)
        )
        patch.write_token(
            APTokenTypes.WRITE,
            name_table_address + (i * 5) + 2,
            struct.pack("<H", item_name_offsets[item_name])
        )
        patch.write_token(
            APTokenTypes.WRITE,
            name_table_address + (i * 5) + 4,
            struct.pack("<B", player_name_ids[player_name])
        )

    # Set starting items
    start_inventory = world.options.start_inventory.value.copy()

    starting_badges = 0
    if start_inventory.pop("Boulder Badge", 0) > 0:
        starting_badges |= (1 << 0)
    if start_inventory.pop("Cascade Badge", 0) > 0:
        starting_badges |= (1 << 1)
    if start_inventory.pop("Thunder Badge", 0) > 0:
        starting_badges |= (1 << 2)
    if start_inventory.pop("Rainbow Badge", 0) > 0:
        starting_badges |= (1 << 3)
    if start_inventory.pop("Soul Badge", 0) > 0:
        starting_badges |= (1 << 4)
    if start_inventory.pop("Marsh Badge", 0) > 0:
        starting_badges |= (1 << 5)
    if start_inventory.pop("Volcano Badge", 0) > 0:
        starting_badges |= (1 << 6)
    if start_inventory.pop("Earth Badge", 0) > 0:
        starting_badges |= (1 << 7)

    pc_slots: List[Tuple[str, int]] = []
    for item, quantity in start_inventory.items():
        if len(pc_slots) >= 19:
            break
        if quantity > 999:
            logging.info(
                f"{world.multiworld.get_file_safe_player_name(world.player)} cannot have more than 999 of an item"
                f"Changing amount to 999"
            )
            quantity = 999
        pc_slots.append([item, quantity])

    for i, slot in enumerate(pc_slots, 1):
        address = data.rom_addresses[game_version_revision]["gNewGamePCItems"] + (i * 4)
        item = reverse_offset_item_value(world.item_name_to_id[slot[0]])
        patch.write_token(APTokenTypes.WRITE, address, struct.pack("<H", item))
        patch.write_token(APTokenTypes.WRITE, address + 2, struct.pack("<H", slot[1]))

    # Set species data
    _set_species_info(world, patch, game_version_revision)

    # Set wild encounters
    _set_wild_encounters(world, patch, game_version, game_version_revision)

    # Set starters
    _set_starters(world, patch, game_version_revision)

    # Set legendaries
    _set_legendaries(world, patch, game_version, game_version_revision)

    # Set misc pokemon
    _set_misc_pokemon(world, patch, game_version, game_version_revision)

    # Set trainer parties
    _set_trainer_parties(world, patch, game_version_revision)

    # Set TM/HM compatability
    _set_tmhm_compatibility(world, patch, game_version_revision)

    # Set TM Moves
    _set_tm_moves(world, patch, game_version_revision)

    # Randomize move tutors
    _randomize_move_tutors(world, patch, game_version_revision)

    # Options
    # struct
    # ArchipelagoOptions
    # {
    # /* 0x00 */ bool8 advanceTextWithHoldA;
    # /* 0x01 */ u8 receivedItemMessageFilter; // 0 = Show All, 1 = Show Progression Only, 2 = Show None
    # /* 0x02 */ bool8 betterShopsEnabled;
    # /* 0x03 */ bool8 reusableTms;
    # /* 0x04 */ bool8 guaranteedCatch;
    #
    # /* 0x05 */ bool8 areTrainersBlind;
    # /* 0x06 */ u16 expMultiplierNumerator;
    # /* 0x08 */ u16 expMultiplierDenominator;
    #
    # /* 0x0A */ bool8 openViridianCity;
    # /* 0x0B */ u8 route3Requirement; // 0 = Open, 1 = Defeat Brock, 2 = Defeat Any Gym Leader,
    #                                     3 = Boulder Badge, 4 = Any Badge
    # /* 0x0C */ bool8 saveBillRequired;
    # /* 0x0D */ bool8 giovanniRequiresGyms;
    # /* 0x0E */ u8 giovanniRequiredCount;
    # /* 0x0F */ bool8 route22GateRequiresGyms;
    # /* 0x10 */ u8 route22GateRequiredCount;
    # /* 0x11 */ bool8 route23GuardRequiresGyms;
    # /* 0x12 */ u8 route23GuardRequiredCount;
    # /* 0x13 */ bool8 eliteFourRequiresGyms;
    # /* 0x14 */ u8 eliteFourRequiredCount;
    # /* 0x15 */ u8 ceruleanCaveRequirement; // 0 = Vanilla, 1 = Become Champion, 2 = Restore Network Center,
    #                                           3 = Badges, 4 = Gyms
    # /* 0x16 */ u8 ceruleanCaveRequiredCount;
    #
    # /* 0x17 */ u8 startingBadges;
    # /* 0x18 */ u8 freeFlyLocation;
    #
    # /* 0x19 */ bool8 itemfinderRequired;
    # /* 0x1A */ bool8 reccuringHiddenItems;
    #
    # /* 0x1B */ u8 oaksAideRequiredCounts[5]; // Route 2, Route 10, Route 11, Route 16, Route 15
    #
    # /* 0x20 */ bool8 isTrainersanity;
    # /* 0x21 */ bool8 extraKeyItems;
    #
    # /* 0x22 */ bool8 removeBadgeRequirement[7]; // Flash, Cut, Fly, Strength, Surf, Rock Smash, Waterfall
    # }
    options_address = data.rom_addresses[game_version_revision]["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if world.options.turbo_a else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x00, struct.pack("<B", turbo_a))

    # Set received item message types
    receive_item_messages = world.options.receive_item_messages.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x01, struct.pack("<B", receive_item_messages))

    # Set better shops
    better_shops = 1 if world.options.better_shops else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x02, struct.pack("<B", better_shops))

    # Set reusable TMs and Move Tutors
    reusable_tm_tutors = 1 if world.options.reusable_tm_tutors else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x03, struct.pack("<B", reusable_tm_tutors))

    # Set guaranteed catch
    guaranteed_catch = 1 if world.options.guaranteed_catch else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x04, struct.pack("<B", guaranteed_catch))

    # Set blind trainers
    blind_trainers = 1 if world.options.blind_trainers else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x05, struct.pack("<B", blind_trainers))

    # Set exp multiplier
    numerator = world.options.exp_modifier.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x06, struct.pack("<H", numerator))
    patch.write_token(APTokenTypes.WRITE, options_address + 0x08, struct.pack("<H", 100))

    # Set Viridian City roadblock
    open_viridian = 1 if world.options.viridian_city_roadblock.value == ViridianCityRoadblock.option_open else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x0A, struct.pack("<B", open_viridian))

    # Set Pewter City roadblock
    route_3_condition = world.options.pewter_city_roadblock.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x0B, struct.pack("<B", route_3_condition))

    # Set Cerulean City roadblocs
    save_bill = 1 if world.options.cerulean_city_roadblocks else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x0C, struct.pack("<B", save_bill))

    # Set Viridian Gym Rrquirement
    viridian_gym_requirement = world.options.viridian_gym_requirement.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x0D, struct.pack("<B", viridian_gym_requirement))

    # Set Viridian Gym count
    viridian_gym_count = world.options.viridian_gym_count.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x0E, struct.pack("<B", viridian_gym_count))

    # Set Route 22 requirement
    route_22_requirement = world.options.route22_gate_requirement.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x0F, struct.pack("<B", route_22_requirement))

    # Set Route 22 count
    route_22_count = world.options.route22_gate_count.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x10, struct.pack("<B", route_22_count))

    # Set Route 23 requirement
    route_23_requirement = world.options.route23_guard_requirement.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x11, struct.pack("<B", route_23_requirement))

    # Set Route 23 count
    route_23_count = world.options.route23_guard_count.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x12, struct.pack("<B", route_23_count))

    # Set Elite Four requirement
    elite_four_requirement = world.options.elite_four_requirement.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x13, struct.pack("<B", elite_four_requirement))

    # Set Elite Four count
    elite_four_count = world.options.elite_four_count.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x14, struct.pack("<B", elite_four_count))

    # Set Cerulean Cave requirement
    cerulean_cave_requirement = world.options.cerulean_cave_requirement.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x15, struct.pack("<B", cerulean_cave_requirement))

    # Set Cerulean Cave count
    cerulean_cave_count = world.options.cerulean_cave_count.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x16, struct.pack("<B", cerulean_cave_count))

    # Set starting badges
    patch.write_token(APTokenTypes.WRITE, options_address + 0x17, struct.pack("<B", starting_badges))

    # Set itemfinder required
    itemfinder_required = 1 if world.options.itemfinder_required.value == ItemfinderRequired.option_required else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x19, struct.pack("<B", itemfinder_required))

    # Set recurring hidden items shuffled
    recurring_hidden_items = 1 if world.options.shuffle_hidden.value == ShuffleHiddenItems.option_all else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x1A, struct.pack("<B", recurring_hidden_items))

    # Set Oak's Aides counts
    oaks_aide_route_2 = world.options.oaks_aide_route_2.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x1B, struct.pack("<B", oaks_aide_route_2))
    oaks_aide_route_10 = world.options.oaks_aide_route_10.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x1C, struct.pack("<B", oaks_aide_route_10))
    oaks_aide_route_11 = world.options.oaks_aide_route_11.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x1D, struct.pack("<B", oaks_aide_route_11))
    oaks_aide_route_16 = world.options.oaks_aide_route_16.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x1E, struct.pack("<B", oaks_aide_route_16))
    oaks_aide_route_15 = world.options.oaks_aide_route_15.value
    patch.write_token(APTokenTypes.WRITE, options_address + 0x1F, struct.pack("<B", oaks_aide_route_15))

    # Set trainersanity
    trainersanity = 1 if world.options.trainersanity else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x20, struct.pack("<B", trainersanity))

    # Set extra key items
    extra_key_items = 1 if world.options.extra_key_items else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x21, struct.pack("<B", extra_key_items))

    # Set remove badge requirements
    hms = ["Flash", "Cut", "Fly", "Strength", "Surf", "Rock Smash", "Waterfall"]
    for i, hm in enumerate(hms):
        remove_badge_requirement = 1 if hm in world.options.remove_badge_requirement.value else 0
        patch.write_token(APTokenTypes.WRITE, options_address + 0x22 + i, struct.pack("<B", remove_badge_requirement))

    # Set slot auth
    patch.write_token(APTokenTypes.WRITE, data.rom_addresses[game_version_revision]["gArchipelagoInfo"], world.auth)

    patch.write_file("token_data.bin", patch.get_token_binary())


def _set_species_info(world: "PokemonFRLGWorld",
                      patch: Union[PokemonFireRedProcedurePatch,
                                   PokemonFireRedRev1ProcedurePatch,
                                   PokemonLeafGreenProcedurePatch,
                                   PokemonLeafGreenRev1ProcedurePatch],
                      game_version_revision: str) -> None:
    for species in world.modified_species.values():
        address = species.address[game_version_revision]

        patch.write_token(APTokenTypes.WRITE, address + 0x06, struct.pack("<B", species.types[0]))
        patch.write_token(APTokenTypes.WRITE, address + 0x07, struct.pack("<B", species.types[1]))
        patch.write_token(APTokenTypes.WRITE, address + 0x08, struct.pack("<B", species.catch_rate))
        patch.write_token(APTokenTypes.WRITE, address + 0x16, struct.pack("<B", species.abilities[0]))
        patch.write_token(APTokenTypes.WRITE, address + 0x17, struct.pack("<B", species.abilities[1]))

        for i, learnset_move in enumerate(species.learnset):
            learnset_address = species.learnset_address[game_version_revision]
            level_move = learnset_move.level << 9 | learnset_move.move_id
            patch.write_token(APTokenTypes.WRITE, learnset_address + (i * 2), struct.pack("<H", level_move))


def _set_wild_encounters(world: "PokemonFRLGWorld",
                         patch: Union[PokemonFireRedProcedurePatch,
                                      PokemonFireRedRev1ProcedurePatch,
                                      PokemonLeafGreenProcedurePatch,
                                      PokemonLeafGreenRev1ProcedurePatch],
                         game_version: str,
                         game_version_revision: str) -> None:
    """
        Encounter tables are lists of
        struct {
            min_level:  uint8,
            max_level:  uint8,
            species_id: uint16
        }
    """
    for map_data in world.modified_maps.values():
        tables = [map_data.land_encounters,
                  map_data.water_encounters,
                  map_data.fishing_encounters]
        for table in tables:
            if table is not None:
                for i, species_data in enumerate(table.slots[game_version]):
                    address = table.address[game_version_revision] + (i * 4)
                    patch.write_token(APTokenTypes.WRITE, address, struct.pack("<B", species_data.min_level))
                    patch.write_token(APTokenTypes.WRITE, address + 0x01, struct.pack("<B", species_data.max_level))
                    patch.write_token(APTokenTypes.WRITE, address + 0x02, struct.pack("<H", species_data.species_id))


def _set_starters(world: "PokemonFRLGWorld",
                  patch: Union[PokemonFireRedProcedurePatch,
                               PokemonFireRedRev1ProcedurePatch,
                               PokemonLeafGreenProcedurePatch,
                               PokemonLeafGreenRev1ProcedurePatch],
                  game_version_revision: str) -> None:

    for name, starter in world.modified_starters.items():
        starter_address = data.rom_addresses[game_version_revision]["sStarterSpecies"] + (STARTER_INDEX[name] * 2)
        patch.write_token(APTokenTypes.WRITE, starter_address, struct.pack("<H", starter.species_id))
        patch.write_token(APTokenTypes.WRITE,
                          starter.player_address[game_version_revision],
                          struct.pack("<H", starter.species_id))
        patch.write_token(APTokenTypes.WRITE,
                          starter.rival_address[game_version_revision],
                          struct.pack("<H", starter.species_id))


def _set_legendaries(world: "PokemonFRLGWorld",
                     patch: Union[PokemonFireRedProcedurePatch,
                                  PokemonFireRedRev1ProcedurePatch,
                                  PokemonLeafGreenProcedurePatch,
                                  PokemonLeafGreenRev1ProcedurePatch],
                     game_version: str,
                     game_version_revision: str) -> None:
    for name, legendary in world.modified_legendary_pokemon.items():
        patch.write_token(APTokenTypes.WRITE,
                          legendary.address[game_version_revision],
                          struct.pack("<H", legendary.species_id[game_version]))
        patch.write_token(APTokenTypes.WRITE,
                          legendary.level_address[game_version_revision],
                          struct.pack("<B", legendary.level[game_version]))


def _set_misc_pokemon(world: "PokemonFRLGWorld",
                      patch: Union[PokemonFireRedProcedurePatch,
                                   PokemonFireRedRev1ProcedurePatch,
                                   PokemonLeafGreenProcedurePatch,
                                   PokemonLeafGreenRev1ProcedurePatch],
                      game_version: str,
                      game_version_revision: str) -> None:

    for name, misc_pokemon in world.modified_misc_pokemon.items():
        patch.write_token(APTokenTypes.WRITE,
                          misc_pokemon.address[game_version_revision],
                          struct.pack("<H", misc_pokemon.species_id[game_version]))
        if misc_pokemon.level[game_version] != 0:
            patch.write_token(APTokenTypes.WRITE,
                              misc_pokemon.level_address[game_version_revision],
                              struct.pack("<B", misc_pokemon.level[game_version]))


def _set_trainer_parties(world: "PokemonFRLGWorld",
                         patch: Union[PokemonFireRedProcedurePatch,
                                      PokemonFireRedRev1ProcedurePatch,
                                      PokemonLeafGreenProcedurePatch,
                                      PokemonLeafGreenRev1ProcedurePatch],
                         game_version_revision: str) -> None:
    for trainer in world.modified_trainers.values():
        party_address = trainer.party.address[game_version_revision]

        if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES,
                                               TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES}:
            pokemon_data_size = 8
        else:
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_address = party_address + (i * pokemon_data_size)

            level = round(pokemon.level + (pokemon.level * (world.options.modify_trainer_levels.value / 100)))
            if level < 1:
                level = 1
            elif level > 100:
                level = 100

            patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x02, struct.pack("<B", level))
            patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x04, struct.pack("<H", pokemon.species_id))

            if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES,
                                                   TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES}:
                offset = 2 if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES else 0
                patch.write_token(APTokenTypes.WRITE,
                                  pokemon_address + 0x06 + offset,
                                  struct.pack("<H", pokemon.moves[0]))
                patch.write_token(APTokenTypes.WRITE,
                                  pokemon_address + 0x08 + offset,
                                  struct.pack("<H", pokemon.moves[1]))
                patch.write_token(APTokenTypes.WRITE,
                                  pokemon_address + 0x0A + offset,
                                  struct.pack("<H", pokemon.moves[2]))
                patch.write_token(APTokenTypes.WRITE,
                                  pokemon_address + 0x0C + offset,
                                  struct.pack("<H", pokemon.moves[3]))


def _set_tmhm_compatibility(world: "PokemonFRLGWorld",
                            patch: Union[PokemonFireRedProcedurePatch,
                                         PokemonFireRedRev1ProcedurePatch,
                                         PokemonLeafGreenProcedurePatch,
                                         PokemonLeafGreenRev1ProcedurePatch],
                            game_version_revision: str) -> None:
    learnsets_address = data.rom_addresses[game_version_revision]["sTMHMLearnsets"]

    for species in world.modified_species.values():
        patch.write_token(
            APTokenTypes.WRITE,
            learnsets_address + (species.species_id * 8),
            struct.pack("<Q", species.tm_hm_compatibility)
        )


def _set_tm_moves(world: "PokemonFRLGWorld",
                  patch: Union[PokemonFireRedProcedurePatch,
                               PokemonFireRedRev1ProcedurePatch,
                               PokemonLeafGreenProcedurePatch,
                               PokemonLeafGreenRev1ProcedurePatch],
                  game_version_revision: str) -> None:
    address = data.rom_addresses[game_version_revision]["sTMHMMoves"]

    for i, move in enumerate(world.modified_tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break

        patch.write_token(APTokenTypes.WRITE, address + (i * 2), struct.pack("<H", move))


def _randomize_move_tutors(world: "PokemonFRLGWorld",
                           patch: Union[PokemonFireRedProcedurePatch,
                                        PokemonFireRedRev1ProcedurePatch,
                                        PokemonLeafGreenProcedurePatch,
                                        PokemonLeafGreenRev1ProcedurePatch],
                           game_version_revision: str) -> None:
    if world.options.tm_tutor_moves:
        new_tutor_moves = randomize_tutor_moves(world)
        address = data.rom_addresses[game_version_revision]["gTutorMoves"]

        for i, move in enumerate(new_tutor_moves):
            patch.write_token(APTokenTypes.WRITE, address + (i * 2), struct.pack("<H", move))

    if world.options.tm_tutor_compatability != TmTutorCompatibility.special_range_names["vanilla"]:
        learnsets_address = data.rom_addresses[game_version_revision]["sTutorLearnsets"]

        for species in world.modified_species.values():
            patch.write_token(
                APTokenTypes.WRITE,
                learnsets_address + (species.species_id * 2),
                struct.pack("<H", bool_array_to_int([
                    world.random.randrange(0, 100) < world.options.tm_tutor_compatability.value
                    for _ in range(16)
                ]))
            )
