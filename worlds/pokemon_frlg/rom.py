"""
Classes and functions related to creating a ROM patch
"""
import bsdiff4
import struct
from typing import TYPE_CHECKING, Dict, List, Tuple

from BaseClasses import ItemClassification

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .data import data, TrainerPokemonDataTypeEnum
from .items import get_random_item, reverse_offset_item_value
from .locations import reverse_offset_flag
from .options import (ItemfinderRequired, HmCompatibility, RandomizeLegendaryPokemon, RandomizeMiscPokemon,
                      RandomizeStarters, RandomizeTrainerParties, RandomizeWildPokemon, ShuffleHiddenItems,
                      TmTutorCompatibility, ViridianCityRoadblock)
from .pokemon import STARTER_INDEX, randomize_tutor_moves
from .util import bool_array_to_int, bound, encode_string

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

FIRERED_REV0_HASH = "e26ee0d44e809351c8ce2d73c7400cdd"
FIRERED_REV1_HASH = "51901a6e40661b3914aa333c802e24e8"
LEAFGREEN_REV0_HASH = "612ca9473451fa42b51d1711031ed5f6"
LEAFGREEN_REV1_HASH = "9d33a02159e018d09073e700e1fd10fd"


class PokemonFRLGPatchExtension(APPatchExtension):
    game = "Pokemon FireRed and LeafGreen"

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str) -> bytes:
        rom_data = bytearray(rom)
        if rom_data[0xBC] == 1:
            return bsdiff4.patch(rom, caller.get_file("base_patch_rev1.bsdiff4"))
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_tokens(caller: APProcedurePatch, rom: bytes, token_file: str) -> bytes:
        rom_data = bytearray(rom)
        if rom_data[0xBC] == 1:
            token_data = caller.get_file("token_data_rev1.bin")
        else:
            token_data = caller.get_file(token_file)
        token_count = int.from_bytes(token_data[0:4], "little")
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = int.from_bytes(token_data[bpr + 1:bpr + 5], "little")
            size = int.from_bytes(token_data[bpr + 5:bpr + 9], "little")
            data = token_data[bpr + 9:bpr + 9 + size]
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                arg = data[0]
                if token_type == APTokenTypes.AND_8:
                    rom_data[offset] = rom_data[offset] & arg
                elif token_type == APTokenTypes.OR_8:
                    rom_data[offset] = rom_data[offset] | arg
                else:
                    rom_data[offset] = rom_data[offset] ^ arg
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                length = int.from_bytes(data[:4], "little")
                value = int.from_bytes(data[4:], "little")
                if token_type == APTokenTypes.COPY:
                    rom_data[offset: offset + length] = rom_data[value: value + length]
                else:
                    rom_data[offset: offset + length] = bytes([value] * length)
            else:
                rom_data[offset:offset + len(data)] = data
            bpr += 9 + size
        return bytes(rom_data)


class PokemonFireRedProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = [FIRERED_REV0_HASH, FIRERED_REV1_HASH]
    patch_file_ending = ".apfirered"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_rev0.bsdiff4"]),
        ("apply_tokens", ["token_data_rev0.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.firered_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


class PokemonLeafGreenProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = [LEAFGREEN_REV0_HASH, LEAFGREEN_REV1_HASH]
    patch_file_ending = ".apleafgreen"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_rev0.bsdiff4"]),
        ("apply_tokens", ["token_data_rev0.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.leafgreen_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


def get_tokens(world: "PokemonFRLGWorld", game_revision: int) -> APTokenMixin:
    tokens: APTokenMixin = APTokenMixin()
    game_version = world.options.game_version.current_key

    if game_revision == 0:
        game_version_revision = game_version
    else:
        game_version_revision = f'{game_version}_rev1'

    # Set item values
    location_info: List[Tuple[int, int, str]] = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        item_address = location.item_address[game_version_revision]

        if location.item.player == world.player:
            if type(item_address) is int:
                tokens.write_token(
                    APTokenTypes.WRITE,
                    item_address,
                    struct.pack("<H", reverse_offset_item_value(location.item.code))
                )
            elif type(item_address) is list:
                for address in item_address:
                    tokens.write_token(
                        APTokenTypes.WRITE,
                        address,
                        struct.pack("<H", reverse_offset_item_value(location.item.code))
                    )
        else:
            if type(item_address) is int:
                tokens.write_token(
                    APTokenTypes.WRITE,
                    item_address,
                    struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])
                )
            elif type(item_address) is list:
                for address in item_address:
                    tokens.write_token(
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

            location_info.extend(
                (
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
                tokens.write_token(
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
            tokens.write_token(
                APTokenTypes.WRITE,
                item_name_address + (item_name_offsets[item_name]),
                encode_string(item_name) + b"\xFF"
            )

        # There should always be enough space for one entry per location
        name_table_address = data.rom_addresses[game_version_revision]["gArchipelagoNameTable"]
        tokens.write_token(
            APTokenTypes.WRITE,
            name_table_address + (i * 5) + 0,
            struct.pack("<H", flag)
        )
        tokens.write_token(
            APTokenTypes.WRITE,
            name_table_address + (i * 5) + 2,
            struct.pack("<H", item_name_offsets[item_name])
        )
        tokens.write_token(
            APTokenTypes.WRITE,
            name_table_address + (i * 5) + 4,
            struct.pack("<B", player_name_ids[player_name])
        )

    # Replace unique items if necessary
    if world.options.kanto_only:
        location_ids = ["NPC_GIFT_GOT_HM06", "ITEM_FOUR_ISLAND_ICEFALL_CAVE_1F_HM07"]
        for location_id in location_ids:
            location_data = data.locations[location_id]
            new_item_id = reverse_offset_item_value(
                world.item_name_to_id[get_random_item(world, ItemClassification.filler)]
            )

            tokens.write_token(
                APTokenTypes.WRITE,
                location_data.address[game_version_revision],
                struct.pack("<H", new_item_id)
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

    starting_fly_unlocks = 0
    if start_inventory.pop("Fly Pallet Town", 0) > 0:
        starting_fly_unlocks |= (1 << 0)
    if start_inventory.pop("Fly Viridian City", 0) > 0:
        starting_fly_unlocks |= (1 << 1)
    if start_inventory.pop("Fly Pewter City", 0) > 0:
        starting_fly_unlocks |= (1 << 2)
    if start_inventory.pop("Fly Cerulean City", 0) > 0:
        starting_fly_unlocks |= (1 << 3)
    if start_inventory.pop("Fly Lavender Town", 0) > 0:
        starting_fly_unlocks |= (1 << 4)
    if start_inventory.pop("Fly Vermilion City", 0) > 0:
        starting_fly_unlocks |= (1 << 5)
    if start_inventory.pop("Fly Celadon City", 0) > 0:
        starting_fly_unlocks |= (1 << 6)
    if start_inventory.pop("Fly Fuchsia City", 0) > 0:
        starting_fly_unlocks |= (1 << 7)
    if start_inventory.pop("Fly Cinnabar Island", 0) > 0:
        starting_fly_unlocks |= (1 << 8)
    if start_inventory.pop("Fly Indigo Plateau", 0) > 0:
        starting_fly_unlocks |= (1 << 9)
    if start_inventory.pop("Fly Saffron City", 0) > 0:
        starting_fly_unlocks |= (1 << 10)
    if start_inventory.pop("Fly One Island", 0) > 0:
        starting_fly_unlocks |= (1 << 11)
    if start_inventory.pop("Fly Two Island", 0) > 0:
        starting_fly_unlocks |= (1 << 12)
    if start_inventory.pop("Fly Three Island", 0) > 0:
        starting_fly_unlocks |= (1 << 13)
    if start_inventory.pop("Fly Four Island", 0) > 0:
        starting_fly_unlocks |= (1 << 14)
    if start_inventory.pop("Fly Five Island", 0) > 0:
        starting_fly_unlocks |= (1 << 15)
    if start_inventory.pop("Fly Seven Island", 0) > 0:
        starting_fly_unlocks |= (1 << 16)
    if start_inventory.pop("Fly Six Island", 0) > 0:
        starting_fly_unlocks |= (1 << 17)
    if start_inventory.pop("Fly Route 4", 0) > 0:
        starting_fly_unlocks |= (1 << 18)
    if start_inventory.pop("Fly Route 10", 0) > 0:
        starting_fly_unlocks |= (1 << 19)

    pc_slots: List[Tuple[str, int]] = []
    for item, quantity in start_inventory.items():
        if len(pc_slots) >= 19:
            break
        if "Unique" in data.items[reverse_offset_item_value(world.item_name_to_id[item])].tags:
            quantity = 1
        if quantity > 999:
            quantity = 999
        pc_slots.append([item, quantity])

    for i, slot in enumerate(pc_slots, 1):
        address = data.rom_addresses[game_version_revision]["gNewGamePCItems"] + (i * 4)
        item = reverse_offset_item_value(world.item_name_to_id[slot[0]])
        tokens.write_token(APTokenTypes.WRITE, address, struct.pack("<H", item))
        tokens.write_token(APTokenTypes.WRITE, address + 2, struct.pack("<H", slot[1]))

    # Set species data
    _set_species_info(world, tokens, game_version_revision)

    # Set wild encounters
    _set_wild_encounters(world, tokens, game_version, game_version_revision)

    # Set starters
    _set_starters(world, tokens, game_version_revision)

    # Set legendaries
    _set_legendaries(world, tokens, game_version, game_version_revision)

    # Set misc pokemon
    _set_misc_pokemon(world, tokens, game_version, game_version_revision)

    # Set trainer parties
    _set_trainer_parties(world, tokens, game_version_revision)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(world, tokens, game_version_revision)

    # Set TM Moves
    _set_tm_moves(world, tokens, game_version_revision)

    # Randomize move tutors
    _randomize_move_tutors(world, tokens, game_version_revision)

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
    # /* 0x18 */ u32 startingFlyUnlocks;
    # /* 0x1C */ u32 startingMoney;
    #
    # /* 0x20 */ bool8 itemfinderRequired;
    # /* 0x21 */ bool8 reccuringHiddenItems;
    #
    # /* 0x22 */ u8 oaksAideRequiredCounts[5]; // Route 2, Route 10, Route 11, Route 16, Route 15
    #
    # /* 0x27 */ bool8 isTrainersanity;
    # /* 0x28 */ bool8 extraKeyItems;
    # /* 0x29 */ bool8 kantoOnly;
    # /* 0x2A */ bool8 flyUnlocks;
    #
    # /* 0x2B */ u8 removeBadgeRequirement; // Flash, Cut, Fly, Strength, Surf, Rock Smash, Waterfall
    #
    # /* 0x2C */ u8 free_fly_id;
    # /* 0x2D */ u8 town_free_fly_id;
    # }
    options_address = data.rom_addresses[game_version_revision]["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if world.options.turbo_a else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x00, struct.pack("<B", turbo_a))

    # Set received item message types
    receive_item_messages = world.options.receive_item_messages.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x01, struct.pack("<B", receive_item_messages))

    # Set better shops
    better_shops = 1 if world.options.better_shops else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x02, struct.pack("<B", better_shops))

    # Set reusable TMs and Move Tutors
    reusable_tm_tutors = 1 if world.options.reusable_tm_tutors else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x03, struct.pack("<B", reusable_tm_tutors))

    # Set guaranteed catch
    guaranteed_catch = 1 if world.options.guaranteed_catch else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x04, struct.pack("<B", guaranteed_catch))

    # Set blind trainers
    blind_trainers = 1 if world.options.blind_trainers else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x05, struct.pack("<B", blind_trainers))

    # Set exp multiplier
    numerator = world.options.exp_modifier.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x06, struct.pack("<H", numerator))
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x08, struct.pack("<H", 100))

    # Set Viridian City roadblock
    open_viridian = 1 if world.options.viridian_city_roadblock.value == ViridianCityRoadblock.option_open else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x0A, struct.pack("<B", open_viridian))

    # Set Pewter City roadblock
    route_3_condition = world.options.pewter_city_roadblock.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x0B, struct.pack("<B", route_3_condition))

    # Set Cerulean City roadblocs
    save_bill = 1 if world.options.cerulean_city_roadblocks else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x0C, struct.pack("<B", save_bill))

    # Set Viridian Gym Rrquirement
    viridian_gym_requirement = world.options.viridian_gym_requirement.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x0D, struct.pack("<B", viridian_gym_requirement))

    # Set Viridian Gym count
    viridian_gym_count = world.options.viridian_gym_count.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x0E, struct.pack("<B", viridian_gym_count))

    # Set Route 22 requirement
    route_22_requirement = world.options.route22_gate_requirement.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x0F, struct.pack("<B", route_22_requirement))

    # Set Route 22 count
    route_22_count = world.options.route22_gate_count.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x10, struct.pack("<B", route_22_count))

    # Set Route 23 requirement
    route_23_requirement = world.options.route23_guard_requirement.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x11, struct.pack("<B", route_23_requirement))

    # Set Route 23 count
    route_23_count = world.options.route23_guard_count.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x12, struct.pack("<B", route_23_count))

    # Set Elite Four requirement
    elite_four_requirement = world.options.elite_four_requirement.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x13, struct.pack("<B", elite_four_requirement))

    # Set Elite Four count
    elite_four_count = world.options.elite_four_count.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x14, struct.pack("<B", elite_four_count))

    # Set Cerulean Cave requirement
    cerulean_cave_requirement = world.options.cerulean_cave_requirement.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x15, struct.pack("<B", cerulean_cave_requirement))

    # Set Cerulean Cave count
    cerulean_cave_count = world.options.cerulean_cave_count.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x16, struct.pack("<B", cerulean_cave_count))

    # Set starting badges
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x17, struct.pack("<B", starting_badges))

    # Set starting fly unlocks
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x18, struct.pack("<I", starting_fly_unlocks))

    # Set starting money
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x1C, struct.pack("<I",
                                                                               world.options.starting_money.value))
    # Set itemfinder required
    itemfinder_required = 1 if world.options.itemfinder_required.value == ItemfinderRequired.option_required else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x20, struct.pack("<B", itemfinder_required))

    # Set recurring hidden items shuffled
    recurring_hidden_items = 1 if world.options.shuffle_hidden.value == ShuffleHiddenItems.option_all else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x21, struct.pack("<B", recurring_hidden_items))

    # Set Oak's Aides counts
    oaks_aide_route_2 = world.options.oaks_aide_route_2.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x22, struct.pack("<B", oaks_aide_route_2))
    oaks_aide_route_10 = world.options.oaks_aide_route_10.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x23, struct.pack("<B", oaks_aide_route_10))
    oaks_aide_route_11 = world.options.oaks_aide_route_11.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x24, struct.pack("<B", oaks_aide_route_11))
    oaks_aide_route_16 = world.options.oaks_aide_route_16.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x25, struct.pack("<B", oaks_aide_route_16))
    oaks_aide_route_15 = world.options.oaks_aide_route_15.value
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x26, struct.pack("<B", oaks_aide_route_15))

    # Set trainersanity
    trainersanity = 1 if world.options.trainersanity else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x27, struct.pack("<B", trainersanity))

    # Set extra key items
    extra_key_items = 1 if world.options.extra_key_items else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x28, struct.pack("<B", extra_key_items))

    # Set kanto only
    kanto_only = 1 if world.options.kanto_only else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x29, struct.pack("<B", kanto_only))

    # Set fly unlocks
    fly_unlocks = 1 if world.options.shuffle_fly_destination_unlocks else 0
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x2A, struct.pack("B", fly_unlocks))

    # Set remove badge requirements
    hms = ["Flash", "Cut", "Fly", "Strength", "Surf", "Rock Smash", "Waterfall"]
    remove_badge_requirements = 0
    for i, hm in enumerate(hms):
        if hm in world.options.remove_badge_requirement.value:
            remove_badge_requirements |= (1 << i)
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x2B, struct.pack("<B", remove_badge_requirements))

    # Set free fly location
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x2C, struct.pack("<B", world.free_fly_location_id))

    # Set town map fly location
    tokens.write_token(APTokenTypes.WRITE, options_address + 0x2D, struct.pack("<B", world.town_map_fly_location_id))

    # Set slot auth
    tokens.write_token(APTokenTypes.WRITE, data.rom_addresses[game_version_revision]["gArchipelagoInfo"], world.auth)

    return tokens


