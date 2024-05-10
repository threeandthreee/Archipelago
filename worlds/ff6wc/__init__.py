import functools
import importlib
import logging
import os
import random
import string
import threading
from typing import Any, Dict, List, Union

from BaseClasses import Item, Location, Region, MultiWorld, ItemClassification, Tutorial
from .gen_data import GenData
from . import Rom
from .patch import FF6WCPatch, NA10HASH
from worlds.generic.Rules import add_rule, set_rule, add_item_rule
from worlds.AutoWorld import World, WebWorld
from . import Locations
from . import Items
from .Logic import can_beat_final_kefka
from .Options import FF6WCOptions, generate_flagstring
import Utils
import settings

importlib.import_module(".Client", "worlds.ff6wc")  # register with SNIClient

BASE_ID = 6000


class FF6WCItem(Item):
    game = 'Final Fantasy 6 Worlds Collide'


class FF6WCLocation(Location):
    game = 'Final Fantasy 6 Worlds Collide'


class FF6WCSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the FF6 NA 1.0 rom"""
        description = "Final Fantasy III (USA) ROM File"
        copy_to = "Final Fantasy III (USA).sfc"
        md5s = [NA10HASH]
    rom_file: RomFile = RomFile(RomFile.copy_to)


class FF6WCWeb(WebWorld):
    theme = "dirt"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the FF6WC randomizer and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["bigmalletman"]
    )
    tutorials = [setup_en]


class FF6WCWorld(World):
    """
    Final Fantasy VI, initially called Final Fantasy III on the Super Nintendo in North America,
    is a role-playing game and the last in the series to feature 2D sprite based graphics.
    Worlds Collide is an open-world randomizer for Final Fantasy VI. Players begin aboard the airship
    and can travel freely between the World of Balance and the World of Ruin to discover characters and espers.
    Once you've gathered enough, you can face off against Kefka. Currently based on Worlds Collide version 1.2.2.
    """
    options_dataclass = FF6WCOptions
    options: FF6WCOptions  # type: ignore
    game = "Final Fantasy 6 Worlds Collide"
    location_name_groups = {
        "Terra Major": {*Locations.major_terra_checks},
        "Locke Major": {*Locations.major_locke_checks},
        "Edgar Major": {*Locations.major_edgar_checks},
        "Sabin Major": {*Locations.major_sabin_checks},
        "Celes Major": {*Locations.major_celes_checks},
        "Shadow Major": {*Locations.major_shadow_checks},
        "Cyan Major": {*Locations.major_cyan_checks},
        "Gau Major": {*Locations.major_gau_checks},
        "Setzer Major": {*Locations.major_setzer_checks},
        "Mog Major": {*Locations.major_mog_checks},
        "Strago Major": {*Locations.major_strago_checks},
        "Relm Major": {*Locations.major_relm_checks},
        "Umaro Major": {*Locations.major_umaro_checks},
        "Gogo Major": {*Locations.major_gogo_checks},
        "Kefka Major": {*Locations.major_kefka_checks},
        "Generic Major": {*Locations.major_generic_checks},
        "All Major": {*Locations.major_checks},
        "Terra Minor": {*Locations.minor_terra_checks},
        "Edgar Minor": {*Locations.minor_edgar_checks},
        "Sabin Minor": {*Locations.minor_sabin_checks},
        "Celes Minor": {*Locations.minor_celes_checks},
        "Shadow Minor": {*Locations.minor_shadow_checks},
        "Cyan Minor": {*Locations.minor_cyan_checks},
        "Gau Minor": {*Locations.minor_gau_checks},
        "Setzer Minor": {*Locations.minor_setzer_checks},
        "Strago Minor": {*Locations.minor_strago_checks},
        "Relm Minor": {*Locations.minor_relm_checks},
        "Umaro Minor": {*Locations.minor_umaro_checks},
        "Gogo Minor": {*Locations.minor_gogo_checks},
        "Kefka Minor": {*Locations.minor_kefka_checks},
        "Generic Minor": {*Locations.minor_generic_checks},
        "All Minor": {*Locations.minor_checks}
    }
    topology_present = False
    data_version = 0
    web = FF6WCWeb()
    wc_ready = threading.Lock()
    item_name_to_id = {name: index + BASE_ID for index, name in enumerate(Items.item_table)}
    location_name_to_id = {name: index + BASE_ID for index, name in enumerate(Locations.location_table)}

    all_characters = [
        'Terra', 'Locke', 'Cyan', 'Shadow', 'Edgar',
        'Sabin', 'Celes', 'Strago', 'Relm', 'Setzer',
        'Mog', 'Gau', 'Gogo', 'Umaro'
    ]

    all_espers = [
        "Ramuh", "Ifrit", "Shiva", "Siren", "Terrato", "Shoat", "Maduin",
        "Bismark", "Stray", "Palidor", "Tritoch", "Odin", "Raiden", "Bahamut",
        "Alexandr", "Crusader", "Ragnarok Esper", "Kirin", "ZoneSeek", "Carbunkl",
        "Phantom", "Sraphim", "Golem", "Unicorn", "Fenrir", "Starlet", "Phoenix",
    ]

    all_dragon_clears = [
        "Removed!", "Stomped!",
        "Blasted!", "Ditched!",
        "Wiped!", "Incinerated!",
        "Skunked!", "Gone!"
    ]

    item_name_groups = {
        'characters': set(all_characters),
        'espers': set(all_espers),
    }

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.starting_characters = None
        self.no_illuminas = False
        self.no_paladin_shields = False
        self.no_exp_eggs = False
        self.generator_in_use = threading.Event()
        self.wc = None
        self.rom_name_available_event = threading.Event()

    def create_item(self, name: str):
        return FF6WCItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_good_filler_item(self, name: str):
        return FF6WCItem(name, ItemClassification.useful, self.item_name_to_id[name], self.player)

    def create_filler_item(self, name: str):
        return FF6WCItem(name, ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return FF6WCItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name: str, id: Union[int, None], parent: Region) -> FF6WCLocation:
        return_location = FF6WCLocation(self.player, name, id, parent)
        return return_location

    def generate_early(self):
        if (self.options.Flagstring.value).capitalize() != "False":

            self.starting_characters = []
            character_list: List[str] = []
            flags = self.options.Flagstring.value
            # Determining Starting Characters
            flags_list = flags.split(" ")
            sc1_index = flags_list.index("-sc1") + 1
            character_list.append(flags_list[sc1_index])
            sc2_index = sc3_index = sc4_index = len(flags_list)
            if "-sc2" in flags_list:
                sc2_index = flags_list.index("-sc2") + 1
                character_list.append(flags_list[sc2_index])
            if "-sc3" in flags_list:
                sc3_index = flags_list.index("-sc3") + 1
                character_list.append(flags_list[sc3_index])
            if "-sc4" in flags_list:
                sc4_index = flags_list.index("-sc4") + 1
                character_list.append(flags_list[sc4_index])

            for character in range(len(character_list)):
                if character_list[character] == "randomngu":
                    compare_character_list = character_list.copy()
                    character_list[character] = random.choice(Rom.characters[:12]).lower()
                    while character_list[character] in compare_character_list:
                        character_list[character] = random.choice(Rom.characters[:12]).lower()
                elif character_list[character] == "random":
                    compare_character_list = character_list.copy()
                    character_list[character] = random.choice(Rom.characters[:14]).lower()
                    while character_list[character] in compare_character_list:
                        character_list[character] = random.choice(Rom.characters[:14]).lower()
                elif character_list[character] not in character_list:
                    character_list[character] = character_list[character]

            for x in range(len(character_list)):
                if x == 0:
                    flags_list[sc1_index] = character_list[x]
                if x == 1:
                    flags_list[sc2_index] = character_list[x]
                if x == 2:
                    flags_list[sc3_index] = character_list[x]
                if x == 3:
                    flags_list[sc4_index] = character_list[x]

            self.options.StartingCharacterCount.value = len(character_list)
            starting_char_options = list(self.options.StartingCharacter1.name_lookup.values())
            self.options.StartingCharacter1.value = starting_char_options.index(character_list[0])
            self.options.StartingCharacter2.value = 14
            self.options.StartingCharacter3.value = 14
            self.options.StartingCharacter4.value = 14
            if len(character_list) > 1:
                self.options.StartingCharacter2.value = starting_char_options.index(character_list[1])
            if len(character_list) > 2:
                self.options.StartingCharacter3.value = starting_char_options.index(character_list[2])
            if len(character_list) > 3:
                self.options.StartingCharacter4.value = starting_char_options.index(character_list[3])

            proper_names = " ".join(character_list)
            proper_names = proper_names.title()
            character_list = proper_names.split(" ")
            self.starting_characters = character_list

            # Determining character, esper, dragon, and boss requirements
            # Finding KT Objective in flagstring (starts with 2)
            character_count = 0
            esper_count = 0
            dragon_count = 0
            boss_count = 0

            kt_obj_list: List[str] = []
            kt_obj_code_index = len(flags_list)
            alphabet = string.ascii_lowercase
            for letter in range(len(alphabet)):
                objective_list = ["-o", alphabet[letter]]
                objective = "".join(objective_list)
                if objective in flags_list:
                    objective_code = flags_list[flags_list.index(objective) + 1]
                    objective_code_list = objective_code.split(".")
                    if objective_code_list[0] == "2":
                        # kt_obj_code = objective_code
                        kt_obj_list = objective_code_list
                        kt_obj_code_index = flags_list.index(objective) + 1
                        break
            # Determining Character, Esper, Dragon and Boss Counts
            # Since AP only (currently) takes in counts for bosses, espers, characters, and dragons, this code
            # identifies the root objective number/prefix, parses the ranges/values, and then tells the loop to skip to
            # the next requirement. There are requirements that have 2 inputs because of ranges (bosses, characters,
            # espers, dragons) and skip the next 2 indices in objective identification. The others only have 1 number in
            # objective identification and only skip 1/the next index

            # Also, the player can input a "range" of conditions to be met for KT entry. When building the AP logic of
            # the seed, suggest not including these ranges in the logic selection, but instead ensuring that all
            # possible conditions are required. As such, this section does not account for the range of conditions that
            # are required for seed completion. For example, if 1 of 2 conditions is required, one being 14 characters
            # and the other being Kill Cid, the logic should still be such that 14 characters can be acquired.

            not_ranged_obj_numbers = ["1", "3", "5", "7", "9", "11", "12"]  # Random or looking for something specific.
            skip = 2  # jumps over the initial KT requirements inputs which are indices 0, 1, and 2

            for index in range(len(kt_obj_list)):
                if skip >= index or skip >= len(kt_obj_list):
                    continue  # skips over the ranges or specific condition inputs based on condition type

                if kt_obj_list[index] in not_ranged_obj_numbers:  # not a ranged objective type
                    skip = index + 1

                else:  # is a ranged objective, note that checks (type "10") are not currently parsed by AP
                    skip = index + 2
                    count_low = int(kt_obj_list[index + 1])
                    count_high = int(kt_obj_list[index + 2])
                    if kt_obj_list[index] == "2":
                        character_count = random.randint(count_low, count_high)
                        kt_obj_list[index + 1] = str(character_count)
                        kt_obj_list[index + 2] = str(character_count)
                    elif kt_obj_list[index] == "4":
                        esper_count = random.randint(count_low, count_high)
                        kt_obj_list[index + 1] = str(esper_count)
                        kt_obj_list[index + 2] = str(esper_count)
                    elif kt_obj_list[index] == "6":
                        dragon_count = random.randint(count_low, count_high)
                        kt_obj_list[index + 1] = str(dragon_count)
                        kt_obj_list[index + 2] = str(dragon_count)
                    elif kt_obj_list[index] == "8":
                        boss_count = random.randint(count_low, count_high)
                        kt_obj_list[index + 1] = str(boss_count)
                        kt_obj_list[index + 2] = str(boss_count)
            kt_obj_list_string = ".".join(kt_obj_list)
            flags_list[kt_obj_code_index] = kt_obj_list_string

            self.options.Flagstring.value = " ".join(flags_list)
            self.options.CharacterCount.value = character_count
            self.options.EsperCount.value = esper_count
            self.options.DragonCount.value = dragon_count
            self.options.BossCount.value = boss_count

        else:
            starting_characters = [
                (self.options.StartingCharacter1.current_key).capitalize(),
                (self.options.StartingCharacter2.current_key).capitalize(),
                (self.options.StartingCharacter3.current_key).capitalize(),
                (self.options.StartingCharacter4.current_key).capitalize()
            ]
            character_count = len(starting_characters) - starting_characters.count("None")
            self.options.StartingCharacterCount.value = character_count

            starting_characters.sort(key=lambda character: character == "None")
            starting_characters = starting_characters[0:character_count]

            starting_characters.sort(key=lambda character: character == "Random_with_no_gogo_or_umaro")

            filtered_starting_characters: List[str] = []
            for character in starting_characters:
                if character != "Random_with_no_gogo_or_umaro" and character in filtered_starting_characters:
                    character = random.choice(Rom.characters[:14])
                    while character in filtered_starting_characters:
                        character = random.choice(Rom.characters[:14])
                elif character == "Random_with_no_gogo_or_umaro":
                    character = random.choice(Rom.characters[:12])
                    while character in filtered_starting_characters:
                        character = random.choice(Rom.characters[:12])
                if character not in filtered_starting_characters:
                    filtered_starting_characters.append(character)
            starting_characters = filtered_starting_characters

            starting_char_options = list(self.options.StartingCharacter1.name_lookup.values())
            self.options.StartingCharacter1.value = starting_char_options.index(starting_characters[0].lower())
            self.options.StartingCharacter2.value = 14
            self.options.StartingCharacter3.value = 14
            self.options.StartingCharacter4.value = 14
            starting_char_options = list(self.options.StartingCharacter2.name_lookup.values())
            if character_count > 1:
                self.options.StartingCharacter2.value = starting_char_options.index(starting_characters[1].lower())
            if character_count > 2:
                self.options.StartingCharacter3.value = starting_char_options.index(starting_characters[2].lower())
            if character_count > 3:
                self.options.StartingCharacter4.value = starting_char_options.index(starting_characters[3].lower())

            self.starting_characters = starting_characters

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        world_map = Region("World Map", self.player, self.multiworld)
        final_dungeon = Region("Kefka's Tower", self.player, self.multiworld)

        for name, id in self.location_name_to_id.items():
            if self.options.Treasuresanity.value == 0:
                if name in Locations.all_minor_checks:
                    continue
            if name in Locations.dragon_events:
                id = None
            if "(Boss)" in name:
                id = None
            if name in Locations.kefka_checks:
                final_dungeon.locations.append(self.create_location(name, id, final_dungeon))
            elif name in Locations.accomplishment_data:
                final_dungeon.locations.append(self.create_location(name, None, final_dungeon))
            else:
                world_map.locations.append(self.create_location(name, id, world_map))

        menu.connect(world_map)
        world_map.connect(final_dungeon)
        final_dungeon.connect(world_map)

        self.multiworld.regions.append(menu)
        self.multiworld.regions.append(world_map)
        self.multiworld.regions.append(final_dungeon)

    def create_items(self) -> None:
        # Setting variables for item restrictions based on custom flagstring or AllowStrongestItems value
        if (self.options.Flagstring.value).capitalize() != "False":
            if "-nfps" in self.options.Flagstring.value.split(" "):
                self.no_paladin_shields = True
            if "-nee" in self.options.Flagstring.value.split(" "):
                self.no_exp_eggs = True
            if "-nil" in self.options.Flagstring.value.split(" "):
                self.no_illuminas = True
        else:
            if not self.options.AllowStrongestItems.value:
                self.no_paladin_shields = True
                self.no_exp_eggs = True
                self.no_illuminas = True
        item_pool: List[FF6WCItem] = []
        assert self.starting_characters
        for item in map(self.create_item, self.item_name_to_id):
            if item.name in self.starting_characters:
                self.multiworld.push_precollected(item)
            elif item.name in Rom.characters or item.name in Rom.espers:
                item_pool.append(item)

        for index, dragon in enumerate(Locations.dragons):
            dragon_event = Locations.dragon_events_link[dragon]
            self.multiworld.get_location(dragon_event, self.player).place_locked_item(
                self.create_event(self.all_dragon_clears[index]))

        for boss in [location for location in Locations.major_checks if "(Boss)" in location]:
            self.multiworld.get_location(boss, self.player).place_locked_item(self.create_event("Busted!"))

        self.multiworld.get_location("Kefka's Tower", self.player).place_locked_item(
            self.create_event("Kefka's Tower Access"))
        self.multiworld.get_location("Beat Final Kefka", self.player).place_locked_item(
            self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        filler_pool: List[str] = []
        # Each filler item has a chest item tier weight
        filler_pool_weights: List[int] = []
        good_filler_pool: List[str] = []

        for item in Items.items:
            # Skips adding an item to filler_pool and good_filler_pool if item restrictions are in place
            if self.no_paladin_shields is True and (item == "Paladin Shld" or item == "Cursed Shld"):
                continue
            if self.no_exp_eggs is True and item == "Exp. Egg":
                continue
            if self.no_illuminas is True and item == "Illumina":
                continue
            if item != "ArchplgoItem":
                filler_pool.append(item)
                # Each filler item has a chest item tier weight
                weight = Items.item_name_weight.get(item)
                assert not (weight is None)
                filler_pool_weights.append(weight)
            if item in Items.good_items:
                good_filler_pool.append(item)

        major_items = len([location for location in Locations.major_checks if "(Boss)" not in location and "Status"
                           not in location])
        progression_items = len(item_pool)
        if not self.options.Treasuresanity.value:
            major_items = major_items - progression_items
            for _ in range(major_items):
                item_pool.append(self.create_good_filler_item(self.multiworld.random.choice(good_filler_pool)))
            self.multiworld.itempool += item_pool
        else:
            for _ in range(major_items):
                item_pool.append(self.create_good_filler_item(self.multiworld.random.choice(good_filler_pool)))
            minor_items = len(Locations.all_minor_checks) - progression_items
            for _ in range(minor_items):
                # random filler item, but use chest item tier weights
                item_pool.append(self.create_filler_item(
                    self.multiworld.random.choices(filler_pool, filler_pool_weights)[0]
                ))
            self.multiworld.itempool += item_pool

    def set_rules(self):
        check_list = {
            "Terra": (Locations.major_terra_checks, Locations.minor_terra_checks, Locations.minor_terra_ext_checks),
            "Locke": (Locations.major_locke_checks, Locations.minor_locke_checks, Locations.minor_locke_ext_checks),
            "Cyan": (Locations.major_cyan_checks, Locations.minor_cyan_checks, Locations.minor_cyan_ext_checks),
            "Shadow": (Locations.major_shadow_checks, Locations.minor_shadow_checks, Locations.minor_shadow_ext_checks),
            "Edgar": (Locations.major_edgar_checks, Locations.minor_edgar_checks, Locations.minor_edgar_ext_checks),
            "Sabin": (Locations.major_sabin_checks, Locations.minor_sabin_checks, Locations.minor_sabin_ext_checks),
            "Celes": (Locations.major_celes_checks, Locations.minor_celes_checks, Locations.minor_celes_ext_checks),
            "Strago": (Locations.major_strago_checks, Locations.minor_strago_checks, Locations.minor_strago_ext_checks),
            "Relm": (Locations.major_relm_checks, Locations.minor_relm_checks, Locations.minor_relm_ext_checks),
            "Setzer": (Locations.major_setzer_checks, Locations.minor_setzer_checks, Locations.minor_setzer_ext_checks),
            "Mog": (Locations.major_mog_checks, Locations.minor_mog_checks, Locations.minor_mog_ext_checks),
            "Gau": (Locations.major_gau_checks, Locations.minor_gau_checks, Locations.minor_gau_ext_checks),
            "Gogo": (Locations.major_gogo_checks, Locations.minor_gogo_checks, Locations.minor_gogo_ext_checks),
            "Umaro": (Locations.major_umaro_checks, Locations.minor_umaro_checks, Locations.minor_umaro_ext_checks),
        }
        # Set every character locked check to require that character.
        for check_name, checks in check_list.items():
            # Major checks. These are always on.
            for check in checks[0]:
                set_rule(self.multiworld.get_location(check, self.player),
                         lambda state, character=check_name: state.has(character, self.player))
            # Minor checks. These are only on if Treasuresanity is on.
            if self.options.Treasuresanity.value != 0:
                for check in checks[1]:
                    set_rule(self.multiworld.get_location(check, self.player),
                             lambda state, character=check_name: state.has(character, self.player))
            # Minor extended gating checks. These are on if Treasuresanity are on, but can be character gated.
            if self.options.Treasuresanity.value == 2:
                for check in checks[2]:
                    set_rule(self.multiworld.get_location(check, self.player),
                             lambda state, character=check_name: state.has(character, self.player))

        # Lock (ha!) these behind Terra as well as Locke, since whatever isn't chosen is put behind Whelk
        for check_name in ["Narshe Weapon Shop 1", "Narshe Weapon Shop 2"]:
            add_rule(self.multiworld.get_location(check_name, self.player),
                     lambda state: state.has("Terra", self.player))

        for check in Locations.major_checks:
            add_item_rule(self.multiworld.get_location(check, self.player),
                          lambda item: item.name not in Items.okay_items)

        for check in Locations.item_only_checks:
            if self.options.Treasuresanity.value != 0 or (
                    check not in Locations.minor_checks and check not in Locations.minor_ext_checks):
                add_item_rule(self.multiworld.get_location(check, self.player),
                              lambda item: (item.name not in self.item_name_groups["characters"]
                                            and item.name not in self.item_name_groups['espers']
                                            or item.player != self.player))

        for check in Locations.no_character_checks:
            add_item_rule(self.multiworld.get_location(check, self.player),
                          lambda item: (item.name not in self.item_name_groups["characters"]
                                        or item.player != self.player))

        for dragon in Locations.dragons:
            dragon_event = Locations.dragon_events_link[dragon]
            add_rule(self.multiworld.get_location(dragon_event, self.player),
                     lambda state: state.can_reach(str(dragon), 'Location', self.player))

        for location in Locations.fanatics_tower_checks:
            if self.options.Treasuresanity.value != 0 or location not in Locations.all_minor_checks:
                add_rule(self.multiworld.get_location(location, self.player),
                         lambda state: state.has_group("espers", self.player, 4))

        set_rule(self.multiworld.get_location("Beat Final Kefka", self.player),
                 functools.partial(can_beat_final_kefka, self.options, self.player))

    def post_fill(self) -> None:
        spheres = list(self.multiworld.get_spheres())
        sphere_count = len(spheres)
        upgrade_base = sphere_count * 2
        for current_sphere_count, sphere in enumerate(spheres):
            for location in sphere:
                if location.item and location.item.player == self.player:
                    if self.multiworld.random.randint(0, upgrade_base) < current_sphere_count:
                        self.upgrade_item(location.item)

    def upgrade_item(self, item: Item):
        if item.name in Items.okay_items:
            # Prevents upgrades to restricted items based on flags or AllowStrongestItems value
            nfps = nee = nil = 1
            temp_new_item = ""
            while (nfps or nee or nil) == 1:
                temp_new_item = self.multiworld.random.choice(Items.good_items)
                if self.no_paladin_shields is True and (temp_new_item == "Paladin Shld"
                                                        or temp_new_item == "Cursed Shld"):
                    nfps = 1
                else:
                    nfps = 0
                if self.no_exp_eggs is True and temp_new_item == "Exp. Egg":
                    nee = 1
                else:
                    nee = 0
                if self.no_illuminas is True and temp_new_item == "Illumina":
                    nil = 1
                else:
                    nil = 0
            assert temp_new_item
            new_item = temp_new_item
            new_item_id = self.item_name_to_id[new_item]
            item.name = new_item
            item.code = new_item_id
            item.classification = ItemClassification.useful
        return

    def generate_output(self, output_directory: str):
        locations: Dict[str, str] = dict()
        # get all locations
        for region in self.multiworld.regions:
            if region.player == self.player:
                for location in region.locations:
                    assert location.item
                    if location.name in Locations.minor_checks:
                        location_name = Rom.treasure_chest_data[location.name][2]
                    elif location.name in Locations.minor_ext_checks:
                        location_name = Rom.treasure_chest_data[location.name][2]
                    else:
                        location_name = location.name
                    location_name = str(location_name)  # dict needs str keys
                    locations[location_name] = "Archipelago Item"
                    if location.item.player == self.player:
                        if location_name in Locations.major_checks or location.item.name in Items.items:
                            locations[location_name] = location.item.name
        self.rom_name_text = f'6WC{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        self.rom_name_text = self.rom_name_text[:20]
        self.romName = bytearray(self.rom_name_text, 'utf-8')
        self.romName.extend([0] * (20 - len(self.romName)))
        self.rom_name = self.romName
        self.rom_name_available_event.set()
        locations["RomName"] = self.rom_name_text
        assert not (self.starting_characters is None), "didn't get starting characters yet"
        flagstring = generate_flagstring(self.options, self.starting_characters)

        gen_data = GenData(locations, flagstring)
        out_file_base = self.multiworld.get_out_file_name_base(self.player)
        patch_file_name = os.path.join(output_directory, f"{out_file_base}{FF6WCPatch.patch_file_ending}")
        patch = FF6WCPatch(patch_file_name,
                           player=self.player,
                           player_name=self.multiworld.player_name[self.player],
                           gen_data_str=gen_data.to_json())
        patch.write()

        logging.debug(f"FF6WC player {self.player} finished generate_output")

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
