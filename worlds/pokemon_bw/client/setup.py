from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


async def early_setup(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:
    from .goals import get_method

    client.goal_checking_method = get_method(client, ctx)

    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.data_address_address, 3, client.ram_read_write_domain),
        )
    )
    client.save_data_address = int.from_bytes(read[0], "little")

    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.var_offset + (2*0x126), 4, client.ram_read_write_domain),
        )
    )
    client.received_items_count = int.from_bytes(read[0], "little")

    if ctx.slot_data["options"]["dexsanity"] == 0:
        client.dexsanity_included = False


async def late_setup(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:
    from ..data.items import seasons

    if ctx.slot_data["options"]["goal"] != "tmhm_hunt":
        await bizhawk.write(
            ctx.bizhawk_ctx, (
                (client.save_data_address+client.flags_offset+(0x192//8),
                 [client.flags_cache[0x192//8] | 4],
                 client.ram_read_write_domain),
            )
        )
    if ctx.slot_data["options"]["season_control"] == "vanilla":
        await bizhawk.write(
            ctx.bizhawk_ctx, (
                (client.save_data_address+client.flags_offset+(0x193//8),
                 [client.flags_cache[0x193//8] | 8],
                 client.ram_read_write_domain),
            )
        )
    elif ctx.slot_data["options"]["season_control"] == "randomized":
        for network_item in ctx.items_received:
            name = ctx.item_names.lookup_in_game(network_item.item)
            if name in seasons.table:
                await bizhawk.write(
                    ctx.bizhawk_ctx, (
                        (client.save_data_address+client.var_offset+(2*0xC1),
                         [seasons.table[name].var_value],
                         client.ram_read_write_domain),
                    )
                )
                break