def _set_species_info(world: "PokemonFRLGWorld", tokens: APTokenMixin, game_version_revision: str) -> None:
    for species in world.modified_species.values():
        address = species.address[game_version_revision]

        tokens.write_token(APTokenTypes.WRITE, address + 0x06, struct.pack("<B", species.types[0]))
        tokens.write_token(APTokenTypes.WRITE, address + 0x07, struct.pack("<B", species.types[1]))
        tokens.write_token(APTokenTypes.WRITE, address + 0x08, struct.pack("<B", species.catch_rate))
        tokens.write_token(APTokenTypes.WRITE, address + 0x16, struct.pack("<B", species.abilities[0]))
        tokens.write_token(APTokenTypes.WRITE, address + 0x17, struct.pack("<B", species.abilities[1]))

        for i, learnset_move in enumerate(species.learnset):
            learnset_address = species.learnset_address[game_version_revision]
            level_move = learnset_move.level << 9 | learnset_move.move_id
            tokens.write_token(APTokenTypes.WRITE, learnset_address + (i * 2), struct.pack("<H", level_move))


def _set_wild_encounters(world: "PokemonFRLGWorld", tokens: APTokenMixin,
                         game_version: str, game_version_revision: str) -> None:
    if not world.options.level_scaling and world.options.wild_pokemon == RandomizeWildPokemon.option_vanilla:
        return

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
                    tokens.write_token(APTokenTypes.WRITE, address, struct.pack("<B", species_data.min_level))
                    tokens.write_token(APTokenTypes.WRITE, address + 0x01, struct.pack("<B", species_data.max_level))
                    tokens.write_token(APTokenTypes.WRITE, address + 0x02, struct.pack("<H", species_data.species_id))


