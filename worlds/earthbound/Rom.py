import hashlib
import os
import Utils
import typing
import bsdiff4
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .local_data import (item_id_table, location_dialogue, present_locations, psi_item_table, npc_locations, psi_locations, 
                         special_name_table, character_item_table, character_locations, locker_locations, starting_psi_table, item_space_checks,
                         special_name_overrides, protection_checks, badge_names, protection_text, local_present_types, nonlocal_present_types,
                         present_text_pointers, ap_text_pntrs, party_id_nums)
from .battle_bg_data import battle_bg_bpp
from .psi_shuffle import write_psi
from .text_data import barf_text, eb_text_table, text_encoder
from .flavor_data import flavor_data
from .enemy_data import combat_regions, scale_enemies
from BaseClasses import ItemClassification, CollectionState
from settings import get_settings
from typing import TYPE_CHECKING, Optional
from logging import warning
# from .local_data import local_locations

if TYPE_CHECKING:
    from . import EarthBoundWorld
valid_hashes = ["a864b2e5c141d2dec1c4cbed75a42a85",  # Cartridge
                "6d71ccc8e2afda15d011348291afdf4f"]  # VC


class LocalRom(object):

    def __init__(self, file: bytes, name: Optional[str] = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def patch_rom(world, rom, player: int, multiworld):
    starting_area_coordinates = {
                    0: [0x50, 0x04, 0xB5, 0x1F],  # North Onett
                    1: [0x52, 0x06, 0x4C, 0x1F],  # Onett
                    2: [0xEF, 0x22, 0x41, 0x1F],  # Twoson
                    3: [0x53, 0x06, 0x85, 0x1D],  # Happy Happy
                    4: [0x55, 0x24, 0x69, 0x1D],  # Threed
                    5: [0x60, 0x1D, 0x30, 0x01],  # Saturn Valley
                    6: [0xAB, 0x10, 0xF3, 0x09],  # Fourside
                    7: [0xE3, 0x09, 0xA3, 0x1D],  # Winters
                    8: [0xCB, 0x24, 0x7B, 0x1E],  # Summers
                    9: [0xD0, 0x1E, 0x31, 0x1D],  # Dalaam
                    10: [0xC7, 0x1F, 0x37, 0x19],  # Scaraba
                    11: [0xDD, 0x1B, 0xB7, 0x17],  # Deep Darkness
                    12: [0xD0, 0x25, 0x47, 0x18],  # Tenda Village
                    13: [0x9C, 0x00, 0x84, 0x17],  # Lost Underworld
                    14: [0x4B, 0x11, 0xAD, 0x18]  # Magicant
    }
    world.start_items = []
    world.handled_locations = []
    
    for item in world.multiworld.precollected_items[world.player]:
        world.start_items.append(item.name)

    if world.options.random_start_location != 0:
        rom.write_bytes(0x0F96C2, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9618, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9629, bytearray([0x69, 0x00]))  # Block Northern Onett
    else:
        rom.write_bytes(0x00B66A, bytearray([0x06]))  # Fix starting direction
    
    rom.write_bytes(0x01FE9B, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE9E, bytearray(starting_area_coordinates[world.start_location][2:4]))  # Start position

    rom.write_bytes(0x01FE91, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE8B, bytearray(starting_area_coordinates[world.start_location][2:4]))  # Respawn position

    if world.options.alternate_sanctuary_goal:
        rom.write_bytes(0x04FD72, bytearray([world.options.sanctuaries_required.value + 2]))
    else:
        rom.write_bytes(0x04FD72, bytearray([0xFF]))

    if world.options.giygas_required == 0:
        rom.write_bytes(0x2E9C29, bytearray([0x10, 0xA5]))

    if world.options.magicant_mode == 2:
        rom.write_bytes(0x04FD71, bytearray([world.options.sanctuaries_required.value + 1]))
        rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE]))  # Alt goal magicant sets the credits
    elif world.options.magicant_mode == 1:
        rom.write_bytes(0x2E9C29, bytearray([0x00, 0xA5]))
        if world.options.giygas_required:
            rom.write_bytes(0x2EA26A, bytearray([0x08, 0xD9, 0x9B, 0xEE]))  # Give stat boost if magicant + giygas required
        else:
            rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE]))  # If no giygas, set credits
    elif world.options.magicant_mode == 3:
        rom.write_bytes(0x2EA26A, bytearray([0x08, 0x0F, 0x9C, 0xEE]))  # Give only stat boost if set to boost

    rom.write_bytes(0x04FD74, bytearray([world.options.death_link.value]))
    rom.write_bytes(0x04FD75, bytearray([world.options.death_link_mode.value]))
    rom.write_bytes(0x04FD76, bytearray([world.options.remote_items.value]))

    if world.options.death_link_mode != 1:
        rom.write_bytes(0x2FFDFE, bytearray([0x80]))  # Mercy healing
        rom.write_bytes(0x2FFE30, bytearray([0x80]))  # Mercy text
        rom.write_bytes(0x2FFE59, bytearray([0x80]))  # Mercy revive
        # IF YOU ADD ASM, CHANGE THESE OR THE GAME WILL CRASH

    if world.options.monkey_caves_mode == 2:
        rom.write_bytes(0x062B87, bytearray([0x0A, 0x28, 0xCA, 0xEE]))
    elif world.options.monkey_caves_mode == 3:
        rom.write_bytes(0x0F1388, bytearray([0x03, 0xCA, 0xEE]))

    rom.write_bytes(0x04FD70, bytearray([world.options.sanctuaries_required.value]))

    for location in world.multiworld.get_locations(player):
        if location.address:
            receiver_name = world.multiworld.get_player_name(location.item.player)
            name = location.name
            if world.options.remote_items:
                item = "Remote Item"
            else:
                item = location.item.name
            item_name_loc = (((location.address - 0xEB0000) * 128) + 0x3F0000)
            item_text = bytearray(0)
            player_text = bytearray(0)
            for char in location.item.name[:128]:
                if char in eb_text_table:
                    item_text.extend(eb_text_table[char])
                else:
                    item_text.extend([0x6F])
            item_text.extend([0x00])
            player_name_loc = (((location.address - 0xEB0000) * 48) + 0x3F8000)
            for char in receiver_name[:48]:
                if char in eb_text_table:
                    player_text.extend(eb_text_table[char])
                else:
                    player_text.extend([0x6F])
            player_text.extend([0x00])
            rom.write_bytes(item_name_loc, bytearray(item_text))
            rom.write_bytes(player_name_loc, bytearray(player_text))

            if item not in item_id_table or location.item.player != location.player:
                item_id = 0xAD
            else:
                item_id = item_id_table[item]

            if name in location_dialogue:
                for i in range(len(location_dialogue[name])):
                    if location.item.player != location.player or item == "Remote Item":
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x17, location.address - 0xEB0000]))
                    elif item in item_id_table:
                        rom.write_bytes(location_dialogue[name][i], bytearray([item_id]))
                    elif item in psi_item_table or item in character_item_table:
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x16, special_name_table[item][0]]))

            if name in present_locations:
                world.handled_locations.append(name)
                if item == "Nothing":  # I can change this to "In nothing_table" later todo: make it so nonlocal items do not follow this table
                    rom.write_bytes(present_locations[name], bytearray([0x00, 0x00, 0x01]))
                elif location.item.player != location.player or item == "Remote Item":
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00, 0x00, (location.address - 0xEB0000)]))
                elif item in item_id_table:
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00]))
                elif item in psi_item_table:
                    rom.write_bytes(present_locations[name], bytearray([psi_item_table[item], 0x00, 0x02]))
                elif item in character_item_table:
                    rom.write_bytes(present_locations[name], bytearray([character_item_table[item][0], 0x00, 0x03]))

            if name in npc_locations:
                world.handled_locations.append(name)
                for i in range(len(npc_locations[name])):
                    if item in item_id_table or location.item.player != location.player or item == "Remote Item":
                        rom.write_bytes(npc_locations[name][i], bytearray([item_id]))
                    elif item in psi_item_table or item in character_item_table:
                        rom.write_bytes(npc_locations[name][i] - 3, bytearray([0x0E, 0x00, 0x0E, special_name_table[item][4]]))
                        rom.write_bytes(npc_locations[name][i] + 2, bytearray([0xA5, 0xAA, 0xEE]))

            if name in psi_locations:
                world.handled_locations.append(name)
                if item in special_name_table and location.item.player == location.player and item != "Remote Item":
                    rom.write_bytes(psi_locations[name][0], bytearray(special_name_table[item][1:4]))
                    rom.write_bytes(psi_locations[name][0] + 4, bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
                else:
                    rom.write_bytes(psi_locations[name][0], bytearray(psi_locations[name][1:4]))
                    rom.write_bytes(psi_locations[name][4], bytearray([item_id]))

            if name in character_locations:
                world.handled_locations.append(name)
                if item in character_item_table and location.item.player == location.player and item != "Remote Item":
                    rom.write_bytes(character_locations[name][0], bytearray(special_name_table[item][1:4]))
                    if name == "Snow Wood - Bedroom":  # Use lying down sprites for the bedroom check
                        rom.write_bytes(character_locations[name][1], bytearray(character_item_table[item][2:4]))
                        rom.write_bytes(0x0FB0D8, bytearray([0x06]))
                    else:
                        rom.write_bytes(character_locations[name][1], bytearray([character_item_table[item][1]]))
                elif item in psi_item_table and location.item.player == location.player:
                    rom.write_bytes(character_locations[name][0], bytearray(special_name_table[item][1:4]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x62]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x70, 0xF9, 0xD5]))
                else:
                    rom.write_bytes(character_locations[name][0], bytearray(character_locations[name][4:7]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x97]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x18, 0xF9, 0xD5]))
                    rom.write_bytes(character_locations[name][3], bytearray([item_id]))
                if name == "Deep Darkness - Barf Character":
                    if item in character_item_table and location.item.player == location.player:
                        rom.write_bytes(0x2EA0E2, bytearray(barf_text[item][0:3]))
                        rom.write_bytes(0x2EA0E8, bytearray(barf_text[item][3:6]))
                    elif item in psi_item_table and location.item.player == location.player:
                        rom.write_bytes(0x2EA0E2, bytearray([0x98, 0xC3, 0xEE]))
                        rom.write_bytes(0x2EA0E8, bytearray([0xF7, 0xC4, 0xEE]))
                    else:
                        rom.write_bytes(0x2EA0E2, bytearray([0x6A, 0xC3, 0xEE]))
                        rom.write_bytes(0x2EA0E8, bytearray([0xB4, 0xC4, 0xEE]))
            
            if name in locker_locations:
                world.handled_locations.append(name)
                if item in item_id_table or location.item.player != location.player or item == "Remote Item":
                    rom.write_bytes(locker_locations[name][0], bytearray([0xFF]))
                    rom.write_bytes(locker_locations[name][1], bytearray([item_id]))
                elif item in psi_item_table:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x02]))
                    rom.write_bytes(locker_locations[name][1], bytearray([psi_item_table[item]]))
                elif item in character_item_table:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x03]))
                    rom.write_bytes(locker_locations[name][1], bytearray(character_item_table[item]))

            if name == "Poo Starting Item":
                world.handled_locations.append(name)
                if item in item_id_table and location.item.player == location.player and item != "Remote Item":
                    rom.write_bytes(0x15F63C, bytearray([item_id]))
                else:
                    rom.write_bytes(0x15F63C, bytearray([0x00]))  # Don't give anything if the item doesn't have a tangible ID

                if item in special_name_table and location.item.player == location.player:  # Apply a special script if teleport or character
                    rom.write_bytes(0x15F7F6, bytearray(special_name_table[item][1:4]))
                    rom.write_bytes(0x2EC618, bytearray([special_name_table[item][4]]))
                    rom.write_bytes(0x2EC61A, bytearray([0xA5, 0xAA, 0xEE]))
            if name not in world.handled_locations:
                warning(f"{name} not placed in {world.multiworld.get_player_name(world.player)}'s EarthBound world. Something went wrong here.")
            
            if name in item_space_checks:
                if item not in item_id_table or location.item.player != location.player:
                    if len(item_space_checks[name]) == 4:
                        rom.write_bytes(item_space_checks[name][0], bytearray(item_space_checks[name][1:4]))
                    else:
                        rom.write_bytes(item_space_checks[name][0], bytearray(item_space_checks[name][1:4]))
                        rom.write_bytes(item_space_checks[name][4], bytearray(item_space_checks[name][5:8]))

            if name in special_name_overrides:
                if location.item.player != location.player:
                    rom.write_bytes(special_name_overrides[name], bytearray([0x1C, 0xB7, location.address - 0xEB0000]))
                else:
                    rom.write_bytes(special_name_overrides[name], bytearray([0x01, 0x01, 0x01]))

            if name in present_locations and "Lost Underworld" not in name and world.options.presents_match_contents:
                if location.item.classification & ItemClassification.trap:
                    world.present_type = "trap"
                elif location.item.classification & ItemClassification.progression:
                    world.present_type = "progression"
                elif location.item.classification & ItemClassification.useful:
                    world.present_type = "useful"
                else:
                    world.present_type = "filler"
                if location.item.player == world.player:
                    rom.write_bytes(present_locations[name] - 12, bytearray(local_present_types[world.present_type]))
                    if name != "Threed - Boogey Tent Trashcan":
                        rom.write_bytes(present_locations[name] - 4, bytearray(present_text_pointers[world.present_type]))
                else:
                    rom.write_bytes(present_locations[name] - 12, bytearray(nonlocal_present_types[world.present_type]))
                    if name != "Threed - Boogey Tent Trashcan":
                        if world.present_type == "progression":
                            rom.write_bytes(present_locations[name] - 4, bytearray(world.random.choice(ap_text_pntrs)))
                        elif world.present_type == "trap":
                            rom.write_bytes(present_locations[name] - 4, bytearray([0x8D, 0xce, 0xee]))
                        else:
                            rom.write_bytes(present_locations[name] - 4, bytearray([0xc1, 0xcd, 0xee]))

    if world.options.skip_prayer_sequences:
        rom.write_bytes(0x07BC96, bytearray([0x02]))
        rom.write_bytes(0x07BA2C, bytearray([0x02]))
        rom.write_bytes(0x07BAC7, bytearray([0x02]))
        rom.write_bytes(0x07BB38, bytearray([0x02]))
        rom.write_bytes(0x07BBF3, bytearray([0x02])) 
        rom.write_bytes(0x07BC56, bytearray([0x02])) 
        rom.write_bytes(0x07B9A1, bytearray([0x1f, 0xeb, 0xff, 0x02, 0x1f, 0x1f, 0xca, 0x01, 0x06, 0x1f, 0x1f, 0x72, 0x01, 0x06, 0x02]))  # Clean up overworld stuff

    if world.options.easy_deaths:
        rom.write_bytes(0x2EBFF9, bytearray([0x0A]))
        rom.write_bytes(0x04C7CE, bytearray([0x5C, 0x8A, 0xFB, 0xEF]))  # Jump to code that restores the party
        rom.write_bytes(0x04C7D4, bytearray([0xEA, 0xEA, 0xEA]))
        # rom.write_bytes(0x04C7DA, bytearray([0xEA, 0xEA]))#Stop the game from zeroing stuff
        rom.write_bytes(0x0912F2, bytearray([0x0A, 0xFE, 0xBF, 0xEE]))
        rom.write_bytes(0x2EBFFE, bytearray([0x00, 0x1B, 0x04, 0x15, 0x38, 0x1F, 0x81, 0xFF, 0xFF, 0x1B, 0x04, 0x0A, 0xF7, 0x12, 0xC9]))  # Hospitals = 0$
        rom.write_bytes(0x04C822, bytearray([0xEA, 0xEA, 0xEA, 0xEA]))

    if world.options.magicant_mode >= 2:
        rom.write_bytes(0x077629, bytearray([item_id_table[world.magicant_junk[0]]]))
        rom.write_bytes(0x077614, bytearray([item_id_table[world.magicant_junk[0]]]))
        rom.write_bytes(0x0FF25C, bytearray([item_id_table[world.magicant_junk[1]]]))
        rom.write_bytes(0x0FF27E, bytearray([item_id_table[world.magicant_junk[2]]]))
        rom.write_bytes(0x0FF28F, bytearray([item_id_table[world.magicant_junk[3]]]))
        rom.write_bytes(0x0FF2A0, bytearray([item_id_table[world.magicant_junk[4]]]))
        rom.write_bytes(0x0FF26D, bytearray([item_id_table[world.magicant_junk[5]]]))

    rom.write_bytes(0x02EC1AA, bytearray([world.options.sanctuaries_required.value]))
    if world.options.alternate_sanctuary_goal:
        rom.write_bytes(0x02EC1E2, bytearray([0xFD, 0xC1, 0xEE]))

    if world.options.magicant_mode == 1:
        rom.write_bytes(0x2EC1D8, bytearray([0x33, 0xC2, 0xEE]))
    elif world.options.magicant_mode == 2:
        rom.write_bytes(0x2EC1D8, bytearray([0x6A, 0xC2, 0xEE]))
    
    flavor_address = 0x3FAF10
    for i in range(4):
        rom.write_bytes(flavor_address, bytearray(world.flavor_text[i]))
        flavor_addr = flavor_address - 0x3F0000
        flavor_addr = struct.pack("H", flavor_addr)
        rom.write_bytes(world.flavor_pointer[i], flavor_addr)
        flavor_address += len(world.flavor_text[i])

    rom.write_bytes(0x202008, bytearray(flavor_data[world.available_flavors[0]]))
    rom.write_bytes(0x202048, bytearray(flavor_data[world.available_flavors[1]]))
    rom.write_bytes(0x202088, bytearray(flavor_data[world.available_flavors[2]]))
    rom.write_bytes(0x2020C8, bytearray(flavor_data[world.available_flavors[3]]))

    rom.write_bytes(0x048037, bytearray(world.lumine_text))
    starting_item_address = 0
    starting_psi = 0
    starting_char = 0
    starting_psi_types = []
    starting_character_count = []
    for item in world.multiworld.precollected_items[player]:
        if world.options.remote_items:
            continue

        if item.name == "Poo" and world.multiworld.get_location("Poo Starting Item", world.player).item.name in special_name_table:
            world.multiworld.push_precollected(world.multiworld.get_location("Poo Starting Item", world.player).item)

        if item.name in ["Progressive Bat", "Progressive Fry Pan", "Progressive Gun", "Progressive Bracelet",
                         "Progressive Other"]:
            old_item_name = item.name
            item.name = world.progressive_item_groups[item.name][world.start_prog_counts[item.name]]
            if world.start_prog_counts[old_item_name] != len(world.progressive_item_groups[old_item_name]) - 1:
                world.start_prog_counts[old_item_name] += 1

        if item.name in item_id_table:
            rom.write_bytes(0x17FC70 + starting_item_address, bytearray([item_id_table[item.name]]))
            starting_item_address += 1
        elif item.name in psi_item_table:
            if item.name != "Progressive Poo PSI":
                if item.name not in starting_psi_types:
                    rom.write_bytes(0x17FC7C + starting_psi, bytearray([starting_psi_table[item.name]]))
                    starting_psi_types.append(item.name)
                    starting_psi += 1
            else:
                if starting_psi_types.count(item.name) < 2:
                    rom.write_bytes(0x17FC7C + starting_psi, bytearray([starting_psi_table[item.name]]))
                    starting_psi_types.append(item.name)
                    starting_psi += 1
        elif item.name in character_item_table:
            if item.name not in starting_character_count:
                rom.write_bytes(0x17FC8D + starting_char, bytearray([party_id_nums[item.name]]))
                starting_character_count.append(item.name)
                starting_char += 1

    if world.options.random_battle_backgrounds:
        bpp2_bgs = [bg_id for bg_id, bpp in battle_bg_bpp.items() if bpp == 2]
        bpp4_bgs = [bg_id for bg_id, bpp in battle_bg_bpp.items() if bpp == 4]
        for i in range(483):
            world.flipped_bg = world.random.randint(0, 100)
            if i == 480:
                drawn_background = struct.pack("H", 0x00E3)
            else:
                drawn_background = struct.pack("H", world.random.randint(0x01, 0x0146))  # clearly this isn't giygas

            if battle_bg_bpp[struct.unpack("H", drawn_background)[0]] == 4:
                drawn_background_2 = struct.pack("H",  0x0000)
            else:
                drawn_background_2 = struct.pack("H", world.random.choice(bpp2_bgs))
            if world.flipped_bg > 33 or drawn_background not in bpp2_bgs:
                rom.write_bytes(0x0BD89A + (i * 4), drawn_background)
                rom.write_bytes(0x0BD89C + (i * 4), drawn_background_2)
            else:
                rom.write_bytes(0x0BD89A + (i * 4), drawn_background_2)
                rom.write_bytes(0x0BD89C + (i * 4), drawn_background)

    if not world.options.prefixed_items:
        rom.write_bytes(0x15F9DB, bytearray([0x06]))
        rom.write_bytes(0x15F9DD, bytearray([0x08]))
        rom.write_bytes(0x15F9DF, bytearray([0x05]))
        rom.write_bytes(0x15F9E1, bytearray([0x0B]))
        rom.write_bytes(0x15F9E3, bytearray([0x0F]))
        rom.write_bytes(0x15F9E4, bytearray([0x10]))
        # change if necessary

    world.Paula_placed = False
    world.Jeff_placed = False
    world.Poo_placed = False
    for sphere_number, sphere in enumerate(world.multiworld.get_spheres(), start=1):
        for location in sphere:
            if location.item.name == "Paula" and location.item.player == world.player and world.Paula_placed == False:
               world.Paula_region = location.parent_region
               world.Paula_placed = True
            elif location.item.name == "Jeff" and location.item.player == world.player and world.Jeff_placed == False:
               world.Jeff_region = location.parent_region
               world.Jeff_placed = True
            elif location.item.name == "Poo" and location.item.player == world.player and world.Poo_placed == False:
               world.Poo_region = location.parent_region
               world.Poo_placed = True

    if world.options.psi_shuffle:
        write_psi(world, rom)
    scale_enemies(world, rom)
    world.badge_name = badge_names[world.franklin_protection]
    world.badge_name = text_encoder(world.badge_name, eb_text_table, 23)
    world.badge_name.extend([0x00])
    rom.write_bytes(0x17FCD0, world.starting_money)
    rom.write_bytes(0x17FCE0, world.prayer_player)
    rom.write_bytes(0x155027, world.badge_name)
    rom.write_bytes(0x3FF0A0, world.world_version.encode("ascii"))

    for element in world.franklinbadge_elements:
        for address in protection_checks[element]:
            if element == world.franklin_protection:
                rom.write_bytes(address, [0xF0])
            else:
                rom.write_bytes(address, [0x80])
                # THIS WILL CRASH IF ADDRESS IS WRONG.
    rom.write_bytes(0x2EC909, bytearray(protection_text[world.franklin_protection][0:3]))  # help text
    rom.write_bytes(0x2EC957, bytearray(protection_text[world.franklin_protection][3:6]))  # battle text
    from Main import __version__
    rom.name = bytearray(f'MOM2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x00FFC0, rom.name)

    rom.write_file("token_patch.bin", rom.get_token_binary())


class EBProcPatch(APProcedurePatch, APTokenMixin):
    hash = valid_hashes
    game = "EarthBound"
    patch_file_ending = ".apeb"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["earthbound_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("repoint_vanilla_tables", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


class EBPatchExtensions(APPatchExtension):
    game = "EarthBound"

    @staticmethod
    def repoint_vanilla_tables(caller: APProcedurePatch, rom: LocalRom) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0x3FF0A0, 16)
        version_check = version_check.split(b'\x00', 1)[0]
        version_check_str = version_check.decode("ascii")
        client_version = "2.1"
        if client_version != version_check_str and version_check_str != "":
            raise Exception(f"Error! Patch generated on EarthBound APWorld version {version_check_str} doesn't match client version {client_version}! " +
                            f"Please use EarthBound APWorld version {version_check_str} for patching.")
        elif version_check_str == "":
            raise Exception(f"Error! Patch generated on old EarthBound APWorld version, doesn't match client version {client_version}! " +
                            f"Please verify you are using the same APWorld as the generator.")

        for action_number in range(0x013F):
            current_action = rom.read_bytes(0x157B68 + (12 * action_number), 12)
            rom.write_bytes(0x3FAFB0 + (12 * action_number), current_action)
        
        for psi_number in range(0x35):
            current_action = rom.read_bytes(0x158A50 + (15 * psi_number), 15)
            rom.write_bytes(0x350000 + (15 * psi_number), current_action)
        
        psi_text_table = rom.read_bytes(0x158D7A, (25 * 17))
        rom.write_bytes(0x3B0500, psi_text_table)

        psi_anim_config = rom.read_bytes(0x0CF04D, 0x0198)
        rom.write_bytes(0x360000, psi_anim_config)
        
        psi_anim_pointers = rom.read_bytes(0x0CF58F, 0x088)
        rom.write_bytes(0x360400, psi_anim_pointers)

        psi_anim_palettes = rom.read_bytes(0x0CF47F, 0x0110)
        rom.write_bytes(0x360600, psi_anim_palettes)

        for psi_number in range(0x32):
            psi_anim = rom.read_bytes(0x2F8583 + (0x04 * psi_number), 4)
            rom.write_bytes(0x3B0003 + (4 * psi_number), psi_anim)
            rom.write_bytes(0x3B0003, bytearray([0x4C]))
            # rom.write_bytes(0x3B0002, bytearray([0x45]))

        main_font_data = rom.read_bytes(0x210C7A, 96)
        main_font_gfx = rom.read_bytes(0x210CDA, 0x0C00)
        saturn_font_data = rom.read_bytes(0x201359, 96)
        saturn_font_gfx = rom.read_bytes(0x2013B9, 0x0C00)

        rom.write_bytes(0x3A0000, main_font_data)
        rom.write_bytes(0x3C0000, main_font_gfx)

        rom.write_bytes(0x3A0100, saturn_font_data)
        rom.write_bytes(0x3C0D00, saturn_font_gfx)
        #---------------------------------------
        #paula_level = rom.read_bytes(0x15f60f, 1)
        #jeff_level = rom.read_bytes(0x15f623, 1)
        #poo_level = rom.read_bytes(0x15f637, 1)

        #paula_start_exp = rom.read_bytes(0x?? + paula_level, ????)
        #jeff_start_exp = rom.read_bytes(0x?? + jeff_level, ????)
        #poo_start_exp = rom.read_bytes(0x?? + poo_level, ????)

        #rom.write_bytes(0x??, paula_start_exp)
        #rom.write_bytes(0x??, jeff_start_exp)
        #rom.write_bytes(0x??, poo_start_exp)
        return rom.get_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        rom_hash = basemd5.hexdigest
        if basemd5.hexdigest() not in valid_hashes:
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["earthbound_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


# Fix hint text, I have a special idea where I can give it info on a random region
