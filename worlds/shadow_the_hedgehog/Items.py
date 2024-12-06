#from __future__ import annotations
import copy
import typing
from dataclasses import dataclass
from math import floor, ceil
from typing import List, Optional


from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from . import Locations, Weapons, Vehicle, Utils as ShadowUtils, Options
from .Levels import LEVEL_ID_TO_LEVEL, ALL_STAGES, MISSION_ALIGNMENT_DARK, \
    MISSION_ALIGNMENT_HERO, MISSION_ALIGNMENT_NEUTRAL, ITEM_TOKEN_TYPE_STANDARD, ITEM_TOKEN_TYPE_FINAL, \
    ITEM_TOKEN_TYPE_OBJECTIVE, ITEM_TOKEN_TYPE_ALIGNMENT, BOSS_STAGES, BANNED_AVAILABLE_STAGES
from .Locations import MissionClearLocations, GetAlignmentsForStage

BASE_ID = 1743800000
ITEM_ID_START_AT_WEAPONS = 2000
ITEM_ID_START_AT_VEHICLES = 2500
ITEM_ID_START_AT_JUNK = 3000
ITEM_ID_START_AT_MISSION = 1000
ITEM_ID_START_AT_IMPORTANT = 10
ITEM_ID_START_AT_LEVEL = 100
ID_START_AT_OTHER = 0
ITEM_ID_START_AT_TOKEN = 5000



@dataclass
class ItemInfo:
    itemId: int
    name: str
    classification: ItemClassification
    stageId: Optional[int]
    alignmentId: Optional[int]
    type: str
    value: Optional[int]


class Progression:
    GoodbyeForever = "Goodbye Forever"
    WhiteEmerald = "White Chaos Emerald"
    RedEmerald = "Red Chaos Emerald"
    CyanEmerald = "Cyan Chaos Emerald"
    PurpleEmerald = "Purple Chaos Emerald"
    GreenEmerald = "Green Chaos Emerald"
    YellowEmerald = "Yellow Chaos Emerald"
    BlueEmerald = "Blue Chaos Emerald"

    StandardHeroToken = "Hero Token"
    StandardDarkToken = "Dark Token"
    StandardMissionToken = "Mission Token"
    FinalToken = "Final Token"
    ObjectiveToken = "Objective Token"

    #FinalHeroToken = "Final Hero Token"
    #FinalDarkToken = "Final Dark Token"
    #ObjectiveDarkToken = "Objective Dark Token"
    #ObjectiveHeroToken = "Objective Hero Token"

TOKENS = [
    Progression.StandardHeroToken, Progression.StandardDarkToken, Progression.StandardMissionToken,
    #Progression.FinalHeroToken, Progression.ObjectiveDarkToken,
    #Progression.FinalDarkToken, Progression.ObjectiveHeroToken,
    Progression.FinalToken, Progression.ObjectiveToken
]

    # TODO: Add boss token

class Junk:
    NothingJunk = "Nothing Junk"

#GaugeAmounts = [1, 1000, 2000, 5000, 10000, 15000, 20000, 30000]
#RingAmounts = [1, 2, 5, 10, 20]

GaugeAmounts = \
{
    1: 1,
    5: 1,
    100: 5,
    500: 10,
    1000: 20,
    2000: 20,
    5000: 10,
    10000: 10,
    15000: 5,
    20000: 2,
    30000: 1
}

RingAmounts = \
{
    1: 10,
    2: 10,
    5: 20,
    10: 20,
    20: 10
}








def GetLevelTokenItems():
    id_iterator = ITEM_ID_START_AT_TOKEN
    level_token_items = []
    for token in TOKENS:
        alignment = MISSION_ALIGNMENT_NEUTRAL

        type = ITEM_TOKEN_TYPE_STANDARD
        if "Final" in token:
            type = ITEM_TOKEN_TYPE_FINAL
        if "Objective" in token:
            type = ITEM_TOKEN_TYPE_OBJECTIVE
        if "Dark" in token:
            type = ITEM_TOKEN_TYPE_ALIGNMENT
            alignment = MISSION_ALIGNMENT_DARK
        elif "Hero" in token:
            type = ITEM_TOKEN_TYPE_ALIGNMENT
            alignment = MISSION_ALIGNMENT_HERO


        i = ItemInfo(id_iterator,token, ItemClassification.progression, None, alignment, "Token", type)
        id_iterator += 1
        level_token_items.append(i)

    return level_token_items



