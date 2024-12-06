from dataclasses import dataclass

from worlds.shadow_the_hedgehog import Options

MISSION_ALIGNMENT_DARK = 0
MISSION_ALIGNMENT_NEUTRAL = 1
MISSION_ALIGNMENT_HERO = 2

STAGE_WESTOPOLIS = 100
STAGE_DIGITAL_CIRCUIT = 200
STAGE_GLYPHIC_CANYON = 201
STAGE_LETHAL_HIGHWAY = 202
STAGE_CRYPTIC_CASTLE = 300
STAGE_PRISON_ISLAND = 301
STAGE_CIRCUS_PARK = 302
STAGE_CENTRAL_CITY = 400
STAGE_THE_DOOM = 401
STAGE_SKY_TROOPS = 402
STAGE_MAD_MATRIX = 403
STAGE_DEATH_RUINS = 404
STAGE_THE_ARK = 500
STAGE_AIR_FLEET = 501
STAGE_IRON_JUNGLE = 502
STAGE_SPACE_GADGET = 503
STAGE_LOST_IMPACT = 504
STAGE_GUN_FORTRESS = 600
STAGE_BLACK_COMET = 601
STAGE_LAVA_SHELTER = 602
STAGE_COSMIC_FALL = 603
STAGE_FINAL_HAUNT = 604

BOSS_BLACK_BULL_LH = 210
BOSS_EGG_BREAKER_CC = 310
BOSS_HEAVY_DOG = 410
BOSS_EGG_BREAKER_MM = 411
BOSS_BLACK_BULL_DR = 412
BOSS_BLUE_FALCON = 510
BOSS_EGG_BREAKER_IJ = 511
BOSS_BLACK_DOOM_GF = 610
BOSS_DIABLON_GF = 611
BOSS_EGG_DEALER_BC = 612
BOSS_DIABLON_BC = 613
BOSS_EGG_DEALER_LS = 614
BOSS_BLACK_DOOM_CF = 615
BOSS_EGG_DEALER_CF = 616
BOSS_BLACK_DOOM_FH = 617
BOSS_DIABLON_FH = 618

STAGE_THE_LAST_WAY = 700
BOSS_DEVIL_DOOM = 710

LOCATION_ID_PLUS = 100066

LEVEL_ID_TO_LEVEL = {
    STAGE_WESTOPOLIS: "Westopolis",
    STAGE_DIGITAL_CIRCUIT: "Digital Circuit",
    STAGE_GLYPHIC_CANYON: "Glyphic Canyon",
    STAGE_LETHAL_HIGHWAY : "Lethal Highway",
    STAGE_CRYPTIC_CASTLE : "Cryptic Castle",
    STAGE_PRISON_ISLAND : "Prison Island",
    STAGE_CIRCUS_PARK : "Circus Park",
    STAGE_CENTRAL_CITY : "Central City",
    STAGE_THE_DOOM : "The Doom",
    STAGE_SKY_TROOPS : "Sky Troops",
    STAGE_MAD_MATRIX : "Mad Matrix",
    STAGE_DEATH_RUINS : "Death Ruins",
    STAGE_THE_ARK : "The Ark",
    STAGE_AIR_FLEET : "Air Fleet",
    STAGE_IRON_JUNGLE : "Iron Jungle",
    STAGE_SPACE_GADGET : "Space Gadget",
    STAGE_LOST_IMPACT : "Lost Impact",
    STAGE_GUN_FORTRESS : "Gun Fortress",
    STAGE_BLACK_COMET : "Black Comet",
    STAGE_LAVA_SHELTER : "Lava Shelter",
    STAGE_COSMIC_FALL : "Cosmic Fall",
    STAGE_FINAL_HAUNT : "Final Haunt",
    BOSS_BLACK_BULL_LH: "Black Bull Lethal Highway",
    BOSS_EGG_BREAKER_CC: "Egg Breaker Cryptic Castle",
    BOSS_HEAVY_DOG: "Heavy Dog",
    BOSS_EGG_BREAKER_MM: "Egg Breaker Mad Matrix",
    BOSS_BLACK_BULL_DR: "Black Bull Death Ruins",
    BOSS_BLUE_FALCON: "Blue Falcon",
    BOSS_EGG_BREAKER_IJ:"Egg Breaker Iron Jungle",
    BOSS_BLACK_DOOM_GF: "Black Doom Gun Fortress",
    BOSS_DIABLON_GF: "Diablon Gun Fortress",
    BOSS_EGG_DEALER_BC: "Egg Dealer Black Comet",
    BOSS_DIABLON_BC: "Diablon Black Comet",
    BOSS_EGG_DEALER_LS : "Egg Dealer Lava Shelter",
    BOSS_EGG_DEALER_CF: "Egg Dealer Cosmic Fall",
    BOSS_BLACK_DOOM_CF: "Black Doom Cosmic Fall",
    BOSS_BLACK_DOOM_FH : "Black Doom Final Haunt",
    BOSS_DIABLON_FH: "Diablon Final Haunt",

    STAGE_THE_LAST_WAY : "The Last Way",
    BOSS_DEVIL_DOOM: "Devil Doom"
}

