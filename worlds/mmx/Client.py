import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

MMX_RAM = WRAM_START + 0x1EE00

MMX_GAME_STATE          = WRAM_START + 0x000D1
MMX_MENU_STATE          = WRAM_START + 0x000D2
MMX_GAMEPLAY_STATE      = WRAM_START + 0x000D3
MMX_LEVEL_INDEX         = WRAM_START + 0x01F7A

MMX_WEAPON_ARRAY            = WRAM_START + 0x01F88
MMX_SUB_TANK_ARRAY          = WRAM_START + 0x01F83
MMX_UPGRADES                = WRAM_START + 0x01F99
MMX_HEART_TANKS             = WRAM_START + 0x01F9C
MMX_HADOUKEN                = WRAM_START + 0x01F7E
MMX_LIFE_COUNT              = WRAM_START + 0x01F80
MMX_MAX_HP                  = WRAM_START + 0x01F9A
MMX_CURRENT_HP              = WRAM_START + 0x00BCF
MMX_UNLOCKED_CHARGED_SHOT   = MMX_RAM + 0x0016
MMX_UNLOCKED_AIR_DASH       = MMX_RAM + 0x0022
MMX_FORTRESS_PROGRESS       = WRAM_START + 0x01F7B

MMX_SFX_FLAG            = MMX_RAM + 0x0003
MMX_SFX_NUMBER          = MMX_RAM + 0x0004

MMX_SIGMA_ACCESS            = MMX_RAM + 0x0002
MMX_COLLECTED_HEART_TANKS   = MMX_RAM + 0x0005
MMX_COLLECTED_UPGRADES      = MMX_RAM + 0x0006
MMX_COLLECTED_HADOUKEN      = MMX_RAM + 0x0007
MMX_DEFEATED_BOSSES         = MMX_RAM + 0x0080
MMX_COMPLETED_LEVELS        = MMX_RAM + 0x0060
MMX_COLLECTED_PICKUPS       = MMX_RAM + 0x00C0
MMX_UNLOCKED_LEVELS         = MMX_RAM + 0x0040

MMX_RECV_INDEX          = MMX_RAM + 0x0000
MMX_ENERGY_LINK_PACKET  = MMX_RAM + 0x0009
MMX_VALIDATION_CHECK    = MMX_RAM + 0x0013

MMX_RECEIVING_ITEM          = MMX_RAM + 0x0015
MMX_ENABLE_HEART_TANK       = MMX_RAM + 0x000B
MMX_ENABLE_HP_REFILL        = MMX_RAM + 0x000F
MMX_HP_REFILL_AMOUNT        = MMX_RAM + 0x0010
MMX_ENABLE_GIVE_1UP         = MMX_RAM + 0x0012
MMX_ENABLE_WEAPON_REFILL    = MMX_RAM + 0x001A
MMX_WEAPON_REFILL_AMOUNT    = MMX_RAM + 0x001B

MMX_SCREEN_BRIGHTNESS  = WRAM_START + 0x000B3
MMX_PAUSE_STATE        = WRAM_START + 0x01F24
MMX_CAN_MOVE           = WRAM_START + 0x01F13

MMX_PICKUPSANITY_ACTIVE    = ROM_START + 0x167C27
MMX_ENERGY_LINK_ENABLED    = ROM_START + 0x167C28
MMX_DEATH_LINK_ACTIVE      = ROM_START + 0x167C29
MMX_JAMMED_BUSTER_ACTIVE   = ROM_START + 0x167C2A
MMX_ABILITIES_FLAGS        = ROM_START + 0x167C31

MMX_ENERGY_LINK_COUNT      = MMX_RAM + 0x00100
MMX_GLOBAL_TIMER           = MMX_RAM + 0x00106
MMX_GLOBAL_DEATHS          = MMX_RAM + 0x0010A
MMX_GLOBAL_DMG_DEALT       = MMX_RAM + 0x0010C
MMX_GLOBAL_DMG_TAKEN       = MMX_RAM + 0x0010E
MMX_CHECKPOINTS_REACHED    = MMX_RAM + 0x00120
MMX_REFILL_REQUEST         = MMX_RAM + 0x00110
MMX_REFILL_TARGET          = MMX_RAM + 0x00111
MMX_ARSENAL_SYNC           = MMX_RAM + 0x00112

EXCHANGE_RATE = 500000000

STARTING_ID = 0xBE0800

MMX_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

PICKUP_ITEMS = ["1up", "hp refill", "weapon refill"]

