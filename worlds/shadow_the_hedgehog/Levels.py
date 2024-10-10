
SHADOW_THE_HEDGEHOG_GAME_ID = "GUPE8P"

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





def GetLevelCompletionNames(stageId, alignmentId):

    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(alignmentId))
    view_name = LEVEL_ID_TO_LEVEL[stageId] + " Mission Clear " + ALIGNMENT_TO_STRING[alignmentId]

    return id_name, view_name

def GetLevelObjectNames(stageId, alignmentId, objectName, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(alignmentId) + str(i))
    objective_location_name = (LEVEL_ID_TO_LEVEL[stageId] + "-" +
                               objectName + " " + str(i))

    return id_name, objective_location_name