from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


async def check_flag_locations(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> list[int]:

    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.flags_offset, client.flag_bytes_amount, client.ram_read_write_domain),
        )
    )
    flags_buffer = read[0]
    for eight_flags in range(client.flag_bytes_amount):
        if client.flags_cache[eight_flags] != flags_buffer[eight_flags]:
            merge = client.flags_cache[eight_flags] | flags_buffer[eight_flags]
            if client.flags_cache[eight_flags] != merge:
                if merge & 1 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8]:
                        locations_to_check.append(loc_id)
                if merge & 2 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+1]:
                        locations_to_check.append(loc_id)
                if merge & 4 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+2]:
                        locations_to_check.append(loc_id)
                if merge & 8 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+3]:
                        locations_to_check.append(loc_id)
                if merge & 16 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+4]:
                        locations_to_check.append(loc_id)
                if merge & 32 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+5]:
                        locations_to_check.append(loc_id)
                if merge & 64 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+6]:
                        locations_to_check.append(loc_id)
                if merge & 128 != 0:
                    for loc_id in client.missing_flag_loc_ids[eight_flags*8+7]:
                        locations_to_check.append(loc_id)
            client.flags_cache[eight_flags] = merge
    return locations_to_check


async def check_dex_locations(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> list[int]:

    if not client.dexsanity_included:
        return []

    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.dex_offset, client.dex_bytes_amount, client.ram_read_write_domain),
        )
    )
    dex_buffer = read[0]
    for eight_flags in range(client.dex_bytes_amount):
        if client.dex_cache[eight_flags] != dex_buffer[eight_flags]:
            merge = client.dex_cache[eight_flags] | dex_buffer[eight_flags]
            if client.dex_cache[eight_flags] != merge:
                if merge & 1:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 1]:
                        locations_to_check.append(loc_id)
                if merge & 2:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 2]:
                        locations_to_check.append(loc_id)
                if merge & 4:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 3]:
                        locations_to_check.append(loc_id)
                if merge & 8:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 4]:
                        locations_to_check.append(loc_id)
                if merge & 16:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 5]:
                        locations_to_check.append(loc_id)
                if merge & 32:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 6]:
                        locations_to_check.append(loc_id)
                if merge & 64:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 7]:
                        locations_to_check.append(loc_id)
                if merge & 128:
                    for loc_id in client.missing_dex_flag_loc_ids[eight_flags * 8 + 8]:
                        locations_to_check.append(loc_id)
            client.dex_cache[eight_flags] = merge
    return locations_to_check