def _set_starters(world: "PokemonFRLGWorld", tokens: APTokenMixin, game_version_revision: str) -> None:
    if world.options.starters == RandomizeStarters.option_vanilla:
        return

    for name, starter in world.modified_starters.items():
        starter_address = data.rom_addresses[game_version_revision]["sStarterSpecies"] + (STARTER_INDEX[name] * 2)
        tokens.write_token(APTokenTypes.WRITE, starter_address, struct.pack("<H", starter.species_id))
        tokens.write_token(APTokenTypes.WRITE,
                           starter.player_address[game_version_revision],
                           struct.pack("<H", starter.species_id))
        tokens.write_token(APTokenTypes.WRITE,
                           starter.rival_address[game_version_revision],
                           struct.pack("<H", starter.species_id))


def _set_legendaries(world: "PokemonFRLGWorld", tokens: APTokenMixin,
                     game_version: str, game_version_revision: str) -> None:
    if not world.options.level_scaling and world.options.legendary_pokemon == RandomizeLegendaryPokemon.option_vanilla:
        return

    for name, legendary in world.modified_legendary_pokemon.items():
        tokens.write_token(APTokenTypes.WRITE,
                           legendary.address[game_version_revision],
                           struct.pack("<H", legendary.species_id[game_version]))
        tokens.write_token(APTokenTypes.WRITE,
                           legendary.level_address[game_version_revision],
                           struct.pack("<B", legendary.level[game_version]))


def _set_misc_pokemon(world: "PokemonFRLGWorld", tokens: APTokenMixin,
                      game_version: str, game_version_revision: str) -> None:
    if not world.options.level_scaling and world.options.misc_pokemon == RandomizeMiscPokemon.option_vanilla:
        return

    for name, misc_pokemon in world.modified_misc_pokemon.items():
        tokens.write_token(APTokenTypes.WRITE,
                           misc_pokemon.address[game_version_revision],
                           struct.pack("<H", misc_pokemon.species_id[game_version]))
        if misc_pokemon.level[game_version] != 0:
            tokens.write_token(APTokenTypes.WRITE,
                               misc_pokemon.level_address[game_version_revision],
                               struct.pack("<B", misc_pokemon.level[game_version]))


def _set_trainer_parties(world: "PokemonFRLGWorld", tokens: APTokenMixin, game_version_revision: str) -> None:
    if (not world.options.level_scaling and
            world.options.trainers == RandomizeTrainerParties.option_vanilla and
            world.options.starters == RandomizeStarters.option_vanilla and
            world.options.modify_trainer_levels.value == 0):
        return

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
            level = bound(level, 1, 100)

            tokens.write_token(APTokenTypes.WRITE, pokemon_address + 0x02, struct.pack("<B", level))
            tokens.write_token(APTokenTypes.WRITE, pokemon_address + 0x04, struct.pack("<H", pokemon.species_id))

            if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES,
                                                   TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES}:
                offset = 2 if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES else 0
                tokens.write_token(APTokenTypes.WRITE,
                                   pokemon_address + 0x06 + offset,
                                   struct.pack("<H", pokemon.moves[0]))
                tokens.write_token(APTokenTypes.WRITE,
                                   pokemon_address + 0x08 + offset,
                                   struct.pack("<H", pokemon.moves[1]))
                tokens.write_token(APTokenTypes.WRITE,
                                   pokemon_address + 0x0A + offset,
                                   struct.pack("<H", pokemon.moves[2]))
                tokens.write_token(APTokenTypes.WRITE,
                                   pokemon_address + 0x0C + offset,
                                   struct.pack("<H", pokemon.moves[3]))


