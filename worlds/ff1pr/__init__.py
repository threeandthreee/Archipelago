from dataclasses import fields
from typing import Dict, List, Any, Tuple, Type, TypedDict, ClassVar, Union, Set, TextIO
from logging import warning
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from .items import item_name_to_id, item_table
from .locations import location_table, standard_location_name_to_id, event_table
from .rules import set_location_rules, set_region_rules
from .regions import ff1pr_regions
from .options import FF1pixelOptions, grouped_options, presets
from worlds.AutoWorld import WebWorld, World
from Options import OptionError, PerGameCommonOptions
from settings import Group, Bool, FilePath

GAME_NAME: str = "FF1 Pixel Remaster"

class FF1pixelSettings(Group):
    class DisableLocalSpoiler(Bool):
        """Disallows the TUNIC client from creating a local spoiler log."""

    disable_local_spoiler: Union[DisableLocalSpoiler, bool] = False

class FF1pixelWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the FF1 Pixel Remaster Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["wildham"]
        )
    ]
    theme = "grassFlowers"
    game = GAME_NAME
    option_groups = grouped_options
    options_presets = presets

class FF1pixelItem(Item):
    game: str = GAME_NAME

class FF1pixelLocation(Location):
    game: str = GAME_NAME

class FF1pixelWorld(World):
    """
    Explore the world of Final Fantasy from its origins.
    """
    game = GAME_NAME
    web = FF1pixelWeb()
    required_client_version = (0, 6, 2)

    options: FF1pixelOptions
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = FF1pixelOptions
    settings: ClassVar[FF1pixelSettings]

    item_name_groups = items.item_name_groups
    location_name_groups = locations.location_name_groups
    item_name_to_id = item_name_to_id
    location_name_to_id = standard_location_name_to_id.copy()


    def generate_early(self) -> None:
        try:
            int(self.settings.disable_local_spoiler)
        except AttributeError:
            raise Exception("You have a TUNIC APWorld in your lib/worlds folder and custom_worlds folder.\n"
                            "This would cause an error at the end of generation.\n"
                            "Please remove one of them, most likely the one in lib/worlds.")

    def create_event(self, event: str) -> FF1pixelItem:
        # while we are at it, we can also add a helper to create events
        return FF1pixelItem(event, ItemClassification.progression, None, self.player)

    def create_item(self, name: str) -> FF1pixelItem:
        return FF1pixelItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        ff1pr_items: List[FF1pixelItem] = []
        items_made: int = 0

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                ff1pr_items.append(self.create_item(item))
            items_made += quantity

        #location_count = len(location_table) # adding events >_<
        #filler_count = location_count - items_made

        #for i in range(filler_count):
        #    ff1pr_items.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += ff1pr_items

    def create_regions(self) -> None:
        for region_name in ff1pr_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, exits in ff1pr_regions.items():
            region = self.get_region(region_name)
            print(region_name)
            region.add_exits(exits)

        for location_name, location_id in self.location_name_to_id.items():
            print(location_name)
            region = self.get_region(location_table[location_name].region)
            location = FF1pixelLocation(self.player, location_name, location_id, region)
            region.locations.append(location)

        for location_name, location_data in event_table.items():
            print(location_name)
            region = self.get_region(location_data.region)
            location = FF1pixelLocation(self.player, location_name, None, region)
            region.locations.append(location)


    def set_rules(self) -> None:
        set_region_rules(self)
        set_location_rules(self)

    def get_filler_item_name(self) -> str:
        filler_list = list(self.item_name_groups["Fillers"])
        return self.random.choice(filler_list)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "shuffle_gear_shops": self.options.shuffle_gear_shops.value,
            "shuffle_spells": self.options.shuffle_spells.value,
            "shuffle_trials_maze": self.options.shuffle_trials_maze.value,
            "dungeon_encounter_rate": self.options.dungeon_encounter_rate.value,
            "overworld_encounter_rate": self.options.overworld_encounter_rate.value,
            "xp_boost": self.options.xp_boost.value,
            "gil_boost": self.options.gil_boost.value,
            "boost_menu": self.options.boost_menu.value,
         }
        return slot_data