def PopulateLevelUnlockItems():
    level_unlock_items = []
    count = ITEM_ID_START_AT_LEVEL
    for stageId in ALL_STAGES:
        if stageId in BOSS_STAGES or stageId in BANNED_AVAILABLE_STAGES:
            continue
        item = ItemInfo(count, GetStageUnlockItem(stageId), ItemClassification.progression, stageId=stageId,
                        alignmentId=None, type="level_unlock", value=None)
        count += 1
        level_unlock_items.append(item)

    return level_unlock_items


def PopulateLevelObjectItems():
    level_object_items = []
    count = ITEM_ID_START_AT_MISSION
    for stageId in ALL_STAGES:
        # TODO: handling for stages without a particular mission type
        alignment_ids = GetAlignmentsForStage(stageId)
        for alignment in alignment_ids:
            alignment_object = GetStageAlignmentObject(stageId, alignment)
            if alignment_object is None:
                continue
            item = ItemInfo(count, alignment_object, ItemClassification.progression,
                            stageId=stageId, alignmentId=alignment, type="level_object", value=None)
            count += 1
            level_object_items.append(item)

    return level_object_items

def GetStageAlignmentObject(stageId, alignmentId):
    i = [ m for m in MissionClearLocations if m.stageId == stageId and m.alignmentId == alignmentId]
    if len(i) == 0:
        return None

    item = i[0]
    if item.mission_object_name is None:
        return None

    return LEVEL_ID_TO_LEVEL[stageId] + " " + item.mission_object_name

def GetStageUnlockItem(stageId):
    return "Stage:"+LEVEL_ID_TO_LEVEL[stageId]



class ShadowTheHedgehogItem(Item):
    game: str = "Shadow The Hedgehog"

    def __init__(self, item: ItemInfo, player):
        #item = item_name_to_info[name]
        super().__init__(item.name, item.classification, item.itemId + BASE_ID, player)




def GetFinalItem():
    info = ItemInfo(ITEM_ID_START_AT_IMPORTANT, Progression.GoodbyeForever,
                    ItemClassification.progression, None, None, type="final", value=None)
    return info

def GetEmeraldItems():
    emeralds: List[ItemInfo] = [
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+1, Progression.WhiteEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+2, Progression.CyanEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+3, Progression.RedEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+4, Progression.GreenEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+5, Progression.BlueEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+6, Progression.PurpleEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT+7, Progression.YellowEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None)
    ]

    return emeralds

def GetItemDict():
    all_items = GetAllItemInfo()

    result = {}
    for item_type in all_items:
        for item in item_type:
            result[item.name] = item.itemId + BASE_ID

    return result

def GetItemLookupDict():
    all_items = GetAllItemInfo()

    result = {}
    for item_type in all_items:
        for item in item_type:
            result[item.itemId + BASE_ID] = item

    return result

def GetItemByName(name):
    d = GetItemLookupDict()
    name_map = {v.name: v for k, v in d.items()}
    return name_map[name]

def GetGaugeItems():
    id_s = ITEM_ID_START_AT_JUNK+1
    infos = []
    alignments = ["Hero", "Dark"]
    for alignment in alignments:
        for gauge in GaugeAmounts.keys():
            infos.append(ItemInfo(id_s, "Gauge:"+alignment+"-"+str(gauge),ItemClassification.filler,
                                  None, MISSION_ALIGNMENT_DARK if alignment == "Dark"
                                  else MISSION_ALIGNMENT_HERO, "gauge", gauge))
            id_s += 1

    return infos

def GetRingItems():
    id_s = ITEM_ID_START_AT_JUNK+50
    infos = []
    for ring in RingAmounts.keys():
        infos.append(ItemInfo(id_s, str(ring) + " Ring" + ("" if ring == 1 else "s") ,ItemClassification.filler,
                              None, None, "rings", ring))
        id_s += 1

    return infos

# The order here matters
def GetSpecialWeapons():
    id_s = ITEM_ID_START_AT_WEAPONS
    weapons = []

    weapons.append(
        ItemInfo(id_s + 3, "Samurai Blade", ItemClassification.useful,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 2, "Satellite Gun", ItemClassification.useful,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 1, "Egg Vacuum", ItemClassification.useful,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 4, "Omochao Gun", ItemClassification.useful,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 5, "Heal Cannon", ItemClassification.useful,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 6, "Shadow Rifle", ItemClassification.useful,
                 None, None, "SpecialWeapon", None)
    )


    return weapons


def GetWeapons():
    id_s = ITEM_ID_START_AT_WEAPONS
    weapons = []
    for weapon in Weapons.WEAPON_INFO:
        weapons.append(
            ItemInfo(id_s + len(weapons), weapon.name, ItemClassification.progression,
            None, None, "Weapon", None)
        )

    return weapons


def GetVehicles():
    id_s = ITEM_ID_START_AT_VEHICLES
    vehicles = []
    for vehicle in Vehicle.VEHICLE_INFO:
        vehicles.append(
            ItemInfo(id_s + len(vehicles), vehicle.name, ItemClassification.progression,
                     None, None, "Vehicle", None)
        )

    return vehicles


def GetJunkItemInfo():
    junk_items = []

    nothing = ItemInfo(ITEM_ID_START_AT_JUNK, Junk.NothingJunk, ItemClassification.filler, None, None, "Junk", None)
    junk_items.append(nothing)

    gauge_items = GetGaugeItems()
    junk_items.extend(gauge_items)

    ring_items = GetRingItems()
    junk_items.extend(ring_items)

    #special_weapons = GetSpecialWeapons()
    #junk_items.extend(special_weapons)

    return junk_items



def GetAllItemInfo():
    level_unlocks_item_table: List[ItemInfo] = PopulateLevelUnlockItems()
    stage_progression_item_table: List[ItemInfo] = PopulateLevelObjectItems()

    emerald_items = GetEmeraldItems()
    key_items = [GetFinalItem()]

    level_unlock_items = []
    for unlock in level_unlocks_item_table:
        level_unlock_items.append(unlock)

    stage_objective_items = []
    for item in stage_progression_item_table:
        reference_stage = item.stageId
        reference_alignment = item.alignmentId

        lookup = [x for x in MissionClearLocations
                  if x.stageId == reference_stage and x.alignmentId == reference_alignment][0]

        for i in range(0, lookup.requirement_count):
            stage_objective_items.append(item)

    junk_items = GetJunkItemInfo()
    token_items = GetLevelTokenItems()
    weapon_items = GetWeapons()
    vehicle_items = GetVehicles()

    return (emerald_items, key_items, level_unlock_items, stage_objective_items, junk_items,
            token_items, weapon_items, vehicle_items)

useful_to_count = {
    "Egg Vacuum": 2,
    "Satellite Gun": 2,
    "Samurai Blade": 2,
    "Omochao Gun": 2,
    "Heal Cannon": 2,
    "Shadow Rifle": 1
}

def ChooseJunkItems(random, junk, options, junk_count):

    junk_distribution = {}

    junk_items = []
    total = 0
    if options.enable_gauge_items:
        for g,c in GaugeAmounts.items():
            g_item_dark = [ j for j in junk if j.type == "gauge" and j.value == g and j.alignmentId == MISSION_ALIGNMENT_DARK][0]
            g_item_hero = [j for j in junk if j.type == "gauge" and j.value == g and j.alignmentId == MISSION_ALIGNMENT_HERO][0]
            junk_items.append(g_item_dark)
            junk_items.append(g_item_hero)
            junk_distribution[total] = c
            total += 2

    for r,c in RingAmounts.items():
        r_item = [j for j in junk if j.type == "rings" and j.value == r][0]
        junk_distribution[total] = c
        junk_items.append(r_item)
        total += 1

    randomised_indicies = random.choices(list(junk_distribution.keys()), k=junk_count, weights=list(junk_distribution.values()))
    return [ junk_items[k] for k in randomised_indicies]

