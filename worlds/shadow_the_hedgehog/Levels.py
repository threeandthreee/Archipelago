


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
    STAGE_FINAL_HAUNT : "Final Haunt"
}

FINAL_STAGES = [STAGE_GUN_FORTRESS, STAGE_BLACK_COMET, STAGE_LAVA_SHELTER, STAGE_COSMIC_FALL, STAGE_FINAL_HAUNT]

CharacterToLevel = {
    "Sonic": [STAGE_WESTOPOLIS, STAGE_LETHAL_HIGHWAY, STAGE_SPACE_GADGET, STAGE_FINAL_HAUNT],
    "Tails": [STAGE_CIRCUS_PARK, STAGE_AIR_FLEET],
    "Knuckles": [STAGE_GLYPHIC_CANYON, STAGE_CENTRAL_CITY, STAGE_BLACK_COMET],
    "Amy": [STAGE_CRYPTIC_CASTLE],
    "Eggman": [STAGE_CRYPTIC_CASTLE, STAGE_CIRCUS_PARK, STAGE_SKY_TROOPS,
               STAGE_IRON_JUNGLE, STAGE_LAVA_SHELTER],
    "Rouge": [STAGE_DIGITAL_CIRCUIT, STAGE_DEATH_RUINS, STAGE_GUN_FORTRESS],
    "Omega": [STAGE_IRON_JUNGLE, STAGE_LAVA_SHELTER],
    "Doom": [STAGE_WESTOPOLIS, STAGE_DIGITAL_CIRCUIT, STAGE_GLYPHIC_CANYON,
             STAGE_LETHAL_HIGHWAY, STAGE_PRISON_ISLAND, STAGE_CENTRAL_CITY,
             STAGE_THE_DOOM, STAGE_SKY_TROOPS, STAGE_MAD_MATRIX,
             STAGE_DEATH_RUINS, STAGE_THE_ARK, STAGE_AIR_FLEET,
             STAGE_SPACE_GADGET, STAGE_GUN_FORTRESS, STAGE_BLACK_COMET,
             STAGE_COSMIC_FALL, STAGE_FINAL_HAUNT],
    "Espio": [STAGE_MAD_MATRIX],
    "Charmy": [STAGE_PRISON_ISLAND],
    "Vector": [STAGE_COSMIC_FALL],
    "Maria": [STAGE_THE_DOOM, STAGE_LOST_IMPACT]
}

ALL_STAGES = list(LEVEL_ID_TO_LEVEL.keys())

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

