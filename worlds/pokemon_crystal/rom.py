import copy
import os
from typing import TYPE_CHECKING

import bsdiff4

from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .data import data, MiscOption, POKEDEX_COUNT_OFFSET, APWORLD_VERSION, POKEDEX_OFFSET, EncounterType, \
    FishingRodType, \
    TreeRarity
from .items import item_const_name_to_id
from .options import UndergroundsRequirePower, RequireItemfinder, Goal, Route2Access, \
    BlackthornDarkCaveAccess, NationalParkAccess, Route3Access, EncounterSlotDistribution, KantoAccessRequirement, \
    FreeFlyLocation, HMBadgeRequirements
from .utils import convert_to_ingame_text, write_bytes, replace_map_tiles

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

CRYSTAL_1_0_HASH = "9f2922b235a5eeb78d65594e82ef5dde"
CRYSTAL_1_1_HASH = "301899b8087289a6436b0a241fbbb474"


class PokemonCrystalAPPatchExtension(APPatchExtension):
    game = "Pokemon Crystal"

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str):
        revision_address = data.rom_addresses["AP_ROM_Revision"]
        rom_bytes = bytearray(rom)
        if rom_bytes[revision_address] == 1:
            if "basepatch11.bsdiff4" not in caller.files:
                raise Exception("This patch was generated without support for Pokemon Crystal V1.1 ROM. "
                                "Please regenerate with a newer APWorld version or use a V1.0 ROM")
            return bsdiff4.patch(rom, caller.get_file("basepatch11.bsdiff4"))
        return bsdiff4.patch(rom, caller.get_file(patch))


class PokemonCrystalProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon Crystal"
    hash = [CRYSTAL_1_0_HASH, CRYSTAL_1_1_HASH]
    patch_file_ending = ".apcrystal"
    result_file_ending = ".gbc"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(world: "PokemonCrystalWorld", output_directory: str, patch: PokemonCrystalProcedurePatch) -> None:
    option_bytes = bytearray(max([item.option_byte_index for item in data.game_settings.values()]) + 1)

    for setting_name, setting in data.game_settings.items():
        option_selection = world.options.game_options.get(setting_name, None)
        if setting_name == "text_frame" and option_selection == "random":
            option_selection = world.random.randint(1, 8)
        if setting_name == "time_of_day" and option_selection == "random":
            option_selection = world.random.choice(("morn", "day", "nite"))
        if setting_name == "_death_link":
            option_selection = "on" if world.options.death_link else "off"
        setting.set_option_byte(option_selection, option_bytes)

    write_bytes(patch, option_bytes, data.rom_addresses["AP_Setting_DefaultOptions"])

    item_texts = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.address > POKEDEX_COUNT_OFFSET:
            location_address = data.rom_addresses["AP_DexcountsanityItems"] + location.rom_address - 1
        elif location.address > POKEDEX_OFFSET:
            location_address = data.rom_addresses["AP_DexsanityItems"] + location.rom_address - 1
        else:
            location_address = location.rom_address

        if not world.options.remote_items and location.item and location.item.player == world.player:
            item_id = location.item.code
            write_bytes(patch, [item_id], location_address)
        else:
            # for in game text
            if location.address < POKEDEX_OFFSET:
                item_flag = location.address
                player_name = world.multiworld.player_name[location.item.player].upper()
                item_name = location.item.name.upper()
                item_texts.append([player_name, item_name, item_flag])

            write_bytes(patch, [item_const_name_to_id("AP_ITEM")], location_address)

    # table has format: location id (2 bytes), string address (2 bytes), string bank (1 byte),
    # and is terminated by 0xFF
    item_name_table_length = len(item_texts) * 5 + 1
    item_name_table_adr = data.rom_addresses["AP_ItemText_Table"]

    # strings are 16 chars each, plus a terminator byte,
    # this gives every pair of item + player names a size of 34 bytes
    item_name_bank1 = item_name_table_adr + item_name_table_length
    item_name_bank1_length = data.rom_addresses["AP_ItemText_Bank1_End"] - item_name_bank1
    item_name_bank1_capacity = int(item_name_bank1_length / 34)

    item_name_bank2 = data.rom_addresses["AP_ItemText_Bank2"]
    item_name_bank2_length = data.rom_addresses["AP_ItemText_Bank2_End"] - item_name_bank2
    item_name_bank2_capacity = int(item_name_bank2_length / 34)

    for i, text in enumerate(item_texts):
        # truncate if too long
        player_text = convert_to_ingame_text(text[0])[:16]
        # pad with terminator byte to keep alignment
        player_text.extend([0x50] * (17 - len(player_text)))
        item_text = convert_to_ingame_text(text[1])[:16]
        item_text.append(0x50)
        # bank 1
        bank = 0x75
        table_offset_adr = item_name_table_adr + i * 5

        if i >= item_name_bank1_capacity + item_name_bank2_capacity:
            # if we somehow run out of capacity in both banks, just finish the table and break,
            # there is a fallback string in the ROM, so it should handle this gracefully.
            write_bytes(patch, [0xFF], item_name_table_adr + table_offset_adr)
            print("oopsie")
            break
        if i + 1 < item_name_bank1_capacity:
            text_offset = i * 34
            text_adr = item_name_bank1 + text_offset
        else:
            # bank 2
            bank = 0x76
            text_offset = (i + 1 - item_name_bank1_capacity) * 34
            text_adr = item_name_bank2 + text_offset
        write_bytes(patch, player_text + item_text, text_adr)
        # get the address within the rom bank (0x4000 - 0x7FFF)
        text_bank_adr = (text_adr % 0x4000) + 0x4000
        write_bytes(patch, text[2].to_bytes(2, "big"), table_offset_adr)
        write_bytes(patch, text_bank_adr.to_bytes(2, "little"), table_offset_adr + 2)
        write_bytes(patch, [bank], table_offset_adr + 4)
    write_bytes(patch, [0xFF], item_name_table_adr + item_name_table_length - 1)

    world.finished_level_scaling.wait()

    for _, pkmn_data in world.generated_static.items():
        pokemon_id = data.pokemon[pkmn_data.pokemon].id
        for address in pkmn_data.addresses:
            cur_address = data.rom_addresses[address] + 1
            write_bytes(patch, [pokemon_id], cur_address)
        if pkmn_data.level_address is not None:
            if pkmn_data.level_type in ("givepoke", "loadwildmon"):
                write_bytes(patch, [pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 2)
            elif pkmn_data.level_type == "custom":
                write_bytes(patch, [pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 1)

    if world.options.randomize_trades:
        trade_table_address = data.rom_addresses["AP_Setting_TradeTable"]
        for trade in world.generated_trades:
            trade_address = trade_table_address + (trade.index * 32)  # each trade record is 32 bytes
            requested = data.pokemon[trade.requested_pokemon].id
            write_bytes(patch, [requested], trade_address + 1)

            received = data.pokemon[trade.received_pokemon].id
            write_bytes(patch, [received], trade_address + 2)

            write_bytes(patch, [trade.requested_gender], trade_address + 30)

            item_id = item_const_name_to_id(trade.held_item)
            write_bytes(patch, [item_id], trade_address + 16)

    if world.options.randomize_starters:
        for j, pokemon in enumerate(["CYNDAQUIL_", "TOTODILE_", "CHIKORITA_"]):
            pokemon_id = data.pokemon[world.generated_starters[j][0]].id
            starter_name = world.generated_pokemon[world.generated_starters[j][0]].friendly_name.upper()
            starter_name = "NIDORAN ♀" if starter_name == "NIDORAN F" else starter_name
            starter_name = "NIDORAN ♂" if starter_name == "NIDORAN M" else starter_name
            starter_text = convert_to_ingame_text(starter_name)
            for i in range(1, 9):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)] + 1
                write_bytes(patch, [pokemon_id], cur_address)
                if i == 4:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes(patch, [helditem], cur_address + 2)
                if i == 8:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes(patch, [helditem], cur_address + 10)
            for i in range(9, 10):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)]
                write_bytes(patch, starter_text + [0x7f] * (10 - len(starter_text)), cur_address)

    tree_encounter_rates = []
    rock_encounter_rates = []
    if world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_balanced:
        tree_encounter_rates = [20, 20, 20, 15, 15, 10]
        rock_encounter_rates = [70, 30]
    elif world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_equal:
        tree_encounter_rates = [16, 16, 17, 17, 17, 17]
        rock_encounter_rates = [50, 50]

    for region_key, encounters in world.generated_wild.items():
        if region_key.encounter_type is EncounterType.Grass:
            cur_address = data.rom_addresses[f"AP_WildGrass_{region_key.region_id}"] + 3

            for _ in range(3):  # morn, day, nite
                for encounter in encounters:
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes(patch, [encounter.level, pokemon_id], cur_address)
                    cur_address += 2

        elif region_key.encounter_type is EncounterType.Water:
            cur_address = data.rom_addresses[f"AP_WildWater_{region_key.region_id}"] + 1
            for encounter in encounters:
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes(patch, [encounter.level, pokemon_id], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.Fish:
            cur_address = data.rom_addresses[f"AP_FishMons_{region_key.region_id}"]
            if region_key.fishing_rod is FishingRodType.Good:
                cur_address += 9  # skip the first 3 encounters, each encounter is 3 bytes
            elif region_key.fishing_rod is FishingRodType.Super:
                cur_address += 21  # skip the first 7 encounters

            for i, encounter in enumerate(encounters):
                if world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_equal:
                    # fishing encounter rates are stored as an increasing fraction of 255
                    encounter_rate = int(((i + 1) / len(encounters)) * 255)
                    write_bytes(patch, [encounter_rate], cur_address)
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes(patch, [pokemon_id, encounter.level], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.Tree:
            cur_address = data.rom_addresses[f"TreeMonSet_{region_key.region_id}"]
            if region_key.rarity is TreeRarity.Rare:
                cur_address += 19  # skip the first 6 encounters + terminator byte, each encounter is 3 bytes
            for i, encounter in enumerate(encounters):
                if tree_encounter_rates:
                    write_bytes(patch, [tree_encounter_rates[i]], cur_address)
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes(patch, [pokemon_id, encounter.level], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.RockSmash:
            cur_address = data.rom_addresses["TreeMonSet_Rock"]
            for i, encounter in enumerate(encounters):
                if rock_encounter_rates:
                    write_bytes(patch, [rock_encounter_rates[i]], cur_address)
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes(patch, [pokemon_id, encounter.level], cur_address)
                cur_address += 2

    wooper_sprite_address = data.rom_addresses["AP_Setting_Intro_Wooper_1"] + 1
    wooper_cry_address = data.rom_addresses["AP_Setting_Intro_Wooper_2"] + 1
    wooper_id = data.pokemon[world.generated_wooper].id
    write_bytes(patch, [wooper_id], wooper_sprite_address)
    write_bytes(patch, [wooper_id], wooper_cry_address)

    grass_probs = []
    water_probs = []

    if world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_remove_one_percents:
        grass_probs = [30, 55, 75, 85, 90, 95, 100]
    elif world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_equal:
        grass_probs = [14, 28, 42, 57, 71, 85, 100]
        water_probs = [33, 66, 100]
    elif world.options.encounter_slot_distribution.value == EncounterSlotDistribution.option_balanced:
        grass_probs = [20, 40, 55, 70, 80, 90, 100]

    if grass_probs:
        grass_prob_table = [f(x) for x in enumerate(grass_probs) for f in (lambda x: x[1], lambda x: x[0] * 2)]
        write_bytes(patch, grass_prob_table, data.rom_addresses["AP_Prob_GrassMon"])

    if water_probs:
        water_prob_table = [f(x) for x in enumerate(water_probs) for f in (lambda x: x[1], lambda x: x[0] * 2)]
        write_bytes(patch, water_prob_table, data.rom_addresses["AP_Prob_WaterMon"])

    if world.options.randomize_berry_trees:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_BerryTrees"] + 1)
        # 0xC9 = ret
        write_bytes(patch, [0xC9], data.rom_addresses["AP_Setting_FruitTreesReset"])

    if world.options.randomize_move_values or world.options.randomize_move_types:
        for move_name, move in world.generated_moves.items():  # effect modification is also possible but not included
            if move_name in ("NO_MOVE", "CURSE"):
                continue
            if world.options.randomize_move_types:
                address = data.rom_addresses["AP_MoveData_Type_" + move_name]
                move_type_id = [data.type_ids[move.type]]
                write_bytes(patch, move_type_id, address)  # uses same type id conversion that pkmn type randomizer
            if world.options.randomize_move_values > 0:
                address = data.rom_addresses["AP_MoveData_Power_" + move_name]
                write_bytes(patch, [move.power], address)  # power 20-150
                address = data.rom_addresses["AP_MoveData_PP_" + move_name]
                write_bytes(patch, [move.pp], address)  # 5-40 PP
                if world.options.randomize_move_values == 3:
                    address = data.rom_addresses["AP_MoveData_Accuracy_" + move_name]
                    acc = int(move.accuracy * 255 / 100)
                    write_bytes(patch, [acc], address)  # accuracy 30-100

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        if world.options.randomize_types.value:
            address = data.rom_addresses["AP_Stats_Types_" + pkmn_name]
            pkmn_types = [pkmn_data.types[0], pkmn_data.types[-1]]
            type_ids = [data.type_ids[pkmn_types[0]], data.type_ids[pkmn_types[1]]]
            write_bytes(patch, type_ids, address)

        if world.options.randomize_base_stats.value:
            address = data.rom_addresses["AP_Stats_Base_" + pkmn_name]
            write_bytes(patch, pkmn_data.base_stats, address)

        if world.options.randomize_learnsets.value:
            address = data.rom_addresses["AP_Attacks_" + pkmn_name]
            for move in pkmn_data.learnset:
                move_id = data.moves[move.move].rom_id
                write_bytes(patch, [move.level, move_id], address)
                address += 2

        if pkmn_name in world.generated_palettes:
            palettes = world.generated_palettes[pkmn_name]
            address = data.rom_addresses["AP_Stats_Palette_" + pkmn_name]
            write_bytes(patch, palettes, address)

        tm_bytes = [0, 0, 0, 0, 0, 0, 0, 0]
        for tm in pkmn_data.tm_hm:
            tm_num = data.tmhm[tm].tm_num
            tm_bytes[int((tm_num - 1) / 8)] |= 1 << (tm_num - 1) % 8
        tm_address = data.rom_addresses["AP_Stats_TMHM_" + pkmn_name]
        write_bytes(patch, tm_bytes, tm_address)

    for trainer_name, trainer_data in world.generated_trainers.items():
        address = data.rom_addresses["AP_TrainerParty_" + trainer_name]
        address += trainer_data.name_length + 1  # skip name and type
        for pokemon in trainer_data.pokemon:
            pokemon_data = [pokemon.level, data.pokemon[pokemon.pokemon].id]
            if pokemon.item is not None:
                item_id = item_const_name_to_id(pokemon.item)
                pokemon_data.append(item_id)
            for move in pokemon.moves:
                move_id = data.moves[move].rom_id
                pokemon_data.append(move_id)
            write_bytes(patch, pokemon_data, address)
            address += len(pokemon_data)

    if world.options.randomize_tm_moves.value or world.options.metronome_only.value:
        tm_moves = [tm_data.move_id for _name, tm_data in world.generated_tms.items()]
        address = data.rom_addresses["AP_Setting_TMMoves"]
        write_bytes(patch, tm_moves, address)

    if world.options.enable_mischief:
        if MiscOption.FuchsiaGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_FuchsiaTrainers"] + 1
            write_bytes(patch, [0x0a], address + 2)  # spin speed
            for c in world.generated_misc.fuchsia_gym_trainers:
                write_coords = [c[1] + 4, c[0] + 4]
                write_bytes(patch, write_coords, address)
                address += 13

        if MiscOption.SaffronGym.value in world.generated_misc.selected:
            for pair in world.generated_misc.saffron_gym_warps.pairs:
                addresses = [data.rom_addresses["AP_Misc_SaffronGymWarp_" + warp] + 2 for warp in pair]
                ids = [world.generated_misc.saffron_gym_warps.warps[warp].id for warp in pair]
                write_bytes(patch, [ids[1]], addresses[0])  # reverse ids
                write_bytes(patch, [ids[0]], addresses[1])

        if MiscOption.EcruteakGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Ecruteak_Gym_Warp"]
            write_bytes(patch, [2, 5], address)

        if MiscOption.OhkoMoves.value in world.generated_misc.selected:
            for move in ("GUILLOTINE", "HORN_DRILL", "FISSURE"):
                address = data.rom_addresses["AP_MoveData_Effect_" + move]
                write_bytes(patch, [0x65], address)  # false swipe effect
                address = data.rom_addresses["AP_MoveData_Power_" + move]
                write_bytes(patch, [0xFF], address)  # power 255
                address = data.rom_addresses["AP_MoveData_Accuracy_" + move]
                write_bytes(patch, [0xFF], address)  # accuracy 100%
                address = data.rom_addresses["AP_MoveData_PP_" + move]
                write_bytes(patch, [0x14], address)  # 20 PP

        if MiscOption.RadioTowerQuestions.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_N"] + 1
            # bad pokedex rating jingle
            write_bytes(patch, [0x9F], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y2"] + 1
            # increasing pokedex rating jingles
            write_bytes(patch, [0xA0], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y3"] + 1
            write_bytes(patch, [0xA1], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y4"] + 1
            write_bytes(patch, [0xA2], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y5"] + 1
            write_bytes(patch, [0xA3], address)
            for i in range(0, 5):
                answer = world.generated_misc.radio_tower_questions[i]
                # # 0x08 is iffalse (.WrongAnswer), 0x09 is iftrue (.WrongAnswer)
                byte = 0x08 if answer == "Y" else 0x09
                address = data.rom_addresses["AP_Misc_RadioTower_Q" + str(i + 1)]
                write_bytes(patch, [byte], address)

        if MiscOption.FanClubChairman.value in world.generated_misc.selected:
            # gives the chairman a 15/16 chance of repeating the rapidash rant each time
            address = data.rom_addresses["AP_Misc_Rapidash_Loop"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.Amphy.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Amphy"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.SecretSwitch.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_SecretSwitch"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.RedGyarados.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RedGyarados"] + 1
            write_bytes(patch, [1], address)

        if MiscOption.RadioChannels.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioChannels"]
            for channel_addr in world.generated_misc.radio_channel_addresses:
                write_bytes(patch, channel_addr.to_bytes(2, "little"), address + 1)
                address += 3

        if MiscOption.MomItems.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_MomItems"]
            for mom_item in world.generated_misc.mom_items:
                write_bytes(patch, [item_const_name_to_id(mom_item.item)], address + (8 * mom_item.index) + 7)

        if MiscOption.IcePath.value in world.generated_misc.selected:
            write_bytes(patch, [13, 3], data.rom_addresses["AP_Misc_IcePathWarp_1"])
            write_bytes(patch, [13, 13], data.rom_addresses["AP_Misc_IcePathWarp_2"])

    if world.options.reusable_tms:
        address = data.rom_addresses["AP_Setting_ReusableTMs"] + 1
        write_bytes(patch, [1], address)

    if world.options.minimum_catch_rate > 0:
        address = data.rom_addresses["AP_Setting_MinCatchrate"] + 1
        write_bytes(patch, [world.options.minimum_catch_rate], address)

    if world.options.randomize_music:
        for map_name, map_music in world.generated_music.maps.items():
            music_address = data.rom_addresses["AP_Music_" + map_name]
            # map music uses a single byte
            write_bytes(patch, [world.generated_music.consts[map_music].id], music_address)
        for i, music_name in enumerate(world.generated_music.encounters):
            music_address = data.rom_addresses["AP_EncounterMusic"] + i
            write_bytes(patch, [world.generated_music.consts[music_name].id], music_address)
        for script_name, script_music in world.generated_music.scripts.items():
            music_address = data.rom_addresses["AP_Music_" + script_name] + 1
            # script music is 2 bytes LE
            write_bytes(patch, world.generated_music.consts[script_music].id.to_bytes(2, "little"), music_address)

    if world.options.better_marts:
        mart_address = data.rom_addresses["Marts"]
        marts_end_address = data.rom_addresses["MartsEnd"]
        better_mart_address = data.rom_addresses["MartBetterMart"] - 0x10000
        better_mart_bytes = better_mart_address.to_bytes(2, "little")
        for i in range((marts_end_address - mart_address) // 2):
            # skip goldenrod and celadon
            if i not in (6, 7, 8, 9, 21, 22, 23, 24, 25, 31):
                write_bytes(patch, better_mart_bytes, mart_address)
            mart_address += 2

    for hm in world.options.remove_badge_requirement.valid_keys:
        hm_address = data.rom_addresses[f"AP_Setting_HMBadges_{hm}"] + 1
        requirement = world.options.hm_badge_requirements.value
        if hm in world.options.remove_badge_requirement:
            requirement = HMBadgeRequirements.option_no_badges
        if requirement == HMBadgeRequirements.option_regional and hm == "Fly":
            requirement = HMBadgeRequirements.option_add_kanto
        write_bytes(patch, [requirement], hm_address)

    if world.options.hm_badge_requirements.value == HMBadgeRequirements.option_regional:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_RegionalHMBadges_1"] + 1)
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_RegionalHMBadges_2"] + 1)

    exp_modifier_address = data.rom_addresses["AP_Setting_ExpModifier"] + 1
    write_bytes(patch, [world.options.experience_modifier], exp_modifier_address)

    elite_four_text = convert_to_ingame_text("{:02d}".format(world.options.elite_four_count.value))
    write_bytes(patch, [world.options.elite_four_requirement.value],
                data.rom_addresses["AP_Setting_VictoryRoadRequirement"] + 1)
    write_bytes(patch, elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadBadges_Text"] + 1)
    write_bytes(patch, elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadGyms_Text"] + 1)
    write_bytes(patch, [world.options.elite_four_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_1"] + 1)
    write_bytes(patch, [world.options.elite_four_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_2"] + 1)

    write_bytes(patch, [world.options.radio_tower_requirement.value],
                data.rom_addresses["AP_Setting_RocketsRequirement"] + 1)
    write_bytes(patch, [world.options.radio_tower_count.value], data.rom_addresses["AP_Setting_RocketsCount"] + 1)

    write_bytes(patch, [world.options.route_44_access_requirement.value],
                data.rom_addresses["AP_Setting_Route44Requirement_1"] + 1)
    write_bytes(patch, [world.options.route_44_access_requirement.value],
                data.rom_addresses["AP_Setting_Route44Requirement_2"] + 1)
    for i in range(4):
        write_bytes(patch, [world.options.route_44_access_count.value],
                    data.rom_addresses[f"AP_Setting_Route44Count_{i + 1}"] + 1)

    mt_silver_text = convert_to_ingame_text("{:02d}".format(world.options.mt_silver_count.value))
    write_bytes(patch, [world.options.mt_silver_requirement.value],
                data.rom_addresses["AP_Setting_MtSilverRequirement_Gate"] + 1)
    write_bytes(patch, [world.options.mt_silver_requirement.value],
                data.rom_addresses["AP_Setting_MtSilverRequirement_Oak"] + 1)
    write_bytes(patch, mt_silver_text, data.rom_addresses["AP_Setting_MtSilverBadges_Gate_Text"] + 1)
    write_bytes(patch, mt_silver_text, data.rom_addresses["AP_Setting_MtSilverGyms_Gate_Text"] + 1)
    write_bytes(patch, mt_silver_text, data.rom_addresses["AP_Setting_MtSilverBadges_Oak_Text"] + 1)
    write_bytes(patch, mt_silver_text, data.rom_addresses["AP_Setting_MtSilverGyms_Oak_Text"] + 1)
    write_bytes(patch, [world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_1"] + 1)
    write_bytes(patch, [world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_2"] + 1)
    write_bytes(patch, [world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_1"] + 1)
    write_bytes(patch, [world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_2"] + 1)

    write_bytes(patch, [world.options.red_requirement.value], data.rom_addresses["AP_Setting_RedRequirement"] + 1)
    write_bytes(patch, [world.options.red_count], data.rom_addresses["AP_Setting_RedCount_1"] + 1)
    write_bytes(patch, [world.options.red_count], data.rom_addresses["AP_Setting_RedCount_2"] + 1)

    if not world.options.johto_only:
        kanto_access_become_champion = [1] if (world.options.kanto_access_requirement.value
                                               == KantoAccessRequirement.option_become_champion) else [0]
        write_bytes(patch, kanto_access_become_champion, data.rom_addresses["AP_Setting_KantoAccess_Champion"] + 1)

        kanto_access_wake_snorlax = [1] if (world.options.kanto_access_requirement.value
                                            == KantoAccessRequirement.option_wake_snorlax) else [0]
        write_bytes(patch, kanto_access_wake_snorlax, data.rom_addresses["AP_Setting_KantoAccess_Snorlax"] + 1)

        kanto_badges_text = convert_to_ingame_text("{:02d}".format(world.options.kanto_access_count.value))
        write_bytes(patch, [world.options.kanto_access_requirement.value],
                    data.rom_addresses["AP_SettingKantoAccess_Requirement"] + 1)
        write_bytes(patch, kanto_badges_text, data.rom_addresses["AP_Setting_KantoAccess_Badges_Text"] + 1)
        write_bytes(patch, kanto_badges_text, data.rom_addresses["AP_Setting_KantoAccess_Gyms_Text"] + 1)
        write_bytes(patch, [world.options.kanto_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_1"] + 1)
        write_bytes(patch, [world.options.kanto_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_2"] + 1)

    if world.options.trainersanity:
        # prevents disabling gym trainers, among a few others
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_Trainersanity"] + 2)
        # removes events from certain trainers, to prevent disabling them.
        missable_trainers = ["GruntM29", "GruntM2", "GruntF1", "GruntM16", "ScientistJed", "GruntM17", "GruntM18",
                             "GruntM19", "RocketMurkrow", "SlowpokeGrunt", "RaticateGrunt", "ScientistRoss",
                             "ScientistMitch", "RocketBaseB3FRocket"]

        for trainer in missable_trainers:
            # the dw at +11 is the event flag.
            write_bytes(patch, [0xFF, 0xFF], data.rom_addresses[f"AP_Setting_Trainersanity_{trainer}"] + 11)

    trainersanity_alerts_address = data.rom_addresses["AP_Setting_TrainersanityMessages"] + 1
    write_bytes(patch, [world.options.trainersanity_alerts], trainersanity_alerts_address)

    for i, script in enumerate(world.generated_phone_traps):
        address = data.rom_addresses["AP_Setting_PhoneCallTrapTexts"] + (i * 0x400)
        s_bytes = script.get_script_bytes()
        # write script text
        write_bytes(patch, s_bytes, address)
        # write script caller id
        address = data.rom_addresses["AP_Setting_SpecialCalls"] + (6 * i) + 2
        write_bytes(patch, [script.caller_id], address)

    phone_location_bytes = []
    for loc in world.generated_phone_indices:
        phone_location_bytes += list(loc.to_bytes(2, "little"))
    phone_location_address = data.rom_addresses["AP_Setting_Phone_Trap_Locations"]
    write_bytes(patch, phone_location_bytes, phone_location_address)

    start_inventory_address = data.rom_addresses["AP_Start_Inventory"]
    start_inventory = copy.copy(world.options.start_inventory.value)
    for item, quantity in world.options.start_inventory_from_pool.value.items():
        if item in start_inventory:
            start_inventory[item] += quantity
        else:
            start_inventory[item] = quantity
    for item, quantity in start_inventory.items():
        if quantity == 0:
            quantity = 1
        while quantity:
            item_code = world.item_name_to_id[item]
            if item_code > 255:
                continue
            if quantity > 99:
                write_bytes(patch, [item_code, 99], start_inventory_address)
                quantity -= 99
            else:
                write_bytes(patch, [item_code, quantity], start_inventory_address)
                quantity = 0
            start_inventory_address += 2

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        free_fly_write = [0, 0, 0, 0]
        free_fly_write[int(world.free_fly_location.id / 8)] = 1 << (world.free_fly_location.id % 8)
        write_bytes(patch, free_fly_write, data.rom_addresses["AP_Setting_FreeFly"])

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_fly_offset = int(world.map_card_fly_location.id / 8).to_bytes(2, "little")
        map_fly_byte = 1 << (world.map_card_fly_location.id % 8)
        write_bytes(patch, [map_fly_byte], data.rom_addresses["AP_Setting_MapCardFreeFly_Byte"] + 1)
        write_bytes(patch, map_fly_offset, data.rom_addresses["AP_Setting_MapCardFreeFly_Offset"] + 1)

    if world.options.remove_ilex_cut_tree:
        # Set cut tree tile to floor
        replace_map_tiles(patch, "IlexForest", 0, 11, [0x1])

    if world.options.skip_elite_four:
        # Lance's room is ID 7
        write_bytes(patch, [0x7], data.rom_addresses["AP_Setting_IndigoPlateauPokecenter1F_E4Warp"] + 4)

    route_32_flag = world.options.route_32_condition.value
    write_bytes(patch, [route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_1"] + 1)
    write_bytes(patch, [route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_2"] + 1)
    write_bytes(patch, [route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_3"] + 1)

    if "North" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute5Blocked"] + 2)
    if "East" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute8Blocked"] + 2)
    if "South" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute6Blocked"] + 2)
    if "West" in world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SaffronRoute7Blocked"] + 2)

    if world.options.saffron_gatehouse_tea.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_TeaEnabled"] + 1)

    if world.options.east_west_underground.value:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_EastWestUndergroundEnabled"] + 1)

    if world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_neither,
                                                          UndergroundsRequirePower.option_east_west):
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_NorthSouthUndergroundOpen"] + 2)

    if (world.options.east_west_underground.value and
            world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_neither,
                                                               UndergroundsRequirePower.option_north_south)):
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_EastWestUndergroundOpen"] + 2)

    if world.options.remote_items:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_RemoteItems"])

    if world.options.require_itemfinder.value == RequireItemfinder.option_hard_required:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_ItemfinderRequired"] + 1)

    if world.options.goal.value != Goal.option_elite_four:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_SkipE4Credits"] + 1)

    if world.options.vanilla_clair:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_VanillaClair"] + 2)

    if world.options.route_2_access.value == Route2Access.option_open:
        tiles = [0x01]  # ground
    elif world.options.route_2_access.value == Route2Access.option_ledge:
        tiles = [0x58, 0x0A]  # grass with left ledge, grass
    else:
        tiles = None

    if tiles:
        replace_map_tiles(patch, "Route2", 5, 1, tiles)

    if world.options.red_gyarados_access:
        whirlpool_tile = 0x07
        rock_tile = 0x0A
        water_tile = 0x35
        map_name = "LakeOfRage"
        replace_map_tiles(patch, map_name, 8, 10, [rock_tile, whirlpool_tile, 0x39])
        replace_map_tiles(patch, map_name, 7, 11, [0x30, water_tile, water_tile, rock_tile])
        replace_map_tiles(patch, map_name, 7, 12, [0x31, whirlpool_tile, 0x3A, 0x31])

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        map_name = "DarkCaveVioletEntrance"
        replace_map_tiles(patch, map_name, 6, 0, [0x11, 0x10])
        replace_map_tiles(patch, map_name, 6, 1, [0x08, 0x0A])
        replace_map_tiles(patch, map_name, 6, 2, [0x0C, 0x0E, 0x27, 0x0C, 0x0D, 0x0E])
        replace_map_tiles(patch, map_name, 6, 3, [0x2D, 0x2F, 0x2C, 0x2D, 0x2E, 0x2F])
        replace_map_tiles(patch, map_name, 9, 4, [0x04, 0x06])

        map_name = "DarkCaveBlackthornEntrance"
        replace_map_tiles(patch, map_name, 2, 7, [0x02])
        replace_map_tiles(patch, map_name, 2, 8, [0x02])

    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_NationalParkBicycle"] + 2)

    if world.options.route_3_access.value == Route3Access.option_boulder_badge:
        # This is a sprite event, so 0 shows the sprite
        write_bytes(patch, [0], data.rom_addresses["AP_Setting_PewterCityBadgeRequired_1"] + 2)
        # Don't set the scene to the noop scene
        write_bytes(patch, [0], data.rom_addresses["AP_Setting_PewterCityBadgeRequired_2"] + 2)

    headbutt_seed = (world.multiworld.seed & 0xFFFF).to_bytes(2, "little")
    write_bytes(patch, headbutt_seed[:0], data.rom_addresses["AP_Setting_TreeMonSeed_1"] + 1)
    write_bytes(patch, headbutt_seed[-1:], data.rom_addresses["AP_Setting_TreeMonSeed_2"] + 1)

    if world.options.randomize_starting_town:
        town_id = world.starting_town.id
        write_bytes(patch, [town_id], data.rom_addresses["AP_Setting_RandomStartTown_1"] + 1)
        write_bytes(patch, [town_id], data.rom_addresses["AP_Setting_RandomStartTown_2"] + 1)
        write_bytes(patch, [town_id], data.rom_addresses["AP_Setting_RandomStartTown_3"] + 1)
        write_bytes(patch, [town_id], data.rom_addresses["AP_Setting_RandomStartTown_4"] + 1)

    if world.options.randomize_starting_town or world.options.dexsanity or world.options.dexcountsanity:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_StartWithPokedex_1"] + 2)
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_StartWithPokedex_2"] + 2)

    if world.options.all_pokemon_seen:
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_AllPokemonSeen_1"] + 1)
        write_bytes(patch, [1], data.rom_addresses["AP_Setting_AllPokemonSeen_2"] + 1)

    start_money = world.options.starting_money.value.to_bytes(3, "big")
    for i, byte in enumerate(start_money):
        write_bytes(patch, [byte], data.rom_addresses[f"AP_Setting_StartMoney_{i + 1}"] + 1)

    if world.options.metronome_only:
        for i in range(4):
            write_bytes(patch, [1], data.rom_addresses[f"AP_Setting_MetronomeOnly_{i + 1}"] + 1)

    # Set slot auth
    ap_version_text = convert_to_ingame_text(APWORLD_VERSION)[:19]
    ap_version_text.append(0x50)
    # truncated to 19 to preserve the "v" at the beginning
    write_bytes(patch, world.auth, data.rom_addresses["AP_Seed_Auth"])
    write_bytes(patch, APWORLD_VERSION.encode("ascii")[:32], data.rom_addresses["AP_Version"])
    write_bytes(patch, ap_version_text, data.rom_addresses["AP_Version_Text"] + 1)

    patch.write_file("token_data.bin", patch.get_token_binary())

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_crystal_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes
