from math import ceil, floor
from typing import Tuple

from . import Levels, Locations

VERSION: Tuple[int, int, int] = (0, 1, 5)

TYPE_ID_ENEMY = 0
TYPE_ID_OBJECTIVE = 1
TYPE_ID_COMPLETION = 2
TYPE_ID_OBJECTIVE_AVAILABLE = 3
TYPE_ID_OBJECTIVE_ENEMY = 4
TYPE_ID_OBJECTIVE_ENEMY_COMPLETION = 5
TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE = 6
TYPE_ID_OBJECTIVE_FREQUENCY = 7
TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY = 8
TYPE_ID_ENEMY_FREQUENCY = 9

def GetVersionString():
    return f"{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"
def getRequiredCount(total, percentage,
                     round_method=ceil,
                     override=None):

    if override is not None:
        percentage = override

    required_count = round_method(total * percentage / 100)
    if required_count == 0 and percentage != 0:
        required_count += 1

    return int(required_count)


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
    elif typeId == TYPE_ID_OBJECTIVE_AVAILABLE:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "AD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "AH"
    elif typeId == TYPE_ID_OBJECTIVE_ENEMY:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OED"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OEH"
    elif typeId == TYPE_ID_OBJECTIVE_ENEMY_COMPLETION:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OECD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OECH"

    elif typeId == TYPE_ID_OBJECTIVE_FREQUENCY:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OFD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OFH"

    elif typeId == TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OEFD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OEFH"

    elif typeId == TYPE_ID_ENEMY_FREQUENCY:
        if alignmentId == Locations.ENEMY_CLASS_EGG:
            type_name = "EFE"
        if alignmentId == Locations.ENEMY_CLASS_GUN:
            type_name = "EFG"
        if alignmentId == Locations.ENEMY_CLASS_ALIEN:
            type_name = "EFH"

    level_name = Levels.LEVEL_ID_TO_LEVEL[stageId]
    key_lookup = key.format(type=type_name, stageName=level_name)

    if key_lookup in override_settings:
        return override_settings[key_lookup]

    return None

def isEnemyObjectiveLocation(name):
    if "Soldier" in name or "Alien" in name or "Artificial Chaos" in name:
        return True

    return False

# TODO: Needs to work with percentage as well...
def getObjectiveTypeAndPercentage(base_objective_type, item_name, options):

    if not options.objective_sanity:
        if base_objective_type in (TYPE_ID_OBJECTIVE_AVAILABLE, TYPE_ID_OBJECTIVE,
                                   TYPE_ID_OBJECTIVE_ENEMY,
                                   TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE, TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY,
                                   TYPE_ID_OBJECTIVE_FREQUENCY):
            return None

    percentage = None
    round_method = None
    if base_objective_type == TYPE_ID_OBJECTIVE:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY
            percentage = options.objective_enemy_percentage
            round_method = floor
        else:
            percentage = options.objective_percentage
            round_method = ceil
    if base_objective_type == TYPE_ID_COMPLETION:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY_COMPLETION
            percentage = options.objective_completion_enemy_percentage
            round_method = floor
        else:
            percentage = options.objective_completion_percentage
            round_method = floor
    if base_objective_type == TYPE_ID_OBJECTIVE_AVAILABLE:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE
            percentage = options.objective_item_enemy_percentage_available
            round_method = ceil
        else:
            percentage = options.objective_item_percentage_available
            round_method = ceil

    if base_objective_type in (TYPE_ID_OBJECTIVE_AVAILABLE, TYPE_ID_OBJECTIVE,
                               TYPE_ID_COMPLETION, TYPE_ID_OBJECTIVE_ENEMY,
                               TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE, TYPE_ID_OBJECTIVE_ENEMY_COMPLETION,
                               TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY, TYPE_ID_OBJECTIVE_FREQUENCY):
        if isEnemyObjectiveLocation(item_name):
            if not options.enemy_objective_sanity:
                return base_objective_type, 0, floor


    if base_objective_type == TYPE_ID_ENEMY:
        percentage = options.enemy_sanity_percentage
        round_method = floor

    if base_objective_type == TYPE_ID_ENEMY_FREQUENCY:
        percentage = options.enemy_frequency
        round_method = floor

    if base_objective_type == TYPE_ID_OBJECTIVE_FREQUENCY:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY
            percentage = options.enemy_objective_frequency
            round_method = floor
        else:
            percentage = options.objective_frequency
            round_method = floor

    return base_objective_type, percentage, round_method


def FrequencyPercentageToIncrementer(perc, round_method):
    if perc == 0:
        return None

    base = 100 / perc
    rounded = round_method(base)
    if rounded == 0:
        return 1

    return rounded

def getMaxRequired(type_default_percentage, total:int, stageId:int, alignmentId:int, override_settings):
    if type_default_percentage is None:
        #print("Type percentage is None: Return 100%")
        return total

    type_value = type_default_percentage[0]
    default_percentage = type_default_percentage[1]
    round_method = type_default_percentage[2]

    override_total = getOverwriteRequiredCount(override_settings, stageId, alignmentId, type_value)
    max_required = getRequiredCount(total, default_percentage, override=override_total, round_method=round_method)

    if type_value in [ TYPE_ID_ENEMY_FREQUENCY, TYPE_ID_OBJECTIVE_FREQUENCY, TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY]:
        return FrequencyPercentageToIncrementer(max_required, round_method)

    return max_required