STAGE_TO_STORY_BLOCK = \
{
    STAGE_WESTOPOLIS: 5,
    STAGE_DIGITAL_CIRCUIT: 6,
    STAGE_GLYPHIC_CANYON: 7,
    STAGE_LETHAL_HIGHWAY: 8,
    STAGE_CRYPTIC_CASTLE: 9,
    STAGE_PRISON_ISLAND: 10,
    STAGE_CIRCUS_PARK: 11,
    STAGE_CENTRAL_CITY: 12,
    STAGE_THE_DOOM: 13,
    STAGE_SKY_TROOPS: 14,
    STAGE_MAD_MATRIX: 15,
    STAGE_DEATH_RUINS: 16,
    STAGE_THE_ARK: 17,
    STAGE_AIR_FLEET: 18,
    STAGE_IRON_JUNGLE: 19,
    STAGE_SPACE_GADGET: 20,
    STAGE_LOST_IMPACT: 21,
    STAGE_GUN_FORTRESS: 22,
    STAGE_BLACK_COMET: 23,
    STAGE_LAVA_SHELTER: 24,
    STAGE_COSMIC_FALL: 25,
    STAGE_FINAL_HAUNT: 26,
}

class REGION_RESTRICTION_TYPES:
    KeyDoor = 1
    BlackHawk = 2
    BlackVolt = 3
    Torch = 4
    AirSaucer = 5
    Car = 6
    GunJumper = 7
    LongRangeGun = 8
    GunLift = 9
    NoRestriction = 10
    Vacuum = 11
    Gun = 12
    Heal = 13,
    BlackArmsTurret = 14
    GunTurret = 15
    ShootOrTurret = 16

def IsWeaponsanityRestriction(restriction_type):
    weapons = [REGION_RESTRICTION_TYPES.Torch, REGION_RESTRICTION_TYPES.LongRangeGun,
               REGION_RESTRICTION_TYPES.Vacuum, REGION_RESTRICTION_TYPES.Gun,
               REGION_RESTRICTION_TYPES.Heal]
    return restriction_type in weapons

def IsVeichleSanityRestriction(restriction_type):
    veichles = [REGION_RESTRICTION_TYPES.BlackHawk, REGION_RESTRICTION_TYPES.BlackVolt,
                REGION_RESTRICTION_TYPES.AirSaucer, REGION_RESTRICTION_TYPES.Car,
                REGION_RESTRICTION_TYPES.GunJumper, REGION_RESTRICTION_TYPES.GunLift,
                REGION_RESTRICTION_TYPES.BlackArmsTurret, REGION_RESTRICTION_TYPES.GunTurret]
    return restriction_type in veichles

@dataclass
class LevelRegion:
    stageId: int
    regionIndex: int
    restrictionType: int
    logicType: int
    fromRegions: list

    def __init__(self, stageId, regionIndex, restrictionType):
        self.stageId = stageId
        self.regionIndex = regionIndex
        self.restrictionType = restrictionType
        self.fromRegions = None if regionIndex is None else [regionIndex - 1]
        self.logicType = Options.LogicLevel.option_normal

    def setLogicType(self, logic):
        self.logicType = logic
        return self

    def setFromRegion(self, fromRegion):
        if type(fromRegion) is int:
            self.fromRegions = [fromRegion]
        elif type(fromRegion) is list:
            self.fromRegions = fromRegion

        return self


