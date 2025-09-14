import logging
import os
import threading
from typing import Any, ClassVar, Dict, List, Optional, Sequence, Set, Tuple

from . import names
from .items import DWItem, item_table, filler_table, lookup_name_to_id, item_names
from .locations import create_locations, all_locations, location_names
from .regions import create_regions, connect_regions
import settings
from BaseClasses import Item, ItemClassification, Location, MultiWorld, Tutorial
from Utils import visualize_regions
from worlds.AutoWorld import World, WebWorld
from .rom import DRAGON_WARRIOR_PRG0_HASH, DRAGON_WARRIOR_PRG1_HASH, DWPatch
from .options import DWOptions, DWOptionGroups
from .client import DragonWarriorClient

class DWSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Dragon Warrior ROM"""
        description = "Dragon Warrior ROM File"
        copy_to: Optional[str] = "Dragon Warrior (USA) (Rev A).nes"
        md5s = [DRAGON_WARRIOR_PRG0_HASH, DRAGON_WARRIOR_PRG1_HASH]
    
    rom_file: RomFile = RomFile(RomFile.copy_to)

class DWWebWorld(WebWorld):
    theme = "grassFlowers"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Dragon Warrior randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serp"]
        )
    ]

    option_groups = DWOptionGroups


class DragonWarriorWorld(World):
    """
    The peace of fair Alefgard has been shattered by the appearance of the nefarious master of the night known as
    the Dragonlord, and the Sphere of Light, which for so long kept the forces of darkness in check, has been stolen!
    It is time for you, a young warrior through whose veins flows the blood of the legendary hero Erdrick, to set out
    on a quest to vanquish the Dragonlord, and save the land from darkness!
    """
    game = "Dragon Warrior"
    settings_key = "dw_options"
    settings: ClassVar[DWSettings]
    options_dataclass = DWOptions
    options: DWOptions
    item_name_to_id = lookup_name_to_id
    item_name_groups = item_names
    location_name_to_id = all_locations
    location_name_groups = location_names
    web = DWWebWorld()
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        levels = 0
        if self.options.levelsanity:
            levels = self.options.levelsanity_range
        tup = create_locations(levels)
        level_locations, high_level_locations = tup[0], tup[1]
        create_regions(self, level_locations, high_level_locations)
        connect_regions(self)

        self.multiworld.get_location(names.rainbow_drop_location, self.player).place_locked_item(self.create_item(names.rainbow_drop))
        self.multiworld.get_location(names.ball_of_light_location, self.player).place_locked_item(self.create_item(names.ball_of_light))

        itempool = []

        # Get the accurate location count between sanity options
        total_locations = 33 + len(level_locations) + len(high_level_locations) + \
            (self.options.searchsanity * 3) + (self.options.shopsanity * 15)

        # The following items always get placed
        itempool += [self.create_item(names.silver_harp),
                     self.create_item(names.staff_of_rain),     
                     self.create_item(names.stones_of_sunlight),
                     self.create_item(names.magic_key),
                     self.create_item(names.death_necklace),
                     self.create_item(names.cursed_belt),
                     self.create_item(names.fighters_ring),
                     self.create_item(names.gwaelins_love),
                     self.create_item(names.high_gold),
                     self.create_item(names.high_gold),
                     self.create_item(names.high_gold)]
        
        
        # The following items are conditional
        if self.options.searchsanity:
            itempool += [
                    self.create_item(names.erdricks_token),
                    self.create_item(names.fairy_flute)
                    ]
            if not self.options.shopsanity:
                itempool.append(self.create_item(names.erdricks_armor))
        
        if self.options.shopsanity:
            itempool += [
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_shield),
                self.create_item(names.progressive_shield),
                self.create_item(names.progressive_shield),
            ]
        else:
            itempool.append(self.create_item(names.erdricks_sword))

        while len(itempool) < total_locations:
            itempool += [self.create_item(self.get_filler_item_name())]

        self.multiworld.itempool += itempool

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has(names.ball_of_light, self.player)
        
        # visualize_regions(self.get_region("Menu"), "dw_regions.puml", show_locations=True)


    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = DWItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(filler_table.keys()))

    def generate_output(self, output_directory: str) -> None:
        try:
            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.nes")

            patch = DWPatch(os.path.splitext(rompath)[0] + ".apdw",
                            self.player, 
                            self.multiworld.player_name[self.player],
                            flags=self.determine_flags(),
                            searchsanity=self.options.searchsanity,
                            shopsanity=self.options.shopsanity)
            patch.write()

        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()

    def determine_flags(self) -> str:
        default_flags = "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAQAAAAAA"
        flag_list = []
        for flag in default_flags:
            flag_list.append(ord(flag))

        # If false, 0 * flag value, otherwise 1 * flag value
        flag_list[1] += int(self.options.random_spell_learning) * 1     # B 
        flag_list[1] += int(self.options.random_growth) * 16            # Q
        flag_list[2] += int(self.options.random_weapon_prices) * 2      # C
        flag_list[8] += int(self.options.random_monster_abilities) * 8  # I
        flag_list[3] += int(self.options.heal_hurt_before_more) * 4     # E
        flag_list[3] += int(self.options.random_xp_requirements) * 16
        flag_list[2] += int(self.options.random_weapon_shops) * 8 * int(not self.options.shopsanity)  # Disable random shops when shopsanity is on
        flag_list[8] += int(self.options.random_monster_zones) * 2
        flag_list[9] += int(self.options.random_monster_stats) * 16
        flag_list[9] += int(self.options.random_monster_xp) * 4
        flag_list[9] += int(self.options.make_random_stats_consistent) * 1

        flag_list[10] += int(self.options.scared_metal_slimes) * 8
        flag_list[10] += int(self.options.scaled_metal_slime_xp) * 2
        flag_list[10] += int(self.options.scared_metal_slimes) * 8
        flag_list[14] += int(self.options.no_hurtmore) * 2
        flag_list[25] += int(self.options.only_healmore) * 2
        flag_list[15] += int(self.options.no_numbers) * 16
        flag_list[15] += int(self.options.invisible_hero) * 4
        flag_list[15] += int(self.options.invisible_npcs) * 1

        flag_list[5] += int(self.options.enable_menu_wrapping) * 16
        flag_list[5] += int(self.options.enable_death_necklace) * 4
        flag_list[5] += int(self.options.enable_battle_torches) * 1
        flag_list[6] += int(self.options.repel_in_dungeons) * 2
        flag_list[7] += int(self.options.permanent_repel) * 16
        flag_list[7] += int(self.options.permanent_torch) * 4
        flag_list[11] += int(self.options.fast_text) * 4
        flag_list[11] += int(self.options.speed_hacks) * 1
        flag_list[21] += int(self.options.summer_sale) * 1
        flag_list[21] += int(self.options.levelling_speed) * 4   # I think this just works???
        flag_list[30] += int(self.options.level_1_radiant) * 8
        flag_list[35] += int(self.options.level_1_repel) * 4
        flag_list[16] += int(self.options.easy_charlock) * 8
        flag_list[17] += int(self.options.modern_spell_names) * 1
        flag_list[23] += int(self.options.skip_original_credits) * 4
        flag_list[30] += int(self.options.return_escapes) * 4
        flag_list[30] += int(self.options.return_to_town) * 2
        flag_list[30] += int(self.options.warp_whistle) * 1
        flag_list[31] += int(self.options.levelup_refill) * 8
        flag_list[33] += int(self.options.ascetic_king) * 4
        flag_list[24] += int(self.options.charlock_inn) * 8
        flag_list[28] += int(self.options.dl1_crits) * 8
        flag_list[28] += int(self.options.dl2_crits) * 2

        flag_list[22] += int(self.options.shuffle_music) * 4
        flag_list[22] += int(self.options.disable_music) * 2
        flag_list[23] += int(self.options.show_death_counter) * 16
        flag_list[22] += int(self.options.disable_spell_flashing) * 1
        flag_list[27] += int(self.options.disable_red_flashes) * 8
        flag_list[18] += int(self.options.noir_mode) * 8
        flag_list[27] += int(self.options.magic_herbs) * 16
        flag_list[35] += int(self.options.normal_flute_speed) * 2

        final_flags = ""
        for flag in flag_list:
            final_flags += chr(flag)
        
        return final_flags


        
