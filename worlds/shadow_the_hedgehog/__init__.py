import copy
import os
import random
from dataclasses import fields
from typing import ClassVar, Dict, List, Set, Tuple, Type

import yaml

from BaseClasses import ItemClassification as IC
from BaseClasses import LocationProgressType, Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from worlds.shadow_the_hedgehog import Regions, Locations
from worlds.shadow_the_hedgehog.Items import ShadowTheHedgehogItem, PopulateItemPool
from worlds.shadow_the_hedgehog.Levels import GetLevelCompletionNames
from worlds.shadow_the_hedgehog.Locations import MissionClearLocations
from worlds.shadow_the_hedgehog.Rules import set_rules

#from . import Macros

VERSION: Tuple[int, int, int] = (2, 5, 0)


def run_client():
    print("Running ShTHClient")
    from .ShTHClient import main

    launch_subprocess(main, name="ShThClient")


components.append(
    Component(
        "Shadow The Hedgehog Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".shth"),
    )
)


class ShtHWebWorld(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago Shadow The Hedgehog software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["choatix"],
        )
    ]

class ShtHWorld(World):
    """
    TODO
    """

    #options_dataclass = ShThOptions
    #options: ShThOptions

    game: ClassVar[str] = "Shadow The Hedgehog"
    topology_present: bool = True

    item_name_to_id: ClassVar[Dict[str, int]] = Items.GetItemDict()
    location_name_to_id: ClassVar[Dict[str, int]] = Locations.GetLocationDict()

    required_client_version: Tuple[int, int, int] = (0, 5, 0)
    web = ShtHWebWorld()

    def __init__(self, *args, **kwargs):
        self.first_regions = []

        super(ShtHWorld, self).__init__(*args, **kwargs)

    def set_rules(self):
        set_rules(self.multiworld, self, self.player)

    def generate_early(self):
        # Choose first level here; pass into regions

        # Set maximum of levels required
        # Exclude missions listed in exclude_locations
        maximum_force_missions = 10
        maximum_force_mission_counter = 150

        mission_counter = 0
        mission_total = 0

        for locationData in MissionClearLocations:
            if mission_counter >= maximum_force_missions:
                continue
            if locationData.requirement_count + mission_total > maximum_force_mission_counter:
                continue
            if locationData.requirement_count == 1:
                continue
            location_id, completion_location_name = GetLevelCompletionNames(locationData.stageId, locationData.alignmentId)
            r = self.multiworld.random.randrange(0, 100)
            if r > 75:
                #print("Make priority location:", completion_location_name)
                self.options.priority_locations.value.add(completion_location_name)
                mission_counter += 1
                mission_total += locationData.requirement_count

        options = self.options

    def create_regions(self):
        regions = Regions.create_regions(self)
        Locations.create_locations(regions, self.player)
        self.multiworld.regions.extend(regions.values())

    #def create_item(self, item: str) -> ShadowTheHedgehogItem:
    #    return ShadowTheHedgehogItem(item, self.player)

    def create_item(self, name: str) -> "ShadowTheHedgehogItem":
        return Items.GetItemByName(name)

    def create_items(self):
        PopulateItemPool(self, self.first_regions)

    def get_filler_item_name(self) -> str:
        # Use the same weights for filler items that are used in the base randomizer.
        pass

    def get_pre_fill_items(self):
        res = []

        return res

    def fill_slot_data(self):
        slot_data = {
            "first_levels": self.first_regions
        }

        return slot_data
