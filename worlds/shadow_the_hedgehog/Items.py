#from __future__ import annotations
import copy
import typing
from dataclasses import dataclass
from math import floor, ceil
from typing import List, Optional


from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from . import Locations, Weapons, Vehicle, Utils as ShadowUtils, Options, Levels
from .Levels import LEVEL_ID_TO_LEVEL, ALL_STAGES, MISSION_ALIGNMENT_DARK, \
    MISSION_ALIGNMENT_HERO, MISSION_ALIGNMENT_NEUTRAL, ITEM_TOKEN_TYPE_STANDARD, ITEM_TOKEN_TYPE_FINAL, \
    ITEM_TOKEN_TYPE_OBJECTIVE, ITEM_TOKEN_TYPE_ALIGNMENT, BOSS_STAGES, LAST_STORY_STAGES, ITEM_TOKEN_TYPE_BOSS, \
    ITEM_TOKEN_TYPE_FINAL_BOSS
from .Locations import MissionClearLocations, GetAlignmentsForStage

BASE_ID = 1743800000
ITEM_ID_START_AT_WEAPONS = 2000
ITEM_ID_START_AT_VEHICLES = 2500
ITEM_ID_START_AT_RIFLE = 2600
ITEM_ID_START_AT_JUNK = 3000
ITEM_ID_START_AT_MISSION = 1000
ITEM_ID_START_AT_IMPORTANT = 10
ITEM_ID_START_AT_LEVEL = 100
ITEM_ID_START_AT_WARP = 150
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
    BossToken = "Boss Token"
    FinalBossToken = "Final Boss Token"

    #FinalHeroToken = "Final Hero Token"
    #FinalDarkToken = "Final Dark Token"
    #ObjectiveDarkToken = "Objective Dark Token"
    #ObjectiveHeroToken = "Objective Hero Token"

class ShadowRifleComponents:
    ShadowRifleBarrel = "Shadow Rifle Barrel"
    ShadowRifleAction = "Shadow Rifle Action"
    ShadowRifleStock = "Shadow Rifle Stock"
    ShadowRifleReceiver = "Shadow Rifle Receiver"
    ShadowRifleMagazine = "Shadow Rifle Magazine"

TOKENS = [
    Progression.StandardHeroToken, Progression.StandardDarkToken, Progression.StandardMissionToken,
    #Progression.FinalHeroToken, Progression.ObjectiveDarkToken,
    #Progression.FinalDarkToken, Progression.ObjectiveHeroToken,
    Progression.FinalToken, Progression.ObjectiveToken, Progression.BossToken, Progression.FinalBossToken
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
        if "Boss" in token:
            type = ITEM_TOKEN_TYPE_BOSS

        if "Final Boss" in token:
            type = ITEM_TOKEN_TYPE_FINAL_BOSS

        if "Final" in token and "Final Boss" not in token:
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
        #if stageId in BOSS_STAGES or stageId in LAST_STORY_STAGES:
        #    continue

        if stageId == Levels.BOSS_DEVIL_DOOM:
            continue

        item = ItemInfo(count, GetStageUnlockItem(stageId), ItemClassification.progression, stageId=stageId,
                        alignmentId=None, type="level_unlock", value=None)
        count += 1
        level_unlock_items.append(item)

    return level_unlock_items

# Upon entering a level, provide the player with a key
def PopulateLevelWarpPoints():
    level_warp_points = []
    count = ITEM_ID_START_AT_WARP
    for stageId in ALL_STAGES:
        item = ItemInfo(count, GetStageWarpItem(stageId), ItemClassification.progression, stageId=stageId,
                        alignmentId=None, type="level_warp", value=None)
        count += 1
        level_warp_points.append(item)

    return level_warp_points


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

def GetStageWarpItem(stageId):
    return "Warp:"+LEVEL_ID_TO_LEVEL[stageId]


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
            None, None, "Weapon", weapon.game_id)
        )

    return weapons


def GetWeaponGroups():
    weapons_count = len(GetWeapons())
    id_s = ITEM_ID_START_AT_WEAPONS + weapons_count
    weapon_groups = []

    for weapon_group in Weapons.WeaponGroups.keys():
        weapon_groups.append(
            ItemInfo(id_s + len(weapon_groups), weapon_group, ItemClassification.progression,
                     None, None, "WeaponGroup", None)
        )

    return weapon_groups


