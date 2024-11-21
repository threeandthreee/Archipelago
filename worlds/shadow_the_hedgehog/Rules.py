from math import ceil

from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from worlds.shadow_the_hedgehog import Items, Levels, LEVEL_ID_TO_LEVEL, CharacterToLevel, ITEM_TOKEN_TYPE_FINAL, \
    MISSION_ALIGNMENT_DARK, MISSION_ALIGNMENT_HERO, MISSION_ALIGNMENT_NEUTRAL, ITEM_TOKEN_TYPE_OBJECTIVE, \
    ITEM_TOKEN_TYPE_STANDARD, ITEM_TOKEN_TYPE_ALIGNMENT
from worlds.shadow_the_hedgehog.Items import ShadowTheHedgehogItem, GetLevelTokenItems
from worlds.shadow_the_hedgehog.Locations import MissionClearLocations, GetAllLocationInfo, LocationInfo
from worlds.shadow_the_hedgehog.Regions import character_name_to_region, stage_id_to_region, region_name_for_character

def GetRelevantTokenItem(token: LocationInfo):
    level_token_items = GetLevelTokenItems()

    if token.other == ITEM_TOKEN_TYPE_FINAL:
        level_token_items = [ t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_FINAL ]
    elif token.other == ITEM_TOKEN_TYPE_OBJECTIVE:
        level_token_items = [ t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_OBJECTIVE ]
    elif token.other == ITEM_TOKEN_TYPE_STANDARD:
        level_token_items = [t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_STANDARD]
    elif token.other == ITEM_TOKEN_TYPE_ALIGNMENT:
        level_token_items = [t for t in level_token_items if t.value == ITEM_TOKEN_TYPE_ALIGNMENT]
        if token.alignmentId == MISSION_ALIGNMENT_DARK:
            level_token_items = [ t for t in level_token_items if t.alignmentId == MISSION_ALIGNMENT_DARK]
        elif token.alignmentId == MISSION_ALIGNMENT_HERO:
            level_token_items = [ t for t in level_token_items if t.alignmentId == MISSION_ALIGNMENT_HERO]

    if len(level_token_items) == 0:
        return None

    return level_token_items[0]

def set_rules(multiworld: MultiWorld, world: World, player: int):

    token_assignments = {}

    for clear in MissionClearLocations:

        if LEVEL_ID_TO_LEVEL[clear.stageId] in world.options.excluded_stages:
            continue

        id, name = Levels.GetLevelCompletionNames(clear.stageId, clear.alignmentId)
        try:
            rule = None
            if clear.requirement_count != 1:
                location = multiworld.get_location(name, player)
                item_name = Items.GetStageAlignmentObject(clear.stageId, clear.alignmentId)
                if world.options.objective_sanity:
                    percentage = world.options.objective_item_percentage.value
                    required_count = ceil(clear.requirement_count * percentage / 100)
                    rule = lambda state, itemname=item_name, count=required_count: state.has(itemname, player, count=count)
                    add_rule(location, rule)


            associated_tokens = [t for t in world.token_locations if
                                 t.alignmentId == clear.alignmentId and
                                 t.stageId == clear.stageId]
            for token in associated_tokens:
                location = multiworld.get_location(token.name, player)
                if rule:
                    add_rule(location, rule)
                allocated_item = GetRelevantTokenItem(token)
                if allocated_item is None:
                    print("Could not resolve:", token)
                    continue
                if allocated_item.name not in token_assignments:
                    token_assignments[allocated_item.name] = []
                token_assignments[allocated_item.name].append(location)
                mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
                location.place_locked_item(
                    mw_token_item)

        except KeyError:
            # Do nothing for mission locations that do not exist
            pass

    for character,stages in CharacterToLevel.items():
        if character in world.available_characters:
            region_name = character_name_to_region(character)
            region = world.get_region(region_name)
            for stage in stages:
                if LEVEL_ID_TO_LEVEL[stage] in world.options.excluded_stages:
                    continue
                region_stage = world.get_region(stage_id_to_region(stage))
                region_stage.connect(region, region_name_for_character(LEVEL_ID_TO_LEVEL[stage], character))


    e = multiworld.get_entrance("final-story-unlock", player)
    goal_has = []
    item_dict = Items.GetItemDict()
    if world.options.goal_chaos_emeralds:
        emeralds = Items.GetEmeraldItems()
        goal_has.extend([ (ce.name,1) for ce in emeralds ])
    if world.options.goal_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardMissionToken, token_assignments, world.options.goal_missions)
        goal_has.append(tokens)
    if world.options.goal_hero_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardHeroToken, token_assignments, world.options.goal_hero_missions)
        goal_has.append(tokens)
    if world.options.goal_dark_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardDarkToken, token_assignments, world.options.goal_dark_missions)
        goal_has.append(tokens)
    if world.options.goal_final_missions > 0:
        tokens = get_token_count(world, Items.Progression.FinalToken, token_assignments, world.options.goal_final_missions)
        goal_has.append(tokens)
    if world.options.goal_objective_missions > 0:
        tokens = get_token_count(world, Items.Progression.ObjectiveToken, token_assignments, world.options.goal_objective_missions)
        goal_has.append(tokens)

    e.access_rule = lambda state, g_has=goal_has: len([ x for x in g_has if state.has(x[0], player, count=x[1]) ]) == len(g_has)


        #e.access_rule = lambda state, : state.has(, player) and state.has(emeralds[1].name, player) \
        #        and state.has(emeralds[2].name, player) and state.has(emeralds[3].name, player) \
        #        and state.has(emeralds[4].name, player) and state.has(emeralds[5].name, player) \
        #        and state.has(emeralds[6].name, player)
    #if world.options.goal_missions:
    #    e.access_rule = lambda state: state.has(emeralds[0].name, player)


    final_item = Items.GetFinalItem()
    mw_final_item = ShadowTheHedgehogItem(final_item, world.player)
    multiworld.get_location(Levels.DevilDoom_Name, world.player).place_locked_item(
        mw_final_item)

    multiworld.completion_condition[player] = lambda state: state.has(Items.Progression.GoodbyeForever, player)


def get_token_count(world, type, token_assignments, goal_value):
    count = len(token_assignments[type])
    goal_req = ceil(count * goal_value / 100)
    world.required_tokens[type] = goal_req
    return (type, goal_req)