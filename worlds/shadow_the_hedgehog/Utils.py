from math import ceil
from typing import Tuple

from . import Levels, Locations

VERSION: Tuple[int, int, int] = (0, 0, 8)

TYPE_ID_ENEMY = 0
TYPE_ID_OBJECTIVE = 1
TYPE_ID_COMPLETION = 2
TYPE_ID_AVAILABLE = 3

def GetVersionString():
    return f"{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"
def getRequiredCount(total, percentage,
                     round_method=ceil,
                     override=None):

    if override is not None:
        percentage = override

    required_count = round_method(total * percentage / 100)
    if required_count == 0:
        required_count += 1

    return int(required_count)

def getOverwriteKeys():
    pass

def getOverwriteRequiredCount(override_settings, stageId, alignmentId, typeId):
    key = "{type}.{stageName}"
    type_name = "O"

    if typeId == TYPE_ID_ENEMY:
        if alignmentId == Locations.ENEMY_CLASS_ALIEN:
            type_name = "EA"
        elif alignmentId == Locations.ENEMY_CLASS_GUN:
            type_name = "EG"
        elif alignmentId == Locations.ENEMY_CLASS_EGG:
            type_name = "EE"
    elif typeId == TYPE_ID_OBJECTIVE:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OH"
    elif typeId == TYPE_ID_COMPLETION:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "CD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "CH"
    elif typeId == TYPE_ID_AVAILABLE:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "AD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "AH"

    level_name = Levels.LEVEL_ID_TO_LEVEL[stageId]
    key_lookup = key.format(type=type_name, stageName=level_name)

    if key_lookup in override_settings:
        return override_settings[key_lookup]

    return None