def CountItems(world: World):
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items) = GetAllItemInfo()

    if not world.options.objective_sanity:
        stage_objective_items = []

    stage_objective_items = [ s for s in stage_objective_items if s.stageId in world.available_levels ]

    # Don't use level unlocks for stages you start with!
    use_level_unlock_items = [l for l in level_unlock_items if l.stageId in world.available_levels
                              and world.options.level_progression != Options.LevelProgression.option_story]

    weapon_dict = Weapons.GetWeaponDict()
    special_weapon_extras = [w for w in weapon_items if
                             Weapons.WeaponAttributes.SPECIAL in weapon_dict[w.name].attributes and
                             w.name != 'Shadow Rifle']

    weapon_items.extend(special_weapon_extras)

    item_count = (len(use_level_unlock_items) + len(stage_objective_items) + 1)  # end item
    if world.options.goal_chaos_emeralds:
        item_count += len(emerald_items)

    if world.options.weapon_sanity_unlock:
        item_count += len(weapon_items)
    else:
        item_count += len(special_weapon_extras) * 2

    if world.options.vehicle_logic:
        item_count += len(vehicle_items)

    return item_count

def GetPotentialDowngradeItems(world, mw_stage_items=None):
    potential_downgrade = []
    to_remove = []
    if mw_stage_items is None:
        (emerald_items, key_items, level_unlock_items, stage_objective_items,
         junk_items, token_items, weapon_items, vehicle_items) = GetAllItemInfo()

        # Handle available

        mw_stage_items = [ShadowTheHedgehogItem(s, world.player) for s in stage_objective_items if
                          s.stageId in world.available_levels]

    percentage = world.options.objective_item_percentage.value
    override_settings = world.options.percent_overrides

    itemdict = GetItemLookupDict()
    percentage_available = world.options.objective_item_percentage_available.value

    indexer = {}
    for item in mw_stage_items:
        item_lookup = itemdict[item.code]
        lookup = [x for x in MissionClearLocations
                  if x.stageId == item_lookup.stageId and x.alignmentId == item_lookup.alignmentId][0]
        if item_lookup.name not in indexer:
            indexer[item_lookup.name] = 0

        indexer[item_lookup.name] += 1

        override_total = ShadowUtils.getOverwriteRequiredCount(override_settings, lookup.stageId,
                                                         lookup.alignmentId, ShadowUtils.TYPE_ID_COMPLETION)

        override_available = ShadowUtils.getOverwriteRequiredCount(override_settings, lookup.stageId,
                                                         lookup.alignmentId, ShadowUtils.TYPE_ID_AVAILABLE)

        max_required = ShadowUtils.getRequiredCount(lookup.requirement_count, percentage,
                                                    override=override_total, round_method=ceil)
        max_available = ShadowUtils.getRequiredCount(lookup.requirement_count, percentage_available,
                                                     override=override_available, round_method=ceil)
        if indexer[item_lookup.name] > max_available:
            print("Removal of item:", item.name, indexer[item_lookup.name], override_total, override_available,
                  max_required, max_available)
            to_remove.append(item)
        elif indexer[item_lookup.name] > max_required:
            potential_downgrade.append(item)

    return potential_downgrade, to_remove

