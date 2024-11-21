import copy
from dataclasses import dataclass
from typing import List, Optional

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from worlds.shadow_the_hedgehog import Locations
from worlds.shadow_the_hedgehog.Levels import LEVEL_ID_TO_LEVEL, ALL_STAGES, MISSION_ALIGNMENT_DARK, \
    MISSION_ALIGNMENT_HERO, MISSION_ALIGNMENT_NEUTRAL, ITEM_TOKEN_TYPE_STANDARD, ITEM_TOKEN_TYPE_FINAL, \
    ITEM_TOKEN_TYPE_OBJECTIVE, ITEM_TOKEN_TYPE_ALIGNMENT
from worlds.shadow_the_hedgehog.Locations import MissionClearLocations, GetAlignmentsForStage

BASE_ID = 1743800000
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
    stageId: Optional[int | None]
    alignmentId: Optional[int | None]
    type: str
    value: Optional[int | None]


class Progression:
    GoodbyeForever = "Goodbye Forever"
    WhiteEmerald = "White Chaos Emerald"
    RedEmerald = "Red Chaos Emerald"
    CyanEmerald = "Cyan Chaos Emerald"
    PurpleEmerald = "Purple Chaos Emerald"
    GreenEmerald = "Green Chaos Emerald"
    YellowEmerald = "Damn Fourth Chaos Emerald"
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

GaugeAmounts = [1, 100, 1000, 2000, 5000, 10000, 25000, 50000]
RingAmounts = [1, 2, 5, 10, 20]








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
        for gauge in GaugeAmounts:
            infos.append(ItemInfo(id_s, "Gauge:"+alignment+"-"+str(gauge),ItemClassification.filler,
                                  None, MISSION_ALIGNMENT_DARK if alignment == "Dark"
                                  else MISSION_ALIGNMENT_HERO, "gauge", gauge))
            id_s += 1

    return infos

def GetRingItems():
    id_s = ITEM_ID_START_AT_JUNK+50
    infos = []
    for ring in RingAmounts:
        infos.append(ItemInfo(id_s, str(ring) + " Ring" + ("" if ring == 1 else "s") ,ItemClassification.filler,
                              None, None, "rings", ring))
        id_s += 1

    return infos

# The order here matters
def GetSpecialWeapons():
    id_s = ITEM_ID_START_AT_JUNK + 100
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


def GetJunkItemInfo():
    junk_items = []

    nothing = ItemInfo(ITEM_ID_START_AT_JUNK, Junk.NothingJunk, ItemClassification.filler, None, None, "Junk", None)
    junk_items.append(nothing)

    gauge_items = GetGaugeItems()
    junk_items.extend(gauge_items)

    ring_items = GetRingItems()
    junk_items.extend(ring_items)

    special_weapons = GetSpecialWeapons()
    junk_items.extend(special_weapons)

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

    return emerald_items, key_items, level_unlock_items, stage_objective_items, junk_items, token_items

useful_to_count = {
    "Egg Vacuum": 2,
    "Satellite Gun": 2,
    "Samurai Blade": 2,
    "Omochao Gun": 2,
    "Shadow Rifle": 1
}

def ChooseJunkItem(random, junk):
    junk_not_useful = [ j for j in junk if j.classification != ItemClassification.useful]

    # TODO: Add a distribution

    return random.choice(junk_not_useful)


def PopulateItemPool(world : World, first_regions):
    # TODO: Do not add item for stages you start with
    (emerald_items, key_items, level_unlock_items, stage_objective_items,
     junk_items, token_items) = GetAllItemInfo()

    if not world.options.objective_sanity:
        stage_objective_items = []

    # Don't use level unlocks for stages you start with!
    use_level_unlock_items = [ l for l in level_unlock_items if l.stageId not in first_regions and
                               LEVEL_ID_TO_LEVEL[l.stageId] not in world.options.excluded_stages]

    # Convert to multiworld items
    mw_em_items = [ ShadowTheHedgehogItem(e, world.player) for e in emerald_items]
    mw_level_unlock_items = [ ShadowTheHedgehogItem(l,world.player) for l in use_level_unlock_items ]
    mw_stage_items =  [ ShadowTheHedgehogItem(s, world.player) for s in stage_objective_items if
                        LEVEL_ID_TO_LEVEL[s.stageId] not in world.options.excluded_stages]

    item_count = len(mw_em_items) + len(mw_level_unlock_items) + len(mw_stage_items) + 1 # end item
    location_count = Locations.count_locations(world)

    mw_useful_items = []
    junk_but_useful = [ j for j in junk_items if j.classification == ItemClassification.useful ]
    for item in junk_but_useful:
        if item.name in useful_to_count:
            mw_useful_items.extend([ ShadowTheHedgehogItem(item, world.player) for _ in range(0, useful_to_count[item.name])])

    junk_items = [ ShadowTheHedgehogItem(
       ChooseJunkItem(world.random, junk_items), world.player) for _ in range(0, location_count - item_count - len(mw_useful_items))]

    world.multiworld.itempool += mw_em_items
    world.multiworld.itempool += mw_level_unlock_items
    world.multiworld.itempool += mw_stage_items
    world.multiworld.itempool += mw_useful_items
    world.multiworld.itempool += junk_items



