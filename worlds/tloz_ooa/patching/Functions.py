from typing import List

from settings import get_settings
from . import RomData
from .Util import *
from .z80asm.Assembler import Z80Assembler
from ..data.Constants import *
from .Constants import *
from pathlib import Path
from .. import LOCATIONS_DATA


def get_treasure_addr(rom: RomData, item_name: str):
    item_id, item_subid = get_item_id_and_subid(item_name)
    addr = 0x59332 + (item_id * 4)
    if rom.read_byte(addr) & 0x80 != 0:
        addr = 0x54000 + rom.read_word(addr + 1)
    return addr + (item_subid * 4)


def set_treasure_data(rom: RomData,
                      item_name: str, text_id: int | None,
                      sprite_id: int | None = None,
                      param_value: int | None = None):
    addr = get_treasure_addr(rom, item_name)
    if text_id is not None:
        rom.write_byte(addr + 0x02, text_id)
    if sprite_id is not None:
        rom.write_byte(addr + 0x03, sprite_id)
    if param_value is not None:
        rom.write_byte(addr + 0x01, param_value)

def alter_treasures(rom: RomData):

    set_treasure_data(rom, "Potion", 0x6d)

    # Set data for remote Archipelago items
    set_treasure_data(rom, "Archipelago Item", 0x57, 0x5a)
    set_treasure_data(rom, "Archipelago Progression Item", 0x57, 0x59)
    set_treasure_data(rom, "King Zora's Potion", 0x45, 0x5e)

    # Make bombs increase max carriable quantity when obtained from treasures,
    # not drops (see asm/seasons/bomb_bag_behavior)
    set_treasure_data(rom, "Bombs (10)", None, None, 0x90)


def get_asm_files(patch_data):
    asm_files = ASM_FILES.copy()
    if patch_data["options"]["quick_flute"]:
        asm_files.append("asm/conditional/quick_flute.yaml")
    if not(patch_data["options"]["enable_dance_and_joke"]):
        asm_files.append("asm/conditional/skip_dance_and_joke.yaml")
    return asm_files


def define_location_constants(assembler: Z80Assembler, patch_data):
    for location_name, location_data in LOCATIONS_DATA.items():
        if "symbolic_name" not in location_data:
            continue
        symbolic_name = location_data["symbolic_name"]

        if location_name in patch_data["locations"]:
            item_name = patch_data["locations"][location_name]
        else:
            item_name = location_data["vanilla_item"]

        if item_name == "Flute":
            item_name = COMPANIONS[patch_data["options"]["animal_companion"]] + "'s Flute"

        item_id, item_subid = get_item_id_and_subid(item_name)
        assembler.define_byte(f"locations.{symbolic_name}.id", item_id)
        assembler.define_byte(f"locations.{symbolic_name}.subid", item_subid)
        assembler.define_word(f"locations.{symbolic_name}", (item_id << 8) + item_subid)

        
def define_option_constants(assembler: Z80Assembler, patch_data):
    options = patch_data["options"]

    assembler.define_byte("option.startingGroup", 0x00)
    assembler.define_byte("option.startingRoom", 0x59)
    assembler.define_byte("option.startingPosY", 0x58)
    assembler.define_byte("option.startingPosX", 0x58)
    assembler.define_byte("option.startingPos", 0x55)

    assembler.define_byte("option.animalCompanion", 0x0b + patch_data["options"]["animal_companion"])
    assembler.define_byte("option.defaultSeedType", 0x20 + patch_data["options"]["default_seed"])
    assembler.define_byte("option.receivedDamageModifier", options["combat_difficulty"])
    assembler.define_byte("option.openAdvanceShop", options["advance_shop"])
    assembler.define_byte("option.warpToStart", options["warp_to_start"])

    assembler.define_byte("option.requiredEssences", options["required_essences"])
    assembler.define_byte("option.required_slates", options["required_slates"])

def process_item_name_for_shop_text(item_name: str) -> List[int]:
    words = item_name.split(" ")
    current_line = 0
    lines = [""]
    while len(words) > 0:
        line_with_word = lines[current_line]
        if len(line_with_word) > 0:
            line_with_word += " "
        line_with_word += words[0]
        if len(line_with_word) <= 16:
            lines[current_line] = line_with_word
        else:
            current_line += 1
            lines.append(words[0])
        words = words[1:]

    result = []
    for line in lines:
        if len(result) > 0:
            result.append(0x01)  # Newline
        result.extend(line.encode())
    return result