def PopulateItemPool(world : World, first_regions):
    # TODO: Do not add item for stages you start with
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items) = GetAllItemInfo()

    if not world.options.objective_sanity:
        stage_objective_items = []

    # Don't use level unlocks for stages you start with!
    use_level_unlock_items = [ l for l in level_unlock_items if l.stageId not in first_regions and
                               l.stageId in world.available_levels
                               and world.options.level_progression != Options.LevelProgression.option_story ]

    # Convert to multiworld items
    mw_em_items = [ ShadowTheHedgehogItem(e, world.player) for e in emerald_items]
    mw_level_unlock_items = [ ShadowTheHedgehogItem(l,world.player) for l in use_level_unlock_items ]

    override_settings = world.options.percent_overrides

    item_duper = []
    for item in stage_objective_items:
        if item.name in item_duper:
            continue
        item_duper.append(item.name)

        override_total = ShadowUtils.getOverwriteRequiredCount(override_settings, item.stageId,
                                                               item.alignmentId, ShadowUtils.TYPE_ID_COMPLETION)

        lookup = [x for x in MissionClearLocations
                  if x.stageId == item.stageId and x.alignmentId == item.alignmentId][0]
        if override_total is not None and override_total > 100:
            max_required = ShadowUtils.getRequiredCount(lookup.requirement_count, None,
                                                        override=override_total, round_method=ceil)

            for i in range(0, max_required - lookup.requirement_count):
                i_item = copy.copy(item)
                stage_objective_items.append(i_item)



    mw_stage_items = [ShadowTheHedgehogItem(s, world.player) for s in stage_objective_items if
                      s.stageId in world.available_levels]

    potential_downgrade = []
    to_remove = []
    downgrade_count = 0
    if world.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_always:
        downgrade_count = 1000
    elif world.excess_item_count > 0:
        downgrade_count = world.excess_item_count

    potential_downgrade, to_remove = GetPotentialDowngradeItems(world,mw_stage_items)
    if downgrade_count > len(potential_downgrade):
        downgrade_count = len(potential_downgrade)

    if downgrade_count > 0:
        for downgrade in potential_downgrade:
            if potential_downgrade.index(downgrade) > downgrade_count:
                break

            downgrade.classification = ItemClassification.useful

    for remove in to_remove:
        mw_stage_items.remove(remove)

    weapon_dict = Weapons.GetWeaponDict()
    special_weapon_extras = [w for w in weapon_items if
                             Weapons.WeaponAttributes.SPECIAL in weapon_dict[w.name].attributes and
                             w.name != 'Shadow Rifle' and w.name != 'Weapon:Shadow Rifle']

    weapon_items.extend(special_weapon_extras)
    mw_weapon_items = [ ShadowTheHedgehogItem(w, world.player) for w in weapon_items ]

    mw_weapon_special_only = [ ShadowTheHedgehogItem(w, world.player) for w in special_weapon_extras ]
    mw_weapon_special_only_dupes = [ShadowTheHedgehogItem(w, world.player) for w in special_weapon_extras]
    mw_weapon_special_only.extend(mw_weapon_special_only_dupes)

    mw_vehicle_items = [ ShadowTheHedgehogItem(w, world.player) for w in vehicle_items ]

    item_count = (len(mw_level_unlock_items) + len(mw_stage_items) + 1) # end item
    if world.options.goal_chaos_emeralds:
        item_count += len(mw_em_items)

    if world.options.weapon_sanity_unlock:
        item_count += len(mw_weapon_items)
    else:
        item_count += len(mw_weapon_special_only)

    if world.options.vehicle_logic:
        item_count += len(mw_vehicle_items)

    location_count = Locations.count_locations(world)

    mw_useful_items = []
    junk_but_useful = [ j for j in junk_items if j.classification == ItemClassification.useful ]
    for item in junk_but_useful:
        if item.name in useful_to_count:
            mw_useful_items.extend([ ShadowTheHedgehogItem(item, world.player) for _ in range(0, useful_to_count[item.name])])

    #junk_items = [ ShadowTheHedgehogItem(

    junk_count = location_count - item_count - len(mw_useful_items)
    print("Create junk items:", junk_count)
    mw_junk_items = [ ShadowTheHedgehogItem(i, world.player) for i in ChooseJunkItems(world.random, junk_items, world.options, junk_count) ]

    if world.options.goal_chaos_emeralds:
        world.multiworld.itempool += mw_em_items

    world.multiworld.itempool += mw_level_unlock_items
    world.multiworld.itempool += mw_stage_items
    world.multiworld.itempool += mw_useful_items
    world.multiworld.itempool += mw_junk_items

    # TODO: Make this work!
    #if False:
    if world.options.weapon_sanity_unlock:
        world.multiworld.itempool += mw_weapon_items
    else:
        world.multiworld.itempool += mw_weapon_special_only

    if world.options.vehicle_logic:
        world.multiworld.itempool += mw_vehicle_items

def get_item_groups():
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items) = GetAllItemInfo()

    item_groups: typing.Dict[str, list] = {
        "Chaos Emeralds": [ e.name for e in emerald_items],
        "Stage Items": [e.name for e in level_unlock_items],
        "Weapons": [e.name for e in weapon_items],
        "Vehicles": [e.name for e in vehicle_items],
        "Vacuums": [w.name for w in weapon_items if "Vacuum" in w.name ]
    }

    return item_groups

