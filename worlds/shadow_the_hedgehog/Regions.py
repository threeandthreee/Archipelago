import typing
from typing import Dict

from BaseClasses import Region, Entrance, MultiWorld
from worlds.shadow_the_hedgehog import Levels
from worlds.shadow_the_hedgehog.Items import GetStageUnlockItem


def stage_id_to_region(level_id: int) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_name = "REGION_" + level_name
    return region_name


def create_regions(world: "ShTHWorld") -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    stages = Levels.ALL_STAGES

    stage_regions = []
    region_to_stage_id = {}
    for level_id in stages:
        region_name = stage_id_to_region(level_id)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        stage_regions.append(new_region)
        region_to_stage_id[new_region] = level_id

    first_regions = world.random.sample(stage_regions, 1)
    world.first_regions = [ region_to_stage_id[region] for region in first_regions]

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    for region in first_regions:
        regions["Menu"].connect(regions[region.name], "Start Game "+region.name)

    for region in stage_regions:
        if region not in first_regions:
            stage_id = region_to_stage_id[region]

            connect_name = "menu-to-stage-"+str(stage_id)
            stage_item_name = GetStageUnlockItem(stage_id)

            connect(world.player, connect_name,
                    regions["Menu"], region,
                    lambda state, si=stage_item_name: state.has(si, world.player))

    regions["FinalStory"] = Region("FinalStory", world.player, world.multiworld)
    connect(world.player, "final-story-unlock", regions["Menu"],
            regions["FinalStory"],

            #lambda state: state.has(item_name, player, count=clear.requirement_count)

            None # Replace with means for unlocking final story

            )


    return regions

def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):

    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)