INDIVIDUAL_LEVEL_REGIONS = \
[
    LevelRegion(STAGE_WESTOPOLIS, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_DIGITAL_CIRCUIT, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_GLYPHIC_CANYON, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_LETHAL_HIGHWAY, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_CRYPTIC_CASTLE, 1, REGION_RESTRICTION_TYPES.Torch),
    LevelRegion(STAGE_CRYPTIC_CASTLE, 2, REGION_RESTRICTION_TYPES.BlackHawk),
    LevelRegion(STAGE_CRYPTIC_CASTLE, 3, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_PRISON_ISLAND, 1, REGION_RESTRICTION_TYPES.AirSaucer),
    LevelRegion(STAGE_PRISON_ISLAND, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_CIRCUS_PARK, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_CENTRAL_CITY, 1, REGION_RESTRICTION_TYPES.Car)
        .setLogicType(Options.LogicLevel.option_easy),
    LevelRegion(STAGE_CENTRAL_CITY, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_THE_DOOM, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_SKY_TROOPS, 1, REGION_RESTRICTION_TYPES.GunJumper)
        .setLogicType(Options.LogicLevel.option_easy),
    LevelRegion(STAGE_SKY_TROOPS, 2, REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_SKY_TROOPS, 3, REGION_RESTRICTION_TYPES.BlackVolt)
        .setFromRegion(2),
    LevelRegion(STAGE_SKY_TROOPS, 4, REGION_RESTRICTION_TYPES.BlackHawk)
        .setFromRegion(1),
    LevelRegion(STAGE_SKY_TROOPS, 5, REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([3,4]),

    LevelRegion(STAGE_MAD_MATRIX, 1, REGION_RESTRICTION_TYPES.LongRangeGun)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_MAD_MATRIX, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_DEATH_RUINS, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_THE_ARK, 1, REGION_RESTRICTION_TYPES.BlackVolt),
    LevelRegion(STAGE_THE_ARK, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_AIR_FLEET, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_IRON_JUNGLE, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_SPACE_GADGET, 1, REGION_RESTRICTION_TYPES.AirSaucer)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_SPACE_GADGET, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_LOST_IMPACT, 1, REGION_RESTRICTION_TYPES.GunLift),
    LevelRegion(STAGE_LOST_IMPACT, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_GUN_FORTRESS, 1, REGION_RESTRICTION_TYPES.ShootOrTurret)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_GUN_FORTRESS, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_BLACK_COMET, 1, REGION_RESTRICTION_TYPES.AirSaucer),
    LevelRegion(STAGE_BLACK_COMET, 2, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_LAVA_SHELTER, 1, REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_COSMIC_FALL, 1, REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_COSMIC_FALL, 2, REGION_RESTRICTION_TYPES.GunJumper)
        .setFromRegion(0),
    LevelRegion(STAGE_COSMIC_FALL, 3, REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([1,2]),

    LevelRegion(STAGE_FINAL_HAUNT, 1, REGION_RESTRICTION_TYPES.Vacuum)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_FINAL_HAUNT, 2, REGION_RESTRICTION_TYPES.BlackVolt),
    LevelRegion(STAGE_FINAL_HAUNT, 3, REGION_RESTRICTION_TYPES.KeyDoor)
        .setFromRegion(1),
]

FINAL_STAGES = [STAGE_GUN_FORTRESS, STAGE_BLACK_COMET, STAGE_LAVA_SHELTER, STAGE_COSMIC_FALL, STAGE_FINAL_HAUNT]

