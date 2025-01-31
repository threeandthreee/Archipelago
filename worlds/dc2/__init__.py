# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DarkCloud2Item, DC2ItemCategory, item_dictionary, key_item_names, item_descriptions
from .Locations import DarkCloud2Location, DC2LocationCategory, location_tables, location_dictionary
from .Options import dark_cloud_options

import random

class DarkCloud2Web(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Dark Cloud 2 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )


    tutorials = [setup_en]


class DarkCloud2World(World):
    """
    Dark Cloud 2 is a game.
    """

    game: str = "Dark Cloud 2"
    is_experimental = True
    option_definitions = dark_cloud_options
    topology_present: bool = True
    web = DarkCloud2Web()
    data_version = 0
    base_id = 694200000
    enabled_location_categories: Set[DC2LocationCategory]
    required_client_version = (0, 4, 6)
    item_name_to_id = DarkCloud2Item.get_name_to_id()
    location_name_to_id = DarkCloud2Location.get_name_to_id()
    item_name_groups = {
    }
    item_descriptions = item_descriptions


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()


    def generate_early(self):
        self.enabled_location_categories.add(DC2LocationCategory.FLOOR)
        #self.enabled_location_categories.add(DC2LocationCategory.DUNGEON)
        self.enabled_location_categories.add(DC2LocationCategory.RECRUIT)
        self.enabled_location_categories.add(DC2LocationCategory.GEORAMA)
        self.enabled_location_categories.add(DC2LocationCategory.MIRACLE_CHEST)
        self.enabled_location_categories.add(DC2LocationCategory.BOSS)
        self.enabled_location_categories.add(DC2LocationCategory.MISC)
        self.enabled_location_categories.add(DC2LocationCategory.GEOSTONE)
        self.enabled_location_categories.add(DC2LocationCategory.EVENT)


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Palm Brinks",
            "Underground Water Channel",
            "Sindain",
            "Rainbow Butterfly Wood"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "New Game", regions["Menu"]))
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Palm Brinks"])

        create_connection("Palm Brinks", "Underground Water Channel")
        
        create_connection("Palm Brinks", "Sindain")
        
        create_connection("Sindain", "Rainbow Butterfly Wood")
        create_connection("Sindain", "Palm Brinks")
        
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            if location.category in self.enabled_location_categories:
            
                new_location = DarkCloud2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                if event_item.classification != ItemClassification.progression:
                    continue

                new_location = DarkCloud2Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)

            if region_name == "Menu":
                add_item_rule(new_location, lambda item: not item.advancement)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        
        itempool_by_category = {category: [] for category in self.enabled_location_categories}

        num_required_extra_items = 0
        for location in self.multiworld.get_locations(self.player):
            if location.category in itempool_by_category:
                if item_dictionary[location.default_item_name].category == DC2ItemCategory.SKIP:
                    num_required_extra_items += 1
                else:
                    itempool_by_category[location.category].append(location.default_item_name)

        itempool: List[DarkCloud2Item] = []
        for category in self.enabled_location_categories:
            itempool += [self.create_item(name) for name in itempool_by_category[category]]

        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]

        guaranteed_items = self.multiworld.guaranteed_items[self.player].value
        for item_name in guaranteed_items:
            if len(removable_items) == 0:
                break

            num_existing_copies = len([item for item in itempool if item.name == item_name])
            for _ in range(guaranteed_items[item_name]):
                if num_existing_copies > 0:
                    num_existing_copies -= 1
                    continue

                if num_required_extra_items > 0:
                    num_required_extra_items -= 1
                else:
                    if len(removable_items) == 0:
                        break

                    removable_shortlist = [
                        item for item
                        in removable_items
                        if item_dictionary[item.name].category == item_dictionary[item_name].category
                    ]
                    if len(removable_shortlist) == 0:
                        removable_shortlist = removable_items

                    removed_item = self.multiworld.random.choice(removable_shortlist)
                    removable_items.remove(removed_item) # To avoid trying to replace the same item twice
                    itempool.remove(removed_item)

                itempool.append(self.create_item(item_name))

        # Extra filler items for locations containing SKIP items
        itempool += [self.create_filler() for _ in range(num_required_extra_items)]

        # Add items to itempool
        self.multiworld.itempool += itempool


    def create_item(self, name: str) -> Item:
        useful_categories = {
            DC2ItemCategory.GEORAMA_RESOURCE, DC2ItemCategory.GEM, DC2ItemCategory.COIN
        }
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DarkCloud2Item(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        chance = random.randint(0, 1000)
        if chance > 990:
            #Get coin
            coinItems = {key: value for key, value in item_dictionary.items() if value.category == DC2ItemCategory.COIN}
            return random.choice(list(coinItems.keys()))
        elif chance > 940:
            weaponItems = {key: value for key, value in item_dictionary.items() if value.category == DC2ItemCategory.WEAPON_MAX_L or value.category == DC2ItemCategory.WEAPON_MAX_R or value.category == DC2ItemCategory.WEAPON_MAX_L or value.category == DC2ItemCategory.WEAPON_MONICA_R or value.category == DC2ItemCategory.WEAPON_MONICA_L} 
            return random.choice(list(weaponItems.keys()))
            #Get weapon
        elif chance > 890:
            #Get gem
            gemItems = {key: value for key, value in item_dictionary.items() if value.category == DC2ItemCategory.GEM}
            return random.choice(list(gemItems.keys()))
        elif chance > 800:
            #get pack
            return "Weapon Powder"
        else:
            consumableItems = {key: value for key, value in item_dictionary.items() if value.category == DC2ItemCategory.CONSUMABLE} 
            return random.choice(list(consumableItems.keys()))
            #get consumable


    def set_rules(self) -> None:
        # Define the access rules to the entrances
       # set_rule(self.multiworld.get_entrance("Sindain", self.player),
       #          lambda state: state.has("Chapter 1 Complete", self.player))     
                 

       
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Grape Juice", self.player) #and \
            #state.has("Chapter 2 Complete", self.player)


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_dc2_code = {item.name: item.dc2_code for item in item_dictionary.values()}
        
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            # Skip events
            if location.item.code is None:
                continue

            if location.item.player == self.player:
                items_id.append(location.item.code)
                items_address.append(name_to_dc2_code[location.item.name])

            if location.player == self.player:
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].dc2_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_dc2_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "fishsanity": self.multiworld.fishsanity[self.player].value,
                "sphedasanity": self.multiworld.sphedasanity[self.player].value,
                "medalsanity": self.multiworld.medalsanity[self.player].value,
                "georamasanity": self.multiworld.georamasanity[self.player].value,
                "photosanity": self.multiworld.photosanity[self.player].value,
                "inventionsanity": self.multiworld.inventionsanity[self.player].value,
                "resource_pack_count": self.multiworld.resource_pack_count[self.player].value,
                "weapon_upgrade_pack_count": self.multiworld.weapon_upgrade_pack_count[self.player].value,
                "element_pack_count": self.multiworld.element_pack_count[self.player].value,
                "chapter_goal_count": self.multiworld.chapter_goal_count[self.player].value,
                "abs_multiplier": self.multiworld.abs_multiplier[self.player].value,
                "gilda_multiplier": self.multiworld.gilda_multiplier[self.player].value,
                "guaranteed_items": self.multiworld.guaranteed_items[self.player].value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
        }

        return slot_data
