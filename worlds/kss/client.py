import logging
import time
import typing
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient
from typing import TYPE_CHECKING
from .items import treasures, BASE_ID
from .client_data import treasure_base_id, boss_flags, deluxe_essence_flags, planet_flags

if TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
SRAM_1_START = 0xE00000

KSS_KIRBY_LIVES = SRAM_1_START + 0x137A
KSS_KIRBY_HP = SRAM_1_START + 0x137C
KSS_DEMO_STATE = SRAM_1_START + 0x138E
KSS_GAME_STATE = SRAM_1_START + 0x1390
KSS_GOURMET_RACE_WON = SRAM_1_START + 0x171D
KSS_DYNA_COMPLETED = SRAM_1_START + 0x1A63
KSS_DYNA_SWITCHES = SRAM_1_START + 0x1A64
KSS_DYNA_IRON_MAM = SRAM_1_START + 0x1A67
KSS_REVENGE_CHAPTERS = SRAM_1_START + 0x1A69
KSS_RAINBOW_STAR = SRAM_1_START + 0x1A6B
KSS_CURRENT_SUBGAMES = SRAM_1_START + 0x1A85
KSS_COMPLETED_SUBGAMES = SRAM_1_START + 0x1A93
KSS_ARENA_HIGH_SCORE = SRAM_1_START + 0x1AA1
KSS_BOSS_DEFEATED = SRAM_1_START + 0x1AE7  # 4 bytes
KSS_TGCO_TREASURE = SRAM_1_START + 0x1B05  # 8 bytes
KSS_TGC0_GOLD = SRAM_1_START + 0x1B0F  # 3-byte 24-bit int
KSS_COPY_ABILITIES = SRAM_1_START + 0x1B1D  # originally Milky Way Wishes deluxe essences
KSS_MWW_ITEMS = SRAM_1_START + 0x1B20
# Remapped for sending
KSS_SENT_DYNA_SWITCH = SRAM_1_START + 0x7A64
KSS_COMPLETED_PLANETS = SRAM_1_START + 0x7A6B
KSS_SENT_TGCO_TREASURE = SRAM_1_START + 0x7B05  # 8 bytes
KSS_SENT_DELUXE_ESSENCE = SRAM_1_START + 0x7B1D  # 3 bytes

# AP-received extras
KSS_RECEIVED_SUBGAMES = SRAM_1_START + 0x8000
KSS_RECEIVED_ITEMS = SRAM_1_START + 0x8002
KSS_RECEIVED_PLANETS = SRAM_1_START + 0x8004

KSS_ROMNAME = SRAM_1_START + 0x8100
KSS_DEATH_LINK_ADDR = SRAM_1_START + 0x9000


