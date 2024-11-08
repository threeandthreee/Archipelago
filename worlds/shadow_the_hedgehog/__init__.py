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
from worlds.shadow_the_hedgehog.Levels import GetLevelCompletionNames

from .Items import *
from .Locations import *
from . import Rules


from .Options import ShadowTheHedgehogOptions

#from . import Macros

VERSION: Tuple[int, int, int] = (0, 0, 2)


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

    options_dataclass = ShadowTheHedgehogOptions
    options: ShadowTheHedgehogOptions

    def __init__(self, *args, **kwargs):
        self.first_regions = []
        self.available_characters = []
        self.token_locations = []
        self.required_tokens = {}

        for token in TOKENS:
            self.required_tokens[token] = 0

        super(ShtHWorld, self).__init__(*args, **kwargs)

    def set_rules(self):
        Rules.set_rules(self.multiworld, self, self.player)

    def generate_early(self):
        # Choose first level here; pass into regions

        # Set maximum of levels required
        # Exclude missions listed in exclude_locations
        maximum_force_missions = self.options.force_objective_sanity_max.value
        maximum_force_mission_counter = self.options.force_objective_sanity_max_counter.value

        mission_counter = 0
        mission_total = 0

        #if self.options.enemy_sanity:
        #    for enemy in Locations.EnemySanityLocations:
        #        for i in range(1, enemy.total_count+1):
        #            id, loc = Locations.GetEnemyLocationName(enemy.stageId, enemy.enemyClass, enemy.mission_object_name, i)
        #            self.options.exclude_locations.value.add(loc)


        if self.options.objective_sanity.value and self.options.force_objective_sanity_chance > 0\
                and self.options.force_objective_sanity_max > 0:
            for locationData in Locations.MissionClearLocations:
                if mission_counter >= maximum_force_missions:
                    continue
                if locationData.requirement_count + mission_total > maximum_force_mission_counter:
                    continue
                if locationData.requirement_count == 1:
                    continue

                location_id, completion_location_name = GetLevelCompletionNames(locationData.stageId, locationData.alignmentId)

                if completion_location_name in self.options.exclude_locations:
                    continue

                r = self.multiworld.random.randrange(0, 100)
                if r > 100 - self.options.force_objective_sanity_chance.value:
                    #print("Make priority location:", completion_location_name)
                    self.options.priority_locations.value.add(completion_location_name)
                    mission_counter += 1
                    mission_total += locationData.requirement_count

    def create_regions(self):
        regions = Regions.create_regions(self)
        Locations.create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        for first_region in self.first_regions:
            stage_item = Items.GetStageUnlockItem(first_region)
            self.options.start_inventory.value[stage_item] = 1
            self.multiworld.push_precollected(self.create_item(stage_item))

        #self.multiworld.start_inventory

    #def create_item(self, item: str) -> ShadowTheHedgehogItem:
    #    return ShadowTheHedgehogItem(item, self.player)

    def create_item(self, name: str) -> "ShadowTheHedgehogItem":
        info = Items.GetItemByName(name)
        return ShadowTheHedgehogItem(info, self.player)

    def create_items(self):
        Items.PopulateItemPool(self, self.first_regions)

    def get_filler_item_name(self) -> str:
        # Use the same weights for filler items that are used in the base randomizer.
        pass

    def get_pre_fill_items(self):
        res = []

        return res

    def fill_slot_data(self):
        slot_data = {
            "first_levels": self.first_regions,
            "objective_sanity": self.options.objective_sanity.value,
            "objective_percentage": self.options.objective_percentage.value,
            "objective_item_percentage": self.options.objective_item_percentage.value,
            "checkpoint_sanity": self.options.checkpoint_sanity.value,
            "character_sanity": self.options.character_sanity.value,

            "required_mission_tokens": self.required_tokens[Items.Progression.StandardMissionToken],
            "required_hero_tokens": self.required_tokens[Items.Progression.StandardHeroToken],
            "required_dark_tokens": self.required_tokens[Items.Progression.StandardDarkToken],
            "required_final_tokens": self.required_tokens[Items.Progression.FinalToken],
            "required_objective_tokens": self.required_tokens[Items.Progression.ObjectiveToken],
            "requires_emeralds": self.options.goal_chaos_emeralds.value
        }


        return slot_data
