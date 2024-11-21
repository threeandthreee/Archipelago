from dataclasses import dataclass
from math import floor
from typing import Dict, Optional

from BaseClasses import Location, Region
from . import Regions, Levels, Utils, Weapons
from .Levels import *


class ShadowTheHedgehogLocation(Location):
    game: str = "Shadow The Hedgehog"

    def __init__(self, player, location_name, location_id, region):
        super().__init__(player, location_name, location_id, region)

LOCATION_TYPE_MISSION_CLEAR = 1
LOCATION_TYPE_MISSION_OBJECTIVE = 2
LOCATION_TYPE_ENEMY = 3
LOCATION_TYPE_TOKEN = 4
LOCATION_TYPE_CHECKPOINT = 5
LOCATION_TYPE_KEY = 6
LOCATION_TYPE_OTHER = 7
LOCATION_TYPE_CHARACTER = 8

@dataclass
class LocationInfo:
    location_type: int
    locationId: int
    name: str
    stageId: Optional[int | None]
    alignmentId: Optional[int | None]
    count: Optional[int | None]
    total: Optional[int | None]
    other: str | None


@dataclass
class MissionClearLocation:
    stageId: int
    alignmentId: int
    requirement_count: int | None
    mission_object_name: Optional[str]
    distribution = None
    requirements = None
    def setDistribution(self, dist):
        self.distribution = dist
        return self

    def getDistribution(self):
        if self.distribution is not None:
            return self.distribution
        else:
            return {0:self.requirement_count}

    def setRequirement(self, reqs):
        if type(reqs) is not list:
            reqs = [reqs]
        self.requirements = reqs
        return self



ENEMY_CLASS_ALIEN = 0
ENEMY_CLASS_GUN = 1
ENEMY_CLASS_EGG = 2

@dataclass
class EnemySanityLocation:
    stageId: int
    enemyClass: int
    total_count: int
    mission_object_name: Optional[str]
    distribution: None

    def __init__(self, stageId, enemyClass, total_count, mission_objective_name):
        self.stageId = stageId
        self.enemyClass = enemyClass
        self.total_count = total_count
        self.mission_object_name = mission_objective_name

    def setDistribution(self, dist):
        self.distribution = dist
        return self

    def getDistribution(self):
        if self.distribution is not None:
            return self.distribution
        else:
            return {0: self.total_count}


@dataclass
class CheckpointLocation:
    stageId: int
    total_count: int
    distribution = None
    region = []

    def __init__(self, stageId, total_count):
        self.stageId = stageId
        self.total_count = total_count
        self.region = []
        for i in range(0, total_count):
            self.region.append(0)

    def setDistribution(self, dist):
        for region,available in dist.items():
            for l in available:
                self.region[l-1] = region
        return self

    def getRegion(self, index):
        return self.region[index-1]

@dataclass
class KeyLocation:
    stageId: int
    region = []

    def __init__(self, stageId):
        self.stageId = stageId
        self.region = [0,0,0,0,0]


    def setDistribution(self, dist):
        total = 0
        for region,count in dist.items():
            for c in range(0, count):
                self.region[total] = region
                total += 1

        return self

    def getRegion(self, index):
        return self.region[index]


    def setIndividual(self, key, region):
        self.region[key-1] = region
        return self


@dataclass
class CharacterLocation:
    name: str