class KSSSNIClient(SNIClient):
    game = "Kirby Super Star"
    patch_suffix = ".apkss"
    item_queue: typing.List[NetworkItem] = []

    async def deathlink_kill_player(self, ctx: "SNIContext") -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_read, snes_flush_writes
        game_state = int.from_bytes(await snes_read(ctx, KSS_GAME_STATE, 1), "little")
        if game_state == 3:
            snes_buffered_write(ctx, KSS_KIRBY_HP, int.to_bytes(0, 2, "little"))
            await snes_flush_writes(ctx)
            ctx.death_state = DeathState.dead
            ctx.last_death_link = time.time()

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, KSS_ROMNAME, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15) or rom_name[:3] != b"KSS":
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b111  # full remote
        ctx.allow_collect = True

        death_link = await snes_read(ctx, KSS_DEATH_LINK_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
        return True

    async def pop_item(self, ctx: "SNIContext", game_state: int):
        from SNIClient import snes_read, snes_buffered_write
        if game_state != 3:
            return
        if self.item_queue:
            item = self.item_queue.pop()
            if item.item & 0xF == 1:
                # 1-Up
                lives = int.from_bytes(await snes_read(ctx, KSS_KIRBY_LIVES, 2), "little")
                snes_buffered_write(ctx, KSS_KIRBY_LIVES, int.to_bytes(lives + 1, 2, "little"))
            elif item.item & 0xF == 2:
                # Maxim
                snes_buffered_write(ctx, KSS_KIRBY_HP, int.to_bytes(0x46, 2, "little"))
                snes_buffered_write(ctx, KSS_KIRBY_HP + 2, int.to_bytes(0x46, 2, "little"))
            elif item.item & 0xF == 3:
                pass # Invincibility, not implemented
                # it needs to hit IRAM, so have to setup in the rom
            else:
                pass

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes, DeathState

        demo_state = int.from_bytes(await snes_read(ctx, KSS_DEMO_STATE, 2), "little")
        if not demo_state:
            return

        current_subgames = int.from_bytes(await snes_read(ctx, KSS_CURRENT_SUBGAMES, 2), "little")
        if current_subgames & 0x0080 != 0:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        game_state = int.from_bytes(await snes_read(ctx, KSS_GAME_STATE, 1), "little")

        if "DeathLink" in ctx.tags and game_state == 3 and ctx.last_death_link + 1 < time.time() \
                and ctx.death_state == DeathState.alive:
            kirby_hp = int.from_bytes(await snes_read(ctx, KSS_KIRBY_HP, 2), "little")
            if kirby_hp == 0:
                # TODO: see if I can get gamemode specific messages
                await ctx.handle_deathlink_state(True, f"Pop Star was too much for {ctx.player_names[ctx.slot]}.")

        save_abilities = 0
        i = 0
        for i, ability in enumerate([item for item in ctx.items_received if item.item & 0x100]):
            save_abilities |= (1 << ((ability.item & 0xFF) - 1))
        snes_buffered_write(ctx, KSS_COPY_ABILITIES, int.to_bytes(save_abilities, 3, "little"))
        snes_buffered_write(ctx, KSS_MWW_ITEMS, int.to_bytes(i+1, 1, "little"))

        known_treasures = int.from_bytes(await snes_read(ctx, KSS_TGCO_TREASURE, 8), "little")
        treasure_data = 0
        treasure_value = 0
        for treasure in [item for item in ctx.items_received if item.item & 0x200]:
            treasure_info = treasures[ctx.item_names[treasure.item]]
            treasure_value += treasure_info.value
            treasure_data |= (1 << ((treasure.item & 0xFF) - 1))
        if treasure_data != known_treasures:
            snes_buffered_write(ctx, KSS_TGCO_TREASURE, treasure_data.to_bytes(8, "little"))
            snes_buffered_write(ctx, KSS_TGC0_GOLD, treasure_value.to_bytes(3, "little"))

        unlocked_planets = int.from_bytes(await snes_read(ctx, KSS_RECEIVED_PLANETS, 2), "little")
        for planet_item in [item for item in ctx.items_received if item.item & 0x400]:
            planet = planet_item.item & 0xFF
            unlocked_planets |= (1 << planet)
        snes_buffered_write(ctx, KSS_RECEIVED_PLANETS, unlocked_planets.to_bytes(2, "little"))

        unlocked_switches = int.from_bytes(await snes_read(ctx, KSS_DYNA_SWITCHES, 1), "little")
        for switch_item in [item for item in ctx.items_received if item.item & 0x800]:
            switch = switch_item.item & 0xFF
            unlocked_switches |= (1 << switch)
        snes_buffered_write(ctx, KSS_DYNA_SWITCHES, unlocked_switches.to_bytes(1, "little"))

        planet_clear = int.from_bytes(await snes_read(ctx, KSS_RAINBOW_STAR, 1), "little")
        current_total = sum(1 for item in ctx.items_received if item.item & 0xFFFF == 0x1004)
        new_clear = 0
        for i in range(min(current_total + 1, 8)):
            new_clear |= (1 << i)
        if planet_clear != new_clear and new_clear:
            snes_buffered_write(ctx, KSS_RAINBOW_STAR, int.to_bytes(new_clear, 1, "little"))

        recv_count = int.from_bytes(await snes_read(ctx, KSS_RECEIVED_ITEMS, 2), "little")
        if recv_count < len(ctx.items_received):
            item = ctx.items_received[recv_count]
            recv_count += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_count, len(ctx.items_received)))
            snes_buffered_write(ctx, KSS_RECEIVED_ITEMS, recv_count.to_bytes(2, "little"))
            if item.item & 0xFF00 == 0:
                # Subgame
                unlocked_subgames = int.from_bytes(await snes_read(ctx, KSS_RECEIVED_SUBGAMES, 2), "little")
                unlocked_subgames |= (1 << (item.item & 0xFF))
                snes_buffered_write(ctx, KSS_RECEIVED_SUBGAMES, unlocked_subgames.to_bytes(2, "little"))
            elif item.item & 0x1000 != 0:
                if item.item & 0xF != 4:
                    self.item_queue.append(item)

        await self.pop_item(ctx, game_state)

        await snes_flush_writes(ctx)

        new_checks = []

        boss_flag = int.from_bytes(await snes_read(ctx, KSS_BOSS_DEFEATED, 4), "little")
        for flag, location in boss_flags.items():
            if boss_flag & flag and location not in ctx.checked_locations:
                new_checks.append(location)

        deluxe_flag = int.from_bytes(await snes_read(ctx, KSS_SENT_DELUXE_ESSENCE, 3), "little")
        for flag, location in deluxe_essence_flags.items():
            if deluxe_flag & flag and location not in ctx.checked_locations:
                new_checks.append(location)

        treasure_flag = int.from_bytes(await snes_read(ctx, KSS_SENT_TGCO_TREASURE, 8), "little")
        for flag in range(60):
            location = treasure_base_id + flag
            if (1 << flag) & treasure_flag and location not in ctx.checked_locations:
                new_checks.append(location)

        dyna_flag = int.from_bytes(await snes_read(ctx, KSS_SENT_DYNA_SWITCH, 1), "little")
        for flag, location in enumerate([BASE_ID + 9, BASE_ID + 10]):
            if (flag + 1) & dyna_flag and location not in ctx.checked_locations:
                new_checks.append(location)

        dyna_stage = int.from_bytes(await snes_read(ctx, KSS_DYNA_COMPLETED, 1), "little")
        for i in range(dyna_stage):
            location = BASE_ID + 4 + i
            if location not in ctx.checked_locations:
                new_checks.append(location)

        dyna_mam = int.from_bytes(await snes_read(ctx, KSS_DYNA_IRON_MAM, 1), "little")
        if dyna_mam and BASE_ID + 11 not in ctx.checked_locations:
            new_checks.append(BASE_ID + 11)

        revenge = int.from_bytes(await snes_read(ctx, KSS_REVENGE_CHAPTERS, 1), "little")
        for i in range(revenge & 0x7):
            location = BASE_ID + 79 + i
            if location not in ctx.checked_locations:
                new_checks.append(location)

        mww_planets = int.from_bytes(await snes_read(ctx, KSS_COMPLETED_PLANETS, 1), "little")
        for i in range(7):
            flag = 1 << i
            location = planet_flags[flag]
            if flag & mww_planets and location not in ctx.checked_locations:
                new_checks.append(location)

        gourmet_race = int.from_bytes(await snes_read(ctx, KSS_GOURMET_RACE_WON, 1), "little")
        for i in range(3):
            flag = 1 << i
            location = BASE_ID + 12 + i
            if flag & gourmet_race and location not in ctx.checked_locations:
                new_checks.append(location)

        arena = int.from_bytes(await snes_read(ctx, KSS_ARENA_HIGH_SCORE, 1), "little")
        for i in range(arena >> 1):
            location = BASE_ID + 113 + i
            if location not in ctx.checked_locations:
                new_checks.append(location)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
