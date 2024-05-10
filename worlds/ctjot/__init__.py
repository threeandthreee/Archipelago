from BaseClasses import Item, Location, MultiWorld, Tutorial, Region, CollectionState
from worlds.AutoWorld import World, WebWorld

from .Client import CTJoTSNIClient
from . import CTJoTDefaults
from .Items import CTJoTItemManager
from .Locations import CTJoTLocationManager
from .Options import Locations, Items, Rules, Victory, GameMode, \
    ItemDifficulty, TabTreasures, BucketFragments, FragmentCount

import threading
from typing import Callable


class CTJoTWebWorld(WebWorld):
    settings_page = "https://multiworld.ctjot.com/"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Jets of Time multiworld.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Anguirel"]
    )]


class CTJoTWorld(World):
    """
    Jet of Time is an open world randomizer for the iconic JRPG Chrono Trigger.

    Players start with two characters and the winged Epoch and must journey through time finding
    additional characters and key items to save the world from the evil Lavos.
    """

    _item_manager = CTJoTItemManager()
    _location_manager = CTJoTLocationManager()

    game = "Chrono Trigger Jets of Time"
    option_definitions = {
        "game_mode": GameMode,
        "item_difficulty": ItemDifficulty,
        "tab_treasures": TabTreasures,
        "bucket_fragments": BucketFragments,
        "fragment_count": FragmentCount,
        "items": Items,
        "locations": Locations,
        "rules": Rules,
        "victory": Victory
    }

    item_name_to_id = _item_manager.get_item_name_to_id_mapping()
    location_name_to_id = _location_manager.get_location_name_to_id_mapping()

    web = CTJoTWebWorld()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()

    def create_item(self, name: str) -> Item:
        """
        Create a CTJoT multiworld item.

        Overridden from World
        """
        return self._item_manager.create_item(name, self.player)

    def create_items(self) -> None:
        """
        Create items for the player from the passed in
        config data and append them to the multiworld item pool.

        Overridden from World
        """
        items_from_config = self._get_config_value("items", CTJoTDefaults.DEFAULT_ITEMS)
        items = []

        # This handles the key items from the yaml.
        for item in items_from_config:
            items.append(self._item_manager.create_item_by_id(item["id"], self.player))

        # Now add filler/useful items to spots that didn't roll key items
        items.extend(
            self._item_manager.select_filler_items(
                self._location_manager.get_filler_location_ids(self.multiworld, self.player),
                self.multiworld,
                self.player))

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        """
        Set up the locations and rules for this player.

        Overridden from World
        """
        locations_from_config = self._get_config_value("locations", CTJoTDefaults.DEFAULT_LOCATIONS)
        rules_from_config = self._get_config_value("rules", CTJoTDefaults.DEFAULT_RULES)
        victory_rules_from_config = self._get_config_value("victory", CTJoTDefaults.DEFAULT_VICTORY)
        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.multiworld = self.multiworld

        # Create Location objects from yaml location data and add them to the menu region.
        for location_entry in locations_from_config:
            if location_entry["classification"] == "event":
                # Create event locations/items (character pickup locations)
                location = Location(self.player, location_entry["name"], None, menu_region)
                location.event = True
                # Add character here as a locked item.
                location.place_locked_item(
                    self._item_manager.create_event_item(location_entry["character"], self.player))
            else:
                # Create normal locations
                location = self._location_manager.get_location(self.player, location_entry, menu_region)

            location.access_rule = self._get_access_rule(rules_from_config[location_entry["name"]])
            menu_region.locations.append(location)

        # Add filler locations for non-progression items
        self._location_manager.add_filler_locations(self.multiworld, self.player, menu_region)

        # Add victory condition event
        victory_location = Location(self.player, "Victory", None, menu_region)
        victory_location.event = True
        victory_location.access_rule = self._get_access_rule(victory_rules_from_config)
        victory_location.place_locked_item(self._item_manager.create_event_item("Victory", self.player))
        menu_region.locations.append(victory_location)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.multiworld.regions += [menu_region]

    def get_filler_item_name(self) -> str:
        """
        Get a random filler item.

        Overridden from World
        """
        return self.multiworld.random.choice(self._item_manager.get_junk_fill_items())

    def modify_multidata(self, multidata: dict):
        import base64
        player_name = self.multiworld.player_name[self.player]
        if player_name and player_name != "":
            new_name = base64.b64encode(bytes(player_name.encode("ascii"))).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def _get_access_rule(self, access_rules: list[list[str]]) -> Callable[[CollectionState], bool]:
        """
        Create an access rule function from yaml access_rule data.

        :param access_rules: A list contains lists of item/character requirements for this access rule
        :return: Callable access rule based on the list of requirements
        """
        def can_access(state: CollectionState) -> bool:
            # No access rules means this is sphere 1
            if len(access_rules) == 0:
                return True

            # loop through each access rule for this location
            for rule in access_rules:
                has_access = True
                for item in rule:
                    if not state.has(item, self.player):
                        has_access = False
                        break
                # Check if we have all the items from the rule
                if has_access:
                    return True

            # We didn't satisfy any of the access rules
            return False

        return can_access

    def _get_config_value(self, value: str, default):
        """
        Get a value from the multiworld config for this player. If the value is
        empty then return the provided default.

        :param value: Name of the value to get from config data
        :param default: Default value to return if the config value is empty
        :return: Config value if it exists or default if it doesn't
        """
        config_value = getattr(self.multiworld, value)[self.player].value
        if len(config_value) == 0:
            return default
        return config_value