def GetVehicles():
    id_s = ITEM_ID_START_AT_VEHICLES
    vehicles = []
    for vehicle in Vehicle.VEHICLE_INFO:
        vehicles.append(
            ItemInfo(id_s + len(vehicles), vehicle.name, ItemClassification.progression,
                     None, None, "Vehicle", None)
        )

    return vehicles


def GetRifleComponents():
    id_s = ITEM_ID_START_AT_RIFLE
    rifle_components = []
    for rifle_name in ShadowRifleComponents.__dict__.keys():
        if "ShadowRifle" in rifle_name:
            rifle_components.append(ItemInfo(id_s + len(rifle_components), ShadowRifleComponents.__dict__[rifle_name], ItemClassification.progression,
                     None, None, "Rifle Component", None)
        )

    return rifle_components


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
    level_warp_item_table = PopulateLevelWarpPoints()

    stage_progression_item_table: List[ItemInfo] = PopulateLevelObjectItems()

    emerald_items = GetEmeraldItems()
    key_items = [GetFinalItem()]

    level_unlock_items = []
    for unlock in level_unlocks_item_table:
        level_unlock_items.append(unlock)

    level_warp_items = []
    for warp in level_warp_item_table:
        level_warp_items.append(warp)

    stage_objective_items = []
    for item in stage_progression_item_table:
        stage_objective_items.append(item)

        #lookup = [x for x in MissionClearLocations
         #         if x.stageId == reference_stage and x.alignmentId == reference_alignment][0]

        #for i in range(0, lookup.requirement_count):


    junk_items = GetJunkItemInfo()
    token_items = GetLevelTokenItems()
    weapon_items = GetWeapons()
    weapon_group_items = GetWeaponGroups()
    vehicle_items = GetVehicles()

    rifle_components = GetRifleComponents()

    return (emerald_items, key_items, level_unlock_items, stage_objective_items, junk_items,
            token_items, weapon_items, vehicle_items, level_warp_items, rifle_components,
            weapon_group_items)

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
            junk_distribution[total+1] = c
            total += 2

    if options.enable_ring_items:
        for r,c in RingAmounts.items():
            r_item = [j for j in junk if j.type == "rings" and j.value == r][0]
            junk_distribution[total] = c
            junk_items.append(r_item)
            total += 1

    NothingJunk = [ j for j in junk if j.type == "Junk"][0]
    junk_items.append(NothingJunk)
    junk_distribution[total] = 1
    total += 1

    randomised_indicies = random.choices(list(junk_distribution.keys()), k=junk_count, weights=list(junk_distribution.values()))
    return [ junk_items[k] for k in randomised_indicies]

def CountItems(world: World):
    (emerald_items, key_items, level_unlock_items, stage_objective_items_x,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items) = GetAllItemInfo()

    if not world.options.objective_sanity:
        stage_objective_items_x = []

    if not world.options.rifle_components:
        rifle_components = []

    stage_objective_items_full = [ s for s in stage_objective_items_x if s.stageId in world.available_levels ]
    using_stage_objective_items = []

    for item in stage_objective_items_full:

        lookup = [x for x in MissionClearLocations
                  if x.stageId == item.stageId and x.alignmentId == item.alignmentId][0]

        max_available = ShadowUtils.getMaxRequired(
        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE, lookup.mission_object_name,
                                                  world.options),
            lookup.requirement_count, lookup.stageId, lookup.alignmentId, world.options.percent_overrides)

        items =  [item] * max_available
        using_stage_objective_items.extend(items)

    # Don't use level unlocks for stages you start with!
    use_level_unlock_items = [l for l in level_unlock_items if l.stageId in world.available_levels
                              and world.options.level_progression != Options.LevelProgression.option_story]

    if len(use_level_unlock_items) > 0:
        unlock_count = len(use_level_unlock_items) - world.options.starting_stages
    else:
        unlock_count = 0

    weapon_dict = Weapons.GetWeaponDict()
    special_weapon_extras = [w for w in weapon_items if
                             Weapons.WeaponAttributes.SPECIAL in weapon_dict[w.name].attributes and
                             w.name != 'Shadow Rifle' and w.name != "Weapon:Shadow Rifle"]

    weapon_items.extend(special_weapon_extras)

    item_count = increment_item_count(0, unlock_count + len(using_stage_objective_items))
    if world.options.goal_chaos_emeralds:
        item_count = increment_item_count(item_count, len(emerald_items))

    HandleAllWeaponsGroups(world.options, weapon_items, weapon_group_items)
    if world.options.weapon_sanity_unlock:
        item_count = increment_item_count(item_count, len(weapon_items))
        if len(rifle_components) > 0:
            item_count = increment_item_count(item_count, len(rifle_components))
    else:
        item_count = increment_item_count(item_count, len(special_weapon_extras) * 2)
        if len(rifle_components) > 0:
            item_count = increment_item_count(item_count, len(rifle_components))
        else:
            item_count = increment_item_count(item_count, 1)

    if world.options.vehicle_logic:
        item_count = increment_item_count(item_count, len(vehicle_items))

    return item_count