CharacterToLevel = {
    "Sonic": [STAGE_WESTOPOLIS, STAGE_LETHAL_HIGHWAY, STAGE_FINAL_HAUNT],
    "Tails": [STAGE_CIRCUS_PARK, STAGE_AIR_FLEET],
    "Knuckles": [STAGE_GLYPHIC_CANYON, STAGE_CENTRAL_CITY, (STAGE_BLACK_COMET, 1)],
    "Amy": [STAGE_CRYPTIC_CASTLE],
    "Eggman": [(STAGE_CRYPTIC_CASTLE, 1), STAGE_CIRCUS_PARK, STAGE_SKY_TROOPS,
               STAGE_IRON_JUNGLE, STAGE_LAVA_SHELTER],
    "Rouge": [STAGE_DIGITAL_CIRCUIT, STAGE_DEATH_RUINS, STAGE_GUN_FORTRESS],
    "Omega": [STAGE_IRON_JUNGLE, STAGE_LAVA_SHELTER],
    "Doom": [STAGE_WESTOPOLIS, STAGE_DIGITAL_CIRCUIT, STAGE_GLYPHIC_CANYON,
             STAGE_LETHAL_HIGHWAY, STAGE_PRISON_ISLAND, STAGE_CENTRAL_CITY,
             STAGE_THE_DOOM, STAGE_SKY_TROOPS, STAGE_MAD_MATRIX,
             STAGE_DEATH_RUINS, STAGE_THE_ARK, STAGE_AIR_FLEET,
             STAGE_SPACE_GADGET, (STAGE_GUN_FORTRESS,1), STAGE_BLACK_COMET,
             STAGE_COSMIC_FALL, (STAGE_FINAL_HAUNT, 1)],
    "Espio": [STAGE_MAD_MATRIX],
    "Charmy": [STAGE_PRISON_ISLAND],
    "Vector": [STAGE_COSMIC_FALL],
    "Maria": [STAGE_THE_DOOM, STAGE_LOST_IMPACT]
}

ALL_STAGES = list(LEVEL_ID_TO_LEVEL.keys())
BOSS_STAGES = [
    BOSS_BLACK_BULL_LH,
    BOSS_EGG_BREAKER_CC,
    BOSS_HEAVY_DOG ,
    BOSS_EGG_BREAKER_MM,
    BOSS_BLACK_BULL_DR,
    BOSS_BLUE_FALCON,
    BOSS_EGG_BREAKER_IJ,
    BOSS_BLACK_DOOM_GF,
    BOSS_DIABLON_GF ,
    BOSS_EGG_DEALER_BC,
    BOSS_DIABLON_BC,
    BOSS_EGG_DEALER_LS,
    BOSS_BLACK_DOOM_CF,
    BOSS_EGG_DEALER_CF,
    BOSS_BLACK_DOOM_FH,
    BOSS_DIABLON_FH
]

BANNED_AVAILABLE_STAGES = [STAGE_THE_LAST_WAY, BOSS_DEVIL_DOOM]

DevilDoom_Name = "Devil Doom"

ALIGNMENT_TO_STRING = \
{
    0: "Dark",
    1: "Neutral",
    2: "Hero"
}






# Starting at Westopolis Clear
# Levels store all ranks of missions even though they don't exist
# We can abuse this :)

ITEM_TOKEN_TYPE_STANDARD = 0
ITEM_TOKEN_TYPE_ALIGNMENT = 1
ITEM_TOKEN_TYPE_FINAL = 2
ITEM_TOKEN_TYPE_OBJECTIVE = 3

TOKEN_TYPE_TO_STRING = \
{
    ITEM_TOKEN_TYPE_STANDARD: "Base",
    ITEM_TOKEN_TYPE_ALIGNMENT: "Alignment",
    ITEM_TOKEN_TYPE_FINAL: "Final",
    ITEM_TOKEN_TYPE_OBJECTIVE: "Objective"
}


def GetLevelTokenNames(stageId, alignmentId, type):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(type) + str(alignmentId) + "0")
    view_name = (LEVEL_ID_TO_LEVEL[stageId] + " Mission Token " + ALIGNMENT_TO_STRING[alignmentId] +
                 (" " + TOKEN_TYPE_TO_STRING[type] if type != ITEM_TOKEN_TYPE_STANDARD else "") )

    return id_name, view_name

def GetLevelCompletionNames(stageId, alignmentId):

    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(alignmentId) + "1")
    view_name = LEVEL_ID_TO_LEVEL[stageId] + " Mission Clear " + ALIGNMENT_TO_STRING[alignmentId]

    return id_name, view_name

def GetLevelObjectNames(stageId, alignmentId, objectName, i):
    id_name =  int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(alignmentId) + str(i) + "0")
    objective_location_name = (LEVEL_ID_TO_LEVEL[stageId] + "-" +
                               objectName + " " + str(i))

    return id_name, objective_location_name