MissionClearLocations = [
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_DARK, 35, "Soldier"),
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_HERO, 45, "Alien"),

    MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_HERO, None, None),
    #MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_DARK, 1, "Core"),
    MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_DARK, None, None),

    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_HERO, 60, "Alien"),
    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_DARK, 5, "Temple"),

    MissionClearLocation(STAGE_LETHAL_HIGHWAY, MISSION_ALIGNMENT_DARK, None, None),
    MissionClearLocation(STAGE_LETHAL_HIGHWAY, MISSION_ALIGNMENT_HERO, 1, "Tank")
        .setRequirement(REGION_RESTRICTION_TYPES.Gun),

    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_DARK, 5, "Lantern")
        .setDistribution(
        {
            1: 2,
            2: 3
        }
        )
        .setRequirement(REGION_RESTRICTION_TYPES.Torch),
    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            2: 1
        }
    ),
    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_HERO, 2, "Cream")
        .setDistribution(
        {
            1: 1,
            2: 1
        }
    ),

    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_DARK, 40, "Soldier")
        .setDistribution(
        {
            0: 1,
            1: 39
        }
    ),
    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            1: 1
        }
    ),

    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_HERO, 5, "Disc")
        .setDistribution(
        {
            0: 1,
            1: 4
        }
    ),

    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_DARK, 20, "Soldier"),
    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_HERO, None, None),

    MissionClearLocation(STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_DARK, 5, "Big Bomb")
        .setDistribution(
        {
            0: 3,
            1: 2
        }
    ),
    MissionClearLocation(STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_HERO, 20, "Little Bomb")
        .setDistribution(
        {
            0: 11,
            1: 9
        }
        )
    .setRequirement(REGION_RESTRICTION_TYPES.Vacuum),

    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_DARK, 60, "Soldier"),
    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_HERO, 10, "Researcher")
        .setRequirement(REGION_RESTRICTION_TYPES.Heal),

    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_DARK, 5, "Egg Ship")
        .setDistribution(
        {
            0: 1,
            1: 3,
            5: 1
        }
        )
    .setRequirement(REGION_RESTRICTION_TYPES.BlackArmsTurret),
    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            5: 1
        }
    ),
    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_HERO, 5, "Temple")
        .setDistribution(
        {
            0: 1,
            1: 3,
            5: 1
        }
    ),

    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_DARK, 30, "Bomb")
        .setDistribution(
        {
            1: 30
        }
    ),
    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            1: 1
        }
    ),

    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_HERO, 4, "Terminal")
        .setDistribution(
        {
            1: 4
        }
    ),

    MissionClearLocation(STAGE_DEATH_RUINS, MISSION_ALIGNMENT_DARK, None, None),
    MissionClearLocation(STAGE_DEATH_RUINS, MISSION_ALIGNMENT_HERO, 50, "Alien"),

    MissionClearLocation(STAGE_THE_ARK, MISSION_ALIGNMENT_DARK, 4, "Defense Unit")
        .setDistribution(
        {
            1: 4
        }
        )
    .setRequirement(REGION_RESTRICTION_TYPES.Gun),
    MissionClearLocation(STAGE_THE_ARK, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            1: 1
        }
    ),

    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_DARK, 1, "President Aircraft")
    .setRequirement(REGION_RESTRICTION_TYPES.Gun),
    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_HERO, 35, "Alien"),

    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_DARK, 28, "Soldier"),
    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_HERO, 1, "Egg Balloon")
        .setRequirement(REGION_RESTRICTION_TYPES.Gun),

    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_DARK, 6, "Defense Unit")
    .setDistribution(
        {
            0: 2,
            1: 4
        })
        .setRequirement(REGION_RESTRICTION_TYPES.Gun),
    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            1: 1
        }),
    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            1: 1
        }),
    MissionClearLocation(STAGE_LOST_IMPACT, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            1: 1
        }
    ),
    MissionClearLocation(STAGE_LOST_IMPACT, MISSION_ALIGNMENT_HERO, 35, "Artificial Chaos")
        .setDistribution(
        {
            0: 1,
            1: 34
        }
    ),

    MissionClearLocation(STAGE_GUN_FORTRESS, MISSION_ALIGNMENT_DARK, 3, "Computer")
    .setRequirement(REGION_RESTRICTION_TYPES.LongRangeGun),
    MissionClearLocation(STAGE_GUN_FORTRESS, MISSION_ALIGNMENT_HERO, None, None),

    MissionClearLocation(STAGE_BLACK_COMET, MISSION_ALIGNMENT_DARK, 50, "Soldier")
        .setDistribution(
        {
            1: 50
        }
    ),
    MissionClearLocation(STAGE_BLACK_COMET, MISSION_ALIGNMENT_HERO, None, None),

    MissionClearLocation(STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_DARK, 5, "Defense"),
    MissionClearLocation(STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_HERO, None, None),

    MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_DARK, None, None),
    MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            3: 1
        }
    ),
    #MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_HERO, 1, "Computer Room"),

    MissionClearLocation(STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_DARK, 4, "Shield")
        .setDistribution(
        {
            1: 1,
            2: 3
        }
    ),
    MissionClearLocation(STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            1: 1
        }
    )
]