def GetPotentialDowngradeItems(world, mw_stage_items=None):
    potential_downgrade = []
    to_remove = []
    if mw_stage_items is None:
        (emerald_items, key_items, level_unlock_items, stage_objective_items,
         junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
         weapon_group_items) = GetAllItemInfo()

        # Handle available

        mw_stage_items = [ShadowTheHedgehogItem(s, world.player) for s in stage_objective_items if
                          s.stageId in world.available_levels]

    override_settings = world.options.percent_overrides
    itemdict = GetItemLookupDict()

    indexer = {}
    for item in mw_stage_items:
        item_lookup = itemdict[item.code]
        lookup = [x for x in MissionClearLocations
                  if x.stageId == item_lookup.stageId and x.alignmentId == item_lookup.alignmentId][0]
        if item_lookup.name not in indexer:
            indexer[item_lookup.name] = 0

        indexer[item_lookup.name] += 1

        max_required_complete = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION, lookup.mission_object_name,
                                                      world.options),
            lookup.requirement_count, lookup.stageId, lookup.alignmentId,
            override_settings)

        max_available = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE, lookup.mission_object_name,
                                                      world.options),
            lookup.requirement_count, lookup.stageId, lookup.alignmentId,
            override_settings)

        if indexer[item_lookup.name] > max_available:
            to_remove.append(item)
        elif indexer[item_lookup.name] > max_required_complete:
            potential_downgrade.append(item)

    return potential_downgrade, to_remove

def GetShadowRifle():
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items) = GetAllItemInfo()

    return [ w for w in weapon_items if w.name == 'Shadow Rifle' or w.name == 'Weapon:Shadow Rifle' ][0]

def HandleAllWeaponsGroups(options, items, group_items):
    if not options.weapon_sanity_unlock:
        return

    weapons_to_remove = []
    for group in Weapons.WeaponGroups.keys():
        if group in options.weapon_groups:
            HandleWeaponGroup(items, group_items, group, weapons_to_remove)

    for weapon in weapons_to_remove:
        if weapon in items:
            items.remove(weapon)

def HandleWeaponGroup(items, group_items, weapon_group_name, weapons_to_remove):
    melee_group = Weapons.WeaponGroups[weapon_group_name]
    weapon_items_to_remove = [w for w in items if w.value in melee_group]

    if len(weapon_items_to_remove) == 0:
        # If no items in the group are available, don't add the group
        return

    weapons_to_remove.extend(weapon_items_to_remove)
    group_item = [w for w in group_items if w.name == weapon_group_name]
    items.extend(group_item)

def increment_item_count(count, plus):
    #print(f"Count={count} + {plus} = {count+plus}")
    return count + plus


