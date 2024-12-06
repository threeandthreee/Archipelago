import typing
from typing import Dict, Any

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .CharacterUtils import get_playable_characters
from .Enums import Character, SADX_BASE_ID, Area, remove_character_suffix, pascal_to_space
from .ItemPool import create_sadx_items, get_item_names, ItemDistribution
from .Items import SonicAdventureDXItem, group_item_table, item_name_to_info
from .Locations import all_location_table, group_location_table
from .Names import ItemName, LocationName
from .Options import sadx_option_groups, SonicAdventureDXOptions
from .Regions import create_sadx_regions, get_location_ids_for_area
from .Rules import create_sadx_rules, LocationDistribution
from .StartingSetup import StarterSetup, generate_early_sadx, write_sadx_spoiler, CharacterArea, level_areas


class SonicAdventureDXWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Sonic Adventure DX randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["ClassicSpeed"]
    )]
    option_groups = sadx_option_groups


class SonicAdventureDXWorld(World):
    game = "Sonic Adventure DX"
    web = SonicAdventureDXWeb()
    starter_setup: StarterSetup = StarterSetup()
    item_distribution: ItemDistribution = ItemDistribution()
    location_distribution: LocationDistribution = LocationDistribution()

    item_name_to_id = {item.name: item.itemId + SADX_BASE_ID for item in item_name_to_info.values()}
    location_name_to_id = {loc["name"]: loc["id"] + SADX_BASE_ID for loc in all_location_table}

    item_name_groups = group_item_table
    location_name_groups = group_location_table

    options_dataclass = SonicAdventureDXOptions
    options: SonicAdventureDXOptions

    tracker_world = {"map_page_folder": "tracker", "map_page_maps": "maps/maps.json",
                     "map_page_locations": "locations/locations.json"}

    def generate_early(self):
        self.starter_setup = generate_early_sadx(self, self.options)
        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Sonic Adventure DX" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Sonic Adventure DX"]
                self.starter_setup.character = Character(passthrough["StartingCharacter"])
                self.starter_setup.item = passthrough["StartingItem"]
                self.starter_setup.area = Area(passthrough["StartingArea"])
                self.starter_setup.charactersWithArea = [
                    CharacterArea(Character.Sonic, Area(passthrough["SonicStartingArea"])),
                    CharacterArea(Character.Tails, Area(passthrough["TailsStartingArea"])),
                    CharacterArea(Character.Knuckles, Area(passthrough["KnucklesStartingArea"])),
                    CharacterArea(Character.Amy, Area(passthrough["AmyStartingArea"])),
                    CharacterArea(Character.Gamma, Area(passthrough["GammaStartingArea"])),
                    CharacterArea(Character.Big, Area(passthrough["BigStartingArea"]))

                ]
                self.starter_setup.level_mapping = {Area(int(original)): Area(int(randomized))
                                                    for original, randomized in passthrough["LevelEntranceMap"].items()}

                # Options synchronization, needed for weighted values
                self.options.goal_requires_levels.value = passthrough["GoalRequiresLevels"]
                self.options.levels_percentage.value = passthrough["LevelsPercentage"]
                self.options.goal_requires_chaos_emeralds.value = passthrough["GoalRequiresChaosEmeralds"]
                self.options.goal_requires_emblems.value = passthrough["GoalRequiresEmblems"]
                self.options.emblems_percentage.value = passthrough["EmblemsPercentage"]
                self.options.goal_requires_missions.value = passthrough["GoalRequiresMissions"]
                self.options.mission_percentage.value = passthrough["MissionsPercentage"]
                self.options.goal_requires_bosses.value = passthrough["GoalRequiresBosses"]
                self.options.goal_requires_chao_races.value = passthrough["GoalRequiresChaoRaces"]
                self.options.logic_level.value = passthrough["LogicLevel"]
                self.options.entrance_randomizer.value = passthrough["EntranceRandomizer"]

                self.options.playable_sonic.value = passthrough["PlayableSonic"]
                self.options.playable_tails.value = passthrough["PlayableTails"]
                self.options.playable_knuckles.value = passthrough["PlayableKnuckles"]
                self.options.playable_amy.value = passthrough["PlayableAmy"]
                self.options.playable_big.value = passthrough["PlayableBig"]
                self.options.playable_gamma.value = passthrough["PlayableGamma"]

                self.options.sonic_action_stage_missions.value = passthrough["SonicActionStageMissions"]
                self.options.tails_action_stage_missions.value = passthrough["TailsActionStageMissions"]
                self.options.knuckles_action_stage_missions.value = passthrough["KnucklesActionStageMissions"]
                self.options.amy_action_stage_missions.value = passthrough["AmyActionStageMissions"]
                self.options.gamma_action_stage_missions.value = passthrough["GammaActionStageMissions"]
                self.options.big_action_stage_missions.value = passthrough["BigActionStageMissions"]

                self.options.randomized_sonic_upgrades.value = passthrough["RandomizedSonicUpgrades"]
                self.options.randomized_tails_upgrades.value = passthrough["RandomizedTailsUpgrades"]
                self.options.randomized_knuckles_upgrades.value = passthrough["RandomizedKnucklesUpgrades"]
                self.options.randomized_amy_upgrades.value = passthrough["RandomizedAmyUpgrades"]
                self.options.randomized_big_upgrades.value = passthrough["RandomizedGammaUpgrades"]
                self.options.randomized_gamma_upgrades.value = passthrough["RandomizedBigUpgrades"]

                self.options.boss_checks.value = passthrough["BossChecks"]
                self.options.unify_chaos4.value = passthrough["UnifyChaos4"]
                self.options.unify_chaos6.value = passthrough["UnifyChaos6"]
                self.options.unify_egg_hornet.value = passthrough["UnifyEggHornet"]

                self.options.field_emblems_checks.value = passthrough["FieldEmblemChecks"]
                self.options.random_starting_location.value = passthrough["RandomStartingLocation"]
                self.options.random_starting_location_per_character.value = passthrough["RandomStartingLocationPerCharacter"]
                self.options.guaranteed_level.value = passthrough["GuaranteedLevel"]
                self.options.guaranteed_starting_checks.value = passthrough["GuaranteedStartingChecks"]

                self.options.chao_egg_checks.value = passthrough["SecretChaoEggs"]
                self.options.chao_races_checks.value = passthrough["ChaoRacesChecks"]
                self.options.chao_races_levels_to_access_percentage.value = passthrough["ChaoRacesLevelsToAccessPercentage"]
                self.options.mission_mode_checks.value = passthrough["MissionModeChecks"]
                self.options.auto_start_missions.value = passthrough["AutoStartMissions"]

                self.options.sub_level_checks.value = passthrough["SubLevelChecks"]
                self.options.sub_level_checks_hard.value = passthrough["SubLevelChecksHard"]
                self.options.sky_chase_checks.value = passthrough["SkyChaseChecks"]
                self.options.sky_chase_checks_hard.value = passthrough["SkyChaseChecksHard"]

                self.options.life_sanity.value = passthrough["LifeSanity"]
                self.options.pinball_life_capsules.value = passthrough["PinballLifeCapsules"]
                self.options.sonic_life_sanity.value = passthrough["SonicLifeSanity"]
                self.options.tails_life_sanity.value = passthrough["TailsLifeSanity"]
                self.options.knuckles_life_sanity.value = passthrough["KnucklesLifeSanity"]
                self.options.amy_life_sanity.value = passthrough["AmyLifeSanity"]
                self.options.big_life_sanity.value = passthrough["BigLifeSanity"]
                self.options.gamma_life_sanity.value = passthrough["GammaLifeSanity"]

    # For the universal tracker, doesn't get called in standard gen
    # Returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    def create_item(self, name: str) -> SonicAdventureDXItem:
        return SonicAdventureDXItem(name, self.player)

    def create_regions(self) -> None:
        create_sadx_regions(self, self.starter_setup, self.options)

    def create_items(self):
        self.item_distribution = create_sadx_items(self, self.starter_setup, self.options)

    def set_rules(self):
        self.location_distribution = create_sadx_rules(self, self.item_distribution.emblem_count_progressive)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        write_sadx_spoiler(self, spoiler_handle, self.starter_setup, self.options)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if not self.options.entrance_randomizer:
            return

        sadx_hint_data = {}
        level_area_strings = [pascal_to_space(area.name) + " (" for area in level_areas]
        # Add level entrance hints if entrance randomizer is on
        for location in self.multiworld.get_locations(self.player):
            if any(location.parent_region.name.startswith(area_string) for area_string in level_area_strings):
                sadx_hint_data[location.address] = remove_character_suffix(location.parent_region.entrances[0].name)

        hint_data[self.player] = sadx_hint_data

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "ModVersion": 90,
            "GoalRequiresLevels": self.options.goal_requires_levels.value,
            "LevelsPercentage": self.options.levels_percentage.value,
            "GoalRequiresChaosEmeralds": self.options.goal_requires_chaos_emeralds.value,
            "GoalRequiresEmblems": self.options.goal_requires_emblems.value,
            "EmblemsPercentage": self.options.emblems_percentage.value,
            "GoalRequiresMissions": self.options.goal_requires_missions.value,
            "MissionsPercentage": self.options.mission_percentage.value,
            "GoalRequiresBosses": self.options.goal_requires_bosses.value,
            "GoalRequiresChaoRaces": self.options.goal_requires_chao_races.value,
            "LogicLevel": self.options.logic_level.value,
            "EmblemsForPerfectChaos": self.item_distribution.emblem_count_progressive,
            "LevelForPerfectChaos": self.location_distribution.levels_for_perfect_chaos,
            "MissionForPerfectChaos": self.location_distribution.missions_for_perfect_chaos,
            "BossesForPerfectChaos": self.location_distribution.bosses_for_perfect_chaos,
            "StartingCharacter": self.starter_setup.character.value,
            "StartingItem": self.starter_setup.item,
            "StartingArea": self.starter_setup.area.value,
            "SonicStartingArea": self.starter_setup.get_starting_area(Character.Sonic).value,
            "TailsStartingArea": self.starter_setup.get_starting_area(Character.Tails).value,
            "KnucklesStartingArea": self.starter_setup.get_starting_area(Character.Knuckles).value,
            "AmyStartingArea": self.starter_setup.get_starting_area(Character.Amy).value,
            "GammaStartingArea": self.starter_setup.get_starting_area(Character.Gamma).value,
            "BigStartingArea": self.starter_setup.get_starting_area(Character.Big).value,
            "EntranceRandomizer": self.options.entrance_randomizer.value,
            "LevelEntranceMap": {original.value: randomized.value for original, randomized in
                                 self.starter_setup.level_mapping.items()},

            "RandomStartingLocation": self.options.random_starting_location.value,
            "RandomStartingLocationPerCharacter": self.options.random_starting_location_per_character.value,
            "GuaranteedLevel": self.options.guaranteed_level.value,
            "GuaranteedStartingChecks": self.options.guaranteed_starting_checks.value,
            "FieldEmblemChecks": self.options.field_emblems_checks.value,
            "SecretChaoEggs": self.options.chao_egg_checks.value,
            "ChaoRacesChecks": self.options.chao_races_checks.value,
            "ChaoRacesLevelsToAccessPercentage": self.options.chao_races_levels_to_access_percentage.value,
            "MissionModeChecks": self.options.mission_mode_checks.value,
            "AutoStartMissions": self.options.auto_start_missions.value,
            "MissionBlackList": {int(mission): int(mission) for mission in self.options.mission_blacklist.value},

            "LifeSanity": self.options.life_sanity.value,
            "PinballLifeCapsules": self.options.pinball_life_capsules.value,
            "SonicLifeSanity": self.options.sonic_life_sanity.value,
            "TailsLifeSanity": self.options.tails_life_sanity.value,
            "KnucklesLifeSanity": self.options.knuckles_life_sanity.value,
            "AmyLifeSanity": self.options.amy_life_sanity.value,
            "BigLifeSanity": self.options.big_life_sanity.value,
            "GammaLifeSanity": self.options.gamma_life_sanity.value,

            "DeathLink": self.options.death_link.value,
            "SendDeathLinkChance": self.options.send_death_link_chance.value,
            "ReceiveDeathLinkChance": self.options.receive_death_link_chance.value,
            "RingLink": self.options.ring_link.value,
            "CasinopolisRingLink": self.options.casinopolis_ring_link.value,
            "HardRingLink": self.options.hard_ring_link.value,
            "RingLoss": self.options.ring_loss.value,
            "SubLevelChecks": self.options.sub_level_checks.value,
            "SubLevelChecksHard": self.options.sub_level_checks_hard.value,
            "SkyChaseChecks": self.options.sky_chase_checks.value,
            "SkyChaseChecksHard": self.options.sky_chase_checks_hard.value,

            "BossChecks": self.options.boss_checks.value,
            "UnifyChaos4": self.options.unify_chaos4.value,
            "UnifyChaos6": self.options.unify_chaos6.value,
            "UnifyEggHornet": self.options.unify_egg_hornet.value,

            "RandomizedSonicUpgrades": self.options.randomized_sonic_upgrades.value,
            "RandomizedTailsUpgrades": self.options.randomized_tails_upgrades.value,
            "RandomizedKnucklesUpgrades": self.options.randomized_knuckles_upgrades.value,
            "RandomizedAmyUpgrades": self.options.randomized_amy_upgrades.value,
            "RandomizedGammaUpgrades": self.options.randomized_big_upgrades.value,
            "RandomizedBigUpgrades": self.options.randomized_gamma_upgrades.value,

            "PlayableSonic": self.options.playable_sonic.value,
            "PlayableTails": self.options.playable_tails.value,
            "PlayableKnuckles": self.options.playable_knuckles.value,
            "PlayableAmy": self.options.playable_amy.value,
            "PlayableBig": self.options.playable_big.value,
            "PlayableGamma": self.options.playable_gamma.value,

            "SonicActionStageMissions": self.options.sonic_action_stage_missions.value,
            "TailsActionStageMissions": self.options.tails_action_stage_missions.value,
            "KnucklesActionStageMissions": self.options.knuckles_action_stage_missions.value,
            "AmyActionStageMissions": self.options.amy_action_stage_missions.value,
            "GammaActionStageMissions": self.options.gamma_action_stage_missions.value,
            "BigActionStageMissions": self.options.big_action_stage_missions.value,

            "JunkFillPercentage": self.options.junk_fill_percentage.value,

            "ReverseControlTrapDuration": self.options.reverse_trap_duration.value,
            "TrapsOnAdventureFields": self.options.traps_and_filler_on_adventure_fields.value,
            "TrapsOnBossFights": self.options.traps_and_filler_on_boss_fights.value,
            "TrapsOnPerfectChaosFight": self.options.traps_and_filler_on_perfect_chaos_fight.value

        }
