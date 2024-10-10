from dataclasses import dataclass
from typing import Dict, Optional

from BaseClasses import Location, Region
from worlds.shadow_the_hedgehog import Regions, Levels
from worlds.shadow_the_hedgehog.Levels import *


class ShadowTheHedgehogLocation(Location):
    game: str = "Shadow The Hedgehog"

    def __init__(self, player, location_name, location_id, region):
        super().__init__(player, location_name, location_id, region)


@dataclass
class LocationInfo:
    locationId: int
    name: str
    stageId: Optional[int | None]
    alignmentId: Optional[int | None]
    count: Optional[int | None]
    total: Optional[int | None]


@dataclass
class MissionClearLocation:
    stageId: int
    alignmentId: int
    requirement_count: int
    mission_object_name: Optional[str]

MissionClearLocations = [
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_DARK, 35, "Solider"),
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_HERO, 45, "Alien"),

    MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_HERO, 1, None),
    MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_DARK, 1, None),

    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_HERO, 60, "Alien"),
    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_DARK, 5, "Temple"),

    MissionClearLocation(STAGE_LETHAL_HIGHWAY, MISSION_ALIGNMENT_DARK, 1, None),
    MissionClearLocation(STAGE_LETHAL_HIGHWAY, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_DARK, 5, "Lantern"),
    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_HERO, 2, "Cream"),

    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_DARK, 40, "Solider"),
    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_HERO, 5, "Discs"),

    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_DARK, 20, "Solider"),
    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_DARK, 5, "Big Bomb"),
    MissionClearLocation(STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_HERO, 20, "Little Bomb"),

    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_DARK, 60, "Solider"),
    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_HERO, 10, "Researcher"),

    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_DARK, 5, "Egg Ship"),
    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_HERO, 5, "Temple"),

    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_DARK, 30, "Bomb"),
    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_HERO, 4, "Terminal"),

    MissionClearLocation(STAGE_DEATH_RUINS, MISSION_ALIGNMENT_DARK, 1, None),
    MissionClearLocation(STAGE_DEATH_RUINS, MISSION_ALIGNMENT_HERO, 50, "Alien"),

    MissionClearLocation(STAGE_THE_ARK, MISSION_ALIGNMENT_DARK, 4, "Defense Unit"),
    MissionClearLocation(STAGE_THE_ARK, MISSION_ALIGNMENT_NEUTRAL, 1, None),

    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_DARK, 1, None),
    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_HERO, 35, "Alien"),

    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_DARK, 28, "Solider"),
    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_DARK, 6, "Defense Unit"),
    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_LOST_IMPACT, MISSION_ALIGNMENT_NEUTRAL, 1, None),
    MissionClearLocation(STAGE_LOST_IMPACT, MISSION_ALIGNMENT_HERO, 35, "Artifical Chaos"),

    MissionClearLocation(STAGE_GUN_FORTRESS, MISSION_ALIGNMENT_DARK, 3, "Computer"),
    MissionClearLocation(STAGE_GUN_FORTRESS, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_BLACK_COMET, MISSION_ALIGNMENT_DARK, 50, "Solider"),
    MissionClearLocation(STAGE_BLACK_COMET, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_DARK, 5, "Defense"),
    MissionClearLocation(STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_DARK, 1, None),
    MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_HERO, 1, None),

    MissionClearLocation(STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_DARK, 4, "Shield"),
    MissionClearLocation(STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_HERO, 1, None),

]

def GetStageInformation(stageId):
    missions = [m for m in MissionClearLocations if m.stageId == stageId]
    return missions


def GetAlignmentsForStage(stageId):
    missions = [ m.alignmentId for m in MissionClearLocations if m.stageId == stageId]
    return missions

def GetLocationDict():
    all_locations = GetAllLocationInfo()

    result = {}
    for location_type in all_locations:
        for location in location_type:
            result[location.name] = location.locationId

    return result

def GetAllLocationInfo():
    mission_clear_locations = []
    mission_locations = []

    for location in MissionClearLocations:
        location_id, completion_location_name = GetLevelCompletionNames(location.stageId, location.alignmentId)
        info = LocationInfo(location_id, completion_location_name,
                            stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None)
        mission_clear_locations.append(info)

        i = 0
        if location.requirement_count > 1:
            for j in range(1, location.requirement_count+1):
                i += 1
                location_id, objective_location_name = (
                    GetLevelObjectNames(location.stageId, location.alignmentId, location.mission_object_name, j))
                info = LocationInfo(location_id, objective_location_name,
                                   stageId=location.stageId, alignmentId=location.alignmentId,
                                    count=j, total=location.requirement_count)
                mission_locations.append(info)

    end_location = [LocationInfo(LOCATION_ID_PLUS+1000, Levels.DevilDoom_Name, stageId=None, alignmentId=None,
                                 total=None, count=None)]
    return mission_clear_locations, mission_locations, end_location

def create_locations(regions: Dict[str, Region], player):
    clear_locations, mission_locations, end_location = GetAllLocationInfo()

    for location in clear_locations:
        within_region = regions[Regions.stage_id_to_region(location.stageId)]
        completion_location = ShadowTheHedgehogLocation(player, location.name, location.locationId, within_region)
        within_region.locations.append(completion_location)

    for location in mission_locations:
        within_region = regions[Regions.stage_id_to_region(location.stageId)]
        completion_location = ShadowTheHedgehogLocation(player, location.name, location.locationId, within_region)
        within_region.locations.append(completion_location)

    end_region = regions["FinalStory"]
    devil_doom_location = ShadowTheHedgehogLocation(player, end_location[0].name, end_location[0].locationId, end_region)
    end_region.locations.append(devil_doom_location)

def count_locations():
    location_groups = GetAllLocationInfo()
    count = 0
    for group in location_groups:
        count += len(group)

    return count