def PopulateItemPool(world : World, first_regions):
    # TODO: Do not add item for stages you start with
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items) = GetAllItemInfo()

    if not world.options.objective_sanity:
        stage_objective_items = []

    # Don't use level unlocks for stages you start with!
    use_level_unlock_items = [ l for l in level_unlock_items if l.stageId not in first_regions and
                               l.stageId in world.available_levels
                               #and (l.stageId not in Levels.FINAL_BOSSES
                               and l.stageId not in Levels.LAST_STORY_STAGES
                               and (l.stageId not in Levels.BOSS_STAGES or world.options.select_bosses)
                               and world.options.level_progression != Options.LevelProgression.option_story ]


    # Convert to multiworld items
    mw_em_items = [ ShadowTheHedgehogItem(e, world.player) for e in emerald_items]
    mw_level_unlock_items = [ ShadowTheHedgehogItem(l,world.player) for l in use_level_unlock_items ]

    override_settings = world.options.percent_overrides
    mw_temp_stage_objective_items = []

    for item in stage_objective_items:
        if item.stageId not in world.available_levels:
            continue

        lookup = [x for x in MissionClearLocations
                  if x.stageId == item.stageId and x.alignmentId == item.alignmentId][0]

        max_required = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                      lookup.mission_object_name, world.options),
            lookup.requirement_count, item.stageId, item.alignmentId,
            override_settings)

        mw_temp_stage_objective_items.extend([item] * max_required)

    mw_stage_items = [ShadowTheHedgehogItem(s, world.player) for s in mw_temp_stage_objective_items]

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

    weapon_items = [w for w in weapon_items if
                       w.name != "Weapon:Shadow Rifle" and
                       w.name != "Shadow Rifle"]

    weapon_items.extend(special_weapon_extras)

    available_weapons = [ w for w in weapon_items if w.name in world.available_weapons ]



    HandleAllWeaponsGroups(world.options, available_weapons, weapon_group_items)

    mw_weapon_items = [ ShadowTheHedgehogItem(w, world.player) for w in available_weapons]

    mw_weapon_special_only = [ ShadowTheHedgehogItem(w, world.player) for w in special_weapon_extras ]
    mw_weapon_special_only_dupes = [ShadowTheHedgehogItem(w, world.player) for w in special_weapon_extras]
    mw_weapon_special_only.extend(mw_weapon_special_only_dupes)

    shadow_rifle = GetShadowRifle()
    if not world.options.rifle_components:
        mw_weapon_special_only.append(ShadowTheHedgehogItem(shadow_rifle, world.player))
        mw_weapon_items.append( ShadowTheHedgehogItem(shadow_rifle, world.player))
    else:
        mw_weapon_special_only.extend([ShadowTheHedgehogItem(w, world.player) for w in rifle_components])
        mw_weapon_items.extend([ShadowTheHedgehogItem(w, world.player) for w in rifle_components])

    mw_vehicle_items = [ ShadowTheHedgehogItem(w, world.player) for w in vehicle_items ]

    if world.options.weapon_sanity_unlock and \
        world.options.weapon_sanity_hold != Options.WeaponsanityHold.option_unlocked:
        for weapon in mw_weapon_items:

            matching_w = [ w for w in Weapons.WEAPON_INFO if w.name == weapon.name ]
            if len(matching_w) == 0:
                continue

            if len(matching_w[0].attributes) == 0:
                weapon.classification = ItemClassification.filler
                #print(weapon.name, "is now filler")

    item_count = increment_item_count(0, (len(mw_level_unlock_items) + len(mw_stage_items)))
    if world.options.goal_chaos_emeralds:
        item_count = increment_item_count(item_count, len(mw_em_items))

    if world.options.weapon_sanity_unlock:
        item_count = increment_item_count(item_count, len(mw_weapon_items))
    else:
        item_count = increment_item_count(item_count, len(mw_weapon_special_only))

    if world.options.vehicle_logic:
        item_count = increment_item_count(item_count, len(mw_vehicle_items))

    location_count = Locations.count_locations(world)

    mw_useful_items = []
    junk_but_useful = [ j for j in junk_items if j.classification == ItemClassification.useful ]
    for item in junk_but_useful:
        if item.name in useful_to_count:
            mw_useful_items.extend([ ShadowTheHedgehogItem(item, world.player) for _ in range(0, useful_to_count[item.name])])


    junk_count = location_count - item_count - len(mw_useful_items)
    mw_junk_items = [ ShadowTheHedgehogItem(i, world.player) for i in ChooseJunkItems(world.random, junk_items, world.options, junk_count) ]

    if world.options.goal_chaos_emeralds:
        world.multiworld.itempool += mw_em_items

    world.multiworld.itempool += mw_level_unlock_items
    world.multiworld.itempool += mw_stage_items
    world.multiworld.itempool += mw_useful_items
    world.multiworld.itempool += mw_junk_items

    if world.options.weapon_sanity_unlock:
        world.multiworld.itempool += mw_weapon_items
    else:
        world.multiworld.itempool += mw_weapon_special_only

    if world.options.vehicle_logic:
        world.multiworld.itempool += mw_vehicle_items

def get_item_groups():
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items) = GetAllItemInfo()

    item_groups: typing.Dict[str, list] = {
        "Chaos Emeralds": [ e.name for e in emerald_items],
        "Unlocks": [e.name for e in level_unlock_items],
        "Weapons": [e.name for e in weapon_items],
        "Vehicles": [e.name for e in vehicle_items],
        "Vacuums": [w.name for w in weapon_items if "Vacuum" in w.name ],
        "Rifles": [w.name for w in rifle_components],
        "Junk": [w.name for w in junk_items]
    }

    return item_groups