class MMXSNIClient(SNIClient):
    game = "Mega Man X"
    patch_suffix = ".apmmx"

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.last_death_link = 0
        self.energy_link_enabled = False
        self.heal_request_command = None
        self.weapon_refill_request_command = None
        self.using_newer_client = False
        self.energy_link_details = False
        self.trade_request = None
        self.data_storage_enabled = False
        self.save_arsenal = False
        self.resync_request = False
        self.current_level_value = 42
        self.item_queue = []


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX_CAN_MOVE, 0x7)
        pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            pause_state[0] != 0x00 or \
            can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
            receiving_item[0] != 0x00:
            return
        
        snes_buffered_write(ctx, MMX_CURRENT_HP, bytes([0x80]))
        snes_buffered_write(ctx, WRAM_START + 0x00BAA, bytes([0x0C]))
        snes_buffered_write(ctx, WRAM_START + 0x00C12, bytes([0x0C]))
        snes_buffered_write(ctx, WRAM_START + 0x00BAB, bytes([0x00]))
        snes_buffered_write(ctx, WRAM_START + 0x00BD7, bytes([0x08]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        energy_link = await snes_read(ctx, MMX_ENERGY_LINK_ENABLED, 0x1)
        rom_name = await snes_read(ctx, MMX_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"MMX1":
            if "resync" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("resync")
            if "trade" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("trade")
            if "heal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("heal")
            if "refill" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("refill")
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True
        if energy_link[0]:
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["heal"] = cmd_heal
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["refill"] = cmd_refill
        if "resync" not in ctx.command_processor.commands:
            ctx.command_processor.commands["resync"] = cmd_resync
        if "trade" not in ctx.command_processor.commands:
            ctx.command_processor.commands["trade"] = cmd_trade

        death_link = await snes_read(ctx, MMX_DEATH_LINK_ACTIVE, 1)
        if death_link[0]:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        ctx.rom = rom_name

        return True
     
    
    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        game_state = await snes_read(ctx, MMX_GAME_STATE, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)

        # Discard uninitialized ROMs
        if menu_state is None:
            self.game_state = False
            self.energy_link_enabled = False
            self.current_level_value = 42
            self.item_queue = []
            return
    
        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            return

        if game_state[0] == 0:
            self.game_state = False
            self.item_queue = []
            self.current_level_value = 42
            ctx.locations_checked = set()
            
            # Resync data if solicited 
            if self.resync_request:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"mmx_arsenal_{ctx.team}_{ctx.slot}", "operations":
                        [{"operation": "replace", "value": dict()}],
                }])
                self.resync_request = False
                logger.info(f"Successfully cleared save data!")
            return
        
        if self.resync_request:
            self.resync_request = False
            logger.info(f"Invalid environment for a resync. Please try again during the Title Menu screen.")
        
        self.game_state = True
        if "DeathLink" in ctx.tags and menu_state[0] == 0x04 and ctx.last_death_link + 1 < time.time():
            currently_dead = gameplay_state[0] == 0x06
            await ctx.handle_deathlink_state(currently_dead)
        
        if game_state[0] != 0x00 and self.data_storage_enabled is True:
            await self.handle_data_storage(ctx)

        # Handle DataStorage
        if ctx.server and ctx.server.socket.open and not self.data_storage_enabled and ctx.team is not None:
            self.data_storage_enabled = True
            ctx.set_notify(f"mmx_global_timer_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_deaths_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_damage_taken_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_damage_dealt_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_checkpoints_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_arsenal_{ctx.team}_{ctx.slot}")

        if self.trade_request is not None:
            await self.handle_hp_trade(ctx)

        await self.handle_item_queue(ctx)

        # This is going to be rewritten whenever SNIClient supports on_package
        energy_link = await snes_read(ctx, MMX_ENERGY_LINK_ENABLED, 0x1)
        if self.using_newer_client:
            if energy_link[0] != 0:
                await self.handle_energy_link(ctx)
        else:
            if energy_link[0] != 0:
                if self.energy_link_enabled and f'EnergyLink{ctx.team}' in ctx.stored_data:
                    await self.handle_energy_link(ctx)

                if ctx.server and ctx.server.socket.open and not self.energy_link_enabled and ctx.team is not None:
                    self.energy_link_enabled = True
                    ctx.set_notify(f"EnergyLink{ctx.team}")
                    logger.info(f"Initialized EnergyLink{ctx.team}, use /help to get information about the EnergyLink commands.")

        from .Rom import weapon_rom_data, upgrades_rom_data, boss_access_rom_data, refill_rom_data
        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        defeated_bosses = list(await snes_read(ctx, MMX_DEFEATED_BOSSES, 0x20))
        cleared_levels = list(await snes_read(ctx, MMX_COMPLETED_LEVELS, 0x20))
        collected_heart_tanks = int.from_bytes(await snes_read(ctx, MMX_COLLECTED_HEART_TANKS, 0x01))
        collected_upgrades = int.from_bytes(await snes_read(ctx, MMX_COLLECTED_UPGRADES, 0x01))
        collected_hadouken = int.from_bytes(await snes_read(ctx, MMX_COLLECTED_HADOUKEN, 0x01))
        collected_pickups = list(await snes_read(ctx, MMX_COLLECTED_PICKUPS, 0x20))
        pickupsanity_enabled = int.from_bytes(await snes_read(ctx, MMX_PICKUPSANITY_ACTIVE, 0x1))
        completed_intro_level = int.from_bytes(await snes_read(ctx, WRAM_START + 0x01F9B, 0x1))
        new_checks = []
        for loc_name, data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x000:
                    # Boss clear
                    if defeated_bosses[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x001:
                    # Maverick Medal
                    if cleared_levels[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x002:
                    # Heart Tank
                    masked_data = collected_heart_tanks & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x003:
                    # Mega Man upgrades
                    masked_data = collected_upgrades & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x004:
                    # Sub Tank
                    masked_data = collected_upgrades & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x005:
                    # Hadouken
                    if collected_hadouken != 0x00:
                        new_checks.append(loc_id)
                elif internal_id == 0x007:
                    # Intro
                    if game_state[0] == 0x02 and \
                       menu_state[0] == 0x00 and \
                       gameplay_state[0] == 0x01 and \
                       completed_intro_level == 0x04:
                        new_checks.append(loc_id)
                elif internal_id == 0x020:
                    # Pickups
                    if not pickupsanity_enabled or pickupsanity_enabled == 0:
                        continue
                    if collected_pickups[data_bit] != 0:
                        new_checks.append(loc_id)
 
        verify_game_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 1)
        if verify_game_state is None:
            snes_logger.info(f'Exit Game.')
            return
        
        rom = await snes_read(ctx, MMX_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            snes_logger.info(f'Exit ROM.')
            return
        
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # Send Current Room for Tracker
        current_level = int.from_bytes(await snes_read(ctx, MMX_LEVEL_INDEX, 0x1), "little")

        if game_state[0] == 0x00 or \
           (game_state[0] == 0x02 and menu_state[0] != 0x04):
            current_level = -1

        if self.current_level_value != (current_level + 1):
            self.current_level_value = current_level + 1

            # Send level id data to tracker
            await ctx.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": f"mmx1_level_id_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [
                            {
                                "operation": "replace",
                                "value": self.current_level_value,
                            }
                        ],
                    }
                ]
            )

        recv_count = await snes_read(ctx, MMX_RECV_INDEX, 2)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        recv_index = int.from_bytes(recv_count, "little")
        sync_arsenal = int.from_bytes(await snes_read(ctx, MMX_ARSENAL_SYNC, 0x2), "little")

        if recv_index < len(ctx.items_received) and sync_arsenal != 0x1337:
            item = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            
            snes_buffered_write(ctx, MMX_RECV_INDEX, bytes([recv_index]))
            await snes_flush_writes(ctx)
            
            if item.item in weapon_rom_data:
                self.add_item_to_queue("weapon", item.item)

            elif item.item == STARTING_ID + 0x0013:
                self.add_item_to_queue("heart tank", item.item)

            elif item.item == STARTING_ID + 0x0014:
                self.add_item_to_queue("sub tank", item.item)

            elif item.item in upgrades_rom_data:
                self.add_item_to_queue("upgrade", item.item)

            elif item.item in boss_access_rom_data:
                if item.item == STARTING_ID + 0x000A:
                    snes_buffered_write(ctx, MMX_SIGMA_ACCESS, bytearray([0x00]))
                boss_access = bytearray(await snes_read(ctx, MMX_UNLOCKED_LEVELS, 0x20))
                level = boss_access_rom_data[item.item]
                boss_access[level[0]] = 0x01
                snes_buffered_write(ctx, MMX_UNLOCKED_LEVELS, boss_access)
                snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x2D]))
                self.save_arsenal = True

            elif item.item in refill_rom_data:
                self.add_item_to_queue(refill_rom_data[item.item][0], item.item, refill_rom_data[item.item][1])
                self.save_arsenal = True

            elif item.item == STARTING_ID:
                # Handle goal
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                self.save_arsenal = True
                return
                
        # Handle collected locations
        game_state = await snes_read(ctx, MMX_GAME_STATE, 0x1)
        if game_state[0] != 0x02:
            ctx.locations_checked = set()
            return
        new_boss_clears = False
        new_cleared_level = False
        new_heart_tank = False
        new_upgrade = False
        new_pickup = False
        new_hadouken = False
        cleared_levels = list(await snes_read(ctx, MMX_COMPLETED_LEVELS, 0x20))
        collected_pickups = list(await snes_read(ctx, MMX_COLLECTED_PICKUPS, 0x40))
        defeated_bosses = list(await snes_read(ctx, MMX_DEFEATED_BOSSES, 0x20))
        collected_heart_tanks = int.from_bytes(await snes_read(ctx, MMX_COLLECTED_HEART_TANKS, 0x01))
        collected_upgrades = int.from_bytes(await snes_read(ctx, MMX_COLLECTED_UPGRADES, 0x01))
        collected_hadouken = int.from_bytes(await snes_read(ctx, MMX_COLLECTED_HADOUKEN, 0x01))
        i = 0
        for loc_id in ctx.checked_locations:
            if loc_id not in ctx.locations_checked:
                ctx.locations_checked.add(loc_id)
                loc_name = ctx.location_names.lookup_in_game(loc_id)

                if loc_name not in location_id_to_level_id:
                    continue

                logging.info(f"Recovered checks ({i:03}): {loc_name}")
                i += 1

                data = location_id_to_level_id[loc_name]
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x000:
                    # Boss clear
                    defeated_bosses[data_bit] = 1
                    new_boss_clears = True
                elif internal_id == 0x001:
                    # Maverick Medal
                    cleared_levels[data_bit] = 0xFF
                    new_cleared_level = True
                elif internal_id == 0x002:
                    # Heart Tank
                    collected_heart_tanks |= data_bit
                    new_heart_tank = True
                elif internal_id == 0x003:
                    # Mega Man upgrades
                    collected_upgrades |= data_bit
                    new_upgrade = True
                elif internal_id == 0x004:
                    # Sub Tank
                    collected_upgrades |= data_bit
                    new_upgrade = True
                elif internal_id == 0x005:
                    # Hadouken
                    collected_hadouken = 0xFF
                    new_hadouken = True
                elif internal_id == 0x20:
                    # Pickups
                    collected_pickups[data_bit] = 0x01
                    new_pickup = True

        if new_cleared_level:
            snes_buffered_write(ctx, MMX_COMPLETED_LEVELS, bytes(cleared_levels))
        if new_boss_clears:
            snes_buffered_write(ctx, MMX_DEFEATED_BOSSES, bytes(defeated_bosses))
        if new_pickup:
            snes_buffered_write(ctx, MMX_COLLECTED_PICKUPS, bytes(collected_pickups))
        if new_hadouken:
            snes_buffered_write(ctx, MMX_COLLECTED_HADOUKEN, bytearray([collected_hadouken]))
        if new_upgrade:
            snes_buffered_write(ctx, MMX_COLLECTED_UPGRADES, bytearray([collected_upgrades]))
        if new_heart_tank:
            snes_buffered_write(ctx, MMX_COLLECTED_HEART_TANKS, bytearray([collected_heart_tanks]))
        await snes_flush_writes(ctx)

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            ctx.set_notify(f"mmx_global_timer_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_deaths_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_damage_taken_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_damage_dealt_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_checkpoints_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx_arsenal_{ctx.team}_{ctx.slot}")
            slot_data = args.get("slot_data", None)
            self.using_newer_client = True
            if slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Energy: Standby"
                    logger.info(f"Initialized EnergyLink{ctx.team}")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if ctx.ui:
                pool = (args["value"] or 0) / EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Energy: {pool:.2f}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Energy: {pool:.2f}"


    async def handle_hp_trade(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Can only process trades during the pause state
        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            receiving_item[0] != 0x00:
            return
        
        for item in self.item_queue:
            if item[0] == "weapon refill":
                self.trade_request = None
                logger.info(f"You already have a Weapon Energy request pending to be received.")
                return

        # Can trade HP -> WPN if HP is above 1
        current_hp = await snes_read(ctx, MMX_CURRENT_HP, 0x1)
        if current_hp[0] > 0x01:
            max_trade = current_hp[0] - 1
            set_trade = self.trade_request if self.trade_request <= max_trade else max_trade
            self.add_item_to_queue("weapon refill", None, set_trade)
            new_hp = current_hp[0] - set_trade
            snes_buffered_write(ctx, MMX_CURRENT_HP, bytearray([new_hp]))
            await snes_flush_writes(ctx)
            self.trade_request = None
            logger.info(f"Traded {set_trade} HP for {set_trade} Weapon Energy.")
        else:
            logger.info("Couldn't process trade. HP is too low.")


    async def handle_energy_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return
        
        # Deposit heals into the pool regardless of energy_link setting
        energy_packet = await snes_read(ctx, MMX_ENERGY_LINK_PACKET, 0x2)
        if energy_packet is None:
            return
        energy_packet_raw = energy_packet[0] | (energy_packet[1] << 8)
        energy_packet = (energy_packet_raw * EXCHANGE_RATE) >> 4
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                    [{"operation": "add", "value": energy_packet},
                    {"operation": "max", "value": 0}],
            }])
            pool = ((ctx.stored_data[f'EnergyLink{ctx.team}'] or 0) / EXCHANGE_RATE) + (energy_packet_raw / 16)
            snes_buffered_write(ctx, MMX_ENERGY_LINK_PACKET, bytearray([0x00, 0x00]))
            await snes_flush_writes(ctx)

        # Expose EnergyLink to the ROM
        pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX_SCREEN_BRIGHTNESS, 0x1)
        if pause_state[0] != 0x00 or screen_brightness[0] == 0x0F:
            pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
            total_energy = int(pool / EXCHANGE_RATE)
            if total_energy < 9999:
                snes_buffered_write(ctx, MMX_ENERGY_LINK_COUNT, bytearray([total_energy & 0xFF, (total_energy >> 8) & 0xFF]))
            else:
                snes_buffered_write(ctx, MMX_ENERGY_LINK_COUNT, bytearray([0x0F, 0x27]))

        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX_CAN_MOVE, 0x7)
        heart_tank = await snes_read(ctx, MMX_ENABLE_HEART_TANK, 0x1)
        hp_refill = await snes_read(ctx, MMX_ENABLE_HP_REFILL, 0x1)
        weapon_refill = await snes_read(ctx, MMX_ENABLE_WEAPON_REFILL, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
            receiving_item[0] != 0x00 or \
            heart_tank[0] != 0x00 or \
            hp_refill[0] != 0x00 or \
            weapon_refill[0] != 0x00:
            return
        
        skip_hp = False
        skip_weapon = False
        for item in self.item_queue:
            if item[0] == "hp refill":
                skip_hp = True
                self.heal_request_command = None
            elif item[0] == "weapon refill":
                skip_weapon = True
                self.weapon_refill_request_command = None
            
        pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
        if not skip_hp or not skip_weapon:
            # Handle in-game requests
            request = int.from_bytes(await snes_read(ctx, MMX_REFILL_REQUEST, 0x1), "little")
            target = int.from_bytes(await snes_read(ctx, MMX_REFILL_TARGET, 0x1), "little")
            if request != 0:
                if target == 0:
                    if self.heal_request_command is None:
                        self.heal_request_command = request
                else: 
                    if self.weapon_refill_request_command is None:
                        self.weapon_refill_request_command = request
                snes_buffered_write(ctx, MMX_REFILL_REQUEST, bytearray([0x00]))

        if not skip_hp:
            # Handle heal requests
            if self.heal_request_command:
                heal_needed = self.heal_request_command
                heal_needed_rate = heal_needed * EXCHANGE_RATE
                if pool < EXCHANGE_RATE:
                    logger.info(f"There's not enough Energy for your request ({heal_needed}). Energy available: {pool / EXCHANGE_RATE:.2f}")
                    self.heal_request_command = None
                    return
                elif pool < heal_needed_rate:
                    heal_needed = int(pool / EXCHANGE_RATE)
                    heal_needed_rate = heal_needed * EXCHANGE_RATE
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                        [{"operation": "add", "value": -heal_needed_rate},
                        {"operation": "max", "value": 0}],
                }])
                self.add_item_to_queue("hp refill", None, heal_needed)
                pool = (pool / EXCHANGE_RATE) - heal_needed
                logger.info(f"Healed by {heal_needed}. Energy available: {pool:.2f}")
                self.heal_request_command = None

        if not skip_weapon:
            # Handle weapon refill requests
            if self.weapon_refill_request_command:
                heal_needed = self.weapon_refill_request_command
                heal_needed_rate = heal_needed * EXCHANGE_RATE
                if pool < EXCHANGE_RATE:
                    logger.info(f"There's not enough Energy for your request ({heal_needed}). Energy available: {pool / EXCHANGE_RATE:.2f}")
                    self.weapon_refill_request_command = None
                    return
                elif pool < heal_needed_rate:
                    heal_needed = int(pool / EXCHANGE_RATE)
                    heal_needed_rate = heal_needed * EXCHANGE_RATE
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                        [{"operation": "add", "value": -heal_needed_rate},
                        {"operation": "max", "value": 0}],
                }])
                self.add_item_to_queue("weapon refill", None, heal_needed)
                pool = (pool / EXCHANGE_RATE) - heal_needed
                logger.info(f"Refilled current weapon by {heal_needed}. Energy available: {pool:.2f}")
                self.weapon_refill_request_command = None


    def add_item_to_queue(self, item_type, item_id, item_additional = None):
        if not hasattr(self, "item_queue"):
            self.item_queue = []
        self.item_queue.append([item_type, item_id, item_additional])


    async def handle_item_queue(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Rom import weapon_rom_data, upgrades_rom_data

        if not hasattr(self, "item_queue") or len(self.item_queue) == 0:
            return

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Do not give items if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        progress = await snes_read(ctx, MMX_FORTRESS_PROGRESS, 0x1)
        can_move = await snes_read(ctx, MMX_CAN_MOVE, 0x7)
        hp_refill = await snes_read(ctx, MMX_ENABLE_HP_REFILL, 0x1)
        weapon_refill = await snes_read(ctx, MMX_ENABLE_WEAPON_REFILL, 0x1)
        if menu_state[0] != 0x04 or \
           gameplay_state[0] != 0x04 or \
           progress[0] >= 0x04 or \
           hp_refill[0] != 0x00 or \
           weapon_refill[0] != 0x00 or \
           can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
           receiving_item[0] != 0x00:
            return
        
        next_item = self.item_queue[0]
        item_id = next_item[1]
        
        if next_item[0] in PICKUP_ITEMS:
            backup_item = self.item_queue.pop(0)
        
            if "hp refill" in next_item[0]:
                current_hp = await snes_read(ctx, MMX_CURRENT_HP, 0x1)
                max_hp = await snes_read(ctx, MMX_MAX_HP, 0x1)

                if current_hp[0] < max_hp[0]:
                    snes_buffered_write(ctx, MMX_ENABLE_HP_REFILL, bytearray([0x02]))
                    snes_buffered_write(ctx, MMX_HP_REFILL_AMOUNT, bytearray([next_item[2]]))
                    snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))
                else:
                    # TODO: Sub Tank logic
                    self.item_queue.append(backup_item)

            elif next_item[0] == "weapon refill":
                snes_buffered_write(ctx, MMX_ENABLE_WEAPON_REFILL, bytearray([0x02]))
                snes_buffered_write(ctx, MMX_WEAPON_REFILL_AMOUNT, bytearray([next_item[2]]))
                snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))

            elif next_item[0] == "1up":
                life_count = await snes_read(ctx, MMX_LIFE_COUNT, 0x1)
                if life_count[0] < 99:
                    snes_buffered_write(ctx, MMX_ENABLE_GIVE_1UP, bytearray([0x01]))
                    snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))
                    self.save_arsenal = True
                else:
                    self.item_queue.append(backup_item)

        pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX_SCREEN_BRIGHTNESS, 0x1)
        if pause_state[0] != 0x00 or screen_brightness[0] != 0x0F:
            await snes_flush_writes(ctx)
            if len(self.item_queue) != 0:
                backup_item = self.item_queue.pop(0)
                self.item_queue.append(backup_item)
            return
        
        if next_item[0] == "weapon":
            weapon = weapon_rom_data[item_id]
            snes_buffered_write(ctx, WRAM_START + weapon[0], bytearray([weapon[1]]))
            snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x0D]))
            self.item_queue.pop(0)
            self.save_arsenal = True
            
        elif next_item[0] == "heart tank":
            heart_tanks = await snes_read(ctx, MMX_HEART_TANKS, 0x1)
            heart_tanks = heart_tanks[0]
            heart_tank_count = heart_tanks.bit_count()
            if heart_tank_count < 8:
                heart_tanks |= 1 << heart_tank_count
                snes_buffered_write(ctx, MMX_HEART_TANKS, bytearray([heart_tanks]))
                snes_buffered_write(ctx, MMX_ENABLE_HEART_TANK, bytearray([0x02]))
                snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))
            self.item_queue.pop(0)
            self.save_arsenal = True

        elif next_item[0] == "sub tank":
            upgrades = await snes_read(ctx, MMX_UPGRADES, 0x1)
            sub_tanks = await snes_read(ctx, MMX_SUB_TANK_ARRAY, 0x4)
            sub_tanks = list(sub_tanks)
            upgrade = upgrades[0]
            upgrade = upgrade & 0xF0
            sub_tank_count = upgrade.bit_count()
            if sub_tank_count < 4:
                upgrade = upgrades[0]
                upgrade |= 0x10 << sub_tank_count
                sub_tanks[sub_tank_count] = 0x8E
                snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrade]))
                snes_buffered_write(ctx, MMX_SUB_TANK_ARRAY, bytearray(sub_tanks))
                snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x17]))
            self.item_queue.pop(0)
            self.save_arsenal = True
        
        elif next_item[0] == "upgrade":
            upgrades = await snes_read(ctx, MMX_UPGRADES, 0x1)

            upgrade = upgrades_rom_data[item_id]
            bit = 1 << upgrade[0]
            check = upgrades[0] & bit

            if bit == 0x08:
                air_dash_check = int.from_bytes(await snes_read(ctx, MMX_ABILITIES_FLAGS, 0x1), "little") & 0x02
                if air_dash_check != 0:
                    # check now becomes the air dash flag
                    check = int.from_bytes(await snes_read(ctx, MMX_UNLOCKED_AIR_DASH, 0x1), "little")

            if check == 0:
                # Armor
                upgrades = upgrades[0]
                original_value = upgrades
                upgrades |= bit
                if bit == 0x01:
                    snes_buffered_write(ctx, WRAM_START + 0x0BBE, bytearray([0x18]))
                    snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                    snes_buffered_write(ctx, WRAM_START + 0x1EE19, bytearray([0x80]))
                elif bit == 0x02:
                    jam_check = await snes_read(ctx, MMX_JAMMED_BUSTER_ACTIVE, 0x1)
                    charge_shot_unlocked = await snes_read(ctx, MMX_UNLOCKED_CHARGED_SHOT, 0x1)
                    if jam_check[0] == 1 and charge_shot_unlocked[0] == 0:
                        snes_buffered_write(ctx, MMX_UNLOCKED_CHARGED_SHOT, bytearray([0x01]))
                    else:
                        value = await snes_read(ctx, WRAM_START + 0x0C38, 0x1)
                        snes_buffered_write(ctx, WRAM_START + 0x0C38, bytearray([value[0] + 1]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C42, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C43, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C39, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C48, bytearray([0x5D]))
                        snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                elif bit == 0x04:
                    value = await snes_read(ctx, WRAM_START + 0x0C58, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0C58, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C62, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C63, bytearray([0x01]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C59, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C68, bytearray([0x5D]))
                    snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                elif bit == 0x08:
                    if air_dash_check != 0 and original_value & bit == 0x08:
                        snes_buffered_write(ctx, MMX_UNLOCKED_AIR_DASH, bytearray([0x01]))
                    else:
                        value = await snes_read(ctx, WRAM_START + 0x0C78, 0x1)
                        snes_buffered_write(ctx, WRAM_START + 0x0C78, bytearray([value[0] + 1]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C82, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C83, bytearray([0x02]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C79, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C88, bytearray([0x5D]))
                        snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x2B]))
            self.item_queue.pop(0)
            self.save_arsenal = True

        await snes_flush_writes(ctx)


    async def handle_data_storage(self, ctx):
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes
        # Only do arsenal after the map's initial load or the intro stage is selected
        menu_state = int.from_bytes(await snes_read(ctx, MMX_MENU_STATE, 0x1))
        gameplay_state = int.from_bytes(await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1))
        map_state = int.from_bytes(await snes_read(ctx, WRAM_START + 0x1E49, 0x1))
        sync_arsenal = int.from_bytes(await snes_read(ctx, MMX_ARSENAL_SYNC, 0x2), "little")
        if (menu_state == 0x00 and map_state == 0x04) or (menu_state == 0x04 and gameplay_state == 0x04):
            # Load Arsenal
            if sync_arsenal == 0x1337:
                arsenal = ctx.stored_data[f"mmx_arsenal_{ctx.team}_{ctx.slot}"] or dict()
                if arsenal:
                    # Data in arsenal
                    snes_buffered_write(ctx, MMX_RECV_INDEX, bytes(arsenal["recv_index"].to_bytes(2, 'little')))
                    snes_buffered_write(ctx, MMX_LIFE_COUNT, bytes(arsenal["life_count"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_UPGRADES, bytes(arsenal["upgrades"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_MAX_HP, bytes(arsenal["max_hp"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_HEART_TANKS, bytes(arsenal["heart_tanks"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_SUB_TANK_ARRAY, bytearray(arsenal["sub_tanks"]))
                    snes_buffered_write(ctx, MMX_UNLOCKED_CHARGED_SHOT, bytes(arsenal["unlocked_buster"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_UNLOCKED_AIR_DASH, bytes(arsenal["unlocked_air_dash"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_WEAPON_ARRAY, bytearray(arsenal["weapons"]))
                    snes_buffered_write(ctx, MMX_HADOUKEN, bytes(arsenal["hadouken"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX_UNLOCKED_LEVELS, bytearray(arsenal["levels"]))
                    snes_buffered_write(ctx, MMX_SIGMA_ACCESS, bytes(arsenal["sigma_access"].to_bytes(1, 'little')))

                snes_buffered_write(ctx, MMX_ARSENAL_SYNC, bytearray([0x00,0x00]))
                await snes_flush_writes(ctx)

        # Save Arsenal
        if self.save_arsenal and sync_arsenal != 0x1337:
            arsenal = dict()
            arsenal["recv_index"] = int.from_bytes(await snes_read(ctx, MMX_RECV_INDEX, 0x2), "little")
            arsenal["life_count"] = int.from_bytes(await snes_read(ctx, MMX_LIFE_COUNT, 0x1), "little")
            arsenal["upgrades"] = int.from_bytes(await snes_read(ctx, MMX_UPGRADES, 0x1), "little")
            arsenal["max_hp"] = int.from_bytes(await snes_read(ctx, MMX_MAX_HP, 0x1), "little")
            arsenal["heart_tanks"] = int.from_bytes(await snes_read(ctx, MMX_HEART_TANKS, 0x1), "little")
            arsenal["sub_tanks"] = list(await snes_read(ctx, MMX_SUB_TANK_ARRAY, 0x4))
            arsenal["unlocked_buster"] = int.from_bytes(await snes_read(ctx, MMX_UNLOCKED_CHARGED_SHOT, 0x1), "little")
            arsenal["unlocked_air_dash"] = int.from_bytes(await snes_read(ctx, MMX_UNLOCKED_AIR_DASH, 0x1), "little")
            arsenal["weapons"] = list(await snes_read(ctx, MMX_WEAPON_ARRAY, 0x10))
            arsenal["hadouken"] = int.from_bytes(await snes_read(ctx, MMX_HADOUKEN, 0x1), "little")
            arsenal["levels"] = list(await snes_read(ctx, MMX_UNLOCKED_LEVELS, 0x20))
            arsenal["sigma_access"] = int.from_bytes(await snes_read(ctx, MMX_SIGMA_ACCESS, 0x1), "little")
            
            # Attempt to not lose any previously saved data in case of RAM corruption
            saved_arsenal = ctx.stored_data[f"mmx_arsenal_{ctx.team}_{ctx.slot}"] or dict()
            if saved_arsenal:
                if saved_arsenal["recv_index"] > arsenal["recv_index"]:
                    arsenal["recv_index"] = saved_arsenal["recv_index"]
                if saved_arsenal["life_count"] > arsenal["life_count"]:
                    arsenal["life_count"] = saved_arsenal["life_count"]
                if saved_arsenal["max_hp"] > arsenal["max_hp"]:
                    arsenal["max_hp"] = saved_arsenal["max_hp"]
                for i in range(0x10):
                    arsenal["weapons"][i] |= saved_arsenal["weapons"][i] & 0x40
                for level in range(0x20):
                    arsenal["levels"][level] |= saved_arsenal["levels"][level]
                arsenal["sigma_access"] = min(saved_arsenal["sigma_access"], arsenal["sigma_access"])
                    
                arsenal["upgrades"] |= saved_arsenal["upgrades"]
                arsenal["unlocked_buster"] |= saved_arsenal["unlocked_buster"]
                arsenal["unlocked_air_dash"] |= saved_arsenal["unlocked_air_dash"]
                arsenal["hadouken"] |= saved_arsenal["hadouken"] & 0xE0
                arsenal["heart_tanks"] |= saved_arsenal["heart_tanks"]
                for i in range(0x4):
                    arsenal["sub_tanks"][i] |= saved_arsenal["sub_tanks"][i] & 0x80

            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx_arsenal_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": arsenal}],
            }])
            self.save_arsenal = False

        keys = {
            f"mmx_checkpoints_{ctx.team}_{ctx.slot}",
            f"mmx_global_timer_{ctx.team}_{ctx.slot}",
            f"mmx_deaths_{ctx.team}_{ctx.slot}",
            f"mmx_damage_dealt_{ctx.team}_{ctx.slot}",
            f"mmx_damage_taken_{ctx.team}_{ctx.slot}",
        }
        if not all(key in ctx.stored_data.keys() for key in keys):
            return

        # Checkpoints reached
        checkpoints = list(await snes_read(ctx, MMX_CHECKPOINTS_REACHED, 0xF))
        data_storage_checkpoints = ctx.stored_data[f"mmx_checkpoints_{ctx.team}_{ctx.slot}"] or [0 for _ in range(0xF)]
        computed_checkpoints = list()
        for i in range(0xF):
            if checkpoints[i] >= data_storage_checkpoints[i]:
                computed_checkpoints.append(checkpoints[i])
            else:
                computed_checkpoints.append(data_storage_checkpoints[i])
        await ctx.send_msgs([{
            "cmd": "Set", "key": f"mmx_checkpoints_{ctx.team}_{ctx.slot}", "operations":
                [{"operation": "replace", "value": computed_checkpoints}],
        }])
        snes_buffered_write(ctx, MMX_CHECKPOINTS_REACHED, bytes(computed_checkpoints))

        # Global timer
        timer = int.from_bytes(await snes_read(ctx, MMX_GLOBAL_TIMER, 0x4), "little")
        data_storage_timer = ctx.stored_data[f"mmx_global_timer_{ctx.team}_{ctx.slot}"] or 0
        if timer >= data_storage_timer:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx_global_timer_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": timer},
                        {"operation": "min", "value": 0x03E73B3B}],
            }])
        else:
            snes_buffered_write(ctx, MMX_GLOBAL_TIMER, data_storage_timer.to_bytes(4, "little"))

        # Death count
        deaths = int.from_bytes(await snes_read(ctx, MMX_GLOBAL_DEATHS, 0x2), "little")
        data_storage_deaths = ctx.stored_data[f"mmx_deaths_{ctx.team}_{ctx.slot}"] or 0
        if deaths >= data_storage_deaths:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx_deaths_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": deaths},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX_GLOBAL_DEATHS, data_storage_deaths.to_bytes(2, "little"))

        # Damage dealt
        dmg_dealt = int.from_bytes(await snes_read(ctx, MMX_GLOBAL_DMG_DEALT, 0x2), "little")
        data_storage_dmg_dealt = ctx.stored_data[f"mmx_damage_dealt_{ctx.team}_{ctx.slot}"] or 0
        if dmg_dealt >= data_storage_dmg_dealt:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx_damage_dealt_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": dmg_dealt},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX_GLOBAL_DMG_DEALT, data_storage_dmg_dealt.to_bytes(2, "little"))
        
        # Damage taken
        dmg_taken = int.from_bytes(await snes_read(ctx, MMX_GLOBAL_DMG_TAKEN, 0x2), "little")
        data_storage_dmg_taken = ctx.stored_data[f"mmx_damage_taken_{ctx.team}_{ctx.slot}"] or 0
        if dmg_taken >= data_storage_dmg_taken:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx_damage_taken_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": dmg_taken},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX_GLOBAL_DMG_TAKEN, data_storage_dmg_taken.to_bytes(2, "little"))
        
        await snes_flush_writes(ctx)


def cmd_heal(self, amount: str = ""):
    """
    Request healing from EnergyLink.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.heal_request_command is not None:
            logger.info(f"You already placed a healing request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much HP you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much HP you will recover.")
                return
            self.ctx.client_handler.heal_request_command = amount
            logger.info(f"Requested {amount} HP from the energy pool.")
        else:
            logger.info(f"You need to specify how much HP you will request.")


def cmd_refill(self, amount: str = ""):
    """
    Request weapon energy from EnergyLink.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.weapon_refill_request_command is not None:
            logger.info(f"You already placed a weapon refill request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            self.ctx.client_handler.weapon_refill_request_command = amount
            logger.info(f"Requested {amount} Weapon Energy from the energy pool.")
        else:
            logger.info(f"You need to specify how much Weapon Energy you will request.")

def cmd_trade(self, amount: str = ""):
    """
    Trades HP to Weapon Energy. 1:1 ratio.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.trade_request is not None:
            logger.info(f"You already placed a weapon refill request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            self.ctx.client_handler.trade_request = amount
            logger.info(f"Set up trade for {amount} Weapon Energy. Pause the game to process the trade.")
        else:
            logger.info(f"You need to specify how much Weapon Energy you will request.")


def cmd_resync(self):
    """
    Resets the save data to force Archipelago to send over every item again. Locations reached aren't affected.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in the title screen.")
    else:
        if self.ctx.client_handler.resync_request:
            logger.info(f"You already placed a resync request.")
            return
        else:
            self.ctx.client_handler.resync_request = True
            logger.info(f"Placing a resync request...")
