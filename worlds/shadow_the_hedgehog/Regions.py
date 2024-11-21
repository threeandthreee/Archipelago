import typing
from typing import Dict

from BaseClasses import Region, Entrance, MultiWorld
from worlds.shadow_the_hedgehog import Levels, Items


def stage_id_to_region(level_id: int) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_name = "REGION_" + level_name
    return region_name

def character_name_to_region(name):
    return "REGION_" + name

def region_name_for_character(stage_name, name):
    return name + "_in_" + stage_name


def create_regions(world: "ShtHWorld") -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    stages = Levels.ALL_STAGES

    stage_regions = []
    region_to_stage_id = {}
    for level_id in stages:
        if Levels.LEVEL_ID_TO_LEVEL[level_id] in world.options.excluded_stages:
            continue
        region_name = stage_id_to_region(level_id)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        stage_regions.append(new_region)
        region_to_stage_id[new_region] = level_id

    first_regions = world.random.sample(stage_regions, world.options.starting_stages.value)
    world.first_regions = [ region_to_stage_id[region] for region in first_regions]

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    for region in first_regions:
        regions["Menu"].connect(regions[region.name], "Start Game "+region.name)

    for region in stage_regions:
        #if region not in first_regions:
        stage_id = region_to_stage_id[region]

        connect_name = "menu-to-stage-"+str(stage_id)
        stage_item_name = Items.GetStageUnlockItem(stage_id)

        connect(world.player, connect_name,
                regions["Menu"], region,
                lambda state, si=stage_item_name: state.has(si, world.player))

    for char_name in Levels.CharacterToLevel.keys():
        levels_in = Levels.CharacterToLevel[char_name]
        levels_left = [ l for l in levels_in if Levels.LEVEL_ID_TO_LEVEL[l] not in world.options.excluded_stages ]
        if len(levels_left) == 0:
            continue

        region_name = character_name_to_region(char_name)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        world.available_characters.append(char_name)

    regions["FinalStory"] = Region("FinalStory", world.player, world.multiworld)
    connect(world.player, "final-story-unlock", regions["Menu"],
            regions["FinalStory"])


    return regions

def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):

    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)