def define_text_constants(assembler: Z80Assembler, patch_data):
    overworld_shops = [
        "Lynna Shop",
        "Hidden Shop",
        "Syrup Shop",
        "Advance Shop",
    ]

    for shop_name in overworld_shops:
        for i in range(1, 4):
            location_name = f"{shop_name} #{i}"
            symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
            text_bytes = []
            if location_name in patch_data["locations"]:
                item_name_bytes = process_item_name_for_shop_text(patch_data["locations"][location_name])
                text_bytes = [0x09, 0x01] + item_name_bytes + [0x09, 0x00, 0x0c, 0x18, 0x01]  # Item name
                text_bytes.extend([0x20, 0x0c, 0x08, 0x20, 0x03, 0x7b, 0x01])  # Price
                text_bytes.extend([0x02, 0x00, 0x00])  # OK / No thanks
            assembler.add_floating_chunk(f"text.{symbolic_name}", text_bytes)


def write_chest_contents(rom: RomData, patch_data):
    """
    Chest locations are packed inside several big tables in the ROM, unlike other more specific locations.
    This puts the item described in the patch data inside each chest in the game.
    """
    for location_name, location_data in LOCATIONS_DATA.items():
        if ('collect' not in location_data or 'room' not in location_data or location_data['collect'] != COLLECT_CHEST) and location_name != "Ridge Bush Cave":
            continue
        if location_name == "Nuun Highlands Cave":
            chest_addr = rom.get_chest_addr(location_data['room'][patch_data["options"]["animal_companion"]])
        else:
            chest_addr = rom.get_chest_addr(location_data['room'])
        item_name = patch_data["locations"][location_name]
        item_id, item_subid = get_item_id_and_subid(item_name)
        rom.write_byte(chest_addr, item_id)
        rom.write_byte(chest_addr + 1, item_subid)


def define_compass_rooms_table(assembler: Z80Assembler, patch_data):
    table = []
    for location_name, item_name in patch_data["locations"].items():
        _, item_subid = get_item_id_and_subid(item_name)
        dungeon = 0xff
        if item_name.startswith("Small Key") or item_name.startswith("Master Key") or item_name.startswith(
                "Dungeon Map"):
            dungeon = item_subid
        elif item_name.startswith("Boss Key"):
            dungeon = item_subid + 1

        if dungeon != 0xff:
            location_data = LOCATIONS_DATA[location_name]
            rooms = location_data["room"]
            if not isinstance(rooms, list):
                rooms = [rooms]
            for room in rooms:
                room_id = room & 0xff
                group_id = room >> 8
                table.extend([group_id, room_id, dungeon])
    table.append(0xff)  # End of table
    assembler.add_floating_chunk("compassRoomsTable", table)
       

def define_collect_properties_table(assembler: Z80Assembler, patch_data):
    """
    Defines a table of (group, room, collect mode) entries for randomized items
    to determine how they spawn, how they are grabbed and whether they set
    a room flag when obtained.
    """
    table = []
    for location_name, item_name in patch_data["locations"].items():
        location_data = LOCATIONS_DATA[location_name]
        if "collect" not in location_data or "room" not in location_data:
            continue
        mode = location_data["collect"]

        # Use no pickup animation for falling small keys
        if mode == COLLECT_DROP and item_name.startswith("Small Key"):
            mode &= 0xf8  # Set grab mode to TREASURE_GRAB_INSTANT

        rooms = location_data["room"]
        if not isinstance(rooms, list):
            rooms = [rooms]
        for room in rooms:
            room_id = room & 0xff
            group_id = room >> 8
            table.extend([group_id, room_id, mode])

    table.append(0xff)
    assembler.add_floating_chunk("collectPropertiesTable", table)

    
def inject_slot_name(rom: RomData, slot_name: str):
    slot_name_as_bytes = list(str.encode(slot_name))
    slot_name_as_bytes += [0x00] * (0x40 - len(slot_name_as_bytes))
    rom.write_bytes(0xfffc0, slot_name_as_bytes)

    
def write_seed_tree_content(rom: RomData, patch_data):
    for _, tree_data in SEED_TREE_DATA.items():
        original_data = rom.read_byte(tree_data["codeAdress"])
        item_name = patch_data["locations"][tree_data["location"]]
        item_id, _ = get_item_id_and_subid(item_name)
        newdata = (original_data & 0x0f) | (item_id - 0x20) << 4
        rom.write_bytes(tree_data["codeAdress"], [newdata])

