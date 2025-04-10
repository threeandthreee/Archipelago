import random
from typing import ClassVar, Tuple, Any
from BaseClasses import  Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .Levels import GetLevelCompletionNames
from .Items import *
from .Locations import *

from . import Options, Rules, Regions, Utils as ShadowUtils, Story
from .Options import shadow_option_groups, PercentOverrides, AutoClearMissions


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
    theme = "dirt"

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

    option_groups = shadow_option_groups

class ShtHWorld(World):
    """
        Shadow The Hedgehog (also known as Shadow 05) allows the player to play through 23 stages
        with the ultimate lifeform, tracking down the answers to his past.
        But this time, it seems the past makes even less sense as nothing appears to be what it seems!
        Help Shadow find the truth and put a stop the his cursed past from coming back to haunt him!
    """
    #options_dataclass = ShThOptions
    #options: ShThOptions

    game: ClassVar[str] = "Shadow The Hedgehog"
    topology_present: bool = True

    item_name_to_id: ClassVar[Dict[str, int]] = Items.GetItemDict()
    location_name_to_id: ClassVar[Dict[str, int]] = Locations.GetLocationDict()

    required_client_version: Tuple[int, int, int] = (0, 5, 1)
    web = ShtHWebWorld()

    options_dataclass = Options.ShadowTheHedgehogOptions
    options: Options.ShadowTheHedgehogOptions

    item_name_groups = Items.get_item_groups()

    location_name_groups = Locations.getLocationGroups()



    def reinitialise(self):
        self.first_regions = []
        self.available_characters = []
        self.available_weapons = []
        self.available_levels = []
        self.token_locations = []
        self.required_tokens = {}
        self.excess_item_count = 0
        self.shuffled_story_mode = None
        self.random_value = None

        for token in TOKENS:
            self.required_tokens[token] = 0

    def __init__(self, *args, **kwargs):
        self.reinitialise()

        super(ShtHWorld, self).__init__(*args, **kwargs)

    def set_rules(self):
        Rules.set_rules(self.multiworld, self, self.player)

    def check_invalid_configurations(self):
        if self.options.auto_clear_missions and not self.options.objective_sanity or \
            (self.options.objective_sanity and not self.options.enemy_objective_sanity):
            print("Shadow Auto clear has been disabled")
            self.options.auto_clear_missions = AutoClearMissions(False)

        if (self.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked
                and not self.options.weapon_sanity_unlock):
            raise OptionError("Cannot use unlock mode for weapons without weaponsanity lock.")

        if self.options.level_progression == Options.LevelProgression.option_select and \
            self.options.starting_stages == 0:
            raise OptionError("Cannot start select mode with 0 starting stages")

        if self.options.shadow_mod.value != Options.ShadowMod.option_vanilla and\
            self.options.character_sanity:
            raise OptionError("Unable to play charactersanity outside of vanilla")

        if self.options.shadow_mod.value == Options.ShadowMod.option_reloaded and \
            self.options.key_sanity:
            raise OptionError("Key/RSR sanity not supported in Reloaded at this time.")

    def calculate_object_discrepancies(self):

        if type(self.options.percent_overrides) == PercentOverrides:
            override_settings = self.options.percent_overrides.value
        else:
            override_settings = self.options.percent_overrides

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
                            override_settings[key] = (max_required_complete * 100) / aliens.total_count
                            #print("Had to adjust key for {key}".format(key=key))
    def generate_early(self):
        random_bytes = self.generate_random_bytes()
        self.random_value = int.from_bytes(random_bytes, byteorder='big')
        self.check_invalid_configurations()

        if self.options.level_progression != Options.LevelProgression.option_select:
            self.shuffled_story_mode = Story.GetStoryMode(self)

            # TODO: Handle this / overwrite this with UT, check validity
            if self.options.story_progression_balancing > 0 and not hasattr(self.multiworld, "re_gen_passthrough"):
                story_spheres = Story.DecideStoryPath(self, self.shuffled_story_mode)
                #print("Story Spheres", [ (s[0].stageId, s[0].alignmentId) if s[0] is not None else "Start"
                #                         for s in story_spheres])
                new_overrides = Story.AlterOverridesForStoryPath(story_spheres, self.options.percent_overrides.value)

                for override in new_overrides.items():
                    self.options.percent_overrides.value[override[0]] = override[1]
            #elif hasattr(self.multiworld, "re_gen_passthrough"):
            #    print("o=", self.options.percent_overrides)

        else:
            self.shuffled_story_mode = Story.DefaultStoryMode

        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Shadow The Hedgehog" in self.multiworld.re_gen_passthrough:
                self.reinitialise()
                passthrough = self.multiworld.re_gen_passthrough["Shadow The Hedgehog"]

                if "objective_sanity" in passthrough:
                    self.options.objective_sanity = passthrough["objective_sanity"]

                if "objective_percentage" in passthrough:
                    self.options.objective_percentage = passthrough["objective_percentage"]

                if "objective_enemy_percentage" in passthrough:
                    self.options.objective_enemy_percentage = passthrough["objective_enemy_percentage"]

                if "objective_completion_percentage" in passthrough:
                    self.options.objective_completion_percentage = passthrough["objective_completion_percentage"]

                if "objective_percentage" in passthrough:
                    self.options.objective_percentage = passthrough["objective_percentage"]

                if "objective_enemy_percentage" in passthrough:
                    self.options.objective_enemy_percentage = passthrough["objective_enemy_percentage"]

                if "objective_completion_enemy_percentage" in passthrough:
                    self.options.objective_completion_enemy_percentage = passthrough["objective_completion_enemy_percentage"]

                if "objective_item_percentage_available" in passthrough:
                    self.options.objective_item_percentage_available = passthrough["objective_item_percentage_available"]

                if "objective_item_enemy_percentage_available" in passthrough:
                    self.options.objective_item_enemy_percentage_available = passthrough["objective_item_enemy_percentage_available"]

                if "enemy_sanity_percentage" in passthrough:
                    self.options.enemy_sanity_percentage = passthrough["enemy_sanity_percentage"]

                if "checkpoint_sanity" in passthrough:
                    self.options.checkpoint_sanity = passthrough["checkpoint_sanity"]

                if "character_sanity" in passthrough:
                    self.options.character_sanity = passthrough["character_sanity"]

                if "required_mission_tokens" in passthrough:
                    self.options.required_mission_tokens = passthrough["required_mission_tokens"]

                if "required_hero_tokens" in passthrough:
                    self.options.required_hero_tokens = passthrough["required_hero_tokens"]

                if "required_dark_tokens" in passthrough:
                    self.options.required_dark_tokens = passthrough["required_dark_tokens"]

                if "required_final_tokens" in passthrough:
                    self.options.required_final_tokens = passthrough["required_final_tokens"]

                if "required_boss_tokens" in passthrough:
                    self.options.required_boss_tokens = passthrough["required_boss_tokens"]

                if "required_final_boss_tokens" in passthrough:
                    self.options.required_final_boss_tokens = passthrough["required_final_boss_tokens"]

                if "objective_completion_percentage" in passthrough:
                    self.options.objective_completion_percentage = passthrough["objective_completion_percentage"]

                if "requires_emeralds" in passthrough:
                    self.options.requires_emeralds = passthrough["requires_emeralds"]

                if "key_sanity" in passthrough:
                    self.options.key_sanity = passthrough["key_sanity"]

                if "enemy_sanity" in passthrough:
                    self.options.enemy_sanity = passthrough["enemy_sanity"]

                if "objective_enemy_sanity" in passthrough:
                    self.options.objective_enemy_sanity = passthrough["objective_enemy_sanity"]

                if "weapon_sanity_unlock" in passthrough:
                    self.options.weapon_sanity_unlock = passthrough["weapon_sanity_unlock"]

                if "weapon_sanity_hold" in passthrough:
                    self.options.weapon_sanity_hold = passthrough["weapon_sanity_hold"]

                if "vehicle_logic" in passthrough:
                    self.options.vehicle_logic = passthrough["vehicle_logic"]

                if "override_settings" in passthrough:
                    print("override=", passthrough["override_settings"])
                    self.options.percent_overrides = passthrough["override_settings"]

                if "level_progression" in passthrough:
                    self.options.level_progression = passthrough["level_progression"]

                if "excluded_stages" in passthrough:
                    self.options.excluded_stages = passthrough["excluded_stages"]

                if "logic_level" in passthrough:
                    self.options.logic_level = passthrough["logic_level"]

                if "include_last_way_shuffle" in passthrough:
                    self.options.include_last_way_shuffle = passthrough["include_last_way_shuffle"]

                if "story_boss_count" in passthrough:
                    self.options.story_boss_count = passthrough["story_boss_count"]

                if "story_shuffle" in passthrough:
                    self.options.story_shuffle = passthrough["story_shuffle"]

                if "select_bosses" in passthrough:
                    self.options.select_bosses = passthrough["select_bosses"]

                if "minimum_rank" in passthrough:
                    self.options.minimum_rank = passthrough["minimum_rank"]

                if "enemy_frequency" in passthrough:
                    self.options.enemy_frequency = passthrough["enemy_frequency"]

                if "objective_frequency" in passthrough:
                    self.options.objective_frequency = passthrough["objective_frequency"]

                if "enemy_objective_frequency" in passthrough:
                    self.options.enemy_objective_frequency = passthrough["enemy_objective_frequency"]

                if "secret_story_progression" in passthrough:
                    self.options.secret_story_progression = passthrough["secret_story_progression"]

                if "goal_missions" in passthrough:
                    self.options.goal_missions = passthrough["goal_missions"]

                if "goal_final_missions" in passthrough:
                    self.options.goal_final_missions = passthrough["goal_final_missions"]

                if "goal_hero_missions" in passthrough:
                    self.options.goal_hero_missions = passthrough["goal_hero_missions"]

                if "goal_dark_missions" in passthrough:
                    self.options.goal_dark_missions = passthrough["goal_dark_missions"]

                if "goal_objective_missions" in passthrough:
                    self.options.goal_objective_missions = passthrough["goal_objective_missions"]

                if "goal_bosses" in passthrough:
                    self.options.goal_bosses = passthrough["goal_bosses"]

                if "goal_final_bosses" in passthrough:
                    self.options.goal_final_bosses = passthrough["goal_final_bosses"]

                if "shuffled_story_mode" in passthrough:
                    self.shuffled_story_mode = Story.StringToStory(passthrough["shuffled_story_mode"])

                if "shadow_mod" in passthrough:
                    self.options.shadow_mod = passthrough["shadow_mod"]

                if "weapon_groups" in passthrough:
                    self.options.weapon_groups = passthrough["weapon_groups"]

                if "single_egg_dealer" in passthrough:
                    self.options.single_egg_dealer = passthrough["single_egg_dealer"]

                if "single_black_doom" in passthrough:
                    self.options.single_black_doom = passthrough["single_black_doom"]

                if "single_diablon" in passthrough:
                    self.options.single_diablon = passthrough["single_diablon"]

                if "boss_logic_level" in passthrough:
                    self.options.boss_logic_level = passthrough["boss_logic_level"]

                if "craft_logic_level" in passthrough:
                    self.options.craft_logic_level = passthrough["craft_logic_level"]

                if "guaranteed_level_clear" in passthrough:
                    self.options.guaranteed_level_clear = passthrough["guaranteed_level_clear"]

        # Set maximum of levels required
        # Exclude missions listed in exclude_locations
        maximum_force_missions = self.options.force_objective_sanity_max.value
        maximum_force_mission_counter = self.options.force_objective_sanity_max_counter.value

        mission_counter = 0
        mission_total = 0

        Regions.early_region_checks(self)

        item_count = Items.CountItems(self)
        location_count = Locations.count_locations(self)

        if self.options.objective_item_percentage_available < self.options.objective_completion_percentage:
            raise OptionError("Invalid available percentage versus requirement")

        if self.options.objective_completion_enemy_percentage < self.options.objective_completion_enemy_percentage:
            raise OptionError("Invalid available enemy percentage versus requirement")

        # TODO: Check all options don't contradict one another from percent_overrides

        if self.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_minimise:
            if item_count > location_count:
                #print("item_count=", item_count, "location_count=", location_count)
                potential_downgrades, removals = GetPotentialDowngradeItems(self)
                if len(potential_downgrades) < item_count - location_count - len(removals):
                    c = item_count - location_count - len(potential_downgrades)
                    print("Issue with counts", item_count, location_count, len(potential_downgrades), c)
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

        if not self.options.objective_sanity and self.options.enemy_sanity:
            self.calculate_object_discrepancies()

        if self.options.objective_sanity and self.options.force_objective_sanity_chance > 0\
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
                if r > 100 - self.options.force_objective_sanity_chance:
                    #print("Make priority location:", completion_location_name)
                    self.options.priority_locations.value.add(completion_location_name)
                    mission_counter += 1
                    mission_total += locationData.requirement_count


    def create_regions(self):
        regions = Regions.create_regions(self)
        Locations.create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        if self.options.level_progression != Options.LevelProgression.option_story:
            for first_region in self.first_regions:
                stage_item = Items.GetStageUnlockItem(first_region)
                self.options.start_inventory.value[stage_item] = 1
                self.multiworld.push_precollected(self.create_item(stage_item))



    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER

        if "shuffled_story_mode" in slot_data:
            pass
            #self.shuffled_story_mode = Story.StringToStory(slot_data["shuffled_story_mode"])

        return slot_data

    def create_item(self, name: str) -> "ShadowTheHedgehogItem":
        info = Items.GetItemByName(name)
        return ShadowTheHedgehogItem(info, self.player)

    def create_items(self):
        Items.PopulateItemPool(self, self.first_regions)

    def get_filler_item_name(self) -> str:
        # Use the same weights for filler items that are used in the base randomizer.
        item_info = Items.ChooseJunkItems(self.random, Items.GetJunkItemInfo(), self.options, 1)[0]
        return item_info.name


    def get_pre_fill_items(self):
        res = []

        return res

    def generate_random_bytes(self):
        return self.multiworld.random.randbytes(8)

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
            "required_boss_tokens": self.required_tokens[Items.Progression.BossToken],
            "required_final_boss_tokens": self.required_tokens[Items.Progression.FinalBossToken],
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
            "shuffled_story_mode": Story.StoryToString(self.shuffled_story_mode),
            "level_progression": self.options.level_progression.value,
            "excluded_stages": self.options.excluded_stages.value,
            "logic_level": self.options.logic_level.value,
            "enable_gauge_items": self.options.enable_gauge_items.value,
            "exceeding_items_filler": self.options.exceeding_items_filler.value,
            "include_last_way_shuffle": self.options.include_last_way_shuffle.value,
            "story_shuffle": self.options.story_shuffle.value,
            "story_boss_count": self.options.story_boss_count.value,
            "secret_story_progression": self.options.secret_story_progression.value,
            "select_bosses": self.options.select_bosses.value,
            "minimum_rank": self.options.minimum_rank.value,
            "enemy_frequency": self.options.enemy_frequency.value,
            "objective_frequency": self.options.objective_frequency.value,
            "enemy_objective_frequency": self.options.enemy_objective_frequency.value,
            "goal_missions": self.options.goal_missions.value,
            "goal_final_missions": self.options.goal_final_missions.value,
            "goal_hero_missions": self.options.goal_hero_missions.value,
            "goal_dark_missions": self.options.goal_dark_missions.value,
            "goal_objective_missions": self.options.goal_objective_missions.value,
            "goal_bosses": self.options.goal_bosses.value,
            "goal_final_bosses": self.options.goal_final_bosses.value,
            "shadow_mod": self.options.shadow_mod.value,
            "weapon_groups": self.options.weapon_groups.value,
            "single_egg_dealer": self.options.single_egg_dealer.value,
            "single_black_doom": self.options.single_black_doom.value,
            "single_diablon": self.options.single_diablon.value,
            "boss_logic_level": self.options.boss_logic_level.value,
            "craft_logic_level": self.options.craft_logic_level.value,
            "guaranteed_level_clear": self.options.guaranteed_level_clear.value,
            "save_value": self.random_value

        }
        return slot_data

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        if self.options.story_shuffle != Options.StoryShuffle.option_off:
            spoiler_handle.write(f"{self.multiworld.get_player_name(self.player)}'s Shuffled Story Path\n")
            for stage in self.shuffled_story_mode:
                text = str(stage)
                spoiler_handle.writelines(text)
            spoiler_handle.write("\n")