EnemySanityLocations = \
[
    EnemySanityLocation(STAGE_WESTOPOLIS, ENEMY_CLASS_ALIEN, 45, "Black Arm"),
    EnemySanityLocation(STAGE_WESTOPOLIS, ENEMY_CLASS_GUN, 36, "GUN"),

    EnemySanityLocation(STAGE_DIGITAL_CIRCUIT, ENEMY_CLASS_GUN, 46, "GUN Soldier"),
    EnemySanityLocation(STAGE_DIGITAL_CIRCUIT, ENEMY_CLASS_ALIEN, 17, "Black Arm"),

    EnemySanityLocation(STAGE_GLYPHIC_CANYON, ENEMY_CLASS_GUN, 8, "GUN Soldier"),
    EnemySanityLocation(STAGE_GLYPHIC_CANYON, ENEMY_CLASS_ALIEN, 60, "Black Arm"),
    
    EnemySanityLocation(STAGE_LETHAL_HIGHWAY, ENEMY_CLASS_GUN, 30, "GUN Soldier"),
    EnemySanityLocation(STAGE_LETHAL_HIGHWAY, ENEMY_CLASS_ALIEN, 137, "Black Arm"),

    EnemySanityLocation(STAGE_CRYPTIC_CASTLE, ENEMY_CLASS_EGG, 17, "Egg Pawn"),
    EnemySanityLocation(STAGE_CRYPTIC_CASTLE, ENEMY_CLASS_ALIEN, 52, "Black Arm"),

    EnemySanityLocation(STAGE_PRISON_ISLAND, ENEMY_CLASS_GUN, 41, "GUN Soldier"),
    EnemySanityLocation(STAGE_PRISON_ISLAND, ENEMY_CLASS_ALIEN, 88, "Black Arm"),

    EnemySanityLocation(STAGE_CIRCUS_PARK, ENEMY_CLASS_GUN, 21, "GUN Soldier"),
    EnemySanityLocation(STAGE_CIRCUS_PARK, ENEMY_CLASS_EGG, 29, "Egg Pawn"),

    #EnemySanityLocation(STAGE_CENTRAL_CITY, ENEMY_CLASS_GUN, 100, "GUN Soldier"),
    #EnemySanityLocation(STAGE_CENTRAL_CITY, ENEMY_CLASS_ALIEN, 100, "Black Arm"),
    # 39 BA, 28G, time limit..

    EnemySanityLocation(STAGE_THE_DOOM, ENEMY_CLASS_GUN, 60, "GUN Soldier"),

    EnemySanityLocation(STAGE_SKY_TROOPS, ENEMY_CLASS_ALIEN, 73, "Black Arm"),
    EnemySanityLocation(STAGE_SKY_TROOPS, ENEMY_CLASS_EGG, 11, "Egg Pawn"),

    EnemySanityLocation(STAGE_MAD_MATRIX, ENEMY_CLASS_EGG, 31, "Egg Pawn"),
    EnemySanityLocation(STAGE_MAD_MATRIX, ENEMY_CLASS_ALIEN, 8, "Black Arm"),

    EnemySanityLocation(STAGE_DEATH_RUINS, ENEMY_CLASS_GUN, 21, "GUN Soldier"),
    EnemySanityLocation(STAGE_DEATH_RUINS, ENEMY_CLASS_ALIEN, 50, "Black Arm"),

    EnemySanityLocation(STAGE_THE_ARK, ENEMY_CLASS_GUN, 74, "GUN Soldier"),
    EnemySanityLocation(STAGE_THE_ARK, ENEMY_CLASS_ALIEN, 21, "Black Arm"),

    EnemySanityLocation(STAGE_AIR_FLEET, ENEMY_CLASS_GUN, 48, "GUN Soldier"),
    EnemySanityLocation(STAGE_AIR_FLEET, ENEMY_CLASS_ALIEN, 35, "Black Arm"),

    EnemySanityLocation(STAGE_IRON_JUNGLE, ENEMY_CLASS_GUN, 28, "GUN Soldier"),
    EnemySanityLocation(STAGE_IRON_JUNGLE, ENEMY_CLASS_EGG, 37, "Egg Pawn"),

    EnemySanityLocation(STAGE_SPACE_GADGET, ENEMY_CLASS_GUN, 25, "GUN Soldier"),
    EnemySanityLocation(STAGE_SPACE_GADGET, ENEMY_CLASS_ALIEN, 33, "Black Arm"),

    EnemySanityLocation(STAGE_LOST_IMPACT, ENEMY_CLASS_GUN, 31, "GUN Soldier"),
    EnemySanityLocation(STAGE_LOST_IMPACT, ENEMY_CLASS_ALIEN, 35, "Artificial Chaos"),

    EnemySanityLocation(STAGE_GUN_FORTRESS, ENEMY_CLASS_GUN, 94, "GUN Soldier"),
    EnemySanityLocation(STAGE_GUN_FORTRESS, ENEMY_CLASS_ALIEN, 18, "Black Arm"),

    EnemySanityLocation(STAGE_BLACK_COMET, ENEMY_CLASS_GUN, 53, "GUN Soldier"),
    EnemySanityLocation(STAGE_BLACK_COMET, ENEMY_CLASS_ALIEN, 83, "Black Arm"),
    # To Handle random respawns from the ships -- might want to make BA lower

    EnemySanityLocation(STAGE_LAVA_SHELTER, ENEMY_CLASS_EGG, 74, "Egg Robot"),

    EnemySanityLocation(STAGE_COSMIC_FALL, ENEMY_CLASS_GUN, 7, "GUN Soldier"),
    EnemySanityLocation(STAGE_COSMIC_FALL, ENEMY_CLASS_ALIEN, 24, "Black Arm"),

    EnemySanityLocation(STAGE_FINAL_HAUNT, ENEMY_CLASS_ALIEN, 122, "Black Arm"),
]

