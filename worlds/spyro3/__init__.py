# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import Spyro3Item, Spyro3ItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import Spyro3Location, Spyro3LocationCategory, location_tables, location_dictionary
from .Options import Spyro3Option

class Spyro3Web(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Spyro 3 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )


    tutorials = [setup_en]


class Spyro3World(World):
    """
    Spyro 3 is a game about a purple dragon who likes eggs.
    """

    game: str = "Spyro 3"
    options_dataclass = Spyro3Option
    options: Spyro3Option
    topology_present: bool = True
    web = Spyro3Web()
    data_version = 0
    base_id = 1230000
    enabled_location_categories: Set[Spyro3LocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = Spyro3Item.get_name_to_id()
    location_name_to_id = Spyro3Location.get_name_to_id()
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
        self.enabled_location_categories.add(Spyro3LocationCategory.EGG),
        self.enabled_location_categories.add(Spyro3LocationCategory.EVENT),

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Sunrise Springs","Sunny Villa","Cloud Spires","Molten Crater","Seashell Shore","Mushroom Speedway","Shiela's Alp", "Buzz", "Crawdad Farm",
            "Midday Garden","Icy Peak","Enchanted Towers","Spooky Swamp","Bamboo Terrace","Country Speedway","Sgt. Byrd's Base","Spike","Spider Town",
            "Evening Lake","Frozen Altars","Lost Fleet","Fireworks Factory","Charmed Ridge","Honey Speedway","Bentley's Outpost","Scorch","Starfish Reef",
            "Midnight Mountain","Crystal Islands","Desert Ruins","Haunted Tomb","Dino Mines","Harbor Speedway","Agent 9's Lab","Sorceress","Bugbot Factory","Super Bonus Round"
        ]})
        
        # Connect Regions
        def create_connection(from_region: str, to_region: str, rule = None):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region], rule)
            print(f"Connecting {from_region} to {to_region} Using entrance: " + connection.name)
            
        create_connection("Menu", "Sunrise Springs")       
                
        create_connection("Sunrise Springs", "Sunny Villa")
        create_connection("Sunrise Springs", "Cloud Spires")
        create_connection("Sunrise Springs", "Molten Crater")
        create_connection("Sunrise Springs", "Seashell Shore")
        create_connection("Sunrise Springs", "Mushroom Speedway")
        create_connection("Sunrise Springs", "Shiela's Alp")
             
        create_connection("Sunrise Springs", "Buzz")
        create_connection("Sunrise Springs", "Crawdad Farm")        
        create_connection("Sunrise Springs", "Midday Garden")     
        
        create_connection("Midday Garden", "Icy Peak")
        create_connection("Midday Garden", "Enchanted Towers")
        create_connection("Midday Garden", "Spooky Swamp")
        create_connection("Midday Garden", "Bamboo Terrace")
        create_connection("Midday Garden", "Country Speedway")
        create_connection("Midday Garden", "Sgt. Byrd's Base")

        create_connection("Midday Garden", "Spike")
        create_connection("Midday Garden", "Spider Town")        
        create_connection("Midday Garden", "Evening Lake")   
        
        create_connection("Evening Lake", "Frozen Altars")
        create_connection("Evening Lake", "Lost Fleet")
        create_connection("Evening Lake", "Fireworks Factory")
        create_connection("Evening Lake", "Charmed Ridge")
        create_connection("Evening Lake", "Honey Speedway")
        create_connection("Evening Lake", "Bentley's Outpost")

        create_connection("Evening Lake", "Scorch")
        create_connection("Evening Lake", "Starfish Reef")        
        create_connection("Evening Lake", "Midnight Mountain")   
        
        create_connection("Midnight Mountain", "Crystal Islands")
        create_connection("Midnight Mountain", "Desert Ruins")
        create_connection("Midnight Mountain", "Haunted Tomb")
        create_connection("Midnight Mountain", "Dino Mines")
        create_connection("Midnight Mountain", "Harbor Speedway")
        create_connection("Midnight Mountain", "Agent 9's Lab")

        create_connection("Midnight Mountain", "Sorceress")
        create_connection("Midnight Mountain", "Bugbot Factory")
        create_connection("Midnight Mountain", "Super Bonus Round")
        
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        #print("location table size: " + str(len(location_table)))
        for location in location_table:
            #print("Creating location: " + location.name)
            if location.category in self.enabled_location_categories and location.category != Spyro3LocationCategory.EVENT:
                #print("Adding location: " + location.name + " with default item " + location.default_item)
                new_location = Spyro3Location(
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
                #if event_item.classification != ItemClassification.progression:
                #    continue
                #print("Adding Location: " + location.name + " as an event with default item " + location.default_item)
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                #print("Placing event: " + event_item.name + " in location: " + location.name)

            new_region.locations.append(new_location)
        print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        print("adding region: " + region_name)
        return new_region


    def create_items(self):
        skip_items: List[Spyro3Item] = []
        itempool: List[Spyro3Item] = []
        itempoolSize = 0
        
        #print("Creating items")
        for location in self.multiworld.get_locations(self.player):
            
                #print("found item in category: " + str(location.category))
                item_data = item_dictionary[location.default_item_name]
                if item_data.category in [Spyro3ItemCategory.SKIP] or location.category in [Spyro3LocationCategory.EVENT]:
                    #print("Adding skip item: " + location.default_item_name)
                    skip_items.append(self.create_item(location.default_item_name))
                elif location.category in self.enabled_location_categories:
                    #print("Adding item: " + location.default_item_name)
                    itempoolSize += 1
                    itempool.append(self.create_item(location.default_item_name))
        
        print("Requesting itempool size: " + str(itempoolSize))
        foo = BuildItemPool(itempoolSize, self.options)
        print("Created item pool size: " + str(len(foo)))

        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]
        print("marked " + str(len(removable_items)) + " items as removable")
        
        for item in removable_items:
            print("removable item: " + item.name)
            itempool.remove(item)
            itempool.append(self.create_item(foo.pop().name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

        # Handle SKIP items separately
        for skip_item in skip_items:
            location = next(loc for loc in self.multiworld.get_locations(self.player) 
                            if loc.default_item_name == skip_item.name)
            location.place_locked_item(skip_item)
            #self.multiworld.itempool.append(skip_item)
            #print("Placing skip item: " + skip_item.name + " in location: " + location.name)
        
        print("Final Item pool: ")
        for item in self.multiworld.itempool:
            print(item.name)


    def create_item(self, name: str) -> Item:
        useful_categories = {
        }
        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category == Spyro3ItemCategory.EGG or item_dictionary[name].category == Spyro3ItemCategory.EVENT:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return Spyro3Item(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return "Egg"
    
    def set_rules(self) -> None:   
        def get_egg_count(self, state):
            egg_count = 0
            eggLocations = self.multiworld.get_locations(self.player)
            
            for location in eggLocations: 
                if location.category == Spyro3LocationCategory.EGG:
                    has_egg = state.has(location.default_item, self.player)
                    if has_egg:
                        egg_count = egg_count + 1
            print("Obtainable egg count: " + str(egg_count))
            return egg_count
        
        def is_level_completed(self, level, entrance, state):
            #print("Checking if level is completed: " + level)
            level_table = location_tables[level]
            #print("Level table size: " + str(len(level_table)))
            lock_location = level_table[0].name    
            #print("Lock location: " + lock_location)   
            reachable = state.can_reach_location(lock_location, self.player)
            return reachable
        
        def is_boss_defeated(self, boss, state):
            level_table = location_tables[boss]
            lock_location = level_table[0].name            
            return state.can_reach_location(lock_location , self.player)    
        print("Setting rules")   
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                    set_rule(location, lambda state: True)
        self.multiworld.completion_condition[self.player] = lambda state:  is_boss_defeated(self,"Sorceress", state) and state.has("Egg", self.player, 100)
        
        #set_rule(self.multiworld.get_location("Sunny Villa Complete", self.player), lambda state: state.can_reach_location("Egg 6", self.player))
        set_rule(self.multiworld.get_entrance("Molten Crater", self.player),
                lambda state: state.has("Egg", self.player, 10))    
        set_rule(self.multiworld.get_entrance("Seashell Shore", self.player),
                lambda state: state.has("Egg", self.player, 14))   
        set_rule(self.multiworld.get_entrance("Mushroom Speedway", self.player),
                lambda state: state.has("Egg", self.player, 20)) 
                  
        set_rule(self.multiworld.get_entrance("Buzz", self.player), lambda state: is_level_completed(self,"Sunny Villa","Buzz", state) and \
                is_level_completed(self,"Cloud Spires","Buzz", state) and \
                is_level_completed(self,"Molten Crater","Buzz", state) and \
                is_level_completed(self,"Seashell Shore","Buzz", state) and \
                is_level_completed(self,"Shiela's Alp","Buzz", state) and \
                state.has("Egg", self.player, 15))       

        set_rule(self.multiworld.get_entrance("Crawdad Farm", self.player), lambda state: is_boss_defeated(self,"Buzz", state) and state.has("Egg", self.player, 16))  
        self.multiworld.register_indirect_condition("Buzz", self.multiworld.get_region("Crawdad Farm", self.player).entrances[0])     

        set_rule(self.multiworld.get_entrance("Midday Garden", self.player), lambda state: is_boss_defeated(self,"Buzz", state))      
                  
        set_rule(self.multiworld.get_entrance("Icy Peak", self.player), lambda state: state.has("Egg", self.player,16))
        set_rule(self.multiworld.get_entrance("Enchanted Towers", self.player), lambda state: state.has("Egg", self.player,16))
        set_rule(self.multiworld.get_entrance("Spooky Swamp", self.player), lambda state: state.has("Egg", self.player,25))
        set_rule(self.multiworld.get_entrance("Bamboo Terrace", self.player), lambda state: state.has("Egg", self.player,30))
        set_rule(self.multiworld.get_entrance("Country Speedway", self.player), lambda state: state.has("Egg", self.player,36))
        set_rule(self.multiworld.get_entrance("Sgt. Byrd's Base", self.player), lambda state: state.has("Egg", self.player,16)    )               

        set_rule(self.multiworld.get_entrance("Spike", self.player), lambda state: is_level_completed(self,"Icy Peak","Spike", state) and \
                is_level_completed(self,"Enchanted Towers","Spike", state) and \
                is_level_completed(self,"Spooky Swamp","Spike", state) and \
                is_level_completed(self,"Bamboo Terrace","Spike", state) and \
                is_level_completed(self,"Sgt. Byrd's Base","Spike", state) and \
                state.has("Egg", self.player,31))
        
        set_rule(self.multiworld.get_entrance("Spider Town", self.player), lambda state: is_boss_defeated(self,"Spike", state) and state.has("Egg", self.player,32))
        set_rule(self.multiworld.get_entrance("Evening Lake", self.player), lambda state: is_boss_defeated(self,"Spike", state))     

        set_rule(self.multiworld.get_entrance("Frozen Altars", self.player), lambda state: state.has("Egg", self.player,32))
        set_rule(self.multiworld.get_entrance("Lost Fleet", self.player), lambda state: state.has("Egg", self.player,32))
        set_rule(self.multiworld.get_entrance("Fireworks Factory", self.player), lambda state: state.has("Egg", self.player,50))
        set_rule(self.multiworld.get_entrance("Charmed Ridge", self.player), lambda state: state.has("Egg", self.player,59))
        set_rule(self.multiworld.get_entrance("Honey Speedway", self.player), lambda state: state.has("Egg", self.player,65))
        set_rule(self.multiworld.get_entrance("Bentley's Outpost", self.player), lambda state: state.has("Egg", self.player,32))

        set_rule(self.multiworld.get_entrance("Scorch", self.player), lambda state: is_level_completed(self,"Frozen Altars","Scorch", state) and \
                is_level_completed(self,"Lost Fleet","Scorch", state) and \
                is_level_completed(self,"Fireworks Factory","Scorch", state) and \
                is_level_completed(self,"Charmed Ridge","Scorch", state) and \
                is_level_completed(self,"Bentley's Outpost","Scorch", state) and \
                state.has("Egg", self.player,60))
        
        set_rule(self.multiworld.get_entrance("Starfish Reef", self.player), lambda state: is_boss_defeated(self,"Scorch", state) and state.has("Egg", self.player,61)) 
        set_rule(self.multiworld.get_entrance("Midnight Mountain", self.player), lambda state: is_boss_defeated(self,"Scorch", state))

        set_rule(self.multiworld.get_entrance("Crystal Islands", self.player), lambda state: state.has("Egg", self.player,61))
        set_rule(self.multiworld.get_entrance("Desert Ruins", self.player), lambda state: state.has("Egg", self.player,61))
        set_rule(self.multiworld.get_entrance("Haunted Tomb", self.player), lambda state: state.has("Egg", self.player,70))
        set_rule(self.multiworld.get_entrance("Dino Mines", self.player), lambda state: state.has("Egg", self.player,80))
        set_rule(self.multiworld.get_entrance("Harbor Speedway", self.player), lambda state: state.has("Egg", self.player,90))
        set_rule(self.multiworld.get_entrance("Agent 9's Lab", self.player), lambda state: state.has("Egg", self.player,61))

        set_rule(self.multiworld.get_entrance("Sorceress", self.player), lambda state: is_level_completed(self,"Crystal Islands","Sorceress", state) and \
                is_level_completed(self,"Desert Ruins","Sorceress", state) and \
                is_level_completed(self,"Haunted Tomb","Sorceress", state) and \
                is_level_completed(self,"Dino Mines","Sorceress", state) and \
                is_level_completed(self,"Agent 9's Lab","Sorceress", state) and \
                state.has("Egg", self.player,99))

        set_rule(self.multiworld.get_entrance("Bugbot Factory", self.player), lambda state: is_boss_defeated(self,"Sorceress", state) and state.has("Egg", self.player,100))
        set_rule(self.multiworld.get_entrance("Super Bonus Round", self.player), lambda state: is_boss_defeated(self,"Sorceress", state) and state.has("Egg", self.player,100))           
                
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_s3_code = {item.name: item.s3_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():


            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_s3_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].s3_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_s3_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "guaranteed_items": self.options.guaranteed_items.value,
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
