import typing
import settings

from Utils import local_path
from BaseClasses import Item, ItemClassification, Tutorial
from .GameID import jak1_id, jak1_name
from .JakAndDaxterOptions import JakAndDaxterOptions
from .Items import JakAndDaxterItem
from .Locations import JakAndDaxterLocation, location_table
from .Items import JakAndDaxterItem, item_table
from .locs import CellLocations as Cells, ScoutLocations as Scouts, OrbLocations as Orbs, SpecialLocations as Specials
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="JakAndDaxterClient")


components.append(Component("Jak and Daxter Client",
                            "JakAndDaxterClient",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="egg"))

icon_paths["egg"] = local_path("worlds", "jakanddaxter", "icons", "egg.png")


class JakAndDaxterSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """Path to folder containing the ArchipelaGOAL mod executables (gk.exe and goalc.exe)."""
        description = "ArchipelaGOAL Root Directory"

    root_directory:  RootDirectory = RootDirectory("D:/Files/Repositories/ArchipelaGOAL/out/build/Release/bin")


class JakAndDaxterWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelaGOAL (Archipelago on OpenGOAL).",
        "English",
        "setup_en.md",
        "setup/en",
        ["markustulliuscicero"]
    )

    tutorials = [setup_en]


class JakAndDaxterWorld(World):
    """
    Jak and Daxter: The Precursor Legacy is a 2001 action platformer developed by Naughty Dog
    for the PlayStation 2. The game follows the eponymous protagonists, a young boy named Jak
    and his friend Daxter, who has been transformed into an ottsel. With the help of Samos
    the Sage of Green Eco and his daughter Keira, the pair travel north in search of a cure for Daxter,
    discovering artifacts created by an ancient race known as the Precursors along the way. When the
    rogue sages Gol and Maia Acheron plan to flood the world with Dark Eco, they must stop their evil plan
    and save the world.
    """
    # ID, name, version
    game = jak1_name
    required_client_version = (0, 4, 6)

    # Options
    settings: typing.ClassVar[JakAndDaxterSettings]
    options_dataclass = JakAndDaxterOptions
    options: JakAndDaxterOptions

    # Web world
    web = JakAndDaxterWebWorld()

    # Items and Locations
    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    # Remember, the game ID and various offsets for each item type have already been calculated.
    item_name_to_id = {item_table[k]: k for k in item_table}
    location_name_to_id = {location_table[k]: k for k in location_table}
    item_name_groups = {
        "Power Cells": {item_table[k]: k for k in item_table
                        if k in range(jak1_id, jak1_id + Scouts.fly_offset)},
        "Scout Flies": {item_table[k]: k for k in item_table
                        if k in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset)},
        "Specials": {item_table[k]: k for k in item_table
                     if k in range(jak1_id + Specials.special_offset, jak1_id + Orbs.orb_offset)},
        # TODO - Make group for Precursor Orbs.
        # "Precursor Orbs": {item_table[k]: k for k in item_table
        #                    if k in range(jak1_id + Orbs.orb_offset, ???)},
    }

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    # Helper function to reuse some nasty if/else trees.
    @staticmethod
    def item_type_helper(item) -> (int, ItemClassification):
        # Make 101 Power Cells.
        if item in range(jak1_id, jak1_id + Scouts.fly_offset):
            classification = ItemClassification.progression_skip_balancing
            count = 101

        # Make 7 Scout Flies per level.
        elif item in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset):
            classification = ItemClassification.progression_skip_balancing
            count = 7

        # Make only 1 of each Special Item.
        elif item in range(jak1_id + Specials.special_offset, jak1_id + Orbs.orb_offset):
            classification = ItemClassification.progression
            count = 1

        # TODO - Make ??? Precursor Orbs.
        # elif item in range(jak1_id + Orbs.orb_offset, ???):
        #     classification = ItemClassification.filler
        #     count = ???

        # If we try to make items with ID's higher than we've defined, something has gone wrong.
        else:
            raise KeyError(f"Tried to fill item pool with unknown ID {item}.")

        return count, classification

    def create_items(self):
        for item_id in item_table:
            count, _ = self.item_type_helper(item_id)
            self.multiworld.itempool += [self.create_item(item_table[item_id]) for k in range(0, count)]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        _, classification = self.item_type_helper(item_id)
        return JakAndDaxterItem(name, classification, item_id, self.player)

    def get_filler_item_name(self) -> str:
        return "Power Cell"  # TODO - Make Precursor Orb the filler item. Until then, enjoy the free progression.


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="JakAndDaxterClient")