CheckpointLocations = \
[
    CheckpointLocation(STAGE_WESTOPOLIS, 6),
    CheckpointLocation(STAGE_DIGITAL_CIRCUIT, 7),
    CheckpointLocation(STAGE_GLYPHIC_CANYON, 8),
    CheckpointLocation(STAGE_LETHAL_HIGHWAY, 5),
    CheckpointLocation(STAGE_CRYPTIC_CASTLE, 8)
        .setDistribution(
        {
            0: [1],
            1: [2],
            2: [3,4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_PRISON_ISLAND, 7)
        .setDistribution(
        {
            0: [1,2],
            1: [3,4,5,6,7]
        }
    ),
    CheckpointLocation(STAGE_CIRCUS_PARK, 7),
    CheckpointLocation(STAGE_CENTRAL_CITY, 6)
        .setDistribution(
        {
            0: [1,2,3],
            1: [4,5,6]
        }
    ),
    CheckpointLocation(STAGE_THE_DOOM, 6),
    CheckpointLocation(STAGE_SKY_TROOPS, 8)
        .setDistribution(
        {
            0: [1,2],
            1: [3,4,5,6],
            5: [7,8]
        }
    ),
    CheckpointLocation(STAGE_MAD_MATRIX, 6)
        .setDistribution(
        {
            0: [1],
            1: [2,3,4,5,6]
        }
    ),
    CheckpointLocation(STAGE_DEATH_RUINS, 7),
    CheckpointLocation(STAGE_THE_ARK, 8)
        .setDistribution(
        {
            0: [1],
            1: [2,3,4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_AIR_FLEET, 8),
    CheckpointLocation(STAGE_IRON_JUNGLE, 8),
    CheckpointLocation(STAGE_SPACE_GADGET, 8).
        setDistribution(
        {
            0: [1,2,3,6],
            1: [4,5,7,8]
        }
    ),
    CheckpointLocation(STAGE_LOST_IMPACT, 8)
        .setDistribution(
        {
            0: [1],
            1: [2,3,4,5,6,7,8],
        }
    ),
    CheckpointLocation(STAGE_GUN_FORTRESS, 7),
    CheckpointLocation(STAGE_BLACK_COMET, 8)
        .setDistribution(
        {
            0: [1],
            1: [2,3,4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_LAVA_SHELTER, 8),
    CheckpointLocation(STAGE_COSMIC_FALL, 7)
        .setDistribution(
        {
            0: [1,2,3,4,5,6],
            3: [7]
        }
    ),
    CheckpointLocation(STAGE_FINAL_HAUNT, 8)
        .setDistribution(
        {
            0: [1,2],
            1: [3,4,5,6,7,8]
        }
    )
]

KeyLocations = \
[
    KeyLocation(STAGE_WESTOPOLIS),
    KeyLocation(STAGE_DIGITAL_CIRCUIT),
    KeyLocation(STAGE_GLYPHIC_CANYON),
    KeyLocation(STAGE_LETHAL_HIGHWAY),
    KeyLocation(STAGE_CRYPTIC_CASTLE)
        .setDistribution(
        {
            0: 1,
            2: 4
        }
    ),
    KeyLocation(STAGE_PRISON_ISLAND)
        .setDistribution(
        {
            0: 1,
            1: 4
        }
    ),
    KeyLocation(STAGE_CIRCUS_PARK),
    KeyLocation(STAGE_CENTRAL_CITY)
        .setDistribution(
        {
            0: 2,
            1: 3
        }
    ),
    KeyLocation(STAGE_THE_DOOM),
    KeyLocation(STAGE_SKY_TROOPS)
        .setDistribution(
        {
            1: 4,
            5: 1
        }
    ),
    KeyLocation(STAGE_MAD_MATRIX)
        .setDistribution(
        {
            1: 5
        }
    ),
    KeyLocation(STAGE_DEATH_RUINS),
    KeyLocation(STAGE_THE_ARK)
        .setDistribution(
        {
            0: 1,
            1: 4
        }
    ),
    KeyLocation(STAGE_AIR_FLEET),
    KeyLocation(STAGE_IRON_JUNGLE),
    KeyLocation(STAGE_SPACE_GADGET)
        .setDistribution(
        {
            0: 2,
            1: 3
        }
    ),
    KeyLocation(STAGE_LOST_IMPACT)
        .setDistribution(
        {
            0: 1,
            1: 4
        }
    ),
    KeyLocation(STAGE_GUN_FORTRESS),
    KeyLocation(STAGE_BLACK_COMET)
        .setDistribution(
        {
            1: 5
        }
    ),
    KeyLocation(STAGE_LAVA_SHELTER),
    KeyLocation(STAGE_COSMIC_FALL)
        .setDistribution(
        {
            0: 3,
            2: 2
        }
    ),
    KeyLocation(STAGE_FINAL_HAUNT)
        .setDistribution(
        {
            0: 1,
            1: 4
        }
    )
    .setIndividual(4, 2),
]



def GetStageInformation(stageId):
    missions = [m for m in MissionClearLocations if m.stageId == stageId]
    return missions

def GetStageEnemysanityInformation(stageId):
    return [ e for e in EnemySanityLocations if e.stageId == stageId]

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

def GetLocationInfoDict():
    all_locations = GetAllLocationInfo()

    result = {}
    for location_type in all_locations:
        for location in location_type:
            result[location.locationId] = location

    return result



def GetEnemyLocationName(stageId, enemyClass, objectName, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(enemyClass) + str(i) + "3")
    objective_location_name = "Enemysanity:" + (LEVEL_ID_TO_LEVEL[stageId] + " " + objectName + " (" + str(i) + ")")

    return id_name, objective_location_name

def GetCheckpointLocationName(stageId, objectName, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(0) + str(i) + "4")
    objective_location_name = "Checkpointsanity:" + (LEVEL_ID_TO_LEVEL[stageId] + " " + objectName + " (" + str(i) + ")")

    return id_name, objective_location_name

def GetCharacterLocationName(objectName,i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + "000" + str(0) + str(i) + "5")
    objective_location_name = "Charactersanity:" + objectName

    return id_name, objective_location_name

def GetKeysanityLocationName(stageId, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(i+1) + "7")
    view_name = (LEVEL_ID_TO_LEVEL[stageId] + " Key " + str(i+1))

    return id_name, view_name

def GetWeaponsanityLocationName(weaponName, weaponId):
    id_name = int(str(LOCATION_ID_PLUS) + str(weaponId) + "8")
    view_name = "Held Weapon:" + weaponName

    return id_name, view_name



def GetAllLocationInfo():
    mission_clear_locations = []
    token_locations = []
    mission_locations = []
    enemysanity_locations = []
    checkpointsanity_locations = []
    charactersanity_locations = []
    keysanity_locations = []
    weaponsanity_locations = []

    for location in MissionClearLocations:
        location_id, completion_location_name = GetLevelCompletionNames(location.stageId, location.alignmentId)
        info = LocationInfo(LOCATION_TYPE_MISSION_CLEAR, location_id, completion_location_name,
                            stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                            other=None)
        mission_clear_locations.append(info)

        base_token_id, base_token_name = GetLevelTokenNames(location.stageId, location.alignmentId, Levels.ITEM_TOKEN_TYPE_STANDARD)
        info = LocationInfo(LOCATION_TYPE_TOKEN,base_token_id, base_token_name,
                            stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                            other=Levels.ITEM_TOKEN_TYPE_STANDARD)
        token_locations.append(info)

        if location.alignmentId != MISSION_ALIGNMENT_NEUTRAL:
            hero_or_dark_token_id, hero_or_dark_token_name = GetLevelTokenNames(location.stageId, location.alignmentId, Levels.ITEM_TOKEN_TYPE_ALIGNMENT)
            info = LocationInfo(LOCATION_TYPE_TOKEN, hero_or_dark_token_id, hero_or_dark_token_name,
                                stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_ALIGNMENT)
            token_locations.append(info)

        if location.stageId in Levels.FINAL_STAGES:
            final_token_id, final_token_name = GetLevelTokenNames(location.stageId, location.alignmentId,
                                                                ITEM_TOKEN_TYPE_FINAL)
            info = LocationInfo(LOCATION_TYPE_TOKEN, final_token_id, final_token_name,
                                stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_FINAL)
            token_locations.append(info)

        i = 0
        if location.requirement_count is not None:
            requirement_token_id, requirement_token_name = GetLevelTokenNames(location.stageId, location.alignmentId,
                                                                ITEM_TOKEN_TYPE_OBJECTIVE)
            info = LocationInfo(LOCATION_TYPE_TOKEN, requirement_token_id, requirement_token_name,
                                stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_OBJECTIVE)
            token_locations.append(info)

            for j in range(1, location.requirement_count+1):
                i += 1
                location_id, objective_location_name = (
                    GetLevelObjectNames(location.stageId, location.alignmentId, location.mission_object_name, j))
                info = LocationInfo(LOCATION_TYPE_MISSION_OBJECTIVE, location_id, objective_location_name,
                                   stageId=location.stageId, alignmentId=location.alignmentId,
                                    count=j, total=location.requirement_count, other=None)
                mission_locations.append(info)

    for enemy in EnemySanityLocations:
        i = 0
        for j in range(1, enemy.total_count+1):
            i += 1
            location_id, objective_location_name = (
                GetEnemyLocationName(enemy.stageId, enemy.enemyClass, enemy.mission_object_name, j))
            info = LocationInfo(LOCATION_TYPE_ENEMY, location_id, objective_location_name,
                               stageId=enemy.stageId, alignmentId=enemy.enemyClass,
                                count=j, total=enemy.total_count, other=None)
            enemysanity_locations.append(info)


    progression_locations = [LocationInfo(LOCATION_TYPE_OTHER, LOCATION_ID_PLUS+1000, Levels.DevilDoom_Name, stageId=None, alignmentId=None,
                                 total=None, count=None, other=None)]

    for location in CheckpointLocations:
        i = 0
        for j in range(1, location.total_count+1):
            i += 1
            location_id, objective_location_name = (
                GetCheckpointLocationName(location.stageId,"Checkpoint", j))
            info = LocationInfo(LOCATION_TYPE_CHECKPOINT, location_id, objective_location_name,
                               stageId=location.stageId, alignmentId=None,
                                count=j, total=location.total_count, other=None)
            checkpointsanity_locations.append(info)

    char_index = 0
    for character in CharacterToLevel.keys():
        location_id, objective_location_name = GetCharacterLocationName(character,char_index)
        info = LocationInfo(LOCATION_TYPE_CHARACTER, location_id, objective_location_name,
                            stageId=None, alignmentId=None,
                            count=None, total=None, other=character)
        charactersanity_locations.append(info)
        char_index+=1

    for key_location in KeyLocations:
        for i in range(0,5):
            key_location_id, key_location_name = GetKeysanityLocationName(key_location.stageId, i)
            info = LocationInfo(LOCATION_TYPE_KEY, key_location_id, key_location_name,
                                        stageId=key_location.stageId, alignmentId=None, count=i, total=5, other=None)
            keysanity_locations.append(info)

    for weapon in Weapons.WEAPON_INFO:
        weapon_location_id, weapon_location_name = GetWeaponsanityLocationName(weapon.name, weapon.game_id)
        info = LocationInfo(LOCATION_TYPE_KEY, weapon_location_id, weapon_location_name,
                            stageId=None, alignmentId=None, count=None, total=None, other=weapon.name)
        weaponsanity_locations.append(info)


    return (mission_clear_locations, mission_locations, progression_locations,
            enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
            token_locations, keysanity_locations, weaponsanity_locations)


def is_token_required_by_goal(world, token : LocationInfo):

    goal_dictates_missions = world.options.goal_missions > 0
    goal_dictates_dark_missions = world.options.goal_dark_missions > 0
    goal_dictates_hero_missions = world.options.goal_hero_missions > 0
    goal_dictates_final_missions = world.options.goal_final_missions > 0
    goal_dictates_neutral_missions = world.options.goal_missions > 0
    goal_dictates_progression_missions = world.options.goal_objective_missions > 0

    if LEVEL_ID_TO_LEVEL[token.stageId] in world.options.excluded_stages:
        return False

    if goal_dictates_missions and token.other == ITEM_TOKEN_TYPE_STANDARD:
        return True

    if goal_dictates_dark_missions and token.other == ITEM_TOKEN_TYPE_ALIGNMENT and \
        token.alignmentId == MISSION_ALIGNMENT_DARK:
        return True

    if goal_dictates_hero_missions and token.other == ITEM_TOKEN_TYPE_ALIGNMENT and \
        token.alignmentId == MISSION_ALIGNMENT_HERO:
        return True

    if goal_dictates_neutral_missions and token.other == ITEM_TOKEN_TYPE_ALIGNMENT and \
        token.alignmentId == MISSION_ALIGNMENT_NEUTRAL:
        return True

    if goal_dictates_final_missions and token.other == ITEM_TOKEN_TYPE_FINAL:
        return True

    if goal_dictates_progression_missions and token.other == ITEM_TOKEN_TYPE_OBJECTIVE:
        return True

    return False


def create_locations(world: "ShtHWorld", regions: Dict[str, Region]):
    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations) = GetAllLocationInfo()

    for location in clear_locations:
        if LEVEL_ID_TO_LEVEL[location.stageId] in world.options.excluded_stages:
            continue
        within_region = regions[Regions.stage_id_to_region(location.stageId)]
        completion_location = ShadowTheHedgehogLocation(world.player, location.name, location.locationId, within_region)
        within_region.locations.append(completion_location)

        # TODO:
        # Work out each stages required tokens and add a location
        # If the various settings are enabled

    if world.options.objective_sanity.value:
        percentage = world.options.objective_percentage.value
        for location in mission_locations:
            if not world.options.enemy_objective_sanity and (location.name == "Soldier" or location.name == "Alien"):
                continue
            if LEVEL_ID_TO_LEVEL[location.stageId] in world.options.excluded_stages:
                continue

            max_required = Utils.getRequiredCount(location.total, percentage, round_method=floor)
            if location.count <= max_required :
                within_region = regions[Regions.stage_id_to_region(location.stageId)]
                completion_location = ShadowTheHedgehogLocation(world.player, location.name, location.locationId, within_region)
                within_region.locations.append(completion_location)

    if world.options.enemy_sanity:
        percentage = world.options.enemy_sanity_percentage.value
        for enemy in enemysanity_locations:
            if LEVEL_ID_TO_LEVEL[enemy.stageId] in world.options.excluded_stages:
                continue
            max_required = Utils.getRequiredCount(enemy.total, percentage, round_method=floor)
            if enemy.count <= max_required:
                within_region = regions[Regions.get_max_stage_region_id(enemy.stageId)]
                completion_location = ShadowTheHedgehogLocation(world.player, enemy.name, enemy.locationId, within_region)
                within_region.locations.append(completion_location)

    if world.options.checkpoint_sanity:
        for checkpoint in checkpointsanity_locations:
            if LEVEL_ID_TO_LEVEL[checkpoint.stageId] in world.options.excluded_stages:
                continue
            found_check_level_info = [ c for c in CheckpointLocations if c.stageId == checkpoint.stageId ][0]
            region_index = found_check_level_info.getRegion(checkpoint.count)
            within_region = regions[Regions.stage_id_to_region(checkpoint.stageId, region_index)]
            completion_location = ShadowTheHedgehogLocation(world.player, checkpoint.name, checkpoint.locationId, within_region)
            within_region.locations.append(completion_location)

    if world.options.key_sanity:
        for key in keysanity_locations:
            if LEVEL_ID_TO_LEVEL[key.stageId] in world.options.excluded_stages:
                continue
            found_key_level_info = [c for c in KeyLocations if c.stageId == key.stageId][0]
            region_index = found_key_level_info.getRegion(key.count)
            within_region = regions[Regions.stage_id_to_region(key.stageId, region_index)]
            completion_location = ShadowTheHedgehogLocation(world.player, key.name, key.locationId, within_region)
            within_region.locations.append(completion_location)

    if world.options.character_sanity:
        for character in charactersanity_locations:
            region_name = Regions.character_name_to_region(character.other)
            if region_name not in regions:
                continue
            within_region = regions[region_name]
            completion_location = ShadowTheHedgehogLocation(world.player, character.name, character.locationId,
                                                            within_region)
            within_region.locations.append(completion_location)

    if world.options.weapon_sanity_hold.value > 0 :
        for weapon in weaponsanity_locations:
            region_name = Regions.weapon_name_to_region(weapon.other)
            if region_name not in regions:
                continue
            within_region = regions[region_name]
            completion_location = ShadowTheHedgehogLocation(world.player, weapon.name, weapon.locationId,
                                                            within_region)
            within_region.locations.append(completion_location)


    for token in token_locations:
        goal_required = is_token_required_by_goal(world, token)
        if not goal_required:
            continue

        within_region = regions[Regions.stage_id_to_region(token.stageId)]
        token_location = ShadowTheHedgehogLocation(world.player, token.name, token.locationId,
                                                        within_region)
        within_region.locations.append(token_location)
        world.token_locations.append(token)


    end_region = regions["FinalStory"]
    devil_doom_location = ShadowTheHedgehogLocation(world.player, end_location[0].name, end_location[0].locationId, end_region)
    end_region.locations.append(devil_doom_location)

def count_locations(world):
    count = 0
    (mission_clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations,
     charactersanity_locations, token_locations, keysanity_locations,
     weaponsanity_locations) = GetAllLocationInfo()

    mission_clear_locations = [ mc for mc in mission_clear_locations if Levels.LEVEL_ID_TO_LEVEL[mc.stageId]
                                not in world.options.excluded_stages]

    mission_locations = [ ml for ml in mission_locations if Levels.LEVEL_ID_TO_LEVEL[ml.stageId]
                                not in world.options.excluded_stages]

    enemysanity_locations = [ml for ml in enemysanity_locations if Levels.LEVEL_ID_TO_LEVEL[ml.stageId]
                         not in world.options.excluded_stages]

    checkpointsanity_locations = [ml for ml in checkpointsanity_locations if Levels.LEVEL_ID_TO_LEVEL[ml.stageId]
                             not in world.options.excluded_stages]

    charactersanity_locations = [ ml for ml in charactersanity_locations if ml.other in world.available_characters ]

    keysanity_locations = [ks for ks in keysanity_locations if Levels.LEVEL_ID_TO_LEVEL[ks.stageId]
                             not in world.options.excluded_stages]

    weaponsanity_locations = [ml for ml in weaponsanity_locations if ml.other in world.available_weapons]

    count += len(mission_clear_locations)

    if world.options.objective_sanity:
        percentage = world.options.objective_percentage.value
        for location in mission_locations:
            if not world.options.enemy_objective_sanity and (location.name == "Soldier" or location.name == "Alien"):
                continue
            max_required = Utils.getRequiredCount(location.total, percentage, round_method=floor)
            if location.count <= max_required:
                count += 1

    if world.options.enemy_sanity:
        percentage = world.options.enemy_sanity_percentage.value
        for enemy in enemysanity_locations:
            max_required = Utils.getRequiredCount(enemy.total, percentage, round_method=floor)
            if enemy.count <= max_required:
                count += 1

    if world.options.checkpoint_sanity:
        count += len(checkpointsanity_locations)

    if world.options.character_sanity:
        count += len(charactersanity_locations)

    if world.options.key_sanity:
        count += len(keysanity_locations)

    if world.options.weapon_sanity_hold > 0:
        count += len(weaponsanity_locations)

    count += len(end_location)

    return count














