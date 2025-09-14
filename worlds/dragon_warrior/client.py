import logging
from worlds._bizhawk.client import BizHawkClient
from NetUtils import ClientStatus, NetworkItem, color
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

nes_logger = logging.getLogger("NES")
logger = logging.getLogger("Client")

EXPECTED_ROM_NAME = "DWAPV"
EXPECTED_VERSION = "050"
EQUIPMENT_BYTES = [0x1, 0x2, 0x3, 0x4, 0x8, 0xC, 0x10, 0x14, 0x18, 0x1C, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0]

class DragonWarriorClient(BizHawkClient):
    game = "Dragon Warrior"
    system = "NES"
    patch_suffix = ".apdw"
    item_queue: List[NetworkItem] = []

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from worlds._bizhawk import RequestFailedError, read
        try:
            # Check ROM name/patch version
            rom_name_bytes, version_bytes = (await read(ctx.bizhawk_ctx, [(0x7FE0, 5, "PRG ROM"),
                                                                          (0x7FE5, 4, "PRG ROM")]))

            if rom_name_bytes[:5].decode("ascii") != EXPECTED_ROM_NAME:
                logger.info(
                    "Expected: " + EXPECTED_ROM_NAME + ", got: " + rom_name_bytes[:5].decode("ascii")
                )
                return False
            
            if version_bytes[:3].decode("ascii") != EXPECTED_VERSION:
                logger.info(
                    "WARNING: Version mismatch, this was generated on an earlier version of the apworld and may not function as expected"
                )
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111

        return True
    
    async def game_watcher(self, ctx):
        from worlds._bizhawk import read, write

        if ctx.server is None or ctx.slot is None:
            return
        
        current_map, chests_array, recv_count, inventory_bytes, \
            dragonlord_dead, herbs, equip_byte, level_byte, gold_byte, \
            ap_byte, status_byte = await read(ctx.bizhawk_ctx, [
            (0x45, 1, "RAM"),
            (0x601C, 16, "System Bus"), # Bruh moment
            (0x0E, 1, "RAM"),
            (0xC1, 4, "RAM"),
            (0xE4, 1, "RAM"),
            (0xC0, 1, "RAM"),
            (0xBE, 1, "RAM"),
            (0xC7, 1, "RAM"),
            (0xBD, 1, "RAM"),
            (0x01, 1, "RAM"),
            (0xDF, 1, "RAM") 
        ])

        if current_map[0] == 0:  # Don't start processing until we load a map
            return
        
        # Search for new location checks
        new_checks = []

        # Game Completion
        dragonlord_dead = dragonlord_dead[0] & 0x4
        if not ctx.finished_game and dragonlord_dead:
            if 0xDD not in ctx.checked_locations:
                new_checks.append(0xDD)  # Send Ball of Light victory item
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

        # Send Shop Hints
        equipment_locations = []
        match current_map[0]:
            case 0x07: # Kol
                equipment_locations = [0x01, 0x10, 0x14, 0x60, 0x80]
            case 0x08: # Brecconary
                equipment_locations = [0x01, 0x04, 0x08, 0x20, 0x40, 0x60]
            case 0x09: # Garinham
                equipment_locations = [0x02, 0x08, 0x0C, 0x10, 0x40, 0x60, 0x80]
            case 0x0A: # Cantlin
                equipment_locations = [0x02, 0x03, 0x0C, 0x10, 0x14, 0x18, 0x20, 0x40, 0x60, 0xA0, 0xC0]
            case 0x0B: # Rimuldar 
                equipment_locations = [0x10, 0x14, 0x18, 0x60, 0x80, 0xA0]
        
        if equipment_locations:
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": equipment_locations,
                "create_as_hint": 2
            }])

        # Chest checks, See locations.py for an explanation
        for i in range(0, 16, 2):
            chest = chests_array[i:i + 2]
            # I hate working with bytes in Python
            location_data = int(hex((current_map[0] << 16) | ((chest[0] << 8) | chest[1])), 16)
            if location_data not in ctx.checked_locations:
                new_checks.append(location_data)

        # Level checks
        for level in range(1, level_byte[0] + 1):
            location_data = "0xD"
            if level < 10:
                location_data += "0"
            location_data += str(level)
            location_data = int(location_data, 16)
            if location_data not in ctx.checked_locations:
                new_checks.append(location_data)

        # Search spot checks
        if ap_byte[0] in [0x81, 0x41, 0x21]:   # +1 offset to have compatibility with equipment checks
            location_data = 0xE00 | (ap_byte[0] - 1)
            if location_data not in ctx.checked_locations:
                new_checks.append(location_data)
        
        # Rainbow drop
        if ap_byte[0] == 0xFF:
            if 0xFF not in ctx.checked_locations:
                new_checks.append(0xFF)

         # Princess Rescue - Carrying Gwaelin
        status_bits = status_byte

        if status_bits[0] & 0x01:  # From mcgrew notes This is picking her up
            gwaelin_location = 0x150513
            if gwaelin_location not in ctx.checked_locations:
                new_checks.append(gwaelin_location)

        # Princess returned - trigger Gwaelin's Love item check
        if status_bits[0] & 0x02:
            love_location = 0x050304
            if love_location not in ctx.checked_locations: 
               new_checks.append(love_location)



        # Buying equipment
        if ap_byte[0] in EQUIPMENT_BYTES:
            if ap_byte[0] not in ctx.checked_locations:
                new_checks.append(ap_byte[0])

        # Send found checks
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            nes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # Receive Items
        # Compare items_received index in the RAM at 0x0E to len(ctx.items_received)
        # If smaller, we should grant the missing items
        writes = []
        important_items = [0x5, 0x7, 0x8, 0xA, 0xC, 0xD, 0xE]
        filler_items = [0x1, 0x2, 0x3, 0x4, 0x6, 0x9, 0xB]

        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            if item.item in important_items:  # Quest item, add to inventory no matter what

                found_space = False

                for i in range(len(inventory_bytes)):
                    slot = inventory_bytes[i]
                    hi_item = ((slot & 0xF0) >> 4)
                    lo_item = slot & 0xF

                    if hi_item == 0:
                        new_byte = (item.item << 4) + lo_item
                        found_space = True
                    elif lo_item == 0:
                        new_byte = (hi_item << 4) + item.item
                        found_space = True
                    if found_space:
                        writes.append((0xC1 + i, new_byte.to_bytes(1, 'little'), "RAM"))
                        break

                if not found_space:  # No free space found, kick out a filler item
                    for i in range(len(inventory_bytes)):
                        slot = inventory_bytes[i]
                        hi_item = ((slot & 0xF0) >> 4)
                        lo_item = slot & 0xF

                        if hi_item in filler_items:
                            new_byte = (item.item << 4) + lo_item
                            found_space = True
                        elif lo_item in filler_items:
                            new_byte = (hi_item << 4) + item.item
                            found_space = True
                        if found_space:
                            writes.append((0xC1 + i, new_byte.to_bytes(1, 'little'), "RAM"))
                            break

            elif item.item < 0xF: # Non-herb consumable, add to inventory if space
                
                found_space = False

                for i in range(len(inventory_bytes)):
                    slot = inventory_bytes[i]
                    hi_item = ((slot & 0xF0) >> 4)
                    lo_item = slot & 0xF

                    if hi_item == 0:
                        new_byte = (item.item << 4) + lo_item
                        found_space = True
                    elif lo_item == 0:
                        new_byte = (hi_item << 4) + item.item
                        found_space = True
                    if found_space:
                        writes.append((0xC1 + i, new_byte.to_bytes(1, 'little'), "RAM"))
                        break
            
            elif item.item == 0xD4:  # Magic Key
                writes.append((0xBF, bytes.fromhex('01'), "RAM"))

            # Make sure there's no overflow when receiving gold
            elif item.item == 0xD1 and gold_byte[0] < 0xFF:  # Gold (256)
                writes.append((0xBD, (gold_byte[0] + 1).to_bytes(1, 'little'), "RAM"))
            
            elif item.item == 0xD2 and gold_byte[0] < 0xFA:  # High Gold (1536)
                writes.append((0xBD, (gold_byte[0] + 6).to_bytes(1, 'little'), "RAM"))
            
            elif item.item == 0xF and herbs[0] < 0xFF:  # Medicinal herb
                writes.append((0xC0, (herbs[0] + 1).to_bytes(1, 'little'), "RAM"))

            elif item.item == 0xFF: # Erdrick's Sword
                new_byte = equip_byte[0] | 0xE0
                writes.append((0xBE, new_byte.to_bytes(1, 'little'), "RAM"))
            elif item.item == 0xFE: # Erdrick's Armor
                new_byte = equip_byte[0] | 0x1C
                writes.append((0xBE, new_byte.to_bytes(1, 'little'), "RAM"))
            
            elif item.item in [0xE01, 0xE04, 0xE20]:  # Progressive equipment
                to_add = item.item & 0xFF
                new_byte = equip_byte[0] + to_add
                if new_byte <= 0xFF:
                    writes.append((0xBE, new_byte.to_bytes(1, 'little'), "RAM"))

            writes.append((0x0E, recv_index.to_bytes(1, 'little'), "RAM"))
        
        await write(ctx.bizhawk_ctx, writes)

        
