import collections
import re
from dataclasses import dataclass, field
from typing import List, Optional, TextIO

from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters, are_character_upgrades_randomized, is_level_playable
from .Enums import Character, Area, SubLevel, pascal_to_space, level_areas
from .Locations import level_location_table, upgrade_location_table, sub_level_location_table, \
    field_emblem_location_table, boss_location_table, life_capsule_location_table, mission_location_table
from .Logic import area_connections
from .Names import ItemName
from .Options import SonicAdventureDXOptions


@dataclass
class CharacterArea:
    character: Character
    area: Area = None


@dataclass
class StarterSetup:
    character: Character = None
    area: Area = None
    item: str = None
    charactersWithArea: List[CharacterArea] = field(default_factory=list)
    level_mapping: dict[Area, Area] = field(default_factory=dict)

    def get_starting_area(self, character: Character) -> Area:
        for char_area in self.charactersWithArea:
            if char_area.character == character:
                return char_area.area
        return self.area


def generate_early_sadx(world: World, options: SonicAdventureDXOptions) -> StarterSetup:
    starter_setup = StarterSetup()
    possible_characters = get_playable_characters(options)
    world.random.shuffle(possible_characters)
    if not possible_characters:
        raise OptionError("SADX Error: You need at least one playable character.")

    if options.entrance_randomizer:
        fixed_areas = {Area[re.sub(r' ', '', area)]: Area[re.sub(r' ', '', dest)]
                       for area, dest in options.level_entrance_plando.items()}
        remaining_areas = [area for area in level_areas if area not in fixed_areas.values()]
        randomized_remaining_areas = world.random.sample(remaining_areas, len(remaining_areas))
        starter_setup.level_mapping = {**fixed_areas, **dict(
            zip([area for area in level_areas if area not in fixed_areas], randomized_remaining_areas))}

    valid_starting_pair = None
    for character in possible_characters:
        possible_starter_areas = get_possible_starting_areas(world, character,
                                                             starter_setup.level_mapping,
                                                             options.guaranteed_level.value == 1)
        if not options.random_starting_location:
            possible_starter_areas = {area: items for area, items in possible_starter_areas.items() if
                                      area == Area.StationSquareMain}

        areas_mixed = [(area, item) for area, items in possible_starter_areas.items() for item in items]
        areas_without_items = [pair for pair in areas_mixed if pair[1] is None]
        areas_with_items = [pair for pair in areas_mixed if pair[1] is not None]

        if areas_with_items or areas_without_items:
            valid_starting_pair = world.random.choice(areas_without_items if areas_without_items else areas_with_items)
            starter_setup.character = character
            starter_setup.area, starter_setup.item = valid_starting_pair
            break

    if not valid_starting_pair:
        raise OptionError(
            "SADX Error: Couldn't define a valid starting location (Probably a problem of low settings, guaranteed level and/or fixed starting location).")

    if options.random_starting_location_per_character and options.random_starting_location:
        used_areas = {starter_setup.area}
        starter_setup.charactersWithArea.append(CharacterArea(starter_setup.character, starter_setup.area))
        possible_areas_dict = {char: get_possible_starting_areas(world, char, starter_setup.level_mapping, False) for
                               char in
                               possible_characters}
        filtered_areas_dict = {char: list(areas_dict.keys()) for char, areas_dict in possible_areas_dict.items()}
        characters_sorted_by_areas = sorted(possible_characters, key=lambda char: len(filtered_areas_dict[char]))

        for character in characters_sorted_by_areas:
            if character == starter_setup.character:
                continue
            unused_areas = [area for area in filtered_areas_dict[character] if area not in used_areas]
            area = world.random.choice(unused_areas if unused_areas else filtered_areas_dict[character])
            used_areas.add(area)
            starter_setup.charactersWithArea.append(CharacterArea(character, area))

    return starter_setup


def get_possible_starting_areas(world, character: Character, level_mapping: dict[Area, Area], guaranteed_level: bool) -> \
        dict[Area, List[Optional[str]]]:
    possible_starting_areas = {}
    for area in {Area.StationSquareMain, Area.Station, Area.Hotel, Area.Casino, Area.TwinkleParkLobby,
                 Area.MysticRuinsMain, Area.AngelIsland, Area.Jungle, Area.EggCarrierMain}:
        possible_list_for_area = get_possible_starting_area_information(character, area, world.options, level_mapping,
                                                                        guaranteed_level)
        if possible_list_for_area:
            possible_starting_areas.update(possible_list_for_area)

    return possible_starting_areas


