from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KHBBSItem, KHBBSItemData, event_item_table, get_items_by_category, item_table, item_name_groups
from .Locations import KHBBSLocation, location_table, get_locations_by_category, location_name_groups
from .Options import KHBBSOptions
from .Regions import create_regions
from .Rules import set_rules
from .OpenKH import patch_khbbs
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="KHBBS Client")


components.append(Component("KHBBS Client", "KHBBSClient", func=launch_client, component_type=Type.CLIENT))


class KHBBSWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kingdom Hearts BBS Randomizer software on your computer. This guide covers single-player, "
            "multiworld, and related software.",
            "English",
            "kh1_en.md",
            "kh1/en",
            ["Gicu"]
    )]


class KHBBSWorld(World):
    """
    Kingdom Hearts is an action RPG following Sora on his journey 
    through many worlds to find Riku and Kairi.
    """
    game = "Kingdom Hearts Birth by Sleep"
    options_dataclass = KHBBSOptions
    options: KHBBSOptions
    topology_present = True
    required_client_version = (0, 3, 5)
    web = KHBBSWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def create_items(self):
        character_letters = ["V", "A", "T"]
        prefilled_items = ["Victory"]
        #Handle starting worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = ["Dwarf Woodlands", 
                "Castle of Dreams", "Enchanted Dominion", "The Mysterious Tower", 
                "Radiant Garden", "Olympus Coliseum", "Deep Space",
                "Never Land", "Disney Town"]
            starting_worlds = self.random.sample(possible_starting_worlds, min(self.options.starting_worlds, len(possible_starting_worlds)))
            for starting_world in starting_worlds:
                self.multiworld.push_precollected(self.create_item(starting_world))
        item_pool: List[KHBBSItem] = []
        
        total_locations = len(self.multiworld.get_unfilled_locations(self.player)) - 1
        
        non_filler_item_categories = ["Movement Command", "Defense Command", "Reprisal Command", 
            "Shotlock Command", "Command Style", "Ability", "Key Item", "World", "Stat Up", "D-Link"]
        for name, data in item_table.items():
            quantity = data.max_quantity
            if data.category not in non_filler_item_categories:
                continue
            if name in starting_worlds:
                continue
            if character_letters[self.options.character] in data.characters and name not in prefilled_items:
                item_pool += [self.create_item(name) for _ in range(0, quantity)]
        # Fill any empty locations with filler items.
        item_names = []
        attempts = 0  # If we ever try to add items 200 times, and all the items are used up, lets clear the item_names array, we probably don't have enough items
        while len(item_pool) < total_locations:
            item_name = self.get_filler_item_name()
            if item_name not in item_names:
                item_names.append(item_name)
                item_pool.append(self.create_item(item_name))
                attempts = 0
            elif attempts >= 200:
                item_names = []
                attempts = 0
            else:
                attempts = attempts + 1

        self.multiworld.itempool += item_pool

    def pre_fill(self) -> None:
        goal_locations = ["(V) The Keyblade Graveyard Defeat Final Vanitas",
            "(A) The Keyblade Graveyard Defeat Ventus-Vanitas",
            "(T) The Keyblade Graveyard Defeat Terra-Xehanort"]
        if self.options.character == 1 and self.options.final_terra_xehanort_ii:
             self.multiworld.get_location("(A) Radiant Garden Defeat Final Terra-Xehanort II", self.player).place_locked_item(self.create_item("Victory"))
        else:
            self.multiworld.get_location(goal_locations[self.options.character], self.player).place_locked_item(self.create_item("Victory"))

    def get_filler_item_name(self) -> str:
        fillers = {}
        exclude = []
        characters = ["V","A","T"]
        fillers.update(get_items_by_category("Attack Command",     exclude, characters[self.options.character]))
        fillers.update(get_items_by_category("Magic Command",      exclude, characters[self.options.character]))
        fillers.update(get_items_by_category("Item Command",       exclude, characters[self.options.character]))
        fillers.update(get_items_by_category("Friendship Command", exclude, characters[self.options.character]))
        weights = [data.weight for data in fillers.values()]
        return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def fill_slot_data(self) -> dict:
        slot_data = {"xpmult":                  int(self.options.exp_multiplier)/16,
                     "non_remote_location_ids": self.get_non_remote_location_ids()}
        return slot_data
    
    def create_item(self, name: str) -> KHBBSItem:
        data = item_table[name]
        return KHBBSItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KHBBSItem:
        data = event_item_table[name]
        return KHBBSItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)

    def generate_output(self, output_directory: str):
        """
        Generates the .zip for OpenKH (The KH Mod Manager)
        """
        patch_khbbs(self, output_directory, self.options.character)
    
    def get_non_remote_location_ids(self):
        non_remote_location_ids = []
        for location in self.multiworld.get_filled_locations(self.player):
            location_data = location_table[location.name]
            if self.player == location.item.player:
                item_data = item_table[location.item.name]
                if location_data.type == "Chest":
                    if item_data.category in ["Attack Command", "Magic Command", "Item Command", "Friendship Command", "Movement Command", "Defense Command", "Reprisal Command", "Shotlock Command", "Key Item"] and not location_data.forced_remote:
                        non_remote_location_ids.append(location_data.code)
                if location_data.type == "Sticker":
                    if item_data.category in ["Key Item"]:
                        non_remote_location_ids.append(location_data.code)
        return non_remote_location_ids