def _set_tmhm_compatibility(world: "PokemonFRLGWorld", tokens: APTokenMixin, game_version_revision: str) -> None:
    if (world.options.hm_compatibility == HmCompatibility.special_range_names["vanilla"] and
            world.options.tm_tutor_compatibility == TmTutorCompatibility.special_range_names["vanilla"]):
        return

    learnsets_address = data.rom_addresses[game_version_revision]["sTMHMLearnsets"]

    for species in world.modified_species.values():
        tokens.write_token(
            APTokenTypes.WRITE,
            learnsets_address + (species.species_id * 8),
            struct.pack("<Q", species.tm_hm_compatibility)
        )


def _set_tm_moves(world: "PokemonFRLGWorld", tokens: APTokenMixin, game_version_revision: str) -> None:
    if not world.options.tm_tutor_moves:
        return

    address = data.rom_addresses[game_version_revision]["sTMHMMoves"]

    for i, move in enumerate(world.modified_tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break

        tokens.write_token(APTokenTypes.WRITE, address + (i * 2), struct.pack("<H", move))


def _randomize_move_tutors(world: "PokemonFRLGWorld", tokens: APTokenMixin, game_version_revision: str) -> None:
    if world.options.tm_tutor_moves:
        new_tutor_moves = randomize_tutor_moves(world)
        address = data.rom_addresses[game_version_revision]["gTutorMoves"]

        for i, move in enumerate(new_tutor_moves):
            tokens.write_token(APTokenTypes.WRITE, address + (i * 2), struct.pack("<H", move))

    if world.options.tm_tutor_compatibility != TmTutorCompatibility.special_range_names["vanilla"]:
        learnsets_address = data.rom_addresses[game_version_revision]["sTutorLearnsets"]

        for species in world.modified_species.values():
            tokens.write_token(
                APTokenTypes.WRITE,
                learnsets_address + (species.species_id * 2),
                struct.pack("<H", bool_array_to_int([
                    world.random.randrange(0, 100) < world.options.tm_tutor_compatibility.value
                    for _ in range(16)
                ]))
            )