def get_possible_starting_area_information(character: Character, area: Area, options: SonicAdventureDXOptions,
                                           level_mapping: dict[Area, Area], guaranteed_level: bool) -> \
        dict[Area, List[Optional[str]]]:
    if guaranteed_level:
        level_with_item: dict[Area, List[Optional[str]]] = collections.defaultdict(list)
        for level in level_location_table:
            if is_level_playable(level, options) and level.levelMission == level.levelMission.C:
                actual_area_to = level.area
                if options.entrance_randomizer:
                    for level_entrance, actual_level in level_mapping.items():
                        if actual_level == level.area:
                            actual_area_to = level_entrance
                key = (character, area, actual_area_to)
                if key in area_connections and not area_connections[key][options.logic_level.value]:
                    if level.character == character:
                        if not level.get_logic_items(options):
                            level_with_item[area].append(None)
                        if len(level.get_logic_items(options)) == 1:
                            level_with_item[area].append(level.get_logic_items(options)[0])
        return level_with_item
    else:
        for level in level_location_table:
            if is_level_playable(level, options):
                actual_area_to = level.area
                if options.entrance_randomizer:
                    for level_entrance, actual_level in level_mapping.items():
                        if actual_level == level.area:
                            actual_area_to = level_entrance
                key = (character, area, actual_area_to)
                if key in area_connections and not area_connections[key][options.logic_level.value]:
                    if level.character == character and not level.get_logic_items(options):
                        return {area: [None]}

    if are_character_upgrades_randomized(character, options):
        for upgrade in upgrade_location_table:
            if upgrade.character == character and upgrade.area == area and not upgrade.get_logic_items(options):
                return {area: [None]}
    if options.sub_level_checks:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SandHill or sub_level.subLevel == SubLevel.TwinkleCircuit:
                if character in sub_level.characters and sub_level.area == area:
                    return {area: [None]}
    if options.sky_chase_checks:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SkyChaseAct1 or sub_level.subLevel == SubLevel.SkyChaseAct2:
                if character in sub_level.characters and sub_level.area == area:
                    return {area: [None]}
    if options.field_emblems_checks:
        for field_emblem in field_emblem_location_table:
            if character in field_emblem.get_logic_characters_upgrades(options) and field_emblem.area == area:
                return {area: [None]}
    if options.boss_checks:
        for boss_fight in boss_location_table:
            if character in boss_fight.characters and boss_fight.area == area:
                return {area: [None]}
    if options.life_sanity:
        for life_capsule in life_capsule_location_table:
            actual_area_to = life_capsule.area
            if options.entrance_randomizer:
                for level_entrance, actual_level in level_mapping.items():
                    if actual_level == life_capsule.area:
                        actual_area_to = level_entrance
            key = (character, area, actual_area_to)
            if key in area_connections and not area_connections[key][options.logic_level.value]:
                if life_capsule.character == character and not life_capsule.get_logic_items(
                        options):
                    return {area: [None]}
    if options.mission_mode_checks:
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if (mission.character == character and mission.cardArea == area
                    and mission.objectiveArea == area and not mission.get_logic_items(options)):
                return {area: [None]}


def write_sadx_spoiler(world: World, spoiler_handle: TextIO, starter_setup: StarterSetup,
                       options: SonicAdventureDXOptions):
    spoiler_handle.write("\n")
    header_text = f"Sonic Adventure starting setup for {world.multiworld.player_name[world.player]}:\n"
    spoiler_handle.write(header_text)

    starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', starter_setup.area.name)
    if starter_setup.item:
        text = "- Will start as {0} in the {1} area with {2}.\n"
        text = text.format(starter_setup.character.name, starting_area_name, starter_setup.item)
    else:
        text = "- Will start as {0} in the {1} area.\n"
        text = text.format(starter_setup.character.name, starting_area_name)

    for characterArea in starter_setup.charactersWithArea:
        if characterArea.character == starter_setup.character:
            continue
        starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', characterArea.area.name)
        text += "- {0} will spawn in the {1} area.\n".format(characterArea.character.name, starting_area_name)

    if options.entrance_randomizer:
        text += f"\nLevel entrances:\n"
        for original, randomized in starter_setup.level_mapping.items():
            text += f"- {pascal_to_space(original.name)} -> {pascal_to_space(randomized.name)}\n"
    spoiler_handle.writelines(text)


starting_area_items = {
    Character.Sonic: {
        Area.StationSquareMain: [ItemName.KeyItem.TwinkleParkTicket, ItemName.KeyItem.EmployeeCard],
        Area.Hotel: [],
        Area.MysticRuinsMain: [ItemName.KeyItem.WindStone],
        Area.EggCarrierMain: []
    },
    Character.Tails: {
        Area.StationSquareMain: [ItemName.KeyItem.EmployeeCard],
        Area.Casino: [],
        Area.MysticRuinsMain: [ItemName.KeyItem.WindStone],
        Area.EggCarrierMain: []
    },
    Character.Knuckles: {
        Area.StationSquareMain: [],
        Area.Casino: [],
    },
    Character.Amy: {
        Area.StationSquareMain: [ItemName.KeyItem.TwinkleParkTicket],
        Area.Jungle: [],
        Area.EggCarrierMain: []
    },
    Character.Gamma: {
        Area.StationSquareMain: [ItemName.KeyItem.HotelKeys],
        Area.Hotel: [],
        Area.MysticRuinsMain: [ItemName.KeyItem.Dynamite],
        Area.Jungle: [],
    },
    Character.Big: {
        Area.StationSquareMain: [],
        Area.Hotel: [],
        Area.EggCarrierMain: []
    }
}
