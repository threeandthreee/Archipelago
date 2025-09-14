from typing import TYPE_CHECKING, Sequence
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

    if ctx.slot_data["options"]["dexsanity"] == 0:
        client.dexsanity_included = False


async def late_setup(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:
    from ..data.items import seasons
    from .items import reload_key_items

    await reload_key_items(client, ctx)

    writes: list[tuple[int, Sequence[int], str]] = []

    if ctx.slot_data["options"]["goal"] not in ("tmhm_hunt", "pokemon_master"):
        writes.append((
            client.save_data_address+client.flags_offset+(0x192//8),
            [client.flags_cache[0x192//8] | 4],
            client.ram_read_write_domain
        ))

    if ctx.slot_data["options"]["season_control"] == "vanilla":
        writes.append((
            client.save_data_address+client.flags_offset+(0x193//8),
            [client.flags_cache[0x193//8] | 8],
            client.ram_read_write_domain
        ))
    elif ctx.slot_data["options"]["season_control"] == "randomized":
        for network_item in ctx.items_received:
            name = ctx.item_names.lookup_in_game(network_item.item)
            if name in seasons.table:
                writes.append((
                    client.save_data_address+client.var_offset+(2*0xC1),
                    [seasons.table[name].var_value],
                    client.ram_read_write_domain
                ))
                break

    master_ball_cost: int = ctx.slot_data["master_ball_seller_cost"]
    writes.append((
        client.save_data_address + client.var_offset + (2 * 0xF2),
        master_ball_cost.to_bytes(2, "little"),
        client.ram_read_write_domain
    ))
    if "N's Castle" in ctx.slot_data["options"]["master_ball_seller"]:
        writes.append((
            client.save_data_address+client.flags_offset+(0x1CF//8),
            [client.flags_cache[0x1CF//8] | 128],
            client.ram_read_write_domain
        ))
    if "PC" in ctx.slot_data["options"]["master_ball_seller"]:
        writes.append((
            client.save_data_address+client.flags_offset+(0x1D1//8),
            [client.flags_cache[0x1D1//8] | 2],
            client.ram_read_write_domain
        ))
    if "Cheren's Mom" in ctx.slot_data["options"]["master_ball_seller"]:
        writes.append((
            client.save_data_address+client.flags_offset+(0x1D2//8),
            [client.flags_cache[0x1D2//8] | 4],
            client.ram_read_write_domain
        ))
    if "Undella Mansion seller" in ctx.slot_data["options"]["master_ball_seller"]:
        writes.append((
            client.save_data_address+client.flags_offset+(0x1D0//8),
            [client.flags_cache[0x1D0//8] | 1],
            client.ram_read_write_domain
        ))

    await bizhawk.write(ctx.bizhawk_ctx, writes)
