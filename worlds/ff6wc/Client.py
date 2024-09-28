import typing
import logging
from logging import Logger

from NetUtils import ClientStatus
from Utils import async_start
from worlds.AutoSNIClient import SNIClient

from . import Rom, Locations
from .id_maps import location_name_to_id
from .patch import FF6WCPatch

if typing.TYPE_CHECKING:
    from SNIClient import SNIClientCommandProcessor, SNIContext
else:
    SNIClientCommandProcessor = typing.Any
    SNIContext = typing.Any

snes_logger: Logger = logging.getLogger("SNES")


class FF6WCClient(SNIClient):
    game: str = "Final Fantasy 6 Worlds Collide"
    location_names: typing.List[str] = list(Rom.event_flag_location_names)
    location_ids: typing.Dict[str, int]
    patch_suffix = FF6WCPatch.patch_file_ending

    def __init__(self):
        super()
        self.location_ids = location_name_to_id

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom_name is None or rom_name[:3] != b"6WC":
            return False

        ctx.game = self.game
        # While this set of flags indicates a fully remote setup, it's worth noting we'll
        # be doing a hybrid approach, with only some "local" items being sent by the server.
        ctx.items_handling = 0b111

        ctx.rom = rom_name

        def cmd_debug(self: "SNIClientCommandProcessor", *args: str) -> None:
            client = self.ctx.client_handler
            if isinstance(client, FF6WCClient):
                if len(args) < 1:
                    snes_logger.info("/debug <address> [bit]")
                    return
                if len(args) > 1:
                    bit = int(args[1])
                else:
                    bit = None
                address_str = args[0]
                if address_str.startswith("0x"):
                    address = int(address_str[2:], 16)
                else:
                    address = int(address_str)
                async_start(client._print_ram(self.ctx, address, bit))
            else:
                snes_logger.info(f"not connected: {client=}")

        if __debug__:
            # TODO: fix typing in core
            if "debug" not in ctx.command_processor.commands:  # type: ignore
                ctx.command_processor.commands["debug"] = cmd_debug  # type: ignore

        return True

    async def _print_ram(self, ctx: SNIContext, address: int, bit: typing.Union[int, None] = None) -> None:
        from SNIClient import snes_read

        data = await snes_read(ctx, address, 1)
        if data is None:
            snes_logger.info("read failed")
            return
        if bit is None:
            value = data[0]
        else:
            value = bool(data[0] & (1 << bit))
        snes_logger.info(f"{hex(address)=} {bit=} {value=}")

    async def _new_location_check(self, ctx: SNIContext, location_name: str) -> None:
        """
        - add to `locations_checked`
        - put message in log
        - send location check to server
        """
        location_id = self.location_ids[location_name]
        ctx.locations_checked.add(location_id)
        if location_id in ctx.missing_locations:
            total_ap_location_count = len(ctx.missing_locations) + len(ctx.checked_locations)
            snes_logger.info(
                f"New Check: {location_name} ({len(ctx.checked_locations) + 1}/{total_ap_location_count})"
            )
        else:  # not an AP location in this seed
            snes_logger.info(f"Picked up: {location_name}")
        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_flush_writes
        if await self.connection_check(ctx) is False:
            return
        await self.location_check(ctx)
        await self.treasure_check(ctx)
        await self.received_items_check(ctx)
        await self.check_victory2(ctx)
        await snes_flush_writes(ctx)

    async def connection_check(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read
        rom = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom != ctx.rom:
            ctx.rom = None
            return False

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return False

        map_data = await snes_read(ctx, Rom.map_index_address, 2)
        if map_data is None:
            return False
        map_index = int.from_bytes(map_data, "little")
        map_index = Rom.get_map_index(map_index)
        if map_index < 6:
            return False
        if map_index == 255:
            return False
        if map_index == 51:
            # moogle defense room - don't give items here unless the moogle defense event is complete
            # because it will bug out if a character is received during the moogle defense event
            all_event_data = await snes_read(ctx, Rom.event_flag_base_address, 211)
            if not all_event_data:
                return False
            event_index, event_bit = Rom.get_event_flag_value(Rom.event_flag_location_names["Narshe Moogle Defense"])
            event_data = all_event_data[event_index]
            event_done = event_data & event_bit
            if not event_done:  # while in map_index 51
                return False

        menu_data = await snes_read(ctx, Rom.menu_address, 1)
        if menu_data is None:
            return False
        if menu_data[0] != 0:
            return False
        return True

    async def location_check(self, ctx: SNIContext) -> None:
        from SNIClient import snes_read
        all_event_data = await snes_read(ctx, Rom.event_flag_base_address, 211)
        if not all_event_data:
            snes_logger.debug("failed to read event data")
            return
        assert self.location_ids, "didn't get location_ids from connection"
        for location_index in range(len(Rom.event_flag_location_names)):
            location_name = self.location_names[location_index]
            location_id = self.location_ids[location_name]
            event_index, event_bit = Rom.get_event_flag_value(Rom.event_flag_location_names[location_name])
            event_data = all_event_data[event_index]

            # Have to special case these, since they work differently.
            if location_name in ["Lone Wolf 1", "Lone Wolf 2", "Narshe Weapon Shop 1", "Narshe Weapon Shop 3"]:
                if location_name[0] == "L":
                    initial_event_done = Rom.additional_event_flags["Lone Wolf Encountered"]
                    first_reward_chosen = Rom.additional_event_flags["Lone Wolf First Reward Picked"]
                    both_rewards_obtained = Rom.additional_event_flags["Lone Wolf Both Rewards Picked"]
                    location_one = "Lone Wolf 1"
                    location_two = "Lone Wolf 2"
                else:
                    initial_event_done = Rom.additional_event_flags["Narshe Weapon Shop Encountered"]
                    first_reward_chosen = Rom.additional_event_flags["Narshe Weapon Shop First Reward Picked"]
                    both_rewards_obtained = Rom.additional_event_flags["Narshe Weapon Shop Both Rewards Picked"]
                    location_one = "Narshe Weapon Shop 1"
                    location_two = "Narshe Weapon Shop 2"
                event_index, event_bit = Rom.get_event_flag_value(initial_event_done)
                first_reward_index, first_reward_bit = Rom.get_event_flag_value(first_reward_chosen)
                both_rewards_index, both_rewards_bit = Rom.get_event_flag_value(both_rewards_obtained)
                initial_event_data = all_event_data[event_index]
                first_reward_data = all_event_data[first_reward_index]
                both_rewards_data = all_event_data[both_rewards_index]

                initial_event_status = initial_event_data & event_bit
                both_rewards_status = both_rewards_data & both_rewards_bit
                if initial_event_status or both_rewards_status:
                    first_reward_status = first_reward_data & first_reward_bit
                    locations_cleared: typing.List[str] = []
                    if first_reward_status:
                        locations_cleared.append(location_one)
                    else:
                        locations_cleared.append(location_two)
                    if both_rewards_status:
                        locations_cleared = [location_one, location_two]
                    for location_name in locations_cleared:
                        location_id = self.location_ids[location_name]
                        if location_id not in ctx.locations_checked:
                            await self._new_location_check(ctx, location_name)
            else:
                event_done = event_data & event_bit
                if event_done and location_id not in ctx.locations_checked:
                    if location_name in Locations.point_of_no_return_checks.keys():
                        for passed_location in Locations.point_of_no_return_checks[location_name]:
                            passed_id = self.location_ids[passed_location]
                            if passed_id not in ctx.locations_checked:
                                await self._new_location_check(ctx, passed_location)
                    await self._new_location_check(ctx, location_name)

    async def treasure_check(self, ctx: SNIContext) -> None:
        from SNIClient import snes_read
        treasure_data = await snes_read(ctx, Rom.treasure_chest_base_address, 40)

        if treasure_data is not None:
            assert self.location_ids
            for chest in Rom.treasure_chest_data.keys():
                treasure_byte, treasure_bit = Rom.get_treasure_chest_bit(chest)
                treasure_found = treasure_data[treasure_byte] & treasure_bit
                treasure_id = self.location_ids[chest]
                if treasure_found and treasure_id not in ctx.locations_checked:
                    await self._new_location_check(ctx, chest)

    async def received_items_check(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_read
        items_received_data = await snes_read(ctx, Rom.items_received_address, 2)
        if items_received_data is None:
            return
        items_received_amount = int.from_bytes(items_received_data, "little")
        if items_received_amount >= len(ctx.items_received):
            return
        else:
            item = ctx.items_received[items_received_amount]
            item_name = ctx.item_names.lookup_in_game(item.item)
            item_id = item.item
            allow_local_network_item = False
            if item.player == ctx.slot:
                assert self.location_ids
                if item.location == self.location_ids["Veldt"]:
                    allow_local_network_item = True
                elif item_name not in Rom.item_name_id.keys():
                    allow_local_network_item = True
                elif item.location < 0:  # sent from server command, not location check
                    allow_local_network_item = True
                else:
                    self.increment_items_received(ctx, items_received_amount)
                    return
            if item.player == ctx.slot and not allow_local_network_item:
                return
            if item_name in Rom.characters:
                character_index = Rom.characters.index(item_name)
                character_init_byte, character_init_bit = Rom.get_character_initialized_bit(character_index)
                character_init_data = await snes_read(ctx, character_init_byte, 1)
                if character_init_data is None:
                    return

                character_recruit_byte, character_recruit_bit = Rom.get_character_recruited_bit(character_index)
                character_recruit_data = await snes_read(ctx, character_recruit_byte, 1)
                if character_recruit_data is None:
                    return

                character_count = await snes_read(ctx, Rom.characters_obtained_address, 1)
                if character_count is None:
                    return

                swdtech_data = await snes_read(ctx, Rom.swdtech_byte, 1)
                blitz_data = await snes_read(ctx, Rom.blitz_byte, 1)
                if swdtech_data is None:
                    return
                if blitz_data is None:
                    return
                character_count = character_count[0]
                character_initialized = character_init_data[0] & character_init_bit
                character_recruited = character_recruit_data[0] & character_recruit_bit
                character_name = Rom.characters[character_index]
                logging.debug(f"{character_initialized=} {character_recruited=} {character_name=}")
                character_ap_id = item_id
                character_item = next((item for item in ctx.items_received if item.item == character_ap_id), None)
                if character_item is not None:
                    new_init_data = character_init_data[0] | character_init_bit
                    if new_init_data == character_init_data[0]:
                        self.increment_items_received(ctx, items_received_amount)
                        return
                    new_recruit_data = character_recruit_data[0] | character_recruit_bit
                    snes_buffered_write(ctx, character_init_byte, bytes([new_init_data]))
                    snes_buffered_write(ctx, character_recruit_byte, bytes([new_recruit_data]))
                    self.increment_items_received(ctx, items_received_amount)

                    snes_buffered_write(ctx, Rom.swdtech_byte, bytes([swdtech_data[0] | 1]))
                    snes_buffered_write(ctx, Rom.blitz_byte, bytes([blitz_data[0] | 1]))

                    snes_buffered_write(ctx, Rom.characters_obtained_address, bytes([character_count + 1]))
                    snes_logger.info('Received %s from %s (%s)' % (
                        ctx.item_names.lookup_in_game(character_item.item),
                        ctx.player_names[character_item.player],
                        ctx.location_names.lookup_in_slot(character_item.location, character_item.player)))
            elif item_name in Rom.espers:
                esper_index = Rom.espers.index(item_name)
                esper_byte, esper_bit = Rom.get_obtained_esper_bit(esper_index)
                esper_data = await snes_read(ctx, esper_byte, 1)
                if esper_data is None:
                    return
                esper_count = await snes_read(ctx, Rom.espers_obtained_address, 1)
                if esper_count is None:
                    return
                esper_count = esper_count[0]
                esper_obtained = esper_data[0] & esper_bit
                new_data = esper_data[0] | esper_bit
                snes_buffered_write(ctx, esper_byte, bytes([new_data]))

                self.increment_items_received(ctx, items_received_amount)
                if esper_obtained == 0:
                    snes_buffered_write(ctx, Rom.espers_obtained_address, bytes([esper_count + 1]))
                snes_logger.info('Received %s from %s (%s)' % (
                    ctx.item_names.lookup_in_game(item.item),
                    ctx.player_names[item.player],
                    ctx.location_names.lookup_in_slot(item.location, item.player)))

            else:
                item_types_data = await snes_read(ctx, Rom.item_types_base_address, 255)
                item_quantities_data = await snes_read(ctx, Rom.item_quantities_base_address, 255)
                if item_types_data is None or item_quantities_data is None:
                    return
                reserved_slots: typing.List[int] = []
                # Field items
                for i in range(0, 255):
                    slot = item_types_data[i]
                    quantity = item_quantities_data[i]
                    exists = False
                    if slot == Rom.item_name_id[item_name]:
                        exists = True
                    if (slot == 255 or quantity == 0 or exists is True):
                        reserved_slots.append(i)
                        type_destination = Rom.item_types_base_address + i
                        amount_destination = Rom.item_quantities_base_address + i
                        type_id = Rom.item_name_id[item_name]
                        amount = quantity + 1
                        snes_buffered_write(ctx, type_destination, bytes([type_id]))
                        snes_buffered_write(ctx, amount_destination, bytes([amount]))
                        self.increment_items_received(ctx, items_received_amount)
                        snes_logger.info('Received %s from %s (%s)' % (
                            item_name,
                            ctx.player_names[item.player],
                            ctx.location_names.lookup_in_slot(item.location, item.player)))
                        break

    async def check_victory1(self, ctx: SNIContext) -> None:
        from SNIClient import snes_read
        formation_data = await snes_read(ctx, Rom.formation_id, 2)
        if formation_data is None:
            return
        animation_data = await snes_read(ctx, Rom.animation_byte, 1)
        if animation_data is None:
            return
        formation_value = int.from_bytes(formation_data, "little")
        animation_value = animation_data[0]
        # for now
        if formation_value == 0x0202 and animation_value == 0x01:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    async def check_victory2(self, ctx: SNIContext) -> None:
        from SNIClient import snes_read
        victory_data = await snes_read(ctx, Rom.victory_address, 1)
        if victory_data is None:
            return

        victory_value = victory_data[0]
        # for now
        if victory_value & 0x02:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def increment_items_received(self, ctx: SNIContext, items_received_amount: int) -> None:
        from SNIClient import snes_buffered_write
        items_received_amount += 1
        snes_buffered_write(ctx, Rom.items_received_address, items_received_amount.to_bytes(2, 'little'))
