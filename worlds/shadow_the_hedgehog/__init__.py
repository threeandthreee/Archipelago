import random
from typing import ClassVar, Tuple
from BaseClasses import  Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .Levels import GetLevelCompletionNames
from .Items import *
from .Locations import *

from . import Options, Rules, Regions, Utils as ShadowUtils


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

    options_dataclass = Options.ShadowTheHedgehogOptions
    options: Options.ShadowTheHedgehogOptions

    item_name_groups = Items.get_item_groups()

    def __init__(self, *args, **kwargs):
        self.first_regions = []
        self.available_characters = []
        self.available_weapons = []
        self.available_levels = []
        self.token_locations = []
        self.required_tokens = {}
        self.excess_item_count = 0

        for token in TOKENS:
            self.required_tokens[token] = 0

        super(ShtHWorld, self).__init__(*args, **kwargs)

    def set_rules(self):
        Rules.set_rules(self.multiworld, self, self.player)

    def check_invalid_configurations(self):
        if self.options.auto_clear_missions and not self.options.objective_sanity:
            raise OptionError("Cannot auto clear missions alongside not objective sanity.")

        if (self.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked
                and not self.options.weapon_sanity_unlock):
            raise OptionError("Cannot use unlock mode for weapons without weaponsanity lock.")

        if self.options.level_progression == Options.LevelProgression.option_select and \
            self.options.starting_stages == 0:
            raise OptionError("Cannot start select mode with 0 starting stages")

    def calculate_object_discrepancies(self):

        override_settings = self.options.percent_overrides
        percentage = self.options.enemy_sanity_percentage.value
        objective_percentage = self.options.objective_percentage.value
        for stage in ALL_STAGES:

            related_clears = [ c for c in MissionClearLocations if c.stageId == stage]
            related_es = [ e for e in EnemySanityLocations if e.stageId == stage ]

            for clear in related_clears:
                clear_class = None
                alignment_id = None
                key_prefix = None

                if clear.mission_object_name == "Alien":
                    clear_class = ENEMY_CLASS_ALIEN
                    alignment_id = MISSION_ALIGNMENT_HERO
                    key_prefix = "EA"
                elif clear.mission_object_name == "Soldier":
                    clear_class = ENEMY_CLASS_GUN
                    alignment_id = MISSION_ALIGNMENT_DARK
                    key_prefix = "EG"

                if clear_class is not None:
                    aliens = [ r for r in related_es if r.enemyClass == clear_class ]
                    if len(aliens) == 0:
                        continue

                    aliens = aliens[0]

                    max_required_complete = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION, clear.mission_object_name, self.options),
                                   clear.requirement_count, clear.stageId, clear.alignmentId,
                                       override_settings)


                    #override_total_complete = ShadowUtils.getOverwriteRequiredCount(override_settings, stage,
                     #                                                      alignment_id, ShadowUtils.TYPE_ID_COMPLETION)
                    #max_required_complete = ShadowUtils.getRequiredCount(clear.requirement_count, objective_percentage,
                    #                                            override=override_total_complete, round_method=floor)

                    d_count = aliens.total_count - max_required_complete

                    if d_count > 0:

                        max_required = ShadowUtils.getMaxRequired(
                            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                                      clear.mission_object_name, self.options),
                            aliens.total_count, stage, alignment_id,
                            override_settings)

                        if max_required > max_required_complete:
                            key = key_prefix + "." + Levels.LEVEL_ID_TO_LEVEL[stage]
                            override_settings.value[key] = (max_required_complete * 100) / aliens.total_count
                            print("Had to adjust key for {key}".format(key=key))
    def generate_early(self):
        self.check_invalid_configurations()

        # Set maximum of levels required
        # Exclude missions listed in exclude_locations
        maximum_force_missions = self.options.force_objective_sanity_max.value
        maximum_force_mission_counter = self.options.force_objective_sanity_max_counter.value

        mission_counter = 0
        mission_total = 0

        Regions.early_region_checks(self)

        item_count = Items.CountItems(self) - self.options.starting_stages
        location_count = Locations.count_locations(self)

        if self.options.objective_item_percentage_available < self.options.objective_completion_percentage:
            raise OptionError("Invalid available percentage versus requirement")

        if self.options.objective_completion_enemy_percentage < self.options.objective_completion_enemy_percentage:
            raise OptionError("Invalid available enemy percentage versus requirement")

        # TODO: Check all options don't contradict one another from percent_overrides

        if self.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_minimise:
            if item_count > location_count:
                print("item_count=", item_count, "location_count=", location_count)
                potential_downgrades, removals = GetPotentialDowngradeItems(self)
                if len(potential_downgrades) < item_count - location_count - len(removals):
                    c = item_count - location_count - len(potential_downgrades)
                    raise OptionError("Not enough locations to fill even with downgrades::"+str(c))
                self.excess_item_count = item_count - location_count

        elif self.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_off and \
            location_count < item_count:
            raise OptionError("Invalid count of items present:"+str(location_count)+" vs "+str(item_count))

        for missionClear in Locations.MissionClearLocations:

            if missionClear.requirement_count is None:
                continue

            max_required_objective = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                          missionClear.mission_object_name, self.options),
                missionClear.requirement_count, missionClear.stageId, missionClear.alignmentId,
                self.options.percent_overrides)

            max_required_available = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                          missionClear.mission_object_name, self.options),
                missionClear.requirement_count, missionClear.stageId, missionClear.alignmentId,
                self.options.percent_overrides)

            max_required_completion = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                          missionClear.mission_object_name, self.options),
                missionClear.requirement_count, missionClear.stageId, missionClear.alignmentId,
                self.options.percent_overrides)

            if max_required_objective > missionClear.requirement_count and not self.options.allow_dangerous_settings:
                raise OptionError("Dangerous objective value set!")

            if max_required_available < max_required_completion:
                raise OptionError(f"Stage specific variables uncompletable for stage:{Levels.LEVEL_ID_TO_LEVEL[missionClear.stageId]}"
                                  f"with {max_required_available} and {max_required_completion}")

        for enemy in Locations.EnemySanityLocations:
            max_required_enemy = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, self.options),
                enemy.total_count, enemy.stageId, enemy.enemyClass, self.options.percent_overrides)

            if max_required_enemy > enemy.total_count and not self.options.allow_dangerous_settings:
                raise OptionError("Dangerous enemy value set!")

        if not self.options.objective_sanity.value and self.options.enemy_sanity:
            self.calculate_object_discrepancies()

        if self.options.objective_sanity.value and self.options.force_objective_sanity_chance > 0\
                and self.options.force_objective_sanity_max > 0:
            for locationData in Locations.MissionClearLocations:
                if locationData.requirement_count is None:
                    continue
                if locationData.requirement_count == 1:
                    continue
                if mission_counter >= maximum_force_missions:
                    continue
                if locationData.requirement_count + mission_total > maximum_force_mission_counter:
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

        if self.options.level_progression != self.options.level_progression.option_story:
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
            "check_level": None if len(self.first_regions) == 0 else self.first_regions[0],
            "first_levels": self.first_regions,

            "objective_sanity": self.options.objective_sanity.value,
            "objective_percentage": self.options.objective_percentage.value,
            "objective_enemy_percentage": self.options.objective_enemy_percentage.value,
            "objective_completion_percentage": self.options.objective_completion_percentage.value,
            "objective_completion_enemy_percentage": self.options.objective_completion_enemy_percentage.value,
            "objective_item_percentage_available": self.options.objective_item_percentage_available.value,
            "objective_item_enemy_percentage_available": self.options.objective_item_enemy_percentage_available.value,
            "enemy_sanity_percentage": self.options.enemy_sanity_percentage.value,

            "checkpoint_sanity": self.options.checkpoint_sanity.value,
            "character_sanity": self.options.character_sanity.value,

            "required_mission_tokens": self.required_tokens[Items.Progression.StandardMissionToken],
            "required_hero_tokens": self.required_tokens[Items.Progression.StandardHeroToken],
            "required_dark_tokens": self.required_tokens[Items.Progression.StandardDarkToken],
            "required_final_tokens": self.required_tokens[Items.Progression.FinalToken],
            "required_objective_tokens": self.required_tokens[Items.Progression.ObjectiveToken],
            "requires_emeralds": self.options.goal_chaos_emeralds.value,
            "key_sanity": self.options.key_sanity.value,
            "enemy_sanity": self.options.enemy_sanity.value,
            "objective_enemy_sanity": self.options.enemy_objective_sanity.value,
            "weapon_sanity_unlock": self.options.weapon_sanity_unlock.value,
            "weapon_sanity_hold": self.options.weapon_sanity_hold.value,
            "vehicle_logic": self.options.vehicle_logic.value,
            "ring_link": self.options.ring_link.value,
            "auto_clear_missions": self.options.auto_clear_missions.value,
            "story_mode_available": self.options.level_progression != Options.LevelProgression.option_select,
            "select_mode_available": self.options.level_progression != Options.LevelProgression.option_story,
            "required_client_version": ShadowUtils.GetVersionString(),
            "override_settings": self.options.percent_overrides.value,
        }

        return slot_data