def set_dungeon_warps(rom: RomData, patch_data):
    warp_matchings = patch_data["dungeon_entrances"]
    enter_values = {name: rom.read_word(dungeon["addr"]) for name, dungeon in DUNGEON_ENTRANCES.items()}
    exit_values = {name: rom.read_word(addr) for name, addr in DUNGEON_EXITS.items()}

    # Apply warp matchings expressed in the patch
    for from_name, to_name in warp_matchings.items():
        default_entrance_of_to_name = [name for name, dungeon in DUNGEON_ENTRANCES.items() if dungeon["default"] == to_name][0]
        default_exit_of_from_name = DUNGEON_ENTRANCES[from_name]["default"]
        entrance_addr = DUNGEON_ENTRANCES[from_name]["addr"]
        exit_addr = DUNGEON_EXITS[to_name]
        rom.write_word(entrance_addr, enter_values[default_entrance_of_to_name])
        rom.write_word(exit_addr, exit_values[default_exit_of_from_name])

    # Build a map dungeon => entrance (useful for essence warps)
    entrance_map = dict((v, k) for k, v in warp_matchings.items())

    # D1-D8 Essence Warps (hardcoded in one array using a unified format)
    for i in range(8):
        entrance_name = f"d{i + 1}"
        if i == 5:
            entrance_name += " past"
        entrance = DUNGEON_ENTRANCES[entrance_map[entrance_name]]
        rom.write_bytes(0x2874f + (i * 4), [
            entrance["group"] | 0x80,
            entrance["room"],
            entrance["position"],
            0x0e if entrance["shifted"] else 0x01
        ])

#    # Change Minimap popups to indicate the randomized dungeon's name
#    for i in range(8):
#        entrance_name = f"d{i}"
#        dungeon_index = int(warp_matchings[entrance_name][1:])
#        map_tile = DUNGEON_ENTRANCES[entrance_name]["map_tile"]
#        rom.write_byte(0x???? + map_tile, 0x81 | (dungeon_index << 3))

def define_dungeon_items_text_constants(assembler: Z80Assembler, patch_data):

    for i in range(0, 10): # D0 has no map, no compass, no boss key, and the unique small key use the default text. 
        # " for\nDungeon X"
        trueI = i if i != 9 else 6
        dungeon_precision = [0x03, 0x39, 0x44, 0x05, 0xe6, 0x20, (0x30 + trueI)]
        dungeon_tag = f"D{trueI}"
        dungeon_precisionForBossKey = dungeon_precision.copy()

        if i == 6:
            #\n(present)
            dungeon_precision.extend([0x01, 0x28, 0x03, 0x2e, 0x29])
            dungeon_tag += "Present"
        if i == 9:
            #\n(past)
            dungeon_precision.extend([0x01, 0x28, 0x70, 0x61, 0x73, 0x74, 0x29])
            dungeon_tag += "Past"

        # ###### Small keys ##############################################
        # "You found a\n\color(RED)"
        small_key_text = [0x02, 0x7c, 0x20, 0x61, 0x01, 0x09, 0x01]
        if patch_data["options"]["master_keys"]:
            # "Master Key"
            small_key_text.extend([0x4d, 0x61, 0x73, 0x74, 0x65, 0x72, 0x20, 0x03, 0x37])
        else:
            # "Small Key"
            small_key_text.extend([0x53, 0x6d, 0x04, 0xd2, 0x4b, 0x65, 0x79])
        if patch_data["options"]["keysanity_small_keys"]:
            small_key_text.extend(dungeon_precision)
        small_key_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.smallKey{dungeon_tag}", small_key_text)

        # Hero's Cave only has Small Keys, so skip other texts
        if i == 0:
            continue

        # ###### Boss keys ##############################################
        # "You found the\n\color(RED)Boss Key"
        if i < 9:
            boss_key_text = [
                0x02, 0x7c, 0x20, 0x05, 0xb4,
                0x09, 0x01, 0x42, 0x6f, 0x73, 0x73, 0x20, 0x4b, 0x65, 0x79
            ]
            if patch_data["options"]["keysanity_boss_keys"]:
                boss_key_text.extend(dungeon_precisionForBossKey)
            boss_key_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
            assembler.add_floating_chunk(f"text.bossKeyD{trueI}", boss_key_text)

        # ###### Dungeon maps ##############################################
        # "You found the\n\color(RED)"
        dungeon_map_text = [0x02, 0x7c, 0x20, 0x05, 0xb4, 0x09, 0x01]
        if patch_data["options"]["keysanity_maps_compasses"]:
            dungeon_map_text.extend([0x4d, 0x61, 0x70])  # "Map"
            dungeon_map_text.extend(dungeon_precision)
        else:
            dungeon_map_text.extend([0x44, 0x05, 0x8a, 0x20, 0x4d, 0x61, 0x70])  # "Dungeon Map"
        dungeon_map_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.dungeonMap{dungeon_tag}", dungeon_map_text)

        # ###### Compasses ##############################################
        # "You found the\n\color(RED)Compass"
        compasses_text = [
            0x02, 0x7c, 0x20, 0x05, 0xb4, 0x09, 0x01,
            0x09, 0x01, 0x43, 0x6f, 0x6d, 0x05, 0xfe
        ]
        if patch_data["options"]["keysanity_maps_compasses"]:
            compasses_text.extend(dungeon_precision)
        compasses_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.compass{dungeon_tag}", compasses_text)
